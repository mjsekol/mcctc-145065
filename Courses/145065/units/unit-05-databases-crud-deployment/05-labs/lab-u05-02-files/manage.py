"""
manage.py · create and inspect the Line 3 database

    python manage.py init --db instance/line3.db            schema and starting data
    python manage.py init --db instance/line3.db --no-seed  empty tables only
    python manage.py init --db instance/line3.db --force    delete and rebuild an existing one
    python manage.py init-if-empty                          safe on every deploy: builds only if no tables exist
    python manage.py tables --db instance/line3.db          rows per table

When DATABASE_URL is set, every command works on that PostgreSQL database
and --db is ignored. [VERIFY on a lab machine or on Render]

The database is data, not code. Never commit a database file.
"""

import argparse
import os
import pathlib
import sys

import db

HERE = pathlib.Path(__file__).parent


def main(argv=None, environ=None):
    env = os.environ if environ is None else environ
    parser = argparse.ArgumentParser(description="Line 3 database tasks")
    parser.add_argument("command", choices=["init", "init-if-empty", "tables"])
    parser.add_argument("--db", default=env.get("DATABASE_PATH", str(HERE / "instance" / "line3.db")))
    parser.add_argument("--no-seed", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    url = env.get("DATABASE_URL", "")
    config = {"DATABASE_URL": url, "DATABASE_PATH": args.db}
    where = "the PostgreSQL database in DATABASE_URL" if url else args.db
    path = pathlib.Path(args.db)

    if not url and args.command != "tables":
        path.parent.mkdir(parents=True, exist_ok=True)
    if not url and args.command == "tables" and not path.exists():
        print(f"No database at {path}.")
        return 1

    conn = db.connect(config, create=args.command != "tables")
    try:
        existing = db.table_names(conn)
        if args.command == "tables":
            for name, count in db.table_counts(conn).items():
                print(f"{name}: {count} row(s)")
            return 0
        if existing and args.command == "init-if-empty":
            print(f"{where} already has tables. Nothing changed.")
            return 0
        if existing and not args.force:
            print(f"{where} already has tables. Add --force to delete every record and rebuild it.")
            return 1
        db.create_schema(conn, seed=not args.no_seed)
        print(f"Created the tables in {where}{'' if args.no_seed else ' with the starting data'}.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
