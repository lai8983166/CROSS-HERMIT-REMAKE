"""Observe the original startup's automatic handoff; no injected game calls/input.

The private process is opened only for read/query/duplicate/synchronize. Frames
are sampled, not traced; normal CRT destruction is not claimed from an exit code.
"""
import argparse
import ctypes as C
import ctypes.wintypes as W
import gzip
import json
from pathlib import Path
import struct
import time
import traceback
from types import SimpleNamespace

from devtools import terminal_scene_owner as base
from devtools.terminal_scene_resources import clone

ROOT=base.ROOT
STARTUP=0x5CAA48
MENU=0x59B060
RANGES=base.RANGES+((0x506150,0x5066A0),(0x50A007,0x50A1E8),
    (0x45E8D0,0x45EDB8),(0x4217C0,0x421BF0),(0x421F50,0x422090),
    (0x41F480,0x41F640),(0x45EFB0,0x45F0CB),(0x415480,0x415C00),
    (0x5066A0,0x50673A),(0x525060,0x525084),(0x49E834,0x49E845))
IAT=tuple(dict.fromkeys(base.IAT+(0x592440,0x592284)))
PARENT=ROOT/'analysis/terminal-scene-preflight-v3-20261107.json.gz'
PARENT_SHA='3a028556e6e0141746df00573766332ee91ec34bb7a6c19ba4e182724ff4d7ff'
word=base.word
need=base.need


def graph(c):
    manager=c.get(c.main+0x64,0x120);rows=[];seen=set()
    for bucket in range(32):
        ptr=word(manager,bucket*8)
        while ptr:
            need(0x10000<=ptr<0x80000000 and ptr not in seen and len(seen)<32,'bounded current scheduler graph')
            seen.add(ptr);head=c.get(ptr,48)
            need(word(head,8)==c.main+0x64,'actual scheduler owner')
            rows.append(dict(pointer=ptr,bucket=bucket,head_hex=head.hex()));ptr=word(head,12)
    return manager,rows


def classify(rows):
    return {kind:[r for r in rows if word(bytes.fromhex(r['head_hex']))==vtable]
            for kind,vtable in (('startup',STARTUP),('menu',MENU))}


def sample(c,owned,main_tid,worker_tid,node):
    tids=[main_tid]+([worker_tid] if worker_tid else [])
    with base.original.frozen(c.h,c.pid,tids) as frames:
        need(any(f['tid']==main_tid for f in frames),'actual MAIN context captured')
        manager,rows=graph(c);kinds=classify(rows)
        game=word(c.get(0x7A49FC,4))
        r=dict(elapsed=owned.elapsed(),frames=frames,manager_hex=manager.hex(),registered_tasks=rows,
               MAIN_event_hex=c.get(c.main+0x2C,8).hex(),game=game,
               mouse_hex=c.get(game+0x196C,0x58).hex(),
               timing_pointer=game+0xB17C,timing_hex=c.get(game+0xB17C,0x7C).hex(),
               group10_hex=c.get(game+0x894,8).hex(),group90_hex=c.get(game+0xB14,8).hex())
        need(len(kinds['startup'])<=1 and len(kinds['menu'])<=1,'unique original startup/menu nodes')
        if kinds['startup']:
            current=kinds['startup'][0]['pointer'];head=c.get(current,0x40)
            need(not node or current==node,'same original startup lifetime')
            r['startup_head_hex']=head.hex();r['startup_node']=current
            f=next((f for f in frames if f['tid']==word(head,0x24)),None)
            if f:
                # The callback frame is the one returning to original421F8A.
                callback=next((x for x in f['chain'] if x['return_va']==0x421F8A),None)
                if callback:
                    bp=callback['bp'];locals_raw=c.get(bp-0x80,0x80)
                    r['callback_locals']=dict(pointer=bp-0x80,hex=locals_raw.hex(),
                        this=word(locals_raw,0x7C),counter=word(locals_raw,0x74))
                    need(r['callback_locals']['this']==current,'actual startup callback this')
                returns={x['return_va'] for x in f['chain']}
                if {0x421F8A,0x56E183}<=returns:
                    r['TLS']=base.capture_tls(c,f,current)
                    r['TLS']['index_memory']=dict(pointer=0x761BC0,hex=c.get(0x761BC0,4).hex())
                    if r['TLS']['TLS_index']>=64:
                        pointer=r['TLS']['TEB']+0xF94
                        r['TLS']['expansion_memory']=dict(pointer=pointer,hex=c.get(pointer,4).hex())
        if kinds['menu']:
            r['menu_node']=kinds['menu'][0]['pointer']
        return r


