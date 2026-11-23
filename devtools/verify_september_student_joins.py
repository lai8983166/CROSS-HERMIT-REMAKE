"""Compare the two sourced opcode-144 prefixes against the played join snapshots."""
import argparse
import json
import struct
from pathlib import Path

from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.roster_join_emulation import RosterJoinEmulator
from tools.scene5_script_emulation import SCRIPT, VM
from tools.school_postbattle_story_export import GAME, SOURCE


def verify(cases):
    assert [(c["chapter"], [r["character_id"] for r in c["new_students"]]) for c in cases] == [
        (54, [14, 15]), (56, [11])]
    counts = []
    image = SOURCE.read_bytes()
    for case in cases:
        cpu = RosterJoinEmulator()
        school = case["initial_ids"]
        teachers = case["teacher_ids"]
        cpu.write(0x7a528c, case["difficulty"], "h")
        cpu.write(0x7a528e, case["date"][0], "h")
        cpu.write(0x7a5290, case["date"][1], "h")
        cpu.write(0x7a5260, len(school), "h")
        cpu.write(0x7a528a, len(teachers), "h")
        for n in range(121):
            cpu.write(0x7a5120+n, int(n in school or n in teachers), "B")
        for n in range(20):
            cpu.write(0x7a5210+2*n, school[n] if n < len(school) else -1, "h")
            cpu.write(0x7a5262+2*n, teachers[n] if n < len(teachers) else -1, "h")
        for n, value in enumerate(case["initial_items"], 1):
            cpu.write(0x7aacaa+2*n, value, "H")
        cpu.source = (GAME / f"DAT/CHAPTER{case['chapter']:03}.YBC").read_bytes()
        cpu.uc.mem_write(SCRIPT, cpu.source)
        cpu.write(VM+0xc, SCRIPT)
        cpu.call(0x4ce560, (0, 7), receiver=VM)
        for student, record in zip(case["new_students"], case["records"], strict=True):
            n = student["character_id"]
            b = CHAR_BASE+n*CHAR_STRIDE
            p = PACKAGE_BASE+n*PACKAGE_STRIDE
            cpu.uc.mem_write(b, bytes(cpu.uc.mem_read(0x6f5088+n*CHAR_STRIDE, CHAR_STRIDE)))
            cpu.uc.mem_write(p, bytes(PACKAGE_STRIDE))
            progress = [0]+[max(0,min(100,x)) for x in struct.unpack_from("<32h",image,0x351242+n*0x42)]
            assert record["job_progress"] == progress and record["week_records"] == [0]*177
            cpu.uc.mem_write(p+0xd7, bytes(progress))
            cpu.call_join_step()
            assert cpu.join_entries[-1]["character_id"] == n
            assert [cpu.join_entries[-1][key] for key in ("group","slot")] == [-1,-1]
            for key, addr, stride, fmt in [
                ("attributes", b+0xc, 8, "B"), ("growth_pools", b+0x10, 8, "I"),
                ("equipped_items", b+0x62, 2, "h"), ("equipped_skills", b+0x52, 2, "h"),
                ("skill_statuses", b+0xb8, 12, "B"), ("unlock_flags", p+0xf9, 1, "B")]:
                actual = [cpu.read(addr+k*stride, fmt) for k in range(len(student[key]))]
                if actual != student[key]:
                    raise ValueError(f"chapter {case['chapter']}, member {n}, {key}: {actual} != {student[key]}")
            assert cpu.read(b+0x50,"B") == student["level_50"]
        ids = school+[row["character_id"] for row in case["new_students"]]
        assert [cpu.read(0x7a5210+2*k, "h") for k in range(cpu.read(0x7a5260,"h"))] == ids
        assert [cpu.read(0x7aacaa+2*n, "H") for n in range(1,361)] == case["items"]
        counts.append({"chapter":case["chapter"],"opcodes":[[r["offset"],r["opcode"]] for r in cpu.commands],
                       "joined":[r["character_id"] for r in cpu.join_entries],"result_count":len(ids)})
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.capture.read_bytes())["joins"])))
