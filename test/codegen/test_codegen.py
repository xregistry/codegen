import platform
import re
import json
import xrcg
import random
import string
import sys
import os
import subprocess
import shutil
import time
import tempfile
import xml.etree.ElementTree as ET

import pytest
from xrcg.generator.generator_context import GeneratorContext
from xrcg.generator.template_renderer import TemplateRenderer
from xrcg.generator.schema_utils import SchemaUtils
from xrcg.generator.xregistry_loader import SchemaReference

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(project_root))

def pascal(string: str) -> str:
    """Convert a string to PascalCase."""
    if not string or len(string) == 0:
        return string
    words = []
    if '_' in string:
        words = re.split(r'_', string)
    elif string[0].isupper():
        words = re.findall(r'[A-Z][a-z0-9_]*\.?', string)
    else:
        words = re.findall(r'[a-z0-9]+\.?|[A-Z][a-z0-9_]*\.?', string)
    return ''.join(word.capitalize() for word in words)

def test_codegen_cs():
    """    
    This does a basic test of the code generation for all the styles in the cs template.    
    """
    input_dir = os.path.join(
        project_root, 'xrcg/templates/cs'.replace('/', os.path.sep))
    # loop through all dirs in the input directory that have no leading underscore in their name
    for dir_name in os.listdir(input_dir):
        print(f'Processing {dir_name}')
        try:
            if os.path.exists(os.path.join(tempfile.gettempdir(), f'tmp/test/cs/{dir_name}/'.replace('/', os.path.sep))):
                shutil.rmtree(os.path.join(
                    tempfile.gettempdir(), f'tmp/test/cs/{dir_name}/'.replace('/', os.path.sep)), ignore_errors=True)
            output_dir = os.path.join(
                tempfile.gettempdir(), f'tmp/test/cs/{dir_name}'.replace('/', os.path.sep))
            if not dir_name.startswith('_') and os.path.isdir(os.path.join(input_dir, dir_name)):
                # generate the code for each directory
                sys.argv = ['xrcg', 'generate',
                            '--style', dir_name,
                            '--language', 'cs',
                            '--definitions', os.path.join(
                                project_root, 'test/xreg/contoso-erp.xreg.json'.replace('/', os.path.sep)),
                            '--output', output_dir,
                            '--projectname', f'Test.{pascal(dir_name)}']
                assert xrcg.cli() == 0
                # run dotnet build on the solution file in the output directory
                cmd = ['dotnet', 'build'] if platform.system() == "Windows" else 'dotnet build'
                assert subprocess.check_call(cmd, cwd=output_dir, shell=True) == 0
        except Exception as e:
            print(f'Error processing {dir_name}: {e}')
            raise e

# @pytest.mark.skip(reason="temporarily disabled")


def test_codegen_py():
    input_dir = os.path.join(
        project_root, 'xrcg/templates/py'.replace('/', os.path.sep))
    # loop through all dirs in the input directory that have no leading underscore in their name
    for dir_name in os.listdir(input_dir):
        if os.path.exists(os.path.join(tempfile.gettempdir(), f'tmp/test/py/{dir_name}/'.replace('/', os.path.sep))):
            shutil.rmtree(os.path.join(
                tempfile.gettempdir(), f'tmp/test/py/{dir_name}/'.replace('/', os.path.sep)), ignore_errors=True)
        output_dir = os.path.join(
            tempfile.gettempdir(), f'tmp/test/py/{dir_name}'.replace('/', os.path.sep))
        if not dir_name.startswith('_') and os.path.isdir(os.path.join(input_dir, dir_name)):
            # generate the code for each directory
            sys.argv = ['xrcg', 'generate',
                        '--style', dir_name,
                        '--language', 'py',
                        '--definitions', os.path.join(
                            project_root, 'samples/message-definitions/contoso-erp.xreg.json'.replace('/', os.path.sep)),
                        '--output', output_dir,
                        '--projectname', f'test_build_{dir_name}']
            assert xrcg.cli() == 0


@pytest.mark.parametrize('template_name', ['amqpconsumer', 'amqpproducer', 'kafkaproducer'])
def test_codegen_java(template_name):
    """Test Java code generation for production-ready templates."""
    # check whether maven is installed
    try:
        result = subprocess.run("mvn -v", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        if result.returncode != 0:
            pytest.skip('Maven is not installed')
    except Exception:
        pytest.skip('Maven is not installed')

    output_dir = os.path.join(project_root, f'tmp/test/java/{template_name}')
    
    # Clean output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)
    
    # Generate code
    sys.argv = ['xrcg', 'generate',
                '--style', template_name,
                '--language', 'java',
                '--definitions', os.path.join(project_root, 'test/java/contoso-erp-java.xreg.json'),
                '--output', output_dir,
                '--projectname', f'test.{template_name}']
    assert xrcg.cli() == 0
    
    # Find generated directories
    subdirs = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]
    
    # Find data and main project directories
    data_dir = None
    main_dir = None
    for subdir in subdirs:
        if 'data' in subdir.lower():
            data_dir = os.path.join(output_dir, subdir)
        else:
            main_dir = os.path.join(output_dir, subdir)
    
    assert main_dir is not None, f"Could not find main project directory in {output_dir}"
    
    # Build data project first if it exists (with timeout to prevent hanging)
    if data_dir and os.path.exists(os.path.join(data_dir, 'pom.xml')):
        result = subprocess.run("mvn install -B", cwd=data_dir, shell=True, timeout=300)
        assert result.returncode == 0, "Data project build failed"
    
    # Build main project (with timeout to prevent hanging)
    assert os.path.exists(os.path.join(main_dir, 'pom.xml')), f"No pom.xml found in {main_dir}"
    result = subprocess.run("mvn package -B", cwd=main_dir, shell=True, timeout=300)
    assert result.returncode == 0, "Main project build failed"


def test_codegen_java_kafka_inkjet_proto_generates():
    """Regression test for Protobuf conversion with multiple nested enums."""
    output_dir = os.path.join(project_root, 'tmp/test/java/kafkaproducer-inkjet-proto')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    sys.argv = ['xrcg', 'generate',
                '--style', 'kafkaproducer',
                '--language', 'java',
                '--definitions', os.path.join(project_root, 'samples/message-definitions/inkjet-proto.xreg.json'),
                '--output', output_dir,
                '--projectname', 'JavaKafkaInkjetProto']
    assert xrcg.cli() == 0


