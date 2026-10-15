import unittest
from copy import deepcopy
from tools.school_world_handoff import *
from tools.school_world_handoff_verification import parent_checked


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.states=[parent_checked(n)[1] for n in ('initial','student9_waiting','fifth_class')]

    def test_every_world_terminal_prior_completion_counter_and_recursive_cleanup(self):
        for initial in self.states:
            state=initial
            for tick in range(119,127):
                r=world_project(state,tick);friends=[u for u in r['units']['units'] if u['index']<3];before=bytes.fromhex(r['unit_before'][6]['hex']);after=bytes.fromhex(r['units']['after'][6]['hex'])
                self.assertEqual(r['prefix']['delay'],182-tick)
                for u in friends:
                    released=[POOL+(2*u['index']+1)*NODE] if tick==125 and u['job'] in (3,4) else []
                    self.assertEqual(u['released_nodes'],released)
                    if released:
                        at=released[0]-POOL;expected=bytearray(before[at:at+NODE]);expected[0]=0;expected[1]=0
                        self.assertEqual(after[at:at+NODE],expected)
                        self.assertEqual((u['phase_after'],u['counter_after']),(2,125));self.assertEqual(u['linked_order'],[])
                    if tick==124 and u['job'] in (3,4):self.assertEqual((u['main_return'],u['phase_after'],u['counter_after']),(1,1,123))
                    if tick==126 and u['job'] in (3,4):self.assertEqual((u['main_return'],u['phase_after'],u['counter_after']),(1,3,1))
                    if u['job']==9:self.assertEqual((u['phase_after'],u['counter_after']),(1,tick-1))
                state=r['next_state']

    def test_source_rng_and_exact_event125_contract(self):
        self.assertEqual(random_step(1),(2745024,41));self.assertEqual(random_step(0xFFFFFFFF),(2531011-214013,(2531011-214013)>>16))
        s=source_contract();self.assertEqual(s['voice'],dict(event=125,kind=2,first_threshold=60,voice=4,second_draw_consumed=True))
        for seed in (True,-1,2**32,1.0):
            with self.assertRaises(ValueError):random_step(seed)

    def test_voice_threshold_and_second_draw_consumption_preserve_other_thread_bytes(self):
        for rem in (59,60):
            seed=next(s for s in range(10000) if random_step(s)[1]%100==rem);thread=bytearray([19])*4096;put(thread,20,seed);before=bytes(thread)
            event=voice_project(thread,3);self.assertEqual(event['selected'],rem==60);self.assertEqual(len(event['draws']),2 if rem==60 else 1)
            self.assertEqual(thread[:20],before[:20]);self.assertEqual(thread[24:],before[24:]);self.assertEqual(event['audio_args'],[9,4,12,0] if rem==60 else None)

    def test_wrong_phase_counter_or_prior_completion_refused(self):
        for at in (4,10,0x293):
            bad=deepcopy(self.states[0])
            for regions in (bad['prefix_before'],bad['unit_before'],bad['tail_before']):
                for r in regions:
                    if r['name']=='works':
                        raw=bytearray.fromhex(r['hex']);raw[at]^=1;r['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(bad,119)
        state=self.states[0]
        for t in range(119,125):state=world_project(state,t)['next_state']
        for at in (2,0x1C,0x24,0x20):
            bad=deepcopy(state);r=bad['unit_before'][6];raw=bytearray.fromhex(r['hex']);raw[NODE+at]^=1;r['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(bad,125)

    def test_complete_parent_bound_thread_region_required(self):
        for field,value in (('pointer',TLS+4),('bytes',4095),('hex','00')):
            bad=deepcopy(self.states[0]);bad['unit_before'][-1][field]=value
            with self.assertRaises(ValueError):world_project(bad,119)

    def test_finite_world_order(self):
        for t in (118,127,True,119.0,120):
            with self.assertRaises(ValueError):world_project(self.states[0],t)


if __name__=='__main__':unittest.main()
