# Line 3 sensor service (lab copy)

This folder is the program that runs on the Line 3 Raspberry Pi, and the simulator you run on a lab PC
when no Pi is wired. Python 3 standard library only: nothing to install.

**Where it came from.** These five files are copied unchanged from the course's instructor HMI anchor,
`anchor-project/hmi/sensor-service/`. The anchor's test file is not copied, because it checks files
that are not in your lab folder. If your instructor updates the anchor, they replace this folder.

**Riverside Fabrication and its Line 3 are a composite**, an invented shop used all semester. It is not
a real company.

---

## Safety first

Running the simulator touches no hardware. The moment a lab asks you to wire the Pi or a sensor, read
the safety brief at the top of that lab aloud with your partner first: ESD strap on, power off before
you wire, no mains voltage ever, and your signed Lab Acceptable Use and Safety Agreement on file.

**The panel you build monitors. It never switches equipment on or off.** Nothing in this folder
controls a machine.

---

## Run it

Unit 8 labs use **port 8700** for your simulator. The service's `--help` text mentions 8660, which is
the port the course's instructor copy uses. Either works on your own PC; the labs say 8700.

Check the port is free first. No output means it is free:

```
netstat -ano | findstr :8700
```

Then, from this folder:

```
python sensor_service.py --port 8700                      # simulator, normal
python sensor_service.py --port 8700 --mode drift         # start in any mode
python sim_control.py --port 8700 mode                    # show the current mode
python sim_control.py --port 8700 mode freeze             # switch mode while it runs
python sim_control.py --port 8700 mode drop-sensor --sensor coolant-level
python sim_control.py --port 8700 read                    # one GET /api/readings
```

Stop the service with **Ctrl+C** (or Ctrl+Break on Windows). It prints `Stopped.`

On the lab Pi only, and only after the hardware lab's safety brief [VERIFY every step on the Pi]:

```
python3 sensor_service.py --port 8700 --backend hardware --host <pi address>
```

---

## Files

| File | What it holds |
|---|---|
| `readings.py` | `SensorReading`, `Sample`, and the JSON shape. The contract lives here. |
| `backends.py` | `SensorBackend` (the interface), `SimulatedBackend` (six modes), `Sampler` (sequence and time) |
| `hardware.py` | `HardwareBackend` and a DS18B20 channel for the lab Pi. Every hardware fact is marked [VERIFY]. |
| `sensor_service.py` | the HTTP server and the command line |
| `sim_control.py` | switch modes and read replies from a second terminal |

## The six simulator modes

| Mode | What the service does | What your panel must call it |
|---|---|---|
| `normal` | three sensors, values inside the Line 3 limits | NORMAL |
| `drift` | the oven climbs 2 C per sample from about 212 C | ALARM on the oven within about 10 samples |
| `freeze` | keeps answering, but `sequence` and `sampled_at` stop | STALE |
| `drop-sensor` | one sensor reports `"value": null, "ok": false` | MISSING for that sensor only |
| `silent` | accepts the connection and never answers | MISSING for all, by timeout |
| `garbage` | answers 200 with JSON cut off in the middle | MISSING for all, by an unreadable reply |

In `silent` mode, `POST /sim/mode` still answers, so `sim_control.py` can always bring the simulator
back.

## The contract, in one reply

```json
{
  "device": "line3-pi",
  "sequence": 1042,
  "sampled_at": "2027-01-11T14:03:22Z",
  "sensors": [
    {"id": "oven-temp", "kind": "temperature", "value": 212.4, "unit": "C", "ok": true},
    {"id": "press-vibration", "kind": "vibration", "value": 3.1, "unit": "mm/s", "ok": true},
    {"id": "coolant-level", "kind": "level", "value": 68.0, "unit": "%", "ok": true}
  ]
}
```

`sequence` goes up by one for every new sample. `sampled_at` is when the sample was taken, in UTC. A
sensor that failed to read reports `"value": null, "ok": false`. `GET /health` answers
`{"status": "ok"}`.

**Security.** The service listens on 127.0.0.1 unless you pass `--host`. `POST /sim/mode` has no
login. Never make the service reachable beyond the isolated lab network.

**Leftovers.** Running Python here can create a `__pycache__` folder. Set
`PYTHONDONTWRITEBYTECODE=1` before you run, or delete the folder before you commit.
