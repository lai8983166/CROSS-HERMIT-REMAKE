"""Inert tests: ownership, native packet ABI, timing, and guaranteed key release."""
import ctypes as C
import unittest
from tools.school_native_dialogue_input import INPUT,space_packet,held_space


class Api:
 def __init__(self,results=None):self.packets=[];self.results=list(results or [])
 def submit(self,p):
  self.packets.append((p.type,p.data.ki.wVk,p.data.ki.wScan,p.data.ki.dwFlags))
  return self.results.pop(0) if self.results else 1


class HeldInputTests(unittest.TestCase):
 def test_real_host_INPUT_layout(self):
  self.assertEqual(C.sizeof(INPUT),40 if C.sizeof(C.c_void_p)==8 else 28)
  p=space_packet();self.assertEqual((p.type,p.data.ki.wVk,p.data.ki.wScan,p.data.ki.dwFlags),(1,0,57,8))
 def test_down_hold_up(self):
  api=Api();sleep=[];guards=[];r=held_space(api,lambda:guards.append(True),sleep=sleep.append)
  self.assertEqual(sleep,[.12]);self.assertEqual(api.packets,[(1,0,57,8),(1,0,57,10)]);self.assertTrue(r['input_returned']);self.assertTrue(r['released']);self.assertEqual(len(guards),3)
 def test_foreign_owner_rejected_without_input(self):
  api=Api()
  with self.assertRaises(ValueError):held_space(api,lambda:(_ for _ in ()).throw(ValueError('foreign')))
  self.assertEqual(api.packets,[])
 def test_second_guard_blocks_down(self):
  api=Api();n=[]
  def guard():
   n.append(1)
   if len(n)==2:raise ValueError('ownership changed')
  r=held_space(api,guard);self.assertFalse(r['input_returned']);self.assertEqual(api.packets,[])
 def test_failed_down_does_not_submit_keyup(self):
  api=Api([0]);r=held_space(api,lambda:None);self.assertFalse(r['input_returned']);self.assertEqual(len(api.packets),1)
 def test_sleep_exception_releases_key(self):
  api=Api();r=held_space(api,lambda:None,sleep=lambda _:(_ for _ in ()).throw(RuntimeError('interrupt')));self.assertFalse(r['input_returned']);self.assertTrue(r['released']);self.assertEqual(api.packets[-1][-1],10)
 def test_failed_up_retries_release(self):
  api=Api([1,0,1]);r=held_space(api,lambda:None,sleep=lambda _:None);self.assertFalse(r['input_returned']);self.assertEqual(r['up_results'],[0,1]);self.assertTrue(r['released'])
 def test_focus_loss_after_up_is_not_success(self):
  api=Api();n=[]
  def guard():
   n.append(1)
   if len(n)==3:raise ValueError('focus changed')
  r=held_space(api,guard,sleep=lambda _:None);self.assertFalse(r['input_returned']);self.assertTrue(r['released'])
 def test_hold_bounds(self):
  for value in (0,79,251,True,120.0):
   with self.assertRaises(ValueError):held_space(Api(),lambda:None,value)


if __name__=='__main__':unittest.main()
