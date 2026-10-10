from collections import Counter
from copy import deepcopy
import json
import unittest
from tools.school_enemy_records_catalog import source_catalog,expected_record,expected_profile,native_fixture,EVIDENCE,COUNTER_EVIDENCE,ROOT,word


class EnemyRecordSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=source_catalog();cls.full=json.loads(EVIDENCE.read_text('utf-8'))

    def test_all_declared_and_actual_full_profiles_and_record_bytes(self):
        actual=[c['scene_unit_record'] for c in self.full['cases'][:3]]
        for n in [*self.full['declared_template_diagnostic']['records'],*actual]:
            e=expected_record(n['template_hex'],rules=self.rules)
            for k in ('profile_pointer','profile_hex','record_hex'):self.assertEqual(e[k],n[k],(n['ordinal'],k))
            if n['identity']<200:
                self.assertEqual(n['scratch_after_hex'],e['profile_hex'])
                original=self.rules['character_definitions'][str(n['identity'])]
                self.assertEqual(n['character_pointer'],original['pointer'])
                self.assertEqual(n['character_input_hex'],original['row_hex'])

    def test_source_selection_category_state_and_reverse_indices(self):
        r=self.rules;s=self.full['scene_inputs'];self.assertEqual(r['template_pointer'],s['pointer'])
        self.assertEqual(r['templates'],s['templates']);self.assertEqual(r['template_count'],35)
        self.assertEqual([x['index'] for x in self.full['declared_template_diagnostic']['records']],
            [r['unit_first_index']-i*r['unit_index_decrement'] for i in range(r['template_count'])])
        records=[bytes.fromhex(x['record_hex']) for x in self.full['declared_template_diagnostic']['records']]
        self.assertEqual(dict(Counter(x[15] for x in records)),{1:11,0:24})
        self.assertEqual(dict(Counter(x[164] for x in records)),{7:2,0:1,5:31,6:1})
        # Overlay category7 occurs after normalization's max5; it must survive.
        self.assertEqual(records[0][164],7);self.assertEqual(list(records[0][155:157]),[52,65])
        self.assertEqual(word(records[0],12),4);self.assertEqual(word(records[0],20),259)
        self.assertEqual(len(r['profiles']),9);self.assertEqual(len(r['normalization']),86)
        self.assertEqual(len(r['source_branch_bodies']),5)

    def test_narrow_wrapping_field_signedness_and_declared_counterfactuals(self):
        n=self.full['declared_template_diagnostic']['records'][0];character=bytearray.fromhex(n['character_input_hex'])
        r=self.rules
        for i in range(7):character[12+8*i]=255
        e=expected_record(n['template_hex'],character.hex(),r);record=bytes.fromhex(e['record_hex'])
        self.assertEqual(list(record[4:11]),[135]*7)
        # Recovery fields use MOVSX after their narrow stores, hence minimum1.
        self.assertEqual(word(record,24),1);self.assertEqual(word(record,30),1)
        self.assertLessEqual(record[55],32);self.assertLessEqual(record[68],32)
        changed=bytearray(character);changed[0x62:0x72]=b'\xff'*16
        self.assertEqual(expected_record(n['template_hex'],changed.hex(),r),e)
        # This path does not import persistent equipped item fields into the profile.
        self.assertEqual(bytes.fromhex(expected_profile(n['template_hex'],changed.hex(),r)['profile_hex'])[14:30],bytes(16))
        counters=json.loads(COUNTER_EVIDENCE.read_text('utf-8'))
        self.assertFalse(counters['school_enemy_loop_executed']);self.assertFalse(counters['unit_work_constructors_executed'])
        self.assertEqual([c['name'] for c in counters['records']],['attributes_zero','attributes_255','ranged_job2','persistent_attributes_255'])
        for c in counters['records']:
            e=expected_record(c['template_hex'],c['character_input_hex'],r)
            self.assertEqual(e['record_hex'],c['record_hex'],c['name'])
            self.assertTrue(c['retained_ranges_unchanged'])
            self.assertTrue(c['declared_mutation_retained'])
        self.assertEqual(counters['records'][-1]['record_hex'],n['record_hex'])

    def test_malformed_unowned_and_unsupported_source_inputs(self):
        n=self.full['declared_template_diagnostic']['records'][0];r=self.rules
        for t,c in ((None,None),('zz',None),('00'*83,None),('00'*84,None),(n['template_hex'],'zz'),(n['template_hex'],'00'*1183)):
            with self.assertRaises(ValueError):expected_record(t,c,r)
        character=bytearray.fromhex(n['character_input_hex'])
        for at,value in ((0,6),(6,255),(80,51)):
            bad=bytearray(character);bad[at]=value
            with self.assertRaises(ValueError):expected_record(n['template_hex'],bad.hex(),r)
        static=self.full['declared_template_diagnostic']['records'][1]
        with self.assertRaises(ValueError):expected_record(static['template_hex'],character.hex(),r)
        bad=bytearray.fromhex(n['template_hex']);bad[3]=3
        with self.assertRaises(ValueError):expected_record(bad.hex(),character.hex(),r)

    def test_independent_rules_and_frozen_native_exports_are_exact(self):
        rules=json.loads((ROOT/'prototype/data/school_enemy_records_rules.json').read_text('utf-8'))
        fixture=json.loads((ROOT/'prototype/data/school_enemy_records_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules);self.assertEqual(fixture,native_fixture())
        self.assertNotIn('cases',rules);self.assertNotIn('normalization',fixture)
        before=deepcopy(rules);fixture['cases'][0]['scene_unit_record']['record_hex']='';self.assertEqual(rules,before)


if __name__=='__main__':unittest.main()
