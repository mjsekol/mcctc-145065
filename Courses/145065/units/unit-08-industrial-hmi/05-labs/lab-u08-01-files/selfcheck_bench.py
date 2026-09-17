"""selfcheck_bench.py . Lab U08-01 . 145065 Unit 8

Checks your contract_problems() and sequence_advanced() against canned
replies. No service needs to be running. Run it from this folder:

    python selfcheck_bench.py

Every reply below is invented sample data in the Line 3 contract's shape.
"""

from __future__ import annotations

import json
import sys

from bench_check import contract_problems, sequence_advanced

GOOD = {
    "device": "line3-pi",
    "sequence": 1042,
    "sampled_at": "2027-01-11T14:03:22Z",
    "sensors": [
        {"id": "oven-temp", "kind": "temperature", "value": 212.4, "unit": "C", "ok": True},
        {"id": "press-vibration", "kind": "vibration", "value": 3.1, "unit": "mm/s", "ok": True},
        {"id": "coolant-level", "kind": "level", "value": None, "unit": "%", "ok": False},
    ],
}

# What the simulator sends in garbage mode: a real reply cut off mid-object.
GARBAGE = '{"device": "line3-pi", "sequence": 17, "sampled_at": "2027-01-11T14:0'


def changed(**edits) -> str:
    """GOOD with some top-level keys replaced. A value of ... deletes the key."""
    reply = json.loads(json.dumps(GOOD))
    for key, value in edits.items():
        if value is ...:
            del reply[key]
        else:
            reply[key] = value
    return json.dumps(reply)


def with_sensor(index: int, **edits) -> str:
    reply = json.loads(json.dumps(GOOD))
    reply["sensors"][index].update(edits)
    return json.dumps(reply)


def mentions(problems: list[str], *words: str) -> bool:
    text = " ".join(problems).lower()
    return len(problems) > 0 and all(word.lower() in text for word in words)


CHECKS = [
    ("a good reply has no problems (a failed sensor is allowed)",
     lambda: contract_problems(json.dumps(GOOD)) == []),
    ("garbage mode's cut-off reply is not valid JSON",
     lambda: mentions(contract_problems(GARBAGE), "json")),
    ("a reply with no sequence says so",
     lambda: mentions(contract_problems(changed(sequence=...)), "sequence")),
    ("true is not a sequence number",
     lambda: mentions(contract_problems(changed(sequence=True)), "sequence")),
    ("a time with no Z is refused",
     lambda: mentions(contract_problems(changed(sampled_at="2027-01-11T14:03:22")), "sampled_at")),
    ("ok true with a null value names the sensor",
     lambda: mentions(contract_problems(with_sensor(0, value=None)), "oven-temp")),
    ("ok false with a value names the sensor",
     lambda: mentions(contract_problems(with_sensor(2, value=0.0)), "coolant-level")),
    ("the same id twice is refused",
     lambda: mentions(contract_problems(with_sensor(1, id="oven-temp")), "twice")),
    ("1041 then 1042 has advanced",
     lambda: sequence_advanced(changed(sequence=1041), changed(sequence=1042)) is True),
    ("1042 then 1042 has not advanced",
     lambda: sequence_advanced(changed(sequence=1042), changed(sequence=1042)) is False),
    ("a Pi restart, 900 then 1, counts as new",
     lambda: sequence_advanced(changed(sequence=900), changed(sequence=1)) is True),
    ("an unreadable second reply is not evidence of anything",
     lambda: sequence_advanced(changed(sequence=5), GARBAGE) is False),
]


def main() -> int:
    passed = 0
    for number, (name, check) in enumerate(CHECKS, 1):
        try:
            ok = bool(check())
        except Exception as problem:  # noqa: BLE001  report, do not crash
            ok = False
            name = f"{name}  (raised {type(problem).__name__}: {problem})"
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {number:2}. {name}")
    print(f"{passed} of {len(CHECKS)} self-checks passed.")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
