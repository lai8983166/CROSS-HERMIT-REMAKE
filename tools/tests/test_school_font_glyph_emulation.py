import json
import unittest
from copy import deepcopy
from tools.school_font_glyph import ROOT
from tools.school_font_glyph_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class RasterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-glyph-raster-v1-20261019.json').read_text())

    def test_complete_original95_glyphs_and_fresh_owned_rerun(self):
        self.assertEqual(verify_report(self.report)['glyphs_per_case'],95)
        from tools.school_font_glyph_emulation import generate
        self.assertEqual(verify_report(generate())['UV_stores_per_case'],380)

    def test_glyph_ABI_dimensions_wrap_returns_CPU_snapshots_and_trace_corruptions_refused(self):
        changes=[lambda c:c['glyph_raster']['before_cpu'].update(EIP=0),lambda c:c['glyph_raster']['api_calls'][0]['args'].__setitem__(2,2),
            lambda c:c['glyph_raster']['api_calls'][1]['request'].update(x=1),lambda c:c['glyph_raster']['api_calls'][2]['request'].update(before_hex='cc'*8),
            lambda c:c['glyph_raster']['returns'][-1].update(eax=0),lambda c:c['glyph_raster']['cpu'].update(EAX=0),
            lambda c:c['glyph_raster']['layout'][25].update(y=0),lambda c:c['glyph_raster']['inspections'][1]['result'].update(native_requested=True),
            lambda c:c['glyph_raster'].update(glyphs_completed=94),lambda c:c['glyph_raster'].update(texture_upload_executed=True),
            lambda c:c['platform_trace'][-2]['reply'].update(id=0)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad=deepcopy(self.report);f(bad['cases'][0])
                with self.assertRaises(ValueError):verify_report(bad)

    def test_rehashed_UV_padding_owner_foreign_maps_and_outside_glyph_pixels_refused(self):
        for field,offset in (('slot',4208),('slot',5728),('slot',5744),('slot',4095),('owner',0x1090),('map',0)):
            bad=deepcopy(self.report);s=bad['cases'][0]['glyph_raster'];row=s['slot_heap'] if field=='slot' else s['state']['owner'] if field=='owner' else s['state']['foreign_maps'][0]
            raw=bytearray(unpack(row));raw[offset]^=1;row.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)
        bad=deepcopy(self.report);row=bad['cases'][0]['glyph_raster']['inspections'][1]['result'];raw=bytearray.fromhex(row['hex']);raw[-1]^=1;row['hex']=raw.hex()
        with self.assertRaises(ValueError):verify_report(bad)
