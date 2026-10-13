import unittest
from tools.school_third_live_text_catalog import *
from tools.school_character_animation_verification import fixture

class ThirdRulesTests(unittest.TestCase):
 def completion(self):
  c=fixture()['cases'][0];p=c['third_text_prefix'];r=raster_state(p['after'],[380,20],c['image_prefix']['renderer']);return p,complete_state(r['after'],0x12345678,0x23456789)
 def test_source_record_and_first_natural_update(self):
  self.assertEqual(source_rules()['texture_record'],OBJECT+0x28);p,c=self.completion();v=memory_regions(c['after'])[VM]
  self.assertEqual(struct.unpack_from('<4H',v,OBJECT-VM+22),(1,3,0,24));self.assertEqual(len(c['text_draws']),2)
 def test_fade_does_not_release_until_next_readiness_observation(self):
  p,c=self.completion();steps=[];before=c['after']
  for i in range(26):s=advance_wait(before,i,p);steps.append(s);before=s['after']
  v=memory_regions(steps[24]['after'])[VM];self.assertEqual(struct.unpack_from('<2H',v,OBJECT-VM+24),(1,24));self.assertEqual(struct.unpack_from('<H',v,32)[0],1)
  self.assertEqual(struct.unpack_from('<H',memory_regions(before)[VM],32)[0],0);self.assertEqual(sum(len(s['predicates']) for s in steps),250)
 def test_invalid_font_parent_geometry_or_released_wait_refused(self):
  p,c=self.completion()
  with self.assertRaises(ValueError):raster_state(c['after'],[380,20],1)
  with self.assertRaises(ValueError):raster_state(p['after'],[380,0],1)
  with self.assertRaises(ValueError):advance_wait(c['after'],1,p)

if __name__=='__main__':unittest.main()
