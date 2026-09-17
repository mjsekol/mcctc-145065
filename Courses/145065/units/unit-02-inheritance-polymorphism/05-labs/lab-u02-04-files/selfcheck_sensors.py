# selfcheck_sensors.py
# Checks your sensors.py against Lab U02-04.
#
# Put this file next to sensors.py and run:
#     python selfcheck_sensors.py

import sensors as model

results = []

EXPECTED = [
    "[WARNING] L3-PRS-01: coolant-level reads 14 %, below 20",
    "[WARNING] L3-PRS-02: press-vibration reads 9.2 mm/s, above 8",
    "[WARNING] L3-OVN-01: 228 C is 28 C from setpoint 200 C",
]


def check(label, test):
    """test() returns None when it passes, or a string saying why not."""
    try:
        problem = test()
    except Exception as error:  # a self-check reports every failure, whatever its type
        problem = f"{type(error).__name__}: {error}"
    results.append((label, problem))


def refused(error_type, action):
    try:
        action()
    except error_type:
        return True
    return False


def vibration():
    return model.Sensor("press-vibration", "vibration", "mm/s", 0, 8)


def t_subclasses_gone():
    left = [name for name in ("VibrationPress", "CoolantPress", "VibrationCoolantPress", "MonitoredOven")
            if hasattr(model, name)]
    if left:
        return "these reading subclasses are still here: " + ", ".join(left)


def t_not_a_sensor():
    for cls in (model.Equipment, model.PoweredEquipment, model.Press, model.Oven):
        if issubclass(cls, model.Sensor):
            return f"{cls.__name__} inherits from Sensor; equipment HAS sensors"
    press = model.Press("L3-PRS-01", "Press 1")
    press.attach_sensor
    press.sensor
    press.sensors


def t_attach_and_find():
    press = model.Press("L3-PRS-01", "Press 1")
    sensor = vibration()
    if press.attach_sensor(sensor) is not sensor:
        return "attach_sensor() should return the sensor it attached"
    if press.sensor("press-vibration") is not sensor:
        return "sensor('press-vibration') did not return the attached sensor"
    if sensor.owner_tag != "L3-PRS-01":
        return "attach_sensor() did not mount the sensor (owner_tag is not set)"
    if not refused(KeyError, lambda: press.sensor("oil-temp")):
        return "asking for a sensor that is not there should raise KeyError"


def t_refusals():
    press = model.Press("L3-PRS-01", "Press 1")
    press.attach_sensor(vibration())
    if not refused(ValueError, lambda: press.attach_sensor(vibration())):
        return "a second sensor with the same id was accepted"
    if not refused(TypeError, lambda: press.attach_sensor("press-vibration")):
        return "a string was accepted as a sensor"
    shared = model.Sensor("coolant-level", "level", "%", 20, 100)
    press.attach_sensor(shared)
    other = model.Press("L3-PRS-02", "Press 2")
    if not refused(ValueError, lambda: other.attach_sensor(shared)):
        return "one physical sensor was mounted on two presses"


def t_sensors_is_a_copy():
    press = model.Press("L3-PRS-01", "Press 1")
    press.attach_sensor(vibration())
    view = press.sensors
    if not isinstance(view, tuple):
        return f"sensors should be a tuple, got {type(view).__name__}"
    press.attach_sensor(model.Sensor("coolant-level", "level", "%", 20, 100))
    if len(view) != 1 or len(press.sensors) != 2:
        return "sensors should be a new tuple each time it is read"


def t_same_findings():
    items = model.build_sample()
    model.record_sample_readings(*items)
    got = [str(finding) for item in items for finding in item.inspect()]
    if got != EXPECTED:
        return f"findings were {got}"


def t_independent_presses():
    press1, press2, _oven = model.build_sample()
    press1.sensor("press-vibration").record(9.9)
    if press2.sensor("press-vibration").value is not None:
        return "a reading on Press 1 showed up on Press 2"
    if [str(f) for f in press2.inspect()] != ["[INFO] L3-PRS-02: press-vibration has no reading"]:
        return f"Press 2 with no reading gave {[str(f) for f in press2.inspect()]}"


def t_any_combination():
    press = model.Press("L3-PRS-03", "Press 3")
    press.attach_sensor(model.Sensor("oil-temp", "temperature", "C", 10, 70))
    press.attach_sensor(vibration())
    press.sensor("oil-temp").record(75)
    press.sensor("press-vibration").record(2.0)
    got = [str(f) for f in press.inspect()]
    if got != ["[WARNING] L3-PRS-03: oil-temp reads 75 C, above 70"]:
        return f"a press with an oil sensor and a vibration sensor gave {got}"


def t_oven_uses_its_sensor():
    oven = model.Oven("L3-OVN-02", "Test Oven", setpoint_c=180, max_c=220)
    if [str(f) for f in oven.inspect()] != ["[WARNING] L3-OVN-02: no temperature sensor mounted"]:
        return f"an oven with no sensor gave {[str(f) for f in oven.inspect()]}"
    oven.attach_sensor(model.Sensor("oven-temp", "temperature", "C", 0, 240))
    oven.start()
    if [str(f) for f in oven.inspect()] != ["[INFO] L3-OVN-02: oven-temp has no reading"]:
        return f"a running oven whose sensor has no reading gave {[str(f) for f in oven.inspect()]}"
    oven.sensor("oven-temp").record(230)
    want = ["[STOP] L3-OVN-02: 230 C is above the oven maximum 220 C",
            "[WARNING] L3-OVN-02: 230 C is 50 C from setpoint 180 C"]
    if [str(f) for f in oven.inspect()] != want:
        return f"an oven at 230 C gave {[str(f) for f in oven.inspect()]}"


check("Step 3  equipment has sensors and is not one", t_not_a_sensor)
check("Step 3  attach_sensor() mounts, sensor() finds", t_attach_and_find)
check("Step 3  duplicates, non-sensors, and shared sensors are refused", t_refusals)
check("Step 3  sensors hands out a copy", t_sensors_is_a_copy)
check("Step 4  any combination of sensors needs no new class", t_any_combination)
check("Step 5  the oven reads its temperature from its own sensor", t_oven_uses_its_sensor)
check("Step 6  the sample still gives the starter's findings", t_same_findings)
check("Step 6  two presses keep their own readings", t_independent_presses)
check("Step 6  the four reading subclasses are gone", t_subclasses_gone)

passed = 0
for label, problem in results:
    if problem is None:
        print(f"PASS  {label}")
        passed += 1
    else:
        print(f"FAIL  {label}")
        print(f"        {problem}")
print(f"\n{passed} of {len(results)} self-checks passed")
