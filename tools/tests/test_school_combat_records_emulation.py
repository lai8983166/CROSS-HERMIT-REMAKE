import hashlib
import json
import unittest
from tools.school_combat_records_emulation import (
    ROOT,SOURCE,SOURCE_SHA256,EVIDENCE,EVIDENCE_SHA256,UNITS,WORK_SIZE,
    SchoolCombatRecordsEmulator,source_rules,fixture)
from tools.tactics_exit_emulation import report_text


class SchoolCombatRecordsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(EVIDENCE.read_text('utf-8'))

    def test_independent_source_and_frozen_exports(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA256)
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        for name,value in [('rules',source_rules()),('evidence',fixture(self.data))]:
            self.assertEqual((ROOT/f'prototype/data/school_combat_records_{name}.json').read_bytes(),report_text(value).encode())
        rules=source_rules()
        for entry in rules['jobs']+rules['skills']:
            raw=bytes.fromhex(entry['record_hex'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),entry['record_sha256'])
        self.assertTrue(all(s['modifier_callback']==0 for s in rules['skills']))
        changed=json.loads(report_text(self.data)); changed['cases'][0]['ready']=False
        with self.assertRaisesRegex(ValueError,'frozen'):fixture(changed)

    def test_actual_native_records_and_retention(self):
        for c in self.data['cases']:
            self.assertEqual(c['before'],c['after'])
            self.assertEqual(c['before']['school']['adventure_gate'],1)
            self.assertEqual(c['combat_records_prepared'],c['ready'])
            self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['resource_loading_executed'])
            self.assertFalse(c['resources_resolved'])
            self.assertFalse(c['live_witness'])
            self.assertFalse(c['authorizes_persistent_write'])
            if c['ready']:
                self.assertEqual(c['requested_states'],[10,16])
                self.assertEqual(c['pending_state'],16)
                self.assertEqual(c['work_resets'],[{'target':'0x8093f8','count':WORK_SIZE,'caller_return_va':'0x4dab39'}])
                entries=c['phases'][-1]['coverage']['visited_function_entries']
                for va in ['0x4b9340','0x4b93c0','0x4db340','0x4dcf00','0x4dab10','0x56cfcc']:
                    self.assertIn(va,entries)
            else:
                self.assertEqual(c['combat_records'],[])
                self.assertEqual(c['work_resets'],[])
                self.assertEqual(c['requested_states'],[])

    def test_owned_order_defined_output_and_modifier_slots(self):
        for c,ids in zip(self.data['cases'][:3],[[3,4,9],[3,4],[3,4]]):
            self.assertEqual([r['input']['character_id'] for r in c['combat_records']],ids)
            for ordinal,r in enumerate(c['combat_records']):
                self.assertEqual(r['ordinal'],ordinal)
                self.assertEqual(r['destination'],UNITS+ordinal*0xB0)
                self.assertEqual(r['input']['equipped_items'],[0]*8)
                self.assertEqual(r['limits']['character_id'],ids[ordinal])
                self.assertEqual(len(bytes.fromhex(r['raw_record_hex'])),176)
                self.assertTrue(set(range(2,11)).issubset(r['defined_offsets']))
                self.assertTrue(set(range(20,40)).issubset(r['defined_offsets']))
                self.assertTrue(all(0<=x<176 for x in r['defined_offsets']))
                mod=bytes.fromhex(r['modifier_hex'])
                self.assertEqual(len(mod),76)
                self.assertEqual(mod[:24]+mod[26:],bytes(74))

    def test_counterfactual_clamps_and_floating_truncation(self):
        a,b,c=self.data['counterfactuals']
        self.assertEqual(a['record']['limits']['attributes'],[1,135,1,135,50,135,1])
        self.assertEqual(a['record']['limits']['level'],99)
        self.assertEqual(a['record']['limits']['engage_initial'],32400)
        self.assertEqual([b['record']['limits'][k] for k in ['hp_max','mp_max','hp_recovery','mp_recovery','engage_initial']],[6,5,223,358,1])
        self.assertEqual([c['record']['limits'][k] for k in ['hp_max','mp_max','hp_recovery','mp_recovery']],[708,877,67,37])
        for probe in self.data['counterfactuals']:
            self.assertEqual(probe['declared_counterfactual_input'],probe['record']['input'])

    def test_finite_guard_protects_other_ordinals_and_persistent_records(self):
        e=SchoolCombatRecordsEmulator.__new__(SchoolCombatRecordsEmulator)
        e.stage='handoff_round';e.writes=[];e.record_writes=[]
        e.current_combat={'destination':UNITS}
        class CPU:
            def reg_read(self,register):return 0
        e._write_hook(CPU(),0,UNITS+20,2,1,None)
        self.assertEqual(e.record_writes,[(UNITS+20,2)])
        for address in [UNITS+176,UNITS+175,0x7E17E8,0x7A528E,0x7CF34C,0x9000000]:
            with self.assertRaises(RuntimeError):e._write_hook(CPU(),0,address,2,0,None)


if __name__=='__main__':unittest.main()
