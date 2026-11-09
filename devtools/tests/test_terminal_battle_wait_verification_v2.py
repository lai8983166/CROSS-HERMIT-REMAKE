import copy
import ctypes as C
import unittest
from devtools.terminal_menu_input import packet
from devtools.terminal_battle_wait_verification_v2 import verify_precise_submissions,trace_boundary


class InitialTraceBoundaryTests(unittest.TestCase):
    def fixture(self):
        rows=[dict(opcode=36,ns=10,data=dict(OldThreadId=7,NewThreadId=8)),
              dict(opcode=36,ns=40,data=dict(OldThreadId=8,NewThreadId=7)),
              dict(opcode=51,ns=50,data={}),dict(opcode=52,ns=60,data={})]
        return rows,dict(initial_unpaired_exits=[],final_unpaired_entry=None),dict(subject=dict(tid=7),capture_interval=dict(begin_ns=1))

    def test_only_pre_entry_raw_switched_out_prefix_is_unproven_boundary(self):
        rows,ledger,source=self.fixture()
        self.assertEqual(trace_boundary(ledger,20,30,rows,source),'initial_before_first_recorded_syscall')
        self.assertIsNone(trace_boundary(ledger,55,56,rows,source))

    def test_crossing_entry_missing_switch_or_before_trace_is_not_excluded(self):
        for bounds in ((20,51),(9,20),(0,5),(41,45)):
            rows,ledger,source=self.fixture()
            with self.subTest(bounds=bounds):self.assertIsNone(trace_boundary(ledger,*bounds,rows,source))
        rows,ledger,source=self.fixture();rows[1]['data']['NewThreadId']=9
        self.assertIsNone(trace_boundary(ledger,20,30,rows,source))

    def test_existing_exit_or_internal_syscall_does_not_use_new_boundary(self):
        rows,ledger,source=self.fixture();rows.insert(1,dict(opcode=52,ns=15,data={}))
        self.assertIsNone(trace_boundary(ledger,20,30,rows,source))
        rows,ledger,source=self.fixture();rows[2]['opcode']=52
        self.assertIsNone(trace_boundary(ledger,20,30,rows,source))


class PreciseSubmissionTests(unittest.TestCase):
    def fixture(self):
        rows=[]
        for flags,start in ((2,110),(4,220)):
            p=packet(flags=flags)
            rows.append(dict(type=0,flags=flags,packet_hex=C.string_at(C.byref(p),C.sizeof(p)).hex(),
                begin_ns=start,end_ns=start+10,result=1,error=None))
        return dict(precise_input_submissions=rows,start_trigger='second_left_button_down_query',
                    start_trigger_ns=90,capture_interval=dict(begin_ns=100)),dict(moves=[],down_result=1,up_results=[1])

    def test_precise_original_submissions_pass_without_rewriting_coarse_clock(self):
        source,action=self.fixture()
        action.update(down_wall_time_ns=95,up_wall_time_ns=250)
        original=copy.deepcopy(action)
        self.assertFalse(verify_precise_submissions(source,action)['original_coarse_timestamps_modified'])
        self.assertEqual(action,original)

    def test_submissions_before_trace_overlap_wrong_packet_or_retry_rejected(self):
        for kind in ('before','overlap','packet','retry','result'):
            source,action=self.fixture();rows=source['precise_input_submissions']
            if kind=='before':rows[0]['begin_ns']=99
            if kind=='overlap':rows[0]['end_ns']=rows[1]['begin_ns']
            if kind=='packet':rows[0]['flags']=4
            if kind=='retry':rows.append(copy.deepcopy(rows[-1]))
            if kind=='result':rows[0]['result']=0
            with self.subTest(kind=kind),self.assertRaises(ValueError):verify_precise_submissions(source,action)


if __name__=='__main__':unittest.main()
