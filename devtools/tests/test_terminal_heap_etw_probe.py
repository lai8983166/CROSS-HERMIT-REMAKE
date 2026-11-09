import copy
import ctypes as C
import struct
import unittest
import uuid
from unittest.mock import patch
from pathlib import Path
from devtools import terminal_heap_etw_probe as p


def fixture():
    ready=dict(stage='ready',pid=123,tid=456,pointer_size=4,wow64=True,filetime=10)
    live=dict(stage='live',pid=123,tid=456,heap=0x1000,freed_address=0x2000,live_address=0x3000,
              freed_size=152,live_size=296,free_result=True,live_not_freed=True,begin_filetime=20,end_filetime=60)
    closed=dict(stage='closed',live_free_result=True,heap_destroy_result=True,begin_filetime=70,end_filetime=80)
    source=dict(helper=dict(ready=ready,live=live,closed=closed));rows=[]
    for op,address,size,t in ((33,0x2000,152,30),(33,0x3000,296,40),(36,0x2000,None,50)):
        h=bytearray(80);h[4:6]=struct.pack('<H',0x20);h[8:16]=struct.pack('<II',456,123);h[16:24]=struct.pack('<q',t)
        h[24:40]=uuid.UUID(p.HEAP_GUID).bytes_le;h[45]=op
        payload=struct.pack('<4I',0x1000,size,address,3)if op==33 else struct.pack('<3I',0x1000,address,3)
        rows.append(dict(header_hex=h.hex(),payload_hex=payload.hex(),pid=123,tid=456,filetime=t,opcode=op,
                         data=p.parse_heap(op,0x20,0,payload)))
    return source,rows


