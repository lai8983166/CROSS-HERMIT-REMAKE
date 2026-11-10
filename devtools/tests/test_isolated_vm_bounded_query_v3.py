import unittest
from unittest.mock import patch
from devtools.isolated_vm_bounded_query_v3 import _supervise,Job,completed
from devtools.tests.test_isolated_vm_bounded_query_v2 import BoundedQueryV2Tests
from devtools import isolated_vm_bounded_query_v2 as old
from devtools import isolated_vm_bounded_query_v3 as new


class CleanupTests(unittest.TestCase):
    def test_initialization_failure_closes_job(self):
        with patch.object(new,'runtime_paths',side_effect=OSError('injected')):r=_supervise({},1)
        self.assertTrue(r['errors']);self.assertIn('elapsed_seconds',r);self.assertNotIn('host_pid',r)

    def test_close_failure_is_reported_without_skipping_final_record(self):
        original=Job.close
        def failing_close(job):original(job);raise OSError('injected')
        with patch.object(Job,'close',failing_close):
            r=_supervise({},2,"import sys,json;sys.stdin.readline();print(json.dumps(dict(ok=True,remote_completion='observed')))")
        self.assertIn('job close: OSError',r['errors']);self.assertIn('elapsed_seconds',r);self.assertFalse(completed(r))

    def test_all_v2_behaviors_against_final_implementation(self):
        # Reuse the earlier cases but redirect their global API and sleep module.
        from devtools.tests import test_isolated_vm_bounded_query_v2 as prior
        with patch.object(prior,'_supervise',new._supervise),patch.object(prior,'request_script',new.request_script),patch.object(prior,'runtime_paths',new.runtime_paths):
            for name in unittest.defaultTestLoader.getTestCaseNames(BoundedQueryV2Tests):
                case=BoundedQueryV2Tests(name);result=unittest.TestResult();case.run(result)
                self.assertTrue(result.wasSuccessful(),str(result.errors+result.failures))


if __name__=='__main__':unittest.main()
