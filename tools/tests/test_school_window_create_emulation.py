import json
import unittest
from tools.school_window_create import *
from tools.school_window_create_emulation import generate
from tools.school_window_create_verification import verify_case,verify_report
from tools.school_window_module_validation import digest


def report():return json.loads((ROOT/'analysis/school-window-create-trajectory-v1-20261020.json').read_text(encoding='utf8'))


class ClientTests(unittest.TestCase):
    def test_actual_client_callback_reuses_owner_and_preserves_real_RECT_full_replay(self):
        r=report();before=digest(r);v=verify_report(r);self.assertEqual(before,digest(r))
        for p in v['case_proofs']:
            n=p['callbacks'][1];self.assertEqual((n['instructions'],n['reads'],n['writes'],n['native_APIs']),(299,73,160,2))
            self.assertTrue(n['bound_property_reused']);self.assertFalse(n['source_binding_repeated']);self.assertEqual(n['result'],0)

    def test_refuses_wrong_RECT_input_output_pointer_or_real_property(self):
        for mutation in ('input','output','opaque','property'):
            c=report()['cases'][0];n=c['callbacks'][1]
            if mutation=='input':n['setup']['packet']['data_hex']='20'+n['setup']['packet']['data_hex'][2:]
            elif mutation=='output':n['platform_calls'][1]['result']['after_hex']='00'*16
            elif mutation=='opaque':n['setup']['args'][-1]=SHADOW
            else:n['platform_calls'][0]['result']['result']=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c)

    def test_refuses_missing_source_read_wrong_write_bad_restore_or_admission_repair(self):
        for mutation in ('read','write','restore','admission'):
            c=report()['cases'][0];n=c['callbacks'][1]
            if mutation=='read':n['native_reads'].pop()
            elif mutation=='write':n['native_writes'][0]['value']^=1
            elif mutation=='restore':n['restored_caller_cpu']['ESP']+=4
            else:c['creation']['import_admission']['after_cpu']['ECX']=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c)


class CreateTests(unittest.TestCase):
    def test_original_message1_switch_returns_zero_without_default_or_rebinding(self):
        r=report();v=verify_report(r)
        for c,p in zip(r['cases'],v['case_proofs']):
            n=c['callbacks'][2];proof=p['callbacks'][2]
            self.assertEqual([a['name'] for a in n['platform_calls']],['GetPropA'])
            self.assertIn(0x450ED3,[a['va'] for a in n['instruction_runs']]);self.assertIn(0x451030,[a['va'] for a in n['instruction_runs']])
            self.assertEqual((proof['instructions'],proof['reads'],proof['writes'],proof['result']),(230,52,126,0))

    def test_refuses_skipped_branch_wrong_return_global_pending_reply_or_cleanup(self):
        for mutation in ('branch','return','global','reply','cleanup','pending'):
            r=report();c=r['cases'][0];n=c['callbacks'][2]
            if mutation=='branch':n['instruction_runs']=[a for a in n['instruction_runs'] if a['va']!=0x450ED3]
            elif mutation=='return':n['result']=1
            elif mutation=='global':c['final_image_sha256']='0'*64
            elif mutation=='reply':c['wire'].append(dict(direction='callback_return',value=dict(op='callback_return',callback_id=4,result=0)))
            elif mutation=='cleanup':c['platform_abort']['explicit_cleanup_performed']=True
            else:c['pending_callback']['packet']['lParam']=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r)

    def test_fresh_full_trajectory_keeps_source_parent_metadata_and_ends_owned_lifetimes(self):
        raw=SOURCE.read_bytes();functions=dict(parent.functions());previous=callback.source_contract()
        r=generate();self.assertEqual(verify_report(r)['completed_messages'],[129,131,1])
        self.assertEqual(SOURCE.read_bytes(),raw);self.assertEqual(parent.functions(),functions);self.assertEqual(callback.source_contract(),previous)
        for c in r['cases']:
            self.assertTrue(c['platform_abort']['owned_process_exited']);self.assertTrue(c['platform_abort']['unanswered']);self.assertIsNone(c['platform_cleanup'])


if __name__=='__main__':unittest.main()
