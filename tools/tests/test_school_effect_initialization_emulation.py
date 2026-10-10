import hashlib
import json
import struct
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_effect_initialization_emulation import (
    SchoolEffectInitializationEmulator,ROOT,ASSET_POOL,CHAR_BASE,UNITS,STACK)

EVIDENCE = ROOT/'analysis/school-effect-initialization-v1-20261010.json'
SHA = 'c48758d10d6fa1c88615f912db0db37fb682d1949dc063542953d2247c5de981'


class EffectNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text('utf-8'))

    def test_actual_school_cases_source_slot_and_stop(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),SHA)
        self.assertEqual([c['effect_initialized'] for c in self.data['cases']],[True,True,True,False,False])
        for c in self.data['cases'][:3]:
            self.assertEqual(c['effect_initialization']['texture_slot'],100)
            self.assertEqual(c['effect_graphics_input']['previous_slot_hex'],'0000000000000000')
            self.assertEqual(c['stop_reason'],'before_mapcom_resource_load')
            self.assertEqual(c['effect_initialization']['mapcom_request']['relative_path'],'data\\Tactics\\mapcom.bin')
            self.assertFalse(c['effect_initialization']['mapcom_request']['loaded'])
            visited = c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x41ebf0','0x41ec40','0x41f0e0','0x41f340','0x409ef0','0x409ff0',
                       '0x40a400','0x40a520','0x466500','0x4937a0','0x43a510'):
                self.assertIn(va,visited)
            for va in ('0x41efd0','0x4680b0','0x453540','0x468910'):
                self.assertNotIn(va,visited)

    def test_texture_count_owned_allocations_and_explicit_gpu_boundaries(self):
        for c in self.data['cases'][:3]:
            allocs = c['asset_allocations']
            self.assertEqual([a['bytes'] for a in allocs],[84,15662260,77212,164560])
            self.assertEqual([a['freed'] for a in allocs],[False,True,False,False])
            self.assertTrue(c['effect_initialization']['source_file_buffer_freed'])
            self.assertEqual(c['effect_initialization']['metadata_sha256'],c['unit_assets']['metadata_sha256'])
            self.assertEqual(c['effect_initialization']['texture_count'],1959)
            self.assertEqual(len(c['effect_entries']),1959)
            self.assertEqual(c['effect_vector']['native_constructors_completed'],1959)
            self.assertTrue(c['effect_vector']['iteration_outside_instruction_hook'])
            for kind in ('texture_creation','pixel_upload'):
                events = [e for e in c['effect_boundaries'] if e['kind']==kind]
                self.assertEqual([e['index'] for e in events],list(range(1959)))
            self.assertEqual(sum(e['kind']=='source_file_release' for e in c['effect_boundaries']),1)
            self.assertFalse(c['gpu_textures_uploaded'])

    def test_work_initialization_and_retention(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['live_witness'])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['current_combat_records_unchanged'])
            groups = c['effect_initialization']['groups']
            self.assertEqual([g['count'] for g in groups],[10,10,5])
            self.assertEqual(len(c['effect_work_calls']),28)
            for g in groups:
                for entry in g['entries']:
                    self.assertEqual(entry['used'],1)
                    self.assertEqual(entry['controller'],c['effect_initialization']['controller'])
                    raw = bytes.fromhex(entry['animation_work_hex'])
                    self.assertEqual(raw[0],1)
                    self.assertEqual(raw[12:14],b'\xff\xff')
                    self.assertEqual(raw[84:87],b'\x80'*3)
                    self.assertEqual(struct.unpack_from('<I',raw,36)[0],entry['animation_work_pointer'])
            initial = c['effect_initialization']['initial_animation']
            self.assertEqual(initial['instruction_hex'],'0000a8fffffff7ff0500')
            self.assertEqual(initial['duration'],5)
            self.assertEqual(initial['descriptor_value'],13)
            self.assertEqual(initial['current_instruction'],initial['instruction_pointer'])
        for c in self.data['cases'][3:]:
            self.assertEqual(c['effect_entries'],[])
            self.assertEqual(c['effect_boundaries'],[])
            self.assertIsNone(c['effect_initialization'])

    def test_guard_rejects_roles_other_slots_freed_buffers_and_assertions(self):
        e = SchoolEffectInitializationEmulator()
        e.bind_resources()
        e.effect_loading = True
        self.assertNotIn(0x56DDA0,e.effect_code)
        for p in (CHAR_BASE,UNITS,0x7CF34C,0x7A528E,ASSET_POOL,e.texture_table,e.texture_table+101*8):
            with self.assertRaises(RuntimeError):
                e._write_hook(e.uc,0,p,4,0,None)
        e._write_hook(e.uc,0,e.texture_table+100*8,8,0,None)
        p = e.asset_allocate(16,'guard_probe',0)
        e._write_hook(e.uc,0,p,4,0,None)
        e.asset_allocations[-1]['freed'] = True
        with self.assertRaises(RuntimeError):
            e._write_hook(e.uc,0,p,4,0,None)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        with self.assertRaises(RuntimeError):
            e._hook(e.uc,0x424F80,1,None)


if __name__ == '__main__':
    unittest.main()
