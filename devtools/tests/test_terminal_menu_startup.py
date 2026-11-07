import copy
import unittest
from devtools.terminal_menu_startup import retired_menu


class RetirementGateTests(unittest.TestCase):
    def fixture(self):
        return ({'worker':{'node':0x10000},'worker_exit':{'wait_status':0,'exit_code':0,'before_WM_CLOSE':True}},
                {'startup_thread_exited':True,'MAIN_event_hex':'00'*8,
                 'registered_tasks':[{'head_hex':'60b05900'+'00'*44}]})
    def test_does_not_require_animation_trigger(self):
        p,r=self.fixture();self.assertTrue(retired_menu(p,r))
        p['natural_animation_limit_observed']=False;self.assertTrue(retired_menu(p,r))
    def test_exit_and_wait_errors_refused(self):
        for field,value in (('wait_status',258),('wait_status',0xffffffff),('exit_code',0xc0000005),('before_WM_CLOSE',False)):
            p,r=self.fixture();p['worker_exit'][field]=value
            with self.subTest(field=field,value=value):self.assertFalse(retired_menu(p,r))
    def test_unrelated_or_overlapping_nodes_refused(self):
        p,r=self.fixture();r['registered_tasks'].append({'head_hex':'48aa5c00'+'00'*44})
        self.assertFalse(retired_menu(p,r))
        r['registered_tasks']=r['registered_tasks'][1:];self.assertFalse(retired_menu(p,r))
    def test_pending_event_and_missing_worker_refused(self):
        p,r=self.fixture();r['MAIN_event_hex']='01000000'+'00'*4;self.assertFalse(retired_menu(p,r))
        p,r=self.fixture();p.pop('worker');self.assertFalse(retired_menu(p,r))
    def test_unsignaled_sample_refused(self):
        p,r=self.fixture();r['startup_thread_exited']=False;self.assertFalse(retired_menu(p,r))


if __name__=='__main__':unittest.main()
