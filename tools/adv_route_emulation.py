"""Execute original CH003 month/week dispatch and chapter replacement loading.

Stop before chapter execution or an unresolved roster opcode; never fake END.
"""
import argparse
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.adv_return_state_emulation import AdvReturnEmulator, VM, FILE, CONTROLLER, CH003
from tools.scene5_script_emulation import EXTERNAL
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, STACK, RETURN, TASK, report_text

NATIVE = ((0x4CE090, 0x4CE210), (0x4CE210, 0x4CE460), (0x4CE6E0, 0x4CE730), (0x4CD7B0, 0x4CD820),
          (0x4C2190, 0x4C22B0), (0x4CE800, 0x4D03B9), (0x4CD8D0, 0x4CDBE0),
          (0x4C1E20, 0x4C1FC0), (0x4C2060, 0x4C2120), (0x4C23F0, 0x4C2500), (0x4C2610, 0x4C2670),
          (0x4D0C80, 0x4D0DA0))
RESOURCES = {0x4500B0: ('resource_key', 4), 0x42ABC0: ('resource_size', 0),
             0x42AE20: ('resource_bytes', 0), 0x428AD0: ('resource_free', 0),
             0x41E500: ('audio_stop', 0)}


class AdvRouteEmulator(AdvReturnEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE
        self._stubs.update(EXTERNAL)
        self._stubs.update(RESOURCES)
        self.commands = []
        self.loads = []
        self.stop_reason = None
        self.loaded = {'ch003.ybc': (FILE, CH003.read_bytes())}
        self._frames = 0

    def _return(self, value, pop):
        sp = self.uc.reg_read(UC_X86_REG_ESP)
        self.uc.reg_write(UC_X86_REG_EAX, value)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+pop)
        self.uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def _path(self, pointer):
        raw = bytes(self.uc.mem_read(pointer, 256)).split(b'\0')[0]
        if len(raw) == 256:
            raise RuntimeError('unbounded resource path')
        parts = [p.lower() for p in raw.decode('ascii').replace('\\', '/').split('/') if p]
        if len(parts) != 4 or parts[:3] != ['data', 'adv', 'dat']:
            raise RuntimeError('resource outside declared ADV directory')
        return parts[-1]

    def _resource(self, pointer):
        name = self._path(pointer)
        if name not in ('ch003.ybc', 'chapter020.ybc', 'chapter028.ybc', 'chapter097.ybc'):
            raise RuntimeError('resource outside declared router cases')
        if name not in self.loaded:
            payload = (CH003.parent / name).read_bytes()
            if len(payload) > 0x10000:
                raise RuntimeError('resource exceeds bounded allocation')
            address = FILE+len(self.loaded)*0x10000
            self.uc.mem_write(address, payload)
            self.loaded[name] = (address, payload)
        return name, self.loaded[name]

    def _hook(self, uc, address, size, user):
        if address == 0x4CE8F0:
            self._frames += 1
            if self._frames > 128:
                raise RuntimeError('router frame budget exceeded')
            pointer = self.read(VM+0xC)
            name, (base, source) = next((n, v) for n, v in self.loaded.items() if v[0] == pointer)
            offset = self.read(VM+0x10)+self.read(VM+0x1C)-base
            if not 0 <= offset <= len(source)-4:
                raise RuntimeError('instruction outside loaded original resource')
            opcode, advance = struct.unpack_from('<HH', source, offset)
            if name != 'ch003.ybc':
                self.stop_reason = 'chapter_execution_boundary'
                uc.emu_stop()
                return
            if opcode not in (8, 11, 15, 19, 90):
                self.stop_reason = 'unresolved_router_world_opcode'
                self.commands.append({'path': name, 'offset': offset, 'opcode': opcode, 'executed': False})
                uc.emu_stop()
                return
            if advance < 4 or offset+advance > len(source):
                raise RuntimeError('malformed sourced instruction')
            self.commands.append({'path': name, 'offset': offset, 'opcode': opcode, 'executed': True})
        if address == 0x439E30:
            self.events.append({'kind': 'state_request', 'state': self.read(uc.reg_read(UC_X86_REG_ESP)+4)})
        if any(a <= address < b for a, b in self._function_ranges):
            return ExitEmulator._hook(self, uc, address, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if address in RESOURCES:
            name, pop = RESOURCES[address]
            self.stub_calls[name] += 1
            value = 0
            if name == 'resource_key':
                value = self.read(sp+4)
                self._path(value)
            elif name in ('resource_size', 'resource_bytes'):
                path, (base, source) = self._resource(self.read(sp+4))
                value = len(source) if name == 'resource_size' else base
                if name == 'resource_bytes':
                    self.loads.append({'path': path, 'source_sha256': hashlib.sha256(source).hexdigest()})
            self._return(value, pop)
            return
        if address in EXTERNAL:
            name, pop = EXTERNAL[address]
            self.stub_calls[name] += 1
            self._return(0, pop)  # Only drawing/debug entries are reached by CH003.
            return
        return ExitEmulator._hook(self, uc, address, size, user)

    def run(self, name, month, week, next_state):
        if (month, week, next_state) not in ((4, 5, 7), (5, 3, 7), (15, 5, 18), (6, 5, 7), (6, 3, 7), (4, 0, 7)):
            raise ValueError('outside declared original-router probes')
        self.write(0x7A528E, month, 'h')
        self.write(0x7A5290, week, 'h')
        path = TASK+0xA0000
        self.uc.mem_write(path, b'Data\\Adv\\dat\\CH003.ybc\0')
        self.call(0x4CE210, (path, next_state), receiver=VM)
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, TASK)
        self.uc.emu_start(0x4D1A80, RETURN, timeout=10_000_000, count=2_000_000)
        if self.stop_reason is None and (self.uc.reg_read(UC_X86_REG_EIP) != RETURN
                                        or self.uc.reg_read(UC_X86_REG_ESP) != sp+8):
            raise RuntimeError('ADV task exceeded bounds or ret4 stack mismatch')
        pointer = self.read(VM+0xC)
        active_path, (base, _) = next((n, v) for n, v in self.loaded.items() if v[0] == pointer)
        return {'name': name, 'synthetic_month': month, 'synthetic_week': week, 'loader_next_state': next_state,
                'commands': self.commands, 'resource_loads': self.loads, 'stop_reason': self.stop_reason,
                'active_path': active_path, 'pc': self.read(VM+0x1C), 'active': self.read(VM+4, 'B'),
                'stored_next_task_state': self.read(VM+0x92DC), 'state_requests': self.events,
                'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
                'stub_calls': dict(self.stub_calls), 'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'chapter_body_executed': False, 'school_initialized': False,
                'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
            'source_ch003_sha256': hashlib.sha256(CH003.read_bytes()).hexdigest(),
            'evidence_kind': 'native_adv_router_and_resource_initialization',
            'additional_native_ranges': [[hex(a), hex(b)] for a, b in NATIVE],
            'resource_stub_manifest': [{'va': hex(a), 'meaning': name, 'callee_pop_bytes': pop}
                                       for a, (name, pop) in RESOURCES.items()],
            'limitations': ['Month/week and task/controller inputs are synthetic.',
                            'Resource I/O supplies exact source bytes; setup/cleanup, drawing and audio are simulated.',
                            'Stops before chapter body or unresolved roster opcodes144/145, never injects END.',
                            '4/0 is an explicit invalid-date control probe, not a supported gameplay case.',
                            'State7, CH001 and school tasks are not executed.'],
            'cases': [AdvRouteEmulator().run('april_week5', 4, 5, 7),
                      AdvRouteEmulator().run('may_week3', 5, 3, 7),
                      AdvRouteEmulator().run('special_final_week', 15, 5, 18),
                      AdvRouteEmulator().run('valid_no_chapter_week', 6, 5, 7),
                      AdvRouteEmulator().run('router_world_side_effect_boundary', 6, 3, 7),
                      AdvRouteEmulator().run('invalid_week0_control', 4, 0, 7)],
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
