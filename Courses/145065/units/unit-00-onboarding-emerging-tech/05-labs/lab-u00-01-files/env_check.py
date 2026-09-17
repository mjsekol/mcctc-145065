# env_check.py
# Checks that this machine and this project folder are ready for 145065 work.
#
# STARTER FILE. It runs right now and checks nothing.
# Every check you write returns three things in a tuple:
#     (name of the check, True or False, a detail a person can act on)
# so print_report can print every check the same way.
#
# Run it from your project folder:
#     python env_check.py
# or point it at a folder:
#     python env_check.py path/to/folder

import shutil
import sys
from pathlib import Path

# The oldest Python this course accepts, as (major, minor).
MINIMUM_PYTHON = (3, 13)

# Part 2 uses these.
REQUIRED_FILES = ["README.md", ".gitignore", "decision-log.md"]
IGNORE_MUST_LIST = [".venv", ".env", "__pycache__"]


# ---------- Part 1: the machine ----------

def check_python_version(version_info=sys.version_info):
    # TODO 1: compare the running version against MINIMUM_PYTHON.
    return None


def check_virtual_environment(prefix=sys.prefix, base_prefix=sys.base_prefix):
    # TODO 2: decide whether this program is running inside a virtual environment.
    return None


def check_git_available(finder=shutil.which):
    # TODO 3: find out whether the git program can be found on this machine.
    return None


# ---------- Part 2: the project folder ----------

def check_required_files(folder):
    # TODO 4: report any file from REQUIRED_FILES that is missing.
    return None


def check_repository(folder):
    # TODO 5: decide whether the folder is a Git repository.
    return None


def check_gitignore(folder):
    # TODO 6: report any entry from IGNORE_MUST_LIST that .gitignore does not list.
    return None


def check_readme_run_section(folder):
    # TODO 7: confirm README.md has a "## How to run" heading.
    return None


# ---------- The report ----------

def run_checks(folder):
    checks = [
        check_python_version(),
        check_virtual_environment(),
        check_git_available(),
        check_required_files(folder),
        check_repository(folder),
        check_gitignore(folder),
        check_readme_run_section(folder),
    ]
    # Unwritten checks return None. Leave them out of the report for now.
    return [result for result in checks if result is not None]


def print_report(results):
    print("ENVIRONMENT CHECK")
    print("-----------------")
    if not results:
        print("No checks written yet.")
        return
    for name, passed, detail in results:
        label = "PASS" if passed else "FAIL"
        print(f"{label}  {name}: {detail}")


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    results = run_checks(folder)
    print_report(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
