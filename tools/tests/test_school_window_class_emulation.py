import json
import unittest
from tools.school_window_class import *
from tools.school_window_class_emulation import generate
from tools.school_window_class_verification import verify_report,verify_case
from tools.school_window_module_validation import digest
from tools.school_device_init_verification import unpack


def report():return json.loads((ROOT/'analysis/school-window-class-trajectory-v1-20261020.json').read_text(encoding='utf8'))


class RegisteredTests(unittest.TestCase):
    def test_original_call_uses_actual_atom_preserves_guest_class_and_raw_evidence(self):
        r=report();before=digest(r);v=verify_report(r,'registered');self.assertEqual(digest(r),before)
        self.assertEqual(v['pending'],'0x450483')
        for c in r['cases']:
            n=c['registered'];self.assertEqual(n['cpu']['EAX'],n['platform_calls'][0]['result']['eax_bits_observed'])
            self.assertEqual(unpack(n['state']['class_structure']),unpack(c['class_ready']['state']['class_structure']))
            self.assertEqual(n['before_cpu'],c['class_ready']['cpu']);self.assertEqual(c['platform_cleanup']['unregistration_calls'],1)

    def test_refuses_repaired_cpu_bad_call_stack_native_return_or_import_admission(self):
        for mutation in ('cpu','args','sp','write','admission'):
            r=report();c=r['cases'][0];n=c['registered']
            if mutation=='cpu':n['cpu']['EAX']=0
            elif mutation=='args':n['platform_calls'][0]['args']=[0]
            elif mutation=='sp':n['platform_calls'][0]['sp']+=4
            elif mutation=='write':n['native_writes'][0]['value']+=1
            else:n['import_admission']['after_cpu']['ECX']=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c,'registered')

    def test_refuses_raw_memory_guest_callback_cleanup_or_callback_execution_claim(self):
        for mutation in ('guard','image','callback','cleanup','claim'):
            r=report();c=r['cases'][0];n=c['registered']
            if mutation=='guard':n['state']['guarded_owner']['sha256']='0'*64
            elif mutation=='image':n['state']['image_sha256']='0'*64
            elif mutation=='callback':n['platform_calls'][0]['result']['pointer_translations'][0]['guest']=0
            elif mutation=='cleanup':c['platform_cleanup']['unregistration']['callback_retained_until_unregister']=False
            else:n['callback_executed']=True
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'registered')


class CreateReadyTests(unittest.TestCase):
    def test_original_success_branch_and_all12_arguments_with_full_state_replay(self):
        r=report();self.assertEqual(verify_report(r)['pending'],'0x4504cf')
        for c in r['cases']:
            n=c['create_ready'];self.assertEqual(n['before_cpu'],c['registered']['cpu'])
            self.assertEqual(n['pending']['stack_args'],creation_args(c['module_input']['value']))
            self.assertFalse(n['pending']['call_instruction_executed']);self.assertEqual(len(n['native_writes']),13)

    def test_refuses_skipped_branch_wrong_args_return_flags_stack_or_creation_claim(self):
        for mutation in ('branch','args','return','flags','stack','claim'):
            r=report();c=r['cases'][0];n=c['create_ready']
            if mutation=='branch':n['instruction_runs']=[i for i in n['instruction_runs'] if i['va']!=0x450491]
            elif mutation=='args':n['pending']['stack_args'][-1]=0
            elif mutation=='return':n['returns'][0]['return_va']='0x4504d5'
            elif mutation=='flags':n['cpu']['EFLAGS']=70
            elif mutation=='stack':n['state']['stack']['sha256']='0'*64
            else:n['window_created']=True
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c)

    def test_fresh_continuous_native_trajectory_preserves_parent_source_and_metadata(self):
        functions=dict(parent.functions());source=SOURCE.read_bytes();old=module.source_contract();legacy=geometry.partial_class()
        r=generate();self.assertEqual(verify_report(r)['cases'],2)
        self.assertEqual(parent.functions(),functions);self.assertEqual(SOURCE.read_bytes(),source)
        self.assertEqual(module.source_contract(),old);self.assertEqual(geometry.partial_class(),legacy)
        for c in r['cases']:
            self.assertTrue(c['module_input']['before_first_original_instruction'])
            self.assertTrue(c['platform_cleanup']['all_owned_resources_released']);self.assertEqual(c['callback_packets'],[])


if __name__=='__main__':unittest.main()
