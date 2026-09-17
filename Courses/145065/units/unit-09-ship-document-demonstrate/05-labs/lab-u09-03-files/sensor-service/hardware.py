"""hardware.py . 145065 HMI anchor . Line 3 sensor service

The real-sensor backend, written for the lab Raspberry Pi. [VERIFY] every
hardware fact in this file on the lab Pi before a class depends on it. There
is no Pi and no sensor on the machine this was written on. The parsing below
is tested against a fake folder that imitates the Pi's; the wiring, the
kernel driver, and the folder names are not tested here.

SAFETY. Power the Pi off before you wire anything. Wear the ESD strap. No
mains voltage, ever. This software MONITORS. Nothing in this file, or in the
panel, switches any equipment on or off.

One real sensor is implemented: a DS18B20 digital temperature sensor on the
Pi's 1-Wire bus, read through the Linux w1 driver's files. It needs no
library beyond Python's standard library, which is why it was chosen.

What to confirm on the lab Pi [VERIFY]:
  1. 1-Wire is enabled. On Raspberry Pi OS this is the w1-gpio overlay
     (raspi-config, Interface Options, 1-Wire, or a dtoverlay=w1-gpio line in
     the boot config file). The data pin is GPIO4 by default. The boot config
     file has moved between OS releases; check where yours is.
  2. The sensor appears as a folder named 28-<serial> under
     /sys/bus/w1/devices/, and that folder has a w1_slave file.
  3. w1_slave has two lines. The first ends in YES when the CRC check passed.
     The second ends in t=<millidegrees C>, for example t=23125 for 23.125 C.
  4. The DS18B20's rated range, and its power-on value, match the datasheet
     for your part. This file assumes -55 to +125 C and treats exactly 85.000 C
     as the power-on value, which is what many DS18B20 guides describe.

THE HONEST LIMIT. A DS18B20 cannot measure a cure oven. Its rated range tops
out far below the oven's working temperature. On the bench it stands in for
the oven probe: you warm it with your hand or a cup of warm water. That is why
the panel ships a second thresholds file, thresholds.bench.json, with limits a
bench sensor can actually cross. A real oven uses a thermocouple and an
amplifier board, which needs more than the standard library.

The other two Line 3 sensors are not wired in the lab kit. They report
value null and ok false on every sample, which the panel shows as MISSING.
That is the contract working as designed: no reading is never a guess.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path

from backends import SensorBackend
from readings import SensorReading

W1_DEVICES = Path("/sys/bus/w1/devices")   # [VERIFY] on the lab Pi
DS18B20_FAMILY_PREFIX = "28-"              # [VERIFY] DS18B20 family code
DS18B20_MIN_C = -55.0                      # [VERIFY] against the datasheet
DS18B20_MAX_C = 125.0                      # [VERIFY] against the datasheet
DS18B20_POWER_ON_C = 85.0                  # [VERIFY] against the datasheet


class Channel(ABC):
    """One physical sensor. read() returns a number, or None when it could not read."""

    def __init__(self, sensor_id: str, kind: str, unit: str) -> None:
        self.sensor_id = sensor_id
        self.kind = kind
        self.unit = unit

    @abstractmethod
    def read(self) -> float | None:
        """Never raises. A failed read is None."""

    def reading(self) -> SensorReading:
        value = self.read()
        if value is None:
            return SensorReading.failed(self.sensor_id, self.kind, self.unit)
        return SensorReading(self.sensor_id, self.kind, self.unit, value, True)


class Ds18b20Channel(Channel):
    """A DS18B20 read through the Linux w1 driver's w1_slave file."""

    def __init__(self, device_dir: Path, sensor_id: str = "oven-temp") -> None:
        super().__init__(sensor_id, "temperature", "C")
        self.device_dir = Path(device_dir)

    def read(self) -> float | None:
        try:
            text = (self.device_dir / "w1_slave").read_text(encoding="ascii")
        except OSError:
            # Unplugged, driver not loaded, or a bus error. All mean: no reading.
            return None
        return parse_w1_slave(text)


class UnwiredChannel(Channel):
    """A sensor Line 3 has but the lab kit does not. Always reports a failed read."""

    def read(self) -> float | None:
        return None


def parse_w1_slave(text: str) -> float | None:
    """Turn the two lines of a w1_slave file into degrees C, or None.

    Returns None, rather than a number, when:
      - the file does not have two lines
      - the CRC line does not end in YES
      - there is no t= field, or it is not an integer
      - the value is outside the rated range
      - the value is exactly the power-on value, which means the sensor
        answered before it finished its first conversion
    """
    lines = text.strip().splitlines()
    if len(lines) < 2:
        return None
    if not lines[0].strip().endswith("YES"):
        return None
    marker = lines[1].rfind("t=")
    if marker < 0:
        return None
    try:
        millidegrees = int(lines[1][marker + 2:].strip())
    except ValueError:
        return None
    celsius = millidegrees / 1000.0
    if celsius == DS18B20_POWER_ON_C:
        return None
    if not DS18B20_MIN_C <= celsius <= DS18B20_MAX_C:
        return None
    return celsius


def find_ds18b20(devices: Path = W1_DEVICES) -> Path | None:
    """The first DS18B20 folder under the w1 devices folder, or None."""
    try:
        names = sorted(os.listdir(devices))
    except OSError:
        return None
    for name in names:
        if name.startswith(DS18B20_FAMILY_PREFIX):
            return devices / name
    return None


class HardwareBackend(SensorBackend):
    """Reads real channels. Simulator modes do not exist here."""

    is_simulator = False

    def __init__(self, channels: list[Channel]) -> None:
        if not channels:
            raise ValueError("a hardware backend needs at least one channel")
        self.channels = channels

    def read(self) -> list[SensorReading] | None:
        # A real read always produces a sample, even when every channel failed.
        # Failed channels say so in their own reading. That keeps sequence
        # advancing, so the panel reports MISSING for the sensor, not STALE for
        # the whole device.
        return [channel.reading() for channel in self.channels]

    def describe(self) -> str:
        parts = []
        for channel in self.channels:
            if isinstance(channel, Ds18b20Channel):
                parts.append(f"{channel.sensor_id} from DS18B20 at {channel.device_dir}")
            else:
                parts.append(f"{channel.sensor_id} not wired")
        return "hardware: " + "; ".join(parts)


def line3_bench_backend(device_dir: Path | None = None) -> HardwareBackend:
    """The lab kit: one DS18B20 standing in for the oven, two unwired sensors."""
    if device_dir is not None and not Path(device_dir).is_dir():
        raise RuntimeError(f"No such sensor folder: {device_dir}")
    if device_dir is None:
        device_dir = find_ds18b20()
    if device_dir is None:
        raise RuntimeError(
            "No DS18B20 found under /sys/bus/w1/devices. Check that 1-Wire is enabled "
            "and the sensor is wired, then try again. Or run the simulator: --backend sim")
    return HardwareBackend([
        Ds18b20Channel(Path(device_dir), "oven-temp"),
        UnwiredChannel("press-vibration", "vibration", "mm/s"),
        UnwiredChannel("coolant-level", "level", "%"),
    ])
