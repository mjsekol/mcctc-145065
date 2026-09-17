# brief_check.py
# Checks an emerging technology brief against the Unit 0 project rules.
#
#     python brief_check.py brief.md
#
# It checks structure and sourcing. It cannot tell whether anything you wrote
# is true. You do that, by opening every source you cite.
#
# Exit code 0 means every check passed. Exit code 1 means at least one failed.

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Summary",
    "## The technology",
    "## Architecture",
    "## How it joins existing systems",
    "## Value to the buyer",
    "## Costs and risks",
    "## Recommendation",
    "## Sources",
]
MIN_WORDS = 600
MAX_WORDS = 1500
MIN_SOURCES = 3
SOURCE_TYPES = {"government", "standards", "academic", "industry-group",
                "news", "vendor", "documentation"}

# A figure that needs an owner: a percentage, a dollar amount, or a large count.
FIGURE = re.compile(
    r"\d[\d,.]*\s*(%|percent\b)|\$\s?\d|\d[\d,.]*\s*(million|billion|trillion)\b",
    re.IGNORECASE)
CITATION = re.compile(r"\[(\d+)\]")
LEFTOVERS = ["[VERIFY]", "TODO", "[student"]


def split_brief(text):
    """Return (body_lines, source_lines). Code blocks are dropped from the body."""
    body, sources = [], []
    in_code = False
    in_sources = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.strip() == "## Sources":
            in_sources = True
            continue
        (sources if in_sources else body).append(line)
    return body, sources


def check_headings(text):
    lines = [line.strip() for line in text.splitlines()]
    missing = [h for h in REQUIRED_HEADINGS if h not in lines]
    if missing:
        return ("Required headings", False, "missing " + ", ".join(missing))
    return ("Required headings", True, f"all {len(REQUIRED_HEADINGS)} present")


def check_length(body):
    prose = [line for line in body if not line.startswith("#")]
    words = len(" ".join(prose).split())
    passed = MIN_WORDS <= words <= MAX_WORDS
    return ("Length", passed, f"{words} words, need {MIN_WORDS} to {MAX_WORDS}")


def parse_sources(source_lines):
    """Return {number: line} for lines shaped like '1. ...'."""
    found = {}
    for line in source_lines:
        match = re.match(r"\s*(\d+)\.\s+(.*)", line)
        if match:
            found[int(match.group(1))] = match.group(2)
    return found


def check_sources(sources):
    problems = []
    if len(sources) < MIN_SOURCES:
        problems.append(f"{len(sources)} sources, need at least {MIN_SOURCES}")
    types = []
    for number, line in sorted(sources.items()):
        if "http://" not in line and "https://" not in line:
            problems.append(f"source {number} has no URL")
        type_match = re.search(r"Type:\s*([\w-]+)", line)
        if not type_match or type_match.group(1).lower() not in SOURCE_TYPES:
            problems.append(f"source {number} has no allowed Type")
        else:
            types.append(type_match.group(1).lower())
    if types and all(t == "vendor" for t in types):
        problems.append("every source is a vendor")
    if problems:
        return ("Sources", False, "; ".join(problems))
    return ("Sources", True, f"{len(sources)} sources, each with a URL and a type")


def check_citations(body, sources):
    cited = set()
    for line in body:
        cited.update(int(n) for n in CITATION.findall(line))
    unknown = sorted(n for n in cited if n not in sources)
    unused = sorted(n for n in sources if n not in cited)
    problems = []
    if unknown:
        problems.append("cites missing sources " + ", ".join(map(str, unknown)))
    if unused:
        problems.append("never cites sources " + ", ".join(map(str, unused)))
    if problems:
        return ("Citations", False, "; ".join(problems))
    return ("Citations", True, f"{len(cited)} sources cited, all listed")


def units_of_text(body):
    """Yield paragraphs and list items as single strings, and each table row alone.

    A figure's owner may sit on the next wrapped line of the same paragraph, so
    wrapped lines are joined. A table row is checked by itself, because one
    labelled row must not vouch for the rows around it.
    """
    current = []
    for line in body:
        stripped = line.strip()
        starts_new = (not stripped or stripped.startswith("#") or stripped.startswith("|")
                      or re.match(r"(-|\*|\d+\.)\s", stripped))
        if starts_new and current:
            yield " ".join(current)
            current = []
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("|"):
            yield stripped
            continue
        current.append(stripped)
    if current:
        yield " ".join(current)


def check_figures(body):
    # Table rows count too, because a table is where figures hide.
    unsupported = []
    for unit in units_of_text(body):
        if FIGURE.search(unit) and not CITATION.search(unit) \
                and "(assumption)" not in unit.lower():
            unsupported.append(unit[:60])
    if unsupported:
        return ("Figures have owners", False,
                f"{len(unsupported)} paragraph(s) or row(s) with a figure and no [n] or (assumption): "
                + " | ".join(unsupported))
    return ("Figures have owners", True, "every figure is cited or labelled")


def check_leftovers(text):
    found = [marker for marker in LEFTOVERS if marker in text]
    if found:
        return ("No leftover markers", False, "still contains " + ", ".join(found))
    return ("No leftover markers", True, "none found")


def main():
    if len(sys.argv) != 2:
        print("Usage: python brief_check.py brief.md")
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"No such file: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    body, source_lines = split_brief(text)
    sources = parse_sources(source_lines)
    results = [
        check_headings(text),
        check_length(body),
        check_sources(sources),
        check_citations(body, sources),
        check_figures(body),
        check_leftovers(text),
    ]
    print(f"BRIEF CHECK: {path.name}")
    for name, passed, detail in results:
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    passed_count = sum(1 for _, passed, _ in results if passed)
    print(f"{passed_count} of {len(results)} checks passed")
    print("This checker cannot tell whether your claims are true. Open every source.")
    return 0 if passed_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
