"""Independent name geometry and bounded original parent refusal."""
import unittest
from tools.school_character_name_catalog import *

class NameRuleTests(unittest.TestCase):
 def test_source_and_name_surface_do_not_alias_dialogue(self):
  c=name_rules();self.assertEqual(c['image_path'],'data\\adv\\bin\\sc004.bin');self.assertEqual(c['image_slot'],32)
  self.assertNotEqual(TEXTURE,VM+0x430+7*0xAB8+0x28)
  prefix=expected_prefix(confirmation_fixture()['cases'][0]['confirmation']['after'])
  p=expected_raster(prefix['after'],[80,20],0x1000000,0x1234)
  m=memory_regions(p['after']);self.assertEqual(struct.unpack_from('<I',m[VM],NODE_OFFSET+0x5C)[0],0x1234)
  self.assertEqual(p['raster_size'],[84,24]);self.assertEqual(pending_texture(prefix)['return_va'],0x405779)
 def test_bad_handles_extent_and_nonempty_surface_refused(self):
  p=expected_prefix(confirmation_fixture()['cases'][0]['confirmation']['after'])
  for size,g,f in (([0,20],1,1),([80,0],1,1),([80,20],0,1),([80,20],1,0)):
   with self.assertRaises(ValueError):expected_raster(p['after'],size,g,f)
  m=memory_regions(p['after']);m[VM][TEXTURE_OFFSET+0x2C]=1
  with self.assertRaises(ValueError):expected_raster(regions(m),[80,20],1,1)

if __name__=='__main__':unittest.main()
