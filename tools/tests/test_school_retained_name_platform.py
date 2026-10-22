"""Owned offscreen DC translation and bounded source name strings."""
import struct,unittest
from types import SimpleNamespace
from tools import school_retained_name_raster as work


class PlatformTests(unittest.TestCase):
 def test_logical_dc_is_never_native_dc_argument(self):
  s=work.Offscreen.__new__(work.Offscreen);s.logical=123;s.actual=456;s.gdi=SimpleNamespace(dcs={456,789})
  self.assertEqual(s.dc(123),456);self.assertEqual(s.dc(789),789)
  with self.assertRaisesRegex(ValueError,'owned fresh'):s.dc(321)
 def test_zero_historical_dc_rejected_before_native_creation(self):
  with self.assertRaisesRegex(ValueError,'nonzero historical'):work.Offscreen(0)
 def test_negative_historical_dc_rejected(self):
  with self.assertRaisesRegex(ValueError,'nonzero historical'):work.Offscreen(-1)
 def test_source_ANSI_string_keeps_raw_bytes(self):
  b=bytes.fromhex('b7e6a7c6b2fab5b7')+bytes(1);g=SimpleNamespace(read=lambda p,n=4:b[p:p+n]);self.assertEqual(work.text(g,0),b[:-1]);self.assertEqual(work.text(g,0,8),b[:-1])
 def test_unterminated_source_string_rejected(self):
  with self.assertRaisesRegex(ValueError,'bounded terminated'):work.text(SimpleNamespace(read=lambda p,n=4:b'x'*n),0)
 def test_embedded_zero_span_rejected(self):
  with self.assertRaisesRegex(ValueError,'nonempty ANSI span'):work.text(SimpleNamespace(read=lambda p,n=4:b'\0'*n),0,1)
 def test_actual_offscreen_owned_cleanup(self):
  s=work.Offscreen(0x12345678)
  try:self.assertEqual(s.dc(s.logical),s.actual);self.assertGreater(s.actual,0)
  finally:cleanup=s.close()
  self.assertEqual(cleanup,dict(fonts=0,bitmaps=0,dcs=1,all_resources_released=True));self.assertEqual(s.close(),cleanup)
 def test_platform_rejects_foreign_DC_before_OS_call(self):
  s=work.Offscreen(0x12345678)
  try:
   with self.assertRaisesRegex(ValueError,'owned fresh'):s.call(None,'SetTextColor',[0x12345000,0xffffff])
  finally:self.assertTrue(s.close()['all_resources_released'])


if __name__=='__main__':unittest.main()
