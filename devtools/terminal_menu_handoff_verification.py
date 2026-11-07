"""Independent bounded verification of recorded original menu continuation.

No native collector or input backend is imported or executed. Successful input
submission, observed input edges, worker exit and successor observation are
separate results. All full battle/resource/replay acceptance remains false.
"""
from __future__ import annotations

import argparse
import functools
import gzip
import json
from pathlib import Path
import struct
import zipfile

from devtools import terminal_scene_owner_verification as owner
from devtools import terminal_startup_handoff_verification as startup
from devtools import terminal_menu_transition_contract as contract

ROOT=owner.ROOT
need=owner.need
word=owner.u32
blob=owner.blob
number=startup.number
MENU=0x59B060
NEW_GAME=0x5A0824
ADV=0x5C306C
LOAD=0x5C8388
WORKROOM=0x5A0904
EXTRA_RANGES=((0x45E8D0,0x45F9A0),(0x49F4E0,0x49F720),
              (0x4B8FF0,0x4B9300),(0x4D9F30,0x4DA550),(0x60CEB0,0x60CEE0))
STORY_RANGES=((0x4D1820,0x4D1B37),(0x4CE210,0x4CE560))
KEY_RANGES=((0x411290,0x411CF0),(0x4128F0,0x412A70),(0x4CCE20,0x4CD060))
INPUT_RANGES=((0x45EFB0,0x45F0CB),(0x45F810,0x45F960),(0x60CEB0,0x60CEE0),
              (0x411DF0,0x4120A0),(0x414400,0x414439))
IMPLEMENTATIONS=('devtools/terminal_menu_handoff.py','devtools/terminal_startup_handoff.py',
                 'devtools/terminal_scene_owner.py','devtools/terminal_scene_resources.py')
INPUT_IMPLEMENTATIONS=('devtools/terminal_menu_input.py','tools/school_native_dialogue_input.py',
                       'tools/school_native_dialogue_desktop.py')
STORY_IMPLEMENTATIONS=('devtools/terminal_story_input.py','devtools/terminal_scene_automation.py',
                       'tools/school_native_dialogue.py','analysis/school-native-dialogue-authorization-v1-20261022.json')
STORY_AUTHORIZATION_SHA='7db2b6b87061595e8f5624ef5220cf0328d9747f59097926047dd962ff191cfb'
V1_SOURCE_SHA='9dfb0e92101b965ff01f20b87f9b426ef582bf3ebafd66afef9685cc87a6458f'
V1_ARCHIVE='analysis/terminal-menu-handoff-observer-v1-20261107.py.gz'
V1_ARCHIVE_SHA='1414ce1f6709ef640f29427743e1d7c46492e5fce1492a1a44520aa531d30f72'
V1_COLLECTOR_SHA='e87fbf4d149d1b7b763e649be628c39e4526a5fce531189ec0468854b48cff76'
V5_SOURCE_SHA='b169a2aff7064e3e6eddf8aefd7c7470031ed826e441bfa18fdf6851bf5d08df'
V5_ARCHIVE='analysis/terminal-menu-implementations-v5-20261107.zip'
V5_ARCHIVE_SHA='b61ba58c6010d1cb0cdff20eae6d99e1593c3f6ca0146dad6537616b9d6a3918'
V5_MEMBERS={
    'devtools/terminal_menu_handoff.py':(16348,'50e3a5389fffe1caed1314bb06225f1899c84363c0474972f19e224fe3f404cf'),
    'devtools/terminal_story_input.py':(4585,'31b1c1ba271b7a2916999cd22c2024a9572247955e06f322a8d95e8b5b20e006'),
}
V6_COLLECTOR_SHA='154efedd03310eee9321c71dd975903ae432dca7f48b5db8ad51f82bc97e9079'
AUTHORIZATION='analysis/terminal-menu-mouse-authorization-v1-20261107.json'
AUTHORIZATION_SHA='711cf7ec337b7d41b9f079a2e3f67ca0c181abb6593eaf602cbe5867ae50e809'
AUTHORIZATION_ARCHIVE='analysis/terminal-menu-implementations-v4-20261107.zip'
AUTHORIZATION_ARCHIVE_SHA='6548365506f4e96ff745b28c571dfbd40ca083b5de92193452a1b7deecda265f'
AUTHORIZATION_MEMBERS={
    'devtools/terminal_menu_handoff.py':(14974,'7ac81a112934243484201ea7e411255a368a182ae9c79bf69ed2f07fbd34088d'),
    'devtools/terminal_menu_input.py':(6969,'22feb6770b4e26d251b845b7ea8992db982de55d28d75537584fee516950ec26'),
    'devtools/terminal_menu_startup.py':(6934,'36b21cb31d1e8a279bd8a7d2ce1810ca3519dbdd16de87632e12b8d325f7afaf'),
}


def authorization_backend():
    archive=ROOT/AUTHORIZATION_ARCHIVE
    data=archive.read_bytes()
    need(len(data)==10367 and owner.sha(data)==AUTHORIZATION_ARCHIVE_SHA,'fixed historical authorization backend archive')
    with zipfile.ZipFile(archive) as z:
        need(len(z.infolist())==len(AUTHORIZATION_MEMBERS)
             and set(z.namelist())==set(AUTHORIZATION_MEMBERS),'exact bounded historical implementation members')
        for path,(size,digest) in AUTHORIZATION_MEMBERS.items():
            need(z.getinfo(path).file_size==size,'historical member size')
            b=z.read(path);need(len(b)==size and owner.sha(b)==digest,'historical member SHA')
    size,digest=AUTHORIZATION_MEMBERS[INPUT_IMPLEMENTATIONS[0]]
    return dict(path=INPUT_IMPLEMENTATIONS[0],bytes=size,sha256=digest)


def read_menu_report(path,digest):
    path=Path(path)
    need(path.stat().st_size<=6*1024*1024,'compressed menu source budget')
    packed=path.read_bytes();need(owner.sha(packed)==digest,'explicit menu report SHA identity')
    with gzip.open(path,'rb') as stream:data=stream.read(64*1024*1024+1)
    need(len(data)<=64*1024*1024,'decompressed menu source budget')
    return json.loads(data)


def archived_v5_sources():
    path=ROOT/V5_ARCHIVE;b=path.read_bytes()
    need(len(b)==7302 and owner.sha(b)==V5_ARCHIVE_SHA,'fixed v5 implementation archive')
    with zipfile.ZipFile(path) as z:
        need(len(z.infolist())==2 and set(z.namelist())==set(V5_MEMBERS),'exact v5 implementation members')
        sources={}
        for name,(size,digest) in V5_MEMBERS.items():
            need(z.getinfo(name).file_size==size,'bounded v5 implementation member')
            data=z.read(name);need(len(data)==size and owner.sha(data)==digest,'v5 archived source bytes')
            sources[name]=data
    return sources


def code_rows(raw,ranges):
    return [dict(pointer=a,bytes=b-a,sha256=owner.sha(raw[a-0x400000:b-0x400000]))
            for a,b in ranges]


def verify_graph(row,main):
    manager=blob(row['manager_hex'],0x120,'complete manager')
    rows=row['registered_tasks']
    need(isinstance(rows,list) and len(rows)<=32,'bounded menu graph')
    nodes={r['pointer']:r for r in rows};need(len(nodes)==len(rows),'unique graph nodes')
    visited=[]
    for bucket in range(32):
        pointer=word(manager,bucket*8)
        while pointer:
            owner.address(pointer,'node pointer')
            need(pointer in nodes and pointer not in visited,'complete acyclic menu graph')
            entry=nodes[pointer];head=blob(entry['head_hex'],48,'registered node')
            need(entry['bucket']==bucket and word(head,8)==main+0x64,'node manager and bucket')
            visited.append(pointer);pointer=word(head,12)
    need(visited==list(nodes),'exact single-linked graph order')
    # bucket+4 is storage with no proven tail meaning; node+10 is not a prev link.
    return nodes,manager


