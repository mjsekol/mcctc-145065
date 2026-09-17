"""readings.py . 145065 HMI anchor . Line 3 sensor service

The shape of one sample, and the only place that turns it into the JSON the
panel reads. If the contract changes, it changes here and in the panel's
ReadingParser.cs, and nowhere else.

The contract (fixed by the course build brief, section 8.3):

    GET /api/readings  ->  200
    {
      "device": "line3-pi",
      "sequence": 1042,
      "sampled_at": "2027-01-11T14:03:22Z",
      "sensors": [
        {"id": "oven-temp", "kind": "temperature", "value": 212.4, "unit": "C", "ok": true},
        ...
      ]
    }

sequence goes up by one for every new sample. sampled_at is when the sample
was taken, in UTC. A sensor that failed to read reports value null and
ok false. Nothing else is allowed to mean "no reading".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

DEVICE_NAME = "line3-pi"


@dataclass(frozen=True)
class SensorReading:
    """One sensor's value at one moment. value is None exactly when ok is False."""

    sensor_id: str
    kind: str
    unit: str
    value: float | None
    ok: bool

    def __post_init__(self) -> None:
        # The contract ties these two together. Enforce it here so no backend
        # can ever send "ok": true with no number, or a number marked failed.
        if self.ok and self.value is None:
            raise ValueError(f"{self.sensor_id}: ok is True but value is None")
        if not self.ok and self.value is not None:
            raise ValueError(f"{self.sensor_id}: ok is False but a value was given")

    @classmethod
    def failed(cls, sensor_id: str, kind: str, unit: str) -> "SensorReading":
        """A sensor that did not produce a reading this time."""
        return cls(sensor_id, kind, unit, None, False)

    def to_json_dict(self) -> dict:
        return {
            "id": self.sensor_id,
            "kind": self.kind,
            "value": None if self.value is None else round(self.value, 1),
            "unit": self.unit,
            "ok": self.ok,
        }


@dataclass(frozen=True)
class Sample:
    """Everything the Pi knew at one moment, stamped with a sequence number."""

    sequence: int
    sampled_at: datetime
    sensors: tuple[SensorReading, ...] = field(default_factory=tuple)
    device: str = DEVICE_NAME

    def to_json_dict(self) -> dict:
        return {
            "device": self.device,
            "sequence": self.sequence,
            "sampled_at": format_utc(self.sampled_at),
            "sensors": [reading.to_json_dict() for reading in self.sensors],
        }


def format_utc(moment: datetime) -> str:
    """ISO 8601 in UTC with a trailing Z and whole seconds, as the contract shows."""
    if moment.tzinfo is None:
        raise ValueError("sampled_at must be timezone-aware; a naive time is ambiguous")
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
