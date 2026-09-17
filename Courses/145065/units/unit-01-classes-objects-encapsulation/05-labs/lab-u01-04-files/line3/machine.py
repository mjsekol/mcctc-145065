"""One machine on Line 3, modeled as a class.

Scope map for this file (Unit 1, Week 3):
  SITE_NAME            module (global) scope: one value for the whole program
  Machine.line_name    class scope: shared by every Machine object
  self._rated_kw       instance scope: each Machine has its own
  minutes (in record_run)  local scope: gone when the method returns
"""

import math
import re

SITE_NAME = "Riverside Fabrication"

# Asset tags look like L3-PRS-01: line, three-letter equipment code, two digits.
# [0-9], not \d: in Python 3, \d also matches digits from other scripts.
_TAG_PATTERN = re.compile(r"L3-[A-Z]{3}-[0-9]{2}")


def celsius_to_fahrenheit(celsius):
    """Convert a temperature. A plain function, because it needs no machine."""
    return celsius * 9 / 5 + 32


class Machine:
    """A piece of powered equipment on Line 3.

    The object bundles the machine's data (tag, rating, temperature, lockout)
    with the only operations allowed to change that data.
    """

    # Class attributes: one copy, shared by every Machine.
    line_name = "Line 3"
    MIN_TEMP_C = -40.0
    MAX_TEMP_C = 1200.0
    MAX_RATED_KW = 500.0
    _machines_created = 0

    def __init__(self, asset_tag, name, rated_kw):
        if not Machine.is_valid_asset_tag(asset_tag):
            raise ValueError(f"asset tag {asset_tag!r} does not match the L3-ABC-00 pattern")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-blank string")
        # Instance attributes: every Machine gets its own copy.
        self._asset_tag = asset_tag
        self._name = name.strip()
        self.rated_kw = rated_kw  # runs the property setter, so it is validated
        self._running = False
        self._temperature_c = None  # None means "never read", which is not 0
        self._run_minutes = 0
        # Two underscores trigger name mangling. Python renames this attribute to
        # _Machine__lockout_holder. That discourages outside access. It does not
        # prevent it. Nothing in Python enforces privacy.
        self.__lockout_holder = None
        Machine._machines_created += 1

    # ----- static and class methods -------------------------------------

    @staticmethod
    def is_valid_asset_tag(tag):
        """True if tag looks like L3-PRS-01. Needs no machine, so it is static."""
        return isinstance(tag, str) and _TAG_PATTERN.fullmatch(tag) is not None

    @classmethod
    def machines_created(cls):
        """How many Machine objects this program has built. Reads class state."""
        return cls._machines_created

    # ----- properties: read access and validated write access -----------

    @property
    def asset_tag(self):
        """Read-only. A tag is painted on the machine; it does not change."""
        return self._asset_tag

    @property
    def name(self):
        return self._name

    @property
    def rated_kw(self):
        return self._rated_kw

    @rated_kw.setter
    def rated_kw(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"rated_kw must be a number, not {type(value).__name__}")
        if not math.isfinite(value) or not 0 < value <= Machine.MAX_RATED_KW:
            raise ValueError(f"rated_kw must be above 0 and at most {Machine.MAX_RATED_KW:g}")
        self._rated_kw = float(value)

    @property
    def temperature_c(self):
        """The last temperature reading, or None if there has never been one."""
        return self._temperature_c

    @temperature_c.setter
    def temperature_c(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"temperature must be a number, not {type(value).__name__}")
        if not math.isfinite(value) or not Machine.MIN_TEMP_C <= value <= Machine.MAX_TEMP_C:
            raise ValueError(
                f"temperature {value} C is outside the possible range "
                f"{Machine.MIN_TEMP_C:g} to {Machine.MAX_TEMP_C:g}"
            )
        self._temperature_c = float(value)

    @property
    def is_running(self):
        return self._running

    @property
    def run_minutes(self):
        return self._run_minutes

    @property
    def is_locked_out(self):
        return self.__lockout_holder is not None

    @property
    def locked_out_by(self):
        return self.__lockout_holder

    # ----- instance methods: behavior that changes this machine ---------

    def start(self):
        if self.is_locked_out:
            raise RuntimeError(
                f"{self._asset_tag} is locked out by {self.__lockout_holder} and cannot start"
            )
        self._running = True

    def stop(self):
        self._running = False

    def lock_out(self, badge):
        """Lock out and tag out: stop the machine and record who holds the lock."""
        if not isinstance(badge, str) or not badge.strip():
            raise ValueError("badge must be a non-blank string")
        badge = badge.strip()
        if self.__lockout_holder is not None and self.__lockout_holder != badge:
            raise RuntimeError(f"{self._asset_tag} is already locked out by {self.__lockout_holder}")
        self.stop()
        self.__lockout_holder = badge

    def release_lockout(self, badge):
        """Only the person who applied the lock may remove it."""
        if self.__lockout_holder is None:
            raise RuntimeError(f"{self._asset_tag} is not locked out")
        if badge != self.__lockout_holder:
            raise RuntimeError(
                f"only {self.__lockout_holder} can release the lockout on {self._asset_tag}"
            )
        self.__lockout_holder = None

    def record_run(self, minutes):
        """Add run time. Only a running machine accumulates run time."""
        if not self._running:
            raise RuntimeError(f"{self._asset_tag} is not running")
        if isinstance(minutes, bool) or not isinstance(minutes, int) or minutes <= 0:
            raise ValueError("minutes must be a positive whole number")
        self._run_minutes += minutes

    def status_text(self):
        if self.is_locked_out:
            state = f"LOCKED OUT ({self.__lockout_holder})"
        elif self._running:
            state = "RUNNING"
        else:
            state = "STOPPED"
        if self._temperature_c is None:
            temp = "no reading"
        else:
            temp = f"{self._temperature_c:.1f} C"
        return f"{self._asset_tag} {self._name}: {state}, {temp}, {self._run_minutes} min run"

    def __repr__(self):
        return (
            f"Machine(asset_tag={self._asset_tag!r}, name={self._name!r}, "
            f"rated_kw={self._rated_kw!r})"
        )
