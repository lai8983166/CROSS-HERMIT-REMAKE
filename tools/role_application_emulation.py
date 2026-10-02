"""Expanded native role evidence: full progress bytes, slot0 relations, skill probes.

Historical reports remain unchanged. These are isolated synthetic scenarios,
not live terminal selection or authority to write a persistent game state.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.all_result_emulation import AllResultEmulator, ALL_TASK
from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE, TLS
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, STACK, RETURN, report_text


class RoleApplicationEmulator(AllResultEmulator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Explicit entry for direct skill-grid probes; body was already native.
        self._function_ranges += ((0x4BFFC0, 0x4C0060), (0x4C1350, 0x4C1910))
        self.learning_draws = []
        self.growth_probe_running = False

    def _hook(self, uc, address, size, user):
        if address == 0x4C114D and (self.all_running or self.growth_probe_running):
            value = uc.reg_read(UC_X86_REG_EAX) & 0xFFFF
            self.learning_draws.append({'return_va': '0x4c114d', 'rand': value,
                'modulo101': value % 101, 'native_rand_state': self.read(TLS+0x14)})
        return super()._hook(uc, address, size, user)

    def application_snapshot(self):
        snapshot = super().application_snapshot()
        for record in snapshot['characters']:
            base = PACKAGE_BASE+record['character_id']*PACKAGE_STRIDE
            progress = [self.read(base+0xD7+k, 'b') for k in range(31)]
            record['job_progress_values'] = progress
            record['learning_job_sums'] = [sum(progress[1+block*10+k*2+j]
                for block in range(3) for j in range(2)) for k in range(5)]
        # Parent's three-student view did not expose the default task teacher
        # slot0. Capture all off-diagonal links among the reached raw slots.
        slots = (0, 3, 4, 9)
        snapshot['relationships'] = [{'from': a, 'to': b,
            'value': self.read(0x7D3D71+a*68+b, 'B')} for a in slots for b in slots if a != b]
        return snapshot

    def replay_roles(self, name):
        result = self.replay_all(name)
        result['school_setup']['task_teacher_slots'] = [0]*5
        result['school_setup']['task_allocation_initial_contents'] = 'explicit_zero_memory'
        result['learning_draws'] = self.learning_draws
        result['native_rand_state'] = self.read(TLS+0x14)
        result['skill_display_needed'] = self.read(ALL_TASK+0x142C, 'h')
        return result

    def call_growth(self, character):
        """Bounded ret4 call; large counterfactual skill pools need a longer walk."""
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, character)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, ALL_TASK)
        self.uc.emu_start(0x4C0C10, RETURN, timeout=10_000_000, count=2_000_000)
        if self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
            raise RuntimeError(f'growth probe exceeded bounds at {self.uc.reg_read(UC_X86_REG_EIP):#x}')
        if self.uc.reg_read(UC_X86_REG_ESP) != sp+8:
            raise RuntimeError('growth probe ret4 stack mismatch')

    def probe_post_fields(self):
        self.replay('post_field_setup')
        for character, value in ((3, 127), (4, 100), (9, 99)):
            job = self.read(CHAR_BASE+character*CHAR_STRIDE+6, 'h')
            self.write(PACKAGE_BASE+character*PACKAGE_STRIDE+0xD7+job, value, 'b')
        before = self.application_snapshot()
        self.call(0x4C1350, receiver=ALL_TASK)
        return {'name': 'job_progress_wrap_sentinel_cap',
            'evidence_kind': 'direct_post_field_probe', 'before': before,
            'after': self.application_snapshot(), 'state12_executed': False,
            'authorizes_persistent_write': False,
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)]}

    def probe_skill(self, name, *, skill_id=8, seed=4660, low_attribute=False,
                    blocked=False, job_progress=0):
        if skill_id not in (8, 61) or seed not in (4660, 17) or job_progress not in (0, 8, 9):
            raise ValueError('outside declared skill probe subset')
        character = 3
        base, package = CHAR_BASE+character*CHAR_STRIDE, PACKAGE_BASE+character*PACKAGE_STRIDE
        self.seed = seed
        cap_pool = sum(self.read(0x6E4308+k*4) for k in range(101))
        for k in range(7):
            value = 9 if low_attribute and k == 1 else 100
            pool = sum(self.read(0x6E4308+i*4) for i in range(value+1))
            self.write(base+0xC+k*8, value, 'B')
            self.write(base+0x10+k*8, pool)
        for k in range(84):
            self.write(base+0xB8+k*0xC, 3, 'B')
        self.write(base+0xB8+(skill_id-1)*0xC, 2 if blocked else 0, 'B')
        self.write(package+0xD7+9, job_progress, 'B')
        self.call(0x4BFFC0, receiver=ALL_TASK)
        self.call(0x4D1C60)
        before = self.application_snapshot()
        self.growth_probe_running = True
        self.call_growth(character)
        self.growth_probe_running = False
        return {'name': name, 'evidence_kind': 'direct_character_growth_skill_probe',
            'synthetic_probe': {'character_id': 3, 'job': 10, 'skill_id': skill_id,
                'clock_seed': seed, 'other_skill_statuses': 3,
                'target_initial_status': 2 if blocked else 0,
                'attributes': [100, 9 if low_attribute else 100, 100, 100, 100, 100, 100],
                'job_progress_index9': job_progress, 'staged_package': [0]*8,
                'cap100_pool': cap_pool,
                'note': 'Counterfactual high pools/learned skills, not a valid live progression witness.'},
            'before': before, 'after': self.application_snapshot(),
            'learning_draws': self.learning_draws, 'native_rand_state': self.read(TLS+0x14),
            'skill_display_needed': self.read(ALL_TASK+0x142C, 'h'),
            'state12_executed': False,
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_role_application_with_synthetic_school_and_skill_probes',
        'limitations': ['World/terminal inputs and original MVP/school script boundaries remain synthetic.',
            'Expanded task probes allocate zero memory; absent teacher leaves raw task slot0, not a named teacher.',
            'Direct skill probes never execute state12 or a battle and use counterfactual learned skills/pools.',
            'Special-date task stops before week; use the separately audited week report for that body.',
            'No persistent world, original process or save is modified.'],
        'task_cases': [RoleApplicationEmulator().replay_roles('ordinary_confirm'),
            RoleApplicationEmulator(confirm=False, max_yields=360).replay_roles('ordinary_unconfirmed'),
            RoleApplicationEmulator(mvp_ready=False, max_yields=360).replay_roles('mvp_boundary_busy'),
            RoleApplicationEmulator(mode=1).replay_roles('mode1_flag0'),
            RoleApplicationEmulator(mode=1, result_flag=1).replay_roles('mode1_flag1'),
            RoleApplicationEmulator(special_date=True).replay_roles('special_week_boundary')],
        'post_field_probes': [RoleApplicationEmulator().probe_post_fields()],
        'skill_probes': [RoleApplicationEmulator().probe_skill('skill8_candidate'),
            RoleApplicationEmulator().probe_skill('skill8_random_reject', seed=17),
            RoleApplicationEmulator().probe_skill('skill8_attribute_reject', low_attribute=True),
            RoleApplicationEmulator().probe_skill('skill8_already_pending', blocked=True),
            RoleApplicationEmulator().probe_skill('skill61_job_below', skill_id=61, job_progress=8),
            RoleApplicationEmulator().probe_skill('skill61_job_exact', skill_id=61, job_progress=9)],
        'authorizes_persistent_write': False}


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