@functools.lru_cache(maxsize=8)
def _module(path,digest):
    import pefile
    p=Path(path)
    need(p.resolve().parent==Path('C:/Windows/SysWOW64').resolve(),'actual x86 system DLL path')
    data=p.read_bytes();need(owner.sha(data)==digest,'recorded system DLL identity')
    pe=pefile.PE(data=data)
    need(pe.FILE_HEADER.Machine==0x14C,'x86 system DLL')
    return pe


def verify_export(row,module,symbol,check_disk=True):
    need(row['module'].lower()==module and row['symbol']==symbol
         and row['target']==row['base']+row['RVA'],'exact cursor module/export target')
    owner.address(row['target'],'OS export target');owner.address(row['base'],'OS module base')
    need(Path(row['module_path']).name.lower()==module,'cursor DLL filename')
    if check_disk:
        pe=_module(row['module_path'],row['module_sha256'])
        export=next((x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==symbol.encode()),None)
        need(export is not None and export.forwarder is None and export.address==row['RVA'],
             'actual cursor export RVA')


def verify_guard(row,raw,pid,main,game,hwnd,menu_node,menu_tid,check_disk=True):
    need((row['pid'],row['main'],row['game'],row['hwnd'],row['node'])==
         (pid,main,game,hwnd,menu_node),'input guard exact owners')
    head=blob(row['head_hex'],64,'guard node header')
    need(word(head)==MENU and word(head,8)==main+0x64 and word(head,12)==0
         and word(head,0x24)==menu_tid and word(head,0x30)==1,'guard original ready menu')
    manager=blob(row['manager_hex'],0x120,'guard manager')
    need([word(manager,i*8) for i in range(32)].count(menu_node)==1
         and all(word(manager,i*8) in (0,menu_node) for i in range(32)), 'guard sole menu graph')
    need(word(blob(row['MAIN_event_hex'],8,'guard MAIN event'))==0,'idle guard MAIN event')
    frame=row['frame'];owner.verify_frame(frame)
    need(frame['tid']==menu_tid,'guard menu thread')
    waits=[r for r in frame['chain'] if r['return_va']==0x45F065]
    need(len(waits)==1 and waits[0]['saved_bp']==row['selector_pointer'],'actual ready selector ancestor')
    selector=blob(row['selector_hex'],0x1C,'selector locals and caller')
    need(word(selector,12)==menu_node and word(selector,20)==0x45EE6A
         and 0<word(selector)<3660,'original selector this/caller/countdown')
    matched=[r for r in frame['chain'] if r['bp']==row['selector_pointer']]
    need(len(matched)==1 and matched[0]['return_va']==0x45EE6A
         and matched[0]['saved_bp']==word(selector,16),'selector raw frame link')
    need(word(blob(row['input_HWND_hex'],4,'input HWND'))==hwnd
         and word(blob(row['coordinate_mode_hex'],4,'coordinate mode')) in (0,1),'original cursor mode and window')
    blob(row['cursor_hex'],8,'guard cursor')
    need(row['code']==code_rows(raw,INPUT_RANGES),'all input code and rectangle bytes')
    exports=row['producer_exports'];need(set(exports)=={'5841772','5841768'},'exact cursor IAT slots')
    expected=((0x59236C,'GetCursorPos'),(0x592368,'ScreenToClient'))
    need([r['slot'] for r in row['IAT']]==[p for p,_ in expected],'complete cursor IAT observations')
    for (slot,symbol),iat in zip(expected,row['IAT']):
        export=exports[str(slot)]
        verify_export(export,'user32.dll',symbol,check_disk)
        need(word(blob(iat['hex'],4,'cursor IAT'))==export['target'],'live cursor IAT binding')
    need(row['all_threads_resumed_before_input'] is True,'input only after snapshot resumes')


def verify_geometry(geometry,target,hwnd,coordinate_mode,normalized=None):
    point=geometry['screen_target'];desktop=geometry['virtual_desktop'];rectangle=geometry['window_rect']
    need(len(point)==2 and len(desktop)==len(rectangle)==4
         and all(type(x) is int for x in point+desktop+rectangle),'integer complete absolute input geometry')
    x,y=point;left,top,width,height=desktop;l,t,r,b=rectangle
    need(width>1 and height>1 and left<=x<left+width and top<=y<top+height,
         'absolute target inside virtual desktop')
    need(l<=x<r and t<=y<b and geometry['point_window']==hwnd,'absolute target belongs to current unobscured window')
    need(geometry['coordinate_mode']==coordinate_mode and coordinate_mode in (0,1),'same original coordinate mode')
    if coordinate_mode==0:need(point==list(target),'original fullscreen screen coordinates')
    if normalized is not None:
        def nearest_even(n,d):
            q,remainder=divmod(n,d)
            return q+int(2*remainder>d or (2*remainder==d and q%2==1))
        expected=[nearest_even((x-left)*65535,width-1),nearest_even((y-top)*65535,height-1)]
        need(normalized==expected and all(type(v) is int and 0<=v<=65535 for v in normalized),
             'absolute virtual desktop normalized coordinates')


def verify_input(p,raw,game,hwnd,menu_worker,check_disk=True):
    controller=p.get('mouse_controller');actions=p['collector_input_actions']
    need(isinstance(actions,list) and len(actions)<=1,'at most one menu input action')
    if controller is None:
        need(actions==[],'no hidden collector input')
        return dict(attempted=False,input_edges_observed=False)
    need(controller['user_override_required'] is True and controller['maximum_clicks']==1,
         'explicit one-click input scope')
    need(type(controller['attempted']) is bool,'attempted bool')
    if not controller['attempted']:
        need(controller['receipt'] is None and actions==[],'no attempted input receipt')
        return dict(attempted=False,input_edges_observed=False)
    receipt=controller['receipt']
    need(actions==[receipt] and receipt['error'] is None,'one identical successful bounded input receipt')
    index=receipt['index'];need(type(index) is int and index in (0,1),'only reviewed menu choices')
    target=(318,508 if index==0 else 540)
    before=number(receipt['before_elapsed'],'input before');after=number(receipt['after_elapsed'],'input after')
    need(0<after-before<=12,'bounded input elapsed interval')
    activation=receipt['activation']
    need(activation['hwnd']==activation['after']==hwnd and len(activation['operations'])<=1,
         'owned foreground activation')
    need(all(r==dict(name='SetForegroundWindow',result=True) for r in activation['operations']),
         'bounded owned activation operation')
    action=receipt['action'];owner.false_fields(action,('game_memory_written','transition_proved'))
    need(action['error'] is None and action.get('release_error') is None
         and action['down_submitted'] is True and action['released'] is True
         and action['down_result']==1 and action['up_results']==[1],'single successful down/up submission')
    need(action['target']==list(target) and action['before_click']==list(target),'actual cursor at original menu target')
    down=action['down_wall_time_ns'];up=action['up_wall_time_ns']
    need(type(down) is int and type(up) is int and 0<(up-down)/1e9<=.25,'bounded down/up wall interval')
    movement_mode=action.get('movement_mode','relative_feedback')
    need(movement_mode in ('relative_feedback','absolute_virtual_desktop'),'known reviewed movement mode')
    moves=action['moves'];need(isinstance(moves,list) and len(moves)<=4,'bounded movement')
    for move in moves:
        need(len(move['before'])==2 and move['submitted']==1,'submitted mouse movement')
        if movement_mode=='relative_feedback':
            need(move['delta']==[max(-512,min(512,target[i]-move['before'][i])) for i in range(2)],
                 'feedback bounded relative movement')
        else:need(move['flags']==0xC001,'absolute move/virtual desktop flags')
    guards=action['guard_observations']
    need(4<=len(guards)<=12,'bounded complete input guards')
    for guard in guards:
        verify_guard(guard,raw,p['pid'],p['main'],game,hwnd,menu_worker['pointer'],
                     menu_worker['thread_id'],check_disk)
        need(word(bytes.fromhex(guard['manager_hex']),0x118)==p['manager_event']['remote_handle'],
             'input guard same manager Event')
    need(tuple(struct.unpack('<ii',bytes.fromhex(guards[-1]['cursor_hex'])))==target,
         'last suspended original cursor equals requested target')
    if movement_mode=='absolute_virtual_desktop':
        modes={word(bytes.fromhex(g['coordinate_mode_hex'])) for g in guards}
        need(len(modes)==1,'coordinate mode stable throughout input guards')
        mode=modes.pop()
        for move in moves:verify_geometry(move['geometry'],target,hwnd,mode,move['normalized'])
        need('click_geometry' in action,'final geometry checked even without movement')
        verify_geometry(action['click_geometry'],target,hwnd,mode)
    samples=receipt['input_samples'];need(2<=len(samples)<=1025,'bounded raw input samples')
    times=[number(s['elapsed'],'input sample elapsed') for s in samples]
    walls=[s['wall_time_ns'] for s in samples]
    need(all(type(t) is int and t>0 for t in walls)
         and all(a<=b for a,b in zip(times,times[1:]))
         and all(a<=b for a,b in zip(walls,walls[1:])), 'ordered input sample clocks')
    need(before<=times[0]<=times[-1]<=after and walls[0]<=down<up<=walls[-1],
         'input submission inside raw observation interval')
    need(abs((times[-1]-times[0])-(walls[-1]-walls[0])/1e9)<=.05,
         'input wall and elapsed clock durations agree')
    pressed=[];held=[];released=[];incoherent=[]
    for i,s in enumerate(samples):
        mouse=blob(s['mouse_hex'],0x58,'actual raw mouse')
        pending=blob(s['MAIN_event_hex'],8,'input MAIN event');need(word(pending) in (0,1),'input event flag')
        previous,current,press,release=(word(mouse,o) for o in (0x1C,0x20,0x24,0x30))
        if press!=((previous^current)&current) or release!=((previous^current)&previous):
            # ReadProcessMemory here does not suspend the original producer.
            incoherent.append(i);continue
        if tuple(struct.unpack_from('<ii',mouse))!=target:continue
        if current&1 and down<=walls[i]<=up:held.append(i)
        if press&1 and down<=walls[i]<=up:pressed.append(i)
        if release&1 and walls[i]>=up:released.append(i)
    observed=bool(pressed and held and released and min(pressed)<max(released))
    return dict(attempted=True,index=index,input_edges_observed=observed,movement_mode=movement_mode,
                press_samples=pressed,held_samples=held,release_samples=released,
                asynchronous_incoherent_samples=incoherent,input_after_elapsed=after,
                down_to_up_ms=(up-down)/1e6)


