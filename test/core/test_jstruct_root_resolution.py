"""Test JSON Structure $root resolution in _process_jstruct_schemas."""

import unittest

from xrcg.generator.template_renderer import TemplateRenderer


class TestJstructRootResolution(unittest.TestCase):
    """The TemplateRenderer must resolve $root wrappers before handing
    schemas to avrotize, otherwise avrotize silently emits no classes."""

    def setUp(self):
        # TemplateRenderer.__init__ takes (output_dir, project_name,
        # template_dirs, ...). For unit-testing the pure helper we only
        # need an instance — construct with minimal args.
        self.renderer = TemplateRenderer.__new__(TemplateRenderer)

    def test_resolves_root_and_derives_namespace(self):
        schema = {
            "$id": "https://example.com/Station",
            "name": "Station",
            "$root": "#/definitions/de/wsv/pegelonline/Station",
            "definitions": {
                "de": {"wsv": {"pegelonline": {
                    "Station": {
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                    },
                    "Water": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                    },
                }}}
            },
        }
        out = self.renderer._resolve_jstruct_root(schema)
        self.assertEqual(out.get("type"), "object")
        self.assertIn("properties", out)
        self.assertEqual(out.get("namespace"), "de.wsv.pegelonline")
        # definitions preserved so sibling $ref targets still resolve
        self.assertIn("definitions", out)
        self.assertIn("Water", out["definitions"]["de"]["wsv"]["pegelonline"])

    def test_passes_through_when_no_root(self):
        schema = {"type": "object", "properties": {"x": {"type": "string"}}}
        out = self.renderer._resolve_jstruct_root(schema)
        self.assertIs(out, schema)

    def test_passes_through_when_root_unresolvable(self):
        schema = {"$root": "#/definitions/nope", "definitions": {}}
        out = self.renderer._resolve_jstruct_root(schema)
        # On failure the original is returned unchanged
        self.assertIs(out, schema)

    def test_non_dict_input_passthrough(self):
        self.assertEqual(self.renderer._resolve_jstruct_root("x"), "x")
        self.assertIsNone(self.renderer._resolve_jstruct_root(None))


if __name__ == "__main__":
    unittest.main()
