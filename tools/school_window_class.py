"""Original class registration/caller and source-only callback dependencies."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools import school_window_module as module

ROOT,SOURCE,SOURCE_SHA256,BASE=module.ROOT,module.SOURCE,module.SOURCE_SHA256,module.BASE
geometry=module.geometry
window,parent=geometry.window,geometry.parent
Cs,CS_ARCH_X86,CS_MODE_32=module.Cs,module.CS_ARCH_X86,module.CS_MODE_32
dword,store=module.dword,module.store
ENTRY=0x45047D
SLOT=0x592408
CALLBACK=0x424980
NAME_BYTES=b'Cross Hermit\0'
STOPS={'registered':0x450483,'create_ready':0x4504CF}
RANGES={ENTRY:STOPS['create_ready'],0x56CE80:0x56CE83}
DEPENDENCIES={0x424730:0x4248D9,0x4248E0:0x42497A,0x424980:0x424A89,
    0x450D30:0x45104A,0x4272E0:0x427527}
DOCS={name:'https://learn.microsoft.com/en-us/windows/win32/api/winuser/'+slug for name,slug in (
    ('RegisterClassExA','nf-winuser-registerclassexa'),('GetClassInfoExA','nf-winuser-getclassinfoexa'),
    ('UnregisterClassA','nf-winuser-unregisterclassa'),('WNDPROC','nc-winuser-wndproc'))}


def validate_source(raw):
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('class original source SHA')
    md=Cs(CS_ARCH_X86,CS_MODE_32);rows=[]
    expected={ENTRY:('call','dword ptr [0x592408]'),0x45048A:('and','eax, 0xffff'),
        0x450491:('jne','0x45049d'),0x4504A2:('push','edx'),0x4504A3:('mov','eax, dword ptr [0x7a2728]'),
        0x4504CF:('call','dword ptr [0x59240c]'),0x4249A3:('call','dword ptr [0x5923dc]'),
        0x4249D1:('mov','eax, dword ptr [edx]'),0x4249F6:('call','0x424730'),
        0x4247AA:('call','dword ptr [0x5923e8]'),0x424A1B:('call','dword ptr [edx]'),
        0x450D85:('call','0x4272e0'),0x4273BC:('or','eax, 0xffffffff')}
    for at,op in expected.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=op:raise ValueError('class source instruction '+hex(at))
        rows.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    if dword(raw,0x5986A0-BASE)!=0x450D30 or raw[0x594AB4-BASE:0x594AB4-BASE+10]!=b'CPP_CLASS\0':
        raise ValueError('class original vtable/property')
    return rows


def creation_args(instance):
    # Stack order at the call instruction; no return address has been pushed yet.
    return [0,window.TITLE,window.TITLE,geometry.STYLE,16,16,1024,768,0,0,instance,parent.OWNER]


def class_bytes(instance,icons,cursor,brush):
    return struct.pack('<12I',48,0,CALLBACK,0,0,instance,icons[0],cursor,brush,0,window.TITLE,icons[1])


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes();rows=validate_source(raw)
    return dict(source_image_sha256=SOURCE_SHA256,parent_source_contract=module.source_contract(),instructions=rows,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest(),
            execution_scope='caller' if a in RANGES else 'source-only dependency') for a,b in {**RANGES,**DEPENDENCIES}.items()],
        registration=dict(call_va=hex(ENTRY),slot=hex(SLOT),return_va=hex(STOPS['registered']),
            class_address=geometry.CLASS_AT,class_bytes=48,callback=hex(CALLBACK),class_name='Cross Hermit',
            pointer_adaptation=[dict(offset=8,guest=CALLBACK,host='owned rooted stdcall IPC transport'),
                dict(offset=40,guest=window.TITLE,host='owned guarded ANSI class-name storage')],
            original_guest_class_modified=False,return_type='ATOM',caller_masks_low_word_at='0x45048a'),
        creation=dict(call_va='0x4504cf',slot='0x59240c',argument_count=12,
            args_with_instance_placeholder=creation_args(0),instance_argument_index=10,owner_argument_index=11,
            call_instruction_executed=False),
        callback_dependency=dict(property_name='CPP_CLASS',property_literal='0x594ab4',
            creation_this='WM_CREATE/WM_NCCREATE lParam CREATESTRUCTA first dword; WM_INITDIALOG lParam',
            binding='0x424730',virtual_table='0x5986a0',first_virtual='0x450d30',input_dispatch='0x4272e0',
            raw_callback_not_host_executable=True,executed=False),
        stops={k:hex(v) for k,v in STOPS.items()},documentation=DOCS,
        scope='Fresh genuine-module scratch startup, dormant callback transport, registration and caller preparation only',
        retained_VM_advanced=False,window_created=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable class source evidence required')
    out.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
