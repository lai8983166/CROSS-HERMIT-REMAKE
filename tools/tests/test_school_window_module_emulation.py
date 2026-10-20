import copy
import json
import unittest
from tools.school_window_module import ROOT,geometry
from tools.school_window_module_emulation import generate
from tools.school_window_module_verification import verify_report
from tools.school_window_module_validation import legacy_prefix_view,digest


def report():return json.loads((ROOT/'analysis/school-window-module-trajectory-v3-20261020.json').read_text(encoding='utf8'))


class InstanceTests(unittest.TestCase):
    def test_actual_initial_module_propagation_and_disclosed_nonmutating_view(self):
        r=report();before=digest(r);verify_report(r,'instance');self.assertEqual(digest(r),before)
        for c in r['cases']:
            view,p=legacy_prefix_view(c);module=c['hello']['resource_module']['pointer']
            self.assertEqual(c['module_input']['value'],module)
            self.assertEqual(c['tasks']['state']['instance_value'],module)
            self.assertEqual(c['class']['pending']['stack_args'],[module,157])
            self.assertEqual(len(p['substitutions']),31)
            self.assertFalse(p['actual_raw_snapshots_modified'] or p['emulator_mutated'])
            self.assertEqual(view['tasks']['state']['instance_value'],geometry.window.HINSTANCE)

    def test_refuses_declaring_instance_after_start_or_repairing_native_store(self):
        for mutation in ('late','slot','frame','native'):
            r=report();c=r['cases'][0]
            if mutation=='late':c['module_input']['before_first_original_instruction']=False
            elif mutation=='slot':c['module_input']['slot']=geometry.window.INSTANCE
            elif mutation=='frame':c['module_input']['initial_stack']['sha256']='0'*64
            else:next(w for w in c['tasks']['native_writes'] if w['pc']==0x49DE26)['value']=geometry.window.HINSTANCE
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'instance')

    def test_verifier_view_cannot_hide_unrelated_callback_cpu_or_resource_changes(self):
        for mutation in ('callback','cpu','resource','image'):
            r=report();c=r['cases'][0]
            if mutation=='callback':next(w for w in c['class']['native_writes'] if w['pc']==0x4503EA)['value']=0
            elif mutation=='cpu':c['class']['cpu']['EBX']=0
            elif mutation=='resource':c['hello']['resource_module']['resources'][0]['sha256']='0'*64
            else:c['class']['state']['image_sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'instance')


if __name__=='__main__':unittest.main()
