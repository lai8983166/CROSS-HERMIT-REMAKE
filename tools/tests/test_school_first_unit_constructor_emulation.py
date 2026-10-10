import hashlib
import json
import struct
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_first_unit_constructor_emulation import (
    SchoolFirstUnitConstructorEmulator,ROOT,WORK_BYTES,WORK_OFFSET,RECORD_OFFSET,UNITCTRL,
    SHARED_OFFSET,SHARED_BYTES,STACK,UNIT_POOL,ANIM_POOL,MAP_POOL,CHAR_BASE,UNITS,CACHE_OFFSET)
EVIDENCE = ROOT/'analysis/school-first-unit-constructor-v2-20261010.json'
EVIDENCE_SHA256 = '406331ecf5f8441f17d56a34a0324a16c9be9c68f610b208e532f3a7a8faf921'


class FirstUnitConstructorNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text('utf-8'))

    def test_exact_actual_school_cases_and_natural_return(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['first_unit_constructor_completed'] for c in self.data['cases']],[True,True,True,False,False])
        for c in self.data['cases'][:3]:
            w = c['first_unit_constructor']
            self.assertEqual(c['stop_reason'],'after_first_unit_constructor_return')
            self.assertEqual((w['return_va'],w['return_eax']),('0x4533fa',0))
            self.assertTrue(w['constructor_completed']);self.assertTrue(w['unit_animation_work_bound'])
            self.assertFalse(w['scene_placement_executed'])
            visited = c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x409ef0','0x409ff0','0x465040','0x46bd30','0x468690','0x43c470','0x480f50','0x437c90'):
                self.assertIn(va,visited)
            for va in ('0x4680b0','0x453540','0x468910','0x4500b0','0x56dda0'):
                self.assertNotIn(va,visited)
        for c in self.data['cases'][3:]:self.assertIsNone(c['first_unit_constructor'])

    def test_original_action_and_exact_owned_clear_calls(self):
        for c in self.data['cases'][:3]:
            w = c['first_unit_constructor'];calls = w['calls']
            select = [x for x in calls if x['va']=='0x465040']
            self.assertEqual(len(select),1);self.assertEqual(select[0]['args'],[w['work_pointer']+0x48,18,2])
            anim = [x for x in calls if x['va']=='0x409ff0']
            self.assertEqual(anim[0]['args'],[w['work_pointer']+0x48,0,89,0])
            coords = next(x for x in calls if x['va']=='0x468690')['args']
            self.assertEqual([v&0xFFFF for v in coords[1:]],[0,0])
            self.assertEqual(len(w['clears']),9)
            self.assertEqual(sum(x['bytes']==88 for x in w['clears']),6)
            self.assertEqual(sum(x['bytes']==236 for x in w['clears']),2)
            self.assertEqual([x['bytes'] for x in w['clears'] if x['target']==w['shared_pointer']],[42])
            self.assertEqual(len(bytes.fromhex(w['work_hex'])),WORK_BYTES)

    def test_single_map_counter_mutation_and_resource_retention(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['live_witness'])
        for c in self.data['cases'][:3]:
            w = c['first_unit_constructor']
            self.assertTrue(w['retained_ranges_unchanged']);self.assertFalse(c['gpu_textures_uploaded'])
            self.assertEqual(w['constructor_coordinates'],[0,0])
            self.assertEqual(w['record_hex'],c['first_unit_work']['record_hex'])
            self.assertEqual(w['cm_pointer'],c['logical_map']['cm_pointer'])
            self.assertEqual((w['cm_data_pointer'],w['cm_bytes']),
                             (c['logical_map']['scratch'][0]['pointer'],c['logical_map']['scratch'][0]['bytes']))
            before,after = bytes.fromhex(w['before_cm_hex']),bytes.fromhex(w['cm_hex'])
            self.assertEqual([(i,a,b) for i,(a,b) in enumerate(zip(before,after)) if a!=b],[(1,0,1)])
            self.assertEqual(hashlib.sha256(after).hexdigest(),w['cm_sha256'])
            self.assertEqual(bytes.fromhex(w['shared_hex']),b'\0\0'+b'\xff\xff'*20)
            raw = bytes.fromhex(w['work_hex'])
            self.assertEqual(struct.unpack_from('<II',raw,0x2EC),(16<<16,8<<16))
            self.assertEqual(struct.unpack_from('<H',raw,0x4FE)[0],900)

    def test_finite_guard_and_undeclared_boundaries_refuse(self):
        e = SchoolFirstUnitConstructorEmulator();e.constructor_loading=True;e.active_index=0;e.constructor_cell=0xE500001
        for p in (UNITS,CHAR_BASE,MAP_POOL,UNIT_POOL,ANIM_POOL,UNITCTRL+RECORD_OFFSET,UNITCTRL+CACHE_OFFSET,
                  UNITCTRL+WORK_OFFSET+WORK_BYTES,UNITCTRL+SHARED_OFFSET+SHARED_BYTES,e.constructor_cell-1,e.constructor_cell+1):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p,1,0,None)
        e._write_hook(e.uc,0,e.constructor_cell,1,1,None)
        with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,e.constructor_cell,2,1,None)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for p in (0x424F80,0x428A40,0x428AD0,0x56DDA0,0x4500B0,0x56CEC0,0x4533FA):
            with self.assertRaises(RuntimeError):e._hook(e.uc,p,1,None)


if __name__=='__main__':unittest.main()
