import os,struct,unittest
from tools.school_gdi_platform import WindowsGDI

@unittest.skipUnless(os.name=='nt','real Windows GDI')
class GDIPlatformTests(unittest.TestCase):
 def test_real_font_measure_raster_and_complete_resource_cleanup(self):
  g=WindowsGDI();f=g.font([0,0,0,0,400,0,0,0,1,5,0,0,0],b'Arial');dc=g.dc();g.select(dc,f)
  size,face=g.measure(dc,b'Original text');self.assertTrue(face);self.assertGreater(size[0],0)
  header=struct.pack('<IiiHHIIiiII',40,256,-32,1,32,0,0,0,0,0,0);dib=g.dib(dc,header);g.select(dc,dib)
  g.g.SetBkMode(dc,1);g.g.SetTextColor(dc,0xFFFFFF)
  self.assertTrue(g.g.TextOutA(dc,2,2,b'Original text',13));raw=g.raster(dib)
  self.assertEqual(len(raw),256*32*4);self.assertTrue(any(raw))
  self.assertEqual(g.close(),{'fonts':1,'bitmaps':1,'dcs':1,'all_resources_released':True})
  self.assertTrue(g.close()['already_closed'])

 def test_reject_bad_api_shapes_before_allocating_resources(self):
  with WindowsGDI() as g:
   for args in ([],[True]*13,[0]*14):
    with self.assertRaises(ValueError):g.font(args,b'Arial')
   for raw in (b'',b'AB\0',b'A'*255,'text'):
    with self.assertRaises(ValueError):g.string(raw)
   with self.assertRaises(ValueError):g.measure(1,b'text')
   with self.assertRaises(ValueError):g.select(1,2)
   with self.assertRaises(ValueError):g.dib(1,bytes(40))
   dc=g.dc()
   for w,h,bpp in ((0,-32,32),(1025,-32,32),(256,32,32),(256,-257,32),(256,-32,16)):
    with self.assertRaises(ValueError):g.dib(dc,struct.pack('<IiiHHIIiiII',40,w,h,1,bpp,0,0,0,0,0,0))
   self.assertEqual(len(g.fonts),0);self.assertEqual(len(g.bitmaps),0)

 def test_zero_oversized_handles_and_closed_adapter_refused(self):
  self.assertEqual(WindowsGDI.handle(0xFFFFFFFF80000001),0x80000001)
  for value in (None,0,0x100000000,-1,0xFFFFFFFF,0xFFFFFFFFFFFFFFFF,0xFFFFFFFF00000001):
   with self.assertRaises(RuntimeError):WindowsGDI.handle(value)
  g=WindowsGDI();g.close()
  with self.assertRaises(RuntimeError):g.dc()
  with self.assertRaises(ValueError):g.font([0]*13,b'Arial')

if __name__=='__main__':unittest.main()
