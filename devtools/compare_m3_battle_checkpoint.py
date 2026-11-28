"""Compare an observed original MAP44 clock with a matching remake command checkpoint."""
import argparse
import hashlib
import json
from pathlib import Path

from devtools.m3_adventure44_orders import TRACE_SHA


def compare(original, remake):
    if (original.get("scene"), original.get("date")) != (44, [13, 2]):
        raise ValueError("Original sample is outside January MAP44")
    if (remake.get("source_kind") != "original_save" or remake.get("trace_sha256") != TRACE_SHA
            or not original.get("exported_school_sha256")
            or remake["source_sha256"] != original["exported_school_sha256"]):
        raise ValueError("Both observations must identify the same original save and fixed order history")
    matches = [sample for sample in remake["samples"] if sample["elapsed"] == original["elapsed"]]
    if len(matches) != 1:
        raise ValueError("No unique remake checkpoint at the observed original clock")
    expected = matches[0]["students"]
    if len(expected) != 19 or len({row[0] for row in expected}) != 19:
        raise ValueError("Incomplete remake student roster")
    native = {unit["slot"]:unit for unit in original["units"]}
    if len(native) != len(original["units"]):
        raise ValueError("Repeated original unit slot")
    for slot, values in enumerate(expected):
        if slot not in native:
            return {"slot":slot, "field":"presence", "original":False, "remake":True}
        unit = native[slot]
        fields = ("role", "side", "state", "x", "y", "max_hp", "hp", "max_mp", "mp")
        actual = dict(unit, x=unit["cell"][0], y=unit["cell"][1])
        for field, projected in zip(fields, values, strict=True):
            if actual[field] != projected:
                return {"slot":slot, "field":field, "original":actual[field], "remake":projected}
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("remake", type=Path)
    parser.add_argument("observations", type=Path, nargs="+")
    args = parser.parse_args()
    report = json.loads(args.remake.read_bytes())
    observations = []
    for path in args.observations:
        raw = path.read_bytes()
        samples = raw.splitlines(keepends=True) if path.suffix.lower()==".jsonl" else [raw]
        if not samples:
            parser.error(f"No original observations in {path}")
        for entry in samples:
            sample = json.loads(entry)
            observations.append((sample["elapsed"], hashlib.sha256(entry).hexdigest(), sample))
    if len({row[0] for row in observations}) != len(observations):
        raise ValueError("Repeated clock among original observations")
    for index, (clock, digest, sample) in enumerate(sorted(observations), 1):
        difference = compare(sample, report)
        if difference:
            print(json.dumps({"first_observed_difference":difference, "elapsed":clock,
                              "original_sha256":digest, "observations_checked":index}))
            return 1
    print(json.dumps({"first_observed_difference":None, "observations_checked":len(observations)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
