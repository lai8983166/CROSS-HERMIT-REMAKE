"""Captured natural CPU returns and bounded adapter write ownership."""
import hashlib,json,struct,unittest
from tools.school_second_live_text_emulation import *
from tools.school_text_preparation_catalog import OBJECT_OFFSET

EVIDENCE=ROOT/'analysis/school-second-live-text-v2-20261013.json'
EVIDENCE_SHA256='bbd276d0bbdb8b18809a4395ab57127b41a663c42c48ad4dcd3f76f18f17eaed'

class SecondNativeTests(unittest.TestCase):
 def test_actual_three_parents_two_completed_records_real_independent_resources(self):
  raw=EVIDENCE.read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[index]);self.assertEqual(c['provenance']['helper_sha256'],data['bridge_build']['helper_sha256'])
   self.assertTrue(c['provenance']['complete_parent_stages_equal']);self.assertEqual(c['provenance']['complete_parent_stages'],8)
   first,p=c['first_live_text'],c['second_live_text'];self.assertEqual(p['preparation']['before'],first['after']);self.assertEqual(p['raster']['before'],p['preparation']['after'])
   self.assertEqual(p['natural_return'],{'va':RETURN,'sp':STACK+0xFF04,'eax':1});self.assertNotEqual(first['texture']['pointer'],p['texture']['pointer'])
   self.assertEqual(p['first_actual_readback'],first['actual_readback']);self.assertEqual(p['actual_readback']['hex'],p['lock']['after_hex'])
   vm=bytes.fromhex(p['after'][3]['hex']);self.assertEqual(struct.unpack_from('<I',vm,28)[0],244);self.assertEqual(struct.unpack_from('<7H',vm,OBJECT_OFFSET+22),(2,3,1,24,2,12,0))
   self.assertEqual(len(p['text_draws']),1);self.assertEqual(p['text_draws'][0]['args'][4],10)
   self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],120000000);self.assertTrue(first['process_exited'])
   self.assertEqual(first['remaining_GDI_cleanup'],{'fonts':0,'bitmaps':0,'dcs':2,'all_resources_released':True})
   self.assertEqual(len(first['COM_process_cleanup']['texture_releases']),2);self.assertTrue(first['COM_process_cleanup']['all_owned_resources_released'])
   for k in ('original_text_draw_body_executed','GPU_draw_or_present_executed','original_renderer_startup_executed','dialogue_playback_completed','waves_executed','world_update_loop_executed'):self.assertFalse(p[k])

 def test_second_guard_protects_first_texture_and_actual_locked_buffer_extent(self):
  e=SchoolSecondLiveTextEmulator();e.second_loading=True;e.live_allowed=[(SECOND_MIRROR,SECOND_MIRROR+MIRROR_BYTES),(ROW+24,ROW+26)];e.lock_bytes=16
  for a,n in ((0,4),(VM,4),(TEXTURE+0x2C,4),(SECOND_MIRROR+15,2),(SECOND_MIRROR+16,1),(ROW+24,3)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,a,n,0,None)
  e._write_hook(e.uc,0,ROW+24,2,0,None);e._write_hook(e.uc,0,SECOND_MIRROR+14,2,0,None)

if __name__=='__main__':unittest.main()