def verify_startup_gate(report,raw):
    """Independent campaign prerequisite, not the frozen animation proof."""
    p=report['probe']['startup'];life=report['lifecycle'];ready=life['ready']
    need(p.get('gate_contract')=='original_startup_retired_v1','explicit startup retirement contract')
    owner.false_fields(p,('retirement_trigger_proved','full_native_instruction_trace',
                          'normal_PTD_cleanup_proved','full_battle_exit_accepted'))
    need(p['error'] is None and p['host_original_calls']==p['host_memory_writes']==p['host_input_actions']==[],
         'successful read-only no-input startup gate')
    need(p['process_access']==0x100450 and Path(p['process_image']).resolve()==(ROOT/owner.APP).resolve(),
         'exact read-only private process')
    pid=p['pid'];main=p['main'];game=ready['game']['pointer'];window=p['window'];worker=p['worker']
    node=worker['node'];tid=worker['thread_id'];main_tid=window['main_tid']
    need((pid,main)==(ready['pid'],ready['main']['pointer'])
         and (window['pid'],main_tid,window['hwnd'])==
         (pid,ready['window']['tid'],ready['window']['hwnd']) and tid!=main_tid,
         'same startup process, window and distinct original threads')
    expected=owner.source_rows(raw)+code_rows(raw,startup.EXTRA_RANGES+startup.V2_RANGES)
    source=p['source_before']
    need(source==p['source_after'] and source['code']==expected,'complete gate original live ranges unchanged')
    need([r['slot'] for r in source['IAT']]==list(startup.V2_IAT)
         and all(word(blob(r['hex'],4,'gate IAT'))>=0x10000 for r in source['IAT']), 'complete gate IAT')
    owner.verify_tls_implementation(p['TLS_implementation'])
    startup.verify_event(worker['node_event'],pid,'startup node')
    startup.verify_event(worker['manager_event'],pid,'startup manager')
    need(worker['node_event']['remote_handle']!=worker['manager_event']['remote_handle'],'distinct startup events')
    owner.address(node,'startup node');owner.address(tid,'startup TID');owner.address(worker['remote_handle'],'startup handle')
    samples=p['samples'];need(1<=len(samples)<=1600,'bounded startup gate samples')
    need([r['index'] for r in samples]==list(range(len(samples))),'startup gate sample indices')
    times=[number(s['elapsed'],'gate sample time') for s in samples]
    need(all(a<=b for a,b in zip(times,times[1:])),'ordered gate samples')
    exited_seen=False;counter_before=None;tls_identity=None;tls_count=0
    thresholds=[];presses=[];startup_seen=[];menu_suffix=[];menu_node=None
    for i,s in enumerate(samples):
        nodes,manager,kinds=startup.verify_graph(s,main)
        need(word(manager,0x118)==worker['manager_event']['remote_handle'],'same raw startup manager Event')
        pending=blob(s['MAIN_event_hex'],8,'gate pending event');need(word(pending) in (0,1),'gate pending flag')
        need(s['game']==game and s['timing_pointer']==game+0xB17C,'same startup game/timing')
        for name,size in [('timing_hex',0x7C),('mouse_hex',0x58),('group10_hex',8),('group90_hex',8)]:blob(s[name],size,name)
        exited=s['startup_thread_exited'];need(type(exited) is bool and (not exited_seen or exited),'no startup resurrection')
        exited_seen|=exited
        frames=s['frames'];need(1<=len(frames)<=2 and len({f['tid'] for f in frames})==len(frames),'gate unique MAIN/worker frames')
        need(any(f['tid']==main_tid for f in frames),'gate MAIN frame')
        for f in frames:
            need(f['tid'] in (main_tid,tid),'only designated gate threads');owner.verify_frame(f)
        wf=next((f for f in frames if f['tid']==tid),None)
        need(not exited or wf is None,'no startup context after signaled exit')
        if kinds[startup.STARTUP]:
            startup_seen.append(i)
            need(kinds[startup.STARTUP]==[node] and s['startup_node']==node,'same original startup node')
            head=blob(s['startup_head_hex'],64,'startup raw header')
            need(head[:48].hex()==nodes[node]['head_hex'] and head[0x28]==1,'same startup header/autodelete')
            if word(head,0x20):
                need((word(head,0x20),word(head,0x24),word(head,0x1C))==
                     (worker['remote_handle'],tid,worker['node_event']['remote_handle']),'same startup native thread/Event')
            if word(bytes.fromhex(s['mouse_hex']),0x24)&1:presses.append(i)
            if 'callback_locals' in s:
                local=s['callback_locals'];b=blob(local['hex'],128,'actual startup locals')
                need(wf is not None,'startup locals require worker context')
                cf=[f for f in wf['chain'] if f['return_va']==0x421F8A]
                need(len(cf)==1 and local['pointer']==cf[0]['bp']-0x80,'startup locals exact callback')
                need(local['this']==word(b,0x7C)==node and local['counter']==word(b,0x74),'raw startup this/counter')
                counter=local['counter']
                if counter!=0xCCCCCCCC:
                    need(counter<=16205 and (counter_before is None or counter>=counter_before),'bounded monotonic startup counter')
                    counter_before=counter
                    if head[0x30]==100 and counter>=16204:thresholds.append(i)
                if 'TLS' in s:
                    startup.verify_tls(s['TLS'],wf,head,node,tid,pid,local,2);tls_count+=1
                    current=tuple(s['TLS'][k] for k in ('TEB','FS','TLS_index','slot','PTD'))+(local['pointer'],)
                    if tls_identity is None:tls_identity=current
                    need(current==tls_identity,'same startup TEB/TLS/PTD/callback lifetime')
            else:need('TLS' not in s,'no unbound startup TLS')
        else:
            need(not any(k in s for k in ('startup_head_hex','startup_node','callback_locals','TLS')),
                 'no stale startup dereference after graph retirement')
        if kinds[startup.MENU]:
            current=kinds[startup.MENU][0]
            need(s['menu_node']==current and menu_node in (None,current),'same original successor menu')
            menu_node=current
        else:need('menu_node' not in s,'no invented menu pointer')
        if exited and not kinds[startup.STARTUP] and len(nodes)==1 and kinds[startup.MENU] and word(pending)==0:
            menu_suffix.append(i)
        else:menu_suffix=[]
    need(startup_seen and tls_count,'actual original startup full owner observations')
    need(p['natural_animation_limit_observed'] is bool(thresholds)
         and p['original_mouse_press_sampled'] is bool(presses),'trigger observations derived only from retained bytes')
    ex=p.get('worker_exit');need(ex is not None,'current retained worker exit required for gate')
    need(ex['thread_id']==tid and type(ex['exit_code']) is int and ex['exit_code']==0
         and ex['wait_status']==0 and ex['before_WM_CLOSE'] is True
         and ex['natural_return_full_trace_proved'] is False and exited_seen,'same startup exit0 before cleanup')
    exit_time=number(ex['elapsed'],'gate worker exit time')
    need(times[0]<=exit_time<=times[-1]+1,'gate exit in observation interval')
    qualified=bool(menu_suffix and times[menu_suffix[-1]]-times[menu_suffix[0]]>=1)
    need(p['native_handoff_observed'] is qualified and qualified,'qualified retained startup retirement and stable menu')
    need(p['stop_reason']=='original_startup_exit0_and_menu_alone','explicit retired startup stop reason')
    life_time=life['lifetime']
    need(life_time['forced_termination'] is False and life_time['members_after_cleanup']==[]
         and any(pid in r['pids'] for r in life_time['membership']),'owned Job drained without forced termination')
    members={p for r in life_time['membership'] for p in r['pids']};exits=life_time['exits']
    need({str(p) for p in members}==set(exits) and life_time['parent_pid'] in members
         and all(e['signaled'] is True and type(e['code']) is int and 0<=e['code']<=0xFFFFFFFF for e in exits.values()),
         'complete owned process exit statuses')
    need(life_time['child_status_is_not_WinMain_return'] is True,'protected child is not WinMain return')
    close=life['close_request']
    need(close['pid']==pid and close['hwnd']==window['hwnd'] and close['message']==16 and close['posted'] is True,
         'owned later WM_CLOSE')
    return dict(native_handoff_observed=True,cleanup_process_exits=exits,gate_contract=p['gate_contract'],
                natural_animation_limit_observed=bool(thresholds),original_mouse_press_sampled=bool(presses),
                retirement_trigger_proved=False)


