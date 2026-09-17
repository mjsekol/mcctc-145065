# Run-book · The disconnect demo

The HMI PANEL project asks you to demonstrate fail-safe behavior by disconnecting the sensor while the
panel runs. This run-book walks the demo on the simulator first, where every failure is on a switch,
then on the lab Pi. Adapted for Unit 8 from the course's instructor run-book. Riverside Fabrication and
its Line 3 are a composite.

**What you are proving:** when data stops, the panel never shows an old number as live, never clears an
alarm, and says plainly what it cannot see.

---

## 0. Safety brief · read it aloud before any hardware step

- **ESD strap on**, clipped to the mat, before you touch the Pi or the probe.
- **Power the Pi off** before you connect or disconnect any wire on its pins.
- **No mains voltage, ever.** The Pi's power supply plugs into the wall; nothing else does.
- **Your signed Lab Acceptable Use and Safety Agreement is on file.**
- **Your instructor is present** for every hardware step.
- **The panel monitors. It never switches equipment on or off.** Nothing in this demo controls a machine.

Sections 1 to 4 touch no hardware.

---

## 1. Start the simulator

Open a terminal in your `sensor-service/` folder. Check the port is free (no output means free), then
start the service:

```
netstat -ano | findstr :8700
python sensor_service.py --port 8700
```

You should see:

```
Line 3 sensor service on http://127.0.0.1:8700
Backend: simulator, mode normal (all three sensors answer with values inside their thresholds)
GET /api/readings, GET /health. Press Ctrl+C to stop.
```

| You see | Cause | Fix |
|---|---|---|
| `error: the following arguments are required: --port` | there is no default port, on purpose | add `--port 8700` |
| `Cannot start: port 8700 is already in use on 127.0.0.1; choose another or stop that program` | another service still holds the port | stop it, or use 8701 and start the panel with `--url http://127.0.0.1:8701` |

Open a **second** terminal in the same folder. This is the control terminal.

```
python sim_control.py --port 8700 read
```

It prints `200` and one reply in the contract's shape.

## 2. Start the panel

Open a **third** terminal in your `HmiPanel/` folder:

```
dotnet run --project Line3.Hmi.Panel --artifacts-path C:\build\hmi
```

Within about a second: **CONNECTED**, and every tile NORMAL. If a box titled "The Line 3 panel cannot
start" appears, read its sentence: it names the problem, for example a thresholds reason that is too
short.

## 3. The demo, step by step (simulator)

Run each command in the control terminal. Wait for what the panel should show before the next step.
Write what you actually see in `docs/DEMO_RECORD.md`.

| Step | Command | Wait | The panel should show | Proves |
|---|---|---|---|---|
| 1. Drift into alarm | `python sim_control.py --port 8700 mode drift` | about 10 s, depending on your high limit | The oven tile in its alarm style, **ALARM HIGH**, a live value above your limit, the **UNACKNOWLEDGED ALARM** banner, and the acknowledge button. | alarms on a live value |
| 2. Ask, then cancel | press **ACKNOWLEDGE ALARM**, then **CANCEL** | | The confirmation covers the panel, then closes. The banner is unchanged. | REQ: confirmation, cancel changes nothing |
| 3. Freeze | `python sim_control.py --port 8700 mode freeze` | about 6 s | **DATA NOT UPDATING**, every tile **STALE** with **NOT LIVE** as the big value, a "Last value ..., N s old. Not live." box, and the oven banner **still up**. | stale is never shown as live; alarms survive stale |
| 4. Drop one sensor | `python sim_control.py --port 8700 mode drop-sensor --sensor coolant-level` | about 2 s | **CONNECTED** again. Coolant **NO DATA**, no number. The oven cools 3 C per sample in this mode, so its banner soon reads **ALARM ENDED, NOT ACKNOWLEDGED**. | one missing sensor, the rest live |
| 5. Garbage | `python sim_control.py --port 8700 mode garbage` | about 2 s | **NO CONNECTION**, every tile **NO DATA**, no numbers, and the oven banner unchanged. | an unreadable reply is missing data |
| 6. Silent | `python sim_control.py --port 8700 mode silent` | about 3 s | **NO CONNECTION**, every tile **NO DATA**. Drag the window: it still responds. | a silent Pi never freezes the window |
| 7. Recover | `python sim_control.py --port 8700 mode normal` | about 2 s | **CONNECTED**. The oven NORMAL, its banner still waiting for an acknowledgement. | recovery does not erase history |
| 8. The disconnect, in alarm | run step 1 again, wait for the alarm, then press **Ctrl+C** in the service terminal | about 2 s | The service prints `Stopped.` The panel shows **NO CONNECTION**, no numbers, and the oven's **alarm banner still up**. | **alarms survive a disconnect** |
| 9. Restart and clear | `python sensor_service.py --port 8700`, wait for NORMAL, then **ACKNOWLEDGE ALARM** and **YES** | about 2 s, then the oven must cool | **CONNECTED**. The sequence number starts over, and the panel accepts it. Once the oven is back inside limits and you confirm, the banner clears. | a restart is new data; clearing needs a person and a live value |

