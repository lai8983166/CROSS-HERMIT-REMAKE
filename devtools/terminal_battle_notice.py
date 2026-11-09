"""One original opening-notice confirmation in a qualified native guest.

The ADV VM has stopped, but controller phase9 still awaits 499910's mode0
notification. No field is written and no native game function is called here.
"""
import struct
import time

from devtools import terminal_battle_input as battle
from devtools import terminal_owned_mouse as mouse
from devtools import terminal_scene_owner as base
from devtools.terminal_scene_resources import clone

TARGETS = {'opening_notice': (512, 336)}
NOTICE_RANGES = (
    (0x4549D0, 0x454AB0), (0x454C80, 0x454EE0),
    (0x467850, 0x467AA0), (0x4998B0, 0x499C90),
    (0x499DA0, 0x49A310), (0x49AD50, 0x49AD8C),
    (0x4DB2B0, 0x4DB2F4), (0x415040, 0x415099),
    (0x497C50, 0x497C90), (0x59EAA4, 0x59EAC0),
)
INPUT_RANGES = battle.INPUT_RANGES + NOTICE_RANGES
ANCESTORS = {0x453CB5, 0x451ABC, 0x451716, 0x421F8A, 0x56E183}


def capture(c, pointer):
    result = battle.capture(c, pointer)
    game = base.word(c.get(0x7A49FC, 4))
    for name, address, size in (
        ('notice', pointer + 0x190 + 0x30998, 0x14),
        ('notice_flags', 0x7F44B9, 2),
        ('keyboard_action', game + 0x1950, 4),
        ('mouse_pressed', game + 0x1990, 4),
        ('VM', base.native.VM, 128),
    ):
        result[name + '_pointer'] = address
        result[name + '_hex'] = c.get(address, size).hex()
    result['game_pointer'] = game
    return result


def ready(row, stage):
    """Strict pre-down predicate; it is never reused after notification advance."""
    if stage not in TARGETS:
        return False
    try:
        tasks = row['tasks']
        if len(tasks) != 1 or tasks[0]['vtable'] != battle.BATTLE:
            return False
        task = tasks[0]
        node = task['pointer']
        head = bytes.fromhex(task['scene_head_hex'])
        gates = task['battle_gates']
        activity = bytes.fromhex(gates['controller_activity_hex'])
        notice = bytes.fromhex(gates['notice_hex'])
        flags = bytes.fromhex(gates['notice_flags_hex'])
        vm = bytes.fromhex(gates['VM_hex'])
        key = bytes.fromhex(gates['keyboard_action_hex'])
        pressed = bytes.fromhex(gates['mouse_pressed_hex'])
        if (len(head), len(activity), len(notice), len(flags), len(vm), len(key), len(pressed)) != (512,32,20,2,128,4,4):
            return False
        game = gates['game_pointer']
        if not (0x10000 <= game < 0x7FFF0000 and game % 4 == 0):
            return False
        if not (row['scene_global'] == node and base.word(bytes.fromhex(row['MAIN_event_hex'])) == 0
                and gates['pointer'] == node and gates['network_hex'] == '00' and gates['panel_hex'] == '00'
                and gates['controller_pointer'] == node + 0x190
                and gates['panel_pointer'] == node + 0x117F20
                and base.word(bytes.fromhex(gates['backpointer_hex'])) == node
                and gates['notice_pointer'] == node + 0x190 + 0x30998
                and gates['notice_flags_pointer'] == 0x7F44B9
                and gates['VM_pointer'] == base.native.VM
                and gates['keyboard_action_pointer'] == game + 0x1950
                and gates['mouse_pressed_pointer'] == game + 0x1990):
            return False
        if not (head[0x30] == head[0x31] == 0 and base.word(head, 0x34) == 2
                and base.word(head, 0x38) == 5 and head[0x43] == 1
                and head[0x44] == 3 and head[0x58] == 0 and head[0x59] == 2
                and struct.unpack_from('<h', activity)[0] != 0
                and activity[8] == 0 and activity[0x16] == 1 and activity[0x18] == 9
                and notice[:3] == b'\x01\x02\x00'
                and base.word(notice, 8) == 0xFF00 and base.word(notice, 12) == 0x800
                and flags[0] != 0 and vm[4] == 0
                and base.word(key) & 0x8000 == 0 and base.word(pressed) == 0):
            return False
        tls = task['TLS']
        if not (tls['thread_id'] == task['thread_id']
                and tls['ancestry']['worker_argument'] == tls['ancestry']['callback_this'] == node):
            return False
        frame = next((f for f in row['frames'] if f['tid'] == task['thread_id']), None)
        return bool(frame and ANCESTORS <= {f['return_va'] for f in frame['chain']})
    except (KeyError, TypeError, ValueError, IndexError, struct.error):
        return False


def guarded_click(api, guard, stage, sleep=time.sleep):
    base.need(stage in TARGETS, 'only reviewed original opening notice')
    # The existing mouse backend runs guard only before down. After release its
    # final guard checks ownership, allowing the original state machine to move.
    return clone(mouse.guarded_click, TARGETS=TARGETS)(
        api, guard, TARGETS[stage], sleep, absolute=True)


