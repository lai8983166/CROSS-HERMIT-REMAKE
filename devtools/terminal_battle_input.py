"""Real retreat request/confirmation, only at the original ordinary battle wait."""
import struct
import time

from devtools import terminal_owned_mouse as mouse
from devtools import terminal_scene_owner as base
from devtools.terminal_scene_resources import clone
from devtools.terminal_startup_handoff import graph
from devtools.terminal_workroom_input import make_api
from tools.school_native_dialogue_input import owned_target_guard

BATTLE=0x59A430
TARGETS={'request':(48,12),'confirmation':(568,390)}
INPUT_RANGES=((0x4539B0,0x453CFC),(0x453D00,0x453E04),(0x458580,0x458929),
    (0x456B20,0x456B58),(0x454C40,0x454C7A),(0x4577F0,0x45782B),
    (0x46B470,0x46B663),(0x411DF0,0x4120A0),(0x414400,0x414439),(0x60CB18,0x60CB28))


def capture(c,pointer):
    return dict(pointer=pointer,network_hex=c.get(0x7F4491,1).hex(),
        panel_pointer=pointer+0x117F20,panel_hex=c.get(pointer+0x117F20,1).hex(),
        controller_pointer=pointer+0x190,
        controller_activity_hex=c.get(pointer+0x190+0x108B32,0x20).hex(),
        backpointer_hex=c.get(pointer+0x190+0x117C38,4).hex())


def ready(row,stage):
    if stage not in TARGETS:return False
    tasks=row['tasks']
    if len(tasks)!=1 or tasks[0]['vtable']!=BATTLE:return False
    task=tasks[0];head=bytes.fromhex(task.get('scene_head_hex',''));gates=task.get('battle_gates')
    if len(head)!=0x200 or not gates or 'TLS' not in task:return False
    if row['scene_global']!=task['pointer'] or base.word(bytes.fromhex(row['MAIN_event_hex'])):return False
    activity=bytes.fromhex(gates['controller_activity_hex'])
    if not (gates['pointer']==task['pointer'] and gates['network_hex']=='00' and gates['panel_hex']=='00'
            and gates['controller_pointer']==task['pointer']+0x190 and gates['panel_pointer']==task['pointer']+0x117F20
            and base.word(bytes.fromhex(gates['backpointer_hex']))==task['pointer'] and len(activity)==0x20
            and struct.unpack_from('<h',activity)[0]!=0 and activity[8]!=0):return False
    if head[0x30]!=(0 if stage=='request' else 1) or head[0x31] or (head[0x43] and head[0x59]) or base.word(head,0x38)!=5:
        return False
    frame=next((f for f in row['frames']if f['tid']==task['thread_id']),None)
    return bool(frame and {0x453CB5,0x451ABC,0x451716,0x421F8A,0x56E183}<={f['return_va']for f in frame['chain']})


def guarded_click(api,guard,stage,sleep=time.sleep):
    base.need(stage in TARGETS,'only original retreat request or confirmation')
    return clone(mouse.guarded_click,TARGETS={0:TARGETS[stage]})(api,guard,TARGETS[stage],sleep,absolute=True)


def action(c,hwnd,stage,*,explicit_user_override=False):
    if explicit_user_override is not True:raise PermissionError('explicit owned mouse authorization required')
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    base.need(stage in TARGETS,'reviewed retreat control');source=base.SOURCE.read_bytes()
    base.need(base.sha(source)==base.SOURCE_SHA,'fixed original source');game=base.word(c.get(0x7A49FC,4))
    exports={slot:base.resolve(c.pid,'user32.dll',name)for slot,name in
             ((0x59236C,'GetCursorPos'),(0x592368,'ScreenToClient'))}
    def guard():
        owned_target_guard(c,hwnd)
        with base.original.frozen(c.h,c.pid)as frames:
            manager,nodes=graph(c)
            base.need(len(nodes)==1 and base.word(bytes.fromhex(nodes[0]['head_hex']))==BATTLE,'sole current original battle')
            pointer=nodes[0]['pointer'];head=c.get(pointer,0x200);tid=base.word(head,0x24)
            frame=next((f for f in frames if f['tid']==tid),None)
            base.need(frame is not None,'current battle worker context')
            tls=base.capture_tls(c,frame,pointer);gates=capture(c,pointer)
            tls['index_memory']=dict(pointer=0x761BC0,hex=c.get(0x761BC0,4).hex())
            if tls['TLS_index']>=64:
                p=tls['TEB']+0xF94;tls['expansion_memory']=dict(pointer=p,hex=c.get(p,4).hex())
            task=dict(pointer=pointer,vtable=BATTLE,thread_id=tid,scene_head_hex=head.hex(),TLS=tls,battle_gates=gates)
            event=c.get(c.main+0x2C,8);scene=base.word(c.get(0x7A4174,4))
            base.need(ready(dict(tasks=[task],frames=frames,MAIN_event_hex=event.hex(),scene_global=scene),stage),
                      'original ordinary-loop retreat gates and owner')
            wait=next(f for f in frame['chain']if f['return_va']==0x453CB5);inner=wait['saved_bp']
            base.need(base.word(c.get(inner-4,4))==pointer and base.word(c.get(inner+4,4))==0x451ABC
                      and base.word(c.get(inner-8,4))==0,'actual scene this/caller and unaccepted result')
            base.need(base.word(c.get(0x7A49FC,4))==game and base.word(c.get(0x7A0BB4,4))==hwnd
                      and base.word(c.get(game+0xB250,4))in(0,1),'actual input window and coordinate mode')
            for slot,export in exports.items():base.need(base.word(c.get(slot,4))==export['target'],'actual cursor export')
            code=[]
            for a,b in INPUT_RANGES:
                value=c.get(a,b-a);base.need(value==source[a-0x400000:b-0x400000],'original retreat bytes')
                code.append(dict(pointer=a,bytes=b-a,sha256=base.sha(value)))
            return dict(pid=c.pid,hwnd=hwnd,game=game,main=c.main,node=pointer,stage=stage,
                inner_pointer=inner,inner_hex=c.get(inner-0x10,0x18).hex(),head_hex=head.hex(),battle_gates=gates,
                manager_hex=manager.hex(),MAIN_event_hex=event.hex(),scene_global=scene,TLS=tls,frame=frame,
                cursor_hex=c.get(game+0x196C,8).hex(),coordinate_mode_hex=c.get(game+0xB250,4).hex(),
                input_HWND_hex=c.get(0x7A0BB4,4).hex(),code=code,producer_exports=exports,
                IAT=[dict(slot=p,hex=c.get(p,4).hex())for p in exports],all_threads_resumed_before_input=True)
    result=guarded_click(make_api(c,hwnd,game),guard,stage);result['stage']=stage;return result
