import json
import struct
import unittest
from tools.school_font_state_device import *


class DeviceTests(unittest.TestCase):
    def test_actual_immutable_build_and_parent(self):
        r=json.loads((ROOT/'analysis/school-font-state-device-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(SOURCE,HELPER)
        p=json.loads((ROOT/'analysis/school-font-glyph-device-v1-20261019.json').read_text())
        self.assertEqual(p['build']['source_sha256'],sha((ROOT/'tools/school_font_glyph_device.cs').read_bytes()))

    def test_actual_VB_description_two_distinct_blocks_and_full_cleanup(self):
        r=probe();self.assertEqual(r['vertex']['inspection'],dict(native_requested=False,method='GetDesc(vertex buffer)',result=dict(hr=0,hex=struct.pack('<6I',100,6,520,0,8400,0).hex())))
        tokens=[c['result']['token'] for c in r['calls'] if c['request']['method']=='end']
        self.assertEqual(len(tokens),2);self.assertNotEqual(tokens[0],tokens[1]);self.assertTrue(all(tokens))
        self.assertEqual(r['cleanup']['font_state_block_delete_results'],[0,0]);self.assertEqual(r['cleanup']['font_vertex_buffer_release_count'],0)
        self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_wrong_owner_order_values_duplicate_and_partial_recording_cleanup(self):
        def run(bridge):
            with self.assertRaises(ValueError):bridge.request('font_vb',pointer=1,args=[8400,520,0,0])
            device,texture=ready(bridge)
            with self.assertRaises(ValueError):bridge.request('font_vb',pointer=device,args=[8401,520,0,0])
            bridge.request('font_vb',pointer=device,args=[8400,520,0,0])
            with self.assertRaises(ValueError):bridge.request('font_vb',pointer=device,args=[8400,520,0,0])
            with self.assertRaises(ValueError):bridge.request('font_state',pointer=device,method='end',args=[])
            bridge.request('font_state',pointer=device,method='begin',args=[])
            with self.assertRaises(ValueError):bridge.request('font_state',pointer=device,method='texture',args=[0,1])
        r=owned_run(run);self.assertEqual(r['cleanup']['abandoned_font_end_hr'],0);self.assertEqual(r['cleanup']['abandoned_font_delete_hr'],0);self.assertTrue(r['cleanup']['all_owned_resources_released'])
