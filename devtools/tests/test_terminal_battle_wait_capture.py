"""Exercise adapter wiring against fake external layers; no game/VM/input calls."""
from contextlib import ExitStack,contextmanager
import ctypes as C
import ctypes.wintypes as W
from types import SimpleNamespace
import time
import unittest
from unittest.mock import patch
from devtools import terminal_battle_wait_capture as capture


class BattleCaptureAdapterTests(unittest.TestCase):
    def test_cloned_controller_triggers_one_trace_and_retains_original_receipt(self):
        from devtools import terminal_school_handoff as school,terminal_battle_input as battle
        from devtools import terminal_scene_owner as base
        events=[];writes=[];controllers=[]
        class Observer:
            def __init__(self,*args):
                events.append('construct');self.active=False;self.kernel=object()
                self.result=dict(error=None,kind='battle_wait_result_window',phase='battle_retreat')
            @contextmanager
            def synchronized_input_snapshots(self):
                events.append('scope');yield;events.append('restore')
            def begin(self):events.append('start');self.active=True
            def prepare(self):events.append('prepare')
            def poll(self):events.append('poll')
            def drain(self):events.append('drain')
            def finish(self):events.append('finish')
        class Dep:
            rows=[];error=None
            def __enter__(self):return self
            def __exit__(self,*args):pass
        @contextmanager
        def factory_scope():
            yield SimpleNamespace(menu_run=school.menu.run,receipts=dict(scope_errors=[]))
        def original_input(c,h,stage,*,explicit_user_override):
            self.assertEqual(stage,'confirmation');self.assertTrue(explicit_user_override)
            api=make_api(c,h,100)  # Deliberately supplied by clone's globals.
            self.assertFalse(api.left_button_down());self.assertFalse(api.left_button_down())
            events.append('down')
            return dict(released=True,down_wall_time_ns=50,up_wall_time_ns=60,error=None)
        def original_observe(action,c,owned,row):
            action.attempted=True
            result=action.send(c,99)
            action.receipt=dict(stage='confirmation',action=result,error=None)
            observe_input_window(None,lambda:{'input':'unchanged'},action.receipt)
        def input_observe(worker,sample,record,**kwargs):
            self.assertEqual(sample(),{'input':'unchanged'})
        def original_school(out,seconds):
            controller=SchoolController(0,True,192)  # Actual clone must install adapter.
            controllers.append(controller)
            action=controller.battle[1];action.ready=lambda row:True;action.since=time.monotonic()-2
            action.observe(SimpleNamespace(pid=123),object(),dict(tasks=[dict(pointer=1000,thread_id=2)]))
            return dict(probe=dict(error=None,battle_inputs=[action.receipt],stop_reason='fixture'),
                lifecycle={},mutable_private_runtime_files=[],input_isolation={})
        def owner(hwnd,ptr):C.cast(ptr,C.POINTER(W.DWORD)).contents.value=123;return 3
        with ExitStack()as stack:
            stack.enter_context(patch('devtools.native_input_isolation.require_qualified_guest',return_value={}))
            stack.enter_context(patch('devtools.isolated_guest_dep_observer.DepObserver',Dep))
            stack.enter_context(patch('devtools.terminal_factory_focus.scope',factory_scope))
            stack.enter_context(patch('devtools.terminal_input_window.observe',input_observe))
            stack.enter_context(patch.object(school,'run',original_school))
            stack.enter_context(patch.object(school.OwnedAction,'observe',original_observe))
            stack.enter_context(patch.object(battle,'action',original_input))
            stack.enter_context(patch.object(battle,'make_api',return_value=SimpleNamespace(left_button_down=lambda:False,submit=lambda p:1)))
            stack.enter_context(patch.object(base.original,'findwindow',return_value=99))
            stack.enter_context(patch.object(base.original,'ownerpid',owner))
            stack.enter_context(patch.object(capture.window,'WaitWindow',Observer))
            stack.enter_context(patch.object(capture.window.original,'utc_now_ns',return_value=40))
            stack.enter_context(patch.object(capture.window,'identity',side_effect=lambda p:dict(path=str(p),bytes=1,sha256='a'*64)))
            stack.enter_context(patch.object(capture,'write_gzip',side_effect=lambda p,r,*limits:writes.append((p,r))))
            out=capture.ROOT/'analysis/terminal-battle-wait-never-written-adapter-test.json.gz'
            result=capture.run(out)
        self.assertEqual(events,['construct','prepare','scope','start','down','poll','drain','restore','finish'])
        self.assertEqual(len(controllers),1);self.assertEqual(len(writes),2)
        self.assertEqual(result['start_trigger'],'second_left_button_down_query')
        self.assertEqual(result['input_receipt']['down_wall_time_ns'],50)
        self.assertTrue(result['input_receipt']['released'])
        self.assertEqual(result['input_receipt']['object_path'],['probe','battle_inputs',0])
        self.assertEqual(writes[0][1]['probe']['battle_inputs'][0]['action']['up_wall_time_ns'],60)
        self.assertFalse(out.exists())

    def test_precise_clock_brackets_actual_unchanged_input_packet(self):
        from devtools.terminal_menu_input import packet
        p=packet(flags=2);calls=[];records=[]
        api=SimpleNamespace(submit=lambda value:calls.append(value)or 1)
        with patch.object(capture.window.original,'utc_now_ns',side_effect=[100,120]):
            wrapped=capture.precise_submit_api(api,object(),records)
            self.assertEqual(wrapped.submit(p),1)
        self.assertIs(calls[0],p)
        self.assertEqual((records[0]['begin_ns'],records[0]['end_ns'],records[0]['flags']),(100,120,2))
        self.assertEqual(records[0]['packet_hex'],C.string_at(C.byref(p),C.sizeof(p)).hex())


if __name__=='__main__':unittest.main()