def probe(pid,owned,progress,duration):
    report=dict(pid=pid,samples=[],error=None,host_original_calls=[],host_memory_writes=[],
                host_input_actions=[],native_handoff_observed=False,full_native_instruction_trace=False,
                natural_animation_limit_observed=False,
                normal_PTD_cleanup_proved=False,full_battle_exit_accepted=False)
    c=None;worker=None;node=tid=None
    try:
        need(pid in owned.members(),'owned private process')
        h=base.original.openp(0x100450,False,pid)
        base.original.check(h,'read/query/duplicate-only process handle')
        c=SimpleNamespace(pid=pid,h=h,owned=owned,get=lambda p,n:base.original.required(h,p,n))
        c.main=word(c.get(0x7A4A00,4))
        need(c.main and word(c.get(c.main,4))==0x5986A0,'actual original MAIN')
        name=C.create_unicode_buffer(32768);size=W.DWORD(len(name))
        base.original.check(base.native.image_name(h,0,name,C.byref(size)),'actual private image path')
        need(Path(name.value).resolve()==base.native.APP.resolve(),'private original executable')
        hwnd=base.original.findwindow(b'Cross Hermit',None);wp=W.DWORD()
        main_tid=base.original.ownerpid(hwnd,C.byref(wp));need(wp.value==pid,'same own HWND')
        identity=clone(base.source_identity,RANGES=RANGES,IAT=IAT)
        report.update(main=c.main,process_image=name.value,process_access=0x100450,
                      window=dict(hwnd=hwnd,pid=pid,main_tid=main_tid),
                      source_before=identity(c),TLS_implementation=base.tls_contract(c))
        deadline=time.monotonic()+duration;last_saved=0;last_signature=None;menu_since=None
        while time.monotonic()<deadline:
            exited=bool(worker and base.original.wait(worker,0)==0)
            row=sample(c,owned,main_tid,None if exited else tid,node)
            kinds=classify(row['registered_tasks'])
            if not worker and kinds['startup']:
                head=bytes.fromhex(kinds['startup'][0]['head_hex'])
                if word(head,0x20) and word(head,0x24):
                    node=kinds['startup'][0]['pointer'];tid=word(head,0x24);worker=W.HANDLE()
                    base.original.check(base.parent.duplicate(h,word(head,0x20),base.parent.current_process(),
                        C.byref(worker),0,False,2),'retain original startup thread reference')
                    need(base.get_thread_pid(worker)==pid and base.get_thread_id(worker)==tid,'actual startup worker owner')
                    report['worker']=dict(node=node,thread_id=tid,remote_handle=word(head,0x20),
                                         node_event=base.event_identity(c,word(head,0x1C)),
                                         manager_event=base.event_identity(c,word(c.get(c.main+0x17C,4))))
            if exited and 'worker_exit' not in report:
                code=W.DWORD();base.original.check(base.parent.exit_thread(worker,C.byref(code)),'actual thread exit code')
                report['worker_exit']=dict(thread_id=tid,exit_code=code.value,wait_status=0,
                    before_WM_CLOSE=True,elapsed=owned.elapsed(),natural_return_full_trace_proved=False)
                need(code.value==0,'startup worker exited abnormally; stop without retry')
            row['startup_thread_exited']=exited
            if ('startup_head_hex' in row and bytes.fromhex(row['startup_head_hex'])[0x30]==100
                    and row.get('callback_locals',{}).get('counter',0)>=16204):
                report['natural_animation_limit_observed']=True
            signature=(tuple((r['pointer'],r['head_hex'][:8]) for r in row['registered_tasks']),
                       row['MAIN_event_hex'],row.get('startup_head_hex','')[0x30*2:0x31*2],exited)
            now=time.monotonic()
            if signature!=last_signature or now-last_saved>=1:
                need(len(report['samples'])<1600,'bounded retained native sample budget')
                row['index']=len(report['samples']);report['samples'].append(row)
                last_saved=now;last_signature=signature
                progress.write_text(json.dumps(dict(status='observing_natural_startup',pid=pid,
                    elapsed=owned.elapsed(),counter=row.get('callback_locals',{}).get('counter'),
                    animation_state=bytes.fromhex(row['startup_head_hex'])[0x30] if 'startup_head_hex' in row else None,
                    startup_registered=bool(kinds['startup']),menu_registered=bool(kinds['menu']),
                    worker_exited=exited,samples=len(report['samples']))),encoding='utf8')
            complete=(report['natural_animation_limit_observed'] and exited
                      and report['worker_exit']['exit_code']==0
                      and not kinds['startup'] and len(row['registered_tasks'])==1
                      and kinds['menu'] and word(bytes.fromhex(row['MAIN_event_hex']))==0)
            if complete:
                if menu_since is None:menu_since=now
                if now-menu_since>=1:
                    report.update(native_handoff_observed=True,stop_reason='startup_thread_exited_and_menu_alone')
                    break
            else:menu_since=None
            time.sleep(.02 if row.get('callback_locals',{}).get('counter',0)>16000 else .1)
        report.setdefault('stop_reason','bounded_deadline')
        report['source_after']=identity(c)
        need(report['source_after']==report['source_before'],'original source unchanged during observation')
    except Exception as exc:
        report.update(error=repr(exc),error_traceback=traceback.format_exc(limit=6))
    finally:
        if worker:base.original.close(worker)
        if c:base.original.close(c.h)
    return report


