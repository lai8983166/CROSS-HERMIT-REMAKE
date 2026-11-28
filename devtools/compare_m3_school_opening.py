"""Check the imported starting school against independently decoded v7 bytes."""
import argparse
import json
from pathlib import Path
import struct

from devtools.compare_m3_native_saves import STATE, snapshot
from devtools.compare_m3_school_return import member_fields


def fields(raw, original, remake):
    def read(va, fmt):
        return list(struct.unpack_from("<"+fmt, raw, va-STATE))

    yield "source_sha256", original["sha256"], remake["origin_sha"]
    yield "school.date", original["date"], [remake["school"]["month"],remake["school"]["week"]]
    yield "school.score", original["global_score"], remake["score"]
    yield "mission.grades", read(0x7a54cb,"100B"), remake["grades"]
    yield "mission.unlock_flags", read(0x7a55fd,"100B"), remake["ledger"]["unlock_flags"]
    yield "school.availability", read(0x7a5120,"45B"), remake["availability"]
    if original["date"]==[13,2]:
        work = [read(va,"h")[0] for va in (0x7aab10,0x7aab12,0x7aab16,0x7aab14)]
        yield "school.lecture_work_fields", work, remake["lecture_work_fields"]
    classes = []
    for index, group in enumerate(original["groups"]):
        if group["teacher"]>=0:
            classes.append({"group":index, "teacher":group["teacher"],
                            "students":[role for role in group["student_slots"] if role>=0],
                            "activity":2 if group["activity"]==0 else 1,
                            "work_fields":read(0x7aaa18+28*index,"4h")})
    yield "school.classes", classes, remake["classes"]
    count, = read(0x7a5b62,"h")
    if not 0<=count<=80:
        raise ValueError("Invalid original adventure count")
    yield "mission.count", count, len(remake["ledger"]["entries"])
    for index in range(count):
        va = 0x7a5662+16*index
        entry = dict(zip(("limit","duration","busy_elapsed","elapsed"),read(va+8,"4h"),strict=True))
        entry.update(id=read(va,"h")[0],metadata=read(va+3,"3B"),busy=read(va+6,"B")[0])
        yield f"mission.entries[{index}]", entry, remake["ledger"]["entries"][index]
    yield from member_fields(original, remake, include_staged=original["date"][0]==13)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save",type=Path)
    parser.add_argument("sha256")
    parser.add_argument("report",type=Path)
    args=parser.parse_args()
    raw=args.save.read_bytes()
    original=snapshot(raw,args.sha256)
    remake=json.loads(args.report.read_bytes())
    count=0
    for name, expected, actual in fields(raw,original,remake):
        count+=1
        if expected!=actual:
            print(json.dumps({"field":name,"original":expected,"remake":actual}))
            return 1
    print(json.dumps({"date":original["date"],"fields_checked":count,"first_difference":None}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
