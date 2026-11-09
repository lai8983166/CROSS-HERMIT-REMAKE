"""Pure contracts only. No Windows APIs, subprocess, VM, ETW or game calls."""
import copy
import ctypes as C
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

from devtools import terminal_wait_etw_probe as p


class FakeAPI:
    def __init__(self, start=0, stops=(0,)):
        self.start_status = start; self.stops = list(stops); self.calls = []

    def StartTraceW(self, handle, name, properties):
        self.calls.append(('start', name))
        if not self.start_status:
            handle._obj.value = 123
        return self.start_status

    def ControlTraceW(self, handle, name, properties, operation):
        self.calls.append(('stop', handle, name, operation))
        properties._obj.BuffersWritten = 2
        return self.stops.pop(0)


def fixture_data():
    helper = dict(pid=42, tid=77, error=None, closed=[True, True], rows=[
        dict(label='success', tid=77, begin_ns=10, end_ns=30, Win32_result=0, expected_NTSTATUS=0),
        dict(label='timeout', tid=77, begin_ns=40, end_ns=70, Win32_result=258, expected_NTSTATUS=258)])
    events = [dict(guid=p.THREAD_GUID, opcode=36, ns=1, pid=0, tid=0, cpu=0,
                   data={'NewThreadId': '77', 'OldThreadId': '4'})]
    for op, stamp, data in ((51, 11, {'SysCallAddress': '0xffff0123'}),
                            (52, 29, {'SysCallNtStatus': '0x0'}),
                            (51, 41, {'SysCallAddress': '0xffff0123'}),
                            (52, 69, {'SysCallNtStatus': '0x102'})):
        events.append(dict(guid=p.PERF_GUID, opcode=op, ns=stamp,
                           pid=42, tid=77, cpu=0, data=data))
    stats = dict(EventsLost=0, LogBuffersLost=0, RealTimeBuffersLost=0)
    return events, helper, stats


class Ownership(unittest.TestCase):
    def test_layout_and_budgets(self):
        buf, props = p.properties(Path('C:/ChaomofaWorker/project/analysis/new/trace.etl'))
        self.assertEqual(C.sizeof(p.PROPERTIES), 120)
        self.assertEqual((props.MaximumFileSize, props.LogFileMode, props.EnableFlags), (4, 1, 0x97))
        self.assertEqual((props.BufferSize, props.MaximumBuffers, props.Wnode.ClientContext), (64, 8, 1))

    def test_existing_logger_never_stopped(self):
        api = FakeAPI(start=183); session = p.Session(api, Path('unused.etl'))
        with self.assertRaisesRegex(ValueError, '183'):
            session.start()
        session.stop()
        self.assertEqual(api.calls, [('start', p.LOGGER)])

    def test_privilege_failure_never_stopped(self):
        api = FakeAPI(start=5); session = p.Session(api, Path('unused.etl'))
        with self.assertRaises(ValueError):
            session.start()
        session.stop()
        self.assertEqual(len(api.calls), 1)

    def test_only_acquired_handle_stopped_once(self):
        api = FakeAPI(); session = p.Session(api, Path('unused.etl'))
        session.start(); result = session.stop(); session.stop()
        self.assertEqual(api.calls[-1], ('stop', 123, p.LOGGER, 1))
        self.assertEqual(len(api.calls), 2)
        self.assertEqual(result['statistics']['EventsLost'], 0)

    def test_failed_stop_retains_ownership_for_final_retry(self):
        api = FakeAPI(stops=(5, 0)); session = p.Session(api, Path('unused.etl'))
        session.start(); session.stop()
        self.assertTrue(session.owned)
        result = session.stop()
        self.assertFalse(session.owned)
        self.assertEqual(result['stop_attempts'], [5, 0])


