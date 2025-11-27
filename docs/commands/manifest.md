# Manifest Command

The `manifest` command manages xRegistry definition files locally. Use it to create, modify, and query xRegistry documents stored as JSON files on your filesystem.

## Synopsis

```bash
xrcg manifest <resource> <action> [options]
```

## Resources and Actions

| Resource | Available Actions |
|----------|-------------------|
| `messagegroup` | `add`, `get`, `update`, `delete`, `list` |
| `message` | `add`, `get`, `update`, `delete`, `list` |
| `schemagroup` | `add`, `get`, `update`, `delete`, `list` |
| `schema` | `add`, `get`, `update`, `delete`, `list` |
| `endpoint` | `add`, `get`, `update`, `delete`, `list` |

## Common Options

| Option | Description |
|--------|-------------|
| `--manifest`, `-m` | Path to the manifest file (JSON). Created if it doesn't exist. |
| `--format` | Output format: `json` (default) or `yaml` |

## Message Groups

Message groups contain related message definitions that share common characteristics.

### Add a Message Group

```bash
xrcg manifest messagegroup add \
  --manifest ./catalog.json \
  --id "Contoso.Orders" \
  --envelope "CloudEvents/1.0" \
  --description "Order-related events"
```

Options:
| Option | Required | Description |
|--------|----------|-------------|
| `--id` | Yes | Unique identifier for the message group |
| `--envelope` | No | Envelope format (e.g., `CloudEvents/1.0`) |
| `--description` | No | Human-readable description |
| `--documentation` | No | URL to external documentation |

### List Message Groups

```bash
xrcg manifest messagegroup list --manifest ./catalog.json
```

### Get a Message Group

```bash
xrcg manifest messagegroup get \
  --manifest ./catalog.json \
  --id "Contoso.Orders"
```

### Update a Message Group

```bash
xrcg manifest messagegroup update \
  --manifest ./catalog.json \
  --id "Contoso.Orders" \
  --description "Updated description"
```

### Delete a Message Group

```bash
xrcg manifest messagegroup delete \
  --manifest ./catalog.json \
  --id "Contoso.Orders"
```

## Messages

Messages define the structure of events or commands within a message group.

### Add a Message

```bash
xrcg manifest message add \
  --manifest ./catalog.json \
  --messagegroupid "Contoso.Orders" \
  --id "OrderPlaced" \
  --description "Raised when a new order is placed" \
  --schemaurl "#/schemagroups/Contoso.Schemas/schemas/OrderData"
```

Options:
| Option | Required | Description |
|--------|----------|-------------|
| `--messagegroupid` | Yes | Parent message group ID |
| `--id` | Yes | Unique message identifier |
| `--description` | No | Human-readable description |
| `--schemaurl` | No | JSON Pointer to the message payload schema |
| `--schemaformat` | No | Schema format (e.g., `JsonSchema/draft-07`) |
| `--basemessageurl` | No | JSON Pointer to a base message for inheritance |

### CloudEvents Metadata

For CloudEvents envelope, add metadata:

```bash
xrcg manifest message add \
  --manifest ./catalog.json \
  --messagegroupid "Contoso.Orders" \
  --id "OrderPlaced" \
  --metadata-type "com.contoso.orders.placed" \
  --metadata-source "/orders/{orderid}" \
  --metadata-subject "orders"
```

### List Messages

```bash
xrcg manifest message list \
  --manifest ./catalog.json \
  --messagegroupid "Contoso.Orders"
```

### Get a Message

```bash
xrcg manifest message get \
  --manifest ./catalog.json \
  --messagegroupid "Contoso.Orders" \
  --id "OrderPlaced"
```

## Schema Groups

Schema groups organize related schemas together.

### Add a Schema Group

```bash
xrcg manifest schemagroup add \
  --manifest ./catalog.json \
  --id "Contoso.Schemas" \
  --description "Data schemas for Contoso services"
```

### List Schema Groups

```bash
xrcg manifest schemagroup list --manifest ./catalog.json
```

## Schemas

Schemas define the structure of message payloads.

### Add a Schema

```bash
xrcg manifest schema add \
  --manifest ./catalog.json \
  --schemagroupid "Contoso.Schemas" \
  --id "OrderData" \
  --format "JsonSchema/draft-07" \
  --schema-file ./schemas/order.json
```

Options:
| Option | Required | Description |
|--------|----------|-------------|
| `--schemagroupid` | Yes | Parent schema group ID |
| `--id` | Yes | Unique schema identifier |
| `--format` | Yes | Schema format: `JsonSchema/draft-07`, `Avro`, `Protobuf` |
| `--schema-file` | No | Path to schema file |
| `--schema` | No | Inline schema content (JSON string) |

### Add Schema with Inline Content

