import copy
import unittest
from unittest.mock import patch
from devtools import isolated_vm_battle_wait as host


class BattleWindowGateTests(unittest.TestCase):
    def setUp(self):
        self.proof=dict(long_capture_preflight_passed=True,errors=[],accepted=False)
        self.window=dict(bytes=10,sha256='a'*64)
        self.source=dict(phase='startup_preflight',error=None,input_isolation=dict(current_guest_uuid='abc',
            current_guest_boot_utc='2026-11-09T00:00:00Z',current_guest_resources=dict(logical_processors=2,memory_bytes=4*1024**3)),
            window_implementations=[dict(self.window,path='C:/ChaomofaWorker/project/devtools/terminal_battle_wait_window_v2.py')],
            preparation=dict(begin_ns=1,end_ns=2,outside_input_window=True,ETW_started=False,thread_duplicate_created=False),
            prepared_trigger=dict(begin_ns=4,end_ns=6,live_bytes_rechecked=True,fresh_owner_snapshot=True,original_ETW_start_tail_unchanged=True),
            capture_interval=dict(begin_ns=5),trigger_concurrency_preflight=dict(observation_begin_ns=3,observation_end_ns=7,
                input_submitted=False,trigger_error=None,original_deadline_seconds=11,input_window=dict(complete=True,maximum_seconds=11,elapsed_seconds=.2)))
        self.current=dict(uuid='ABC',boot='2026-11-09T00:00:00Z',cpu=2,memory=4*1024**3)

    def test_only_explicit_capability_allows_next_bounded_capture(self):
        host.preflight_gate(self.proof,self.source,self.current,self.window)
        for change in ({'long_capture_preflight_passed':False},{'errors':['missing wait']},{'accepted':True}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                host.preflight_gate(dict(self.proof,**change),self.source,self.current,self.window)

    def test_old_boot_wrong_machine_or_resources_cannot_reuse_preflight(self):
        for change in ({'boot':'another'},{'uuid':'wrong'},{'cpu':4},{'memory':8*1024**3}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                host.preflight_gate(self.proof,self.source,dict(self.current,**change),self.window)

    def test_changed_collector_or_non_preflight_source_rejected(self):
        with self.assertRaises(ValueError):host.preflight_gate(self.proof,self.source,self.current,dict(self.window,sha256='b'*64))
        with self.assertRaises(ValueError):host.preflight_gate(self.proof,dict(self.source,phase='battle_retreat'),self.current,self.window)

    def test_prepare_inside_input_window_or_increased_deadline_rejected(self):
        for mutation in (lambda s:s['preparation'].update(end_ns=4),
                         lambda s:s['trigger_concurrency_preflight']['input_window'].update(maximum_seconds=20),
                         lambda s:s['trigger_concurrency_preflight']['input_window'].update(elapsed_seconds=12),
                         lambda s:s['trigger_concurrency_preflight']['input_window'].update(complete=False)):
            changed=copy.deepcopy(self.source);mutation(changed)
            with self.assertRaises(ValueError):host.preflight_gate(self.proof,changed,self.current,self.window)

    def test_every_executed_producer_dependency_is_checked_not_just_entry(self):
        names=('terminal_battle_wait_window.py','terminal_battle_wait_window_v2.py','terminal_original_wait_etw.py',
               'terminal_wait_etw_probe.py','terminal_input_window.py')
        rows=[host.identity(host.ROOT/'devtools'/n)for n in names]
        source=dict(window_implementations=rows);proof=copy.deepcopy(source)
        host.authenticate_producers(source,proof)
        original=host.identity
        for name in names:
            def changed(path):
                row=original(path)
                if path.name==name:row['sha256']='0'*64
                return row
            with patch.object(host,'identity',changed),self.subTest(name=name),self.assertRaises(ValueError):
                host.authenticate_producers(source,proof)
        with self.assertRaises(ValueError):host.authenticate_producers(dict(window_implementations=rows[:-1]),proof)
        with self.assertRaises(ValueError):host.authenticate_producers(source,dict(window_implementations=list(reversed(rows))))


if __name__=='__main__':unittest.main()
