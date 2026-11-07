"""Bounded original-byte menu/school/battle transition contract; no native I/O.

Unicorn executes isolated original hit-test, input-edge and branch blocks in
synthetic memory. These checks establish instruction semantics, not game state,
legal native input authorization, real thread retirement, or battle acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
SOURCE_BYTES = 5980160
BASE = 0x400000
CHECKS = {
    0x411F2F: ('call', 'dword ptr [0x59236c]'),
    0x411F46: ('call', '0x414400'),
    0x411F5C: ('call', 'dword ptr [0x592368]'),
    0x411F6F: ('mov', 'dword ptr [eax + 0x8b4], ecx'),
    0x411F7B: ('mov', 'dword ptr [edx + 0x8b8], eax'),
    0x411F8D: ('mov', 'dword ptr [ecx + 0x8c4], eax'),
    0x412070: ('mov', 'dword ptr [eax + 0x8d8], ecx'),
    0x412094: ('mov', 'dword ptr [edx + 0x8e4], eax'),
    0x414420: ('cmp', 'dword ptr [eax + 0xb250], 1'),
    0x41F4AF: ('cmp', 'dword ptr [ebp - 8], 0x100'),
    0x41F4BF: ('call', '0x41f4e0'),
    0x45EAD3: ('call', '0x41f480'),
    0x45EBC5: ('call', '0x45ecc0'),
    0x45EBE7: ('ret', '4'),
    0x45ED02: ('call', '0x4e1b60'),
    0x45ED07: ('push', '7'),
    0x45ED12: ('call', '0x439e30'),
    0x45ED19: ('call', '0x4e1b60'),
    0x45ED1E: ('mov', 'word ptr [0x7e11a8], 0'),
    0x45ED27: ('push', '0xd'),
    0x45EE65: ('call', '0x45efb0'),
    0x45EFCD: ('mov', 'dword ptr [ebp - 0x10], 0xe4c'),
    0x45F013: ('mov', 'eax, dword ptr [edx + 0x199c]'),
    0x45F019: ('and', 'eax, 1'),
    0x45F060: ('call', '0x422360'),
    0x45F09B: ('call', '0x422360'),
    0x49F52D: ('push', '8'),
    0x49F52F: ('push', '0x5a082c'),
    0x49F539: ('call', '0x4ce210'),
    0x49F53E: ('push', '6'),
    0x49F549: ('call', '0x439e30'),
    0x4D1B0B: ('call', '0x439e30'),
    0x4D75E3: ('call', '0x42add0'),
    0x4D75F1: ('mov', 'ecx, 0xc1b5'),
    0x4D84B4: ('call', '0x4d75a0'),
    0x4D9E51: ('push', '9'),
    0x4D9E5C: ('call', '0x439e30'),
    0x4AB8A5: ('call', '0x4a6a10'),
    0x4AB989: ('push', '0xa'),
    0x4AB994: ('call', '0x439e30'),
    0x4B9052: ('call', '0x4da860'),
    0x4B905A: ('call', '0x4b9210'),
    0x4B90AF: ('call', '0x4b9270'),
    0x4B90B9: ('call', '0x4b92c0'),
    0x4B90DA: ('push', '0x10'),
    0x4B90E5: ('call', '0x439e30'),
    0x4B90F9: ('call', '0x422360'),
    0x4B910E: ('ret', '4'),
}
# All ranges are half open. Code and table ranges are identified separately.
RANGES = {
    'mouse_producer': (0x411DF0, 0x41209A),
    'window_mode': (0x414400, 0x414439),
    'all_pool_groups_cleanup': (0x41F480, 0x41F4D9),
    'menu_destructor': (0x45EA50, 0x45EB30),
    'menu_callback': (0x45EB90, 0x45EBEA),
    'menu_dispatch': (0x45ECC0, 0x45ED9C),
    'menu_selection_lifecycle': (0x45EDF0, 0x45EF46),
    'menu_selector': (0x45EFB0, 0x45F0CB),
    'menu_hit_test': (0x45F810, 0x45F8F2),
    'main_event_dispatch': (0x49E2B0, 0x49E4D3),
    'new_game_callback': (0x49F4E0, 0x49F561),
    'adv_callback': (0x4D1A80, 0x4D1B37),
    'load_mouse_hit': (0x4D5EC0, 0x4D5FA0),
    'load_file_copy': (0x4D75A0, 0x4D76A0),
    'load_ui': (0x4D7E80, 0x4D8600),
    'load_callback': (0x4D9D50, 0x4D9EFA),
    'school_confirmation': (0x4A7C40, 0x4A7D30),
    'school_group_callback': (0x4AB7A0, 0x4ABA2F),
    'battle_producer': (0x4B8FF0, 0x4B9111),
}
TABLES = {'menu_rectangles': (0x60CEB0, 0x60CEE0),
          'menu_dispatch_table': (0x45ED9C, 0x45EDB8),
          'main_event_table': (0x49E4D3, 0x49E517)}
RECTANGLES = [(215, 492, 207, 32), (215, 524, 207, 33),
              (215, 557, 207, 30), (422, 492, 103, 32),
              (422, 524, 103, 33), (0, 0, 207, 32)]
DISPATCH = [0x45ED02, 0x45ED19, 0x45ED39, 0x45ED55,
            0x45ED67, 0x45ED89, 0x45ED79]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate(raw):
    need(len(raw) == SOURCE_BYTES, 'original mapped image size')
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'original mapped image SHA')
    return raw


def read_source():
    return authenticate((ROOT / 'analysis/hermit_game.exe').read_bytes())


def _u32(value):
    return struct.pack('<I', value & 0xFFFFFFFF)


def _guest(raw):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
    from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EBP
    authenticate(raw)
    u = Uc(UC_ARCH_X86, UC_MODE_32)
    u.mem_map(BASE, 0x800000)
    u.mem_write(BASE, raw)
    u.mem_map(0x31000000, 0x10000)
    u.mem_map(0x32000000, 0x10000)
    u.reg_write(UC_X86_REG_ESP, 0x31008000)
    u.reg_write(UC_X86_REG_EBP, 0x31009000)
    u.mem_write(0x7A49FC, _u32(0x32000000))
    return u


def _run(u, start, stops, budget=1000):
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_EIP
    count = 0
    def step(guest, address, size, _):
        nonlocal count
        count += 1
        if address in stops:
            guest.emu_stop()
    hook = u.hook_add(UC_HOOK_CODE, step)
    try:
        u.emu_start(start, 0, count=budget)
    finally:
        u.hook_del(hook)
    pc = u.reg_read(UC_X86_REG_EIP)
    need(pc in stops, 'bounded original block did not reach required boundary')
    return {'stop': hex(pc), 'instructions': count}


def original_hit_test(raw, x, y):
    from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ESP
    need(all(type(v) is int and -2**31 <= v < 2**31 for v in (x, y)), 'signed mouse coordinates')
    u = _guest(raw)
    u.mem_write(0x3200196C, struct.pack('<ii', x, y))
    u.mem_write(0x31008000, _u32(0x30000000))
    result = _run(u, 0x45F810, {0x45F8F1})  # Before RET: inspect original stack.
    need(u.reg_read(UC_X86_REG_ESP) == 0x31008000, 'hit-test original return stack')
    need(bytes(u.mem_read(0x31008000, 4)) == _u32(0x30000000), 'hit-test return sentinel')
    result['selection'] = struct.unpack('<i', _u32(u.reg_read(UC_X86_REG_EAX)))[0]
    return result


def original_selection_gate(raw, selection, released, held=0):
    from unicorn.x86_const import UC_X86_REG_EAX
    need(type(selection) is int and -1 <= selection <= 6, 'selection bound')
    need(all(type(v) is int and 0 <= v <= 7 for v in (released, held)), 'mouse masks')
    u = _guest(raw)
    u.reg_write(UC_X86_REG_EAX, selection & 0xFFFFFFFF)
    u.mem_write(0x3200199C, _u32(released))
    u.mem_write(0x3200198C, _u32(held))
    result = _run(u, 0x45F004, {0x45F020, 0x45F02C})
    result['accepted'] = result['stop'] == '0x45f020'
    return result


def original_input_edges(raw, previous, current):
    need(all(type(v) is int and 0 <= v <= 7 for v in (previous, current)), 'mouse masks')
    u = _guest(raw)
    owner = 0x320010B8
    u.mem_write(0x31008FFC, _u32(owner))
    u.mem_write(owner + 0x8D4, _u32(previous))
    u.mem_write(owner + 0x118, bytes(0x80 if current & (1 << i) else 0 for i in range(3)))
    result = _run(u, 0x411FB7, {0x41209A})
    result.update(held=int.from_bytes(u.mem_read(0x3200198C, 4), 'little'),
                  pressed=int.from_bytes(u.mem_read(0x32001990, 4), 'little'),
                  released=int.from_bytes(u.mem_read(0x3200199C, 4), 'little'))
    return result


def original_dispatch(raw, selection):
    need(type(selection) is int and -1 <= selection <= 7, 'selection bound')
    u = _guest(raw)
    u.mem_write(0x31008FF8, _u32(selection))
    return _run(u, 0x45ECE8, set(DISPATCH))


def contract(raw):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    authenticate(raw)
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = []
    for address, expected in CHECKS.items():
        ins = next(decoder.disasm(raw[address - BASE:address - BASE + 15], address))
        need((ins.mnemonic, ins.op_str) == expected, f'original instruction {address:x}')
        instructions.append(dict(address=hex(address), hex=ins.bytes.hex(),
                                 instruction=f'{ins.mnemonic} {ins.op_str}'))
    rects = list(struct.iter_unpack('<hhhh', raw[0x60CEB0 - BASE:0x60CEE0 - BASE]))
    need(rects == RECTANGLES, 'original menu rectangles')
    need(list(struct.unpack_from('<7I', raw, 0x45ED9C - BASE)) == DISPATCH, 'dispatch table')
    need(raw[0x5A082C-BASE:0x5A082C-BASE+64].split(b'\0', 1)[0] == b'Data\\Adv\\dat\\CH001.ybc', 'new-game chapter string')
    chapter = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT/CH001.YBC'
    save = ROOT / 'CROSS HERMIT/CROSS HERMIT/SAVEDATA/ATWIKI_ALL_CHARACTERS.SAV'
    assets = []
    for path, size, sha in [
        (chapter, 7112, 'e06ba2055ba380de4e819f9036c0816bdd33a4ec85347379fc3e9f5f415385b9'),
        (save, 198356, 'd97cdbcb6e76ad8f285f8733c6a63561e0dab102ad5e3c2457a3750ccf0336e4'),
    ]:
        data = path.read_bytes()
        need(len(data) == size and hashlib.sha256(data).hexdigest() == sha, f'original asset {path.name}')
        assets.append(dict(path=path.relative_to(ROOT).as_posix(), bytes=size, sha256=sha))
    save_data = save.read_bytes()
    save_fields = {name: struct.unpack_from('<h', save_data, address - 0x7A50E8)[0]
                   for name, address in [('difficulty', 0x7A528C), ('month', 0x7A528E),
                                         ('week', 0x7A5290), ('schedule_cursor', 0x7A5296),
                                         ('schedule_count', 0x7A5298)]}
    ranges = [dict(name=name, start=hex(a), end=hex(b), kind=kind,
                   sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest())
              for mapping, kind in ((RANGES, 'code'), (TABLES, 'table'))
              for name, (a, b) in mapping.items()]
    return dict(
        schema='terminal-menu-transition-static-v1',
        source=dict(path='analysis/hermit_game.exe', bytes=len(raw), sha256=SOURCE_SHA),
        assets=assets, ranges=ranges, instructions=instructions,
        mouse=dict(owner='game+0x10B8', xy='game+0x196C/0x1970',
                   producer='411F2F obtains POINT; mode B250==1 calls 411F5C using HWND[7A0BB4]; 411F6F/7B copy unchanged',
                   api_identity='59236C/592368 are inferred GetCursorPos/ScreenToClient by ABI; live export identity still required',
                   scaling='No scale/clamp in POINT assignment; independent DirectInput xyz stored at game+197C/1980/1984',
                   held='game+198C', press='game+1990=(previous XOR held)&held',
                   release='game+199C=(previous XOR held)&previous',
                   authorization='No OS input is sent or authorized by this static contract'),
        title=dict(rectangles=rects, boundary='strict open rectangle',
                   menu_vtable='0x59B060', callback='0x45EB90', selector='0x45EFB0',
                   ready=dict(wait_return='0x45F065', selector_return='0x45EE6A',
                              selector_this='BP-4', selector_countdown='BP-0x10',
                              last_hit='BP-0xC', node_stage='dword node+0x30 == 1'),
                   confirmed_wait_return='0x45F0A0; eight post-selection waits; not ready for another input',
                   timeout_iterations=3660, timeout_selection=6,
                   keyboard='No keyboard-confirm branch in 45EFB0; no claim about all engine input mappings',
                   actions=['new_game:event7', 'load:event13', 'quit', 'network:event14 excluded',
                            'options:event3', 'no_dispatch', 'timeout:event0']),
        new_game=dict(chain=['menu0', '4E1B60', 'event7/49F570', '49F4E0',
                             '4CE210(CH001.YBC,next=8)', 'event6/4D1820',
                             '4D1A80 original ADV', 'event8/4A16C0 school workroom'],
                      unresolved='Actual dialogue completion and school preparation are not observed by this contract'),
        load=dict(chain=['menu1', '4E1B60', '7E11A8=0', 'event13/4D9F30',
                         '4D9D50/4D7E80 original load UI', '4D75A0 original file load',
                         '4D9E5C publishes9', '4ABA70 school group + 4B89A0 school UI'],
                  file_copy_bytes=0x306D4, file_copy_target='0x7A50E8',
                  rows='original *.sav enumeration; node+19AAC count; node+14C + index*20C filename; node+2C726 selected signed16',
                  select_rect='row i: (176,190+14*i,660,13); first row center (500,196)',
                  confirm_rect=[320,626,141,31], input_edge='game+1990 press mask1',
                  save_fields=save_fields,
                  consequence='This original save has no scheduled battle; do not synthesize schedule or bypass school'),
        battle_producer=dict(chain=['real school confirmation return8', '4A6A10 prepares rounds',
                                    '4AB994 publishes10', '4B9120 creates vtable5A0C38',
                                    '4B8FF0 compares schedule cursor/count',
                                    '4DA860(map)', '4B9210/4B9270/4B92C0 original roster',
                                    'increment original schedule cursor', '4B90E5 publishes16',
                                    'MAIN event16 creates451080', '451170/451670 actual battle'],
                             map='signed16 [7A5308+cursor*70]',
                             actors='count [7A52F8+cursor*70], ids [7A52D0+cursor*70+2*i]',
                             empty_schedule='cursor==count publishes12, not battle',
                             legal_overlap='Producer publishes16 then yields at4B90F9 before RET4 at4B910E. A brief original producer/battle overlap is legal; do not impose universal empty graph.',
                             unresolved='Original school UI must create eligible map/roster; map4/T0004 is not established'),
        lifetime=dict(menu='45EBE7 RET4 ->421F8A; manager observes real worker exit/unlinks/destructs before next MAIN event dispatch',
                      pool='Menu destructor45EAD3->41F480 frees all256 resource groups. Never host-construct battle over live menu/startup.',
                      evidence_required=['Actual input edge + selector ancestry + target window/coordinates',
                                         'Original callback normal return and worker exit0 with same PID/TEB/TLS/PTD',
                                         'Manager unlink/destructor then successor factory and events; no host game-state writes',
                                         'School original schedule/roster production before event10 and16',
                                         '451670 result, 422360 actual wait return,4539B0 consumption and natural exit still separately required']),
        validation=dict(local_original_blocks=True, native_input_executed=False,
                        native_menu_handoff_proved=False, native_battle_producer_proved=False,
                        wait_return_proved=False, result_consumption_proved=False,
                        full_resource_lifetime_proved=False, full_battle_acceptance=False),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = read_source()
    report = contract(raw)
    report['local_examples'] = dict(
        centers=[original_hit_test(raw, x+w//2, y+h//2) for x,y,w,h in RECTANGLES],
        title_release=original_selection_gate(raw, 0, 1),
        title_held_only=original_selection_gate(raw, 0, 0, 1),
        input_release=original_input_edges(raw, 1, 0),
        dispatch=[original_dispatch(raw, i) for i in range(7)],
    )
    encoded = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    need(len(encoded) < 65536, 'static report budget')
    if args.output:
        with args.output.open('xb') as stream:
            stream.write(encoded)
        print(json.dumps(dict(path=str(args.output), bytes=len(encoded), sha256=hashlib.sha256(encoded).hexdigest())))
    else:
        print(encoded.decode(), end='')


if __name__ == '__main__':
    main()
