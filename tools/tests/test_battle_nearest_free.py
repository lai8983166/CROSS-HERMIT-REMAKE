"""Original selection/reservation and integrated rerouting evidence checks."""
from copy import deepcopy
import gzip
import json
import struct
import unittest
from tools.battle_nearest_free import expected_table,select,selection_corpus,movement_corpus
from tools.battle_nearest_free_emulation import (ROOT,MAP,TABLE,REGIONS,NearestMachine,declared_table,selection,validate_selection,source_contract,sha)
from tools.battle_nearest_free_verification import verify_selection,verify_route,verify_flood

REPORT='analysis/battle-nearest-free-source-v1-20261024.json.gz'
REPORT_SHA='420887b69bbf2eea29429aac41b82721a68201e283253eb2936e01ad91fe9e1d'


class NearestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('immutable nearest-free source corpus')
        cls.report=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.report['selection']}
        cls.routes={r['input']['movement']['name']:r for r in cls.report['routes']}
        cls.table=bytes.fromhex(cls.report['declared_table_hex'])

    def bad_selection(self,edit,replay=False):
        row=deepcopy(self.rows['rotation_4']);edit(row)
        with self.assertRaises(ValueError):verify_selection(row,replay,self.table)

    def bad_route(self,edit,replay=False):
        row=deepcopy(self.routes['east']);edit(row)
        with self.assertRaises(ValueError):verify_route(row,replay,self.table)

    def test_source_identity_and_complete_inputs(self):
        self.assertEqual(self.report['source_contract'],source_contract())
        self.assertEqual([r['input'] for r in self.report['selection']],selection_corpus())
        self.assertEqual([r['input'] for r in self.report['routes']],movement_corpus())

    def test_all_4225_candidates_independent(self):
        self.assertEqual(self.table,expected_table());self.assertEqual(self.table,declared_table())
        records=list(struct.iter_unpack('<bbHH',self.table));self.assertEqual(len(records),4225)
        self.assertEqual(len({(x,y) for x,y,_,_ in records}),4225)
        self.assertTrue(all(d==abs(x)+abs(y) and i==k for k,(x,y,d,i) in enumerate(records)))

    def test_original_recursive_fill_all_4225(self):verify_flood(self.report['flood'],False,self.table)
    def test_all_selection_models_and_work_bytes(self):
        for row in self.rows.values():
            with self.subTest(case=row['input']['name']):verify_selection(row,False,self.table)
    def test_all_whole_unit_models(self):
        for row in self.routes.values():
            with self.subTest(case=row['input']['movement']['name']):verify_route(row,False,self.table)
    def test_fresh_original_selection_replay(self):verify_selection(self.rows['rotation_0'],True,self.table)
    def test_fresh_original_route_replay(self):verify_route(self.routes['east'],True,self.table)
    def test_rotation_can_precede_free_seed(self):
        self.assertEqual(self.rows['rotation_0']['calls'][0]['output'],[4,4])
        self.assertEqual(self.rows['rotation_4']['calls'][0]['output'],[3,3])
    def test_mode4_skips_terrain_and_occupancy(self):
        for name in ('all_blocked','all_occupied'):self.assertEqual(self.rows[name]['calls'][0]['call']['result'],0)
        self.assertEqual(self.rows['mode4_bypasses_both']['calls'][0]['call']['result'],1)
    def test_failure_output_retained(self):
        for name in ('all_blocked','all_occupied','view0_reserved'):self.assertEqual(self.rows[name]['calls'][0]['output'],[0xA55A,0x5AA5])
    def test_forty_reservations_no_duplicates(self):
        row=self.rows['reserve_40'];points=[tuple(r['output']) for r in row['calls']]
        self.assertEqual(len(set(points)),40);self.assertEqual(len(row['calls'][-1]['state']['points']),40)
    def test_reset_entire_work_retains_rotation(self):
        row=self.rows['reservation_reset'];self.assertEqual(row['calls'][0]['state'],dict(counter=0,points=[],work_hex='00'*0xA4))
    def test_no_full_constructor_or_global_completion_claim(self):
        self.assertFalse(self.report['source_contract']['full_original_constructor_executed'])
        self.assertFalse(self.report['source_contract']['table_builder_reference']['executed'])
        for k in ('R3_complete','R4_complete','R6_complete'):self.assertFalse(self.report[k])
    def test_faction_gate_sets_thirty_frame_cooldown(self):
        base=verify_route(self.routes['east'],False,self.table);delayed=verify_route(self.routes['east_faction4_cooldown'],False,self.table)
        self.assertEqual(delayed['AI_calls']-base['AI_calls'],30);self.assertEqual(delayed['maximum_cooldown'],30)
        self.assertEqual(delayed['positive_cooldown_boundaries'],30)
    def test_original_target_preserved_adjusted_target_reached(self):
        for row in self.routes.values():
            r=verify_route(row,False,self.table);self.assertEqual(len(r['adjustments']),1);self.assertEqual(r['stop'],'secondary_only_arrived')
    def test_invalid_selection_inputs_rejected(self):
        for change in ({'view':33},{'view':-1},{'mode':5},{'mode':True},{'counter':-1},{'counter':5},{'calls':41},{'seed':[True,0]}):
            c=deepcopy(selection_corpus()[0]);c.update(change)
            with self.assertRaises(ValueError):validate_selection(c)
    def test_forty_first_original_reservation_assertion_rejected(self):
        c=deepcopy(selection_corpus()[0]);c['reservations']=[[x,y] for y in range(7) for x in range(7)][:40]
        with self.assertRaisesRegex(ValueError,'0x424f80'):selection(c,self.table)
    def test_candidate_table_and_other_map_write_rejected(self):
        m=NearestMachine(movement_corpus()[0],self.table)
        for at in (TABLE,MAP+0x263B8,MAP+0x2646C):
            with self.assertRaises(ValueError):m.write_hook(m.uc,0,at,4,0,None)
    def test_unknown_code_rejected(self):
        m=NearestMachine(movement_corpus()[0],self.table)
        with self.assertRaises(ValueError):m.code(m.uc,0x44EA80,1,None)
    def test_wrong_return_rejected(self):self.bad_selection(lambda r:r['calls'][0]['call'].update(result=0))
    def test_wrong_output_rejected(self):self.bad_selection(lambda r:r['calls'][0].update(output=[0,0]))
    def test_wrong_counter_rejected(self):self.bad_selection(lambda r:r['calls'][0]['state'].update(counter=3))
    def test_wrong_work_tail_rejected(self):self.bad_selection(lambda r:r['calls'][0]['state'].update(work_hex='00'*0xA4))
    def test_wrong_abi_rejected(self):self.bad_selection(lambda r:r['calls'][0]['call'].update(ESP_after=0))
    def test_missing_memory_rejected(self):self.bad_selection(lambda r:r['final'].pop())
    def test_readonly_table_corruption_rejected(self):
        def edit(r):
            region=next(v for v in r['final'] if v['pointer']==TABLE);region['hex']='ff'+region['hex'][2:]
        self.bad_selection(edit)
    def test_original_trace_corruption_rejected_by_replay(self):self.bad_selection(lambda r:r.update(code_trace_sha256='0'*64),True)
    def test_route_unit_corruption_rejected(self):self.bad_route(lambda r:r['steps'][0].update(after_hex='00'*0x520))
    def test_route_host_search_root_rejected(self):self.bad_route(lambda r:r['roots'][0].update(entry=0x437E40))
    def test_route_search_order_corruption_rejected(self):self.bad_route(lambda r:r['search_popped'].append([99,99]))
    def test_route_coordinate_count_rejected(self):self.bad_route(lambda r:r.update(original_coordinate_write_count=0))
    def test_route_false_completion_rejected(self):self.bad_route(lambda r:r.update(stop='attack_complete'))
    def test_route_CPU_corruption_rejected_by_replay(self):self.bad_route(lambda r:r['steps'][0]['calls'][0]['cpu_after'].update(EAX=999),True)
    def test_flood_distance_corruption_rejected(self):
        row=deepcopy(self.report['flood']);row['distances_hex']='ffff'+row['distances_hex'][4:]
        with self.assertRaises(ValueError):verify_flood(row,False,self.table)


if __name__=='__main__':unittest.main()
