"""Original route admission, independent two-packet/frontier model and rejection."""
from copy import deepcopy
import gzip
import json
import unittest
from tools.battle_route_admission import corpus
from tools.battle_route_admission_emulation import ROOT,UNIT,FINDER,AdmissionMachine,source_contract,sha
from tools.battle_route_admission_verification import verify_case

REPORT='analysis/battle-route-admission-source-v1-20261024.json.gz'
REPORT_SHA='00a369224e6b7979b8e7bbe3fb1aa6e73a1cdf8b85888d2c7ffecaa392cadc6b'


class AdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('immutable source admission corpus')
        cls.report=json.loads(gzip.decompress(raw));cls.rows={r['input']['movement']['name']:r for r in cls.report['cases']}

    def bad(self,fn,replay=False):
        row=deepcopy(self.rows['movement_type4_gate']);fn(row)
        with self.assertRaises(ValueError):verify_case(row,replay)

    def test_source_identity_and_all_22_inputs(self):
        self.assertEqual(self.report['source_contract'],source_contract())
        self.assertEqual([r['input'] for r in self.report['cases']],corpus());self.assertEqual(len(self.rows),22)

    def test_all_complete_unit_and_persistent_queue_models(self):
        for row in self.rows.values():
            with self.subTest(case=row['input']['movement']['name']):verify_case(row,False)

    def test_new_original_execution_and_full_memory(self):verify_case(self.rows['direction_2'],True)

    def test_only_original_AI_prepares_and_consumes_both_packets(self):
        row=self.rows['direction_2'];self.assertEqual(len(row['roots']),2)
        self.assertEqual({x['calls'][0]['entry'] for x in row['steps']},{0x476680})
        self.assertGreater(row['entries']['0x47d210'],1);self.assertGreater(row['entries']['0x47d830'],1)

    def test_primary_and_secondary_partial_search_resume(self):
        for name,phase in [('primary_partial_1001',2),('secondary_partial_1001',6)]:
            row=self.rows[name];self.assertEqual(row['steps'][0]['phase'],phase)
            proof=verify_case(row,False);self.assertGreater(proof['partial_search_returns'],0)
            self.assertGreater(len(row['search_popped']),1001);self.assertGreater(row['entries']['0x47d730'],0)
            self.assertEqual(len(row['final_ownership'][2]['links']),1600)

    def test_primary_proximity_handoff_precedes_exact_arrival(self):
        row=self.rows['wall_detour'];self.assertEqual([x['phase'] for x in row['steps'][:3]],[4,9,3])
        a=bytes.fromhex(row['steps'][1]['after_hex']);b=bytes.fromhex(row['steps'][2]['after_hex'])
        self.assertEqual(a[0x2EC:0x2F4],b[0x2EC:0x2F4])

    def test_signed_retry_threshold(self):
        self.assertEqual(self.rows['retry_11']['stop'],'stationary_phase_4')
        for name in ('retry_10','retry_-128'):self.assertEqual(self.rows[name]['stop'],'secondary_only_arrived')

    def test_initial_cooldown_decrements_without_route_writes(self):
        row=self.rows['initial_cooldown'];self.assertEqual([r['phase'] for r in row['steps'][:4]],[0,0,0,4])
        for step in row['steps'][:3]:
            a=bytes.fromhex(step['before_hex']);b=bytes.fromhex(step['after_hex'])
            self.assertEqual(a[:0x4E0]+a[0x4E2:],b[:0x4E0]+b[0x4E2:])

    def test_movement_and_AI_mode_gates(self):
        for name in ('movement_type4_gate','AI_mode_gate_2','AI_mode_gate_3'):
            row=self.rows[name];self.assertEqual(row['stop'],'stationary_phase_0');self.assertEqual(row['original_coordinate_write_count'],0)
            self.assertNotIn('0x47d210',row['entries'])

    def test_same_cell_is_phase0_no_route(self):self.assertEqual(self.rows['same_cell']['stop'],'stationary_phase_0')
    def test_forced_primary_and_local_evaluation(self):
        for name in ('force_primary_search','retry_search'):self.assertGreater(self.rows[name]['entries']['0x47d570'],0)

    def test_far_region_graph_dependency_rejected(self):
        c=deepcopy(corpus()[0]);c['movement']['path'].update(grid=['00000000001000000000']*12,start=[0,0],goal=[19,0])
        c['movement']['frames']=1;m=AdmissionMachine(c)
        with self.assertRaisesRegex(ValueError,'0x44ea80'):m.run()

    def test_blocked_primary_goal_also_requires_region_graph(self):
        c=deepcopy(corpus()[2]);c['movement']['path']['grid'][3]='0000001'
        c['movement']['frames']=1
        with self.assertRaisesRegex(ValueError,'0x44ea80'):AdmissionMachine(c).run()

    def test_invalid_declared_inputs_rejected(self):
        for change in ({'initial_phase':2},{'retry':128},{'retry':True},{'cooldown':6},{'movement_type':3},{'unit_kind':2},{'ai_mode':1}):
            c=deepcopy(corpus()[0]);c.update(change)
            with self.assertRaises(ValueError):AdmissionMachine(c)

    def test_foreign_write_rejected(self):
        m=AdmissionMachine(corpus()[0])
        with self.assertRaises(ValueError):m.write_hook(m.uc,0,FINDER+0x100,4,0,None)

    def test_wrong_packet_initializer_rejected(self):self.bad(lambda r:r['roots'][0].update(entry=0x437E40))
    def test_host_primary_path_injection_rejected(self):self.bad(lambda r:r.update(host_unit_fields_changed_after_initialization=True))
    def test_wrong_state_input_rejected(self):self.bad(lambda r:r['steps'][0].update(before_hex='00'+r['steps'][0]['before_hex'][2:]))
    def test_wrong_state_output_rejected(self):self.bad(lambda r:r['steps'][0].update(after_hex='00'+r['steps'][0]['after_hex'][2:]))
    def test_wrong_stop_rejected(self):self.bad(lambda r:r.update(stop='attack_complete'))
    def test_wrong_coordinate_count_rejected(self):self.bad(lambda r:r.update(original_coordinate_write_count=2))
    def test_wrong_phase_rejected(self):self.bad(lambda r:r['steps'][0].update(phase=3))
    def test_host_helper_scheduling_rejected(self):self.bad(lambda r:r['steps'][0]['calls'][0].update(entry=0x47D210))
    def test_wrong_stack_rejected(self):self.bad(lambda r:r['steps'][0]['calls'][0].update(ESP_after=0))
    def test_register_corruption_rejected(self):self.bad(lambda r:r['steps'][0]['calls'][0]['cpu_after'].update(EBX=1))
    def test_missing_mapping_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_unrelated_controller_corruption_rejected(self):self.bad(lambda r:r['final'][11].update(hex='01'+r['final'][11]['hex'][2:]))
    def test_wrong_search_order_rejected(self):self.bad(lambda r:r['search_popped'].append([0,0]))
    def test_missing_pool_cleanup_rejected(self):self.bad(lambda r:r['final_ownership'][0]['links'].append(1))
    def test_code_trace_corruption_rejected(self):self.bad(lambda r:r.update(code_trace_sha256='0'*64),True)
    def test_write_trace_corruption_rejected(self):self.bad(lambda r:r.update(write_trace_sha256='0'*64),True)
    def test_mutable_finder_corruption_rejected_by_replay(self):
        def mutate(r):
            region=r['final'][11];data=bytearray.fromhex(region['hex']);data[FINDER-0x11000000]^=1;region['hex']=data.hex()
        self.bad(mutate,True)


if __name__=='__main__':unittest.main()
