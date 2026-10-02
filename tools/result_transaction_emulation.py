"""Native state12 role and complete week writes in one isolated CPU instance.

Combines existing native audit policies, preserving their immutable reports.
World, school roster, availability, equipment and presentation inputs remain
declared synthetic inputs. State6 is a request, not school task execution.
"""
import argparse
import hashlib

from tools.role_application_emulation import RoleApplicationEmulator
from tools.week_settlement_emulation import WeekSettlementEmulator
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text


class ResultTransactionEmulator(WeekSettlementEmulator, RoleApplicationEmulator):
    def __init__(self, *, special_date=False, confirm=True, mvp_ready=True,
                 mode=0, result_flag=0):
        # Cooperative MRO retains Role's RNG capture and Week's native helpers.
        super().__init__()
        if type(mode) is not int or mode not in (0, 1) or result_flag not in (0, 1):
            raise ValueError('outside declared mode/result subset')
        self.all_inputs.update(special_date=special_date, confirm=confirm,
            mvp_ready=mvp_ready, mode=mode, result_flag=result_flag,
            max_yields=360 if not confirm or not mvp_ready else 450)
        self.role_week_entry_snapshot = None

    def _hook(self, uc, address, size, user):
        if address == 0x4D3510:
            if self.role_week_entry_snapshot is not None:
                raise RuntimeError('duplicate week entry in transaction')
            self.role_week_entry_snapshot = self.application_snapshot()
        return super()._hook(uc, address, size, user)

    def application_snapshot(self):
        roles, week = super().application_snapshot(), self.week_snapshot()
        for key in ('flags', 'availability', 'item_flags'):
            roles[key] = week[key]
        for record, week_record in zip(roles['characters'], week['participants']):
            if record['character_id'] != week_record['character_id']:
                raise RuntimeError('snapshot identity mismatch')
            for key in ('unlock_flags', 'equipped_skills', 'equipped_items'):
                record[key] = week_record[key]
        return roles

    def replay_transaction(self, name):
        result = self.replay_roles(name)
        result['before_week'] = self.role_week_entry_snapshot
        result['week_events'] = self.week_events
        result['native_week_body_executed'] = self.role_week_entry_snapshot is not None
        result['school_task_executed'] = False
        return result


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_state12_role_week_transaction_with_synthetic_inputs',
        'limitations': ['Same original task instance executes state11/10/12, role application and optional complete week.',
            'World, terminal selection, roster, availability, equipment and clock remain synthetic.',
            'Mode1 is injected after mode0 preparation, not a complete mode1 battle witness.',
            'MVP completion and CH003 script loading remain declared external boundaries.',
            'Only state6/13/15 requests are observed; their tasks and school script are not executed.',
            'No original process, save or persistent world is modified.'],
        'cases': [ResultTransactionEmulator().replay_transaction('ordinary_confirm'),
            ResultTransactionEmulator(confirm=False).replay_transaction('ordinary_unconfirmed'),
            ResultTransactionEmulator(mvp_ready=False).replay_transaction('mvp_boundary_busy'),
            ResultTransactionEmulator(mode=1).replay_transaction('mode1_flag0'),
            ResultTransactionEmulator(mode=1, result_flag=1).replay_transaction('mode1_flag1'),
            ResultTransactionEmulator(special_date=True).replay_transaction('special_complete_week')],
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
