# shift_counters.py
# Lab U01-04, Part 1: the scope hunt. STARTER.
#
# Line 3 counts press starts and strokes for each shift. The program runs
# and prints a report. The report is wrong in three places, and nothing
# crashes. Every one of the three problems is a name living at the wrong
# scope level. Find them, fix them, and map every name in the file.
#
# Riverside Fabrication is a composite shop. Everything here is invented.
#
#     python shift_counters.py
#     python selfcheck_scope.py

SHIFT_NAMES = ("First shift", "Second shift")
current_shift = SHIFT_NAMES[0]


class Press:
    """One press, with a stroke count for the current shift."""

    line_name = "Line 3"
    starts_this_shift = 0     # one count for ALL presses on the line

    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self.strokes = 0

    def start(self):
        # Count this start in the line-wide total.
        self.starts_this_shift += 1

    def run(self, minutes, strokes_per_minute):
        strokes = minutes * strokes_per_minute
        self.strokes += strokes
        return strokes

    def reset_for_new_shift(self):
        # A new shift starts every press at zero strokes.
        strokes = 0


def change_shift(presses):
    """Move the whole line to the second shift and zero every counter."""
    current_shift = SHIFT_NAMES[1]
    Press.starts_this_shift = 0
    for press in presses:
        press.reset_for_new_shift()


def summary(presses):
    lines = [f"{current_shift} on {Press.line_name}: {Press.starts_this_shift} starts"]
    for press in presses:
        lines.append(f"  {press.asset_tag}: {press.strokes} strokes")
    return "\n".join(lines)


def main():
    presses = [Press("L3-PRS-01"), Press("L3-PRS-02")]
    for press in presses:
        press.start()
    presses[0].run(30, 12)
    presses[1].run(45, 10)
    presses[0].start()          # Press 1 jammed and was restarted
    print(summary(presses))

    change_shift(presses)
    print(summary(presses))


if __name__ == "__main__":
    main()
