import json
import struct
import unittest
from tools.school_font_finish_platform import *


class GDITests(unittest.TestCase):
    def test_immutable_x86_GDI_and_preserved_parent(self):
        r=json.loads((ROOT/'analysis/school-font-finish-gdi-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(GDI_SOURCE.read_bytes()),helper_sha256=sha(GDI_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(GDI_SOURCE,GDI_HELPER)
        old=json.loads((ROOT/'analysis/school-font-second-glyph-gdi-v2-20261019.json').read_text())
        self.assertEqual(old['build']['source_sha256'],sha((ROOT/'tools/school_font_second_glyph_gdi_v2.cs').read_bytes()))

    def test_actual_second_native_delete_order_lifetime_and_independent_counters(self):
        r=gdi_probe();self.assertEqual([x['result']['result'] for x in r['deletion']],[1,1,1])
        self.assertEqual(r['deletion'][1]['result']['inspection'],dict(native_requested=False,method='GdiFlush/GetObjectA/GetObjectType(bitmap)',result=0,reported_type=7))
        for kind in ('fonts','dcs','bitmaps'):
            self.assertEqual(r['cleanup']['second_native_atlas_'+kind+'_released'],1)
            self.assertEqual(r['cleanup']['native_atlas_'+kind+'_released'],1)
            self.assertEqual(r['cleanup']['second_atlas_'+kind+'_released'],0)
        self.assertTrue(r['cleanup']['second_native_GDI_cleanup_executed']);self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_early_foreign_wrong_order_and_partial_pending_bitmap_cleanup_refused(self):
        with FinishGDI() as p:
            with self.assertRaises(ValueError):p.request('second_font_delete_bitmap',pointer=1)
            ready=gdi_ready(p);second_raster(p,ready);prep=ready['second']
            with self.assertRaises(ValueError):p.request('second_font_delete_dc',pointer=prep[0]['result']['result'])
            with self.assertRaises(ValueError):p.request('second_font_delete_bitmap',pointer=1)
            p.request('second_font_delete_bitmap',pointer=prep[1]['result']['result'])
        self.assertTrue(p.cleanup['all_owned_resources_released']);self.assertTrue(p.cleanup['second_atlas_selection_restored'])
        self.assertFalse(p.cleanup['second_native_GDI_cleanup_executed'])


class DeviceTests(unittest.TestCase):
    def test_immutable_x86_device_and_preserved_parent(self):
        r=json.loads((ROOT/'analysis/school-font-finish-device-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(DEVICE_SOURCE.read_bytes()),helper_sha256=sha(DEVICE_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(DEVICE_SOURCE,DEVICE_HELPER)
        old=json.loads((ROOT/'analysis/school-font-second-glyph-device-v1-20261019.json').read_text())
        self.assertEqual(old['build']['source_sha256'],sha((ROOT/'tools/school_font_second_glyph_device.cs').read_bytes()))

    def test_distinct_two_VBs_four_tokens_exact_second_states_and_complete_cleanup(self):
        r=device_probe();self.assertNotEqual(r['vertex']['buffer']['pointer'],r['first']['vertex']['buffer']['pointer'])
        self.assertEqual(r['vertex']['inspection'],dict(native_requested=False,method='GetDesc(vertex buffer)',result=dict(hr=0,hex=struct.pack('<6I',100,6,520,0,8400,0).hex())))
        tokens=[x['result']['token'] for x in r['first']['states']+r['states'] if x['request']['method']=='end']
        self.assertEqual(len(set(tokens)),4);self.assertTrue(all(tokens))
        for field in ('font_state_block_delete_results','second_font_state_block_delete_results'):self.assertEqual(r['cleanup'][field],[0,0])
        for field in ('font_vertex_buffer_release_count','second_font_vertex_buffer_release_count','atlas_texture_release_count','second_atlas_texture_release_count'):self.assertEqual(r['cleanup'][field],0)
        self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_foreign_early_duplicate_wrong_texture_and_partial_second_recording_refused(self):
        def run(b):
            with self.assertRaises(ValueError):b.request('second_font_vb',pointer=1,args=[8400,520,0,0])
            first,second=ready_device(b);device=first['device']
            with self.assertRaises(ValueError):b.request('second_font_vb',pointer=device,args=[8401,520,0,0])
            b.request('second_font_vb',pointer=device,args=[8400,520,0,0])
            with self.assertRaises(ValueError):b.request('second_font_vb',pointer=device,args=[8400,520,0,0])
            b.request('second_font_state',pointer=device,method='begin',args=[])
            with self.assertRaises(ValueError):b.request('second_font_state',pointer=device,method='texture',args=[0,first['texture']])
        r=owned_run(run);self.assertEqual(r['cleanup']['abandoned_second_font_end_hr'],0);self.assertEqual(r['cleanup']['abandoned_second_font_delete_hr'],0)
        self.assertTrue(r['cleanup']['all_owned_resources_released'])
