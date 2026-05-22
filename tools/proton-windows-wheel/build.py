"""
Build a patched python-qpid-proton wheel for Windows that links against
OpenSSL (via vcpkg) instead of SChannel, so TLS 1.3 works.

See tools/proton-windows-wheel/README.md for context.

Usage:
    python build.py --proton-version 0.40.0 --xrcg-build 1 \
        --openssl-dir C:/vcpkg/installed/x64-windows-static-md \
        --output-dir dist/
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path


PYPI_SDIST_URL = (
    "https://files.pythonhosted.org/packages/source/p/"
    "python-qpid-proton/python_qpid_proton-{version}.tar.gz"
)


def download_sdist(version: str, dest_dir: Path) -> Path:
    url = PYPI_SDIST_URL.format(version=version)
    out = dest_dir / f"python_qpid_proton-{version}.tar.gz"
    print(f"[build] Downloading {url}")
    with urllib.request.urlopen(url) as resp, open(out, "wb") as fh:
        shutil.copyfileobj(resp, fh)
    print(f"[build] Saved {out} ({out.stat().st_size:,} bytes)")
    return out


def extract_sdist(tarball: Path, dest_dir: Path) -> Path:
    print(f"[build] Extracting {tarball.name}")
    with tarfile.open(tarball) as tf:
        tf.extractall(dest_dir)
    # the sdist extracts into a single top-level dir
    [root] = [p for p in dest_dir.iterdir() if p.is_dir()]
    return root


# Original Windows block we look for and replace.
_WIN_BLOCK_RE = re.compile(
    r"if os\.name == 'nt':\s*\n"
    r"\s*libraries \+= \['crypt32', 'secur32'\]\s*\n"
    r"\s*sources\.append\(os\.path\.join\(proton_c_src, 'ssl', 'schannel\.cpp'\)\)",
    re.MULTILINE,
)

# Replacement: use OpenSSL on Windows. Reads OPENSSL_DIR env at build time.
_WIN_BLOCK_REPLACEMENT = """if os.name == 'nt':
    # PATCHED by xregistry-codegen tools/proton-windows-wheel:
    # use OpenSSL on Windows (via vcpkg) instead of SChannel,
    # so TLS 1.3 works against Azure Service Bus and other strict brokers.
    _openssl_dir = os.environ.get('OPENSSL_DIR')
    if not _openssl_dir:
        raise RuntimeError(
            'OPENSSL_DIR env var is required for the patched Windows build. '
            'Set it to your vcpkg install root (the dir containing include/ and lib/).'
        )
    libraries += ['libssl', 'libcrypto', 'crypt32', 'ws2_32', 'advapi32', 'user32']
    include_dirs_extra = [os.path.join(_openssl_dir, 'include')]
    library_dirs_extra = [os.path.join(_openssl_dir, 'lib')]
    sources.append(os.path.join(proton_c_src, 'ssl', 'openssl.c'))
    # Bump Win32 API floor to Vista+ so InitOnceExecuteOnce et al. are declared.
    macros_extra = [('_WIN32_WINNT', '0x0A00'), ('_CRT_SECURE_NO_WARNINGS', '1')]"""


# Original set_source call (the "no pkgconfig" branch is the one Windows hits).
# We need to inject library_dirs into it.
_SET_SOURCE_RE = re.compile(
    r"ffibuilder\.set_source\(\s*\n"
    r"\s*\"cproton_ffi\",\s*\n"
    r"\s*c_code,\s*\n"
    r"\s*define_macros=macros,\s*\n"
    r"\s*extra_compile_args=extra,\s*\n"
    r"\s*sources=sources,\s*\n"
    r"\s*include_dirs=include_dirs,\s*\n"
    r"\s*libraries=libraries\s*\n"
    r"\s*\)"
)

_SET_SOURCE_REPLACEMENT = """ffibuilder.set_source(
        "cproton_ffi",
        c_code,
        define_macros=macros + (macros_extra if 'macros_extra' in dir() else []),
        extra_compile_args=extra,
        sources=sources,
        include_dirs=include_dirs + (include_dirs_extra if 'include_dirs_extra' in dir() else []),
        library_dirs=library_dirs_extra if 'library_dirs_extra' in dir() else None,
        libraries=libraries
    )"""


def patch_ext_build(src_root: Path) -> None:
    ext_build = src_root / "ext_build.py"
    if not ext_build.is_file():
        raise SystemExit(f"ext_build.py not found at {ext_build}")
    print(f"[build] Patching {ext_build.relative_to(src_root)}")
    text = ext_build.read_text(encoding="utf-8")

    new_text, n = _WIN_BLOCK_RE.subn(_WIN_BLOCK_REPLACEMENT, text)
    if n != 1:
        raise SystemExit(
            "FATAL: could not find the SChannel Windows block in ext_build.py. "
            "Upstream layout has changed; this patcher needs updating."
        )

    new_text, n = _SET_SOURCE_RE.subn(_SET_SOURCE_REPLACEMENT, new_text)
    if n != 1:
        raise SystemExit(
            "FATAL: could not find the ffibuilder.set_source call in ext_build.py. "
            "Upstream layout has changed; this patcher needs updating."
        )

    ext_build.write_text(new_text, encoding="utf-8")
    print("[build] Patched ext_build.py OK")


# Proton's openssl.c was never built on Windows: the InitOnceExecuteOnce call
# in the _WIN32 ensure_initialized block calls `&initialize` directly, but
# initialize() is `void(void)`, not the BOOL CALLBACK(PINIT_ONCE,PVOID,PVOID*)
# signature InitOnceExecuteOnce expects. Also the forward decl of initialize
# lives in the #else (POSIX) branch, so it's invisible to the _WIN32 block.
# Replace the broken Win32 block with a correctly-typed wrapper.
_OPENSSL_WIN_INIT_RE = re.compile(
    r"INIT_ONCE initialize_once = INIT_ONCE_STATIC_INIT;\s*\n"
    r"static inline bool ensure_initialized\(void\)\s*\{\s*\n"
    r"\s*void\* dummy;\s*\n"
    r"\s*InitOnceExecuteOnce\(&initialize_once, &initialize, NULL, &dummy\);\s*\n"
    r"\s*return init_ok;\s*\n"
    r"\}",
    re.MULTILINE,
)

_OPENSSL_WIN_INIT_REPLACEMENT = """/* PATCHED by xregistry-codegen tools/proton-windows-wheel:
 * upstream openssl.c was never built on Windows; the original code passed
 * &initialize directly to InitOnceExecuteOnce, but initialize() is void(void),
 * not the BOOL CALLBACK(PINIT_ONCE, PVOID, PVOID*) callback type the API
 * requires. Also forward-declare initialize() so it's visible from this block.
 */
