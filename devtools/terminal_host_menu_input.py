"""Host-only explicitly authorized menu input with release-time checks.

Does not call or weaken the guest-qualified entry. Reuses its pure coordinate
feedback algorithm; all native input remains inside the original owned guard.
"""
import struct
import time
from devtools import terminal_menu_input as original
from devtools import terminal_owned_mouse as feedback
from devtools.terminal_scene_resources import clone


def guarded_click(api, guard, target, sleep=time.sleep, *, absolute=True, expected_owner=None):
    if absolute is not True:
        raise ValueError('absolute owned coordinate feedback required')
    checks = []
    generation = None
    geometry = None
    release_failed = False
    release_failure = None
    previous_countdown = None
    deadline = time.monotonic() + 3

    def within_deadline():
        if time.monotonic() >= deadline:
            raise TimeoutError('bounded host input exceeded three seconds')

    def checked():
        nonlocal generation, previous_countdown
        within_deadline()
        row = guard()
        within_deadline()
        countdown = struct.unpack_from('<I', bytes.fromhex(row['selector_hex']))[0]
        if not 300 <= countdown < 3660:
            raise ValueError('insufficient original selector iterations before timeout')
        if previous_countdown is not None and countdown > previous_countdown:
            raise ValueError('selector countdown restarted')
        previous_countdown = countdown
        head = bytes.fromhex(row['head_hex'])
        owner = (row['node'], struct.unpack_from('<I',head,0x24)[0],
                 *struct.unpack_from('<II',head,0x1C), row['selector_pointer'])
        if expected_owner is not None and owner != expected_owner:
            raise ValueError('live input owner differs from readiness samples')
        key = (row['pid'], row['hwnd'], row['game'], row['main'], row['node'],
               row['selector_pointer'], *struct.unpack_from('<III', head, 0x1C),
               row['coordinate_mode_hex'])
        if generation is not None and key != generation:
            raise ValueError('owned selector generation or coordinate mode changed')
        generation = key
        return row

    class Proxy:
        def __getattr__(self, name):
            return getattr(api, name)

        def submit(self, packet):
            nonlocal geometry, release_failed, release_failure
            flags = packet.data.mi.dwFlags
            # Always submit UP even when its guard fails, including when this
            # call already comes from finally. Record failure, never success.
            if flags in (2, 4) and not (flags == 4 and release_failed):
                try:
                    row = checked()
                    cursor = api.cursor_snapshot(target)
                    if cursor['os_game_point'] != list(target) or cursor['game_point'] != list(target):
                        raise ValueError('OS/game cursor changed before button edge')
                    if geometry is not None and geometry != cursor['geometry']:
                        raise ValueError('window geometry changed during button hold')
                    geometry = cursor['geometry']
                    if api.left_button_down() != (flags == 4):
                        raise ValueError('unexpected physical left button state')
                    within_deadline()
                    checks.append(dict(flags=flags, guard=row, cursor=cursor))
                except Exception as exc:
                    if flags == 4:
                        release_failed = True
                        release_failure = repr(exc)
                    else:
                        raise
            if flags != 4:
                within_deadline()
            return api.submit(packet)

    result = feedback.guarded_click(Proxy(), checked, target, sleep, absolute=True)
    result.update(button_edge_checks=checks, release_guard_failed=release_failed,
                  release_guard_error=release_failure, screenshot_required=False, accepted=False)
    if release_failed and result['error'] is None:
        result['error'] = release_failure
    return result


def owned_main_menu_click(c, hwnd, index, *, explicit_user_override=False, expected_owner=None):
    if explicit_user_override is not True:
        raise PermissionError('current host window and mouse authorization required')
    if index != 0 or type(index) is not int:
        raise ValueError('this host preflight permits new game only')
    if expected_owner is None:
        raise ValueError('current readiness owner required')
    def click(api, guard, target, sleep=time.sleep, *, absolute=False):
        game = struct.unpack('<I', c.get(0x7A49FC, 4))[0]
        return guarded_click(feedback.attach_cursor_snapshot(api, c, hwnd, game),
                             guard, target, sleep, absolute=absolute, expected_owner=expected_owner)
    return clone(original.owned_main_menu_click, guarded_click=click)(
        c, hwnd, index, explicit_user_override=True)
