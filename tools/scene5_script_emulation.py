"""Execute sourced scene-5 script control flow and exit code in isolated x86 memory.

VM dispatch, register/branch instructions, timers, work waits and request initialization
run original instructions. Presentation and world callbacks are declared simulations.
This is not a live scene witness and never authorizes a persistent transaction.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.tactics_exit_emulation import (ExitEmulator, ROOT, TASK, report_text,
                                         SOURCE_SHA256, FUNCTIONS, STUBS)

VM, SCRIPT, WORK, IMPORTS = 0x7D7C28, 0x5000000, 0x6000000, 0x7000000
PROBE = 0x8000000
SCRIPT_SOURCE = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0005.BIN'
SCRIPT_SHA256 = '44ca546b5ea90ec23a4bc7d8dffeac6547a44bfd035383c91983f7c13ae72a52'
# Explicit original function bounds; VM's final ret is at 4D03B6 (then jump-table data).
NATIVE = ((0x454AB0, 0x454AF0), (0x454AF0, 0x454BB0), (0x454BB0, 0x454C40),
          (0x455060, 0x455160), (0x4551C0, 0x455310), (0x4214F0, 0x421540),
          (0x4CE030, 0x4CE060), (0x4CE060, 0x4CE090), (0x4CE090, 0x4CE150),
          (0x4CE460, 0x4CE4B0), (0x4CE4B0, 0x4CE560), (0x4CE560, 0x4CE6E0),
          (0x4CD700, 0x4CD760), (0x4CD8D0, 0x4CDBE0), (0x4CE800, 0x4CE870),
          (0x4CE8F0, 0x4D03B9), (0x4D0790, 0x4D0860), (0x4CDF80, 0x4CE030),
          (0x4C1E20, 0x4C1EB0), (0x4C1EB0, 0x4C1F40), (0x4C1F40, 0x4C1FC0),
          (0x4C2060, 0x4C2120), (0x4C23F0, 0x4C2500), (0x4C2610, 0x4C2670),
          (0x4C2670, 0x4C2730), (0x4CCB90, 0x4CCE20), (0x4C4210, 0x4C4280),
          (0x4C5260, 0x4C52A0), (0x4C6820, 0x4C6860), (0x4C5430, 0x4C54C0),
          (0x4C5BC0, 0x4C5D00), (0x42E340, 0x42E470),
          (0x42FBE0, 0x42FC60), (0x42FC60, 0x42FCD0), (0x496D80, 0x496DC0),
          (0x496DC0, 0x496DF0), (0x496DF0, 0x496E30), (0x496E30, 0x496E70),
          (0x497720, 0x4977A0), (0x42D960, 0x42D9F0), (0x42D9F0, 0x42DA80),
          (0x42DCF0, 0x42DDE0), (0x42E9E0, 0x42EBC0), (0x42F120, 0x42F1E0),
          (0x42F2D0, 0x42F460), (0x4D0ED0, 0x4D0FB0), (0x4D0FB0, 0x4D1060))
# Remaining presentation stubs return their third dispatcher argument.
# BORDDISP runs native code: it replaces the third argument with 0/1 from mode.
UI_HANDLERS = {0x4C4B80: 'text', 0x4C61C0: 'board_pack_on', 0x4C5EA0: 'board_on',
               0x4C4DC0: 'text_active', 0x4C4EB0: 'text_clear', 0x4C6330: 'board_pack_off',
               0x4C5500: 'adv_mode', 0x4C5590: 'all_off', 0x4C64D0: 'character_set',
               0x4C5D40: 'board_change'}
EXTERNAL = {**{va: (name, 12) for va, name in UI_HANDLERS.items()},
            0x4CD060: ('ui_ready', 4), 0x4CD120: ('ui_ready', 4),
            0x4CCE20: ('key_ready', 4), 0x4C7AB0: ('ui_ready', 0),
            0x4CD350: ('text_or_key_ready', 4),
            0x4CC7D0: ('board_visibility', 4), 0x4CC8D0: ('board_visibility', 4),
            0x4C76B0: ('presentation_fade', 4),
            0x499560: ('world_animation', 0), 0x497DF0: ('world_animation_stop', 0),
            0x4997D0: ('world_query', 0), 0x4987C0: ('world_request_112', 0),
            0x4988D0: ('world_request_130', 0),
            0x4978C0: ('world_fade_in', 0), 0x497980: ('start_script_work_fade', 0),
            0x4D29E0: ('draw_vm_overlay', 64), 0x4CA1B0: ('draw_vm_layer', 0),
            0x4C99E0: ('draw_vm_layer', 0), 0x4CD4D0: ('draw_vm_object', 8),
            0x4C7190: ('draw_vm_board', 0), 0x4C7770: ('draw_vm_fade', 0),
            0x4CBA60: ('draw_vm_resource', 0), 0x40D120: ('audio_stop', 4),
            0x42B2D0: ('debug_print', 0),
            IMPORTS: ('lstrcmpA', 8), IMPORTS+0x10: ('GetTickCount', 0)}
OPCODE_HANDLERS = {8: 0x4C23F0, 11: 0x4C2610, 12: 0x4C2670, 24: 0x4C5BC0,
                   112: 0x42DCF0, 117: 0x42D960, 118: 0x42D9F0, 130: 0x42E340,
                   136: 0x42E9E0, 142: 0x42F120, 146: 0x42F2D0,
                   147: 0x4D0ED0, 148: 0x4D0FB0, 166: 0x42FBE0, 167: 0x42FC60}


class Scene5Emulator(ExitEmulator):
    def __init__(self, *, ui_ready=True, key_ready=True, work_delay=2, release_work=True):
        super().__init__()
        if not 1 <= work_delay <= 60:
            raise ValueError('work_delay must be 1..60 synthetic frames')
        self._function_ranges += NATIVE
        self._stubs.update(EXTERNAL)
        # Original initializer/dispatcher callers use this literal VM address.
        self.uc.mem_write(VM, bytes(0x9400))
        for base, size in ((SCRIPT, 0x10000), (WORK, 0x10000), (IMPORTS, 0x1000)):
            self.uc.mem_map(base, size)
        self.source = SCRIPT_SOURCE.read_bytes()
        if hashlib.sha256(self.source).hexdigest() != SCRIPT_SHA256:
            raise ValueError('scene script differs from audited source')
        self.uc.mem_write(SCRIPT, self.source)
        self.write(TASK+0x60, VM)
        self.write(TASK+0x64, SCRIPT)
        self.write(0x7A49F8, WORK)
        self.write(0x7A4A00, 0)  # Disable VM END music path; audio is simulated.
        self.write(0x592278, IMPORTS)
        self.write(0x592210, IMPORTS+0x10)
        self.write(0x7F4488, 5, 'h')
        self.write(0x7A417C, 0, 'h')
        self.write(0x7A4184, 0, 'h')
        self.external.update(ui_ready=ui_ready, key_ready=key_ready,
                             work_delay=work_delay, release_work=release_work,
                             world_query_value=0)
        self.frame_index = -1
        self.external.pop('vm_busy')  # The VM runs native code, never the old VM stub.
        self.work_due = None
        self.commands = []
        self.callbacks = []
        self.world_requests = []
        self.handler_entries = []
        self.probe_bytes = None

    def _stub_return(self, result, pop_bytes):
        sp = self.uc.reg_read(UC_X86_REG_ESP)
        target = self.read(sp)
        self.uc.reg_write(UC_X86_REG_EAX, result & 0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+pop_bytes)
        self.uc.reg_write(UC_X86_REG_EIP, target)

    def _hook(self, uc, address, size, user):
        if (address == 0x4CE8F0 and self.read(VM+4, 'B')
                and not self.read(VM+0x93E2, 'B') and self.read(VM+0x20, 'H') == 0):
            instruction = self.read(VM+0x10) + self.read(VM+0x1C)
            segment_base, segment = SCRIPT, self.source
            if self.probe_bytes is not None and PROBE <= instruction < PROBE+len(self.probe_bytes):
                segment_base, segment = PROBE, self.probe_bytes
            if not segment_base <= instruction < segment_base+len(segment)-3:
                raise RuntimeError('VM instruction outside sourced script')
            opcode, advance = struct.unpack('<HH', uc.mem_read(instruction, 4))
            if advance < 4 or instruction+advance > segment_base+len(segment):
                raise RuntimeError('malformed sourced instruction')
            self.commands.append({'frame': self.frame_index, 'offset': instruction-segment_base,
                                  'opcode': opcode, 'advance': advance})
        if address in OPCODE_HANDLERS.values():
            self.handler_entries.append({'frame': self.frame_index,
                                         'opcode': self.read(VM+0x22, 'H'),
                                         'handler_va': hex(address)})
        # Original opcode handlers and the dispatcher take priority over stubs.
        if any(start <= address < end for start, end in self._function_ranges):
            return super()._hook(uc, address, size, user)
        if address in EXTERNAL:
            name, pop = EXTERNAL[address]
            self.stub_calls[name] += 1
            sp = uc.reg_read(UC_X86_REG_ESP)
            result = 0
            if address in UI_HANDLERS:
                result = self.read(sp+12)
            elif name in ('ui_ready', 'key_ready'):
                result = int(self.external[name])
            elif name == 'text_or_key_ready':
                result = int(self.external['ui_ready'] or self.external['key_ready'])
            elif name == 'world_query':
                result = self.external['world_query_value']
            elif name in ('world_animation', 'world_animation_stop', 'world_fade_in',
                          'start_script_work_fade'):
                self.work_due = self.frame_index+self.external['work_delay']
                self.external['script_work_busy'] = True
            elif name == 'world_request_112':
                self.world_requests.append(list(struct.unpack('<III', uc.mem_read(sp+4, 12))))
            elif name == 'world_request_130':
                self.world_requests.append(list(struct.unpack('<IIII', uc.mem_read(sp+4, 16))))
            elif name == 'lstrcmpA':
                a, b = self.read(sp+4), self.read(sp+8)
                for i in range(256):
                    left, right = self.read(a+i, 'B'), self.read(b+i, 'B')
                    if left != right or left == 0:
                        result = left-right
                        break
                else:
                    raise RuntimeError('unbounded lstrcmpA input')
            self._stub_return(result, pop)
            return
        return super()._hook(uc, address, size, user)

    def request(self, selector=2, sub=2):
        if (selector, sub) not in ((2, 2), (5, 5), (8, 8), (11, 11), (14, 8), (14, 14)):
            raise ValueError('not a sourced terminal selector/sub')
        self.write(TASK+0x38, 5)  # Declared synthetic battle phase; not script completion.
        self.call(0x454AF0, (selector, sub))
        return self.snapshot()

    def snapshot(self):
        return {**super().snapshot(), 'execute_vm': self.read(TASK+0x48),
                'result_selector': self.read(TASK+0x174),
                'vm_active': self.read(VM+4, 'B'), 'vm_pc': self.read(VM+0x1C),
                'vm_wait_state': self.read(VM+0x20, 'H'),
                'vm_work_wait': self.read(VM+0x92E0, 'B'),
                'register': self.read(WORK, 'B'), 'register_request': self.read(WORK+1, 'B'),
                'variable0': self.read(VM+0x3C)}

    def frame(self):
        self.frame_index += 1
        if self.work_due is not None and self.frame_index >= self.work_due and self.external['release_work']:
            self.call(0x4CDF80, receiver=VM)
            self.external['script_work_busy'] = False
            self.callbacks.append({'frame': self.frame_index, 'va': '0x4cdf80',
                                   'evidence_kind': 'synthetic_work_completion_callback'})
            self.work_due = None
        return super().frame()


def replay(name='terminal_sub2', *, selector=2, sub=2, max_frames=400, **external):
    if not 1 <= max_frames <= 2000:
        raise ValueError('max_frames must be 1..2000')
    emulator = Scene5Emulator(**external)
    initial = emulator.request(selector, sub)
    preflight = list(emulator.commands)
    states = []
    for _ in range(max_frames):
        frame = emulator.frame()
        states.append(frame)
        if frame['transition_function_return']:
            break
    return {'name': name, 'selector_argument': selector, 'script_sub': sub,
            'synthetic_external_inputs': emulator.external, 'initial_state': initial,
            'preflight_commands': preflight, 'commands': emulator.commands[len(preflight):],
            'external_callbacks': emulator.callbacks, 'states': states,
            'handler_entries': emulator.handler_entries,
            'stub_calls': dict(emulator.stub_calls),
            'visited_original_addresses': [hex(a) for a in sorted(emulator.visited)],
            'transition_returned': bool(states[-1]['transition_function_return']),
            'state11_observed': False, 'authorizes_persistent_write': False}


def dispatch_probe(opcode, *, source_offset=None, cells=(0x20000007, 0x20000010, 0x20000028)):
    """Run one dispatcher step; artificial bytes are explicitly separate from source."""
    emulator = Scene5Emulator()
    if source_offset is None:
        emulator.probe_bytes = struct.pack('<HH', opcode, 4+4*len(cells))+struct.pack(
            '<'+'I'*len(cells), *cells)
        emulator.uc.mem_map(PROBE, 0x1000)
        emulator.uc.mem_write(PROBE, emulator.probe_bytes)
        code = PROBE
        provenance = {'evidence_kind': 'synthetic_instruction',
                      'instruction_hex': emulator.probe_bytes.hex()}
    else:
        raw_opcode, advance = struct.unpack_from('<HH', emulator.source, source_offset)
        if raw_opcode != opcode:
            raise ValueError('source opcode mismatch')
        code = SCRIPT+source_offset
        provenance = {'evidence_kind': 'sourced_instruction_with_synthetic_vm_state',
                      'source_offset': source_offset,
                      'instruction_hex': emulator.source[source_offset:source_offset+advance].hex()}
    emulator.write(VM+4, 1, 'B')
    emulator.write(VM+0x10, code)
    emulator.write(VM+0x92E1, 1, 'B')  # Suppress presentation for this isolated dispatch probe.
    emulator.write(VM+0x3C, 60)  # Explicit variable0 input, never inferred from the script.
    busy = emulator.call(0x4CE8F0, receiver=VM)
    return {**provenance, 'opcode': opcode, 'synthetic_variable0': 60,
            'handler_entries': emulator.handler_entries,
            'vm_return': busy, 'vm_wait_state': emulator.read(VM+0x20, 'H'),
            'vm_work_wait': emulator.read(VM+0x92E0, 'B'),
            'vm_temporaries': [emulator.read(VM+offset) for offset in (0x9250, 0x9254, 0x9258, 0x925C)],
            'world_requests': emulator.world_requests, 'authorizes_persistent_write': False}


def report():
    effective_stubs = {va: spec for va, spec in {**STUBS, **EXTERNAL}.items()
                       if not any(start <= va < end for start, end in FUNCTIONS+NATIVE)}
    return {'schema_version': 2, 'evidence_kind': 'original_vm_control_with_synthetic_callbacks',
            'source_image_sha256': SOURCE_SHA256, 'script_sha256': SCRIPT_SHA256,
            'native_function_ranges': [[hex(a), hex(b)] for a, b in FUNCTIONS+NATIVE],
            'effective_stub_manifest': [{'va': hex(va), 'meaning': name, 'callee_pop_bytes': pop}
                                        for va, (name, pop) in effective_stubs.items()],
            'limitations': ['Scene event selection and initial battle phase are synthetic.',
                            'UI opcode bodies, rendering, audio and world callbacks are simulated.',
                            '4CDF80 completion callbacks are supplied externally; live caller unresolved.',
                            'No full 4539B0 loop or state11 dispatch; no persistent writes.'],
            'dispatch_probes': [dispatch_probe(112, source_offset=0x2AE8),
                                dispatch_probe(117, source_offset=0x540),
                                dispatch_probe(118, source_offset=0x76C),
                                dispatch_probe(130, source_offset=0x2A68),
                                dispatch_probe(147), dispatch_probe(148)],
            'cases': [replay('terminal_sub2'),
                      replay('terminal_selector14_sub8', selector=14, sub=8),
                      replay('sub2_work_completion_missing', max_frames=20, release_work=False),
                      replay('sub2_key_missing', max_frames=80, key_ready=False),
                      replay('sub2_ui_missing', max_frames=30, ui_ready=False)],
            'authorizes_persistent_write': False}


def godot_fixture(result):
    case = next(c for c in result['cases'] if c['name'] == 'terminal_sub2')
    index = next(i for i, state in enumerate(case['states']) if state['script_phase'] == 5)
    return {'schema_version': 1, 'evidence_kind': result['evidence_kind'],
            'source_report_sha256': hashlib.sha256(report_text(result).encode('utf-8')).hexdigest(),
            'script_sha256': SCRIPT_SHA256, 'source_image_sha256': SOURCE_SHA256,
            'script': 'T0005.BIN', 'script_sub': case['script_sub'],
            'limitations': result['limitations'],
            'preflight_commands': case['preflight_commands'], 'commands': case['commands'],
            'external_callbacks': case['external_callbacks'],
            'handoff_frame': index, 'initial_state': case['states'][index],
            'states': case['states'][index+1:],
            'state11_observed': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--godot-out', type=Path)
    args = parser.parse_args()
    if args.godot_out and args.out.resolve() == args.godot_out.resolve():
        parser.error('report and fixture must have different paths')
    for path in (args.out, args.godot_out):
        if path and path.exists():
            parser.error('refusing to overwrite existing output')
    result = report()
    with args.out.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(report_text(result))
    if args.godot_out:
        with args.godot_out.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(report_text(godot_fixture(result)))


if __name__ == '__main__':
    main()
