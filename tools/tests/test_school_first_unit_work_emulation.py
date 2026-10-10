import hashlib
import json
import struct
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_first_unit_work_emulation import (
    SchoolFirstUnitWorkEmulator,ROOT,UNITCTRL,UNIT_POOL,WORK_OFFSET,WORK_BYTES,
    RECORD_OFFSET,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,STACK,UNITS,CHAR_BASE,
    MAP_POOL,ASSET_POOL,TASK)

EVIDENCE = ROOT/'analysis/school-first-unit-work-v1-20261010.json'
EVIDENCE_SHA256 = 'ccca98bc858881706f3199384c27706300d9a9fa5e07b4a0dba0cef79a65b8a2'


class FirstUnitNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text('utf-8'))

    def test_actual_school_branches_and_original_request_boundary(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['first_unit_work_prefix_initialized'] for c in self.data['cases']],[True,True,True,False,False])
        for c in self.data['cases'][:3]:
            self.assertEqual(c['stop_reason'],'before_first_unit_animation_resource_load')
            w = c['first_unit_work']
            self.assertFalse(w['constructor_completed'])
            self.assertEqual(w['resource_request']['relative_path'],'data\\DxAnim\\d1a.bin')
            self.assertEqual(w['resource_request']['caller_return_va'],'0x464f1f')
            self.assertFalse(w['resource_request']['loaded'])
            self.assertEqual(w['resource_request']['args'][1:],[3,1,0])
            visited = c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x4680b0','0x46c040','0x474fb0','0x4750b0','0x475370','0x467020',
                       '0x466da0','0x466b40','0x466c80','0x466e90','0x464c60','0x464d70','0x464eb0'):
                self.assertIn(va,visited)
            for va in ('0x468690','0x468910','0x453540','0x41ebf0','0x4500b0'):
                self.assertNotIn(va,visited)
        for c in self.data['cases'][3:]:
            self.assertIsNone(c['first_unit_work'])

    def test_exact_owned_work_record_cache_and_controller_fields(self):
        for c in self.data['cases'][:3]:
            w = c['first_unit_work']
            work,record,controller = [bytes.fromhex(w[k]) for k in ('work_hex','record_hex','controller_hex')]
            self.assertEqual(len(work),WORK_BYTES)
            self.assertEqual(work[:4],b'\x01\x00\x00\x00')
            self.assertEqual(struct.unpack_from('<I',work,0x258)[0],w['record_pointer'])
            self.assertEqual(work[0x28A:0x28C],b'\x02\x02')
            self.assertEqual(work[0x290],25)
            self.assertEqual(work[0x501],255)
            self.assertEqual(record[0x9F:0xA1],b'\x02\0')
            self.assertEqual(record[0xA6:0xAE],b'\xff\xff'+bytes(6))
            self.assertEqual(w['before_work_hex'],'00'*WORK_BYTES)
            self.assertEqual(w['allocation']['pointer'],UNIT_POOL)
            self.assertEqual(w['allocation']['bytes'],84)
            self.assertFalse(w['allocation']['freed'])
            self.assertEqual(len(controller),84)
            self.assertEqual(struct.unpack_from('<I',controller,0x28)[0],110)
            self.assertEqual(struct.unpack_from('<I',controller,0x44)[0],TASK)
            self.assertEqual(struct.unpack_from('<H',controller,0x48)[0],18)
            self.assertEqual(w['counter'],111)
            cache = bytes.fromhex(w['cache_hex'])
            self.assertEqual(struct.unpack_from('<BBHI',cache),(1,3,10,UNIT_POOL))
            self.assertEqual(cache[8:],bytes(CACHE_COUNT*8-8))

    def test_explicit_primitives_and_upstream_retention(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['live_witness'])
        for c in self.data['cases'][:3]:
            w = c['first_unit_work']
            self.assertTrue(w['current_persistent_map_effect_bytes_unchanged'])
            self.assertEqual([e['bytes'] for e in w['boundaries'] if e['kind']=='clear'],[WORK_BYTES,92])
            self.assertEqual(sum(e.get('caller_return_va')=='0x466bb8' for e in w['boundaries']),1)
            self.assertEqual(sum(e['kind']=='debug_log' for e in w['boundaries']),1)
            self.assertFalse(c['gpu_textures_uploaded'])
            self.assertEqual(w['cache_input']['previous_counter'],110)
            self.assertEqual(w['cache_input']['previous_cache_hex'],'00'*(CACHE_COUNT*8))

    def test_finite_guard_rejects_other_work_current_and_retained_resources(self):
        e = SchoolFirstUnitWorkEmulator()
        e.first_unit_loading = True
        e.active_index = 0
        for address in (UNITS,CHAR_BASE,MAP_POOL,ASSET_POOL,UNIT_POOL,0x7A528E,TASK+0x844,
                        UNITCTRL+WORK_OFFSET+WORK_BYTES,UNITCTRL+CACHE_OFFSET+8):
            with self.assertRaises(RuntimeError):
                e._write_hook(e.uc,0,address,4,0,None)
        for address,count in ((UNITCTRL+WORK_OFFSET,WORK_BYTES),(UNITCTRL+RECORD_OFFSET,176),
                              (UNITCTRL+CACHE_OFFSET,8),(UNITCTRL+COUNTER_OFFSET,4)):
            e._write_hook(e.uc,0,address,count,0,None)
        e.unit_allocation = {'pointer':UNIT_POOL,'bytes':84,'freed':False}
        e._write_hook(e.uc,0,UNIT_POOL,84,0,None)
        e.unit_allocation['freed'] = True
        with self.assertRaises(RuntimeError):
            e._write_hook(e.uc,0,UNIT_POOL,1,0,None)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for address in (0x424F80,0x56DDA0,0x56CEC0,0x428A40,0x4500B0):
            with self.assertRaises(RuntimeError):
                e._hook(e.uc,address,1,None)


if __name__ == '__main__':
    unittest.main()
