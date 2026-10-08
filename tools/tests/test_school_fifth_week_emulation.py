import hashlib
import json
import struct
import unittest

from tools.school_fifth_week_emulation import (
    EVIDENCE,EVIDENCE_SHA256,SchoolFifthWeekEmulator,exported_fixture,exported_rules)
from tools.school_course_result_handoff_emulation import RESOURCE_ROOT
from tools.tactics_exit_emulation import ROOT,report_text
from tools.battle_preparation_emulation import CHAR_BASE,CHAR_STRIDE,PACKAGE_BASE,PACKAGE_STRIDE


class FifthWeekNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = EVIDENCE.read_bytes()
        if hashlib.sha256(raw).hexdigest() != EVIDENCE_SHA256:
            raise ValueError('frozen native fifth-week report differs')
        cls.data = json.loads(raw)

    def test_same_cpu_date_branch_and_effectful_exit(self):
        c = self.data['cases'][0]
        self.assertTrue(c['fifth_completed'])
        self.assertEqual(c['upstream']['state_requests'],[6,7,6])
        before = dict(c['before']);before.pop('adv_globals')
        self.assertEqual(before,c['upstream']['after_week'])
        self.assertEqual([c['before'][k] for k in ('month','week')],[4,5])
        self.assertEqual(c['state_requests'],[8])
        self.assertEqual([c[k] for k in ('pending_flag','pending_state','next_task','vm_active')],[1,8,8,0])
        self.assertEqual(c['active_path'],'adv/dat/chapter018.ybc')
        self.assertEqual([load['path'] for load in c['loads']],['adv/dat/chapter018.ybc'])
        expected = json.loads(json.dumps(c['before']))
        expected['flags'].update({'0x7a55f6':2,'0x7e11a0':1})
        expected['adv_globals']['0x7a5292'] = 6
        self.assertEqual(c['after'],expected,'no growth, availability, equipment or unrelated role writes')
        entries = c['coverage']['visited_function_entries']
        for address in ('0x4c4750','0x4d0da0'):
            self.assertIn(address,entries)
        self.assertFalse(c['workroom_body_executed'])

    def test_native_text_order_and_movie_resource(self):
        c = self.data['cases'][0]
        raw = (RESOURCE_ROOT/'adv/dat/chapter018.ybc').read_bytes()
        at = 20;expected = []
        while True:
            op,size = struct.unpack_from('<HH',raw,at)
            if op == 17:
                expected.append(at)
            if op == 19:
                break
            at += size
        self.assertEqual([i['offset'] for i in c['commands'] if i['path'].endswith('chapter018.ybc') and i['opcode'] == 17],expected)
        self.assertEqual(c['movie_events'][0]['path'],'data/adv/bin/tc0405.bin')
        self.assertFalse(c['movie_events'][0]['body_executed'])
        for path,sha in self.data['script_sha256'].items():
            self.assertEqual(hashlib.sha256((RESOURCE_ROOT/path).read_bytes()).hexdigest(),sha)

    def test_readiness_waits_and_finite_guard(self):
        for c in self.data['cases'][1:]:
            self.assertFalse(c['fifth_completed'])
            self.assertEqual(c['before'],c['after'])
            self.assertEqual(c['state_requests'],[])
            self.assertEqual(c['stop_reason'],'bounded_pending_result')
        e = SchoolFifthWeekEmulator();e.stage = 'fifth_week'
        for address,size in ((CHAR_BASE+3*CHAR_STRIDE+0xC,2),
                (PACKAGE_BASE+3*PACKAGE_STRIDE+0x120,2),(0x7A5294,2),(0x7E1182,4)):
            with self.assertRaisesRegex(RuntimeError,'finite guard'):
                e._write_hook(e.uc,None,address,size,1,None)
        with self.assertRaises(ValueError):
            SchoolFifthWeekEmulator(key_ready=1)

    def test_separate_exports_and_non_authority(self):
        for path,data in [('prototype/data/school_fifth_week_evidence.json',exported_fixture(self.data)),
                ('prototype/data/school_fifth_week_rules.json',exported_rules(self.data))]:
            self.assertEqual((ROOT/path).read_bytes(),report_text(data).encode())
        rules = exported_rules(self.data)
        self.assertNotIn('cases',rules)
        self.assertNotIn('after',rules)
        for c in [self.data,*self.data['cases'],rules]:
            for key in ('school_initialized','interactive_school_ready','live_witness','authorizes_persistent_write'):
                self.assertFalse(c[key])


if __name__ == '__main__':
    unittest.main()
