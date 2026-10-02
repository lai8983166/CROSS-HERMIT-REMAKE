"""Audit ADV's next-task field with original loader and task-body instructions.

VM completion is an explicit synthetic input; CH003 and school are not executed.
"""
import argparse
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE, SOURCE_SHA256, TASK, report_text

VM, FILE, CONTROLLER = 0x7D7C28, TASK+0x40000, TASK+0x80000
CH003 = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT/CH003.YBC'
FUNCTIONS = ((0x4CE560, 0x4CE6E0), (0x4CD700, 0x4CD75B),
             (0x4D1A80, 0x4D1B37), (0x439E30, 0x439EF0))


class AdvReturnEmulator(ExitEmulator):
    def __init__(self, *, vm_busy=False):
        super().__init__(vm_busy=vm_busy)
        self._function_ranges = FUNCTIONS
        self._stubs.update({0x4D0860: ('adv_setup', 0), 0x4D0750: ('adv_cleanup', 0),
                            0x422360: ('task_yield', 4), 0x4D1A40: ('task_destructor', 0)})
        self.events = []
        self.bounded_stop = False
        self.frame_count = 0
        self.uc.mem_write(FILE, CH003.read_bytes())
        self.write(VM+0xC, FILE)
        self.write(VM+0x92DC, 7)
        self.write(TASK, 0x5C306C)  # Original ADV vtable, task construction not executed.
        self.write(0x7A4A00, CONTROLLER)
        for index, pointer in enumerate((0x3100000, 0x3100010)):
            if index == 0:
                self.uc.mem_map(pointer, 0x1000)
            self.write(0x592234+index*4, pointer)
            self._stubs[pointer] = ('critical_section', 4)

    def _hook(self, uc, address, size, data):
        if address == 0x4CE8F0:
            self.frame_count += 1
            if self.frame_count > 4:
                self.bounded_stop = True
                uc.emu_stop()
                return
        if address == 0x439E30:
            self.events.append({'kind': 'state_request',
                                'state': self.read(uc.reg_read(UC_X86_REG_ESP)+4, 'i')})
        super()._hook(uc, address, size, data)

    def run(self, name, next_state):
        # Same real code entry irrespective of the next-task value.
        self.call(0x4CE560, (0, next_state & 0xFFFFFFFF), receiver=VM)
        initialized = {'next_task_state': self.read(VM+0x92DC, 'i'),
                       'code_file_offset': self.read(VM+0x10)-FILE,
                       'string_file_offset': self.read(VM+0x14)-FILE,
                       'text_file_offset': self.read(VM+0x18)-FILE,
                       'pc': self.read(VM+0x1C), 'active': self.read(VM+4, 'B'),
                       'registers': [self.read(VM+0x3C+i*4) for i in range(50)]}
        try:
            self.call(0x4D1A80, (0,))
        except RuntimeError:
            if not self.bounded_stop or self.uc.reg_read(UC_X86_REG_EIP) != 0x4CE8F0:
                raise
        return {'name': name, 'loader_parameter': next_state,
                'synthetic_initial_next_task_state': 7, 'synthetic_vm_busy': self.external['vm_busy'],
                'initialized': initialized, 'state_requests': self.events,
                'pending_flag': self.read(CONTROLLER+0x2C),
                'pending_state': self.read(CONTROLLER+0x30),
                'bounded_stop': self.bounded_stop, 'stub_calls': dict(self.stub_calls),
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'adv_script_executed': False, 'school_task_executed': False,
                'live_witness': False, 'authorizes_persistent_write': False}


def report():
    image = SOURCE.read_bytes()
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
            'source_ch003_sha256': hashlib.sha256(CH003.read_bytes()).hexdigest(),
            'evidence_kind': 'original_x86_with_synthetic_vm_completion',
            'function_ranges': [[hex(a), hex(b)] for a, b in FUNCTIONS],
            'state6_dispatch_target': hex(struct.unpack_from('<I', image, 0x49E4D3-0x400000+6*4)[0]),
            'adv_task_body_vtable_entry': hex(struct.unpack_from('<I', image, 0x5C306C-0x400000)[0]),
            'next_task_field_va': hex(VM+0x92DC),
            'limitations': ['CH003 instructions and school constructors are not executed.',
                            'VM completion, ADV setup/cleanup, task yield/destruction and locks are stubbed.',
                            'The task/vtable and controller workspace are synthetic inputs.',
                            'State6 dispatch/constructor are inspected as source operands, not executed.'],
            'cases': [AdvReturnEmulator().run('ordinary_next7', 7),
                      AdvReturnEmulator().run('special_next18', 18),
                      AdvReturnEmulator().run('no_next_state', -1),
                      AdvReturnEmulator().run('child_preserves_next_state', 0x7F),
                      AdvReturnEmulator(vm_busy=True).run('busy_vm_no_next_request', 18)],
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
