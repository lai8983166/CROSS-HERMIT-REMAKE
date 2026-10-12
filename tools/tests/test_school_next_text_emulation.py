"""Actual next-text capture, preserved live resource and strict native guards."""
import hashlib,json,struct,unittest
from types import SimpleNamespace
from tools.school_next_text_emulation import *

EVIDENCE=ROOT/'analysis/school-next-text-v4-20261012.json'
EVIDENCE_SHA256='47e76776fc4eaddf701e99242bccd0968029093ce2faf6056cf3492f0614f69a'

class NextNativeTests(unittest.TestCase):
 def test_actual_three_cases_live_pixels_natural_stack_and_cleanup(self):
  raw=EVIDENCE.read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,case in enumerate(data['cases']):
   self.assertEqual((case['name'],case['provenance']['checkpoint_sha256']),CHECKPOINTS[index])
   self.assertEqual(case['provenance']['helper_sha256'],data['bridge_build']['helper_sha256'])
   self.assertEqual(case['provenance']['complete_parent_stages'],8)
   self.assertTrue(case['provenance']['complete_parent_stages_equal'])
   first,p=case['first_live_text'],case['next_text']
   self.assertEqual(p['before'],first['after']);self.assertEqual(p['first_actual_readback'],first['actual_readback'])
   self.assertTrue(p['first_owner_alive_at_boundary']);self.assertTrue(p['first_resource_retained'])
   predicate=p['first_readiness'];self.assertEqual((predicate['va'],predicate['receiver'],predicate['return_value']),('0x4cb5f0',OBJECT,0))
   self.assertEqual(predicate['CPU_register_count'],len(CPU_REGISTERS));self.assertTrue(predicate['CPU_and_stack_restored'])
   self.assertFalse(predicate['original_VM_called_predicate'])
   font=p['pending_font'];self.assertTrue(font['natural_stack_verified']);self.assertFalse(font['first_instruction_executed'])
   self.assertEqual(font['return_va'],'0x4cad09');self.assertEqual(len(font['args']),14)
   self.assertTrue(first['process_exited']);self.assertTrue(first['COM_process_cleanup']['all_owned_resources_released'])
   self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],120000000)
   for k in ('second_font_executed','second_texture_created','second_handler_completed','first_fade_completed','GPU_draw_or_present_executed','world_update_loop_executed','waves_executed'):self.assertFalse(p[k])

 def test_predicate_stack_extent_and_next_record_write_guard(self):
  e=SchoolNextTextEmulator();e.predicate_loading=True
  for at,size in ((0,4),(VM,1),(STACK-1,2),(STACK+65535,2),(STACK+65536,1)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,size,0,None)
  e._write_hook(e.uc,0,STACK+65535,1,0,None)
  e.predicate_loading=False;e.next_loading=True;e.next_allowed=[(ROW+o,ROW+o+2) for o in FIELDS]
  for at,size in ((OBJECT+24,2),(ROW+38,1),(ROW+36,3),(VM,4),(0,4)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,size,0,None)
  e._write_hook(e.uc,0,ROW+24,2,0,None)

 def test_wrong_continuation_and_dead_ownership_refused_before_execution(self):
  e=SchoolNextTextEmulator()
  with self.assertRaises(ValueError):e.run_live_text({},'unused',continuation=1)
  with self.assertRaises(RuntimeError):e.run_next_text({})
  e.live_loading=True;e.bridge=SimpleNamespace(closed=True)
  with self.assertRaises(RuntimeError):e.run_next_text({})
  with self.assertRaises(RuntimeError):e.observe_first_readiness()

if __name__=='__main__':unittest.main()
