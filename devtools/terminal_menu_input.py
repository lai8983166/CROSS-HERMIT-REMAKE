"""Reviewable, disabled-by-default mouse fallback for the private original menu.

Computer Use is the default. Calling the production entry requires a separate
explicit user override of that skill's JS-only rule; old scan-code permission
does not authorize this mouse backend. Unit tests inject an inert API only.
"""
import ctypes as C
import ctypes.wintypes as W
import time

from tools.school_native_dialogue_input import INPUT,MOUSEINPUT,owned_target_guard

TARGETS={0:(318,508),1:(318,540)}


def packet(dx=0,dy=0,flags=1):
    value=INPUT();value.type=0;value.data.mi=MOUSEINPUT(dx,dy,0,flags,0,0)
    return value


def absolute_coordinates(point,desktop):
    x,y=point;left,top,width,height=desktop
    if not all(type(v) is int for v in (*point,*desktop)) or width<=1 or height<=1:
        raise ValueError('integer nonempty virtual desktop')
    if not (left<=x<left+width and top<=y<top+height):raise ValueError('target outside virtual desktop')
    return (round((x-left)*65535/(width-1)),round((y-top)*65535/(height-1)))


def guarded_click(api,guard,target,sleep=time.sleep,*,absolute=False):
    """Feedback from actual game coordinates is mandatory before button-down."""
    if target not in TARGETS.values():raise ValueError('only reviewed original main-menu targets')
    receipt=dict(target=list(target),moves=[],down_submitted=False,released=False,error=None,
                 game_memory_written=False,transition_proved=False,guard_observations=[],
                 movement_mode='absolute_virtual_desktop' if absolute else 'relative_feedback')
    def checked():receipt['guard_observations'].append(guard())
    try:
        checked()
        if api.left_button_down():raise ValueError('left button already held; no action')
        for attempt in range(4):
            checked();position=api.position()
            if position==target:break
            if absolute:
                geometry=api.geometry(target)
                dx,dy=absolute_coordinates(geometry['screen_target'],geometry['virtual_desktop'])
                movement=packet(dx,dy,0xC001)
                entry=dict(before=list(position),normalized=[dx,dy],geometry=geometry,flags=0xC001)
            else:
                dx=max(-512,min(512,target[0]-position[0]));dy=max(-512,min(512,target[1]-position[1]))
                movement=packet(dx,dy);entry=dict(before=list(position),delta=[dx,dy])
            checked();sent=api.submit(movement)
            receipt['moves'].append(dict(**entry,submitted=sent))
            if sent!=1:raise ValueError('mouse movement submission failed')
            sleep(.05)
        checked();receipt['before_click']=list(api.position())
        if tuple(receipt['before_click'])!=target:raise ValueError('original game cursor did not reach reviewed target')
        if api.left_button_down():raise ValueError('left button changed before click')
        checked()
        if absolute:
            receipt['click_geometry']=api.geometry(target)
            absolute_coordinates(receipt['click_geometry']['screen_target'],receipt['click_geometry']['virtual_desktop'])
        receipt['down_wall_time_ns']=time.time_ns()
        receipt['down_result']=api.submit(packet(flags=2))
        if receipt['down_result']!=1:raise ValueError('left down was not submitted')
        receipt['down_submitted']=True
        sleep(.08)
        receipt['up_results']=[api.submit(packet(flags=4))]
        receipt['released']=receipt['up_results'][-1]==1
        receipt['up_wall_time_ns']=time.time_ns()
        if not receipt['released']:raise ValueError('left up was not submitted')
        # Post-input guard checks only the owned foreground target: the menu may
        # legitimately retire after the click, which is observed separately.
        api.final_guard()
    except Exception as exc:
        receipt['error']=repr(exc)
    finally:
        if receipt['down_submitted'] and not receipt['released']:
            try:
                receipt.setdefault('up_results',[]).append(api.submit(packet(flags=4)))
                receipt['released']=receipt['up_results'][-1]==1
            except Exception as exc:
                receipt['release_error']=repr(exc)
    return receipt


