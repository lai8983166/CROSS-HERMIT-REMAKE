import unittest
from tools.school_character_animation_catalog import *
from tools.tests.test_school_character_image_live import fixture

class AnimationRulesTests(unittest.TestCase):
 def steps(self):
  c=fixture()['cases'][0];v=c['image_live']['after'];steps=[]
  for i in range(78):
   s=advance(v,i,c['image_prefix']['renderer']);steps.append(s);v=s['after']
  return steps
 def test_source_dispatch_and_distinct_counter_edges(self):
  self.assertEqual(source_rules()['updates'],78);s=self.steps()
  self.assertEqual((s[29]['after_state']['mode'],s[30]['after_state']['mode']),(6,3))
  self.assertEqual((s[60]['after_state']['background_mode'],s[61]['after_state']['background_mode']),(3,2))
  self.assertEqual((s[75]['after_state']['mode'],s[76]['after_state']['mode']),(3,2))
  self.assertEqual([x['after_state']['wait'] for x in s],[1]*77+[0])
  self.assertEqual([len(x['presentation']) for x in s],[53]*31+[60]*46+[61])
 def test_third_text_changes_layer_without_mutating_previous_text(self):
  before=self.steps()[-1]['after'];v=memory_regions(before)[VM];ptr=struct.unpack_from('<I',v,16)[0]-452;p=third_prefix(before,ptr);after=memory_regions(p['after'])[VM]
  self.assertEqual(after[OBJECT7-VM:OBJECT7-VM+BYTES],v[OBJECT7-VM:OBJECT7-VM+BYTES])
  self.assertEqual(after[0x1CC],5);self.assertEqual(p['third_text']['index'],2);self.assertFalse(p['pending_font']['first_instruction_executed'])
 def test_bad_parent_driver_or_unreleased_wait_refused(self):
  c=fixture()['cases'][0]
  for i in (-1,78,True):
   with self.assertRaises(ValueError):advance(c['image_live']['after'],i,c['image_prefix']['renderer'])
  with self.assertRaises(ValueError):third_prefix(self.steps()[76]['after'],0xE000000)

if __name__=='__main__':unittest.main()
