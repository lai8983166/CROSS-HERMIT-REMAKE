"""Compare the first deployed student slots before either MAP44 clock advances."""
import argparse
import hashlib
import json
from pathlib import Path


FIELDS = ("role", "side", "state", "cell", "max_hp", "hp", "max_mp", "mp")


def compare(original, remake, admission):
    digest = admission["before"]["sha256"]
    if original.get("exported_school_sha256") != digest:
        raise ValueError("Guest checkpoint differs from the admission report")
    if (original["scene"], original["date"], original["elapsed"]) != (44, [13, 2], 0):
        raise ValueError("Original sample must come from the January MAP44 opening at tick zero")
    if (remake["scene"], remake["elapsed"], remake["source_sha256"]) != (44, 0, digest):
        raise ValueError("Remake opening clock, scene or source save differs")
    squad, = admission["original_prepared"]["rounds"]
    expected = squad["student_ids"]
    if len(expected) != 19 or len(set(expected)) != 19 or squad != remake["party"]:
        raise ValueError("The two departures must agree on all 19 students and their classes")
    projected = remake["opening_students"]
    if [row["role"] for row in projected] != expected:
        raise ValueError("Remake student slots disagree with the accepted departure")
    actual = {row["slot"]: row for row in original["units"]}
    if len(actual) != len(original["units"]):
        raise ValueError("Duplicate original work slot")
    for slot, row in enumerate(projected):
        if slot not in actual:
            return {"slot": slot, "field": "presence", "original": False, "remake": True}
        for field in FIELDS:
            if actual[slot][field] != row[field]:
                return {"slot": slot, "field": field, "original": actual[slot][field], "remake": row[field]}
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("original", "remake", "admission"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    inputs = {key: path.read_bytes() for key, path in vars(args).items()}
    difference = compare(**{key: json.loads(data) for key, data in inputs.items()})
    print(json.dumps({"checkpoint": "opening_students", "elapsed": 0, "first_difference": difference,
                      "input_sha256": {k: hashlib.sha256(v).hexdigest() for k, v in inputs.items()}},
                     ensure_ascii=False))
    return int(difference is not None)


if __name__ == "__main__":
    raise SystemExit(main())
