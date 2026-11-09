"""One original cooperative wait observed in a qualified guest, before long capture."""
import argparse
import ctypes as C
import gzip
import json
from pathlib import Path
import struct
import time
from types import SimpleNamespace

from devtools import terminal_debug_relay as relay
from devtools import terminal_menu_handoff as menu
from devtools import terminal_startup_handoff as startup
from devtools.terminal_scene_resources import clone
from devtools.native_input_isolation import require_qualified_guest

base=menu.base
need=base.need
word=base.word
SITES=(0x422360,0x4223A8,0x4223AE,0x4223BE,0x4223C4,0x4223D7,
       0x4223DD,0x4223EF,0x4223F5,0x422407,0x42240D,0x422431)
SLOTS=(0x592234,0x592228,0x59222C,0x592238,0x59226C)


def probe(pid,owned,progress,duration):
    result=dict(error=None,host_game_calls=[],host_memory_writes=[],accepted=False)
    h=base.original.openp(0x100450,False,pid)
    base.original.check(h,'read owned original for wait preflight')
    try:
        c=SimpleNamespace(pid=pid,h=h,owned=owned,get=lambda a,n:base.original.required(h,a,n))
        c.main=word(c.get(0x7A4A00,4))
        from devtools.isolated_guest_focus import focus_owned_window
        hwnd=base.original.findwindow(b'Cross Hermit',None)
        result['guest_activation']=focus_owned_window(c,hwnd)
        with base.original.frozen(h,pid) as frames:
            manager,nodes=startup.graph(c)
            starts=[r for r in nodes if word(bytes.fromhex(r['head_hex']))==startup.STARTUP]
            need(len(starts)==1,'one original startup worker for short wait probe')
            task=starts[0];node=task['pointer'];head=bytes.fromhex(task['head_hex']);tid=word(head,0x24)
            frame=next(f for f in frames if f['tid']==tid)
            tls=base.capture_tls(c,frame,node)
            result['owner']=dict(node=node,thread_id=tid,head_hex=head.hex(),TLS=tls,frame=frame,
                node_event=base.event_identity(c,word(head,0x1C)),
                manager_event=base.event_identity(c,word(manager,0x118)))
        raw=base.SOURCE.read_bytes();need(base.sha(raw)==base.SOURCE_SHA,'fixed original image')
        result['code']=[]
        for a,b in ((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98)):
            code=c.get(a,b-a);need(code==raw[a-0x400000:b-0x400000],'unchanged original wait instructions')
            result['code'].append(dict(pointer=a,hex=code.hex()))
        result['IAT']=[dict(slot=s,target=word(c.get(s,4)))for s in SLOTS]
        import pefile
        result['API_exports']=[]
        for row,name in zip(result['IAT'],('EnterCriticalSection','ResetEvent','SetEvent','LeaveCriticalSection','WaitForSingleObject')):
            exported=relay.resolve(pid,'kernel32.dll',name)
            need(exported['target']==row['target'],'original IAT equals actual current OS export '+name)
            disk=pefile.PE(exported['module_path']).get_memory_mapped_image(ImageBase=exported['base'])[exported['RVA']:exported['RVA']+32]
            actual=c.get(exported['target'],32)
            result['API_exports'].append(dict(name=name,slot=row['slot'],entry_hex=actual.hex(),
                relocated_disk_entry_hex=disk.hex(),**exported))
            need(actual==disk,'actual OS API export entry bytes after declared PE relocations '+name)
        result['TLS_implementation']=base.tls_contract(c)
        index=0;return_ip=None
        def capture(context):
            nonlocal index,return_ip
            ip=word(context,184);sp=word(context,196)
            expected=SITES[index] if index<len(SITES) else return_ip
            need(ip==expected,'ordered native wait entry/API/return sites')
            if index==0:
                need(word(context,172)==node,'wait ECX is current startup node')
                return_ip=word(c.get(sp,4))
                need(0x401000<=return_ip<0x591000,'natural original wait caller')
            row=dict(stack_pointer=sp,stack_hex=c.get(sp,128).hex(),
                node_pointer=node,node_hex=c.get(node,64).hex(),
                manager_pointer=c.main+0x64,manager_hex=c.get(c.main+0x64,0x120).hex(),
                PTD_pointer=tls['PTD'],PTD_hex=c.get(tls['PTD'],116).hex())
            bp=word(context,180);chain=[]
            for _ in range(100):
                pair=c.get(bp,8);next_bp,ret=struct.unpack('<II',pair)
                chain.append(dict(bp=bp,saved_bp=next_bp,return_va=ret))
                if not bp<next_bp<bp+0x100000:break
                bp=next_bp
            current_frame=dict(tid=tid,context_hex=context.hex(),EIP=ip,ESP=sp,EBP=word(context,180),chain=chain)
            row['frame']=current_frame
            row['current_TLS']=base.capture_tls(c,current_frame,node)
            need(row['current_TLS']['PTD']==tls['PTD'],'same actual current TLS slot, not just old PTD memory')
            index+=1
            return row,SITES[index] if index<len(SITES) else return_ip if index==len(SITES) else None
        result['relay']=relay.observe(c,owned,tid,SITES[0],capture,seconds=30,maximum_hits=32)
        need(result['relay']['error'] is None and result['relay']['scope_completed'],
             'short hardware relay must observe one complete original wait scope')
        need(not result['relay']['cleanup']['errors'] and result['relay']['cleanup']['parent_detached'],
             'restore debug instrumentation and detach without terminating original')
        hits=result['relay']['hits']
        need(len(hits)==len(SITES)+1,'every required native wait boundary observed')
        values={r['target']:word(bytes.fromhex(r['context_hex']),176)for r in hits}
        need(values[0x4223C4]!=0 and values[0x4223DD]!=0 and values[0x42240D]==0,
             'ResetEvent and SetEvent succeeded; WaitForSingleObject returned WAIT_OBJECT_0')
        result['native_wait_API_sequence_observed']=True
    except Exception as exc:
        import traceback
        result['error']=repr(exc);result['traceback']=traceback.format_exc(limit=8)
    finally:base.original.close(h)
    return result


def run(out):
    from devtools.terminal_wait_observer_gate import require_supported_relay
    require_supported_relay()
    isolation=require_qualified_guest()
    paths=[Path(__file__),Path(relay.__file__)]
    identities=[base.identity(p)for p in paths]
    result=clone(menu.run,continue_menu=probe)(out,30,None,False,0)
    need(identities==[base.identity(p)for p in paths],'native wait observer stayed frozen')
    result.update(kind='original_native_wait_debug_preflight',input_isolation=isolation,
        observer_implementations=identities,accepted=False,full_battle_exit_accepted=False,
        full_instruction_trace=False,full_resource_lifetime_proved=False)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    out=parser.parse_args().out.resolve()
    need(out.is_relative_to(base.ROOT/'analysis')and not out.exists(),'new guest-owned evidence')
    result=run(out);raw=json.dumps(result,separators=(',',':')).encode()
    need(len(raw)<=16*1024*1024,'bounded wait preflight report')
    with out.open('xb')as f:f.write(gzip.compress(raw,mtime=0))
    print(json.dumps(dict(report=base.identity(out),probe_error=(result.get('probe')or{}).get('error'),
        lifecycle_error=result['lifecycle']['error'])),flush=True)
    if (result.get('probe')or{}).get('error')or result['lifecycle']['error']:raise SystemExit(1)