```bash
xrcg manifest schema add \
  --manifest ./catalog.json \
  --schemagroupid "Contoso.Schemas" \
  --id "OrderData" \
  --format "JsonSchema/draft-07" \
  --schema '{"type": "object", "properties": {"orderId": {"type": "string"}}}'
```

### List Schemas

```bash
xrcg manifest schema list \
  --manifest ./catalog.json \
  --schemagroupid "Contoso.Schemas"
```

## Endpoints

Endpoints define where and how messages are sent or received.

### Add an Endpoint

```bash
xrcg manifest endpoint add \
  --manifest ./catalog.json \
  --id "Orders.Kafka" \
  --protocol "Kafka" \
  --usage "producer" \
  --messagegroups "#/messagegroups/Contoso.Orders"
```

Options:
| Option | Required | Description |
|--------|----------|-------------|
| `--id` | Yes | Unique endpoint identifier |
| `--protocol` | Yes | Protocol: `HTTP`, `AMQP/1.0`, `MQTT/5.0`, `Kafka` |
| `--usage` | Yes | Role: `producer`, `consumer`, or `subscriber` |
| `--messagegroups` | No | JSON Pointer(s) to message groups (comma-separated) |
| `--channel` | No | Channel/topic/queue name |

### Protocol-Specific Options

```bash
# Kafka endpoint with topic
xrcg manifest endpoint add \
  --manifest ./catalog.json \
  --id "Orders.Kafka" \
  --protocol "Kafka" \
  --usage "producer" \
  --channel "orders-topic" \
  --messagegroups "#/messagegroups/Contoso.Orders"

# AMQP endpoint with queue
xrcg manifest endpoint add \
  --manifest ./catalog.json \
  --id "Orders.AMQP" \
  --protocol "AMQP/1.0" \
  --usage "consumer" \
  --channel "orders-queue" \
  --messagegroups "#/messagegroups/Contoso.Orders"
```

### List Endpoints

```bash
xrcg manifest endpoint list --manifest ./catalog.json
```

## Complete Workflow Example

Create a complete xRegistry document from scratch:

```bash
# 1. Create schema group and schema
xrcg manifest schemagroup add \
  --manifest ./my-catalog.json \
  --id "MyApp.Schemas"

xrcg manifest schema add \
  --manifest ./my-catalog.json \
  --schemagroupid "MyApp.Schemas" \
  --id "UserData" \
  --format "JsonSchema/draft-07" \
  --schema '{"type": "object", "properties": {"userId": {"type": "string"}, "email": {"type": "string"}}}'

# 2. Create message group and messages
xrcg manifest messagegroup add \
  --manifest ./my-catalog.json \
  --id "MyApp.UserEvents" \
  --envelope "CloudEvents/1.0"

xrcg manifest message add \
  --manifest ./my-catalog.json \
  --messagegroupid "MyApp.UserEvents" \
  --id "UserCreated" \
  --schemaurl "#/schemagroups/MyApp.Schemas/schemas/UserData" \
  --metadata-type "com.myapp.user.created"

xrcg manifest message add \
  --manifest ./my-catalog.json \
  --messagegroupid "MyApp.UserEvents" \
  --id "UserDeleted" \
  --metadata-type "com.myapp.user.deleted"

# 3. Create endpoint
xrcg manifest endpoint add \
  --manifest ./my-catalog.json \
  --id "Users.Kafka" \
  --protocol "Kafka" \
  --usage "producer" \
  --channel "user-events" \
  --messagegroups "#/messagegroups/MyApp.UserEvents"

# 4. Validate
xrcg validate --definitions ./my-catalog.json

# 5. Generate code
xrcg generate \
  --projectname MyApp \
  --language py \
  --style kafkaproducer \
  --definitions ./my-catalog.json \
  --output ./generated
```

## Output Formats

### JSON (Default)

```bash
xrcg manifest messagegroup get \
  --manifest ./catalog.json \
  --id "Contoso.Orders" \
  --format json
```

### YAML

```bash
xrcg manifest messagegroup get \
  --manifest ./catalog.json \
  --id "Contoso.Orders" \
  --format yaml
```

## File Creation

If the manifest file doesn't exist, it will be created with proper xRegistry structure:

```bash
# Creates new file with initial structure
xrcg manifest messagegroup add \
  --manifest ./new-catalog.json \
  --id "MyApp.Events"
```

Initial file content:
```json
{
  "$schema": "https://xregistry.io/schema/xregistry",
  "specversion": "1.0",
  "messagegroups": {
    "MyApp.Events": {
      "messagegroupid": "MyApp.Events"
    }
  }
}
```

## See Also

- [Catalog Command](catalog.md) - Manage remote xRegistry registries
- [Validate Command](validate.md) - Validate manifest files
- [Generate Command](generate.md) - Generate code from manifests
