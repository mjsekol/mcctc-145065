"""
import_csv.py · load issues from a CSV file into the Line 3 database

Every row is checked with the same rules the form uses. If any row fails,
nothing is imported, and every problem is listed with its line number. Half an
import is worse than none: you cannot tell which rows made it in.

    python import_csv.py data/issues_import.csv --db instance/line3.db
    python import_csv.py data/issues_import_bad.csv --db instance/line3.db --dry-run

The file needs this header row:
    equipment_code,reported_by,title,description,severity,status,
    downtime_minutes,locked_out,reported_at,closed_at

utf-8-sig reads plain UTF-8 and also the UTF-8 files Excel saves, which start
with an invisible byte order mark. Without it, the first column name would
arrive as "\\ufeffequipment_code" and every row would fail.
"""

import argparse
import csv
import os
import pathlib
import sys

import db
from validation import validate_import_row

HERE = pathlib.Path(__file__).parent
REQUIRED_COLUMNS = ["equipment_code", "reported_by", "title", "description", "severity",
                    "status", "downtime_minutes", "locked_out", "reported_at", "closed_at"]


def read_rows(csv_path, conn):
    """Return (clean_rows, problems). problems is a list of printable lines."""
    codes, badges = db.equipment_codes(conn), db.active_badges(conn)
    clean_rows, problems = [], []
    with open(csv_path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [], [f"header: missing column(s) {', '.join(missing)}"]
        # Line 1 is the header, so the first data row is line 2.
        for line_no, row in enumerate(reader, start=2):
            clean, errors = validate_import_row(row, codes, badges)
            for field, message in errors.items():
                problems.append(f"line {line_no}: {field}: {message}")
            if not errors:
                clean_rows.append(clean)
    return clean_rows, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Import issues from CSV")
    parser.add_argument("csv_file")
    parser.add_argument("--db", default=os.environ.get("DATABASE_PATH",
                                                       str(HERE / "instance" / "line3.db")))
    parser.add_argument("--dry-run", action="store_true", help="check every row, import nothing")
    args = parser.parse_args(argv)

    if not pathlib.Path(args.db).exists():
        print(f"No database at {args.db}. Run: python manage.py init --db {args.db}")
        return 1
    conn = db.connect(args.db)
    try:
        rows, problems = read_rows(args.csv_file, conn)
        if problems:
            print(f"Nothing imported. {len(problems)} problem(s):")
            for line in problems:
                print(f"  {line}")
            return 1
        if args.dry_run:
            print(f"Dry run: all {len(rows)} row(s) are valid. Nothing imported.")
            return 0
        ids = db.import_issues(conn, rows)
        print(f"Imported {len(ids)} issue(s): ids {ids[0]} to {ids[-1]}." if ids
              else "The file has no data rows.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