def action(c, hwnd, stage, *, explicit_user_override=False):
    return clone(battle.action, ready=ready, capture=capture,
                 INPUT_RANGES=INPUT_RANGES, TARGETS=TARGETS, guarded_click=guarded_click)(
                     c, hwnd, stage, explicit_user_override=explicit_user_override)


CHECKS = {
    0x46B4B5: ('movsx', 'eax, byte ptr [edx + 0x108b48]'),
    0x46B4C3: ('call', '0x499da0'),
    0x499DFC: ('jmp', 'dword ptr [ecx*4 + 0x49a2cf]'),
    0x49A1B3: ('call', '0x499910'),
    0x49A1BA: ('je', '0x49a1d8'),
    0x49A1C5: ('call', '0x454c80'),
    0x454CD8: ('mov', 'byte ptr [ecx + 0x14], 1'),
    0x454DD5: ('movsx', 'ecx, byte ptr [eax + 0x14]'),
    0x454DDB: ('je', '0x454e13'),
    0x454E89: ('mov', 'byte ptr [edx + 0x43], 0'),
    0x49A285: ('mov', 'byte ptr [eax + 0x108b3a], 1'),
    0x499A56: ('mov', 'edx, dword ptr [ecx + 0x1990]'),
    0x499A5C: ('and', 'edx, 1'),
    0x499A61: ('jne', '0x499a78'),
    0x499A68: ('mov', 'ecx, dword ptr [eax + 0x1950]'),
    0x499A6E: ('and', 'ecx, 0x8000'),
    0x499A76: ('je', '0x499ab9'),
    0x499A9C: ('mov', 'byte ptr [ecx + 1], 4'),
    0x499B38: ('mov', 'byte ptr [edx], 0'),
    0x499B3B: ('mov', 'dword ptr [ebp - 0x10], 1'),
}


def source_contract(raw):
    """Authenticate original code and tables; this is not native acceptance."""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    base.need(len(raw) == 5980160 and base.sha(raw) == base.SOURCE_SHA, 'fixed original source identity')
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    for address, expected in CHECKS.items():
        instruction = next(decoder.disasm(raw[address-0x400000:address-0x400000+15], address))
        base.need((instruction.mnemonic, instruction.op_str) == expected, 'original notice instruction ' + hex(address))
    def table(address, count):
        return struct.unpack_from('<%dI' % count, raw, address-0x400000)
    base.need(table(0x499B5D, 6) == (0x49999D,0x4999CF,0x499A50,0x499ABE,0x499AFD,0x499B35), 'notice state table')
    base.need(table(0x49A2CF, 14)[7:] == (0x49A159,0x49A180,0x49A1B0,0x49A1DD,0x49A203,0x49A233,0x49A250), 'controller notice states')
    base.need(table(0x454EC2, 6) == (0x454D51,0x454D6C,0x454D7D,0x454DD2,0x454E18,0x454E38), 'scene script states')
    base.need(struct.unpack_from('<14h', raw, 0x59EAA4-0x400000) ==
              (0,0x800,120,0x800,512,336,1,0,0x800,16,0x800,512,304,0), 'original notice modes')
    return dict(source_sha256=base.SOURCE_SHA, accepted=False, native_execution=False,
                ranges=[dict(pointer=a,bytes=b-a,sha256=base.sha(raw[a-0x400000:b-0x400000])) for a,b in INPUT_RANGES])


def branch_probe(raw, *, mouse_pressed=0, keyboard_action=0):
    """Bounded synthetic x86 input gate; never substitutes live input fields."""
    source_contract(raw)
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP
    u = Uc(UC_ARCH_X86, UC_MODE_32)
    u.mem_map(0x490000, 0x10000)
    u.mem_write(0x490000, raw[0x90000:0xA0000])
    u.mem_map(0x7A4000, 0x1000)
    game = 0x20000000
    u.mem_map(game, 0x2000)
    u.mem_write(0x7A49FC, struct.pack('<I', game))
    u.mem_write(game+0x1990, struct.pack('<I', mouse_pressed))
    u.mem_write(game+0x1950, struct.pack('<I', keyboard_action))
    u.reg_write(UC_X86_REG_EBP, 0x30000000)
    trace = []
    def stop(uc, at, size, data):
        trace.append(at)
        if at in (0x499A78, 0x499AB9):
            uc.emu_stop()
    u.hook_add(UC_HOOK_CODE, stop)
    u.emu_start(0x499A50, 0, count=32)
    reached = u.reg_read(UC_X86_REG_EIP)
    base.need(reached in (0x499A78, 0x499AB9), 'bounded original notice branch reached')
    return dict(accepted=False, native_execution=False, synthetic_input=True,
                mouse_pressed=mouse_pressed, keyboard_action=keyboard_action,
                trace=trace, reached=reached, opens_gate=reached == 0x499A78)
