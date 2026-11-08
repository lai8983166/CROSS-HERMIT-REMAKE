"""Two authorized original school task-1 controls; no game-memory writes."""
import struct
import time

from devtools import terminal_owned_mouse as mouse
from devtools import terminal_scene_owner as base
from devtools import terminal_school_preparation_contract as contract
from devtools.terminal_scene_resources import clone
from devtools.terminal_startup_handoff import graph
from devtools.terminal_workroom_input import make_api
from tools.school_native_dialogue_input import owned_target_guard

GROUP=0x5A0A40
UI=0x5A0C18
TARGETS={'departure':contract.DEPART_TARGET,'confirmation':contract.CONFIRM_TARGET}
MODES={'departure':0,'confirmation':14}
INPUT_RANGES=tuple(contract.RANGES.values())+(
    (0x61B628,0x61B63A),(0x625558,0x625560),(0x73BFD0,0x73C0D0),
    (0x5A0A40,0x5A0A48),(0x5A0C18,0x5A0C20),
    (0x411DF0,0x4120A0),(0x414400,0x414439))


def _blob(value,size,label):
    base.need(isinstance(value,str) and len(value)==size*2,label+' hex length')
    data=bytes.fromhex(value);base.need(len(data)==size,label+' byte length');return data


def capture(c):
    """Caller must hold original.frozen; all reads bounded and originals only."""
    manager,rows=graph(c)
    nodes=[]
    for entry in rows:
        if base.word(bytes.fromhex(entry['head_hex']))==GROUP:
            pointer=entry['pointer']
            nodes.append(dict(pointer=pointer,header_hex=c.get(pointer,64).hex(),
                control_pointer=pointer+0x76BC,control_hex=c.get(pointer+0x76BC,16).hex(),
                selection_pointer=pointer+0x7950,selection_hex=c.get(pointer+0x7950,2).hex()))
    count=int.from_bytes(c.get(0x7A5B62,2),'little',signed=True)
    base.need(0<=count<=80,'bounded original school task ledger')
    fields=((0x7A528E,4,'date_hex'),(0x7A55FA,2,'gate_hex'),
        (0x7AAB08,20,'selected_hex'),(0x7AAA12,140,'classes_hex'),
        (0x7D6A26,1,'ready_hex'),(0x7A4E60,2,'school_ui_state_hex'))
    return dict(nodes=nodes,ledger_count=count,ledger_pointer=0x7A5662,
        ledger_hex=c.get(0x7A5662,count*16).hex() if count else '',
        fields=[dict(pointer=a,bytes=n,name=name,hex=c.get(a,n).hex())for a,n,name in fields])


def validate_preparation(data,stage):
    """Narrow current new-game/task1 contract, fail closed on other schools."""
    base.need(stage in MODES,'one of two original school controls')
    expected=((0x7A528E,4,'date_hex'),(0x7A55FA,2,'gate_hex'),
        (0x7AAB08,20,'selected_hex'),(0x7AAA12,140,'classes_hex'),
        (0x7D6A26,1,'ready_hex'),(0x7A4E60,2,'school_ui_state_hex'))
    rows=data['fields']
    base.need(isinstance(rows,list) and len(rows)==len(expected),'complete bounded school fields')
    values={}
    for row,(address,size,name) in zip(rows,expected):
        base.need((row['pointer'],row['bytes'],row['name'])==(address,size,name),'original school field identity')
        values[name]=_blob(row['hex'],size,name)
    base.need(values['date_hex']==struct.pack('<HH',4,1),'initial actual month/week4/1')
    base.need(values['gate_hex']==b'\x01\x00' and values['ready_hex']==b'\x01','original mandatory ready gate')
    base.need(values['school_ui_state_hex']==b'\0\0','original school companion active')
    selection=values['selected_hex']
    base.need(struct.unpack_from('<H',selection,2)[0]==1 and struct.unpack_from('<H',selection,14)[0]==1,
              'original mandatory task1 selected')
    base.need(type(data['ledger_count']) is int and data['ledger_count']==1 and data['ledger_pointer']==0x7A5662,
              'current minimal task1 ledger only')
    ledger=_blob(data['ledger_hex'],16,'task1 ledger')
    base.need(struct.unpack_from('<H',ledger)[0]==1 and ledger[2]==1 and ledger[3]==3
              and ledger[5]==0 and ledger[6]==0,'enabled original mandatory task1 ledger row')
    classes=values['classes_hex']
    base.need(struct.unpack_from('<h',classes)[0]==101 and classes[3]==0
              and struct.unpack_from('<4h',classes,16)==(3,4,9,-1),'unchanged legal initial adventure class')
    base.need(all(struct.unpack_from('<h',classes,i*28)[0]==-1 for i in range(1,5)),
              'no additional teacher class requiring readiness proof')
    base.need(len(data['nodes'])==1,'one original school grouping node')
    node=data['nodes'][0];pointer=node['pointer'];header=_blob(node['header_hex'],64,'group header')
    base.need(0x10000<=pointer<0x80000000 and base.word(header)==GROUP,'actual school grouping object')
    control=_blob(node['control_hex'],16,'group control')
    base.need(node['control_pointer']==pointer+0x76BC and node['selection_pointer']==pointer+0x7950,'group field pointers')
    base.need(struct.unpack_from('<H',header,0x30)[0]==0 and
              tuple(struct.unpack_from('<H',control,o)[0]for o in (0,2,4,8,10))==(0,1,1,1,MODES[stage])
              and _blob(node['selection_hex'],2,'group selection')==b'\0\0','current original school selector phase')
    return pointer,base.word(header,0x24)


