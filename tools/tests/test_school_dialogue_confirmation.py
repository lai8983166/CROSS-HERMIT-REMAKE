"""Natural confirmation input/boundary evidence and strict counterfactual refusal."""
import unittest
from copy import deepcopy
from tools.school_dialogue_confirmation_catalog import *
from tools.school_dialogue_confirmation_emulation import SchoolDialogueConfirmationEmulator
from tools.school_second_live_text_catalog import native_fixture as second_fixture

class ConfirmationTests(unittest.TestCase):
 def test_three_actual_held_gates_confirm_then_stop_before_next_handler(self):
  d=native_fixture();self.assertEqual(len(d['cases']),3)
  for c in d['cases']:
   r=compare_confirmation(c);self.assertTrue(r['confirmation_wait_cleared']);self.assertEqual(r['PC'],252);self.assertEqual(r['pending_opcode'],30);self.assertEqual(r['pending_handler'],'0x4c61c0');self.assertFalse(r['next_handler_executed'])
   self.assertEqual(c['provenance']['helper_sha256'],d['bridge_build']['helper_sha256']);self.assertTrue(c['first_live_text']['process_exited'])
 def test_declared_input_natural_stack_and_complete_boundary_tampering_refused(self):
  original=native_fixture()['cases'][0]
  for kind in ('binding','event','query','stack','memory','pixel','handler_scope'):
   c=deepcopy(original);p=c['confirmation']
   if kind=='binding':p['binding']['before']=1
   elif kind=='event':p['confirmation_step']['events']['mouse_buttons']=0
   elif kind=='query':p['confirmation_step']['input_calls'][1]['output_hex'][1]='00000000'
   elif kind=='stack':p['pending_call']['args'][1]+=20
   elif kind=='memory':r=p['after'][3];r['hex']=f"{int(r['hex'][:2],16)^1:02x}"+r['hex'][2:]
   elif kind=='pixel':p['actual_readbacks'][1]['sha256']='0'*64
   else:p['next_handler_executed']=True
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_confirmation(c)
 def test_invalid_event_and_missing_actual_held_parent_refused(self):
  e=SchoolDialogueConfirmationEmulator()
  for value in (True,0,2,-1):
   with self.assertRaises(ValueError):e.run_confirmation({},value)
  with self.assertRaises(RuntimeError):e.run_confirmation({})
  for offset,value in ((28,272),(32,1),(34,50)):
   mem=memory_regions(expected_sequence(second_fixture()['cases'][0]['second_live_text']['after'])['after']);vm=mem[VM]
   struct.pack_into('<H',vm,32,0);struct.pack_into('<I' if offset==28 else '<H',vm,offset,value)
   with self.assertRaises(ValueError):expected_boundary(regions(mem))
 def test_next_prefix_guard_protects_texture_mouse_and_record_counters(self):
  e=SchoolDialogueConfirmationEmulator();e.next_boundary_loading=True;e.boundary_allowed=[(STACK,STACK+65536),(VM+28,VM+38)]
  for at,n in ((0,4),(TASK+0x1990,4),(VM+OBJECT_OFFSET+26,2),(VM+38,4),(STACK+65535,2)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,n,0,None)
  e._write_hook(e.uc,0,VM+34,2,0,None)

if __name__=='__main__':unittest.main()
