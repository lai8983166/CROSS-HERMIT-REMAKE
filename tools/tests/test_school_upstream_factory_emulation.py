import json
import unittest
from copy import deepcopy
from tools.school_upstream_factory import ROOT,OUTPUT,OWNER_BYTES
from tools.school_upstream_factory_verification import verify_report,verify_case
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'analysis/school-upstream-factory-trajectory-v2-20261019.json').read_text(encoding='utf8'))

    def refuse(self,phase,changes,index=0):
        for n,change in enumerate(changes):
            with self.subTest(change=n):
                c=deepcopy(self.report['cases'][index]);change(c[phase])
                with self.assertRaises(ValueError):verify_case(c)


class AllocationTests(Base):
    def test_both_actual_roots_exact_CRT_parent_stack_and_native_counter(self):
        self.assertEqual(verify_report(self.report)['actual_factory_owner_allocations'],4)
        self.refuse('allocation',[lambda r:r['allocations'][0]['args'].__setitem__(0,OWNER_BYTES-1),
            lambda r:r['allocations'][0].update(initial_byte=0),lambda r:r['native']['entries'][0]['args'].__setitem__(1,0),
            lambda r:r['native']['returns'][-1].update(return_va='0x22000000'),
            lambda r:r['native']['cpu'].update(ESP=0),lambda r:r['state'].update(SEH=0),
            lambda r:r['state'].update(image_sha256='00'*32),lambda r:r['instruction_runs'][0].update(count=2)])

    def test_rehashed_complete_allocation_output_guards_and_unowned_writes_refused(self):
        for key,offset in (('guarded_owner',0),('guarded_owner',4096),('guarded_owner',4096+OWNER_BYTES),('guarded_output',4096),('guarded_output',12287)):
            c=deepcopy(self.report['cases'][0]);r=c['allocation'][key];raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_case(c)
        from tools.school_upstream_factory_emulation import FactoryEmulator,OWNER,COUNTER
        e=FactoryEmulator.__new__(FactoryEmulator);e.factory_running=True;e.factory_phase='allocation'
        for at in (OWNER,OUTPUT,0x80A398,0x7A4A00):
            with self.assertRaises(RuntimeError):e._write(None,None,at,4,0,None)


class ConstructorTests(Base):
    def test_original42_nested_calls_and_live_DC_timers_on_each_parent_frame(self):
        self.assertEqual(verify_report(self.report)['original_constructor_calls_per_case'],42)
        self.refuse('constructor',[lambda r:r['native']['entries'][0].update(receiver=0),
            lambda r:r['native']['entries'][19]['args'].__setitem__(2,1),lambda r:r['native']['entries'].pop(),
            lambda r:r['platform_calls'][1]['args'].__setitem__(0,0),lambda r:r['platform_calls'][0].update(sp=0),
            lambda r:r['native']['cpu'].update(EDI=0),lambda r:r['instruction_runs'].pop(),
            lambda r:r['pending'].update(return_va='0x44332211')])

    def test_full_owner_padding_image_SEH_and_owned_platform_cleanup_preserved(self):
        for offset in (0x1090,0xB1A4,0xB208,OWNER_BYTES):
            c=deepcopy(self.report['cases'][0]);r=c['constructor']['state']['owner'];raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_case(c)
        for change in (lambda c:c['platform_cleanup'].update(dcs_released=0),
                lambda c:c['platform_trace'][0]['reply'].update(id=0),
                lambda c:c['constructor']['state']['foreign_maps'].pop()):
            c=deepcopy(self.report['cases'][0]);change(c)
            with self.assertRaises(ValueError):verify_case(c)


class AdmissionTests(Base):
    def test_distinct_natural_child_entries_keep_actual_mode_and_missing_game_context(self):
        result=verify_report(self.report);self.assertEqual(result['window_stop'],'0x413450');self.assertEqual(result['game_stop'],'0x4500b0')
        self.refuse('admission',[lambda r:r['pending']['args'].__setitem__(1,0),lambda r:r['pending'].update(first_instruction_executed=True),
            lambda r:r['native']['cpu'].update(EDX=0),lambda r:r.update(factory_output_published=True)])
        self.refuse('admission',[lambda r:r['pending'].update(receiver=0),lambda r:r['pending']['args'].__setitem__(0,0),
            lambda r:r['inherited_missing_heaps'][1].update(mapped=True),lambda r:r.update(game_context_body_executed=True)],index=2)

    def test_inherited_cache_global_retention_remaining_authority_and_v1_metadata_refused(self):
        self.refuse('admission',[lambda r:r['inherited_missing_heaps'][0].update(pointer=0),
            lambda r:r['state'].update(image_sha256='00'*32),lambda r:r.update(original_device_startup_executed=True),
            lambda r:r.update(audio_COM_initialized=True),lambda r:r.update(retained_VM_advanced=True)])
        old=json.loads((ROOT/'analysis/school-upstream-factory-trajectory-v1-20261019.json').read_text())
        with self.assertRaises(ValueError):verify_report(old)
        bad=deepcopy(self.report);bad['platform_build']['helper_sha256']='00'*32
        with self.assertRaises(ValueError):verify_report(bad)


class TrajectoryTests(Base):
    def test_fresh_four_case_same_original_factory_CPU_through_all_three_boundaries(self):
        from tools.school_upstream_factory_emulation import generate
        result=verify_report(generate());self.assertEqual(result['cases'],4);self.assertFalse(result['factory_output_published'])
