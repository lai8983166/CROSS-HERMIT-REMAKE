"""Capture both role and school layouts from one native CPU's data buffers.

The ordinary result continues through a DIRECT Chapter020 opcode144 prefix and
a DIRECT whole-week probe. CH003/Chapter021 completion, request7 and subsequent
school tasks are NOT asserted. This is layout/data continuity evidence only.
"""
import argparse
from copy import deepcopy
import hashlib

from tools.result_transaction_emulation import ResultTransactionEmulator
from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.roster_join_emulation import CHAPTER, JOIN_NATIVE, RosterJoinEmulator
from tools.scene5_script_emulation import VM, SCRIPT
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

IDS = (3, 4, 9, 5)


class CampaignSchoolLayoutEmulator(ResultTransactionEmulator):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self._ran_layout = False
        # A declared candidate record prepared BEFORE battle/result execution.
        # It is unavailable and not in any result group; no existing role resets.
        self.uc.mem_write(CHAR_BASE+5*CHAR_STRIDE,
                         bytes(self.uc.mem_read(0x6F5088+5*CHAR_STRIDE, CHAR_STRIDE)))
        self.uc.mem_write(PACKAGE_BASE+5*PACKAGE_STRIDE, bytes(PACKAGE_STRIDE))
        for index in range(31):
            self.write(PACKAGE_BASE+5*PACKAGE_STRIDE+0xD7+index, index-15, 'b')
        self.uc.mem_write(PACKAGE_BASE+5*PACKAGE_STRIDE+0xF9, bytes([1])*32)
        for index in range(8):
            self.write(CHAR_BASE+5*CHAR_STRIDE+0x52+index*2, [1, 2, 1][index] if index < 3 else 0, 'h')
            self.write(CHAR_BASE+5*CHAR_STRIDE+0x62+index*2, [6, 7, 6][index] if index < 3 else 0, 'h')
        for index in range(2):
            self.write(CHAR_BASE+5*CHAR_STRIDE+0xB8+index*12, 0, 'B')
        self.write(CHAR_BASE+5*CHAR_STRIDE+0x50, 47, 'B')
        self.write(0x7AACAA+6*2, 0x100, 'H')
        self.write(0x7AACAA+7*2, 0x101, 'H')
        self.write(0x7A528A, 0, 'h')
        for index in range(20):
            self.write(0x7A5262+index*2, -1, 'h')

    def profile(self, identity, *, result_fields):
        char, package = CHAR_BASE+identity*CHAR_STRIDE, PACKAGE_BASE+identity*PACKAGE_STRIDE
        row = {'character_id': identity, 'job': self.read(char+6, 'h'),
            'attributes': [self.read(char+0xC+i*8, 'B') for i in range(7)],
            'growth_pools': [self.read(char+0x10+i*8) for i in range(7)],
            'level_50': self.read(char+0x50, 'B'),
            'job_progress': [self.read(package+0xD7+i, 'b') for i in range(31)],
            'unlock_flags': [self.read(package+0xF9+i, 'B') for i in range(30)],
            'unlock_reserved_bytes': [self.read(package+0x117+i, 'B') for i in range(2)],
            'skill_statuses': [self.read(char+0xB8+i*12, 'B') for i in range(84)],
            'equipped_skills': [self.read(char+0x52+i*2, 'h') for i in range(8)],
            'equipped_items': [self.read(char+0x62+i*2, 'h') for i in range(8)]}
        if result_fields:
            row.update(staged_package=[self.read(package+i*4, 'i') for i in range(8)],
                staged_total=self.read(package+0x20, 'i'), recipient_count=self.read(package+0x120, 'h'),
                week_records=list(bytes(self.uc.mem_read(package+0x24, 177))))
        return row

    def school_metadata(self):
        return {'student_count': self.read(0x7A5260, 'h'),
            'student_ids': [self.read(0x7A5210+i*2, 'h') for i in range(20)],
            'teacher_count': self.read(0x7A528A, 'h'),
            'teacher_ids': [self.read(0x7A5262+i*2, 'h') for i in range(20)],
            'group_student_ids': [[self.read(0x7AAA22+g*28+i*2, 'h') for i in range(4)] for g in range(5)],
            'group_student_indices': [[self.read(0x7AAAE0+g*8+i*2, 'h') for i in range(4)] for g in range(5)],
            # 7E1180 is the result recipient alias, projected from the canonical field.
            'adv_globals': {hex(a): self.read(a, 'h') for a in (0x7A5292, 0x7E1182)}}

    def canonical_snapshot(self):
        return {'month': self.read(0x7A528E, 'h'), 'week': self.read(0x7A5290, 'h'),
            'global_total_511c': self.read(0x7A511C, 'i'), 'recipient_id': self.read(0x7E1180, 'h'),
            'flags': {hex(a): self.read(a, 'h') for a in (0x7A55FA, 0x7A4E62, 0x7A55F6, 0x7E11A0)},
            'characters': [self.profile(c, result_fields=True) for c in IDS],
            'relationships': [{'from': a, 'to': b, 'value': self.read(0x7D3D71+a*68+b, 'B')}
                              for a in (0,)+IDS for b in (0,)+IDS if a != b],
            'availability': [self.read(0x7A5120+c, 'B') for c in range(45)],
            'item_flags': [self.read(0x7AACAA+i*2, 'H') for i in range(1, 361)],
            'school': self.school_metadata()}

    def school_snapshot(self):
        # Independently read source buffers, not a Godot adapter's expectation.
        return {'month': self.read(0x7A528E, 'h'), 'week': self.read(0x7A5290, 'h'),
            'flags': {hex(a): self.read(a, 'h') for a in (0x7A55FA, 0x7A4E62, 0x7A55F6, 0x7E11A0)},
            'participants': [self.profile(c, result_fields=False) for c in IDS],
            'availability': [self.read(0x7A5120+c, 'B') for c in range(45)],
            'item_flags': [self.read(0x7AACAA+i*2, 'H') for i in range(1, 361)],
            **self.school_metadata(), 'adv_globals': {hex(a): self.read(a, 'h')
                for a in (0x7A5292, 0x7E1180, 0x7E1182)}}

    def application_snapshot(self):
        result = super().application_snapshot()
        result['canonical_layout'] = self.canonical_snapshot()
        result['school_layout'] = self.school_snapshot()
        return result

    def run_layout(self, name, *, probe_join_week=False):
        if self._ran_layout:
            raise RuntimeError('single-run layout probe')
        self._ran_layout = True
        result = self.replay_transaction(name)
        joined = after_week = None
        school_joined = school_after_week = None
        if probe_join_week:
            if self.all_inputs['special_date'] or not self.all_inputs['confirm'] or result['requested_state'] != 6:
                raise RuntimeError('direct join/week requires completed ordinary result')
            self._function_ranges += JOIN_NATIVE
            self.source = CHAPTER.read_bytes()
            self.uc.mem_write(SCRIPT, self.source)
            self.write(VM+0xC, SCRIPT)
            self.write(VM+5, 1, 'B')
            self.call(0x4CE560, (0, 7), receiver=VM)
            RosterJoinEmulator.call_join_step(self)
            joined, school_joined = self.canonical_snapshot(), self.school_snapshot()
            self.call_week()
            after_week, school_after_week = self.canonical_snapshot(), self.school_snapshot()
        return {'name': name, 'context_inputs': deepcopy(self.all_inputs),
            'before': result['before']['canonical_layout'], 'school_before': result['before']['school_layout'],
            'after_result': result['after']['canonical_layout'], 'school_after_result': result['after']['school_layout'],
            'after_join_probe': joined, 'school_after_join_probe': school_joined,
            'after_week_probe': after_week, 'school_after_week_probe': school_after_week,
            'result_branch': result['branch'], 'result_requested_state': result['requested_state'],
            'result_native_week': result['native_week_body_executed'],
            'result_before_week': result['before_week']['canonical_layout'] if result['before_week'] else None,
            'learning_draws': result['learning_draws'], 'native_rand_state': result['native_rand_state'],
            'result_events': result['events'], 'week_events': deepcopy(self.week_events),
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'chapter_completed': False, 'school_initialized': False, 'live_witness': False,
            'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'chapter020_sha256': hashlib.sha256(CHAPTER.read_bytes()).hexdigest(),
        'evidence_kind': 'same_cpu_result_school_layout_and_direct_join_week_probes',
        'limitations': ['Candidate5, roster/equipment and presentation are declared inputs before result execution.',
            'Both layouts read the same original buffers, including an unavailable candidate and 20 directed relations.',
            'Join prefix and subsequent whole week are DIRECT probes after ordinary result; no CH003/Chapter021 END or request7 is claimed.',
            'Special-date native week remains inside state12; no extra direct week is performed.',
            'No shared live world, school body or persistent save authority.'],
        'cases': [CampaignSchoolLayoutEmulator().run_layout('ordinary_layout_join_week', probe_join_week=True),
            CampaignSchoolLayoutEmulator(confirm=False).run_layout('ordinary_layout_wait'),
            CampaignSchoolLayoutEmulator(special_date=True).run_layout('special_layout_week')],
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    payload = report_text(report())
    path = ROOT / args.out
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
