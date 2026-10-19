import json
import unittest
from copy import deepcopy
from tools.school_font_finish import ROOT,SECOND
from tools.school_font_finish_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_font_state_emulation import unpack_large
from tools.school_renderer_init_emulation import buffer_evidence


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-font-finish-trajectory-v1-20261019.json').read_text())

    def refuse(self,changes):
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad=deepcopy(self.report);f(bad['cases'][0])
                with self.assertRaises(ValueError):verify_report(bad)


class CleanupTests(Base):
    def test_native_second_GDI_ret4_and_index1_caller_ABI(self):
        self.assertTrue(verify_report(self.report)['original_second_cleanup_executed'])
        self.refuse([lambda c:c['finish_cleanup']['api_calls'][0]['args'].__setitem__(0,1),
            lambda c:c['finish_cleanup']['api_calls'][1]['result']['inspection'].update(native_requested=True),
            lambda c:c['finish_cleanup']['api_calls'][1]['result']['inspection'].update(result=24),
            lambda c:c['finish_cleanup']['returns'][-1].update(eax=1),
            lambda c:c['finish_cleanup']['cpu'].update(EAX=0),
            lambda c:c['finish_cleanup'].update(original_second_GDI_cleanup_executed=False)])

    def test_complete_objects_pixels_retired_evidence_and_native_lifetime_refused(self):
        for key,offset in (('second_heap',4188),('slot_heap',5744)):
            bad=deepcopy(self.report);r=bad['cases'][0]['finish_cleanup'][key];raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)
        bad=deepcopy(self.report);r=bad['cases'][0]['finish_cleanup']['external_regions'][1]['buffer'];raw=bytearray(unpack_large(r));raw[-1]^=1;r.update(buffer_evidence(bytes(raw)))
        with self.assertRaises(ValueError):verify_report(bad)
        self.refuse([lambda c:c['platform_cleanup'].update(second_native_atlas_bitmaps_released=0),
            lambda c:c['finish_cleanup']['retired_regions'][0].update(host_release_performed_by_retirement=True)])


class VertexTests(Base):
    def test_native_second_VB_distinct_identity_description_and_output_ABI(self):
        self.assertEqual(verify_report(self.report)['vertex_buffers'],2)
        self.refuse([lambda c:c['finish_vertex']['api_calls'][0]['result']['buffer'].update(pointer=c['font_vertex']['api_calls'][0]['result']['buffer']['pointer']),
            lambda c:c['finish_vertex']['api_calls'][0]['args'].__setitem__(1,8399),
            lambda c:c['finish_vertex']['api_calls'][0]['args'].__setitem__(5,0x2300D060),
            lambda c:c['finish_vertex']['api_calls'][0]['result']['inspection']['result'].update(hex='00'*24),
            lambda c:c['finish_vertex']['entries'][0].update(receiver=0),lambda c:c['finish_vertex']['returns'][0].update(eax=1)])

    def test_complete_second_VB_field_padding_guard_and_owned_maps_refused(self):
        for offset in (4192,4208,5744,0,12287):
            bad=deepcopy(self.report);r=bad['cases'][0]['finish_vertex']['second_heap'];raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_report(bad)
        self.refuse([lambda c:c['finish_vertex']['state']['foreign_maps'].pop(),
            lambda c:c['device_cleanup'].update(second_font_vertex_buffer_release_count=1)])
