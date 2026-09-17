"""sim_control.py . 145065 HMI anchor . Line 3 sensor service

Switch a running simulator's mode from a second terminal, and read what the
panel would read. Python standard library only.

    python sim_control.py --port 8660 mode              # show the current mode
    python sim_control.py --port 8660 mode drift        # switch to drift
    python sim_control.py --port 8660 mode drop-sensor --sensor coolant-level
    python sim_control.py --port 8660 read              # one GET /api/readings

This talks to the simulator, not to equipment. Nothing here switches a machine.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

from backends import MODES


def call(url: str, body: dict | None = None, timeout: float = 3.0) -> tuple[int, str]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="GET" if body is None else "POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as reply:
            return reply.status, reply.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as reply:
        return reply.code, reply.read().decode("utf-8", "replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Control the Line 3 sensor simulator.")
    parser.add_argument("--port", type=int, required=True, help="the port the service runs on")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--timeout", type=float, default=3.0, help="seconds to wait (default 3)")
    sub = parser.add_subparsers(dest="command", required=True)
    mode = sub.add_parser("mode", help="show or switch the simulator mode")
    mode.add_argument("name", nargs="?", choices=MODES)
    mode.add_argument("--sensor", default=None, help="for drop-sensor: which sensor fails")
    sub.add_parser("read", help="GET /api/readings once and print it")
    args = parser.parse_args(argv)

    base = f"http://{args.host}:{args.port}"
    try:
        if args.command == "read":
            status, text = call(f"{base}/api/readings", timeout=args.timeout)
        elif args.name is None:
            status, text = call(f"{base}/sim/mode", timeout=args.timeout)
        else:
            body = {"mode": args.name}
            if args.sensor:
                body["sensor"] = args.sensor
            status, text = call(f"{base}/sim/mode", body, timeout=args.timeout)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as problem:
        # silent mode lands here on "read": the service never answers.
        reason = getattr(problem, "reason", problem)
        print(f"No answer from {base}: {reason}", file=sys.stderr)
        return 1
    print(status, text)
    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    sys.exit(main())
