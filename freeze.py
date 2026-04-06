"""Generate a static snapshot of key views into the `docs/` folder.

This script uses Flask's test client to GET pages and writes the HTML
to `docs/`. It also copies `PeakPulse/static` into `docs/static`.

Run: `python freeze.py` from the repository root (venv recommended).
"""
from pathlib import Path
import shutil

import sys
import os

# Make the package modules importable when running from the repository root.
# The project's application files live in the `PeakPulse/` directory and use
# top-level imports like `from models import ...`, so add that folder to
# `sys.path` before importing the app module.
repo_root = Path(__file__).resolve().parent
peakpulse_dir = repo_root / "PeakPulse"
sys.path.insert(0, str(peakpulse_dir))

try:
    import app as flask_app_module
    flask_app = flask_app_module.app
except Exception:
    # Fall back to trying to import as a package
    from importlib import import_module
    flask_app = import_module("PeakPulse.app").app


def write_response(path: str, out_file: Path):
    with flask_app.test_client() as client:
        resp = client.get(path)
        if resp.status_code == 200:
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(resp.data)
            print(f"Wrote {out_file}")
        else:
            print(f"Warning: {path} returned {resp.status_code}")


def main():
    root = Path(__file__).resolve().parent
    docs = root / "docs"

    # Remove existing docs/ to ensure a clean snapshot
    if docs.exists():
        shutil.rmtree(docs)
    docs.mkdir(parents=True)

    pages = {
        "/": "index.html",
        "/timer": "timer.html",
        "/dashboard": "dashboard.html",
    }

    for url, filename in pages.items():
        write_response(url, docs / filename)

    # Copy static assets
    static_src = root / "PeakPulse" / "static"
    static_dst = docs / "static"
    if static_src.exists():
        shutil.copytree(static_src, static_dst)
        print(f"Copied static files to {static_dst}")
    else:
        print("No static/ folder found at PeakPulse/static")

    print("Static snapshot complete. Commit and push the `docs/` folder to publish on GitHub Pages.")


if __name__ == "__main__":
    main()
