# xRegistry Code Generation CLI - AI Coding Agent Guide

## Project Overview

The xRegistry Code Generation CLI (`xregistry` / `xcg`) is a Python-based tool that generates production-ready, type-safe messaging/eventing SDKs from [xRegistry](https://xregistry.io/) message catalog definitions. It's not a simple code snippet generator—it produces complete, compile-ready projects with tests, dependency management, and Docker-based integration tests.

**Core Architecture:** Template-driven code generation using Jinja2 extensions → Schema conversion via [Avrotize](https://github.com/clemensv/avrotize) → Multi-language SDK output (C#, Java, Python, TypeScript).

## Essential Knowledge

### 1. The Two Operating Modes

- **Manifest Mode** (`xcg manifest`): Works with local JSON/YAML files containing xRegistry definitions (offline, Git-friendly)
- **Catalog Mode** (`xcg catalog`): Interacts with remote xRegistry HTTP APIs (team collaboration, currently supports [xreg-github](https://github.com/duglin/xreg-github/))

### 2. xRegistry Document Structure

You need to understand these documents:

- https://raw.githubusercontent.com/xregistry/spec/refs/heads/main/core/spec.md
- https://raw.githubusercontent.com/xregistry/spec/refs/heads/main/schema/spec.md
- https://raw.githubusercontent.com/xregistry/spec/refs/heads/main/message/spec.md
- https://raw.githubusercontent.com/xregistry/spec/refs/heads/main/endpoint/spec.md

xRegistry documents that we handle here in particular contain three interconnected catalogs:

```
/schemagroups/{id}/schemas/{id}        ← Schema definitions (JSON Schema, Avro, Protobuf)
/messagegroups/{id}/messages/{id}      ← Message definitions (CloudEvents envelopes + schemas)
/endpointgroups/{id}/endpoints/{id}    ← Protocol endpoints (AMQP, MQTT, Kafka, HTTP)
```

**Critical:** Message definitions reference schemas via JSON Pointers (e.g., `/schemagroups/devices/schemas/temperature`). Endpoints reference message groups. The generator follows these references to build complete SDKs.

### 3. Template System Architecture

```
xregistry/templates/
├── {language}/           # cs, java, py, ts, asaql, asyncapi, openapi
│   ├── _templateinfo.json          # Language metadata (priority, description)
│   ├── _common/                    # Shared Jinja macros
│   │   ├── amqp.jinja.include
│   │   ├── cloudevents.jinja.include
│   │   └── mqtt.jinja.include
│   └── {style}/                    # producer, consumer, kafkaproducer, ehconsumer, etc.
│       ├── _templateinfo.json      # Style metadata (main_project_name, data_project_name, src_layout)
│       └── *.jinja                 # Template files (use {projectdir}, {projectname} placeholders)
```

**Template Resolution:** Custom templates (via `--templates`) override built-in templates by matching `{language}/{style}` paths. Templates use special filename placeholders like `{projectdir}`, `{projectname}` that the renderer expands.

**See:** [`docs/authoring_templates.md`](../docs/authoring_templates.md) for complete template authoring guide.

### 4. Core Generation Pipeline

1. **XRegistryLoader** (`xregistry/generator/xregistry_loader.py`): Loads and validates xRegistry documents, performs **basemessage resolution** (transitive inheritance via `basemessageurl` attribute—see [`docs/basemessage_resolution.md`](../docs/basemessage_resolution.md))
2. **ResourceProcessor** (`xregistry/generator/resource_processor.py`): Traverses document, filters by `--messagegroup` or `--endpoint`, resolves JSON Pointer references
3. **SchemaProcessor** (`xregistry/generator/schema_processor.py`): Collects schemas, queues them for Avrotize conversion (JSON Schema ↔ Avro ↔ Protobuf)
4. **TemplateRenderer** (`xregistry/generator/template_renderer.py`): Renders Jinja2 templates with custom filters (pascal/camel/snake case, regex ops—see `xregistry/generator/jinja_filters.py`)
5. **Avrotize Integration**: Batch-converts schemas to target language using `avrotize` library, generates data classes

### 5. Command Structure & Configuration

**Primary commands:**
```bash
xcg generate --projectname MyProject --language cs --style producer --definitions ./my-catalog.json --output ./out
xcg validate --definitions ./my-catalog.json
xcg list --templates ./custom-templates      # Enumerate available templates
xcg config set defaults.language cs           # Persist defaults to platform-specific config
xcg manifest messagegroup add --manifest ./catalog.json --id orders
xcg catalog endpoint get --id orders-endpoint # Requires registry.base_url config
```

**Config precedence:** CLI args → `xcg config` values → environment (`XREGISTRY_MODEL_PATH`) → defaults

**Config storage:** `%APPDATA%\xregistry\config.json` (Windows) / `~/.config/xregistry/config.json` (Linux/Mac)

## Testing Best Practices

### Critical: Full Test Suite Takes 30+ Minutes

**ALWAYS** follow these rules (enforced in [`.github/instructions/pytest-runs.instructions.md`](instructions/pytest-runs.instructions.md)):

1. **Never run full suite** unless explicitly requested—target specific tests
2. **Always redirect output to file** in `{rootdir}/tmp` to preserve error details:
   ```bash
   pytest test/py/test_python.py::test_kafkaproducer_contoso_erp_py > tmp/test_output.txt 2>&1
   ```
3. **Do NOT use** `Select-String` or `grep` on live output—this loses stack traces

### Test Organization

- `test/codegen/test_codegen.py`: Core template rendering and generation logic
- `test/{language}/test_{language}.py`: Language-specific generated code compilation/execution
- `test/core/test_basemessage_resolution.py`: Message inheritance validation
- Generated tests use **testcontainers** (Docker) for MQTT, Kafka, AMQP brokers

**See:** [`test/KNOWN_TEST_ISSUES.md`](../test/KNOWN_TEST_ISSUES.md) for skipped tests and environment issues (e.g., EventHub emulator flakiness on Windows).

## Development Setup

**Python:** 3.10+ required

**External dependencies for testing generated code:**
- .NET SDK 6.0+ (C# templates)
- OpenJDK 17+ (Java templates)
- Node.js 14+ (TypeScript templates)
- Docker (testcontainers)
- Azure Functions Core Tools, AsyncAPI CLI, OpenAPI Generator CLI (for validation)

**C# dependency:** Requires building experimental CloudEvents extension from [CloudNative.CloudEvents.Endpoints](https://github.com/clemensv/CloudNative.CloudEvents.Endpoints/) and setting `CEDISCO_NUGET_LOCAL_FEED` env var.

**Java dependency:** Build [io.cloudevents.experimental.endpoints](https://github.com/clemensv/io.cloudevents.experimental.endpoints) with `mvn install`.

**See:** [`docs/development_environment.md`](../docs/development_environment.md) for complete setup.

## Common Workflows

### Adding a New Template Style

1. Create directory: `xregistry/templates/{language}/{new-style}/`
2. Add `_templateinfo.json` with `description`, `priority`, `main_project_name`, `data_project_name`
3. Add Jinja templates (use existing styles as reference—copy from `producer` or `consumer`)
4. Add test case in `test/{language}/test_{language}.py` using sample definitions from `samples/message-definitions/`
5. Run targeted test: `pytest test/{language}/test_{language}.py::test_{style}_{sample}_{lang} > tmp/output.txt 2>&1`

### Debugging Template Rendering

- Enable debug logging: Set `logging.basicConfig(level=logging.DEBUG)` in `xregistry/cli.py`
- Check context variables: Templates receive `root_document`, `messagegroup`, `endpoint`, `message`, `schema` variables
- Use `{% do log(variable) %}` in templates to debug (via `JinjaExtensions.log`)
- Inspect rendered output before compilation—generated code is in `--output` dir

### Extending Schema Support

Schema conversion is handled by **Avrotize**—don't reinvent schema translation logic. The `SchemaProcessor` queues schemas and batch-processes them via `avrotize.avrotize()`. To add new schema formats, extend Avrotize first, then update `SchemaProcessor._get_schema_format_short()`.

## Project-Specific Conventions

- **No file duplication:** Utility scripts go in `/tmp`, not new project files. Update existing files, don't create summaries.
- **Jinja2 extensions:** Use custom filters (`pascal`, `camel`, `snake`, `strip_invalid_identifier_characters`, `regex_replace`) from `JinjaFilters` class—these are critical for cross-language identifier translation.
- **CloudEvents-centric:** Message definitions are modeled on CloudEvents spec. Envelope metadata uses CE attributes (`type`, `source`, `subject`).
- **JSON Pointer navigation:** Use `jsonpointer.JsonPointer()` for document traversal (see `ResourceProcessor.resolve_resource_reference()`).
- **Context stacks:** `ContextStacksManager` tracks nested Jinja rendering contexts—don't use Python `with` statements for context management in templates.

## Key Files Reference

| File | Purpose |
|------|---------|
| `xregistry/cli.py` | Argument parsing, subcommand registration |
| `xregistry/commands/generate_code.py` | Entry point for code generation |
| `xregistry/generator/template_renderer.py` | Core rendering engine (~1100 lines) |
| `xregistry/generator/xregistry_loader.py` | Document loading, basemessage resolution |
| `xregistry/generator/jinja_filters.py` | Custom Jinja2 filters (case conversion, regex) |
| `xregistry/common/model.py` | xRegistry model schema definitions |
| `samples/message-definitions/*.xreg.json` | Test fixtures (Contoso ERP, Inkjet, etc.) |

## Anti-Patterns to Avoid

- ❌ Generating partial/uncompilable code—always produce full projects with build files
- ❌ Using `async for` over dict fixtures in tests—use `.values()` or `.items()`
- ❌ Calling `pytest` without output redirection—30+ minute runs without error capture
- ❌ Creating new files for fixes/summaries—modify existing files per instructions
- ❌ Ignoring `_templateinfo.json` metadata—priority affects UI ordering in VS Code extension
- ❌ Hardcoding language-specific logic in generator—use templates and filters

## Resources

- [xRegistry Spec](https://github.com/xregistry/spec) – Protocol documentation
- [Avrotize](https://github.com/clemensv/avrotize) – Schema conversion library
- [CloudEvents](https://cloudevents.io) – Event envelope specification
- VS Code Extension: `xregistry_vscode/` (separate package using this CLI)
