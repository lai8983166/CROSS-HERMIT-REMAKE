import unittest
from tools.school_d3d8_multi_bridge import *

class MultiBridgeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.helper,cls.identity=build(ROOT/'.venv-audit/school-d3d8-multi-bridge-test.exe')

 def test_two_independent_real_buffers_and_reverse_cleanup(self):
  d=MultiD3D8(self.helper)
  try:
   pointers=[];expected=[]
   for w,h,v in ((4,2,0x81),(8,4,0x32)):
    ptr=d.create(w,h)['texture']['pointer'];pointers.append(ptr)
    lock=d.lock(ptr);raw=bytes([v])*len(bytes.fromhex(lock['hex']));expected.append(raw)
    self.assertEqual(d.unlock(ptr,raw)['uploaded_sha256'],sha(raw))
   self.assertNotEqual(*pointers);self.assertEqual(len(d.textures),2)
   for ptr,raw in zip(pointers,expected):self.assertEqual(bytes.fromhex(d.readback(ptr)['hex']),raw)
   self.assertEqual([d.describe(p)['width'] for p in pointers],[4,8])
  finally:d.close()
  self.assertEqual([r['pointer'] for r in d.cleanup['texture_releases']],list(reversed(pointers)))
  self.assertTrue(d.cleanup['all_owned_resources_released']);self.assertTrue(all(r['count']==0 for r in d.cleanup['texture_releases']))

 def test_independent_lock_states_foreign_stale_and_malformed(self):
  with MultiD3D8(self.helper) as d:
   a=d.create(4,2)['texture']['pointer'];b=d.create(8,2)['texture']['pointer']
   la=d.lock(a);lb=d.lock(b)
   for fn in (lambda:d.lock(a),lambda:d.readback(a),lambda:d.release(b),lambda:d.describe(0),lambda:d.unlock(a,b'')):
    with self.assertRaises(ValueError):fn()
   d.unlock(a,bytes.fromhex(la['hex']));d.unlock(b,bytes.fromhex(lb['hex']))
   self.assertEqual(d.release(a)['count'],0)
   with self.assertRaises(ValueError):d.describe(a)
   self.assertEqual(d.describe(b)['width'],8)
   for args in ((3,2),(4,2,2),(4,2,1,1)):
    with self.assertRaises(ValueError):d.create(*args)

 def test_resource_limit_and_cleanup_multiple_locked_objects(self):
  d=MultiD3D8(self.helper)
  try:
   pointers=[d.create(4,2)['texture']['pointer'] for _ in range(10)]
   with self.assertRaises(ValueError):d.create(4,2)
   d.lock(pointers[0]);d.lock(pointers[-1])
  finally:d.close()
  self.assertEqual(len(d.cleanup['texture_releases']),10)
  self.assertTrue(all(r['unlock_hr']==0 and r['count']==0 for r in d.cleanup['texture_releases']))
  self.assertEqual(d.process.poll(),0)

 def test_retired_addresses_never_readmitted(self):
  with MultiD3D8(self.helper) as d:
   keep=d.create(8,4)['texture']['pointer'];retired=set();refused=False
   for _ in range(40):
    try:ptr=d.create(4,2)['texture']['pointer']
    except ValueError as error:
     self.assertTrue('retired' in str(error) or 'capacity' in str(error));refused=True;break
    self.assertNotIn(ptr,retired);retired.add(ptr);d.release(ptr)
   self.assertTrue(refused);self.assertEqual(d.describe(keep)['width'],8)

if __name__=='__main__':unittest.main()
