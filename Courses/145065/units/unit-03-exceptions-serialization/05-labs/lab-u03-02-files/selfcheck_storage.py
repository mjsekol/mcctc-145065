# selfcheck_storage.py
# Checks plant.py and storage.py against the three parts of Lab U03-02.
#
# Put this file next to plant.py, storage.py, errors.py, and sample_data/,
# then run:
#     python selfcheck_storage.py
#
# It writes only inside a temporary folder, which it deletes when it ends.

import ast
import json
import os
import tempfile
from pathlib import Path

import errors
import plant
import storage

HERE = Path(__file__).parent
SAMPLES = HERE / "sample_data"
BAD = SAMPLES / "bad"
results = []

# file name -> (error class name, where), for Part 2
BAD_FILES = {
    "truncated.json": ("PlantFileFormatError", "document"),
    "nan_load.json": ("PlantFileFormatError", "document"),
    "unknown_kind.json": ("PlantFileFormatError", "line.cells[0].items[0].kind"),
    "typo_field.json": ("PlantFileFormatError", "line.cells[0].items[1]"),
    "true_as_power.json": ("PlantFileFormatError", "line.cells[1].items[0].rated_kw"),
    "negative_rating.json": ("PlantFileFormatError", "line.cells[1].items[0]"),
    "newer_version.json": ("UnsupportedVersionError", "version"),
    "duplicate_tag.json": ("PlantFileFormatError", "line"),
    "latin1_name.json": ("PlantFileFormatError", "document"),
}


def check(part, label, test):
    """test() returns None when it passes, or a string saying why not."""
    try:
        problem = test()
    except NotImplementedError as error:
        problem = f"NOT YET: {error}"
    except Exception as error:  # a self-check reports every failure, whatever its type
        problem = f"{type(error).__name__}: {error}"
    results.append((part, label, problem))


def busy_line():
    line = plant.build_sample_line()
    press1 = line.get("L3-PRS-01")
    press1.close_guard()
    press1.start()
    press1.record_strokes(1250)
    press2 = line.get("L3-PRS-02")
    press2.close_guard()
    press2.lock_out("tech-07")
    line.get("L3-CNV-01").speed_mps = 0.8
    line.get("L3-RCK-01").load_kg = 640
    line.get("L3-OVN-01").setpoint_c = 205
    return line


# ---------------- Part 1 ----------------

def t_to_dict():
    line = busy_line()
    want = {
        "L3-OVN-01": {"kind": "oven", "tag": "L3-OVN-01", "name": "Cure Oven", "rated_kw": 45.0,
                      "setpoint_c": 205.0, "max_c": 240.0, "locked_out_by": None},
        "L3-CNV-01": {"kind": "conveyor", "tag": "L3-CNV-01", "name": "Transfer Conveyor", "rated_kw": 3.0,
                      "max_speed_mps": 1.5, "speed_mps": 0.8, "locked_out_by": None},
        "L3-RCK-01": {"kind": "rack", "tag": "L3-RCK-01", "name": "Finished Goods Rack",
                      "capacity_kg": 1200.0, "load_kg": 640.0},
    }
    for tag, expected in want.items():
        got = line.get(tag).to_dict()
        if got != expected:
            return f"{tag}.to_dict() gave {got}"


def t_from_dict():
    line = busy_line()
    for tag in ("L3-OVN-01", "L3-CNV-01", "L3-RCK-01"):
        item = line.get(tag)
        rebuilt = type(item).from_dict(item.to_dict())
        if rebuilt.to_dict() != item.to_dict():
            return f"{tag}: from_dict(to_dict()) lost something: {rebuilt.to_dict()}"
    bad = line.get("L3-CNV-01").to_dict()
    bad["speed_mps"] = 9.0
    try:
        plant.Conveyor.from_dict(bad)
    except errors.ConfigurationError:
        return None
    return "Conveyor.from_dict() accepted a speed above max_speed_mps; set it through the property"


def t_text_round_trip():
    line = busy_line()
    text = storage.dumps(line)
    if not text.endswith("}\n") or '\n  "version": 2,' not in text:
        return "dumps() should use indent=2 and end with a newline"
    again = storage.dumps(storage.loads(text))
    if again != text:
        return "dumps(loads(dumps(line))) is not identical to dumps(line)"


