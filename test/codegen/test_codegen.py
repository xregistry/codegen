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

import pytest
from xrcg.generator.generator_context import GeneratorContext
from xrcg.generator.template_renderer import TemplateRenderer

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
        segs = [s.lower().replace('_', '') for s in root.split(os.sep)]
        if data_marker in segs:
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
    sys.argv = [
        'xrcg', 'generate',
        '--style', style,
        '--language', language,
        '--definitions', os.path.join(
            project_root,
            f'samples/message-definitions/{sample}'.replace('/', os.path.sep)),
        '--output', output_dir,
        '--projectname', projectname,
    ]
    assert xrcg.cli() == 0
    return output_dir


@pytest.mark.parametrize('language,style', [
    ('py', 'amqpproducer'),
    ('cs', 'amqpproducer'),
    ('java', 'amqpproducer'),
    ('ts', 'amqpproducer'),
    ('go', 'amqpproducer'),
    ('rust', 'producer'),
])
def test_codegen_producer_content_type_defaults_from_datacontenttype(language, style):
    """Producers default their outgoing content type to the message's declared
    ``datacontenttype`` (falling back to ``application/json``).

    A message whose ``datacontenttype`` is ``application/xml`` must produce a
    producer that defaults to ``application/xml`` — otherwise an XML payload
    would be serialized/labelled as JSON. A message that declares no
    ``datacontenttype`` must keep the historical ``application/json`` default.
    """
    # XSD sample declares datacontenttype: application/xml.
    xml_dir = _generate_producer(
        language, style, 'minimal-xsd.xreg.json', 'test_xsd', 'ct-xml')
    xml_hit = any(
        'application/xml' in open(p, 'r', encoding='utf-8', errors='ignore').read()
        for p in _producer_sources(xml_dir, 'test_xsd'))
    assert xml_hit, (
        f"{language} producer did not default content type to application/xml "
        f"for an application/xml message")

    # contoso-erp declares no datacontenttype -> must remain application/json.
    json_dir = _generate_producer(
        language, style, 'contoso-erp.xreg.json', 'test_erp', 'ct-json')
    json_sources = list(_producer_sources(json_dir, 'test_erp'))
    assert any(
        'application/json' in open(p, 'r', encoding='utf-8', errors='ignore').read()
        for p in json_sources), (
        f"{language} producer lost the application/json default")
    assert not any(
        'application/xml' in open(p, 'r', encoding='utf-8', errors='ignore').read()
        for p in json_sources), (
        f"{language} producer emitted application/xml for a message with no "
        f"declared datacontenttype")


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
