import hashlib
import json
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_scene_unit_work_emulation import (
    SchoolSceneUnitWorkEmulator,UNITCTRL,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,
    CACHE_OFFSET,COUNTER_OFFSET,SCENE_CONTROLLER,STACK)
from tools.school_scene_unit_work_emulation import ROOT

EVIDENCE=ROOT/'analysis/school-scene-unit-work-v1-20261010.json'
EVIDENCE_SHA256='74c4c43d8befdffcdaac206955956d919f1437e3a1ce808dbfc0a969b6e1d5e7'


class SceneUnitWorkNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.full=json.loads(EVIDENCE.read_text('utf-8'))

    def test_actual_school_boundary_refusal_and_native_calls(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['scene_unit_work_prefix_initialized'] for c in self.full['cases']],[True,True,True,False,False])
        for c in self.full['cases'][:3]:
            n=c['scene_unit_work'];self.assertEqual(c['stop_reason'],'before_first_scene_unit_animation_load')
            self.assertEqual((n['ordinal'],n['index'],n['role'],n['job'],n['category'],n['variant']),(0,249,5,4,7,5))
            self.assertEqual(n['constructor_entry']['caller_return_va'],'0x453630')
            self.assertEqual(n['resource_request']['relative_path'],'data\\DxAnim\\a1a.bin')
            seen=n['coverage']['visited_function_entries']
            for va in ('0x4680b0','0x474fb0','0x4750b0','0x4da710','0x467020','0x466c80','0x464d70'):self.assertIn(va,seen)
            for va in ('0x4500b0','0x467147','0x468910'):self.assertNotIn(va,seen)
            self.assertFalse(n['constructor_completed']);self.assertFalse(n['animation_loaded'])
        for c in self.full['cases'][3:]:self.assertIsNone(c['scene_unit_work'])

    def test_declared_all_templates_have_explicit_isolated_inputs(self):
        d=self.full['declared_scene_prefix_diagnostic'];units=d['units']
        self.assertEqual(len(units),35);self.assertEqual([n['index'] for n in units],list(range(249,214,-1)))
        self.assertFalse(d['school_enemy_loop_executed']);self.assertFalse(d['archives_loaded'])
        self.assertFalse(d['constructor_tails_executed'])
        for n in units:
            self.assertEqual(n['cache_before_hex'],'00'*4096);self.assertEqual(n['counter_before'],110)
            self.assertEqual(n['constructor_entry']['caller_return_va'],'0x3000000')
            self.assertEqual(n['classification_selector'],d['declared_inputs']['classification_selector'])
            self.assertEqual(n['relation_hex'],d['declared_inputs']['relation_hex'])
            self.assertEqual(n['cache_slot'],0);self.assertEqual(n['counter'],111)
            self.assertEqual([x['bytes'] for x in n['clears']],[1312,92])
            self.assertTrue(n['retained_ranges_unchanged'])
        self.assertEqual({n['mode'] for n in units},{0,1,2})
        self.assertEqual({bytes.fromhex(n['work_hex'])[0x290] for n in units},{2,11})

    def test_all_other_mapped_bytes_and_previous_file_events_retained(self):
        for c in self.full['cases']:
            self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed']);self.assertFalse(c['live_witness'])
        for c in self.full['cases'][:3]:
            n=c['scene_unit_work'];self.assertGreater(n['retained_bytes'],100_000_000)
            self.assertEqual(sum(x['bytes'] for x in n['retained_ranges']),n['retained_bytes'])
            self.assertTrue(n['retained_ranges_unchanged']);self.assertFalse(n['scene_vm_executed']);self.assertFalse(n['scene_placement_executed'])
            self.assertEqual(n['cache_slot'],len(c['current_units']))
            self.assertEqual(n['counter_before'],110+len(c['current_units']))
            self.assertEqual(sum(e['name']=='CloseHandle' for e in c['file_events']),10+len(c['current_units']))

    def test_guard_rejects_other_work_cache_source_and_loading(self):
        e=SchoolSceneUnitWorkEmulator();e.scene_work_loading=True
        work=UNITCTRL+WORK_OFFSET+249*WORK_BYTES;record=UNITCTRL+RECORD_OFFSET+249*176
        e.scene_work={'work_pointer':work,'record_pointer':record,'cache_pointer':UNITCTRL+CACHE_OFFSET+24,'allocation':None}
        for p in (work-1,work+WORK_BYTES,record-1,record+176,UNITCTRL+CACHE_OFFSET,
            UNITCTRL+COUNTER_OFFSET+4,SCENE_CONTROLLER,0x62AF80,0x7E17E8,0x17000000):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p,1,0,None)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for p in (0x424F80,0x468910,0x467147,0x409B70,0x403BD0,0x422360):
            with self.assertRaises(RuntimeError):e._hook(e.uc,p,1,None)


if __name__=='__main__':unittest.main()
