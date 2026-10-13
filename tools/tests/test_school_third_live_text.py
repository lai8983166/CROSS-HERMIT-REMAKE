import unittest
from copy import deepcopy
from tools.school_third_live_text_verification import *
from tools.school_third_live_text_emulation import SchoolThirdLiveTextEmulator

class ThirdLiveTests(unittest.TestCase):
 def test_three_actual_fifth_textures_full_source_and_cleanup(self):
  self.assertEqual(len(fixture()['cases']),3)
  for c in fixture()['cases']:
   r=compare_live(c);self.assertEqual((r['GDI_calls'],r['COM_calls'],r['handler_return_PC']),(23,4,286));self.assertGreater(r['fifth_texture_bytes'],0)
 def test_corrupt_gdi_com_band_geometry_record_pixel_parent_cleanup_or_scope_refused(self):
  for kind in ('GDI','slot','COM','band','geometry','record','pixel','parent','cleanup','scope','raster','body'):
   c=deepcopy(fixture()['cases'][0]);p=c['third_live_text']
   if kind=='GDI':p['raster']['font_api'][22]['args'][1]+=1
   elif kind=='slot':p['raster']['font_api'][0]['slot']='0x5920a4'
   elif kind=='COM':p['COM_calls'][0]['args'][1]*=2
   elif kind=='band':p['conversion_calls'][0]['rect'][0]+=1
   elif kind=='geometry':p['raster']['measured'][1]=0
   elif kind=='record':
    m=memory_regions(p['after']);struct.pack_into('<H',m[VM],OBJECT-VM+22,2);p['after']=regions(m)
   elif kind=='pixel':p['actual_readback']['sha256']='0'*64
   elif kind=='parent':p['prior_actual_readbacks'][3]['sha256']='0'*64
   elif kind=='cleanup':c['first_live_text']['COM_process_cleanup']['texture_releases'][0]['count']=1
   elif kind=='scope':p['GPU_draw_or_present_executed']=True
   elif kind=='body':p['visited'].remove(0x405A80)
   else:p['raster']['texture_creation_executed']=True
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_live(c)
 def test_guard_preserves_older_textures_and_live_input(self):
  e=SchoolThirdLiveTextEmulator();e.third_live_loading=True;e.third_allowed=[(OBJECT+24,OBJECT+38)];e.lock_bytes=0
  e._write_hook(e.uc,0,OBJECT+24,2,3,None)
  for at in (OBJECT7+0x28,NODE+0x60,TASK+0x1990,MIRROR):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,4,0,None)
 def test_original_empty_record_cleanup_runs_before_texture_creation(self):
  from tools.school_third_live_text_emulation import STACK,RETURN,UC_X86_REG_ECX,UC_X86_REG_EAX
  e=SchoolThirdLiveTextEmulator();e.third_live_loading=True;e.third_allowed=[(STACK,STACK+65536),(TEXTURE+0x28,TEXTURE+0x2C)];e.third_visited=set();e.lock_bytes=0
  e._root();e.uc.reg_write(UC_X86_REG_ECX,TEXTURE);e.uc.emu_start(0x403730,RETURN,timeout=1000000,count=10000)
  self.assertEqual(e.uc.reg_read(UC_X86_REG_EAX),0);self.assertIn(0x403730,e.third_visited)
  self.assertEqual(bytes(e.uc.mem_read(TEXTURE+0x28,12)),bytes(12))

if __name__=='__main__':unittest.main()
