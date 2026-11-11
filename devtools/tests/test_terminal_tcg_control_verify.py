import copy,unittest
from devtools.terminal_tcg_control_verify import evaluate
from devtools.terminal_tcg_guest_query import UUID

class ControlContract(unittest.TestCase):
    def setUp(self):
        self.status=dict(errors=[],host_job_active_after=0,host_exit_code=0,remote_completion='observed',
            response=dict(ok=True,value=dict(computer='CHAOMOFA-WORKER',manufacturer='QEMU',uuid=UUID,cpu=2,memory=4*1024**3,boot='owned-boot')))
        self.report=dict(errors=[],all_processes_exited=True,parent_size_mtime_unchanged=True,observations=[dict(control=self.status)])
        self.sidecar=dict(errors=[],process_exited=True,host_job_active_after=0,stop_requested=True)
    def test_scoped_success_is_not_replay_admission(self):
        r=evaluate(self.report,self.sidecar)
        self.assertTrue(r['control_preflight_passed']);self.assertFalse(r['full_state_replay_admitted']);self.assertFalse(r['accepted'])
    def test_timeout_cannot_be_promoted(self):
        self.status['timed_out']=True
        self.assertFalse(evaluate(self.report,self.sidecar)['control_preflight_passed'])
    def test_foreign_guest_rejected(self):
        self.status['response']['value']['uuid']='foreign'
        self.assertFalse(evaluate(self.report,self.sidecar)['control_preflight_passed'])
    def test_sidecar_cleanup_required(self):
        self.sidecar['host_job_active_after']=1
        self.assertFalse(evaluate(self.report,self.sidecar)['control_preflight_passed'])
    def test_wow64_requires_actual_32bit_and_exit(self):
        self.report['wow64']=copy.deepcopy(self.status)
        value=dict(pointer_bytes=4,process64=False,os64=True,child_exited=True,uuid=UUID)
        self.report['wow64']['response']['value']=value
        self.assertTrue(evaluate(self.report,self.sidecar)['wow64_process_preflight_passed'])
        for key,bad in [('pointer_bytes',8),('process64',True),('os64',False),('child_exited',False)]:
            changed=copy.deepcopy(self.report);changed['wow64']['response']['value'][key]=bad
            self.assertFalse(evaluate(changed,self.sidecar)['wow64_process_preflight_passed'])

if __name__=='__main__':unittest.main()
