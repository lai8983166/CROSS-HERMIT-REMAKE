import json
import unittest
from copy import deepcopy
from tools.school_font_second_glyph import ROOT,SECOND
from tools.school_font_second_glyph_verification import verify_report
from tools.school_font_state_emulation import unpack_large
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class RetirementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-second-glyph-retirement-v2-20261019.json').read_text())

    def test_exact_mapping_retirement_and_fresh_CPU_preserving_rerun(self):
        self.assertTrue(verify_report(self.report)['deleted_first_DIB_mapping_retired'])
        from tools.school_font_second_glyph_emulation import generate
        self.assertEqual(verify_report(generate('retirement'))['second_glyphs_per_case'],0)

    def test_wrong_mapping_CPU_release_authority_or_native_call_refused(self):
        changes=[lambda r:r['cpu'].update(EIP=0),lambda r:r['mappings_after'].pop(),
            lambda r:r['mappings_before'][0].__setitem__(2,0),lambda r:r['retired_regions'][0].update(host_release_performed_by_retirement=True),
            lambda r:r['retired_regions'][0].update(native_game_call_executed=True),lambda r:r.update(original_instructions_executed=1),
            lambda r:r['api_calls'].append({}),lambda r:r.update(full415F50_returned=True)]
        for f in changes:
            bad=deepcopy(self.report);f(bad['cases'][0]['DIB_retirement'])
            with self.assertRaises(ValueError):verify_report(bad)

    def test_rehashed_deleted_DIB_and_retained_first_texture_guard_refused(self):
        for name in ('retired','active'):
            bad=deepcopy(self.report);r=bad['cases'][0]['DIB_retirement']
            b=r['retired_regions'][0]['region']['buffer'] if name=='retired' else r['external_regions'][0]['buffer']
            raw=bytearray(unpack_large(b));raw[-1]^=1;b.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)


class RasterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-second-glyph-raster-v2-20261019.json').read_text())

    def test_original95_dynamic_glyphs_UV_ink_and_fresh_rerun(self):
        self.assertEqual(verify_report(self.report)['second_glyphs_per_case'],95)
        from tools.school_font_second_glyph_emulation import generate
        self.assertEqual(verify_report(generate('raster'))['second_UV_stores'],380)

    def test_GDI_ABI_dynamic_layout_ABC_inspection_return_CPU_and_scope_refused(self):
        changes=[lambda r:r['api_calls'][0]['args'].__setitem__(2,2),lambda r:r['api_calls'][1]['request'].update(x=1),
            lambda r:r['inspections'][0]['result']['ink_inspection'].update(native_requested=True),
            lambda r:r['inspections'][1]['result']['ink_inspection'].update(hex='00'*1140),
            lambda r:r['layout'][87].update(width=7),lambda r:r['returns'][-1].update(sp=0),
            lambda r:r['cpu'].update(EDX=126),lambda r:r.update(UV_stores_completed=379),lambda r:r.update(second_texture_upload_executed=True)]
        for f in changes:
            bad=deepcopy(self.report);f(bad['cases'][0]['second_raster'])
            with self.assertRaises(ValueError):verify_report(bad)

    def test_full_UV_padding_guard_and_outside_ink_pixel_refused(self):
        for offset in (4208,5728,5744,0,12287):
            bad=deepcopy(self.report);r=bad['cases'][0]['second_raster']['second_heap'];raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)
        bad=deepcopy(self.report);r=bad['cases'][0]['second_raster']['inspections'][1]['result'];raw=bytearray.fromhex(r['hex']);raw[-4]^=255;r['hex']=raw.hex()
        with self.assertRaises(ValueError):verify_report(bad)


class UploadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-second-glyph-upload-v2-20261019.json').read_text())

    def test_original65536_pixels_second_readback_and_actual_first_retention_fresh_rerun(self):
        self.assertTrue(verify_report(self.report)['actual_second_upload_verified'])
        from tools.school_font_second_glyph_emulation import generate
        self.assertTrue(verify_report(generate('upload'))['actual_first_texture_readback_unchanged'])

    def test_lock_output_full_pixel_order_both_readbacks_CPU_and_cleanup_refused(self):
        changes=[lambda c:c['second_upload']['api_calls'][0]['args'].__setitem__(2,0),
            lambda c:c['second_upload']['api_calls'][1]['result']['retained_first_texture_inspection'].update(hex='00'*131072),
            lambda c:c['second_upload']['api_calls'][1]['result']['inspection'].update(native_requested=True),
            lambda c:c['second_upload'].update(native_pixel_reads=65535),lambda c:c['second_upload'].update(write_sequence_sha256='00'*32),
            lambda c:c['second_upload']['cpu'].update(ESP=0),lambda c:c['second_upload']['locals'].update(y=255),
            lambda c:c['second_upload'].update(full4010D0_returned=True),lambda c:c['device_cleanup'].update(second_atlas_texture_release_count=1)]
        for f in changes:
            bad=deepcopy(self.report);f(bad['cases'][0])
            with self.assertRaises(ValueError):verify_report(bad)

    def test_retired_evidence_new_pixels_guards_overlap_and_native_ownership_refused(self):
        for index in range(3):
            bad=deepcopy(self.report);b=bad['cases'][0]['second_upload']['external_regions'][index]['buffer'];raw=bytearray(unpack_large(b));raw[-1]^=1;b.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)
        bad=deepcopy(self.report);bad['cases'][0]['second_upload']['external_regions'][1]['base']=bad['cases'][0]['second_upload']['external_regions'][0]['base']
        with self.assertRaises(ValueError):verify_report(bad)
        from tools.school_font_second_glyph_emulation import SecondGlyphEmulator
        e=SecondGlyphEmulator.__new__(SecondGlyphEmulator);e.second_glyph_running=False;e.second_pixel_running=True;e.second_bits=0x30001000;e.second_pixel_reads=0
        for at in (SECOND+112,0x2300D070,0x30001001):
            if at==0x30001001:
                with self.assertRaises(RuntimeError):e._slot_read(None,None,at,4,0,None)
            else:
                with self.assertRaises(RuntimeError):e._write(None,None,at,4,0,None)
