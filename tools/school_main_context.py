"""Original WinMain allocation tail and main-context constructor source contracts."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools.school_upstream_factory import (ROOT, SOURCE, SOURCE_SHA256, BASE,
    Cs, CS_ARCH_X86, CS_MODE_32, dword, store, source_contract as factory_source)

ENTRY=0x49DDC9
CTOR=0x44FBB0
GLOBAL=0x7A4A00
COUNTER=0x79FC74
DIRECTORY=0x7A2000
DIRECTORY_BYTES=0x20D
SIZE=0x1110
BACKING=0x2000
OWNER=0x20000000
STACK=0x21000000
TOP=STACK+0xF000
RETURN=0x22000000
BP=TOP-4
SP=TOP-0xAC
STOPS={'allocation':CTOR,'constructor':0x49DDEC,'publication':0x49DE15}
STARTS=(0x4288E0,0x428A40,CTOR,0x439D10,0x424670,0x429310,0x423480,
    0x421540,0x425780,0x425800,0x426110,0x426190,0x426250,0x428B90,
    0x429540,0x429720,0x4297A0,0x56CE80)
ARGS={0x428A40:1,0x56CEC0:3,0x4297A0:1}
IMPORTS={
    0x59227C:('InitializeCriticalSection',0x5FD5CC,1,[0x439D63,0x42156E]),
    0x592274:('CreateEventA',0x5FD5CC,4,[0x421585]),
    0x592214:('GetCurrentDirectoryA',0x5FD5CC,2,[0x42975E]),
    0x592310:('PathAddBackslashA',0x5FD680,1,[0x4297C4]),
    0x592294:('lstrcpyA',0x5FD5CC,2,[0x44FD16,0x44FD38,0x44FD5A,0x44FD7D,0x44FD9F,0x44FDC1,0x44FDE4]),
    0x592218:('lstrcatA',0x5FD5CC,2,[0x44FE01])}
PATHS=(0x9EC,0xAF0,0xBF4,0xCF8,0xDFC,0xF00,0x1004)
CONSTRUCTOR_SEQUENCE=[CTOR,0x439D10,0x56CEC0,0x424670,0x429310,0x423480,
    0x421540,0x425780,0x425800,0x426110,0x56CEC0,0x426190,0x56CEC0,
    0x426250,0x56CEC0,0x428B90,*([0x56CEC0]*6),0x429540,0x429720,0x56CEC0,0x4297A0]


@lru_cache(maxsize=1)
def functions():
    raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    result={ENTRY:0x49DE15,0x56CEC0:0x56CF16}
    for start in STARTS:
        for ins in md.disasm(raw[start-BASE:start-BASE+4096],start):
            if ins.mnemonic=='ret':result[start]=ins.address+ins.size;break
        else:raise ValueError('main finite source function')
    return result


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('main original image SHA')
    imports=[]
    for slot,(name,desc,count,returns) in IMPORTS.items():
        d=struct.unpack_from('<5I',raw,desc-BASE)
        thunk=dword(raw,d[0]+slot-BASE-d[4])
        if raw[thunk+2:].split(b'\0',1)[0]!=name.encode():raise ValueError('main original import')
        imports.append(dict(slot=hex(slot),descriptor=hex(desc),symbol=name,arguments=count,
            dll=raw[d[3]:].split(b'\0',1)[0].decode(),returns=[hex(x) for x in returns]))
    checks={0x49DDC9:('call','0x4288e0'),0x49DDCE:('push','0x1110'),
        0x49DDD3:('call','0x428a40'),0x49DDE7:('call','0x44fbb0'),
        0x49DE01:('mov','dword ptr [0x7a4a00], ecx'),
        0x429738:('push','0'),0x42973A:('push','0x20d'),
        0x42973F:('push','0x7a2000'),0x429744:('call','0x56cec0')}
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    for at,op in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=op:raise ValueError('main source instruction')
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    if raw[0x598694-BASE:].split(b'\0',1)[0]!=b'SaveData\\':raise ValueError('main source save suffix')
    return dict(source_image_sha256=SOURCE_SHA256,entry=hex(ENTRY),constructor=hex(CTOR),
        allocation_bytes=SIZE,backing_bytes=BACKING,stops={k:hex(v) for k,v in STOPS.items()},
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in functions().items()],
        imports=imports,instructions=proof,constructor_calls=CONSTRUCTOR_SEQUENCE,
        allocator=factory_source()['allocator'],directory_memset_args=[DIRECTORY,0x20D,0],
        directory_memset_clears_bytes=0,save_suffix_hex=b'SaveData\\'.hex(),
        inherited_missing_heaps=factory_source()['inherited_missing_heaps'],
        declared_mid_WinMain_frame=True,WinMain_prelude_executed=False,full_WinMain_executed=False,
        scope='Original49DDC9 allocation tail through44FBB0 and49DE01 publication, on an explicitly declared mid-WinMain frame; retained VM and inherited cache are not repaired')


def initial_owner(fill):
    if fill not in (0xA5,0xCC):raise ValueError('main declared dirty fill')
    return b'\xcd'*SIZE+bytes([fill])*(BACKING-SIZE)


def project_constructor(before,calls):
    if len(before)!=BACKING:raise ValueError('main full allocation backing')
    after=bytearray(before)
    def fields(base,values):
        for offset,value in values.items():store(after,base+offset,value)
    def zero(at,n):after[at:at+n]=bytes(n)
    fields(0,{0:0x5986A0,4:0,8:0,12:0,0x10:1,0x2C:0,0x30:-1,
        0x34:0,0x38:0,0x3C:0,0x48:0,0x8CC:0,0x8D0:0,0x8E0:0,0x8E4:0,0x1108:0})
    sections=[r for r in calls if r['name']=='InitializeCriticalSection']
    if len(sections)!=2:raise ValueError('main two actual critical sections')
    for offset,row in zip((0x14,0x164),sections):
        b=bytes.fromhex(row['result']['hex'])
        if len(b)!=24:raise ValueError('main complete x86 critical section')
        after[offset:offset+24]=b
    event=next(r['result']['result'] for r in calls if r['name']=='CreateEventA')
    fields(0x64,{0x118:event})
    fields(0x180,{0:0,4:0,8:0,12:0,16:0,0x628:256,0x62C:256,0x638:64,0x634:0})
    after[0x195]=0;after[0x7B0]=0
    for at,n in ((0x6A8,256),(0x5A8,256),(0x7BC,64),(0x8D4,12),
            (0x9EC,260),(0xBF4,260),(0xCF8,260),(0xF00,260),(0x1004,260)):zero(at,n)
    directory=next(r['result'] for r in calls if r['name']=='GetCurrentDirectoryA')
    text=bytes.fromhex(directory['hex']).split(b'\0',1)[0]+b'\\'
    if not text.endswith(b'\\\\'):
        pass
    else:text=text[:-1]
    if len(text)+10>260:raise ValueError('main bounded original path')
    for offset in PATHS:
        value=text+(b'SaveData\\' if offset==0x1004 else b'')+b'\0'
        after[offset:offset+len(value)]=value
    return bytes(after)


def project_image(phase,calls):
    image=bytearray(SOURCE.read_bytes());store(image,COUNTER-BASE,SIZE)
    if phase!='allocation':
        result=next(r['result'] for r in calls if r['name']=='PathAddBackslashA')
        raw=bytes.fromhex(result['hex'])
        if len(raw)!=DIRECTORY_BYTES:raise ValueError('main complete directory static buffer')
        image[DIRECTORY-BASE:DIRECTORY-BASE+DIRECTORY_BYTES]=raw
    if phase=='publication':store(image,GLOBAL-BASE,OWNER)
    return bytes(image)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable main-context source required')
    path.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
