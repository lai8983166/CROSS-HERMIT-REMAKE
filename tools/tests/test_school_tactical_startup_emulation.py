import hashlib
import json
import struct
import unittest
from tools.school_tactical_startup_emulation import (
    ROOT,SOURCE,SOURCE_SHA256,EVIDENCE,EVIDENCE_SHA256,TACT,TACT_SIZE,SCRIPT_WORK,
    SchoolTacticalStartupEmulator,source_rules,fixture,resource_identity)
from tools.tactics_exit_emulation import report_text


class SchoolTacticalStartupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(EVIDENCE.read_text('utf-8'))

    def test_source_tables_resources_and_frozen_exports(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA256)
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        for name,value in [('rules',source_rules()),('evidence',fixture(self.data))]:
            self.assertEqual((ROOT/f'prototype/data/school_tactical_startup_{name}.json').read_bytes(),report_text(value).encode())
        r=source_rules();self.assertEqual(r['selected_name'],'TactStart05.bin')
        image=SOURCE.read_bytes();pointer=struct.unpack_from('<I',image,0x60C2B8-0x400000+20)[0]
        self.assertEqual(hex(pointer),r['selected_pointer'])
        for resource in r['resources']:
            raw=(ROOT/resource['local_file']).read_bytes()
            self.assertEqual(len(raw),resource['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),resource['sha256'])
            self.assertFalse(resource['loader_executed'])
        with self.assertRaises(ValueError):resource_identity('data\\Tactics\\TactStart\\TactStart5.bin')

    def test_actual_pending16_dispatch_and_outer_constructor(self):
        for c in self.data['cases']:
            self.assertEqual(c['handoff']['before'],c['handoff']['after'])
            self.assertTrue(c['persistent_ranges_unchanged'])
            for flag in ['subcomponents_constructed','resources_loaded','battle_world_constructed','live_witness','authorizes_persistent_write']:
                self.assertFalse(c[flag])
            if c['ready']:
                self.assertEqual(c['pending_flag'],0)
                self.assertEqual([x['size'] for x in c['allocations']],[TACT_SIZE,0x24C4])
                task=c['task_after']
                self.assertEqual([task['vtable'],task['active'],task['phase'],task['field_180']],['0x59a430',1,0,4])
                self.assertEqual(task['world_task_pointer'],hex(TACT))
                self.assertEqual(task['unitctrl_task_pointer'],hex(TACT))
                self.assertEqual(task['script_work_pointer'],hex(SCRIPT_WORK))
                entries=c['phases'][0]['coverage']['visited_function_entries']
                for va in ['0x451080','0x451170','0x439ef0','0x496b30','0x496bc0']:
                    self.assertIn(va,entries)
                self.assertTrue(any(e.get('name')=='unitctrl_subconstructor' for e in c['events']))
            else:
                self.assertEqual(c['allocations'],[]);self.assertEqual(c['phases'],[])
                self.assertIsNone(c['task_after']);self.assertEqual(c['normalized_students'],[])
                self.assertIsNone(c['common_request']);self.assertIsNone(c['independent_start_request'])

    def test_script_work_setup_and_native_current_unit_normalization(self):
        for c in self.data['cases'][:3]:
            task=c['task_after']
            self.assertEqual(task['script_indices'],[{'slot':i,'active':0,'unit':-1} for i in range(100)])
            self.assertEqual(task['script_counts'],[0,0,0]);self.assertEqual(task['unitctrl_mode'],0)
            self.assertEqual(task['loading_color'],[255]*3)
            for record,original in zip(c['normalized_students'],c['handoff']['combat_records']):
                self.assertEqual(record['character_id'],original['input']['character_id'])
                self.assertEqual(record['hp'],original['limits']['hp'])
                self.assertEqual(record['mp'],original['limits']['mp'])
                self.assertEqual(record['level'],min(original['limits']['level'],50))
                raw=bytes.fromhex(record['raw_record_hex'])
                self.assertEqual(len(raw),176)
                self.assertEqual(raw[0x63:0x66],bytes(3))
                self.assertEqual(raw[0x9B:0xA4],bytes(9))
            entries=c['phases'][1]['coverage']['visited_function_entries']
            for va in ['0x451670','0x452040','0x452130','0x452cf0','0x451b10']:
                self.assertIn(va,entries)

    def test_natural_resource_boundary_is_distinct_from_independent_probe(self):
        for c in self.data['cases'][:3]:
            common=c['common_request'];start=c['independent_start_request']
            self.assertEqual(common['probe_kind'],'natural_startup_first_resource')
            self.assertEqual(start['probe_kind'],'independent_current_scene_selection')
            self.assertEqual(common['caller_return_va'],'0x451b3d')
            self.assertEqual(start['caller_return_va'],'0x451c4f')
            self.assertEqual(common['resource'],source_rules()['resources'][0])
            self.assertEqual(start['resource'],source_rules()['resources'][1])
            self.assertNotIn('0x451bf0',c['phases'][1]['coverage']['visited_function_entries'])
            self.assertIn('0x451bf0',c['phases'][2]['coverage']['visited_function_entries'])
            self.assertIn('0x451d10',c['phases'][2]['coverage']['visited_function_entries'])

    def test_finite_guard_rejects_persistent_and_outside_allocations(self):
        e=SchoolTacticalStartupEmulator.__new__(SchoolTacticalStartupEmulator)
        e.writes=[];e.startup_writes=[];e.combat_records=[{}]*3;e.stage='tactical_dispatch'
        class CPU:
            def reg_read(self,register):return 0
        e._write_hook(CPU(),0,TACT+0x34,4,0,None)
        for address in [TACT+TACT_SIZE-1,SCRIPT_WORK+0x24C4,0x7E17E8,0x7A528E,0x7CF34C,0x7F4518,0x9000000]:
            with self.assertRaisesRegex(RuntimeError,'finite guard'):e._write_hook(CPU(),0,address,2,0,None)
        e.stage='tactical_startup';e._write_hook(CPU(),0,0x7F4518+22,2,1,None)


if __name__=='__main__':unittest.main()
