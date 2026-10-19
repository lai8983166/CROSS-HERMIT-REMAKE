import json
import unittest
from copy import deepcopy
from tools.school_font_second_resource import ROOT,SECOND
from tools.school_font_second_resource_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class TextureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((ROOT/'analysis/school-font-second-resource-texture-v1-20261019.json').read_text())

    def test_original_second_texture_header_and_fresh_owned_rerun(self):
        self.assertTrue(verify_report(self.report)['second_real_texture_created'])
        from tools.school_font_second_resource_emulation import generate
        self.assertFalse(verify_report(generate('texture'))['second_GDI_prepared'])

    def test_distinct_identity_retained_descriptions_tokens_native_ABI_and_cleanup_refused(self):
        changes=[lambda c:c['second_texture']['api_calls'][0]['result']['texture'].update(pointer=c['atlas_texture']['api_calls'][0]['result']['texture']['pointer']),
            lambda c:c['second_texture']['api_calls'][0]['args'].__setitem__(7,0x2300D05C),
            lambda c:c['second_texture']['api_calls'][0]['result']['retention_inspection'].update(native_requested=True),
            lambda c:c['second_texture']['api_calls'][0]['result']['retention_inspection']['first_vertex']['result'].update(hex='00'*24),
            lambda c:c['second_texture']['api_calls'][0]['result']['retained_state_tokens'].__setitem__(0,0),
            lambda c:c['second_texture']['entries'][0]['args'].__setitem__(2,39),
            lambda c:c['second_texture']['returns'][1].update(eax=0),
            lambda c:c['second_texture']['cpu'].update(EAX=0x2300D000),
            lambda c:c['second_texture']['pending'].update(platform_call_executed=True),
            lambda c:c['device_cleanup'].update(second_atlas_texture_release_count=1)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad=deepcopy(self.report);f(bad['cases'][0])
                with self.assertRaises(ValueError):verify_report(bad)

    def test_rehashed_complete_second_object_first_font_owner_and_maps_refused(self):
        for field,offset in (('second',4188),('second',4192),('second',0),('second',12287),('first',5744),('owner',0x1094),('map',0)):
            bad=deepcopy(self.report);s=bad['cases'][0]['second_texture']
            r=s['second_heap'] if field=='second' else s['slot_heap'] if field=='first' else s['state']['owner'] if field=='owner' else s['state']['foreign_maps'][0]
            raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)


class GDITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((ROOT/'analysis/school-font-second-resource-preparation-v1-20261019.json').read_text())

    def test_original_second_GDI_arithmetic_font_and_first_glyph_boundary_fresh_rerun(self):
        self.assertTrue(verify_report(self.report)['second_GDI_prepared'])
        from tools.school_font_second_resource_emulation import generate
        self.assertEqual(verify_report(generate('gdi'))['second_glyphs_measured'],0)

    def test_original_second_ANSI_height_weight_returns_locals_CPU_trace_and_scope_refused(self):
        changes=[lambda c:c['second_GDI']['api_calls'][3]['args'].__setitem__(0,12),
            lambda c:c['second_GDI']['api_calls'][3]['result'].update(result=10),
            lambda c:c['second_GDI']['api_calls'][4]['request'].update(face_hex='4669786564537973'),
            lambda c:c['second_GDI']['api_calls'][4]['args'].__setitem__(4,700),
            lambda c:c['second_GDI']['api_calls'][4]['result']['inspection'].update(native_requested=True),
            lambda c:c['second_GDI']['GDI_locals'].update(height=0xFFFFFFF0),
            lambda c:c['second_GDI']['returns'][4].update(eax=16),
            lambda c:c['second_GDI']['cpu'].update(ESP=0),
            lambda c:c['second_GDI']['pending']['args'].__setitem__(2,2),
            lambda c:c['second_GDI'].update(second_DIB_pixels_read=True),
            lambda c:c['platform_cleanup'].update(second_native_GDI_cleanup_executed=True),
            lambda c:c['platform_trace'][-2]['reply'].update(id=0)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad=deepcopy(self.report);f(bad['cases'][0])
                with self.assertRaises(ValueError):verify_report(bad)

    def test_full_pixel_snapshot_header_guard_maps_and_native_ownership_refused(self):
        from tools.school_font_state_emulation import unpack_large
        bad=deepcopy(self.report);r=bad['cases'][0]['second_GDI']['external_regions'][0]['buffer']
        raw=bytearray(unpack_large(r));raw[-1]^=1;r.update(buffer_evidence(bytes(raw)))
        with self.assertRaises(ValueError):verify_report(bad)
        for f in (lambda s:s['bitmap_header'].update(hex='00'*40),
                  lambda s:s['state'].update(image_sha256='00'*32),
                  lambda s:s['state'].update(SEH=0),
                  lambda s:s['state']['foreign_maps'].pop()):
            bad=deepcopy(self.report);f(bad['cases'][0]['second_GDI'])
            with self.assertRaises(ValueError):verify_report(bad)
        from tools.school_font_second_resource_emulation import SecondResourceEmulator
        e=SecondResourceEmulator.__new__(SecondResourceEmulator);e.resource_running=True
        for at in (SECOND+0x5C,SECOND-4,0x2300D064,0x20001094,0x79FC74):
            with self.assertRaises(RuntimeError):e._write(None,None,at,4,0,None)
        e.image,e.foreign=bytes(8),{}
        for at in (SECOND-1,SECOND+1655,0x24000000):
            with self.assertRaises(RuntimeError):e._slot_read(None,None,at,4,0,None)
