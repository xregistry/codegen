"""Test the TypeScript code generation and integration with the generated code."""

import platform
import subprocess
import sys
import os
import tempfile
import xrcg
import pytest

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(project_root))

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def run_typescript_test(xreg_file: str, output_dir: str, projectname: str, style: str):
    """
    Run npm test on the generated TypeScript project.

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
                '--language', "ts"]
    print(f"sys.argv: {sys.argv}")
    assert xrcg.cli() == 0
    
    # The generated TypeScript project is in a subdirectory based on the style
    # Map style to directory name (e.g., kafkaproducer -> TestProjectKafkaProducer)
    style_map = {
        'kafkaproducer': 'KafkaProducer',
        'kafkaconsumer': 'KafkaConsumer',
        'ehproducer': 'EventHubsProducer',
        'ehconsumer': 'EventHubsConsumer',
        'sbproducer': 'ServiceBusProducer',
        'sbconsumer': 'ServiceBusConsumer',
        'amqpproducer': 'AmqpProducer',
        'amqpconsumer': 'AmqpConsumer',
        'mqttclient': 'MqttClient',
        'egproducer': 'EventGridProducer'
    }
    
    style_suffix = style_map.get(style, style.capitalize())
    project_dir = os.path.join(output_dir, f"{projectname}{style_suffix}")
    data_project_dir = os.path.join(output_dir, f"{projectname}Data")
    
    if not os.path.exists(project_dir):
        raise FileNotFoundError(f"Generated project directory not found: {project_dir}")
    
    # Use shell=True on Windows to find .cmd files in PATH
    use_shell = platform.system() == 'Windows'
    
    # First, install and build the data project if it exists
    if os.path.exists(data_project_dir):
        print(f"\n=== Installing data project in {data_project_dir} ===")
        subprocess.check_call(['npm', 'install'], cwd=data_project_dir, shell=use_shell)
        
        print(f"\n=== Building data project in {data_project_dir} ===")
        subprocess.check_call(['npm', 'run', 'build'], cwd=data_project_dir, shell=use_shell)
    
    # Run npm install in main project
    subprocess.check_call(['npm', 'install'], cwd=project_dir, shell=use_shell)
    
    # Run npm test
    subprocess.check_call(['npm', 'test'], cwd=project_dir, shell=use_shell)


def test_kafkaproducer_contoso_erp_ts():
    """ Test the Kafka producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "kafkaproducer")


def test_kafkaproducer_fabrikam_motorsports_ts():
    """ Test the Kafka producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "kafkaproducer")


def test_kafkaproducer_inkjet_ts():
    """ Test the Kafka producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "kafkaproducer")


def test_kafkaproducer_inkjet_jstruct_ts():
    """ Test the Kafka producer for Inkjet with JSON Structure schema."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet-jstruct.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "kafkaproducer")


def test_kafkaproducer_lightbulb_ts():
    """ Test the Kafka producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "kafkaproducer")


def test_kafkaconsumer_contoso_erp_ts():
    """ Test the Kafka consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "kafkaconsumer")


def test_kafkaconsumer_fabrikam_motorsports_ts():
    """ Test the Kafka consumer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "kafkaconsumer")


def test_kafkaconsumer_inkjet_ts():
    """ Test the Kafka consumer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "kafkaconsumer")


def test_kafkaconsumer_lightbulb_ts():
    """ Test the Kafka consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "kafkaconsumer")


def test_ehproducer_contoso_erp_ts():
    """ Test the Event Hubs producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "ehproducer")


def test_ehproducer_fabrikam_motorsports_ts():
    """ Test the Event Hubs producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "ehproducer")


def test_ehproducer_inkjet_ts():
    """ Test the Event Hubs producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "ehproducer")


def test_ehproducer_lightbulb_ts():
    """ Test the Event Hubs producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "ehproducer")


def test_ehproducer_lightbulb_amqp_ts():
    """ Test the Event Hubs producer for Lightbulb with AMQP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb-amqp.xreg.json"),
                        tmpdirname, "TestProject", "ehproducer")


def test_ehconsumer_contoso_erp_ts():
    """ Test the Event Hubs consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "ehconsumer")


