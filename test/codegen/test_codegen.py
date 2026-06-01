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
