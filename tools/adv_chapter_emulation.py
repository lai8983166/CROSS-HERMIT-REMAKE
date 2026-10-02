"""Execute CH003 -> Chapter020 -> Chapter021 and native ADV completion.

Join and VM/loader instructions are native; presentation readiness is explicit.
This starts from a synthetic date/roster, not a battle or school witness.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.roster_join_emulation import RosterJoinEmulator
from tools.adv_route_emulation import NATIVE as ROUTE_NATIVE, RESOURCES, AdvRouteEmulator
from tools.adv_return_state_emulation import FUNCTIONS as ADV_NATIVE, CONTROLLER, CH003
from tools.scene5_script_emulation import Scene5Emulator, VM, SCRIPT
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, STACK, RETURN, TASK, report_text

PRESENTATION = {0x4C5810: 'background_set', 0x4C5FC0: 'board_off',
    0x4C44D0: 'screen_transition', 0x4C45C0: 'voice', 0x4C4950: 'sound',
    0x4C59A0: 'rectangle', 0x4C6AA0: 'character_change',
    0x4C6400: 'board_pack_change'}
TASK_STUBS = {0x4D0860: ('adv_setup', 0),
    0x422360: ('task_yield', 4), 0x4D1A40: ('task_destructor', 0),
    0x4CD1E0: ('ui_ready', 4), 0x4DB270: ('chapter_fade_ready', 0),
    0x4DB010: ('chapter_fade_install', 0), 0x4DB120: ('chapter_fade_release', 0),
    0x4CC3E0: ('character_effect_show', 4), 0x4CC500: ('character_effect_hide', 4)}
CHAPTER_NATIVE = ((0x4C66E0, 0x4C680C),)


class AdvChapterEmulator(RosterJoinEmulator):
    def __init__(self, *, difficulty=0, already_available=False, ui_ready=True,
                 key_ready=True, fade_ready=True, max_frames=6000):
        super().__init__(difficulty=difficulty, already_available=already_available)
        if any(type(v) is not bool for v in (ui_ready, key_ready, fade_ready)) \
                or type(max_frames) is not int or not 1 <= max_frames <= 6000:
            raise ValueError('outside declared chapter readiness/frame inputs')
        self._function_ranges += ROUTE_NATIVE + ADV_NATIVE + CHAPTER_NATIVE
        self._stubs.update(RESOURCES)
        self._stubs.update(TASK_STUBS)
        self._stubs.update({a: (n, 12) for a, n in PRESENTATION.items()})
        self.external.update(ui_ready=ui_ready, key_ready=key_ready, fade_ready=fade_ready)
        self.max_frames = max_frames
        self.frame_index = -1
        self.commands = []
        self.loads = []
        self.state_requests = []
        self.stop_reason = None
        self.active_path = None
        self.write(TASK, 0x5C306C)  # Explicit ADV vtable input, constructor not executed.
        self.write(0x7A4A00, CONTROLLER)
        self.write(VM+0x92E1, 1, 'B')  # Suppress simulated drawing only.
        for index, pointer in enumerate((0x3100000, 0x3100010)):
            if index == 0:
                self.uc.mem_map(pointer, 0x1000)
            self.write(0x592234+index*4, pointer)
            self._stubs[pointer] = ('critical_section', 4)

    def _resource(self, pointer):
        name = AdvRouteEmulator._path(self, pointer)
        if name not in ('ch003.ybc', 'chapter020.ybc', 'chapter021.ybc'):
            raise RuntimeError('resource outside declared chapter chain')
        source = (CH003.parent / name).read_bytes()
        if len(source) > 0x10000:
            raise RuntimeError('chapter exceeds fixed bounded resource allocation')
        return name, source

    def _hook(self, uc, address, size, user):
        if address == 0x4CE8F0:
            self.frame_index += 1
            if self.frame_index >= self.max_frames:
                self.stop_reason = 'bounded_pending_chapter'
                uc.emu_stop()
                return
            count = len(self.commands)
            result = Scene5Emulator._hook(self, uc, address, size, user)
            if len(self.commands) > count:
                self.commands[-1]['path'] = self.active_path
            return result
        if address == 0x439E30:
            self.state_requests.append({'va': hex(address),
                'state': self.read(uc.reg_read(UC_X86_REG_ESP)+4, 'i')})
        if any(a <= address < b for a, b in ROUTE_NATIVE + ADV_NATIVE + CHAPTER_NATIVE):
            # Bypass inherited historical stop/stub policies ONLY for the
            # sourced loader, VM and task bodies explicitly enabled here.
            return ExitEmulator._hook(self, uc, address, size, user)
        if any(a <= address < b for a, b in self._function_ranges):
            return super()._hook(uc, address, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if address in RESOURCES:
            name, pop = RESOURCES[address]
            self.stub_calls[name] += 1
            value = 0
            if name == 'resource_key':
                value = self.read(sp+4)
                AdvRouteEmulator._path(self, value)
            elif name in ('resource_size', 'resource_bytes'):
                path, source = self._resource(self.read(sp+4))
                value = len(source) if name == 'resource_size' else SCRIPT
                if name == 'resource_bytes':
                    self.loads.append({'path': path, 'source_sha256': hashlib.sha256(source).hexdigest()})
                    self.source = source
                    self.uc.mem_write(SCRIPT, source)
                    self.active_path = path
            self._stub_return(value, pop)
            return
        if address in PRESENTATION:
            self.stub_calls[PRESENTATION[address]] += 1
            self._stub_return(self.read(sp+12), 12)
            return
        if address in TASK_STUBS:
            name, pop = TASK_STUBS[address]
            self.stub_calls[name] += 1
            result = int(self.external['ui_ready']) if name == 'ui_ready' else \
                     int(self.external['fade_ready']) if name == 'chapter_fade_ready' else 0
            self._stub_return(result, pop)
            return
        return super()._hook(uc, address, size, user)

    def run(self, name):
        before = self.roster_snapshot()
        path = TASK+0xA0000
        self.uc.mem_write(path, b'Data\\Adv\\dat\\CH003.ybc\0')
        self.call(0x4CE210, (path, 7), receiver=VM)
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, TASK)
        self.uc.emu_start(0x4D1A80, RETURN, timeout=30_000_000, count=8_000_000)
        if self.stop_reason is None and (self.uc.reg_read(UC_X86_REG_EIP) != RETURN
                                        or self.uc.reg_read(UC_X86_REG_ESP) != sp+8):
            raise RuntimeError('chapter task exceeded bounds or ret4 stack mismatch')
        return {'name': name, 'before': before, 'after': self.roster_snapshot(),
            'synthetic_readiness': {k: self.external[k] for k in ('ui_ready', 'key_ready', 'fade_ready')},
            'difficulty': self.read(0x7A528C, 'h'), 'max_frames': self.max_frames,
            'commands': self.commands, 'loads': self.loads, 'join_entries': self.join_entries,
            'stop_reason': self.stop_reason, 'frames': self.frame_index,
            'active_path': self.active_path, 'vm_active': self.read(VM+4, 'B'),
            'vm_pc': self.read(VM+0x1C), 'vm_wait': self.read(VM+0x20, 'H'),
            'stored_next_task_state': self.read(VM+0x92DC, 'i'), 'state_requests': self.state_requests,
            'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
            'stub_calls': dict(self.stub_calls), 'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'chapter_completed': self.stop_reason is None and self.read(VM+4, 'B') == 0,
            'school_initialized': False, 'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_adv_chapter_chain_with_synthetic_presentation_readiness',
        'additional_native_ranges': [[hex(a), hex(b)] for a, b in ROUTE_NATIVE + ADV_NATIVE + CHAPTER_NATIVE],
        'presentation_stub_manifest': [{'va': hex(a), 'meaning': n, 'callee_pop_bytes': 12}
                                       for a, n in PRESENTATION.items()],
        'task_stub_manifest': [{'va': hex(a), 'meaning': n, 'callee_pop_bytes': p}
                              for a, (n, p) in TASK_STUBS.items()],
        'limitations': ['Date4/5, roster/templates/equipment and task/controller initial state are synthetic.',
            'Resource I/O supplies exact CH003/Chapter020/Chapter021 bytes using a reusable fixed allocation.',
            'UI/audio opcode bodies and readiness, ADV setup, task yield/destruction and locks are simulated.',
            'Native VM dispatch/branches/timers, replacement loading, roster join, actual END and 4D0750 cleanup wrapper are executed.',
            'State7/week start, CH001 and school tasks are not executed; this does not originate from a battle.'],
        'cases': [AdvChapterEmulator().run('chapter020_021_complete'),
                  AdvChapterEmulator(key_ready=False, max_frames=200).run('key_wait_blocks_completion'),
                  AdvChapterEmulator(ui_ready=False, max_frames=200).run('ui_wait_blocks_completion'),
                  AdvChapterEmulator(fade_ready=False, max_frames=600).run('fade_wait_blocks_completion')],
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
