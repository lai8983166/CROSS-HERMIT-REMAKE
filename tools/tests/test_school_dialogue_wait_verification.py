import unittest
from copy import deepcopy
from tools.school_dialogue_wait_verification import *

class WaitSourceTests(unittest.TestCase):
 def test_all_actual_update_regions_inputs_stack_readiness_and_pixels(self):
  for c in native_fixture()['cases']:
   r=compare_case(c);self.assertEqual(r['updates'],52);self.assertEqual(r['predicate_calls'],360);self.assertEqual(r['arrow_draws'],14);self.assertEqual(r['actual_texture_bytes'],[16384,32768])
 def test_intermediate_memory_readiness_arrow_and_input_stack_tampering_refused(self):
  original=native_fixture()['cases'][0]
  for kind in ('memory','predicate','arrow','input','return','event','presentation','pixel'):
   c=deepcopy(original);w=c['waits']
   if kind=='memory':r=w['steps'][11]['after'][3];r['hex']=f"{int(r['hex'][:2],16)^1:02x}"+r['hex'][2:]
   elif kind=='predicate':w['steps'][36]['predicates'][7]['return_value']=0
   elif kind=='arrow':w['steps'][44]['arrow_draws'][0]['args'][6]+=18
   elif kind=='input':w['steps'][1]['input_calls'][0]['args'][0]+=4
   elif kind=='return':w['steps'][1]['natural_return']['eax']=0
   elif kind=='event':w['steps'][44]['events']['mouse_buttons']=1
   elif kind=='presentation':w['steps'][44]['presentation_sha256']='0'*64
   else:w['actual_readbacks'][1]['hex']='ff'+w['actual_readbacks'][1]['hex'][2:]
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_case(c)

if __name__=='__main__':unittest.main()
