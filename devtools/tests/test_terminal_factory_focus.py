"""Factory/focus ordering only; synthetic methods never invoke native input."""
import copy
import unittest
from unittest.mock import patch

from devtools import terminal_factory_focus as v
from devtools.terminal_scene_resources import clone


def frames(*sites):
    return [dict(tid=9,EIP=0x401000,chain=[dict(return_va=a)for a in sites])]


def capture(h,pid,fs,g,elapsed,raw,objects=False):
    result=dict(pid=pid,elapsed=elapsed,globals=g,frames=fs,source={'hex':'1234'})
    if objects:
        result.update(window=dict(pid=pid),main=dict(pointer=g['0x7a4a00']),
                      game=dict(pointer=g['0x7a49fc']),cache=dict(pointer=g['0x80a398']))
    return result


class Base:
    def __init__(self):self.handles={7:50};self.enumerations=0;self.focus_calls=0
    def members(self):self.enumerations+=1;return [7]
    def elapsed(self):return 2.0


class Focused(Base):
    def members(self):
        members=super().members();self.focus_calls+=1
        return members


class FactoryFocusTests(unittest.TestCase):
    def setUp(self):
        qualified=patch.object(v,'require_qualified_guest',return_value={'synthetic_test_only':True})
        qualified.start();self.addCleanup(qualified.stop)
        self.g=v.FactoryFocusGate(capture,lambda:7)
        self.runtime=self.g.deferred_runtime(Focused)()
        self.globals={'0x7a4a00':1,'0x7a49fc':2,'0x80a398':3}

    def record(self,fs,objects=False,h=50,pid=7):
        return self.g.capture(h,pid,fs,self.globals,1.0,b'raw',objects)

    def test_original_focused_members_only_after_both_complete_captures(self):
        self.assertEqual(self.runtime.members(),[7]);self.assertEqual(self.runtime.focus_calls,0)
        factory=frames(0x49DF8A,0x45060F);before=copy.deepcopy(factory)
        result=self.record(factory)
        self.assertIs(result['frames'],factory);self.assertEqual(factory,before)
        self.runtime.members();self.assertEqual(self.runtime.focus_calls,0)
        ready=frames(0x49DFD1);self.record(ready,True)
        self.runtime.members();self.assertEqual(self.runtime.focus_calls,1)
        self.runtime.members();self.assertEqual(self.runtime.focus_calls,2)
        self.assertEqual([x['kind']for x in self.g.receipts['captures']],['factory','ready'])
        self.assertEqual(len(self.g.receipts['focused_members_resumed']),1)
        self.assertFalse(self.g.receipts['focused_members_resumed'][0]['activation_success_claimed'])

    def test_factory_sites_must_share_one_original_frame(self):
        self.record(frames(0x49DF8A)+frames(0x45060F))
        self.record(frames(0x49DFD1),True);self.runtime.members()
        self.assertEqual(self.runtime.focus_calls,0)
        self.assertEqual([x['kind']for x in self.g.receipts['captures']],['ready'])

    def test_ready_requires_objects_true_and_actual_winmain_loop(self):
        self.record(frames(0x49DF8A,0x45060F))
        self.record(frames(0x49DFD1),False);self.runtime.members()
        self.record(frames(0x401000),True);self.runtime.members()
        self.assertEqual(self.runtime.focus_calls,0)
        self.assertEqual([x['kind']for x in self.g.receipts['captures']],['factory'])

    def test_other_pid_handle_or_window_never_opens_target_gate(self):
        self.record(frames(0x49DF8A,0x45060F))
        self.record(frames(0x49DFD1),True,h=51)
        self.runtime.members();self.assertEqual(self.runtime.focus_calls,0)
        self.record(frames(0x49DFD1),True)
        self.g.window_owner=lambda:8
        self.runtime.members();self.assertEqual(self.runtime.focus_calls,0)
        self.g.window_owner=lambda:7;self.runtime.handles[7]=52
        self.runtime.members();self.assertEqual(self.runtime.focus_calls,0)

    def test_throwing_original_capture_never_marks_factory(self):
        def bad(*args,**kwargs):raise OSError('original capture failed')
        self.g.original_capture=bad
        with self.assertRaisesRegex(OSError,'original capture failed'):
            self.record(frames(0x49DF8A,0x45060F))
        self.assertEqual(self.g.receipts['captures'],[]);self.runtime.members()
        self.assertEqual(self.runtime.focus_calls,0)

    def test_focus_error_remains_original_error_without_success_receipt(self):
        class FailedFocus(Base):
            def members(self):raise ValueError('original foreground guard rejected')
        runtime=self.g.deferred_runtime(FailedFocus)()
        runtime.members()  # Deferral skips exactly the original focus override.
        self.record(frames(0x49DF8A,0x45060F));self.record(frames(0x49DFD1),True)
        with self.assertRaisesRegex(ValueError,'foreground guard rejected'):runtime.members()
        self.assertFalse(self.g.receipts['activation_success_inferred'])

    def test_scope_hook_and_original_globals_restore_on_exception(self):
        original=v.base.original.capture
        with self.assertRaisesRegex(RuntimeError,'caller failure'):
            with v.scope()as scoped:
                self.assertIsNot(v.base.original.capture,original)
                self.assertIs(scoped.menu_run.__globals__['base'],v.menu.base)
                self.assertEqual(scoped.menu_run.__globals__['__file__'],v.menu.__file__)
                sentinel=object();adapted=clone(scoped.menu_run,OneMenuSelection=sentinel)
                self.assertIs(adapted.__globals__['OneMenuSelection'],sentinel)
                self.assertIs(adapted.__globals__['_deferred_runtime'],scoped.menu_run.__globals__['_deferred_runtime'])
                raise RuntimeError('caller failure')
        self.assertIs(v.base.original.capture,original)
        self.assertTrue(scoped.receipts['capture_hook_restored'])
        self.assertEqual(scoped.receipts['scope_errors'],[])

    def test_scope_reentry_and_hook_tampering_fail_closed(self):
        original=v.base.original.capture
        with v.scope():
            with self.assertRaisesRegex(ValueError,'cannot overlap or reenter'):
                with v.scope():pass
        with self.assertRaisesRegex(ValueError,'capture hook changed'):
            with v.scope()as scoped:v.base.original.capture=lambda:None
        self.assertIs(v.base.original.capture,original)
        self.assertTrue(scoped.receipts['capture_hook_restored'])
        # The lock must release even when the prior scope rejected tampering.
        with v.scope():pass

    def test_source_change_rejected_and_stale_runtime_cannot_run(self):
        with patch.object(v,'MENU_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'source identities'):
                with v.scope():pass
        before=v.authenticate();after=copy.deepcopy(before);after[-1]['sha256']='0'*64
        with patch.object(v,'authenticate',side_effect=[before,after]):
            with self.assertRaisesRegex(ValueError,'implementation changed'):
                with v.scope():pass
        self.g.active=False
        with self.assertRaisesRegex(ValueError,'cannot outlive'):self.runtime.members()

    def test_unqualified_host_rejected_before_any_hook_or_source_execution(self):
        original=v.base.original.capture
        with patch.object(v,'require_qualified_guest',side_effect=ValueError('unqualified host')), \
             patch.object(v,'authenticate')as authenticate:
            with self.assertRaisesRegex(ValueError,'unqualified host'):
                with v.scope():self.fail('unqualified scope yielded an executable menu_run')
            authenticate.assert_not_called()
        self.assertIs(v.base.original.capture,original)
        self.assertFalse(v._LOCK.locked())


if __name__=='__main__':unittest.main()
