"""Test the Python code generation and integration with the generated code."""

import platform
import subprocess
import sys
import os
import tempfile
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
    pyp = open(pyproject_files[0], encoding="utf-8").read()
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