class HeapProbeTests(unittest.TestCase):
    def test_extension_matches_pinned_word_encoding(self):
        b=p.extension_bytes(123);self.assertEqual(struct.unpack('<6I',b),(0x20006,0x20002,123,0x30003,0x1021,0x1024))
        for bad in (0,-1,True,2**32):
            with self.assertRaises(ValueError):p.extension_bytes(bad)

    def test_properties_are_pid_only_sequential_and_bounded(self):
        b,x=p.properties('ChaomofaOwnedHeap-test','C:/analysis/trace.etl',123)
        off=x.EnableFlags&0xffff
        self.assertEqual(bytes(b)[off:off+24],p.extension_bytes(123));self.assertEqual(x.MaximumFileSize,4)
        self.assertEqual(x.LogFileMode,1);self.assertEqual(bytes(x.Wnode.Guid),uuid.UUID(p.HEAP_GUID).bytes_le)

    def test_valid_free_and_kept_live_counterexample(self):
        s,rows=fixture();r=p.analyze_matches(rows,s)
        self.assertTrue(r['two_allocations_and_one_free_observed']);self.assertFalse(r['event_HeapFree_BOOL_present'])

    def test_live_free_duplicate_or_missing_record_rejected(self):
        s,rows=fixture()
        for bad in (rows[:-1],rows+[rows[-1]]):
            with self.assertRaises(ValueError):p.analyze_matches(bad,s)
        rows[-1]['data']['address']=s['helper']['live']['live_address']
        with self.assertRaises(ValueError):p.analyze_matches(rows,s)

    def test_raw_owner_timestamp_and_opcode_tamper_rejected(self):
        for offset in (8,12,16,45):
            s,rows=fixture();h=bytearray.fromhex(rows[0]['header_hex']);h[offset]^=1;rows[0]['header_hex']=h.hex()
            with self.assertRaises(ValueError):p.analyze_matches(rows,s)

    def test_schema_and_pointer_width_fail_closed(self):
        for flags,version,payload in ((0,0,b'0'*16),(0x60,0,b'0'*16),(0x20,1,b'0'*16),(0x20,0,b'0'*15)):
            with self.assertRaises(ValueError):p.parse_heap(33,flags,version,payload)

    def test_source_pid_extension_and_raw_loss_are_bound(self):
        s,rows=fixture();b,props=p.properties('ChaomofaOwnedHeap-test','C:/analysis/a.etl',123)
        stop=p.abi.PROPERTIES()
        s.update(kind='owned_WOW64_PID_heap_ETW_capability',accepted=False,original_game=False,fullABI=False,PTDcleanup=False,
                 helper_exit=0,elapsed_seconds=1,registry_modified=False,IFEO_modified=False,global_kernel_logger_used=False,
                 process_memory_written=False,cleanup=dict(logger_still_owned=False),
                 trace=dict(start_status=0,stop_status=0,owned=True,pid=123,requested_properties_hex=bytes(b).hex(),
                    returned_stop_properties_hex=bytes(stop).hex(),statistics=dict(EventsLost=0,LogBuffersLost=0,RealTimeBuffersLost=0),
                    start_begin_filetime=11,start_end_filetime=19,stop_attempts=[0],stop_intervals=[dict(begin_filetime=61,end_filetime=69)]))
        p.check_capture_source(s)
        bad=copy.deepcopy(s);raw=bytearray.fromhex(bad['trace']['requested_properties_hex']);raw[(props.EnableFlags&0xffff)+8]^=1
        bad['trace']['requested_properties_hex']=raw.hex()
        with self.assertRaises(ValueError):p.check_capture_source(bad)
        bad=copy.deepcopy(s);stop.EventsLost=1;bad['trace']['returned_stop_properties_hex']=bytes(stop).hex()
        with self.assertRaises(ValueError):p.check_capture_source(bad)
        bad=copy.deepcopy(s);bad['trace']['stop_intervals'][0]['end_filetime']=71
        with self.assertRaises(ValueError):p.check_capture_source(bad)

    def test_failed_kill_does_not_block_reading_stderr_or_erase_failure(self):
        class Stream:
            def write(self,*args):raise OSError('pipe failed')
            def read(self,*args):raise AssertionError('must not block reading live helper')
            def close(self):raise AssertionError('must not close locked live reader')
        class Process:
            stdin=stdout=stderr=Stream();returncode=None
            def poll(self):return None
            def kill(self):raise OSError('kill failed')
        result=dict(cleanup={},errors=[],status='captured_decode_required')
        p.cleanup_helper(Process(),result)
        self.assertEqual(result['status'],'blocked');self.assertEqual(len(result['errors']),2)
        self.assertTrue(result['cleanup']['helper_forced'])

    def test_receipts_cannot_claim_other_thread_or_unordered_time(self):
        s,rows=fixture();s['helper']['live']['tid']+=1
        with self.assertRaises(ValueError):p.analyze_matches(rows,s)
        s,rows=fixture();s['helper']['closed']['begin_filetime']=30
        with self.assertRaises(ValueError):p.analyze_matches(rows,s)

    def test_guest_rejection_precedes_any_creation_or_api(self):
        with patch.object(p,'qualified',side_effect=ValueError('host forbidden')),patch.object(p,'dependencies')as dep:
            with self.assertRaisesRegex(ValueError,'host forbidden'):p.run(Path('never-created.json'))
            dep.assert_not_called()

    def test_failed_start_never_stops_existing_logger(self):
        class API:
            def StartTraceW(self,*args):return 183
            def ControlTraceW(self,*args):raise AssertionError('unowned stop')
        session=p.Session(API(),'ChaomofaOwnedHeap-test',Path('C:/analysis/a.etl'),123)
        with self.assertRaises(ValueError):session.start()
        session.stop();self.assertFalse(session.owned)

    def test_owned_stop_uses_exact_acquired_handle_and_name(self):
        calls=[]
        class API:
            def StartTraceW(self,h,name,props):C.cast(h,C.POINTER(C.c_uint64))[0]=77;return 0
            def ControlTraceW(self,h,name,props,control):calls.append((h,name,control));return 0
        session=p.Session(API(),'ChaomofaOwnedHeap-test',Path('C:/analysis/a.etl'),123)
        session.start();session.stop();session.stop()
        self.assertEqual(calls,[(77,'ChaomofaOwnedHeap-test',1)]);self.assertFalse(session.owned)


if __name__=='__main__':unittest.main()
