# selfcheck_pipeline.py
# Tries your integration layer against the three sample moments and checks
# every row against what the existing maintenance log expects.
#
# Put this file next to line3_pipeline.py and run:
#     python selfcheck_pipeline.py
#
# It never writes to maintenance_log.csv.

import line3_pipeline as pipeline

EXPECTED = {
    1041: [
        ["2027-01-11 14:03:17", "Paint cure oven", "temperature", 408.0, "F", "OK"],
        ["2027-01-11 14:03:17", "Press 2", "vibration", 2.8, "mm/s", "OK"],
        ["2027-01-11 14:03:17", "Coolant tank", "level", 68.5, "%", "OK"],
    ],
    1042: [
        ["2027-01-11 14:03:22", "Paint cure oven", "temperature", 414.3, "F", "OK"],
        ["2027-01-11 14:03:22", "Press 2", "vibration", 3.1, "mm/s", "OK"],
        ["2027-01-11 14:03:22", "Coolant tank", "level", 68.0, "%", "OK"],
    ],
    1043: [
        ["2027-01-11 14:03:27", "Paint cure oven", "temperature", 430.7, "F", "CHECK"],
        ["2027-01-11 14:03:27", "Press 2", "vibration", 7.4, "mm/s", "CHECK"],
        ["2027-01-11 14:03:27", "Coolant tank", "level", "", "%", "NO READING"],
    ],
}

COLUMN_NAMES = ["logged_at", "equipment", "measurement", "value", "unit", "status"]

passed = 0
total = 0

total += 1
if pipeline.celsius_to_fahrenheit(100) == 212 and pipeline.celsius_to_fahrenheit(0) == 32:
    print("PASS  celsius_to_fahrenheit: 100 C is 212 F and 0 C is 32 F")
    passed += 1
else:
    print("FAIL  celsius_to_fahrenheit: 100 C should be 212 F and 0 C should be 32 F, got",
          pipeline.celsius_to_fahrenheit(100), "and", pipeline.celsius_to_fahrenheit(0))

for tick in pipeline.TICKS:
    sequence = tick["sequence"]
    text = pipeline.package(sequence, tick["sampled_at"], pipeline.read_sensors(tick))
    rows = pipeline.to_log_rows(text)
    wanted = EXPECTED[sequence]
    total += 1
    if len(rows) != len(wanted):
        print(f"FAIL  sequence {sequence}: expected {len(wanted)} rows, got {len(rows)}")
        continue
    problems = []
    for row_number, (got, want) in enumerate(zip(rows, wanted), 1):
        if len(got) != len(want):
            problems.append(f"row {row_number} has {len(got)} columns, needs {len(want)}")
            continue
        for column, (g, w) in enumerate(zip(got, want)):
            if g != w:
                problems.append(f"row {row_number} {COLUMN_NAMES[column]}: got {g!r}, want {w!r}")
    if problems:
        print(f"FAIL  sequence {sequence}: " + "; ".join(problems))
    else:
        print(f"PASS  sequence {sequence}: all {len(wanted)} rows match the log format")
        passed += 1

print(f"\n{passed} of {total} self-checks passed")
