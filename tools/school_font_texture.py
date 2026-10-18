"""Original font-cache texture requirements and bounded creation source contract."""
import hashlib
import json
import struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_font_startup import SOURCE, SOURCE_SHA256, BASE, ROOT, CACHE, FONT, HEAD, COUNTER, dword, store

RANGES = {0x52755E: 0x527584, 0x527234: 0x52755E, 0x526C46: 0x526C6A,
          0x526C6A: 0x526CDF, 0x526D4D: 0x526E2F, 0x52B019: 0x52B0A9,
          0x5275D7: 0x52763D}
ARGS = {0x52755E: 7, 0x527234: 8, 0x526C46: 1, 0x526D4D: 5,
        0x52B019: 1, 0x5275D7: 8}
STOPS = dict(requirements=0x5275D7, texture=0x52AE80)
DEBUG_GLOBAL = 0x8097A8
DEBUG_TARGET = 0x55F0E830


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('texture original source SHA')
    if dword(raw, DEBUG_GLOBAL-BASE) != DEBUG_TARGET or dword(raw, 0x8097A4-BASE) != 0:
        raise ValueError('texture inherited debug-export fast path')
    end = dword(raw, 0x75DDA4-BASE)
    if end != 0x5D09D4 or (end-0x5D03C8) % 36:
        raise ValueError('texture complete format table boundary')
    formats = [dict(pointer=a, fields=list(struct.unpack_from('<9I', raw, a-BASE)))
               for a in range(0x5D03C8, end, 36)]
    checks = {0x52757A: ('call', '0x527234'), 0x5272A4: ('call', '0x526d4d'),
              0x526D73: ('call', 'dword ptr [eax + 0x18]'),
              0x526D80: ('call', 'dword ptr [eax + 0x1c]'),
              0x526D8A: ('call', 'dword ptr [eax + 0x20]'),
              0x526DCC: ('call', 'dword ptr [edx + 0x28]'),
              0x526E19: ('call', 'dword ptr [ecx + 8]'),
              0x52736A: ('call', 'dword ptr [eax + 0x1c]'),
              0x52760F: ('call', '0x52755e'),
              0x52762E: ('call', 'dword ptr [eax + 0x50]'),
              0x5486E9: ('call', 'dword ptr [edx + 0x3c]'),
              0x5487B4: ('call', '0x52ae80')}
    md, proof = Cs(CS_ARCH_X86, CS_MODE_32), []
    for at, expected in checks.items():
        ins = next(md.disasm(raw[at-BASE:at-BASE+16], at))
        if (ins.mnemonic, ins.op_str) != expected:
            raise ValueError('texture original instruction '+hex(at))
        proof.append(dict(va=hex(at), hex=ins.bytes.hex(), mnemonic=ins.mnemonic, operands=ins.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,
                functions=[dict(va=hex(a), end=hex(b), sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest())
                           for a, b in RANGES.items()], instructions=proof, formats=formats,
                format_table_sha256=hashlib.sha256(raw[0x5D03C8-BASE:end-BASE]).hexdigest(),
                debug_global=DEBUG_GLOBAL, inherited_debug_target=DEBUG_TARGET, debug_arguments=[1, 0],
                explicit_empty_cache_experiment=True, retained_VM_advanced=False,
                requirements_stop=hex(STOPS['requirements']), sprite_stop=hex(STOPS['texture']))


def requirements(width, height, levels, caps):
    """Declared 2D format21 inputs; source size/mipmap path, with no synthetic COM result."""
    if len(caps) != 212 or min(width, height) < 0 or levels < 0:
        raise ValueError('texture bounded complete caps and unsigned dimensions')
    w = min(max(1, width), dword(caps, 88))
    h = min(max(1, height), dword(caps, 92))
    texture_caps = dword(caps, 60)
    aspect = 1 if texture_caps & 32 else dword(caps, 104)
    if aspect:
        w = min(w, aspect*h)
        h = min(h, aspect*w)
    if texture_caps & 2:
        w = 1 << (max(1, w)-1).bit_length()
        h = 1 << (max(1, h)-1).bit_length()
    full_levels = max(w.bit_length(), h.bit_length(), 1)
    if not texture_caps & 0x4000 or (texture_caps & 0x100 and (w & (w-1) or h & (h-1))):
        mipmaps = 1
    else:
        mipmaps = min(levels, full_levels) if levels else full_levels
    return dict(width=w, height=h, levels=mipmaps, format=21)


def texture_cache(before, texture, surface):
    if len(before) != 176 or not texture or not surface:
        raise ValueError('texture full cache and actual resource identities')
    after = bytearray(before)
    store(after, 0x10, texture)
    store(after, 0x30, surface)
    return bytes(after)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable source report required')
    path.write_text(json.dumps(source_contract(), indent=2)+'\n', encoding='utf-8', newline='\n')
