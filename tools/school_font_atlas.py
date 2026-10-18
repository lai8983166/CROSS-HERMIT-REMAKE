"""Original additional atlas texture and GDI setup to first glyph measurement."""
import hashlib
import json
import struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_font_slots import SOURCE, SOURCE_SHA256, BASE, ROOT, SLOT, SIZE, dword, store

RANGES = {0x40120C: 0x401497, 0x56CE80: 0x56CE83, 0x56CEC0: 0x56CF18,
          0x56CFCC: 0x56CFF3}
IMPORTS = [(0x592094, 'CreateCompatibleDC', 0x401284, 1, 'atlas_dc'),
           (0x592098, 'CreateDIBSection', 0x4012B4, 6, 'atlas_dib'),
           (0x59209C, 'SetMapMode', 0x4012D2, 2, 'atlas_map'),
           (0x59223C, 'MulDiv', 0x401306, 3, 'atlas_muldiv'),
           (0x5920A0, 'CreateFontA', 0x40137E, 14, 'atlas_font'),
           (0x5920A4, 'SelectObject', 0x4013B4, 2, 'atlas_bitmap_select'),
           (0x5920A4, 'SelectObject', 0x4013D1, 2, 'atlas_font_select'),
           (0x5920B0, 'SetTextColor', 0x4013EC, 2, 'atlas_text'),
           (0x5920B4, 'SetBkColor', 0x401404, 2, 'atlas_background'),
           (0x5920B8, 'SetTextAlign', 0x40141C, 2, 'atlas_align')]
FONT_ARGS = [-16, 0, 0, 0, 700, 0, 0, 0, 1, 0, 0, 4, 2]


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('font atlas original image SHA')
    md, proof = Cs(CS_ARCH_X86, CS_MODE_32), []
    checks = {0x40120C: ('call', 'dword ptr [edx + 0x50]'),
              0x401232: ('call', '0x56cec0'), 0x40123A: ('mov', 'dword ptr [ebp - 0x10c], 0x28'),
              0x401258: ('mov', 'dword ptr [ebp - 0x104], ecx'),
              0x4012F3: ('call', '0x56cfcc'), 0x40130D: ('neg', 'eax'),
              0x401322: ('and', 'ecx, 0x12c'), 0x401328: ('add', 'ecx, 0x190'),
              0x401378: ('call', 'dword ptr [0x5920a0]'),
              0x401444: ('mov', 'byte ptr [ebp - 0x140], 0x20'),
              0x401491: ('call', 'dword ptr [0x5920bc]')}
    for at, expected in checks.items():
        i = next(md.disasm(raw[at-BASE:at-BASE+16], at))
        if (i.mnemonic, i.op_str) != expected: raise ValueError('font atlas source '+hex(at))
        proof.append(dict(va=hex(at), hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
    imports = []
    for slot, name, ret, count, op in [*IMPORTS, (0x5920BC, 'GetTextExtentPoint32A', 0x401497, 4, 'pending_glyph')]:
        for at in (0x5FD5CC, 0x5FD5E0, 0x5FD5F4):
            desc = struct.unpack_from('<5I', raw, at-BASE)
            index = (slot-BASE-desc[4])//4
            if index < 0 or not 0 <= desc[0]+4*index < len(raw)-4: continue
            thunk = dword(raw, desc[0]+4*index)
            if thunk >= len(raw)-2: continue
            if raw[thunk+2:].split(b'\0', 1)[0] == name.encode('ascii'):
                imports.append(dict(slot=hex(slot), target=hex(dword(raw, slot-BASE)), symbol=name,
                    return_va=hex(ret), args=count, op=op, descriptor=hex(at),
                    dll=raw[desc[3]:].split(b'\0', 1)[0].decode('ascii')))
                break
        else: raise ValueError('font atlas original import '+name)
    return dict(source_image_sha256=SOURCE_SHA256,
        functions=[dict(va=hex(a), end=hex(b), sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a, b in RANGES.items()],
        instructions=proof, imports=imports, texture_args=[256, 256, 1, 0, 26, 1],
        bitmap_header_hex=bitmap_header().hex(), font_args=FONT_ARGS, face_hex='4669786564537973',
        texture_stop=hex(dword(raw, 0x592094-BASE)), GDI_stop='0x401491', first_character=32,
        first_character_source_word=raw[0x5924BC-BASE:0x5924BC-BASE+2].hex(),
        glyph_measurement_executed=False, retained_VM_advanced=False)


def bitmap_header():
    return struct.pack('<IiiHH6I', 40, 256, -256, 1, 32, 0, 0, 0, 0, 0, 0)


def font_logfont():
    return struct.pack('<5i8B32s', *FONT_ARGS, b'FixedSys')


def texture_object(before, pointer):
    if len(before) != SIZE or not 0 < pointer <= 0xFFFFFFFF:
        raise ValueError('font atlas full object and actual texture required')
    after = bytearray(before)
    store(after, 0x5C, pointer)
    return bytes(after)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', required=True)
    a = p.parse_args(); path = ROOT/a.out
    if path.exists(): p.error('fresh immutable atlas source report required')
    path.write_text(json.dumps(source_contract(), indent=2)+'\n', encoding='utf-8', newline='\n')
