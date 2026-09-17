# Dataflow · <your panel's name>

Read this before you change anything. It shows what moves where, and where each failure is caught.

## 1. The whole path

Draw every layer as a box, from the sensor to the operator's eyes. Label every arrow with what crosses it.
Name the contract on the network arrow. **Every arrow points toward the operator.** Nothing flows back
toward a machine.

```
+------------------+
|  sensor          |
+--------+---------+
         |  <what crosses>
         v
   ... your boxes ...
         |
         v
   the operator's eyes
```

## 2. Inputs and outputs

Copy your tables from `REQUIREMENTS.md` section 4, or point to them.

## 3. Where each failure is caught

At least six rows.

| Failure | Caught in (layer and class) | Becomes | What the operator sees |
|---|---|---|---|
| the sensor fails to read | | | |
| the Pi's service is not running | | | |
| the Pi answers too slowly | | | |
| the Pi answers with something unreadable | | | |
| the Pi keeps sending the same sample | | | |
| the Pi's clock is wrong | | | |
| the panel's own loop stalls | | | |

## 4. Why the layers are separate

Two or three sentences: which layer owns time, which owns trust, which owns what may appear on screen.
