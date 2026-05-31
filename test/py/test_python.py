"""Test the Python code generation and integration with the generated code."""

import platform
import subprocess
import sys
import os
import tempfile
import json
from datetime import datetime
import pytest

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)  # Prioritize local xregistry over installed version

import xrcg


# this test invokes the xregistry command line tool to generate a C# proxy and a consumer
# and then builds the proxy and the consumer and runs a prepared test that integrates both

def run_python_test(xreg_file: str, output_dir: str, projectname: str, style: str):
    """
    Run python test via make

    Args:
        xreg_file (str): The path to the xregistry file.
        output_dir (str): The output directory for the generated files.
        projectname (str): The name of the project.
        style (str): The style of the generated code.

    Returns:
        None
    """

    sys.argv = ['xrcg', 'generate',
                '--definitions', xreg_file,
                '--output', output_dir,
                '--projectname', projectname,
                '--style', style,
                '--language', "py"]
    print(f"sys.argv: {sys.argv}")
    assert xrcg.cli() == 0
    use_shell = platform.system() == 'Windows'
    subprocess.check_call(['make', 'test', '-C', output_dir], cwd=os.path.dirname(__file__), shell=use_shell)


def test_ehproducer_contoso_erp_py():
    """ Test the EventHub producer for Contoso ERP. """
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_ehproducer_contoso_erp_py", "ehproducer")


def test_ehproducer_fabrikam_motorsports_py():
    """ Test the EventHub producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_ehproducer_fabrikam_motorsports_py", "ehproducer")


def test_ehproducer_inkjet_py():
    """ Test the EventHub producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_ehproducer_inkjet_py", "ehproducer")


def test_ehproducer_lightbulb_py():
    """ Test the EventHub producer for Lightbulb. """
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(
            project_root, "test/xreg/lightbulb.xreg.json"), tmpdirname, "test_ehproducer_lightbulb_py", "ehproducer")
        
def test_ehproducer_lightbulb_amqp_py():
    """ Test the EventHub producer for Lightbulb. """
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(
            project_root, "test/xreg/lightbulb-amqp.xreg.json"), tmpdirname, "test_ehproducer_lightbulb_amqp_py", "ehproducer")

def test_ehconsumer_contoso_erp_py():
    """ Test the EventHub consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_ehconsumer_contoso_erp_py", "ehconsumer")


def test_ehconsumer_fabrikam_motorsports_py():
    """ Test the EventHub consumer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_ehconsumer_fabrikam_motorsports_py", "ehconsumer")


def test_ehconsumer_inkjet_py():
    """ Test the EventHub consumer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_ehconsumer_inkjet_py", "ehconsumer")


def test_ehconsumer_lightbulb_py():
    """ Test the EventHub consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(
            project_root, "test/xreg/lightbulb.xreg.json"), tmpdirname, "test_ehconsumer_lightbulb_py", "ehconsumer")


def test_kafkaproducer_contoso_erp_py():
    """ Test the Kafka producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaproducer_contoso_erp_py", "kafkaproducer")


def test_kafkaproducer_fabrikam_motorsports_py():
    """ Test the Kafka producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaproducer_fabrikam_motorsports_py", "kafkaproducer")


def test_kafkaproducer_inkjet_py():
    """ Test the Kafka producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaproducer_inkjet_py", "kafkaproducer")


def test_kafkaproducer_inkjet_jstruct_py():
    """ Test the Kafka producer for Inkjet with JSON Structure schema."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet-jstruct.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaproducer_inkjet_jstruct_py", "kafkaproducer")


def test_kafkaproducer_lightbulb_py():
    """ Test the Kafka producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "test_kafkaproducer_lightbulb_py", "kafkaproducer")


def test_kafkaproducer_dwd_py():
    """ Test the Kafka producer for DWD weather data with endpoint-level Kafka key templates."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/dwd.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaproducer_dwd_py", "kafkaproducer")


def test_kafkaconsumer_contoso_erp_py():
    """ Test the Kafka consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaconsumer_contoso_erp_py", "kafkaconsumer")


def test_kafkaconsumer_fabrikam_motorsports_py():
    """ Test the Kafka consumer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaconsumer_fabrikam_motorsports_py", "kafkaconsumer")


def test_kafkaconsumer_inkjet_py():
    """ Test the Kafka consumer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_kafkaconsumer_inkjet_py", "kafkaconsumer")


def test_kafkaconsumer_lightbulb_py():
    """ Test the Kafka consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "test_kafkaconsumer_lightbulb_py", "kafkaconsumer")


