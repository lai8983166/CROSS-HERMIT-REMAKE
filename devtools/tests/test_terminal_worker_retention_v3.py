from contextlib import contextmanager
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from devtools import terminal_worker_retention_v3 as v


class CohortRetryTests(unittest.TestCase):
    def test_inventory_change_restores_every_hold_before_retryable_exception_escapes(self):
        calls=[];inventories=iter([[77,88],[77,88,99]])
        @contextmanager
        def held(c,tids,backend):
            tid=tids[0];calls.append(('hold',tid))
            try:yield [dict(tid=tid)]
            finally:calls.append(('restore',tid))
        backend=SimpleNamespace(original=SimpleNamespace(threads=lambda pid:next(inventories)))
        with patch.object(v.original_wait,'owned_frames',held):
            with self.assertRaises(v.CohortChanged)as error:
                with v.owned_cohort(SimpleNamespace(pid=7),77,backend):self.fail('unstable snapshot')
        self.assertEqual(error.exception.before,[77,88]);self.assertEqual(error.exception.after,[77,88,99])
        self.assertEqual(calls,[('hold',77),('hold',88),('restore',88),('restore',77)])

    def test_retry_returns_only_fresh_successful_row_and_keeps_difference(self):
        tracker=v.WorkerRetention(SimpleNamespace(pid=7),77)
        row=dict(worker_retention={})
        with patch.object(v.parent.WorkerRetention,'capture',side_effect=[v.CohortChanged([77],[77,88]),row])as capture:
            with patch.object(v.time,'sleep'):result=tracker.capture(None)
        self.assertIs(result,row);self.assertEqual(capture.call_count,2)
        self.assertEqual(result['cohort_observation_retries'][0]['after_tids'],[77,88])
        self.assertFalse(result['cohort_observation_retries'][0]['source_snapshot_emitted'])

    def test_restore_and_identity_errors_are_never_retried(self):
        tracker=v.WorkerRetention(SimpleNamespace(pid=7),77)
        for message in ('own suspend increment restore count mismatch','thread owner mismatch'):
            with patch.object(v.parent.WorkerRetention,'capture',side_effect=ValueError(message))as capture:
                with self.assertRaisesRegex(ValueError,message):tracker.capture(None)
                self.assertEqual(capture.call_count,1)

    def test_exhaustion_retains_bounded_inventory_differences_without_source(self):
        tracker=v.WorkerRetention(SimpleNamespace(pid=7),77)
        with patch.object(v.parent.WorkerRetention,'capture',side_effect=v.CohortChanged([77],[77,88]))as capture:
            with patch.object(v.time,'sleep'):
                with self.assertRaisesRegex(ValueError,'retries exhausted'):tracker.capture(None)
        self.assertEqual(capture.call_count,5);self.assertEqual(len(tracker.failure['attempts']),5)
        self.assertFalse(tracker.failure['source_snapshot_emitted'])

    def test_retry_budget_prevents_starting_another_attempt(self):
        tracker=v.WorkerRetention(SimpleNamespace(pid=7),77)
        with patch.object(v.parent.WorkerRetention,'capture',side_effect=v.CohortChanged([77],[77,88]))as capture:
            with patch.object(v.time,'sleep'),patch.object(v.time,'perf_counter_ns',side_effect=[1,2,3,600_000_002]):
                with self.assertRaisesRegex(ValueError,'retries exhausted'):tracker.capture(None)
        self.assertEqual(capture.call_count,1);self.assertEqual(len(tracker.failure['attempts']),1)


if __name__=='__main__':unittest.main()
