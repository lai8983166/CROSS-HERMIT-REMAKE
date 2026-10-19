"""Original font-success caller, manager queues and gamma-call admission."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools.school_font_finish import ROOT,SOURCE,SOURCE_SHA256,BASE,Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_renderer_init import bind,initialize_queues

HEADS=0x24001000
ARENA=0x25001000
LAYER_BYTES=4096*8
ARENA_BYTES=1048576
PHASES={'bind':(0x4134E3,0x413505),'queues':(0x413505,0x413513),'gamma':(0x413513,0x416CFA)}
RANGES={0x4134E3:0x413559,0x40D970:0x40D9BA,0x4142B0:0x4142DD,
        0x40DAB0:0x40DB10,0x40DB10:0x40DB81,0x40DB90:0x40DBEB,
        0x40DBF0:0x40DC76,0x40DC80:0x40DCCC,0x428A40:0x428AC6,
        0x56CEC0:0x56CF18,0x56CE80:0x56CE83,0x416C40:0x416CBF,0x416CC0:0x416D17}
ARGS={0x40D970:1,0x4142B0:0,0x40DAB0:0,0x40DB10:1,0x40DB90:0,
      0x40DBF0:1,0x40DC80:0,0x428A40:1,0x56CEC0:3,0x416C40:1,0x416CC0:1}


def gamma_bytes():
    return struct.pack('<256H',*(i<<8 for i in range(256)))*3


def project_owner(before,phase,owner,device):
    if len(before)!=0xC000 or phase not in PHASES:raise ValueError('font caller full owner/phase required')
    after=bytearray(before)
    if phase=='bind':after[0x1058:0x10B8]=bind(before[0x1058:0x10B8],owner,device)
    elif phase=='queues':after[0x1058:0x10B8]=initialize_queues(before[0x1058:0x10B8],HEADS,ARENA)
    else:after[0xB408:0xBA08]=gamma_bytes()
    return bytes(after)


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('font caller source image SHA')
    checks={0x4134E3:('mov','dword ptr [ebp - 8], eax'),0x4134EA:('je','0x4134f3'),
        0x413500:('call','0x40d970'),0x40D993:('mov','dword ptr [eax], ecx'),
        0x4142D0:('mov','eax, dword ptr [eax + 0xb210]'),0x41350E:('call','0x40dab0'),
        0x40DACD:('push','0x1000'),0x40DAE5:('push','0x100000'),0x428A6E:('call','0x56e810'),
        0x41351A:('je','0x413523'),0x41352F:('call','0x416c40'),0x413541:('call','0x416cc0'),
        0x416C84:('mov','word ptr [eax + edx*2 + 0xb408], cx'),
        0x416C98:('mov','word ptr [eax + edx*2 + 0xb608], cx'),
        0x416CAC:('mov','word ptr [eax + edx*2 + 0xb808], cx'),
        0x416CE3:('push','1'),0x416CFA:('call','dword ptr [eax + 0x48]')}
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    for at,expected in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=expected:raise ValueError('font caller instruction '+hex(at))
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,instructions=proof,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        phases={p:dict(start=hex(a),stop=hex(b)) for p,(a,b) in PHASES.items()},
        manager_offset=0x1058,queue_allocations=[LAYER_BYTES,ARENA_BYTES],
        allocator=dict(va='0x56e810',return_va='0x428a73',block_type=1,file=0x594E28,
            line=struct.unpack_from('<h',raw,0x5FF6D8-BASE)[0]+3,initial_byte=0xCD),
        gamma=dict(offset=0xB408,bytes=1536,channels=3,entries_per_channel=256,shift=8,
            device_method_offset=72,flags=1,call_instruction_executed=False),
        full413450_returned=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable caller source required')
    path.write_text(json.dumps(source_contract(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
