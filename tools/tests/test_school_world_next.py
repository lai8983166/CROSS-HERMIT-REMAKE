import json,unittest
from copy import deepcopy
from tools.school_world_next import ROOT,source_contract,prefix_project,animation_project,clearing_project,put


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cases=json.loads((ROOT/'analysis/school-world-next-inputs-20261015.json').read_bytes())['cases']

    def test_actual_next_prefix_and_phase1_waits(self):
        self.assertEqual(source_contract()['source_image_sha256'],source_contract()['student']['source_image_sha256'])
        for c in self.cases:
            p=prefix_project(c['prefix_inputs'],c['prefix_before']);a=animation_project(c['animation_inputs'],c['animation_before'])
            self.assertEqual(p['delay'],179);self.assertEqual(a['frame_waits'],[28,27,3]);self.assertEqual(a['work_counter'],2)

    def test_refuse_skipped_wait_changed_gates_or_command(self):
        c=self.cases[0]
        for name,offset,value in [('control',28,0),('control',4,0),('task',0x170,1),('works',0x293,0),('queue',8,1)]:
            b=deepcopy(c['prefix_before']);r=next(r for r in b if r['name']==name);raw=bytearray.fromhex(r['hex']);raw[offset]=value;r['hex']=raw.hex()
            with self.assertRaises(ValueError):prefix_project(c['prefix_inputs'],b)

    def test_ended_roots_clear_pc_only_and_reject_children(self):
        for c in self.cases:
            for row in c['ended']:
                self.assertEqual(clearing_project(bytes.fromhex(row['before_hex'])).hex(),row['after_hex'])
                for at,value in [(8,1),(11,0),(32,1)]:
                    a=bytearray.fromhex(row['before_hex']);a[at]=value
                    with self.assertRaises(ValueError):clearing_project(a)

    def test_unproved_animation_expiry_or_link_rejected(self):
        c=self.cases[0]
        for kind in ('main_expiry','child_expiry','cycle','events'):
            b=deepcopy(c['animation_before']);w=bytearray.fromhex(b[0]['hex']);pool=bytearray.fromhex(b[6]['hex'])
            if kind=='main_expiry':put(w,0x48+14,1,'h')
            elif kind=='child_expiry':put(pool,14,1,'h')
            elif kind=='cycle':put(pool,32,0x765728)
            else:put(w,0x48+0x34,1)
            b[0]['hex']=w.hex();b[6]['hex']=pool.hex()
            with self.assertRaises(ValueError):animation_project(c['animation_inputs'],b)


if __name__=='__main__':unittest.main()
