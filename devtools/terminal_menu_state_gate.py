"""Pure scheduling gate for one native menu click, independent of screenshots.

Recorded rows can test scheduling only. Production still rechecks live Job,
window, original code/selector and actual cursor in the guarded input backend.
"""
import math
import struct

MENU = 0x59B060
ADV = 0x5C306C


def word(raw, offset=0):
    return struct.unpack_from('<I', raw, offset)[0]


def ready_owner(row):
    tasks = row['tasks']
    if len(tasks) != 1 or tasks[0]['vtable'] != MENU:
        return None
    task = tasks[0]
    head = bytes.fromhex(task['header_hex'])
    tid = task['thread_id']
    if (word(head) != MENU or word(head, 0x24) != tid or not tid
            or not word(head, 0x1C) or not word(head, 0x20)
            or word(head, 0x30) != 1
            or word(bytes.fromhex(row['MAIN_event_hex'])) != 0):
        return None
    frames = [f for f in row['frames'] if f['tid'] == tid]
    if len(frames) != 1 or sum(f['return_va'] == 0x45F065
                              for f in frames[0]['chain']) != 1:
        return None
    wait = next(f for f in frames[0]['chain'] if f['return_va'] == 0x45F065)
    return (task['pointer'], tid, word(head, 0x1C), word(head, 0x20), wait['saved_bp'])


class MenuGate:
    """Fail closed on timeout or owner replacement; never retry a click."""
    def __init__(self):
        self.first = self.since = self.previous = self.owner = None
        self.attempted = False

    def observe(self, row, now):
        if not math.isfinite(now) or (self.previous is not None and now < self.previous):
            raise ValueError('invalid monotonic menu clock')
        if self.attempted:
            return False
        gap = None if self.previous is None else now-self.previous
        self.previous = now
        has_menu = any(t['vtable'] == MENU for t in row['tasks'])
        if self.first is None:
            if not has_menu:
                return False
            self.first = now
        if now-self.first >= 15:
            raise TimeoutError('native menu readiness exceeded 15 seconds; no retry')
        if not has_menu:
            raise ValueError('menu retired before input; do not wait for another cycle')
        owner = ready_owner(row)
        if self.owner is not None and owner is not None and owner != self.owner:
            raise ValueError('menu worker/event generation changed before input')
        if owner is None or (gap is not None and gap > 2.5):
            self.since = None
        if owner is None:
            return False
        self.owner = owner
        if self.since is None:
            self.since = now
        return now-self.since >= 1

    def claim(self):
        if self.attempted:
            raise ValueError('one input attempt only')
        self.attempted = True
