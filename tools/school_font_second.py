"""Second original font-slot source and bounded constructor/atlas projections."""
import argparse
import hashlib
import json
from functools import lru_cache
from tools.school_font_slots import (SOURCE, SOURCE_SHA256, BASE, ROOT, SIZE,
    constructor as slot_constructor, atlas as slot_atlas, source_contract as slot_source,
    RANGES as SLOT_RANGES, Cs, CS_ARCH_X86, CS_MODE_32)

SECOND = 0x23011000
RANGES = dict(SLOT_RANGES)
RANGES[0x416021] = 0x416133
PHASES = {'loop': (0x416101, 0x41603D),
          'constructor': (0x41603D, 0x4010D0),
          'atlas': (0x4010D0, 0x40120C)}
LOOP_TRACE = [0x416101, 0x416104, 0x416108, 0x416111,
              0x41602A, 0x41602D, 0x416030, 0x416033, 0x416037]


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('second font source image SHA')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    checks = {0x416101: ('mov', 'dword ptr [ebp - 0x14], eax'),
              0x416104: ('cmp', 'dword ptr [ebp - 0x14], 0'),
              0x416108: ('jge', '0x416111'), 0x416111: ('jmp', '0x41602a'),
              0x41602A: ('mov', 'ecx, dword ptr [ebp - 0x18]'),
              0x41602D: ('add', 'ecx, 1'),
              0x416030: ('mov', 'dword ptr [ebp - 0x18], ecx'),
              0x416033: ('cmp', 'dword ptr [ebp - 0x18], 2'),
              0x416037: ('je', '0x416116'),
              0x41603D: ('push', '0x678'),
              0x4160A5: ('mov', 'dword ptr [ecx + eax*4 + 0x1090], edx'),
              0x416116: ('xor', 'eax, eax'),
              0x416118: ('mov', 'ecx, dword ptr [ebp - 0xc]'),
              0x41611B: ('mov', 'dword ptr fs:[0], ecx'),
              0x41612A: ('call', '0x56ce80'), 0x416132: ('ret', '')}
    proof = []
    for at, expected in checks.items():
        i = next(md.disasm(raw[at-BASE:at-BASE+16], at))
        if (i.mnemonic, i.op_str) != expected:
            raise ValueError('second font original instruction '+hex(at))
        proof.append(dict(va=hex(at), hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256, slot_source=slot_source(),
                instructions=proof, functions=[dict(va=hex(a), end=hex(b),
                    sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
                loop_trace=[hex(a) for a in LOOP_TRACE], index=1,
                declared_second_heap=SECOND, owner_offset=0x1094, allocation_bytes=SIZE,
                total_declared_allocation_counter_delta=3600,
                phases={p: dict(start=hex(a), stop=hex(b)) for p,(a,b) in PHASES.items()},
                return_source=dict(success_index=2, success_result=0, SEH_restore='0x41611b',
                                   ret='0x416132', executed=False),
                second_texture_created=False, full415F50_returned=False, retained_VM_advanced=False)


def constructor(before):
    return slot_constructor(before, index=1)


def atlas(before, device, max_width):
    return slot_atlas(before, device, max_width)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable second font source required')
    path.write_text(json.dumps(source_contract(), indent=2)+'\n', encoding='utf8', newline='\n')
