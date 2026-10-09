import hashlib
import json
import struct
import unittest
from tools.school_adventure_handoff_emulation import (
    EVIDENCE, EVIDENCE_SHA256, ROOT, SOURCE, SOURCE_SHA256,
    SchoolAdventureHandoffEmulator, source_rules, exported_fixture)
from tools.tactics_exit_emulation import report_text

class SchoolAdventureHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_source_and_exports(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), SOURCE_SHA256)
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(), EVIDENCE_SHA256)
        for name,value in [('rules',source_rules()),('evidence',exported_fixture(self.data))]:
            self.assertEqual((ROOT/f'prototype/data/school_adventure_handoff_{name}.json').read_bytes(),report_text(value).encode())
        raw=bytes.fromhex(source_rules()['configuration_record_hex'])
        self.assertEqual(len(raw),42)
        self.assertEqual(struct.unpack_from('<H',raw)[0],5)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),source_rules()['configuration_record_sha256'])

    def test_actual_native_handoff_and_retained_records(self):
        self.assertEqual(self.data['upstream']['state_requests'],[6,9])
        self.assertTrue(self.data['upstream']['school_data_prepared'])
        for c in self.data['cases']:
            self.assertEqual(c['before'],c['after'])
            self.assertEqual(c['before']['school']['adventure_gate'],1)
            for key in ['combat_units_ready','resources_resolved','live_witness','authorizes_persistent_write']:
                self.assertFalse(c[key])
            if c['ready']:
                self.assertEqual(c['requested_states'],[10,16])
                self.assertEqual(c['ledger_after'],{'entries':[]})
                self.assertEqual([c['pending_flag'],c['pending_state']],[1,16])
                for phase,entry in [('commit','0x4a1920'),('group','0x4a6a10'),('dispatch10','0x4b9120'),('round','0x4b8ff0')]:
                    coverage=next(p['coverage'] for p in c['phases'] if p['phase']==phase)
                    self.assertIn(entry,coverage['visited_function_entries'])
                self.assertIn('0x4da860',c['phases'][-1]['coverage']['visited_function_entries'])
            else:
                self.assertEqual(c['requested_states'],[])
                self.assertEqual(c['phases'],[])
                self.assertEqual(c['ledger_before'],c['ledger_after'])
                self.assertIsNone(c['prepared'])
                self.assertIsNone(c['round_after'])

    def test_student_order_and_unresolved_unit_calls(self):
        for c,ids,groups in zip(self.data['cases'][:3],[[3,4,9],[3,4],[3,4]],[[0,0,0],[0,0],[4,4]]):
            r=c['prepared']['rounds'][0]
            self.assertEqual(r['student_ids'],ids)
            self.assertEqual(r['student_groups'],groups)
            self.assertEqual(r['teacher_ids'],[101])
            after=c['round_after']
            self.assertEqual(after['temp_roster'],ids+[-1]*(100-len(ids)))
            self.assertEqual([after['current'],after['total'],after['scene_id']],[1,1,5])
            self.assertEqual([after['temp_count'],after['combat_count']],[len(ids)]*2)
            calls=[(e['character_id'],e['ordinal']) for e in c['events'] if e['kind']=='unresolved_combat_unit_derivation']
            self.assertEqual(calls,list(zip(ids,range(len(ids)))))
            self.assertEqual(len([e for e in c['events'] if e['kind']=='unresolved_configuration_resources']),1)
            self.assertEqual(len([e for e in c['events'] if e['kind']=='scheduler_registration_boundary']),1)

    def test_ledger_is_derived_from_source_initialization(self):
        t=json.loads((ROOT/'prototype/data/school_fifth_planning_rules.json').read_text('utf-8'))['adventure_template']
        expected={'entries':[{'id':t['id'],'metadata':[t['kind']-1,t['ordinal']-1,0],'busy':0,
                             'limit':t['limit'],'duration':t['metadata'],'busy_elapsed':0,'elapsed':0}]}
        for c in self.data['cases']:
            self.assertEqual(c['ledger_before'],expected)

    def test_finite_guards_and_actual_ranges(self):
        e=SchoolAdventureHandoffEmulator.__new__(SchoolAdventureHandoffEmulator)
        e.writes=[]
        class CPU:
            def reg_read(self,register): return 0
        protected=[(0x7A528E,0x7A5292),(0x7CF34C,0x7CF34C+45*0x124),
                   (0x7E17E8,0x7F4488),(0x7F4518,0x7F4518+80*0xB0)]
        for stage in ['handoff_commit','handoff_group','handoff_dispatch','handoff_round']:
            e.stage=stage
            for a in [0x7A528E,0x7A5290,0x7CF34C,0x7E17E8,0x7F4518,0x9000000]:
                with self.assertRaisesRegex(RuntimeError,'finite guard'):
                    e._write_hook(CPU(),0,a,2,0,None)
            e._write_hook(CPU(),0,0x7A5662,2,0,None)
        e.stage='handoff_round'
        e._write_hook(CPU(),0,0x7A4AEC,2,3,None)
        e._write_hook(CPU(),0,0x7F4488,2,5,None)
        for c in self.data['cases']:
            for phase in c['phases']:
                for a,b in phase['coverage']['native_written_ranges']:
                    start,end=int(a,16),int(b,16)
                    for low,high in protected:
                        self.assertFalse(start<high and end>low)

if __name__ == '__main__':
    unittest.main()
