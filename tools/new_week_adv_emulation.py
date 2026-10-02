"""Continue native state7's actual CH001 load through Chapter022/208 to next8.

The same CPU/roster continues; movie/render readiness is explicit simulation.
The workroom body and school constructor are not executed by this probe.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.adv_week_handoff_emulation import AdvWeekHandoffEmulator
from tools.adv_route_emulation import AdvRouteEmulator
from tools.adv_chapter_emulation import CH003, CONTROLLER
from tools.scene5_script_emulation import VM
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, STACK, RETURN, TASK, report_text

NEW_ADV_NATIVE = ((0x4C2730, 0x4C27F0), (0x4C28B0, 0x4C2940),
                  (0x4C4750, 0x4C4840), (0x4D0DA0, 0x4D0EB0), (0x4CCB30, 0x4CCB90))
MOVIE_STUBS = {0x4CDE10: ('movie_resource', 8), 0x4C2AF0: ('movie_display', 12),
              0x4C3730: ('movie_unload', 12)}
ADV_GLOBALS = (0x7A5292, 0x7E1180, 0x7E1182)


class NewWeekAdvEmulator(AdvWeekHandoffEmulator):
    def __init__(self, *, new_ui_ready=True, new_key_ready=True, new_fade_ready=True, new_max_frames=6000):
        if any(type(v) is not bool for v in (new_ui_ready, new_key_ready, new_fade_ready)) \
                or type(new_max_frames) is not int or not 1 <= new_max_frames <= 6000:
            raise ValueError('outside declared new-week ADV inputs')
        super().__init__()
        self._function_ranges += NEW_ADV_NATIVE
        self._stubs.update(MOVIE_STUBS)
        self._stubs[0x4128F0] = ('declared_skip_key', 8)
        self.new_inputs = {'ui_ready': new_ui_ready, 'key_ready': new_key_ready, 'fade_ready': new_fade_ready}
        self.new_max_frames = new_max_frames
        self.movie_events = []
        self.new_adv_consumed = None
        self._ran_new_adv = False
        self.write(TASK+0x198C, 0)
        self.write(TASK+0x1990, 0)  # Declared no mouse button for movie timer/or-key.

    def flow_snapshot(self):
        result = self.roster_snapshot()
        result['adv_globals'] = {hex(a): self.read(a, 'h') for a in ADV_GLOBALS}
        return result

    def _resource(self, pointer):
        if self.phase == 'new_adv':
            name = AdvRouteEmulator._path(self, pointer)
            if name not in ('chapter022.ybc', 'chapter208.ybc'):
                raise RuntimeError('new-week ADV attempted an undeclared resource')
            source = (CH003.parent / name).read_bytes()
            if len(source) > 0x10000:
                raise RuntimeError('new-week ADV exceeds bounded workspace')
            return name, source
        return super()._resource(pointer)

    def _hook(self, uc, address, size, user):
        if any(a <= address < b for a, b in NEW_ADV_NATIVE):
            return ExitEmulator._hook(self, uc, address, size, user)
        if self.phase == 'new_adv':
            sp = uc.reg_read(UC_X86_REG_ESP)
            if address == 0x4128F0:
                if (self.read(sp+4), self.read(sp+8)) != (0x39, 0):
                    raise RuntimeError('undeclared new-week skip key query')
                self.stub_calls['declared_skip_key'] += 1
                self._stub_return(int(self.external['key_ready']), 8)
                return
            if address == 0x4D1A80:
                if self.new_adv_consumed is not None or self.read(CONTROLLER+0x2C) != 1 \
                        or self.read(CONTROLLER+0x30) != 6 or self.active_path != 'ch001.ybc' \
                        or self.read(VM+4, 'B') != 1 or self.read(VM+0x1C) != 0 or self.read(VM+0x92DC, 'i') != 8:
                    raise RuntimeError('CH001 requires actual state7 load and unconsumed request6/next8')
                self.new_adv_consumed = {'state': 6, 'pending_flag': 1, 'path': self.active_path,
                    'next_task_state': 8, 'vm_active': 1, 'vm_pc': 0,
                    'driver_boundary': 'consume_native_pending_request_without_scheduler_constructor'}
                self.write(CONTROLLER+0x2C, 0)
            if address in MOVIE_STUBS:
                name, pop = MOVIE_STUBS[address]
                self.stub_calls[name] += 1
                if name == 'movie_resource':
                    raw = bytes(uc.mem_read(self.read(sp+4), 256)).split(b'\0')[0]
                    path = '/'.join(p for p in raw.decode('ascii').lower().replace('\\', '/').split('/') if p)
                    if path != 'data/adv/bin/tc0501.bin' or self.read(sp+8) != 0x15:
                        raise RuntimeError('undeclared movie resource')
                    source = (ROOT / 'CROSS HERMIT/CROSS HERMIT' / path).read_bytes()
                    self.movie_events.append({'path': path, 'source_sha256': hashlib.sha256(source).hexdigest(),
                                              'resource_slot': self.read(sp+8), 'body_executed': False})
                    self._stub_return(0, pop)
                else:
                    self._stub_return(self.read(sp+12), pop)
                return
        return super()._hook(uc, address, size, user)

    def run_new_adv(self, name):
        if self._ran_new_adv:
            raise RuntimeError('single-run new-week ADV probe cannot replay consumed request')
        self._ran_new_adv = True
        previous = deepcopy(super().run_handoff(name))
        if previous['stop_reason'] is not None or previous['active_path'] != 'ch001.ybc':
            raise RuntimeError('new-week ADV lacks completed native predecessor')
        before = self.flow_snapshot()
        self.phase = 'new_adv'
        self.external.update(self.new_inputs)
        self.max_frames = self.new_max_frames
        self.frame_index = -1
        self.stop_reason = None
        command_start, load_start, request_start = len(self.commands), len(self.loads), len(self.state_requests)
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, TASK)
        self.uc.emu_start(0x4D1A80, RETURN, timeout=30_000_000, count=8_000_000)
        if self.stop_reason is None and (self.uc.reg_read(UC_X86_REG_EIP) != RETURN
                                        or self.uc.reg_read(UC_X86_REG_ESP) != sp+8):
            raise RuntimeError('new-week ADV exceeded bounds or ret4 stack mismatch')
        return {'name': name, 'upstream': {'state_requests': previous['state_requests'],
            'loads': previous['resource_loads'], 'week_events': previous['week_events'],
            'week_executed': previous['week_executed'], 'pending_flag': previous['pending_flag'],
            'pending_state': previous['pending_state']},
            'before_ch001': before, 'after_ch001': self.flow_snapshot(),
            'consumed_request': self.new_adv_consumed, 'synthetic_readiness': self.new_inputs,
            'max_frames': self.new_max_frames, 'frames': self.frame_index,
            'commands': self.commands[command_start:], 'loads': self.loads[load_start:],
            'movie_events': self.movie_events, 'state_requests': self.state_requests[request_start:],
            'stop_reason': self.stop_reason, 'active_path': self.active_path,
            'vm_active': self.read(VM+4, 'B'), 'vm_pc': self.read(VM+0x1C), 'vm_wait': self.read(VM+0x20, 'H'),
            'stored_next_task_state': self.read(VM+0x92DC, 'i'),
            'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
            'stub_calls': dict(self.stub_calls), 'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'ch001_completed': self.stop_reason is None and self.read(VM+4, 'B') == 0,
            'workroom_executed': False, 'school_initialized': False,
            'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_new_week_adv_after_actual_shared_week_handoff',
        'additional_native_ranges': [[hex(a), hex(b)] for a, b in NEW_ADV_NATIVE],
        'movie_stub_manifest': [{'va': hex(a), 'meaning': n, 'callee_pop_bytes': p}
                                for a, (n, p) in MOVIE_STUBS.items()],
        'synthetic_movie_inputs': {'skip_key_va': '0x4128f0', 'skip_key_code': 0x39,
                                   'skip_key_callee_pop_bytes': 8, 'mouse_position': 0, 'mouse_buttons': 0},
        'limitations': ['All cases actually execute the prior CH003/Chapter020/021 and state7 in the same CPU.',
            'Task scheduler/constructor handoffs, presentation readiness, drawing/audio/movie are declared boundaries.',
            'Movie original filename/hash is recorded but its visual body is not executed.',
            'CH001 date branches, Chapter022/208 replacement loads, timers, opcode151/91 writes and END are native.',
            'Does not execute workroom/state8, CH002 or school constructors, nor originate from a battle.'],
        'cases': [NewWeekAdvEmulator().run_new_adv('ch001_ch022_ch208_complete'),
                  NewWeekAdvEmulator(new_key_ready=False, new_max_frames=1200).run_new_adv('ch001_key_wait'),
                  NewWeekAdvEmulator(new_ui_ready=False, new_max_frames=200).run_new_adv('ch001_ui_wait'),
                  NewWeekAdvEmulator(new_fade_ready=False, new_max_frames=1200).run_new_adv('ch001_fade_wait')],
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
