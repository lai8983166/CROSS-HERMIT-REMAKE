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


class ConstructorTests(unittest.TestCase):
    def test_complete_native_constructor_and_real_system_protocol(self):
        r=verify_report(report(),'constructor')
        self.assertEqual(r['constructor_calls_per_case'],26)
        self.assertEqual(r['real_system_calls_per_case'],13)
        self.assertFalse(r['original_publication_verified'])

    def test_refuses_zero_length_clear_rewrite_and_wrong_subobject_receiver(self):
        for receiver in (False,True):
            r=report();entries=r['cases'][0]['constructor']['entries']
            if receiver:entries[1]['receiver']+=4
            else:next(e for e in entries if e['return_va']=='0x429749')['args']=[0x7A2000,0,525]
            with self.subTest(receiver=receiver),self.assertRaises(ValueError):verify_report(r,'constructor')

    def test_refuses_system_argument_buffer_tail_and_void_status_fabrication(self):
        for mutation in ('args','tail','void','return_pointer','guards'):
            r=report();calls=r['cases'][0]['constructor']['platform_calls']
            if mutation=='args':calls[2]['args'][1]=1
            elif mutation=='tail':calls[3]['result']['hex']=calls[3]['result']['hex'][:-2]+'ff'
            elif mutation=='void':calls[0]['result']['eax_is_status']=True
            elif mutation=='return_pointer':calls[4]['observed_EAX']+=1
            else:calls[5]['result']['guards_unchanged']=False
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'constructor')

    def test_refuses_missing_original_writes_returns_and_modified_object(self):
        for mutation in ('write','value','return','object','SEH'):
            r=report();n=r['cases'][0]['constructor']
            if mutation=='write':n['native_writes'].pop()
            elif mutation=='value':next(w for w in n['native_writes'] if w['pointer']==0x20000180)['value']=1
            elif mutation=='return':n['returns'][-1]['return_va']='0x49ddf1'
            elif mutation=='object':n['state']['owner']['sha256']='0'*64
            else:n['state']['SEH']=1
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'constructor')

    def test_refuses_incomplete_repetitions_and_unbalanced_live_resources(self):
        for mutation in ('REP','cleanup','helper'):
            r=report();c=r['cases'][0]
            if mutation=='REP':next(x for x in c['constructor']['instruction_runs'] if x['count']>1)['count']-=1
            elif mutation=='cleanup':c['platform_cleanup']['event_handles_closed']=0
            else:r['platform_build']['helper_sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'constructor')


class PublicationTests(unittest.TestCase):
    def test_native_publication_keeps_inherited_cache_and_full_object(self):
        r=verify_report(report())
        self.assertTrue(r['original_publication_verified'])
        self.assertFalse(r['retained_VM_advanced'])
        for c in report()['cases']:
            self.assertEqual(c['publication']['state']['global_value'],0x20000000)
            self.assertEqual(c['publication']['state']['owner'],c['constructor']['state']['owner'])
            self.assertEqual(c['publication']['platform_calls'],[])

    def test_refuses_handwritten_global_and_false_full_WinMain_claim(self):
        for mutation in ('instruction','global','continuity','scope','saved_register'):
            r=report();p=r['cases'][0]['publication']
            if mutation=='instruction':next(w for w in p['native_writes'] if w['pointer']==0x7A4A00)['pc']=0x49DDFE
            elif mutation=='global':p['state']['global_value']=0x04D60B38
            elif mutation=='continuity':p['before_cpu']['EIP']+=1
            elif mutation=='scope':r['WinMain_prelude_executed']=True
            else:p['cpu']['EBX']=0
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r)

    def test_fresh_two_case_continuous_execution(self):
        r=generate()
        self.assertEqual(verify_report(r),verify_report(report()))
        for c in r['cases']:
            self.assertEqual(c['constructor']['before_cpu'],c['allocation']['cpu'])
            self.assertEqual(c['publication']['before_cpu'],c['constructor']['cpu'])
            self.assertTrue(c['platform_cleanup']['all_owned_resources_released'])


if __name__=='__main__':unittest.main()
