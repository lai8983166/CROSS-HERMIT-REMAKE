import hashlib
import json
import struct
import unittest
from tools.school_scene_resources_emulation import (SchoolSceneResourcesEmulator,ROOT,
    SCENE_NAMES,SCENE_POOL,SCENE_POOL_SIZE,map_resource,CHAR_BASE,UNITS,TASK)

EVIDENCE=ROOT/'analysis/school-scene-resources-v1-20261009.json'
SHA='81924937ded1ed70e5889dd068abe05e2479caf3c50210a9275bc3b7eb35abac'


class SceneResourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(EVIDENCE.read_text('utf-8'))

    def test_frozen_school_cases_order_handles_and_original_buffers(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),SHA)
        self.assertEqual([c['scene_resources_loaded'] for c in self.data['cases']],[True,True,True,False,False])
        for c in self.data['cases'][:3]:
            self.assertEqual([r['source']['relative_path'] for r in c['scene_requests']],list(SCENE_NAMES))
            self.assertEqual([r['caller_return_va'] for r in c['scene_requests']],['0x43a989','0x43aa6e','0x44e49b'])
            for r in c['scene_requests']:
                raw,identity=map_resource(r['source']['filename'])
                self.assertEqual(r['loaded_bytes'],len(raw));self.assertEqual(r['loaded_sha256'],identity['sha256'])
            opened=[e['result'] for e in c['file_events'] if e['name']=='CreateFileA']
            closed=[e['args'][0] for e in c['file_events'] if e['name']=='CloseHandle']
            self.assertEqual(len(opened),8);self.assertEqual(opened,closed)
            for e in c['file_events']:
                if e['name']=='CreateFileA':self.assertEqual(e['args'][1:],[0x80000000,1,0,3,1,0])

    def test_native_texture_minimap_fog_and_owned_allocations(self):
        for c in self.data['cases'][:3]:
            self.assertEqual(len(c['texture_entries']),632);self.assertEqual(len(c['gpu_boundaries']),1026)
            entries=[e for e in c['texture_entries'] if e['resource']>=5]
            self.assertEqual(len(entries),49)
            for e in entries[:48]:self.assertEqual([e['width'],e['height'],e['format']],[256,256,25])
            self.assertEqual([entries[-1]['width'],entries[-1]['height'],entries[-1]['format']],[172,128,25])
            fog=c['scene_resources']['fog'];self.assertEqual(fog['values'],[0x8000])
            self.assertEqual(fog['sha256'],hashlib.sha256(struct.pack('<H',0x8000)*22016).hexdigest())
            self.assertEqual(c['scene_boundaries'][-1]['sha256'],fog['sha256'])
            allocs=c['scene_allocations']
            self.assertEqual([a['bytes'] for a in allocs],[6293260,4036,23094,44032,44032,100888])
            self.assertEqual([a['freed'] for a in allocs],[True,False,True,False,False,False])
            for a in allocs:self.assertTrue(SCENE_POOL<=a['pointer']<a['pointer']+a['bytes']<=SCENE_POOL+SCENE_POOL_SIZE)
            self.assertEqual(c['scene_resources']['pathfinding']['pointer'],allocs[-1]['pointer'])
            self.assertEqual(c['scene_graphics_input']['declared_empty_texture_slot'],92)

    def test_refusal_retention_and_next_boundary(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertEqual(c['handoff']['before'],c['handoff']['after'])
            for flag in ('battle_world_constructed','gpu_textures_uploaded','live_witness','authorizes_persistent_write'):
                self.assertFalse(c[flag])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['current_combat_records_unchanged']);self.assertEqual(c['stop_reason'],'before_unit_art_reset')
            visited=[va for phase in c['phases'] for va in phase['coverage']['visited_function_entries']]
            for va in ('0x43a920','0x404b90','0x4404a0','0x440a10','0x440af0','0x440c10','0x44e440','0x44e4c0','0x44e5d0'):
                self.assertIn(va,visited)
        for c in self.data['cases'][3:]:
            self.assertEqual(c['scene_requests'],[]);self.assertIsNone(c['scene_resources'])

    def test_finite_scene_guard_denies_current_persistent_freed_and_outside(self):
        e=SchoolSceneResourcesEmulator();e.scene_loading=True;e.texture_table=TASK+0x844
        for address in (CHAR_BASE,UNITS,0x7CF34C,0x7A528E,SCENE_POOL):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,address,4,0,None)
        p=e.scene_allocate(16,'declared_test',0)
        e._write_hook(e.uc,0,p,4,1,None)
        with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p+15,4,0,None)
        e.scene_allocations[-1]['freed']=True
        with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p,4,0,None)
        with self.assertRaises(RuntimeError):e.scene_allocate(SCENE_POOL_SIZE+1,'declared_test',0)


if __name__=='__main__':unittest.main()
