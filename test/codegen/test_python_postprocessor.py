"""Regression tests for the Avrotize Python post-processing fixes.

Covers issue #501: ``apply_python_avrotize_fixes`` injected a ``str -> bytes``
guard into the ``application/json`` branch of ``to_byte_array`` non-idempotently,
so regenerating over an existing output appended a duplicate guard on every run.
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from xrcg.generator.python_codegen_postprocessor import (  # noqa: E402
    _JSON_TO_BYTES_PATTERN,
    _encode_json_result,
    apply_python_avrotize_fixes,
)

# Raw Avrotize output for the ``to_byte_array`` JSON branch, i.e. BEFORE the
# post-processor adds the ``str -> bytes`` guard.
_RAW_DATACLASS = (
    "import json\n"
    "\n"
    "\n"
    "class Sample:\n"
    "    def to_byte_array(self, content_type: str) -> bytes:\n"
    "        base_content_type = content_type.split('+')[0]\n"
    "        result = None\n"
    "        if base_content_type == 'application/json':\n"
    "            #pylint: disable=no-member\n"
    "            result = self.to_json()\n"
    "            #pylint: enable=no-member\n"
    "        return result\n"
)

_GUARD = "if isinstance(result, str):"
_ENCODE = "result = result.encode('utf-8')"


def _guard_count(text: str) -> int:
    return text.count(_GUARD)


def test_pattern_injects_guard_once():
    """First pass over raw output injects exactly one guard."""
    once = _JSON_TO_BYTES_PATTERN.sub(_encode_json_result, _RAW_DATACLASS)
    assert _guard_count(once) == 1
    assert once.count(_ENCODE) == 1


def test_pattern_is_idempotent():
    """A second pass must not append a duplicate guard (issue #501)."""
    once = _JSON_TO_BYTES_PATTERN.sub(_encode_json_result, _RAW_DATACLASS)
    twice = _JSON_TO_BYTES_PATTERN.sub(_encode_json_result, once)
    assert twice == once
    assert _guard_count(twice) == 1


def test_pattern_idempotent_without_pylint_comments():
    """Guard injection stays idempotent when the pylint markers are absent."""
    raw = _RAW_DATACLASS.replace("            #pylint: disable=no-member\n", "")
    raw = raw.replace("            #pylint: enable=no-member\n", "")
    once = _JSON_TO_BYTES_PATTERN.sub(_encode_json_result, raw)
    twice = _JSON_TO_BYTES_PATTERN.sub(_encode_json_result, once)
    assert _guard_count(once) == 1
    assert twice == once


def test_apply_fixes_idempotent_on_disk(tmp_path):
    """Regenerating over existing output is a no-op (the reported scenario)."""
    py_file = tmp_path / "sample.py"
    py_file.write_text(_RAW_DATACLASS, encoding="utf-8")

    apply_python_avrotize_fixes(str(tmp_path))
    first = py_file.read_text(encoding="utf-8")
    assert _guard_count(first) == 1

    apply_python_avrotize_fixes(str(tmp_path))
    second = py_file.read_text(encoding="utf-8")
    assert second == first
    assert _guard_count(second) == 1
