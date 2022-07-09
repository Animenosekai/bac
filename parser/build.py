import sys
import json
import hashlib
import pathlib

INDENT = 4


def log_debug(*args, indent: int = 1, end: str = "\n"):
    if "-v" in sys.argv or "--verbose" in sys.argv:
        print(" " * (INDENT * indent) + " ".join([str(v) for v in args]), end=end)


print("Building parser...")

log_debug("Reading parser source code")
with open("parser/page.py") as f:
    lines = f.read()

log_debug("Reading class data")
with open("data/class.json") as f:
    data = json.load(f)

log_debug("Initializing variables")
BUILD_NUMBER = 0
BUILD_HASH = None
results = ""

log_debug("Analyzing lines")
for index, line in enumerate(lines.splitlines()):
    log_debug("Analyzing line...", index + 1, indent=2, end="\r")
    if line.endswith("# BUILD: CLASS_DATA"):
        log_debug("")
        log_debug("Found CLASS_DATA flag", indent=2)
        if "# BUILT: CLASS_DATA" in results:
            log_debug("CLASS_DATA already replaced", indent=2)
            continue
        log_debug("Replacing CLASS_DATA...", indent=2)
        results += "# BUILT: CLASS_DATA\n"
        results += "CLASS_DATA = " + str(data) + "\n"
        log_debug("")
        continue
    results += line + "\n"

log_debug("")
log_debug("Computing the resulting file hash")
current_hash = hashlib.sha256(results.encode("utf-8")).hexdigest()
log_debug("Resulting hash:", current_hash)

print("Gathering information on the previous version...")
if pathlib.Path("website/parser.py").is_file():
    log_debug("website/parser.py found")
    log_debug("Analyzing lines")
    for index, line in enumerate(pathlib.Path("website/parser.py").read_text().splitlines()):
        log_debug("Analyzing line...", index + 1, indent=2, end="\r")
        if line.startswith("# BUILD_NUMBER"):
            log_debug("")
            log_debug("Found BUILD_NUMBER flag", indent=2)
            _, _, BUILD_NUMBER = line.partition(":")
            BUILD_NUMBER = int(BUILD_NUMBER.strip())
            log_debug("Previous build number:", BUILD_NUMBER, indent=2)
            log_debug("")
            if BUILD_HASH is not None:
                break
            continue
        if line.startswith("# BUILD_HASH"):
            log_debug("")
            log_debug("Found BUILD_HASH flag", indent=2)
            _, _, BUILD_HASH = line.partition(":")
            BUILD_HASH = BUILD_HASH.strip()
            log_debug("Previous hash:", BUILD_HASH, indent=2)
            log_debug("")
            if BUILD_NUMBER > 0:
                break
            continue
    log_debug("")
    if BUILD_HASH != current_hash:
        log_debug("Parser source code has changed")
        BUILD_NUMBER += 1
else:
    BUILD_NUMBER += 1

log_debug("New build number:", BUILD_NUMBER)

print("Exporting parser...")
with open("website/parser.py", "w") as f:
    log_debug("Adding new BUILD_NUMBER and BUILD_HASH")
    f.write(f"# BUILD_NUMBER: {BUILD_NUMBER}\n# BUILD_HASH: {current_hash}\n" + results)
