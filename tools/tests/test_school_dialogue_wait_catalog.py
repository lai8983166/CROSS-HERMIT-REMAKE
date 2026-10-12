"""Independent original wait ordering and bounded sequence prediction."""
import struct,unittest
from copy import deepcopy
from tools.school_dialogue_wait_catalog import *
from tools.school_second_live_text_catalog import native_fixture as second_fixture

class WaitContractTests(unittest.TestCase):
 def test_original_dispatch_tables_identify_text_then_input_wait(self):
  r=source_catalog();self.assertEqual([(c['opcode'],c['handler']) for c in r['commands']],[(50,'0x4c5260'),(51,'0x4c4210'),(30,'0x4c61c0')]);self.assertEqual(r['commands'][0]['wait_dispatch_entry'],'0x4d0153');self.assertEqual(r['commands'][1]['wait_dispatch_entry'],'0x4d0181')
 def test_all_three_parents_predict_original_ready_and_held_gate(self):
  for c in second_fixture()['cases']:
   seq=expected_sequence(c['second_live_text']['after']);self.assertEqual(seq['text_wait_release_update'],36);self.assertEqual(seq['confirmation_started_update'],37);self.assertEqual(len(seq['steps']),52)
   self.assertEqual(seq['steps'][10]['state']['records'][1],{'mode':3,'fade':0,'interval':1,'following_ready':0})
   self.assertEqual(seq['steps'][35]['state']['wait'],1);self.assertEqual(seq['steps'][36]['state']['wait'],0)
   self.assertEqual(seq['steps'][-1]['state']['arrow_phase'],2);self.assertEqual(seq['steps'][-1]['state']['wait'],1)
 def test_mouse_confirmation_clears_wait_without_advancing_same_call_PC(self):
  s=expected_sequence(second_fixture()['cases'][0]['second_live_text']['after']);p=advance(s['after'],{'mouse_buttons':1,'space_key':0});self.assertEqual(p['state']['PC'],252);self.assertEqual(p['state']['wait'],0);self.assertEqual(p['input_call_order'],['keyboard','mouse_buttons'])
 def test_invalid_events_wait_state_extra_objects_and_unbounded_hold_refused(self):
  before=second_fixture()['cases'][0]['second_live_text']['after']
  for events in ({'mouse_buttons':True,'space_key':0},{'mouse_buttons':2,'space_key':0},{'mouse_buttons':0,'space_key':1},{}):
   with self.assertRaises(ValueError):advance(before,events)
  for offset,value in ((28,300),(32,1),(OBJECT_OFFSET+22,3),(0x430+22,1)):
   mem=memory_regions(before);struct.pack_into('<I' if offset==28 else '<H',mem[VM],offset,value)
   with self.assertRaises(ValueError):advance(regions(mem),{'mouse_buttons':0,'space_key':0})
  for hold in (0,33,True):
   with self.assertRaises(ValueError):expected_sequence(before,hold)

if __name__=='__main__':unittest.main()
