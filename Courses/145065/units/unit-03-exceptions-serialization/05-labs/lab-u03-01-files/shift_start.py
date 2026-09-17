# shift_start.py
# Runs the start-of-shift plan for Line 3 at Riverside Fabrication, a
# composite shop invented for this course.
# STARTER FILE for Lab U03-01. It runs.
#
#     python shift_start.py
#
# Read run_plan() first. One except clause catches every failure the same
# way. Then read the report it prints, and look at step 7.

from plant import build_sample_line

# The plan a supervisor typed this morning. Invented. Step 6 has a letter O
# where a zero belongs.
PLAN = [
    "L3-PRS-01 start",
    "L3-PRS-02 start",
    "L3-CNV-01 start",
    "L3-OVN-01 setpoint 205",
    "L3-PRS-07 start",
    "L3-OVN-01 setpoint 2O5",
    "L3-OVN-01 start",
]


def parse_number(text, label):
    """Turn plan text into a number."""
    return float(text)


def run_step(line, step):
    parts = step.split()
    if len(parts) < 2:
        raise ValueError(f"cannot read plan step {step!r}")
    tag, action, *rest = parts
    item = line.get(tag)
    if action == "start":
        item.start()
    elif action == "setpoint" and len(rest) == 1:
        item.setpoint_c = parse_number(rest[0], "setpoint")
    else:
        raise ValueError(f"cannot read plan step {step!r}")


def run_plan(line, plan):
    """Run each step in order. Return the report, one line per step."""
    report = []
    for number, step in enumerate(plan, 1):
        try:
            run_step(line, step)
        except Exception:
            report.append(f"step {number} failed: something went wrong")
        else:
            report.append(f"step {number} done: {step}")
    return report


def main():
    line = build_sample_line()
    press2 = line.get("L3-PRS-02")
    press2.close_guard()
    press2.lock_out("tech-07")  # a technician is working inside Press 2
    for row in run_plan(line, PLAN):
        print(row)
    print()
    print(f"Oven setpoint is {line.get('L3-OVN-01').setpoint_c:g} C and the oven is "
          f"{'running' if line.get('L3-OVN-01').is_running else 'stopped'}")


if __name__ == "__main__":
    main()
