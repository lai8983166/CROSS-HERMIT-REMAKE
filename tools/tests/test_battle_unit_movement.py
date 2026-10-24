"""Whole original AI movement phases, fixed-point rules and evidence corruption."""
from copy import deepcopy
import gzip
import json
import unittest
from tools.battle_unit_movement import Model, corpus
from tools.battle_unit_movement_emulation import ROOT, UNIT, CTRL, MovementMachine, source_contract, sha
from tools.battle_unit_movement_verification import verify_case

REPORT = 'analysis/battle-unit-movement-source-v1-20261024.json.gz'
REPORT_SHA = '32a42d9b89bb4a2ef1143d9c1cfaa63b578c8c38e8612d445b430a04474b97de'


class MovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw) != REPORT_SHA: raise ValueError('frozen source movement matrix')
        cls.report=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.report['cases']}

    def bad(self,fn,replay=False):
        row=deepcopy(self.rows['blocking_wall']);fn(row)
        with self.assertRaises(ValueError):verify_case(row,replay)

    def test_original_source_and_declared_corpus(self):
        self.assertEqual(self.report['source_contract'],source_contract())
        self.assertEqual([r['input'] for r in self.report['cases']],corpus())
        self.assertEqual(len(self.rows),21)

    def test_every_AI_call_matches_complete_independent_unit(self):
        for row in self.rows.values():
            with self.subTest(case=row['input']['name']):verify_case(row,False)

    def test_fresh_complete_original_AI_and_memory(self):verify_case(self.rows['wall_detour'],True)

    def test_all_eight_directions_reach_source_arrival(self):
        for i in range(8):self.assertEqual(self.rows['direction_'+str(i)]['stop'],'arrived')

    def test_slow_unit_keeps_real_frame_budget(self):
        row=self.rows['speed_1'];self.assertEqual((row['stop'],len(row['steps'])),('frame_budget',128))
        self.assertGreater(row['original_coordinate_write_count'],0)

    def test_speed_changes_elapsed_AI_calls(self):
        self.assertGreater(len(self.rows['speed_100']['steps']),len(self.rows['speed_999']['steps']))

    def test_half_scale_and_terrain_rate(self):
        self.assertGreater(len(self.rows['half_scale']['steps']),len(self.rows['direction_3']['steps']))
        self.assertGreater(len(self.rows['terrain_25']['steps']),len(self.rows['terrain_200']['steps']))

    def test_original_AI_consumes_multiple_segments(self):
        row=self.rows['wall_detour'];proof=verify_case(row,False)
        self.assertGreater(proof['helper_events']['segment'],1)
        self.assertEqual(proof['final_cursor'],proof['path_points'])

    def test_search_success_does_not_override_blocked_next_tile(self):
        row=self.rows['blocking_wall'];self.assertEqual(row['roots'][1]['result'],1)
        self.assertEqual((row['stop'],row['original_coordinate_write_count']),('next_tile_blocked',0))

    def test_missing_occupant_owner_stays_stationary(self):
        row=self.rows['missing_occupant_owner'];self.assertEqual(row['stop'],'frame_budget')
        self.assertEqual(row['original_coordinate_write_count'],0)

    def test_actual_friendly_occupant_speed_branch(self):
        self.assertGreater(len(self.rows['ally_speed_750']['steps']),len(self.rows['ally_speed_250']['steps']))

    def test_original_zero_terrain_rate_falls_back_to_fifty(self):
        c=deepcopy(corpus()[2]);c['name']='blocked_start';c['path']['grid'][3]='0001000';c['frames']=8
        verify_case(MovementMachine(c).run(),False)

    def test_empty_packet_source_fallback_reads_x_twice(self):
        c=deepcopy(corpus()[0]);m=MovementMachine(c)
        m.call(0x437C90,(UNIT+0x3E0,),0x10000000);m.call(0x47D930,(UNIT,))
        x=m.get(UNIT+0x2EC,'i')>>16
        self.assertEqual((m.get(UNIT+0x4D8,'h'),m.get(UNIT+0x4DA,'h')),(x*32+16,x*16+8))

    def test_invalid_scalar_inputs_rejected(self):
        for change in ({'speed':0},{'speed':True},{'terrain_rate':0},{'status':13},{'frames':513},{'blocker_speed':-1}):
            c=deepcopy(corpus()[0]);c.update(change)
            with self.assertRaises(ValueError):MovementMachine(c)

    def test_other_unit_write_guard(self):
        m=MovementMachine(corpus()[0])
        with self.assertRaises(ValueError):m.write_hook(m.uc,0,UNIT+0x520,4,0,None)

    def test_unrelated_AI_root_rejected(self):
        m=MovementMachine(corpus()[0])
        with self.assertRaises(ValueError):m.call(0x477980,(UNIT,))

    def test_wrong_stop_rejected(self):self.bad(lambda r:r.update(stop='arrived'))
    def test_fake_coordinate_claim_rejected(self):self.bad(lambda r:r.update(original_coordinate_write_count=2))
    def test_host_position_write_claim_rejected(self):self.bad(lambda r:r.update(host_unit_coordinates_changed_after_initialization=True))
    def test_discontinuous_unit_rejected(self):self.bad(lambda r:r['steps'][0].update(before_hex='00'+r['steps'][0]['before_hex'][2:]))
    def test_wrong_full_unit_output_rejected(self):self.bad(lambda r:r['steps'][0].update(after_hex='00'+r['steps'][0]['after_hex'][2:]))
    def test_wrong_AI_phase_rejected(self):self.bad(lambda r:r['steps'][0].update(phase=3))
    def test_host_helper_scheduling_rejected(self):self.bad(lambda r:r['steps'][0]['calls'][0].update(entry=0x47DA30))
    def test_wrong_AI_receiver_rejected(self):self.bad(lambda r:r['steps'][0]['calls'][0].update(receiver=0))
    def test_wrong_source_packet_rejected(self):self.bad(lambda r:r.update(path_hex='00'*236))
    def test_wrong_stack_rejected(self):self.bad(lambda r:r['steps'][0]['calls'][0].update(ESP_after=0))
    def test_callee_saved_register_corruption_rejected(self):self.bad(lambda r:r['steps'][0]['calls'][0]['cpu_after'].update(EBX=1))
    def test_missing_mapping_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_other_unit_or_map_corruption_rejected(self):self.bad(lambda r:r['final'][11].update(hex='01'+r['final'][11]['hex'][2:]))
    def test_instruction_trace_corruption_rejected(self):self.bad(lambda r:r.update(code_trace_sha256='0'*64),True)
    def test_write_trace_corruption_rejected(self):self.bad(lambda r:r.update(write_trace_sha256='0'*64),True)


if __name__ == '__main__':unittest.main()
