# Resource Alias Resolution Feature

This document describes the resource alias resolution feature in the xRegistry
Code Generation CLI, which follows the [xRegistry Core Specification —
Cross Referencing Resources](https://github.com/xregistry/spec/blob/main/core/spec.md#cross-referencing-resources).

## Overview

An xRegistry resource can be an **alias** of another, same-typed resource in the
same registry. Instead of declaring its own `versions`/`versionsurl`, an alias
resource carries an `xref` attribute whose value is an XID pointing at the
canonical resource, for example:

```json
{
  "schemagroups": {
    "route": {
      "schemas": {
        "EventData": {
          "meta": { "xref": "/schemagroups/canonical/schemas/EventData" }
        }
      }
    }
  }
}
```

The alias projects the target resource's metadata, versions, default version,
and document through the alias identity.

## How It Works

Alias resolution runs inside the loader during document loading — **before**
validation, schema processing, and template rendering — so aliases are
completely transparent to code generation. Each alias resource is replaced in
place by a deep copy of its target's content, while the alias retains its own
identity (its collection key and `<singular>id`, e.g. `schemaid`/`messageid`).

Because resolution happens before validation, a document whose only otherwise
"invalid" content is an `xref` alias validates cleanly against the document
schema.

### Where `xref` may appear

Both forms are honored:

- A resource-level `xref` attribute.
- An `xref` inside the resource's `meta` sub-object (`meta.xref`) — the form
  emitted when a resource has no versions of its own.

### Model-driven

Resolution is driven by the extension model, so it applies uniformly to every
resource type — `schemas`, `messages`, and any custom resources — without
hard-coding.

### Non-transitive

Per the Core specification, aliases are **not** resolved transitively. An alias
that targets another alias is reported as an error; point aliases at canonical
resources.

## Diagnostics

When an alias cannot be resolved, the loader logs an actionable error and leaves
the alias untouched (so downstream validation still flags the unresolved
resource). Reported conditions are:

- **Malformed target** — the `xref` is not an XID of the form
  `/<group>/<groupid>/<resource>/<resourceid>`.
- **Missing target** — the target XID does not exist in the document.
- **Type mismatch** — the target is a different resource type than the alias.
- **Self-reference** — the `xref` points at the alias itself.
- **Alias-to-alias** — the target is itself an alias (transitive resolution is
  not performed).
