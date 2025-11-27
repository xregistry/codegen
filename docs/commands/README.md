# Command Reference

The xRegistry Code Generation CLI (`xrcg`) provides commands for generating code, managing xRegistry definitions, and configuring the tool.

## Quick Reference

| Command | Purpose |
|---------|---------|
| [`generate`](generate.md) | Generate type-safe messaging code from xRegistry definitions |
| [`validate`](validate.md) | Check xRegistry definition files for errors |
| [`list`](list.md) | Show available languages and code generation styles |
| [`config`](config.md) | Manage persistent configuration settings |
| [`manifest`](manifest.md) | Create and modify local xRegistry JSON files |
| [`catalog`](catalog.md) | Interact with remote xRegistry HTTP APIs |

## Primary Workflow

```bash
# 1. Generate code from a definition file
xrcg generate --projectname MyApp --language py --style kafkaproducer \
  --definitions ./catalog.json --output ./generated

# 2. Build and run the generated project
cd generated && pip install -e . && pytest
```

## Getting Help

Each command supports `--help`:

```bash
xrcg --help                    # General help
xrcg generate --help           # Generate command options
xrcg manifest --help           # Manifest subcommands
xrcg manifest message --help   # Message operations
```

## Command Categories

### Code Generation

- **[generate](generate.md)** — The main event. Transforms xRegistry definitions into compile-ready projects with type-safe producer/consumer code, data classes, build files, and tests.

- **[list](list.md)** — Discover available language/style combinations. Useful for finding the right `--language` and `--style` values.

- **[validate](validate.md)** — Check your xRegistry documents for structural errors before generating code.

### Definition Management

- **[manifest](manifest.md)** — Work with local xRegistry JSON files. Create message groups, add messages, define schemas, and configure endpoints—all stored in version-controllable files.

- **[catalog](catalog.md)** — Connect to remote xRegistry servers for team collaboration. Same operations as manifest, but against an HTTP API.

### Configuration

- **[config](config.md)** — Store default values (language, output directory) and registry connection settings to avoid repetitive command-line arguments.

## Installation

See the main [README](../../README.md#installation) for installation options (Docker or pip).
