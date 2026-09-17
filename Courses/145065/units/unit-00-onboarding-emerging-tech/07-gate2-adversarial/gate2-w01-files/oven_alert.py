# oven_alert.py
# Copyright (c) 2023 Hollowbrook Sensor Works. All rights reserved.
# Licensed only for use with Hollowbrook sensor hardware. Do not redistribute.
#
# Adapted integration example: reads the latest Line 3 payload and alerts
# when the paint cure oven goes over the shop's temperature limit.

import json

# The shop's written limit for the paint cure oven, in Fahrenheit.
OVEN_LIMIT_F = 425.0

# The latest payload from the Line 3 gateway.
LATEST_PAYLOAD = """
{
  "device": "line3-pi",
  "sequence": 1043,
  "sampled_at": "2027-01-11T14:03:27Z",
  "sensors": [
    {"id": "oven-temp", "kind": "temperature", "value": 221.5, "unit": "C", "ok": true},
    {"id": "press-vibration", "kind": "vibration", "value": 7.4, "unit": "mm/s", "ok": true},
    {"id": "coolant-level", "kind": "level", "value": null, "unit": "%", "ok": false}
  ]
}
"""


def oven_status(payload_text):
    """Return a one-line status for the paint cure oven."""
    payload = json.loads(payload_text)
    for sensor in payload["sensors"]:
        if sensor["id"] != "oven-temp":
            continue
        if not sensor["ok"]:
            return "Oven reading missing. Check the sensor."
        # The gateway converts every reading to Fahrenheit before sending,
        # so the value can be compared with the limit directly.
        if sensor["value"] > OVEN_LIMIT_F:
            return f"ALERT: paint cure oven at {sensor['value']} F, over the {OVEN_LIMIT_F} F limit"
        return f"Oven normal at {sensor['value']} F"
    return "Oven sensor not found in payload."


if __name__ == "__main__":
    print(oven_status(LATEST_PAYLOAD))