static void initialize(void);

static BOOL CALLBACK pn_initialize_once_callback(PINIT_ONCE once, PVOID param, PVOID *context) {
  (void)once; (void)param; (void)context;
  initialize();
  return TRUE;
}

static INIT_ONCE initialize_once = INIT_ONCE_STATIC_INIT;
static inline bool ensure_initialized(void) {
  void* dummy;
  InitOnceExecuteOnce(&initialize_once, pn_initialize_once_callback, NULL, &dummy);
  return init_ok;
}"""


def patch_openssl_c(src_root: Path) -> None:
    """Fix proton's openssl.c so it actually compiles on Windows."""
    openssl_c = src_root / "src" / "ssl" / "openssl.c"
    if not openssl_c.is_file():
        raise SystemExit(f"openssl.c not found at {openssl_c}")
    print(f"[build] Patching {openssl_c.relative_to(src_root)}")
    text = openssl_c.read_text(encoding="utf-8")
    new_text, n = _OPENSSL_WIN_INIT_RE.subn(_OPENSSL_WIN_INIT_REPLACEMENT, text)
    if n != 1:
        raise SystemExit(
            "FATAL: could not find the Windows InitOnceExecuteOnce block in openssl.c. "
            "Upstream layout has changed; this patcher needs updating."
        )
    openssl_c.write_text(new_text, encoding="utf-8")
    print("[build] Patched openssl.c OK")


def patch_version(src_root: Path, version: str, xrcg_build: int) -> str:
    """
    Bump the project version to <version>+xrcg<N>.
    Proton's sdist uses PEP 621 dynamic version sourced from VERSION.txt.
    """
    new_version = f"{version}+xrcg{xrcg_build}"
    version_txt = src_root / "VERSION.txt"
    if version_txt.is_file():
        version_txt.write_text(new_version + "\n", encoding="utf-8")
        print(f"[build] Set version to {new_version} (VERSION.txt)")
        return new_version
    raise SystemExit(
        "FATAL: VERSION.txt not found in proton sdist. Upstream layout has changed; "
        "this patcher needs updating."
    )


def build_wheel(src_root: Path, output_dir: Path, python: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[build] Running 'python -m build --wheel' in {src_root}")
    subprocess.check_call(
        [python, "-m", "pip", "install", "--upgrade", "build", "wheel", "cffi", "setuptools"],
    )
    subprocess.check_call(
        [python, "-m", "build", "--wheel", "--outdir", str(output_dir.resolve())],
        cwd=src_root,
    )
    # find the wheel just built
    wheels = sorted(output_dir.glob("python_qpid_proton-*.whl"), key=lambda p: p.stat().st_mtime)
    if not wheels:
        raise SystemExit("FATAL: build produced no wheel")
    wheel = wheels[-1]
    print(f"[build] Built {wheel.name} ({wheel.stat().st_size:,} bytes)")
    return wheel


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proton-version", default="0.40.0")
    parser.add_argument("--xrcg-build", type=int, default=1, help="our local build number")
    parser.add_argument("--openssl-dir", help="OpenSSL prefix (vcpkg install root). If omitted, uses $OPENSSL_DIR.")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--python", default=sys.executable, help="Python interpreter to build for")
    parser.add_argument("--keep-source", action="store_true", help="don't delete the extracted source dir")
    args = parser.parse_args(argv)

    if args.openssl_dir:
        os.environ["OPENSSL_DIR"] = args.openssl_dir
    if not os.environ.get("OPENSSL_DIR"):
        print("ERROR: OPENSSL_DIR is not set; pass --openssl-dir or export OPENSSL_DIR.", file=sys.stderr)
        return 2

    work = Path(tempfile.mkdtemp(prefix="proton-build-"))
    try:
        sdist = download_sdist(args.proton_version, work)
        src_root = extract_sdist(sdist, work)
        patch_ext_build(src_root)
        patch_openssl_c(src_root)
        new_version = patch_version(src_root, args.proton_version, args.xrcg_build)
        wheel = build_wheel(src_root, args.output_dir.resolve(), args.python)
        print(f"\n[build] SUCCESS: {wheel}  (version {new_version})")
    finally:
        if args.keep_source:
            print(f"[build] Source kept at {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
