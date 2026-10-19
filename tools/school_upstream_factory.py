"""Actual renderer factory allocation/constructor and distinct caller prerequisites."""
import argparse
import hashlib
import json
import pickle
import struct
from functools import lru_cache
from tools.school_owner_startup import (ROOT,SOURCE,SOURCE_SHA256,BASE,CTOR,functions,
    project_constructor,project_image,Cs,CS_ARCH_X86,CS_MODE_32,dword,store,ARGS)
from tools.school_font_startup import HEAD,COUNTER,CHECKPOINT,CHECKPOINT_SHA

OWNER_BYTES=0xBA20
OUTPUT=0x26001000
WINDOW=0x13572468
RECEIVER=0x24681357
OUTPUT_VALUE=0xDEADBEEF
GAME_GLOBAL=0x7A4A00
FACTORIES={'window':dict(entry=0x412C70,constructor_return=0x412CC2,admission=0x413450,
    admission_return=0x412D06,constructor_depth=116),
    'game':dict(entry=0x450570,constructor_return=0x4505C7,admission=0x4500B0,
    admission_return=0x450606,constructor_depth=120)}
RANGES=dict(functions());RANGES.update({0x412C70:0x412D3B,0x450570:0x45072B,0x428A40:0x428AC6})
CTOR_SEQUENCE=[0x412E30,0x409900,0x420990,0x41EAD0,0x417530,0x420990,
    0x41EE30,0x420990,0x41EAD0,0x40D7E0,0x4107B0,0x410C20,0x40BE70,
    0x420990,0x56CEC0,0x40C1A0,0x56CEC0,0x40C140,0x41D0D0,0x56DDA0,
    0x41D2E0,0x41E6B0,0x41D2E0,0x41E6B0,0x417C40,0x417E00,
    *([0x56CEC0]*5),0x41AB10,0x56CEC0,0x56CEC0,0x56CEC0,0x40B590,
    0x56CEC0,0x415A90,0x4170C0,0x414F90,0x415370,0x415530]


def initial_owner(fill):
    if fill not in (0xA5,0xCC):raise ValueError('factory declared guard fill')
    return b'\xcd'*OWNER_BYTES+bytes([fill])*(0xC000-OWNER_BYTES)


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('factory original source SHA')
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    checks={0x412C9D:('push','0xba20'),0x412CA2:('call','0x428a40'),0x412CBD:('call','0x412e30'),
        0x412CF6:('push','1'),0x412CF8:('push','1'),0x412D01:('call','0x413450'),
        0x4505A2:('push','0xba20'),0x4505A7:('call','0x428a40'),
        0x4505C2:('call','0x412e30'),0x4505FB:('mov','ecx, dword ptr [0x7a4a00]'),
        0x450601:('call','0x4500b0'),0x45060A:('call','0x4135d0'),0x45063A:('call','0x413630'),
        0x45066F:('push','1'),0x450671:('push','0'),0x45067A:('call','0x413450'),0x4506AC:('call','0x413560'),
        0x548D89:('mov','eax, dword ptr [0x80a398]'),0x54874F:('mov','dword ptr [0x80a398], esi')}
    for at,expected in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=expected:raise ValueError('factory original instruction '+hex(at))
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    captured=(ROOT/CHECKPOINT).read_bytes()
    if hashlib.sha256(captured).hexdigest()!=CHECKPOINT_SHA:raise ValueError('factory retained checkpoint SHA')
    state=pickle.loads(captured)
    if state['source_sha']!=SOURCE_SHA256 or state['pending_eip']!=0x40E2D0:raise ValueError('factory retained checkpoint boundary')
    missing=[]
    for at in (HEAD,GAME_GLOBAL):
        pointer=dword(raw,at-BASE)
        if any(a<=pointer<a+len(b) for a,b in state['memory']):raise ValueError('factory inherited heap absence changed')
        missing.append(dict(global_va=hex(at),captured_pointer=hex(pointer),mapped_in_retained_checkpoint=False))
    # Both real call sites push their own mode inputs; no new device call executes here.
    return dict(source_image_sha256=SOURCE_SHA256,instructions=proof,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        factories=FACTORIES,allocation_bytes=OWNER_BYTES,allocation_initial_byte=0xCD,
        allocator=dict(va='0x56e810',return_va='0x428a73',block_type=1,file=0x594E28,
            line=struct.unpack_from('<h',raw,0x5FF6D8-BASE)[0]+3),
        window_startup_middle_args=[1,1],game_startup_middle_args=[0,1],
        data_literal=dict(va='0x598758',hex=raw[0x598758-BASE:0x59875E-BASE].hex()),
        game_pre_start_calls=['0x4500b0','0x4135d0','0x413630'],game_post_start_call='0x413560',
        constructor_calls=CTOR_SEQUENCE,retained_checkpoint=dict(path=CHECKPOINT,sha256=CHECKPOINT_SHA),
        inherited_missing_heaps=missing,cache_head_reset_by_factory_prefix=False,
        original_factory_output_published=False,original_device_startup_executed=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable upstream factory source required')
    path.write_text(json.dumps(source_contract(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
