"""backends.py . 145065 HMI anchor . Line 3 sensor service

Where readings come from. The HTTP server never talks to a sensor. It asks a
Sampler for the newest Sample, and the Sampler asks a SensorBackend.

    SensorBackend      the interface: one method, read()
    SimulatedBackend   the default. Runs anywhere. Has six modes.
    HardwareBackend    in hardware.py. Runs on the lab Pi only. [VERIFY]
    Sampler            owns the sequence number and the timestamp

Why the Sampler owns the sequence number: a backend only knows values. Whether
a sample is NEW is a fact about time, and one object should own it. When a
backend returns None from read(), it is saying "I have nothing new", and the
Sampler keeps the old sample, old sequence, old timestamp. That is exactly
what a hung sensor bus looks like from the outside, and it is what the panel
must learn to call STALE.

Setting: Riverside Fabrication, Line 3, is a composite. It is not a real shop.
"""

from __future__ import annotations

import random
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from readings import Sample, SensorReading

# The six simulator modes. The names are the contract with the run-book, the
# command line, POST /sim/mode, and the unit labs. Do not rename them.
MODES = ("normal", "drift", "freeze", "drop-sensor", "silent", "garbage")

# What each mode looks like from the panel's side.
MODE_MEANING = {
    "normal": "all three sensors answer with values inside their thresholds",
    "drift": "oven temperature climbs past its alarm threshold and keeps climbing",
    "freeze": "the service answers, but sequence and sampled_at stop advancing (STALE)",
    "drop-sensor": "one sensor reports value null and ok false (MISSING for that sensor)",
    "silent": "the service accepts connections and never answers (MISSING, by timeout)",
    "garbage": "the service answers 200 with malformed JSON (MISSING, by parse failure)",
}


@dataclass(frozen=True)
class SensorSpec:
    """A sensor the simulator pretends to have."""

    sensor_id: str
    kind: str
    unit: str
    base: float      # where the value sits in normal running
    noise: float     # the value wanders at most this far either side of base


# Line 3's three sensors. The bases sit well inside the thresholds in
# panel/Line3.Hmi.Panel/thresholds.json, and the noise can never carry a normal
# reading across a threshold. A simulator that raises false alarms in normal
# mode teaches operators to ignore alarms.
LINE3_SENSORS = (
    SensorSpec("oven-temp", "temperature", "C", base=212.0, noise=1.0),
    SensorSpec("press-vibration", "vibration", "mm/s", base=3.1, noise=0.3),
    SensorSpec("coolant-level", "level", "%", base=68.0, noise=0.4),
)

DRIFT_SENSOR = "oven-temp"
DRIFT_STEP = 2.0          # degrees C added per sample while drifting
DRIFT_CEILING = 290.0     # the simulated oven stops climbing here
RECOVERY_STEP = 3.0       # degrees C removed per sample on the way back to base
DEFAULT_DROP_SENSOR = "press-vibration"


class SensorBackend(ABC):
    """Anything that can produce one set of readings on request."""

    #: True only for the simulator. The server refuses POST /sim/mode otherwise.
    is_simulator: bool = False

    @abstractmethod
    def read(self) -> list[SensorReading] | None:
        """Take one reading of every sensor.

        Return a list with one SensorReading per sensor. A sensor that could not
        be read is SensorReading.failed(...), never left out and never a guess.
        Return None only when there is no new sample at all.
        Must not raise: a backend that raises would stop the sampler thread.
        """

    @abstractmethod
    def describe(self) -> str:
        """One line for the startup banner."""


