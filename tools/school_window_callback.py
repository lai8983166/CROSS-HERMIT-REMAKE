"""Bounded genuine creation: complete original WM_NCCREATE, then pause."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools import school_window_class as previous

ROOT,SOURCE,SOURCE_SHA256,BASE=previous.ROOT,previous.SOURCE,previous.SOURCE_SHA256,previous.BASE
geometry,window,parent=previous.geometry,previous.window,previous.parent
Cs,CS_ARCH_X86,CS_MODE_32=previous.Cs,previous.CS_ARCH_X86,previous.CS_MODE_32
dword,store=previous.dword,previous.store
ENTRY=0x424980
CREATE=0x4504CF
STACK=0x23000000
TOP=STACK+0xF000
RETURN=0x24000000
SHADOW=0x25001000
PROPERTY=b'CPP_CLASS\0'
RANGES={0x424730:0x4248D9,ENTRY:0x424A89,0x424A90:0x424B1D,0x450D30:0x45104C,
    0x4272E0:0x427527,0x56CE80:0x56CE83}
IMPORTS={0x5923DC:('GetPropA',2),0x5923EC:('GetWindowLongA',2),
    0x5923E8:('SetPropA',3),0x5923E0:('DefWindowProcA',4)}
CREATE_SLOT=0x59240C


def callback_cpu():
    return dict(EIP=ENTRY,ESP=TOP,EBP=0x11223344,EBX=0x55667788,ESI=0x88776655,EDI=0x44332211,
        EAX=0x01020304,ECX=0x05060708,EDX=0x090A0B0C,EFLAGS=0x202)


def callback_stack(packet):
    b=bytearray(b'\xd7'*65536)
    args=[packet['hwnd'],packet['message'],packet['wParam'],SHADOW if packet['message']==129 else packet['lParam']]
    for i,v in enumerate([RETURN,*args]):store(b,TOP-STACK+i*4,v)
    return bytes(b),args


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('callback source SHA')
    desc=struct.unpack_from('<5I',raw,0x5FD5E0-BASE);imports=[]
    for slot,(name,n) in {**IMPORTS,CREATE_SLOT:('CreateWindowExA',12)}.items():
        thunk=dword(raw,desc[0]+slot-BASE-desc[4])
        if raw[thunk+2:].split(b'\0',1)[0]!=name.encode():raise ValueError('callback original import symbol')
        imports.append(dict(slot=hex(slot),symbol=name,arguments=n,descriptor='0x5fd5e0',dll='USER32.dll'))
    if raw[0x594AB4-BASE:0x594AB4-BASE+10]!=PROPERTY:raise ValueError('callback property source')
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    for at in (CREATE,0x4249D1,0x4249F6,0x4247AA,0x424805,0x424A1B,0x450D85,0x451029,0x424AFD,0x49DF73,0x49DF85):
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at));proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,parent_source_contract=previous.source_contract(),imports=imports,instructions=proof,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        declared_callback_cpu=callback_cpu(),callback_stack=STACK,callback_return=RETURN,create_shadow=SHADOW,
        callback_frame_scope='Declared stdcall guest ABI frame and opaque register seeds; not a capture of host callback registers',
        global_dependency=dict(va='0x7a49fc',captured_value=dword(raw,0x7A49FC-BASE),factory_output_argument='0x49df73',
            factory_call='0x49df85',publication_after_window_creation=True,global_modified=False,heap_resolved=False),
        scope='Actual original CreateWindowExA arguments; execute callbacks through completed WM_NCCREATE and pause before next callback first instruction',
        native_WNDPROC_reverse_translation='Owned host callback pointer -> original424980 for GetWindowLongA(-4)',
        create_struct='Actual48-byte host CREATESTRUCTA copied to guarded guest shadow; only lParam callback ABI value translated',
        termination='At next callback retain unanswered packet and terminate owned helper process; no fabricated callback result, CreateWindowExA return or explicit unregistration claimed',
        retained_VM_advanced=False,successful_CreateWindowExA_return=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable callback source evidence required')
    out.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
