import hashlib
import json
import unittest
from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_enemy_records_emulation import (
    SchoolEnemyRecordsEmulator,ROOT,TACT,UNITCTRL,RECORD_OFFSET,WORK_OFFSET,STACK,SCRATCH)

EVIDENCE=ROOT/'analysis/school-enemy-records-v2-20261010.json'
EVIDENCE_SHA256='afe6d5f2e9076de16c294cf305342e8208aa29fa31c3abe1096c6f28ac4e3e21'


class EnemyRecordNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.full=json.loads(EVIDENCE.read_text('utf-8'))

    def test_actual_school_first_record_boundary_and_refusal(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['scene_unit_record_prepared'] for c in self.full['cases']],[True,True,True,False,False])
        for c in self.full['cases'][:3]:
            self.assertEqual(c['stop_reason'],'before_first_scene_unit_work_constructor')
            r=c['scene_unit_record'];self.assertEqual((r['ordinal'],r['index'],r['identity']),(0,249,5))
            self.assertEqual(r['caller_return_va'],'0x45361b')
            self.assertTrue(r['retained_ranges_unchanged']);self.assertFalse(r['unit_work_constructor_executed'])
            self.assertEqual(r['work_hex'],'00'*1312);self.assertEqual(len(bytes.fromhex(r['record_hex'])),176)
            seen=c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x453540','0x4da450','0x4da5f0','0x4dfc20','0x4e0a00'):self.assertIn(va,seen)
            for va in ('0x4680b0','0x468910','0x4500b0'):self.assertNotIn(va,seen)
        for c in self.full['cases'][3:]:self.assertIsNone(c['scene_unit_record'])

    def test_declared_driver_transforms_all_templates_without_work(self):
        d=self.full['declared_template_diagnostic'];r=d['records']
        self.assertEqual(d['evidence_kind'],'declared_scene5_template_record_driver')
        self.assertFalse(d['school_enemy_loop_executed']);self.assertFalse(d['unit_work_constructors_executed'])
        self.assertEqual(len(r),35);self.assertEqual([x['index'] for x in r],list(range(249,214,-1)))
        self.assertEqual([x['template_hex'] for x in r],self.full['scene_inputs']['templates'])
        for x in r:
            self.assertEqual(x['caller_return_va'],'0x3000000');self.assertTrue(x['retained_ranges_unchanged'])
            self.assertFalse(x['unit_work_constructor_executed']);self.assertEqual(x['work_hex'],'00'*1312)
            self.assertEqual(len(x['clears']),2 if x['identity']<200 else 1)
            if x['identity']>=200:self.assertEqual(x['scratch_before_hex'],x['scratch_after_hex'])

    def test_retained_current_units_resources_and_no_new_handles(self):
        for c in self.full['cases']:
            self.assertFalse(c['battle_world_constructed']);self.assertFalse(c['live_witness']);self.assertTrue(c['persistent_ranges_unchanged'])
        for c in self.full['cases'][:3]:
            r=c['scene_unit_record'];self.assertGreater(r['retained_bytes'],20_000_000)
            self.assertEqual(sum(x['bytes'] for x in r['retained_ranges']),r['retained_bytes'])
            self.assertEqual([n['bytes'] for n in r['clears']],[48,176])
            self.assertTrue(c['current_loop']['retained_ranges_unchanged']);self.assertFalse(r['scene_placement_executed'])
            n=len(c['current_units']);self.assertEqual(sum(e['name']=='CloseHandle' for e in c['file_events']),10+n)

    def test_guard_rejects_current_work_persistence_other_record_and_files(self):
        e=SchoolEnemyRecordsEmulator();e.enemy_loading=True
        at=UNITCTRL+RECORD_OFFSET+249*176;e.enemy_record={'identity':5,'record_pointer':at,'clears':[]}
        for p in (TACT,UNITCTRL+WORK_OFFSET,at-1,at+176,SCRATCH-1,SCRATCH+48,0x6F5088,0x17000000):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p,1,0,None)
        e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        for p in (0x428A40,0x4500B0,0x424F80,0x468910,0x422360):
            with self.assertRaises(RuntimeError):e._hook(e.uc,p,1,None)
        e.enemy_record['identity']=301
        with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,SCRATCH,1,0,None)


if __name__=='__main__':unittest.main()
