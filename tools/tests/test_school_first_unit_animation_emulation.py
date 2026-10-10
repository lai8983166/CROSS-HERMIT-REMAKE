import hashlib
import json
import struct
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_first_unit_animation_emulation import (
    SchoolFirstUnitAnimationEmulator,ROOT,UNITCTRL,UNIT_POOL,WORK_OFFSET,WORK_BYTES,
    RECORD_OFFSET,CACHE_OFFSET,COUNTER_OFFSET,STACK,ANIM_POOL,ANIM_POOL_SIZE,
    UNITS,CHAR_BASE,MAP_POOL,ASSET_POOL,TASK,UNIT_SHA)
EVIDENCE = ROOT/'analysis/school-first-unit-animation-v1-20261010.json'
EVIDENCE_SHA256 = 'f929d55717a2ab6d2513db6834b455e73c1746b15d178e7588752143b0990c2f'


class FirstUnitAnimationNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text('utf-8'))

    def test_actual_school_branches_and_completed_resource_boundary(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['first_unit_animation_loaded'] for c in self.data['cases']],[True,True,True,False,False])
        for c in self.data['cases'][:3]:
            w = c['first_unit_animation']
            self.assertEqual(c['stop_reason'],'before_first_unit_animation_work_binding')
            self.assertTrue(w['request']['loaded'])
            self.assertEqual(w['request']['loaded_bytes'],916980)
            self.assertEqual(w['request']['loaded_sha256'],UNIT_SHA)
            self.assertFalse(w['unit_constructor_completed'])
            self.assertFalse(w['unit_animation_work_bound'])
            visited = c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x4500b0','0x4142b0','0x409b70','0x4214f0','0x41ec40','0x41f0e0','0x41f340','0x40b960'):
                self.assertIn(va,visited)
            for va in ('0x41efd0','0x409ef0','0x468690','0x453540','0x468910'):
                self.assertNotIn(va,visited)
        for c in self.data['cases'][3:]:
            self.assertIsNone(c['first_unit_animation'])
            self.assertEqual(c['unit_texture_entries'],[])

    def test_native_metadata_texture_vector_palette_and_controller(self):
        for c in self.data['cases'][:3]:
            w = c['first_unit_animation']
            self.assertEqual(w['metadata_bytes'],11476)
            self.assertEqual(len(bytes.fromhex(w['metadata_hex'])),11476)
            self.assertEqual(w['texture_slot'],110)
            self.assertEqual(w['texture_count'],193)
            self.assertEqual(w['mode_field'],1)
            self.assertEqual(w['vector']['count'],193)
            self.assertEqual(w['vector']['native_constructors_completed'],193)
            self.assertTrue(w['vector']['iteration_outside_instruction_hook'])
            entries = c['unit_texture_entries']
            self.assertEqual(len(entries),193)
            self.assertEqual(sum(e['palette_pointer']!=0 for e in entries),123)
            self.assertEqual(sum(e['mask_value']==1 for e in entries),70)
            for index,e in enumerate(entries):
                self.assertEqual(e['index'],index)
                self.assertEqual(len(bytes.fromhex(e['raw_record_hex'])),84)
                self.assertEqual(len(bytes.fromhex(e['upload_palette_hex'])),1024)
                self.assertEqual(e['record_pointer'],w['texture_records']+index*84)
            allocations = {a['kind']:a for a in w['allocations']}
            self.assertTrue(allocations['unit_file_buffer']['freed'])
            self.assertFalse(allocations['unit_metadata']['freed'])
            self.assertFalse(allocations['unit_texture_array']['freed'])
            self.assertEqual(allocations['unit_texture_array']['bytes'],193*84+4)
            self.assertEqual(w['file_release']['caller_return_va'],'0x409e5d')

    def test_readonly_closed_handles_gpu_boundaries_and_previous_retention(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['live_witness'])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['first_unit_animation_retained_ranges_unchanged'])
            self.assertFalse(c['gpu_textures_uploaded'])
            boundaries = c['unit_animation_boundaries']
            self.assertEqual(sum(e['kind']=='texture_creation' for e in boundaries),193)
            self.assertEqual(sum(e['kind']=='pixel_upload' for e in boundaries),193)
            self.assertEqual(boundaries[-1]['kind'],'source_file_release')
            opened = [e for e in c['file_events'] if e['name']=='CreateFileA']
            # Map common's original audit keeps its CreateFile event separately;
            # its size/close events are also in the shared upstream list.
            opened += [e for e in c['map_common']['file_events'] if e['name']=='CreateFileA']
            closed = [e for e in c['file_events'] if e['name']=='CloseHandle']
            self.assertEqual(len(opened),len(closed))
            self.assertEqual(len(opened),11)
            self.assertEqual(sorted(e['result'] for e in opened),sorted(e['args'][0] for e in closed))
            self.assertEqual([e for e in opened if e['result']==0xC00][0]['args'][1:],[0x80000000,1,0,3,1,0])

    def test_finite_guard_rejects_unowned_freed_and_previous_objects(self):
        e = SchoolFirstUnitAnimationEmulator()
        e.animation_loading = True
        e.texture_table = TASK+0x844
        for address in (UNITS,CHAR_BASE,MAP_POOL,ASSET_POOL,ANIM_POOL,UNIT_POOL+84,
                        UNITCTRL+WORK_OFFSET,UNITCTRL+RECORD_OFFSET,UNITCTRL+CACHE_OFFSET,
                        UNITCTRL+COUNTER_OFFSET,e.texture_table+100*8,e.texture_table+111*8):
            with self.assertRaises(RuntimeError):
                e._write_hook(e.uc,0,address,4,0,None)
        at = e.animation_allocate(128,'unit_file_buffer',0x42AD54)
        e._write_hook(e.uc,0,at,128,0,None)
        with self.assertRaises(RuntimeError):
            e._write_hook(e.uc,0,at+127,2,0,None)
        e.animation_allocations[0]['freed'] = True
        with self.assertRaises(RuntimeError):
            e._write_hook(e.uc,0,at,1,0,None)
        with self.assertRaises(RuntimeError):
            e.animation_allocate(ANIM_POOL_SIZE,'invalid',0)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for address in (0x424F80,0x41EFD0,0x4500B0,0x56DDA0,0x428AD0,0x56D810):
            with self.assertRaises(RuntimeError):
                e._hook(e.uc,address,1,None)


if __name__=='__main__':
    unittest.main()
