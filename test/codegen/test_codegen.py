import json
import platform
import re
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

def test_sbproducer_preserves_dotted_amqp_message_ids(tmp_path, monkeypatch):
    """Raw AMQP message IDs sharing a version must generate distinct factories."""
    messages = {
        f"example.{kind}.02": {"protocol": "AMQP/1.0", "protocoloptions": {}}
        for kind in ("001", "002")
    }
    messages["example.status.updated"] = {
        "protocol": "AMQP/1.0",
        "envelope": "CloudEvents/1.0",
        "envelopemetadata": {},
    }
    definitions = tmp_path / "catalogue.json"
    definitions.write_text(json.dumps({
        "messagegroups": {"example": {"messages": messages}},
    }), encoding="utf-8")
    output = tmp_path / "generated"
    monkeypatch.setattr(sys, "argv", [
        "xrcg", "generate", "--language", "cs", "--style", "sbproducer",
        "--projectname", "NamingProbe", "--definitions", str(definitions),
        "--output", str(output), "--noschema",
    ])
    assert xrcg.cli() == 0

    factory = next(output.rglob("EventFactory.cs")).read_text(encoding="utf-8")
    tests = next(output.rglob("ProducerTest.cs")).read_text(encoding="utf-8")
    expected = {"CreateExample00102Event", "CreateExample00202Event", "CreateUpdatedEvent"}
    assert set(re.findall(r"public static ServiceBusMessage (Create\w+Event)\(", factory)) == expected
    assert set(re.findall(r"EventFactory\.(Create\w+Event)\(", tests)) == expected


def test_xsd_model_generation_is_shared_across_csharp_templates(tmp_path, monkeypatch):
    """The same registry XSD binds to the same generated type across transports."""
    definitions = tmp_path / "catalogue.json"
    xsd = """<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
        targetNamespace="urn:example:payments" elementFormDefault="qualified">
      <xs:element name="Document"><xs:complexType><xs:sequence>
        <xs:element name="Id" type="xs:string"/>
      </xs:sequence></xs:complexType></xs:element>
    </xs:schema>"""
    definitions.write_text(json.dumps({
        "messagegroups": {"example": {"messages": {
            "payment.001.02": {
                "protocol": "AMQP/1.0", "dataschemaformat": "XSD/1.0",
                "dataschemaxid": "/schemagroups/example/schemas/payment.001.02",
                "protocoloptions": {"properties": {
                    "subject": {"type": "string", "value": "Payment"},
                    "content-type": {"type": "string", "value": "application/xml"},
                }},
            },
        }}},
        "schemagroups": {"example": {"schemas": {"payment.001.02": {
            "defaultversionid": "1", "versions": {"1": {"format": "XSD/1.0", "schema": xsd}},
        }}}},
    }), encoding="utf-8")
    model_names = set()
    for style, source in (
        ("sbproducer", "EventFactory.cs"),
        ("sbazfn", "DispatchInterfaces.cs"),
        ("amqpproducer", "EventProducer.cs"),
    ):
        output = tmp_path / style
        monkeypatch.setattr(sys, "argv", [
            "xrcg", "generate", "--language", "cs", "--style", style,
            "--projectname", "XmlProbe", "--definitions", str(definitions), "--output", str(output),
        ])
        assert xrcg.cli() == 0
        model, = output.rglob("Document.cs")
        generated = model.read_text(encoding="utf-8")
        assert '[XmlRoot("Document", Namespace="urn:example:payments")]' in generated
        namespace = re.search(r"^namespace (\S+)", generated, re.MULTILINE).group(1)
        code = next(output.rglob(source)).read_text(encoding="utf-8")
        assert f"global::{namespace}.Document" in code
        model_names.add(namespace)
        if style == "sbproducer":
            assert 'message.Subject = "Payment"' in code
            assert 'string contentType = "application/xml"' in code
        elif style == "sbazfn":
            dispatch = next(output.rglob("Function.cs")).read_text(encoding="utf-8")
            assert 'case "Payment":' in dispatch
            assert f"global::{namespace}.Document.FromData(" in dispatch
    assert len(model_names) == 1


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
