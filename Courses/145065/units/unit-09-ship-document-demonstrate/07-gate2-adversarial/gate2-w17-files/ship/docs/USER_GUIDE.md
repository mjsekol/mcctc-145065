# LINE 3 SENSOR MONITOR · Operator User Guide

**Version 1.0.0**

Thank you for using the LINE 3 SENSOR MONITOR. This guide helps you get the most from your panel,
so you can keep Line 3 running smoothly and safely.

## What the panel does

The panel shows three live readings from Line 3: cure oven temperature, press vibration, and coolant
level. It warns you when a reading leaves its limits. It only watches. It never switches equipment on
or off.

Picture: [The panel with every sensor normal](screens/panel-normal.png)

## Reading the screen at a glance

Each tile's color tells you everything you need, so you can read the panel from across the bay:

- **Light tile:** NORMAL. Everything is fine.
- **Red tile:** ALARM HIGH or ALARM LOW. A reading is outside its limits.
- **Yellow tile:** STALE. The reading is old, and NOT LIVE replaces the large number.
- **Dark tile:** NO DATA. The panel has no reading.

Scan for color first. There is no need to read the words on the tiles.

## The top bar

| Badge | Meaning |
|---|---|
| CONNECTED | new readings are arriving |
| DATA NOT UPDATING | the sensor computer answers, but its readings stopped changing |
| NO CONNECTION | the sensor computer is not answering |
| WAITING | the panel has started and heard nothing yet |

Picture: [Data not updating](screens/panel-stale.png)

## When the connection is lost

If the panel loses its connection, each tile keeps showing the last reading it received, next to the
time it arrived, so you always have a number to work from. The badge changes to NO CONNECTION and the
tiles turn dark with the words NO DATA. Use the last reading until the connection returns.

Picture: [No connection](screens/panel-missing-connection.png)

## Handling alarms

*The following section is reproduced from the Northgate Controls ProView 8 Operator Handbook, Chapter 6.
Copyright Northgate Controls. All rights reserved.*

> **6.2 Alarm acknowledgement.** When an alarm annunciates on the faceplate, the operator shall first
> verify the process condition at the equipment. The operator shall then select ACKNOWLEDGE ALARM and
> confirm with YES, ACKNOWLEDGE. Selecting CANCEL returns to the faceplate without change. After
> acknowledgement the alarm indicator displays ACKNOWLEDGED, NOT CLEARED until the process value
> returns within limits. An alarm that is still active and has not been acknowledged displays
> UNACKNOWLEDGED ALARM. An alarm that returns to normal before acknowledgement displays
> ALARM ENDED, NOT ACKNOWLEDGED.

Picture: [Oven temperature in alarm](screens/panel-alarm.png)

Picture: [The confirmation box](screens/panel-alarm-confirm.png)

If you open the confirmation box by mistake, press CANCEL or the Esc key on the keyboard.

## Adjusting a limit

If an alarm keeps coming back and you have confirmed the machine is fine, tap the gear icon in the top
right corner to open LIMIT SETTINGS. Raise the limit by no more than five degrees and tap SAVE. The new
limit takes effect immediately and is recorded in the EVENTS list.

## How the panel works inside

For the technically curious: the PollingLoop sends an HTTP request to the Pi's API every 1000 ms.
Replies are JSON. If a value is null, or an exception is thrown while a reply is read, the ViewModel
marks the tile as missing. The panel talks to the sensor service at http://127.0.0.1:8700 unless the
csproj settings say otherwise.

## When to call someone

| You see | Call |
|---|---|
| NO CONNECTION for more than a minute | maintenance |
| DATA NOT UPDATING for more than a minute | maintenance |
| The same sensor showing NO DATA again and again | maintenance |
| An alarm you do not understand | your lead, before you acknowledge it |

The EVENTS list at the bottom of the screen shows the newest events with their times.
