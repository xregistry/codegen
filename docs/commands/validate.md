# Validate Command

The `validate` command checks xRegistry definition files for structural correctness and schema compliance. Use this command to verify your definitions before generating code.

## Synopsis

```bash
xrcg validate --definitions <file-or-url> [<file-or-url> ...] [options]
```

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--definitions`, `-d` | Yes | One or more local files or URLs containing xRegistry definitions (JSON or YAML). Later documents override matching resources in earlier documents. |
| `--requestheaders` | No | HTTP headers for fetching remote definitions, as `key=value`. Useful for authenticated endpoints. |

## What Gets Validated

The validator checks:

### Document Structure

- Valid JSON/YAML syntax
- Attribute types and required properties declared by the document schema
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
- Mutually exclusive schema content: `schema`, `schemabase64`, or `schemaurl`

### Endpoints

- Valid `endpointid` identifiers
- Protocol specification (`HTTP`, `AMQP/1.0`, `MQTT/5.0`, `Kafka`)
- Message group references (JSON Pointers)
- Protocol-specific options

### References

Validation checks the authored document, or the authored stack of documents.
It does not fetch linked schemas, expand aliases, materialize base messages,
or check whether reference targets exist. Generation resolves those references.

For example, a version with only `schemaurl` is valid. A version containing
both `schemaurl` and `schema` is rejected. Loading a linked schema for generation
does not change the form checked by structural validation.

## Examples

### Validate a Local File

```bash
xrcg validate --definitions ./my-catalog.json
```

Output on success:
```
OK: definitions file(s) ./my-catalog.json is valid
```

Output on failure:
```
./my-catalog.json Validation errors:
! at $.endpoints.KafkaEndpoint.protocol: 123 is not of type 'string'
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

### Reference Errors During Generation

Structural validation does not verify reference targets. Generation can report
an unresolved reference:

```
Error: /endpoints/MyEndpoint/messagegroups/0: Cannot resolve '#/messagegroups/NonExistent'
```

**Fix:** Ensure the referenced message group exists in the document.

### Invalid Schema Format

```
Error: /schemagroups/Data/schemas/Order: Unknown schema format 'json-schema'
```

**Fix:** Use a valid format identifier: `JsonSchema/draft-07`, `Avro`, or `Protobuf`.

### Circular Base Message Reference During Generation

Generation resolves inheritance chains and can report a cycle:

```
Error: /messagegroups/Events/messages/EventA: Circular reference detected in basemessageurl chain
```

**Fix:** Break the circular dependency in your message inheritance chain.

## Validation vs. Generation

The `validate` command performs structural validation only. It ensures:

- ✓ The document is syntactically correct
- ✓ Required fields are present
- ✓ Reference attributes have the required structural form
- ✓ Types and formats are valid

It does **not** verify:

- ✗ Schema content validity (e.g., JSON Schema semantics)
- ✗ Reference targets or inheritance cycles
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
