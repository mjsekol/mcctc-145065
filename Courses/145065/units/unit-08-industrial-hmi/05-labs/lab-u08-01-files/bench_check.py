"""bench_check.py . Lab U08-01 . 145065 Unit 8 . STARTER

Checks that a Line 3 sensor service keeps its contract, before any panel
trusts a single number from it. Python standard library only.

    python bench_check.py --port 8700
    python bench_check.py --port 8700 --host 127.0.0.1

It asks the service five questions and prints PASS or FAIL for each:

    1. Does GET /health answer 200 with {"status": "ok"}?
    2. Does GET /api/readings answer 200 within the time limit?
    3. Does that reply keep the contract?          <- you write this check
    4. Did sequence change between two reads?      <- you write this check
    5. Did every sensor report a value?

The service is Riverside Fabrication's Line 3 sensor service. Riverside
Fabrication is a composite, invented for this course. This program only
READS. It never changes the simulator's mode and never controls anything.

STARTER STATE: it runs, reaches the service, and prints the table, but
checks 3 and 4 always FAIL, because contract_problems() and
sequence_advanced() are not written yet.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request

# How long one request may take before this program gives up. The Line 3
# panel uses the same limit, 1.5 seconds.
TIME_LIMIT_SECONDS = 1.5

# How long to wait between the two reads for check 4. The Pi samples once a
# second, so 1.5 seconds is long enough for at least one new sample.
GAP_SECONDS = 1.5

# The four keys every reply must have, and the five every sensor must have.
REPLY_KEYS = ("device", "sequence", "sampled_at", "sensors")
SENSOR_KEYS = ("id", "kind", "value", "unit", "ok")


def fetch(url: str, timeout: float = TIME_LIMIT_SECONDS) -> tuple[int | None, str, float]:
    """GET one address. Returns (status, body text, seconds taken).

    status is None when nothing answered in time or the connection failed.
    An HTTP error status such as 503 still counts as an answer.
    """
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as reply:
            body = reply.read().decode("utf-8", "replace")
            return reply.status, body, time.perf_counter() - started
    except urllib.error.HTTPError as reply:
        body = reply.read().decode("utf-8", "replace")
        return reply.code, body, time.perf_counter() - started
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        return None, "", time.perf_counter() - started


def contract_problems(text: str) -> list[str]:
    """Every way this reply breaks the contract. An empty list means it keeps it.

    YOUR JOB (steps 5 to 8). Return one short sentence per problem.
    """
    # TODO step 5: parse the text. Not JSON is a problem, and nothing else can be checked.
    # TODO step 6: the four reply keys, device, sequence, and sampled_at.
    # TODO step 7: sensors is a list, and each sensor has its five keys.
    # TODO step 8: ok and value agree, and no id appears twice.
    return ["contract_problems() is not written yet"]


def sequence_advanced(first_text: str, second_text: str) -> bool:
    """True when the second reply carries a different sequence than the first.

    YOUR JOB (step 9). Any change counts as new, including a smaller number,
    because a Pi that restarted starts counting again.
    """
    # TODO step 9
    return False


def every_sensor_reported(text: str) -> bool:
    """Check 5. True when every sensor says ok. Given to you."""
    try:
        sensors = json.loads(text)["sensors"]
        return all(sensor.get("ok") is True for sensor in sensors)
    except (ValueError, KeyError, TypeError, AttributeError):
        return False


def health_ok(status: int | None, body: str) -> bool:
    """Check 1. Given to you."""
    if status != 200:
        return False
    try:
        return json.loads(body) == {"status": "ok"}
    except ValueError:
        return False


def mark(passed: bool) -> str:
    return "PASS" if passed else "FAIL"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a Line 3 sensor service against the contract.")
    parser.add_argument("--port", type=int, required=True, help="the port the service listens on")
    parser.add_argument("--host", default="127.0.0.1", help="the service's address (default 127.0.0.1)")
    args = parser.parse_args(argv)
    base = f"http://{args.host}:{args.port}"

    print(f"Bench check for {base}")

    status, body, seconds = fetch(f"{base}/health")
    check1 = health_ok(status, body)
    print(f"  1. /health answers ok ............... {mark(check1)}  ({seconds:.2f} s)")

    status, first, seconds = fetch(f"{base}/api/readings")
    check2 = status == 200 and seconds <= TIME_LIMIT_SECONDS
    shown = "no answer" if status is None else f"status {status}"
    print(f"  2. /api/readings answers in time .... {mark(check2)}  ({shown}, {seconds:.2f} s)")

    problems = contract_problems(first) if status == 200 else ["no reply to check"]
    check3 = not problems
    print(f"  3. the reply keeps the contract ..... {mark(check3)}")
    for problem in problems:
        print(f"       - {problem}")

    time.sleep(GAP_SECONDS)
    status2, second, _ = fetch(f"{base}/api/readings")
    check4 = status == 200 and status2 == 200 and sequence_advanced(first, second)
    print(f"  4. sequence changed in {GAP_SECONDS} s ....... {mark(check4)}")

    check5 = status2 == 200 and every_sensor_reported(second)
    print(f"  5. every sensor reported a value .... {mark(check5)}")

    passed = sum([check1, check2, check3, check4, check5])
    print(f"{passed} of 5 checks passed.")
    return 0 if passed == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
