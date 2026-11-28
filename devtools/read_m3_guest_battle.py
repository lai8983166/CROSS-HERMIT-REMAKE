"""Read a bounded tactical snapshot from the qualified original-game guest."""
import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
from pathlib import Path
import struct
import sys


def parse_units(work, records, controller):
    units = []
    for slot in range(250):
        w, r = slot*0x520, slot*176
        work_id, = struct.unpack_from('<h', work, w)
        if not work_id:
            continue
        pointer, = struct.unpack_from('<I', work, w+600)
        if pointer != controller+0xD0C2C+r:
            raise ValueError(f'Unverified record for work slot {slot}')
        role, = struct.unpack_from('<H', records, r+2)
        max_hp,hp = struct.unpack_from('<2h', records, r+0x14)
        max_mp,mp = struct.unpack_from('<2h', records, r+0x1A)
        units.append({'slot': slot, 'role': role, 'state': records[r+15],
                      'side':records[r+0xA4], 'work_id':work_id,
                      'action':work[w+0x290], 'hp': hp,'max_hp':max_hp,'mp':mp,'max_mp':max_mp,
                      'cell': list(work[w+1255:w+1257])})
    return units


def command_state(units, work, read):
    """46F170 selected flag and 48DD60's first pending 16-byte unit command."""
    rows = []
    for unit in units:
        if unit["side"] != 0 or not 1 <= unit["role"] <= 45:
            continue
        at = unit["slot"] * 0x520
        head, = struct.unpack_from("<I", work, at + 0x518)
        pending = None
        if head:
            payload, = struct.unpack("<I", read(head + 8, 4))
            pending = read(payload, 16).hex()
        rows.append({"slot":unit["slot"], "role":unit["role"], "selected":work[at+0x28c],
                     "move_phase":work[at+0x293], "goal_pixels":list(struct.unpack_from("<hh",work,at+0x4d0)),
                     "first_pending_command":pending})
    return rows


def observe(pid, scene, game, include_commands=False):
    kernel = ctypes.windll.kernel32
    kernel.OpenProcess.restype = wintypes.HANDLE
    handle = kernel.OpenProcess(0x1010, False, pid)
    if not handle:
        raise ctypes.WinError()
    h = wintypes.HANDLE(handle)

    def read(address, size):
        buf = ctypes.create_string_buffer(size)
        got = ctypes.c_size_t()
        if not kernel.ReadProcessMemory(h, ctypes.c_void_p(address), buf, size, ctypes.byref(got)) or got.value!=size:
            raise ctypes.WinError()
        return buf.raw

    def word(address):
        return struct.unpack('<I', read(address, 4))[0]

    try:
        name = ctypes.create_unicode_buffer(1024)
        capacity = wintypes.DWORD(len(name))
        if not kernel.QueryFullProcessImageNameW(h, 0, name, ctypes.byref(capacity)):
            raise ctypes.WinError()
        if Path(name.value).resolve()!=game.resolve() or hashlib.sha256(game.read_bytes()).hexdigest()!='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7':
            raise ValueError('Original executable identity mismatch')
        task = word(0x7A49F4)
        ctrl = task+0x190
        if not task or word(task)!=0x59A430 or word(ctrl+0x117C38)!=task:
            raise ValueError('Original tactical task is not active')
        if struct.unpack('<h',read(0x7F4488,2))[0]!=scene:
            raise ValueError('Unexpected original tactical scene')
        for _ in range(20):
            clock=read(ctrl+0x2E6F4,12)
            work=read(ctrl+0x80AEC,250*0x520)
            records=read(ctrl+0xD0C2C,250*176)
            if read(ctrl+0x2E6F4,12)!=clock or word(0x7A49F4)!=task:
                continue
            units = parse_units(work,records,ctrl)
            extra = {}
            if include_commands:
                try:
                    extra["command_state"] = command_state(units,work,read)
                except OSError:
                    if read(ctrl+0x2E6F4,12)!=clock:
                        continue
                    raise
            if read(ctrl+0x2E6F4,12)==clock and word(0x7A49F4)==task:
                remaining,elapsed,limit=struct.unpack('<3i',clock)
                return {'scene':scene,'date':list(struct.unpack('<hh',read(0x7A528E,4))),
                        'remaining':remaining,'elapsed':elapsed,'limit':limit,
                        'units':units, **extra}
        raise ValueError('Tactical clock changed during all samples')
    finally:
        kernel.CloseHandle(h)


if __name__=='__main__':
    root=Path('C:/ChaomofaWorker')
    sys.path.insert(0,str(root/'project'))
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pid',type=int)
    parser.add_argument('scene',type=int)
    parser.add_argument('--departure-sha256', help='verify the last original school save exported by this guest')
    parser.add_argument('--commands',action='store_true',help='record selected students, movement goals and pending commands')
    args=parser.parse_args()
    game=root/'project/.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
    output=root/'m3-battle-sample.json'
    if args.departure_sha256:
        digest=hashlib.sha256((root/'m3-export.sav').read_bytes()).hexdigest()
        if digest!=args.departure_sha256:
            raise ValueError('Guest school checkpoint differs from the requested departure')
    sample=observe(args.pid,args.scene,game,args.commands)
    if args.departure_sha256:
        sample['exported_school_sha256']=digest
    output.write_text(json.dumps(sample,separators=(',',':')),encoding='utf8')