def test_codegen_py_kafkaproducer_basemessageuri():
    """Regression test: kafkaproducer (py) must generate without error when
    Kafka overlay messages use the canonical ``basemessageuri`` attribute
    (instead of ``basemessageurl``) and ``protocoloptions.key`` (instead of
    ``protocolmetadata.key.value``) to specify the Kafka partition key.

    This reproduces the bug reported in
    https://github.com/xregistry/codegen/issues/362 where Jinja rendering
    failed with:
      UndefinedError: 'dict object' has no attribute 'envelopemetadata'
    """
    output_dir = os.path.join(
        tempfile.gettempdir(),
        'tmp/test/py/kafkaproducer-basemessageuri'.replace('/', os.path.sep))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    sys.argv = ['xrcg', 'generate',
                '--style', 'kafkaproducer',
                '--language', 'py',
                '--definitions', os.path.join(
                    project_root,
                    'test/xreg/inkjet-kafka-basemessageuri.xreg.json'.replace('/', os.path.sep)),
                '--output', output_dir,
                '--projectname', 'test_kafkaproducer_basemessageuri']
    assert xrcg.cli() == 0


def test_codegen_py_kafkaproducer_keeps_jstruct_exports_with_unused_avro_schemas():
    """Regression test for issue #371.

    Full-document generation must not treat inline schema bodies under
    ``schemagroups`` as additional top-level schema references. Doing so makes
    the Python data package process alternate schema encodings twice and can
    overwrite ``__init__.py`` exports for JsonStructure-only types.
    """
    work_dir = tempfile.mkdtemp()
    try:
        definitions_path = os.path.join(work_dir, 'issue-371.xreg.json')
        output_dir = os.path.join(work_dir, 'out')

        document = {
            "specversion": "1.0-rc2",
            "endpoints": {
                "Test.Reference.Kafka": {
                    "usage": ["producer"],
                    "protocol": "KAFKA",
                    "envelope": "CloudEvents/1.0",
                    "envelopeoptions": {
                        "mode": "structured",
                        "format": "application/cloudevents+json"
                    },
                    "protocoloptions": {
                        "options": {
                            "topic": "issue-371",
                            "key": "{entity_id}"
                        }
                    },
                    "messagegroups": [
                        "#/messagegroups/Test.Reference"
                    ]
                }
            },
            "messagegroups": {
                "Test.Reference": {
                    "messages": {
                        "Test.Reference.Info": {
                            "name": "Info",
                            "envelope": "CloudEvents/1.0",
                            "description": "Referenced JsonStructure message.",
                            "envelopemetadata": {
                                "type": {"value": "Test.Reference.Info"},
                                "source": {
                                    "value": "https://example.test/issue-371",
                                    "type": "uritemplate"
                                },
                                "subject": {
                                    "value": "{entity_id}",
                                    "type": "uritemplate"
                                }
                            },
                            "dataschemaformat": "JsonStructure/draft-02",
                            "dataschemauri": "#/schemagroups/Test.jstruct/schemas/Test.Reference.Info"
                        }
                    }
                }
            },
            "schemagroups": {
                "Test.jstruct": {
                    "schemas": {
                        "Test.Reference.Info": {
                            "defaultversionid": "v1",
                            "versions": {
                                "v1": {
                                    "schemaid": "Test.Reference.Info",
                                    "format": "JsonStructure/draft-02",
                                    "schema": {
                                        "$schema": "https://json-structure.org/meta/core/v0/#",
                                        "name": "Info",
                                        "type": "object",
                                        "description": "JsonStructure-only reference data type.",
                                        "properties": {
                                            "entity_id": {
                                                "type": "string",
                                                "description": "Stable identifier."
                                            },
                                            "name": {
                                                "type": "string",
                                                "description": "Display name."
                                            }
                                        },
                                        "required": ["entity_id", "name"]
                                    }
                                }
                            }
                        }
                    }
                },
                "Test.avro": {
                    "schemas": {
                        "Test.Reference.Unused": {
                            "defaultversionid": "v1",
                            "versions": {
                                "v1": {
                                    "schemaid": "Test.Reference.Unused",
                                    "format": "Avro/1.11.3",
                                    "schema": {
                                        "type": "record",
                                        "name": "Unused",
                                        "namespace": "Test.Reference",
                                        "doc": "Unreferenced alternate schema format.",
                                        "fields": [
                                            {
                                                "name": "entity_id",
                                                "type": "string",
                                                "doc": "Stable identifier."
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        with open(definitions_path, 'w', encoding='utf-8') as handle:
            json.dump(document, handle, indent=2)

        sys.argv = [
            'xrcg', 'generate',
            '--style', 'kafkaproducer',
            '--language', 'py',
            '--definitions', definitions_path,
            '--output', output_dir,
            '--projectname', 'test_issue_371'
        ]
        assert xrcg.cli() == 0

        init_path = os.path.join(
            output_dir,
            'test_issue_371_data',
            'src',
            'test_issue_371_data',
            '__init__.py'
        )
        with open(init_path, 'r', encoding='utf-8') as handle:
            init_contents = handle.read()

        producer_path = os.path.join(
            output_dir,
            'test_issue_371_kafka_producer',
            'src',
            'test_issue_371_kafka_producer',
            'producer.py'
        )
        with open(producer_path, 'r', encoding='utf-8') as handle:
            producer_contents = handle.read()

        assert 'from .info import Info' in init_contents
        assert '"Info"' in init_contents
        assert 'from test_issue_371_data import Info' in producer_contents
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def test_codegen_py_xsd_emits_xml_serialization():
    """XSD schemas are converted to Avro and emitted with XML serialization.

    When a message references an ``XSD`` schema (typically paired with a
    ``datacontenttype`` of ``application/xml``), codegen must convert the XSD
    to Avro via avrotize and enable XML annotations on the generated data
    classes so the runtime ``to_byte_array`` / ``from_data`` handle
    ``application/xml``.
    """
    output_dir = os.path.join(
        tempfile.gettempdir(),
        'tmp/test/py/xsd-amqpproducer'.replace('/', os.path.sep))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    sys.argv = [
        'xrcg', 'generate',
        '--style', 'amqpproducer',
        '--language', 'py',
        '--definitions', os.path.join(
            project_root,
            'samples/message-definitions/minimal-xsd.xreg.json'.replace('/', os.path.sep)),
        '--output', output_dir,
        '--projectname', 'test_xsd'
    ]
    assert xrcg.cli() == 0

    person_path = os.path.join(
        output_dir, 'test_xsd_data', 'src', 'test_xsd_data',
        'com', 'example', 'grp1', 'person.py')
    assert os.path.exists(person_path), f"Expected data class not generated: {person_path}"
    with open(person_path, 'r', encoding='utf-8') as handle:
        person_contents = handle.read()
    assert 'application/xml' in person_contents
    assert 'def to_byte_array' in person_contents
    assert 'def from_data' in person_contents

    # The XML runtime helper module must be emitted alongside the data class.
    xml_runtime_path = os.path.join(
        output_dir, 'test_xsd_data', 'src', 'test_xsd_data', 'xml_runtime.py')
    assert os.path.exists(xml_runtime_path), "xml_runtime.py was not generated for XSD/XML data"

    # Generated data class must import cleanly.
    import py_compile
    py_compile.compile(person_path, doraise=True)

    data_src = os.path.join(output_dir, 'test_xsd_data', 'src')
    sys.path.insert(0, data_src)
    try:
        from test_xsd_data.com.example.grp1.person import Person

        person = Person(name='Ada', age=37, id='person-1')
        xml_bytes = person.to_byte_array('application/xml')
        assert isinstance(xml_bytes, bytes)
        root = ET.fromstring(xml_bytes)
        assert root.tag.rsplit('}', 1)[-1] == 'Person'
        assert root.attrib['id'] == 'person-1'
        children = {child.tag.rsplit('}', 1)[-1]: child.text for child in root}
        assert children == {'name': 'Ada', 'age': '37'}

        round_tripped = Person.from_data(xml_bytes, 'application/xml')
        assert round_tripped == person
    finally:
        sys.path.remove(data_src)
        for module_name in list(sys.modules):
            if module_name == 'test_xsd_data' or module_name.startswith('test_xsd_data.'):
                del sys.modules[module_name]


@pytest.mark.parametrize('language,style,xml_marker', [
    ('cs', 'amqpproducer', 'Xml'),
    ('java', 'amqpproducer', 'Xml'),
    ('ts', 'amqpproducer', 'xml'),
    ('go', 'amqpproducer', 'xml:"'),
    ('rust', 'producer', 'rename'),
])
def test_codegen_xsd_generates_xml_annotations(language, style, xml_marker):
    """XSD/XML generation succeeds and emits XML metadata for every language.

    Regression guard: previously XSD schemas were silently dropped (empty data
    classes) and the Go emitter crashed. With avrotize XML support wired in,
    each language must generate without error and produce XML-aware types.
    """
    output_dir = os.path.join(
        tempfile.gettempdir(),
        f'tmp/test/{language}/xsd-{style}'.replace('/', os.path.sep))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    sys.argv = [
        'xrcg', 'generate',
        '--style', style,
        '--language', language,
        '--definitions', os.path.join(
            project_root,
            'samples/message-definitions/minimal-xsd.xreg.json'.replace('/', os.path.sep)),
        '--output', output_dir,
        '--projectname', 'test_xsd'
    ]
    assert xrcg.cli() == 0

    source_exts = {'.cs', '.java', '.ts', '.go', '.rs'}
    found_xml = False
    for root, _dirs, files in os.walk(output_dir):
        for fn in files:
            if os.path.splitext(fn)[1] in source_exts:
                with open(os.path.join(root, fn), 'r', encoding='utf-8', errors='ignore') as handle:
                    if xml_marker in handle.read():
                        found_xml = True
                        break
        if found_xml:
            break
    assert found_xml, f"No XML annotations found in generated {language} sources"


def _producer_sources(output_dir, projectname):
    """Yield generated *producer* (main-project) source paths, excluding the
    avrotize data project (whose data classes always contain XML support and
    would mask what the producer itself defaults to)."""
    data_marker = projectname.lower().replace('_', '') + 'data'
    exts = {'.cs', '.java', '.ts', '.go', '.rs', '.py'}
    for root, _dirs, files in os.walk(output_dir):
        relative_root = os.path.relpath(root, output_dir)
        segs = [s.lower().replace('_', '') for s in relative_root.split(os.sep)]
        if data_marker in segs or any(seg in ('test', 'tests') for seg in segs):
            continue
        for fn in files:
            if os.path.splitext(fn)[1] in exts:
                yield os.path.join(root, fn)


def _generate_producer(language, style, sample, projectname, subdir):
    output_dir = os.path.join(
        tempfile.gettempdir(),
        f'tmp/test/{language}/ct-{subdir}'.replace('/', os.path.sep))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)
    definitions_path = sample if os.path.isabs(sample) else os.path.join(
        project_root,
        f'samples/message-definitions/{sample}'.replace('/', os.path.sep))
    sys.argv = [
        'xrcg', 'generate',
        '--style', style,
        '--language', language,
        '--definitions', definitions_path,
        '--output', output_dir,
        '--projectname', projectname,
    ]
    assert xrcg.cli() == 0
    return output_dir


def _versioned_schema_document():
    schema = {
        "versionid": "stable",
        "format": "Avro/1.11.0",
        "schema": {
            "type": "record", "name": "Reading", "namespace": "Example",
            "fields": [{"name": "value", "type": "string"}],
        },
    }
    return {
        "messagegroups": {
            "Example": {
                "messagegroupid": "Example",
                "messages": {
                    "Reading": {
                        "messageid": "Reading",
                        "envelope": "CloudEvents/1.0",
                        "dataschemaformat": "Avro/1.11.0",
                        "dataschemauri": "#/schemagroups/Example/schemas/Reading",
                        "envelopemetadata": {
                            "type": {"type": "string", "value": "Example.Reading"},
                            "source": {"type": "uri", "value": "urn:readings"},
                        },
                    },
                },
            },
        },
        "schemagroups": {
            "Example": {
                "schemagroupid": "Example",
                "schemas": {
                    "Reading": {
                        "schemaid": "Reading", "defaultversionid": "stable",
                        "versions": {
                            "stable": schema,
                            "zzz": {**schema, "versionid": "zzz"},
                        },
                    },
                },
            },
        },
    }


@pytest.mark.parametrize("origin,reference,expected", [
    ("catalog.json", "#/schemagroups/Example/schemas/Reading",
     "xreg://./schemagroups/Example/schemas/Reading/versions/stable"),
    ("catalog.json", "#/schemagroups/Example/schemas/Reading/versions/zzz",
     "xreg://./schemagroups/Example/schemas/Reading/versions/zzz"),
    ("catalog.json", "#/schemagroups/Example/schemas/Reading:Example.Reading",
     "xreg://./schemagroups/Example/schemas/Reading/versions/stable"),
    ("https://api.example/tenant/registry", "#/schemagroups/Example/schemas/Reading",
     "https://api.example/tenant/registry/schemagroups/Example/schemas/Reading/versions/stable"),
    ("https://api.example/tenant/registry/messagegroups/Example/messages/Reading",
     "/schemagroups/Example/schemas/Reading",
     "https://api.example/tenant/registry/schemagroups/Example/schemas/Reading/versions/stable"),
    ("https://api.example/tenant/registry/messagegroups/Example/messages/Reading",
     "../../../schemagroups/Example/schemas/Reading",
     "https://api.example/tenant/registry/schemagroups/Example/schemas/Reading/versions/stable"),
])
def test_versioned_dataschema_resolution(origin, reference, expected):
    document = _versioned_schema_document()
    message = document["messagegroups"]["Example"]["messages"]["Reading"]
    message["dataschemauri"] = SchemaReference(reference, origin)
    ctx = GeneratorContext()
    ctx.base_uri = origin
    SchemaUtils.project_schema_references(ctx, document)
    assert message["envelopemetadata"]["dataschema"]["value"] == expected


def test_versioned_dataschema_does_not_add_envelope_to_plain_message():
    document = _versioned_schema_document()
    message = document["messagegroups"]["Example"]["messages"]["Reading"]
    message.pop("envelope")
    message.pop("envelopemetadata")
    message["protocol"] = "AMQP/1.0"
    ctx = GeneratorContext()
    ctx.base_uri = "catalog.json"
    SchemaUtils.project_schema_references(ctx, document)
    assert "envelopemetadata" not in message


def test_versioned_dataschema_override_and_unresolved_reference():
    document = _versioned_schema_document()
    message = document["messagegroups"]["Example"]["messages"]["Reading"]
    message["envelopemetadata"]["dataschema"] = {
        "type": "uri", "value": "https://registered.example/avro/versions/17"}
    ctx = GeneratorContext()
    ctx.base_uri = "catalog.json"
    SchemaUtils.project_schema_references(ctx, document)
    assert message["envelopemetadata"]["dataschema"]["value"] == (
        "https://registered.example/avro/versions/17")
    message["dataschemauri"] += "/versions/missing"
    with pytest.raises(RuntimeError, match=r"message /messagegroups/Example/messages/Reading: .*missing"):
        SchemaUtils.project_schema_references(ctx, document)


@pytest.mark.parametrize("selection", ["meta", "defaultversionurl", "version-body"])
def test_versioned_dataschema_default_selection(selection):
    document = _versioned_schema_document()
    schemas = document["schemagroups"]["Example"]["schemas"]
    resource = schemas["Reading"]
    resource.pop("defaultversionid")
    if selection == "version-body":
        schemas["Reading"] = resource["versions"]["stable"]
    elif selection == "meta":
        resource["meta"] = {"defaultversionid": "stable"}
    else:
        resource["defaultversionurl"] = "https://api.example/schemas/Reading/versions/stable?api-version=1"
    ctx = GeneratorContext()
    ctx.base_uri = "catalog.json"
    SchemaUtils.project_schema_references(ctx, document)
    message = document["messagegroups"]["Example"]["messages"]["Reading"]
    assert message["envelopemetadata"]["dataschema"]["value"] == (
        "xreg://./schemagroups/Example/schemas/Reading/versions/stable")


@pytest.mark.parametrize("reference", [
    "schemas.xreg.json#/schemagroups/Example/schemas/Reading",
    "absolute-file",
    "file-uri",
    "https://schemas.example/registry/schemagroups/Example/schemas/Reading",
    "https://schemas.example/registry/schemagroups/Example/schemas/Reading?api-version=1",
])
def test_versioned_dataschema_external_origin(reference, tmp_path, monkeypatch):
    if reference in ("absolute-file", "file-uri"):
        path = tmp_path / "schemas.xreg.json"
        reference = (path.as_uri() if reference == "file-uri" else str(path)) + (
            "#/schemagroups/Example/schemas/Reading")
    document = _versioned_schema_document()
    message = document["messagegroups"]["Example"]["messages"]["Reading"]
    message["dataschemauri"] = SchemaReference(reference, str(tmp_path / "catalog.json"))
    external = document if "#" in reference else document["schemagroups"]["Example"]["schemas"]["Reading"]
    ctx = GeneratorContext()
    monkeypatch.setattr(ctx.loader, "_load_core", lambda *args, **kwargs: (args[0], external))
    SchemaUtils.project_schema_references(ctx, document)
    expected = (reference if reference.startswith("https:") else
                "schemas.xreg.json#/schemagroups/Example/schemas/Reading")
    expected = expected.replace("?api-version=1", "") + "/versions/stable"
    if "?" in reference:
        expected += "?api-version=1"
    if not expected.startswith("https:"):
        expected = "xreg://./" + expected
    assert message["envelopemetadata"]["dataschema"]["value"] == expected


@pytest.mark.parametrize("api", [False, True])
def test_versioned_dataschema_escaped_version(api):
    document = _versioned_schema_document()
    resource = document["schemagroups"]["Example"]["schemas"]["Reading"]
    resource["defaultversionid"] = "release/1~b"
    resource["versions"]["release/1~b"] = {
        **resource["versions"]["stable"], "versionid": "release/1~b"}
    ctx = GeneratorContext()
    ctx.base_uri = "https://api.example/registry" if api else "catalog.json"
    SchemaUtils.project_schema_references(ctx, document)
    value = document["messagegroups"]["Example"]["messages"]["Reading"]["envelopemetadata"]["dataschema"]["value"]
    assert value.endswith("/versions/release%2F1~b")


def test_versioned_dataschema_stacked_inheritance(tmp_path):
    document = _versioned_schema_document()
    base_dir = tmp_path / "contracts"
    base_dir.mkdir()
    base = base_dir / "catalog.json"
    external = base_dir / "schemas.xreg.json"
    external.write_text(json.dumps({"schemagroups": document.pop("schemagroups")}), encoding="utf-8")
    document["messagegroups"]["Example"]["messages"]["Reading"]["dataschemauri"] = (
        "schemas.xreg.json#/schemagroups/Example/schemas/Reading")
    base.write_text(json.dumps(document), encoding="utf-8")
    overlay = tmp_path / "overlay.json"
    overlay.write_text(json.dumps({
        "messagegroups": {"Transport": {"messages": {
            "Reading": {"basemessageuri": "#/messagegroups/Example/messages/Reading"},
        }}},
    }), encoding="utf-8")
    ctx = GeneratorContext()
    ctx.base_uri = str(base)
    _, loaded = ctx.loader.load_stacked([str(base), str(overlay)], {})
    assert loaded is not None
    SchemaUtils.project_schema_references(ctx, loaded)
    message = loaded["messagegroups"]["Transport"]["messages"]["Reading"]
    assert message["envelopemetadata"]["dataschema"]["value"] == (
        "xreg://./schemas.xreg.json#/schemagroups/Example/schemas/Reading/versions/stable")


@pytest.mark.parametrize("entry,reference", [
    ("", "#/schemagroups/Example/schemas/Reading"),
    ("/messagegroups/Example", "#/schemagroups/Example/schemas/Reading"),
    ("/messagegroups/Example", "/schemagroups/Example/schemas/Reading"),
    ("/messagegroups/Example", "schemagroups/Example/schemas/Reading"),
    ("/messagegroups/Example", "../../../schemagroups/Example/schemas/Reading"),
])
def test_versioned_dataschema_api_input(entry, reference, monkeypatch):
    import io
    import urllib.error
    import urllib.parse
    import urllib.request

    document = _versioned_schema_document()
    base = "https://api.example/tenant/registry"
    message = document["messagegroups"]["Example"]["messages"]["Reading"]
    message["dataschemauri"] = reference
    message["self"] = base + "/messagegroups/Example/messages/Reading"
    responses = {
        base: document,
        base + "/capabilities": {},
        base + "/messagegroups/Example": document["messagegroups"]["Example"],
        base + "/schemagroups/Example/schemas/Reading": document["schemagroups"]["Example"]["schemas"]["Reading"],
    }

    def open_request(request):
        url = request.full_url.split("?", 1)[0]
        if url not in responses:
            raise urllib.error.HTTPError(url, 404, "Not found", {}, None)
        return io.BytesIO(json.dumps(responses[url]).encode("utf-8"))

    ctx = GeneratorContext()
    ctx.base_uri = base + entry
    monkeypatch.setattr(urllib.request, "urlopen", open_request)
    _, loaded = ctx.loader.load_with_dependencies(base + entry, {})
    assert loaded is not None
    SchemaUtils.project_schema_references(ctx, loaded)
    effective = loaded["messagegroups"]["Example"]["messages"]["Reading"]
    assert effective["envelopemetadata"]["dataschema"]["value"] == (
        base + "/schemagroups/Example/schemas/Reading/versions/stable")
    assert SchemaUtils.schema_type(
        ctx, effective["dataschemauri"], "Generated", loaded, "Avro/1.11.0"
    ) == "Generated.Example.Reading"


@pytest.mark.parametrize("language,style", [
    ("cs", "amqpproducer"), ("cs", "kafkaproducer"),
    ("cs", "ehproducer"), ("cs", "sbproducer"), ("cs", "egproducer"), ("cs", "mqttclient"),
    ("java", "producer"), ("java", "amqpproducer"), ("java", "amqpjmsproducer"), ("java", "kafkaproducer"),
    ("java", "ehproducer"), ("java", "sbproducer"), ("java", "mqttclient"),
    ("py", "producer"), ("py", "amqpproducer"), ("py", "kafkaproducer"), ("py", "ehproducer"),
    ("py", "sbproducer"), ("py", "mqttclient"),
    ("ts", "producerhttp"), ("ts", "amqpproducer"), ("ts", "kafkaproducer"),
    ("ts", "ehproducer"), ("ts", "sbproducer"), ("ts", "egproducer"), ("ts", "mqttclient"),
    ("go", "producer"), ("go", "amqpproducer"), ("go", "kafkaproducer"),
    ("go", "ehproducer"), ("go", "sbproducer"), ("go", "mqttclient"),
    ("rust", "producer"),
    ("asyncapi", "producer"), ("asyncapi", "consumer"),
    ("openapi", "producer"), ("openapi", "subscriber"),
])
def test_codegen_producer_versioned_dataschema(language, style, tmp_path, monkeypatch, caplog):
    import copy

    document = _versioned_schema_document()
    messages = document["messagegroups"]["Example"]["messages"]
    messages["Override"] = copy.deepcopy(messages["Reading"])
    messages["Override"]["messageid"] = "Override"
    messages["Override"]["envelopemetadata"]["type"]["value"] = "Example.Override"
    messages["Override"]["envelopemetadata"]["dataschema"] = {
        "type": "uri", "value": "https://registered.example/avro/versions/17"}
    is_specification = language in ("asyncapi", "openapi")
    if not is_specification:
        messages["Pinned"] = copy.deepcopy(messages["Reading"])
        messages["Pinned"]["messageid"] = "Pinned"
        messages["Pinned"]["envelopemetadata"]["type"]["value"] = "Example.Pinned"
        messages["Pinned"]["dataschemauri"] += "/versions/zzz"
    document["endpoints"] = {
        "http": {
            "endpointid": "http", "protocol": "HTTP/1.1",
            "usage": ["producer"], "messagegroups": ["#/messagegroups/Example"],
            "config": {"uri": "https://events.example/"},
        },
    }
    definitions = tmp_path / "catalog.json"
    definitions.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", [
        "xrcg", "generate", "--language", language, "--style", style,
        "--definitions", str(definitions), "--output", str(output),
        "--projectname", "SchemaContract",
    ])
    assert xrcg.cli() == 0
    assert not [record.message for record in caplog.records if record.levelno >= 40]
    paths = (output.rglob("*.yml") if is_specification else
             _producer_sources(str(output), "SchemaContract"))
    sources = "\n".join(open(path, encoding="utf-8").read() for path in paths)
    assert "xreg://./schemagroups/Example/schemas/Reading/versions/stable" in sources
    if not is_specification:
        assert "xreg://./schemagroups/Example/schemas/Reading/versions/zzz" in sources
    assert "https://registered.example/avro/versions/17" in sources
    assert "xreg:schemagroups" not in sources
    assert str(tmp_path) not in sources
    if language == "go":
        assert 'SetExtension("dataschema"' not in sources
        assert "event.SetDataSchema(" in sources
    if language == "py":
        import py_compile
        for path in output.rglob("*.py"):
            py_compile.compile(str(path), doraise=True)
    if not is_specification:
        override_name = "dataschema_overrides" if language in ("py", "rust") else "dataschemaOverrides"
        assert override_name in sources


@pytest.mark.parametrize("pinned", [False, True])
def test_codegen_dataschema_matches_generated_payload_version(pinned, tmp_path, monkeypatch):
    import copy
    import runpy

    document = _versioned_schema_document()
    versions = document["schemagroups"]["Example"]["schemas"]["Reading"]["versions"]
    versions["zzz"] = copy.deepcopy(versions["zzz"])
    versions["stable"]["schema"]["fields"][0]["name"] = "stable_value"
    versions["zzz"]["schema"]["fields"][0]["name"] = "pinned_value"
    if pinned:
        document["messagegroups"]["Example"]["messages"]["Reading"]["dataschemauri"] += "/versions/zzz"
    definitions = tmp_path / "catalog.json"
    definitions.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", [
        "xrcg", "generate", "--language", "py", "--style", "amqpproducer",
        "--definitions", str(definitions), "--output", str(output),
        "--projectname", "VersionContract",
    ])
    assert xrcg.cli() == 0
    generated = runpy.run_path(str(next(output.rglob("reading.py"))))
    assert [field.name for field in generated["Reading"].AvroType.fields] == (
        ["pinned_value"] if pinned else ["stable_value"])
    source = next(output.rglob("producer.py")).read_text(encoding="utf-8")
    assert ("/versions/zzz" if pinned else "/versions/stable") in source


@pytest.mark.parametrize("topic_key", ["topic_name", "topic-name", "topic"])
def test_codegen_py_mqtt_tests_cover_topic_and_envelope_variables(topic_key, tmp_path, monkeypatch):
    import ast
    import py_compile

    document = _versioned_schema_document()
    message = document["messagegroups"]["Example"]["messages"]["Reading"]
    message["envelopemetadata"]["source"] = {
        "type": "uritemplate", "value": "https://example.test/{station_id}",
    }
    message["envelopemetadata"]["subject"] = {"type": "uritemplate", "value": "{station_id}"}
    message["protocoloptions"] = {topic_key: "hydro/{water_shortname}/{station_id}/{station_id}"}
    definitions = tmp_path / "catalog.json"
    definitions.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", [
        "xrcg", "generate", "--language", "py", "--style", "mqttclient",
        "--definitions", str(definitions), "--output", str(output), "--projectname", "TopicContract",
    ])
    assert xrcg.cli() == 0
    for source in output.rglob("*.py"):
        py_compile.compile(str(source), doraise=True)
    generated = ast.parse(next(output.rglob("test_client.py")).read_text(encoding="utf-8"))
    calls = [node for node in ast.walk(generated)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
             and node.func.attr.startswith("publish_")]
    assert len(calls) == 1
    names = [keyword.arg for keyword in calls[0].keywords]
    assert names.count("station_id") == 1
    assert names.count("water_shortname") == 1
    assert "_time" in names


def test_codegen_py_kafka_cross_event_test_uses_inherited_wire_types(tmp_path, monkeypatch):
    import ast
    import copy
    import py_compile

    document = _versioned_schema_document()
    messages = document["messagegroups"]["Example"]["messages"]
    messages["Reading"]["envelopemetadata"]["subject"] = {
        "type": "uritemplate", "value": "{station_id}",
    }
    messages["Other"] = copy.deepcopy(messages["Reading"])
    messages["Other"]["envelopemetadata"]["type"]["value"] = "Example.Other"
    document["messagegroups"]["Kafka"] = {"messages": {
        "Reading.kafka": {"basemessageuri": "#/messagegroups/Example/messages/Reading"},
        "Other.kafka": {"basemessageuri": "#/messagegroups/Example/messages/Other"},
    }}
    document["endpoints"] = {"Kafka": {
        "protocol": "Kafka", "usage": ["producer"], "messagegroups": ["#/messagegroups/Kafka"],
        "protocoloptions": {"options": {"key": "{station_id}"}},
    }}
    definitions = tmp_path / "catalog.json"
    definitions.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", [
        "xrcg", "generate", "--language", "py", "--style", "kafkaproducer",
        "--endpoint", "Kafka", "--definitions", str(definitions),
        "--output", str(output), "--projectname", "WireTypeContract",
    ])
    assert xrcg.cli() == 0
    for source in output.rglob("*.py"):
        py_compile.compile(str(source), doraise=True)
    generated = ast.parse(next(output.rglob("test_producer.py")).read_text(encoding="utf-8"))
    test = next(node for node in generated.body if isinstance(node, ast.FunctionDef)
                and node.name.endswith("cross_event_type_kafka_key"))
    filters = [node.comparators[0] for node in ast.walk(test)
               if isinstance(node, ast.Compare) and isinstance(node.ops[0], ast.In)
               and isinstance(node.left, ast.Subscript) and isinstance(node.left.slice, ast.Constant)
               and node.left.slice.value == "type"]
    assert len(filters) == 1
    assert [item.value for item in filters[0].elts] == ["Example.Reading", "Example.Other"]


@pytest.mark.parametrize("content_mode", ["binary", "structured"])
@pytest.mark.parametrize("mapping_kind", ["none", "empty", "match", "unmatched", "chain"])
def test_generated_dataschema_overrides(content_mode, mapping_kind, tmp_path, monkeypatch):
    import copy
    import runpy

    original = "xreg://./schemagroups/Example/schemas/Reading/versions/stable"
    registered = "https://registered.example/schemas/Reading/versions/2"
    explicit = "https://explicit.example/schemas/Reading/versions/1"
    mappings = {
        "none": None,
        "empty": {},
        "match": {original: registered, explicit: registered},
        "unmatched": {"urn:unrelated": registered},
        "chain": {original: registered, registered: "urn:must-not-chain", explicit: registered},
    }
    overrides = mappings[mapping_kind]
    document = _versioned_schema_document()
    messages = document["messagegroups"]["Example"]["messages"]
    for name in ("Shared", "Explicit"):
        messages[name] = copy.deepcopy(messages["Reading"])
        messages[name]["messageid"] = name
    messages["Explicit"]["envelopemetadata"]["dataschema"] = {"type": "uri", "value": explicit}
    definitions = tmp_path / "catalog.json"
    definitions.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", [
        "xrcg", "generate", "--language", "py", "--style", "kafkaproducer",
        "--definitions", str(definitions), "--output", str(output),
        "--projectname", "UriOverrideContract",
    ])
    assert xrcg.cli() == 0
    for directory in output.rglob("src"):
        monkeypatch.syspath_prepend(str(directory))
    generated = runpy.run_path(str(next(output.rglob("producer.py"))))
    producer_class = generated["ExampleEventProducer"]
    data = generated["Reading"](value="live")

    class CaptureProducer:
        def __init__(self):
            self.messages = []

        def produce(self, topic, **kwargs):
            self.messages.append(kwargs)

    sender = CaptureProducer()
    producer = producer_class(sender, "readings", content_mode, dataschema_overrides=overrides)
    if overrides is not None:
        overrides[original] = "urn:caller-mutated"
    for name in ("reading", "shared", "explicit"):
        getattr(producer, "send_" + name)(data, flush_producer=False)

    def schema(message):
        if content_mode == "structured":
            return json.loads(message["value"])["dataschema"]
        return message["headers"]["ce_dataschema"].decode("utf-8")

    expected = registered if mapping_kind in ("match", "chain") else original
    expected_explicit = registered if mapping_kind in ("match", "chain") else explicit
    assert list(map(schema, sender.messages)) == [expected, expected, expected_explicit]
    untouched = CaptureProducer()
    producer_class(untouched, "readings", content_mode).send_reading(data, flush_producer=False)
    assert schema(untouched.messages[0]) == original
    with pytest.raises(ValueError, match="nonempty URI strings"):
        producer_class(sender, "readings", dataschema_overrides={original: ""})


