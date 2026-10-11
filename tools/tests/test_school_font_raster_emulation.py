import hashlib,json,struct,unittest
from tools.school_font_raster_emulation import *
REPORT=ROOT/'analysis/school-font-raster-v1-20261012.json'
REPORT_SHA='b95eead169b1962e33cf59f6b365d58fa31645f45591d297c42d0cda0c35e6c0'

class RasterNativeTests(unittest.TestCase):
 def test_three_actual_font_frames_real_api_results_and_retention(self):
  raw=REPORT.read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),REPORT_SHA);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for i,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[i]);self.assertEqual(c['provenance']['complete_parent_stages'],8)
   self.assertTrue(c['provenance']['complete_parent_stages_equal']);self.assertFalse(c['provenance']['upstream_rerun'])
   p=c['font_raster'];self.assertEqual(len(p['font_api']),23);self.assertEqual(p['font_api'][0]['args'],read_text_parent()['cases'][i]['text_preparation']['pending_font']['args'])
   self.assertGreater(p['font_api'][0]['result'],0);self.assertTrue(p['selected_face']);self.assertTrue(p['retained_ranges_unchanged'])
   self.assertGreater(p['retained_bytes'],100000000);self.assertEqual(p['before'][:3],p['after'][:3])
   self.assertEqual(p['pending_texture'],{'va':'0x403bd0','receiver':TEXTURE,'args':[0,0],'return_va':'0x405779','first_instruction_executed':False,'natural_stack_verified':True})
   self.assertEqual(p['platform_cleanup'],{'fonts':1,'bitmaps':1,'dcs':2,'all_resources_released':True})
   self.assertEqual(hashlib.sha256(bytes.fromhex(p['raster']['hex'])).hexdigest(),p['raster']['sha256']);self.assertTrue(any(bytes.fromhex(p['raster']['hex'])))
   for k in ('font_api_executed','original_raster_geometry_executed','real_offscreen_GDI_drawing'):self.assertTrue(p[k])
   for k in ('original_gpu_executed','texture_creation_executed','text_record_completed','text_readiness_executed','natural_VM_returned','dialogue_playback_completed','waves_executed','full_task_wrapper_executed','world_update_loop_executed'):self.assertFalse(p[k])
  self.assertEqual(data['inherited_refusals'],read_text_parent()['inherited_refusals'])

 def test_pending_font_cpu_and_exact_owned_ranges_required(self):
  e=SchoolFontRasterEmulator()
  with self.assertRaises(RuntimeError):e.run_font_raster({})
  e.raster_loading=True;e.raster_allowed=[(TEXTURE+0x28,TEXTURE+0x44)]
  for at,n in ((0,1),(TACT,1),(WORK,1),(TEXTURE+0x27,1),(TEXTURE+0x43,2)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,n,0,None)
  e._write_hook(e.uc,0,TEXTURE+0x40,4,0,None)

 def test_wrong_font_import_and_texture_callers_refused(self):
  e=SchoolFontRasterEmulator();e.raster_loading=True;e.device=0
  sp=STACK+0xFF00;e.uc.reg_write(UC_X86_REG_ESP,sp);e.uc.mem_write(sp,struct.pack('<15I',RETURN,*([0]*14)))
  for address in (0xE300000,0x403BD0,0x454CF0,0x46B470):
   with self.assertRaises(RuntimeError):e._hook(e.uc,address,1,None)

if __name__=='__main__':unittest.main()
