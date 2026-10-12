import hashlib,json,struct,unittest
from tools.school_dialogue_wait_emulation import *
from tools.school_dialogue_wait_catalog import OBJECT_OFFSET

EVIDENCE=ROOT/'analysis/school-dialogue-wait-v1-20261013.json'
EVIDENCE_SHA256='7188b484705e4aa999ebfb04db2c2ad4425872479705eddffa89ada0f9035d27'

class WaitNativeTests(unittest.TestCase):
 def test_actual_three_parent_replays_natural_wait_and_retained_texture_resources(self):
  raw=EVIDENCE.read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);d=json.loads(raw)
  for i,c in enumerate(d['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[i]);self.assertEqual(c['provenance']['helper_sha256'],d['bridge_build']['helper_sha256']);self.assertTrue(c['provenance']['complete_parent_stages_equal'])
   w=c['waits'];self.assertEqual(len(w['steps']),52);self.assertEqual(w['text_wait_release_update'],36);self.assertEqual(w['held_confirmation_updates'],14)
   self.assertTrue(w['natural_text_readiness_executed']);self.assertTrue(w['original_input_query_bodies_executed']);self.assertTrue(w['retained_ranges_unchanged']);self.assertGreater(w['retained_bytes'],120000000)
   self.assertEqual(w['steps'][36]['state']['wait'],0);self.assertEqual(w['steps'][-1]['state']['wait'],1);self.assertEqual(w['steps'][-1]['state']['PC'],252)
   self.assertEqual(w['actual_readbacks'],[c['first_live_text']['actual_readback'],c['second_live_text']['actual_readback']]);self.assertTrue(c['first_live_text']['process_exited']);self.assertTrue(c['first_live_text']['COM_process_cleanup']['all_owned_resources_released'])
 def test_wait_guard_refuses_texture_input_and_unowned_counter_writes(self):
  e=SchoolDialogueWaitEmulator();e.wait_loading=True;e.wait_allowed=[(STACK,STACK+65536),(OBJECT+26,OBJECT+28)]
  for at,n in ((0,4),(TASK+0x1990,4),(TEXTURE+0x2C,4),(SECOND_TEXTURE+0x2C,4),(VM+28,4),(OBJECT+26,3)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,n,0,None)
  e._write_hook(e.uc,0,OBJECT+26,2,0,None)

if __name__=='__main__':unittest.main()
