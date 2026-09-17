"""Print the sample crib report. Your C# port must print the same lines."""

from crib import Kit, build_sample_crib, crib_report

things = build_sample_crib()
for thing in things:
    if isinstance(thing, Kit):
        print(f"{thing.label}: {thing.count_tools()} tools")
    else:
        print(thing.describe())
print("Issues:")
for line in crib_report(things):
    print("  " + line)