@pytest.mark.parametrize('language,style,serializer_marker', [
    ('py', 'amqpproducer', 'to_byte_array(content_type)'),
    ('cs', 'amqpproducer', 'ToByteArray(contentType)'),
    ('java', 'amqpproducer', 'toByteArray(contentType)'),
    ('ts', 'amqpproducer', 'toByteArray(contentType)'),
    ('go', 'amqpproducer', 'ToByteArray(event.DataContentType())'),
    ('rust', 'producer', 'to_byte_array(&datacontenttype)'),
])
def test_codegen_producer_content_type_defaults_from_datacontenttype(
        language, style, serializer_marker):
    """Producer metadata and payload serialization follow the schema format."""
    # XSD sample declares datacontenttype: application/xml.
    xml_dir = _generate_producer(
        language, style, 'minimal-xsd.xreg.json', 'test_xsd', 'ct-xml')
    xml_sources = [
        open(p, 'r', encoding='utf-8', errors='ignore').read()
        for p in _producer_sources(xml_dir, 'test_xsd')
    ]
    assert any('application/xml' in source for source in xml_sources), (
        f"{language} producer did not default content type to application/xml "
        f"for an application/xml message")
    assert any(serializer_marker in source for source in xml_sources), (
        f"{language} producer labels XML but does not invoke its schema-aware "
        "byte serializer")

    # A conflicting XML declaration must not make JSON Schema serializers
    # advertise XML while emitting JSON.
    work_dir = tempfile.mkdtemp()
    try:
        json_sample = os.path.join(
            project_root,
            'samples/message-definitions/contoso-erp.xreg.json'.replace('/', os.path.sep))
        with open(json_sample, 'r', encoding='utf-8') as handle:
            document = json.load(handle)
        for group in document['messagegroups'].values():
            for message in group['messages'].values():
                if message.get('dataschemaformat', '').lower().startswith('json'):
                    message.setdefault('envelopemetadata', {})['datacontenttype'] = {
                        'type': 'string',
                        'value': 'application/xml',
                    }
        conflicting_sample = os.path.join(work_dir, 'json-declared-as-xml.xreg.json')
        with open(conflicting_sample, 'w', encoding='utf-8') as handle:
            json.dump(document, handle)

        json_dir = _generate_producer(
            language, style, conflicting_sample, 'test_erp', 'ct-json')
        json_sources = [
            open(p, 'r', encoding='utf-8', errors='ignore').read()
            for p in _producer_sources(json_dir, 'test_erp')
        ]
        assert any('application/json' in source for source in json_sources), (
            f"{language} producer lost the JSON Schema content type")
        assert not any('application/xml' in source for source in json_sources), (
            f"{language} producer advertised XML for JSON Schema data")
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)

    avro_dir = _generate_producer(
        language, style, 'inkjet.xreg.json', 'test_avro', 'ct-avro')
    avro_sources = [
        open(p, 'r', encoding='utf-8', errors='ignore').read()
        for p in _producer_sources(avro_dir, 'test_avro')
    ]
    assert any('avro/binary' in source for source in avro_sources), (
        f"{language} producer did not preserve the Avro binary content type")


