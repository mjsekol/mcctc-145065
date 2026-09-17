# Line 3 sensor service

The program on the Line 3 Raspberry Pi, and the simulator you run on a lab PC. Python 3 standard library only: nothing to install. Riverside Fabrication and its Line 3 are a composite, not a real shop.

**Where this copy came from.** It is the course's Line 3 sensor service, copied for the Unit 9 operator test. One thing changed in the Python files: the example commands and the `--help` text name port 8700, the classroom port Unit 8 used, where the course's instructor copy says 8660. This README was changed too: this paragraph, the port under "Run it", and two lines about the test file, which is not in this copy because its tests read files that live beside the reference panel. Your own panel from Unit 8 is the other half.

## Run it

Use **port 8700**, as in Unit 8. Check it is free first; no output means it is free:

```
netstat -ano | findstr :8700
```

Then, from this folder:

```
python sensor_service.py --port 8700                       # simulator, normal
python sensor_service.py --port 8700 --mode drift          # start in any mode
python sensor_service.py --port 8700 --backend hardware    # lab Pi only [VERIFY]
python sim_control.py --port 8700 mode freeze              # switch mode while it runs
python sim_control.py --port 8700 read                     # one GET /api/readings
```

Stop the service with Ctrl+C (or Ctrl+Break on Windows).

## Files

| File | What it holds |
|---|---|
| `readings.py` | `SensorReading`, `Sample`, and the JSON shape. The contract lives here. |
| `backends.py` | `SensorBackend` (the interface), `SimulatedBackend` (six modes), `Sampler` (sequence and time) |
| `hardware.py` | `HardwareBackend` and a DS18B20 channel for the lab Pi. Every hardware fact is marked [VERIFY]. |
| `sensor_service.py` | the HTTP server and the command line |
| `sim_control.py` | switch modes and read replies from a second terminal |

## Modes

| Mode | What the panel should call it |
|---|---|
| `normal` | NORMAL |
| `drift` | ALARM on oven temperature within about 10 samples |
| `freeze` | STALE: answers keep coming, `sequence` and `sampled_at` stop |
| `drop-sensor` | MISSING for one sensor (`--drop-sensor` or `"sensor"` picks which) |
| `silent` | MISSING for all, by timeout. `POST /sim/mode` still answers. |
| `garbage` | MISSING for all, by a malformed reply |

**Security.** The service listens on 127.0.0.1 unless you pass `--host`. `POST /sim/mode` has no login. Never make the service reachable beyond the isolated lab network.
