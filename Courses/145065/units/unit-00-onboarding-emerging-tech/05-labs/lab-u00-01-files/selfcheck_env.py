# selfcheck_env.py
# Tries your env_check.py functions against situations you cannot easily
# create on your own machine: an old Python, no virtual environment, no git,
# and project folders with pieces missing.
#
# Put this file next to env_check.py and run:
#     python selfcheck_env.py
#
# It creates throwaway folders in your system's temporary folder and removes
# them when it finishes. It never touches your project folder.

import tempfile
from pathlib import Path

import env_check

results = []


def expect(label, result, want_passed):
    # A check that is not written yet returns None. Say so plainly
    # instead of crashing, so Part 1 can be tested before Part 2 exists.
    if result is None:
        results.append(("NOT WRITTEN", label))
        return
    name, passed, detail = result
    if passed == want_passed and isinstance(detail, str) and detail:
        results.append(("PASS", label))
    else:
        results.append(("FAIL", f"{label} (got passed={passed}, detail={detail!r})"))


# ---------- Part 1 ----------
expect("Python 3.14 passes", env_check.check_python_version((3, 14, 0)), True)
expect("Python 3.13 passes", env_check.check_python_version((3, 13, 7)), True)
expect("Python 3.9 fails", env_check.check_python_version((3, 9, 18)), False)
expect("Python 2.7 fails", env_check.check_python_version((2, 7, 18)), False)
expect("inside a venv passes",
       env_check.check_virtual_environment("C:/proj/.venv", "C:/Python314"), True)
expect("outside a venv fails",
       env_check.check_virtual_environment("C:/Python314", "C:/Python314"), False)
expect("git found passes",
       env_check.check_git_available(lambda name: "C:/Program Files/Git/cmd/git.exe"), True)
expect("git missing fails",
       env_check.check_git_available(lambda name: None), False)

# ---------- Part 2 ----------
with tempfile.TemporaryDirectory() as temp:
    good = Path(temp) / "good"
    good.mkdir()
    (good / ".git").mkdir()
    (good / "README.md").write_text("# Line 3 tools\n\n## How to run\n\npython env_check.py\n",
                                    encoding="utf-8")
    (good / ".gitignore").write_text(".venv/\n.env\n__pycache__/\n", encoding="utf-8")
    (good / "decision-log.md").write_text("# Decision log\n", encoding="utf-8")

    bare = Path(temp) / "bare"
    bare.mkdir()
    (bare / "README.md").write_text("# Notes\n\nSomeday this will say how to run it.\n",
                                    encoding="utf-8")
    (bare / ".gitignore").write_text(".venv\n", encoding="utf-8")

    expect("complete folder: required files", env_check.check_required_files(good), True)
    expect("bare folder: required files", env_check.check_required_files(bare), False)
    expect("complete folder: repository", env_check.check_repository(good), True)
    expect("bare folder: repository", env_check.check_repository(bare), False)
    expect("complete folder: .gitignore", env_check.check_gitignore(good), True)
    expect("bare folder: .gitignore", env_check.check_gitignore(bare), False)
    expect("complete folder: README run section",
           env_check.check_readme_run_section(good), True)
    expect("bare folder: README run section",
           env_check.check_readme_run_section(bare), False)

for status, label in results:
    print(f"{status:<12}{label}")

passed = sum(1 for status, _ in results if status == "PASS")
print(f"\n{passed} of {len(results)} self-checks passed")
