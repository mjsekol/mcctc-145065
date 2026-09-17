# Thresholds · <your panel's name>

Every limit the panel alarms on, and why. The numbers live in `HmiPanel/Line3.Hmi.Panel/thresholds.json`.
These are decisions for an invented shop, not figures from a real process sheet.

**The rule on a limit:** a value exactly on a limit is <inside or outside>. Write it here and make your
tests agree.

---

## The oven

| Item | Your entry |
|---|---|
| Low limit | |
| High limit | |
| The problem each limit prevents | |
| The evidence (normal range, drift rate, the process range you were given) | |
| The reason, as it appears in `thresholds.json` | |
| The strongest case for a tighter limit | |
| The strongest case for a looser limit | |
| Which cost is worse on this line, and why | |
| Who agreed, and when (week and day) | |
| What new evidence would change this decision | |

## The press and the coolant

Say whether you kept the file's limits and reasons, and why. If you changed one, fill a table like the
oven's for it.

## The timing values

| Setting | Value | Why this value |
|---|---|---|
| `poll_interval_ms` | | |
| `request_timeout_ms` | | |
| `stale_after_seconds` | | |

## The meeting record

Who played the operator, who played the maintenance lead, the questions they asked, and the answers.