class Pairing(unittest.TestCase):
    def test_header_tid_and_real_status_pairing(self):
        events, helper, stats = fixture_data()
        result = p.analyze_events(events, helper, stats)
        self.assertTrue(result['capability_observed'])
        self.assertEqual([r['NTSTATUS'] for r in result['selected_pairs']], [0, 258])
        self.assertFalse(result['accepted'])
        self.assertFalse(result['kernel_symbol_identity_verified'])

    def test_missing_header_tid_uses_actual_cswitch(self):
        events, helper, stats = fixture_data()
        for event in events[1:]: event.update(tid=0xffffffff, pid=0xffffffff)
        result = p.analyze_events(events, helper, stats)
        self.assertEqual(result['selected_pairs'][0]['entry_tid_method'], 'CSwitch_current_thread')

    def test_no_cswitch_tid_inference_is_not_invented(self):
        events, helper, stats = fixture_data()
        for event in events[1:]: event.update(tid=0xffffffff, pid=0xffffffff, cpu=None)
        with self.assertRaisesRegex(ValueError, 'no unique'):
            p.analyze_events(events, helper, stats)

    def test_each_lost_counter_fails(self):
        for field in ('EventsLost', 'LogBuffersLost', 'RealTimeBuffersLost'):
            events, helper, stats = fixture_data(); stats[field] = 1
            with self.assertRaisesRegex(ValueError, 'loss counters'):
                p.analyze_events(events, helper, stats)

    def test_missing_loss_counter_fails(self):
        events, helper, stats = fixture_data(); del stats['EventsLost']
        with self.assertRaises(ValueError): p.analyze_events(events, helper, stats)

    def test_wrong_return_and_wrong_address_fail(self):
        for data in ({'SysCallNtStatus': '0'}, {'SysCallNtStatus': '0x103'}):
            events, helper, stats = fixture_data(); events[-1]['data'] = data
            with self.assertRaises(ValueError): p.analyze_events(events, helper, stats)
        events, helper, stats = fixture_data(); events[-2]['data']['SysCallAddress'] = '0xffff2222'
        with self.assertRaises(ValueError): p.analyze_events(events, helper, stats)

    def test_ambiguous_success_fails(self):
        events, helper, stats = fixture_data()
        extra = copy.deepcopy(events[1:3]); extra[0]['ns'] = 15; extra[1]['ns'] = 20
        events[2]['ns'] = 14
        events[3:3] = extra
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            p.analyze_events(events, helper, stats)

    def test_tid_conflict_and_nonmonotonic_fail(self):
        events, helper, stats = fixture_data(); events[1]['tid'] = 78
        with self.assertRaisesRegex(ValueError, 'conflict'): p.analyze_events(events, helper, stats)
        events, helper, stats = fixture_data(); events[-1]['ns'] = 20
        with self.assertRaisesRegex(ValueError, 'monotonic'): p.analyze_events(events, helper, stats)

    def test_helper_wrong_result_and_interval_fail(self):
        events, helper, stats = fixture_data(); helper['rows'][1]['Win32_result'] = 0
        with self.assertRaisesRegex(ValueError, 'actual helper'): p.analyze_events(events, helper, stats)
        events, helper, stats = fixture_data(); helper['rows'][1]['begin_ns'] = 90
        with self.assertRaisesRegex(ValueError, 'time window'): p.analyze_events(events, helper, stats)

    def test_overlap_diagnostic_keeps_strict_rejection(self):
        events, helper, stats = fixture_data()
        overlapping = copy.deepcopy(events[1]); overlapping['ns'] = 12
        events.insert(2, overlapping)
        diagnostic = {}
        with self.assertRaisesRegex(ValueError, 'overlapping/unclosed'):
            p.analyze_events(events, helper, stats, diagnostic)
        self.assertEqual(diagnostic['prior_open']['ns'], 11)
        self.assertEqual(diagnostic['current_event']['ns'], 12)
        self.assertEqual(diagnostic['current_inside_fixture'], ['success'])
        self.assertTrue(diagnostic['strict_rejection_preserved'])
        self.assertEqual(diagnostic['CPU_current_threads'], {0: 77})
        self.assertLessEqual(len(p.json.dumps(diagnostic,separators=(',',':')).encode()),8192)

    def test_overlap_outside_fixture_explicit(self):
        events, helper, stats = fixture_data()
        events[1]['ns'] = 2
        overlapping = copy.deepcopy(events[1]); overlapping['ns'] = 3
        events.insert(2, overlapping)
        diagnostic = {}
        with self.assertRaisesRegex(ValueError, 'overlapping/unclosed'):
            p.analyze_events(events, helper, stats, diagnostic)
        self.assertEqual(diagnostic['current_inside_fixture'], [])
        self.assertEqual(diagnostic['completed_target_pairs'], 0)


