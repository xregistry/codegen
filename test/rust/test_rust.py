"""
Rust template tests for xRegistry CLI code generation.

Tests generate Rust code from xRegistry files, compile with ``cargo build`` and
run the generated ``cargo test`` suite. The HTTP ``producer`` style is fully
self-contained (it exercises the generated CloudEvents producer against an
in-process TCP capture server), so it needs neither Docker nor a broker.
"""

import os
import sys
import shutil
import tempfile
import subprocess
import pytest

# Get the project root directory (two levels up from this file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to the Python path so we can import xrcg
sys.path.insert(0, project_root)

import xrcg

# Environment variable check for CI/CD
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def _cargo_env():
    """Return an environment with the user cargo bin directory on PATH."""
    env = os.environ.copy()
    cargo_bin = os.path.join(os.path.expanduser("~"), ".cargo", "bin")
    if os.path.isdir(cargo_bin) and cargo_bin not in env.get("PATH", ""):
        env["PATH"] = cargo_bin + os.pathsep + env.get("PATH", "")
    return env


# Skip the whole module when the Rust toolchain is unavailable so the suite still
# runs on machines without cargo installed.
_cargo = shutil.which("cargo") or shutil.which(
    "cargo", path=os.path.join(os.path.expanduser("~"), ".cargo", "bin"))
pytestmark = pytest.mark.skipif(
    _cargo is None, reason="cargo (Rust toolchain) is not installed")


def run_rust_test(xreg_file: str, output_dir: str, projectname: str, style: str):
    """
    Generate Rust code from an xRegistry file, then build and test it.

    Args:
        xreg_file: Path to the xRegistry definition file
        output_dir: Directory where generated code will be placed
        projectname: Name of the Rust project
        style: Template style (producer, etc.)
    """
    try:
        sys.argv = [
            'xregistry',
            'generate',
            '--definitions', xreg_file,
            '--output', output_dir,
            '--projectname', projectname,
            '--style', style,
            '--language', 'rust'
        ]
        xrcg.cli()

        project_dir = os.path.join(output_dir, projectname)
        assert os.path.exists(project_dir), f"Project directory not found: {project_dir}"

        cargo_toml_path = os.path.join(project_dir, "Cargo.toml")
        assert os.path.exists(cargo_toml_path), f"Cargo.toml not found: {cargo_toml_path}"

        env = _cargo_env()

        print(f"Building Rust code in {project_dir}")
        result = subprocess.run(
            ['cargo', 'build'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=1200,
            env=env,
        )
        if result.returncode != 0:
            print(f"cargo build stdout: {result.stdout}")
            print(f"cargo build stderr: {result.stderr}")
            pytest.fail(f"cargo build failed with return code {result.returncode}")

        print(f"Running Rust tests in {project_dir}")
        result = subprocess.run(
            ['cargo', 'test'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=1800,
            env=env,
        )
        if result.returncode != 0:
            print(f"cargo test stdout: {result.stdout}")
            print(f"cargo test stderr: {result.stderr}")
            pytest.fail(f"cargo test failed with return code {result.returncode}")

        print(f"Rust code built and tested successfully: {project_dir}")

    except subprocess.TimeoutExpired:
        pytest.fail("Rust build/test timed out")


# Generic HTTP Producer Tests

def test_producer_contoso_erp_rust():
    with tempfile.TemporaryDirectory() as tmpdirname:
        run_rust_test(os.path.join(project_root, 'samples', 'message-definitions', 'contoso-erp.xreg.json').replace(
            '/', os.sep), tmpdirname, "test_producer_contoso_erp_rust", "producer")


def test_producer_lightbulb_rust():
    with tempfile.TemporaryDirectory() as tmpdirname:
        run_rust_test(os.path.join(project_root, 'samples', 'message-definitions', 'lightbulb.xreg.json').replace(
            '/', os.sep), tmpdirname, "test_producer_lightbulb_rust", "producer")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
