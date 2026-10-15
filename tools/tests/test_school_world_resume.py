import unittest
from copy import deepcopy
from tools.school_world_resume import *
from tools.school_world_idle_verification import phase_checked

class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.states=[phase_checked(n,'wait')[1] for n in ('initial','student9_waiting','fifth_class')]

    def test_last_enabled_then_paused_complete_world_projections(self):
        for state in self.states:
            last=world_project(state,182);paused=world_project(last['next_state'],183)
            self.assertEqual((last['prefix']['delay'],last['prefix']['action'],last['prefix']['controller_state']),(0,1,5))
            self.assertEqual((paused['prefix']['delay'],paused['prefix']['action'],paused['prefix']['controller_state']),(0,0,6))
            self.assertEqual(last['units']['after'][0]['hex'],paused['units']['after'][0]['hex'])
            for i in (1,5,6,10):self.assertEqual(last['units']['after'][i]['hex'],paused['units']['after'][i]['hex'])
            self.assertEqual(paused['unit_before'][2]['hex'],paused['units']['after'][2]['hex'])
            self.assertTrue(all(u['animation_frozen'] for u in paused['units']['units']))
            self.assertEqual([u['counter_after'] for u in last['units']['units'] if u['index']<3],[55,55]+([51] if len(last['units']['unit_indices'])==38 else []))
            effects=bytes.fromhex(paused['tail_after'][3]['hex']);self.assertTrue(all(get(effects,i*STRIDE+10)==183 for i in range(10)))

    def test_source_zero_test_precedes_decrement_and_busy_entry(self):
        s=source_contract();self.assertEqual(len(s['resume_instructions']),9);self.assertEqual(s['script']['sha256'],SCRIPT_SHA)
        self.assertEqual(s['resume_instructions'][0]['va'],'0x49a07d')

    def test_busy_script_identity_and_paused_boundary_refusal(self):
        state=self.states[0]
        for tick in (182,183):state=world_project(state,tick)['next_state']
        before=state['prefix_before'];task=bytes.fromhex(before[0]['hex']);inputs=dict(mouse=[0,0],busy=0,entry_receiver=before[0]['pointer'],script_pointer=u32(task,0x64),script_sha256=SCRIPT_SHA,script_bytes=SCRIPT.stat().st_size)
        self.assertEqual(preflight_boundary(inputs,before)['after'],before)
        for key,value in (('busy',1),('entry_receiver',0),('script_sha256','0'*64),('script_bytes',0)):
            bad=deepcopy(inputs);bad[key]=value
            with self.assertRaises(ValueError):preflight_boundary(bad,before)

    def test_wrong_delay_action_state_or_skipped_call_refused(self):
        for tick in (181,184,True,182.0,183):
            with self.assertRaises(ValueError):world_project(self.states[0],tick)
        for offset in (4,24,26,28):
            bad=deepcopy(self.states[0]);r=bad['prefix_before'][1];raw=bytearray.fromhex(r['hex']);raw[offset]^=1;r['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(bad,182)

    def test_paused_changed_record_or_moving_cell_refused(self):
        state=world_project(self.states[0],182)['next_state'];p=prefix_project(state['prefix_inputs'],state['prefix_before'],183);before=overlay(state['unit_before'],p['after']);slots=struct.unpack('<3I',bytes.fromhex(p['after'][3]['hex']));before[3]['pointer']=slots[1];before[3]['hex']=next(r['hex'] for r in p['after'] if r['pointer']==slots[1])
        bad=deepcopy(state['unit_inputs']);bad['units'][0]['record_hex']='00'
        with self.assertRaises(ValueError):units_project(bad,before,183)
        for offset in (0x4E7,):
            bad=deepcopy(before);raw=bytearray.fromhex(bad[0]['hex']);raw[offset]^=1;bad[0]['hex']=raw.hex()
            with self.assertRaises(ValueError):units_project(state['unit_inputs'],bad,183)

if __name__=='__main__':unittest.main()
