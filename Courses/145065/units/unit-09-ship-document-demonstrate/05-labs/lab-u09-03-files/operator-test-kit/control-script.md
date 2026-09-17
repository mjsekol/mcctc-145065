# Control script · for the partner behind the divider

**You run the simulator. The person at the panel must never see you type.**
Riverside Fabrication and its Line 3 are a composite, an invented shop.

**No hardware.** Everything below runs on the lab PC. Using the lab Pi for an operator test is your
instructor's decision, under the Lab Acceptable Use and Safety Agreement, and never during a session.

---

## Before the first session

In the `sensor-service` folder, check the port is free, then start the simulator:

```
netstat -ano | findstr :8660
python sensor_service.py --port 8660
```

No output from the first command means the port is free. The second prints three lines. The first of
them is `Line 3 sensor service on http://127.0.0.1:8660`.

Open a **second** terminal in the same folder. Every command below goes there.

The facilitator starts the panel pointed at `http://127.0.0.1:8660` and confirms CONNECTED.

## The signal

Agree on one before the first session. A tap on the divider works. The facilitator taps once and says
the task number in a normal voice, as if reading the card.

## During a session

| Task | When | Command | Then |
|---|---|---|---|
| T1 | before the person sits down | `python sim_control.py --port 8660 mode normal` | nothing changes |
| T2 | on the facilitator's T2 signal | `python sim_control.py --port 8660 mode drift` | the oven alarms in about 10 seconds |
| T3 | on the T3 signal | `python sim_control.py --port 8660 mode freeze` | readings stop changing; STALE in about 6 seconds |
| T4 | on the T4 signal | `python sim_control.py --port 8660 mode drop-sensor --sensor coolant-level` | coolant goes dark in about 2 seconds |
| T5 | on the T5 signal | `python sim_control.py --port 8660 mode silent` | every tile goes dark in about 3 seconds |
| after | when the person has left | `python sim_control.py --port 8660 mode normal` | CONNECTED returns |

Every mode command prints a line that starts with `200`. If yours does not, tell the facilitator
quietly before the next task.

**Note for T3.** Freeze holds every reading at its value when you typed the command. If T2 left the oven
in alarm, T3 shows a STALE oven tile with the alarm banner still up. That is correct, and it is worth
watching how the person reads it.

**Note for T4.** Drop-sensor starts new readings again, and the oven cools quickly in this mode. If
nobody acknowledged the T2 alarm, the oven tile reads NORMAL with the banner ALARM ENDED, NOT
ACKNOWLEDGED within a few seconds, and that banner stays through T5. That is correct.

## After the last session

Press **Ctrl+C** in the first terminal. It prints `Stopped.` Then check the port is free:

```
netstat -ano | findstr :8660
```

No output means you are done.