class Decoder(unittest.TestCase):
    def test_real_schema_shape_and_100ns_precision(self):
        xml = '''<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
        <System><Provider Guid="{ce1dbfb4-137e-4da6-87b0-3f59aa102cbc}"/>
        <Opcode>52</Opcode><TimeCreated SystemTime="2026-11-09T01:02:03.1234567Z"/>
        <Execution ProcessID="42" ThreadID="77" ProcessorID="0"/></System>
        <EventData><Data Name="SysCallNtStatus">0x102</Data></EventData></Event>'''
        row = p.decode_event(ET.fromstring(xml))
        self.assertEqual(row['ns'] % 10**9, 123456700)
        self.assertEqual(p.number(row['data']['SysCallNtStatus']), 258)
        self.assertEqual(row['tid'], 77)

    def test_other_provider_not_accepted_as_systemcall(self):
        xml = '<Event><System><Provider Guid="{123}"/><Opcode>52</Opcode></System></Event>'
        self.assertIsNone(p.decode_event(ET.fromstring(xml)))

    def test_named_classic_userdata(self):
        xml = '''<Event><System><Provider Guid="{ce1dbfb4-137e-4da6-87b0-3f59aa102cbc}"/>
        <Opcode>51</Opcode><TimeCreated SystemTime="2026-11-09T01:02:03Z"/>
        <Execution ProcessID="42" ThreadID="77" ProcessorNumber="1"/></System>
        <UserData><SysClEnter><SysCallAddress>0xffff0123</SysCallAddress></SysClEnter></UserData></Event>'''
        row = p.decode_event(ET.fromstring(xml))
        self.assertEqual(p.number(row['data']['SysCallAddress']), 0xffff0123)
        self.assertEqual(row['cpu'], 1)

    def test_dtd_rejected_on_F_only(self):
        folder = p.ROOT / '.venv-audit/native-worker/tmp'
        folder.mkdir(exist_ok=True, parents=True)
        with tempfile.TemporaryDirectory(dir=folder) as directory:
            path = Path(directory) / 'test.xml'; path.write_bytes(b'<!DOCTYPE e [<!ENTITY a "x">]><Events/>')
            with self.assertRaisesRegex(ValueError, 'DTD'):
                list(p.read_events(path))


