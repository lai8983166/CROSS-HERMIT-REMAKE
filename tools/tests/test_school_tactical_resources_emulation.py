import hashlib
import json
import unittest
from tools.school_tactical_resources_emulation import (
    SchoolTacticalResourcesEmulator, ROOT, SOURCE, SOURCE_SHA256, RESOURCE_NAMES,
    RESOURCE_HASHES, original_resource, POOL, POOL_SIZE, TACT, TACT_SIZE, SCRIPT_WORK, TASK)

EVIDENCE=ROOT/'analysis/school-tactical-resources-v1-20261009.json'
EVIDENCE_SHA256='4c48078de40cd452b486292c5b7e17d08ea0319f39339281d3d1f4a710a30a42'


class SchoolTacticalResourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(EVIDENCE.read_text('utf-8'))

    def test_source_identity_and_actual_resource_order(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA256)
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        for name,sha in zip(RESOURCE_NAMES,RESOURCE_HASHES):
            raw,identity=original_resource(name)
            self.assertEqual(identity['sha256'],sha)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)
        with self.assertRaises(ValueError):original_resource('data\\Tactics\\MAP05.bin')
        for c in self.data['cases'][:3]:
            self.assertTrue(c['buffers_loaded'])
            self.assertEqual([r['source']['relative_path'] for r in c['requests']],list(RESOURCE_NAMES))
            self.assertEqual([r['caller_return_va'] for r in c['requests']],
                             ['0x451b3d','0x451c4f','0x45490d','0x454ff9'])
            for r in c['requests']:
                self.assertEqual(r['loaded_sha256'],r['source']['sha256'])
                self.assertEqual(r['loaded_bytes'],r['source']['bytes'])

    def test_original_file_loader_and_balanced_read_only_handles(self):
        for c in self.data['cases'][:3]:
            events=c['file_events']
            self.assertEqual(sum(e['name']=='CreateFileA' for e in events),4)
            self.assertEqual(sum(e['name']=='CloseHandle' for e in events),4)
            opened=[e['result'] for e in events if e['name']=='CreateFileA']
            closed=[e['args'][0] for e in events if e['name']=='CloseHandle']
            self.assertEqual(opened,closed)
            for e in events:
                if e['name']=='CreateFileA':self.assertEqual(e['args'][1:],[0x80000000,1,0,3,1,0])
                if e['name']=='ReadFile':self.assertEqual(e['args'][4],0)
            coverage=c['phases'][-1]['coverage']['visited_function_entries']
            for va in ['0x4500b0','0x42ae20','0x42ac50','0x41f0e0','0x41f830',
                       '0x4214f0','0x4048d0','0x404fb0','0x4548e0','0x454fa0']:
                self.assertIn(va,coverage)
            self.assertNotIn('0x4519c0',coverage)

    def test_texture_records_and_script_buffer_ownership(self):
        for c in self.data['cases'][:3]:
            entries=c['texture_entries']
            self.assertEqual(len(entries),583)
            self.assertEqual([sum(e['resource']==i for e in entries) for i in range(3)],[580,2,1])
            self.assertEqual(len(c['gpu_boundaries']),928)
            self.assertEqual([e['va'] for e in c['audio_boundaries']],['0x458ff0','0x459080'])
            self.assertEqual(c['graphics_input']['declared_empty_slots'],[20,90,91])
            allocations=c['resource_allocations']
            self.assertEqual([a['kind'] for a in allocations],
                ['file_buffer','texture_array','file_buffer','texture_array','file_buffer','texture_array','file_buffer'])
            self.assertEqual([a['freed'] for a in allocations],[True,False,True,False,True,False,False])
            for a in allocations:self.assertLessEqual(a['pointer']+a['bytes'],POOL+POOL_SIZE)
            self.assertEqual(c['scene_script']['pointer'],allocations[-1]['pointer'])
            self.assertEqual(c['scene_script']['sha256'],RESOURCE_HASHES[-1])
            self.assertEqual(c['stop_reason'],'before_first_tactical_phase_update')
            for e in entries:self.assertEqual(len(bytes.fromhex(e['raw_record_hex'])),84)

    def test_refusal_and_persistent_retention(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertEqual(c['handoff']['before'],c['handoff']['after'])
            for flag in ['gpu_textures_uploaded','unitctrl_constructed','battle_world_constructed',
                         'live_witness','authorizes_persistent_write']:
                self.assertFalse(c[flag])
        for c in self.data['cases'][3:]:
            self.assertFalse(c['ready']);self.assertFalse(c['buffers_loaded'])
            for key in ['requests','file_events','resource_allocations','texture_entries','gpu_boundaries','audio_boundaries','phases']:
                self.assertEqual(c[key],[])
            self.assertIsNone(c['scene_script']);self.assertIsNone(c['task_after'])

    def test_finite_guard_rejects_persistent_freed_and_outside_memory(self):
        e=SchoolTacticalResourcesEmulator.__new__(SchoolTacticalResourcesEmulator)
        e.loading=True;e.combat_records=[{}]*3;e.writes=[];e.startup_writes=[]
        e.texture_table=TASK+0x844
        e.resource_allocations=[{'pointer':POOL,'bytes':32,'freed':False}]
        class CPU:
            def reg_read(self,_):return 0
        e._write_hook(CPU(),0,POOL+30,2,1,None)
        for address in [POOL+31,POOL+32,TACT+TACT_SIZE-1,SCRIPT_WORK,0x7E17E8,0x7CF34C,0x7A528E,0x9000000]:
            with self.assertRaisesRegex(RuntimeError,'finite guard'):
                e._write_hook(CPU(),0,address,2,1,None)
        e.resource_allocations[0]['freed']=True
        with self.assertRaisesRegex(RuntimeError,'finite guard'):e._write_hook(CPU(),0,POOL,2,0,None)


if __name__=='__main__':unittest.main()
