"""
Generate a PEP 503 "simple" repository index for the patched python-qpid-proton
Windows wheels published as assets on GitHub Releases tagged `proton-windows-*`.

Output layout (written under --output-dir, default `_site_wheels/`):

    simple/
        index.html                              <- lists all projects
        python-qpid-proton/index.html           <- lists all wheel files

Each wheel link points to the direct GitHub Release asset URL.

Usage:
    python scripts/build_wheel_index.py --repo xregistry/codegen --output-dir _site_wheels/

Environment:
    GITHUB_TOKEN   optional; used to raise the API rate limit
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
import urllib.request
from pathlib import Path

GH_API = "https://api.github.com"


def gh_api(path: str, token: str | None) -> object:
    url = f"{GH_API}{path}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "xregistry-codegen-wheel-indexer",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def fetch_proton_wheel_assets(repo: str, token: str | None) -> list[dict]:
    """Return a list of {name, url, size, tag} for every wheel asset on every
    release tagged `proton-windows-*`."""
    assets: list[dict] = []
    page = 1
    while True:
        rels = gh_api(f"/repos/{repo}/releases?per_page=100&page={page}", token)
        if not rels:
            break
        for rel in rels:
            tag = rel.get("tag_name", "")
            if not tag.startswith("proton-windows-"):
                continue
            for asset in rel.get("assets", []):
                name = asset["name"]
                if not name.endswith(".whl"):
                    continue
                assets.append({
                    "name": name,
                    "url": asset["browser_download_url"],
                    "size": asset["size"],
                    "tag": tag,
                })
        page += 1
        if len(rels) < 100:
            break
    assets.sort(key=lambda a: (a["tag"], a["name"]), reverse=True)
    return assets


def write_root_index(out_dir: Path, project_names: list[str]) -> None:
    rows = "\n".join(
        f'    <a href="{html.escape(p)}/">{html.escape(p)}</a><br>'
        for p in sorted(set(project_names))
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(
        "<!DOCTYPE html>\n"
        "<html><head><meta name='pypi:repository-version' content='1.0'>\n"
        "<title>Simple Index</title></head><body>\n"
        f"{rows}\n"
        "</body></html>\n",
        encoding="utf-8",
    )


def write_project_index(project_dir: Path, project_name: str, assets: list[dict]) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        f'    <a href="{html.escape(a["url"])}">{html.escape(a["name"])}</a><br>'
        for a in assets
    ]
    body = "\n".join(rows) if rows else "    <!-- no wheels yet -->"
    (project_dir / "index.html").write_text(
        "<!DOCTYPE html>\n"
        "<html><head><meta name='pypi:repository-version' content='1.0'>\n"
        f"<title>Links for {html.escape(project_name)}</title></head><body>\n"
        f"<h1>Links for {html.escape(project_name)}</h1>\n"
        f"{body}\n"
        "</body></html>\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", "xregistry/codegen"),
    )
    parser.add_argument("--output-dir", type=Path, default=Path("_site_wheels"))
    args = parser.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN")
    print(f"[wheel-index] Fetching releases for {args.repo}")
    assets = fetch_proton_wheel_assets(args.repo, token)
    print(f"[wheel-index] Found {len(assets)} proton wheel assets")

    simple_dir = args.output_dir / "simple"
    write_root_index(simple_dir, ["python-qpid-proton"])
    write_project_index(simple_dir / "python-qpid-proton", "python-qpid-proton", assets)

    print(f"[wheel-index] Wrote index to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
