"""Native ADV loader parameter is a task state, not a bytecode subroutine."""
import hashlib
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.adv_return_state_emulation import report, ROOT, SOURCE, CH003
    from tools.tactics_exit_emulation import report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class AdvReturnStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_native_report_reexecutes_exactly(self):
        path = ROOT / 'analysis/adv-return-state-v1-20261002.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.report))
        self.assertNotIn(b'\r', path.read_bytes())
        self.assertEqual(hashlib.sha256(CH003.read_bytes()).hexdigest(), self.report['source_ch003_sha256'])

    def test_every_parameter_initializes_same_flat_code_entry(self):
        for case in self.cases.values():
            state = case['initialized']
            self.assertEqual((state['code_file_offset'], state['string_file_offset'], state['text_file_offset']),
                             (0x14, 0x5D4, 0xCC4))
            self.assertEqual((state['pc'], state['active'], state['registers']), (0, 1, [0]*50))
        self.assertEqual(self.report['next_task_field_va'], '0x7e0f04')

    def test_original_task_body_requests_loaded_next_state(self):
        for name, state in [('ordinary_next7', 7), ('special_next18', 18)]:
            case = self.cases[name]
            self.assertEqual(case['initialized']['next_task_state'], state)
            self.assertEqual(case['state_requests'], [{'kind': 'state_request', 'state': state}])
            self.assertEqual((case['pending_flag'], case['pending_state']), (1, state))
            self.assertEqual(case['stub_calls']['task_destructor'], 1)
            self.assertFalse(case['bounded_stop'])

    def test_minus1_suppresses_request_and_child_sentinel_preserves_parent_state(self):
        case = self.cases['no_next_state']
        self.assertEqual(case['initialized']['next_task_state'], -1)
        self.assertEqual(case['state_requests'], [])
        self.assertEqual(case['pending_flag'], 0)
        case = self.cases['child_preserves_next_state']
        self.assertEqual(case['loader_parameter'], 0x7F)
        self.assertEqual(case['initialized']['next_task_state'], 7)
        self.assertEqual(case['state_requests'], [{'kind': 'state_request', 'state': 7}])

    def test_busy_vm_cannot_request_next_task_or_cleanup(self):
        case = self.cases['busy_vm_no_next_request']
        self.assertTrue(case['bounded_stop'])
        self.assertEqual(case['stub_calls']['vm_update'], 4)
        self.assertEqual(case['state_requests'], [])
        self.assertEqual(case['pending_flag'], 0)
        for name in ('adv_cleanup', 'task_destructor'):
            self.assertNotIn(name, case['stub_calls'])
        for case in self.cases.values():
            for key in ('adv_script_executed', 'school_task_executed', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(case[key])

    def test_dispatch_and_loader_call_operands_match_original_image(self):
        image = SOURCE.read_bytes()
        self.assertEqual(self.report['state6_dispatch_target'], '0x49e329')
        self.assertEqual(self.report['adv_task_body_vtable_entry'], '0x4d1a80')
        for address, target in [(0x49E329, 0x4D1820), (0x4D186A, 0x4D1910),
                                (0x4D1930, 0x439EF0), (0x4D1B0B, 0x439E30),
                                (0x4CE23A, 0x4CE260), (0x4CE33E, 0x4CE560)]:
            offset = address-0x400000
            self.assertEqual(image[offset], 0xE8)
            self.assertEqual(address+5+struct.unpack_from('<i', image, offset+1)[0], target)
        self.assertEqual(image[0x4D1938-0x400000:0x4D193E-0x400000], b'\xc7\x00\x6c\x30\x5c\x00')


if __name__ == '__main__':
    unittest.main()
