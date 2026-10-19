"""Original second-font cleanup/state and complete415F50 return source contract."""
import argparse
import hashlib
import json
from functools import lru_cache
from tools.school_font_state import (SOURCE,SOURCE_SHA256,BASE,ROOT,SIZE,IMPORTS,CALLS,RENDER,STAGES,plan,project,
    RANGES as STATE_RANGES,source_contract as state_source,Cs,CS_ARCH_X86,CS_MODE_32)
from tools.school_font_second import SECOND

RANGES=dict(STATE_RANGES,**{})
RANGES.update({0x41602A:0x41603D,0x416101:0x416133})
PHASES={'cleanup':(0x4017B6,0x401810),'vertex':(0x401810,0x40186E),
        'states':(0x40186E,0x416101),'return':(0x416101,0x4134E3)}
EXIT_TRACE=[0x416101,0x416104,0x416108,0x416111,0x41602A,0x41602D,0x416030,0x416033,0x416037,
    0x416116,0x416118,0x41611B,0x416122,0x416123,0x416124,0x416125,0x416128,0x41612A,
    0x56CE80,0x56CE82,0x41612F,0x416131,0x416132]


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('font finish source SHA')
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    checks={0x4134DE:('call','0x415f50'),0x41602D:('add','ecx, 1'),0x416033:('cmp','dword ptr [ebp - 0x18], 2'),
        0x416037:('je','0x416116'),0x416108:('jge','0x416111'),0x416116:('xor','eax, eax'),
        0x41611B:('mov','dword ptr fs:[0], ecx'),0x416125:('add','esp, 0x64'),
        0x41612A:('call','0x56ce80'),0x416131:('pop','ebp'),0x416132:('ret','')}
    for at,expected in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=expected:raise ValueError('font finish original caller/loop/SEH/return '+hex(at))
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(shared_state_source=state_source(),source_image_sha256=SOURCE_SHA256,instructions=proof,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        second_object=SECOND,VB_args=[8400,520,0,0],state_blocks=2,state_calls_per_block=30,
        exit_trace=[hex(a) for a in EXIT_TRACE],loop_index_before=1,loop_index_after=2,
        captured_prior_SEH=0,success_result=0,native_return='0x4134e3',
        phases={p:dict(start=hex(a),stop=hex(b)) for p,(a,b) in PHASES.items()},
        caller_suffix_executed=False,manager_bound=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable font finish source required')
    path.write_text(json.dumps(source_contract(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
