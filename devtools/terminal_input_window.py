"""Bounded continuous input observation, including slow pre-input checks.

Only a recent window is retained. Original press/held/release evidence must still
pass the independent verifier; eviction never synthesizes an input edge.
"""
from collections import deque
import time


def observe(worker, capture, record, *, after_finished=None,
            clock=time.monotonic, sleep=time.sleep, wall_clock=time.time_ns):
    rows=deque(record.get('input_samples',()),maxlen=1024)
    captured=len(rows);start=clock();finished=None;finished_wall=None;complete=False
    try:
        while clock()-start<11:
            rows.append(capture());captured+=1
            if not worker.is_alive():
                if finished is None:finished=clock();finished_wall=wall_clock()
                if after_finished is not None:after_finished()
                if clock()-finished>=.1:
                    rows.append(capture());captured+=1
                    complete=True;break
            sleep(.005)
        if not complete:
            raise ValueError('mouse action did not finish inside continuous observation window')
    finally:
        record['input_samples']=list(rows)
        record['input_window']=dict(maximum_seconds=11,maximum_retained_samples=1024,
            retained_samples=len(rows),captured_samples=captured,evicted_samples=captured-len(rows),
            complete=complete,elapsed_seconds=clock()-start,finished_wall_time_ns=finished_wall)
