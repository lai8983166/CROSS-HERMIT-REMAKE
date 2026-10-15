import unittest
from copy import deepcopy
from tools.school_world_idle import *
from tools.school_world_idle_verification import parent_checked


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.states=[parent_checked(n)[1] for n in ('initial','student9_waiting','fifth_class')]

    def test_every_world_pending_mode_idle_terminal_and_final_delay(self):
        for initial in self.states:
            state=initial
            for tick in range(127,182):
                r=world_project(state,tick);friends=[a for a in r['units']['units'] if a['index']<3];after=bytes.fromhex(r['units']['after'][0]['hex'])
                self.assertEqual(r['prefix']['delay'],182-tick)
                for u in friends:
                    bind=132 if u['job']==9 else 128;at=u['index']*STRIDE
                    self.assertEqual(u['mode_requested'],tick==bind-1);self.assertEqual(u['mode_applied'],tick==bind);self.assertEqual(u['idle_bound'],tick==bind)
                    if tick==bind:self.assertEqual((u['mode_after'],u['previous_mode'],u['phase_after'],u['counter_after'],u['main_return']),(2,25,1,1,1));self.assertNotEqual(u32(after,at+0x4C),0)
                    if tick>=bind+1:self.assertEqual(u32(after,at+0x4C),0)
                    if tick>=bind:self.assertEqual(get(after,at+0x54),1)
                state=r['next_state']
            self.assertEqual(r['prefix']['delay'],1)
            self.assertEqual([(a['mode_after'],a['phase_after'],a['counter_after']) for a in friends],[(2,1,54),(2,1,54)]+([(2,1,50)] if len(friends)==3 else []))

    def test_job9_voice_reject_consumes_one_draw_and_recursive_residue(self):
        state=self.states[0]
        for t in (127,128):state=world_project(state,t)['next_state']
        r=world_project(state,129);u=r['units']['units'][2];v=u['voice'];self.assertFalse(v['selected']);self.assertEqual([d['value'] for d in v['draws']],[6906]);self.assertIsNone(v['audio_args']);self.assertEqual(u['released_nodes'],[POOL+5*NODE])
        before=bytes.fromhex(r['unit_before'][6]['hex']);after=bytes.fromhex(r['units']['after'][6]['hex']);n=bytearray(before[5*NODE:6*NODE]);n[0]=0;n[1]=0;self.assertEqual(after[5*NODE:6*NODE],n)

    def test_source_pose1_full_archive_mapping(self):
        s=source_contract()
        self.assertEqual({k:(v['pose'],v['code'],v['lookup_hex'],v['program']['duration'],v['program']['sprite']) for k,v in s['idle_poses'].items()},{'3':(1,4,'0400',1,383),'4':(1,4,'0400',1,659),'9':(1,4,'0400',1,263)})

    def test_wrong_pending_previous_phase_or_counter_refused(self):
        state=world_project(self.states[0],127)['next_state']
        for at in (0x290,0x291,0x292,0x293,10,6,7):
            bad=deepcopy(state)
            for rows in (bad['prefix_before'],bad['unit_before'],bad['tail_before']):
                for row in rows:
                    if row['name']=='works':
                        raw=bytearray.fromhex(row['hex']);raw[at]^=1;row['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(bad,128)

    def test_live_or_incomplete_path_manager_refused(self):
        for value in ('00',self.states[0]['unit_inputs']['path_manager_hex'][:192]+'01000000'):
            bad=deepcopy(self.states[0]);bad['unit_inputs']['path_manager_hex']=value
            with self.assertRaises(ValueError):world_project(bad,127)
        bad=deepcopy(self.states[0]);bad['unit_inputs']['path_manager_pointer']+=4
        with self.assertRaises(ValueError):world_project(bad,127)

    def test_modified_idle_bank0_controller_table_refused(self):
        state=world_project(self.states[0],127)['next_state'];bad=deepcopy(state);binding=bad['unit_inputs']['units'][0]['bindings'][0];raw=bytearray.fromhex(binding['controller_hex']);raw[4]^=1;binding['controller_hex']=raw.hex()
        with self.assertRaises(ValueError):world_project(bad,128)

    def test_modified_pose_after_binding_refused(self):
        state=self.states[0]
        for t in (127,128):state=world_project(state,t)['next_state']
        bad=deepcopy(state)
        for rows in (bad['prefix_before'],bad['unit_before'],bad['tail_before']):
            for row in rows:
                if row['name']=='works':
                    raw=bytearray.fromhex(row['hex']);raw[0x54]^=1;row['hex']=raw.hex()
        with self.assertRaises(ValueError):world_project(bad,129)

    def test_finite_tick_and_no_skipped_world(self):
        for t in (126,182,True,127.0,128):
            with self.assertRaises(ValueError):world_project(self.states[0],t)


if __name__=='__main__':unittest.main()