class SimulatedBackend(SensorBackend):
    """Line 3's three sensors, invented, with modes that break on purpose."""

    is_simulator = True

    def __init__(self, mode: str = "normal", seed: int = 3,
                 drop_sensor: str = DEFAULT_DROP_SENSOR,
                 sensors: tuple[SensorSpec, ...] = LINE3_SENSORS) -> None:
        self._sensors = sensors
        self._rng = random.Random(seed)
        self._lock = threading.Lock()
        self._current = {spec.sensor_id: spec.base for spec in sensors}
        self._mode = "normal"
        self._drop_sensor = DEFAULT_DROP_SENSOR
        self._has_sampled = False
        self.set_mode(mode, drop_sensor)

    @property
    def mode(self) -> str:
        with self._lock:
            return self._mode

    @property
    def drop_sensor(self) -> str:
        with self._lock:
            return self._drop_sensor

    def sensor_ids(self) -> list[str]:
        return [spec.sensor_id for spec in self._sensors]

    def set_mode(self, mode: str, drop_sensor: str | None = None) -> None:
        """Switch mode. Raises ValueError for a mode or sensor that does not exist."""
        if mode not in MODES:
            raise ValueError(f"unknown mode {mode!r}; choose one of: {', '.join(MODES)}")
        if drop_sensor is not None and drop_sensor not in self.sensor_ids():
            raise ValueError(
                f"unknown sensor {drop_sensor!r}; choose one of: {', '.join(self.sensor_ids())}")
        with self._lock:
            self._mode = mode
            if drop_sensor is not None:
                self._drop_sensor = drop_sensor

    def read(self) -> list[SensorReading] | None:
        with self._lock:
            mode = self._mode
            drop = self._drop_sensor
            # A simulator started frozen still takes one sample first, so there
            # is something to be stale. After that, freeze means nothing new.
            if mode == "freeze" and self._has_sampled:
                return None
            self._has_sampled = True
            readings = []
            for spec in self._sensors:
                value = self._next_value(spec, drifting=(mode == "drift"))
                if mode == "drop-sensor" and spec.sensor_id == drop:
                    readings.append(SensorReading.failed(spec.sensor_id, spec.kind, spec.unit))
                else:
                    readings.append(
                        SensorReading(spec.sensor_id, spec.kind, spec.unit, value, True))
            return readings

    def _next_value(self, spec: SensorSpec, drifting: bool) -> float:
        # Caller holds the lock.
        held = self._current[spec.sensor_id]
        if drifting and spec.sensor_id == DRIFT_SENSOR:
            # Drift is a steady climb with no noise, so a test can predict
            # exactly which sample crosses the threshold.
            held = min(held + DRIFT_STEP, DRIFT_CEILING)
            self._current[spec.sensor_id] = held
            return held
        # Everything else heads back toward base, then wanders a little.
        if held > spec.base + spec.noise:
            held = max(held - RECOVERY_STEP, spec.base)
        elif held < spec.base - spec.noise:
            held = min(held + RECOVERY_STEP, spec.base)
        else:
            held = spec.base
        self._current[spec.sensor_id] = held
        if held != spec.base:
            return held
        return spec.base + self._rng.uniform(-spec.noise, spec.noise)

    def describe(self) -> str:
        return f"simulator, mode {self.mode} ({MODE_MEANING[self.mode]})"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Sampler:
    """Takes samples on a schedule and keeps the newest one.

    tick() is the whole job, and a test can call it by hand with a fake clock.
    start() runs tick() on a background thread every `interval` seconds, so a
    slow sensor never makes an HTTP request wait.
    """

    def __init__(self, backend: SensorBackend, interval: float = 1.0,
                 clock: Callable[[], datetime] = utc_now) -> None:
        if interval <= 0:
            raise ValueError("interval must be greater than zero")
        self.backend = backend
        self.interval = interval
        self._clock = clock
        self._lock = threading.Lock()
        self._latest: Sample | None = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def tick(self) -> Sample | None:
        """Ask the backend once. Returns the newest sample after asking."""
        try:
            readings = self.backend.read()
        except Exception:  # noqa: BLE001  a backend bug must not kill sampling
            readings = None
        with self._lock:
            if readings is not None:
                sequence = 1 if self._latest is None else self._latest.sequence + 1
                self._latest = Sample(sequence, self._clock(), tuple(readings))
            return self._latest

    def latest(self) -> Sample | None:
        with self._lock:
            return self._latest

    def start(self) -> None:
        self.tick()
        self._thread = threading.Thread(target=self._run, name="sampler", daemon=True)
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.wait(self.interval):
            self.tick()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
