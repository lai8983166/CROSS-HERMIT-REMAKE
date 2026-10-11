import hashlib,json,struct,unittest
from copy import deepcopy
from tools.school_font_raster_catalog import *
from tools.school_text_pixel_emulation import run_conversion

class RasterSourceTests(unittest.TestCase):
 def test_complete_memory_and_original_bitmap_texture_geometry(self):
  self.assertGreater(len(source_catalog()['code_inputs']),40)
  for c in native_fixture()['cases']:
   p=c['font_raster'];e=expected_raster(p['inputs'],p['before'],p['measured'])
   self.assertEqual(e['after'],p['after']);self.assertEqual(e['raster_size'],p['raster']['size'])
   self.assertEqual(e['header_hex'],next(r['header_hex'] for r in p['font_api'] if r['name']=='CreateDIBSection'))
   draw=[r for r in p['font_api'] if r['name']=='TextOutA'];pad=e['padding']
   self.assertEqual([r['args'][1:3] for r in draw],[[2*pad,2*pad],[pad,pad]])

 def test_source_geometry_clamps_and_exact_256_band_boundary(self):
  self.assertEqual(geometry([170,20])['raster_size'],[174,24])
  self.assertEqual(geometry([254,1])['bands'],2)
  self.assertEqual(geometry([254,1])['texture_size'],[256,6])
  self.assertEqual(geometry([100000,250])['raster_size'],[512,256]);self.assertEqual(geometry([100000,250])['texture_size'],[256,256])
  for bad in ([True,20],[1,0],[1,251],[0,1],[1],None):
   with self.assertRaises(ValueError):geometry(bad)
  p=native_fixture()['cases'][0]['font_raster']
  for key,value in (('device',1),('graphics_context',False),('host_ansi_code_page',False),('platform','GPU')):
   inputs=deepcopy(p['inputs']);inputs[key]=value
   with self.assertRaises(ValueError):expected_raster(inputs,p['before'],p['measured'])

 def test_pixel_alpha_is_rgb_nonzero_and_channels_are_five_bits(self):
  values=[0,0xFF000000,1,0xFFFFFFFF,0x00FF0000,0x0000FF00,0x000000FF,0x80808]
  self.assertEqual([convert_pixel(v) for v in values],[0,0,0x8000,0xFFFF,0xFC00,0x83E0,0x801F,0x8421])
  raw=struct.pack('<8I',*values);dest=bytes([0xA5])*24
  p=run_conversion(raw,[4,2],[1,0,3,2],dest,12,[1,0]);expected=convert_surface(raw,[4,2],[1,0,3,2],dest,12,[1,0])
  self.assertEqual(bytes.fromhex(p['after_hex']),expected);self.assertEqual(p['write_count'],6)
  self.assertEqual(expected[:2],b'\xA5\xA5');self.assertEqual(expected[8:12],b'\xA5'*4)

 def test_real_rasters_all_pixels_and_padding_match_original_cpu(self):
  raw_report=(ROOT/'analysis/school-text-pixels-v1-20261012.json').read_bytes()
  self.assertEqual(hashlib.sha256(raw_report).hexdigest(),'e969ad431ae28920e00d7c065d91046633a66b58b0681739d78ee1c6def094d2')
  report=json.loads(raw_report)
  self.assertEqual(len(report['cases']),3)
  for c,r in zip(native_fixture()['cases'],report['cases']):
   raster=c['font_raster']['raster'];p=r['conversion'];raw=bytes.fromhex(raster['hex'])
   self.assertEqual(bytes.fromhex(p['after_hex']),convert_surface(raw,p['source_size'],p['rect'],bytes.fromhex(p['before_hex']),p['destination_pitch'],p['destination_point']))
   self.assertEqual(p['write_count'],raster['size'][0]*raster['size'][1]);self.assertTrue(p['source_and_metadata_retained']);self.assertFalse(p['GPU_executed'])

 def test_malformed_surface_extents_and_exports_refused_or_separated(self):
  raw=bytes(4*4);dest=bytes(12)
  for args in ((raw,[True,1],[0,0,1,1],dest,4,[0,0]),(raw,[4,1],[0,0,5,1],dest,12,[0,0]),
   (raw,[4,1],[0,0,4,1],dest,7,[0,0]),(raw,[4,1],[0,0,4,1],dest,12,[3,0]),(raw,[4,1],[0,0,4,1],dest,12,[0,1])):
   with self.assertRaises(ValueError):run_conversion(*args)
  rules=json.loads((ROOT/'prototype/data/school_font_raster_rules.json').read_text('utf-8'));evidence=json.loads((ROOT/'prototype/data/school_font_raster_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules);self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertFalse(evidence['runtime_fixture'])

if __name__=='__main__':unittest.main()