def test_codegen_cs_mqttclient_dedups_repeated_topic_placeholder():
    """Regression test for duplicate URI-template placeholders in MQTT topic templates.

    A transport-native MQTT ``topic_name`` that references the same placeholder more
    than once (for example ``{region}`` twice) must not emit that method parameter
    twice. Before the fix the generated ``Send*Async`` signature contained
    ``string region, string region`` which is a C# CS0100 duplicate-parameter
    compile error. This mirrors the CloudEvents-path de-duplication from issue #471,
    applied to the transport-native topic-template argument collection.
    """
    work_dir = tempfile.mkdtemp()
    try:
        definitions_path = os.path.join(work_dir, 'mqtt-dup-topic.xreg.json')
        output_dir = os.path.join(work_dir, 'out')

        document = {
            "$schema": "https://xregistry.io/schema/xregistry_messaging_catalog.json",
            "messagegroups": {
                "Contoso.Telemetry": {
                    "protocol": "MQTT/5.0",
                    "messages": {
                        "Contoso.Telemetry.VehicleEvent": {
                            "name": "VehicleEvent",
                            "protocol": "MQTT/5.0",
                            "protocoloptions": {
                                "topic_name": "contoso/telemetry/{region}/vehicles/{region}/vp"
                            },
                            "dataschemaformat": "JsonStructure/draft-02",
                            "dataschemauri": "#/schemagroups/Contoso.Telemetry.jstruct/schemas/Contoso.Telemetry.VehicleEvent"
                        }
                    }
                }
            },
            "schemagroups": {
                "Contoso.Telemetry.jstruct": {
                    "schemas": {
                        "Contoso.Telemetry.VehicleEvent": {
                            "name": "VehicleEvent",
                            "format": "JsonStructure/draft-02",
                            "defaultversionid": "1",
                            "versions": {
                                "1": {
                                    "format": "JsonStructure/draft-02",
                                    "schema": {
                                        "$schema": "https://json-structure.org/meta/core/v0/#",
                                        "name": "VehicleEvent",
                                        "type": "object",
                                        "properties": {
                                            "oper": {"type": "int32"},
                                            "veh": {"type": "int32"}
                                        },
                                        "required": ["oper", "veh"]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        with open(definitions_path, 'w', encoding='utf-8') as handle:
            json.dump(document, handle, indent=2)

        sys.argv = [
            'xrcg', 'generate',
            '--style', 'mqttclient',
            '--language', 'cs',
            '--definitions', definitions_path,
            '--output', output_dir,
            '--projectname', 'MqttDupTopic'
        ]
        assert xrcg.cli() == 0

        producer_path = None
        for dirpath, _dirnames, filenames in os.walk(output_dir):
            if 'Producer.cs' in filenames:
                producer_path = os.path.join(dirpath, 'Producer.cs')
                break
        assert producer_path is not None, f"Producer.cs not found under {output_dir}"

        with open(producer_path, 'r', encoding='utf-8') as handle:
            producer_contents = handle.read()

        # The repeated {region} placeholder must yield a single parameter, not two.
        assert 'string region, string region' not in producer_contents, (
            "Duplicate 'string region' parameter (C# CS0100) emitted for a repeated "
            "topic placeholder"
        )
        # ...but the parameter must still be present (no over-de-duplication).
        assert 'string region' in producer_contents
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def test_codegen_cs_data_project_targetframework_matches_main():
    """The Avrotize-generated C# *data* project must target the same framework
    as the generated main project.

    Historically a ``_update_csproj_target_framework`` post-processor rewrote the
    ``<TargetFramework>`` of the Avrotize output to match the templates. That
    post-processing was removed once Avrotize exposed a ``target_framework``
    parameter (clemensv/avrotize#403); the renderer now passes
    ``_get_target_framework()`` straight through to ``convert_*_schema_to_csharp``.
    This regression test locks in that the data project ends up aligned with the
    main project (and with the expected framework) so a future divergence between
    Avrotize's default framework and the repository's target framework is caught
    without re-introducing any post-processing step.
    """
    definitions_path = os.path.join(project_root, 'test/xreg/contoso-erp.xreg.json')
    output_dir = tempfile.mkdtemp()
    try:
        sys.argv = [
            'xrcg', 'generate',
            '--style', 'kafkaproducer',
            '--language', 'cs',
            '--definitions', definitions_path,
            '--output', output_dir,
            '--projectname', 'TfmAlign'
        ]
        assert xrcg.cli() == 0

        csproj_paths = []
        for dirpath, _dirnames, filenames in os.walk(output_dir):
            for name in filenames:
                if name.endswith('.csproj'):
                    csproj_paths.append(os.path.join(dirpath, name))
        assert csproj_paths, f"no .csproj generated under {output_dir}"

        # The Avrotize-generated data project must be present; its
        # TargetFramework used to be rewritten by the removed post-processor.
        data_csprojs = [p for p in csproj_paths
                        if os.path.basename(p) == 'TfmAlignData.csproj']
        assert data_csprojs, f"data project csproj not found among {csproj_paths}"

        tfm_re = re.compile(r'<TargetFramework>(.*?)</TargetFramework>')

        def _tfm_of(path):
            with open(path, 'r', encoding='utf-8') as handle:
                match = tfm_re.search(handle.read())
            assert match, f"no <TargetFramework> in {path}"
            return match.group(1)

        expected = TemplateRenderer(
            GeneratorContext(), 'TfmAlign', 'cs', 'kafkaproducer',
            output_dir, '', {}, [], {}, False, False
        )._get_target_framework()

        for path in csproj_paths:
            actual = _tfm_of(path)
            assert actual == expected, (
                f"{os.path.basename(path)} targets {actual}, expected {expected}")
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)


@pytest.mark.parametrize("language,style", [
    ("ts", "kafkaproducer"), ("ts", "egproducer"), ("ts", "producerhttp"),
    ("ts", "dashboard"), ("ts", "mqttclient"),
    ("go", "ehproducer"), ("go", "kafkaproducer"),
])
def test_generated_projects_use_central_dependency_floors(tmp_path, monkeypatch, language, style):
    definitions = os.path.join(project_root, "test", "xreg", "lightbulb.xreg.json")
    monkeypatch.setattr(sys, "argv", [
        "xrcg", "generate", "--definitions", definitions,
        "--output", str(tmp_path), "--projectname", "DependencyFloors",
        "--language", language, "--style", style,
    ])
    assert xrcg.cli() == 0
    if language == "ts":
        with open(os.path.join(project_root, "xrcg", "dependencies", "typescript",
                               "node22", "package.json"), encoding="utf-8") as handle:
            central = json.load(handle)
        manifests = list(tmp_path.rglob("package.json"))
        assert manifests
        overrides_found = False
        for manifest in manifests:
            package = json.loads(manifest.read_text(encoding="utf-8"))
            if "overrides" in package:
                overrides_found = True
                assert package["overrides"] == central["overrides"]
            for section in ("dependencies", "devDependencies"):
                for name, version in package.get(section, {}).items():
                    if name in central.get(section, {}) and "overrides" in package:
                        assert version == central[section][name]
        assert overrides_found
    else:
        manifest = tmp_path / "DependencyFloors" / "go.mod"
        content = manifest.read_text(encoding="utf-8")
        floor = TemplateRenderer.dependency("go", "go121", "golang.org/x/net").strip()
        assert floor in content


def test_extract_schema_info_keeps_names_for_top_level_schemagroup_refs():
    """Top-level schemagroup refs must retain class and namespace metadata.

    Issue #371 stopped collecting inline ``.../versions/.../schema`` refs under
    ``schemagroups`` to avoid processing alternate encodings twice. The
    top-level schema ref path still needs to supply the name/namespace metadata
    required for JSONSchema-to-Avro conversion in the C#/Java generators.
    """
    with open(os.path.join(project_root, 'test/xreg/contoso-erp.xreg.json'), 'r', encoding='utf-8') as handle:
        document = json.load(handle)

    renderer = TemplateRenderer(
        GeneratorContext(),
        'test_project',
        'cs',
        'amqpconsumer',
        os.path.join(tempfile.gettempdir(), 'tmp', 'schema-info-check'),
        '',
        {},
        [],
        {},
        False,
        False
    )
    schema_ref = '#/schemagroups/Contoso.ERP.Events/schemas/purchaseOrderData'
    schema_data = renderer.resolve_schema_reference_in_document(schema_ref, document)
    assert schema_data is not None

    schema_info = renderer.extract_schema_info_from_resolved_data(schema_ref, schema_data)
    assert schema_info is not None
    assert schema_info['class_name'] == 'Contoso.ERP.Events.purchaseOrderData'
    assert schema_info['namespace'] == 'Contoso.ERP.Events'

    renderer.convert_json_to_avro_if_needed(schema_info)
    assert schema_info['format_short'] == 'avro'
    assert schema_info['content']['name'] == 'PurchaseOrderData'
    assert schema_info['content']['namespace'] == 'Contoso.ERP.Events'