def test_ehconsumer_fabrikam_motorsports_ts():
    """ Test the Event Hubs consumer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "ehconsumer")


def test_ehconsumer_inkjet_ts():
    """ Test the Event Hubs consumer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "ehconsumer")


def test_ehconsumer_lightbulb_ts():
    """ Test the Event Hubs consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "ehconsumer")


def test_sbproducer_contoso_erp_ts():
    """ Test the Service Bus producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "sbproducer")


def test_sbproducer_fabrikam_motorsports_ts():
    """ Test the Service Bus producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "sbproducer")


def test_sbproducer_inkjet_ts():
    """ Test the Service Bus producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "sbproducer")


def test_sbproducer_lightbulb_ts():
    """ Test the Service Bus producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "sbproducer")


def test_sbconsumer_contoso_erp_ts():
    """ Test the Service Bus consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "sbconsumer")


def test_sbconsumer_fabrikam_motorsports_ts():
    """ Test the Service Bus consumer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "sbconsumer")


def test_sbconsumer_inkjet_ts():
    """ Test the Service Bus consumer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "sbconsumer")


def test_sbconsumer_lightbulb_ts():
    """ Test the Service Bus consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "sbconsumer")


def test_amqpproducer_contoso_erp_ts():
    """ Test the AMQP producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "amqpproducer")


def test_amqpproducer_fabrikam_motorsports_ts():
    """ Test the AMQP producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "amqpproducer")


def test_amqpproducer_inkjet_ts():
    """ Test the AMQP producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "amqpproducer")


def test_amqpproducer_lightbulb_ts():
    """ Test the AMQP producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "amqpproducer")


def test_amqpconsumer_contoso_erp_ts():
    """ Test the AMQP consumer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "amqpconsumer")


def test_amqpconsumer_fabrikam_motorsports_ts():
    """ Test the AMQP consumer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "amqpconsumer")


def test_amqpconsumer_inkjet_ts():
    """ Test the AMQP consumer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "amqpconsumer")


def test_amqpconsumer_lightbulb_ts():
    """ Test the AMQP consumer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "amqpconsumer")


def test_mqttclient_contoso_erp_ts():
    """ Test the MQTT client for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "mqttclient")


def test_mqttclient_fabrikam_motorsports_ts():
    """ Test the MQTT client for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "mqttclient")


def test_mqttclient_inkjet_ts():
    """ Test the MQTT client for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "mqttclient")


def test_mqttclient_lightbulb_ts():
    """ Test the MQTT client for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "mqttclient")


def test_mqttclient_protocoloptions_ts():
    """ Test the MQTT client for MQTT/5.0 protocoloptions fixture (broker-backed)."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/mqtt-protocoloptions.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "mqttclient")


def test_egproducer_contoso_erp_ts():
    """ Test the Event Grid producer for Contoso ERP."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/contoso-erp.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "egproducer")


def test_egproducer_fabrikam_motorsports_ts():
    """ Test the Event Grid producer for Fabrikam Motorsports."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/fabrikam-motorsports.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "egproducer")


