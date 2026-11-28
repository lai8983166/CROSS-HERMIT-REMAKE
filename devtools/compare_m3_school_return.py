"""Compare the returned January school with the independently saved original."""
import argparse
import json
from pathlib import Path

from devtools.compare_m3_native_saves import adventure44_party, compare, snapshot


def differences(original, remake, before, squad):
    if remake["origin_sha"] != before["sha256"]:
        raise ValueError("Remake continuation belongs to a different school save")
    school = remake["school"]
    result = remake["last_result"]
    yield "school.date", original["date"], [school["month"], school["week"]]
    yield "result.scene", original["departure_mission"], result["scene"]
    ids = squad["original_prepared"]["rounds"][0]["student_ids"]
    yield "result.students", ids, [row["id"] for row in result["changes"]]
    yield "result.experience", original["global_score"] - before["global_score"], result["experience"]
    yield "school.score", original["global_score"], remake["score"]
    yield "school.mission44_grade", original["mission44_grade"], remake["grades"][43]
    yield from member_fields(original, remake)


def member_fields(original, remake, include_staged=True):
    school = remake["school"]
    yield "school.roster", original["roster"], school["student_ids"]
    yield "school.item_flags", original["item_flags"], remake["item_flags"]
    for member in original["roster"]:
        native = original["roles"][str(member)]
        row = remake["members"][str(member)]
        for key in ("job", "level", "attributes", "growth_pools", "staged_package", "staged_total",
                    "skill_statuses", "week_records", "equipped_skills", "equipped_items", "unlock_flags", "mvp_count"):
            if include_staged or key not in ("staged_package","staged_total"):
                yield f"member[{member}].{key}", native[key], row["level_50" if key == "level" else key]
        yield f"member[{member}].job_progress", native["job_progress"][:31], [v & 255 for v in row["job_progress"]]
    people = original["roster"] + original["teachers"]
    pairs = {(r["from"], r["to"]): r["value"] for r in school["relationships"]}
    for source in people:
        native = (original["roles"][str(source)]["relationships"] if source in original["roster"]
                  else original["teacher_relationships"][str(source)])
        for target in people:
            if source != target:
                index = target - 55 if target in original["teachers"] else target
                yield f"relationship[{source},{target}]", native[index], pairs.get((source, target))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("before", "after", "remake"):
        parser.add_argument(arg, type=Path)
    parser.add_argument("--before-sha256", required=True)
    parser.add_argument("--after-sha256", required=True)
    args = parser.parse_args()
    raw = args.before.read_bytes()
    before = snapshot(raw, args.before_sha256)
    after = snapshot(args.after.read_bytes(), args.after_sha256)
    compare(before, after, require_44=True)
    party = adventure44_party(raw, before)
    remake = json.loads(args.remake.read_bytes())
    count = 0
    for field, original, projected in differences(after, remake, before, party):
        count += 1
        if original != projected:
            if isinstance(original, list) and isinstance(projected, list) and len(original) == len(projected):
                index = next(i for i in range(len(original)) if original[i] != projected[i])
                field, original, projected = f"{field}[{index}]", original[index], projected[index]
            print(json.dumps({"checkpoint": "school_return", "field": field, "original": original, "remake": projected}))
            return 1
    print(json.dumps({"checkpoint": "school_return", "fields_checked": count, "first_difference": None}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