def test_amqpproducer_lightbulb_py():
    """ Test the AMQP producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/lightbulb-amqp.xreg.json"),
                        tmpdirname, "test_amqpproducer_lightbulb_py", "amqpproducer")


def test_amqpproducer_contoso_erp_py():
    """ Test the AMQP producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_amqpproducer_contoso_erp_py", "amqpproducer")


def test_amqpconsumer_lightbulb_py():
    """ Test the AMQP consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/lightbulb-amqp.xreg.json"),
                        tmpdirname, "test_amqpconsumer_lightbulb_py", "amqpconsumer")


def test_amqpconsumer_contoso_erp_py():
    """ Test the AMQP consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_amqpconsumer_contoso_erp_py", "amqpconsumer")


def test_mqttclient_lightbulb_py():
    """ Test the MQTT client for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "test_mqttclient_lightbulb_py", "mqttclient")


def test_mqttclient_contoso_erp_py():
    """ Test the MQTT client for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_mqttclient_contoso_erp_py", "mqttclient")


def test_mqttclient_fabrikam_motorsports_py():
    """ Test the MQTT client for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_mqttclient_fabrikam_motorsports_py", "mqttclient")


def test_mqttclient_inkjet_py():
    """ Test the MQTT client for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_mqttclient_inkjet_py", "mqttclient")


def test_mqttclient_protocoloptions_py():
    """ Test the MQTT client with MQTT/5.0 protocoloptions (qos/retain/topic_name)."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/mqtt-protocoloptions.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_mqttclient_protocoloptions_py", "mqttclient")


def test_sbproducer_lightbulb_py():
    """ Test the Service Bus producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "test_sbproducer_lightbulb_py", "sbproducer")


def test_sbproducer_contoso_erp_py():
    """ Test the Service Bus producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_sbproducer_contoso_erp_py", "sbproducer")


def test_sbproducer_fabrikam_motorsports_py():
    """ Test the Service Bus producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_sbproducer_fabrikam_motorsports_py", "sbproducer")


def test_sbproducer_inkjet_py():
    """ Test the Service Bus producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_sbproducer_inkjet_py", "sbproducer")


@pytest.mark.skip(reason="Flaky test: Service Bus consumer dispatcher times out intermittently")
def test_sbconsumer_lightbulb_py():
    """ Test the Service Bus consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "test_sbconsumer_lightbulb_py", "sbconsumer")


@pytest.mark.skip(reason="Flaky test: Service Bus consumer dispatcher times out intermittently in CI")
def test_sbconsumer_contoso_erp_py():
    """ Test the Service Bus consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_sbconsumer_contoso_erp_py", "sbconsumer")


@pytest.mark.skip(reason="Flaky test: Service Bus consumer dispatcher times out intermittently in CI")
def test_sbconsumer_fabrikam_motorsports_py():
    """ Test the Service Bus consumer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_sbconsumer_fabrikam_motorsports_py", "sbconsumer")


