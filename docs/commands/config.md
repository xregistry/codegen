# Config Command

The `config` command manages persistent configuration settings for the xRegistry CLI. Use it to set default values, configure registry connections, and customize tool behavior.

## Synopsis

```bash
xrcg config <subcommand> [options]
```

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `list` | Display all configuration settings |
| `get <key>` | Get a specific configuration value |
| `set <key> <value>` | Set a configuration value |
| `unset <key>` | Remove a configuration value |
| `reset` | Reset all configuration to defaults |

## Configuration File Location

Configuration is stored in a JSON file at a platform-specific location:

| Platform | Location |
|----------|----------|
| **Linux** | `~/.config/xrcg/config.json` |
| **macOS** | `~/Library/Application Support/xrcg/config.json` |
| **Windows** | `%APPDATA%\xrcg\config.json` |

## Available Configuration Keys

### Default Values

These settings provide default values for `generate` command options:

| Key | Description | Example |
|-----|-------------|---------|
| `defaults.project_name` | Default project name | `MyProject` |
| `defaults.language` | Default target language | `java`, `cs`, `py`, `ts` |
| `defaults.style` | Default code style | `kafkaproducer` |
| `defaults.output_dir` | Default output directory | `./generated` |

### Registry Connection

Settings for connecting to remote xRegistry catalogs:

| Key | Description | Example |
|-----|-------------|---------|
| `registry.base_url` | Base URL for the registry API | `https://registry.example.com` |
| `registry.auth_token` | Authentication token (Bearer) | `eyJhbGc...` |
| `registry.timeout` | HTTP timeout in seconds | `30` |

### Model Settings

| Key | Description | Example |
|-----|-------------|---------|
| `model.url` | Custom xRegistry model schema URL | `https://example.com/model.json` |
| `model.cache_timeout` | Cache duration in seconds | `3600` |

## Examples

### View All Configuration

```bash
xrcg config list
```

Output:
```
Configuration (from ~/.config/xrcg/config.json):

defaults:
  language: java
  output_dir: ./generated

registry:
  base_url: https://registry.example.com
  timeout: 30
```

### Export as JSON

```bash
xrcg config list --format json
```

Output:
```json
{
  "defaults": {
    "language": "java",
    "output_dir": "./generated"
  },
  "registry": {
    "base_url": "https://registry.example.com",
    "timeout": 30
  }
}
```

### Get a Specific Value

```bash
xrcg config get defaults.language
```

Output:
```
java
```

### Set Default Values

```bash
# Set default language
xrcg config set defaults.language java

# Set default output directory
xrcg config set defaults.output_dir ./generated

# Set multiple defaults
xrcg config set defaults.project_name MyProject
xrcg config set defaults.style kafkaproducer
```

Now you can run generate with fewer arguments:

```bash
# Before: all options required
xrcg generate --projectname MyProject --language java --style kafkaproducer \
  --definitions ./catalog.json --output ./generated

# After: using defaults
xrcg generate --definitions ./catalog.json
```

### Configure Registry Connection

```bash
# Set registry URL
xrcg config set registry.base_url https://registry.example.com

# Set authentication token
xrcg config set registry.auth_token "eyJhbGciOiJIUzI1NiIs..."

# Set timeout
xrcg config set registry.timeout 60
```

### Remove a Setting

```bash
# Remove a specific setting
xrcg config unset defaults.language

# Verify it's removed
xrcg config get defaults.language
# Output: (not set)
```

### Reset All Configuration

```bash
xrcg config reset
```

Output:
```
Configuration reset to defaults.
```

## Configuration Precedence

Command-line arguments always take precedence over configuration file settings:

1. **Command-line arguments** (highest priority)
2. **Configuration file** (`config.json`)
3. **Environment variables** (where applicable)
4. **Built-in defaults** (lowest priority)

Example:
```bash
# Config has: defaults.language = java
# This command uses Python despite the config:
xrcg generate --language py --definitions ./catalog.json --output ./out
```

## Environment Variables

Some settings can also be set via environment variables:

| Environment Variable | Equivalent Config Key |
|---------------------|----------------------|
| `XREGISTRY_MODEL_PATH` | `model.url` |
| `XREGISTRY_REGISTRY_URL` | `registry.base_url` |

Environment variables take precedence over config file but are overridden by CLI arguments.

## Security Considerations

### Protecting Sensitive Data

The `registry.auth_token` is stored in plain text. For production use:

1. **Use environment variables** for tokens in CI/CD:
   ```bash
   export XREGISTRY_AUTH_TOKEN="..."
   ```

2. **Use credential helpers** (future feature)

3. **Restrict file permissions**:
   ```bash
   chmod 600 ~/.config/xrcg/config.json
   ```

### Token Rotation

When rotating tokens:

```bash
# Update the token
xrcg config set registry.auth_token "new-token-value"

# Verify connection
xrcg catalog endpoint list
```

## Troubleshooting

### Config File Not Found

If you see "Configuration file not found", run any `set` command to create it:

```bash
xrcg config set defaults.language java
```

### Permission Denied

On Unix systems, check file permissions:

```bash
ls -la ~/.config/xrcg/config.json
chmod 600 ~/.config/xrcg/config.json
```

### Invalid JSON

If the config file becomes corrupted:

```bash
# Reset to defaults
xrcg config reset

# Or manually delete and recreate
rm ~/.config/xrcg/config.json
xrcg config set defaults.language java
```

## See Also

- [Generate Command](generate.md) - Uses configuration defaults
- [Catalog Command](catalog.md) - Uses registry connection settings
- [Manifest Command](manifest.md) - Local file operations (no registry needed)
