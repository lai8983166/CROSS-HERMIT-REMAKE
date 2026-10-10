import hashlib
import json
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_current_units_emulation import (
    SchoolCurrentUnitsEmulator,ROOT,UNITCTRL,WORK_OFFSET,RECORD_OFFSET,CACHE_OFFSET,
    UNIT_POOL,ANIM_POOL,CONTROLLERS,CURRENT_ANIM,UNITS,CHAR_BASE,MAP_POOL,STACK)
EVIDENCE = ROOT/'analysis/school-current-units-v1-20261010.json'
EVIDENCE_SHA256 = '01cc487814a01ed2ad61c1f061b6b125ba587ff58fdd7957584bed525f1cd7ef'
CACHE_EVIDENCE = ROOT/'analysis/school-current-cache-reuse-v3-20261010.json'
CACHE_SHA256 = '487665ecb2fc353dbd827153ddb9cc1a2a6285f50cabd79f508963e20792eaed'


class CurrentUnitNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text('utf-8'));cls.cache = json.loads(CACHE_EVIDENCE.read_text('utf-8'))

    def test_actual_current_loops_all_units_and_enemy_stop(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([len(c['current_units']) for c in self.data['cases']],[3,2,2,0,0])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['current_units_constructed']);self.assertEqual(c['stop_reason'],'before_enemy_unit_construction')
            self.assertEqual([u['index'] for u in c['current_units']],list(range(len(c['current_units']))))
            self.assertEqual([u['role'] for u in c['current_units']],[3,4,9][:len(c['current_units'])])
            self.assertTrue(all(u['constructor_completed'] for u in c['current_units']))
            visited = c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x4680b0','0x451d80','0x465040','0x409ff0'):self.assertIn(va,visited)
            for va in ('0x453540','0x468910','0x41efd0'):self.assertNotIn(va,visited)
            self.assertFalse(c['current_loop']['enemy_constructor_executed']);self.assertFalse(c['current_loop']['scene_placement_executed'])
        for c in self.data['cases'][3:]:self.assertIsNone(c['current_loop'])

    def test_complete_resources_progress_handles_and_retention(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed']);self.assertFalse(c['live_witness'])
        for c in self.data['cases'][:3]:
            loop = c['current_loop'];units = c['current_units'];self.assertTrue(loop['retained_ranges_unchanged'])
            self.assertEqual(len(loop['progress']),len(units));self.assertEqual(len(loop['primitives']),3*len(units))
            self.assertEqual([u['texture_slot'] for u in units],list(range(110,110+len(units))))
            self.assertEqual(loop['counter'],110+len(units))
            cm = bytes.fromhex(loop['cm_hex']);self.assertEqual(cm[1],len(units));self.assertEqual(sum(cm),len(units))
            for u in units[1:]:
                self.assertFalse(u['cache_hit']);self.assertTrue(u['retained_ranges_unchanged'])
                count = {6:219,7:147}[u['job']];self.assertEqual(len(u['entries']),count)
                self.assertEqual(u['vector']['native_constructors_completed'],count)
                self.assertTrue(u['vector']['iteration_outside_instruction_hook'])
                self.assertEqual(len(u['clears']),11);self.assertEqual(len(bytes.fromhex(u['work_hex'])),1312)
                self.assertEqual(u['request']['loaded_sha256'],u['source']['sha256'])
                self.assertTrue(next(a for a in u['animation_allocations'] if a['kind']=='unit_file_buffer')['freed'])
                self.assertEqual(sum(b['kind']=='pixel_upload' for b in u['animation_boundaries']),count)
            opened = [e for e in c['file_events']+c['map_common']['file_events'] if e['name']=='CreateFileA']
            # Only mapcom's CreateFile is separate; its close is already shared.
            closed = [e for e in c['file_events'] if e['name']=='CloseHandle']
            self.assertEqual(len(opened),10+len(units));self.assertEqual(len(closed),len(opened))
            self.assertEqual(sorted(e['result'] for e in opened),sorted(e['args'][0] for e in closed))

    def test_declared_cache_reuse_is_separate_and_no_second_resource(self):
        d = self.cache
        self.assertEqual(hashlib.sha256(CACHE_EVIDENCE.read_bytes()).hexdigest(),CACHE_SHA256)
        self.assertEqual(d['evidence_kind'],'declared_two_identical_job6_records_native_cache_diagnostic')
        a,b = d['units'];self.assertFalse(a['cache_hit']);self.assertTrue(b['cache_hit'])
        self.assertEqual((a['controller'],a['metadata_pointer'],a['texture_slot']),(b['controller'],b['metadata_pointer'],b['texture_slot']))
        self.assertEqual(b['counter_before'],b['counter_after']);self.assertEqual(b['cache_before_hex'],b['cache_after_hex'])
        self.assertIsNone(b['request']);self.assertEqual(b['entries'],[]);self.assertEqual(b['animation_allocations'],[])
        self.assertEqual(len(d['controller_allocations']),1);self.assertEqual(len(d['animation_allocations']),3)
        self.assertEqual(sum(e['name']=='CreateFileA' for e in d['file_events']),1)
        self.assertEqual(bytes.fromhex(b['cm_hex'])[1],2);self.assertFalse(d['live_witness'])

    def test_guard_refuses_previous_freed_and_outside_phase_bytes(self):
        e = SchoolCurrentUnitsEmulator();e.current_loading=True
        for p in (UNITS,CHAR_BASE,MAP_POOL,UNIT_POOL,ANIM_POOL,CONTROLLERS,CURRENT_ANIM,UNITCTRL+WORK_OFFSET,UNITCTRL+RECORD_OFFSET,UNITCTRL+CACHE_OFFSET):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p,1,0,None)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for p in (0x424F80,0x41EFD0,0x56DDA0,0x428AD0,0x56D810,0x4500B0,0x428A40,0x56CEC0):
            with self.assertRaises(RuntimeError):e._hook(e.uc,p,1,None)


if __name__=='__main__':unittest.main()
