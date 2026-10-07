import hashlib
import json
import struct
import unittest

from tools.school_story_week_emulation import (
    EVIDENCE,EVIDENCE_SHA256,RESOURCE_ROOT,SchoolStoryWeekEmulator,exported_fixture,exported_rules)
from tools.tactics_exit_emulation import ROOT,report_text
from tools.battle_preparation_emulation import CHAR_BASE,CHAR_STRIDE,PACKAGE_BASE,PACKAGE_STRIDE


class SchoolStoryWeekTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = EVIDENCE.read_bytes()
        if hashlib.sha256(raw).hexdigest() != EVIDENCE_SHA256:
            raise ValueError('frozen native continuation differs')
        cls.data = json.loads(raw)

    def test_shared_course_story_request_and_week(self):
        case = self.data['cases'][0]
        self.assertTrue(case['story_completed'])
        self.assertTrue(case['week_executed'])
        self.assertEqual(case['state_requests'],[6,7,6])
        self.assertEqual(case['course_request_consumed']['state'],6)
        self.assertEqual(case['consumed_request']['state'],7)
        self.assertEqual(case['before_week'],case['after_story'])
        self.assertEqual([case['after_week'][k] for k in ('month','week')],[4,5])
        self.assertEqual(case['active_path'],'adv/dat/ch001.ybc')
        self.assertEqual(case['stored_next_task'],8)
        self.assertEqual([case[k] for k in ('pending_flag','pending_state')],[1,6])
        entries = [e['va'] for e in case['week_events']]
        self.assertEqual(entries.count('0x4d3510'),1)
        for va in ('0x4d31f0','0x4d34a0','0x4d3aa0'):
            self.assertIn(va,entries)
        for before,after in zip(case['before_week']['participants'],case['after_week']['participants']):
            for field in ('attributes','job_progress','equipped_items','equipped_skills'):
                self.assertEqual(before[field],after[field])
        for key in ('live_witness','school_initialized','interactive_school_ready','authorizes_persistent_write'):
            self.assertFalse(case[key])

    def test_executed_dialogue_is_original_order(self):
        case = self.data['cases'][0]
        for chapter in (16,17):
            path = f'adv/dat/chapter{chapter:03}.ybc'
            raw = (RESOURCE_ROOT/path).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),self.data['script_sha256'][path])
            offset = struct.unpack_from('<I',raw,4)[0]
            expected = []
            while True:
                op,advance = struct.unpack_from('<HH',raw,offset)
                if op == 17:
                    expected.append(offset)
                if op == 19:
                    break
                offset += advance
            executed = [c['offset'] for c in case['commands'] if c['path'] == path and c['opcode'] == 17]
            self.assertEqual(executed,expected)
        self.assertTrue(any(c['path'].endswith('chapter017.ybc') and c['opcode'] == 19 for c in case['commands']))

    def test_pending_cases_and_finite_guard(self):
        fade,story = self.data['cases'][1:]
        self.assertTrue(fade['week_executed'])
        self.assertEqual(fade['after_week'],self.data['cases'][0]['after_week'])
        self.assertEqual(fade['stop_reason'],'week_fade_pending_after_settlement')
        self.assertFalse(any(c['path'].endswith('ch001.ybc') for c in fade['loads']))
        self.assertFalse(story['story_completed'])
        self.assertFalse(story['week_executed'])
        self.assertIsNone(story['consumed_request'])
        e = SchoolStoryWeekEmulator()
        e.stage = 'story_week'
        for address,size in ((CHAR_BASE+5*CHAR_STRIDE+0xB8,1),
                             (PACKAGE_BASE+3*PACKAGE_STRIDE+0x120,2),(0x7A5292,2)):
            with self.assertRaisesRegex(RuntimeError,'finite guard'):
                e._write_hook(e.uc,None,address,size,1,None)

    def test_exports_are_exact_and_rules_do_not_contain_expected_results(self):
        for name,object in (
            ('prototype/data/school_story_week_evidence_v1.json',exported_fixture(self.data)),
            ('prototype/data/school_story_week_rules.json',exported_rules(self.data))):
            self.assertEqual((ROOT/name).read_bytes(),report_text(object).encode())
        rules = exported_rules(self.data)
        for key in ('cases','expected','after_week','before_week','course_result'):
            self.assertNotIn(key,rules)


if __name__ == '__main__':
    unittest.main()
