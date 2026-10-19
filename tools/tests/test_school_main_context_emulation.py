import copy
import json
import unittest
from tools.school_main_context_emulation import generate
from tools.school_main_context_verification import verify_report,verify_case
from tools.school_main_context import ROOT

TRAJECTORY=ROOT/'analysis/school-main-context-trajectory-v2-20261019.json'


def report():return json.loads(TRAJECTORY.read_text(encoding='utf8'))


class AllocationTests(unittest.TestCase):
    def test_both_original_allocations_and_exact_dirty_backing(self):
        r=verify_report(report(),'allocation')
        self.assertEqual(r['cases'],2)
        self.assertFalse(r['original_publication_verified'])

    def test_refuses_fabricated_allocation_counter_cpu_and_frame(self):
        for key in ('allocations','cpu','native_writes','pending'):
            r=report();row=r['cases'][0]['allocation']
            if key=='allocations':row[key][0]['args'][0]+=4
            elif key=='cpu':row[key]['ESP']+=4
            elif key=='native_writes':row[key].pop()
            else:row[key]['return_va']='0x49ddf1'
            with self.subTest(key=key),self.assertRaises(ValueError):verify_report(r,'allocation')

    def test_refuses_forged_memory_and_trace(self):
        for key in ('owner','guarded_owner','stack','foreign_maps'):
            r=report();state=r['cases'][0]['allocation']['state']
            node=state[key][0] if key=='foreign_maps' else state[key];node['sha256']='0'*64
            with self.subTest(key=key),self.assertRaises(ValueError):verify_report(r,'allocation')
        r=report();r['cases'][0]['allocation']['instruction_runs'][0]['va']+=1
        with self.assertRaises(ValueError):verify_report(r,'allocation')


if __name__=='__main__':unittest.main()
