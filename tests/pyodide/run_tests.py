"""Run pytest for the files given on the command line, capturing all output.

Executed inside pyodide by ``index.html``; returns a JSON-serializable dict so
the page can show the pytest output and the exit code.
"""

from __future__ import annotations

import io
import sys
import traceback


def main(test_files):
    import pytest

    buf = io.StringIO()
    stdout, stderr = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = buf
    try:
        exit_code = pytest.main(
            ["-v", "-p", "no:cacheprovider", "--tb=short", *test_files]
        )
    except Exception:
        traceback.print_exc(file=buf)
        exit_code = 99
    finally:
        sys.stdout, sys.stderr = stdout, stderr
    return {"exit_code": int(exit_code), "output": buf.getvalue()}