def vm_dispatch_contract(raw):
    """Original fetch/dispatch writes opcode and length before advancing PC."""
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    decoder=Cs(CS_ARCH_X86,CS_MODE_32)
    checks={0x4CE9DD:('mov','word ptr [edx + ecx + 0x22], ax'),
            0x4CE9FB:('mov','word ptr [edx + ecx + 0x24], ax'),
            0x4CEEDE:('call','0x4c6aa0'),
            0x4CFEF2:('mov','dword ptr [eax + edx + 0x1c], ecx'),
            0x4CFF0C:('mov','word ptr [edx + ecx + 0x20], ax')}
    need(word(raw,0x4D03CF-0x400000+(40-5)*4)==0x4CEECC,'original opcode40 dispatch table')
    rows=[]
    for address,expected in checks.items():
        instruction=next(decoder.disasm(raw[address-0x400000:address-0x400000+15],address))
        need((instruction.mnemonic,instruction.op_str)==expected,'original VM dispatch update order')
        rows.append(dict(address=address,hex=instruction.bytes.hex(),instruction=instruction.mnemonic+' '+instruction.op_str))
    return rows


def verify_story_actions(p,raw,game,hwnd,workers,maximum_allowed=96):
    present='collector_story_input_actions' in p
    if not present:
        need('maximum_story_confirmations' not in p and 'collector_input_actions_scope' not in p,
             'no undeclared story input metadata')
        return []
    need(p['collector_input_actions_scope']=='mouse_menu_only','mouse and story actions explicitly separated')
    maximum=p['maximum_story_confirmations'];actions=p['collector_story_input_actions']
    need(type(maximum) is int and 1<=maximum<=maximum_allowed and isinstance(actions,list) and len(actions)<=maximum,
         'bounded declared story action budget')
    need(p.get('mouse_controller',{}).get('attempted') is True and len(p['collector_input_actions'])==1,
         'story follows current one-menu flow')
    from tools.school_native_dialogue_verification import OriginalKeyQuery
    vm_dispatch_contract(raw)
    query=OriginalKeyQuery();results=[];keys=set();last_after=0
    for action in actions:
        owner.false_fields(action,('game_memory_written','full_instruction_causality_proved'))
        need(action['error'] is None,'successful bounded story action')
        before=number(action['before_elapsed'],'story before');after=number(action['after_elapsed'],'story after')
        need(last_after<=before<after<=before+10,'ordered bounded story actions');last_after=after
        key=action['key'];need(isinstance(key,list) and len(key)==3 and tuple(key) not in keys,'no story confirmation retry')
        keys.add(tuple(key));node,program,pc=key
        owner.address(node,'story node');owner.address(program,'story program')
        need(type(pc) is int and 0<=pc<0x1000000,'bounded actual story PC')
        row=action['before_sample'];nodes,manager=verify_graph(row,p['main'])
        need(row['game']==game and row['elapsed']<=before and len(row['tasks'])==len(nodes)==1,
             'current sole ADV input owner')
        task=row['tasks'][0];head=blob(task['header_hex'],64,'story original task header')
        need(task['pointer']==node and list(nodes)==[node] and task['vtable']==word(head)==ADV
             and head[:48].hex()==nodes[node]['head_hex'],'same original ADV registered node')
        need(blob(task['vtable_hex'],8,'story vtable')==raw[ADV-0x400000:ADV-0x400000+8],
             'original ADV callback/destructor')
        tid=task['thread_id'];need(tid==word(head,0x24) and (node,tid) in workers,'retained original ADV worker')
        worker=workers[(node,tid)]
        need(worker['vtable']==ADV and word(head,0x20)==worker['original_handle']
             and word(head,0x1C)==worker['event']['remote_handle'],'same ADV thread and node Event')
        need(word(manager,0x118)==p['manager_event']['remote_handle'],'story same manager Event')
        frames=row['frames'];need(len({f['tid'] for f in frames})==len(frames),'story unique complete frames')
        need(1<=len(frames)<=256 and any(f['tid']==p['startup']['window']['main_tid'] for f in frames),
             'story complete MAIN and worker context set')
        for frame in frames:owner.verify_frame(frame)
        frame=next((f for f in frames if f['tid']==tid),None)
        need(frame is not None and 'TLS' in task,'actual ADV original callback and TLS')
        callbacks=[f for f in frame['chain'] if f['return_va']==0x421F8A]
        need(len(callbacks)==1,'one original ADV callback')
        startup.verify_tls(task['TLS'],frame,head,node,tid,p['pid'],{'pointer':callbacks[0]['bp']-0x80},2)
        vm=blob(row['VM_hex'],128,'story initial VM')
        for name,size in [('keyboard_hex',0xA00),('mouse_hex',0x58),('scenario_hex',80),('group90_hex',8),('MAIN_event_hex',8)]:
            blob(row[name],size,'story before '+name)
        need(vm[4]!=0 and (word(vm,16),word(vm,28))==(program,pc)
             and struct.unpack_from('<HH',vm,32)==(1,51),'original active ADV opcode51 wait')
        # The collector calls this only after a stable retained/task-owned wait.
        matching=[]
        for s in reversed([s for s in p['samples'] if s['elapsed']<=row['elapsed']]):
            v=bytes.fromhex(s['VM_hex']);tasks=s['tasks']
            if not (len(tasks)==1 and tasks[0]['pointer']==node and tasks[0]['vtable']==ADV
                    and v[4] and (word(v,16),word(v,28))==(program,pc)
                    and struct.unpack_from('<HH',v,32)==(1,51)):break
            matching.append(s['elapsed'])
        # row.elapsed precedes its frozen reads; first input sample is later,
        # still before key-down and independently checked below for the same
        # active wait/program/PC and released key. Use that actual raw endpoint.
        samples=action['samples'];need(3<=len(samples)<=256,'bounded story input samples')
        first_input_time=number(samples[0]['elapsed'],'first raw story input time')
        need(matching and first_input_time-min(matching)>=1-1e-6,
             'observed stable original story wait before input')
        need(action['input_code_identity']==code_rows(raw,KEY_RANGES),'live original story input ranges')
        activation=action['activation']
        need(activation['hwnd']==activation['after']==hwnd and len(activation['operations'])<=1
             and all(x==dict(name='SetForegroundWindow',result=True) for x in activation['operations']),
             'owned story foreground activation')
        need([s['index'] for s in samples]==list(range(len(samples))),'contiguous story input samples')
        times=[number(s['elapsed'],'story sample time') for s in samples]
        need(before<=times[0]<=times[-1]<=after and all(a<=b for a,b in zip(times,times[1:])),'ordered story sample times')
        walls=[s['wall_time_ns'] for s in samples]
        need(all(type(t) is int and t>0 for t in walls) and all(a<=b for a,b in zip(walls,walls[1:])),
             'ordered story wall times')
        states=[];pcs=[];dispatch_samples=[]
        for s in samples:
            need(s['foreground_hwnd']==hwnd,'same actual story foreground')
            keyboard=blob(s['keyboard_hex'],0xA00,'complete story keyboard');v=blob(s['VM_hex'],128,'story VM')
            blob(s['mouse_hex'],0x58,'story mouse')
            states.append(query.query(keyboard));pcs.append(word(v,28))
            if not any(states):
                need(v[4]!=0 and word(v,16)==program and struct.unpack_from('<HH',v,32)==(1,51),
                     'same active original story wait before first press')
            elif all(x==pc for x in pcs):
                need(v[4]!=0 and word(v,16)==program,'active same-program story consumption before PC advancement')
                opcode=struct.unpack_from('<H',v,34)[0]
                if opcode!=51:
                    length=struct.unpack_from('<H',v,36)[0]
                    need(opcode==40 and struct.unpack_from('<H',v,32)[0]==0 and 0<length<=0x1000,
                         'original opcode40 dispatch phase before PC advancement')
                    dispatch_samples.append(dict(index=s['index'],opcode=opcode,length=length,PC=pc))
        need(states[0]==0 and pcs[0]==pc and set(states)<={0,1},'original key initially released')
        press=next((i for i,x in enumerate(states) if x),None)
        need(press is not None,'original story key query observes press')
        release=next((i for i in range(press+1,len(states)) if not states[i]),None)
        advance=next((i for i,x in enumerate(pcs) if x!=pc),None)
        need(release is not None and advance is not None and advance>=press,'original story release and PC advance')
        for dispatch in dispatch_samples:
            after_vm=bytes.fromhex(samples[advance]['VM_hex'])
            need(dispatch['index']>=press and dispatch['index']<advance
                 and word(after_vm,16)==program and pcs[advance]==pc+dispatch['length']
                 and struct.unpack_from('<H',after_vm,34)[0]==dispatch['opcode'],
                 'observed dispatch phase followed by exact original command-length PC advancement')
        transition=dict(press_index=press,release_index=release,advanced_index=advance,before_PC=pc,
                        after_PC=pcs[advance],transition_observed=True,full_instruction_causality_proved=False)
        need(action['transition']==transition,'independently derived story transition')
        backend=action['backend'];need(set(backend)=={'receipt'},'one successful bounded story backend')
        receipt=backend['receipt']
        need(receipt['scan_code']==0x39 and receipt['hold_ms']==receipt['maximum_hold_ms']==120
             and receipt['hold_ms_is_ceiling'] is True
             and receipt['hold_policy']=='release_on_first_observed_VM_advance_or_120ms','authorized bounded story key policy')
        need(receipt['input_returned'] is True and receipt['released'] is True
             and receipt['down_submitted'] is True and receipt['up_attempted'] is True
             and receipt['down_result']==1 and receipt['up_results']==[1],'actual guarded story down/up submission')
        need((receipt['hwnd'],receipt['pid'])==(hwnd,p['pid']) and receipt['existing_process_memory_written'] is False,
             'exact story input owner and no game writes')
        need(walls[0]<=receipt['down_wall_time_ns']<=receipt['up_wall_time_ns']<=walls[-1], 'story input bracketed by samples')
        need(receipt['start_ns']<=receipt['down_ns']<=receipt['up_ns']<=receipt['end_ns'],'story monotonic backend clocks')
        hold=receipt['up_ns']-receipt['down_ns'];wall_hold=receipt['up_wall_time_ns']-receipt['down_wall_time_ns']
        need(0<hold<=120_000_000 and abs(hold-wall_hold)<=25_000_000,'actual story hold limit and clock tolerance')
        need(abs((receipt['end_ns']-receipt['start_ns'])-
                 (receipt['end_wall_time_ns']-receipt['start_wall_time_ns']))<=25_000_000,'story backend clock durations agree')
        results.append(dict(node=node,program=program,original_key_query_replays=len(samples),
                            ready_task_snapshot_seconds=row['elapsed']-min(matching),
                            ready_VM_sample_seconds=first_input_time-min(matching),
                            ready_decision_seconds=before-min(matching),
                            opcode_dispatch_samples=dispatch_samples,
                            observed_hold_ns=hold,**transition))
    return results


