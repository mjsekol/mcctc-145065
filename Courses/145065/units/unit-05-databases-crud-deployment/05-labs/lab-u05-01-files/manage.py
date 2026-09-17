"""
manage.py · create the Line 3 database

    python manage.py init --db instance/line3.db            schema and starting data
    python manage.py init --db instance/line3.db --no-seed  empty tables only
    python manage.py init --db instance/line3.db --force    delete and rebuild an existing one
    python manage.py tables --db instance/line3.db          list the tables

--db defaults to the DATABASE_PATH environment variable, then instance/line3.db.

The database file is data, not code. Never commit it. Keep it outside the
repository or make sure .gitignore covers it.
"""

import argparse
import os
import pathlib
import sys

import db

HERE = pathlib.Path(__file__).parent


def main(argv=None):
    parser = argparse.ArgumentParser(description="Line 3 database tasks")
    parser.add_argument("command", choices=["init", "tables"])
    parser.add_argument("--db", default=os.environ.get("DATABASE_PATH",
                                                       str(HERE / "instance" / "line3.db")))
    parser.add_argument("--no-seed", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    path = pathlib.Path(args.db)

    if args.command == "init":
        if path.exists() and not args.force:
            print(f"{path} already exists. Add --force to delete every record and rebuild it.")
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        db.create_database(path, seed=not args.no_seed)
        print(f"Created {path}{'' if args.no_seed else ' with the starting data'}.")
        return 0

    if not path.exists():
        print(f"No database at {path}.")
        return 1
    conn = db.connect(path)
    try:
        for name, count in db.table_counts(conn).items():
            print(f"{name}: {count} row(s)")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
