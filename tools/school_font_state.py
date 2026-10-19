"""Original temporary-font cleanup and first-font vertex/state-block initialization."""
import hashlib
import json
import struct
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_font_glyph import SOURCE,SOURCE_SHA256,BASE,ROOT,SLOT,SIZE,dword

RANGES={0x4017B6:0x401810,0x4160DF:0x416101,0x401810:0x401D29,0x56CE80:0x56CE83}
IMPORTS={0x4017C5:(0x5920C4,'DeleteObject','font_delete_bitmap'),
         0x4017DB:(0x592060,'DeleteDC','font_delete_dc'),
         0x4017F1:(0x5920C4,'DeleteObject','font_delete_font')}
RENDER=[(0x401913,27,1),(0x401935,19,5),(0x401957,20,6),(0x401979,15,1),
        (0x40199B,24,8),(0x4019BD,25,5),(0x4019DF,8,3),(0x401A01,52,0),
        (0x401A26,136,1),(0x401A48,40,0),(0x401A6D,152,0),(0x401A92,151,0),
        (0x401AB7,167,0),(0x401AD9,28,0)]
STAGES=[(0x401AFD,0,1,4),(0x401B21,0,2,2),(0x401B45,0,3,0),(0x401B69,0,4,4),
        (0x401B8D,0,5,2),(0x401BB1,0,6,0),(0x401BD5,0,17,1),(0x401BF9,0,16,1),
        (0x401C1D,0,18,0),(0x401C41,0,11,0),(0x401C65,0,24,0),(0x401C89,1,1,1),(0x401CAD,1,4,1)]
CALLS={0x401853:('vb',92,[8400,520,0,0]),0x40189B:('begin',208,[]),0x4018C2:('texture',244,[0])}
CALLS.update({at:('render',200,[a,b]) for at,a,b in RENDER})
CALLS.update({at:('stage',252,[a,b,c]) for at,a,b,c in STAGES})
CALLS.update({0x401CDA:('end',212,[]),0x401D04:('end',212,[])})


def plan(texture):
    one=[dict(method='begin',args=[]),dict(method='texture',args=[0,texture])]
    one += [dict(method='render',args=[a,b]) for _,a,b in RENDER]
    one += [dict(method='stage',args=[a,b,c]) for _,a,b,c in STAGES]
    one += [dict(method='end',args=[])]
    return one*2


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('font state source SHA')
    md=Cs(CS_ARCH_X86,CS_MODE_32);instructions=list(md.disasm(raw[0x401810-BASE:0x401D29-BASE],0x401810));proof=[];calls=[]
    for at,(method,offset,args) in CALLS.items():
        i=next(i for i in instructions if i.address==at)
        if i.mnemonic!='call' or not i.op_str.endswith(' + '+hex(offset)+']'):raise ValueError('font state original virtual method '+hex(at))
        start=max(n for n,j in enumerate(instructions) if j.address<at and (j.mnemonic,j.op_str)==('mov','esi, esp'))
        immediates=[int(j.op_str,0) for j in instructions[start:] if j.address<at and j.mnemonic=='push' and j.op_str.startswith(('0x','1','2','3','4','5','6','7','8','9','0'))]
        if list(reversed(immediates))!=args:raise ValueError('font state original push arguments '+hex(at))
        calls.append(dict(va=hex(at),return_va=hex(at+i.size),method=method,offset=offset,immediate_args=args,hex=i.bytes.hex()))
    checks={0x40180D:('ret','4'),0x4160FC:('call','0x401810'),0x4018D5:('and','edx, 4'),
        0x401CC3:('add','eax, 0x670'),0x401CEC:('add','ecx, 0x674'),0x401D28:('ret',''),
        0x401DAB:('call','dword ptr [edx + 0xe0]')}
    for at,expected in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=expected:raise ValueError('font state original cleanup/return '+hex(at))
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    desc=struct.unpack_from('<5I',raw,0x5FD5F4-BASE);imports=[]
    for ret,(slot,name,op) in IMPORTS.items():
        thunk=dword(raw,desc[0]+4*((slot-BASE-desc[4])//4))
        if raw[thunk+2:].split(b'\0',1)[0]!=name.encode('ascii'):raise ValueError('font state original GDI import')
        imports.append(dict(slot=hex(slot),target=hex(dword(raw,slot-BASE)),symbol=name,return_va=hex(ret),op=op,args=1))
    return dict(source_image_sha256=SOURCE_SHA256,functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        instructions=proof,calls=calls,imports=imports,VB_args=[8400,520,0,0],state_calls_per_block=30,state_blocks=2,
        optional_state7_branch_executed=False,cleanup_stop='0x401810',VB_stop='0x40186e',states_stop='0x416101',
        original_415F50_returned=False,retained_VM_advanced=False)


def project(before,vb,tokens=(0,0)):
    if len(before)!=SIZE or not 0<vb<=0xFFFFFFFF or len(tokens)!=2 or any(not 0<=t<=0xFFFFFFFF for t in tokens):raise ValueError('font state full object/actual owned resources')
    after=bytearray(before)
    for at,value in ((0x60,vb),(0x670,tokens[0]),(0x674,tokens[1])):struct.pack_into('<I',after,at,value)
    return bytes(after)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable font state source report required')
    path.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf-8',newline='\n')
