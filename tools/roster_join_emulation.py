"""Run Chapter020's sourced opcode144 and complete native student-join helpers.

Templates, roster, availability and equipment are explicit isolated inputs.
Only the joining prefix is executed; the chapter never gets a synthetic END.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.week_settlement_emulation import WeekSettlementEmulator
from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.scene5_script_emulation import VM, SCRIPT
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, STACK, RETURN, report_text

CHAPTER = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT/Chapter020.ybc'
JOIN_NATIVE = ((0x4D0900, 0x4D0990), (0x4D3E90, 0x4D4250), (0x4D4730, 0x4D4770))


class RosterJoinEmulator(WeekSettlementEmulator):
    def __init__(self, *, difficulty=0, already_available=False):
        super().__init__()
        if type(difficulty) is not int or difficulty not in (0, 2) or type(already_available) is not bool:
            raise ValueError('outside declared student-join inputs')
        self._function_ranges += JOIN_NATIVE
        self.join_entries = []
        self.source = CHAPTER.read_bytes()
        self.uc.mem_write(SCRIPT, self.source)
        self.write(VM+0xC, SCRIPT)
        self.write(VM+5, 1, 'B')
        self.write(0x7A528C, difficulty, 'h')
        self.write(0x7A528E, 4, 'h')
        self.write(0x7A5290, 5, 'h')
        self.write(0x7A5260, 4 if already_available else 3, 'h')
        self.write(0x7A528A, 0, 'h')
        for index in range(20):
            self.write(0x7A5210+index*2, ([3, 4, 9, 5] if already_available else [3, 4, 9])[index]
                       if index < (4 if already_available else 3) else -1, 'h')
            self.write(0x7A5262+index*2, -1, 'h')
        self.write(0x7A5120+5, int(already_available), 'B')
        template = bytes(self.uc.mem_read(0x6F5088+5*CHAR_STRIDE, CHAR_STRIDE))
        self.template_sha256 = hashlib.sha256(template).hexdigest()
        self.uc.mem_write(CHAR_BASE+5*CHAR_STRIDE, template)
        self.uc.mem_write(PACKAGE_BASE+5*PACKAGE_STRIDE, bytes(PACKAGE_STRIDE))
        for k in range(31):
            self.write(PACKAGE_BASE+5*PACKAGE_STRIDE+0xD7+k, k-15, 'b')
        self.uc.mem_write(PACKAGE_BASE+5*PACKAGE_STRIDE+0xF9, bytes([1])*32)
        base = CHAR_BASE+5*CHAR_STRIDE
        for slot in range(8):
            self.write(base+0x52+slot*2, [1, 2, 1][slot] if slot < 3 else 0, 'h')
            self.write(base+0x62+slot*2, [6, 7, 6][slot] if slot < 3 else 0, 'h')
        self.write(base+0xB8, 0, 'B')
        self.write(base+0xB8+0xC, 0, 'B')
        self.write(base+0x50, 47, 'B')
        self.write(0x7AACAA+6*2, 0x100, 'H')
        self.write(0x7AACAA+7*2, 0x101, 'H')
        self.call(0x4CE560, (0, 7), receiver=VM)

    def _hook(self, uc, address, size, user):
        if address == 0x4D3E90:
            sp = uc.reg_read(UC_X86_REG_ESP)
            self.join_entries.append({'va': hex(address), 'caller_return_va': hex(self.read(sp)),
                'character_id': self.read(sp+4, 'h'), 'group': self.read(sp+8, 'h'),
                'slot': self.read(sp+12, 'h')})
        return super()._hook(uc, address, size, user)

    def roster_snapshot(self):
        result = self.week_snapshot()
        # Include all known candidates, not only initially available students.
        result['participants'] = []
        for character in (3, 4, 5, 9):
            base, package = CHAR_BASE+character*CHAR_STRIDE, PACKAGE_BASE+character*PACKAGE_STRIDE
            result['participants'].append({'character_id': character, 'job': self.read(base+6, 'h'),
                'attributes': [self.read(base+0xC+k*8, 'B') for k in range(7)],
                'growth_pools': [self.read(base+0x10+k*8) for k in range(7)],
                'level_50': self.read(base+0x50, 'B'),
                'job_progress': [self.read(package+0xD7+k, 'b') for k in range(31)],
                'unlock_flags': [self.read(package+0xF9+k, 'B') for k in range(30)],
                'unlock_reserved_bytes': [self.read(package+0x117+k, 'B') for k in range(2)],
                'skill_statuses': [self.read(base+0xB8+k*0xC, 'B') for k in range(84)],
                'equipped_skills': [self.read(base+0x52+k*2, 'h') for k in range(8)],
                'equipped_items': [self.read(base+0x62+k*2, 'h') for k in range(8)],
                'character_sha256': hashlib.sha256(bytes(self.uc.mem_read(base, CHAR_STRIDE))).hexdigest(),
                'package_sha256': hashlib.sha256(bytes(self.uc.mem_read(package, PACKAGE_STRIDE))).hexdigest()})
        result.pop('nonparticipant_character_sha256')
        result.pop('nonparticipant_package_sha256')
        result['student_count'] = self.read(0x7A5260, 'h')
        result['student_ids'] = [self.read(0x7A5210+k*2, 'h') for k in range(20)]
        result['teacher_count'] = self.read(0x7A528A, 'h')
        result['teacher_ids'] = [self.read(0x7A5262+k*2, 'h') for k in range(20)]
        result['group_student_ids'] = [[self.read(0x7AAA22+g*0x1C+k*2, 'h') for k in range(4)] for g in range(5)]
        result['group_student_indices'] = [[self.read(0x7AAAE0+g*8+k*2, 'h') for k in range(4)] for g in range(5)]
        return result

    def run_prefix(self, name, *, repeat=False):
        before = self.roster_snapshot()
        self.call_join_step()
        once = self.roster_snapshot()
        if repeat:
            self.write(VM+0x1C, 0)  # Declared duplicate delivery of the same sourced opcode.
            self.call_join_step()
        return {'name': name, 'difficulty': self.read(0x7A528C, 'h'), 'repeat_opcode': repeat,
                'before': before, 'after_once': once, 'after': self.roster_snapshot(),
                'commands': self.commands, 'join_entries': self.join_entries,
                'vm_active': self.read(VM+4, 'B'), 'vm_pc': self.read(VM+0x1C),
                'template5_sha256': self.template_sha256,
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'stub_calls': dict(self.stub_calls), 'chapter_completed': False,
                'school_initialized': False, 'live_witness': False, 'authorizes_persistent_write': False}

    def call_join_step(self):
        # The full join includes stat aggregation and 30 unlock evaluations.
        # Use the same bounded budget as whole-week evaluation, not the short
        # leaf-helper timeout; retain the actual VM and stack-return checks.
        sp = STACK+0xff00
        self.write(sp, RETURN)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, VM)
        self.uc.emu_start(0x4CE8F0, RETURN, timeout=10_000_000, count=2_000_000)
        if self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
            raise RuntimeError('join VM step did not return within audit bounds')
        if self.uc.reg_read(UC_X86_REG_ESP) != sp+4:
            raise RuntimeError('join VM calling convention/stack mismatch')


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
            'source_chapter020_sha256': hashlib.sha256(CHAPTER.read_bytes()).hexdigest(),
            'evidence_kind': 'native_sourced_student_join_with_synthetic_roster_inputs',
            'additional_native_ranges': [[hex(a), hex(b)] for a, b in JOIN_NATIVE],
            'synthetic_setup': {'initial_students': [3, 4, 9], 'candidate': 5,
                'candidate_template_va': hex(0x6F5088+5*CHAR_STRIDE),
                'job_progress': list(range(-15, 16)), 'unlock_and_reserved_bytes': [1]*32,
                'equipped_skills': [1, 2, 1]+[0]*5, 'equipped_items': [6, 7, 6]+[0]*5,
                'skill_status_overrides': {'1': 0, '2': 0}, 'level_50': 47,
                'item6_flags': 0x100, 'item7_flags': 0x101},
            'limitations': ['Chapter020 opcode144 at file0x14 runs native dispatcher and all join helpers.',
                'Templates, roster, availability, equipment and package markers are declared isolated inputs.',
                'Only the joining prefix is executed; remaining chapter/UI/Chapter021 and school are not executed.',
                'Duplicate opcode delivery resets PC explicitly; availability gate itself runs native code.',
                'Group=-1/slot=-1 student-join case only; teachers, removals and assigned class slots are not covered.'],
            'cases': [RosterJoinEmulator().run_prefix('chapter020_join5'),
                      RosterJoinEmulator(difficulty=2).run_prefix('difficulty2_clears_equipped_skills'),
                      RosterJoinEmulator(already_available=True).run_prefix('already_available_noop'),
                      RosterJoinEmulator().run_prefix('duplicate_join_opcode', repeat=True)],
            'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT / args.out
    if path.exists():
        parser.error('output already exists; use a new path')
    payload = report_text(report())
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
