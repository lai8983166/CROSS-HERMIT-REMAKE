"""Pure bounded contracts; no VM, Windows API, ETW logger or input calls."""
import copy
from pathlib import Path
import struct
import time
import unittest
from unittest.mock import patch
from devtools import terminal_battle_wait_verification as v
from devtools import terminal_battle_wait_etl as reader
from devtools.tests.test_terminal_original_wait_etw_verification import sample,event


def window_source():
    s,_,_=sample();s.update(kind='battle_wait_result_window',phase='startup_preflight',
        trace_limits=dict(reader.LIMITS),ETL_limit=reader.ETL_LIMIT,maximum_snapshots=768,
        observer_thread_duplicate_closed=True,before=s['owner_snapshots']['before'],
        window_snapshots=[s['owner_snapshots']['observed_wait']])
    p=v.etw.PROPERTIES.from_buffer_copy(bytes.fromhex(s['trace']['requested_properties_hex']))
    p.MaximumFileSize=64;p.MinimumBuffers=4;s['trace']['requested_properties_hex']=bytes(p).hex()
    return s


def cycles(n=3):
    s=window_source();rows=[];proofs=[];tid=s['subject']['tid'];address=s['kernel_wait_export']['target']
    for i in range(n):
        offset=i*30000;base=i*10
        rows.extend([event(base+1,offset+5000,36,0,dict(NewThreadId=tid,OldThreadId=9),9),
            event(base+2,offset+8000,51,0,dict(SysCallAddress=address),tid),
            event(base+3,offset+9000,36,0,dict(NewThreadId=9,OldThreadId=tid),tid),
            event(base+4,offset+12000,36,1,dict(NewThreadId=tid,OldThreadId=10),10),
            event(base+5,offset+13000,52,1,dict(SysCallNtStatus=0),tid),
            event(base+6,offset+20000,36,1,dict(NewThreadId=10,OldThreadId=tid),tid)])
        proofs.append(dict(supported_Nt_context=True,snapshot_interval=[offset+10000,offset+11000],
            wait_return_site=0x50a030,wait_frame_bp=0x100200,caller_frame_bp=0x100300,result_locals={}))
    return s,rows,proofs