class NativeDecoderContracts(unittest.TestCase):
    def test_sizes_offsets(self):
        sizes = p.decoder_layout()
        self.assertEqual((sizes['EVENT_RECORD'], sizes['LOGFILE'], sizes['LOG_HEADER']), (112, 448, 280))
        self.assertEqual(p.LOGFILE.EventRecordCallback.offset, 424)
        self.assertEqual(p.EVENT_RECORD.UserData.offset, 96)

    def test_actual_retained_source_binding_and_tampering(self):
        # Only a small committed-shape fixture is synthesized; no native APIs.
        buf, props = p.properties()
        props.BuffersWritten = 2
        stats = {k: int(getattr(props, k)) for k in (
            'EventsLost', 'LogBuffersLost', 'RealTimeBuffersLost', 'BuffersWritten', 'NumberOfBuffers')}
        _, helper, _ = fixture_data()
        source = dict(kind='owned_ETW_capability_fixture', helper=helper,
            helper_ready=dict(pid=42, tid=77), helper_exit=0, cleanup=dict(owned_helper_forced=False),
            trace=dict(start_status=0, stop_status=0, stopped=True, statistics=stats,
                returned_stop_properties_hex=bytes(props).hex()),
            artifacts=[dict(path='C:/source/trace.etl', bytes=1024, sha256='abc')])
        ident = dict(bytes=1024, sha256='abc')
        p.validate_decode_source(source, ident)
        with self.assertRaisesRegex(ValueError, 'exact artifact'):
            p.validate_decode_source(source, dict(bytes=1024, sha256='wrong'))
        bad = copy.deepcopy(source); bad['trace']['statistics']['EventsLost'] = 1
        with self.assertRaisesRegex(ValueError, 'lost events'):
            p.validate_decode_source(bad, ident)
        bad = copy.deepcopy(source); bad['trace']['statistics']['BuffersWritten'] = 3
        with self.assertRaisesRegex(ValueError, 'original bytes'):
            p.validate_decode_source(bad, ident)

    def test_header_time_and_cpu_cross_binding(self):
        start = 134386769891524074
        _, helper, _ = fixture_data()
        for row in helper['rows']:
            row['begin_ns'] += p.filetime_ns(start)
            row['end_ns'] += p.filetime_ns(start)
        source = dict(helper=helper, qualification=dict(current_guest_resources=dict(logical_processors=2)),
                      trace=dict(statistics=dict(BuffersWritten=57)))
        header = dict(StartTime=start, EndTime=start+100, NumberOfProcessors=2,
                      PointerSize=8, PerfFreq=10000000, EventsLost=0, BuffersLost=0, BuffersWritten=57)
        p.validate_log_header(header, source)
        bad = dict(header, StartTime=start+600000000, EndTime=start+600000100)
        with self.assertRaisesRegex(ValueError, 'no tolerance'):
            p.validate_log_header(bad, source)
        with self.assertRaisesRegex(ValueError, 'processor'):
            p.validate_log_header(dict(header, NumberOfProcessors=4), source)
        with self.assertRaisesRegex(ValueError, 'converted FILETIME'):
            p.filetime_ns(12345)

    def test_qualification_precedes_decoder_WinAPI(self):
        with mock.patch.object(p, 'qualify', side_effect=RuntimeError('not guest')):
            with mock.patch.object(p.C, 'WinDLL') as win:
                with self.assertRaisesRegex(RuntimeError, 'not guest'):
                    p.decode_only(Path('x'), 'a', Path('y'), 'b', Path('z'))
                win.assert_not_called()

    def test_callback_error_cancels_and_closes_only_owned_reader(self):
        class Function:
            def __init__(self, fn): self.fn = fn
            def __call__(self, *args): return self.fn(*args)
        class API:
            def __init__(self):
                self.closed = []; self.log = None; self.buffer_result = None
                self.OpenTraceW = Function(self.open)
                self.ProcessTrace = Function(self.process)
                self.CloseTrace = Function(lambda handle: self.closed.append(handle) or 0)
            def open(self, ptr):
                self.log = ptr._obj; h = self.log.LogfileHeader
                h.StartTime = 116444736000000000; h.EndTime = h.StartTime+100
                h.NumberOfProcessors = 2; h.PointerSize = 8; h.PerfFreq = 10000000; h.BuffersWritten = 1
                return 123
            def process(self, handles, count, start, end):
                self.asserted_handles = (handles[0], count, start, end)
                record = p.EVENT_RECORD(); h = record.EventHeader
                h.ProviderId[:] = p.uuid.UUID(p.SYSTEM_GUID).bytes_le
                h.EventDescriptor.Opcode = 51; h.TimeStamp = 116444736000000000
                callback = C.WINFUNCTYPE(None, C.POINTER(p.EVENT_RECORD))(self.log.EventRecordCallback)
                callback(C.byref(record))
                buffer = C.WINFUNCTYPE(C.c_uint32, C.POINTER(p.LOGFILE))(self.log.BufferCallback)
                self.log.BuffersRead = 1
                self.buffer_result = buffer(C.byref(self.log))
                return 1223
        api = API()
        tdh = type('TDH', (), {})()
        tdh.TdhGetEventInformation = Function(lambda *args: 5)
        tdh.TdhGetPropertySize = Function(lambda *args: 5)
        tdh.TdhGetProperty = Function(lambda *args: 5)
        _, helper, _ = fixture_data()
        source = dict(helper=helper, qualification=dict(current_guest_resources=dict(logical_processors=2)),
                      trace=dict(statistics=dict(BuffersWritten=1)))
        result = {}
        with mock.patch.object(p.C, 'WinDLL', side_effect=[api, tdh]):
            with self.assertRaisesRegex(ValueError, 'complete ProcessTrace failed'):
                p._decode_etl(Path('synthetic.etl'), source, result, p.time.monotonic()+10)
        self.assertEqual(api.asserted_handles, (123, 1, None, None))
        self.assertEqual(api.buffer_result, 0)
        self.assertEqual(api.closed, [123])
        self.assertTrue(result['callback_errors'])
        self.assertEqual(result['close_trace_status'], 0)


