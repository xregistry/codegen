import copy
import os
import re
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Set, Union

import jsonpointer

from xrcg.cli import logger
from xrcg.generator.generator_context import GeneratorContext
from xrcg.generator.jinja_filters import JinjaFilters

JsonNode = Union[Dict[str, 'JsonNode'], List['JsonNode'], str, bool, int, float, None]

class SchemaUtils:
    """Utility class for schema operations."""

    schema_files_collected: Set[str] = set()
    schema_references_collected: Set[str] = set()

    @staticmethod
    def select_schema_version(schema: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        versions = schema.get("versions")
        if not isinstance(versions, dict) or not versions:
            raise RuntimeError("Schema has no versions")
        metadata = schema.get("meta") or {}
        version_id = str(schema.get("defaultversionid") or metadata.get("defaultversionid") or "")
        if not version_id:
            version_url = schema.get("defaultversionurl") or metadata.get("defaultversionurl", "")
            if version_url:
                path = urllib.parse.urlsplit(str(version_url)).path
                version_id = urllib.parse.unquote(path.rstrip("/").rsplit("/", 1)[-1])
        if not version_id:
            version_id = max(versions.keys())
        version = versions.get(version_id)
        if not isinstance(version, dict):
            raise RuntimeError(f"Schema version not found: {version_id}")
        return version_id, version

    @staticmethod
    def registry_base_uri(ctx: GeneratorContext, origin: str) -> str:
        parsed = urllib.parse.urlsplit(origin)
        parts = parsed.path.split("/")
        for index, part in enumerate(parts):
            if part in ctx.loader.model.groups:
                return urllib.parse.urlunsplit((
                    parsed.scheme, parsed.netloc, "/".join(parts[:index]), "", ""))
        return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", ""))

    @staticmethod
    def split_schema_reference(reference: str) -> tuple[str, str]:
        """Separate the optional type selector without splitting URL schemes/ports."""
        document, separator, fragment = reference.partition("#")
        if separator:
            pointer, selector, name = fragment.rpartition(":")
            return (document + "#" + pointer, name) if selector else (reference, "")
        if "://" not in reference and ":" in reference and not re.match(r"^[A-Za-z]:[\\/]", reference):
            return tuple(reference.rsplit(":", 1))
        return reference, ""

    @staticmethod
    def project_schema_references(ctx: GeneratorContext, root: Dict[str, Any],
                                  headers: Optional[Dict[str, str]] = None) -> None:
        """Project effective schema-version references into CloudEvents metadata."""
        if not isinstance(root, dict):
            return

        def project(message: Dict[str, Any], path: str) -> None:
            reference = message.get("dataschemauri")
            if not isinstance(reference, str) or not reference:
                return
            try:
                uri = SchemaUtils.versioned_schema_uri(ctx, root, message, headers or {})
            except Exception as exc:
                raise RuntimeError(
                    f"Cannot resolve dataschema for message {path}: {reference}: {exc}") from exc
            if str(message.get("envelope", "")).lower().startswith("cloudevents"):
                metadata = dict(message.get("envelopemetadata") or {})
                metadata.setdefault("dataschema", {"type": "uri", "value": uri})
                message["envelopemetadata"] = metadata

        def messages(collection: Dict[str, Any], path: str) -> None:
            if not isinstance(collection, dict):
                return
            for name, message in collection.items():
                if isinstance(message, dict):
                    project(message, f"{path}/{name}")
                    if isinstance(message.get("versions"), dict):
                        messages(message["versions"], f"{path}/{name}/versions")

        for group_id, group in root.get("messagegroups", {}).items():
            if isinstance(group, dict):
                messages(group.get("messages", {}), f"/messagegroups/{group_id}/messages")
        for endpoint_id, endpoint in root.get("endpoints", {}).items():
            if isinstance(endpoint, dict):
                messages(endpoint.get("messages", {}), f"/endpoints/{endpoint_id}/messages")

    @staticmethod
    def versioned_schema_uri(ctx: GeneratorContext, root: Dict[str, Any],
                             message: Dict[str, Any], headers: Dict[str, str]) -> str:
        reference = message["dataschemauri"]
        origin = getattr(reference, "origin", "") or ctx.base_uri
        authored, _ = SchemaUtils.split_schema_reference(
            getattr(reference, "authored", str(reference)))
        code_reference, selector = SchemaUtils.split_schema_reference(str(reference))
        is_api = origin.startswith(("http://", "https://"))
        base = SchemaUtils.registry_base_uri(ctx, origin) if is_api else ""

        if code_reference.startswith("#"):
            pointer = urllib.parse.unquote(code_reference[1:])
            schema = jsonpointer.resolve_pointer(root, pointer, None)
            wire_reference = authored
            if is_api:
                wire_reference = base.rstrip("/") + "/" + "/".join(
                    urllib.parse.quote(part, safe="") for part in jsonpointer.JsonPointer(pointer).parts)
                if schema is None:
                    resolved_message = {**message, "dataschemauri": wire_reference}
                    uri = SchemaUtils.versioned_schema_uri(ctx, root, resolved_message, headers)
                    message["dataschemauri"] = resolved_message["dataschemauri"]
                    return uri
        else:
            location, fragment = urllib.parse.urldefrag(authored)
            if urllib.parse.urlsplit(location).scheme in ("http", "https"):
                resolved = location
            elif is_api:
                if location.startswith(("/schemagroups/", "schemagroups/")):
                    resolved = base.rstrip("/") + "/" + location.lstrip("/")
                else:
                    resolved = urllib.parse.urljoin(message.get("self") or origin, location)
            else:
                local_path = (urllib.request.url2pathname(urllib.parse.urlsplit(location).path)
                              if location.startswith("file:") else location)
                resolved = os.path.normpath(os.path.join(os.path.dirname(origin), local_path))
            parsed = urllib.parse.urlsplit(resolved)
            resource_path = parsed.path
            marker = resource_path.find("/schemagroups/")
            pointer = "/" + fragment.lstrip("/") if fragment else (
                resource_path[marker:] if marker >= 0 else "")
            pointer = urllib.parse.unquote(pointer)
            same_registry = is_api and resolved.startswith(base.rstrip("/") + "/")
            schema = jsonpointer.resolve_pointer(root, pointer, None) if same_registry and pointer else None
            if schema is None:
                _, external = ctx.loader._load_core(resolved, headers, ignore_handled=True)
                if external is None:
                    raise RuntimeError(f"Schema document not found: {resolved}")
                schema = jsonpointer.resolve_pointer(external, "/" + fragment.lstrip("/")) if fragment else external
                if pointer.startswith("/schemagroups/"):
                    parts = jsonpointer.JsonPointer(pointer).parts
                    if len(parts) not in (4, 6) or parts[2] != "schemas":
                        raise RuntimeError(f"Not a schema resource/version: {authored}")
                    schemas = root.setdefault("schemagroups", {}).setdefault(parts[1], {}).setdefault("schemas", {})
                    if len(parts) == 6:
                        resource = schemas.setdefault(parts[3], {"versions": {}})
                        versions = resource.setdefault("versions", {})
                        if parts[5] in versions and versions[parts[5]] != schema:
                            raise RuntimeError(f"Conflicting schema version: {authored}")
                        versions.setdefault(parts[5], copy.deepcopy(schema))
                    elif parts[3] not in schemas:
                        schemas[parts[3]] = copy.deepcopy(schema)
                    elif schemas[parts[3]] != schema:
                        raise RuntimeError(f"Conflicting schema resource: {authored}")
            wire_reference = (resolved + ("#" + fragment if fragment else "")) if is_api else authored
            if urllib.parse.urlsplit(authored).scheme in ("http", "https"):
                wire_reference = authored
            elif not is_api and (location.startswith("file:") or os.path.isabs(location)):
                wire_reference = os.path.relpath(
                    resolved, os.path.dirname(os.path.abspath(origin))).replace(os.sep, "/")
                if fragment:
                    wire_reference += "#" + fragment
            if pointer.startswith("/schemagroups/"):
                message["dataschemauri"] = "#" + pointer + (":" + selector if selector else "")

        if not isinstance(schema, dict):
            raise RuntimeError("Schema reference does not identify a schema resource or version")
        version_id = ""
        if "versions" in schema:
            version_id, _ = SchemaUtils.select_schema_version(schema)
        elif "/versions/" not in code_reference and "/versions/" not in authored:
            version_id = str(schema.get("versionid") or "")
            if not version_id:
                raise RuntimeError("Schema reference has no selected version")
        if version_id:
            if "#" in wire_reference:
                token = version_id.replace("~", "~0").replace("/", "~1")
                suffix = "/versions/" + urllib.parse.quote(token, safe="")
                document, fragment = wire_reference.split("#", 1)
                wire_reference = document + "#" + fragment.rstrip("/") + suffix
            else:
                suffix = "/versions/" + urllib.parse.quote(version_id, safe="")
                parsed_wire = urllib.parse.urlsplit(wire_reference)
                wire_reference = urllib.parse.urlunsplit(
                    parsed_wire._replace(path=parsed_wire.path.rstrip("/") + suffix))
        if wire_reference.startswith("file:") or os.path.isabs(wire_reference) and not wire_reference.startswith("/"):
            raise RuntimeError("A local filesystem path cannot be emitted as dataschema")
        if not urllib.parse.urlsplit(wire_reference).scheme:
            if wire_reference.startswith("#/"):
                parts = jsonpointer.JsonPointer(urllib.parse.unquote(wire_reference[1:])).parts
                wire_reference = "/".join(urllib.parse.quote(part, safe="") for part in parts)
            wire_reference = "xreg://./" + wire_reference.lstrip("/")
        return wire_reference

    @staticmethod
    def get_json_pointer(root: JsonNode, node: JsonNode) -> str:
        """Get the JSON Pointer to a node in a JSON document."""
        logger.debug("Getting JSON pointer to node in JSON document")

        def find_path(current: JsonNode, target: JsonNode, path: List[str]) -> Optional[List[str]]:
            if current is target:
                return path
            elif isinstance(current, dict):
                for k, v in current.items():
                    new_path = find_path(v, target, path + [k])
                    if new_path is not None:
                        return new_path
            elif isinstance(current, list):
                for i, item in enumerate(current):
                    new_path = find_path(item, target, path + [str(i)])
                    if new_path is not None:
                        return new_path
            return None

        def path_to_pointer(path: List[str]) -> str:
            pointer = ""
            for p in path:
                escaped = p.replace("~", "~0").replace("/", "~1")
                pointer += f"/{escaped}"
            return pointer

        path = find_path(root, node, [])
        if path is None:
            raise RuntimeError("Node not found in document")
        return path_to_pointer(path)

    @staticmethod
    def schema_type(ctx: GeneratorContext, schema_ref: JsonNode, project_name: str, root: JsonNode, schema_format: str = "jsonschema/draft-07") -> str:
        """Get the schema type from a schema reference."""
        logger.debug("Getting schema type from schema reference")

        class_name: str = ''
        schema_obj: JsonNode = None

        def resolve_pointer(root: JsonNode, schema_ref: str) -> JsonNode:
            if schema_ref.startswith("#"):
                try:
                    obj = jsonpointer.resolve_pointer(root, urllib.parse.unquote(schema_ref[1:]))
                    if isinstance(obj, (dict, list, str)):
                        return obj
                    else:
                        raise RuntimeError(f"Schema not found: {schema_ref}")
                except jsonpointer.JsonPointerException as jpe:
                    schema_ref = schema_ref[1:]
            if schema_ref.startswith("/"):
                schema_ref = urllib.parse.urljoin(ctx.base_uri, schema_ref)            
            schema_ref, fragment = urllib.parse.urldefrag(schema_ref)
            _, obj = ctx.loader.load(schema_ref, {}, True, True)
            if fragment:
                fragment, class_name = fragment.split(":")
                obj = resolve_pointer(obj, fragment)
            return obj

        if schema_format.lower().startswith("proto") and isinstance(schema_ref, str) and SchemaUtils.is_proto_doc(schema_ref):
            ptr = SchemaUtils.get_json_pointer(root, schema_ref)
            ptr = ptr.rsplit("/", 1)[0]
            SchemaUtils.schema_references_collected.add('#' + ptr)
            schema_format = schema_format.lower().split("/")[0]
            schema_obj = schema_ref
            schema_ref = '#' + ptr
        elif isinstance(schema_ref, str):
            schema_ref, class_name = SchemaUtils.split_schema_reference(schema_ref)
            if schema_ref.startswith("#"):
                if schema_ref not in SchemaUtils.schema_references_collected:
                    SchemaUtils.schema_references_collected.add(schema_ref)
                schema_obj = resolve_pointer(root, schema_ref)
            else:
                schema_ref, fragment = urllib.parse.urldefrag(schema_ref)
                _, schema_obj = ctx.loader.load(schema_ref, {}, True, True)
                if fragment:
                    fragment, class_name = fragment.split(":")
                    schema_obj = resolve_pointer(schema_obj, fragment)

            schema_version = None
            if isinstance(schema_obj, dict) and "versions" in schema_obj and isinstance(schema_obj['versions'], dict):
                _, schema_version = SchemaUtils.select_schema_version(schema_obj)
                if not class_name:
                    class_name = str(schema_obj.get("schemaid", ''))
                if not class_name:
                    # Extract schema name from the reference path (e.g., /schemagroups/.../schemas/orderData)
                    path_elements = schema_ref.split('/')
                    if len(path_elements) >= 2 and path_elements[-2] == 'schemas':
                        class_name = path_elements[-1]
                parent_reference = schema_ref.rsplit("/", 2)[0]
                try:
                    parent = jsonpointer.resolve_pointer(root, parent_reference[1:])
                    if parent and isinstance(parent, dict):
                        # Try to get schema group ID from the parent object
                        prefix = parent.get("schemagroupid", '')
                        if not prefix:
                            # If not in the object, extract from the reference path
                            # e.g., #/schemagroups/Contoso.ERP.Events/schemas/orderData → parent_reference = #/schemagroups/Contoso.ERP.Events/schemas
                            # We want "Contoso.ERP.Events"
                            path_elements = schema_ref.split('/')
                            for i, elem in enumerate(path_elements):
                                if elem == 'schemas' and i > 0:
                                    prefix = path_elements[i - 1]
                                    break
                        if class_name and prefix and not class_name.startswith(prefix):
                            class_name = prefix + '.' + class_name
                except jsonpointer.JsonPointerException:
                    raise RuntimeError(f"Schema not found: {parent_reference}")
            elif isinstance(schema_obj, dict) and ("versionid" in schema_obj or "/versions/" in schema_ref):
                schema_version = schema_obj
                resource_reference = schema_ref.rsplit("/versions/", 1)[0]
                parent = resolve_pointer(root, resource_reference)
                parts = jsonpointer.JsonPointer(urllib.parse.unquote(resource_reference.lstrip("#"))).parts
                class_name = class_name or str(schema_obj.get("schemaid") or parent.get("schemaid") or parts[-1])
                if len(parts) == 4 and parts[0] == "schemagroups" and not class_name.startswith(parts[1] + "."):
                    class_name = parts[1] + "." + class_name

            if not schema_version or not isinstance(schema_version, dict):
                raise RuntimeError(f"Schema version not found: {schema_ref}")
            if not "format" in schema_version or not isinstance(schema_version["format"], str) or schema_format != schema_version["format"]:
                raise RuntimeError(f"Schema format mismatch: {schema_format} != {str(schema_version['format']) if 'format' in schema_version else ''}")
            schema_format = schema_version["format"].lower().split("/")[0]
            if "schemaurl" in schema_version:
                external_schema_url = str(schema_version["schemaurl"])
                _, schema_obj = ctx.loader.load(external_schema_url, {}, True)
                if not schema_obj:
                    raise RuntimeError(f"Schema not found: {external_schema_url}")
            elif "schema" in schema_version:
                schema_obj = schema_version["schema"]
            else:
                raise RuntimeError(f"Schema not found: {schema_ref}")
        else:
            ptr = SchemaUtils.get_json_pointer(root, schema_ref)
            ptr = ptr.rsplit("/", 1)[0]
            SchemaUtils.schema_references_collected.add('#' + ptr)
            schema_format = schema_format.lower().split("/")[0]
            schema_obj = schema_ref
            schema_ref = '#' + ptr

        if schema_format.startswith("avro"):
            if isinstance(schema_obj, dict) and "type" in schema_obj and schema_obj["type"] == "record":
                ref = str(f"{schema_obj['namespace']}.{schema_obj['name']}" if "namespace" in schema_obj else schema_obj["name"])
                #if class_name and ref.lower() != class_name.lower():
                #    raise RuntimeError(f"Avro: Class name reference mismatch for top-level record object: {project_name}.{ref} != {project_name}.{class_name}")
                #    return f"{project_name}.{class_name}"
                return f"{project_name}.{ref}"
            elif isinstance(schema_obj, list):
                if not class_name:
                    raise RuntimeError("Avro: Explicit class name reference (':{classname}' suffix) required for Avro schema with top-level union: ")
                for record in schema_obj:
                    if isinstance(record, dict) and "type" in record and record["type"] == "record":
                        ref = f"{record['namespace']}.{record['name']}" if "namespace" in record else record["name"]
                        if ref == class_name:
                            return f"{project_name}.{ref}"
            raise RuntimeError("Avro: Top-level record object not found in Avro schema: ")
        elif schema_format.startswith("proto"):
            if isinstance(schema_obj, str):
                if class_name:
                    local_class_name = JinjaFilters.strip_namespace(class_name)
                    match = re.search(r"message[\s]+([\w]+)[\s]*{", schema_obj)
                    if local_class_name and match:
                        for g in match.groups():
                            if g.lower() == local_class_name.lower():
                                return f"{project_name}.{class_name}"
                    if match and match.groups() and len(match.groups()) == 1:
                        class_name = JinjaFilters.namespace_dot(class_name) + match.groups()[0]
                        return f"{project_name}.{class_name}"
                    else:
                        raise RuntimeError(f"Proto: Top-level message {class_name} not found in Proto schema")
                else:
                    match = re.search(r"message[\s]+([\w]+)[\s]*{", schema_obj)
                    if match:
                        if len(match.groups()) > 1:
                            raise RuntimeError("Proto: Multiple top-level message objects found in Proto schema: ")
                        return f"{project_name}.{match.group(1)}"
                    else:
                        raise RuntimeError("Proto: Top-level message object not found in Proto schema: ")
            raise RuntimeError("Proto: Top-level message object not found in Proto schema: ")
        elif schema_format.startswith("jstruct") or schema_format.startswith("jsonstructure"):
            # JSON Structure schemas don't use namespace prefixes in generated code
            # avrotize generates flat class names without schema group prefixes
            if class_name:
                # Strip the schema group prefix if present (e.g., "Fabrikam.InkJetPrinter.PrintJobStartedEventData" -> "PrintJobStartedEventData")
                simple_class_name = class_name.split('.')[-1]
                return f"{project_name}.{simple_class_name}"
            path_elements = schema_ref.split('/')
            if path_elements[-2] == "versions":
                return path_elements[-3]
            else:
                return path_elements[-1]
        else:
            if class_name:
                return f"{project_name}.{class_name}"
            path_elements = schema_ref.split('/')
            if path_elements[-2] == "versions":
                return path_elements[-3]
            else:
                return path_elements[-1]

    @staticmethod
    def schema_object(root: Dict[str, Any], schema_url: str) -> Optional[Any]:
        """Return the object in the document that the schema URL points to."""
        logger.debug("Getting schema object from URL: %s", schema_url)
        if schema_url is None:
            return None
        try:
            obj = jsonpointer.resolve_pointer(root, schema_url[1:].split(":")[0])
        except jsonpointer.JsonPointerException:
            return None
        return obj

    @staticmethod
    def latest_dict_entry(dict_obj: Dict[str, Any]) -> Any:
        """Return the dictionary entry with the last key."""
        logger.debug("Getting the latest entry from dictionary")
        m = max([len(k) for k in dict_obj.keys()])
        return dict_obj[sorted([k.ljust(m) for k in dict_obj.keys()])[-1].strip()]

    @staticmethod
    def concat_namespace(namespace: str, class_name: str) -> str:
        """Concatenate a namespace and a class name."""
        logger.debug("Concatenating namespace: %s with class name: %s", namespace, class_name)
        if namespace:
            return f"{namespace}.{class_name}"
        return class_name
    
    @staticmethod
    def is_proto_doc(docroot: JsonNode) -> bool:
        """Check if the document is a proto document."""
        return isinstance(docroot, str) and re.search(r"syntax[\s]*=[\s]*\"proto3\"", docroot) is not None