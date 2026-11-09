"""Bounded fresh retries when the actual suspended thread inventory changes.

Only an inventory difference is retryable, after every owned suspend scope has
restored successfully. No failed attempt supplies a snapshot or an input guard.
"""
from contextlib import ExitStack,contextmanager
import time
from devtools import terminal_worker_retention_v2 as parent
from devtools import terminal_original_wait_etw as original_wait
from devtools.terminal_scene_resources import clone

base=parent.base
need=parent.need
MAX_ATTEMPTS=5
RETRY_BUDGET_NS=500_000_000


class CohortChanged(ValueError):
    def __init__(self,before,after):
        super().__init__('actual thread inventory changed before snapshot; no source row emitted')
        self.before=list(before);self.after=list(after)


@contextmanager
def owned_cohort(c,main_tid,backend=base):
    with ExitStack()as stack:
        frames=list(stack.enter_context(original_wait.owned_frames(c,[main_tid],backend)))
        before=backend.original.threads(c.pid)
        need(main_tid in before and 0<len(before)<=256 and len(before)==len(set(before)),
             'bounded unique current game cohort includes MAIN')
        for tid in before:
            if tid!=main_tid:frames.extend(stack.enter_context(original_wait.owned_frames(c,[tid],backend)))
        after=backend.original.threads(c.pid)
        need(main_tid in after and 0<len(after)<=256 and len(after)==len(set(after)),
             'bounded current game cohort still includes MAIN')
        if set(before)!=set(after):raise CohortChanged(before,after)
        yield frames


class WorkerRetention(parent.WorkerRetention):
    def __init__(self,c,main_tid,backend=base,cohort=owned_cohort,snapshot=parent.parent.school.snapshot):
        super().__init__(c,main_tid,backend,cohort,snapshot)

    def capture(self,owned):
        retries=[];started=time.perf_counter_ns()
        for attempt in range(1,MAX_ATTEMPTS+1):
            begin=time.perf_counter_ns()
            if retries and begin-started>=RETRY_BUDGET_NS:break
            try:
                row=super().capture(owned)
            except CohortChanged as exc:
                # This except runs after ExitStack completed. A resume/close
                # failure replaces CohortChanged and is deliberately not caught.
                retries.append(dict(pid=self.c.pid,main_tid=self.main_tid,attempt=attempt,
                    before_tids=exc.before,after_tids=exc.after,capture_begin_perf_ns=begin,
                    capture_end_perf_ns=time.perf_counter_ns(),owned_suspend_restored=True,
                    source_snapshot_emitted=False))
                if attempt<MAX_ATTEMPTS:time.sleep(.01)
                continue
            row['cohort_observation_retries']=retries
            row['cohort_retry_budget']=dict(maximum_attempts=MAX_ATTEMPTS,retry_budget_ns=RETRY_BUDGET_NS,
                started_perf_ns=started,successful_attempt_begin_perf_ns=begin,
                deadline_applies_to_next_attempt_start=True)
            return row
        self.failure=dict(error='bounded thread inventory retries exhausted',attempts=retries,
            pid=self.c.pid,main_tid=self.main_tid,source_snapshot_emitted=False)
        raise ValueError(self.failure['error'])


continue_school=clone(parent.parent.continue_school,WorkerRetention=WorkerRetention,
                      progress_signature=parent.progress_signature)
