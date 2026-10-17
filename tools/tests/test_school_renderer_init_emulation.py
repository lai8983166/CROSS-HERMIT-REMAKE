import json
import unittest
from copy import deepcopy

from tools.school_renderer_init import ROOT
from tools.school_renderer_init_emulation import RendererEmulator, MANAGER
from tools.school_renderer_init_verification import verify_initialization


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


if __name__ == '__main__':
    unittest.main()