def ready(row,stage):
    try:
        pointer,tid=validate_preparation(row['school'],stage)
        tasks=row['tasks']
        if len(tasks)!=2 or {t['vtable']for t in tasks}!={GROUP,UI}:return False
        group=next(t for t in tasks if t['vtable']==GROUP)
        if group['pointer']!=pointer or group['thread_id']!=tid or 'TLS' not in group:return False
        if base.word(_blob(row['MAIN_event_hex'],8,'MAIN event')):return False
        frame=next((f for f in row['frames'] if f['tid']==tid),None)
        return bool(frame and {0x4A7CEA,0x4AB7F1,0x421F8A,0x56E183}<={f['return_va']for f in frame['chain']})
    except (KeyError,ValueError,TypeError,StopIteration,struct.error):
        return False


def guarded_click(api,guard,stage,sleep=time.sleep):
    base.need(stage in TARGETS,'one of two fixed school controls')
    return clone(mouse.guarded_click,TARGETS={0:TARGETS[stage]})(api,guard,TARGETS[stage],sleep,absolute=True)


def action(c,hwnd,stage,*,explicit_user_override=False):
    if explicit_user_override is not True:
        raise PermissionError('explicit owned mouse authorization required')
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    base.need(stage in TARGETS,'one of two fixed school controls')
    source=base.SOURCE.read_bytes();base.need(base.sha(source)==base.SOURCE_SHA,'fixed original image')
    game=base.word(c.get(0x7A49FC,4))
    exports={slot:base.resolve(c.pid,'user32.dll',name)for slot,name in
        ((0x59236C,'GetCursorPos'),(0x592368,'ScreenToClient'))}
    def guard():
        owned_target_guard(c,hwnd)
        with base.original.frozen(c.h,c.pid) as frames:
            manager,rows=graph(c)
            base.need(len(rows)==2 and {base.word(bytes.fromhex(r['head_hex']))for r in rows}=={GROUP,UI},
                      'exact two original school owners')
            base.need(base.word(c.get(c.main+0x2C,4))==0,'idle original MAIN event')
            observed=capture(c);pointer,tid=validate_preparation(observed,stage)
            frame=next((f for f in frames if f['tid']==tid),None)
            waits=[f for f in frame['chain']if f['return_va']==0x4A7CEA]if frame else []
            base.need(len(waits)==1 and {0x4AB7F1,0x421F8A,0x56E183}<={f['return_va']for f in frame['chain']},
                      'current original school selector and CRT wait ancestry')
            selector=waits[0]['saved_bp']
            base.need(base.word(c.get(selector-4,4))==pointer and base.word(c.get(selector+4,4))==0x4AB7F1,
                      'actual school selector this and caller')
            tls=base.capture_tls(c,frame,pointer)
            tls['index_memory']=dict(pointer=0x761BC0,hex=c.get(0x761BC0,4).hex())
            if tls['TLS_index']>=64:
                expansion=tls['TEB']+0xF94
                tls['expansion_memory']=dict(pointer=expansion,hex=c.get(expansion,4).hex())
            base.need(base.word(c.get(0x7A49FC,4))==game and base.word(c.get(0x7A0BB4,4))==hwnd
                      and base.word(c.get(game+0xB250,4))in(0,1),'actual input owner window and mode')
            for slot,export in exports.items():base.need(base.word(c.get(slot,4))==export['target'],'actual cursor API target')
            code=[]
            for a,b in INPUT_RANGES:
                data=c.get(a,b-a);base.need(data==source[a-0x400000:b-0x400000],'original school input source bytes')
                code.append(dict(pointer=a,bytes=b-a,sha256=base.sha(data)))
            return dict(pid=c.pid,hwnd=hwnd,game=game,main=c.main,node=pointer,stage=stage,
                selector_pointer=selector,selector_hex=c.get(selector-4,12).hex(),
                school=observed,TLS=tls,head_hex=c.get(pointer,64).hex(),manager_hex=manager.hex(),
                registered_tasks=rows,MAIN_event_hex=c.get(c.main+0x2C,8).hex(),frame=frame,
                cursor_hex=c.get(game+0x196C,8).hex(),coordinate_mode_hex=c.get(game+0xB250,4).hex(),
                input_HWND_hex=c.get(0x7A0BB4,4).hex(),code=code,producer_exports=exports,
                IAT=[dict(slot=p,hex=c.get(p,4).hex())for p in exports],all_threads_resumed_before_input=True)
    result=guarded_click(make_api(c,hwnd,game),guard,stage)
    result['stage']=stage
    return result
