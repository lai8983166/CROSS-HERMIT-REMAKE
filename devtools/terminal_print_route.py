"""Offline original WM_PRINT/WM_PRINTCLIENT routing; no Windows API execution.

Uses authenticated retained MAIN bytes, synthetic callback stack/HDC, and one
declared GetPropA result from the retained HWND property. Stops BEFORE the OS
default procedure. Does not reconstruct pixels or certify the live subclass.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ESP

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
RECORD=ROOT/'analysis/terminal-host-menu-native-v1-20261112.json.gz'
RECORD_SHA='e9d178a7dee62d1b30c7d2722058c906ae12c4f5753f8363e5614e446511fd08'


def authenticated():
    raw=(ROOT/'analysis/hermit_game.exe').read_bytes()
    packed=RECORD.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA or hashlib.sha256(packed).hexdigest()!=RECORD_SHA:
        raise ValueError('fixed original/observation identity')
    return raw,json.loads(gzip.decompress(packed))


def route(raw, record, message):
    if message not in (0x317,0x318): raise ValueError('only print messages')
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA: raise ValueError('original image changed')
    ready=record['lifecycle']['ready']; owner=ready['main']['pointer']
    body=bytes.fromhex(ready['main']['hex']); hwnd=ready['window']['hwnd']
    if struct.unpack_from('<I',body)[0]!=0x5986A0 or ready['window']['property']!=owner:
        raise ValueError('retained MAIN/window owner')
    if struct.unpack_from('<II',body,8)!=(0,0):
        raise ValueError('retained default-procedure route changed')
    u=Uc(UC_ARCH_X86,UC_MODE_32)
    u.mem_map(0x400000,(len(raw)+4095)&~4095);u.mem_write(0x400000,raw)
    start=owner&~4095;u.mem_map(start,((owner-start+len(body)+4095)//4096)*4096);u.mem_write(owner,body)
    stack=0x20000000;u.mem_map(stack,0x10000);sp=stack+0xf000
    hdc=0x12345678;flags=4|8
    u.mem_write(sp,struct.pack('<5I',0x2000ffff,hwnd,message,hdc,flags));u.reg_write(UC_X86_REG_ESP,sp)
    trace=[];leaves=[];stop={}
    def word(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    def code(uc,at,size,_):
        trace.append(at)
        if len(trace)>2000: raise ValueError('bounded callback route')
        if at==0x4249A3:
            top=uc.reg_read(UC_X86_REG_ESP)
            if [word(top),word(top+4)]!=[hwnd,0x594AB4]:raise ValueError('GetProp arguments')
            leaves.append(dict(api='GetPropA',source='retained HWND property, not native call',result=owner))
            uc.reg_write(UC_X86_REG_EAX,owner);uc.reg_write(UC_X86_REG_ESP,top+8)
            from unicorn.x86_const import UC_X86_REG_EIP
            uc.reg_write(UC_X86_REG_EIP,at+size)
        elif at==0x424AFD:
            top=uc.reg_read(UC_X86_REG_ESP);args=[word(top+i*4) for i in range(4)]
            if args!=[hwnd,message,hdc,flags]:raise ValueError('default callback ABI changed')
            stop.update(pc=at,api_slot=0x5923E0,arguments=args);uc.emu_stop()
    def write(uc,access,at,size,value,_):
        if not stack<=at<at+size<=stack+0x10000:
            raise ValueError('unexpected non-stack write')
    u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,write)
    u.emu_start(0x424980,0x2000ffff,count=2000)
    if not stop:raise ValueError('default procedure boundary not reached')
    return dict(message=message,trace=trace,steps=len(trace),platform_leaf=leaves,stop_before=stop,
        original_dispatch=[hex(p) for p in (0x424980,0x450D30,0x4272E0,0x424A90) if p in trace],
        stack_only_writes=True,native_OS_executed=False,pixels_recovered=False)


def report():
    raw,record=authenticated()
    return dict(accepted=False,source_sha256=SOURCE_SHA,retained_source_sha256=RECORD_SHA,
        routes=[route(raw,record,m) for m in (0x317,0x318)],
        conclusion='Original print messages reach default procedure without game drawing',
        scope='Original disk instructions and retained owner at ready sample; not actual PrintWindow message delivery trace',
        original_pixels='Unavailable: uniform RGB values and sentinel differences were discarded',
        live_subclass_qualified=False,PrintWindow_menu_qualified=False,
        menu_gate='blocked until independent framebuffer capture is qualified',
        documentation=['https://learn.microsoft.com/en-us/windows/desktop/gdi/wm-printclient',
                       'https://learn.microsoft.com/en-us/windows/win32/gdi/wm-print'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    with a.out.open('x',encoding='utf8') as stream:json.dump(report(),stream,indent=2)
