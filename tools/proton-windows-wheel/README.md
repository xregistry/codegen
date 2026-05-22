# proton-windows-wheel

**Temporary infrastructure to ship a Windows-only `python-qpid-proton` wheel that links against OpenSSL instead of SChannel — so TLS 1.3 works.**

## Why this exists

The upstream `python-qpid-proton` Windows wheel uses [SChannel](https://learn.microsoft.com/en-us/windows/win32/com/schannel) via the legacy `SCHANNEL_CRED` API, which Microsoft caps at TLS 1.2. Azure Service Bus namespaces with `minimumTlsVersion=1.3` (or any other AMQP 1.0 broker that requires TLS 1.3) cannot be reached from Windows with the official wheel.

The Linux/macOS wheels link against OpenSSL via pkg-config, which already supports TLS 1.3 — no change needed there.

Until [PROTON-XXXX](https://issues.apache.org/jira/projects/PROTON) lands a fix in the upstream wheel (likely switching to `SCH_CREDENTIALS` + `TLS_PARAMETERS` for Windows 10 1809+), this repo publishes a patched Windows wheel that links against OpenSSL via vcpkg.

## Naming & versioning

We **keep the distribution name** `python-qpid-proton` and append a PEP 440 [local version](https://peps.python.org/pep-0440/#local-version-identifiers) suffix:

```
python_qpid_proton-0.40.0+xrcg1-cp311-cp311-win_amd64.whl
```

This way:

- On **Linux/macOS**, `pip install python-qpid-proton` resolves to `0.40.0` from PyPI as usual.
- On **Windows**, with `--extra-index-url https://xregistry.github.io/codegen/wheels/`, pip resolves to `0.40.0+xrcg1` (strictly higher under PEP 440 ordering) and installs the OpenSSL-backed build.

Generated app `pyproject.toml` files declare a single unconditional dependency: `python-qpid-proton>=0.40.0`. Only the install command on Windows needs the extra-index-url, and the generated README documents it.

## When to drop this

The day the upstream Windows wheel supports TLS 1.3:

1. Stop publishing new wheels here.
2. Bump the recommended `python-qpid-proton` version floor in generated `pyproject.toml.jinja` to the first upstream version that works on Windows TLS 1.3.
3. Remove the `--extra-index-url` note from the generated README.
4. Archive `tools/proton-windows-wheel/`.

## How it works locally

```powershell
# Prereqs: Python (any cp310/cp311/cp312/cp313), vcpkg + OpenSSL, MSVC build tools
vcpkg install openssl:x64-windows-static-md
$env:OPENSSL_DIR = "$(vcpkg integrate install | Select-String 'CMAKE_TOOLCHAIN_FILE' | %% { ... })\..\..\installed\x64-windows-static-md"

python tools\proton-windows-wheel\build.py --proton-version 0.40.0 --xrcg-build 1 --output-dir dist\
```

The script:

1. Downloads `python_qpid_proton-<ver>.tar.gz` from PyPI.
2. Extracts to a temp dir.
3. Patches `ext_build.py` to compile `ssl/openssl.c` instead of `ssl/schannel.cpp` on Windows, using OpenSSL headers/libs from `$OPENSSL_DIR`.
4. Patches the project metadata version to `<ver>+xrcg<N>`.
5. Runs `python -m build --wheel`.
6. Drops the resulting wheel into `--output-dir`.

CI ([`.github/workflows/build-proton-windows-wheels.yml`](../../.github/workflows/build-proton-windows-wheels.yml)) runs this matrix-style across Python versions on `windows-latest`, then uploads to a GitHub Release tagged `proton-windows-<ver>+xrcg<N>`. A second workflow regenerates the PEP 503 simple index page on `gh-pages`.
