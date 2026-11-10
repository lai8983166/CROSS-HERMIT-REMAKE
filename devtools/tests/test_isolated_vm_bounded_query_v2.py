import json
import sys
import time
import unittest
from unittest.mock import patch
from devtools.isolated_vm_bounded_query_v2 import _supervise,request_script,runtime_paths


class BoundedQueryV2Tests(unittest.TestCase):
    def test_oversized_request_refused_before_start(self):
        with self.assertRaises(ValueError):request_script('read_text','kd-'+('a'*10000)+'/ready.json')
        with self.assertRaises(ValueError):_supervise({'x':'y'*2000},1)

    def test_actual_dependency_paths_without_site_hooks(self):
        code='import sys,json;json.loads(sys.stdin.readline());sys.path[:0]='+repr(runtime_paths())+';import winrm,requests,requests_ntlm;print(json.dumps(dict(ok=True,remote_completion="not_applicable")))'
        r=_supervise({},3,code)
        self.assertEqual(r['host_exit_code'],0);self.assertTrue(r['response']['ok']);self.assertEqual(r['host_job_active_after'],0)

    def test_late_completed_response_is_rejected(self):
        real_sleep=time.sleep
        def late_sleep(_):real_sleep(.4)
        code="import sys,json,time;sys.stdin.readline();time.sleep(.04);print(json.dumps(dict(ok=True,remote_completion='observed')))"
        with patch('devtools.isolated_vm_bounded_query_v2.time.sleep',late_sleep):r=_supervise({},.2,code)
        self.assertTrue(r['timed_out']);self.assertNotIn('response',r);self.assertEqual(r['remote_completion'],'unknown')

    def test_timeout_stops_owned_descendants(self):
        code="import sys,time,subprocess;sys.stdin.readline();subprocess.Popen([sys.executable,'-I','-S','-c','import time;time.sleep(30)']);time.sleep(30)"
        r=_supervise({},.5,code)
        self.assertTrue(r['timed_out']);self.assertEqual(r['host_job_active_after'],0);self.assertLess(r['elapsed_seconds'],3)


if __name__=='__main__':unittest.main()