def owned_main_menu_click(c,hwnd,index,*,explicit_user_override=False):
    if explicit_user_override is not True:raise PermissionError('explicit user mouse fallback override required')
    if type(index) is not int or index not in TARGETS:raise ValueError('only new-game or load menu action')
    from devtools import terminal_scene_owner as base
    from devtools.terminal_startup_handoff import graph,MENU,word
    game=word(c.get(0x7A49FC,4));original=base.original
    source=base.SOURCE.read_bytes()
    if base.sha(source)!=base.SOURCE_SHA:raise ValueError('fixed original source identity')
    exports={slot:base.resolve(c.pid,'user32.dll',name) for slot,name in
             ((0x59236C,'GetCursorPos'),(0x592368,'ScreenToClient'))}
    def guard():
        owned_target_guard(c,hwnd)
        # All original threads paused only while checking. Never inject while
        # paused; every input occurs after this context has resumed them.
        with original.frozen(c.h,c.pid) as frames:
            _,rows=graph(c)
            if len(rows)!=1 or word(bytes.fromhex(rows[0]['head_hex']))!=MENU:
                raise ValueError('original menu must be sole registered task')
            if word(c.get(c.main+0x2C,4)):raise ValueError('original MAIN event must be idle')
            pointer=rows[0]['pointer'];head=bytes.fromhex(rows[0]['head_hex'])
            frame=next((f for f in frames if f['tid']==word(head,0x24)),None)
            waiting=[f for f in frame['chain'] if f['return_va']==0x45F065] if frame else []
            if len(waiting)!=1 or word(c.get(pointer+0x30,4))!=1:
                raise ValueError('original menu selector not waiting for a choice')
            selector=waiting[0]['saved_bp']
            if word(c.get(selector-4,4))!=pointer or word(c.get(selector+4,4))!=0x45EE6A:
                raise ValueError('actual selector stack owner/caller mismatch')
            if word(c.get(0x7A0BB4,4))!=hwnd or word(c.get(game+0xB250,4)) not in (0,1):
                raise ValueError('actual original input HWND/coordinate mode mismatch')
            for slot,export in exports.items():
                if word(c.get(slot,4))!=export['target']:raise ValueError('actual cursor API target mismatch')
            code=[]
            for a,b in ((0x45EFB0,0x45F0CB),(0x45F810,0x45F960),(0x60CEB0,0x60CEE0),
                        (0x411DF0,0x4120A0),(0x414400,0x414439)):
                actual=c.get(a,b-a)
                if actual!=source[a-0x400000:b-0x400000]:
                    raise ValueError('original menu input code/table changed')
                code.append(dict(pointer=a,bytes=b-a,sha256=base.sha(actual)))
            return dict(pid=c.pid,hwnd=hwnd,game=game,main=c.main,node=pointer,
                selector_pointer=selector,selector_hex=c.get(selector-0x10,0x1C).hex(),
                head_hex=c.get(pointer,64).hex(),manager_hex=c.get(c.main+0x64,0x120).hex(),
                MAIN_event_hex=c.get(c.main+0x2C,8).hex(),frame=frame,
                cursor_hex=c.get(game+0x196C,8).hex(),coordinate_mode_hex=c.get(game+0xB250,4).hex(),
                input_HWND_hex=c.get(0x7A0BB4,4).hex(),code=code,
                producer_exports=exports,IAT=[dict(slot=p,hex=c.get(p,4).hex()) for p in exports],
                all_threads_resumed_before_input=True)
    class Api:
        @staticmethod
        def geometry(target):
            mode=word(c.get(game+0xB250,4));point=W.POINT(*target)
            if mode==1:
                original.check(original.ubind('ClientToScreen',W.BOOL,[W.HWND,C.POINTER(W.POINT)])(hwnd,C.byref(point)),
                               'original client target mapped to screen')
            elif mode!=0:raise ValueError('unknown original coordinate mode')
            rectangle=W.RECT()
            original.check(original.ubind('GetWindowRect',W.BOOL,[W.HWND,C.POINTER(W.RECT)])(hwnd,C.byref(rectangle)),
                           'current target window bounds')
            if not (rectangle.left<=point.x<rectangle.right and rectangle.top<=point.y<rectangle.bottom):
                raise ValueError('mouse target is outside owned window')
            if original.ubind('WindowFromPoint',W.HWND,[W.POINT])(point)!=hwnd:
                raise ValueError('mouse target is covered by another window')
            metric=original.ubind('GetSystemMetrics',C.c_int,[C.c_int])
            return dict(screen_target=[point.x,point.y],virtual_desktop=[metric(i) for i in (76,77,78,79)],
                        window_rect=[rectangle.left,rectangle.top,rectangle.right,rectangle.bottom],
                        coordinate_mode=mode,point_window=hwnd)
        @staticmethod
        def position():
            import struct
            return struct.unpack('<ii',c.get(game+0x196C,8))
        @staticmethod
        def left_button_down():
            return bool(original.ubind('GetAsyncKeyState',C.c_short,[C.c_int])(1)&0x8000)
        @staticmethod
        def submit(value):
            return original.ubind('SendInput',W.UINT,[W.UINT,C.POINTER(INPUT),C.c_int])(1,C.byref(value),C.sizeof(INPUT))
        @staticmethod
        def final_guard():owned_target_guard(c,hwnd)
    return guarded_click(Api(),guard,TARGETS[index],absolute=True)
