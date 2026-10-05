"""Execute original student waiting-sort commands with explicitly declared inputs.

This isolated replay does not run school boot, mouse hit testing or teacher work.
"""
import argparse
from collections import Counter
import hashlib
import json

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE, SOURCE_SHA256, STACK, report_text

INPUT_PATH = ROOT / 'prototype/data/campaign_scene5_evidence.json'
INPUT_SHA = 'b349bb3d0bfcd51407595f8cec02e37fd744684332e31f08d3279d9f615f79f0'
FUNCTIONS = ((0x4A3CA0, 0x4A45AB), (0x4A8BF0, 0x4A95F0))
STUBS = {
    0x4A8BC0: ('selected_group_input', 0),
    0x4AA4B0: ('menu_command_input', 0),
    0x4AA590: ('button_feedback_boundary', 4),
    0x4DB2B0: ('sound_boundary', 0),
    0x56CE80: ('debug_stack_check', 0),
}
CHAR_BASE, CATEGORY_BASE = 0x7E17E8, 0x6B2D8A
COUNT, IDS, MODE = 0x7D57DE, 0x7D57E2, 0x7D57DA


def category_rules():
    source = SOURCE.read_bytes()
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise ValueError('source image differs')
    return {'source_image_sha256': SOURCE_SHA256,
            'job_categories': [source[CATEGORY_BASE-0x400000+j*0x40] for j in range(31)]}


class WaitlistEmulator(ExitEmulator):
    def __init__(self, profiles, waiting_ids, mode=0):
        super().__init__()
        self._function_ranges = FUNCTIONS
        self._stubs = STUBS.copy()
        self.command = 0x37
        self.stub_events = []
        self.writes = []
        self.profiles = profiles
        if len(waiting_ids) > 20 or len(set(waiting_ids)) != len(waiting_ids):
            raise ValueError('waiting list outside declared domain')
        records = {p['character_id']: p for p in profiles}
        if any(i not in records for i in waiting_ids):
            raise ValueError('missing waiting profile')
        self.write(COUNT, len(waiting_ids), 'h')
        self.write(MODE, mode, 'B')
        for i in range(20):
            self.write(IDS+2*i, waiting_ids[i] if i < len(waiting_ids) else -1, 'h')
        for p in profiles:
            a = CHAR_BASE+p['character_id']*0x4A0
            self.write(a+6, p['job'], 'h')
            self.write(a+0x50, p['level_50'], 'B')
            for i, value in enumerate(p['attributes']):
                self.write(a+0xC+i*8, value, 'B')
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._write_hook)

    def _write_hook(self, uc, access, address, size, value, _):
        if STACK <= address and address+size <= STACK+0x10000:
            return
        if not ((address == MODE and size == 1) or
                (IDS <= address and address+size <= IDS+2*self.read(COUNT, 'h') and size == 2)):
            raise RuntimeError(f'undeclared native write at {address:#x}, size {size}')
        self.writes.append({'address': hex(address), 'size': size, 'value': value & ((1 << (8*size))-1)})

    def _hook(self, uc, address, size, context):
        if address not in (0x4A8BC0, 0x4AA4B0, 0x4AA590, 0x4DB2B0):
            return super()._hook(uc, address, size, context)
        name, pop = self._stubs[address]
        self.stub_calls[name] += 1
        sp = uc.reg_read(UC_X86_REG_ESP)
        event = {'boundary': name}
        if address in (0x4AA590, 0x4DB2B0):
            event['argument_low16'] = self.read(sp+4) & 65535
        self.stub_events.append(event)
        result = 0xFFFFFFFF if address == 0x4A8BC0 else (self.command if address == 0x4AA4B0 else 0)
        uc.reg_write(UC_X86_REG_EAX, result)
        uc.reg_write(UC_X86_REG_ESP, sp+4+pop)
        uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def waiting_snapshot(self):
        return {'idle_student_ids': [self.read(IDS+2*i, 'h') for i in range(self.read(COUNT, 'h'))],
                'idle_sort_mode': self.read(MODE, 'B'), 'idle_student_count': self.read(COUNT, 'h'),
                'buffer_tail': [self.read(IDS+2*i, 'h') for i in range(self.read(COUNT, 'h'), 20)]}

    def run_command(self, command):
        if command not in (0xB, 0xC, 0xD, 0x37):
            raise ValueError('command outside waiting-sort audit')
        before = self.waiting_snapshot()
        self.command = command
        self.visited.clear()
        self.stub_calls = Counter()
        self.stub_events.clear()
        self.writes.clear()
        self.call(0x4A3CA0)
        return {'command': command, 'before': before, 'after': self.waiting_snapshot(),
                'stub_calls': dict(self.stub_calls), 'stub_events': self.stub_events.copy(),
                'native_writes': self.writes.copy(),
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)]}


