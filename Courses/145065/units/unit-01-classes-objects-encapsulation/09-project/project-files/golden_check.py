# golden_check.py
# Unit 1 refactor project. Proves a refactor kept the program's behavior.
#
# A refactor changes how code is organized and never what it does. This tool
# runs your old program once and saves everything it produced: what it
# printed, its exit code, and any output files. That saved copy is the
# "golden" baseline. After every change, it runs your new program the same way
# and compares, line by line.
#
# From your unit-01-refactor folder:
#
#   python golden_check.py record  --dir before --outputs output --clean -- python pipeline.py
#   python golden_check.py compare --dir after  --outputs output --clean -- python pipeline.py
#
# Everything after "--" is the command, run inside --dir. Add whatever your
# program needs, such as a URL or a file name.
#
#   --dir DIR         the folder to run the command in (default: this folder)
#   --outputs PATH    a file or folder the program writes, relative to --dir;
#                     repeat it for more than one
#   --clean           delete each --outputs path before running, so an old
#                     file cannot hide a missing new one
#   --ignore REGEX    skip lines that match, such as a timestamp; repeatable,
#                     and every use must be explained in CLASS_BOUNDARIES.md
#   --golden DIR      where the baseline is saved (default: golden)
#
# Standard library only. It never changes your program's files, and it only
# deletes the --outputs paths you name, and only with --clean.

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

TIMEOUT_SECONDS = 300


def parse_args(argv):
    if "--" not in argv:
        raise SystemExit("Put the command after --, for example:  -- python pipeline.py")
    split = argv.index("--")
    options, command = argv[:split], argv[split + 1:]
    if not command:
        raise SystemExit("There is no command after --.")
    parser = argparse.ArgumentParser(prog="golden_check.py")
    parser.add_argument("mode", choices=["record", "compare"])
    parser.add_argument("--dir", default=".")
    parser.add_argument("--outputs", action="append", default=[])
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--ignore", action="append", default=[])
    parser.add_argument("--golden", default="golden")
    args = parser.parse_args(options)
    args.command = command
    return args


def inside(child, parent):
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def prepare_outputs(workdir, outputs, clean):
    """Delete old outputs with --clean, or refuse to run if any exist without it."""
    for name in outputs:
        path = workdir / name
        if not inside(path, workdir) or path.resolve() == workdir.resolve():
            raise SystemExit(f"--outputs {name} must be inside {workdir}, not the folder itself.")
        if not path.exists():
            continue
        if not clean:
            raise SystemExit(f"{path} already exists. Delete it, or add --clean, so an old file "
                             f"cannot pass for a new one.")
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def run_program(workdir, command):
    try:
        result = subprocess.run(command, cwd=workdir, capture_output=True, timeout=TIMEOUT_SECONDS)
    except FileNotFoundError:
        raise SystemExit(f"Could not run {command[0]!r}. Check the command after --.")
    except subprocess.TimeoutExpired:
        raise SystemExit(f"The program ran longer than {TIMEOUT_SECONDS} seconds and was stopped.")
    text = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    # Windows prints CR LF at the end of each line, and other systems print LF.
    # Keep one form.
    return result.returncode, text.replace("\r\n", "\n")


def collect_files(workdir, outputs):
    """Every output file, as {relative path with forward slashes: bytes}."""
    files = {}
    for name in outputs:
        path = workdir / name
        if path.is_file():
            files[Path(name).as_posix()] = path.read_bytes()
        elif path.is_dir():
            for item in sorted(path.rglob("*")):
                if item.is_file():
                    files[item.relative_to(workdir).as_posix()] = item.read_bytes()
    return files


def comparable_lines(text, patterns):
    lines = text.replace("\r\n", "\n").split("\n")
    return [line for line in lines if not any(pattern.search(line) for pattern in patterns)]


def first_difference(expected, actual):
    for number, (old, new) in enumerate(zip(expected, actual), start=1):
        if old != new:
            return f"line {number}\n      expected: {old!r}\n      got:      {new!r}"
    if len(expected) != len(actual):
        return f"expected {len(expected)} lines, got {len(actual)}"
    return None


def record(args, workdir, golden):
    prepare_outputs(workdir, args.outputs, args.clean)
    code, text = run_program(workdir, args.command)
    files = collect_files(workdir, args.outputs)
    if golden.exists():
        shutil.rmtree(golden)
    (golden / "files").mkdir(parents=True)
    # Bytes, not write_text: on Windows, write_text would turn each LF into
    # CR LF, and the baseline would no longer be what was printed.
    (golden / "stdout.txt").write_bytes(text.encode("utf-8"))
    (golden / "exit_code.txt").write_text(f"{code}\n", encoding="utf-8")
    (golden / "command.txt").write_text(" ".join(args.command) + "\n", encoding="utf-8")
    for name, data in files.items():
        target = golden / "files" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    printed = len(comparable_lines(text, []))
    print(f"Recorded the baseline in {golden}: exit code {code}, {printed} lines of output, "
          f"{len(files)} output files.")
    for name in files:
        print(f"  {name}")
    if code != 0:
        print("Warning: the program exited with an error. Is that really the behavior to keep?")
    return 0


def compare(args, workdir, golden):
    if not (golden / "stdout.txt").is_file():
        raise SystemExit(f"No baseline in {golden}. Run the record step on your old program first.")
    patterns = [re.compile(pattern) for pattern in args.ignore]
    prepare_outputs(workdir, args.outputs, args.clean)
    code, text = run_program(workdir, args.command)
    results = []

    expected_code = int((golden / "exit_code.txt").read_text(encoding="utf-8").strip())
    results.append(("exit code", None if code == expected_code
                    else f"expected {expected_code}, got {code}"))

    expected_text = (golden / "stdout.txt").read_bytes().decode("utf-8")
    results.append(("printed output", first_difference(comparable_lines(expected_text, patterns),
                                                       comparable_lines(text, patterns))))

    expected_files = {path.relative_to(golden / "files").as_posix(): path.read_bytes()
                      for path in sorted((golden / "files").rglob("*")) if path.is_file()}
    actual_files = collect_files(workdir, args.outputs)
    for name in sorted(set(expected_files) | set(actual_files)):
        if name not in actual_files:
            results.append((name, "the new program did not write this file"))
        elif name not in expected_files:
            results.append((name, "the new program wrote a file the old one did not"))
        else:
            old = comparable_lines(expected_files[name].decode("utf-8", errors="replace"), patterns)
            new = comparable_lines(actual_files[name].decode("utf-8", errors="replace"), patterns)
            results.append((name, first_difference(old, new)))

    matched = 0
    for label, problem in results:
        if problem is None:
            matched += 1
            print(f"MATCH      {label}")
        else:
            print(f"DIFFERENT  {label}: {problem}")
    print()
    if matched == len(results):
        print(f"GOLDEN CHECK PASSED: {matched} of {len(results)} match")
        return 0
    print(f"GOLDEN CHECK FAILED: {matched} of {len(results)} match")
    return 1


def main(argv):
    args = parse_args(argv)
    workdir = Path(args.dir)
    if not workdir.is_dir():
        raise SystemExit(f"--dir {args.dir} is not a folder.")
    golden = Path(args.golden)
    if args.mode == "record":
        return record(args, workdir, golden)
    return compare(args, workdir, golden)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
