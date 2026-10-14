import json,unittest,struct
from copy import deepcopy
from tools.school_following_students import *

INPUTS=ROOT/'analysis/school-following-students-inputs-20261015.json'


class FollowingStudentSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cases=json.loads(INPUTS.read_bytes())['cases']

    def test_actual_source_jobs_and_distinct_archives_attachments(self):
        s=source_contract();self.assertEqual([s['jobs'][str(j)]['class'] for j in (4,9)],[6,7])
        self.assertEqual([s['jobs'][str(j)]['attachments'][1]['animation'] for j in (4,9)],[2104,2109])
        self.assertNotEqual(s['jobs']['4']['main_source']['sha256'],s['jobs']['9']['main_source']['sha256'])
        for job in s['jobs'].values():self.assertEqual([job['main']['duration']]+[p['duration'] for p in job['attachments']],[30,6,30])

    def test_three_full_unit_projections_preserve_records_and_other_units(self):
        for c,count in zip(self.cases,[2,1,1]):
            original=deepcopy(c['before']);out=project(c['inputs'],c['before']);self.assertEqual(c['before'],original)
            self.assertEqual(out['friendly_unit_updates_completed'],count);self.assertEqual(out['next_slot'],215);self.assertFalse(out['world_completed'])
            for i in (1,5,7,8):self.assertEqual(out['after'][i],original[i])
            self.assertEqual(out['after'][0]['hex'][:STRIDE*2],original[0]['hex'][:STRIDE*2])
            for u in out['units']:
                w=bytes.fromhex(out['after'][0]['hex'])[u['index']*STRIDE:(u['index']+1)*STRIDE]
                self.assertEqual(w[0x293],1);self.assertEqual(struct.unpack_from('<h',w,10)[0],1)
                self.assertEqual(u['frame_waits'],[29,4,28]);self.assertEqual(u['linked_order'],u['allocated_nodes'][::-1])

    def test_wrong_full_source_binding_status_queue_and_empty_interval_refuse(self):
        c=self.cases[0]
        for off in (0x292,0x293,0x2A7,0x518,0x510,0xA0+0x34):
            bad=deepcopy(c['before']);w=bytearray.fromhex(bad[0]['hex']);w[STRIDE+off]=1;bad[0]['hex']=w.hex()
            with self.assertRaises(ValueError):project(c['inputs'],bad)
        bad=deepcopy(c['inputs']);bad['units'][0]['bindings'][0]['metadata_sha256']='0'*64
        with self.assertRaises(ValueError):project(bad,c['before'])
        bad=deepcopy(c['before']);w=bytearray.fromhex(bad[0]['hex']);w[4*STRIDE]=1;bad[0]['hex']=w.hex()
        with self.assertRaises(ValueError):project(c['inputs'],bad)

    def test_complete_map_and_pool_exhaustion_refuse(self):
        c=self.cases[0];bad=deepcopy(c['inputs']);bad['map_all_bytes_verified']=16
        with self.assertRaises(ValueError):project(bad,c['before'])
        bad=deepcopy(c['before']);pool=bytearray.fromhex(bad[6]['hex'])
        for at in range(0,len(pool),NODE):pool[at]=1
        bad[6]['hex']=pool.hex()
        with self.assertRaises(ValueError):project(c['inputs'],bad)


if __name__=='__main__':unittest.main()