def profile_subset(snapshot):
    return [{key: p[key] for key in ('character_id', 'job', 'level_50', 'attributes')}
            for p in snapshot['characters'] if p['character_id'] in snapshot['school']['school_control']['idle_student_ids']]


def replay(name, profiles, waiting_ids, commands, mode=0):
    emulator = WaitlistEmulator(profiles, waiting_ids, mode)
    return {'name': name, 'declared_profiles': profiles,
            'declared_initial': emulator.waiting_snapshot(),
            'steps': [emulator.run_command(c) for c in commands]}


def report():
    source = INPUT_PATH.read_bytes()
    if hashlib.sha256(source).hexdigest() != INPUT_SHA:
        raise ValueError('declared input catalog differs')
    inputs = json.loads(source)
    cases = []
    for index in range(2):
        s = inputs['cases'][index]['expected_after']
        cases.append(replay(f'route_{index}', profile_subset(s),
                           s['school']['school_control']['idle_student_ids'], [12, 11, 13, 13, 55]))
    ids = [3, 4, 9, 5]
    profiles = [{'character_id': i, 'job': j, 'level_50': level, 'attributes': [v]*7}
                for i, j, level, v in zip(ids, [2, 1, 4, 3], [10, 10, 20, 5], [10, 10, 20, 5])]
    cases.append(replay('exchange_ties', profiles, ids, [11, 13, 12, 12, 55]))
    divergent = [dict(p, level_50=level, attributes=[v]*7)
                 for p, level, v in zip(profiles, [0, 255, 10, 20], [255, 0, 20, 10])]
    cases.append(replay('divergent_keys', divergent, ids, [11, 13, 12]))
    cases.append(replay('empty', [], [], [11, 12, 13, 55]))
    cases.append(replay('single', profiles[:1], ids[:1], [12, 13, 11]))
    return {'schema_version': 1, 'evidence_kind': 'isolated_original_waiting_sort_commands',
            'source_image_sha256': SOURCE_SHA256, 'declared_input_catalog_sha256': INPUT_SHA,
            'function_ranges': [[hex(a), hex(b)] for a, b in FUNCTIONS],
            'stub_manifest': [{'va': hex(a), 'meaning': name, 'callee_pop_bytes': pop}
                              for a, (name, pop) in STUBS.items()],
            'read_fields': {'count': hex(COUNT), 'ids': hex(IDS), 'mode': hex(MODE),
                            'character_base': hex(CHAR_BASE), 'character_stride': 0x4A0,
                            'job_offset': 6, 'level_offset': 0x50,
                            'attribute_offsets': [0xC+8*i for i in range(7)],
                            'job_category_base': hex(CATEGORY_BASE), 'job_stride': 0x40},
            'rules': category_rules(), 'cases': cases,
            'limitations': ['Starting catalogs are declared frozen replay inputs, not native boot continuity.',
                            'Only job, level, seven attributes and waiting control inputs are seeded.',
                            'Selected-group and menu hit tests return declared values; audio/feedback are stubs.',
                            'Only the original command/sort bodies execute; no full menu loop or teacher work.',
                            'Native non-stack writes are restricted to active waiting IDs and mode byte.',
                            'No live game witness, complete school interaction or save-write authorization.'],
            'school_initialized': False, 'interactive_school_ready': False,
            'live_witness': False, 'authorizes_persistent_write': False}


def fixture(native):
    return {key: native[key] for key in ('schema_version', 'evidence_kind', 'source_image_sha256',
            'declared_input_catalog_sha256', 'rules', 'cases', 'limitations', 'school_initialized',
            'interactive_school_ready', 'live_witness', 'authorizes_persistent_write')} | {
            'native_report_sha256': hashlib.sha256(report_text(native).encode('utf-8')).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--godot-out', required=True)
    args = parser.parse_args()
    paths = [ROOT / args.out, ROOT / args.godot_out]
    if paths[0].resolve() == paths[1].resolve() or any(p.exists() for p in paths):
        parser.error('report and fixture must be different new files')
    native = report()
    for path, data in zip(paths, [native, fixture(native)]):
        payload = report_text(data)
        with path.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
