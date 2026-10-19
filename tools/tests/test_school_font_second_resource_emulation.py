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
