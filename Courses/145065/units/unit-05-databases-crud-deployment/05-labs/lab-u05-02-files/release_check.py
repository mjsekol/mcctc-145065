"""
release_check.py · does every place that names the version agree?

A release is a promise: "the live app is version X, and RELEASE.md says what X
contains." The version is written in three places. This script reads all three
and refuses when they disagree.

    python release_check.py

1. APP_VERSION in app.py
2. the newest row of the table in RELEASE.md
3. what GET /health answers, from a throwaway database

Standard library plus the app itself. Exit 0 when all three agree, 1 when not.
"""

import json
import pathlib
import re
import sys
import tempfile

import db
from app import APP_VERSION, create_app

HERE = pathlib.Path(__file__).parent
ROW = re.compile(r"^\| (\d+\.\d+\.\d+) \|", re.MULTILINE)


def newest_release(text):
    """The last version row in RELEASE.md's table, or None."""
    rows = ROW.findall(text)
    return rows[-1] if rows else None


def health_version():
    with tempfile.TemporaryDirectory() as folder:
        path = pathlib.Path(folder) / "release_check.db"
        db.create_database(path)
        app = create_app(overrides={"DATABASE_PATH": str(path)},
                         environ={"APP_ENV": "test", "SECRET_KEY": "release-check-only"})
        with app.test_client() as client:
            answer = client.get("/health")
            return json.loads(answer.get_data(as_text=True))["version"]


def main():
    found = {
        "app.py APP_VERSION": APP_VERSION,
        "RELEASE.md newest row": newest_release((HERE / "RELEASE.md").read_text(encoding="utf-8")),
        "GET /health": health_version(),
    }
    for where, version in found.items():
        print(f"{where:24} {version}")
    if len(set(found.values())) == 1:
        print(f"OK: release {APP_VERSION} is consistent.")
        return 0
    print("MISMATCH: fix every place before you deploy or tag.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
