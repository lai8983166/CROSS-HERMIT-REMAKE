"""Original sprite stores and complete first static font return projections."""
import hashlib
import json
import struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_font_startup import SOURCE, SOURCE_SHA256, BASE, ROOT, FONT, CACHE, HEAD, COUNTER, dword, store

SPRITE = 0x23009000
RANGES = {0x52AE80: 0x52AEEC, 0x53C665: 0x53C683, 0x53BC06: 0x53BC7B,
          0x428A40: 0x428AC6, 0x56CE80: 0x56CE83, 0x548735: 0x548876,
          0x548D89: 0x548DFE, 0x53B9F8: 0x53BA56, 0x52AE11: 0x52AE80,
          0x52AFE6: 0x52B019, 0x4162C0: 0x416317, 0x415F50: 0x416133}
ARGS = {0x52AE80: 2, 0x428A40: 1, 0x53BC06: 1, 0x548735: 1, 0x548D89: 2,
        0x53B9F8: 2, 0x52AE11: 3, 0x52AFE6: 3, 0x4162C0: 1}
IMPORTS = {0x592094: ('CreateCompatibleDC', 0x548805, 1),
           0x592098: ('CreateDIBSection', 0x548828, 6),
           0x59208C: ('SetBkMode', 0x548840, 2),
           0x5920B4: ('SetBkColor', 0x54884A, 2),
           0x5920B0: ('SetTextColor', 0x548858, 2),
           0x5920A4: ('SelectObject', 0x548867, 2),
           0x5920AC: ('CreateFontIndirectA', 0x53BA25, 1)}


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('cache sprite original source SHA')
    md, proof = Cs(CS_ARCH_X86, CS_MODE_32), []
    checks = {0x52AEA0: ('push', '0x20'), 0x52AEAE: ('call', '0x53c665'),
              0x52AECA: ('call', '0x53bc06'),
              0x53BC28: ('call', 'dword ptr [ecx + 4]'),
              0x53BC35: ('call', 'dword ptr [ecx + 0x1c]'),
              0x53BC42: ('call', 'dword ptr [ecx + 0x24]'),
              0x52AEE2: ('mov', 'dword ptr [ebx], esi'),
              0x5487CD: ('rep stosd', 'dword ptr es:[edi], eax'),
              0x548813: ('neg', 'dword ptr [esi + 0x78]'),
              0x548832: ('neg', 'dword ptr [esi + 0x78]'),
              0x548DF7: ('mov', 'dword ptr [eax], esi'),
              0x53BA39: ('call', 'dword ptr [eax + 4]'),
              0x53BA46: ('rep movsd', 'dword ptr es:[edi], dword ptr [esi]'),
              0x52AE6E: ('mov', 'dword ptr [ebx], esi'),
              0x416005: ('mov', 'dword ptr [edx + 0xb270], eax')}
    for at, expected in checks.items():
        ins = next(md.disasm(raw[at-BASE:at-BASE+16], at))
        if (ins.mnemonic, ins.op_str) != expected:
            raise ValueError('cache source instruction '+hex(at))
        proof.append(dict(va=hex(at), hex=ins.bytes.hex(), mnemonic=ins.mnemonic, operands=ins.op_str))
    descriptor = struct.unpack_from('<5I', raw, 0x5FD5F4-BASE)
    imports = []
    for slot, (name, ret, count) in IMPORTS.items():
        thunk = dword(raw, descriptor[0]+4*((slot-BASE-descriptor[4])//4))
        if raw[thunk+2:].split(b'\0', 1)[0] != name.encode('ascii'):
            raise ValueError('cache original GDI import '+name)
        imports.append(dict(slot=hex(slot), target=hex(dword(raw, slot-BASE)), symbol=name,
                            return_va=hex(ret), args=count, dll='GDI32.dll'))
    return dict(source_image_sha256=SOURCE_SHA256,
                functions=[dict(va=hex(a), end=hex(b), sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest())
                           for a, b in RANGES.items()], instructions=proof, imports=imports,
                CRT_size=32, explicit_empty_cache_experiment=True, retained_VM_advanced=False,
                sprite_stop=hex(dword(raw, 0x592094-BASE)), first_font_stop='0x416021',
                state_blocks_created=False)


def sprite(before, device, caps, creation):
    if len(before) != 32 or len(caps) != 212 or len(creation) != 16 or not device:
        raise ValueError('sprite full object and actual device buffers')
    values = [0x5D1180, 1, device, 0, 0, 0,
              int(bool(caps[44] & 16 and caps[48] & 32)),
              int(bool(caps[33] & 2 or creation[12] & 16))]
    return struct.pack('<8I', *values)


def bitmap_header(top_down=False):
    return struct.pack('<IiiHH6I', 40, 256, -256 if top_down else 256, 1, 32, 0, 0, 0, 0, 0, 0)


def cache_before_gdi(before):
    if len(before) != 176:
        raise ValueError('cache complete object')
    after = bytearray(before)
    store(after, 12, SPRITE)
    after[0x70:0x98] = bitmap_header()
    store(after, 0xA4, 21)
    return bytes(after)


def cache_after_gdi(before, dc, bitmap, old_bitmap, bits):
    if not all((dc, bitmap, old_bitmap, bits)):
        raise ValueError('cache actual owned GDI handles/bits required')
    after = bytearray(cache_before_gdi(before))
    for at, value in {0x6C: dc, 0x98: bitmap, 0x9C: old_bitmap, 0xA0: bits}.items():
        store(after, at, value)
    return bytes(after)


def font_complete(device, font_handle, logfont):
    if not device or not font_handle or len(logfont) != 60:
        raise ValueError('font actual handles and complete LOGFONT')
    return struct.pack('<3I', 0x5D1154, 1, font_handle)+logfont+struct.pack('<2I', CACHE, device)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable source report required')
    path.write_text(json.dumps(source_contract(), indent=2)+'\n', encoding='utf-8', newline='\n')
