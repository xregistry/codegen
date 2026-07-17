# Generate Command

The `generate` command is the primary function of the xRegistry Code Generation CLI. It transforms xRegistry message catalog definitions into production-ready, type-safe code for various languages and messaging platforms.

## Synopsis

```bash
xrcg generate --projectname <name> --language <lang> --style <style> \
  --definitions <file-or-url> --output <dir> [options]
```

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--projectname`, `-p` | Yes | The project name used for namespaces, package names, and generated class prefixes. Should be a valid identifier (e.g., `MyProject`, `ContosoEvents`). |
| `--language`, `-l` | Yes | Target language for code generation. See [Available Languages](#available-languages). |
| `--style`, `-s` | Yes | The code style/template to use, typically indicating the protocol and role (producer/consumer). See [Available Styles](#available-styles). |
| `--definitions`, `-d` | Yes | Path to a local file or URL containing xRegistry definitions (JSON or YAML). |
| `--output`, `-o` | Yes | Output directory for generated code. Will be created if it doesn't exist. **Warning:** Existing files may be overwritten. |
| `--templates`, `-t` | No | Path to custom template directory. Templates here override built-in templates. |
| `--template-args` | No | Extra arguments passed to templates as `key=value` pairs. Can be specified multiple times. |
| `--requestheaders` | No | HTTP headers for fetching remote definitions, as `key=value`. Useful for authenticated endpoints. |
| `--messagegroup` | No | Filter to generate code for a specific message group only. |
| `--endpoint` | No | Filter to generate code for a specific endpoint only. |

## Available Languages

| Language Code | Description | Runtime Requirements |
|---------------|-------------|---------------------|
| `java` | Java 21+ | JDK 21+, Maven 3.8+ |
| `cs` | C# / .NET | .NET SDK 6.0+ |
| `py` | Python | Python 3.9+ |
| `ts` | TypeScript/JavaScript | Node.js 18+, npm/yarn |
| `go` | Go | Go 1.21+ |
| `rust` | Rust | Rust 1.75+ (cargo) |
| `asyncapi` | AsyncAPI 3.0 specification | None (YAML output) |
| `openapi` | OpenAPI 3.0 specification | None (YAML output) |
| `asaql` | Azure Stream Analytics Query | None (SQL output) |

## Available Styles

Styles determine the protocol binding and whether the generated code is a producer (sends messages) or consumer (receives messages).

### Java Styles

| Style | Description |
|-------|-------------|
| `kafkaproducer` | Apache Kafka producer using kafka-clients |
| `kafkaconsumer` | Apache Kafka consumer using kafka-clients |
| `ehproducer` | Azure Event Hubs producer |
| `ehconsumer` | Azure Event Hubs consumer |
| `sbproducer` | Azure Service Bus producer |
| `sbconsumer` | Azure Service Bus consumer |
| `amqpproducer` | AMQP 1.0 producer (works with RabbitMQ 4+, Artemis, Qpid) |
| `amqpconsumer` | AMQP 1.0 consumer |
| `mqttclient` | MQTT 5.0 client (publish and subscribe) |
| `producer` | Generic producer (abstract base) |
| `consumer` | Generic consumer (abstract base) |

### C# Styles

| Style | Description |
|-------|-------------|
| `kafkaproducer` | Apache Kafka producer using Confluent.Kafka |
| `kafkaconsumer` | Apache Kafka consumer |
| `ehproducer` | Azure Event Hubs producer |
| `ehconsumer` | Azure Event Hubs consumer |
| `ehazfn` | Azure Event Hubs triggered Azure Function |
| `sbproducer` | Azure Service Bus producer |
| `sbconsumer` | Azure Service Bus consumer |
| `sbazfn` | Azure Service Bus triggered Azure Function |
| `egproducer` | Azure Event Grid producer |
| `egazfn` | Azure Event Grid triggered Azure Function |
| `amqpproducer` | AMQP 1.0 producer |
| `amqpconsumer` | AMQP 1.0 consumer |
| `mqttclient` | MQTT 5.0 client |

### Python Styles

| Style | Description |
|-------|-------------|
| `kafkaproducer` | Apache Kafka producer using confluent-kafka |
| `kafkaconsumer` | Apache Kafka consumer |
| `ehproducer` | Azure Event Hubs producer |
| `ehconsumer` | Azure Event Hubs consumer |
| `mqttclient` | MQTT 5.0 client using paho-mqtt |

### TypeScript Styles

| Style | Description |
|-------|-------------|
| `kafkaproducer` | Apache Kafka producer using kafkajs |
| `kafkaconsumer` | Apache Kafka consumer |
| `ehproducer` | Azure Event Hubs producer |
| `ehconsumer` | Azure Event Hubs consumer |
| `sbproducer` | Azure Service Bus producer |
| `sbconsumer` | Azure Service Bus consumer |
| `egproducer` | Azure Event Grid producer |
| `amqpproducer` | AMQP 1.0 producer using rhea |
| `amqpconsumer` | AMQP 1.0 consumer |
| `mqttclient` | MQTT 5.0 client |

### Rust Styles

| Style | Description |
|-------|-------------|
| `producer` | HTTP CloudEvents producer (structured and binary content modes) using reqwest |

Rust data types are generated as a companion Serde-serializable crate. Additional
protocol styles (AMQP, Kafka, MQTT, Event Hubs, Service Bus producers/consumers)
are tracked as follow-up work.

### AsyncAPI/OpenAPI Styles

| Style | Description |
|-------|-------------|
| `producer` | Generates specification for message producers |
| `consumer` | Generates specification for message consumers |
| `subscriber` | (OpenAPI only) CloudEvents subscription endpoint |

## Examples

### Basic Code Generation

Generate a Python Kafka producer:

```bash
xrcg generate \
  --projectname PrinterEvents \
  --language py \
  --style kafkaproducer \
  --definitions ./inkjet.xreg.json \
  --output ./generated
