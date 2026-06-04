"""Post-processing fixes for Avrotize-generated Python code."""

import glob
import os
import re

from xrcg.cli import logger

_JSON_TO_BYTES_PATTERN = re.compile(
    r"(?P<indent>[ \t]*)if base_content_type == 'application/json':\n"
    r"(?P<disable>(?P=indent)    #pylint: disable=no-member\n)?"
    r"(?P=indent)    result = self\.to_json\(\)\n"
    r"(?P<enable>(?P=indent)    #pylint: enable=no-member\n)?",
    re.MULTILINE,
)


def _encode_json_result(match: re.Match[str]) -> str:
    indent = match.group("indent")
    disable = match.group("disable") or ""
    enable = match.group("enable") or ""
    return (
        f"{indent}if base_content_type == 'application/json':\n"
        f"{disable}"
        f"{indent}    result = self.to_json()\n"
        f"{enable}"
        f"{indent}    if isinstance(result, str):\n"
        f"{indent}        result = result.encode('utf-8')\n"
    )


def apply_python_avrotize_fixes(project_data_dir: str) -> None:
    """Apply local compatibility fixes to generated Python data classes."""
    for py_path in glob.glob(os.path.join(project_data_dir, "**", "*.py"), recursive=True):
        with open(py_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "def to_byte_array" not in content or "result = self.to_json()" not in content:
            continue
        updated = _JSON_TO_BYTES_PATTERN.sub(_encode_json_result, content)
        if updated != content:
            with open(py_path, "w", encoding="utf-8") as f:
                f.write(updated)
            logger.debug("Updated JSON byte-array handling in %s", py_path)
