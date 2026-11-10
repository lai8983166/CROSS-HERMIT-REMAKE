import json
import unittest
from devtools.isolated_vm_bounded_query import _supervise,request_script


class BoundedQueryTests(unittest.TestCase):
    def test_owned_path_and_mutation_rejected(self):
        for action,arg in [('read_text','../private.json'),('read_text','kd-test/a.json;whoami'),('run_script','Remove-Item x'),('sleep_echo',16)]:
            with self.assertRaises(ValueError):request_script(action,arg)

    def test_normal_child_response(self):
        code="import sys,json;json.loads(sys.stdin.readline());print(json.dumps(dict(ok=True,remote_completion='observed')))"
        r=_supervise({},2,code)
        self.assertTrue(r['assigned_before_request']);self.assertEqual(r['host_job_active_after'],0)
        self.assertEqual(r['remote_completion'],'observed');self.assertFalse(r['errors'])

    def test_hung_child_and_descendant_have_one_deadline(self):
        code="import sys,time,subprocess,json;json.loads(sys.stdin.readline());subprocess.Popen([sys.executable,'-I','-S','-c','import time;time.sleep(30)']);time.sleep(30)"
        r=_supervise({},.5,code)
        self.assertTrue(r['timed_out']);self.assertEqual(r['host_job_active_after'],0)
        self.assertEqual(r['remote_completion'],'unknown');self.assertLess(r['elapsed_seconds'],3)

    def test_invalid_output_does_not_prove_remote_completion(self):
        r=_supervise({},2,"import sys;sys.stdin.readline();print('not-json')")
        self.assertIn('invalid worker response',r['errors']);self.assertEqual(r['remote_completion'],'unknown')

    def test_output_limit(self):
        r=_supervise({},2,"import sys;sys.stdin.readline();print('x'*2200000)")
        self.assertIn('output budget',r['errors']);self.assertEqual(r['host_job_active_after'],0)


if __name__=='__main__':unittest.main()
