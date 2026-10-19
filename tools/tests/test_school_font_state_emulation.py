import json
import unittest
from copy import deepcopy
from tools.school_font_state import ROOT
from tools.school_font_state_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class CleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-state-cleanup-v1-20261019.json').read_text())

    def test_original_cleanup_ret4_caller_and_fresh_owned_rerun(self):
        self.assertTrue(verify_report(self.report)['full4010D0_returned'])
        from tools.school_font_state_emulation import generate
        self.assertEqual(verify_report(generate('cleanup'))['cases'],2)

    def test_GDI_lifetime_ABI_returns_CPU_and_native_cleanup_authority_refused(self):
        changes=[lambda c:c['font_cleanup']['before_cpu'].update(EIP=0),lambda c:c['font_cleanup']['api_calls'][0]['args'].__setitem__(0,0),
            lambda c:c['font_cleanup']['api_calls'][1]['result']['inspection'].update(native_requested=True),lambda c:c['font_cleanup']['api_calls'][1]['result']['inspection'].update(result=24),
            lambda c:c['font_cleanup']['returns'][-1].update(sp=0),lambda c:c['font_cleanup']['cpu'].update(EDX=0),
            lambda c:c['font_cleanup'].update(full4010D0_returned=False),lambda c:c['platform_cleanup'].update(native_atlas_bitmaps_released=0)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad=deepcopy(self.report);f(bad['cases'][0])
                with self.assertRaises(ValueError):verify_report(bad)

    def test_rehashed_preserved_object_owner_and_new_GDI_maps_refused(self):
        for field,offset in (('slot',4188),('slot',4208),('owner',0x1090),('map',0)):
            bad=deepcopy(self.report);s=bad['cases'][0]['font_cleanup'];r=s['slot_heap'] if field=='slot' else s['state']['owner'] if field=='owner' else s['state']['foreign_maps'][0]
            raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)


class VertexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-state-vertex-v1-20261019.json').read_text())

    def test_original_VB_creation_and_fresh_owned_rerun(self):
        self.assertTrue(verify_report(self.report)['vertex_buffer_created'])
        from tools.school_font_state_emulation import generate
        self.assertEqual(verify_report(generate('vertex'))['state_blocks'],0)

    def test_native_VB_output_description_CPU_trace_and_cleanup_refused(self):
        changes=[lambda c:c['font_vertex']['entries'][0].update(receiver=0),lambda c:c['font_vertex']['api_calls'][0]['args'].__setitem__(1,8399),
            lambda c:c['font_vertex']['api_calls'][0]['result']['inspection'].update(native_requested=True),lambda c:c['font_vertex']['api_calls'][0]['result']['buffer'].update(pointer=0),
            lambda c:c['font_vertex']['returns'][0].update(eax=1),lambda c:c['font_vertex']['cpu'].update(ESP=0),
            lambda c:c['font_vertex'].update(state_blocks_created=True),lambda c:c['device_cleanup'].update(font_vertex_buffer_release_count=1)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad=deepcopy(self.report);f(bad['cases'][0])
                with self.assertRaises(ValueError):verify_report(bad)

    def test_rehashed_VB_field_padding_and_interface_maps_refused(self):
        for field,offset in (('slot',4192),('slot',5728),('slot',5744),('map',0)):
            bad=deepcopy(self.report);s=bad['cases'][0]['font_vertex'];r=s['slot_heap'] if field=='slot' else s['state']['foreign_maps'][0]
            raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)
