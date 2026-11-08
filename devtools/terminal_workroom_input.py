"""Explicitly authorized owned-window input for the original workroom exit only."""
import ctypes as C
import ctypes.wintypes as W
import struct
import time

from devtools import terminal_owned_mouse as mouse
from devtools import terminal_scene_owner as base
from devtools.terminal_scene_resources import clone
from devtools.terminal_workroom_contract import TARGET
from devtools.terminal_startup_handoff import graph
from tools.school_native_dialogue_input import INPUT,owned_target_guard

WORKROOM=0x5A0904
INPUT_RANGES=((0x49FD50,0x49FFF0),(0x4D5B70,0x4D5BEC),(0x4D5EC0,0x4D5FA7),
              (0x4A1570,0x4A1750),(0x411DF0,0x4120A0),(0x414400,0x414439),
              (0x5A0904,0x5A0930))
word=base.word


def ready(row):
    tasks=row['tasks']
    if len(tasks)!=1 or tasks[0]['vtable']!=WORKROOM or word(bytes.fromhex(row['MAIN_event_hex'])):
        return False
    task=tasks[0];head=bytes.fromhex(task['header_hex'])
    if len(head)!=64 or struct.unpack_from('<H',head,0x30)[0]!=1 or 'TLS' not in task:return False
    frame=next((f for f in row['frames'] if f['tid']==task['thread_id']),None)
    return bool(frame and {0x49FF57,0x4A15D0,0x421F8A,0x56E183}<={f['return_va']for f in frame['chain']})


def guarded_click(api,guard,sleep=time.sleep):
    # New reviewed target, original generic safety/release algorithm unchanged.
    return clone(mouse.guarded_click,TARGETS={0:TARGET})(api,guard,TARGET,sleep,absolute=True)


def owned_workroom_exit(c,hwnd,*,explicit_user_override=False):
    if explicit_user_override is not True:raise PermissionError('explicit owned mouse authorization required')
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    game=word(c.get(0x7A49FC,4));original=base.original;source=base.SOURCE.read_bytes()
    base.need(base.sha(source)==base.SOURCE_SHA,'fixed original source')
    exports={slot:base.resolve(c.pid,'user32.dll',name)for slot,name in
             ((0x59236C,'GetCursorPos'),(0x592368,'ScreenToClient'))}
    def guard():
        owned_target_guard(c,hwnd)
        with original.frozen(c.h,c.pid) as frames:
            manager,rows=graph(c)
            base.need(len(rows)==1 and word(bytes.fromhex(rows[0]['head_hex']))==WORKROOM,
                      'sole original workroom owner')
            base.need(word(c.get(c.main+0x2C,4))==0,'idle original MAIN event')
            pointer=rows[0]['pointer'];head=c.get(pointer,64);tid=word(head,0x24)
            base.need(struct.unpack_from('<H',head,0x30)[0]==1,'workroom original selection state')
            frame=next((f for f in frames if f['tid']==tid),None)
            waits=[f for f in frame['chain']if f['return_va']==0x49FF57]if frame else []
            base.need(len(waits)==1 and {0x4A15D0,0x421F8A,0x56E183}<={f['return_va']for f in frame['chain']},
                      'current original workroom selection wait and CRT ancestry')
            selector=waits[0]['saved_bp']
            base.need(word(c.get(selector-4,4))==pointer and word(c.get(selector+4,4))==0x4A15D0,
                      'actual workroom selector owner and caller')
            base.need(struct.unpack('<H',c.get(selector-0x18,2))[0]==1,'original selection has not already accepted input')
            tls=base.capture_tls(c,frame,pointer)
            tls['index_memory']=dict(pointer=0x761BC0,hex=c.get(0x761BC0,4).hex())
            if tls['TLS_index']>=64:
                p=tls['TEB']+0xF94;tls['expansion_memory']=dict(pointer=p,hex=c.get(p,4).hex())
            base.need(word(c.get(0x7A0BB4,4))==hwnd and word(c.get(game+0xB250,4)) in (0,1),
                      'actual input window and coordinate mode')
            for slot,export in exports.items():base.need(word(c.get(slot,4))==export['target'],'actual cursor API target')
            code=[]
            for a,b in INPUT_RANGES:
                actual=c.get(a,b-a);base.need(actual==source[a-0x400000:b-0x400000],'original workroom input bytes')
                code.append(dict(pointer=a,bytes=b-a,sha256=base.sha(actual)))
            return dict(pid=c.pid,hwnd=hwnd,game=game,main=c.main,node=pointer,
                selector_pointer=selector,selector_hex=c.get(selector-0x1C,0x24).hex(),
                head_hex=head.hex(),manager_hex=manager.hex(),MAIN_event_hex=c.get(c.main+0x2C,8).hex(),frame=frame,TLS=tls,
                cursor_hex=c.get(game+0x196C,8).hex(),coordinate_mode_hex=c.get(game+0xB250,4).hex(),
                input_HWND_hex=c.get(0x7A0BB4,4).hex(),code=code,producer_exports=exports,
                IAT=[dict(slot=p,hex=c.get(p,4).hex())for p in exports],all_threads_resumed_before_input=True)
    return guarded_click(make_api(c,hwnd,game),guard)


def make_api(c,hwnd,game):
    original=base.original
    class Api:
        @staticmethod
        def geometry(target):
            mode=word(c.get(game+0xB250,4));point=W.POINT(*target)
            if mode==1:
                original.check(original.ubind('ClientToScreen',W.BOOL,[W.HWND,C.POINTER(W.POINT)])(hwnd,C.byref(point)),
                               'original client target mapped to screen')
            elif mode!=0:raise ValueError('unknown coordinate mode')
            rect=W.RECT();original.check(original.ubind('GetWindowRect',W.BOOL,[W.HWND,C.POINTER(W.RECT)])(hwnd,C.byref(rect)),
                                        'current owned bounds')
            base.need(rect.left<=point.x<rect.right and rect.top<=point.y<rect.bottom,'target within owned window')
            base.need(original.ubind('WindowFromPoint',W.HWND,[W.POINT])(point)==hwnd,'target not covered')
            metric=original.ubind('GetSystemMetrics',C.c_int,[C.c_int])
            return dict(screen_target=[point.x,point.y],virtual_desktop=[metric(i)for i in (76,77,78,79)],
                        window_rect=[rect.left,rect.top,rect.right,rect.bottom],coordinate_mode=mode,point_window=hwnd)
        @staticmethod
        def position():return struct.unpack('<ii',c.get(game+0x196C,8))
        @staticmethod
        def left_button_down():return bool(original.ubind('GetAsyncKeyState',C.c_short,[C.c_int])(1)&0x8000)
        @staticmethod
        def submit(value):
            return original.ubind('SendInput',W.UINT,[W.UINT,C.POINTER(INPUT),C.c_int])(1,C.byref(value),C.sizeof(INPUT))
        @staticmethod
        def final_guard():owned_target_guard(c,hwnd)
    return mouse.attach_cursor_snapshot(Api(),c,hwnd,game)
