"""Desktop refusal and private launch/focus guards; no live GUI operations."""
import unittest
from unittest.mock import Mock,patch
from tools import school_native_dialogue_desktop as desktop
from tools.school_native_dialogue_input import owned_target_guard,focus_target
from tools.school_native_dialogue_launch import root_pid,descendants,ToolLaunchedRuntime
from tools.school_native_dialogue import VisibleOwnedRuntime


class DesktopTests(unittest.TestCase):
 def test_normal_desktop(self):self.assertEqual(desktop.classify('Default','default',r'C:\apps\game.exe'),'ready')
 def test_lock_and_credentials_refused_even_on_default(self):
  for name in ('LockApp.exe','LOGONUI.EXE','CredentialUIBroker.exe'):
   self.assertEqual(desktop.classify('Default','Default','C:\\Windows\\'+name),'locked_foreground')
 def test_inaccessible_desktop(self):
  for names in ((None,'Default'),('Default',None)):
   self.assertEqual(desktop.classify(*names,None),'input_desktop_unavailable')
 def test_other_input_desktop(self):self.assertEqual(desktop.classify('Winlogon','Default',None),'different_input_desktop')
 def test_refusal_is_before_process_launch_or_owned_input_access(self):
  with patch.object(desktop,'desktop_status',return_value={'ready':False,'reason':'locked_foreground'}):
   for runtime in (VisibleOwnedRuntime,ToolLaunchedRuntime):
    with self.assertRaisesRegex(RuntimeError,'locked_foreground'):runtime.start(Mock())
   with self.assertRaisesRegex(RuntimeError,'locked_foreground'):owned_target_guard(None,1)
 def test_ready_status_returned_unchanged(self):
  ready={'ready':True,'reason':'ready'}
  with patch.object(desktop,'desktop_status',return_value=ready):self.assertIs(desktop.require_unlocked(),ready)


class FocusTests(unittest.TestCase):
 def test_already_foreground_needs_no_mutation(self):
  api=Mock();api.foreground.return_value=10;r=focus_target(api,lambda:None,10);self.assertEqual(r['operations'],[]);api.foreground_window.assert_not_called()
 def test_only_owned_window_activated(self):
  api=Mock();api.foreground.side_effect=[11,10];api.foreground_window.return_value=True;r=focus_target(api,lambda:None,10);api.foreground_window.assert_called_once_with(10);self.assertEqual(r['after'],10)
 def test_guard_refuses_before_activation(self):
  api=Mock()
  with self.assertRaisesRegex(ValueError,'foreign'):focus_target(api,lambda:(_ for _ in ()).throw(ValueError('foreign')),10)
  api.foreground.assert_not_called();api.foreground_window.assert_not_called()
 def test_return_true_does_not_prove_actual_foreground(self):
  api=Mock();api.foreground.return_value=11;api.foreground_window.return_value=True
  with self.assertRaisesRegex(ValueError,'actual foreground'):focus_target(api,lambda:None,10)


class PrivateLaunchTests(unittest.TestCase):
 def test_one_tree_only(self):
  self.assertEqual(root_pid([{'pid':2,'parent_pid':1},{'pid':3,'parent_pid':2}]),2)
  for rows in ([],[{'pid':2,'parent_pid':1},{'pid':3,'parent_pid':1}]):
   with self.assertRaises(ValueError):root_pid(rows)
 def test_descendants_exclude_unrelated_private_process(self):
  rows=[{'pid':5,'parent_pid':3},{'pid':3,'parent_pid':2},{'pid':9,'parent_pid':1},{'pid':2,'parent_pid':1}]
  self.assertEqual({x['pid'] for x in descendants(rows,2,[])},{2,3,5})
 def test_known_descendant_survives_parent_exit(self):
  rows=[{'pid':5,'parent_pid':3},{'pid':9,'parent_pid':1}]
  self.assertEqual(descendants(rows,2,[3]),[rows[0]])


if __name__=='__main__':unittest.main()
