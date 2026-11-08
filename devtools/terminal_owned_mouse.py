"""Exact game-coordinate feedback correction for bounded owned mouse input.

The original endpoint mapping is retained for the first movement. A same-window,
same-desktop feedback error of at most two pixels permits at most three small
normalized corrections. Final exact game coordinates and all guards still apply.
"""
import time
import struct
from devtools import terminal_menu_input as original
from devtools.terminal_scene_resources import clone

TARGETS=original.TARGETS
packet=original.packet
absolute_coordinates=original.absolute_coordinates

def attach_cursor_snapshot(api,c,hwnd,game):
    from devtools import terminal_scene_owner as base
    C=original.C;W=original.W
    def snapshot(target):
        geometry=api.geometry(target);point=W.POINT()
        base.original.check(base.original.ubind('GetCursorPos',W.BOOL,[C.POINTER(W.POINT)])(C.byref(point)),
                            'current OS cursor position')
        screen=[point.x,point.y]
        if geometry['coordinate_mode']==1:
            base.original.check(base.original.ubind('ScreenToClient',W.BOOL,[W.HWND,C.POINTER(W.POINT)])(hwnd,C.byref(point)),
                                'current OS cursor in original game coordinates')
        return dict(screen_point=screen,os_game_point=[point.x,point.y],game_point=list(api.position()),
                    geometry=geometry,wall_time_ns=time.time_ns(),monotonic_ns=time.monotonic_ns())
    api.cursor_snapshot=snapshot
    return api


def settle(api,target,samples,sleep):
    deadline=time.monotonic()+.30;stable=None;count=0;since=None
    for _ in range(32):
        sample=api.cursor_snapshot(target);samples.append(sample)
        if time.monotonic()>deadline:
            raise ValueError('cursor settling exceeded total deadline')
        if sample['geometry']!=samples[0]['geometry']:
            raise ValueError('owned geometry changed during cursor settling')
        if sample['os_game_point']==sample['game_point']:
            key=(sample['geometry'],sample['game_point'])
            if key==stable:count+=1
            else:stable=key;count=1;since=sample['monotonic_ns']
            if count>=3 and sample['monotonic_ns']-since>=50_000_000:
                return tuple(sample['game_point'])
        else:stable=None;count=0;since=None
        if time.monotonic()>=deadline:break
        sleep(.01)
    raise ValueError('OS and original game cursor did not settle within bounded interval')


def guarded_click(api,guard,target,sleep=time.sleep,*,absolute=False):
    """Feedback from actual game coordinates is mandatory before button-down."""
    if target not in TARGETS.values():raise ValueError('only reviewed original main-menu targets')
    receipt=dict(target=list(target),moves=[],down_submitted=False,released=False,error=None,
                 game_memory_written=False,transition_proved=False,guard_observations=[],
                 movement_mode='absolute_virtual_desktop_feedback' if absolute else 'relative_feedback')
    def checked():receipt['guard_observations'].append(guard())
    last_movement=None
    try:
        checked()
        if api.left_button_down():raise ValueError('left button already held; no action')
        for attempt in range(4):
            checked();position=api.position()
            if position==target:break
            if absolute:
                geometry=api.geometry(target)
                if last_movement and (geometry!=last_movement['geometry'] or
                        list(position)!=last_movement['settling'][-1]['game_point']):
                    raise ValueError('settled cursor or geometry changed before feedback')
                dx,dy=absolute_coordinates(geometry['screen_target'],geometry['virtual_desktop'])
                entry=dict(before=list(position),geometry=geometry,flags=0xC001)
                if last_movement and geometry==last_movement['geometry']:
                    error=[target[i]-position[i]for i in range(2)]
                    if max(abs(v)for v in error)<=2:
                        left,top,right,bottom=geometry['window_rect'];sx,sy=geometry['screen_target']
                        if not (left+8<=sx<right-8 and top+8<=sy<bottom-8):
                            raise ValueError('feedback target lacks bounded movement margin')
                        width,height=geometry['virtual_desktop'][2:]
                        correction=[round(error[0]*65536/width),round(error[1]*65536/height)]
                        previous=last_movement['normalized'];dx,dy=[previous[i]+correction[i]for i in range(2)]
                        if not (0<=dx<=65535 and 0<=dy<=65535):raise ValueError('feedback outside normalized desktop')
                        entry['feedback_correction']=dict(error=error,previous_normalized=list(previous),delta=correction)
                entry['normalized']=[dx,dy]
                movement=packet(dx,dy,0xC001)
            else:
                dx=max(-512,min(512,target[0]-position[0]));dy=max(-512,min(512,target[1]-position[1]))
                movement=packet(dx,dy);entry=dict(before=list(position),delta=[dx,dy])
            checked();sent=api.submit(movement)
            receipt['moves'].append(dict(**entry,submitted=sent))
            if sent!=1:raise ValueError('mouse movement submission failed')
            if absolute:
                last_movement=receipt['moves'][-1];last_movement['settling']=[]
                settled=settle(api,target,last_movement['settling'],sleep)
                if last_movement['settling'][-1]['geometry']!=geometry:
                    raise ValueError('owned geometry changed while settling movement')
                if max(abs(target[i]-settled[i])for i in range(2))>2:
                    raise ValueError('settled cursor outside bounded feedback correction')
            else:sleep(.05)
        if absolute:
            receipt['before_click_settling']=[]
            if settle(api,target,receipt['before_click_settling'],sleep)!=target:
                raise ValueError('final stable cursor is not the reviewed target')
        checked();receipt['before_click']=list(api.position())
        if tuple(receipt['before_click'])!=target:raise ValueError('original game cursor did not reach reviewed target')
        if api.left_button_down():raise ValueError('left button changed before click')
        checked()
        if absolute:
            receipt['click_geometry']=api.geometry(target)
            absolute_coordinates(receipt['click_geometry']['screen_target'],receipt['click_geometry']['virtual_desktop'])
            receipt['pre_down_cursor']=api.cursor_snapshot(target)
            current=receipt['pre_down_cursor'];settled=receipt['before_click_settling'][-1]
            if not (current['geometry']==settled['geometry']==receipt['click_geometry']
                    and current['os_game_point']==current['game_point']==list(target)):
                raise ValueError('cursor or geometry changed before button-down')
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
    if explicit_user_override is not True:raise PermissionError('explicit owned mouse authorization required')
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    def click(api,guard,target,sleep=time.sleep,*,absolute=False):
        game=struct.unpack('<I',c.get(0x7A49FC,4))[0]
        return guarded_click(attach_cursor_snapshot(api,c,hwnd,game),guard,target,sleep,absolute=absolute)
    return clone(original.owned_main_menu_click,guarded_click=click)(
        c,hwnd,index,explicit_user_override=explicit_user_override)
