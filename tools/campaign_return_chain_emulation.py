"""Continue actual native state12's CH003 load to native school construction.

One CPU and catalog are retained. The initial battle/world/round inputs, MVP,
presentation and some scheduler boundaries remain declared isolated inputs.
No preceding live battle, complete school body, or save authority is claimed.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_ESP

from tools.campaign_school_layout_emulation import CampaignSchoolLayoutEmulator
from tools.result_transaction_emulation import ResultTransactionEmulator
from tools.adv_chapter_emulation import AdvChapterEmulator, CH003, CONTROLLER
from tools.adv_week_handoff_emulation import AdvWeekHandoffEmulator
from tools.adv_route_emulation import AdvRouteEmulator
from tools.school_dispatch_emulation import SchoolDispatchEmulator
from tools.scene5_script_emulation import VM, SCRIPT, SCRIPT_SOURCE
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, TASK, report_text


class CampaignChapterStart(AdvChapterEmulator):
    """Insert the native result predecessor before the inherited ADV driver."""

    def run(self, name):
        self.phase = 'result'
        # Battle presentation readiness is a separate declared predecessor input.
        self.external.update(ui_ready=True, key_ready=True, fade_ready=True)
        self.result_record = deepcopy(self.replay_transaction(name))
        # The historical result tool reads its own synthetic controller address.
        # This combined driver declares the ADV controller from construction;
        # the native global pointer has used it for EVERY actual state request.
        # Read the real controller here; never copy/fabricate its memory fields.
        self.result_record['requested_state'] = self.read(CONTROLLER+0x30)
        self.after_result = self.canonical_snapshot()
        self.result_requests = deepcopy(self.state_requests)
        self.result_controller = self.controller_snapshot()
        before = self.roster_snapshot()
        completed_result = not self.result_record['bounded_stop'] and self.result_record['requested_state'] == 6
        if completed_result:
            if self.result_return_load is None or self.active_path != 'ch003.ybc' \
                    or self.read(VM+4, 'B') != 1 or self.read(VM+0x1C) != 0 \
                    or self.read(VM+0x92DC, 'i') != 7 \
                    or self.read(CONTROLLER+0x2C) != 1 or self.read(CONTROLLER+0x30) != 6:
                raise RuntimeError('ADV lacks actual result CH003 load and pending6/next7')
            self.result_adv_consumed = {'state': 6, 'pending_flag': 1, 'path': 'ch003.ybc',
                'next_task_state': 7, 'vm_active': 1, 'vm_pc': 0,
                'driver_boundary': 'consume_actual_result_request_without_adv_scheduler_constructor'}
            self.write(CONTROLLER+0x2C, 0)
            # Task construction/presentation remains a declared driver boundary.
            self.write(TASK, 0x5C306C)
            self.phase = 'chapter'
            self.external.update(self.chapter_inputs)
            self.frame_index, self.max_frames, self.stop_reason = -1, self.chapter_max_frames, None
            start = len(self.commands)
            requests = len(self.state_requests)
            self._thread(0x4D1A80, TASK, timeout=60_000_000, count=8_000_000)
            chapter_commands = deepcopy(self.commands[start:])
            chapter_requests = deepcopy(self.state_requests[requests:])
        else:
            chapter_commands, chapter_requests = [], []
        self.after_chapter = self.canonical_snapshot()
        self.chapter_controller = self.controller_snapshot()
        return {'name': name, 'before': before, 'after': self.roster_snapshot(),
            'commands': chapter_commands, 'loads': deepcopy(self.loads),
            'state_requests': chapter_requests, 'join_entries': deepcopy(self.join_entries),
            'chapter_completed': completed_result and self.stop_reason is None and self.read(VM+4, 'B') == 0,
            'stop_reason': self.stop_reason, 'active_path': self.active_path,
            'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30)}


class CampaignReturnChainEmulator(SchoolDispatchEmulator, CampaignChapterStart, CampaignSchoolLayoutEmulator):
    def __init__(self, *, confirm=True, chapter_key_ready=True, chapter_max_frames=6000,
                 continue_ready=True, school_fade_ready=True):
        if any(type(v) is not bool for v in (confirm, chapter_key_ready)) \
                or type(chapter_max_frames) is not int or not 1 <= chapter_max_frames <= 6000:
            raise ValueError('outside declared campaign chain inputs')
        self.phase = 'initializing'
        self.loading_result_return = None
        self.result_return_load = None
        self.result_adv_consumed = None
        self.result_record = None
        self.after_result = self.after_chapter = None
        self.result_controller = self.chapter_controller = None
        self.result_requests = []
        self._ran_campaign = False
        self.campaign_boundaries = []
        super().__init__(continue_ready=continue_ready, school_fade_ready=school_fade_ready)
        self.all_inputs.update(confirm=confirm, max_yields=450 if confirm else 360)
        self.chapter_inputs = {'ui_ready': True, 'key_ready': chapter_key_ready, 'fade_ready': True}
        self.chapter_max_frames = chapter_max_frames
        # Restore the original battle script BEFORE running the native predecessor.
        # The join setup performed by inherited constructors remains an initial
        # declaration; no roster/template/role buffer is reset between stages.
        self.source = SCRIPT_SOURCE.read_bytes()
        self.uc.mem_write(SCRIPT, self.source)
        self.write(VM+0xC, SCRIPT)
        self.write(TASK, 0)

    def controller_snapshot(self):
        return {'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
            'vm_active': self.read(VM+4, 'B'), 'vm_pc': self.read(VM+0x1C),
            'next_task_state': self.read(VM+0x92DC, 'i'), 'active_path': self.active_path}

    def flow_snapshot(self):
        # Existing drivers' snapshots now include the independently read full
        # catalog/history/relations, without changing their historical reports.
        result = super().flow_snapshot()
        result['canonical_layout'] = self.canonical_snapshot()
        result['school_layout'] = self.school_snapshot()
        return result

    def _hook(self, uc, address, size, user):
        if self.phase == 'result':
            sp = uc.reg_read(UC_X86_REG_ESP)
            if address == 0x439E30:
                self.state_requests.append({'va': hex(address), 'state': self.read(sp+4, 'i')})
            if self.loading_result_return is not None:
                if address == self.loading_result_return:
                    self.loading_result_return = None
                else:
                    return AdvChapterEmulator._hook(self, uc, address, size, user)
            if address == 0x4CE210 and self._raw_path(uc, self.read(sp+4)) == 'data/adv/dat/ch003.ybc':
                if self.result_return_load is not None or self.read(sp+8, 'i') != 7:
                    raise RuntimeError('unsupported or duplicate actual result return load')
                self.result_return_load = {'loader_va': '0x4ce210', 'path': 'ch003.ybc',
                    'next_task_state': 7, 'caller_return_va': hex(self.read(sp)),
                    'before': self.canonical_snapshot()}
                self.loading_result_return = self.read(sp)
                return AdvChapterEmulator._hook(self, uc, address, size, user)
            # Result/MVP retains its original audited policies. In particular,
            # an ADV driver must not run the MVP stub as a sourced chapter.
            return ResultTransactionEmulator._hook(self, uc, address, size, user)
        if address in (0x49F4E0, 0x49E2B0, 0x4D1A80) and self.phase in (
                'week', 'new_adv', 'workroom', 'ch002_adv', 'school_dispatch'):
            self.campaign_boundaries.append({'phase': self.phase, 'entry_va': hex(address),
                'controller': self.controller_snapshot(), 'canonical_layout': self.canonical_snapshot()})
        return super()._hook(uc, address, size, user)

    def run_chain(self, name, *, stop_at_handoff=False):
        if self._ran_campaign:
            raise RuntimeError('single-run campaign chain cannot replay consumed requests')
        self._ran_campaign = True
        if stop_at_handoff:
            continuation = AdvWeekHandoffEmulator.run_handoff(self, name)
        else:
            continuation = SchoolDispatchEmulator.run_school_dispatch(self, name)
        result = self.result_record
        return {'name': name, 'declared_inputs': {'result': deepcopy(self.all_inputs),
                'chapter': deepcopy(self.chapter_inputs), 'chapter_max_frames': self.chapter_max_frames,
                'continue_ready': self.continue_ready, 'school_fade_ready': self.school_fade_ready},
            'before_result': result['before']['canonical_layout'],
            'after_result': self.after_result, 'result_branch': result['branch'],
            'result_requested_state': result['requested_state'], 'result_events': result['events'],
            'result_native_week': result['native_week_body_executed'],
            'learning_draws': result['learning_draws'], 'native_rand_state': result['native_rand_state'],
            'native_result_return_load': self.result_return_load,
            'result_controller': self.result_controller, 'result_state_requests': self.result_requests,
            'result_adv_consumed_request': self.result_adv_consumed,
            'after_chapter': self.after_chapter, 'chapter_controller': self.chapter_controller,
            'continuation': continuation, 'boundaries': self.campaign_boundaries,
            'after': self.canonical_snapshot(), 'school_after': self.school_snapshot(),
            'resource_loads': deepcopy(self.loads), 'commands': deepcopy(self.commands),
            'state_requests': deepcopy(self.state_requests), 'week_events': deepcopy(self.week_events),
            'controller': self.controller_snapshot(), 'stop_reason': self.stop_reason,
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'stub_calls': dict(self.stub_calls), 'school_initialized': False,
            'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'same_cpu_native_result_return_load_adv_week_workroom_school_dispatch',
        'limitations': ['Initial battle/world/round/role inputs and MVP completion are declared isolated inputs.',
            'Actual state12 CH003 load/next7 and pending6 are retained; the ADV driver does not reload CH003.',
            'All result/ADV/roster/week/workroom/school construction buffers continue in one CPU without role resets.',
            'Some task handoffs, UI/audio/movie, allocation and registration remain explicit boundaries.',
            'School construction is not complete school initialization or interaction; no live/save authority.'],
        'cases': [CampaignReturnChainEmulator().run_chain('result_to_school_construction'),
            CampaignReturnChainEmulator(confirm=False).run_chain('result_confirmation_wait', stop_at_handoff=True),
            CampaignReturnChainEmulator(chapter_key_ready=False, chapter_max_frames=200).run_chain(
                'chapter_key_wait', stop_at_handoff=True),
            CampaignReturnChainEmulator(continue_ready=False).run_chain('workroom_continue_wait'),
            CampaignReturnChainEmulator(school_fade_ready=False).run_chain('ch002_fade_wait')],
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
