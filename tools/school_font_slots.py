"""Source-derived additional font objects and atlas admission, not completed fonts."""
import hashlib
import json
import struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_font_cache import SOURCE, SOURCE_SHA256, BASE, ROOT, dword, store

SLOT = 0x2300D000
SIZE = 0x678
RANGES = {0x416021: 0x4160DF, 0x428A40: 0x428AC6, 0x401000: 0x40108D,
          0x56CD90: 0x56CD97, 0x56CE01: 0x56CE80, 0x56CE80: 0x56CE83,
          0x4010D0: 0x40120F}
ARGS = {0x428A40: 1, 0x401000: 3, 0x56CD90: 2, 0x4010D0: 1}


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('font slots original image SHA')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    checks = {0x41603D: ('push', '0x678'), 0x416042: ('call', '0x428a40'),
              0x41605D: ('mov', 'eax, dword ptr [edx*4 + 0x5ff520]'),
              0x416068: ('mov', 'edx, dword ptr [ecx*4 + 0x5ff508]'),
              0x416073: ('mov', 'ecx, dword ptr [eax*4 + 0x5ff528]'),
              0x41607E: ('call', '0x401000'),
              0x4160A5: ('mov', 'dword ptr [ecx + eax*4 + 0x1090], edx'),
              0x4160DA: ('call', '0x4010d0'), 0x401025: ('call', '0x56cd90'),
              0x401033: ('mov', 'dword ptr [edx + 0x50], eax'),
              0x40103C: ('mov', 'dword ptr [ecx + 0x54], edx'),
              0x40108A: ('ret', '0xc'), 0x401170: ('call', 'dword ptr [edx + 0x1c]'),
              0x401180: ('cmp', 'ecx, dword ptr [ebp - 0x84]'),
              0x4011E9: ('push', '0x1a'), 0x40120C: ('call', 'dword ptr [edx + 0x50]')}
    proof = []
    for at, expected in checks.items():
        i = next(md.disasm(raw[at-BASE:at-BASE+16], at))
        if (i.mnemonic, i.op_str) != expected:
            raise ValueError('font slots instruction '+hex(at))
        proof.append(dict(va=hex(at), hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
    slots = []
    for n in range(2):
        face = dword(raw, 0x5FF528-BASE+4*n)
        name = raw[face-BASE:].split(b'\0', 1)[0]
        slots.append(dict(index=n, face_pointer=face, face_hex=name.hex(),
                          size=dword(raw, 0x5FF508-BASE+4*n), flags=dword(raw, 0x5FF520-BASE+4*n)))
    if [(s['face_hex'], s['size'], s['flags']) for s in slots] != [('4669786564537973', 12, 1), ('b2d3a9fac5e920', 8, 0)]:
        raise ValueError('font slots original fixed input tables')
    return dict(source_image_sha256=SOURCE_SHA256, slots=slots, allocation_bytes=SIZE,
                functions=[dict(va=hex(a), end=hex(b), sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest())
                           for a, b in RANGES.items()], instructions=proof,
                constructor_stop='0x4010d0', atlas_stop='0x40120c',
                caps_method_offset=28, texture_method_offset=80,
                texture_parameters=dict(levels=1, usage=0, format=26, pool=1, output_offset=0x5C),
                retained_VM_advanced=False, additional_fonts_completed=False)


def constructor(before, index=0):
    if len(before) != SIZE or index not in (0, 1):
        raise ValueError('font slots full object and original slot index')
    slot = source_contract()['slots'][index]
    after = bytearray(before)
    name = bytes.fromhex(slot['face_hex'])+b'\0'
    after[:len(name)] = name
    for at, value in {0x50: slot['size'], 0x54: slot['flags'], 0x58: 0, 0x5C: 0,
                      0x60: 0, 0x670: 0, 0x674: 0}.items():
        store(after, at, value)
    return bytes(after)


def atlas(before, device, max_width):
    if len(before) != SIZE or not 0 < device <= 0xFFFFFFFF or not 0 < max_width <= 0xFFFFFFFF:
        raise ValueError('font slots original object and live caps prerequisite')
    after = bytearray(before)
    size = dword(before, 0x50)
    dimension = 1024 if size > 40 else 512 if size > 20 else 256
    scale = min(max_width / dimension, 1.0)
    dimension = min(dimension, max_width)
    for at, value in {0x58: device, 0x64: dimension, 0x68: dimension}.items():
        store(after, at, value)
    after[0x6C:0x70] = struct.pack('<f', scale)
    return bytes(after)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable font slots report required')
    path.write_text(json.dumps(source_contract(), indent=2)+'\n', encoding='utf-8', newline='\n')
