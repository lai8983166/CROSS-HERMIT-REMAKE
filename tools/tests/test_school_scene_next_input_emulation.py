import hashlib,json,unittest
from tools.school_scene_next_input_emulation import (
 SchoolSceneNextInputEmulator,ROOT,UNITCTRL,TACT,SCENE_CONTROLLER,WORK_OFFSET,WORK_BYTES,
 RECORD_OFFSET,CACHE_OFFSET,STACK,UC_X86_REG_ESP)
EVIDENCE=ROOT/'analysis/school-scene-next-input-v1-20261010.json'
EVIDENCE_SHA256='b78b913b3d8ffe895a86675f8c77c9b630caafb731d58c40a66adb7262b58276'
CACHE=ROOT/'analysis/school-scene-cache-query-v1-20261010.json'
CACHE_SHA256='5de16b7c89e433595a6c103fc26fef82e8bcbb997804b3cfdfbc17740a665995'

class SceneNextInputNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full=json.loads(EVIDENCE.read_text('utf-8'));cls.cache=json.loads(CACHE.read_text('utf-8'))

    def test_actual_second_input_natural_progress_record_and_mode0_request(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['second_scene_input_prepared'] for c in self.full['cases']],[True,True,True,False,False])
        for c in self.full['cases'][:3]:
            r,p=c['second_scene_record'],c['second_scene_work']
            self.assertEqual((r['ordinal'],r['index'],r['identity']),(1,248,387))
            self.assertEqual((p['ordinal'],p['index'],p['role'],p['job'],p['variant'],p['mode']),(1,248,387,387,0,0))
            self.assertEqual(p['resource_request']['relative_path'],'data\\DxAnim\\51e.bin')
            self.assertEqual(p['resource_request']['args'][1:],[0,0,0])
            self.assertEqual(p['allocation']['pointer'],SCENE_CONTROLLER+96)
            self.assertEqual(p['constructor_entry']['caller_return_va'],'0x453630')
            self.assertEqual(c['scene_progress']['caller_return_va'],'0x453638')
            self.assertEqual([x['va'] for x in c['scene_progress']['primitives']],['0x451e20','0x415420','0x422360'])
            self.assertFalse(p['animation_loaded']);self.assertFalse(p['constructor_completed'])
            self.assertEqual(c['stop_reason'],'before_second_scene_unit_animation_load')
        for c in self.full['cases'][3:]:self.assertIsNone(c['second_scene_work'])

    def test_first_npc_current_units_files_and_all_other_mapped_bytes_preserved(self):
        old=json.loads((ROOT/'analysis/school-scene-unit-constructor-v1-20261010.json').read_text('utf-8'))
        for c,prior in zip(self.full['cases'],old['cases']):
            self.assertEqual(c['file_events'],prior['file_events'])
            self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed']);self.assertFalse(c['live_witness'])
        for c,prior in zip(self.full['cases'][:3],old['cases'][:3]):
            for key in ('work_hex','record_hex','shared_hex','cm_hex'):
                self.assertEqual(c['scene_unit_constructor'][key],prior['scene_unit_constructor'][key])
            for n in (c['second_scene_record'],c['second_scene_work'],c['scene_progress']):
                self.assertTrue(n['retained_ranges_unchanged']);self.assertGreater(n['retained_bytes'],100_000_000)
            self.assertEqual(c['second_scene_work']['cache_slot'],len(c['current_units'])+1)
            self.assertEqual(c['second_scene_work']['counter_before'],111+len(c['current_units']))

    def test_declared_queries_and_signed_duplicate_hole_full_boundaries(self):
        d=self.cache;self.assertEqual(hashlib.sha256(CACHE.read_bytes()).hexdigest(),CACHE_SHA256)
        self.assertEqual((len(d['queries']),d['hits'],d['misses']),(35,26,9))
        self.assertEqual(sum(q['declared_insertion'] is not None for q in d['queries']),9)
        self.assertFalse(d['controller_allocation_executed']);self.assertFalse(d['cache_binding_executed'])
        self.assertFalse(d['school_scene_loop_executed']);self.assertFalse(d['constructors_executed']);self.assertFalse(d['archives_loaded'])
        self.assertTrue(d['retained_ranges_unchanged'])
        for q in [*d['queries'],*d['boundary_probes']]:self.assertEqual(q['cache_hex'],q['cache_after_hex'])
        base=UNITCTRL+CACHE_OFFSET
        self.assertEqual([q['return_pointer'] for q in d['boundary_probes']],
                         [base+511*8,base+8,base+511*8,base+511*8,0,0])

    def test_write_guards_reject_first_npc_cache_and_other_records(self):
        e=SchoolSceneNextInputEmulator();e.next_loading=True;e.next_phase='cache_query'
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for at in (UNITCTRL+CACHE_OFFSET,SCENE_CONTROLLER,TACT+0x40):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
        for at in (0x466B40,0x4500B0,0x468910):
            with self.assertRaises(RuntimeError):e._hook(e.uc,at,1,None)
        e.next_phase='record';e.enemy_record={'record_pointer':UNITCTRL+RECORD_OFFSET+248*176,'identity':387}
        for at in (UNITCTRL+RECORD_OFFSET+249*176,UNITCTRL+WORK_OFFSET+249*WORK_BYTES,SCENE_CONTROLLER):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
        before=bytes(e.uc.mem_read(UNITCTRL+CACHE_OFFSET,4096+4))
        for cache in (None,b'',bytes(4097)):
            with self.assertRaises(ValueError):e.query(cache,4,5)
        for value in (True,'4',2**31,-2**31-1):
            with self.assertRaises(ValueError):e.query(bytes(4096),value,5)
        self.assertEqual(bytes(e.uc.mem_read(UNITCTRL+CACHE_OFFSET,4096+4)),before)

if __name__=='__main__':unittest.main()
