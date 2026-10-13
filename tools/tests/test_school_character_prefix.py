"""Character configuration resolution and independent prefix rejection."""
import unittest
from tools.school_character_prefix_catalog import *

class CharacterPrefixTests(unittest.TestCase):
 def test_actual_configuration_name_and_image(self):
  c=source_catalog();self.assertEqual(c['layer'],5);self.assertEqual(c['operands'],[8,4,0,30])
  self.assertEqual(c['image_dependency']['filename'],'sc004.bin');self.assertFalse(c['image_dependency']['executed'])
  self.assertEqual(c['name']['hex'],'b7e6a7c6b2fab5b7')
 def test_three_parent_predictions_preserve_unowned_regions(self):
  for case in confirmation_fixture()['cases']:
   before=case['confirmation']['after'];p=expected_prefix(before);a=memory_regions(p['after']);b=memory_regions(before)
   for pointer in a:
    if pointer!=VM:self.assertEqual(a[pointer],b[pointer])
   self.assertEqual(a[VM][0x430+7*0xAB8:0x430+8*0xAB8],b[VM][0x430+7*0xAB8:0x430+8*0xAB8])
   self.assertEqual(p['pending_font']['args'][0],20);self.assertEqual(p['pending_font']['args'][4],700)
 def test_unsupported_pc_layer_and_text_object_refused(self):
  for offset in (28,32,34,NODE_OFFSET,NODE_OFFSET+2,NODE_OFFSET+0x34,OBJECT_OFFSET+22):
   mem=memory_regions(confirmation_fixture()['cases'][0]['confirmation']['after']);mem[VM][offset]^=1
   with self.subTest(offset=offset):
    with self.assertRaises(ValueError):expected_prefix(regions(mem))

 def test_prefix_write_guard_refuses_texture_and_live_input(self):
  from tools.school_character_prefix_emulation import SchoolCharacterPrefixEmulator
  e=SchoolCharacterPrefixEmulator();e.character_loading=True;e.character_allowed=[(NODE,NODE+2)]
  e._write_hook(e.uc,0,NODE,2,1,None)
  for address in (NODE+2,VM+0x430+7*0xAB8+0x28,0x1001990):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,address,2,1,None)
  e.character_loading=False
  with self.assertRaises(RuntimeError):e.continue_character({})

if __name__=='__main__':unittest.main()
