import json
import struct
import unittest
from tools.school_font_second_resource_platform import *
from tools.school_font_second_resource import font_logfont


class DeviceTests(unittest.TestCase):
    def test_immutable_x86_build_and_preserved_parent(self):
        r=json.loads((ROOT/'analysis/school-font-second-resource-device-v2-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(DEVICE_SOURCE.read_bytes()),helper_sha256=sha(DEVICE_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(DEVICE_SOURCE,DEVICE_HELPER)
        parent=json.loads((ROOT/'analysis/school-font-state-device-v1-20261019.json').read_text())
        self.assertEqual(parent['build']['source_sha256'],sha((ROOT/'tools/school_font_state_device.cs').read_bytes()))

    def test_distinct_live_atlases_retained_VB_tokens_and_balanced_cleanup(self):
        r=device_probe();second=r['second'];first=r['first']
        self.assertNotEqual(second['texture']['pointer'],first['texture'])
        desc=struct.pack('<8I',26,1,0,1,131072,0,256,256).hex()
        self.assertEqual(second['inspection'],dict(native_requested=False,method='GetLevelDesc',level=0,result=dict(hr=0,hex=desc)))
        self.assertEqual(second['retention_inspection'],dict(native_requested=False,method='GetLevelDesc(first texture)/GetDesc(first vertex buffer)',first_texture=dict(pointer=first['texture'],hr=0,hex=desc),first_vertex=dict(pointer=first['vertex']['buffer']['pointer'],result=dict(hr=0,hex=struct.pack('<6I',100,6,520,0,8400,0).hex()))))
        self.assertEqual(second['retained_state_tokens'],[row['result']['token'] for row in first['states'] if row['request']['method']=='end'])
        self.assertIs(second['retained_state_tokens_are_ownership_metadata'],True)
        self.assertEqual(r['cleanup']['second_atlas_texture_release_count'],0)
        self.assertEqual(r['cleanup']['font_state_block_delete_results'],[0,0])
        self.assertIs(r['cleanup']['all_owned_resources_released'],True)

    def test_foreign_early_duplicate_wrong_format_and_partial_cleanup_refused(self):
        def run(bridge):
            with self.assertRaises(ValueError):create_second(bridge,1)
            device,texture=ready(bridge)
            with self.assertRaises(ValueError):create_second(bridge,device)
            bridge.request('font_vb',pointer=device,args=[8400,520,0,0])
            for row in plan(texture):bridge.request('font_state',pointer=device,**row)
            with self.assertRaises(ValueError):create_second(bridge,device,format=21)
            second=create_second(bridge,device)
            with self.assertRaises(ValueError):create_second(bridge,device)
            with self.assertRaises(ValueError):bridge.request('atlas_lock',pointer=second['texture']['pointer'],level=0,rect=0,flags=0)
        r=owned_run(run)
        self.assertIs(r['cleanup']['all_owned_resources_released'],True)
        self.assertEqual(r['cleanup']['second_atlas_texture_release_count'],0)
