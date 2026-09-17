# licenses.py
# Flask is code you did not write. What came with it, and under what terms?
from importlib.metadata import metadata, requires, version


def license_of(package):
    """Newer packages state a license expression. Older ones use a classifier."""
    info = metadata(package)
    if info.get("License-Expression"):
        return info["License-Expression"]
    for line in info.get_all("Classifier") or []:
        if line.startswith("License ::"):
            return line.split(" :: ")[-1]
    return "not stated: read the LICENSE file"


print(f"flask {version('flask')}  {license_of('flask')}")
for requirement in requires("flask"):
    if ";" in requirement:          # skip extras and old-Python-only packages
        continue
    name = requirement.split(">")[0].split("=")[0].strip()
    print(f"  needs {name} {version(name)}  {license_of(name)}")
