import json
import unittest
from tools.school_main_window_emulation import generate
from tools.school_main_window_verification import verify_report
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


if __name__=='__main__':unittest.main()
