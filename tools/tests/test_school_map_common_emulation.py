import hashlib
import json
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_map_common_emulation import (
    SchoolMapCommonEmulator,ROOT,MAP_POOL,MAP_POOL_SIZE,MAP_OWNER,MAP_SHA256,
    CHAR_BASE,UNITS,STACK,TASK,UNITCTRL,ASSET_POOL)

EVIDENCE = ROOT/'analysis/school-map-common-v1-20261010.json'
EVIDENCE_SHA256 = 'ccaf87f94cfb5c1382168f67af75ece728d8bbae7b6cc593cacbdc82ed08368c'


class MapCommonNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text('utf-8'))

    def test_actual_school_branches_and_constructor_stop(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['map_common_loaded'] for c in self.data['cases']],[True,True,True,False,False])
        for c in self.data['cases'][:3]:
            self.assertEqual(c['stop_reason'],'before_first_current_unit_work_constructor')
            request = c['current_constructor_input']
            self.assertEqual(request['va'],'0x4680b0')
            self.assertEqual(request['receiver'],UNITCTRL)
            self.assertFalse(request['body_executed'])
            visited = c['phases'][-1]['coverage']['visited_function_entries']
            self.assertIn('0x43a510',c['phases'][-2]['coverage']['visited_function_entries'])
            for va in ('0x4500b0','0x42ae20','0x42ac50','0x4214f0'):
                self.assertIn(va,visited)
            for va in ('0x4680b0','0x453540','0x468910'):
                self.assertNotIn(va,visited)
        for c in self.data['cases'][3:]:
            self.assertIsNone(c['map_common'])
            self.assertIsNone(c['current_record_preparation'])
            self.assertEqual(c['current_copies'],[])
            self.assertIsNone(c['current_constructor_input'])

    def test_read_only_buffer_pointers_and_closed_handles(self):
        for c in self.data['cases'][:3]:
            m = c['map_common']
            self.assertEqual(m['owner'],MAP_OWNER)
            self.assertEqual(m['allocation']['pointer'],MAP_POOL)
            self.assertEqual(m['allocation']['bytes'],69368)
            self.assertFalse(m['allocation']['freed'])
            self.assertEqual(m['request']['loaded_sha256'],MAP_SHA256)
            self.assertEqual(m['retained_buffer_sha256'],MAP_SHA256)
            self.assertEqual(m['open_handles'],0)
            self.assertEqual(len(m['top_level_pointers']),4)
            self.assertEqual(len(m['nested_pointers']),33)
            self.assertEqual(len(m['pointer_calls']),37)
            create = [e for e in m['file_events'] if e['name']=='CreateFileA']
            self.assertEqual(len(create),1)
            self.assertEqual(create[0]['args'][1:],[0x80000000,1,0,3,1,0])
            self.assertEqual(sum(e['name']=='CloseHandle' for e in m['file_events']),1)
            self.assertFalse(any('texture' in e['kind'] for e in m['boundaries']))

    def test_prepared_record_copy_and_persistent_effect_retention(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['live_witness'])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['map_common_persistent_and_effect_bytes_unchanged'])
            p = c['current_record_preparation']
            for before,after in zip(p['before_records'],p['after_records']):
                changed = [i for i,(a,b) in enumerate(zip(bytes.fromhex(before),bytes.fromhex(after))) if a!=b]
                self.assertTrue(set(changed) <= set(p['allowed_changed_offsets']))
            self.assertEqual(len(c['current_copies']),1)
            copy = c['current_copies'][0]
            self.assertEqual(copy['record_hex'],p['after_records'][copy['index']])
            self.assertEqual(copy['sha256'],hashlib.sha256(bytes.fromhex(copy['record_hex'])).hexdigest())
            self.assertEqual(copy['target'],UNITCTRL+0xD0C2C+copy['index']*176)
            self.assertEqual(copy['source'],UNITS+copy['index']*176)
            self.assertEqual(c['current_constructor_input']['index'],copy['index'])
            self.assertFalse(c['gpu_textures_uploaded'])

    def test_guard_rejects_persistent_other_current_fields_and_unowned_memory(self):
        e = SchoolMapCommonEmulator()
        e.map_loading = True
        e.combat_records = [{}]*3
        for p in (CHAR_BASE,UNITS,UNITS+0x14,0x7CF34C,0x7A528E,ASSET_POOL,
                  TASK+0x844,MAP_POOL,MAP_POOL+MAP_POOL_SIZE):
            with self.assertRaises(RuntimeError):
                e._write_hook(e.uc,0,p,4,0,None)
        e._write_hook(e.uc,0,UNITS+0xF,1,0,None)
        e._write_hook(e.uc,0,UNITS+0x24,4,0,None)
        e.map_allocation = {'pointer':MAP_POOL,'bytes':69368,'freed':False}
        e._write_hook(e.uc,0,MAP_POOL,69368,0,None)
        e.map_allocation['freed'] = True
        with self.assertRaises(RuntimeError):
            e._write_hook(e.uc,0,MAP_POOL,1,0,None)
        self.assertNotIn(0x56DDA0,e.map_code)
        self.assertNotIn(0x4680B0,e.map_code)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for address in (0x424F80,0x4680B0,0x56D4D0,0x56DDA0):
            with self.assertRaises(RuntimeError):
                e._hook(e.uc,address,1,None)


if __name__ == '__main__':
    unittest.main()
