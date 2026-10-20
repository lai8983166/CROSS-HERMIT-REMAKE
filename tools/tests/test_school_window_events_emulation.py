import json
import unittest
from tools.school_window_events import *
from tools.school_window_events_emulation import generate
from tools.school_window_events_verification import verify_case,verify_report
from tools.school_window_module_validation import digest


def report():return json.loads((ROOT/'analysis/school-window-events-trajectory-v1-20261020.json').read_text(encoding='utf8'))


class ScalarTests(unittest.TestCase):
    def test_original_scalar_messages_full_independent_replay(self):
        r=report();before=digest(r);v=verify_report(r);self.assertEqual(before,digest(r))
        for c,p in zip(r['cases'],v['case_proofs']):
            for index,counts in ((3,(230,52,126,1)),(4,(299,74,161,2)),(5,(295,71,161,2))):
                n=p['callbacks'][index];self.assertEqual(tuple(n[k] for k in ('instructions','reads','writes','native_APIs')),counts)
                self.assertTrue(n['bound_property_reused']);self.assertEqual(n['result'],0)
            self.assertEqual([a['name'] for a in c['callbacks'][3]['platform_calls']],['GetPropA'])
            self.assertIn(0x450EDD,[a['va'] for a in c['callbacks'][3]['instruction_runs']])

    def test_refuses_wrong_size_move_show_or_forwarded_scalar(self):
        for index,key in ((3,'lParam'),(4,'lParam'),(5,'wParam'),(5,'forwarded')):
            c=report()['cases'][0];n=c['callbacks'][index]
            if key=='forwarded':n['platform_calls'][-1]['result']['host_args'][2]=0
            else:n['setup']['packet'][key]^=1
            with self.subTest(index=index,key=key),self.assertRaises(ValueError):verify_case(c)

    def test_refuses_missing_reads_wrong_write_restore_or_rebinding(self):
        for mutation in ('read','write','restore','property'):
            c=report()['cases'][0];n=c['callbacks'][4]
            if mutation=='read':n['native_reads'].pop()
            elif mutation=='write':n['native_writes'][0]['value']^=1
            elif mutation=='restore':n['restored_caller_cpu']['ESP']+=4
            else:n['platform_calls'][0]['result']['result']=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c)


class PositionTests(unittest.TestCase):
    def test_actual_WINDOWPOS_before_after_and_unanswered_second_position(self):
        r=report();v=verify_report(r)
        for c,p in zip(r['cases'],v['case_proofs']):
            n=c['callbacks'][6];proof=p['callbacks'][6]
            self.assertEqual(tuple(proof[k] for k in ('instructions','reads','writes','native_APIs','result')),(299,73,160,2,0))
            self.assertEqual(n['platform_calls'][-1]['result']['before_hex'],n['setup']['packet']['data_hex'])
            self.assertEqual(n['platform_calls'][-1]['result']['after_hex'],n['setup']['packet']['data_hex'])
            self.assertEqual(p['pending_WINDOWPOS_flags'],3);self.assertEqual(p['pending_message'],70)

    def test_refuses_bad_WINDOWPOS_ownership_output_pending_reply_or_cleanup(self):
        for mutation in ('short','hwnd','flags','output','pending','reply','cleanup','global'):
            r=report();c=r['cases'][0];n=c['callbacks'][6];packet=n['setup']['packet']
            if mutation=='short':packet['data_hex']=packet['data_hex'][:-2]
            elif mutation=='hwnd':packet['hwnd']^=1
            elif mutation=='flags':packet['data_hex']=packet['data_hex'][:-8]+'03000000'
            elif mutation=='output':n['platform_calls'][-1]['result']['after_hex']='00'*28
            elif mutation=='pending':c['pending_callback']['packet']['data_hex']=packet['data_hex']
            elif mutation=='reply':c['wire'].append(dict(direction='callback_return',value=dict(op='callback_return',callback_id=8,result=0)))
            elif mutation=='cleanup':c['platform_abort']['explicit_cleanup_performed']=True
            else:c['final_image_sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r)

    def test_fresh_same_CPU_trajectory_preserves_original_metadata_and_ends_owned_processes(self):
        raw=SOURCE.read_bytes();functions=dict(parent.functions());previous=base.source_contract()
        r=generate();self.assertEqual(verify_report(r)['completed_messages'],list(MESSAGES))
        self.assertEqual(SOURCE.read_bytes(),raw);self.assertEqual(parent.functions(),functions);self.assertEqual(base.source_contract(),previous)
        for c in r['cases']:
            self.assertTrue(c['platform_abort']['owned_process_exited']);self.assertTrue(c['platform_abort']['unanswered']);self.assertIsNone(c['platform_cleanup'])


if __name__=='__main__':unittest.main()
