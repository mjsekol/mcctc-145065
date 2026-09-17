# Fallback Hierarchy · The Riverside Tool Crib

**Use this only if your own Unit 2 hierarchy does not run and your instructor has approved the
switch.** Write the approval, and the reason, in your decision log.

Riverside Fabrication is a composite: an invented small metal fabrication shop. The badge ids are
invented and stand for no one.

## What it is

A Unit 2 style class hierarchy for the shop's tool crib, the room where tools are checked out.

```
CribItem (abstract)            level 1: anything with a crib tag
├── PoweredTool                level 2: runs, needs service, can be checked out
│   ├── Drill                  level 3: has a Battery (composition)
│   └── Grinder                level 3: has a guard
└── HandTool                   level 2: needs calibration

Battery                        not a CribItem: a drill HAS a battery
Kit                            a named group of items and smaller kits
```

The polymorphic method is `issues()`. `crib_report(things)` is the loop that calls it on everything.
`Kit.count_tools()` is recursive.

## Run it

Standard library only. From this folder:

```
python demo.py
python -m unittest -v
```

`python demo.py` prints:

```
CRIB-001 Cordless Drill (drill)
CRIB-002 Angle Grinder (grinder)
kit setup: 2 tools
Issues:
  CRIB-001 Cordless Drill: service due (52 h)
  CRIB-001 Cordless Drill: battery low (12%)
  CRIB-002 Angle Grinder: guard missing, do not issue
  CRIB-003 Torque Wrench: calibration expired
```

`python -m unittest` runs 10 tests, all passing. Checked on Python 3.13.7. The lab runs 3.14.

## Before you port it

Read the tests as carefully as the classes. One of them documents a place where the Python does not
do what its own comment says. Your comparison is stronger if you find places like that yourself and
prove each one with a build.
