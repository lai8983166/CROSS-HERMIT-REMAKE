"""Original already-bound client calculation and ordinary creation callbacks."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools import school_window_callback as callback
from tools.school_window_callback import (ROOT,SOURCE,SOURCE_SHA256,BASE,geometry,window,parent,Cs,
    CS_ARCH_X86,CS_MODE_32,dword,store,ENTRY,CREATE,STACK,TOP,RETURN,SHADOW,PROPERTY,RANGES,
    IMPORTS,CREATE_SLOT,callback_cpu,callback_stack)

MESSAGES=(129,131,1)
STOP_REASON='after original WM_CREATE; next callback first instruction unexecuted'


def rectangle(raw,wparam):
    if wparam!=0 or len(raw)!=16:raise ValueError('only observed WM_NCCALCSIZE wParam0 RECT16 admitted')
    left,top,right,bottom=struct.unpack('<4i',raw)
    if right<left or bottom<top:raise ValueError('bounded nonnegative client rectangle required')
    return [left,top,right,bottom]


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('create original source SHA')
    md=Cs(CS_ARCH_X86,CS_MODE_32);rows=[]
    for at,op in {0x4249B7:('jne','0x4249fb'),0x424A1B:('call','dword ptr [edx]'),
            0x450DCF:('jmp','dword ptr [eax*4 + 0x45104c]'),0x450ED3:('jmp','0x451030'),
            0x451030:('xor','eax, eax'),0x451029:('call','0x424a90'),
            0x424AFD:('call','dword ptr [0x5923e0]')}.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=op:raise ValueError('create source instruction')
        rows.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    selector=raw[0x451068-BASE]
    if selector!=0 or dword(raw,0x45104C-BASE+selector*4)!=0x450ED3:raise ValueError('create original message1 switch')
    return dict(source_image_sha256=SOURCE_SHA256,parent_source_contract=callback.source_contract(),instructions=rows,
        admitted_messages=list(MESSAGES),client_contract=dict(message=131,wParam=0,bytes=16,type='RECT',
            input_output='actual native LPARAM bytes before and after real DefWindowProcA',nonzero_wParam_admitted=False),
        create_contract=dict(message=1,bytes=48,type='CREATESTRUCTA',source_switch_target='0x450ed3',
            source_zero_return_at='0x451030',default_procedure_called=False),
        already_bound_this='real GetPropA CPP_CLASS -> existing original owner; original branch skips binding and CREATESTRUCT dereference',
        opaque_lParam='131 and1 retain actual host LPARAM as opaque ABI value; original code forwards but does not dereference it',
        pending_policy=STOP_REASON,successful_CreateWindowExA_return=False,normal_cleanup_claimed=False,
        captured_game_global_modified=False,retained_VM_advanced=False,
        documentation=dict(WM_NCCALCSIZE='https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-nccalcsize',
            WM_CREATE='https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-create'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable client/create source evidence required')
    out.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
