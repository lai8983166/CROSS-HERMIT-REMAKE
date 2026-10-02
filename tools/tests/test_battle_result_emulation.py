"""Native result control, with unresolved preparation excluded from authority."""
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.battle_result_emulation import report
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class BattleResultEmulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {case['name']: case for case in cls.report['cases']}
        cls.image = (ROOT / 'analysis/hermit_game.exe').read_bytes()

    def test_native_cleanup_precedes_state_ten_and_constructor(self):
        for name in ('confirm', 'skip_flag', 'special_date'):
            case = self.cases[name]
            self.assertFalse(case['bounded_stop'])
            self.assertEqual([event['state'] for event in case['dispatch_events']
                              if event['kind'] == 'state_request'], [11, 10])
            request = next(event for event in case['dispatch_events']
                           if event.get('state') == 10)
            self.assertEqual(request['caller_return_va'], '0x4bd6d4')
            native = [event['va'] for event in case['result_events']
                      if event['kind'] == 'native_entry']
            self.assertLess(native.index('0x4bd620'), native.index('0x4bd590'))
            self.assertLess(native.index('0x4bd590'), native.index('0x4b9120'))
            self.assertEqual(case['preparation_task'],
                             {'pointer': '0x9401000', 'vtable': '0x5a0c38', 'active': 1})
            self.assertEqual((case['requested_state'], case['request_pending']), (10, 0))
            self.assertIn('0x4bd660', case['visited_original_addresses'])
            self.assertIn('0x4b8f20', case['visited_original_addresses'])

    def test_distinct_skip_branches_preserve_preparation_call_order(self):
        for name, expected in (('confirm', ['0x4bd210', '0x4bca40', '0x4bbd40']),
                               ('skip_flag', []),
                               ('special_date', ['0x4bd210', '0x4bca40', '0x4bbd40'])):
            case = self.cases[name]
            self.assertEqual([event['va'] for event in case['result_events']
                              if event['kind'] == 'unresolved_preparation'], expected)
            self.assertEqual(case['skip_display'], int(name != 'confirm'))
            self.assertEqual(case['result_phase'], 4 if name == 'confirm' else 0)

    def test_missing_confirm_or_cleanup_blocks_exit_and_destructor(self):
        for name, phase in (('confirm_missing', 2), ('audio_missing', 3)):
            case = self.cases[name]
            self.assertTrue(case['bounded_stop'])
            self.assertEqual(case['result_phase'], phase)
            self.assertEqual([event['state'] for event in case['dispatch_events']
                              if event['kind'] == 'state_request'], [11])
            self.assertNotIn('0x4bd590', case['visited_original_addresses'])
            self.assertEqual(case['preparation_task']['pointer'], '0x0')

    def test_raw_calls_and_input_flag_offset_match_execution(self):
        for call, target in ((0x4BD686, 0x4BAA90), (0x4BD69B, 0x4BAB60),
                             (0x4BD6CF, 0x439E30), (0x49E36E, 0x4B9120)):
            at = call-0x400000
            self.assertEqual(self.image[at], 0xE8)
            self.assertEqual(call+5+struct.unpack_from('<i', self.image, at+1)[0], target)
        # lea buffer,[ebp-1C]; following test uses [ebp-18] == buffer+4.
        self.assertEqual(self.image[0x4BACB3-0x400000:0x4BACB6-0x400000], bytes.fromhex('8d55e4'))
        self.assertEqual(self.image[0x4BACC1-0x400000:0x4BACC4-0x400000], bytes.fromhex('8b45e8'))

    def test_reexecution_matches_report_and_never_authorizes_transactions(self):
        raw = (ROOT / 'analysis/battle-result-control-v1-20261002.json').read_bytes()
        self.assertEqual(raw.decode('utf-8'), report_text(self.report))
        for case in self.report['cases']:
            self.assertFalse(case['live_witness'])
            self.assertFalse(case['preparation_resolved'])
            self.assertFalse(case['authorizes_persistent_write'])
            for va in ('0x4bd210', '0x4bca40', '0x4bbd40', '0x4b8ff0', '0x4c1aa0'):
                self.assertNotIn(va, case['visited_original_addresses'])


if __name__ == '__main__':
    unittest.main()
