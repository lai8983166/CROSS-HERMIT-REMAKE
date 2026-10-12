import hashlib,json,struct,unittest
from tools.school_live_text_emulation import *

class LiveNativeTests(unittest.TestCase):
 def test_three_actual_parents_text_texture_root_return_and_resources(self):
  raw=(ROOT/'analysis/school-live-text-v1-20261012.json').read_bytes();data=json.loads(raw)
  self.assertEqual(hashlib.sha256(raw).hexdigest(),'de4828ab6f278822b0f2d5ac0508c3db56b24be1ee66f4f7dd390cdf610b7818')
  self.assertEqual(len(data['cases']),3)
  for i,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[i]);self.assertEqual(c['provenance']['complete_parent_stages'],8);self.assertTrue(c['provenance']['complete_parent_stages_equal'])
   p=c['live_text'];self.assertEqual(p['raster']['before'],read_text_parent()['cases'][i]['text_preparation']['after'])
   self.assertEqual(p['raster']['inputs']['device'],p['binding']['bound']);self.assertEqual(p['binding']['before'],0)
   self.assertEqual(p['natural_return'],{'va':RETURN,'sp':STACK+0xFF04,'eax':1});self.assertEqual(len(p['COM_calls']),4);self.assertEqual(len(p['remote_reads']),4)
   self.assertEqual(p['actual_readback']['hex'],p['lock']['after_hex']);self.assertEqual(p['accounting_after']-p['accounting_before'],16384)
   self.assertEqual(p['remaining_GDI_cleanup'],{'fonts':0,'bitmaps':0,'dcs':1,'all_resources_released':True})
   self.assertEqual(p['COM_process_cleanup'],{'texture_release_count':0,'device_release_count':0,'factory_release_count':0,'window_destroyed':True,'all_owned_resources_released':True});self.assertTrue(p['process_exited'])
   self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],120000000)
   for key in ('text_record_completed','text_handler_completed','natural_VM_returned','original_texture_create_upload_executed'):self.assertTrue(p[key])
   for key in ('text_readiness_executed','GPU_draw_or_present_executed','original_renderer_startup_executed','dialogue_playback_completed','waves_executed','world_update_loop_executed'):self.assertFalse(p[key])

 def test_foreign_remote_object_finite_guard_and_locked_extent_refused(self):
  e=SchoolLiveTextEmulator();e.live_loading=True;e.live_allowed=[(MIRROR,MIRROR+MIRROR_BYTES)];e.lock_bytes=16
  for address,n in ((0,4),(VM,4),(MIRROR+16,1),(MIRROR+14,4)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,address,n,0,None)
  e._write_hook(e.uc,0,MIRROR+14,2,0,None)
  with self.assertRaises(RuntimeError):e._remote_load(0x403C81,UC_X86_REG_ECX,0,{'pointer':1,'vtable':2})
  with self.assertRaises(ValueError):e.run_font_raster({},keep_resources=1)

 def test_real_GDI_native_deletions_owned_lifecycle(self):
  with WindowsGDI() as g:
   dc=g.dc();font=g.font([0,0,0,0,400,0,0,0,1,5,0,0,0],bytes.fromhex('826c827220835383568362834e'))
   self.assertEqual(g.delete_object(font),1)
   with self.assertRaises(ValueError):g.delete_object(font)
   self.assertEqual(g.delete_dc(dc),1)
   with self.assertRaises(ValueError):g.delete_dc(dc)
  self.assertTrue(g.closed)

if __name__=='__main__':unittest.main()