```

### Using Remote Definitions

Fetch definitions from a URL:

```bash
xrcg generate \
  --projectname MyEvents \
  --language java \
  --style ehproducer \
  --definitions https://registry.example.com/catalogs/events.json \
  --output ./generated
```

### With Authentication Headers

For authenticated registry endpoints:

```bash
xrcg generate \
  --projectname MyEvents \
  --language cs \
  --style kafkaconsumer \
  --definitions https://registry.example.com/catalogs/events.json \
  --requestheaders "Authorization=Bearer token123" \
  --output ./generated
```

### Filtering by Message Group

Generate code for a specific message group only:

```bash
xrcg generate \
  --projectname OrderEvents \
  --language java \
  --style kafkaproducer \
  --definitions ./full-catalog.json \
  --messagegroup "Contoso.ERP.OrderEvents" \
  --output ./generated
```

### Using Custom Templates

Override built-in templates with your own:

```bash
xrcg generate \
  --projectname MyEvents \
  --language java \
  --style kafkaproducer \
  --definitions ./catalog.json \
  --templates ./my-custom-templates \
  --output ./generated
```

### Template Arguments

Pass extra arguments to templates:

```bash
# AsyncAPI with binary CloudEvents mode
xrcg generate \
  --language asyncapi \
  --style producer \
  --projectname MyAPI \
  --definitions ./catalog.json \
  --template-args ce_content_mode=binary \
  --output ./generated
```

## Generated Output Structure

The generated output varies by language but typically includes:

### Java Project Structure

```
generated/
├── pom.xml                      # Maven build file with dependencies
├── src/main/java/
│   └── com/example/
│       ├── EventProducer.java   # Main producer class
│       ├── events/              # Generated event classes
│       └── data/                # Data classes from schemas
└── src/test/java/
    └── com/example/
        └── EventProducerTest.java  # Integration tests
```

### Python Project Structure

```
generated/
├── pyproject.toml               # Project metadata and dependencies
├── src/
│   └── printerevents/
│       ├── __init__.py
│       ├── producer.py          # Main producer class
│       ├── events/              # Event type definitions
│       └── data/                # Data classes from schemas
└── tests/
    └── test_producer.py         # Integration tests with testcontainers
```

### C# Project Structure

```
generated/
├── MyProject.csproj             # Project file with NuGet references
├── Program.cs                   # Entry point example
├── EventProducer.cs             # Main producer class
├── Events/                      # Event type definitions
├── Data/                        # Data classes from schemas
└── Tests/
    └── EventProducerTests.cs    # Integration tests
```

## Schema Handling

The generator uses [Avrotize](https://github.com/clemensv/avrotize) to convert schemas between formats. Supported input schemas:

- **JSON Schema** (draft-07, draft-2020-12)
- **Apache Avro**
- **Protocol Buffers** (proto3)

Schemas are automatically converted to the target language's native data structures with proper serialization support.

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Definition file not found` | Invalid path or URL | Verify the `--definitions` path exists |
| `Invalid language` | Unknown language code | Use `xrcg list` to see available languages |
| `Invalid style` | Style not available for language | Check available styles for your language |
| `Schema conversion failed` | Malformed schema in definition | Validate your xRegistry document first |

## See Also

- [Authoring Templates](authoring_templates.md) - Create custom code generation templates
- [Validate Command](validate.md) - Validate xRegistry definitions before generation
- [List Command](list.md) - View available languages and styles
