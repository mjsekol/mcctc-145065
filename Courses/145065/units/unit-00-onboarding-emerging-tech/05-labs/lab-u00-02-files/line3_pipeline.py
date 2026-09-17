# line3_pipeline.py
# A simulated IoT pipeline for Line 3 at Riverside Fabrication, a composite
# shop invented for this course. It carries three sensor readings through four
# layers and lands them in the maintenance log the shop already uses.
# STARTER FILE. It runs, and it writes nothing useful yet.
#
#     python line3_pipeline.py
#
# Layers, in the order data moves:
#   1. DEVICE       reads the sensors               (on the Raspberry Pi)
#   2. GATEWAY      packages readings as JSON       (on the Pi)
#   3. TRANSPORT    carries the JSON                (the network, simulated here)
#   4. INTEGRATION  turns JSON into log rows        (YOU WRITE THIS)
# and then the EXISTING SYSTEM, a CSV file the supervisor already opens in a
# spreadsheet. The new technology has to fit the old system, not the reverse.

import csv
import json
import sys
from pathlib import Path

LOG_FILE = Path(__file__).parent / "maintenance_log.csv"
LOG_COLUMNS = ["logged_at", "equipment", "measurement", "value", "unit", "status"]

# Invented sample data. Three moments, five seconds apart.
# None means the sensor did not answer.
TICKS = [
    {"sequence": 1041, "sampled_at": "2027-01-11T14:03:17Z",
     "values": {"oven-temp": 208.9, "press-vibration": 2.8, "coolant-level": 68.5}},
    {"sequence": 1042, "sampled_at": "2027-01-11T14:03:22Z",
     "values": {"oven-temp": 212.4, "press-vibration": 3.1, "coolant-level": 68.0}},
    {"sequence": 1043, "sampled_at": "2027-01-11T14:03:27Z",
     "values": {"oven-temp": 221.5, "press-vibration": 7.4, "coolant-level": None}},
]

# (sensor id, kind, unit the sensor reports in)
SENSORS = [
    ("oven-temp", "temperature", "C"),
    ("press-vibration", "vibration", "mm/s"),
    ("coolant-level", "level", "%"),
]

# The existing log names equipment the way the people on the floor do.
EQUIPMENT_NAMES = {
    "oven-temp": "Paint cure oven",
    "press-vibration": "Press 2",
    "coolant-level": "Coolant tank",
}

# The existing log's limits, in the existing log's units. Temperature is in
# Fahrenheit because the shop's paper log always was. A limit only means
# something in the unit it was written in.
CHECK_ABOVE = {"temperature": 425.0, "vibration": 7.0}


# ---------- 1. DEVICE layer ----------

def read_sensors(tick):
    readings = []
    for sensor_id, kind, unit in SENSORS:
        value = tick["values"][sensor_id]
        readings.append({"id": sensor_id, "kind": kind, "value": value,
                         "unit": unit, "ok": value is not None})
    return readings


# ---------- 2. GATEWAY layer ----------

def package(sequence, sampled_at, readings):
    # This is the same shape the Line 3 sensor service uses all semester.
    payload = {"device": "line3-pi", "sequence": sequence,
               "sampled_at": sampled_at, "sensors": readings}
    return json.dumps(payload)


# ---------- 3. TRANSPORT layer ----------

def send(json_text):
    # On the real line this is an HTTP request across the shop network.
    # Here it hands the text straight through, which is enough to show that
    # the only thing crossing the boundary is text.
    return json_text


# ---------- 4. INTEGRATION layer: YOU WRITE THIS ----------

def celsius_to_fahrenheit(celsius):
    # TODO 1: return the temperature in Fahrenheit.
    return celsius


def to_log_rows(json_text):
    # TODO 2: turn one payload of JSON text into a list of rows for the
    # existing log. One row per sensor, in LOG_COLUMNS order:
    #     [logged_at, equipment, measurement, value, unit, status]
    # The lab steps tell you what each column must hold.
    rows = []
    return rows


# ---------- EXISTING SYSTEM ----------

def append_rows(csv_path, rows):
    new_file = not csv_path.exists()
    # newline="" is what the csv module asks for, so Windows does not get a
    # blank line between rows.
    with open(csv_path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(LOG_COLUMNS)
        writer.writerows(rows)
    return len(rows)


def main():
    all_rows = []
    for tick in TICKS:
        readings = read_sensors(tick)
        text = package(tick["sequence"], tick["sampled_at"], readings)
        received = send(text)
        rows = to_log_rows(received)
        print(f"sequence {tick['sequence']}: DEVICE {len(readings)} readings | "
              f"GATEWAY {len(text)} characters | INTEGRATION {len(rows)} rows")
        all_rows.extend(rows)

    print()
    print("Last payload as it crossed the network:")
    print(json.dumps(json.loads(received), indent=2))
    print()
    written = append_rows(LOG_FILE, all_rows)
    print(f"Wrote {written} rows to {LOG_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