def t_what_survives():
    reloaded = storage.loads(storage.dumps(busy_line()))
    press1, press2 = reloaded.get("L3-PRS-01"), reloaded.get("L3-PRS-02")
    if press1.is_running:
        return "a reloaded press is running; running state must not be saved"
    if press1.guard_closed:
        return "a reloaded press has its guard closed; unknown must count as open"
    if press1.strokes_since_service != 1250:
        return "strokes since service were not saved"
    if press2.locked_out_by != "tech-07":
        return "the lockout was lost on reload; that leaves a technician unprotected"


def t_encoding():
    line = busy_line()
    line.items[2].add(plant.Cell("Área de Soldadura"))
    text = storage.dumps(line)
    if "\\u00c1" in text:
        return "the name was escaped as \\u00c1; pass ensure_ascii=False"
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "line3.json"
        storage.save_line(line, path)
        raw = path.read_bytes()
        if "Área".encode("utf-8") not in raw:
            return "the file does not hold the name as UTF-8 bytes; open it with encoding='utf-8'"
        reloaded = storage.load_line(path)
        names = [cell.name for cell in reloaded.items[2].items if isinstance(cell, plant.Cell)]
        if names != ["Área de Soldadura"]:
            return f"the name came back as {names}"


def t_file_round_trip():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "line3.json"
        line = busy_line()
        storage.save_line(line, path)
        if storage.dumps(storage.load_line(path)) != storage.dumps(line):
            return "save_line() then load_line() did not give back the same line"


# ---------------- Part 2 ----------------

def t_bad_files():
    for name, (error_name, where) in BAD_FILES.items():
        try:
            storage.load_line(BAD / name)
        except errors.PlantFileFormatError as error:
            if type(error).__name__ != error_name or error.where != where:
                return f"{name}: raised {type(error).__name__} at {error.where!r}, want {error_name} at {where!r}"
        except Exception as error:  # anything else is the wrong refusal
            return f"{name}: raised {type(error).__name__}: {error}; want {error_name}"
        else:
            return f"{name} loaded; it should be refused"


def t_nan_refused():
    text = storage.dumps(busy_line()).replace('"load_kg": 640.0', '"load_kg": Infinity')
    try:
        storage.loads(text)
    except errors.PlantFileFormatError as error:
        if "Infinity" not in error.problem:
            return f"refused, but the problem should name Infinity: {error.problem}"
        return None
    return "a load_kg of Infinity was accepted; pass parse_constant to json.loads"


def t_missing_file():
    try:
        storage.load_line(SAMPLES / "no_such_file.json")
    except errors.PlantFileMissingError as error:
        if not isinstance(error, FileNotFoundError):
            return "PlantFileMissingError must still be a FileNotFoundError"
        return None
    except Exception as error:  # anything else is the wrong refusal
        return f"raised {type(error).__name__}; want PlantFileMissingError"
    return "a missing file did not raise"


def t_bom_accepted():
    line = storage.load_line(BAD / "bom_but_valid.json")
    if line.get("L3-PRS-02").locked_out_by != "tech-07":
        return "the file with a byte order mark loaded, but lost data"


def t_size_limit():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "huge.json"
        path.write_bytes(b" " * (storage.MAX_FILE_BYTES + 1))
        try:
            storage.load_line(path)
        except errors.PlantFileFormatError as error:
            if "limit" not in error.problem:
                return f"refused, but not for its size: {error.problem}"
            return None
    return "a file over MAX_FILE_BYTES was read"


def t_no_pickle():
    tree = ast.parse((HERE / "storage.py").read_text(encoding="utf-8"))
    risky = {"pickle", "dill", "shelve", "marshal"}
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module.split(".")[0]]
        if risky.intersection(names):
            return f"storage.py imports {sorted(risky.intersection(names))}; loading those formats can run code"


# ---------------- Part 3 ----------------

def t_backup():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "line3.json"
        line = busy_line()
        if storage.save_line(line, path) is not None:
            return "the first save should return None: there was nothing to back up"
        first = path.read_bytes()
        line.get("L3-RCK-01").load_kg = 950
        backup = storage.save_line(line, path)
        if backup is None or Path(backup).name != "line3.json.bak":
            return f"the second save should return the .bak path, got {backup}"
        if Path(backup).read_bytes() != first:
            return "the .bak does not hold the previous file"
        leftovers = sorted(p.name for p in Path(folder).iterdir())
        if leftovers != ["line3.json", "line3.json.bak"]:
            return f"the folder should hold the file and its backup only, holds {leftovers}"


