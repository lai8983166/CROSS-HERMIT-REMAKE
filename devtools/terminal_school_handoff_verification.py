"""Independent bounded observation checks for original workroom/school input.

This verifier does not import a collector or native input implementation. Native
input edges and observed task retirement remain distinct from complete original
instruction/API tracing and terminal battle acceptance.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
import functools
import gzip
import json
from pathlib import Path, PureWindowsPath
import re
import struct
import types

from devtools import terminal_menu_handoff_verification as menu
from devtools import terminal_school_preparation_contract as school_contract
from devtools import terminal_workroom_contract as workroom_contract
from devtools import terminal_story_dispatch_verification as story_dispatch

owner=menu.owner
startup=menu.startup
need=owner.need
word=owner.u32
blob=owner.blob
number=startup.number
ROOT=owner.ROOT
GROUP=0x5A0A40
UI=0x5A0C18
WORKROOM=0x5A0904
BATTLE=0x59A430
TARGETS={'workroom':(917,741),'departure':(374,57),'confirmation':(456,404),
         'opening_notice':(512,336),'retreat_request':(48,12),'retreat_confirmation':(568,390)}
SCHOOL_INPUT_RANGES=tuple(school_contract.RANGES.values())+(
    (0x61B628,0x61B63A),(0x625558,0x625560),(0x73BFD0,0x73C0D0),
    (0x5A0A40,0x5A0A48),(0x5A0C18,0x5A0C20),
    (0x411DF0,0x4120A0),(0x414400,0x414439))
WORKROOM_INPUT_RANGES=((0x49FD50,0x49FFF0),(0x4D5B70,0x4D5BEC),(0x4D5EC0,0x4D5FA7),
    (0x4A1570,0x4A1750),(0x411DF0,0x4120A0),(0x414400,0x414439),(0x5A0904,0x5A0930))
BATTLE_INPUT_RANGES=((0x4539B0,0x453CFC),(0x453D00,0x453E04),(0x458580,0x458929),
    (0x456B20,0x456B58),(0x454C40,0x454C7A),(0x4577F0,0x45782B),
    (0x46B470,0x46B663),(0x411DF0,0x4120A0),(0x414400,0x414439),(0x60CB18,0x60CB28))
NOTICE_INPUT_RANGES=BATTLE_INPUT_RANGES+(
    (0x4549D0,0x454AB0),(0x454C80,0x454EE0),(0x467850,0x467AA0),
    (0x4998B0,0x499C90),(0x499DA0,0x49A310),(0x49AD50,0x49AD8C),
    (0x4DB2B0,0x4DB2F4),(0x415040,0x415099),(0x497C50,0x497C90),(0x59EAA4,0x59EAC0))


def notice_fields(head,gates,pointer,game):
    """Independently bind the opening notification to its actual waiting owner."""
    need(len(head)==512 and word(head)==BATTLE,'original notice battle owner')
    need(gates['pointer']==pointer and gates['controller_pointer']==pointer+0x190
         and gates['panel_pointer']==pointer+0x117F20
         and word(blob(gates['backpointer_hex'],4,'notice backpointer'))==pointer,
         'notice actual controller and scene binding')
    need(blob(gates['network_hex'],1,'notice network')==b'\0'
         and blob(gates['panel_hex'],1,'notice panel')==b'\0','local unoccupied notice')
    fields=(('notice',pointer+0x30B28,20),('notice_flags',0x7F44B9,2),
            ('VM',0x7D7C28,128),('keyboard_action',game+0x1950,4),('mouse_pressed',game+0x1990,4))
    values={}
    for name,address,size in fields:
        need(gates[name+'_pointer']==address,'original notice field address '+name)
        values[name]=blob(gates[name+'_hex'],size,'notice '+name)
    need(gates['game_pointer']==game,'notice actual original input owner')
    activity=blob(gates['controller_activity_hex'],32,'notice controller state')
    anim=values['notice']
    need(head[0x30:0x32]==b'\0\0' and word(head,0x34)==2 and word(head,0x38)==5
         and (head[0x43],head[0x44],head[0x58],head[0x59])==(1,3,0,2),
         'original scene waits for post-script notice handshake')
    need(struct.unpack_from('<h',activity)[0]!=0 and activity[8]==0
         and activity[0x16]==1 and activity[0x18]==9,'original controller notice phase9')
    need(anim[:3]==bytes((1,2,0)) and word(anim,8)==0xFF00 and word(anim,12)==0x800,
         'original mode0 notification fully visible and waiting for input')
    need(values['notice_flags'][0]!=0 and values['VM'][4]==0,'enabled opening notice after VM end')
    need(word(values['mouse_pressed'])==0 and not(word(values['keyboard_action'])&0x8000),
         'notice confirmation not already pressed')


def notice_contract(raw):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    menu.contract.authenticate(raw);decoder=Cs(CS_ARCH_X86,CS_MODE_32)
    checks={0x49A1B3:('call','0x499910'),0x49A1BA:('je','0x49a1d8'),
        0x49A1C5:('call','0x454c80'),0x454CD8:('mov','byte ptr [ecx + 0x14], 1'),
        0x454DDB:('je','0x454e13'),0x454E89:('mov','byte ptr [edx + 0x43], 0'),
        0x49A285:('mov','byte ptr [eax + 0x108b3a], 1'),
        0x499A5C:('and','edx, 1'),0x499A61:('jne','0x499a78'),
        0x499A6E:('and','ecx, 0x8000'),0x499A76:('je','0x499ab9'),
        0x499A9C:('mov','byte ptr [ecx + 1], 4'),0x499B38:('mov','byte ptr [edx], 0')}
    for address,expected in checks.items():
        ins=next(decoder.disasm(raw[address-0x400000:address-0x400000+15],address))
        need((ins.mnemonic,ins.op_str)==expected,'original opening-notice branch '+hex(address))
    need(struct.unpack_from('<6I',raw,0x499B5D-0x400000)==
         (0x49999D,0x4999CF,0x499A50,0x499ABE,0x499AFD,0x499B35),'original notice dispatch')
    need(struct.unpack_from('<14h',raw,0x59EAA4-0x400000)==
         (0,0x800,120,0x800,512,336,1,0,0x800,16,0x800,512,304,0),'original notice modes')
    return dict(instruction_checks=len(checks),accepted=False)


def notice_transition(receipt,edge_result):
    need(edge_result['input_edges_observed'],'notice actual press/held/release edges')
    rows=receipt['input_samples'];down=receipt['action']['down_wall_time_ns']
    states=[blob(r['notice_state_hex'],20,'sampled original notification')for r in rows]
    heads=[blob(r['battle_head_tail_hex'],29,'sampled original script gate')for r in rows]
    need(states[0][:3]==bytes((1,2,0)) and heads[0][0:2]==bytes((1,3)),
         'notification waiting before actual input')
    progress=[i for i,(r,s)in enumerate(zip(rows,states))if r['wall_time_ns']>=down
              and s[2]==0 and (s[0]==1 and s[1]in(4,5) or s[0]==0 and s[1]==5)]
    need(progress,'actual original notification left input wait after press')
    need(all(s[:3]==bytes((1,2,0))for r,s in zip(rows,states)if r['wall_time_ns']<down),
         'notification did not advance before the declared click')
    return dict(post_press_progress_samples=progress,accepted=False,
                full_native_instruction_causality_proved=False)


def battle_fields(head,gates,pointer,stage):
    need(stage in ('retreat_request','retreat_confirmation'),'original retreat control')
    need(len(head)==0x200 and word(head)==BATTLE,'actual complete battle object head')
    need(gates['pointer']==pointer and gates['controller_pointer']==pointer+0x190 and
         gates['panel_pointer']==pointer+0x117F20,'actual scene/controller field addresses')
    need(blob(gates['network_hex'],1,'network gate')==b'\0' and
         blob(gates['panel_hex'],1,'panel gate')==b'\0' and
         word(blob(gates['backpointer_hex'],4,'controller backpointer'))==pointer,'original local battle/controller gates')
    activity=blob(gates['controller_activity_hex'],0x20,'controller activity')
    need(struct.unpack_from('<h',activity)[0]!=0 and activity[8]!=0,'actual controller callback active')
    need(head[0x30]==(0 if stage=='retreat_request' else 1) and head[0x31]==0 and
         not(head[0x43] and head[0x59]) and word(head,0x38)==5,'original ordinary-loop retreat gates')


def clone_verifier(function,**globals_):
    """Reuse frozen verification code with one explicitly declared task owner."""
    result=types.FunctionType(function.__code__,dict(function.__globals__,**globals_),function.__name__,
                              function.__defaults__,function.__closure__)
    result.__kwdefaults__=function.__kwdefaults__
    return result


def retreat_contract(raw):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    menu.contract.authenticate(raw);decoder=Cs(CS_ARCH_X86,CS_MODE_32)
    checks={0x45860A:('cmp','dword ptr [ecx + 0x19b8], 3'),
        0x45863D:('mov','ecx, dword ptr [eax + 0x19bc]'),
        0x45864C:('mov','eax, dword ptr [edx + 0x19c0]'),
        0x45868B:('mov','edx, dword ptr [ecx + 0x199c]'),
        0x4586A5:('mov','byte ptr [eax + 0x30], 1'),
        0x45871E:('mov','eax, dword ptr [edx + 0x199c]'),
        0x458756:('mov','eax, 2'),0x453DBC:('mov','dword ptr [0x5ff720], 0xffffffff'),
        0x453DC9:('mov','byte ptr [eax + 0x31], 1'),0x453C34:('mov','dword ptr [ebp - 8], eax'),
        0x453CB5:('cmp','dword ptr [ebp - 8], 0'),0x451AB7:('call','0x4539b0'),
        0x451ABC:('mov','dword ptr [ebp - 8], eax'),0x451716:('mov','dword ptr [ebp - 0xc], eax'),
        0x4517D6:('call','0x439e30'),0x4519A0:('ret','4')}
    result=[]
    for a,expected in checks.items():
        ins=next(decoder.disasm(raw[a-0x400000:a-0x400000+15],a))
        need((ins.mnemonic,ins.op_str)==expected,'original retreat instruction '+hex(a))
        result.append(dict(pointer=a,hex=ins.bytes.hex(),instruction=ins.mnemonic+' '+ins.op_str))
    need(struct.unpack_from('<8h',raw,0x60CB18-0x400000)==(27,52,103,28,140,52,102,28),
         'original retreat relative hit rectangles')
    return result


def school_fields(data,stage):
    """Independently interpret original addresses, widths and branch inputs."""
    need(stage in ('departure','confirmation'),'explicit original school stage')
    expected=((0x7A528E,4,'date_hex'),(0x7A55FA,2,'gate_hex'),
        (0x7AAB08,20,'selected_hex'),(0x7AAA12,140,'classes_hex'),
        (0x7D6A26,1,'ready_hex'),(0x7A4E60,2,'school_ui_state_hex'))
    need(isinstance(data['fields'],list) and len(data['fields'])==6,'all bounded original school fields')
    values={}
    for row,(address,size,name) in zip(data['fields'],expected):
        need((row['pointer'],row['bytes'],row['name'])==(address,size,name),'school field original location')
        values[name]=blob(row['hex'],size,name)
    need(struct.unpack('<HH',values['date_hex'])==(4,1),'actual initial school date')
    need(values['gate_hex']==b'\x01\0' and values['ready_hex']==b'\x01','original mandatory ready')
    need(values['school_ui_state_hex']==b'\0\0','active original companion UI')
    selected=values['selected_hex']
    need(struct.unpack_from('<H',selected,2)[0]==1 and struct.unpack_from('<H',selected,14)[0]==1,
         'actual selected mandatory task1')
    need(type(data['ledger_count']) is int and data['ledger_count']==1 and data['ledger_pointer']==0x7A5662,
         'exact current task1 ledger size and pointer')
    ledger=blob(data['ledger_hex'],16,'current task ledger')
    need(struct.unpack_from('<H',ledger)[0]==1 and (ledger[2],ledger[3],ledger[5],ledger[6])==(1,3,0,0),
         'registered enabled original mandatory task1')
    classes=values['classes_hex'];teachers=[struct.unpack_from('<h',classes,28*i)[0]for i in range(5)]
    need(teachers==[101,-1,-1,-1,-1] and classes[3]==0 and
         struct.unpack_from('<4h',classes,16)==(3,4,9,-1),'legal unchanged original first adventure class')
    # 4A95F0 produces state2 for a nonempty adventure class with selected task;
    # absent teachers produce0. The relation average affects the other output
    # words, not this readiness state. No persistent global rating is invented.
    ratings=[2,0,0,0,0]
    need(len(data['nodes'])==1,'one grouping field record')
    n=data['nodes'][0];pointer=n['pointer'];owner.address(pointer,'school node')
    head=blob(n['header_hex'],64,'school field header');control=blob(n['control_hex'],16,'school control words')
    need(word(head)==GROUP and n['control_pointer']==pointer+0x76BC and
         n['selection_pointer']==pointer+0x7950,'actual school object field locations')
    values16=tuple(struct.unpack_from('<H',control,o)[0]for o in (0,2,4,8,10))
    need(values16==(0,1,1,1,0 if stage=='departure' else 14) and
         struct.unpack_from('<H',head,0x30)[0]==0 and blob(n['selection_hex'],2,'school selection')==b'\0\0',
         'original selector input phase remains unconsumed')
    return dict(pointer=pointer,thread_id=word(head,0x24),head=head,ratings=ratings)


def verify_task_row(row,p,raw,game,workers,require_retained=True):
    """All rows, contexts, single-linked graph and recorded TLS are checked."""
    nodes,manager=menu.verify_graph(row,p['main'])
    need(row['game']==game and word(manager,0x118)==p['manager_event']['remote_handle'],'same game and manager event')
    need(word(blob(row['MAIN_event_hex'],8,'MAIN event'))in(0,1),'MAIN event pending state')
    for name,size in [('keyboard_hex',0xA00),('mouse_hex',0x58),('scenario_hex',80),('VM_hex',128),('group90_hex',8)]:
        blob(row[name],size,'complete '+name)
    frames=row['frames'];need(1<=len(frames)<=256 and len({f['tid']for f in frames})==len(frames),'complete unique contexts')
    need(any(f['tid']==p['startup']['window']['main_tid'] for f in frames),'actual MAIN context')
    for frame in frames:owner.verify_frame(frame)
    tasks=row['tasks'];need([t['pointer']for t in tasks]==list(nodes),'exact graph task order')
    kinds=[t['vtable']for t in tasks]
    need(startup.STARTUP not in kinds,'no obsolete startup overlay')
    # The original retreat callback publishes event1 before RET4, so a newly
    # constructed menu may overlap that retiring battle. Enforce its provenance
    # in verify_report rather than treating all native overlap as host roots.
    tls=0
    for task in tasks:
        ptr=task['pointer'];head=blob(task['header_hex'],64,'task complete header');vt=task['vtable'];tid=task['thread_id']
        need(head[:48].hex()==nodes[ptr]['head_hex'] and word(head)==vt,'actual task graph prefix')
        need(type(vt)is int and 0x400000<=vt<=0x400000+len(raw)-8 and
             blob(task['vtable_hex'],8,'task original vtable')==raw[vt-0x400000:vt-0x400000+8],
             'actual original callback/destructor identity')
        need(tid==word(head,0x24),'actual worker ID')
        if word(head,0x20) and tid:
            if require_retained:need((ptr,tid)in workers,'retained current original worker')
            if (ptr,tid)in workers:
                w=workers[(ptr,tid)]
                need(w['vtable']==vt and w['original_handle']==word(head,0x20) and
                     w['event']['remote_handle']==word(head,0x1C),'same thread handle and task Event')
        if 'TLS'in task:
            frame=next((f for f in frames if f['tid']==tid),None)
            need(frame is not None,'TLS suspended same worker')
            cb=[f for f in frame['chain']if f['return_va']==0x421F8A]
            need(len(cb)==1,'one original CRT callback frame')
            startup.verify_tls(task['TLS'],frame,head,ptr,tid,p['pid'],{'pointer':cb[0]['bp']-0x80},2)
            tls+=1
    return tls


def verify_ready(row,p,raw,game,workers,stage):
    verify_task_row(row,p,raw,game,workers)
    need(word(bytes.fromhex(row['MAIN_event_hex']))==0,'ready MAIN idle')
    if stage=='workroom':
        need(len(row['tasks'])==1 and row['tasks'][0]['vtable']==WORKROOM,'sole original workroom')
        task=row['tasks'][0];head=bytes.fromhex(task['header_hex'])
        need(struct.unpack_from('<H',head,0x30)[0]==1,'original workroom input stage')
        wait,caller=0x49FF57,0x4A15D0
    elif stage in ('departure','confirmation'):
        need(len(row['tasks'])==2 and {t['vtable']for t in row['tasks']}=={GROUP,UI},'both original school owners only')
        info=school_fields(row['school'],stage);task=next(t for t in row['tasks']if t['vtable']==GROUP)
        need((task['pointer'],task['thread_id'])==(info['pointer'],info['thread_id']) and
             task['header_hex']==info['head'].hex(),'school fields associated with actual registered worker')
        wait,caller=0x4A7CEA,0x4AB7F1
    else:
        need(len(row['tasks'])==1 and row['tasks'][0]['vtable']==BATTLE,'sole actual battle ready owner')
        task=row['tasks'][0];head=blob(task['scene_head_hex'],0x200,'ready battle head')
        need(head[:64].hex()==task['header_hex'] and row['scene_global']==task['pointer'],'current battle global/head')
        if stage=='opening_notice':
            notice_fields(head,task['battle_gates'],task['pointer'],game)
            need(task['battle_gates']['VM_hex']==row['VM_hex'],'same frozen notice VM fields')
        else:battle_fields(head,task['battle_gates'],task['pointer'],stage)
        wait,caller=0x453CB5,0x451ABC
    need('TLS'in task,'ready full real TLS captured')
    frame=next(f for f in row['frames']if f['tid']==task['thread_id'])
    waits=[f for f in frame['chain']if f['return_va']==wait]
    need(len(waits)==1 and any(f['bp']==waits[0]['saved_bp'] and f['return_va']==caller for f in frame['chain']),
         'actual selector wait and caller frame')
    return task


def verify_action_guard(g,stage,p,raw,game,hwnd,worker,check_disk=True):
    need((g['pid'],g['hwnd'],g['game'],g['main'],g['node'])==
         (p['pid'],hwnd,game,p['main'],worker['pointer']),'actual guard owner tuple')
    need(g['all_threads_resumed_before_input']is True,'input after snapshot resume')
    is_battle=stage.startswith('retreat_') or stage=='opening_notice'
    head=blob(g['head_hex'],0x200 if is_battle else 64,'guard node header');ptr=worker['pointer'];tid=worker['thread_id']
    need(word(head,8)==p['main']+0x64 and word(head,0x24)==tid and
         word(head,0x20)==worker['original_handle'] and word(head,0x1C)==worker['event']['remote_handle'],
         'same guard manager/thread/node event')
    manager=blob(g['manager_hex'],0x120,'guard full manager')
    need(word(manager,0x118)==p['manager_event']['remote_handle'] and
         word(blob(g['MAIN_event_hex'],8,'guard MAIN'))==0,'guard manager event and idle MAIN')
    frame=g['frame'];owner.verify_frame(frame);need(frame['tid']==tid,'guard actual worker context')
    school=stage in ('departure','confirmation')
    wait=0x453CB5 if is_battle else 0x4A7CEA if school else 0x49FF57
    caller=0x451ABC if is_battle else 0x4AB7F1 if school else 0x4A15D0
    waits=[f for f in frame['chain']if f['return_va']==wait]
    need(len(waits)==1 and {caller,0x421F8A,0x56E183}<={f['return_va']for f in frame['chain']},'guard original callback wait ancestry')
    bp=g['inner_pointer']if is_battle else g['selector_pointer'];need(bp==waits[0]['saved_bp'],'original selector BP')
    need(any(f['bp']==bp and f['return_va']==caller for f in frame['chain']),'actual caller at selector frame')
    if school:
        need(g['stage']==stage,'actual school guard stage')
        info=school_fields(g['school'],stage)
        need((info['pointer'],info['thread_id'],info['head'])==(ptr,tid,head),'guard school fields same original node')
        nodes,_=menu.verify_graph(g,p['main'])
        need(len(nodes)==2 and {word(bytes.fromhex(n['head_hex']))for n in nodes.values()}=={GROUP,UI}
             and nodes[ptr]['head_hex']==head[:48].hex(),'guard both original school nodes')
        selected=blob(g['selector_hex'],12,'original school selector locals')
        need(word(selected)==ptr and word(selected,8)==caller,'school actual selector this/caller memory')
    elif is_battle:
        need(g['stage']==stage.removeprefix('retreat_') and g['scene_global']==ptr,'actual retreat stage/current scene')
        if stage=='opening_notice':notice_fields(head,g['battle_gates'],ptr,game)
        else:battle_fields(head,g['battle_gates'],ptr,stage)
        heads=[word(manager,i*8)for i in range(32)]
        need(sum(v!=0 for v in heads)==1 and ptr in heads and word(head,12)==0,'guard sole original battle')
        inner=blob(g['inner_hex'],0x18,'ordinary battle original locals')
        need(word(inner,8)==0 and word(inner,12)==ptr and word(inner,20)==caller,'actual unaccepted result/this/caller')
    else:
        need(word(head)==WORKROOM and struct.unpack_from('<H',head,0x30)[0]==1 and word(head,12)==0,'unconsumed original workroom')
        heads=[word(manager,i*8)for i in range(32)]
        need(sum(v!=0 for v in heads)==1 and ptr in heads,'guard sole registered workroom')
        selected=blob(g['selector_hex'],0x24,'original workroom selector locals')
        need(word(selected,0x18)==ptr and word(selected,0x20)==caller and
             struct.unpack_from('<H',selected,4)[0]==1,'workroom actual selector this/caller/unaccepted state')
    cb=next(f for f in frame['chain']if f['return_va']==0x421F8A)
    startup.verify_tls(g['TLS'],frame,head,ptr,tid,p['pid'],{'pointer':cb['bp']-0x80},2)
    need(g['code']==menu.code_rows(raw,NOTICE_INPUT_RANGES if stage=='opening_notice' else BATTLE_INPUT_RANGES if is_battle else SCHOOL_INPUT_RANGES if school else WORKROOM_INPUT_RANGES),'complete original input ranges')
    need(word(blob(g['input_HWND_hex'],4,'actual input HWND'))==hwnd,'original input HWND global')
    mode=word(blob(g['coordinate_mode_hex'],4,'coordinate mode'));need(mode in(0,1),'original coordinate mode')
    blob(g['cursor_hex'],8,'actual game cursor')
    exports=g['producer_exports'];need(set(exports)=={'5841772','5841768'} or set(exports)=={0x59236C,0x592368},'both cursor exports')
    for slot,symbol in ((0x59236C,'GetCursorPos'),(0x592368,'ScreenToClient')):
        e=exports.get(str(slot),exports.get(slot));menu.verify_export(e,'user32.dll',symbol,check_disk)
    need([r['slot']for r in g['IAT']]==[0x59236C,0x592368],'exact cursor IAT slots')
    for row in g['IAT']:
        e=exports.get(str(row['slot']),exports.get(row['slot']))
        need(word(blob(row['hex'],4,'live cursor IAT'))==e['target'],'actual cursor IAT target')
    return mode


def nearest_even(n,d):
    need(type(n)is int and type(d)is int and d>0,'integer normalized coordinate ratio')
    q,r=divmod(n,d)
    return q+int(2*r>d or (2*r==d and q%2==1))


def verify_cursor_sample(sample,geometry,target,hwnd,mode):
    need(sample['geometry']==geometry,'same owned geometry during cursor observation')
    menu.verify_geometry(geometry,target,hwnd,mode)
    for name in('screen_point','os_game_point','game_point'):
        need(isinstance(sample[name],list) and len(sample[name])==2 and all(type(x)is int for x in sample[name]),
             'complete actual cursor '+name)
    sx,sy=sample['screen_point'];origin=geometry['screen_target']
    expected=[sx-origin[0]+target[0],sy-origin[1]+target[1]] if mode==1 else [sx,sy]
    need(sample['os_game_point']==expected,'original screen/client cursor transformation')
    need(type(sample['wall_time_ns'])is int and sample['wall_time_ns']>0 and
         type(sample['monotonic_ns'])is int and sample['monotonic_ns']>0,'actual cursor sample clocks')


def verify_settling(samples,geometry,target,hwnd,mode):
    need(isinstance(samples,list) and 3<=len(samples)<=32,'bounded complete OS/game cursor settling')
    for sample in samples:verify_cursor_sample(sample,geometry,target,hwnd,mode)
    walls=[s['wall_time_ns']for s in samples];monotonic=[s['monotonic_ns']for s in samples]
    need(all(a<=b for a,b in zip(walls,walls[1:])) and all(a<=b for a,b in zip(monotonic,monotonic[1:])),
         'ordered settling clocks')
    need(abs((walls[-1]-walls[0])-(monotonic[-1]-monotonic[0]))<=25_000_000,'settling two clock durations agree')
    need(monotonic[-1]-monotonic[0]<=300_000_000,'settling within total 300 millisecond deadline')
    point=samples[-1]['game_point'];suffix=[]
    for sample in reversed(samples):
        if sample['os_game_point']!=point or sample['game_point']!=point:break
        suffix.append(sample)
    need(len(suffix)>=3 and monotonic[-1]-suffix[-1]['monotonic_ns']>=50_000_000,
         'same OS/game point continuously sampled for fifty milliseconds')
    return point


def verify_absolute_moves(action,target,hwnd,mode):
    need(action['movement_mode']=='absolute_virtual_desktop_feedback','explicit reviewed absolute feedback policy')
    moves=action['moves'];need(isinstance(moves,list) and len(moves)<=4,'at most four actual movements')
    previous=None;canonical=[];corrections=[]
    for i,move in enumerate(moves):
        before=move['before'];need(isinstance(before,list) and len(before)==2 and all(type(x)is int for x in before)
            and before!=list(target) and move['submitted']==1 and move['flags']==0xC001,'bounded successful absolute movement')
        geometry=move['geometry'];menu.verify_geometry(geometry,target,hwnd,mode)
        x,y=geometry['screen_target'];left,top,width,height=geometry['virtual_desktop']
        initial=[nearest_even((x-left)*65535,width-1),nearest_even((y-top)*65535,height-1)]
        error=[target[j]-before[j]for j in range(2)]
        if previous:
            need(before==previous['settling'][-1]['game_point'],'feedback uses the previously settled actual point')
        correct=bool(previous and geometry==previous['geometry'] and max(abs(x)for x in error)<=2)
        if correct:
            l,t,r,b=geometry['window_rect']
            need(l+8<=x<r-8 and t+8<=y<b-8,'feedback original target has eight-pixel window margin')
            delta=[nearest_even(error[0]*65536,width),nearest_even(error[1]*65536,height)]
            need(move.get('feedback_correction')==dict(error=error,previous_normalized=previous['normalized'],delta=delta),
                 'exact bounded same-geometry feedback correction')
            expected=[previous['normalized'][j]+delta[j]for j in range(2)]
            corrections.append(dict(index=i,error=error,delta=delta,normalized=expected))
        else:
            need('feedback_correction'not in move,'no unqualified feedback correction')
            expected=initial
        need(move['normalized']==expected and all(type(x)is int and 0<=x<=65535 for x in expected),'actual submitted normalized feedback coordinates')
        settled=verify_settling(move['settling'],geometry,target,hwnd,mode)
        need(max(abs(target[j]-settled[j])for j in range(2))<=2,'settled landing error bounded to two pixels')
        canonical.append(initial);previous=move
    menu.verify_geometry(action['click_geometry'],target,hwnd,mode)
    point=verify_settling(action['before_click_settling'],action['click_geometry'],target,hwnd,mode)
    need(point==list(target),'exact OS/game target before button-down')
    if previous:need(action['before_click_settling'][0]['monotonic_ns']>=previous['settling'][-1]['monotonic_ns'],
                     'final settling follows movement settling')
    final=action['pre_down_cursor'];verify_cursor_sample(final,action['click_geometry'],target,hwnd,mode)
    need(final['os_game_point']==final['game_point']==list(target) and
         final['monotonic_ns']>=action['before_click_settling'][-1]['monotonic_ns'] and
         action['before_click_settling'][-1]['wall_time_ns']<=final['wall_time_ns']<=action['down_wall_time_ns'],
         'last original OS/game cursor recheck immediately before down')
    return corrections,canonical


def verify_input_window(receipt):
    window=receipt['input_window'];samples=receipt['input_samples']
    need(window['maximum_seconds']==11 and window['maximum_retained_samples']==1024
         and window['complete']is True,'complete bounded continuous mouse observation')
    for key in ('retained_samples','captured_samples','evicted_samples'):
        need(type(window[key])is int and window[key]>=0,'integer observation retention counts')
    need(1<=len(samples)==window['retained_samples']<=1024 and
         window['captured_samples']==len(samples)+window['evicted_samples'] and
         len(samples)==min(window['captured_samples'],1024),
         'exact bounded retained raw sample count')
    need(0<=number(window['elapsed_seconds'],'input observation elapsed')<=12,
         'observation within existing full mouse action bound')
    finished=window['finished_wall_time_ns'];up=receipt['action']['up_wall_time_ns']
    need(type(finished)is int and type(up)is int and 0<up<=finished and
         type(samples[-1]['wall_time_ns'])is int and samples[-1]['wall_time_ns']-finished>=95_000_000,
         'actual worker completion and release followed by 100ms raw tail with 5ms clock tolerance')


def verify_title_input(p,raw,game,hwnd,worker,check_disk=True):
    controller=p.get('mouse_controller')
    if not controller or not controller.get('attempted'):
        return menu.verify_input(p,raw,game,hwnd,worker,check_disk)
    receipt=controller['receipt'];action=receipt['action'];target=(318,508)
    verify_input_window(receipt)
    guards=action['guard_observations'];need(4<=len(guards)<=12,'complete original title guards')
    modes={word(blob(g['coordinate_mode_hex'],4,'title coordinate mode'))for g in guards}
    need(len(modes)==1,'stable original title coordinate mode')
    corrections,canonical=verify_absolute_moves(action,target,hwnd,modes.pop())
    # The recorded new movements were checked above. The immutable verifier
    # below verifies unchanged title guards, raw press/held/release, clocks and
    # down/up receipts. Only its old geometry-policy fields are normalized in
    # this local view; the source report is never changed or re-signed.
    view_receipt=copy.deepcopy(receipt);view_action=view_receipt['action']
    view_action['movement_mode']='absolute_virtual_desktop'
    for move,normalized in zip(view_action['moves'],canonical):
        move['normalized']=normalized;move.pop('feedback_correction',None)
    view=dict(p,mouse_controller=dict(controller,receipt=view_receipt),collector_input_actions=[view_receipt])
    need(p['collector_input_actions']==[receipt],'one unchanged actual title input receipt')
    result=menu.verify_input(view,raw,game,hwnd,worker,check_disk)
    result.update(movement_mode='absolute_virtual_desktop_feedback',feedback_corrections=corrections)
    return result


def supplemental_release_rows(receipt,stage,p,raw,game,hwnd,workers,key):
    """Use actual frozen release frames bracketed by raw fast input samples.

    observe() captures a fast row, detects worker completion, then captures one
    supplemental frame before the next fast row. Its final fast row closes the
    last bracket. Keep these indices separate; never invent a fast sample.
    """
    post=receipt['post_release_snapshots']
    if stage!='retreat_confirmation':
        need(not post,'only retreat confirmation collects supplemental frames')
        return []
    if not post:return []
    fast=receipt['input_samples'];finished=receipt['input_window']['finished_wall_time_ns']
    up=receipt['action']['up_wall_time_ns']
    starts=[i for i,s in enumerate(fast)if s['wall_time_ns']<=finished]
    need(starts and up<=finished,'actual mouse release precedes completed-worker observation')
    first=starts[-1]
    need(first+len(post)<len(fast),'each frozen observation has both raw input brackets')
    result=[]
    for j,row in enumerate(post):
        before,after=fast[first+j:first+j+2]
        need(up<=before['wall_time_ns']<=after['wall_time_ns']
             and before['elapsed']<=row['elapsed']<=after['elapsed']
             and before['foreground_hwnd']==after['foreground_hwnd']==hwnd,
             'frozen frame lies after release inside the same owned input bracket')
        verify_task_row(row,p,raw,game,workers,False)
        mouse=blob(row['mouse_hex'],0x58,'frozen original mouse fields')
        previous,current,pressed,released=(word(mouse,o)for o in(28,32,36,48))
        need(pressed==((previous^current)&current) and released==((previous^current)&previous),
             'coherent mouse edge in atomic suspended frame')
        if not(released&1):continue
        need(previous&1 and not(current&1) and struct.unpack_from('<ii',mouse)==TARGETS[stage],
             'actual left release at the reviewed retreat confirmation target')
        task=next((t for t in row['tasks']if(t['pointer'],t['thread_id'])==key),None)
        need(task is not None and task['vtable']==BATTLE and 'TLS'in task
             and bytes.fromhex(task['scene_head_hex'])[0x31]==1,
             'frozen release retains the same current retreat worker and TLS')
        terminal=verify_terminal_rows([row],p,workers)
        need(any(t['node']==key[0]and t['thread_id']==key[1]
                 and(t['original_result_locals'].get('inner_result')==1
                     or t['original_result_locals'].get('callback_result')==1)for t in terminal),
             'frozen release bound to actual original accepted retreat result')
        result.append(dict(post_release_index=j,before_input_index=first+j,
            after_input_index=first+j+1,elapsed=row['elapsed'],
            before_wall_time_ns=before['wall_time_ns'],after_wall_time_ns=after['wall_time_ns']))
    return result


def verify_mouse_action(receipt,stage,p,raw,game,hwnd,workers,check_disk=True):
    verify_input_window(receipt)
    need(stage in TARGETS and receipt['error']is None,'successful scoped mouse action')
    need(receipt['stage']==('workroom_exit'if stage=='workroom'else stage.removeprefix('retreat_')),'declared mouse receipt stage')
    target=TARGETS[stage];before=number(receipt['before_elapsed'],'mouse before');after=number(receipt['after_elapsed'],'mouse after')
    need(0<after-before<=12,'bounded mouse action')
    first=receipt['ready_start_sample'];decision=receipt['ready_decision_sample']
    need(receipt['before_sample']==decision,'actual input decision snapshot retained unchanged')
    task=verify_ready(first,p,raw,game,workers,stage);task2=verify_ready(decision,p,raw,game,workers,stage)
    key=(task['pointer'],task['thread_id'])
    need(key==(task2['pointer'],task2['thread_id']) and first['elapsed']+1-1e-6<=decision['elapsed']<=before,
         'same original input phase stable sampled one second')
    activation=receipt['activation']
    need(activation['hwnd']==activation['after']==hwnd and len(activation['operations'])<=1 and
         all(x==dict(name='SetForegroundWindow',result=True)for x in activation['operations']),'owned foreground activation only')
    action=receipt['action'];owner.false_fields(action,('game_memory_written','transition_proved'))
    need(action['error']is None and action.get('release_error')is None and action['down_submitted']is True
         and action['released']is True and action['down_result']==1 and action['up_results']==[1],'single real mouse down/up submission')
    need(action['target']==action['before_click']==list(target),'exact reviewed original target')
    if stage!='workroom':need(action['stage']==stage.removeprefix('retreat_'),'actual backend stage')
    guards=action['guard_observations'];need(4<=len(guards)<=12,'bounded original input guards')
    modes={verify_action_guard(g,stage,p,raw,game,hwnd,workers[key],check_disk)for g in guards}
    need(len(modes)==1 and struct.unpack('<ii',bytes.fromhex(guards[-1]['cursor_hex']))==target,'stable mode and original cursor at target')
    mode=modes.pop();corrections,_=verify_absolute_moves(action,target,hwnd,mode)
    down=action['down_wall_time_ns'];up=action['up_wall_time_ns']
    need(type(down)is int and type(up)is int and 0<up-down<=250_000_000,'bounded actual mouse hold')
    samples=receipt['input_samples'];need(2<=len(samples)<=1025,'bounded raw mouse observations')
    times=[number(s['elapsed'],'mouse elapsed')for s in samples];walls=[s['wall_time_ns']for s in samples]
    need(all(type(t)is int and t>0 for t in walls) and all(a<=b for a,b in zip(times,times[1:]))
         and all(a<=b for a,b in zip(walls,walls[1:])),'ordered raw mouse clocks')
    need(before<=times[0]<=times[-1]<=after and walls[0]<=down<up<=walls[-1],'mouse submission bracketed by raw observations')
    need(abs(times[-1]-times[0]-(walls[-1]-walls[0])/1e9)<=.05,'mouse clocks agree')
    press=[];release=[];held=[];incoherent=[];request_releases=[]
    for i,s in enumerate(samples):
        mouse=blob(s['mouse_hex'],0x58,'original raw mouse');event=blob(s['MAIN_event_hex'],8,'raw MAIN event')
        need(s['foreground_hwnd']==hwnd,'actual owned input foreground')
        need(word(event)in(0,1),'raw pending event state')
        previous,current,pressed,released=(word(mouse,o)for o in(0x1C,0x20,0x24,0x30))
        if pressed!=((previous^current)&current) or released!=((previous^current)&previous):
            incoherent.append(i);continue
        if struct.unpack_from('<ii',mouse)!=target:continue
        if current&1 and down<=walls[i]<=up:held.append(i)
        if pressed&1 and down<=walls[i]<=up:press.append(i)
        if released&1 and walls[i]>=up:
            release.append(i)
            if stage=='retreat_request':
                stored=struct.unpack_from('<ii',mouse,0x50)
                if word(mouse,0x4C)==3 and 9<=stored[0]<=88 and 3<=stored[1]<=24:request_releases.append(i)
    supplemental=supplemental_release_rows(receipt,stage,p,raw,game,hwnd,workers,key)
    observed=bool(press and held and ((release and min(press)<max(release))
                  or(supplemental and min(press)<supplemental[0]['before_input_index'])))
    if stage=='retreat_request':observed=bool(observed and request_releases)
    # Replay original hit consumer separately; native state is never input to a
    # host-side game call. This only checks the meaning of the recorded target.
    if stage=='departure':need(school_contract.original_depart_hit(raw,*target,pressed=1)['control']==0,'original departure control replay')
    elif stage=='confirmation':need(school_contract.original_confirm_hit(raw,*target,pressed=1)['selected'],'original confirmation replay')
    elif stage=='workroom':need(workroom_contract.original_hit(raw,*target,pressed=1)['exit_press_observed'],'original workroom exit replay')
    elif stage=='opening_notice':notice_contract(raw)
    else:retreat_contract(raw)
    return dict(stage=stage,node=key[0],thread_id=key[1],input_edges_observed=observed,
        press_samples=press,held_samples=held,release_samples=release,asynchronous_incoherent_samples=incoherent,
        supplemental_release_samples=supplemental,
        original_request_release_gate_samples=request_releases,
        feedback_corrections=corrections,
        down_to_up_ms=(up-down)/1e6,before_elapsed=before,after_elapsed=after,
        native_transition_proved_by_submission=False)


def source_rows(raw):
    rows=owner.source_rows(raw)+menu.code_rows(raw,startup.EXTRA_RANGES+startup.V2_RANGES+
        menu.EXTRA_RANGES+menu.STORY_RANGES+WORKROOM_INPUT_RANGES+SCHOOL_INPUT_RANGES+BATTLE_INPUT_RANGES+NOTICE_INPUT_RANGES)
    seen=set();result=[]
    for row in rows:
        key=(row['pointer'],row['bytes'])
        if key not in seen:result.append(row);seen.add(key)
    return result


@functools.lru_cache(maxsize=128)
def asset_bytes(path,digest,size):
    p=(ROOT/path).resolve();base=(ROOT/'CROSS HERMIT/CROSS HERMIT').resolve()
    need(p.is_relative_to(base) and 0<size<=16*1024*1024,'bounded original script asset path/size')
    data=p.read_bytes();need(len(data)==size and owner.sha(data)==digest,'original script asset identity')
    return data


def verify_program(record,vm,inventory):
    """Hashes bind observed bytes to immutable bytes, not merely code length."""
    start,end=struct.unpack_from('<II',vm,16)
    if record.get('matched')is not True:
        need(record.get('matched')is False,'explicit unrecognized program state')
        return None
    need(record['pointer']==start and record['bytes']==end-start and
         0x10000<=start<end<0x80000000 and 4<=end-start<=1024*1024,'bounded live program range')
    need(record['live_bytes_compared_via_sha256']is True and record['raw_bytes_available_from_fixed_assets']is True,
         'explicit live code hash and retained original byte source')
    assets=record['assets'];need(isinstance(assets,list) and 1<=len(assets)<=512,'bounded matching original program candidates')
    seen=set()
    for row in assets:
        path=row['path'];key=(path,row['code_offset']);need(key not in seen,'unique original program candidate');seen.add(key)
        relative=Path(path).relative_to('CROSS HERMIT/CROSS HERMIT').as_posix().upper()
        need(relative in inventory,'program asset in fixed runtime inventory')
        expected=inventory[relative]
        need((row['bytes'],row['sha256'])==(expected['bytes'],expected['sha256']),'fixed original program asset identity')
        data=asset_bytes(path,row['sha256'],row['bytes']);offset=row['code_offset'];count=row['code_bytes']
        need(type(offset)is int and type(count)is int and 0<=offset<offset+count<=len(data),'asset program extent')
        need(count==end-start and row['code_sha256']==record['sha256']==owner.sha(data[offset:offset+count]),
             'actual live code digest equals retained asset bytes')
        if path.upper().endswith('.YBC'):
            blocks=word(data);need(2<=blocks<=8 and len(data)>=4+blocks*4,'original ADV block table')
            begin,finish=struct.unpack_from('<II',data,4)
            need(4+blocks*4<=begin==offset and finish==offset+count<=len(data),'exact original ADV code block')
        else:
            need(relative=='DATA/TACTICS/SCRIPT/T0001.BIN','only actual task1 battle script')
            block=row['block'];rec=row['record'];n=word(data,4)
            need(type(block)is int and 0<=block<n<=64,'bounded original tactics block')
            begin=word(data,8+4*block);need(0<=begin<=len(data)-8,'tactics block extent')
            records=word(data,begin+4);need(type(rec)is int and 0<=rec<records<=1024,'bounded original tactics record')
            where=begin+8+rec*4;need(where<=len(data)-4,'tactics offset table extent')
            sub=begin+word(data,where);need(0<=sub<=len(data)-20 and word(data,sub)==4,'original tactics four-block VM')
            need(sub+word(data,sub+4)==offset and sub+word(data,sub+8)==offset+count,'exact original tactics code block')
    return dict(pointer=start,bytes=end-start,sha256=record['sha256'],assets=[r['path']for r in assets],
                unique_asset_proved=False)


def verify_terminal_rows(rows,p,workers):
    observations=[]
    for row in rows:
        for task in row['tasks']:
            if task['vtable']!=BATTLE:continue
            pointer=task['pointer'];tid=task['thread_id'];head=blob(task['scene_head_hex'],0x200,'battle observation head')
            need(head[:64].hex()==task['header_hex'] and task['controller_task_backpointer']==pointer,
                 'same actual derived scene controller owner')
            frame=next((f for f in row['frames']if f['tid']==tid),None)
            saved=task['terminal_frames'];need(isinstance(saved,list) and len(saved)<=3,'bounded terminal local observations')
            expected=[f for f in frame['chain']if f['return_va']in(0x451ABC,0x451716,0x421F8A)]if frame else []
            need(len(saved)==len(expected),'complete selected original terminal frames')
            values={}
            for local,f in zip(saved,expected):
                data=blob(local['hex'],0x90,'complete terminal frame memory')
                need(local['return_va']==f['return_va'] and local['pointer']==f['bp']-0x80 and
                     word(data,0x7C)==pointer and word(data,0x80)==f['saved_bp'] and word(data,0x84)==f['return_va'],
                     'actual terminal locals belong to same worker/frame/this')
                if f['return_va']==0x451ABC:values['inner_result']=word(data,0x78)
                elif f['return_va']==0x451716:values['dispatcher_result']=word(data,0x78)
                else:values['callback_result']=word(data,0x74)
            returns={f['return_va']for f in frame['chain']}if frame else set()
            if head[0x31] or values.get('inner_result')==1 or values.get('callback_result')==1 or returns&{0x453CD3,0x453CDD,0x451758,0x451796}:
                observations.append(dict(elapsed=row['elapsed'],node=pointer,thread_id=tid,
                    retreat_flag=head[0x31],original_result_locals=values,
                    return_sites=sorted(returns&{0x453CB5,0x453CD3,0x453CDD,0x451716,0x451758,0x451796,0x421F8A}),
                    TLS_verified='TLS'in task))
    return observations


def verify_report(report,raw,inventory,check_disk=True,startup_root=None):
    menu.contract.authenticate(raw);school_contract.contract(raw);workroom_contract.contract(raw);retreat_contract(raw)
    need(report['schema_version']==1 and report['kind']=='original_workroom_school_continuation_observation','new school source schema')
    owner.false_fields(report,('accepted','old_terminal_cases_replayed','independent_full_replay',
        'full_native_instruction_or_API_trace','R3_complete','R4_complete','R5_complete','R6_complete',
        'human_operation_required','host_game_roots_called','full_battle_exit_accepted',
        'full_resource_lifetime_proved','wait_return_proved','result_consumption_proved'))
    p=report['probe'];life=report['lifecycle'];ready=life['ready']
    need(p['error']is None and life['error']is None,'successful bounded observation, not a failed acquisition')
    owner.false_fields(p,('full_native_instruction_trace','full_battle_exit_accepted'))
    need(p['host_game_calls']==p['host_memory_writes']==[],'zero original game roots or host game writes')
    owner.false_fields(life,('original_code_written','original_registers_written','original_IAT_written'))
    gate=menu.verify_startup_gate if startup_root is None else clone_verifier(menu.verify_startup_gate,ROOT=startup_root)
    initial=gate(report,raw)
    need((p['pid'],p['main'])==(p['startup']['pid'],p['startup']['main'])==(ready['pid'],ready['main']['pointer']),
         'one actual lifetime from startup')
    game=ready['game']['pointer'];hwnd=ready['window']['hwnd']
    # Validate actual new operations before adapting only private action views
    # for the frozen input-edge verifiers. No raw receipt is rewritten.
    isolation=verify_input_isolation(report['input_isolation'])
    report,focus_observations=guest_focus_view(report,isolation,p['pid'],hwnd)
    p=report['probe']
    activations=report.get('startup_activation',[])
    need(isinstance(activations,list) and len(activations)<=1,'bounded early owned activation')
    for a in activations:
        number(a['elapsed'],'startup activation time')
        if 'error'in a:need(set(a)=={'elapsed','error'} and isinstance(a['error'],str),'explicit activation failure')
        else:need(a['hwnd']==a['after']==hwnd and len(a['operations'])<=1 and
             all(op==dict(name='SetForegroundWindow',result=True)for op in a['operations']),'only current owned foreground activation')
    source=p['source_before'];need(source==p['source_after'] and source['code']==source_rows(raw),'all original live continuation source ranges unchanged')
    need([r['slot']for r in source['IAT']]==list(startup.V2_IAT) and
         all(word(blob(r['hex'],4,'live original IAT'))>=0x10000 for r in source['IAT']),'complete live original IAT')
    owner.verify_tls_implementation(p['TLS_implementation'])
    need(p['TLS_implementation']==p['startup']['TLS_implementation'],'same actual TLS implementation')
    startup.verify_event(p['manager_event'],p['pid'],'continuation manager')
    need(p['manager_event']['remote_handle']==p['startup']['worker']['manager_event']['remote_handle'],'same original scheduler event')
    plan=report['observation_plan'];need(type(plan['maximum_seconds'])is int and 900<=plan['maximum_seconds']<=1800 and
        plan['maximum_mouse_actions']==7 and plan['story_phase_budgets']==[192,192,64] and
        plan['stable_unhandled_wait_seconds']==60 and plan['retreat_is_separate_from_retained_neutral_timeout_cases']is True,
        'explicit bounded independent retreat observation plan')
    need(p['maximum_mouse_actions']==7 and p['maximum_story_actions']==448 and
         p['collector_input_actions_scope']=='title_menu_only','all mouse/story action budgets explicit')
    samples=p['samples'];need(1<=len(samples)<=5000 and [s['index']for s in samples]==list(range(len(samples))),'bounded ordered retained snapshots')
    times=[number(s['elapsed'],'snapshot elapsed')for s in samples]
    need(all(a<=b for a,b in zip(times,times[1:])) and times[0]>=p['startup']['samples'][-1]['elapsed'],
         'continuation observations follow same original startup')
    ws=p['workers'];need(1<=len(ws)<=128,'bounded retained worker identities')
    workers={(w['pointer'],w['thread_id']):w for w in ws};need(len(workers)==len(ws),'unique actual worker lifetimes')
    seen={};tls_ids={};tls_count=0;programs={};all_rows=list(samples);post_only=[]
    action_lists=[p['workroom_inputs'],p['school_inputs'],p['notice_inputs'],p['battle_inputs']]
    need(all(isinstance(x,list)for x in action_lists)
         and all(len(x)<=n for x,n in zip(action_lists,(1,2,1,2))),'bounded declared continuation mouse actions')
    for actions in action_lists:
        for action in actions:
            post=action['post_release_snapshots'];need(isinstance(post,list) and len(post)<=128,'bounded supplemental post-release snapshots')
            if actions is not action_lists[3] or action.get('stage')!='confirmation':need(not post,'only battle confirmation supplements terminal snapshots')
            need(all(action['before_elapsed']<=r['elapsed']<=action['after_elapsed']for r in post),'post-release snapshots within action interval')
            all_rows.extend(post)
            post_only.extend(post)
    all_rows.sort(key=lambda r:r['elapsed'])
    for row in all_rows:
        supplemental=any(row is r for r in post_only)
        tls_count+=verify_task_row(row,p,raw,game,workers,not supplemental)
        flags=row['workroom_flags'];need([f['pointer']for f in flags]==[0x7A4E62,0x7E11A0],'original workroom flags')
        for flag in flags:blob(flag['hex'],2,'original workroom flag')
        for t in row['tasks']:
            key=(t['pointer'],t['thread_id']);head=bytes.fromhex(t['header_hex'])
            if not supplemental and word(head,0x20) and t['thread_id']:seen.setdefault(key,[]).append(row['elapsed'])
            if 'TLS'in t:
                identity=tuple(t['TLS'][k]for k in('TEB','FS','TLS_index','slot','PTD'))
                need(tls_ids.setdefault(key,identity)==identity,'same TEB/TLS/PTD over current worker lifetime')
        vm=bytes.fromhex(row['VM_hex'])
        if 'program_code'in row:
            matched=verify_program(row['program_code'],vm,inventory)
            if matched:programs[(matched['pointer'],matched['bytes'],matched['sha256'])]=matched
    for key,w in workers.items():
        startup.verify_event(w['event'],p['pid'],'current node')
        need(key in seen and w['first_elapsed']==min(seen[key]),'retained worker first observed in original graph')
        if 'exit'in w:
            e=w['exit'];need(type(e['code'])is int and e['code']==0 and e['wait_status']==0 and e['before_WM_CLOSE']is True,'actual worker exit0 queried before cleanup')
            elapsed=number(e['elapsed'],'worker exit elapsed');need(min(seen[key])<=elapsed<=times[-1]+1,'actual worker exit within observation')
            need(not any(r['elapsed']>elapsed and any(f['tid']==key[1]for f in r['frames'])for r in all_rows),'no original worker context after queried exit')
    initial_menu=p['startup']['samples'][-1]['menu_node']
    initial_menu_row=next(r for r in p['startup']['samples'][-1]['registered_tasks']if r['pointer']==initial_menu)
    initial_menu_tid=word(bytes.fromhex(initial_menu_row['head_hex']),0x24)
    opening=[w for w in ws if w['vtable']==menu.MENU and (w['pointer'],w['thread_id'])==(initial_menu,initial_menu_tid)]
    need(len(opening)==1,'one actual original title menu from startup')
    title=verify_title_input(p,raw,game,hwnd,opening[0],check_disk)
    if title['attempted']:
        receipt=p['mouse_controller']['receipt']
        for row in(receipt['ready_start_sample'],receipt['ready_decision_sample']):
            menu.verify_ready_owner(row,p,raw,game,opening[0],menu.MENU,0x45F065)
        need(receipt['ready_decision_sample']['elapsed']-receipt['ready_start_sample']['elapsed']>=1-1e-6,'actual title menu stable one second')
        need(receipt['index']==0,'authorized original new-game title input')
    phases=p['story_phases'];need(len(phases)==3,'all three bounded story phases declared')
    story_results=[]
    for phase,name,maximum,vt in zip(phases,('opening_ADV','after_workroom_ADV','battle_dialogue'),(192,192,64),(menu.ADV,menu.ADV,BATTLE)):
        need(phase['name']==name and phase['maximum']==maximum and type(phase['budget_exhausted'])is bool,'explicit original story phase')
        view=dict(p,collector_story_input_actions=phase['actions'],maximum_story_confirmations=maximum,collector_input_actions_scope='mouse_menu_only')
        def code_for_action(action):
            row=action['before_sample'];record=row['program_code']
            need(verify_program(record,bytes.fromhex(row['VM_hex']),inventory)is not None,
                 'dispatch extension requires original live byte-identified program')
            asset=record['assets'][0];data=asset_bytes(asset['path'],asset['sha256'],asset['bytes'])
            return data[asset['code_offset']:asset['code_offset']+asset['code_bytes']]
        results=story_dispatch.verify(view,raw,game,hwnd,workers,maximum,vt,code_for_action)
        for action in phase['actions']:
            row=action['before_sample'];need('program_code'in row and verify_program(row['program_code'],bytes.fromhex(row['VM_hex']),inventory)is not None,'input only to live byte-identified script')
            if vt==BATTLE:
                head=blob(row['tasks'][0]['scene_head_hex'],0x200,'battle dialogue head')
                need(head[0x43] and head[0x59],'original battle script/dialogue active')
        story_results.append(dict(name=name,confirmations=results,budget_exhausted=phase['budget_exhausted']))
    outputs=[]
    for receipts,stages in zip(action_lists,(('workroom',),('departure','confirmation'),('opening_notice',),('retreat_request','retreat_confirmation'))):
        for receipt,stage in zip(receipts,stages):
            observed=verify_mouse_action(receipt,stage,p,raw,game,hwnd,workers,check_disk)
            if stage=='opening_notice':observed['notice_transition']=notice_transition(receipt,observed)
            outputs.append(observed)
    before_by_stage={r['stage']:r['before_elapsed']for r in outputs}
    order=['workroom','departure','confirmation','opening_notice','retreat_request','retreat_confirmation']
    need([r['stage']for r in outputs]==order[:len(outputs)],'original UI continuation stages without bypass')
    need(all(a['after_elapsed']<=b['before_elapsed']for a,b in zip(outputs,outputs[1:])),'ordered nonoverlapping UI actions')
    if outputs:need(title.get('input_edges_observed')and 'exit'in opening[0],'workroom actions follow actual title input and menu retirement')
    for i,phase in enumerate(phases):
        for action in phase['actions']:
            if i==0:need('workroom'not in before_by_stage or action['after_elapsed']<=before_by_stage['workroom'],'opening confirmations before workroom input')
            elif i==1:need('workroom'in before_by_stage and action['before_elapsed']>=outputs[0]['after_elapsed'],'second ADV follows workroom input')
            else:need('confirmation'in before_by_stage and action['before_elapsed']>=next(x['after_elapsed']for x in outputs if x['stage']=='confirmation'),'battle dialogue follows school confirmation')
    terminal=verify_terminal_rows(all_rows,p,workers)
    post_wait_observed=any(t['retreat_flag']==1 and t['original_result_locals'].get('inner_result')==1
        and set(t['return_sites'])&{0x453CD3,0x453CDD} for t in terminal)
    callback_consumer_observed=any(t['retreat_flag']==1 and t['original_result_locals'].get('callback_result')==1
        and set(t['return_sites'])&{0x451758,0x451796} for t in terminal)
    for row in all_rows:
        kinds=[t['vtable']for t in row['tasks']]
        if menu.MENU in kinds and len(kinds)>1:
            need(set(kinds)=={menu.MENU,BATTLE} and len(kinds)==2 and 'retreat_confirmation'in before_by_stage
                 and row['elapsed']>=before_by_stage['retreat_confirmation'] and
                 any(t['vtable']==BATTLE and bytes.fromhex(t['scene_head_hex'])[0x31]==1 for t in row['tasks']),
                 'only original retreat publication allows transient battle/menu overlap')
    allowed_stops={'bounded_school_battle_deadline','controller_finished_observation','stable_unhandled_native_wait',
        'battle_worker_exit_and_menu_observed','story_phase_budget_0','story_phase_budget_1','story_phase_budget_2'}
    need(p['stop_reason']in allowed_stops,'explicit bounded observation stop reason')
    if p['stop_reason'].startswith('story_phase_budget_'):
        i=int(p['stop_reason'][-1]);phase=phases[i]
        need(phase['budget_exhausted']is True and len(phase['actions'])==phase['maximum'],'exact story phase budget exhaustion')
        row=p['dependency_sample'];verify_task_row(row,p,raw,game,workers);vm=bytes.fromhex(row['VM_hex'])
        need(vm[4] and struct.unpack_from('<HH',vm,32)==(1,51),'budget stopped at unconsumed original wait')
        key=[row['tasks'][0]['pointer'],word(vm,16),word(vm,28)]
        need(all(a['key']!=key for a in phase['actions']),'no extra budget confirmation submitted')
    exit_rows=[dict(pointer=w['pointer'],thread_id=w['thread_id'],vtable=w['vtable'],**w['exit'])for w in ws if 'exit'in w]
    observed_kinds={t['vtable']for r in all_rows for t in r['tasks']if 'TLS'in t}
    battle_exits=[r for r in exit_rows if r['vtable']==BATTLE]
    workroom_exits=[r for r in exit_rows if r['vtable']==WORKROOM]
    edge_stages={r['stage']for r in outputs if r['input_edges_observed']}
    workroom_to_school=bool('workroom'in edge_stages and workroom_exits and {GROUP,UI}<=observed_kinds)
    school_to_battle=bool({'departure','confirmation'}<=edge_stages and BATTLE in observed_kinds)
    new_menu=[dict(elapsed=r['elapsed'],node=t['pointer'],thread_id=t['thread_id'])for r in all_rows for t in r['tasks']
              if t['vtable']==menu.MENU and 'TLS'in t and (t['pointer'],t['thread_id'])!=(opening[0]['pointer'],opening[0]['thread_id'])]
    if p['stop_reason']=='battle_worker_exit_and_menu_observed':
        need(battle_exits and new_menu and any(m['elapsed']>=e['elapsed']for m in new_menu for e in battle_exits),'actual battle exit and distinct original successor menu')
    return dict(status='partial_original_school_battle_observation',accepted=False,
        samples=len(samples),post_release_samples=len(all_rows)-len(samples),TLS_observations=tls_count,
        startup_native_handoff_observed=True,startup_retirement_trigger_proved=False,title_input=title,
        guest_focus_observations=focus_observations,
        observed_worker_exits=exit_rows,story_phases=story_results,mouse_actions=outputs,
        original_program_identities=list(programs.values()),school_two_owners_TLS_observed={GROUP,UI}<=observed_kinds,
        workroom_exit0_and_school_observed=workroom_to_school,school_UI_to_battle_owner_observed=school_to_battle,
        battle_owner_TLS_observed=BATTLE in observed_kinds,terminal_frame_observations=terminal,
        original_post_wait_callsite_with_saved_result_observed=post_wait_observed,
        callback_nonzero_result_and_tail_wait_observed=callback_consumer_observed,
        battle_worker_exit0_observed=bool(battle_exits),post_battle_original_menu_observations=new_menu,
        short_lived_NEW_GAME_owner_observed=menu.NEW_GAME in observed_kinds,stop_reason=p['stop_reason'],
        complete_instruction_causality_proved=False,original_constructor_full_trace_proved=False,
        successful_OS_wait_return_proved=False,wait_return_proved=False,result_consumption_proved=False,
        full_resource_lifetime_proved=False,normal_PTD_cleanup_proved=False,WinMain_normal_return_proved=False,
        full_battle_exit_accepted=False,old_terminal_cases_replayed=False,independent_full_replay=False,
        formal_terminal_boundary_advanced=False,cleanup_process_exits=initial['cleanup_process_exits'],
        limitations=['Original graph, full worker contexts, TLS and input are bounded observations, not a complete native instruction/API replay.',
          'Observed saved result and tail call sites do not prove every original wait API return or all resource/PTD cleanup.',
          'Retreat input is a separately declared case; retained neutral/timeout acceptance remains outstanding.',
          'Asset hashes bind observed live program bytes to retained fixed bytes; identical candidate assets are not uniquely named.'])


PARENT_IMPLEMENTATIONS=menu.IMPLEMENTATIONS+('devtools/terminal_menu_startup.py',)+menu.INPUT_IMPLEMENTATIONS+menu.STORY_IMPLEMENTATIONS
LAYER_IMPLEMENTATIONS=('devtools/terminal_school_handoff.py','devtools/terminal_workroom_input.py',
    'devtools/terminal_workroom_contract.py','devtools/terminal_school_input.py',
    'devtools/terminal_school_preparation_contract.py','devtools/terminal_battle_input.py',
    'devtools/terminal_scene_owner_contract.py','devtools/terminal_story_catalog.py',
    'devtools/terminal_owned_mouse.py',
    'devtools/native_input_isolation.py','devtools/isolated_vm_preflight.py',
    'devtools/isolated_guest_focus.py','devtools/terminal_input_window.py',
    'devtools/terminal_battle_notice.py',
    'analysis/terminal-school-input-authorization-v2-20261109.json')


def read_report(path,digest):
    path=Path(path);need(path.stat().st_size<=24*1024*1024,'compressed new source budget')
    data=path.read_bytes();need(owner.sha(data)==digest,'fixed supplied new source SHA')
    with gzip.open(path,'rb')as stream:raw=stream.read(192*1024*1024+1)
    need(len(raw)<=192*1024*1024,'bounded expanded new source')
    return json.loads(raw)


def identities(paths):
    result=[]
    for path in paths:
        b=(ROOT/path).read_bytes();result.append(dict(path=path,bytes=len(b),sha256=owner.sha(b)))
    return result


def verify_implementations(report):
    parent=identities(PARENT_IMPLEMENTATIONS);layers=identities(LAYER_IMPLEMENTATIONS)
    need(report['parent_implementations']==parent and parent[0]['sha256']==menu.V6_COLLECTOR_SHA,
         'exact frozen parent collector/input implementation set')
    need(report['implementation_layers']==layers and report['observer']==parent[2],
         'exact new collector/input/catalog implementation layers and base identity')
    authorization=(ROOT/LAYER_IMPLEMENTATIONS[-1]).read_bytes();doc=json.loads(authorization)
    need(doc['prior_explicit_mouse_override']==dict(path=menu.AUTHORIZATION,sha256=menu.AUTHORIZATION_SHA)
         and doc['maximum_mouse_actions']==7 and doc['story_phase_budgets']==[192,192,64]
         and len(doc['mouse_actions'])==7 and doc['keyboard_authorization_record']==menu.STORY_IMPLEMENTATIONS[-1]
         and doc['notice_confirmation_is_separate_from_ADV_opcode51'] is True,
         'continued explicit original input authorization scope')
    owner.false_fields(doc,('game_memory_or_result_writes_authorized','forced_task_termination_as_handoff_authorized',
                           'approval_repeated'))
    need(doc['all_inputs_require_current_private_Job_PID_HWND_unlocked_desktop_foreground_original_state_and_code']is True
         and doc['source_implementation_identities_bound_separately']is True,'original owned-input safety scope')
    original=(ROOT/menu.AUTHORIZATION).read_bytes();need(owner.sha(original)==menu.AUTHORIZATION_SHA,'immutable original mouse approval')
    need(json.loads(original)['backend']==menu.authorization_backend(),'actual historical mouse approval backend')
    keyboard=(ROOT/menu.STORY_IMPLEMENTATIONS[-1]).read_bytes()
    need(owner.sha(keyboard)==menu.STORY_AUTHORIZATION_SHA and json.loads(keyboard)['approved']is True,'fixed original keyboard approval')
    return dict(parent=parent,layers=layers)


def _verify_file(path,digest,report,startup_root=None):
    raw=menu.contract.read_source();implementations=verify_implementations(report)
    isolation=verify_input_isolation(report['input_isolation'])
    need(report['original']==dict(path='analysis/hermit_game.exe',bytes=len(raw),sha256=menu.contract.SOURCE_SHA),
         'fixed original mapped image identity')
    parent=owner.read_report(ROOT/startup.PARENT,startup.PARENT_SHA);pr=parent['runtime'];runtime=report['runtime']
    need(runtime['immutable_files_reference']==dict(path=startup.PARENT,sha256=startup.PARENT_SHA,
        rows=len(pr['immutable_files']),freshly_hashed_this_lifetime=True),'fixed freshly checked native asset inventory')
    need({k:v for k,v in runtime.items()if k!='immutable_files_reference'}==
         {k:v for k,v in pr.items()if k!='immutable_files'},'exact private runtime metadata')
    wanted={str(Path(pr['private_root'])/r['path']).replace('\\','/'):r['private_sha256']for r in pr['private_writable_files']}
    restored=report['mutable_private_runtime_files']
    need(len(restored)==len(wanted) and {r['path']for r in restored}==set(wanted) and
         all(r['restored_exact']is True and r['sha256']==wanted[r['path']]for r in restored),'all private mutable files restored exactly')
    need(owner.sha((ROOT/owner.APP).read_bytes())=='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7',
         'exact private original executable')
    tls=report['probe']['TLS_implementation'];pe=menu._module(tls['module_path'],tls['module_sha256'])
    ex=next(x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'TlsGetValue')
    need(ex.forwarder is None and ex.address==tls['RVA'] and pe.get_data(ex.address,64).hex()==tls['code_hex'],
         'actual current x86 OS TLS implementation')
    inventory={r['path'].upper():r for r in pr['immutable_files']}
    result=verify_report(report,raw,inventory,startup_root=startup_root)
    result.update(source_report=dict(path=str(Path(path).resolve()),bytes=Path(path).stat().st_size,sha256=digest),
        input_isolation=isolation,
        verifier_sha256=owner.sha(Path(__file__).read_bytes()),implementation_identities=implementations,
        native_dependency_attestation_complete=False,current_verification_dependencies=identities((
            'devtools/terminal_menu_handoff_verification.py','devtools/terminal_scene_owner_verification.py',
            'devtools/terminal_startup_handoff_verification.py','devtools/terminal_menu_transition_contract.py',
            'devtools/terminal_school_preparation_contract.py','devtools/terminal_workroom_contract.py',
            'devtools/terminal_story_dispatch_verification.py',
            'tools/school_native_dialogue_verification.py','tools/school_native_scene_verification.py')))
    return result


def guest_module_key(path,digest):
    need(isinstance(path,str) and isinstance(digest,str) and re.fullmatch('[0-9a-f]{64}',digest),
         'explicit original guest module path and SHA')
    p=PureWindowsPath(path)
    need(p.is_absolute() and p.drive.lower()=='c:' and len(p.parts)==4 and
         tuple(s.lower()for s in p.parts[1:3])==('windows','syswow64') and
         re.fullmatch(r'[A-Za-z0-9_.-]+\.dll',p.name,re.I),
         'direct original guest C:/Windows/SysWOW64 DLL only')
    return str(p).lower(),digest


def guest_module_references(report):
    result=set();stack=[report]
    while stack:
        item=stack.pop()
        if isinstance(item,dict):
            if 'module_path'in item:
                result.add(guest_module_key(item['module_path'],item.get('module_sha256')))
            stack.extend(item.values())
        elif isinstance(item,list):stack.extend(item)
    need(0<len(result)<=16,'bounded complete recorded guest module set')
    return result


class GuestModuleSources:
    """Explicit authenticated copies; never fall back to a host same-name DLL."""
    def __init__(self,manifest,report,digest):
        import pefile
        root=(ROOT/'.venv-audit/native-worker').resolve()
        path=Path(manifest).resolve()
        need(path.is_relative_to(root) and path.is_file() and 0<path.stat().st_size<=65536,
             'bounded manifest inside owned host worker root')
        raw=path.read_bytes();doc=json.loads(raw)
        need(set(doc)=={'schema_version','kind','guest_uuid','guest_boot_utc','source_report_sha256','modules'} and
             type(doc['schema_version'])is int and doc['schema_version']==1 and
             doc['kind']=='isolated_guest_system_module_sources',
             'explicit guest DLL source manifest schema')
        isolation=verify_input_isolation(report['input_isolation'])
        need(doc['source_report_sha256']==digest and
             doc['guest_uuid'].lower()==isolation['current_guest_uuid'].lower() and
             doc['guest_boot_utc']==isolation['current_guest_boot_utc'],
             'module copies bound to exact source report guest and boot')
        rows=doc['modules'];need(isinstance(rows,list) and 0<len(rows)<=16,'bounded guest DLL manifest')
        self.modules={};self.records=[];paths=set();total=0
        for row in rows:
            need(set(row)=={'module_path','module_sha256','local_path','bytes'},'exact guest DLL mapping fields')
            key=guest_module_key(row['module_path'],row['module_sha256'])
            need(key not in self.modules and key[0]not in paths,'no duplicate or conflicting guest DLL mappings')
            paths.add(key[0]);local=Path(row['local_path'])
            need(local.is_absolute(),'explicit absolute host guest-DLL copy path')
            local=local.resolve()
            need(local.is_relative_to(root/'guest-system-dlls') and local.is_file(),
                 'guest DLL copy confined to owned host system-DLL directory')
            need(local.name.lower()==PureWindowsPath(row['module_path']).name.lower(),
                 'guest DLL copy filename retains original module identity')
            need(type(row['bytes'])is int and 0<row['bytes']<=32*1024*1024 and local.stat().st_size==row['bytes'],
                 'bounded exact guest DLL copy size')
            total+=row['bytes'];need(total<=128*1024*1024,'bounded total guest DLL copies')
            data=local.read_bytes();need(owner.sha(data)==key[1],'exact recorded guest DLL copy SHA')
            pe=pefile.PE(data=data)
            need(pe.FILE_HEADER.Machine==0x14C and pe.OPTIONAL_HEADER.Magic==0x10B and
                 pe.FILE_HEADER.Characteristics&0x2000 and hasattr(pe,'DIRECTORY_ENTRY_EXPORT'),
                 'actual x86 PE32 exported guest DLL')
            self.modules[key]=pe
            self.records.append(dict(row,local_path=str(local)))
        need(set(self.modules)==guest_module_references(report),'exact complete guest module mappings without extras')
        self.identity=dict(manifest_path=str(path),bytes=len(raw),sha256=owner.sha(raw),
            source_report_sha256=digest,guest_uuid=doc['guest_uuid'],guest_boot_utc=doc['guest_boot_utc'],
            modules=self.records,host_system_DLL_fallback=False)

    def load(self,path,digest):
        key=guest_module_key(path,digest)
        need(key in self.modules,'requested guest DLL has an exact manifest mapping')
        return self.modules[key]

    @contextmanager
    def scope(self):
        # Frozen verify_export resolves _module through its module globals;
        # cloned story verifiers call that same verify_export function. The
        # per-manifest dictionary never consumes or populates the host LRU.
        previous=menu._module;menu._module=self.load
        try:yield
        finally:menu._module=previous


def verify_file(path,digest,guest_modules=None):
    report=read_report(path,digest)
    if guest_modules is None:return _verify_file(path,digest,report)
    sources=GuestModuleSources(guest_modules,report,digest)
    runtime=guest_runtime_location(report)
    with sources.scope():result=_verify_file(path,digest,report,Path(runtime['guest_project_root']))
    result['guest_system_module_sources']=sources.identity
    result['guest_runtime_location']=runtime
    return result


def guest_runtime_location(report):
    """Only the private original EXE location differs, never its asset identity."""
    root=PureWindowsPath('C:/ChaomofaWorker/project')
    relative=PureWindowsPath(owner.APP)
    need(not relative.is_absolute() and '..'not in relative.parts,'fixed original private executable layout')
    actual=PureWindowsPath(report['probe']['startup']['process_image'])
    need(actual==root/relative and len(actual.parts)==len(root.parts)+len(relative.parts),
         'exact dedicated guest private original executable relative layout')
    return dict(guest_project_root=str(root),guest_process_image=str(actual),
        private_relative_executable=owner.APP,host_original_copy=str((ROOT/owner.APP).resolve()),
        original_executable_sha256='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7',
        original_asset_identity_checks_unchanged=True)


def verify_input_isolation(receipt):
    """Authenticate the exact embedded guest qualification, never a success flag."""
    from devtools.isolated_vm_preflight import verify
    raw=receipt['source_utf8'].encode('utf8')
    need(0<len(raw)<=128*1024 and len(raw)==receipt['bytes'] and owner.sha(raw)==receipt['sha256'],
         'exact bounded qualification source bytes and SHA')
    need(receipt['path'].replace('\\','/').lower()=='c:/chaomofaworker/isolation-qualified.json',
         'dedicated guest qualification path')
    source=json.loads(raw);result=verify(source)
    need(source['guest']['machine']['uuid'].lower()==receipt['current_guest_uuid'].lower(),
         'qualification belongs to current guest UUID')
    machine=source['guest']['machine']
    need(receipt['current_guest_boot_utc']==machine['boot_utc'],
         'qualification belongs to current guest boot')
    need(receipt['current_guest_resources']=={k:machine[k]for k in ('logical_processors','memory_bytes')},
         'qualification binds actual guest resources')
    need(receipt['verification']==result,'qualification result independently recomputed')
    paths=('devtools/isolated_vm_preflight.py','devtools/isolated_windows_vm.py','devtools/isolated_guest_preflight.cs')
    actual=source['implementations'];expected=identities(paths)
    need(len(actual)==len(expected) and all(Path(a['path']).name==Path(e['path']).name and
         a['bytes']==e['bytes'] and a['sha256']==e['sha256']for a,e in zip(actual,expected)),
         'qualification implementation source identity')
    return dict(bytes=len(raw),sha256=receipt['sha256'],current_guest_uuid=receipt['current_guest_uuid'],
                current_guest_boot_utc=machine['boot_utc'],console_session=machine['session'],
                current_guest_resources=receipt['current_guest_resources'],
                verification=result,original_game_compatible=False)


def verify_guest_focus(receipt,isolation,pid,hwnd):
    """Validate the recorded guest-only operation path, not API success alone."""
    base={'hwnd','before','after','operations','guest_only','current_tid','console_session',
          'guest_uuid','guest_boot_utc','own_pid','own_session','target_pid','target_session',
          'foreground_wait_seconds'}
    attached={'attached_foreground','attached_tid','attached_pid','attached_session'}
    need(isinstance(receipt,dict) and base<=receipt.keys() and
         set(receipt)<=base|attached|{'elapsed'},'complete bounded guest focus receipt')
    need(receipt['guest_only']is True and receipt['hwnd']==receipt['after']==hwnd and
         receipt['target_pid']==pid,'actual owned target window and process')
    for key in ('current_tid','own_pid','target_pid'):
        need(type(receipt[key])is int and 0<receipt[key]<2**32,'actual guest focus participant ID')
    need(receipt['own_pid']!=pid,'observer is distinct from original game process')
    need(type(receipt['before'])is int and 0<=receipt['before']<2**64,'actual initial foreground window')
    session=isolation['console_session']
    need(all(type(receipt[k])is int and receipt[k]==session for k in
             ('console_session','own_session','target_session')),'same qualified active console session')
    need(receipt['guest_uuid'].lower()==isolation['current_guest_uuid'].lower() and
         receipt['guest_boot_utc']==isolation['current_guest_boot_utc'],'same qualified guest UUID and boot')
    wait=number(receipt['foreground_wait_seconds'],'foreground acknowledgement time')
    need(0<=wait<=.35,'bounded .30s foreground acknowledgement with .05s scheduling tolerance')
    ops=receipt['operations']
    need(isinstance(ops,list) and len(ops)<=4 and all(isinstance(o,dict) and
         set(o)=={'name','result'} and type(o['result'])is bool for o in ops),'bounded actual foreground operations')
    prefix=['SetForegroundWindow']if receipt['before']!=hwnd else []
    names=[o['name']for o in ops]
    uses_attach=names==prefix+['AttachThreadInput','SetForegroundWindow','DetachThreadInput']
    need(names==prefix or uses_attach,'exact original guest focus operation sequence')
    if uses_attach:
        need(attached<=receipt.keys(),'actual attachment participant evidence')
        for key in ('attached_tid','attached_pid'):
            need(type(receipt[key])is int and 0<receipt[key]<2**32,'actual attached guest participant')
        need(type(receipt['attached_foreground'])is int and 0<receipt['attached_foreground']<2**64 and
             receipt['attached_tid']!=receipt['current_tid'],'distinct actual foreground queue')
        if receipt['attached_foreground']==hwnd:
            need(receipt['attached_pid']==pid,'target foreground queue belongs to actual game PID')
        need(type(receipt['attached_session'])is int and receipt['attached_session']==session,
             'attachment stays inside qualified guest console session')
        need(ops[len(prefix)]['result']is True and ops[-1]['result']is True,
             'actual successful queue attachment and detachment')
    else:need(not attached.intersection(receipt),'no invented attachment evidence on direct path')
    # SetForegroundWindow's BOOL is not the completion test. The actual final
    # foreground query and owned-target guard must agree, including asynchronous
    # acknowledgement after the recorded bounded wait.
    return dict(path='attached'if uses_attach else 'direct',receipt=copy.deepcopy(receipt),
                full_desktop_API_trace_proved=False)


def guest_focus_view(report,isolation,pid,hwnd):
    """Private shallow views preserve all original input/VM/memory evidence.

    Empty legacy operations mean this old verifier is delegated only edge
    validation. Actual focus operations have already passed the independent
    contract and remain verbatim in the returned observations and source.
    """
    observations=[]
    def activation(actual,label):
        observations.append(dict(location=label,**verify_guest_focus(actual,isolation,pid,hwnd)))
        return dict(actual,operations=[])
    def action(actual,label):
        return dict(actual,activation=activation(actual['activation'],label))
    p=report['probe'];view=dict(p);result=dict(report,probe=view)
    early=report.get('startup_activation',[])
    need(isinstance(early,list) and len(early)<=1,'bounded early guest focus')
    result['startup_activation']=[]
    for index,a in enumerate(early):
        if 'error'in a:
            need(set(a)=={'elapsed','error'} and isinstance(a['error'],str),'explicit early focus failure')
            result['startup_activation'].append(dict(a))
        else:result['startup_activation'].append(activation(a,'startup:'+str(index)))
    controller=p['mouse_controller'];receipt=controller.get('receipt')
    need(p['collector_input_actions']==([receipt]if receipt is not None else []),
         'actual title receipt aliases match before compatibility view')
    if receipt is not None:
        adapted=action(receipt,'title')
        view['mouse_controller']=dict(controller,receipt=adapted)
        view['collector_input_actions']=[adapted]
    view['story_phases']=[]
    for i,phase in enumerate(p['story_phases']):
        view['story_phases'].append(dict(phase,actions=[action(a,'story:%d:%d'%(i,j))
            for j,a in enumerate(phase['actions'])]))
    for key in ('workroom_inputs','school_inputs','notice_inputs','battle_inputs'):
        view[key]=[action(a,key+':'+str(j))for j,a in enumerate(p[key])]
    need(len({o['receipt']['own_pid']for o in observations})<=1,
         'all guest activations belong to the same collector process lifetime')
    return result,observations


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True)
    p.add_argument('--sha256',required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--guest-modules',type=Path);args=p.parse_args()
    result=verify_file(args.report,args.sha256,args.guest_modules)
    with args.out.open('x',encoding='utf-8',newline='\n')as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps(dict(status=result['status'],accepted=False)))


if __name__=='__main__':main()
