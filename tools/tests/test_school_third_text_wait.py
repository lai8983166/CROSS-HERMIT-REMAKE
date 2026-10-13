import unittest
from copy import deepcopy
from tools.school_third_live_text_verification import *

class ThirdWaitTests(unittest.TestCase):
 def test_three_actual_fades_readiness_and_five_resources(self):
  for c in fixture()['cases']:
   r=compare_wait(c);self.assertEqual((r['wait_updates'],r['object_readiness_calls'],r['original_input_queries'],r['released_PC']),(26,250,50,290));self.assertTrue(r['confirmation_pending'])
 def test_corrupt_predicate_input_reset_fade_draw_return_pixels_or_scope_refused(self):
  for kind in ('predicate','input','reset','fade','draw','return','pixel','scope'):
   c=deepcopy(fixture()['cases'][0]);p=c['third_text_wait']
   if kind=='predicate':p['steps'][24]['predicates'][5]['return_value']=1
   elif kind=='input':p['steps'][1]['input_calls'][0]['return_eax']=1
   elif kind=='reset':p['input_binding']['after_mouse_words'][1]=1
   elif kind=='fade':
    m=memory_regions(p['steps'][24]['after']);struct.pack_into('<H',m[VM],OBJECT-VM+24,3);p['steps'][24]['after']=regions(m)
   elif kind=='draw':p['steps'][1]['text_draws'][0]['args'][4]+=1
   elif kind=='return':p['steps'][25]['natural_return']['sp']+=4
   elif kind=='pixel':p['actual_readbacks'][4]['sha256']='0'*64
   else:p['confirmation_started']=True
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_wait(c)
 def test_font_stack_does_not_shift_for_other_actual_formation(self):
  self.assertEqual(len({c['third_text_prefix']['pending_font']['frames']['font'] for c in fixture()['cases']}),1)

if __name__=='__main__':unittest.main()
