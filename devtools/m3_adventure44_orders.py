"""Resolve the fixed January action history into original work slots and map cells."""
import argparse
import hashlib
import json
from pathlib import Path


TRACE_SHA = "b759b1f62f2bdcc3db937d52da17649985fb30c3df6835029093befb552f8107"
HANDOFF_SHA = "7364582c5aaf000907a3d82b94d2e59c58db8cea73616881abf2d9e5646d0edb"


def authenticated(path, digest):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError(f"Unexpected January source {path.name}")
    return json.loads(raw)


def orders(trace, party):
    slots = {role: slot for slot, role in enumerate(party["student_ids"])}
    if len(slots) != 19 or party["scene_id"] != 44:
        raise ValueError("Invalid January party")
    result = []
    for seq, (frame, op, *args) in enumerate(trace["commands"], 1):
        row = {"sequence":seq, "remake_frame":frame}
        if op == 1:
            row.update(action="opening", skip=bool(args[0]))
        else:
            student, *operands = args
            row.update(actor_slot=slots[student], actor_role=student)
            if op in (3, 9):
                row.update(action="move" if op == 3 else "field_spell", cell=operands)
                if op == 9:
                    row["spell"] = 31
            elif op in (4, 10, 11):
                target, = operands
                slot = target - 1000 if 1000 <= target < 1250 else slots[target]
                row.update(action="attack" if op == 4 else "aimed_spell", target_slot=slot)
                if op != 4:
                    row["spell"] = 11 if op == 10 else 20
            else:
                raise ValueError(f"Unexpected command {seq}: {op}")
        result.append(row)
    return result


def class_layout(school, party):
    """Identify the exact school UI slots to change without modifying the source save."""
    desired = [[] for _ in party["teacher_ids"]]
    for student, group in zip(party["student_ids"], party["student_groups"], strict=True):
        desired[group].append(student)
    changes = []
    for group, (actual, teacher, target) in enumerate(zip(school["groups"], party["teacher_ids"], desired, strict=True)):
        current = actual["student_slots"][:actual["student_count"]]
        if actual["teacher"]!=teacher or current!=target:
            changes.append({"class":group+1, "teacher_before":actual["teacher"], "teacher_after":teacher,
                            "students_before":current, "students_after":target})
    return {"school_sha256":school["sha256"], "date":school["date"], "classes":changes,
            "missing_students":sorted(set(party["student_ids"])-set(school["roster"])),
            "missing_teachers":sorted(set(party["teacher_ids"])-set(school["teachers"]))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="corrected campaign evidence directory")
    parser.add_argument("--admission", type=Path, help="verified original departure report")
    parser.add_argument("--output", type=Path, help="create a new guest order file")
    parser.add_argument("--inspect-school", type=Path, help="show class changes for this pinned original school save")
    parser.add_argument("--school-sha256")
    args = parser.parse_args()
    if bool(args.inspect_school) != bool(args.school_sha256):
        parser.error("--inspect-school and --school-sha256 must be used together")
    handoff = authenticated(args.source / "formal/handoff-44.json", HANDOFF_SHA)
    party, = handoff["prepared"]["rounds"]
    trace = authenticated(args.source / "trace-44.json", TRACE_SHA)
    result = {"trace_sha256":TRACE_SHA, "party":party, "orders":orders(trace, party)}
    if args.inspect_school:
        from devtools.compare_m3_native_saves import snapshot
        school = snapshot(args.inspect_school.read_bytes(), args.school_sha256)
        print(json.dumps(class_layout(school,party), ensure_ascii=False))
    if args.admission:
        admission = json.loads(args.admission.read_bytes())
        original, = admission["original_prepared"]["rounds"]
        if original != party or admission["before"]["date"] != [13, 2]:
            raise ValueError("Original departure does not match the January order file")
        result["departure_sha256"] = admission["before"]["sha256"]
    if args.output:
        with args.output.open("x", encoding="utf-8") as fp:
            json.dump(result, fp, separators=(",", ":"))
    print(f'{len(result["orders"])} orders across {len(set(r["remake_frame"] for r in result["orders"]))} command frames')


if __name__ == "__main__":
    main()