class RetainedWaitWindows(unittest.TestCase):
    def source(self):
        artifact = p.ROOT / 'analysis/terminal-wait-etw-decode-v2-20261109.helper.json.gz'
        raw = artifact.read_bytes()
        self.assertEqual(p.hashlib.sha256(raw).hexdigest(),
                         'f43c9cee281e55e7ab4f1b93de421d48562eadf63ab67b06fc1fc25cc0f6e54a')
        source = p.json.loads(p.gzip.decompress(raw))
        # Small contract projection; the generated proof separately pins the
        # complete original decode report, ETL and frozen decoder implementation.
        report = dict(status='blocked', errors=["ValueError('overlapping/unclosed target syscall')"],
            process_trace_status=0, close_trace_status=0, callback_errors=[], ETL=source['ETL'],
            retained_helper_records=511, helper_thread_bindings=[dict(pid=2112,tid=1168)])
        return source, report

    def test_actual_two_windows_and_original_global_failure(self):
        source, report = self.source()
        proof = p.verify_wait_window_records(source, report)
        self.assertEqual([w['global_indices'] for w in proof['windows']],
                         [[5867,5868,5956,5957],[5962,5963,6403,6404]])
        self.assertEqual([w['NTSTATUS'] for w in proof['windows']], [0,258])
        self.assertEqual(proof['observed_prefix_ledger']['final_balance'], 1)
        self.assertEqual(len(proof['observed_prefix_ledger']['overlap_entries']), 7)
        self.assertEqual(proof['original_global_status'], 'blocked')
        self.assertFalse(proof['fullglobalpairing'])
        with self.assertRaisesRegex(ValueError,'overlapping/unclosed'):
            p.analyze_events(source['records'], source['helper'],
                dict(EventsLost=0,LogBuffersLost=0,RealTimeBuffersLost=0))

    def test_cannot_resign_global_success(self):
        source, report = self.source(); report['status'] = 'capability_observed'
        with self.assertRaisesRegex(ValueError,'retain original'):
            p.verify_wait_window_records(source,report)

    def test_no_window_event_can_be_discarded(self):
        source, report = self.source(); del source['records'][28]
        report['retained_helper_records'] -= 1
        with self.assertRaises(ValueError): p.verify_wait_window_records(source,report)

    def test_raw_return_and_raw_cpu_tampering_fail(self):
        source, report = self.source(); source['records'][34]['payload_hex'] = '00000000'
        with self.assertRaisesRegex(ValueError,'exit payload'):
            p.verify_wait_window_records(source,report)
        source, report = self.source(); source['records'][30]['buffer_context_hex'] = '0000ffff'
        with self.assertRaisesRegex(ValueError,'actual CPU'):
            p.verify_wait_window_records(source,report)

    def test_decoded_and_raw_return_both_wrong_still_fail(self):
        source, report = self.source(); source['records'][34]['payload_hex'] = '00000000'
        source['records'][34]['data']['SysCallNtStatus'] = 0
        with self.assertRaisesRegex(ValueError,'true NT return'):
            p.verify_wait_window_records(source,report)

    def test_no_time_tolerance_and_no_wrong_etl(self):
        source, report = self.source(); source['helper']['rows'][0]['begin_ns'] = source['records'][27]['ns']+1
        with self.assertRaisesRegex(ValueError,'exactly four'):
            p.verify_wait_window_records(source,report)
        source, report = self.source(); report['ETL'] = dict(report['ETL'],sha256='wrong')
        with self.assertRaisesRegex(ValueError,'same complete ETL'):
            p.verify_wait_window_records(source,report)


if __name__ == '__main__':
    unittest.main()