def verify_ready_owner(row,p,raw,game,worker,vtable,wait_return=None):
    nodes,manager=verify_graph(row,p['main'])
    need(row['game']==game and len(nodes)==len(row['tasks'])==1,'sole original ready task')
    task=row['tasks'][0];head=blob(task['header_hex'],64,'ready task complete header')
    need(task['pointer']==worker['pointer'] and list(nodes)==[worker['pointer']]
         and task['vtable']==word(head)==vtable and head[:48].hex()==nodes[task['pointer']]['head_hex'],
         'same ready task/vtable/registered header')
    need(blob(task['vtable_hex'],8,'ready original vtable')==raw[vtable-0x400000:vtable-0x400000+8],
         'ready original callback/destructor')
    need(word(manager,0x118)==p['manager_event']['remote_handle'],'ready task same manager Event')
    need(task['thread_id']==word(head,0x24)==worker['thread_id'] and word(head,0x20)==worker['original_handle']
         and word(head,0x1C)==worker['event']['remote_handle'],'ready actual worker/event identity')
    need(word(blob(row['MAIN_event_hex'],8,'ready MAIN event'))==0,'ready MAIN idle')
    for name,size in [('keyboard_hex',0xA00),('mouse_hex',0x58),('scenario_hex',80),('VM_hex',128),('group90_hex',8)]:
        blob(row[name],size,'ready '+name)
    frames=row['frames'];need(1<=len(frames)<=256 and len({f['tid'] for f in frames})==len(frames),
                             'bounded complete ready contexts')
    need(any(f['tid']==p['startup']['window']['main_tid'] for f in frames),'ready MAIN context')
    for frame in frames:owner.verify_frame(frame)
    frame=next((f for f in frames if f['tid']==worker['thread_id']),None)
    need(frame is not None and 'TLS' in task,'ready worker original TLS')
    callbacks=[f for f in frame['chain'] if f['return_va']==0x421F8A]
    need(len(callbacks)==1,'ready original callback ancestor')
    startup.verify_tls(task['TLS'],frame,head,task['pointer'],worker['thread_id'],p['pid'],
                       {'pointer':callbacks[0]['bp']-0x80},2)
    if wait_return is not None:
        waits=[f for f in frame['chain'] if f['return_va']==wait_return]
        need(len(waits)==1,'ready original wait ancestor')
        if vtable==MENU:
            need(word(head,0x30)==1 and any(f['bp']==waits[0]['saved_bp'] and f['return_va']==0x45EE6A
                for f in frame['chain']),'ready selector stage/caller')
    return task


