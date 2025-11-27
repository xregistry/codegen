# List Command

The `list` command displays all available code generation templates organized by language and style.

## Synopsis

```bash
xrcg list [options]
```

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--templates`, `-t` | No | Path to custom template directory. Shows custom templates alongside built-in ones. |

## Output

The command displays a tree structure of available languages and styles:

```
$ xrcg list

Available templates:

├── asaql: Azure Stream Analytics
│   ├── dispatch: Azure Stream Analytics Query Dispatch
│   └── dispatchpayload: Azure Stream Analytics Query Dispatch with Payload
├── py: Python 3.9+
│   ├── mqttclient: Python MQTT 5.0 Client
│   ├── ehconsumer: Python Azure Event Hubs Consumer
│   ├── ehproducer: Python Azure Event Hubs Producer
│   ├── kafkaconsumer: Python Apache Kafka Consumer
│   ├── kafkaproducer: Python Apache Kafka Producer
│   └── producer: Python Generic Producer
├── ts: JavaScript/TypeScript
│   ├── amqpconsumer: TypeScript AMQP 1.0 Consumer
│   ├── amqpproducer: TypeScript AMQP 1.0 Producer
│   ├── egproducer: TypeScript Azure Event Grid Producer
│   ├── ehproducer: TypeScript Azure Event Hubs Producer
│   ├── mqttclient: TypeScript MQTT 5.0 Client
│   ├── sbconsumer: TypeScript Azure Service Bus Consumer
│   ├── sbproducer: TypeScript Azure Service Bus Producer
│   ├── ehconsumer: TypeScript Azure Event Hubs Consumer
│   ├── kafkaconsumer: TypeScript Apache Kafka Consumer
│   └── kafkaproducer: TypeScript Apache Kafka Producer
├── asyncapi: Async API 3.0
│   ├── consumer: AsyncAPI Consumer Definition
│   └── producer: AsyncAPI Producer Definition
├── openapi: Open API 3.0
│   ├── producer: OpenAPI Producer Definition
│   └── subscriber: OpenAPI Subscriber Definition
├── java: Java 21+
│   ├── amqpconsumer: Java AMQP 1.0 Consumer
│   ├── amqpproducer: Java AMQP 1.0 Producer
│   ├── ehconsumer: Java Azure Event Hubs Consumer
│   ├── ehproducer: Java Azure Event Hubs Producer
│   ├── kafkaconsumer: Java Apache Kafka Consumer
│   ├── kafkaproducer: Java Apache Kafka Producer
│   ├── mqttclient: Java MQTT 5.0 Client
│   ├── sbconsumer: Java Azure Service Bus Consumer
│   ├── sbproducer: Java Azure Service Bus Producer
│   ├── consumer: Java Generic Consumer
│   └── producer: Java Generic Producer
└── cs: C# / .NET 6.0+
    ├── egazfn: C# Azure Event Grid Azure Function
    ├── ehazfn: C# Azure Event Hubs Azure Function
    ├── sbazfn: C# Azure Service Bus Azure Function
    ├── amqpconsumer: C# AMQP 1.0 Consumer
    ├── amqpproducer: C# AMQP 1.0 Producer
    ├── egproducer: C# Azure Event Grid Producer
    ├── ehconsumer: C# Azure Event Hubs Consumer
    ├── ehproducer: C# Azure Event Hubs Producer
    ├── kafkaconsumer: C# Apache Kafka Consumer
    ├── kafkaproducer: C# Apache Kafka Producer
    ├── mqttclient: C# MQTT 5.0 Client
    ├── sbconsumer: C# Azure Service Bus Consumer
    └── sbproducer: C# Azure Service Bus Producer
```

## With Custom Templates

When you specify a custom template directory, the output shows both built-in and custom templates:

```bash
xrcg list --templates ./my-templates
```

```
Available templates:

├── java: Java 21+
│   ├── kafkaproducer: Java Apache Kafka Producer
│   ├── kafkaconsumer: Java Apache Kafka Consumer
│   ├── myproducer: My Custom Producer (custom)    ← Custom template
│   └── ...
└── ...
```

## Understanding the Output

### Language Codes

The first level shows language identifiers used with `--language`:

| Code | Description |
|------|-------------|
| `java` | Java 21+ |
| `cs` | C# / .NET 6.0+ |
| `py` | Python 3.9+ |
| `ts` | TypeScript/JavaScript |
| `asyncapi` | AsyncAPI 3.0 specification |
| `openapi` | OpenAPI 3.0 specification |
| `asaql` | Azure Stream Analytics Query Language |

### Style Codes

The second level shows style identifiers used with `--style`. Styles follow a naming convention:

| Pattern | Meaning |
|---------|---------|
| `*producer` | Sends/publishes messages |
| `*consumer` | Receives/subscribes to messages |
| `*client` | Bidirectional (publish and subscribe) |
| `*azfn` | Azure Functions trigger |

### Protocol Prefixes

| Prefix | Protocol |
|--------|----------|
| `kafka*` | Apache Kafka |
| `eh*` | Azure Event Hubs |
| `sb*` | Azure Service Bus |
| `eg*` | Azure Event Grid |
| `amqp*` | AMQP 1.0 |
| `mqtt*` | MQTT 5.0 |

## Using List Output

The `list` command helps you discover valid values for `generate`:

```bash
# Find what styles are available for Python
xrcg list | grep -A 10 "py:"

# Then use the discovered values
xrcg generate --language py --style kafkaproducer ...
```

## Template Priority

Templates are sorted by priority (defined in `_templateinfo.json`). Higher priority templates appear first. This affects ordering in the VS Code extension UI as well.

## See Also

- [Generate Command](generate.md) - Use discovered templates to generate code
- [Authoring Templates](../authoring_templates.md) - Create custom templates
