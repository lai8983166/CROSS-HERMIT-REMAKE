import json
import unittest
from copy import deepcopy
from tools.school_font_caller import ROOT,HEADS,ARENA
from tools.school_font_caller_verification import verify_report,verify_case,source_runs
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((ROOT/'analysis/school-font-caller-trajectory-v3-20261019.json').read_text(encoding='utf8'))

    def refuse(self,phase,changes):
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                c=deepcopy(self.report['font_report']['cases'][0]);f(c['caller_'+phase])
                with self.assertRaises(ValueError):verify_case(c)


class BindingTests(Base):
    def test_original_success_branch_real_owner_device_and_natural_ABI(self):
        self.assertTrue(verify_report(self.report)['manager_bound'])
        self.refuse('bind',[lambda r:r['entries'][0]['args'].__setitem__(0,0),
            lambda r:r['entries'][1].update(receiver=0),lambda r:r['returns'][0].update(eax=0),
            lambda r:r['cpu'].update(ESP=r['cpu']['ESP']-4),lambda r:r['before_cpu'].update(EAX=1),
            lambda r:r['instruction_runs'].pop(0),lambda r:r['native_writes']['manager'].update(count=1)])

    def test_complete_owner_prior_fonts_and_owned_interface_maps_preserved(self):
        for key,offset in (('state',0x1058),('state',0x1090),('second_heap',4096+0x670)):
            c=deepcopy(self.report['font_report']['cases'][0]);r=c['caller_bind']
            b=r['state']['owner'] if key=='state' else r[key]
            raw=bytearray(unpack(b));raw[offset]^=1;b.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_case(c)
        self.refuse('bind',[lambda r:r['state']['foreign_maps'].pop(),lambda r:r.update(manager_bound=False),
            lambda r:r['state'].update(SEH=1)])


class QueueTests(Base):
    def test_two_exact_CRT_responses_full_native_zeroing_and_return(self):
        self.assertEqual(verify_report(self.report)['queue_payload_bytes'],1081344)
        self.refuse('queues',[lambda r:r['allocations'][0]['args'].__setitem__(0,32767),
            lambda r:r['allocations'][1].update(pointer=HEADS),lambda r:r['allocations'][1].update(initial_byte=0),
            lambda r:r['native_writes']['arena'].update(count=262143),lambda r:r['state'].update(image_sha256='00'*32),
            lambda r:r['returns'][-1].update(eax=1),lambda r:r['entries'][4]['args'].__setitem__(2,32764),
            lambda r:r['instruction_runs'][next(i for i,x in enumerate(r['instruction_runs']) if x['va']==0x56CF01)].update(count=1)])

    def test_rehashed_queue_bytes_guards_and_unowned_writes_refused(self):
        import base64,zlib
        for index,offset in ((0,4096),(0,0),(1,4096+1048575),(1,1056767)):
            c=deepcopy(self.report['font_report']['cases'][0]);r=c['caller_queues']['queues'][index]['buffer']
            raw=bytearray(zlib.decompress(base64.b64decode(r['zlib_base64'])));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_case(c)
        from tools.school_font_caller_emulation import CallerEmulator,OWNER,COUNTER
        e=CallerEmulator.__new__(CallerEmulator);e.caller_running=True;e.caller_phase='bind';e.caller_writes={}
        for at in (HEADS,ARENA,COUNTER,OWNER+0x1090,OWNER+0xB408,0):
            with self.assertRaises(RuntimeError):e._write(None,None,at,4,0,None)


class GammaTests(Base):
    def test_all768_original_gamma_stores_and_exact_unexecuted_call(self):
        self.assertEqual(verify_report(self.report)['gamma_entries'],768)
        self.assertEqual(sum(x['count'] for x in source_runs('gamma')),5470)
        self.refuse('gamma',[lambda r:r['pending']['args'].__setitem__(1,0),lambda r:r['pending'].update(method_offset=76),
            lambda r:r['pending'].update(target_read_executed=True),lambda r:r['native_writes']['gamma'].update(count=767),
            lambda r:r['instruction_runs'].pop(-1),lambda r:r['cpu'].update(ESI=0),
            lambda r:r.update(gamma_device_call_executed=True),lambda r:r.update(full413450_returned=True)])

    def test_rehashed_gamma_channels_and_parent_prefix_authority_refused(self):
        for offset in (0xB408,0xB608,0xBA07,0xBA08):
            c=deepcopy(self.report['font_report']['cases'][0]);r=c['caller_gamma']['state']['owner']
            raw=bytearray(unpack(r));raw[offset]^=1;r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError):verify_case(c)
        bad=deepcopy(self.report);bad['font_report']['cases'][0]['finish_return']['cpu']['ESP']-=4
        with self.assertRaises(ValueError):verify_report(bad)
        bad=deepcopy(self.report);bad['retained_VM_advanced']=True
        with self.assertRaises(ValueError):verify_report(bad)


class TrajectoryTests(Base):
    def test_fresh_two_case_same_CPU_and_helpers_through_all_boundaries(self):
        from tools.school_font_caller_emulation import generate
        result=verify_report(generate());self.assertEqual(result['cases'],2);self.assertEqual(result['stop'],'0x416cfa')
