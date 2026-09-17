# Release plan · Line 3 Sensor Monitor 1.1.0

Prepared for the Line 3 panel team after the Week 18 operator test.

## Summary

Version 1.1.0 of the Line 3 Sensor Monitor responds to what operators told us in the operator test. It
clarifies what a NO DATA tile means, adds an alarm tone, and strengthens the tests. It installs safely
over 1.0.0 with the new install gate.

## Version decision

This release is **1.1.0 (MINOR)**, because operators will see new words on the screen. A MINOR number
tells everyone that something visible changed while everything that worked before still works.

## What changed for operators

- Changed three explanation strings in `PanelMonitor` (`MissingStatus` and `Evaluate`).
- Added `ReleaseTests`, six new xunit tests with a shared `NotStopped` constant.
- The snapshot harness now renders `panel-missing-unreadable.png` as a worst-case layout check.
- Added a limits table to `docs/USER_GUIDE.md`.

## Added

- **Alarm tone.** An audible tone now sounds on the panel PC when any sensor enters ALARM HIGH or
  ALARM LOW, as operators requested in session O4. The tone repeats every ten seconds until the alarm
  is acknowledged.

## Change impact

*Change impact analysis prepared by the Line 2 Wash Monitor team.*

| Area | Impact |
|---|---|
| Wash tank temperature tile (`wash-temp`) | none; its limits are unchanged |
| Rinse conductivity tile (`rinse-cond`) | none |
| Shared thresholds file | Team Wash's panel reads the same file, so no edit is needed |
| Operators on the wash line | retrained at the Line 2 stand-up |
| Version | patch |

## Install gate

The install step runs `ReleaseGate` before copying anything, so an older build can never overwrite a
newer one. `ReleaseCheck.IsUpgrade` has been verified for every version this panel will ever ship, as
the table below shows.

| Installed | Candidate | Decision |
|---|---|---|
| 1.0.0 | 1.0.1 | INSTALL |
| 1.0.1 | 1.1.0 | INSTALL |
| 1.0.0 | 1.1.0 | INSTALL |
| 1.1.0 | 1.0.1 | KEEP INSTALLED |

The code is in `ReleaseGate/`.

## Rollout

Copy 1.1.0 onto the panel PC at shift change. Operators adapt quickly to small wording changes, so
there is no need to tell them, update the training card, or involve the shift lead. The fewer people
involved in a release, the faster it goes.

## Rollback

Keep the 1.0.0 folder on the panel PC. If 1.1.0 misbehaves, start 1.0.0 from its folder and check that
the header reads Version 1.0.0.
