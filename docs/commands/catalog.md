# Catalog Command

The `catalog` command interacts with remote xRegistry HTTP APIs. Use it for team collaboration, centralized registry management, and integration with CI/CD pipelines.

## Synopsis

```bash
xrcg catalog <resource> <action> [options]
```

## Prerequisites

Before using catalog commands, configure the registry connection:

```bash
xrcg config set registry.base_url https://registry.example.com
xrcg config set registry.auth_token <your-token>
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
| `--registry-url` | Override configured registry URL |
| `--auth-token` | Override configured auth token |
| `--format` | Output format: `json` (default) or `yaml` |

## Supported Registries

The catalog command currently supports:

- [xrserver](https://github.com/xregistry/xrserver/) - Reference xRegistry implementation

## Message Groups

### List Message Groups

```bash
xrcg catalog messagegroup list
```

Output:
```
Message Groups:
  - Contoso.Orders (3 messages)
  - Contoso.Payments (2 messages)
  - Contoso.Shipping (4 messages)
```

### Add a Message Group

```bash
xrcg catalog messagegroup add \
  --id "MyApp.Events" \
  --envelope "CloudEvents/1.0" \
  --description "Application events"
```

### Get a Message Group

```bash
xrcg catalog messagegroup get --id "Contoso.Orders"
```

### Update a Message Group

```bash
xrcg catalog messagegroup update \
  --id "Contoso.Orders" \
  --description "Updated order events"
```

### Delete a Message Group

```bash
xrcg catalog messagegroup delete --id "Contoso.Orders"
```

## Messages

### List Messages in a Group

```bash
xrcg catalog message list --messagegroupid "Contoso.Orders"
```

### Add a Message

```bash
xrcg catalog message add \
  --messagegroupid "Contoso.Orders" \
  --id "OrderPlaced" \
  --description "Raised when order is placed" \
  --schemaurl "#/schemagroups/Schemas/schemas/OrderData"
```

### Get a Message

```bash
xrcg catalog message get \
  --messagegroupid "Contoso.Orders" \
  --id "OrderPlaced"
```

## Schema Groups and Schemas

### Add a Schema Group

```bash
xrcg catalog schemagroup add \
  --id "Schemas" \
  --description "Shared data schemas"
```

### Add a Schema

```bash
xrcg catalog schema add \
  --schemagroupid "Schemas" \
  --id "OrderData" \
  --format "JsonSchema/draft-07" \
  --schema-file ./schemas/order.json
```

### List Schemas

```bash
xrcg catalog schema list --schemagroupid "Schemas"
```

## Endpoints

### List Endpoints

```bash
xrcg catalog endpoint list
```

### Add an Endpoint

```bash
xrcg catalog endpoint add \
  --id "Orders.Kafka" \
  --protocol "Kafka" \
  --usage "producer" \
  --channel "orders" \
  --messagegroups "#/messagegroups/Contoso.Orders"
```

### Get an Endpoint

```bash
xrcg catalog endpoint get --id "Orders.Kafka"
```

## Authentication

### Bearer Token

```bash
# Set token in config
xrcg config set registry.auth_token "eyJhbGciOiJIUzI1..."

# Or pass directly
xrcg catalog messagegroup list --auth-token "eyJhbGciOiJIUzI1..."
```

### Environment Variable

```bash
export XREGISTRY_AUTH_TOKEN="eyJhbGciOiJIUzI1..."
xrcg catalog messagegroup list
```

## Downloading Catalog for Code Generation

A common workflow is to fetch the catalog and generate code:

```bash
# Download catalog to local file
xrcg catalog messagegroup get --id "Contoso.Orders" --format json > orders.json

# Or get everything
curl -H "Authorization: Bearer $TOKEN" \
  https://registry.example.com/messagegroups > catalog.json

# Generate code from downloaded catalog
xrcg generate \
  --projectname ContosoOrders \
  --language java \
  --style kafkaproducer \
  --definitions ./catalog.json \
  --output ./generated
```

## Generating Directly from Registry

You can also generate code directly from a registry URL:

```bash
xrcg generate \
  --projectname ContosoOrders \
  --language java \
  --style kafkaproducer \
  --definitions https://registry.example.com/messagegroups/Contoso.Orders \
  --requestheaders "Authorization=Bearer $TOKEN" \
  --output ./generated
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Generate SDK
on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install xrcg
        run: pip install git+https://github.com/xregistry/codegen.git
      
      - name: Configure registry
        run: |
          xrcg config set registry.base_url ${{ secrets.REGISTRY_URL }}
          xrcg config set registry.auth_token ${{ secrets.REGISTRY_TOKEN }}
      
      - name: List available message groups
        run: xrcg catalog messagegroup list
      
      - name: Generate SDK
        run: |
          xrcg generate \
            --projectname OrdersSDK \
            --language java \
            --style kafkaproducer \
            --definitions ${{ secrets.REGISTRY_URL }}/messagegroups/Orders \
            --requestheaders "Authorization=Bearer ${{ secrets.REGISTRY_TOKEN }}" \
            --output ./sdk
      
      - name: Build SDK
        run: cd sdk && mvn package
```

### Azure DevOps

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'

  - script: pip install git+https://github.com/xregistry/codegen.git
    displayName: 'Install xrcg'

  - script: |
      xrcg generate \
        --projectname $(ProjectName) \
        --language java \
        --style kafkaproducer \
        --definitions $(RegistryUrl)/messagegroups/$(MessageGroup) \
        --requestheaders "Authorization=Bearer $(RegistryToken)" \
        --output ./generated
    displayName: 'Generate SDK'
```

## Error Handling

### Connection Errors

```
Error: Unable to connect to registry at https://registry.example.com
```

**Solutions:**
- Verify the URL is correct
- Check network connectivity
- Ensure the registry is running

### Authentication Errors

```
Error: 401 Unauthorized
```

**Solutions:**
- Verify the auth token is correct
- Check if the token has expired
- Ensure the token has required permissions

### Resource Not Found

```
Error: 404 Not Found - Message group 'NonExistent' does not exist
```

**Solutions:**
- Verify the resource ID is correct
- List available resources first

## Comparison: Catalog vs Manifest

| Feature | Catalog | Manifest |
|---------|---------|----------|
| Storage | Remote server | Local file |
| Collaboration | Multi-user | Single user / Git |
| Network | Required | Not required |
| Version control | Server-managed | Git-managed |
| Use case | Team registries | Local development |

## See Also

- [Manifest Command](manifest.md) - Local file operations
- [Config Command](config.md) - Configure registry connection
- [Generate Command](generate.md) - Generate code from registry