class BudgetAndSource(unittest.TestCase):
    def test_explicit_64MiB_contract_not_old_fixture_limits(self):
        s=window_source();self.assertTrue(v.source_contract(s,s['ETL'])['strict_source_cleanup_verified'])
        self.assertEqual((reader.ETL_LIMIT,reader.MAX_BUFFERS,reader.MAX_SELECTED,reader.DECODE_SECONDS),
                         (64*1024*1024,1024,16384,180))
        reader.decoder_layout()

    def test_budget_source_and_raw_configuration_must_both_match(self):
        for change in (lambda s:s['trace_limits'].update(maximum_file_mib=4),
                       lambda s:s.update(trace_flags=0x97),lambda s:s.update(observer_thread_duplicate_closed=False),
                       lambda s:s['trace']['statistics'].update(EventsLost=1)):
            s=window_source();change(s)
            with self.assertRaises(ValueError):v.source_contract(s,s['ETL'])
        s=window_source();raw=bytearray.fromhex(s['trace']['requested_properties_hex']);struct.pack_into('<I',raw,60,4)
        s['trace']['requested_properties_hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'64 MiB'):v.source_contract(s,s['ETL'])

    def test_qualification_precedes_native_reader(self):
        with patch.object(reader.frozen,'qualify',side_effect=ValueError('unqualified')):
            with self.assertRaisesRegex(ValueError,'unqualified'):
                reader.decode_etl(Path('unused'),{}, {},time.monotonic()+180,lambda x:None)


class UniqueActualPairs(unittest.TestCase):
    def test_three_distinct_pairs_not_snapshot_count(self):
        s,rows,proofs=cycles();proofs.insert(1,copy.deepcopy(proofs[0]))
        groups,ledger,boundaries,unsupported=v.pair_snapshots(s,rows,proofs)
        self.assertEqual(len(groups),3);self.assertEqual(groups[0]['snapshot_indices'],[0,1])
        self.assertEqual(ledger['closed_calls'],3);self.assertEqual(boundaries,[]);self.assertEqual(unsupported,[])
        s,rows,proofs=cycles(2);proofs.extend(copy.deepcopy(proofs))
        with self.assertRaisesRegex(ValueError,'three distinct'):v.pair_snapshots(s,rows,proofs)

    def test_changed_pending_frame_not_silently_deduplicated(self):
        s,rows,proofs=cycles();extra=copy.deepcopy(proofs[0]);extra['wait_return_site']=0x453cb5;proofs.append(extra)
        with self.assertRaisesRegex(ValueError,'cannot change'):v.pair_snapshots(s,rows,proofs)

    def test_initial_and_final_partial_waits_remain_explicit(self):
        s,rows,proofs=cycles();rows.insert(1,event(2,6000,52,0,dict(SysCallNtStatus=0),77))
        first=copy.deepcopy(proofs[0]);first['snapshot_interval']=[5500,5600];proofs.insert(0,first)
        rows.extend([event(90,85000,36,0,dict(NewThreadId=77,OldThreadId=9),9),
                     event(91,88000,51,0,dict(SysCallAddress=s['kernel_wait_export']['target']),77),
                     event(92,89000,36,0,dict(NewThreadId=9,OldThreadId=77),77)])
        last=copy.deepcopy(first);last['snapshot_interval']=[90000,91000];proofs.append(last)
        for i,row in enumerate(rows):row['index']=i+1
        groups,ledger,boundaries,_=v.pair_snapshots(s,rows,proofs)
        self.assertEqual(len(groups),3)
        self.assertEqual([x['reason'] for x in boundaries],['initial_partial','final_partial'])
        self.assertFalse(ledger['full_global_pairing'])

    def test_unexplained_missing_pair_or_inside_overlap_fails(self):
        s,rows,proofs=cycles();proofs[0]['snapshot_interval']=[21000,22000]
        with self.assertRaisesRegex(ValueError,'boundary explanation'):v.pair_snapshots(s,rows,proofs)
        s,rows,proofs=cycles();rows.insert(2,event(3,8500,51,0,dict(SysCallAddress=123),77))
        with self.assertRaisesRegex(ValueError,'overlapping'):v.pair_snapshots(s,rows,proofs)

    def test_raw_payload_CPU_and_return_status_stay_bound(self):
        for change in (lambda r:r[1].update(payload_hex='00'*8),lambda r:r[1].update(decoder_cpu_tid_before=88),
                       lambda r:r[1].update(ns=8100)):
            s,rows,proofs=cycles();change(rows)
            with self.assertRaises(ValueError):v.pair_snapshots(s,rows,proofs)
        s,rows,proofs=cycles();rows[4]=event(5,13000,52,1,dict(SysCallNtStatus=258),77)
        with self.assertRaisesRegex(ValueError,'successful kernel'):v.pair_snapshots(s,rows,proofs)

    def test_sample_must_be_inside_actual_switch_out_interval(self):
        s,rows,proofs=cycles();proofs[0]['snapshot_interval']=[8500,8600]
        with self.assertRaisesRegex(ValueError,'switch-out interval'):v.pair_snapshots(s,rows,proofs)

    def test_larger_explicit_record_limit_is_real_and_bounded(self):
        s,rows,_=cycles(700);self.assertGreater(len(rows),4096)
        pairs,_=v.validate_records(rows,s['subject'],2);self.assertEqual(len(pairs),700)
        with self.assertRaisesRegex(ValueError,'bounded complete'):v.validate_records([rows[0]]*16385,s['subject'],2)


class ResultEndpoints(unittest.TestCase):
    def group(self,site,counter=None,result=1):
        return dict(semantic=dict(wait_return_site=site,tail_counter=counter,
                                 result_locals=dict(inner_result=result,callback_result=result)))

    def test_sparse_samples_do_not_prove_missing_waits_or_recording(self):
        result=v.endpoint_coverage([self.group(0x453cb5),self.group(0x453cdd),self.group(0x451758,9)])
        self.assertFalse(result['post_result_three_wait_endpoints_observed'])
        self.assertFalse(result['ten_distinct_tail_waits_observed'])
        self.assertFalse(result['recording_call_execution_verified'])
        self.assertFalse(result['continuous_instruction_result_consumption_verified'])

    def test_three_waits_and_ten_counters_are_observed_only_when_present(self):
        groups=[self.group(x) for x in (0x453cb5,0x453cd3,0x453cdd)]
        groups.extend(self.group(0x451758,i) for i in range(10));groups.append(self.group(0x451796,10))
        result=v.endpoint_coverage(groups)
        self.assertTrue(result['post_result_three_wait_endpoints_observed']);self.assertTrue(result['ten_distinct_tail_waits_observed'])
        self.assertTrue(result['callback_nonzero_consumption_endpoint_observed'])
        self.assertFalse(result['recording_file_effects_verified'])
        with self.assertRaisesRegex(ValueError,'two different'):v.endpoint_coverage(groups+[self.group(0x451758,9)])


if __name__=='__main__':unittest.main()
