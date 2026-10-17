import json
import unittest
from copy import deepcopy

from tools.school_renderer_init import ROOT, dword
from tools.school_renderer_init_emulation import (
    RendererEmulator, MANAGER, ARENA, initialize, queue_report,
)
from tools.school_renderer_init_verification import verify_initialization, verify_queue


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-renderer-init-native-v1-20261017.json').read_text(encoding='utf-8'))

    def test_full_native_evidence_passes_independent_projection(self):
        self.assertEqual(verify_initialization(self.report)['cases'], 2)

    def test_native_constructor_callee_saves_and_full_buffer(self):
        e = RendererEmulator()
        call = e.call(0x40D7E0)
        self.assertEqual(call['cpu']['EAX'], MANAGER)
        self.assertEqual(len(call['entries']), 2)

    def test_allocator_rejects_undeclared_root_or_size(self):
        e = RendererEmulator()
        with self.assertRaisesRegex(RuntimeError, 'undeclared CRT'):
            e.call(0x56E810, (32768, 1, 0x594E28, 141))

    def test_native_write_and_instruction_guards_refuse_unowned_access(self):
        e = RendererEmulator()
        with self.assertRaisesRegex(RuntimeError, 'forbidden native write'):
            e._write(e.uc, 0, MANAGER+96, 1, 0, None)
        with self.assertRaisesRegex(RuntimeError, 'undeclared renderer native'):
            e.call(0x4144B0)

    def test_scope_inputs_counter_packet_and_caller_tampering_refused(self):
        changes = [lambda r: r.update(GPU_executed=True),
                   lambda r: r['cases'][0]['inputs'].update(device=1),
                   lambda r: r['cases'][0]['stages'][2]['state'].update(counter=0),
                   lambda r: r['cases'][0]['stages'][0]['state'].update(manager_hex='00'*96),
                   lambda r: r['cases'][0]['stages'][1]['call']['entries'][1].update(return_va='0x413505'),
                   lambda r: r['cases'][0]['stages'][2]['call']['visited'].append(0x49E540),
                   lambda r: r['cases'][0]['allocations'][0].update(result=0)]
        for change in changes:
            bad = deepcopy(self.report)
            change(bad)
            with self.assertRaises(ValueError):
                verify_initialization(bad)


class QueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-renderer-init-queue-v1-20261017.json').read_text(encoding='utf-8'))

    def test_all_queue_evidence_matches_independent_full_byte_projection(self):
        checks = verify_queue(self.report)
        self.assertEqual(checks['rectangles'], 4)
        self.assertEqual(checks['clip_probes'], 12)
        self.assertEqual(checks['debug_bodies_executed'], 0)

    def test_replay_original_bodies_matches_archived_queue_evidence(self):
        self.assertEqual(queue_report(), self.report)

    def test_same_layer_link_and_reset_high_watermark(self):
        rows = self.report['insertions']
        self.assertEqual(rows[1]['previous_head'], ARENA)
        self.assertEqual(rows[2]['previous_head'], 0)
        reset = self.report['reset_arena']['state']
        self.assertEqual(dword(bytes.fromhex(reset['manager_hex']), 0x1C), 96)
        self.assertEqual(dword(bytes.fromhex(reset['manager_hex']), 0x30), ARENA)
        self.assertEqual(reset['arena'], rows[-1]['state']['arena'])

    def test_native_reset_clears_dirty_count_but_keeps_high_watermark(self):
        import struct
        e, manager, heads, arena, _ = initialize()
        e.uc.mem_write(MANAGER+0x2C, struct.pack('<I', 123))
        e.uc.mem_write(MANAGER+0x30, struct.pack('<I', ARENA+72))
        e.uc.mem_write(MANAGER+0x1C, struct.pack('<I', 96))
        call = e.call(0x40DC80)
        self.assertEqual(call['cpu']['EAX'], 0)
        self.assertEqual(e.read(MANAGER+0x2C), 0)
        self.assertEqual(e.read(MANAGER+0x30), ARENA)
        self.assertEqual(e.read(MANAGER+0x1C), 96)

    def test_scope_links_packet_padding_reset_and_debug_cpu_tampering_refused(self):
        changes = [lambda r: r.update(retained_VM_advanced=True),
                   lambda r: r['insertions'][1].update(previous_head=0),
                   lambda r: r['insertions'][0].update(packet_pointer=ARENA+1),
                   lambda r: r['insertions'][0]['call']['entries'][-1].update(args=[ARENA, 68]),
                   lambda r: r['insertions'][0]['call']['entries'][-1].update(sp=1),
                   lambda r: r['reset_arena']['state'].update(manager_hex='00'*96),
                   lambda r: r['closed_gate']['call']['cpu'].update(EIP=0x40DD1A),
                   lambda r: r['capacity_probes'][1]['call']['pending'].update(instruction_executed=True),
                   lambda r: r['capacity_probes'][1]['call']['visited'].append(0x40DE74),
                   lambda r: r['clip_probes'][8].update(expected=1)]
        for change in changes:
            bad = deepcopy(self.report)
            change(bad)
            with self.assertRaises(ValueError):
                verify_queue(bad)

    def test_compressed_full_buffers_reject_extra_data_or_forged_hash(self):
        import base64
        changes = [lambda row: row.update(sha256='0'*64),
                   lambda row: row.update(bytes=1),
                   lambda row: row.update(zlib_base64=base64.b64encode(
                       base64.b64decode(row['zlib_base64'])+b'extra').decode('ascii'))]
        for change in changes:
            bad = deepcopy(self.report)
            change(bad['insertions'][0]['state']['arena'])
            with self.assertRaises(ValueError):
                verify_queue(bad)


if __name__ == '__main__':
    unittest.main()
