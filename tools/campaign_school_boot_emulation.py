"""Continue the same native result-return CPU through captured school boot.

Keeps all role/roster/control memory, with no reset at school construction.
Stops before group menu interaction and after two person idle yields.
"""
import argparse
from copy import deepcopy
import hashlib

from tools.campaign_return_chain_emulation import CampaignReturnChainEmulator
from tools.school_boot_emulation import SchoolBootEmulator, BOOT_NATIVE
from tools.school_dispatch_emulation import GROUP_TASK, PERSON_TASK
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text


class CampaignSchoolBootEmulator(CampaignReturnChainEmulator, SchoolBootEmulator):
    def school_metadata(self):
        result = super().school_metadata()
        result['school_control'] = self.boot_control_snapshot()
        return result

    def run_campaign_boot(self, name):
        if self._ran_boot:
            raise RuntimeError('single-run campaign school boot')
        self._ran_boot = True
        upstream = self.run_chain(name)
        before = self.canonical_snapshot()
        school_before = self.school_snapshot()
        checkpoints = []
        if upstream['continuation']['school_constructed']:
            self._function_ranges += BOOT_NATIVE
            self.phase = 'school_group_boot'
            self.stop_reason = None
            self._thread(0x4AB7A0, GROUP_TASK)
            if not self.group_initialized:
                raise RuntimeError('group boot did not reach source menu boundary')
            checkpoints.append({'phase': 'school_group_boot', 'after': self.canonical_snapshot()})
            self.phase = 'school_person_boot'
            self.stop_reason = None
            self._thread(0x4B8D50, PERSON_TASK)
            if not self.person_resource_initialized:
                raise RuntimeError('person boot did not reach source idle boundary')
            checkpoints.append({'phase': 'school_person_boot', 'after': self.canonical_snapshot()})
        return {'name': name, 'upstream': deepcopy(upstream), 'before': before,
            'school_before': school_before, 'after': self.canonical_snapshot(),
            'school_after': self.school_snapshot(), 'boot_checkpoints': checkpoints,
            'boot_events': deepcopy(self.boot_events), 'state_requests': deepcopy(self.state_requests),
            'group_initialized': self.group_initialized,
            'person_resource_initialized': self.person_resource_initialized,
            'person_idle_yields': self.person_idle_yields, 'stop_reason': self.stop_reason,
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'stub_calls': dict(self.stub_calls), 'school_initialized': False,
            'interactive_school_ready': False, 'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'same_cpu_result_return_to_captured_school_boot',
        'limitations': ['All result/ADV/week/workroom/school buffers continue without resets in one CPU.',
            'The tactical predecessor, MVP completion, presentation, allocation and scheduling retain declared boundaries.',
            'Group initialization stops before 4A7C40 menu interaction; person initialization stops at two idle yields.',
            'Teacher worksheets and uncaptured school controls are outside the captured projection; no live/save authority.'],
        'cases': [CampaignSchoolBootEmulator().run_campaign_boot('result_to_school_boot'),
            CampaignSchoolBootEmulator(school_fade_ready=False).run_campaign_boot('ch002_wait_blocks_campaign_boot')],
        'school_initialized': False, 'interactive_school_ready': False,
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
