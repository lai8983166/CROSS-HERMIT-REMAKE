import unittest
from copy import deepcopy
from tools.school_character_animation_verification import *

class ThirdPrefixTests(unittest.TestCase):
 def test_three_actual_text2_layer5_natural_font_entries(self):
  for c in fixture()['cases']:
   r=compare_third(c);self.assertEqual((r['pending_PC'],r['third_layer']),(280,5));self.assertFalse(r['third_font_executed'])
 def test_bad_target_stack_text_split_calls_resource_or_authority_refused(self):
  for kind in ('target','stack','line','call','pixel','scope','parent'):
   c=deepcopy(fixture()['cases'][0]);p=c['third_text_prefix']
   if kind=='target':
    m=memory_regions(p['after']);m[VM][0x1CC]=7;p['after']=regions(m)
   elif kind=='stack':p['pending_font']['frames']['text']+=4
   elif kind=='line':p['split']['lines'][0]['hex']='00'+p['split']['lines'][0]['hex'][2:]
   elif kind=='call':p['calls'][2]['args'][1]=1
   elif kind=='pixel':p['actual_readbacks'][2]['sha256']='0'*64
   elif kind=='scope':p['font_API_executed']=True
   else:p['before']=c['image_live']['after']
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_third(c)

if __name__=='__main__':unittest.main()
