"""Actual one-entry DX geometry, full rows and malformed image refusal."""
import unittest
from tools.school_character_image_catalog import *

class ImageRuleTests(unittest.TestCase):
 def test_actual_resource_header_pixels_and_padding(self):
  raw,c=resource();self.assertEqual(c['pixel_bytes'],262144);self.assertEqual(source_rules()['container'],c)
  out=expected_pixels(b'\xaa'*(520*512),520)
  for row in range(512):
   self.assertEqual(out[row*520:row*520+512],raw[24+row*512:24+(row+1)*512]);self.assertEqual(out[row*520+512:(row+1)*520],b'\xaa'*8)
 def test_bad_container_mode_geometry_pitch_and_extent_refused(self):
  raw,_=resource()
  for offset in (0,4,8,12,14,16,18,20,22):
   data=bytearray(raw);data[offset]^=1
   with self.assertRaises(ValueError):parse_resource(bytes(data))
  with self.assertRaises(ValueError):parse_resource(raw[:-1])
  for pitch,initial in ((511,b''),(513,b''),(512,b'')):
   with self.assertRaises(ValueError):expected_pixels(initial,pitch)

if __name__=='__main__':unittest.main()
