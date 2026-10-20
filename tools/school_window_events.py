"""Original creation size, move, show and changing-position source contracts."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools import school_window_create as base
from tools.school_window_create import (ROOT,SOURCE,SOURCE_SHA256,BASE,geometry,window,parent,Cs,
    CS_ARCH_X86,CS_MODE_32,dword,store,ENTRY,CREATE,STACK,TOP,RETURN,SHADOW,PROPERTY,RANGES,
    IMPORTS,CREATE_SLOT,callback_cpu,callback_stack)

MESSAGES=(129,131,1,5,3,24,70)
STOP_REASON='after original WM_WINDOWPOSCHANGING; next callback first instruction unexecuted'


def scalar(message,wparam,lparam):
    if not all(type(v) is int and 0<=v<=0xFFFFFFFF for v in (wparam,lparam)):raise ValueError('events uint32 scalar ABI')
    if message==5:return dict(width=lparam&65535,height=lparam>>16,size_state=wparam)
    if message==3:
        x,y=struct.unpack('<hh',struct.pack('<I',lparam));return dict(x=x,y=y)
    if message==24:return dict(shown=wparam!=0,reason=lparam)
    raise ValueError('events not a declared scalar message')


def windowpos(raw,hwnd):
    if len(raw)!=28:raise ValueError('actual x86 WINDOWPOS28 required')
    h,after,x,y,cx,cy,flags=struct.unpack('<II4iI',raw)
    if h!=hwnd:raise ValueError('WINDOWPOS must refer to actual owned callback window')
    return dict(hwnd=h,hwnd_insert_after=after,x=x,y=y,cx=cx,cy=cy,flags=flags)


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('events source SHA')
    rows=[];md=Cs(CS_ARCH_X86,CS_MODE_32)
    for at in (0x4249B7,0x424A1B,0x450DA1,0x450DCF,0x450EDD,0x451016,0x451029,0x451030,0x450E40):
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at));rows.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    selector=raw[0x451068-BASE+5-1]
    if selector!=2 or dword(raw,0x45104C-BASE+selector*4)!=0x450EDD:raise ValueError('events original size switch')
    return dict(source_image_sha256=SOURCE_SHA256,parent_source_contract=base.source_contract(),instructions=rows,
        admitted_messages=list(MESSAGES),scalar_messages=dict(size=5,move=3,show=24),
        scalar_contract='WM_SIZE unsigned16 width/height; WM_MOVE signed16 x/y; WM_SHOWWINDOW boolean WPARAM and scalar reason',
        WINDOWPOS=dict(message=70,bytes=28,layout=['HWND32','HWND32','int32 x','int32 y','int32 cx','int32 cy','uint32 flags'],
            actual_native_input_output=True,guest_dereference=False),
        source_routes=dict(size='450EDD ->451030 zero',move_show_position='450D30 ->424A90 -> actual DefWindowProcA'),
        pending_policy=STOP_REASON,captured_game_global_modified=False,retained_VM_advanced=False,
        successful_CreateWindowExA_return=False,normal_cleanup_claimed=False,
        documentation=dict(WINDOWPOS='https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowpos',
            WM_WINDOWPOSCHANGING='https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-windowposchanging'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable events source evidence required')
    out.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