@pytest.mark.skip(reason="Flaky test: Service Bus consumer dispatcher times out intermittently in CI")
def test_sbconsumer_inkjet_py():
    """ Test the Service Bus consumer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_python_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "test_sbconsumer_inkjet_py", "sbconsumer")

def _generate_with_template_args(xreg_file, output_dir, projectname, style, template_args):
    """Run xrcg generate with --template-args; no build/test step."""
    argv = ['xrcg', 'generate',
            '--definitions', xreg_file,
            '--output', output_dir,
            '--projectname', projectname,
            '--style', style,
            '--language', 'py']
    for kv in template_args:
        argv += ['--template-args', kv]
    sys.argv = argv
    assert xrcg.cli() == 0


@pytest.mark.parametrize("target,expected_audience", [
    ("eventhubs", "https://eventhubs.azure.net/.default"),
    ("servicebus", "https://servicebus.azure.net/.default"),
])
def test_amqpproducer_azure_cbs_codegen(target, expected_audience):
    """Codegen-only: --template-args azure_cbs_target={eventhubs,servicebus}
    emits a syntactically valid producer with the CBS reactor handler wired in
    and the correct audience.
    """
    import ast, glob
    tmpdirname = tempfile.mkdtemp()
    _generate_with_template_args(
        os.path.join(project_root, "test/xreg/lightbulb-amqp.xreg.json"),
        tmpdirname,
        "test_cbs_" + target,
        "amqpproducer",
        ["azure_cbs_target=" + target],
    )
    producer_files = glob.glob(os.path.join(tmpdirname, "**", "producer.py"), recursive=True)
    assert producer_files, "no producer.py emitted under " + tmpdirname
    src = open(producer_files[0], encoding="utf-8").read()
    ast.parse(src)
    assert "_CbsAzureHandler" in src, "CBS handler missing from generated producer"
    assert "from azure.core.credentials import TokenCredential" in src
    assert expected_audience in src, f"expected audience {expected_audience!r} not in generated producer"
    # pyproject must include azure deps
    pyproject_files = glob.glob(os.path.join(tmpdirname, "**", "pyproject.toml"), recursive=True)
    assert pyproject_files, "no pyproject.toml emitted"
    pyp = None
    for pyproject_file in pyproject_files:
        content = open(pyproject_file, encoding="utf-8").read()
        if "python-qpid-proton" in content:
            pyp = content
            break
    assert pyp is not None, "producer pyproject.toml not emitted"
    assert "azure-identity" in pyp
    assert "azure-core" in pyp


def test_amqpproducer_azure_cbs_invalid_target_fails():
    """Invalid azure_cbs_target value must abort producer.py generation."""
    import glob
    tmpdirname = tempfile.mkdtemp()
    try:
        _generate_with_template_args(
            os.path.join(project_root, "test/xreg/lightbulb-amqp.xreg.json"),
            tmpdirname,
            "test_cbs_bad",
            "amqpproducer",
            ["azure_cbs_target=bogus"],
        )
    except (Exception, SystemExit):
        pass
    producer_files = glob.glob(os.path.join(tmpdirname, "**", "producer.py"), recursive=True)
    assert not producer_files, (
        "producer.py must not be generated when azure_cbs_target is invalid; "
        "found: " + repr(producer_files)
    )


def test_amqpproducer_no_azure_cbs_has_no_azure_deps():
    """Without azure_cbs_target, no azure imports must leak into the producer."""
    import glob
    tmpdirname = tempfile.mkdtemp()
    _generate_with_template_args(
        os.path.join(project_root, "test/xreg/lightbulb-amqp.xreg.json"),
        tmpdirname,
        "test_cbs_off",
        "amqpproducer",
        [],
    )
    producer_files = glob.glob(os.path.join(tmpdirname, "**", "producer.py"), recursive=True)
    src = open(producer_files[0], encoding="utf-8").read()
    assert "azure.core.credentials" not in src
    assert "_CbsAzureHandler" not in src
    pyproject_files = glob.glob(os.path.join(tmpdirname, "**", "pyproject.toml"), recursive=True)
    pyp = open(pyproject_files[0], encoding="utf-8").read()
    assert "azure-identity" not in pyp


def test_amqpproducer_password_mode_uses_artemis_safe_blocking_sender():
    """Password-mode AMQP producers must use the Artemis-safe blocking sender path."""
    src = _generate_amqp_producer_src("test/xreg/lightbulb-amqp.xreg.json")
    assert "from proton.reactor import AtMostOnce" in src
    assert "def _init_blocking_sender(self) -> None:" in src
    assert "self._blocking_sender_is_presettled = sender_options is not None" in src
    assert "def _send_via_blocking_sender(self, amqp_msg: Message, timeout: float = 30.0) -> None:" in src
    assert "connection_timeout = 120 if self.username and self.password else 30" in src
    assert "sender_options = AtMostOnce() if self.username and self.password else None" in src
    assert "self._sender = self._connection.create_sender(self.address, options=sender_options)" in src
    assert "self._sender.send(amqp_msg, timeout=timeout)" in src
    assert "self._connection.conn.transport.pending() == 0" in src
    assert 'msg=f"Flushing sender {self._sender.link.name} transport"' in src
    assert "self._send_via_blocking_sender(amqp_msg)" in src
    assert "self._connection.create_sender(self.address)\n" not in src
    assert "BlockingConnection(connection_url, timeout=30)" not in src


def _generate_amqp_producer_src(xreg_relpath="test/xreg/lightbulb-amqp.xreg.json", template_args=None):
    """Generate the Python AMQP producer for the given fixture and return
    the contents of the generated producer.py as a string.
    """
    import glob
    tmpdirname = tempfile.mkdtemp()
    _generate_with_template_args(
        os.path.join(project_root, xreg_relpath.replace('/', os.sep)),
        tmpdirname,
        "test_amqp_introspect",
        "amqpproducer",
        template_args or [],
    )
    producer_files = glob.glob(os.path.join(tmpdirname, "**", "producer.py"), recursive=True)
    assert producer_files, "no producer.py emitted under " + tmpdirname
    return open(producer_files[0], encoding="utf-8").read()


def _generate_amqp_producer_src_from_document(document):
    """Generate the Python AMQP producer for an inline xRegistry document."""
    with tempfile.NamedTemporaryFile("w", suffix=".xreg.json", delete=False, encoding="utf-8") as fp:
        json.dump(document, fp)
        manifest_path = fp.name
    try:
        return _generate_amqp_producer_src(manifest_path)
    finally:
        os.unlink(manifest_path)


def _generate_python_entrypoint_from_document(document, style, entrypoint_name):
    """Generate a Python entrypoint file from an inline xRegistry document."""
    import glob
    import uuid

    with tempfile.NamedTemporaryFile("w", suffix=".xreg.json", delete=False, encoding="utf-8") as fp:
        json.dump(document, fp)
        manifest_path = fp.name
    try:
        tmpdirname = tempfile.mkdtemp()
        projectname = f"test_{style}_{uuid.uuid4().hex[:8]}"
        _generate_with_template_args(
            manifest_path,
            tmpdirname,
            projectname,
            style,
            [],
        )
        entrypoint_files = glob.glob(os.path.join(tmpdirname, "**", entrypoint_name), recursive=True)
        assert entrypoint_files, f"no {entrypoint_name} emitted under {tmpdirname}"
        return tmpdirname, entrypoint_files[0]
    finally:
        os.unlink(manifest_path)


def _generate_kafka_producer_src_from_document(document):
    """Generate the Python Kafka producer for an inline xRegistry document."""
    _, producer_file = _generate_python_entrypoint_from_document(document, "kafkaproducer", "producer.py")
    return open(producer_file, encoding="utf-8").read()


def _generate_mqtt_client_src_from_document(document):
    """Generate the Python MQTT client for an inline xRegistry document."""
    _, client_file = _generate_python_entrypoint_from_document(document, "mqttclient", "client.py")
    return open(client_file, encoding="utf-8").read()


def _load_generated_python_module_from_document(document, style, entrypoint_name):
    """Load the generated CloudEvents time normalizer from emitted source."""
    import ast
    import types

    _, entrypoint_file = _generate_python_entrypoint_from_document(document, style, entrypoint_name)
    entrypoint_src = open(entrypoint_file, encoding="utf-8").read()
    parsed = ast.parse(entrypoint_src, filename=entrypoint_file)
    selected_nodes = []
    for node in parsed.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "_RFC3339_TIMESTAMP_PATTERN"
            for target in node.targets
        ):
            selected_nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == "_normalize_cloudevents_time":
            selected_nodes.append(node)
    helper_module = ast.Module(
        body=[
            ast.Import(names=[ast.alias(name="re")]),
            ast.Import(names=[ast.alias(name="typing")]),
            ast.ImportFrom(module="datetime", names=[ast.alias(name="datetime"), ast.alias(name="timezone")], level=0),
            *selected_nodes,
        ],
        type_ignores=[],
    )
    ast.fix_missing_locations(helper_module)
    namespace = {}
    exec(compile(helper_module, entrypoint_file, "exec"), namespace)
    return types.SimpleNamespace(**namespace)


def _generate_mqtt_client_src(xreg_relpath="test/xreg/lightbulb.xreg.json"):
    """Generate the Python MQTT client for the given fixture and return the
    contents of the generated client.py as a string.
    """
    import glob
    tmpdirname = tempfile.mkdtemp()
    _generate_with_template_args(
        os.path.join(project_root, xreg_relpath.replace('/', os.sep)),
        tmpdirname,
        "test_mqtt_introspect",
        "mqttclient",
        [],
    )
    client_files = glob.glob(os.path.join(tmpdirname, "**", "client.py"), recursive=True)
    assert client_files, "no client.py emitted under " + tmpdirname
    return open(client_files[0], encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Wire-format regression tests for the Python producer/client templates.
#
# These guard against two specific regressions reported in production:
#   1. The CloudEvents AMQP Protocol Binding v1.0.2 §3.1 mandates
#      ``cloudEvents:`` as the application-properties prefix for CE
#      attributes. The cloudevents-sdk's ``to_binary`` emits HTTP-style
#      ``ce-`` headers; the producer MUST translate them. Assigning the
#      raw dict to ``amqp_msg.properties`` produces wire-noncompliant
#      messages that no CE-AMQP consumer will recognize.
#   2. The generated dataclass ``to_byte_array("application/json")``
#      returns ``str``; if passed straight to ``proton.Message(body=...)``
#      proton emits an AMQP string section containing JSON (double-encoded
#      on the wire). Same hazard for paho-mqtt PUBLISH payloads. The
#      producer/client MUST coerce to ``bytes`` and proton MUST be told
#      ``inferred=True`` so the body becomes an AMQP binary section.
# ---------------------------------------------------------------------------


def _build_kafka_time_document():
    return {
        "messagegroups": {
            "Example.Kafka": {
                "envelope": "CloudEvents/1.0",
                "messages": {
                    "Example.Event": {
                        "envelope": "CloudEvents/1.0",
                        "envelopemetadata": {
                            "type": {"value": "Example.Event"},
                            "source": {"value": "urn:test"},
                            "time": {"type": "uritemplate", "value": "{event_time}"},
                            "datacontenttype": {"value": "application/json"},
                        },
                        "dataschemaformat": "JsonSchema/draft-07",
                        "dataschema": {
                            "type": "object",
                            "properties": {"value": {"type": "string"}},
                        },
                    }
                }
            }
        }
    }


def _build_amqp_time_document():
    return {
        "messagegroups": {
            "Example.Amqp": {
                "envelope": "CloudEvents/1.0",
                "protocol": "AMQP/1.0",
                "messages": {
                    "Example.Event": {
                        "envelope": "CloudEvents/1.0",
                        "protocol": "AMQP/1.0",
                        "envelopemetadata": {
                            "type": {"value": "Example.Event"},
                            "source": {"type": "uritemplate", "value": "{feedurl}"},
                            "subject": {"type": "uritemplate", "value": "{spacecraft}"},
                            "time": {"type": "uritemplate", "value": "{time_tag}"},
                            "datacontenttype": {"value": "application/json"}
                        },
                        "dataschemaformat": "JsonSchema/draft-07",
                        "dataschema": {
                            "type": "object",
                            "properties": {"value": {"type": "string"}}
                        }
                    }
                }
            }
        }
    }


def _build_mqtt_time_document():
    return {
        "messagegroups": {
            "Example.Mqtt": {
                "envelope": "CloudEvents/1.0",
                "protocol": "MQTT/5.0",
                "messages": {
                    "Example.Event": {
                        "envelope": "CloudEvents/1.0",
                        "protocol": "MQTT/5.0",
                        "envelopemetadata": {
                            "type": {"value": "Example.Event"},
                            "source": {"value": "urn:test"},
                            "time": {"type": "uritemplate", "value": "{event_time}"},
                            "datacontenttype": {"value": "application/json"},
                        },
                        "protocoloptions": {
                            "topic_name": "example/{event_time}"
                        },
                        "dataschemaformat": "JsonSchema/draft-07",
                        "dataschema": {
                            "type": "object",
                            "properties": {"value": {"type": "string"}},
                        },
                    }
                }
            }
        }
    }

def test_amqpproducer_emits_cloudevents_prefix_not_ce_prefix():
    """CloudEvents AMQP §3.1: application-properties prefix MUST be
    ``cloudEvents:``. The legacy ``ce-`` HTTP-binding prefix MUST NOT
    appear in any property key the producer puts on the wire.
    """
    # Use the CloudEvents-enveloped fixture so the CE code paths are emitted.
    src = _generate_amqp_producer_src("test/xreg/lightbulb.xreg.json")
    assert "cloudEvents:" in src, (
        "producer.py must use the CloudEvents AMQP §3.1 'cloudEvents:' "
        "prefix when mapping CE attributes onto application-properties"
    )
    assert "_ce_headers_to_amqp_properties" in src, (
        "producer.py must translate cloudevents-sdk 'ce-' HTTP headers "
        "into AMQP 'cloudEvents:' application-properties via a helper"
    )
    # Raw assignment of the cloudevents-sdk headers dict is the bug.
    assert "amqp_msg.properties = headers" not in src, (
        "producer.py must not assign the raw cloudevents-sdk headers "
        "dict (which has 'ce-' prefixes) to amqp_msg.properties"
    )


def test_kafkaproducer_time_uritemplate_is_normalized_before_cloudevent_creation():
    """Kafka producer must normalize mapped CloudEvents time before sending."""
    src = _generate_kafka_producer_src_from_document(_build_kafka_time_document())
    assert "def _normalize_cloudevents_time(value: typing.Any) -> typing.Optional[str]:" in src
    assert "if 'time' in attributes:" in src
    assert "normalized_time = _normalize_cloudevents_time(attributes['time'])" in src
    assert "del attributes['time']" in src


def test_amqpproducer_body_is_bytes_with_inferred_true():
    """The AMQP body MUST be a binary section. The producer must coerce
    str payloads to bytes and instantiate ``Message`` with
    ``inferred=True`` so proton emits an AMQP binary section instead of
    an AMQP string section containing JSON.
    """
    # Use the CloudEvents-enveloped fixture so the CE binary/structured
    # branches are emitted alongside the non-CE form.
    src = _generate_amqp_producer_src("test/xreg/lightbulb.xreg.json")
    # _serialize_payload coerces str -> bytes.
    assert "payload.encode('utf-8')" in src or 'payload.encode("utf-8")' in src, (
        "producer.py _serialize_payload must coerce str payloads to bytes"
    )
    # CE-enveloped messages must use the CE binary + structured forms.
    assert "Message(body=body, inferred=True)" in src, (
        "CloudEvent binary-mode send must build Message with inferred=True"
    )
    assert "Message(body=msg_body, inferred=True)" in src, (
        "CloudEvent structured-mode send must build Message with inferred=True"
    )
    # Regression guards: the buggy forms must not reappear in CE paths.
    for bad in (
        "Message(body=body)\n",
        "Message(body=msg_body)\n",
    ):
        assert bad not in src, (
            "producer.py contains a Message(...) construction without "
            "inferred=True (would emit AMQP string section for bytes): "
            + bad.strip()
        )


def test_amqpproducer_non_cloudevent_body_is_bytes_with_inferred_true():
    """The non-CloudEvent AMQP path must also build ``Message`` with
    ``inferred=True`` so a bytes body becomes an AMQP binary section.
    """
    src = _generate_amqp_producer_src("test/xreg/lightbulb-amqp.xreg.json")
    assert "Message(body=byte_data, inferred=True)" in src, (
        "Non-CloudEvent send must build Message with inferred=True"
    )
    assert "Message(body=byte_data)\n" not in src, (
        "Non-CloudEvent send must not build Message without inferred=True"
    )


def test_amqpproducer_protocoloptions_application_properties_codegen():
    """AMQP protocoloptions.application_properties must become send
    parameters and qpid-proton application-properties.
    """
    src = _generate_amqp_producer_src("test/xreg/lightbulb-amqp.xreg.json")
    sig_start = src.index("def send_turned_on(")
    sig_end = src.index(") -> None:", sig_start)
    send_signature = src[sig_start:sig_end]
    batch_sig_start = src.index("def send_turned_on_batch(")
    batch_sig_end = src.index(") -> None:", batch_sig_start)
    batch_signature = src[batch_sig_start:batch_sig_end]
    assert send_signature.count("_tenantid: str") == 1
    assert send_signature.count("_deviceid: str") == 1
    assert batch_signature.count("_tenantid: str") == 1
    assert batch_signature.count("_deviceid: str") == 1
    assert 'amqp_msg.subject = "{tenantid}".format(tenantid=_tenantid)' in src
    assert 'app_properties["water_shortname"] = "{deviceid}".format(deviceid=_deviceid)' in src
    assert "_tenantid=_tenantid" in src
    assert "_deviceid=_deviceid" in src
    assert "amqp_msg.properties.update(app_properties)" in src


def test_amqpproducer_protocoloptions_message_annotations_codegen():
    """AMQP protocoloptions.message_annotations must become qpid-proton
    message annotations with AMQP symbol keys.
    """
    src = _generate_amqp_producer_src("test/xreg/lightbulb-amqp.xreg.json")
    sig_start = src.index("def send_turned_on(")
    sig_end = src.index(") -> None:", sig_start)
    send_signature = src[sig_start:sig_end]
    assert send_signature.count("_tenantid: str") == 1
    assert send_signature.count("_deviceid: str") == 1
    assert "from proton import Message, symbol" in src
    assert 'annotation_value = "{tenantid}-{deviceid}".format(tenantid=_tenantid, deviceid=_deviceid)' in src
    assert "annotation_value = str(annotation_value)[:128]" in src
    assert 'annotations[symbol("x-opt-partition-key")] = annotation_value' in src
    assert "amqp_msg.annotations.update(annotations)" in src


def test_amqpproducer_group_level_message_annotations_codegen():
    """AMQP producer must merge messagegroup-level message_annotations into
    CloudEvents messages and de-dupe placeholders already used by metadata.
    """
    src = _generate_amqp_producer_src_from_document({
        "messagegroups": {
            "Example.Amqp": {
                "envelope": "CloudEvents/1.0",
                "protocol": "AMQP/1.0",
                "protocoloptions": {
                    "message_annotations": {
                        "x-opt-partition-key": {
                            "type": "uritemplate",
                            "value": "{spacecraft}"
                        }
                    }
                },
                "messages": {
                    "Example.Event": {
                        "envelope": "CloudEvents/1.0",
                        "protocol": "AMQP/1.0",
                        "envelopemetadata": {
                            "type": {"value": "Example.Event"},
                            "source": {"type": "uritemplate", "value": "{feedurl}"},
                            "subject": {"type": "uritemplate", "value": "{spacecraft}"},
                            "datacontenttype": {"value": "application/json"}
                        },
                        "dataschemaformat": "JsonSchema/draft-07",
                        "dataschema": {
                            "type": "object",
                            "properties": {"value": {"type": "string"}}
                        }
                    }
                }
            }
        }
    })
    sig_start = src.index("def send_event(")
    sig_end = src.index(") -> None:", sig_start)
    send_signature = src[sig_start:sig_end]
    assert send_signature.count("_spacecraft: str") == 1
    assert 'annotation_value = "{spacecraft}".format(spacecraft=_spacecraft)' in src
    assert 'annotations[symbol("x-opt-partition-key")] = annotation_value' in src


def test_amqpproducer_time_uritemplate_sets_ce_and_creation_time():
    """AMQP producer must not drop CloudEvents time URI templates and should
    project parseable values onto AMQP properties.creation-time.
    """
    src = _generate_amqp_producer_src_from_document(_build_amqp_time_document())
    assert "_time_tag: str" in src
    assert '"{time_tag}".format(time_tag=_time_tag)' in src
    assert "None,  # Will be auto-generated" not in src
    assert "normalized_time = _normalize_cloudevents_time(attributes['time'])" in src
    assert "amqp_creation_time = self._coerce_amqp_timestamp(attributes.get('time'))" in src
    assert "amqp_msg.creation_time = amqp_creation_time" in src


def test_mqttclient_body_is_bytes_not_str():
    """The MQTT PUBLISH payload MUST be bytes. ``to_byte_array`` returns
    ``str`` for text content types; the client must coerce to bytes
    before handing to cloudevents-sdk / paho-mqtt so receivers do not
    have to double-decode JSON.
    """
    src = _generate_mqtt_client_src()
    assert "byte_data = data.to_byte_array(content_type)" in src, (
        "client.py must call to_byte_array on the dataclass"
    )
    # The coercion guard must be immediately downstream.
    assert "isinstance(byte_data, str)" in src and "byte_data.encode('utf-8')" in src, (
        "client.py must coerce byte_data str -> bytes before constructing "
        "the CloudEvent (otherwise the wire body is a JSON string literal "
        "containing JSON)"
    )
    # Final payload coercion guard for both content modes.
    assert "isinstance(payload, dict)" in src, (
        "client.py must coerce structured-mode dict payload to bytes "
        "(otherwise paho-mqtt crashes on dict payloads)"
    )
    assert "isinstance(payload, str)" in src, (
        "client.py must coerce str payload to bytes before publish so the "
        "wire representation matches the declared content-type byte-for-byte"
    )


def test_mqttclient_time_uritemplate_is_normalized_before_cloudevent_creation():
    """MQTT client must normalize mapped CloudEvents time before publishing."""
    src = _generate_mqtt_client_src_from_document(_build_mqtt_time_document())
    assert "def _normalize_cloudevents_time(value: typing.Any) -> typing.Optional[str]:" in src
    assert "if 'time' in attributes:" in src
    assert "normalized_time = _normalize_cloudevents_time(attributes['time'])" in src
    assert "del attributes['time']" in src


@pytest.mark.parametrize("style,entrypoint_name,document_builder", [
    ("kafkaproducer", "producer.py", _build_kafka_time_document),
    ("amqpproducer", "producer.py", _build_amqp_time_document),
    ("mqttclient", "client.py", _build_mqtt_time_document),
])
def test_generated_py_cloudevents_time_normalizer_validates_rfc3339(style, entrypoint_name, document_builder):
    """Generated Python CloudEvents helpers must validate and normalize time."""
    module = _load_generated_python_module_from_document(
        document_builder(),
        style,
        entrypoint_name,
    )
    assert module._normalize_cloudevents_time(None) is None
    assert module._normalize_cloudevents_time(datetime(2024, 1, 2, 3, 4, 5)) == "2024-01-02T03:04:05Z"
    assert module._normalize_cloudevents_time("2024-01-02T03:04:05.123456") == "2024-01-02T03:04:05.123456Z"
    assert module._normalize_cloudevents_time("2024-01-02t03:04:05z") == "2024-01-02T03:04:05Z"
    with pytest.raises(ValueError, match="RFC 3339"):
        module._normalize_cloudevents_time("2024-01-02")


def _generate_eh_producer_src(xreg_relpath="test/xreg/lightbulb.xreg.json"):
    """Generate the Python Event Hubs producer for the given fixture."""
    import glob
    tmpdirname = tempfile.mkdtemp()
    _generate_with_template_args(
        os.path.join(project_root, xreg_relpath.replace('/', os.sep)),
        tmpdirname,
        "test_eh_introspect",
        "ehproducer",
        [],
    )
    producer_files = glob.glob(os.path.join(tmpdirname, "**", "producer.py"), recursive=True)
    assert producer_files, "no producer.py emitted under " + tmpdirname
    return open(producer_files[0], encoding="utf-8").read()


def _generate_sb_producer_src(xreg_relpath="test/xreg/lightbulb.xreg.json"):
    """Generate the Python Service Bus producer for the given fixture."""
    import glob
    tmpdirname = tempfile.mkdtemp()
    _generate_with_template_args(
        os.path.join(project_root, xreg_relpath.replace('/', os.sep)),
        tmpdirname,
        "test_sb_introspect",
        "sbproducer",
        [],
    )
    producer_files = glob.glob(os.path.join(tmpdirname, "**", "producer.py"), recursive=True)
    assert producer_files, "no producer.py emitted under " + tmpdirname
    return open(producer_files[0], encoding="utf-8").read()


def test_ehproducer_emits_cloudevents_prefix_not_cloudevents_underscore():
    """Event Hubs producer must use the CE-AMQP §3.1 ``cloudEvents:``
    prefix on application-properties; the previous ``cloudEvents_``
    (underscore) form is not recognized by spec-compliant CE consumers
    such as azure-servicebus ``CloudEvent.from_message``.
    """
    src = _generate_eh_producer_src("test/xreg/lightbulb.xreg.json")
    assert 'event_data.properties["cloudEvents:"+key[3:]]' in src, (
        "ehproducer must map cloudevents-sdk 'ce-' headers to "
        "'cloudEvents:' application-properties (CE-AMQP §3.1)"
    )
    assert "cloudEvents_" not in src, (
        "ehproducer must not emit the non-spec 'cloudEvents_' "
        "(underscore) prefix on application-properties"
    )


def test_ehproducer_body_is_bytes_not_str():
    """Event Hubs producer must coerce JSON ``str`` payloads to bytes
    before constructing ``EventData`` so the wire body is a binary AMQP
    data section, not a string section containing escaped JSON.
    """
    src = _generate_eh_producer_src("test/xreg/lightbulb.xreg.json")
    assert "byte_data = data.to_byte_array(content_type)" in src
    assert "isinstance(byte_data, str)" in src and "byte_data.encode('utf-8')" in src, (
        "ehproducer must coerce to_byte_array str result to bytes before "
        "handing to the CloudEvent constructor"
    )
    assert "isinstance(body, str)" in src and "body.encode('utf-8')" in src, (
        "ehproducer must coerce cloudevents-sdk body str to bytes before "
        "constructing EventData (avoids AMQP string section + JSON double-encode)"
    )


def test_sbproducer_emits_cloudevents_prefix():
    """Service Bus producer already maps to 'cloudEvents:' — guard the
    mapping against regressions.
    """
    src = _generate_sb_producer_src("test/xreg/lightbulb.xreg.json")
    assert 'message.application_properties["cloudEvents:"+key[3:]]' in src, (
        "sbproducer must keep mapping 'ce-' headers to 'cloudEvents:' "
        "application-properties (CE-AMQP §3.1)"
    )


def test_sbproducer_body_is_bytes_not_str():
    """Service Bus producer must coerce JSON ``str`` payloads to bytes
    before constructing ``ServiceBusMessage`` so the wire body is a
    binary AMQP data section.
    """
    src = _generate_sb_producer_src("test/xreg/lightbulb.xreg.json")
    assert "isinstance(byte_data, str)" in src and "byte_data.encode('utf-8')" in src, (
        "sbproducer must coerce to_byte_array str result to bytes before "
        "handing to the CloudEvent constructor"
    )
    assert "isinstance(body, str)" in src and "body.encode('utf-8')" in src, (
        "sbproducer must coerce cloudevents-sdk body str to bytes before "
        "constructing ServiceBusMessage"
    )