**Step 8 is the strongest step.** It is the one the whole demo exists for.

`POST /sim/mode` still answers in silent mode, on purpose, so you can always bring the simulator back.

## 4. Things that look wrong and are not

| You see | Why |
|---|---|
| After Ctrl+C the badge detail says "no answer in time", not "no connection" | On the course's build PC, Windows took about 2 s to refuse a connection to a closed port. The panel gives up at 1.5 s, so it reports a timeout. Both are NO DATA. |
| "taken 1.5 s ago" when the Pi samples every second | The service stamps whole seconds, so ages can read up to about a second high. |
| **ALARM ENDED, NOT ACKNOWLEDGED** on a normal tile | The alarm happened and nobody acknowledged it. That is correct. |
| After step 9 the sequence number is small again | The service restarted. Any change in sequence is new data. |

## 5. The demo on the lab Pi [VERIFY every step on the hardware, with your instructor present]

1. **Power off.** Wire the DS18B20 to the Pi as the lab's wiring sheet shows, with its pull-up resistor.
   [VERIFY] the pins and the resistor against the sheet and the part's datasheet.
2. **Power on.** Confirm 1-Wire is enabled and the probe appears:

   ```
   ls /sys/bus/w1/devices/
   cat /sys/bus/w1/devices/28-*/w1_slave
   ```

3. **Start the service on the Pi**, on the address your instructor gives you (never an address outside
   the lab network):

   ```
   python3 sensor_service.py --port 8700 --backend hardware --host <pi address>
   ```

4. **Start the panel on the lab PC** with the bench limits:

   ```
   dotnet run --project Line3.Hmi.Panel --artifacts-path C:\build\hmi -- --config thresholds.bench.json --url http://<pi address>:8700
   ```

   Expect the probe tile live near room temperature and the two unwired tiles **NO DATA**. That is
   correct: those sensors are not there.
5. **Make a real alarm.** Hold the probe or dip it in warm tap water until it passes the bench high limit.
   Do not acknowledge yet.
6. **Disconnect.** Pull the Ethernet cable between the Pi and the lab switch. The panel should show
   **NO CONNECTION**, no numbers, and the alarm banner still up. Write down how long it took.
7. **Reconnect.** Plug the cable back in. **CONNECTED** returns. The alarm stays until the probe cools
   below the limit and you acknowledge it.
8. **The sensor itself.** With the Pi **powered off**, unplug the probe. Power on and restart the service.
   The probe tile shows **NO DATA**. Whether a probe may be unplugged while powered is your instructor's
   call under the lab safety agreement; the default here is power off first.
9. **Stop everything.** Ctrl+C on the Pi. Close the panel. Power off the Pi before you unwire anything.

## 6. Afterward

- `netstat -ano | findstr :8700` prints nothing.
- Every step in `docs/DEMO_RECORD.md` names what you saw and the requirement it proves.
