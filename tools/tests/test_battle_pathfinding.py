"""Original full-chain and independent path rules, with corrupted-evidence rejection."""
from copy import deepcopy
import gzip
import json
import unittest
from tools.battle_pathfinding import corpus, oracle, source_contract, validate_case
from tools.battle_pathfinding_emulation import ROOT, PathMachine, MAP, PACKET, sha
from tools.battle_pathfinding_verification import verify_case

REPORT = 'analysis/battle-pathfinding-source-v2-20261024.json.gz'
REPORT_SHA = 'd9bc9a9071e2b1482c25bfdf7e1a1d3b49006f6cb8b23461decc6f4680a96d45'


class PathfindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (ROOT/REPORT).read_bytes()
        if sha(raw) != REPORT_SHA: raise ValueError('immutable original source matrix identity')
        cls.report = json.loads(gzip.decompress(raw))
        cls.rows = {row['input']['name']: row for row in cls.report['cases']}

    def bad(self, mutate, name='open_diagonal', replay=False):
        row = deepcopy(self.rows[name]); mutate(row)
        with self.assertRaises(ValueError): verify_case(row, replay)

    def test_complete_source_and_corpus(self):
        self.assertEqual(self.report['source_contract'], source_contract())
        self.assertEqual([r['input'] for r in self.report['cases']], corpus())
        self.assertEqual(len(self.rows), 77)

    def test_all_original_rules_full_packet_and_cost(self):
        for row in self.report['cases']:
            with self.subTest(case=row['input']['name']): verify_case(row)

    def test_fresh_original_complete_lifetime(self):
        verify_case(self.rows['wall_gap'], replay=True)

    def test_blocked_destination_special_case(self):
        r = self.rows['blocked_destination']
        self.assertEqual((r['result'], r['waypoints'], r['popped']), (1, [[4, 1]], []))

    def test_wall_is_cost_not_absolute_exclusion(self):
        r = self.rows['full_wall_penalty']
        self.assertIn([2, 2], r['waypoints'])
        self.assertEqual(oracle(r['input'])['cost'], 3603)

    def test_diagonal_does_not_check_orthogonal_corners(self):
        c = deepcopy(self.rows['same_cell']['input'])
        c.update(name='corner', grid=['010', '100', '000'], start=[0, 0], goal=[1, 1])
        row = PathMachine(c).run(); verify_case(row)
        self.assertEqual(row['waypoints'], [[1, 1]])

    def test_occupancy_changes_path(self):
        self.assertNotEqual(self.rows['occupancy_False']['waypoints'], self.rows['occupancy_True']['waypoints'])

    def test_mode_four_aliases_zero(self):
        a, b = self.rows['terrain_mode_0'], self.rows['terrain_mode_4']
        self.assertEqual((a['waypoints'], a['popped']), (b['waypoints'], b['popped']))

    def test_same_cell_success_empty_packet(self):
        r = self.rows['same_cell']; self.assertEqual(r['result'], 1); self.assertEqual(r['waypoints'], [])
        self.assertEqual([x['result'] for x in r['consume']], [1, 1])

    def test_limit_and_reopened_nodes(self):
        r = self.rows['expansion_limit']
        self.assertEqual((r['result'], len(r['popped'])), (-1, 1001))
        self.assertGreater(r['reopened'], 0)
        self.assertTrue(r['ownership_after_search'][0]['links'])
        self.assertFalse(r['ownership_final'][0]['links'])
        self.assertEqual(len(r['ownership_final'][2]['links']), 1600)

    def test_all_keypad_directions(self):
        self.assertEqual({r['input']['direction'] for r in self.rows.values() if r['input']['kind'] == 'ray'}, {1, 2, 3, 4, 6, 7, 8, 9})

    def test_nonconvergent_direction_rejected(self):
        for direction in (0, 5):
            c = deepcopy(self.rows['ray_1']['input']); c['direction'] = direction
            with self.assertRaisesRegex(ValueError, 'nonzero keypad'): PathMachine(c)

    def test_direct_slopes_in_all_quadrants(self):
        for goal in ([0, 1], [1, 0], [4, 0], [5, 1], [5, 4], [4, 5], [1, 5], [0, 4]):
            c = deepcopy(self.rows['direct_octant_0']['input'])
            c.update(name='slope', grid=['000000']*6, start=[2, 2], goal=goal)
            verify_case(PathMachine(c).run())

    def test_invalid_inputs_rejected(self):
        changes = ({'mode': True}, {'mode': -1}, {'avoid': 1}, {'grid': ['00', '0']},
                   {'grid': ['x']}, {'start': [-1, 0]}, {'goal': [99, 99]},
                   {'occupied': [[0, 0], [0, 0]]}, {'direction': 10}, {'kind': 'astar'})
        for change in changes:
            c = deepcopy(self.rows['open_diagonal']['input']); c.update(change)
            with self.assertRaises(ValueError): validate_case(c)

    def test_unexpected_root_rejected(self):
        m = PathMachine(corpus()[0])
        with self.assertRaisesRegex(ValueError, 'root'): m.call(0x477980)

    def test_forbidden_map_write_rejected(self):
        m = PathMachine(corpus()[0])
        with self.assertRaisesRegex(ValueError, 'forbidden'): m.write_hook(m.uc, 0, MAP, 4, 0, None)

    def test_wrong_result_rejected(self): self.bad(lambda r: r.update(result=0))
    def test_wrong_waypoint_rejected(self): self.bad(lambda r: r['waypoints'][0].__setitem__(0, 4))
    def test_wrong_search_order_rejected(self): self.bad(lambda r: r['popped'].reverse())
    def test_wrong_reopen_count_rejected(self): self.bad(lambda r: r.update(reopened=1))
    def test_wrong_packet_tail_rejected(self): self.bad(lambda r: r.update(packet_hex=r['packet_hex'][:-2]+'01'))
    def test_wrong_consumption_convention_rejected(self): self.bad(lambda r: r['consume'][0].update(result=1))
    def test_exhausted_coordinates_rejected(self): self.bad(lambda r: r['consume'][-1].update(x=0))
    def test_wrong_stack_rejected(self): self.bad(lambda r: r['calls'][1].update(ESP_after=0))
    def test_map_tampering_rejected(self): self.bad(lambda r: r['final'][1].update(hex='00'+r['final'][1]['hex'][2:-2]+'01'))
    def test_omitted_mapping_rejected(self): self.bad(lambda r: r['final'].pop())
    def test_incomplete_cleanup_rejected(self): self.bad(lambda r: r['ownership_final'][0]['links'].append(1))
    def test_native_scope_inflation_rejected(self): self.bad(lambda r: r.update(unit_coordinates_updated=True))
    def test_instruction_trace_tampering_rejected(self): self.bad(lambda r: r.update(code_trace_sha256='0'*64), replay=True)
    def test_write_trace_tampering_rejected(self): self.bad(lambda r: r.update(write_trace_sha256='0'*64), replay=True)
    def test_mutable_memory_tampering_rejected_by_replay(self):
        self.bad(lambda r: r['final'][0].update(hex='01'+r['final'][0]['hex'][2:]), replay=True)


if __name__ == '__main__': unittest.main()
