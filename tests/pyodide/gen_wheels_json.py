"""Write ``tests/pyodide/wheels.json`` for the pyodide browser test page.

The page (``index.html``) is meant to be served from the repository root, e.g.::

    python -m http.server 8123        # run at the repo root
    # then open http://localhost:8123/tests/pyodide/index.html

Besides the wasm wheel(s) it lists the files the tests need: ``tests/test_*.py``
and everything under ``data/`` (if present), mirrored into the pyodide
filesystem under ``/tmp/`` keeping their relative layout, so tests that read
``../data/...`` keep working.

Usage::

    python tests/pyodide/gen_wheels_json.py [wheel_dir ...]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

WHEEL_NAME = re.compile(r"^(?P<name>[^-]+)-(?P<version>[^-]+)-")


def sort_key(path: Path) -> tuple[str, tuple]:
    """Sort wheels by project name, then by version (0.1.10 > 0.1.9)."""
    match = WHEEL_NAME.match(path.name)
    name, version = match.group("name", "version") if match else (path.name, "0")
    return name, tuple(
        int(part) if part.isdigit() else 0 for part in version.split(".")
    )


def pyodide_version() -> str | None:
    """Ask the locally installed pyodide-build which pyodide the wheels target."""
    try:
        out = subprocess.run(
            ["pyodide", "config", "get", "pyodide_version"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return out or None


def url_of(path: Path) -> str | None:
    try:
        return "/" + path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        print(f"{path}: outside the repository root, skipped", file=sys.stderr)
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "wheel_dirs",
        nargs="*",
        type=Path,
        default=[REPO_ROOT / "dist"],
        help="directories to scan for wasm wheels (default: dist/)",
    )
    parser.add_argument("--pyodide-version", default=None)
    args = parser.parse_args()

    # Wasm wheels are tagged pyodide_2024_0 / pyemscripten_2024_0 / emscripten_3_1_58.
    # Older builds pile up in dist/, so keep only the newest one per project.
    newest: dict[str, Path] = {}
    for wheel_dir in args.wheel_dirs:
        found = {
            wheel
            for pattern in ("*pyodide*.whl", "*pyemscripten*.whl", "*emscripten*.whl")
            for wheel in wheel_dir.glob(pattern)
        }
        for wheel in sorted(found, key=sort_key):
            newest[sort_key(wheel)[0]] = wheel

    wheels = [url for wheel in sorted(newest.values()) if (url := url_of(wheel))]

    files = {}
    for test in sorted((REPO_ROOT / "tests").glob("test_*.py")):
        if url := url_of(test):
            files[url] = "/tmp/" + test.relative_to(REPO_ROOT).as_posix()
    data_dir = REPO_ROOT / "data"
    if data_dir.is_dir():
        for data in sorted(p for p in data_dir.rglob("*") if p.is_file()):
            if url := url_of(data):
                files[url] = "/tmp/" + data.relative_to(REPO_ROOT).as_posix()

    config = {
        "pyodide_version": args.pyodide_version or pyodide_version() or "0.27.8",
        "wheels": wheels,
        "files": files,
    }
    # A local mirror (tests/pyodide/pyodide-dist) wins over the CDN.
    if (HERE / "pyodide-dist" / "pyodide.js").exists():
        config["indexURL"] = "/tests/pyodide/pyodide-dist/"
    (HERE / "wheels.json").write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps(config, indent=2))
    return 0 if wheels else 1


if __name__ == "__main__":
    sys.exit(main())
