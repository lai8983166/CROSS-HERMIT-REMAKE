"""Actual x86 owned static-lock13 lifecycle and rejection of foreign ownership."""
import os,unittest
from functools import lru_cache
from tools import school_retained_world_loop_platform as p

@lru_cache(maxsize=1)
def helper():return p.build(p.ROOT/('.venv-audit/world-static-lock-test-'+str(os.getpid())+'.exe'))[0]

class WorldStaticLockTests(unittest.TestCase):
 def setUp(self):self.live=p.Live(helper())
 def tearDown(self):
  if self.live.process.poll() is None:self.live._terminate()
 def test_actual_initialized_lock13_nested_and_normal_source_teardown(self):
  self.assertEqual(self.live.hello['critical'],0);r=self.live.request('initialize',guest=0x80a4c8);self.assertEqual(len(bytes.fromhex(r['hex'])),24)
  for op,depth in [('enter_static',1),('enter_static',2),('leave_static',1),('leave_static',0)]:
   result=self.live.request(op,guest=0x80a4c8,pointer=r['pointer']);self.assertEqual(result['depth'],depth);self.assertEqual(len(bytes.fromhex(result['critical_hex'])),24)
  self.live.request('delete',guest=0x80a4c8,pointer=r['pointer']);self.live.close();self.assertEqual(self.live.process.returncode,0);self.assertFalse(self.live.cleanup['forced_cleanup']);self.assertTrue(self.live.cleanup['all_owned_resources_released'])
 def test_uninitialized_lock_rejected(self):
  with self.assertRaises(ValueError):self.live.request('enter_static',guest=0x80a4c8,pointer=1)
 def test_foreign_pointer_rejected(self):
  r=self.live.request('initialize',guest=0x80a4c8)
  with self.assertRaises(ValueError):self.live.request('enter_static',guest=0x80a4c8,pointer=r['pointer']+4)
 def test_lock9_cannot_be_used_as_lock13(self):
  r=self.live.request('initialize',guest=0x80a4b0)
  with self.assertRaises(ValueError):self.live.request('enter_static',guest=0x80a4b0,pointer=r['pointer'])
 def test_unbalanced_leave_rejected(self):
  r=self.live.request('initialize',guest=0x80a4c8)
  with self.assertRaises(ValueError):self.live.request('leave_static',guest=0x80a4c8,pointer=r['pointer'])
 def test_held_lock_cannot_be_deleted(self):
  r=self.live.request('initialize',guest=0x80a4c8);self.live.request('enter_static',guest=0x80a4c8,pointer=r['pointer'])
  with self.assertRaises(ValueError):self.live.request('delete',guest=0x80a4c8,pointer=r['pointer'])
 def test_held_lock_cannot_close(self):
  r=self.live.request('initialize',guest=0x80a4c8);self.live.request('enter_static',guest=0x80a4c8,pointer=r['pointer'])
  with self.assertRaises(ValueError):self.live.request('close')
