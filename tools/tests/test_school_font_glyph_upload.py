import base64
import json
import unittest
import zlib
from copy import deepcopy
from tools.school_font_glyph import ROOT
from tools.school_font_glyph_upload_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class UploadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-glyph-upload-v1-20261019.json').read_text())

    def test_full_native_pixels_real_upload_and_fresh_owned_rerun(self):
        self.assertTrue(verify_report(self.report)['actual_texture_upload_verified'])
        from tools.school_font_glyph_upload import generate
        self.assertEqual(verify_report(generate())['pixels_per_case'],65536)

    def test_lock_ABI_pixel_sequence_CPU_readback_trace_and_scope_corruptions_refused(self):
        changes=[lambda c:c['pixel_upload']['before_cpu'].update(EIP=0),lambda c:c['pixel_upload']['api_calls'][0]['args'].__setitem__(4,16),
            lambda c:c['pixel_upload']['api_calls'][0]['result'].update(locked_hex='00'*8),lambda c:c['pixel_upload']['api_calls'][1]['result']['inspection'].update(native_requested=True),
            lambda c:c['pixel_upload']['returns'][0].update(eax=1),lambda c:c['pixel_upload']['cpu'].update(ESP=0),
            lambda c:c['pixel_upload']['locals'].update(x=255),lambda c:c['pixel_upload'].update(native_pixel_reads=65535),
            lambda c:c['pixel_upload'].update(write_sequence_sha256='0'*64),lambda c:c['pixel_upload'].update(full4010D0_returned=True),
            lambda c:c['device_trace'][-2]['reply'].update(id=0)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad=deepcopy(self.report);f(bad['cases'][0])
                with self.assertRaises(ValueError):verify_report(bad)

    def test_rehashed_full_DIB_texture_data_guards_and_ownership_refusals(self):
        for n,kind in ((0,'guard'),(0,'data'),(1,'guard'),(1,'data')):
            bad=deepcopy(self.report);r=bad['cases'][0]['pixel_upload']['external_regions'][n]
            self.assertLessEqual(r['buffer']['bytes'],274432)
            dec=zlib.decompressobj();data=bytearray(dec.decompress(base64.b64decode(r['buffer']['zlib_base64'],validate=True),r['buffer']['bytes']+1))
            self.assertEqual(len(data),r['buffer']['bytes']);self.assertTrue(dec.eof);self.assertFalse(dec.unused_data or dec.unconsumed_tail)
            offset=0 if kind=='guard' else r['pointer']-r['base'];data[offset]^=1;r['buffer'].update(buffer_evidence(bytes(data)))
            with self.assertRaises(ValueError):verify_report(bad)
        from tools.school_font_glyph_upload import PixelEmulator
        e=PixelEmulator.__new__(PixelEmulator);e.pixel_running=True
        with self.assertRaises(RuntimeError):e._write(None,None,0x2300D070,4,0,None)
        with self.assertRaises(RuntimeError):e._write(None,None,0x80A398,4,0,None)
