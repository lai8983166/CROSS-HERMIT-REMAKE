"""Source-derived95-character atlas layout and complete16-bit pixel conversion."""
import hashlib
import json
import struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_font_atlas import ROOT, SOURCE, SOURCE_SHA256, BASE, SLOT, SIZE, dword

RANGES = {0x40144D: 0x4017B6, 0x56CE80: 0x56CE83}
IMPORTS = {0x401497: (0x5920BC, 'GetTextExtentPoint32A', 4, 'glyph_measure'),
           0x401502: (0x5920C0, 'ExtTextOutA', 8, 'glyph_draw')}


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256: raise ValueError('glyph source SHA')
    md, proof = Cs(CS_ARCH_X86, CS_MODE_32), []
    checks = {0x401463: ('cmp', 'edx, 0x7f'), 0x401491: ('call', 'dword ptr [0x5920bc]'),
        0x4014B4: ('jbe', '0x4014d6'), 0x4014CC: ('lea', 'ecx, [eax + edx + 1]'),
        0x4014FC: ('call', 'dword ptr [0x5920c0]'), 0x401551: ('fstp', 'dword ptr [ecx + eax + 0x70]'),
        0x401597: ('shl', 'edx, 4'), 0x401641: ('fstp', 'dword ptr [ecx + eax + 0x7c]'),
        0x40167E: ('call', 'dword ptr [edx + 0x40]'), 0x401713: ('mov', 'edx, dword ptr [ecx + eax*4]'),
        0x40171C: ('shr', 'edx, 4'), 0x401743: ('or', 'ecx, 0xfff'),
        0x40174F: ('mov', 'word ptr [edx], cx'), 0x401769: ('mov', 'word ptr [ecx], 0'),
        0x401788: ('add', 'eax, dword ptr [ebp - 0x148]'), 0x4017AC: ('call', 'dword ptr [eax + 0x44]')}
    for at, expected in checks.items():
        i = next(md.disasm(raw[at-BASE:at-BASE+16], at))
        if (i.mnemonic, i.op_str) != expected: raise ValueError('glyph source '+hex(at))
        proof.append(dict(va=hex(at), hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
    desc = struct.unpack_from('<5I', raw, 0x5FD5F4-BASE); imports = []
    for ret, (slot, name, count, op) in IMPORTS.items():
        thunk = dword(raw, desc[0]+4*((slot-BASE-desc[4])//4))
        if raw[thunk+2:].split(b'\0', 1)[0] != name.encode('ascii'): raise ValueError('glyph import '+name)
        imports.append(dict(slot=hex(slot), target=hex(dword(raw, slot-BASE)), symbol=name, return_va=hex(ret), args=count, op=op))
    return dict(source_image_sha256=SOURCE_SHA256, functions=[dict(va=hex(a), end=hex(b),
        sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a, b in RANGES.items()], instructions=proof,
        imports=imports, characters=list(range(32,127)), atlas=[256,256], UV_offset=112, UV_bytes=1520,
        raster_stop='0x401660', upload_stop='0x4017b6', lock_method=64, lock_return='0x401681',
        unlock_method=68, unlock_return='0x4017af', pixel_count=65536,
        pixel_rule='alpha=blue>>4; word=0 if alpha==0 else (alpha<<12)|0xfff',
        original_cleanup_executed=False, retained_VM_advanced=False)


def layout(measures):
    if len(measures) != 95: raise ValueError('glyph exact95 dimensions')
    x = y = 0; rows = []
    for ch, (w, h) in zip(range(32,127), measures):
        if not 0 < w <= 256 or not 0 < h <= 256: raise ValueError('glyph bounded actual dimensions')
        if x+w+1 > 256: x, y = 0, y+h+1
        rows.append(dict(character=ch, x=x, y=y, width=w, height=h))
        x += w+1
    return rows, (x, y)


def glyph_object(before, measures):
    if len(before) != SIZE: raise ValueError('glyph full slot required')
    after = bytearray(before); rows, _ = layout(measures)
    for n, r in enumerate(rows):
        struct.pack_into('<4f', after, 112+n*16, r['x']/256, r['y']/256,
                         (r['x']+r['width'])/256, (r['y']+r['height'])/256)
    return bytes(after)


def pixels(dib, before, pitch):
    if len(dib) != 262144 or not 512 <= pitch <= 4096 or len(before) != pitch*256:
        raise ValueError('glyph complete DIB/actual pitch/locked buffer required')
    after = bytearray(before)
    for y in range(256):
        for x in range(256):
            alpha = dib[(y*256+x)*4] >> 4
            struct.pack_into('<H', after, y*pitch+x*2, (alpha<<12)|0xFFF if alpha else 0)
    return bytes(after)


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable glyph source report required')
    path.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf-8',newline='\n')
