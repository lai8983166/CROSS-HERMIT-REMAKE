import json,unittest
from copy import deepcopy
from tools.school_world_frames import *
from tools.school_world_countdown_verification import REPORTS,verify_case


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.states=[verify_case(c,'sound') for c in json.loads(REPORTS['sound'].read_bytes())['cases']]

    def test_source_schedules_and_no_same_call_regular_decrement(self):
        for state in self.states:
            for tick in range(7,16):
                r=world_project(state,tick);units=r['units']['units'];scene=next(u for u in units if u['index']==240)
                if tick==9:self.assertEqual(scene['main_wait'],6)
                if tick==15:self.assertEqual(scene['main_wait'],50)
                node=bytes.fromhex(r['units']['after'][6]['hex'])[:NODE]
                self.assertEqual(get(node,14),5-(tick-6) if tick<11 else 6-(tick-11))
                self.assertEqual(r['prefix']['delay'],182-tick);self.assertEqual(r['units']['idle_root_indices'],[217,247,248]);state=r['next_state']

    def test_finite_tick_bool_and_skipped_update_refused(self):
        for tick in (6,16,True,7.0):
            with self.assertRaises(ValueError):world_project(self.states[0],tick)
        with self.assertRaises(ValueError):world_project(self.states[0],8)

    def test_complete_program_pc_timer_and_sprite_layer_refused(self):
        for at in (4,14,0x18,0x28):
            state=deepcopy(self.states[0]);row=state['unit_before'][6];raw=bytearray.fromhex(row['hex']);raw[at]^=1;row['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(state,7)

    def test_cleared_root_and_inactive_template_cannot_reinitialize(self):
        for at in (217*STRIDE+0x4C,215*STRIDE+0x293):
            state=deepcopy(self.states[0]);raw=bytearray.fromhex(state['unit_before'][0]['hex']);raw[at]^=1
            for row in (state['unit_before'][0],state['prefix_before'][12]):row['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(state,7)

    def test_unexecuted_repeat_and_spawn_rejected_at_execution(self):
        s=source_contract();self.assertFalse(s['upcoming_repeat']['native_executed']);self.assertEqual(s['upcoming_repeat']['earliest_world'],65)
        self.assertEqual(get(schedule(s['programs']['main:383'],63),14),1)
        with self.assertRaises(ValueError):schedule(s['programs']['main:383'],64)
        for op in (1,3):
            aw=bytearray(NODE);put(aw,4,100)
            with self.assertRaises(ValueError):step_animation(aw,0,[dict(offset=100,opcode=op,frame_hex=(bytes([op])+bytes(9)).hex())])

    def test_same_call_sound_loop_differs_from_regular_frame_setup(self):
        program=source_contract()['programs']['attached:2063'];aw=schedule(program,6)
        self.assertEqual(u32(aw,4),8728);self.assertEqual(get(aw,14),5)
        aw=schedule(program,11);self.assertEqual(u32(aw,4),8738);self.assertEqual(get(aw,14),6)


if __name__=='__main__':unittest.main()
