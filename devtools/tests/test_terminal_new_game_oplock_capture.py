"""Offline gate sequencing and fail-closed checks; no native imports execute."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from devtools import terminal_new_game_oplock_capture as capture


class GateTests(unittest.TestCase):
    def setup_case(self):
        sequence=[];session=capture.Session.__new__(capture.Session)
        session.pending=True;session.data={};session.c=None;tick=iter(range(100,120))
        session.owner=lambda: {'pid':1,'parent_pid':2,'debug_port':-1}
        session.data['owner_before']=session.owner()
        class Lock:
            receipt={'file_closed':False,'watchdog_release':False}
            def observe_break(self,ms):sequence.append('event');return True
            def release(self):
                if not self.receipt['file_closed']:sequence.append('release')
                self.receipt['file_closed']=True
        session.lock=Lock()
        def wait(h,ms):
            self.assertTrue(session.lock.receipt['file_closed']);sequence.append('wait_exit');return 0
        session.w=SimpleNamespace(qpc=lambda:next(tick),wait=wait)
        worker={'pointer':11,'thread_id':22}
        observer=SimpleNamespace(handles={(11,22):33},api=SimpleNamespace(status=lambda h:0),
            workers=[worker],owned=SimpleNamespace(elapsed=lambda:1.))
        row={'tasks':[{'vtable':capture.old.NEW_GAME,'TLS':{},'pointer':11,'thread_id':22}],
             'frames':[{'tid':22,'oplock_file_open':{'captured_qpc':101}}], 'elapsed':.5}
        return session,observer,row,sequence

    def test_one_event_capture_then_release_then_original_exit(self):
        s,c,row,sequence=self.setup_case()
        def snapshot(_):sequence.append('snapshot');return row
        with patch.object(capture.old.Capture,'snapshot',snapshot):self.assertIs(s.collect(c),row)
        self.assertEqual(sequence,['event','snapshot','release','wait_exit'])
        self.assertEqual(c.workers[0]['exit']['code'],0);self.assertFalse(s.pending)
        with self.assertRaisesRegex(ValueError,'outstanding'):s.collect(c)

    def test_wrong_live_worker_never_waits_or_retries(self):
        s,c,row,sequence=self.setup_case();row['tasks']=[]
        with patch.object(capture.old.Capture,'snapshot',lambda _:row):
            with self.assertRaisesRegex(ValueError,'live NEW_GAME'):s.collect(c)
        self.assertEqual(sequence,['event','release']);self.assertFalse(s.pending)

    def test_watchdog_between_event_and_snapshot_rejects(self):
        s,c,row,sequence=self.setup_case();s.lock.receipt={'file_closed':False,'watchdog_release':False}
        def snapshot(_):s.lock.receipt['watchdog_release']=True;return row
        with patch.object(capture.old.Capture,'snapshot',snapshot):
            with self.assertRaisesRegex(ValueError,'throughout'):s.collect(c)
        self.assertNotIn('wait_exit',sequence);self.assertFalse(s.pending)


if __name__=='__main__':unittest.main()
