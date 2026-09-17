# Line 3 practice panel · User guide

Version 1.0.0. Riverside Fabrication and its Line 3 are a composite, an invented shop.

This screen only watches the line. It never starts, stops, or changes a machine.

## The top bar

| You see | It means | What you do |
|---|---|---|
| WAITING | the panel has started and has not heard anything yet | wait a few seconds |
| CONNECTED | new readings are arriving | nothing |
| DATA NOT UPDATING | the sensor computer answers, but its readings stopped changing | treat every number as old, and call maintenance if it lasts a minute |
| NO CONNECTION | the sensor computer is not answering | check the machines yourself, and call maintenance if it lasts a minute |

## Each tile

| You see | It means | What you do |
|---|---|---|
| NORMAL | a live reading inside its limits | nothing |
| ALARM HIGH | a live reading above its limit | look at the machine first, then acknowledge |
| ALARM LOW | a live reading below its limit | look at the machine first, then acknowledge |
| STALE | the newest reading is too old to trust | check the reading at the machine |
| NO DATA | the panel has no reading for this sensor | check the reading at the machine |

**A STALE number is not the current number.** The machine may be different now.
