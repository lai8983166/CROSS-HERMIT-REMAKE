"""Second original atlas texture and raw ANSI GDI preparation contract."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools.school_font_atlas import (SOURCE,SOURCE_SHA256,BASE,ROOT,SIZE,RANGES,IMPORTS,
    bitmap_header,texture_object,Cs,CS_ARCH_X86,CS_MODE_32,source_contract as atlas_source)
from tools.school_font_second import SECOND,source_contract as second_source

FACE = bytes.fromhex('b2d3a9fac5e920')
FONT_ARGS = [-11,0,0,0,400,0,0,0,1,0,0,4,2]


def font_logfont():
    return struct.pack('<5i8B32s',*FONT_ARGS,FACE)


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:
        raise ValueError('second resource source SHA')
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    checks = {0x4012D9:('mov','dword ptr [ebp - 0x118], 0x60'),
        0x4012F0:('fmul','dword ptr [eax + 0x6c]'),0x4012FC:('mov','edx, dword ptr [ecx + 0x50]'),
        0x40131B:('and','ecx, 1'),0x401322:('and','ecx, 0x12c'),
        0x401328:('add','ecx, 0x190'),0x40133A:('and','eax, 2'),
        0x40134E:('push','ecx'),0x401378:('call','dword ptr [0x5920a0]')}
    proof = []
    for at,expected in checks.items():
        i = next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=expected:
            raise ValueError('second resource source instruction '+hex(at))
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,shared_atlas_source=atlas_source(),
        second_slot_source=second_source(),instructions=proof,second_object=SECOND,
        texture_args=[256,256,1,0,26,1],texture_output=SECOND+0x5C,
        bitmap_header_hex=bitmap_header().hex(),muldiv_args=[8,96,72],
        expected_bounded_actual_muldiv_result=11,font_args=FONT_ARGS,face_hex=FACE.hex(),
        LOGFONT_hex=font_logfont().hex(),GDI_stop='0x401491',first_character=32,
        first_font_resources_must_remain_owned=True,new_DIB_pixels_mapped=False,
        second_glyph_measurement_executed=False,full415F50_returned=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args()
    path=ROOT/a.out
    if path.exists():p.error('fresh immutable second resource source required')
    path.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
