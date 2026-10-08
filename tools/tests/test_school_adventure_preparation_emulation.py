import hashlib
import json
import unittest

from tools.school_adventure_preparation_emulation import (
    EVIDENCE, ROOT, SOURCE, SOURCE_SHA256, SchoolAdventurePreparationEmulator,
    source_rules, exported_fixture)
from tools.tactics_exit_emulation import report_text


class DeparturePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_source_and_exports_exact(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA256)
        for name,value in [('rules',source_rules()),('evidence',exported_fixture(self.data))]:
            self.assertEqual((ROOT/f'prototype/data/school_adventure_preparation_{name}.json').read_bytes(),
                             report_text(value).encode('utf-8'))
        self.assertEqual(source_rules()['round_specs'],[{'scene_id':5,'selection_word':1}])

    def test_actual_chain_and_records_preserved(self):
        self.assertTrue(self.data['upstream']['school_data_prepared'])
        self.assertEqual(self.data['upstream']['state_requests'],[6,9])
        self.assertFalse(self.data['live_witness'])
        for c in self.data['cases']:
            self.assertEqual(c['before'],c['after'])
            self.assertEqual([c['before']['school']['month'],c['before']['school']['week']],[4,5])
            self.assertEqual(c['before']['school']['adventure_gate'],1)
            self.assertIn('0x4a7d30',c['readiness_coverage']['visited_function_entries'])
            if c['ready']:
                self.assertIn('0x4a6a10',c['preparation_coverage']['visited_function_entries'])
                self.assertEqual(c['prepared']['class_ratings'],c['class_ratings'])
            else:
                self.assertIsNone(c['prepared'])
                self.assertIsNone(c['preparation_coverage'])

    def test_current_squads_and_refusals(self):
        cases={c['name']:c for c in self.data['cases']}
        self.assertEqual([c['ready'] for c in self.data['cases']],[True,True,True,False,False])
        for name,students,groups in [('initial',[3,4,9],[0,0,0]),('student9_waiting',[3,4],[0,0]),
                                    ('fifth_class',[3,4],[4,4])]:
            self.assertEqual(cases[name]['prepared']['rounds'],[{'scene_id':5,'student_ids':students,
                              'student_groups':groups,'teacher_ids':[101]}])
        for c in self.data['cases'][1:]:
            for move in c['movement_coverage']:
                self.assertIn('0x4a4680',move['phases'][0]['coverage']['visited_function_entries'])

    def test_finite_write_guard(self):
        e=SchoolAdventurePreparationEmulator.__new__(SchoolAdventurePreparationEmulator)
        e.stage='departure_rounds'
        e.writes=[]
        class CPU:
            def reg_read(self,reg): return 0
        for address in [0x7A528E,0x7A5290,0x7CF34C,0x7E17E8,0x9000000]:
            with self.assertRaisesRegex(RuntimeError,'finite guard'):
                e._write_hook(CPU(),0,address,2,1,None)
        for address in [0x7A5294,0x7A529A,0x7A5308]:
            e._write_hook(CPU(),0,address,2,1,None)
        self.assertEqual(len(e.writes),3)

    def test_report_writes_never_touch_date_or_roles(self):
        for c in self.data['cases']:
            for key in ['rating_coverage','readiness_coverage','preparation_coverage']:
                if c[key] is None: continue
                for a,b in c[key]['native_written_ranges']:
                    start,end=int(a,16),int(b,16)
                    self.assertFalse(start<0x7A5292 and end>0x7A528E)
                    self.assertFalse(start<0x7CF34C+45*0x124 and end>0x7CF34C)


if __name__ == '__main__':
    unittest.main()