def t_model_error_touches_nothing():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "line3.json"
        line = busy_line()
        storage.save_line(line, path)
        before = path.read_bytes()
        line.get("L3-RCK-01")._load_kg = {640}  # a set cannot be written as JSON
        try:
            storage.save_line(line, path)
        except TypeError:
            pass
        if path.read_bytes() != before:
            return "a save that failed while building the text damaged the file"
        if sorted(p.name for p in Path(folder).iterdir()) != ["line3.json"]:
            return "a save that failed before writing still made a .bak or .tmp"


def t_crash_mid_save():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "line3.json"
        line = busy_line()
        storage.save_line(line, path)
        before = path.read_bytes()
        real_replace = os.replace

        def power_cut(*args, **kwargs):
            raise OSError("simulated power cut")

        storage.os.replace = power_cut
        try:
            storage.save_line(line, path)
        except errors.PlantFileError:
            pass
        else:
            return "a failed os.replace() should raise PlantFileError"
        finally:
            storage.os.replace = real_replace
        if path.read_bytes() != before:
            return "the real file changed even though the save failed"
        if (Path(folder) / "line3.json.tmp").exists():
            return "the .tmp file was left behind after a failed save"


def t_restore():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "line3.json"
        line = busy_line()
        storage.save_line(line, path)
        line.get("L3-RCK-01").load_kg = 950
        storage.save_line(line, path)
        path.write_text('{"format": "line3-plant", "version": 2, "line": ', encoding="utf-8")
        restored = storage.restore_backup(path)
        if restored.get("L3-RCK-01").load_kg != 640:
            return "restore_backup() did not bring back the previous save"
        if storage.load_line(path).get("L3-RCK-01").load_kg != 640:
            return "restore_backup() returned the line but did not put the file back"
        storage.backup_path(path).write_text("not json", encoding="utf-8")
        good = path.read_bytes()
        try:
            storage.restore_backup(path)
        except errors.PlantFileFormatError:
            pass
        else:
            return "a corrupt backup was restored"
        if path.read_bytes() != good:
            return "a corrupt backup overwrote the last good file"


def t_migration():
    document = json.loads((SAMPLES / "line3_v1.json").read_text(encoding="utf-8"))
    snapshot = json.dumps(document, sort_keys=True)
    upgraded = storage.migrate(document)
    if json.dumps(document, sort_keys=True) != snapshot:
        return "migrate() changed the version 1 document it was given"
    if upgraded["version"] != 2:
        return "the migrated document is not version 2"
    press = upgraded["line"]["cells"][0]["items"][0]
    if press.get("rated_kw") != 15 or "power_kw" in press:
        return f"power_kw was not renamed to rated_kw: {press}"
    line = storage.load_line(SAMPLES / "line3_v1.json")
    if len(line.equipment()) != 5 or line.get("L3-PRS-01").service_interval != 20000:
        return "the version 1 sample did not load as five machines with default service intervals"
    if storage.dumps(storage.loads(storage.dumps(line))) != storage.dumps(line):
        return "a migrated line does not survive a round trip as version 2"


check(1, "Step 2   to_dict() for oven, conveyor, and rack", t_to_dict)
check(1, "Step 2   from_dict() rebuilds them through their rules", t_from_dict)
check(1, "Step 4   text round trip is identical", t_text_round_trip)
check(1, "Step 4   running and guard are not saved; lockout is", t_what_survives)
check(1, "Step 5   file round trip is identical", t_file_round_trip)
check(1, "Step 6   non-ASCII names survive as UTF-8", t_encoding)
check(2, "Step 7-8 every bad sample file is refused at the right place", t_bad_files)
check(2, "Step 8   NaN and Infinity are refused", t_nan_refused)
check(2, "Step 9   a missing file is PlantFileMissingError", t_missing_file)
check(2, "Step 9   a byte order mark is accepted", t_bom_accepted)
check(2, "Step 9   an oversized file is refused before reading", t_size_limit)
check(2, "Step 10  no pickle anywhere in storage.py", t_no_pickle)
check(3, "Step 11  the second save leaves a .bak of the first", t_backup)
check(3, "Step 11  a failure while building the text touches no file", t_model_error_touches_nothing)
check(3, "Step 11  a failure mid-save leaves the real file whole", t_crash_mid_save)
check(3, "Step 11  restore_backup() checks the backup first", t_restore)
check(3, "Step 12  version 1 files migrate to version 2", t_migration)

passed = 0
for part, label, problem in results:
    if problem is None:
        print(f"PASS  Part {part}  {label}")
        passed += 1
    else:
        print(f"FAIL  Part {part}  {label}")
        for line in problem.splitlines():
            print(f"        {line}")
print(f"\n{passed} of {len(results)} self-checks passed")
