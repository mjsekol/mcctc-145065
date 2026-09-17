"""Check the shape of your Python-to-C# port before you submit it.

Run from anywhere:   python port_check.py path/to/your-port

It checks that the pieces exist and are in the right form. It cannot tell
you whether your comparison is true or your design is good. A person does
that, in the walkthrough and in grading.

Standard library only. Nothing is installed and nothing is changed.
"""

import re
import sys
from pathlib import Path

REQUIRED_FILES = ["README.md", "COMPARISON.md", "DECISION_LOG.md", "WALKTHROUGH.md", "IMPACT.md"]
COMPARISON_HEADINGS = [
    "what the compiler caught",
    "what the compiler did not catch",
    "what is more verbose in c#",
]
MIN_CATCHES = 5
IGNORED_PARTS = {"bin", "obj", ".git", ".vs"}


def source_files(root, pattern):
    return [p for p in root.rglob(pattern) if not IGNORED_PARTS.intersection(p.parts)]


def check(root):
    results = []

    def report(ok, message):
        results.append((ok, message))

    for name in REQUIRED_FILES:
        report((root / name).is_file(), f"{name} exists")

    python_dir = root / "python"
    py_files = source_files(python_dir, "*.py") if python_dir.is_dir() else []
    report(bool(py_files), "python/ holds your Unit 2 hierarchy")
    report(any(p.name.startswith("test") for p in py_files), "python/ keeps its tests")

    csharp_dir = root / "csharp"
    slns = list(csharp_dir.glob("*.sln")) if csharp_dir.is_dir() else []
    slnx = list(csharp_dir.glob("*.slnx")) if csharp_dir.is_dir() else []
    report(len(slns) == 1 and not slnx,
           "csharp/ has one classic .sln (dotnet new sln --format sln), no .slnx")

    projects = source_files(csharp_dir, "*.csproj") if csharp_dir.is_dir() else []
    tests = [p for p in projects if "IsTestProject" in p.read_text(encoding="utf-8")
             or p.stem.endswith(".Tests")]
    libraries = [p for p in projects if p not in tests
                 and "<OutputType>Exe</OutputType>" not in p.read_text(encoding="utf-8")]
    report(bool(libraries), "a C# class library project")
    report(bool(tests), "a C# test project")
    for project in projects:
        text = project.read_text(encoding="utf-8")
        report("<TargetFramework>net8.0</TargetFramework>" in text, f"{project.name} targets net8.0")
    for library in libraries:
        text = library.read_text(encoding="utf-8")
        report("<TreatWarningsAsErrors>true</TreatWarningsAsErrors>" in text,
               f"{library.name} treats warnings as errors")

    code = "\n".join(p.read_text(encoding="utf-8") for p in source_files(csharp_dir, "*.cs")
                     if not any(t.parent in p.parents for t in tests)) if csharp_dir.is_dir() else ""
    interfaces = re.findall(r"\binterface\s+(I[A-Z]\w*)", code)
    best = 0
    for name in interfaces:
        implementers = set(re.findall(r"\bclass\s+(\w+)[^{;]*:\s*[^{;]*\b" + name + r"\b", code))
        best = max(best, len(implementers))
    report(bool(interfaces), "at least one interface in the library")
    report(best >= 2, "an interface with at least two implementing classes")
    report(bool(re.search(r"\b(private|protected|internal)\b", code)),
           "access modifiers other than public are used")
    report(bool(re.search(r"\bswitch\b", code)), "a switch statement or expression")

    comparison = root / "COMPARISON.md"
    if comparison.is_file():
        text = comparison.read_text(encoding="utf-8")
        lower = text.lower()
        for heading in COMPARISON_HEADINGS:
            report(re.search(r"^#+\s+" + re.escape(heading), lower, re.M) is not None,
                   f"COMPARISON.md has a section named '{heading}'")
        fenced = "\n".join(re.findall(r"```(?:\w*)\n(.*?)```", text, re.S))
        codes = sorted(set(re.findall(r"\b(?:error|warning) (CS\d{4})\b", fenced)))
        report(len(codes) >= MIN_CATCHES,
               f"COMPARISON.md quotes at least {MIN_CATCHES} different compiler messages "
               f"in code blocks (found {len(codes)}: {', '.join(codes) or 'none'})")

    impact = root / "IMPACT.md"
    if impact.is_file():
        report("CS0535" in impact.read_text(encoding="utf-8"),
               "IMPACT.md quotes the CS0535 list from the interface change")

    decisions = root / "DECISION_LOG.md"
    if decisions.is_file():
        lower = decisions.read_text(encoding="utf-8").lower()
        report("rejected" in lower, "DECISION_LOG.md names a design you rejected")

    ignore = root / ".gitignore"
    ignore_text = ignore.read_text(encoding="utf-8") if ignore.is_file() else ""
    report("bin" in ignore_text and "obj" in ignore_text, ".gitignore excludes bin/ and obj/")

    return results


def main():
    if len(sys.argv) != 2:
        print("usage: python port_check.py path/to/your-port")
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"not a folder: {root}")
        return 2
    results = check(root)
    for ok, message in results:
        print(f"[{'ok' if ok else 'MISSING'}] {message}")
    missing = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - missing} of {len(results)} checks passed")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