def verify_budget_stop(p,raw,game,workers,results):
    if p['stop_reason']!='story_confirmation_budget':
        need('story_budget_wait_sample' not in p,'no unclaimed story budget stop sample')
        return None
    need('collector_story_input_actions' in p and len(results)==p['maximum_story_confirmations'],
         'story budget stop occurs exactly at declared completed action count')
    row=p.get('story_budget_wait_sample');need(isinstance(row,dict),'complete retained unconsumed budget wait')
    need(len(row['tasks'])==1,'one budget-wait task')
    task=row['tasks'][0];key=(task['pointer'],task['thread_id'])
    need(key in workers,'retained budget-wait worker')
    verify_ready_owner(row,p,raw,game,workers[key],ADV)
    vm=bytes.fromhex(row['VM_hex']);program=word(vm,16);pc=word(vm,28)
    need(vm[4] and struct.unpack_from('<HH',vm,32)==(1,51),'budget stops at original unconsumed opcode51')
    need(not bytes.fromhex(row['keyboard_hex'])[0x4B9]&0x80,'budget stop key released')
    completed=p['collector_story_input_actions'];wait_key=[task['pointer'],program,pc]
    need(all(a['key']!=wait_key for a in completed),'budget stop did not retry or consume current wait')
    elapsed=number(row['elapsed'],'budget wait time')
    need(elapsed>=completed[-1]['after_elapsed'],'budget wait follows last completed confirmation')
    suffix=[]
    for s in reversed([s for s in p['samples'] if s['elapsed']<=elapsed]):
        v=bytes.fromhex(s['VM_hex']);ts=s['tasks']
        if not (len(ts)==1 and ts[0]['pointer']==task['pointer'] and ts[0]['vtable']==ADV
                and v[4] and (word(v,16),word(v,28))==(program,pc)
                and struct.unpack_from('<HH',v,32)==(1,51)):break
        suffix.append(s['elapsed'])
    return dict(node=task['pointer'],thread_id=task['thread_id'],program=program,PC=pc,
                observed_wait_span_seconds=elapsed-min(suffix) if suffix else 0,
                completed_confirmations=len(results),next_confirmation_submitted=False,
                chapter_completion_proved=False)


