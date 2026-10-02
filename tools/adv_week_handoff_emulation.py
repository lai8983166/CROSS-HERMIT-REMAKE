"""Consume actual Chapter021 next7 request and run native state7 in one CPU.

The driver consumes a verified pending request; scheduler construction remains
an explicit boundary. CH001 is loaded natively but its body is not executed.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.adv_chapter_emulation import AdvChapterEmulator, CH003, CONTROLLER
from tools.adv_route_emulation import AdvRouteEmulator
from tools.scene5_script_emulation import VM
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, STACK, RETURN, TASK, report_text

START_NATIVE = ((0x49F4E0, 0x49F570),)


class AdvWeekHandoffEmulator(AdvChapterEmulator):
    def __init__(self, *, week_fade_ready=True, **chapter_inputs):
        if type(week_fade_ready) is not bool:
            raise ValueError('week fade must be declared boolean')
        self.phase = 'chapter'
        super().__init__(**chapter_inputs)
        self._function_ranges += START_NATIVE
        self.week_fade_ready = week_fade_ready
        self.week_yields = 0
        self.week_start_events = []
        self.consumed_request = None
        self._ran_handoff = False

    def _resource(self, pointer):
        if self.phase == 'week':
            name = AdvRouteEmulator._path(self, pointer)
            if name != 'ch001.ybc':
                raise RuntimeError('state7 attempted an undeclared resource')
            source = (CH003.parent / name).read_bytes()
            if len(source) > 0x10000:
                raise RuntimeError('CH001 exceeds bounded resource workspace')
            return name, source
        return super()._resource(pointer)

    def _hook(self, uc, address, size, user):
        if self.phase == 'week':
            sp = uc.reg_read(UC_X86_REG_ESP)
            if address == 0x49F4E0:
                if self.consumed_request is not None or self.read(VM+4, 'B') != 0 \
                        or self.read(CONTROLLER+0x2C) != 1 or self.read(CONTROLLER+0x30) != 7:
                    raise RuntimeError('state7 requires unconsumed actual ADV completion request')
                self.consumed_request = {'state': self.read(CONTROLLER+0x30),
                    'pending_flag': self.read(CONTROLLER+0x2C), 'adv_active': self.read(VM+4, 'B'),
                    'source': 'native_439e30_after_chapter021_end',
                    'driver_boundary': 'consume_pending_request_without_scheduler_constructor'}
                self.write(CONTROLLER+0x2C, 0)  # Declared driver consumption, not fabricated state7.
            if address in (0x4DB230, 0x4DB270, 0x4DB120):
                name = {0x4DB230: 'fade_start', 0x4DB270: 'fade_ready', 0x4DB120: 'fade_release'}[address]
                event = {'kind': name, 'va': hex(address)}
                if address == 0x4DB230:
                    event['frames'] = self.read(sp+4)
                self.week_start_events.append(event)
                self.stub_calls['declared_week_'+name] += 1
                self._stub_return(int(self.week_fade_ready) if address == 0x4DB270 else 0, 0)
                return
            if address == 0x422360:
                self.week_yields += 1
                if self.week_yields > 4:
                    self.stop_reason = 'week_fade_pending_after_settlement'
                    uc.emu_stop()
                    return
            if address == 0x4CE210:
                self.week_start_events.append({'kind': 'script_load', 'path': AdvRouteEmulator._path(self, self.read(sp+4)),
                                               'next_task_state': self.read(sp+8, 'i')})
            if address == 0x439E30:
                self.week_start_events.append({'kind': 'state_request', 'state': self.read(sp+4, 'i')})
            if any(a <= address < b for a, b in START_NATIVE):
                return ExitEmulator._hook(self, uc, address, size, user)
        return super()._hook(uc, address, size, user)

    def run_handoff(self, name):
        if self._ran_handoff:
            raise RuntimeError('single-run native handoff probe cannot replay a consumed request')
        self._ran_handoff = True
        chapter = deepcopy(super().run(name))
        after_adv = self.roster_snapshot()
        if chapter['chapter_completed']:
            # Select the actual requested task. Do not substitute a synthetic
            # completion boolean or paste a previous week probe's snapshot.
            if chapter['state_requests'] != [{'va': '0x439e30', 'state': 7}]:
                raise RuntimeError('chapter completed without the audited next7 request')
            self.phase = 'week'
            sp = STACK+0xFF00
            self.write(sp, RETURN)
            self.write(sp+4, 0)
            self.uc.reg_write(UC_X86_REG_ESP, sp)
            self.uc.reg_write(UC_X86_REG_ECX, TASK)
            self.uc.emu_start(0x49F4E0, RETURN, timeout=10_000_000, count=2_000_000)
            if self.stop_reason is None and (self.uc.reg_read(UC_X86_REG_EIP) != RETURN
                                            or self.uc.reg_read(UC_X86_REG_ESP) != sp+8):
                raise RuntimeError('post-ADV state7 exceeded bounds or ret4 stack mismatch')
        return {'name': name, 'chapter': chapter, 'after_adv': after_adv,
            'consumed_request': self.consumed_request, 'week_fade_ready': self.week_fade_ready,
            'week_executed': self.week_entry_snapshot is not None,
            'week_events': self.week_events, 'week_start_events': self.week_start_events,
            'after': self.roster_snapshot(), 'resource_loads': self.loads,
            'active_path': self.active_path, 'vm_active': self.read(VM+4, 'B'), 'vm_pc': self.read(VM+0x1C),
            'stored_next_task_state': self.read(VM+0x92DC, 'i'), 'state_requests': self.state_requests,
            'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
            'stop_reason': self.stop_reason, 'stub_calls': dict(self.stub_calls),
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'ch001_body_executed': False, 'school_initialized': False,
            'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_adv_completion_and_whole_week_in_shared_memory',
        'additional_native_ranges': [[hex(a), hex(b)] for a, b in START_NATIVE],
        'limitations': ['Inherits explicit synthetic date4/5, roster/templates/equipment and presentation boundaries.',
            'Same CPU, roster and equipment continue from sourced CH003/Chapter020/Chapter021 execution.',
            'Driver consumes actual native pending7 request; task scheduler/constructor is not executed.',
            'State7 runs full week with all four students, then native CH001 load and request6 when fade ready.',
            'CH001 body, state8/workroom, CH002 and school initialization are not executed.',
            'No preceding battle or live/persistent transaction authority.'],
        'cases': [AdvWeekHandoffEmulator().run_handoff('adv_complete_then_week'),
                  AdvWeekHandoffEmulator(week_fade_ready=False).run_handoff('week_fade_wait_after_adv'),
                  AdvWeekHandoffEmulator(key_ready=False, max_frames=200).run_handoff('pending_adv_never_runs_week')],
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
