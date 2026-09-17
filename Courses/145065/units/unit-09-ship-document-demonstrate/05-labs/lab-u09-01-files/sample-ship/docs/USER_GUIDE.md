# LINE 3 SENSOR MONITOR · User guide

Riverside Fabrication is a composite, an invented shop.

## What this screen is for

The panel shows three readings from Line 3. It only watches. It never starts or stops a machine.

Picture: [Every sensor normal](screens/panel-normal.png)

## Reading a tile

| You see | It means | What you do |
|---|---|---|
| NORMAL and a number | a live reading inside its limits | nothing |
| ALARM HIGH or ALARM LOW | a live reading outside its limits | check the machine, then acknowledge |
| STALE and NOT LIVE | the newest reading is too old to trust | check the reading at the machine |
| NO DATA | the panel has no reading at all | check the reading at the machine |

Picture: [A stale tile](screens/panel-stale.png)

## The top bar

CONNECTED means readings are arriving. NO CONNECTION means the sensor computer is not answering.
WAITING means the panel has started and heard nothing yet. If the Pi's JSON stops changing, the top bar turns yellow.

## When a sensor alarms

Picture: [Oven temperature in alarm](screens/panel-alarm.png)

1. Look at the machine first.
2. Press ACKNOWLEDGE ALARM on that tile.
3. Press YES, ACKNOWLEDGE, or CANCEL to go back.

The banner then reads ACKNOWLEDGED, NOT CLEARED until a live reading is back inside limits. If the
reading comes back first, the banner reads UNACKNOWLEDGED ALARM until someone acknowledges it.

The EVENTS list at the bottom shows what happened and when.