def verify_report(report,raw,check_disk=True):
    contract.authenticate(raw)
    need(report['schema_version']==1 and report['kind']=='original_menu_continuation_observation','menu source schema')
    collector_sha=report['implementations'][0]['sha256']
    need(collector_sha in (V1_COLLECTOR_SHA,V5_MEMBERS[IMPLEMENTATIONS[0]][1],V6_COLLECTOR_SHA),
         'explicit reviewed menu collector generation')
    generation=6 if collector_sha==V6_COLLECTOR_SHA else 5 if collector_sha==V5_MEMBERS[IMPLEMENTATIONS[0]][1] else 1
    owner.false_fields(report,('accepted','old_terminal_cases_replayed','independent_full_replay',
        'full_native_instruction_or_API_trace','R3_complete','R4_complete','R5_complete','R6_complete',
        'human_operation_required','host_game_roots_called','full_battle_exit_accepted'))
    p=report['probe'];life=report['lifecycle'];ready=life['ready']
    need(p['error'] is None and life['error'] is None,'successful bounded menu observation')
    owner.false_fields(p,('full_native_instruction_trace','full_battle_exit_accepted'))
    need(p['host_game_calls']==p['host_memory_writes']==[],'no host game calls or writes')
    owner.false_fields(life,('original_code_written','original_registers_written','original_IAT_written'))
    # Adapt only the wrapper schema for the separately implemented startup
    # verifier. These false values constrain the proof; they do not invent data.
    if 'gate_contract' in p['startup']:
        startup_result=verify_startup_gate(report,raw)
    else:
        startup_view=dict(report,kind='native_startup_natural_handoff_observation',probe=p['startup'],
                          original_scene_roots_called=report['host_game_roots_called'],
                          full_resource_lifetime_proved=False)
        startup_result=startup.verify_report(startup_view,raw)
    need(startup_result['native_handoff_observed'],'same lifetime startup must naturally retire first')
    need((p['pid'],p['main'])==(p['startup']['pid'],p['startup']['main'])==(ready['pid'],ready['main']['pointer']),
         'same native menu/startup owner')
    game=ready['game']['pointer'];hwnd=ready['window']['hwnd'];main_tid=ready['window']['tid']
    activations=report.get('startup_activation',[])
    need(isinstance(activations,list) and len(activations)<=1,'bounded early owned activation')
    for activation in activations:
        number(activation['elapsed'],'early activation time')
        if 'error' in activation:
            need(set(activation)=={'elapsed','error'} and isinstance(activation['error'],str),
                 'explicit early activation failure only')
        else:
            need(activation['hwnd']==activation['after']==hwnd and len(activation['operations'])<=1
                 and all(x==dict(name='SetForegroundWindow',result=True) for x in activation['operations']),
                 'successful early activation only targets current owned window')
    source=p['source_before']
    expected=owner.source_rows(raw)+code_rows(raw,startup.EXTRA_RANGES+startup.V2_RANGES+EXTRA_RANGES)
    extended=expected+code_rows(raw,STORY_RANGES)
    need(source==p['source_after'] and source['code'] in (expected,extended),'complete live menu ranges unchanged')
    if 'collector_story_input_actions' in p:need(source['code']==extended,'story requires extended ADV live code identity')
    need([r['slot'] for r in source['IAT']]==list(startup.V2_IAT)
         and all(word(blob(r['hex'],4,'menu IAT'))>=0x10000 for r in source['IAT']), 'complete menu IAT')
    owner.verify_tls_implementation(p['TLS_implementation'])
    need(p['TLS_implementation']==p['startup']['TLS_implementation'],'same TLS implementation')
    startup.verify_event(p['manager_event'],p['pid'],'menu manager')
    need(p['manager_event']['remote_handle']==p['startup']['worker']['manager_event']['remote_handle'],
         'same manager Event across startup/menu phases')
    samples=p['samples'];need(1<=len(samples)<=2000,'bounded menu samples')
    need([s['index'] for s in samples]==list(range(len(samples))),'menu sample indices')
    times=[number(s['elapsed'],'menu sample time') for s in samples]
    need(all(a<=b for a,b in zip(times,times[1:])) and times[0]>=p['startup']['samples'][-1]['elapsed'],
         'ordered menu samples after startup')
    workers=p['workers'];need(1<=len(workers)<=128,'bounded retained workers')
    mapping={(w['pointer'],w['thread_id']):w for w in workers}
    need(len(mapping)==len(workers),'unique worker lifetimes')
    menu_workers=[w for w in workers if w['vtable']==MENU];need(len(menu_workers)==1,'one original menu worker')
    menu_worker=menu_workers[0]
    need(menu_worker['pointer']==p['startup']['samples'][-1]['menu_node'],'startup successor is input menu')
    seen={};tls_count=0;tls_identities={};ready_times=[];menu_absent=[];successors=[]
    for s in samples:
        nodes,manager=verify_graph(s,p['main'])
        need(word(manager,0x118)==p['manager_event']['remote_handle'],'same manager Event handle')
        need(s['game']==game,'same game owner')
        need(word(blob(s['MAIN_event_hex'],8,'MAIN event')) in (0,1),'MAIN event pending flag')
        for field,size in [('keyboard_hex',0xA00),('mouse_hex',0x58),('scenario_hex',80),
                           ('VM_hex',128),('group90_hex',8)]:blob(s[field],size,field)
        frames=s['frames'];need(1<=len(frames)<=256 and len({f['tid'] for f in frames})==len(frames),
                               'bounded complete unique thread contexts')
        need(any(f['tid']==main_tid for f in frames),'MAIN context present')
        for frame in frames:owner.verify_frame(frame)
        tasks=s['tasks'];need([t['pointer'] for t in tasks]==list(nodes),'exact task/graph association')
        kinds=[t['vtable'] for t in tasks]
        need(startup.STARTUP not in kinds and not (MENU in kinds and len(kinds)>1),
             'no observed startup/menu resource-owner overlap with successor')
        menu_present=False
        for task in tasks:
            node=task['pointer'];head=blob(task['header_hex'],64,'task complete head');vt=task['vtable']
            need(head[:48].hex()==nodes[node]['head_hex'] and vt==word(head),'task raw graph prefix')
            need(type(vt) is int and 0x400000<=vt<=0x400000+len(raw)-8
                 and blob(task['vtable_hex'],8,'original task vtable')==raw[vt-0x400000:vt-0x400000+8],
                 'actual original callback/destructor vtable')
            tid=task['thread_id'];need(tid==word(head,0x24),'actual worker thread ID')
            key=(node,tid)
            if word(head,0x20) and tid:
                need(key in mapping,'every live task has retained worker identity')
                w=mapping[key]
                need(w['vtable']==vt and w['original_handle']==word(head,0x20)
                     and w['event']['remote_handle']==word(head,0x1C),'same actual worker and node Event')
                seen.setdefault(key,[]).append(s['elapsed'])
            frame=next((f for f in frames if f['tid']==tid),None)
            if 'TLS' in task:
                need(frame is not None,'TLS requires actual suspended worker')
                callbacks=[f for f in frame['chain'] if f['return_va']==0x421F8A]
                need(len(callbacks)==1,'TLS exact callback frame')
                startup.verify_tls(task['TLS'],frame,head,node,tid,p['pid'],
                                   {'pointer':callbacks[0]['bp']-0x80},2)
                identity=tuple(task['TLS'][k] for k in ('TEB','FS','TLS_index','slot','PTD'))
                need(tls_identities.setdefault(key,identity)==identity,'same worker TEB/TLS/PTD lifetime')
                tls_count+=1
            if vt==MENU:
                menu_present=True;need(key==(menu_worker['pointer'],menu_worker['thread_id']),'same menu lifetime')
                if word(head,0x30)==1 and len(tasks)==1 and word(bytes.fromhex(s['MAIN_event_hex']))==0:
                    if frame and any(f['return_va']==0x45F065 for f in frame['chain']):ready_times.append(s['elapsed'])
            if vt in (NEW_GAME,ADV,LOAD,WORKROOM):
                successors.append(dict(index=s['index'],elapsed=s['elapsed'],vtable=vt,node=node,
                                       TLS_verified='TLS' in task,thread_id=tid))
        if not menu_present:menu_absent.append(s['elapsed'])
    need(tls_count>0,'actual retained full menu/task TLS observations')
    for key,w in mapping.items():
        startup.verify_event(w['event'],p['pid'],'node')
        need(key in seen and number(w['first_elapsed'],'worker first seen')==min(seen[key]),'retained worker originates in graph')
        if 'exit' in w:
            e=w['exit'];need(type(e['code']) is int and e['code']==0 and e['wait_status']==0 and e['before_WM_CLOSE'] is True,
                            'normal worker exit observed before WM_CLOSE')
            elapsed=number(e['elapsed'],'worker exit time')
            need(min(seen[key])<=elapsed<=times[-1]+1,'worker exit in observation interval')
            need(not any(s['elapsed']>elapsed and any(f['tid']==key[1] for f in s['frames']) for s in samples),
                 'no observed worker context after queried termination')
    input_result=verify_input(p,raw,game,hwnd,menu_worker,check_disk)
    story_results=verify_story_actions(p,raw,game,hwnd,mapping,192 if generation==6 else 96)
    need(p['stop_reason'] in ('bounded_menu_deadline','controller_finished_observation','story_confirmation_budget'),
         'bounded menu observation stop only')
    if p['stop_reason']=='story_confirmation_budget':need(generation==6,'budget stop only in explicit new generation')
    budget_stop=verify_budget_stop(p,raw,game,mapping,story_results)
    ready_span=None;ready_stability_sampled=False
    if input_result['attempted']:
        before=p['mouse_controller']['receipt']['before_elapsed']
        before_ready=[]
        for t in reversed([t for t in times if t<=before]):
            if t not in ready_times:break
            before_ready.append(t)
        ready_span=max(before_ready)-min(before_ready) if before_ready else None
        ready_stability_sampled=bool(len(before_ready)>=2 and ready_span>=1-1e-6)
        receipt=p['mouse_controller']['receipt']
        if generation==6:
            first=receipt.get('ready_start_sample');last=receipt.get('ready_decision_sample')
            need(isinstance(first,dict) and isinstance(last,dict),'explicit new menu ready endpoints')
            for row in (first,last):verify_ready_owner(row,p,raw,game,menu_worker,MENU,0x45F065)
            a=number(first['elapsed'],'first ready sample');b=number(last['elapsed'],'decision ready sample')
            need(a<=b<=before,'ordered actual menu ready endpoints')
            ready_span=b-a;ready_stability_sampled=ready_span>=1-1e-6
        else:need('ready_start_sample' not in receipt and 'ready_decision_sample' not in receipt,
                  'older collector cannot acquire unverified ready-endpoint fields')
    qualified=False;event_observations=[]
    if input_result.get('attempted'):
        event_id=7 if input_result['index']==0 else 13
        for s in samples:
            pending=bytes.fromhex(s['MAIN_event_hex'])
            if word(pending)==1 and word(pending,4)==event_id:
                event_observations.append(dict(source='menu_snapshot',elapsed=s['elapsed'],event=event_id))
        for s in p['mouse_controller']['receipt']['input_samples']:
            pending=bytes.fromhex(s['MAIN_event_hex'])
            if word(pending)==1 and word(pending,4)==event_id:
                event_observations.append(dict(source='unsuspended_input_sample',elapsed=s['elapsed'],event=event_id))
    if input_result.get('input_edges_observed') and 'exit' in menu_worker:
        exit_time=menu_worker['exit']['elapsed'];index=input_result['index']
        expected_vt=NEW_GAME if index==0 else LOAD
        next_rows=[s for s in successors if s['vtable']==expected_vt
                   and s['TLS_verified'] and s['elapsed']>=input_result['input_after_elapsed']]
        qualified=bool(menu_absent and next_rows and exit_time>=p['mouse_controller']['receipt']['before_elapsed']
                       and any(t>=exit_time for t in menu_absent))
    adv_exits=[dict(pointer=w['pointer'],thread_id=w['thread_id'],**w['exit']) for w in workers
               if w['vtable']==ADV and 'exit' in w]
    workrooms=[s for s in successors if s['vtable']==WORKROOM and s['TLS_verified']]
    suffix=[]
    for s in reversed(samples):
        if not (len(s['tasks'])==1 and s['tasks'][0]['vtable']==WORKROOM
                and 'TLS' in s['tasks'][0] and word(bytes.fromhex(s['MAIN_event_hex']))==0):break
        suffix.append(s)
    workroom_span=suffix[0]['elapsed']-suffix[-1]['elapsed'] if suffix else 0
    adv_handoff=bool(adv_exits and workrooms and suffix and workroom_span>=1
                    and any(e['elapsed']<=suffix[-1]['elapsed'] for e in adv_exits))
    workroom_code_live=any(r['pointer']<=0x4A1570 and r['pointer']+r['bytes']>=0x4A16A2
                           for r in source['code'])
    return dict(status='partial_native_menu_handoff_observation' if qualified else 'partial_menu_observation',
        accepted=False,startup_native_handoff_observed=True,samples=len(samples),TLS_samples=tls_count,
        startup_gate_contract=p['startup'].get('gate_contract','frozen_animation_threshold_contract'),
        startup_retirement_trigger_proved=False,
        startup_activation_observations=activations,
        input=input_result,menu_worker_exit=menu_worker.get('exit'),successor_observations=successors,
        menu_ready_one_second_independently_sampled=ready_stability_sampled,
        menu_ready_retained_snapshot_span_seconds=ready_span,
        story_confirmations=story_results,
        VM_dispatch_order_source=vm_dispatch_contract(raw) if story_results else [],
        story_budget_stop=budget_stop,chapter_completion_proved=False,
        pending_successor_event_observations=event_observations,
        native_menu_handoff_observed=qualified,original_constructor_full_trace_proved=False,
        ADV_exit0_observations=adv_exits,ADV_exit0_and_workroom_observed=adv_handoff,
        workroom_stable_observed_seconds=workroom_span,
        workroom_callback_code_live_authenticated=workroom_code_live,
        collector_workroom_input_executed=False,workroom_exit_observed=False,
        full_native_instruction_trace=False,normal_PTD_cleanup_proved=False,
        full_resource_lifetime_proved=False,full_battle_exit_accepted=False,
        wait_return_proved=False,result_consumption_proved=False,formal_terminal_boundary_advanced=False,
        continuously_proved_no_overlap=False,
        WinMain_normal_return_proved=False,cleanup_process_exits=startup_result['cleanup_process_exits'],
        limitations=['Snapshots and retained worker query results are not a complete causal instruction/API trace.',
            'Unsuspended raw input reads can intersect a producer update; incoherent samples do not establish edges.',
            'Original vtable, graph, PTD and successor observations do not individually trace every constructor instruction.',
            'No claim of successful OS wait return, battle result consumption, resource cleanup trace, or complete battle acceptance.'])


