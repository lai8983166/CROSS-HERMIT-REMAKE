import unittest

from tools.school_course_confirmation_emulation import (
    report,fixture,source_rules,CourseConfirmationEmulator,IDS)
from tools.tactics_exit_emulation import ROOT,report_text
from tools.new_game_school_emulation import CHAR,STRIDE
from tools.battle_preparation_emulation import PACKAGE_BASE,PACKAGE_STRIDE


class CourseConfirmationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = report()

    def test_byte_exact_regeneration_and_source_only_rules(self):
        for name,value in [
            ('analysis/school-course-confirmation-v3-20261007.json',self.data),
            ('prototype/data/school_course_confirmation_evidence_v3.json',fixture(self.data)),
            ('prototype/data/school_course_confirmation_rules.json',source_rules()),
        ]:
            self.assertEqual((ROOT/name).read_bytes(),report_text(value).encode())
        for key in ('before','after','cases','expected_after'):
            self.assertNotIn(key,source_rules())
        for case in self.data['cases']:
            self.assertEqual(source_rules()['initial_records'],case['initial_records'])

    def test_native_entry_chain_and_growth_date_preserved(self):
        self.assertEqual(len(self.data['cases']),6)
        for case in self.data['cases']:
            entries = case['confirmation_coverage']['visited_function_entries']
            for entry in ('0x4c1350','0x4bf9e0','0x4d3960'):
                self.assertIn(entry,entries)
            self.assertEqual(case['before']['month'],4)
            self.assertEqual(case['before']['week'],4)
            for key in case['before']:
                if key != 'relationships':
                    self.assertEqual(case['before'][key],case['after'][key],(case['name'],key))
            # Only career progress changes its derived sums; pools/status/levels stay fixed.
            for old,new in zip(case['growth_records'],case['after_growth_records']):
                for key in old:
                    if key != 'job_sums':
                        self.assertEqual(old[key],new[key],(case['name'],key))
            for key in ('authorizes_persistent_write','interactive_school_ready','school_initialized','live_witness'):
                self.assertFalse(case[key])

    def test_waiting_history_caps_signed_bytes_and_directed_relations(self):
        cases = self.data['cases']
        self.assertEqual(cases[2]['after_records'][2]['week_records'][9],3)
        self.assertEqual(cases[2]['before_records'][2]['job_progress'][7]+1,
                         cases[2]['after_records'][2]['job_progress'][7])
        self.assertEqual(cases[4]['after_records'],cases[0]['after_records'])
        probe = cases[5]
        for index,value in enumerate((99,100,0)):
            job = probe['before']['member_profiles'][index+1]['job']
            self.assertEqual(probe['after_records'][index]['job_progress'][job],value)
        self.assertEqual(probe['after_records'][2]['week_records'][9:12],[3,8,9])
        self.assertEqual([call['delta'] for call in probe['relationship_calls']
                          if (call['from'],call['to']) == (4,9)],[1,1,2])
        self.assertTrue(all(1 <= r['value'] <= 100 for r in probe['after']['relationships']))

    def test_finite_guard_and_nonparticipant(self):
        e = CourseConfirmationEmulator()
        e.initialize()
        record = bytes(e.uc.mem_read(CHAR+5*STRIDE,STRIDE))
        package = bytes(e.uc.mem_read(PACKAGE_BASE+5*PACKAGE_STRIDE,PACKAGE_STRIDE))
        e.declare_date(4,4)
        e.run('teaching','mode')
        e.run('assign','course',row=2)
        e.settle('guard_growth')
        e.confirm()
        self.assertEqual(record,bytes(e.uc.mem_read(CHAR+5*STRIDE,STRIDE)))
        self.assertEqual(package,bytes(e.uc.mem_read(PACKAGE_BASE+5*PACKAGE_STRIDE,PACKAGE_STRIDE)))
        e.stage = 'course_confirmation'
        for address,size in [(0x7A5290,2),(CHAR+3*STRIDE+0x10,4),
                (PACKAGE_BASE+5*PACKAGE_STRIDE+0xD8,1),(0x7D3D71+5*68+3,1)]:
            with self.assertRaisesRegex(RuntimeError,'finite guard'):
                e._write_hook(e.uc,None,address,size,1,None)


if __name__ == '__main__':
    unittest.main()
