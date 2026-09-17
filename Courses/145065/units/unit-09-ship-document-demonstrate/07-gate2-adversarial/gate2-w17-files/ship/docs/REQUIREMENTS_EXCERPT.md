# Operator requirements · excerpt

These rows are copied unchanged from the Line 3 panel's operator requirements, which the panel was
built and tested against in Unit 8. Riverside Fabrication and its Line 3 are a composite, an invented
shop.

| ID | Requirement | Why | Checked by |
|---|---|---|---|
| REQ-01 | Show each sensor's state three ways: a word, a shape, and a color. | Color alone fails for color-blind operators and under colored shop light. | `docs/screens/*.png`; `PanelViewModelTests` state text checks; design review |
| REQ-02 | Never show a stale number as live. A stale value may appear only in a box labelled not live, with its age. | An operator who trusts an old number makes a decision on a machine that has moved on. | `StaleNeverShowsTheNumberAsTheValue`, `StaleBySequenceKeepsTheLastValueButNeverAsLive` |
| REQ-03 | Show no number at all for a missing value. | There is nothing to show. A guess is worse than a blank. | `MissingShowsNoNumberAnywhere`, `AFailedRequestIsMissingWithNoNumberAtAll` |
| REQ-04 | Never clear an alarm because data stopped. Only a live value back inside limits, plus an acknowledgement, clears it. | A pulled cable must not make an overheating oven look fine. | `FailSafeAnAlarmSurvivesStaleThenMissingThenRecovery`, `NoSequenceOfStaleOrMissingEverClearsAnAlarm`, `TheAlarmBannerStaysUpThroughADisconnect`, the live simulator test |
| REQ-07 | Require a confirmation before acknowledging an alarm. Cancel changes nothing. | A glove brushing the screen must not acknowledge anything. | `TheButtonOnlyOpensTheConfirmation`, `CancelChangesNothing` |
| REQ-08 | Say in words which sensors the panel cannot vouch for, and tell the operator to check them at the machine. | The fail-safe rule: tell the operator what the panel does not know. | `MissingShowsNoNumberAnywhere` (status line), `StartsWaitingWithNoNumbers` |
| REQ-10 | Touch targets at least 72 px tall at the 1280 by 800 design size; the two confirmation buttons at least 80 px apart. | Gloved fingers are wide and imprecise. | `PanelView.xaml` review; `docs/screens/panel-alarm-confirm.png`; **a person with gloves on the lab screen [VERIFY]** |
| REQ-12 | Monitoring only. The panel sends no request except `GET /api/readings`. | Software on this panel must never switch equipment. | Code review of `SensorClient`; it has one request, a GET |
| REQ-13 | Load every limit from `thresholds.json`, each with a written reason. Refuse to start on a limit with no reason, or on a broken file. | A number nobody can defend should not be on an operator's screen. | `RefusesALimitWithNoReason`, `RefusesAFileItCannotTrust` |

## The limits, from `thresholds.json`

| Sensor | Low | High | Where the limit comes from |
|---|---|---|---|
| Cure oven temperature | 190.0 C | 230.0 C | the thresholds file, with a written reason. The panel refuses to start with a limit that has no reason. |
| Press vibration | none | 6.0 mm/s | the same file |
| Coolant level | 25 % | none | the same file |

The panel reads the limits file when it starts. It has no screen for changing limits.
