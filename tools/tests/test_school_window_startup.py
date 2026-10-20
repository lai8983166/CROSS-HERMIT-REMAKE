import json,unittest
from tools.school_window_startup import ROOT,SOURCE,SOURCE_SHA256,generate
from tools.school_window_startup_verification import verify_report,verify_case
from tools.school_startup_inputs import observe,verify_observation
from tools.school_window_module_validation import digest


def report():return json.loads((ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json').read_text(encoding='utf8'))


class StartupTests(unittest.TestCase):
    def test_natural_creation_and_publication_with_independent_nested_replay(self):
        r=report();before=digest(r);v=verify_report(r);self.assertEqual(before,digest(r))
        for c,p in zip(r['cases'],v['case_proofs']):
            self.assertEqual((p['callback_count'],p['max_depth']),(17,3));self.assertTrue(p['creation_returned'] and p['HWND_published'])
            self.assertEqual(p['pending_original_EIP'],'0x4504e1')
            self.assertEqual([(n['message'],n['depth']) for n in p['callbacks']][10:14],[(6,1),(641,2),(642,3),(7,2)])
            self.assertEqual(c['hwnd_publication']['native_writes'][-1],dict(pc=0x4504dc,pointer=0x7a0bb4,bytes=4,value=c['creation_result']['result']))

    def test_refuses_nested_depth_subtree_state_or_access_corruption(self):
        for mutation in ('depth','subtree','restore','read','write'):
            c=report()['cases'][0];n=c['callbacks'][11]
            if mutation=='depth':n['setup']['packet']['depth']=1
            elif mutation=='subtree':c['callbacks'][10]['platform_calls'][-1]['nested_callback_ids']=[]
            elif mutation=='restore':n['outer_guest_buffers_restored']=False
            elif mutation=='read':n['native_reads'].pop()
            else:n['native_writes'][0]['value']^=1
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c)

    def test_refuses_late_declared_inputs_wrong_fresh_image_or_read(self):
        for mutation in ('late','value','image','read'):
            c=report()['cases'][0]
            if mutation=='late':c['initial_input_declaration']['prefix_instruction_count']=1
            elif mutation=='value':c['initial_input_declaration']['globals']['0x7a49fc']=0x04d70068
            elif mutation=='image':c['constructor']['state']['image_sha256']='0'*64
            else:c['declared_input_reads'][0]['hex']='6800d704'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_case(c)

    def test_refuses_bad_native_return_publication_protocol_or_cleanup(self):
        for mutation in ('return','publication','protocol','cleanup','forward'):
            r=report();c=r['cases'][0]
            if mutation=='return':c['creation_result']['result']^=1
            elif mutation=='publication':c['hwnd_publication']['native_writes'][-1]['value']^=1
            elif mutation=='protocol':c['wire'].pop()
            elif mutation=='cleanup':c['lifetime']['explicit_normal_cleanup']=True
            else:c['callbacks'][5]['platform_calls'][-1]['result']['host_args'][2]=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r)

    def test_fresh_real_observation_and_full_startup_preserve_original(self):
        original=SOURCE.read_bytes();o=observe();self.assertEqual(verify_observation(o),{0x7a49fc:0,0x80a398:0})
        bad=json.loads(json.dumps(o));bad['result']['globals']['0x7a49fc']='01000000'
        with self.assertRaises(ValueError):verify_observation(bad)
        r=generate();self.assertTrue(verify_report(r)['original_creation_returned'])
        self.assertEqual(SOURCE.read_bytes(),original)


if __name__=='__main__':unittest.main()
