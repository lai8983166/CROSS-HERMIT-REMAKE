"""Original static font factory/cache stores and explicit cache-state experiments."""
import hashlib
import json
import pickle
import struct
from functools import lru_cache

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_owner_startup import SOURCE, SOURCE_SHA256, BASE, ROOT, dword, store, u32

HEAD = 0x80A398
COUNTER = 0x79FC74
FONT = 0x23001000
CACHE = 0x23005000
RANGES = {0x52AE11: 0x52AE80, 0x428A40: 0x428AC6,
          0x53BB9E: 0x53BBB9, 0x53B9F8: 0x53BA56,
          0x548D89: 0x548DFE, 0x5483B1: 0x5483FC,
          0x548735: 0x548876, 0x54864C: 0x548706}
ARGS = {0x52AE11: 3, 0x428A40: 1, 0x53B9F8: 2,
        0x548D89: 2, 0x548735: 1}
STOPS = dict(inherited=0x548D95, empty=0x52755E)
CHECKPOINT = '.venv-audit/vm-graphics-owner_read-initial.pkl'
CHECKPOINT_SHA = 'e34231d77ed31137288766ef2c5479e98fdac6cce7e2163bdde21b745266a5c4'


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('font startup fixed original source')
    head = dword(raw, HEAD-BASE)
    if head != 0x4D61D08:
        raise ValueError('font startup inherited nonempty cache')
    checkpoint = (ROOT/CHECKPOINT).read_bytes()
    if hashlib.sha256(checkpoint).hexdigest() != CHECKPOINT_SHA:
        raise ValueError('font startup private checkpoint identity before unpickle')
    captured = pickle.loads(checkpoint)
    if captured['source_sha'] != SOURCE_SHA256 or captured['pending_eip'] != 0x40E2D0:
        raise ValueError('font startup captured source/VM identity')
    if any(a <= head < a+len(data) for a, data in captured['memory']):
        raise ValueError('font startup missing-node scope changed')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    checks = {0x52AE2A: ('push', '0x50'), 0x52AE38: ('call', '0x53bb9e'),
              0x52AE56: ('call', '0x53b9f8'), 0x53BA10: ('call', '0x548d89'),
              0x548D89: ('mov', 'eax, dword ptr [0x80a398]'),
              0x548D95: ('cmp', 'dword ptr [eax + 4], edi'),
              0x548DA5: ('push', '0xb0'), 0x548DB6: ('call', '0x5483b1'),
              0x548DDB: ('call', '0x548735'),
              0x54874F: ('mov', 'dword ptr [0x80a398], esi'),
              0x54875B: ('call', 'dword ptr [ecx + 4]'),
              0x54876B: ('call', 'dword ptr [ecx + 0x1c]'),
              0x548778: ('call', 'dword ptr [ecx + 0x24]'),
              0x5487A0: ('call', '0x54864c'), 0x5486A4: ('call', '0x52755e')}
    proof = []
    for va, pair in checks.items():
        ins = next(md.disasm(raw[va-BASE:va-BASE+16], va))
        if (ins.mnemonic, ins.op_str) != pair:
            raise ValueError('font startup original instruction '+hex(va))
        proof.append(dict(va=hex(va), hex=ins.bytes.hex(), mnemonic=ins.mnemonic, operands=ins.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,
                functions=[dict(va=hex(a), end=hex(b), sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest())
                           for a, b in RANGES.items()], instructions=proof,
                inherited_head=head, missing_target=head+4,
                checkpoint=dict(path=CHECKPOINT, sha256=CHECKPOINT_SHA,
                                pending_eip='0x40e2d0', cache_head_target_mapped=False),
                allocation_sizes=[80, 176], CRT_boundary='0x56e810',
                texture_entry='0x52755e', retained_VM_advanced=False,
                empty_cache_is_declared_experiment=True)


def font_constructor(before):
    if len(before) != 80:
        raise ValueError('font full80-byte object')
    result = bytearray(before)
    for at, value in {0: 0x5D1154, 4: 1, 8: 0, 72: 0, 76: 0}.items():
        store(result, at, value)
    return bytes(result)


def cache_constructor(before):
    if len(before) != 176:
        raise ValueError('font full176-byte cache')
    result = bytearray(before)
    for at in (0, 4, 8, 12, *range(16, 80, 4), 0x60, 0x64, 0x68, 0x98, 0x9C, 0xA8, 0x6C, 0xAC):
        store(result, at, 1 if at == 0 else 0)
    return bytes(result)


def cache_prefix(before, device, caps):
    if len(caps) != 212:
        raise ValueError('font cache complete actual D3DCAPS8')
    result = bytearray(cache_constructor(before))
    for at, value in {4: device, 0xAC: 0, 0x50: dword(caps, 12) & 0x20000000,
                      0x58: 64, 0x5C: 16, 0x54: 21}.items():
        store(result, at, value)
    return bytes(result)


def texture_arguments(device, caps):
    if len(caps) != 212:
        raise ValueError('font texture complete caps')
    dynamic = bool(dword(caps, 12) & 0x20000000)
    return [device, CACHE+0x58, CACHE+0x5C, 0, 0x200 if dynamic else 0,
            CACHE+0x54, 0 if dynamic else 1]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT/args.out
    if path.exists():
        parser.error('fresh immutable report required')
    path.write_text(json.dumps(source_contract(), indent=2)+'\n', encoding='utf-8', newline='\n')
