import json
import unittest
from copy import deepcopy
from tools.school_startup_return import ROOT
from tools.school_startup_return_verification import verify_report,verify_return_case
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-startup-return-trajectory-v1-20261019.json').read_text(encoding='utf8'))

    def refuse(self,changes):
        for n,change in enumerate(changes):
            with self.subTest(change=n):
                c=deepcopy(self.report['cases'][0]);change(c)
                device=next(r['result']['device'] for r in c['device']['native']['live_results'] if r['op']=='create_device' and r['result'].get('device'))
                with self.assertRaises(ValueError):verify_return_case(c,device)


class GammaTests(Base):
    def test_late_owned_method_preserves_CPU_and_actual_void_call_returns_on_original_stack(self):
        self.assertTrue(verify_report(self.report)['original416CC0_returned'])
        self.refuse([lambda c:c['gamma_admission']['cpu'].update(EIP=0),
            lambda c:c['gamma_admission']['inspection']['result']['device']['methods'].update({'72':1}),
            lambda c:c['gamma_admission'].update(stack_after_sha256='00'*32),
            lambda c:c['startup_gamma']['api_calls'][0]['args'].__setitem__(1,0),
            lambda c:c['startup_gamma']['api_calls'][0]['result'].update(hr=0),
            lambda c:c['startup_gamma']['api_calls'][0]['result'].update(eax_is_status=True),
            lambda c:c['startup_gamma']['api_calls'][0]['result'].update(forwarder_hex='90'*25),
            lambda c:c['startup_gamma']['api_calls'][0]['result'].update(forwarder_freed=False),
            lambda c:c['startup_gamma']['returns'][-1].update(sp=0)])

    def test_rehashed_full_owner_font_queue_pixels_and_source_trace_corruption_refused(self):
        for key,offset in (('state',0xB408),('second_heap',4096+0x670)):
            c=deepcopy(self.report['cases'][0]);row=c['startup_gamma'];r=row['state']['owner'] if key=='state' else row[key]
            raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            device=next(r['result']['device'] for r in c['device']['native']['live_results'] if r['op']=='create_device' and r['result'].get('device'))
            with self.assertRaises(ValueError):verify_return_case(c,device)
        self.refuse([lambda c:c['gamma_admission']['state']['foreign_maps'].pop(),
            lambda c:c['startup_gamma']['instruction_trace'].remove(0x416D14),
            lambda c:c['startup_gamma']['api_calls'][0]['result']['inspection'].update(native_requested=True),
            lambda c:c['startup_gamma']['api_calls'][0]['result'].update(input_after_hex='00'*1536),
            lambda c:c['startup_gamma']['queues'][0].update(pointer=0),
            lambda c:c['startup_gamma']['external_regions'].pop(),
            lambda c:c['startup_gamma'].update(full413450_returned=True)])


class ReturnTests(Base):
    def test_original_success0_ret20_saved_registers_and_exact_final_CPU(self):
        self.assertEqual(verify_report(self.report)['startup_stack_cleanup'],20)
        self.refuse([lambda c:c['startup_return']['cpu'].update(EAX=1),lambda c:c['startup_return']['cpu'].update(EBP=0),
            lambda c:c['startup_return']['cpu'].update(ESP=c['startup_return']['cpu']['ESP']-20),
            lambda c:c['startup_return']['cpu'].update(EDI=0),lambda c:c['startup_return']['returns'][-1].update(return_va='0x413546'),
            lambda c:c['startup_return']['instruction_trace'].remove(0x413546),
            lambda c:c['startup_return'].update(upstream_caller_executed=True),lambda c:c['startup_return']['state'].update(SEH=1)])

    def test_honest_new_helper_old_prefix_cleanup_and_remaining_VM_boundaries_refused(self):
        for change in (lambda r:r['device_build'].update(helper_sha256='00'*32),
                lambda r:r['cases'][0]['caller_queues']['cpu'].update(EAX=1),
                lambda r:r['cases'][0]['finish_return']['loop_locals'].update(index=1),
                lambda r:r['cases'][0]['device_cleanup'].update(gamma_device_restored=False),
                lambda r:r['cases'][0]['device_cleanup'].update(gamma_DCs_released=0),
                lambda r:r['cases'][0]['device_cleanup'].update(gamma_desktop_restored=False),
                lambda r:r.update(retained_VM_advanced=True)):
            bad=deepcopy(self.report);change(bad)
            with self.assertRaises(ValueError):verify_report(bad)


class TrajectoryTests(Base):
    def test_fresh_two_case_same_helpers_complete_original_startup_return(self):
        from tools.school_startup_return_emulation import generate
        result=verify_report(generate());self.assertTrue(result['original413450_returned']);self.assertEqual(result['startup_result'],0)
