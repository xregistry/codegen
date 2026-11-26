import sys
import os
import glob
import json

import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(project_root))

import xrcg

# this test invokes the xregistry command line tool to generate a C# proxy and a consumer
# and then builds the proxy and the consumer and runs a prepared test that integrates both
def test_validate():
    # clean the output directory
    input_dir = os.path.join(project_root, 'samples'.replace('/', os.path.sep))
    disco_files = glob.glob("**/*.xreg.json", root_dir=input_dir, recursive=True)
    for disco_file in disco_files:
        # generate the producer
        sys.argv = ['xrcg', 'validate',  
                    '--definitions', os.path.join(input_dir, disco_file)]
        assert xrcg.cli() == 0
    disco_files = glob.glob("**/*.xreg.yaml", root_dir=input_dir, recursive=True)
    for disco_file in disco_files:
        # generate the producer
        sys.argv = ['xrcg', 'validate',
                    '--definitions', os.path.join(input_dir, disco_file)]
        assert xrcg.cli() == 0


@pytest.mark.parametrize("stacked", [False, True])
@pytest.mark.parametrize("inline_schema,expected", [(False, 0), (True, 1)])
def test_validate_preserves_schema_content_choice(tmp_path, monkeypatch, stacked, inline_schema, expected):
    schema = {"type": "object", "properties": {"value": {"type": "string"}}}
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps(schema), encoding="utf-8")
    version: dict[str, object] = {"format": "JSONSchema/draft-07", "schemaurl": str(schema_path)}
    if inline_schema:
        version["schema"] = schema
    document = {
        "schemagroups": {
            "example": {
                "schemas": {"record": {"versions": {"1": version}}},
            },
        },
    }
    definitions_path = tmp_path / "definitions.xreg.json"
    definitions_path.write_text(json.dumps(document), encoding="utf-8")
    definitions = [str(definitions_path)]
    if stacked:
        overlay_path = tmp_path / "overlay.xreg.json"
        overlay_path.write_text(json.dumps({"messagegroups": {}}), encoding="utf-8")
        definitions.append(str(overlay_path))
    monkeypatch.setattr(sys, "argv", ["xrcg", "validate", "--definitions", *definitions])
    assert xrcg.cli() == expected
