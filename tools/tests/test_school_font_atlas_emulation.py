import json
import unittest
from copy import deepcopy
from tools.school_font_atlas import ROOT
from tools.school_font_atlas_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class TextureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-atlas-texture-v1-20261018.json').read_text())

    def test_original_texture_and_bitmap_header_with_fresh_rerun(self):
        self.assertTrue(verify_report(self.report)['atlas_texture_created'])
        from tools.school_font_atlas_emulation import generate
        self.assertEqual(verify_report(generate('texture'))['cases'], 2)

    def test_texture_ABI_original_returns_header_CPU_trace_and_scope_corruptions_refused(self):
        changes = [lambda c: c['atlas_texture']['before_cpu'].update(EIP=0),
                   lambda c: c['atlas_texture']['api_calls'][0]['args'].__setitem__(5, 21),
                   lambda c: c['atlas_texture']['api_calls'][0]['result']['inspection'].update(native_requested=True),
                   lambda c: c['atlas_texture']['entries'][0]['args'].__setitem__(2, 39),
                   lambda c: c['atlas_texture']['returns'][1].update(eax=0),
                   lambda c: c['atlas_texture']['bitmap_header'].update(hex='00'*40),
                   lambda c: c['atlas_texture']['cpu'].update(EFLAGS=0),
                   lambda c: c['atlas_texture']['pending'].update(platform_call_executed=True),
                   lambda c: c['atlas_texture']['state'].update(image_sha256='0'*64),
                   lambda c: c['atlas_texture'].update(GDI_prepared=True),
                   lambda c: c['device_cleanup'].update(atlas_texture_release_count=1),
                   lambda c: c['device_trace'][-2]['reply'].update(id=0)]
        for n, change in enumerate(changes):
            with self.subTest(change=n):
                bad = deepcopy(self.report); change(bad['cases'][0])
                with self.assertRaises(ValueError): verify_report(bad)

    def test_rehashed_complete_slot_parent_heap_owner_and_foreign_map_corruptions_refused(self):
        for field, offset in (('slot_heap', 4188), ('slot_heap', 4208), ('slot_heap', 5752),
                              ('slot_heap', 4095), ('owner', 0x1090), ('heap', 4104), ('map', 0)):
            bad = deepcopy(self.report); s = bad['cases'][0]['atlas_texture']
            row = s['slot_heap'] if field == 'slot_heap' else s['state']['owner'] if field == 'owner' else s['heaps'][0] if field == 'heap' else s['state']['foreign_maps'][0]
            raw = bytearray(unpack(row)); raw[offset] ^= 1; row.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError): verify_report(bad)


class PreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-atlas-preparation-v1-20261018.json').read_text())

    def test_original_GDI_preparation_and_fresh_owned_rerun(self):
        self.assertTrue(verify_report(self.report)['GDI_prepared'])
        from tools.school_font_atlas_emulation import generate
        self.assertEqual(verify_report(generate('gdi'))['cases'], 2)

    def test_GDI_ABI_native_arithmetic_locals_pending_CPU_trace_and_cleanup_corruptions_refused(self):
        changes = [lambda c: c['GDI_preparation']['before_cpu'].update(ESP=0),
            lambda c: c['GDI_preparation']['api_calls'][1]['request'].update(header_hex='00'*40),
            lambda c: c['GDI_preparation']['api_calls'][3]['result'].update(result=15),
            lambda c: c['GDI_preparation']['api_calls'][4]['request']['args'].__setitem__(0, -15),
            lambda c: c['GDI_preparation']['api_calls'][4]['result']['inspection'].update(native_requested=True),
            lambda c: c['GDI_preparation']['api_calls'][5]['args'].__setitem__(1, 0),
            lambda c: c['GDI_preparation']['returns'][3].update(eax=95),
            lambda c: c['GDI_preparation']['entries'][0].update(sp=0),
            lambda c: c['GDI_preparation']['GDI_locals'].update(text_hex='2100'),
            lambda c: c['GDI_preparation']['GDI_locals'].update(height=16),
            lambda c: c['GDI_preparation']['pending']['args'].__setitem__(2, 2),
            lambda c: c['GDI_preparation']['pending'].update(first_instruction_executed=True),
            lambda c: c['GDI_preparation']['cpu'].update(EFLAGS=0),
            lambda c: c['GDI_preparation'].update(glyph_upload_executed=True),
            lambda c: c['GDI_preparation'].update(DIB_pixels_read=True),
            lambda c: c['platform_trace'][-2]['reply'].update(id=0),
            lambda c: c['platform_cleanup'].update(atlas_selection_restored=False)]
        for n, change in enumerate(changes):
            with self.subTest(change=n):
                bad = deepcopy(self.report); change(bad['cases'][0])
                with self.assertRaises(ValueError): verify_report(bad)

    def test_rehashed_GDI_objects_maps_and_native_ownership_refusals(self):
        for field, offset in (('slot', 4188), ('slot', 4208), ('heap', 4104), ('map', 0), ('owner', 0x1094)):
            bad = deepcopy(self.report); s = bad['cases'][0]['GDI_preparation']
            row = s['slot_heap'] if field == 'slot' else s['heaps'][0] if field == 'heap' else s['state']['owner'] if field == 'owner' else s['state']['foreign_maps'][0]
            raw = bytearray(unpack(row)); raw[offset] ^= 1; row.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError): verify_report(bad)
        from tools.school_font_atlas_emulation import AtlasEmulator
        e = AtlasEmulator.__new__(AtlasEmulator); e.atlas_running, e.image, e.foreign = True, b'', {}
        for at in (0x2300D000, 0x23001000, 0x80A398):
            with self.assertRaises(RuntimeError): e._write(None, None, at, 4, 0, None)
        with self.assertRaises(RuntimeError): e._slot_read(None, None, 0x2300D678, 1, 0, None)
