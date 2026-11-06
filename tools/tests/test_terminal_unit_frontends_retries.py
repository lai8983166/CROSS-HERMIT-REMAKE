"""Match the captured REP retry pattern while rejecting unpaired observations."""
import copy
import struct
import unittest

from unicorn import x86_const as x86
from tools.tests.test_terminal_unit_frontends_trace import Mini
from tools import terminal_unit_frontends_trace as trace
from tools.terminal_unit_frontends_retries import RepReplay


class RepRetryTests(unittest.TestCase):
    def fixture(self,count=4,stop_ecx=None):
        class StopMini(Mini):
            def code(self,uc,pc,size,context):
                if (stop_ecx is not None and pc==RepReplay.REP
                        and uc.reg_read(x86.UC_X86_REG_ECX)==stop_ecx):
                    r=self.recorder
                    if r is not None and not r.begin_code(pc):return
                    try:uc.emu_stop()
                    finally:
                        if r is not None:r.end_code(pc)
                    return
                super().code(uc,pc,size,context)
        machine=StopMini()
        machine.uc.mem_map(0x56C000,4096)
        machine.uc.mem_write(RepReplay.REP,b'\xF3\xAB\xC3')
        machine.uc.reg_write(x86.UC_X86_REG_ECX,count)
        machine.uc.reg_write(x86.UC_X86_REG_EDI,0x403000)
        machine.uc.reg_write(x86.UC_X86_REG_EAX,0xCDCDCDCD)
        recorder=trace.Recorder(machine);machine.recorder=recorder
        try:
            machine.uc.emu_start(RepReplay.REP,0x404000 if stop_ecx is None else 0)
            report=recorder.finish()
        finally:recorder.detach()
        code=bytearray(0x170000)
        for row in report['initial_memory']:
            at=row['pointer']-0x400000
            code[at:at+row['bytes']]=bytes.fromhex(row['hex'])
        return report,bytes(code)

    def replay(self,kind='normal',count=4,stop_ecx=None):
        report,code=self.fixture(count,stop_ecx)
        class Probe(RepReplay):
            injected=False
            def code(self,uc,pc,size,context):
                if (kind!='normal' and not self.injected and pc==self.REP
                        and uc.reg_read(x86.UC_X86_REG_ECX)==3):
                    self.injected=True
                    super().code(uc,pc,size,context)
                    p=uc.reg_read(x86.UC_X86_REG_EDI)
                    value=uc.reg_read(x86.UC_X86_REG_EAX)
                    if kind!='no_store':
                        self.write(uc,0,p,4,value,None)
                        if kind not in ('aborted_retry','missing_commit'):
                            uc.mem_write(p,struct.pack('<I',value))
                    if kind=='missing_commit':
                        super().code(uc,pc,size,context)
                        self.write(uc,0,p,4,value,None)
                        uc.reg_write(x86.UC_X86_REG_ECX,2)
                        uc.reg_write(x86.UC_X86_REG_EDI,p+4)
                    if kind=='unrelated_RAM':uc.mem_write(p,b'bad!')
                    if kind=='changed_CPU':uc.reg_write(x86.UC_X86_REG_EBX,1)
                    if kind=='boundary':self.rep_boundary=None
                super().code(uc,pc,size,context)
        replay=Probe(report,code,[(RepReplay.REP,RepReplay.REP+3)],
            lambda *a:None,lambda *a:None,lambda *a:None,
            heap_owner=lambda p,n:kind!='unowned' and 0x403000<=p and p+n<=0x404000)
        return replay,report

    def test_real_advancing_rep_and_zero_count_keep_every_observation(self):
        for count in (0,1,4):
            replay,report=self.replay(count=count)
            result=replay.run()
            self.assertEqual(result['final_trace'],report['final_trace'])
            self.assertEqual(result['raw_original_callback_trace'],report['final_trace'])
            self.assertEqual(result['REP_callback_retries'],[])

    def test_same_architectural_attempt_has_one_canonical_store(self):
        replay,report=self.replay('retry')
        result=replay.run()
        self.assertEqual(result['final_trace'],report['final_trace'])
        raw=result['raw_original_callback_trace']
        self.assertEqual(raw['instructions'],report['final_trace']['instructions']+1)
        self.assertEqual(raw['writes'],report['final_trace']['writes']+1)
        self.assertEqual(len(result['REP_callback_retries']),1)
        self.assertFalse(result['raw_trace_matches_source'])

    def test_aborted_attempt_must_commit_when_the_retry_advances(self):
        replay,report=self.replay('aborted_retry')
        result=replay.run()
        self.assertEqual(result['final_trace'],report['final_trace'])
        retry=result['REP_callback_retries'][0]
        self.assertEqual(retry['memory_before'],retry['memory_before_retry'])

    def test_unrelated_memory_change_is_rejected(self):
        replay,_=self.replay('unrelated_RAM')
        with self.assertRaises(ValueError):replay.run()

    def test_register_progress_without_a_committed_store_is_rejected(self):
        replay,_=self.replay('missing_commit')
        with self.assertRaises(ValueError):replay.run()

    def test_missing_store_cannot_be_normalized(self):
        replay,_=self.replay('no_store')
        with self.assertRaises(ValueError):replay.run()

    def test_changed_architectural_register_cannot_be_normalized(self):
        replay,_=self.replay('changed_CPU')
        with self.assertRaises(ValueError):replay.run()

    def test_retry_cannot_cross_a_host_boundary(self):
        replay,_=self.replay('boundary')
        with self.assertRaises(ValueError):replay.run()

    def test_unowned_ram_never_qualifies_for_normalization(self):
        replay,_=self.replay('unowned')
        with self.assertRaises(ValueError):replay.run()

    def test_raw_retry_limit_is_independent_of_canonical_instruction_count(self):
        replay,_=self.replay('retry')
        replay.MAX_RETRIES=0
        with self.assertRaisesRegex(ValueError,'raw REP retry budget'):replay.run()

    def test_actual_owned_return_stops_without_executing_its_stub(self):
        report,code=self.fixture()
        report['transactions'][0]['end']=0
        def make(data):
            return RepReplay(data,code,[(RepReplay.REP,RepReplay.REP+3)],
                lambda *a:None,lambda *a:None,lambda *a:None,
                heap_owner=lambda p,n:0x403000<=p and p+n<=0x404000,
                quiescent_return=0x404000)
        result=make(report).run()
        self.assertEqual([r['transaction'] for r in result['implicit_owned_RETURN_stops']],[0])
        for kind in ('CPU','RAM','end','events'):
            bad=copy.deepcopy(report)
            if kind=='CPU':bad['transactions'][0]['after_CPU']['EAX']=1
            elif kind=='RAM':bad['transactions'][0]['after_memory']['sha256']='0'*64
            elif kind=='end':bad['transactions'][0]['end']=0x405000
            else:bad['transactions'][0]['events']=[dict(pc=0x402000,stop=False,
                continues_guest=True,effects=[],CPU_changes={})]
            with self.subTest(kind=kind),self.assertRaises(ValueError):make(bad).run()

    def test_pure_loop_stop_matches_its_original_pc_and_cumulative_ordinal(self):
        report,code=self.fixture(stop_ecx=2)
        def make(data):
            return RepReplay(data,code,[(RepReplay.REP,RepReplay.REP+3)],
                lambda *a:None,lambda *a:None,lambda *a:None,
                heap_owner=lambda p,n:0x403000<=p and p+n<=0x404000)
        result=make(report).run()
        self.assertEqual(result['final_trace'],report['final_trace'])
        self.assertEqual(result['deferred_earlier_stop_PC_hits'],2)
        for kind in ('ordinal','PC','digest'):
            bad=copy.deepcopy(report)
            if kind=='ordinal':bad['transactions'][0]['after_trace']['instructions']-=1
            elif kind=='PC':bad['transactions'][0]['events'][-1]['pc']+=2
            else:bad['transactions'][0]['after_trace']['code_sha256']='0'*64
            with self.subTest(kind=kind),self.assertRaises(ValueError):make(bad).run()

    def test_aborted_iteration_commits_before_a_coincident_stop(self):
        replay,report=self.replay('aborted_retry',stop_ecx=2)
        result=replay.run()
        self.assertEqual(result['final_trace'],report['final_trace'])
        self.assertEqual(len(result['REP_callback_retries']),1)
        self.assertEqual(result['raw_original_callback_trace']['writes'],report['final_trace']['writes']+1)
