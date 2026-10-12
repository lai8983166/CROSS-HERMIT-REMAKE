import struct,unittest
from tools.school_d3d8_bridge import *

class LiveBridgeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.helper,cls.build=build(ROOT/'.venv-audit/school-d3d8-bridge-test.exe')
 def test_live_methods_complete_rows_and_close(self):
  d=LiveD3D8(self.helper)
  try:
   r=d.create(4,2);ptr=r['texture']['pointer'];self.assertGreater(ptr,0);self.assertGreater(r['texture']['methods']['64'],0)
   desc=d.describe(ptr);self.assertEqual(struct.unpack('<8I',bytes.fromhex(desc['hex'])),(25,1,0,1,16,0,4,2))
   lock=d.lock(ptr);raw=struct.pack('<8H',0,0x8000,0xFFFF,0xFC00,0x83E0,0x801F,0x8421,1)
   self.assertEqual(lock['pitch'],8);self.assertEqual(d.unlock(ptr,raw)['uploaded_sha256'],sha(raw));self.assertEqual(bytes.fromhex(d.readback(ptr)['hex']),raw)
  finally:d.close()
  self.assertTrue(d.closed);self.assertEqual(d.process.poll(),0);self.assertTrue(d.cleanup['all_owned_resources_released']);self.assertEqual(d.cleanup['texture_release_count'],0)
  with self.assertRaises(ValueError):d.describe(ptr)

 def test_foreign_stale_malformed_and_wrong_lock_state_refused(self):
  with LiveD3D8(self.helper) as d:
   for args in ((3,2),(4,2,2),(4,2,1,1)):
    with self.assertRaises(ValueError):d.create(*args)
   ptr=d.create(4,2)['texture']['pointer']
   for fn in (lambda:d.describe(0),lambda:d.lock(ptr,0),lambda:d.readback(1),lambda:d.unlock(ptr,bytes(16)),lambda:d.request('unsupported')):
    with self.assertRaises(ValueError):fn()
   locked=d.lock(ptr)
   for fn in (lambda:d.lock(ptr),lambda:d.release(ptr),lambda:d.unlock(ptr,b''),lambda:d.readback(ptr)):
    with self.assertRaises(ValueError):fn()
   d.unlock(ptr,bytes.fromhex(locked['hex']));self.assertEqual(d.release(ptr)['count'],0)
   with self.assertRaises(ValueError):d.describe(ptr)
  self.assertTrue(d.cleanup['all_owned_resources_released'])

 def test_cleanup_while_locked_and_exception(self):
  d=LiveD3D8(self.helper)
  try:
   ptr=d.create(4,2)['texture']['pointer'];d.lock(ptr);raise ValueError('driver failure')
  except ValueError:pass
  finally:d.close()
  self.assertEqual(d.cleanup['unlock_hr'],0);self.assertEqual(d.cleanup['device_release_count'],0);self.assertEqual(d.cleanup['factory_release_count'],0)

if __name__=='__main__':unittest.main()
