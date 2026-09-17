"""sensor_service.py . 145065 HMI anchor . Line 3 sensor service

The program that runs on the Line 3 Raspberry Pi, and on your lab machine as
a simulator. Python standard library only.

    GET  /api/readings   200, the newest sample (the contract in readings.py)
    GET  /health         200, {"status": "ok"}
    GET  /sim/mode       200, the current simulator mode (simulator only)
    POST /sim/mode       switch simulator mode, body {"mode": "drift"}
                         optional "sensor" for drop-sensor
                         409 when a hardware backend is running

Run it (from this folder):

    python sensor_service.py --port 8700
    python sensor_service.py --port 8700 --mode freeze
    python sensor_service.py --port 8700 --backend hardware      # lab Pi only [VERIFY]

There is no default port. You name one every time, and the service refuses a
port something else is already using, instead of quietly sharing it.

By default the service listens on 127.0.0.1, so only this machine can reach
it. On the lab Pi you pass --host with the Pi's address on the isolated lab
network. [VERIFY] that address with your instructor. Never expose this
service beyond the lab network: POST /sim/mode has no login.

Setting: Riverside Fabrication, Line 3, is a composite. It is not a real shop.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from backends import MODE_MEANING, MODES, Sampler, SensorBackend, SimulatedBackend

# How long a request is held open in silent mode before the socket is closed
# with no reply. Longer than any sensible client timeout, so the client is the
# one that gives up, the way it would with a pulled network cable.
SILENT_HOLD_SECONDS = 30.0

# The body garbage mode sends: the start of a real reply, cut off mid-object.
GARBAGE_BODY = b'{"device": "line3-pi", "sequence": 17, "sampled_at": "2027-01-11T14:0'

MAX_BODY_BYTES = 1024
PORT_MIN, PORT_MAX = 1024, 65535


class SensorServer(ThreadingHTTPServer):
    """An HTTP server that knows its sampler and, if simulated, its simulator."""

    daemon_threads = True
    # Do not wait for held silent-mode requests when shutting down.
    block_on_close = False
    # On Windows, SO_REUSEADDR lets two programs bind the same port at once.
    # That is the opposite of what you want, so it is only on elsewhere.
    allow_reuse_address = os.name != "nt"

    def __init__(self, address: tuple[str, int], sampler: Sampler) -> None:
        self.sampler = sampler
        backend: SensorBackend = sampler.backend
        self.simulator = backend if isinstance(backend, SimulatedBackend) else None
        # Set when the server stops or the mode changes, so held requests let go.
        self.release_held = threading.Event()
        super().__init__(address, ReadingsHandler)

    def set_mode(self, mode: str, sensor: str | None) -> None:
        if self.simulator is None:
            raise PermissionError("simulator modes are unavailable with a hardware backend")
        self.simulator.set_mode(mode, sensor)
        # Wake any request that silent mode is holding, then re-arm.
        self.release_held.set()
        self.release_held = threading.Event()

    def current_mode(self) -> str | None:
        return None if self.simulator is None else self.simulator.mode


class ReadingsHandler(BaseHTTPRequestHandler):
    server: SensorServer
    server_version = "Line3SensorService/1.0"
    # Short socket timeout on reads from the client, so a slow client cannot
    # tie up a thread forever.
    timeout = 10

    # ---- routing -------------------------------------------------------

    def do_GET(self) -> None:  # noqa: N802  (name fixed by http.server)
        path = self.path.split("?", 1)[0]
        if path in ("/api/readings", "/health") and self._misbehave():
            return
        if path == "/api/readings":
            sample = self.server.sampler.latest()
            if sample is None:
                self._send_json(503, {"error": "no sample has been taken yet"})
            else:
                self._send_json(200, sample.to_json_dict())
        elif path == "/health":
            self._send_json(200, {"status": "ok"})
        elif path == "/sim/mode":
            mode = self.server.current_mode()
            if mode is None:
                self._send_json(409, {"error": "no simulator is running"})
            else:
                self._send_json(200, self._mode_body())
        else:
            self._send_json(404, {"error": f"no such path: {path}"})

    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path != "/sim/mode":
            self._send_json(404, {"error": f"no such path: {path}"})
            return
        if self.server.simulator is None:
            self._send_json(409, {"error": "simulator modes are unavailable with a hardware backend"})
            return
        body = self._read_json_body()
        if body is None:
            return
        mode = body.get("mode")
        sensor = body.get("sensor")
        if not isinstance(mode, str) or (sensor is not None and not isinstance(sensor, str)):
            self._send_json(400, {"error": "send {\"mode\": \"<name>\"}, and optionally \"sensor\"",
                                  "modes": list(MODES)})
            return
        try:
            self.server.set_mode(mode, sensor)
        except ValueError as problem:
            self._send_json(400, {"error": str(problem), "modes": list(MODES)})
            return
        self.log_message("simulator mode is now %s", mode)
        self._send_json(200, self._mode_body())

    # ---- simulator misbehaviour -----------------------------------------

    def _misbehave(self) -> bool:
        """Act out silent or garbage mode. True when the request was handled."""
        mode = self.server.current_mode()
        if mode == "silent":
            # Say nothing. Hold the connection until the client gives up, the
            # mode changes, or the server stops. Then close with no reply.
            self.server.release_held.wait(SILENT_HOLD_SECONDS)
            self.close_connection = True
            return True
        if mode == "garbage":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(GARBAGE_BODY)))
            self.end_headers()
            self.wfile.write(GARBAGE_BODY)
            return True
        return False

    # ---- helpers ---------------------------------------------------------

    def _mode_body(self) -> dict:
        simulator = self.server.simulator
        assert simulator is not None
        mode = simulator.mode
        body = {"mode": mode, "meaning": MODE_MEANING[mode]}
        if mode == "drop-sensor":
            body["sensor"] = simulator.drop_sensor
        return body

    def _read_json_body(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = -1
        if length < 0:
            self._send_json(400, {"error": "Content-Length is not a number"})
            return None
        if length > MAX_BODY_BYTES:
            self._send_json(413, {"error": f"body larger than {MAX_BODY_BYTES} bytes"})
            return None
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(400, {"error": "body is not valid JSON"})
            return None
        if not isinstance(body, dict):
            self._send_json(400, {"error": "body must be a JSON object"})
            return None
        return body

    def _send_json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        if not getattr(self.server, "quiet", False):
            super().log_message(format, *args)


# ---- starting and stopping ----------------------------------------------

def port_in_use(host: str, port: int) -> bool:
    """True when something already accepts connections on host:port."""
    probe_host = "127.0.0.1" if host in ("0.0.0.0", "") else host
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        return probe.connect_ex((probe_host, port)) == 0


def create_server(host: str, port: int, sampler: Sampler, quiet: bool = False) -> SensorServer:
    """Build the server, refusing a busy port. Does not start sampling or serving."""
    if not PORT_MIN <= port <= PORT_MAX:
        raise ValueError(f"port must be between {PORT_MIN} and {PORT_MAX}")
    if port_in_use(host, port):
        raise OSError(f"port {port} is already in use on {host}; choose another or stop that program")
    server = SensorServer((host, port), sampler)
    server.quiet = quiet
    return server


class RunningService:
    """A service running on background threads. Used by tests and by main()."""

    def __init__(self, host: str, port: int, backend: SensorBackend,
                 interval: float = 1.0, quiet: bool = False) -> None:
        self.sampler = Sampler(backend, interval)
        self.server = create_server(host, port, self.sampler, quiet)
        self._thread = threading.Thread(target=self.server.serve_forever,
                                        name="http", daemon=True)

    def start(self) -> "RunningService":
        self.sampler.start()
        self._thread.start()
        return self

    def stop(self) -> None:
        self.server.release_held.set()
        self.server.shutdown()
        self.server.server_close()
        self.sampler.stop()
        self._thread.join(timeout=5)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Line 3 sensor service (composite setting). Serves GET /api/readings.")
    parser.add_argument("--port", type=int, required=True,
                        help="port to listen on. Required. The lab uses 8700.")
    parser.add_argument("--host", default="127.0.0.1",
                        help="address to listen on (default 127.0.0.1, this machine only)")
    parser.add_argument("--backend", choices=("sim", "hardware"), default="sim",
                        help="sim (default) or hardware (lab Pi only)")
    parser.add_argument("--mode", choices=MODES, default="normal",
                        help="simulator mode to start in (default normal)")
    parser.add_argument("--drop-sensor", default=None,
                        help="which sensor drop-sensor mode fails (default press-vibration)")
    parser.add_argument("--interval", type=float, default=1.0,
                        help="seconds between samples (default 1.0)")
    parser.add_argument("--seed", type=int, default=3,
                        help="random seed for the simulator's noise (default 3)")
    parser.add_argument("--w1-device", default=None,
                        help="hardware only: the DS18B20 folder, if not the first one found")
    parser.add_argument("--quiet", action="store_true", help="do not log each request")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.backend == "hardware":
        if args.mode != "normal" or args.drop_sensor:
            print("Simulator modes do not apply to a hardware backend.", file=sys.stderr)
            return 2
        from hardware import line3_bench_backend
        try:
            backend: SensorBackend = line3_bench_backend(args.w1_device)
        except RuntimeError as problem:
            print(problem, file=sys.stderr)
            return 2
    else:
        try:
            backend = SimulatedBackend(args.mode, args.seed,
                                       args.drop_sensor or "press-vibration")
        except ValueError as problem:
            print(problem, file=sys.stderr)
            return 2

    try:
        service = RunningService(args.host, args.port, backend, args.interval, args.quiet)
    except (OSError, ValueError) as problem:
        print(f"Cannot start: {problem}", file=sys.stderr)
        return 2

    stopping = threading.Event()
    signal.signal(signal.SIGINT, lambda *_: stopping.set())
    for name in ("SIGTERM", "SIGBREAK"):   # SIGBREAK is Ctrl+Break on Windows
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), lambda *_: stopping.set())

    service.start()
    print(f"Line 3 sensor service on http://{args.host}:{args.port}", flush=True)
    print(f"Backend: {backend.describe()}", flush=True)
    print("GET /api/readings, GET /health. Press Ctrl+C to stop.", flush=True)
    try:
        while not stopping.wait(0.5):
            pass
    finally:
        service.stop()
        print("Stopped.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
