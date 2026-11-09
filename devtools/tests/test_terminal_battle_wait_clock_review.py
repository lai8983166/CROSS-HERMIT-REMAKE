import copy
import struct
import unittest
from unittest.mock import patch
from devtools import terminal_battle_wait_clock_review as c


class RawClockComparisonTests(unittest.TestCase):
    def row(self,ns,ticks):
        a=bytearray(80);b=bytearray(80)
        struct.pack_into('<q',a,16,ns);struct.pack_into('<q',b,16,ticks)
        return dict(index=1,ns=ns,record_header_hex=a.hex(),payload_hex='01020304'),dict(index=1,qpc_ticks=ticks,record_header_hex=b.hex(),payload_hex='01020304')

    def test_only_timestamp_bytes_may_differ(self):
        left,right=self.row(100000,100);c.bind_raw([left],[right])
        for key,value in [('payload_hex','01020305'),('index',2),('qpc_ticks',101)]:
            bad=dict(right,**{key:value})
            with self.assertRaises(ValueError):c.bind_raw([left],[bad])
        h=bytearray.fromhex(right['record_header_hex']);h[10]=1
        with self.assertRaises(ValueError):c.bind_raw([left],[dict(right,record_header_hex=h.hex())])

    def test_raw_sequence_cannot_be_truncated_or_reordered(self):
        a,b=self.row(100000,100);x,y=self.row(100001,99)
        with self.assertRaises(ValueError):c.bind_raw([a,x],[b])
        with self.assertRaises(ValueError):c.bind_raw([a,x],[b,y])

    def rows(self):
        return [dict(qpc_ticks=10,opcode=51),dict(qpc_ticks=20,opcode=36,data=dict(OldThreadId=7,NewThreadId=8)),
                dict(qpc_ticks=80,opcode=36,data=dict(OldThreadId=8,NewThreadId=7)),dict(qpc_ticks=90,opcode=52)]

    def test_complete_interval_and_cross_cpu_one_tick_guard(self):
        rows=self.rows()
        self.assertTrue(c.interval_check(rows,(0,3),7,22,78,'qpc_ticks',1))
        for lo,hi in [(20,70),(21,70),(22,79),(22,80),(15,85),(22,91)]:
            self.assertFalse(c.interval_check(rows,(0,3),7,lo,hi,'qpc_ticks',1))

    def test_middle_switch_cannot_be_bridged(self):
        rows=self.rows();rows[2:2]=[dict(qpc_ticks=40,opcode=36,data=dict(OldThreadId=8,NewThreadId=7)),dict(qpc_ticks=50,opcode=36,data=dict(OldThreadId=7,NewThreadId=8))]
        self.assertFalse(c.interval_check(rows,(0,5),7,25,75,'qpc_ticks',1))

    def test_raw_report_ETL_subject_and_count_must_match(self):
        sid=dict(bytes=123,sha256='source');eid=dict(bytes=456,sha256='etl');subject=dict(pid=12,tid=7)
        source=dict(ETL=eid,subject=subject)
        report=dict(source=sid,ETL=eid,retained_subject_records=1,total_records=10)
        artifact=dict(source=sid,ETL=eid,subject=subject,records=[{}])
        c.bind_reader_artifact(source,sid,report,artifact)
        for change in (lambda r,a:r['ETL'].update(sha256='other'),
                       lambda r,a:r.update(retained_subject_records=2),
                       lambda r,a:a['subject'].update(tid=8)):
            r,a=copy.deepcopy(report),copy.deepcopy(artifact);change(r,a)
            with self.assertRaises(ValueError):c.bind_reader_artifact(source,sid,r,a)

    def comparison_fixture(self):
        raw=self.rows()
        for i,row in enumerate(raw):row['index']=i
        raw[0]['data']=dict(SysCallAddress=123);raw[-1]['data']=dict(SysCallNtStatus=0)
        utc=[dict(row,ns=row['qpc_ticks'])for row in raw]
        timing=dict(clock_reads=[dict(qpc_before=22,qpc_after=23,UTC_ns=22),dict(qpc_before=77,qpc_after=78,UTC_ns=78)],
            data_interval_qpc=[22,78],includes_original_context_acquisition=False,
            context_acquired_while_same_handles_suspended=True,TLS_calls=[dict(qpc_begin=25,qpc_end=70,completed=True,
                selector_query=dict(qpc_begin=30,qpc_end=60,result=1))])
        source=dict(subject=dict(tid=7),kernel_wait_export=dict(target=123),window_snapshots=[dict(snapshot_begin_ns=22,snapshot_end_ns=78,timing_diagnostic=timing)])
        return source,utc,raw,[(0,3)],[dict(supported_Nt_context=True,wait_frame_bp=100)]

    def test_no_zip_truncation_or_changed_same_pending_semantics(self):
        args=self.comparison_fixture()
        with patch.object(c,'bind_raw'):
            self.assertTrue(c.compare(*args)[0]['raw_QPC_strict_single_off_interval'])
            with self.assertRaisesRegex(ValueError,'every original snapshot'):c.compare(*args[:-1],[])
            args[0]['window_snapshots'].append(copy.deepcopy(args[0]['window_snapshots'][0]))
            args[-1].append(dict(supported_Nt_context=True,wait_frame_bp=104))
            with self.assertRaisesRegex(ValueError,'same pending syscall'):c.compare(*args)

    def test_incomplete_or_outside_TLS_timing_rejected(self):
        for change in (lambda t:t['TLS_calls'][0].update(completed=False),
                       lambda t:t['TLS_calls'][0].update(qpc_end=79),
                       lambda t:t['TLS_calls'][0]['selector_query'].update(result=0)):
            args=self.comparison_fixture();change(args[0]['window_snapshots'][0]['timing_diagnostic'])
            with patch.object(c,'bind_raw'),self.assertRaisesRegex(ValueError,'TLS/selector timing'):c.compare(*args)

    def test_bool_float_and_unordered_clock_fields_rejected(self):
        changes=[lambda t:t['clock_reads'][0].update(qpc_before=True),
                 lambda t:t['clock_reads'][0].update(qpc_after=23.0),
                 lambda t:t['clock_reads'][1].update(qpc_before=21),
                 lambda t:t['TLS_calls'][0]['selector_query'].update(result=True),
                 lambda t:t['TLS_calls'][0]['selector_query'].update(qpc_begin=61,qpc_end=60)]
        for change in changes:
            args=self.comparison_fixture();change(args[0]['window_snapshots'][0]['timing_diagnostic'])
            with patch.object(c,'bind_raw'),self.assertRaises(ValueError):c.compare(*args)


if __name__=='__main__':unittest.main()
