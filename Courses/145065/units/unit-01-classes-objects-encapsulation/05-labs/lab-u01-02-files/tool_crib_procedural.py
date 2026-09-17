# tool_crib_procedural.py
# The Line 3 tool crib program, as it runs today: one dictionary of tools and
# eight loose functions. Technicians check tools out with their badge, and the
# crib attendant prints a report so nothing walks off for a whole shift.
#
# Riverside Fabrication is a composite: an invented small metal fabrication
# shop. Every tag, badge, and time here is invented.
#
#     python tool_crib_procedural.py
#
# Times are whole minutes since the shift started. Minute 90 is 1 h 30 min in.

OVERDUE_AFTER_MINUTES = 240   # a tool out longer than four hours gets chased


def add_tool(crib, tag, name):
    crib[tag] = {"tag": tag, "name": name, "holder": None, "out_at": None}


def check_out(crib, tag, badge, minute):
    tool = crib[tag]
    if tool["holder"] is not None:
        print(f"  refused: {tag} is already out to {tool['holder']}")
        return
    tool["holder"] = badge
    tool["out_at"] = minute


def check_in(crib, tag, minute):
    tool = crib[tag]
    minutes = minutes_between(tool["out_at"], minute)
    tool["holder"] = None
    tool["out_at"] = None
    return minutes


def is_out(crib, tag):
    return crib[tag]["holder"] is not None


def tools_out(crib):
    return [tool for tool in crib.values() if tool["holder"] is not None]


def minutes_between(start_minute, end_minute):
    return end_minute - start_minute


def format_duration(minutes):
    hours, leftover = divmod(minutes, 60)
    return f"{hours} h {leftover:02d} min"


def crib_report(crib, now):
    lines = []
    for tool in crib.values():
        if tool["holder"] is None:
            lines.append(f"{tool['tag']} {tool['name']}: in the crib")
        else:
            out_for = minutes_between(tool["out_at"], now)
            flag = " OVERDUE" if out_for > OVERDUE_AFTER_MINUTES else ""
            lines.append(f"{tool['tag']} {tool['name']}: out to {tool['holder']} "
                         f"for {format_duration(out_for)}{flag}")
    return lines


def main():
    crib = {}
    add_tool(crib, "TC-014", "Torque wrench")
    add_tool(crib, "TC-022", "Digital caliper")
    add_tool(crib, "TC-031", "Feeler gauge set")

    check_out(crib, "TC-014", "tech-07", 30)
    check_out(crib, "TC-022", "tech-12", 95)
    check_out(crib, "TC-022", "tech-07", 120)         # refused, correctly
    print("  TC-022 back after", format_duration(check_in(crib, "TC-022", 150)))
    print("  Out now:", [tool["tag"] for tool in tools_out(crib)])

    print("Crib report at minute 300")
    for line in crib_report(crib, 300):
        print("  " + line)

    # Two things the functions never stop.
    add_tool(crib, "TC-014", "Torque wrench (spare)")  # replaces the one tech-07 has
    print("After the spare was added, is TC-014 out?", is_out(crib, "TC-014"))
    # The last line crashes on purpose, so you can read where the damage shows up.
    check_in(crib, "TC-031", 310)                      # it was never checked out


if __name__ == "__main__":
    main()
