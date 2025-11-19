# xRegistry Code Generator - VS Code Extension

Generate type-safe messaging/eventing SDKs from [xRegistry](https://xregistry.io/) message catalog definitions directly in Visual Studio Code.

## Features

- **Multi-Language Support**: Generate SDKs for Python, TypeScript, C#, Java
- **Multiple Protocol Styles**: AMQP, MQTT, Kafka, HTTP, Azure Event Hubs, Azure Service Bus, Azure Event Grid
- **Producer & Consumer Templates**: Generate both message producers and consumers
- **Context Menu Integration**: Right-click on `.xreg.json` files to generate code
- **CloudEvents Support**: Full CloudEvents envelope support
- **AsyncAPI & OpenAPI**: Generate API definitions from message catalogs

## Requirements

- Python 3.10 or later
- [xRegistry Code Generator](https://pypi.org/project/xregistry/) CLI installed (`pip install xregistry`)

The extension will prompt you to install the CLI if it's not found.

## Usage

1. Create or open an xRegistry message catalog file (`.xreg.json`)
2. Right-click on the file in the Explorer
3. Select **Generate Code** from the context menu
4. Choose your target language (Python, TypeScript, C#, Java, etc.)
5. Select the style (producer, consumer, or protocol-specific variant)
6. Choose an output location

The extension will generate a complete, compile-ready project with tests and dependencies.

## Supported Languages & Styles

### Python
- AMQP 1.0 Producer/Consumer
- Apache Kafka Producer/Consumer
- Azure Event Hubs Producer/Consumer
- Azure Service Bus Producer/Consumer
- MQTT Client

### TypeScript
- AMQP 1.0 Producer/Consumer
- Apache Kafka Producer/Consumer
- Azure Event Hubs Producer/Consumer
- Azure Event Grid Producer
- Azure Service Bus Producer/Consumer
- HTTP Producer
- MQTT 5.0 Client
- Dashboard

### C#
- AMQP 1.0 Producer/Consumer
- Apache Kafka Producer/Consumer
- Azure Event Hubs Producer/Consumer/Azure Function
- Azure Event Grid Producer/Azure Function
- Azure Service Bus Producer/Consumer/Azure Function
- MQTT 5.0 Client

### Java
- AMQP 1.0 Producer/Consumer
- AMQP JMS Producer
- Apache Kafka Producer/Consumer
- Azure Event Hubs Producer/Consumer
- Azure Service Bus Producer/Consumer
- MQTT 5.0 Client

### API Definitions
- AsyncAPI (Producer/Consumer)
- OpenAPI (Producer/Subscriber)

### Azure Stream Analytics
- Query Dispatch
- Query Dispatch with Payload

## Known Issues

- None currently reported

## Release Notes

### 0.13.0

- Updated branding and metadata
- Full xRegistry code generation support

### 0.0.1

- Initial release

## More Information

- [xRegistry Specification](https://github.com/xregistry/spec)
- [Code Generator GitHub Repository](https://github.com/xregistry/codegen)
- [Sample Message Catalogs](https://github.com/xregistry/codegen/tree/main/samples/message-definitions)

## License

Apache 2.0