"""Original VPT graph, source compression and full original AI evidence tests."""
from copy import deepcopy
import gzip
import json
import struct
import unittest
from tools.battle_region_routing import inputs,parse_vpt,oracle,query_corpus,route_corpus,clear
from tools.battle_region_routing_emulation import (ROOT,COARSE,FINE,UNIT,VPT,TERR,SCRATCH,RegionMachine,validate_query,run_route,source_contract,sha)
from tools.battle_region_routing_verification import verify_query,verify_route

REPORT='analysis/battle-region-routing-source-v1-20261024.json.gz'
REPORT_SHA='4424256c7289f13010051fac61bdf01b1bc57b9f3bc83c32b9038dfd6239a7d5'


class RegionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('immutable region source report')
        cls.report=json.loads(gzip.decompress(raw));cls.queries={r['input']['name']:r for r in cls.report['queries']};cls.routes={r['input']['name']:r for r in cls.report['routes']}

    def bad_query(self,edit,replay=False):
        row=deepcopy(self.queries['mode2_same']);edit(row)
        with self.assertRaises(ValueError):verify_query(row,replay)

    def bad_route(self,edit,replay=False):
        row=deepcopy(self.routes['same_region_fallback']);edit(row)
        with self.assertRaises(ValueError):verify_route(row,replay)

    def test_fixed_source_and_complete_corpora(self):
        self.assertEqual(self.report['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.report['queries']],query_corpus())
        self.assertEqual([r['input'] for r in self.report['routes']],route_corpus());self.assertEqual(len(self.queries),17);self.assertEqual(len(self.routes),5)
    def test_all_original_records_edges_and_cell_maps(self):
        d=inputs()['parsed'];self.assertEqual((d['width'],d['height']),(64,96))
        self.assertEqual([len(g) for g in d['graphs']],[120,120,96,120]);self.assertEqual([sum(len(p['edges']) for p in g) for g in d['graphs']],[928,928,1212,928])
        self.assertTrue(all(len(ids)==6144 for ids in d['cell_regions']));self.assertEqual(sum(len(r) for r in d['relative_records']),456)
    def test_all_independent_packets_and_queues(self):
        for row in self.queries.values():
            with self.subTest(case=row['input']['name']):verify_query(row,False)
    def test_all_independent_complete_units_and_memory(self):
        for row in self.routes.values():
            with self.subTest(case=row['input']['name']):verify_route(row,False)
    def test_new_original_coarse_query_replay(self):verify_query(self.queries['mode2_long'],True)
    def test_new_original_complete_AI_replay(self):verify_route(self.routes['same_region_fallback'],True)
    def test_same_region_returns_two_without_packet_output(self):
        for mode in range(4):
            r=self.queries['mode'+str(mode)+'_same'];self.assertEqual(r['call']['result'],2);self.assertEqual(r['popped']['coarse'],[])
    def test_same_region_blocked_line_falls_back_to_real_fine_search(self):
        self.assertFalse(clear([23,66],[15,73]));row=self.routes['same_region_fallback'];v=verify_route(row,False)
        self.assertEqual(v['region_results'],[2]);self.assertGreater(v['fine_expansions'],0);self.assertNotIn('0x44f1e0',row['entries'])
    def test_four_routes_naturally_use_coarse_and_arrive(self):
        for name in ('north_south','south_north','cross_middle','reverse_middle'):
            v=verify_route(self.routes[name],False);self.assertEqual(v['region_results'],[1]);self.assertGreater(v['region_expansions'],0);self.assertEqual(v['final_cell'],self.routes[name]['input']['goal'])
    def test_source_graph_reopens_closed_nodes(self):
        r=verify_query(self.queries['mode0_middle'],False);self.assertEqual(r['reopened'],91);self.assertEqual(r['improved'],90)
    def test_source_compression_mode_changes_points(self):
        self.assertGreater(len(oracle(self.queries['mode0_long']['input'])['points']),1);self.assertEqual(len(oracle(self.queries['mode1_long']['input'])['points']),1)
    def test_coarse_compression_ignores_avoid_flag_and_occupied_goal(self):
        for mode in range(4):
            a=self.queries['mode'+str(mode)+'_long'];b=self.queries['mode'+str(mode)+'_avoid_occupied']
            self.assertEqual(a['packet_hex'],b['packet_hex']);self.assertEqual(a['popped'],b['popped'])
    def test_loader_and_native_world_remain_explicit_boundaries(self):
        self.assertFalse(self.report['source_contract']['original_file_API_or_allocator_executed']);self.assertFalse(self.report['source_contract']['native_scene_or_world_frame'])
        for k in ('R3_complete','R4_complete','R6_complete'):self.assertFalse(self.report[k])
    def test_invalid_query_fields_rejected(self):
        for values in ({'mode':4},{'mode':True},{'avoid':1},{'start':[-1,0]},{'goal':[64,0]},{'goal':[0,96]},{'occupied':[[0,0],[0,0]]}):
            c=deepcopy(query_corpus()[0]);c.update(values)
            with self.assertRaises(ValueError):validate_query(c)
    def test_invalid_AI_budget_rejected(self):
        for v in (0,1025,True):
            c=deepcopy(route_corpus()[0]);c['frames']=v
            with self.assertRaises(ValueError):run_route(c)
    def test_invalid_container_size_rejected(self):
        r=bytearray(inputs()['vpt']);struct.pack_into('<I',r,0,len(r)-1)
        with self.assertRaises(ValueError):parse_vpt(r)
    def test_invalid_relative_record_offset_rejected(self):
        r=bytearray(inputs()['vpt']);struct.pack_into('<I',r,40+24,0)
        with self.assertRaises(ValueError):parse_vpt(r)
    def test_invalid_edge_target_rejected(self):
        d=inputs()['parsed'];r=bytearray(inputs()['vpt']);struct.pack_into('<h',r,40+d['relative_records'][0][0]+4,32767)
        with self.assertRaises(ValueError):parse_vpt(r)
    def test_negative_edge_cost_rejected(self):
        d=inputs()['parsed'];r=bytearray(inputs()['vpt']);struct.pack_into('<i',r,40+d['relative_records'][0][0]+12,-1)
        with self.assertRaises(ValueError):parse_vpt(r)
    def test_negative_cell_region_index_rejected(self):
        d=inputs()['parsed'];r=bytearray(inputs()['vpt']);struct.pack_into('<h',r,d['offsets'][4],-1)
        with self.assertRaises(ValueError):parse_vpt(r)
    def test_source_global_and_code_writes_limited(self):
        m=RegionMachine(query_corpus()[0])
        for at in (SCRATCH-1,SCRATCH+200,0x44EA80,0x59221C,VPT+40):
            with self.assertRaises(ValueError):m.write_hook(m.uc,0,at,1,0,None)
    def test_unknown_loader_body_is_rejected(self):
        m=RegionMachine(query_corpus()[0])
        with self.assertRaisesRegex(ValueError,'0x44e4c0'):m.code(m.uc,0x44E4C0,1,None)
    def test_wrong_query_return_rejected(self):self.bad_query(lambda r:r['call'].update(result=1))
    def test_wrong_query_packet_rejected(self):self.bad_query(lambda r:r.update(packet_hex='00'*236))
    def test_wrong_query_queue_rejected(self):self.bad_query(lambda r:r['popped']['coarse'].append([0,0]))
    def test_wrong_query_CPU_rejected_by_replay(self):self.bad_query(lambda r:r['call']['cpu_after'].update(EAX=17),True)
    def test_wrong_original_trace_rejected_by_replay(self):self.bad_query(lambda r:r.update(code_trace_sha256='0'*64),True)
    def test_missing_relocation_root_rejected(self):self.bad_query(lambda r:r['roots'].pop(0))
    def test_corrupt_relocated_data_rejected(self):
        def edit(r):
            p=next(v for v in r['final'] if v['pointer']==VPT);p['hex']='ff'+p['hex'][2:]
        self.bad_query(edit)
    def test_foreign_map_change_rejected(self):
        def edit(r):
            p=next(v for v in r['final'] if v['pointer']==TERR);p['hex']='ff'+p['hex'][2:]
        self.bad_query(edit)
    def test_missing_owned_memory_rejected(self):self.bad_query(lambda r:r['final'].pop())
    def test_wrong_root_ESP_rejected(self):self.bad_query(lambda r:r['call'].update(ESP_after=0))
    def test_host_path_root_rejected(self):self.bad_route(lambda r:r['roots'][4].update(entry=0x437E40))
    def test_whole_unit_corruption_rejected(self):self.bad_route(lambda r:r['steps'][0].update(after_hex='00'*0x520))
    def test_invented_attack_completion_rejected(self):self.bad_route(lambda r:r.update(stop='attack_complete'))
    def test_missing_coordinate_writes_rejected(self):self.bad_route(lambda r:r.update(original_coordinate_writes=0))
    def test_wrong_dual_pool_cleanup_rejected(self):self.bad_route(lambda r:r['cleanup'][0].update(receiver=FINE+0x18))
    def test_global_scratch_corruption_rejected(self):
        row=deepcopy(self.queries['mode2_long']);p=next(v for v in row['final'] if v['pointer']==0x7A3000);at=(SCRATCH-0x7A3000)*2;p['hex']=p['hex'][:at]+'ff'+p['hex'][at+2:]
        with self.assertRaises(ValueError):verify_query(row,False)


if __name__=='__main__':unittest.main()
