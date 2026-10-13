"""Exact scene-image size extension and immutable old-helper separation."""
import unittest
from tools.school_d3d8_image_bridge import *

class ImageBridgeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.helper,cls.identity=build(ROOT/'.venv-audit/school-d3d8-image-bridge-test.exe')
 def test_full_real_image_rows_and_retained_text_buffer(self):
  d=ImageD3D8(self.helper)
  try:
   a=d.create(128,32)['texture']['pointer'];b=d.create(256,512)['texture']['pointer']
   for ptr,value in ((a,0x81),(b,0xAC)):
    locked=d.lock(ptr);raw=bytes([value])*len(bytes.fromhex(locked['hex']));d.unlock(ptr,raw)
    self.assertEqual(d.readback(ptr)['hex'],raw.hex())
   self.assertEqual(d.describe(b)['size'],262144);self.assertNotEqual(a,b)
  finally:d.close()
  self.assertEqual([r['pointer'] for r in d.cleanup['texture_releases']],[b,a]);self.assertTrue(d.cleanup['all_owned_resources_released']);self.assertEqual(d.process.poll(),0)
 def test_extension_rejects_other_tall_shapes_and_bad_parameters(self):
  with ImageD3D8(self.helper) as d:
   for args in ((128,512),(512,512),(256,1024),(256,511),(256,512,2),(256,512,1,1)):
    with self.assertRaises(ValueError):d.create(*args)

if __name__=='__main__':unittest.main()
