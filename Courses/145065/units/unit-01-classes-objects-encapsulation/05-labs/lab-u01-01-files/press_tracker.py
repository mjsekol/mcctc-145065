# press_tracker.py
# The Line 3 press tracker, written the way you wrote programs last semester:
# the data is a dictionary, and the rules are loose functions.
#
# Riverside Fabrication is a composite: an invented small metal fabrication
# shop. Every tag, badge, and number here is invented.
#
#     python press_tracker.py
#
# It runs. Read the end of main() before you trust what it prints.


def new_press(asset_tag, name, rated_kw):
    """Return a dictionary for one press. Nothing is checked."""
    return {
        "asset_tag": asset_tag,
        "name": name,
        "rated_kw": rated_kw,
        "running": False,
        "locked_by": None,     # the badge of the person holding the lockout
        "run_minutes": 0,
    }


def start(press):
    """Start a press, unless someone holds a lockout on it."""
    if press["locked_by"] is not None:
        print(f"  refused: {press['asset_tag']} is locked out by {press['locked_by']}")
        return
    press["running"] = True


def stop(press):
    press["running"] = False


def lock_out(press, badge):
    """Lock out and tag out: stop the press and record who holds the lock."""
    stop(press)
    press["locked_by"] = badge


def release_lockout(press, badge):
    """Only the person who applied the lock may remove it."""
    if press["locked_by"] != badge:
        print(f"  refused: only {press['locked_by']} can release {press['asset_tag']}")
        return
    press["locked_by"] = None


def record_run(press, minutes):
    """Add run time, but only while the press is running."""
    if press["running"]:
        press["run_minutes"] += minutes


def status_text(press):
    state = "RUNNING" if press["running"] else "STOPPED"
    if press["locked_by"] is not None:
        state += f", LOCKED OUT ({press['locked_by']})"
    return (f"{press['asset_tag']} {press['name']}: {state}, "
            f"{press['rated_kw']} kW, {press['run_minutes']} min run")


def main():
    press1 = new_press("L3-PRS-01", "Press 1", 15)
    press2 = new_press("L3-PRS-02", "Press 2", 22)

    print("First half of the shift")
    start(press1)
    record_run(press1, 45)
    lock_out(press2, "tech-07")
    start(press2)                       # refused, correctly
    release_lockout(press2, "tech-12")  # refused, correctly

    # Every rule above lives in a function. Nothing forces anyone to call it.
    # These three lines were added later, by three different people.
    press2["running"] = True            # a "quick fix" for a stuck status light
    press1["rated_kw"] = -15            # a setup script with a sign error
    press1["runing"] = False            # a typo: this makes a NEW key

    print("End of the shift")
    for press in [press1, press2]:
        print("  " + status_text(press))


if __name__ == "__main__":
    main()
