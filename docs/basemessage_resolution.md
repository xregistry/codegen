# Basemessage Resolution Feature

This document describes the basemessage resolution feature implemented in the xRegistry Code Generation CLI, which follows the [xRegistry Message Specification](https://github.com/xregistry/spec/blob/main/message/spec.md#reusing-message-definitions).

## Overview

The `basemessageurl` attribute allows message definitions to inherit from other message definitions, enabling reuse and reducing repetition in message catalogs. This is particularly useful for:

- Defining common message attributes across multiple related messages
- Creating protocol-specific variants of envelope-only messages
- Building message hierarchies for related event types

## How It Works

### Basic Inheritance

When a message definition includes a `basemessageurl` attribute, the xRegistry loader:

1. Resolves the reference to the base message
2. Deep-merges the base message attributes with the current message
3. Attributes in the current message shadow/override those from the base
4. Removes the `basemessageurl` attribute after resolution

### Transitive Resolution

The resolution process is transitive - if the base message itself has a `basemessageurl`, the chain is followed until a message with no base is found. The attributes are then merged from the root of the chain down to the final message.

### Circular Reference Detection

The loader detects circular references (e.g., MessageA → MessageB → MessageA) and prevents infinite loops. When a circular reference is detected, an error is logged but the message is not removed from the document.

### Missing References

Per the xRegistry spec, if a referenced base message cannot be found, no error is generated. The message is processed as if it had no base, with the `basemessageurl` attribute removed.

## Usage Example

```json
{
  "messagegroups": {
    "devices": {
      "messagegroupid": "devices",
      "envelope": "CloudEvents/1.0",
      "messages": {
        "BaseDeviceEvent": {
          "messageid": "BaseDeviceEvent",
          "description": "Base event for all device events",
          "envelope": "CloudEvents/1.0",
          "envelopemetadata": {
            "source": {
              "value": "/devices/{deviceid}",
              "type": "uritemplate"
            },
            "datacontenttype": {
              "value": "application/json"
            }
          },
          "dataschemaformat": "JSONSchema/draft-07"
        },
        "SensorEvent": {
          "messageid": "SensorEvent",
          "description": "Event from sensor devices",
          "basemessageurl": "/messagegroups/devices/messages/BaseDeviceEvent",
          "envelope": "CloudEvents/1.0",
          "envelopemetadata": {
            "type": {
              "value": "com.example.device.sensor"
            },
            "subject": {
              "value": "/sensors/{sensorid}",
              "type": "uritemplate"
            }
          }
        },
        "TemperatureSensorEvent": {
          "messageid": "TemperatureSensorEvent",
          "description": "Temperature sensor reading",
          "basemessageurl": "/messagegroups/devices/messages/SensorEvent",
          "envelope": "CloudEvents/1.0",
          "envelopemetadata": {
            "type": {
              "value": "com.example.device.sensor.temperature"
            }
          }
        }
      }
    }
  }
}
```

After resolution, `TemperatureSensorEvent` will have:
- Its own `type`: `com.example.device.sensor.temperature`
- `subject` inherited from `SensorEvent`: `/sensors/{sensorid}`
- `source` inherited from `BaseDeviceEvent`: `/devices/{deviceid}`
- `datacontenttype` inherited from `BaseDeviceEvent`: `application/json`
- `dataschemaformat` inherited from `BaseDeviceEvent`: `JSONSchema/draft-07`

## CloudEvents Schema References

Generated CloudEvents producers set `dataschema` from the effective
`dataschemauri`, including inherited references. The URI identifies the schema
version selected for payload generation. An explicit envelope `dataschema`
value takes precedence.

File-backed definitions use the `xreg://./` prefix for catalog-local references.
For example, `#/schemagroups/devices/schemas/Temperature` becomes
`xreg://./schemagroups/devices/schemas/Temperature/versions/1` when version `1`
is selected. A document-relative reference such as
`schemas.json#/schemagroups/devices/schemas/Temperature` retains its document
path and fragment after the prefix. Generated URIs never contain the generator's
absolute filesystem path. The `xreg` URI identifies a local catalog resource;
it does not imply an HTTP endpoint.

API-backed definitions use the actual API host and registry prefix. Explicit
absolute schema URIs retain their host and path. Unversioned resource references
gain `/versions/{versionid}`; already pinned references retain their version.
Selection uses the declared default version, including `meta` and
`defaultversionurl`, or the existing lexicographic fallback when no default is
declared. Unresolved references fail generation with the message and reference
in the error.

### Runtime schema URI overrides

Generated producer constructors accept an optional map from the original emitted
`dataschema` URI to its deployment-specific replacement. For example:

```python
producer = ExampleEventProducer(
    client, "readings",
    dataschema_overrides={
        "xreg://./schemagroups/devices/schemas/Temperature/versions/1":
            "https://catalog.example/schemagroups/registered/schemas/Temperature/versions/2"
    },
)
```

The key is the complete, case-sensitive URI that the producer would otherwise
emit, including its version. This can be a generated `xreg://./` URI, an
API-backed URI, or an explicit envelope `dataschema` value. No match preserves
the original. Replacement is one lookup, never a chain of substitutions.
An omitted or empty map preserves existing behavior. Producers copy the map at
construction, so instances do not share mutable overrides.

Overrides apply before binary or structured CloudEvents serialization. They do
not change payload serialization, schema definitions, or plain protocol messages.
The deployment must verify that the replacement identifies a compatible schema;
producers do not fetch or compare schemas. Empty keys or values are rejected.

| Language | Constructor API |
|---|---|
| Python | Optional final `dataschema_overrides` mapping |
| TypeScript | Optional final `dataschemaOverrides` record; the Event Grid credential argument can be `undefined` |
| Go | Optional final variadic `map[string]string`; supply at most one map |
| Java | Optional final variadic `Map<String, String>` on constructors; supply at most one map |
| C# | Optional final `IReadOnlyDictionary<string, string>? dataschemaOverrides` |
| Rust | `new_with_dataschema_overrides` or `with_client_and_dataschema_overrides`, taking an owned `HashMap<String, String>` |

Factory-backed transports forward the instance map into event construction.
Java's generic event factory accepts the map in its constructor. The C# Service
Bus style emits a factory rather than a sender: construct it with the map and
call `Create<Event>EventWithOverrides`, or pass the optional map to its existing
static `Create<Event>Event` methods. Other static C#/Java message factories also
accept a final map. C# AMQP's builder offers `WithDataschemaOverrides`.

Go's pointer-only constructors cannot return configuration errors; invalid
override maps panic. Other languages report invalid constructor configuration
through their normal exception or `Result` paths.

## Endpoint Message Inheritance

The basemessage mechanism also applies to messages embedded in endpoint definitions:

```json
{
  "endpoints": {
    "device-telemetry": {
      "endpointid": "device-telemetry",
      "usage": ["producer"],
      "protocol": "HTTP",
      "messages": {
        "ActuatorEvent": {
          "messageid": "ActuatorEvent",
          "description": "Event from actuator devices",
          "basemessageurl": "/messagegroups/devices/messages/BaseDeviceEvent",
          "envelope": "CloudEvents/1.0",
          "envelopemetadata": {
            "type": {
              "value": "com.example.device.actuator"
            }
          }
        }
      }
    }
  }
}
```

## Deep Merge Behavior

When merging attributes, the process is "deep" for nested objects:

**Base Message:**
```json
{
  "envelopemetadata": {
    "type": {
      "value": "base.type",
      "required": true
    },
    "source": {
      "value": "base.source"
    }
  }
}
```

**Derived Message:**
```json
{
  "basemessageurl": "/messagegroups/group/messages/Base",
  "envelopemetadata": {
    "type": {
      "value": "derived.type"
    }
  }
}
```

**Result after resolution:**
```json
{
  "envelopemetadata": {
    "type": {
      "value": "derived.type",      // overridden
      "required": true              // inherited
    },
    "source": {
      "value": "base.source"        // completely inherited
    }
  }
}
```

## Testing

Comprehensive unit tests are provided in `test/core/test_basemessage_resolution.py` covering:

- Simple basemessage resolution
- Transitive chain resolution
- Circular reference detection
- Missing reference handling
- Endpoint message inheritance
- Deep merge with nested objects

Run tests with:
```bash
python -m pytest test/core/test_basemessage_resolution.py -v
```

## Implementation Details

The basemessage resolution is implemented in the `MessageResolver` class in `xregistry/generator/xregistry_loader.py`. The resolution happens after resource resolution (schemas, etc.) but before any filtering is applied.

The resolution process is called automatically by:
- `XRegistryLoader.load()` - basic document loading
- `XRegistryLoader.load_stacked()` - stacked document loading
- `XRegistryLoader.load_with_dependencies()` - dependency-resolved loading

This ensures that basemessage references are always resolved regardless of how the document is loaded.
