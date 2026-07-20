"""Tests for xRegistry resource alias (xref) resolution.

Aliases are resolved during document loading so they are transparent to
validation, schema processing, and template rendering (see issue #582).
"""

import json
import logging
import os
import tempfile
import unittest

from xrcg.generator.xregistry_loader import XRegistryLoader
from xrcg.commands.validate_definitions import validate


def _canonical_schema():
    return {
        "format": "JSONSchema/draft-07",
        "defaultversionid": "1",
        "versions": {
            "1": {
                "format": "JSONSchema/draft-07",
                "schema": {
                    "type": "object",
                    "properties": {"value": {"type": "string"}},
                },
            }
        },
    }


class TestAliasResolution(unittest.TestCase):
    """Resource alias (xref) resolution during load."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def _write(self, doc):
        path = os.path.join(self.temp_dir, "test.xreg.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f)
        return path

    def _load(self, doc):
        path = self._write(doc)
        loader = XRegistryLoader()
        _, result = loader.load(path)
        return result

    def test_schema_alias_meta_xref_resolves(self):
        """An alias authored as meta.xref projects the target's content."""
        doc = {
            "schemagroups": {
                "canonical": {"schemas": {"EventData": _canonical_schema()}},
                "route": {
                    "schemas": {
                        "EventData": {
                            "meta": {"xref": "/schemagroups/canonical/schemas/EventData"}
                        }
                    }
                },
            }
        }
        result = self._load(doc)
        alias = result["schemagroups"]["route"]["schemas"]["EventData"]

        # Target content is projected through the alias.
        self.assertIn("versions", alias)
        self.assertEqual(alias["defaultversionid"], "1")
        self.assertEqual(
            alias["versions"]["1"]["schema"]["properties"]["value"]["type"], "string"
        )
        # The alias retains its own identity.
        self.assertEqual(alias["schemaid"], "EventData")
        # xref markers are gone.
        self.assertNotIn("xref", alias)
        self.assertNotIn("meta", alias)

    def test_resource_level_xref_resolves(self):
        """An alias authored as a resource-level xref also resolves."""
        doc = {
            "schemagroups": {
                "canonical": {"schemas": {"EventData": _canonical_schema()}},
                "route": {
                    "schemas": {
                        "Aliased": {"xref": "/schemagroups/canonical/schemas/EventData"}
                    }
                },
            }
        }
        result = self._load(doc)
        alias = result["schemagroups"]["route"]["schemas"]["Aliased"]
        self.assertIn("versions", alias)
        self.assertEqual(alias["schemaid"], "Aliased")

    def test_message_alias_resolves(self):
        """Aliases are model-driven and work for messages, not only schemas."""
        doc = {
            "messagegroups": {
                "canonical": {
                    "messages": {
                        "OrderCreated": {
                            "envelope": "CloudEvents/1.0",
                            "envelopemetadata": {
                                "type": {"value": "com.example.order.created"}
                            },
                        }
                    }
                },
                "route": {
                    "messages": {
                        "OrderCreated": {
                            "meta": {
                                "xref": "/messagegroups/canonical/messages/OrderCreated"
                            }
                        }
                    }
                },
            }
        }
        result = self._load(doc)
        alias = result["messagegroups"]["route"]["messages"]["OrderCreated"]
        self.assertEqual(alias["envelope"], "CloudEvents/1.0")
        self.assertEqual(
            alias["envelopemetadata"]["type"]["value"], "com.example.order.created"
        )
        self.assertEqual(alias["messageid"], "OrderCreated")
        self.assertNotIn("meta", alias)

    def test_alias_document_validates(self):
        """A document whose only alias content is meta.xref validates cleanly."""
        doc = {
            "schemagroups": {
                "canonical": {"schemas": {"EventData": _canonical_schema()}},
                "route": {
                    "schemas": {
                        "EventData": {
                            "meta": {"xref": "/schemagroups/canonical/schemas/EventData"}
                        }
                    }
                },
            }
        }
        path = self._write(doc)
        self.assertEqual(validate([path], {}, verbose=False), 0)

    # --- error diagnostics -------------------------------------------------

    def _assert_unresolved_with_error(self, doc, needle):
        path = self._write(doc)
        loader = XRegistryLoader()
        with self.assertLogs(
            "xrcg.generator.xregistry_loader.AliasResolver", level="ERROR"
        ) as cm:
            _, result = loader.load(path)
        self.assertTrue(any(needle in m for m in cm.output), cm.output)
        return result

    def test_malformed_target(self):
        doc = {
            "schemagroups": {
                "route": {"schemas": {"Alias": {"meta": {"xref": "not-an-xid"}}}}
            }
        }
        result = self._assert_unresolved_with_error(doc, "malformed xref target")
        # Alias left untouched so downstream validation still flags it.
        self.assertIn(
            "xref", result["schemagroups"]["route"]["schemas"]["Alias"]["meta"]
        )

    def test_missing_target(self):
        doc = {
            "schemagroups": {
                "canonical": {"schemas": {"EventData": _canonical_schema()}},
                "route": {
                    "schemas": {
                        "Alias": {
                            "meta": {"xref": "/schemagroups/canonical/schemas/Nope"}
                        }
                    }
                },
            }
        }
        self._assert_unresolved_with_error(doc, "was not found")

    def test_type_mismatch(self):
        doc = {
            "schemagroups": {
                "route": {
                    "schemas": {
                        "Alias": {
                            "meta": {
                                "xref": "/messagegroups/canonical/messages/EventData"
                            }
                        }
                    }
                }
            }
        }
        self._assert_unresolved_with_error(doc, "different resource type")

    def test_self_reference(self):
        doc = {
            "schemagroups": {
                "route": {
                    "schemas": {
                        "Alias": {
                            "meta": {"xref": "/schemagroups/route/schemas/Alias"}
                        }
                    }
                }
            }
        }
        self._assert_unresolved_with_error(doc, "refers to itself")

    def test_alias_to_alias_not_transitive(self):
        doc = {
            "schemagroups": {
                "canonical": {"schemas": {"EventData": _canonical_schema()}},
                "route": {
                    "schemas": {
                        "First": {
                            "meta": {"xref": "/schemagroups/route/schemas/Second"}
                        },
                        "Second": {
                            "meta": {
                                "xref": "/schemagroups/canonical/schemas/EventData"
                            }
                        },
                    }
                },
            }
        }
        self._assert_unresolved_with_error(doc, "is itself an alias")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