def test_egproducer_inkjet_ts():
    """ Test the Event Grid producer for Inkjet."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/inkjet.xreg.json".replace(
            '/', os.sep)), tmpdirname, "TestProject", "egproducer")


def test_egproducer_lightbulb_ts():
    """ Test the Event Grid producer for Lightbulb."""
    tmpdirname = tempfile.mkdtemp()
    run_typescript_test(os.path.join(project_root, "test/xreg/lightbulb.xreg.json"),
                        tmpdirname, "TestProject", "egproducer")


# ---------------------------------------------------------------------------
# Wire-format introspection tests (codegen-only, no npm build required).
#
# Guard against the CloudEvents AMQP §3.1 prefix violation observed in the
# TS amqpproducer / ehproducer / sbproducer templates: application-properties
# carrying CE attributes were being emitted with the non-spec ``ce_*``
# prefix (Kafka header convention) instead of the spec-mandated
# ``cloudEvents:*`` prefix. Any compliant CE-AMQP consumer (azure-servicebus
# ``CloudEvent.from_message``, Knative eventing, NATS adapters, …) will
# fail to recognize ``ce_*`` keys as CloudEvents attributes.
# ---------------------------------------------------------------------------

def _generate_ts_producer_src(style, source_filename):
    """Run xrcg for the given TS style against lightbulb.xreg.json and return
    the contents of ``<style-output-dir>/src/<source_filename>`` as a string.
    """
    import glob
    tmpdirname = tempfile.mkdtemp()
    sys.argv = ['xrcg', 'generate',
                '--definitions', os.path.join(project_root, 'test/xreg/lightbulb.xreg.json'),
                '--output', tmpdirname,
                '--projectname', 'TestProject',
                '--style', style,
                '--language', 'ts']
    assert xrcg.cli() == 0
    candidates = glob.glob(os.path.join(tmpdirname, '**', source_filename), recursive=True)
    assert candidates, f'no {source_filename} emitted under {tmpdirname}'
    return open(candidates[0], encoding='utf-8').read()


def test_ts_amqpproducer_emits_cloudevents_prefix_not_ce_underscore():
    """ts/amqpproducer must emit ``cloudEvents:*`` application-properties
    keys (CE-AMQP §3.1) rather than the Kafka-style ``ce_*`` prefix that
    was previously hardcoded in the template.
    """
    src = _generate_ts_producer_src('amqpproducer', 'producer.ts')
    assert "'cloudEvents:specversion'" in src
    assert "'cloudEvents:id'" in src
    assert "'cloudEvents:type'" in src
    assert "'cloudEvents:source'" in src
    # Regression guards: the buggy spellings must not reappear.
    for bad in ('ce_specversion', 'ce_id:', 'ce_type:', 'ce_source:',
                'ce_subject', 'ce_time'):
        assert bad not in src, (
            f'ts/amqpproducer must not emit non-spec CE prefix: {bad!r}'
        )


def test_ts_amqpproducer_body_is_buffer_not_object():
    """ts/amqpproducer must serialize the payload to a ``Buffer`` so rhea
    emits an AMQP binary section. Passing a raw class instance / string
    causes rhea to encode an AMQP map / string section, which produces
    double-encoded wire payloads.
    """
    src = _generate_ts_producer_src('amqpproducer', 'producer.ts')
    assert 'Buffer.from(' in src, (
        'ts/amqpproducer must coerce payload bodies into Buffer instances'
    )
    # The raw-object body bug.
    assert 'body: data,\n' not in src, (
        'ts/amqpproducer must not pass raw `data` object as message body '
        '(rhea would AMQP-encode it as a map)'
    )


def test_ts_ehproducer_emits_cloudevents_prefix_not_ce_underscore():
    """ts/ehproducer must emit ``cloudEvents:*`` keys on EventData.properties
    (which become AMQP application-properties on the wire).
    """
    src = _generate_ts_producer_src('ehproducer', 'producer.ts')
    assert "'cloudEvents:specversion'" in src
    assert "'cloudEvents:id'" in src
    assert "'cloudEvents:type'" in src
    assert "'cloudEvents:source'" in src
    for bad in ("'ce_specversion'", "'ce_id'", "'ce_type'", "'ce_source'"):
        assert bad not in src, (
            f'ts/ehproducer must not emit non-spec CE prefix: {bad}'
        )


def test_ts_sbproducer_emits_cloudevents_prefix_not_ce_underscore():
    """ts/sbproducer must emit ``cloudEvents:*`` keys on
    ServiceBusMessage.applicationProperties.
    """
    src = _generate_ts_producer_src('sbproducer', 'producer.ts')
    assert "'cloudEvents:specversion'" in src
    assert "'cloudEvents:id'" in src
    assert "'cloudEvents:type'" in src
    assert "'cloudEvents:source'" in src
    for bad in ("'ce_specversion'", "'ce_id'", "'ce_type'", "'ce_source'",
                'ce_specversion:', 'ce_id:', 'ce_type:', 'ce_source:'):
        assert bad not in src, (
            f'ts/sbproducer must not emit non-spec CE prefix: {bad}'
        )