def run(output,duration):
    paths=[Path(__file__),Path(base.__file__),ROOT/'devtools/terminal_scene_resources.py']
    implementations=[base.identity(p) for p in paths]
    report=clone(base.run,run_probe=probe)(output,duration)
    need(implementations==[base.identity(p) for p in paths],
         'observers unchanged throughout native lifetime')
    need(base.sha(PARENT.read_bytes())==PARENT_SHA,'fixed parent asset manifest source')
    with gzip.open(PARENT,'rt',encoding='utf8') as stream:parent=json.load(stream)
    inventory=report['runtime'].pop('immutable_files')
    need(inventory==parent['runtime']['immutable_files'],'fresh asset hashes equal retained parent inventory')
    report['runtime']['immutable_files_reference']=dict(path=PARENT.relative_to(ROOT).as_posix(),sha256=PARENT_SHA,
        rows=len(inventory),freshly_hashed_this_lifetime=True)
    report.update(kind='native_startup_natural_handoff_observation',implementations=implementations,
                  original_scene_roots_called=False,human_operation_required=False,
                  full_resource_lifetime_proved=False,full_battle_exit_accepted=False)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--seconds',type=int,default=600)
    args=parser.parse_args();out=args.out.resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh local bounded output')
    need(30<=args.seconds<=900,'bounded30..900-second natural startup observation')
    result=run(out,args.seconds);raw=json.dumps(result,separators=(',',':')).encode()
    need(len(raw)<=32*1024*1024,'bounded raw observation')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=2*1024*1024,'bounded compressed incremental observation')
    with out.open('xb') as stream:stream.write(packed)
    p=result.get('probe') or {}
    print(json.dumps(dict(report=base.identity(out),handoff=p.get('native_handoff_observed'),
                          error=p.get('error'),lifecycle_error=result['lifecycle']['error'])),flush=True)
    if p.get('error') or result['lifecycle']['error'] or not p.get('native_handoff_observed'):raise SystemExit(1)


if __name__=='__main__':main()
