import json
import unittest
from tools.school_main_window_emulation import generate
from tools.school_main_window_verification import verify_report,source_runs
from tools.school_main_window import ROOT,parent


def report():return json.loads((ROOT/'analysis/school-main-window-trajectory-v1-20261020.json').read_text(encoding='utf8'))


class TaskTests(unittest.TestCase):
    def test_full_original_constructor_prefix_and32_task_slots(self):
        r=verify_report(report(),'tasks')
        self.assertEqual(r['original_task_slots'],32)

    def test_refuses_missing_reordered_or_adjacent_task_store(self):
        for mutation in ('missing','reorder','adjacent'):
            r=report();writes=r['cases'][0]['tasks']['native_writes'];indexes=[i for i,w in enumerate(writes) if w['pc']==0x42169B]
            if mutation=='missing':writes.pop(indexes[-1])
            elif mutation=='reorder':writes[indexes[0]],writes[indexes[1]]=writes[indexes[1]],writes[indexes[0]]
            else:writes[indexes[-1]]['pointer']=parent.OWNER+0x164
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'tasks')

    def test_refuses_wrong_instance_parent_return_or_loop_trace(self):
        for mutation in ('instance','return','REP','prefix'):
            r=report();t=r['cases'][0]['tasks']
            if mutation=='instance':t['state']['instance_value']=0x400000
            elif mutation=='return':t['returns'][0]['sp']+=4
            elif mutation=='REP':next(x for x in t['instruction_runs'] if x['count']>1)['count']-=1
            else:r['cases'][0]['constructor']['cpu']['ESP']+=4
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'tasks')


class QueryTests(unittest.TestCase):
    def test_original_title_query_boolean_and_natural_return(self):
        r=report();verify_report(r,'query')
        for c in r['cases']:
            hwnd=c['query']['platform_calls'][1]['result']['result']
            self.assertEqual(c['query']['cpu']['EAX'],int(hwnd!=0))
            self.assertEqual(c['query']['state']['owner'],c['tasks']['state']['owner'])

    def test_refuses_import_admission_cpu_memory_or_extra_map_change(self):
        for mutation in ('cpu','owner','map'):
            r=report();a=r['cases'][0]['query']['import_admission']
            if mutation=='cpu':a['after_cpu']['ESP']+=4
            elif mutation=='owner':a['retained_owner_sha256']='0'*64
            else:a['foreign_after'][0]['sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'query')

    def test_refuses_title_tail_source_pointer_or_query_ownership_fabrication(self):
        for mutation in ('tail','source','pointer','ownership'):
            r=report();calls=r['cases'][0]['query']['platform_calls']
            if mutation=='tail':calls[0]['result']['hex']=calls[0]['result']['hex'][:-2]+'ff'
            elif mutation=='source':calls[0]['request']['source_hex']='00'
            elif mutation=='pointer':calls[1]['args'][0]+=4
            else:calls[1]['result']['window_owned']=True
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'query')

    def test_refuses_synthesized_boolean_return_and_changed_helper_identity(self):
        for mutation in ('boolean','return','cleanup','build'):
            r=report();q=r['cases'][0]['query']
            if mutation=='boolean':q['cpu']['EAX']=1-q['cpu']['EAX']
            elif mutation=='return':q['returns'][-1]['sp']+=4
            elif mutation=='cleanup':r['cases'][0]['platform_cleanup']['user32_module_refs_released']=0
            else:r['platform_build']['helper_sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'query')


if __name__=='__main__':unittest.main()
