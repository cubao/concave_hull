"""Mirror the pyodide runtime (plus a few packages) into ``pyodide-dist/``.

Handy when the CDN is slow: the browser test page then loads pyodide from
localhost instead of jsdelivr.  ``gen_wheels_json.py`` picks the mirror up
automatically when it exists.

Usage::

    python tests/pyodide/fetch_pyodide_dist.py --version 0.27.8
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent

CDN = "https://cdn.jsdelivr.net/pyodide/v{version}/full/"
CORE_FILES = [
    "pyodide.js",
    "pyodide.asm.js",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
]


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size:
        print(f"have {dest.name}")
        return
    print(f"fetch {dest.name}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("aria2c"):
        subprocess.run(
            [
                "aria2c",
                "-x8",
                "-s8",
                "-k1M",
                "--file-allocation=none",
                "--auto-file-renaming=false",
                "--allow-overwrite=true",
                "--console-log-level=error",
                "--summary-interval=0",
                "-d",
                str(dest.parent),
                "-o",
                dest.name,
                url,
            ],
            check=True,
        )
    else:
        urllib.request.urlretrieve(url, dest)


def resolve_deps(lock: dict, names: list[str]) -> set[str]:
    packages = lock["packages"]

    def walk(name: str, seen: set[str]) -> set[str]:
        if name in seen:
            return seen
        seen.add(name)
        for dep in packages[name].get("depends", []):
            walk(dep, seen)
        return seen

    resolved: set[str] = set()
    for name in names:
        walk(name, resolved)
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.27.8")
    parser.add_argument("--dir", type=Path, default=HERE / "pyodide-dist")
    parser.add_argument("--packages", nargs="*", default=["numpy", "pytest"])
    args = parser.parse_args()

    index_url = CDN.format(version=args.version)
    args.dir.mkdir(parents=True, exist_ok=True)

    for name in CORE_FILES:
        download(index_url + name, args.dir / name)

    lock = json.loads((args.dir / "pyodide-lock.json").read_text())
    for name in sorted(resolve_deps(lock, args.packages)):
        file_name = lock["packages"][name]["file_name"]
        download(index_url + file_name, args.dir / file_name)

    print(f"\npyodide {args.version} mirrored to {args.dir}")
    print("run `python tests/pyodide/gen_wheels_json.py dist` to use it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
