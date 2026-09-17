# value_model.py
# A small, honest value model for your emerging technology brief.
#
# STARTER FILE. It runs and prints your inputs. It calculates nothing yet.
#
# Rules:
#   1. Every input is a pair: (number, where it came from).
#   2. "where it came from" is either a source number from your brief, like
#      "source [2]", or the word "assumption" followed by your reasoning.
#   3. No number appears anywhere else in this file. Calculations use names.
#
# The example inputs below are for Riverside Fabrication, a composite shop.
# They are invented. Replace them with your own buyer's inputs.

INPUTS = {
    "kit_cost": (1800.00, "assumption: sensors plus one Pi, to be replaced with a quote"),
    "install_hours": (16, "assumption: two technicians for one shift"),
    "labor_rate": (38.00, "assumption: loaded hourly cost of a technician"),
    "downtime_hours_avoided": (10, "assumption: per year, from the shop's own log"),
    "cost_per_downtime_hour": (450.00, "assumption: lost output while Line 3 is down"),
}


def value(name):
    # Returns only the number, so calculations read cleanly.
    return INPUTS[name][0]


def print_inputs():
    print("INPUTS")
    for name, (number, origin) in INPUTS.items():
        print(f"  {name:<24} {number:>10,.2f}   {origin}")


# TODO 1: calculate the upfront cost from the inputs.

# TODO 2: calculate the yearly benefit from the inputs.

# TODO 3: calculate the payback period in months, and print it with a label.

# TODO 4 (medium scope): print a low, likely, and high scenario by changing
# the input you are least sure of, and say which input the answer depends on most.


if __name__ == "__main__":
    print_inputs()
    print("No calculations written yet.")
