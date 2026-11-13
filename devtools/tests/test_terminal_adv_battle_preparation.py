import copy
import gzip
import hashlib
import json
import unittest

from devtools import terminal_adv_battle_preparation as preparation


class RetainedRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (preparation.ROOT / preparation.SOURCE).read_bytes()
        if hashlib.sha256(raw).hexdigest() != preparation.SOURCE_SHA:
            raise ValueError('fixed real route source required')
        cls.source = json.loads(gzip.decompress(raw))

    def altered(self):
        return dict(self.source, probe=dict(self.source['probe']))

    def test_real_preparation_owner_and_order_are_retained(self):
        route = preparation.extract_route(self.source)
        self.assertEqual(route['post_ADV_input_actions'], 350)
        self.assertEqual(route['input_predicates_replayed'], 356)
        self.assertEqual(route['observed_owners'][6]['vtable'], '0x5a0c38')
        self.assertGreater(route['battle_first_observed_seconds'], 600)

    def test_omitting_short_preparation_owner_is_rejected(self):
        altered = self.altered()
        altered['probe']['workers'] = self.source['probe']['workers'][:6] + self.source['probe']['workers'][7:]
        with self.assertRaisesRegex(ValueError, 'including preparation'):
            preparation.extract_route(altered)

    def test_another_school_date_cannot_reuse_this_route(self):
        altered = self.altered()
        altered['probe']['school_inputs'] = copy.deepcopy(self.source['probe']['school_inputs'])
        row = altered['probe']['school_inputs'][0]['ready_decision_sample']
        date = next(x for x in row['school']['fields'] if x['name'] == 'date_hex')
        date['hex'] = '05000100'
        with self.assertRaisesRegex(ValueError, 'school_departure'):
            preparation.extract_route(altered)

    def test_different_dialogue_pc_is_not_a_matching_confirmation(self):
        altered = self.altered()
        phases = list(self.source['probe']['story_phases'])
        phases[0] = dict(phases[0], actions=list(phases[0]['actions']))
        phases[0]['actions'][0] = dict(phases[0]['actions'][0], key=[1, 2, 3])
        altered['probe']['story_phases'] = phases
        with self.assertRaisesRegex(ValueError, 'dialogue key'):
            preparation.extract_route(altered)

    def test_retreat_cannot_be_moved_before_notice(self):
        altered = self.altered()
        actions = list(self.source['probe']['battle_inputs'])
        actions[0] = dict(actions[0], before_elapsed=1000, after_elapsed=1001)
        altered['probe']['battle_inputs'] = actions
        with self.assertRaisesRegex(ValueError, 'legal chronological route'):
            preparation.extract_route(altered)

    def test_missing_actual_wait_ancestry_rejects_retreat(self):
        altered = self.altered()
        actions = copy.deepcopy(self.source['probe']['battle_inputs'])
        row = actions[0]['ready_decision_sample']
        tid = row['tasks'][0]['thread_id']
        frame = next(f for f in row['frames'] if f['tid'] == tid)
        frame['chain'] = [f for f in frame['chain'] if f['return_va'] != 0x453CB5]
        altered['probe']['battle_inputs'] = actions
        with self.assertRaisesRegex(ValueError, 'retreat_request'):
            preparation.extract_route(altered)


if __name__ == '__main__':
    unittest.main()
