# Validate Command

The `validate` command checks xRegistry definition files for structural correctness and schema compliance. Use this command to verify your definitions before generating code.

## Synopsis

```bash
xrcg validate --definitions <file-or-url> [options]
```

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--definitions`, `-d` | Yes | Path to a local file or URL containing xRegistry definitions (JSON or YAML). |
| `--requestheaders` | No | HTTP headers for fetching remote definitions, as `key=value`. Useful for authenticated endpoints. |

## What Gets Validated

The validator checks:

### Document Structure

- Valid JSON/YAML syntax
- Required top-level properties (`$schema`, `specversion`)
- Proper structure of `messagegroups`, `schemagroups`, and `endpoints`

### Message Groups

- Valid `messagegroupid` identifiers
- Proper `envelope` specification (e.g., `CloudEvents/1.0`)
- Message definitions with required fields
- Valid `envelopemetadata` structure

### Schema Groups

- Valid `schemagroupid` identifiers
- Schema format specification (`JsonSchema/draft-07`, `Avro`, `Protobuf`)
- Schema version management
- Resolvable schema references

### Endpoints

- Valid `endpointid` identifiers
- Protocol specification (`HTTP`, `AMQP/1.0`, `MQTT/5.0`, `Kafka`)
- Message group references (JSON Pointers)
- Protocol-specific options

### Cross-References

- JSON Pointer references resolve correctly (e.g., `#/schemagroups/foo/schemas/bar`)
- `basemessageurl` references for message inheritance
- Schema references from messages

## Examples

### Validate a Local File

```bash
xrcg validate --definitions ./my-catalog.json
```

Output on success:
```
✓ Validation passed: ./my-catalog.json
  - 3 message groups
  - 2 schema groups
  - 4 endpoints
```

Output on failure:
```
✗ Validation failed: ./my-catalog.json

Errors:
  - /messagegroups/Orders/messages/OrderPlaced: Missing required field 'envelope'
  - /schemagroups/Schemas/schemas/OrderData: Invalid schema format 'JSONSchema' (expected 'JsonSchema/draft-07')
  - /endpoints/KafkaEndpoint: Unresolved reference '#/messagegroups/NonExistent'
```

### Validate a Remote Definition

```bash
xrcg validate --definitions https://registry.example.com/catalogs/events.json
```

### With Authentication

```bash
xrcg validate \
  --definitions https://registry.example.com/private/catalog.json \
  --requestheaders "Authorization=Bearer mytoken"
```

### Validate Before Generation

A common workflow is to validate before generating:

```bash
# Validate first
xrcg validate --definitions ./catalog.json

# If successful, generate
xrcg generate \
  --projectname MyProject \
  --language py \
  --style kafkaproducer \
  --definitions ./catalog.json \
  --output ./generated
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation passed |
| 1 | Validation failed (errors found) |
| 2 | File not found or network error |

## Common Validation Errors

### Missing Required Fields

```
Error: /messagegroups/Events/messages/UserCreated: Missing required field 'messageid'
```

**Fix:** Add the required `messageid` field to the message definition.

### Invalid Envelope Format

```
Error: /messagegroups/Events: Invalid envelope 'CloudEvents' (expected format like 'CloudEvents/1.0')
```

**Fix:** Use the full envelope specification with version: `CloudEvents/1.0`.

### Unresolved Reference

```
Error: /endpoints/MyEndpoint/messagegroups/0: Cannot resolve '#/messagegroups/NonExistent'
```

**Fix:** Ensure the referenced message group exists in the document.

### Invalid Schema Format

```
Error: /schemagroups/Data/schemas/Order: Unknown schema format 'json-schema'
```

**Fix:** Use a valid format identifier: `JsonSchema/draft-07`, `Avro`, or `Protobuf`.

### Circular Base Message Reference

```
Error: /messagegroups/Events/messages/EventA: Circular reference detected in basemessageurl chain
```

**Fix:** Break the circular dependency in your message inheritance chain.

## Validation vs. Generation

The `validate` command performs structural validation only. It ensures:

- ✓ The document is syntactically correct
- ✓ Required fields are present
- ✓ References are resolvable
- ✓ Types and formats are valid

It does **not** verify:

- ✗ Schema content validity (e.g., JSON Schema semantics)
- ✗ Protocol-specific constraints
- ✗ Business logic rules

For deep schema validation, the `generate` command performs additional checks during schema conversion.

## Integration with CI/CD

Add validation to your pipeline:

```yaml
# GitHub Actions example
- name: Validate xRegistry definitions
  run: |
    xrcg validate --definitions ./catalogs/events.xreg.json
    xrcg validate --definitions ./catalogs/commands.xreg.json
```

```yaml
# Azure Pipelines example
- script: |
    xrcg validate --definitions $(Build.SourcesDirectory)/catalogs/events.xreg.json
  displayName: 'Validate message definitions'
```

## See Also

- [Generate Command](generate.md) - Generate code from validated definitions
- [Manifest Command](manifest.md) - Create and modify xRegistry documents
- [xRegistry Specification](https://github.com/xregistry/spec) - Full specification details
