import json
import unittest
from tools.school_window_callback import *
from tools.school_window_callback_emulation import generate
from tools.school_window_callback_verification import verify_case,verify_report
from tools.school_window_module_validation import digest


def report():return json.loads((ROOT/'analysis/school-window-callback-trajectory-v1-20261020.json').read_text(encoding='utf8'))


class CallbackTests(unittest.TestCase):
    def test_full_independent_original_replay_binding_default_return_and_pending_message(self):
        r=report();before=digest(r);v=verify_report(r);self.assertEqual(digest(r),before)
        self.assertEqual(v['pending_message'],131)
        for p in v['callbacks']:
            self.assertEqual((p['native_instructions'],p['reads'],p['writes'],p['native_APIs']),(416,110,208,5))
            self.assertFalse(p['captured_game_global_read']);self.assertEqual(p['result'],1)

    def test_refuses_wrong_create_abi_shadow_property_or_host_procedure_translation(self):
        for mutation in ('create','shadow','property','procedure','default','native_push'):
            r=report();c=r['cases'][0];n=c['callbacks'][0]
            if mutation=='create':c['creation']['args'][-1]=0
            elif mutation=='shadow':n['setup']['args'][-1]=n['setup']['packet']['lParam']
            elif mutation=='property':n['platform_calls'][2]['result']['observed_property']=0
            elif mutation=='procedure':n['platform_calls'][3]['result']['host_result']=ENTRY
            elif mutation=='default':n['platform_calls'][4]['result']['result']=0
            else:c['creation']['native_writes'][0]['value']=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c)

    def test_refuses_missing_access_bad_restore_fabricated_pending_reply_or_cleanup(self):
        for mutation in ('read','write','restore','reply','cleanup','global'):
            r=report();c=r['cases'][0];n=c['callbacks'][0]
            if mutation=='read':n['native_reads'].pop()
            elif mutation=='write':n['native_writes'][0]['value']^=1
            elif mutation=='restore':n['restored_caller_cpu']['ESP']+=4
            elif mutation=='reply':c['wire'].append(dict(direction='callback_return',value=dict(op='callback_return',callback_id=2,result=1)))
            elif mutation=='cleanup':c['platform_abort']['explicit_cleanup_performed']=True
            else:c['final_image_sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r)

    def test_fresh_real_callbacks_preserve_parent_functions_and_source_and_end_owned_processes(self):
        source=SOURCE.read_bytes();functions=dict(parent.functions());old=previous.source_contract()
        r=generate();self.assertEqual(verify_report(r)['cases'],2)
        self.assertEqual(SOURCE.read_bytes(),source);self.assertEqual(parent.functions(),functions);self.assertEqual(previous.source_contract(),old)
        for c in r['cases']:
            self.assertTrue(c['platform_abort']['owned_process_exited']);self.assertTrue(c['platform_abort']['unanswered'])
            self.assertIsNone(c['platform_cleanup'])


if __name__=='__main__':unittest.main()
