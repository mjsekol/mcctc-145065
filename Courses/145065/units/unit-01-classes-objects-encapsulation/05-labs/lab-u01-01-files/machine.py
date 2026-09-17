# machine.py
# Lab U01-01: Machine Rules. STARTER.
#
# One press on Line 3, as a class: the data, and the only operations allowed
# to change it, in one place. Riverside Fabrication is a composite shop.
#
# This file runs and does nothing useful yet. Every method below is a stub.
# The lab handout tells you what each one must do, one step at a time.
#
# The rule for this week: a name that starts with an underscore, such as
# self._running, is internal. Code outside this class never touches it.
# Week 3, Monday explains exactly what Python does and does not enforce.

MAX_RATED_KW = 500   # the largest motor on Line 3 is well under this


class Machine:
    """A powered machine on Line 3."""

    def __init__(self, asset_tag, name, rated_kw):
        # Part 1, steps 3 and 4: check every argument, then store it.
        # A Machine that exists must be a valid Machine.
        self.asset_tag = asset_tag
        self.name = name
        self.rated_kw = rated_kw
        self._running = False
        self._locked_by = None      # None means nobody holds a lockout
        self._run_minutes = 0

    # ----- Part 1: starting and stopping -----

    def start(self):
        pass

    def stop(self):
        pass

    def is_running(self):
        return False

    # ----- Part 2: lockout and run time -----

    def lock_out(self, badge):
        pass

    def release_lockout(self, badge):
        pass

    def is_locked_out(self):
        return False

    def locked_out_by(self):
        return None

    def record_run(self, minutes):
        pass

    def run_minutes(self):
        return 0

    def status_text(self):
        return ""

    # ----- Part 1, step 5 -----

    def __repr__(self):
        return object.__repr__(self)


if __name__ == "__main__":
    press = Machine("L3-PRS-01", "Press 1", 15)
    print(press)
    print("running:", press.is_running())