def verify_file(path,digest,allow_v1_archive=False,allow_v5_archive=False):
    report=read_menu_report(path,digest);raw=contract.read_source()
    need(not (allow_v1_archive and allow_v5_archive),'one explicit historical implementation exception')
    archived={}
    if allow_v5_archive:
        need(digest==V5_SOURCE_SHA,'v5 archive only for exact fixed v5 source')
        archived=archived_v5_sources()
    need(report['original']==dict(path='analysis/hermit_game.exe',bytes=len(raw),sha256=contract.SOURCE_SHA),
         'recorded original source identity')
    has_controller='mouse_controller' in report['probe']
    paths=IMPLEMENTATIONS
    if 'gate_contract' in report['probe']['startup']:
        paths=paths+('devtools/terminal_menu_startup.py',)
    paths=paths+(INPUT_IMPLEMENTATIONS if has_controller else ())
    if 'collector_story_input_actions' in report['probe']:paths=paths+STORY_IMPLEMENTATIONS
    expected=[]
    for name in paths:
        b=archived[name] if name in archived else (ROOT/name).read_bytes()
        if name==IMPLEMENTATIONS[0] and allow_v1_archive:
            need(digest==V1_SOURCE_SHA and not has_controller,'archive exception only for exact no-input v1')
            packed=(ROOT/V1_ARCHIVE).read_bytes()
            need(len(packed)==3404 and owner.sha(packed)==V1_ARCHIVE_SHA,'explicit v1 archive identity')
            b=gzip.decompress(packed)
            need(len(b)==9268 and owner.sha(b)==V1_COLLECTOR_SHA,'archived v1 implementation identity')
        expected.append(dict(path=name,bytes=len(b),sha256=owner.sha(b)))
    need(report['implementations']==expected and report['observer']==expected[2],'exact collector/base/input implementation set')
    if 'collector_story_input_actions' in report['probe']:
        original_authorization=(ROOT/STORY_IMPLEMENTATIONS[-1]).read_bytes()
        need(owner.sha(original_authorization)==STORY_AUTHORIZATION_SHA
             and json.loads(original_authorization)['approved'] is True,'fixed explicit original scan-code39 authorization')
    authorization_identity=None
    if has_controller:
        authorization=(ROOT/AUTHORIZATION).read_bytes()
        need(owner.sha(authorization)==AUTHORIZATION_SHA,'fixed explicit mouse authorization')
        document=json.loads(authorization)
        need(document['backend']==authorization_backend() and document['user_manual_operation_required'] is False
             and document['does_not_waive_acceptance'] is True,'historical authorized mouse backend and unchanged scope')
        authorization_identity=dict(path=AUTHORIZATION,bytes=len(authorization),sha256=AUTHORIZATION_SHA)
        authorization_identity['historical_backend_archive']=dict(path=AUTHORIZATION_ARCHIVE,
            bytes=10367,sha256=AUTHORIZATION_ARCHIVE_SHA)
        authorization_identity['current_backend']=next(r for r in expected if r['path']==INPUT_IMPLEMENTATIONS[0])
        authorization_identity['scope']='Same two private owned menu targets, original readiness guards, no game writes; current movement bugfix authenticated separately'
    parent=owner.read_report(ROOT/startup.PARENT,startup.PARENT_SHA)
    runtime=report['runtime'];pr=parent['runtime']
    need(runtime['immutable_files_reference']==dict(path=startup.PARENT,sha256=startup.PARENT_SHA,
        rows=len(pr['immutable_files']),freshly_hashed_this_lifetime=True),'fixed freshly checked native asset inventory')
    need({k:v for k,v in runtime.items() if k!='immutable_files_reference'}==
         {k:v for k,v in pr.items() if k!='immutable_files'},'exact private runtime metadata')
    paths_expected={str(Path(pr['private_root'])/r['path']).replace('\\','/'):r['private_sha256']
                    for r in pr['private_writable_files']}
    restored=report['mutable_private_runtime_files']
    need(len(restored)==len(paths_expected) and {r['path'] for r in restored}==set(paths_expected)
         and all(r['restored_exact'] is True and r['sha256']==paths_expected[r['path']] for r in restored),
         'all private mutable source files restored')
    need(owner.sha((ROOT/owner.APP).read_bytes())=='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7',
         'exact private original executable')
    tls=report['probe']['TLS_implementation'];pe=_module(tls['module_path'],tls['module_sha256'])
    ex=next(x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'TlsGetValue')
    need(ex.forwarder is None and ex.address==tls['RVA'] and pe.get_data(ex.address,64).hex()==tls['code_hex'],
         'actual OS TLS implementation bytes')
    result=verify_report(report,raw)
    result.update(source_report=dict(path=str(Path(path).resolve()),bytes=Path(path).stat().st_size,sha256=digest),
        verifier_sha256=owner.sha(Path(__file__).read_bytes()),native_dependency_attestation_complete=False,
        mouse_authorization=authorization_identity,
        implementation_archive_used=V1_ARCHIVE if allow_v1_archive else V5_ARCHIVE if allow_v5_archive else None)
    result['current_verification_dependencies']=[dict(path=name,bytes=(ROOT/name).stat().st_size,
        sha256=owner.sha((ROOT/name).read_bytes())) for name in
        ('devtools/terminal_scene_owner_verification.py','devtools/terminal_startup_handoff_verification.py',
         'devtools/terminal_startup_handoff_contract.py','devtools/terminal_menu_transition_contract.py')]
    if 'collector_story_input_actions' in report['probe']:
        for name in ('tools/school_native_dialogue_verification.py','tools/school_native_scene_verification.py'):
            data=(ROOT/name).read_bytes()
            result['current_verification_dependencies'].append(dict(path=name,bytes=len(data),sha256=owner.sha(data)))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);parser.add_argument('--sha256',required=True)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--allow-v1-archive',action='store_true')
    parser.add_argument('--allow-v5-archive',action='store_true')
    args=parser.parse_args();result=verify_file(args.report,args.sha256,args.allow_v1_archive,args.allow_v5_archive)
    with args.out.open('x',encoding='utf8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps(dict(status=result['status'],accepted=False)))


if __name__=='__main__':main()
