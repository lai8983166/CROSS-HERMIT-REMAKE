import hashlib
import json
import unittest

from tools.school_fifth_planning_emulation import (
    EVIDENCE,EVIDENCE_SHA256,SchoolFifthPlanningEmulator,exported_fixture,exported_rules)
from tools.school_course_result_handoff_emulation import RESOURCE_ROOT
from tools.tactics_exit_emulation import ROOT,report_text
from tools.battle_preparation_emulation import CHAR_BASE,CHAR_STRIDE,PACKAGE_BASE,PACKAGE_STRIDE


class FifthPlanningNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hashlib.sha256(EVIDENCE.read_bytes()).hexdigest() != EVIDENCE_SHA256:
            raise ValueError('frozen fifth-school report differs')
        cls.data = json.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_actual_chain_and_native_school_fields(self):
        c = self.data['cases'][0]
        self.assertTrue(c['school_data_prepared'])
        self.assertEqual(c['state_requests'],[6,9])
        self.assertEqual(c['upstream']['state_requests'],[8])
        self.assertEqual(c['school_consumed']['state'],9)
        self.assertEqual([c['pending_flag'],c['pending_state']],[0,9])
        self.assertEqual(c['stop_reason'],'school_person_idle_boundary')
        self.assertEqual([r['path'] for r in c['loads']],['adv/dat/ch002.ybc','adv/dat/chapter205.ybc'])
        self.assertEqual([c['after']['school'][k] for k in ('month','week')],[4,5])
        self.assertEqual(c['after']['school']['lecture_work_fields'],[3,4,5,0])
        self.assertEqual(c['after']['school']['group_raw_bytes'][3],0)
        self.assertEqual(c['work_state']['news_count'],18)
        for va in ('0x4a5a60','0x4a17b0','0x4a2ba0','0x4a1c70','0x4a5f40','0x4b8d50'):
            self.assertIn(va,c['coverage']['visited_function_entries'])
        self.assertIn('data/adv/bin/bg002_b.bin',[r.get('path') for r in c['work_events']])

    def test_preserves_earned_roles_relationships_and_mvp(self):
        for c in self.data['cases']:
            self.assertEqual(c['before']['counts'],c['after']['counts'])
            for k in ('participants','nonparticipant_character_sha256','nonparticipant_package_sha256','month','week','adv_globals'):
                self.assertEqual(c['before']['roles'][k],c['after']['roles'][k],k)
            for k in ('member_profiles','relationships','global_total_511c','student_ids','teacher_ids','availability'):
                self.assertEqual(c['before']['school'][k],c['after']['school'][k],k)

    def test_waits_prevent_school_and_guard_refuses_growth_date_mvp(self):
        for c in self.data['cases'][1:]:
            self.assertFalse(c['school_data_prepared'])
            self.assertIsNone(c['school_consumed'])
        self.assertEqual(self.data['cases'][1]['stop_reason'],'workroom_waiting_continue')
        self.assertEqual(self.data['cases'][2]['stop_reason'],'bounded_pending_result')
        e = SchoolFifthPlanningEmulator();e.stage = 'fifth_school'
        for address,size in ((CHAR_BASE+3*CHAR_STRIDE+0xC,1),(PACKAGE_BASE+3*PACKAGE_STRIDE+0x120,2),
                (0x7A528E,2),(0x7A5290,4),(0x7A4AE2,1)):
            with self.assertRaisesRegex(RuntimeError,'finite guard'):
                e._write_hook(e.uc,None,address,size,1,None)
        with self.assertRaises(ValueError):
            SchoolFifthPlanningEmulator(school_key_ready=1)

    def test_source_only_exports_hashes_and_declared_authority(self):
        for path,sha in self.data['script_sha256'].items():
            self.assertEqual(hashlib.sha256((RESOURCE_ROOT/path).read_bytes()).hexdigest(),sha)
        for path,data in [('prototype/data/school_fifth_planning_evidence.json',exported_fixture(self.data)),
                ('prototype/data/school_fifth_planning_rules.json',exported_rules(self.data))]:
            self.assertEqual((ROOT/path).read_bytes(),report_text(data).encode())
        rules = exported_rules(self.data)
        for key in ('cases','after','group_raw_bytes','member_profiles'):
            self.assertNotIn(key,rules)
        for c in [self.data,*self.data['cases'],rules]:
            for key in ('interactive_school_ready','live_witness','authorizes_persistent_write'):
                self.assertFalse(c[key])


if __name__ == '__main__':
    unittest.main()
