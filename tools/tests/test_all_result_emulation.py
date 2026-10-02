"""Real native writes and timing, separate from synthetic MVP/control boundaries."""
import hashlib
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.all_result_emulation import report, AllResultEmulator
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class AllResultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_same_instance_state10_gate_and_state12_constructor(self):
        for case in self.report['cases']:
            self.assertEqual([e['state'] for e in case['dispatch_events']
                              if e['kind'] == 'state_request'][:3], [11, 10, 12])
            self.assertEqual(case['constructor'],
                {'pointer': '0x9700000', 'vtable': '0x5a0f74', 'active': 1})
            self.assertEqual([e['va'] for e in case['events'][:5]],
                ['0x4b8ff0', '0x4c1d30', '0x4c1910', '0x4c1aa0', '0x4bd870'])
            self.assertFalse(case['live_witness'])
            self.assertFalse(case['authorizes_persistent_write'])

    def test_growth_pools_and_attributes_match_independent_original_thresholds(self):
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        increments = struct.unpack_from('<136i', image, 0x6E4308-0x400000)
        levels = struct.unpack_from('<50i', image, 0x625300-0x400000)
        def attribute(pool):
            total = 0
            for level in range(1, 136):
                total += increments[level]
                if total > pool:
                    return max(1, level-1)
            self.fail('pool outside source table')
        for name, case in self.cases.items():
            if name == 'mode1_flag0':
                continue
            for before, after in zip(case['before']['characters'], case['after']['characters']):
                pools = [p+v for p, v in zip(before['growth_pools'], before['staged_package'][:7])]
                self.assertEqual(after['growth_pools'], pools)
                self.assertEqual(after['attributes'], [attribute(pool) for pool in pools])
                character = before['character_id']
                record = 0x6F5088+character*0x4A0-0x400000
                skill_points = sum(struct.unpack_from('<i', image, 0x6C2E08+(i+1)*0x48-0x400000)[0]
                    for i, status in enumerate(before['skill_statuses']) if status in (3, 5, 6))
                self.assertEqual(image[record+0xB8:record+0xB9], bytes([before['skill_statuses'][0]]))
                total = sum(pools)+skill_points
                level = 2
                while level < 51 and levels[level-1] <= total:
                    level += 1
                self.assertEqual(after['level_50'], level-1)
                self.assertEqual(after['staged_package'], before['staged_package'])

    def test_unconfirmed_and_busy_mvp_apply_growth_but_not_later_fields(self):
        confirmed = self.cases['ordinary_confirm']
        for name, phase in [('ordinary_unconfirmed', 3), ('mvp_boundary_busy', 5)]:
            case = self.cases[name]
            self.assertTrue(case['bounded_stop'])
            self.assertEqual(case['phase'], phase)
            self.assertEqual(case['stop_reason'], 'presentation_yield_bound')
            self.assertEqual(case['requested_state'], 12)
            self.assertNotIn('0x4c1350', [e.get('va') for e in case['events']])
            for before, after, complete in zip(case['before']['characters'],
                    case['after']['characters'], confirmed['after']['characters']):
                for key in ('growth_pools', 'attributes', 'level_50', 'character_sha256'):
                    self.assertEqual(after[key], complete[key])
                for key in ('job_progress', 'week_records_hex', 'recipient_count'):
                    self.assertEqual(after[key], before[key])
            self.assertEqual(case['after']['relationships'], case['before']['relationships'])

    def test_ordinary_confirmation_records_history_relationships_and_recipient(self):
        case = self.cases['ordinary_confirm']
        self.assertFalse(case['bounded_stop'])
        self.assertEqual((case['branch'], case['phase'], case['requested_state']), (0, 6, 6))
        self.assertEqual(case['after']['recipient_id'], 4)
        for before, after in zip(case['before']['characters'], case['after']['characters']):
            self.assertEqual(after['job_progress'], before['job_progress']+1)
            history = bytes.fromhex(after['week_records_hex'])
            self.assertEqual(history[4*3:5*3], bytes([2, 5, 7]))
            self.assertEqual(after['recipient_count'], int(after['character_id'] == 4))
        self.assertTrue(all(r['value'] == 54 for r in case['after']['relationships']))
        requests = [e for e in case['events'] if 'boundary' in e]
        self.assertEqual([(r['path'], r['sub']) for r in requests],
                         [('Data\\AllResult\\dat\\mvp.ybc', -1), ('Data\\Adv\\dat\\CH003.ybc', 7)])

    def test_mode1_flag_is_not_equivalent_to_no_character_writes(self):
        unchanged, growth = self.cases['mode1_flag0'], self.cases['mode1_flag1']
        self.assertEqual(unchanged['before']['characters'], unchanged['after']['characters'])
        self.assertEqual(unchanged['requested_state'], 15)
        self.assertEqual(growth['requested_state'], 13)
        self.assertEqual(growth['after']['recipient_id'], -1)
        self.assertIn('0x4c0350', [e.get('va') for e in growth['events']])
        for before, after in zip(growth['before']['characters'], growth['after']['characters']):
            self.assertNotEqual(after['growth_pools'], before['growth_pools'])
            for key in ('job_progress', 'week_records_hex', 'recipient_count'):
                self.assertEqual(after[key], before[key])
        self.assertEqual(growth['after']['relationships'], growth['before']['relationships'])

    def test_special_date_stops_before_week_transaction_without_fake_return(self):
        case = self.cases['special_week_boundary']
        self.assertEqual(case['branch'], 2)
        self.assertEqual(case['stop_reason'], 'week_transaction_boundary')
        self.assertEqual(case['events'][-1]['va'], '0x4d3510')
        self.assertNotIn('0x4d3510', case['visited_original_addresses'])
        for character in case['after']['characters']:
            history = bytes.fromhex(character['week_records_hex'])
            self.assertEqual(history[58*3:59*3], bytes([2, 5, 7]))

    def test_nonparticipants_and_calendar_remain_unchanged_in_every_case(self):
        for case in self.report['cases']:
            for key in ('month', 'week', 'global_total_511c',
                        'nonparticipant_character_sha256', 'nonparticipant_package_hex'):
                self.assertEqual(case['before'][key], case['after'][key])

    def test_source_edges_and_report_reexecute_exactly(self):
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        for call, target in ((0x4BD9D0, 0x4C00C0), (0x4BD9E7, 0x4C0350),
                (0x4C01A3, 0x4C0C10), (0x4C0D4A, 0x4D5600),
                (0x4C0DD7, 0x4D58E0), (0x4C18EE, 0x4BF9E0)):
            at = call-0x400000
            self.assertEqual(image[at], 0xE8)
            self.assertEqual(call+5+struct.unpack_from('<i', image, at+1)[0], target)
        path = ROOT / 'analysis/all-result-application-v1-20261002.json'
        self.assertEqual(path.read_bytes().decode(), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)

    def test_rejects_unknown_mode_and_out_of_bound_replay(self):
        for kwargs in ({'mode': 2}, {'mode': 0.5}, {'result_flag': 2}, {'max_yields': 0}):
            with self.assertRaises(ValueError):
                AllResultEmulator(**kwargs)


REPORT_SHA256 = '9e014832d373221dc22d269e308caa4e1a256740faccbdb9835df1bc4ad22dc9'


if __name__ == '__main__':
    unittest.main()
