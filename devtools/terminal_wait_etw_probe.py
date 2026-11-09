"""Guest-only, bounded ETW capability fixture; never starts or attaches to a game.

This tests kernel event availability, not original-game behavior or full ABI.
StartTrace owns NT Kernel Logger only on ERROR_SUCCESS. An existing logger is
never stopped, updated or reused. Unsupported privilege/schema is a blockage.
"""
import argparse
from collections import deque
import ctypes as C
import datetime as DT
import hashlib
import gzip
import json
import os
from pathlib import Path
import queue
import re
import struct
import subprocess
import sys
import threading
import time
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LOGGER = 'NT Kernel Logger'
ETL_LIMIT = 4 * 1024 * 1024
XML_LIMIT = 24 * 1024 * 1024
EVENT_LIMIT = 150000
WALL_SECONDS = 30
PERF_GUID = 'ce1dbfb4-137e-4da6-87b0-3f59aa102cbc'
THREAD_GUID = '3d6fa8d1-fe05-11d0-9dda-00c04fd7ba7c'
SYSTEM_GUID = '9e814aad-3204-11d2-9a82-006008a86939'
REFERENCES = [
    'https://learn.microsoft.com/en-us/windows/win32/etw/syscallenter',
    'https://learn.microsoft.com/en-us/windows/win32/etw/syscallexit',
    'https://learn.microsoft.com/en-us/windows/win32/etw/cswitch',
    'https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-starttracew',
    'https://learn.microsoft.com/en-us/windows/win32/etw/configuring-and-starting-the-nt-kernel-logger-session',
    'https://learn.microsoft.com/en-us/windows/win32/etw/logging-mode-constants',
    'https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tracerpt',
    'https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_logfilew',
    'https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-processtrace',
    'https://learn.microsoft.com/en-us/windows/win32/api/tdh/ns-tdh-trace_event_info',
    'https://learn.microsoft.com/en-us/windows/win32/api/tdh/nf-tdh-tdhgetproperty',
    'https://learn.microsoft.com/en-us/windows/win32/etw/thread-v2-typegroup1',
]


def need(value, message):
    if not value:
        raise ValueError(message)


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def number(value):
    s = str(value).strip()
    return int(s, 16 if s.lower().startswith('0x') else 10)


def utc_ns(value):
    match = re.fullmatch(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d{1,9}))?Z', value)
    need(match, 'unsupported tracerpt UTC timestamp: ' + value[:80])
    seconds = int(DT.datetime.fromisoformat(match[1]).replace(tzinfo=DT.timezone.utc).timestamp())
    return seconds * 10**9 + int((match[2] or '').ljust(9, '0'))


class WNODE(C.Structure):
    _fields_ = [('BufferSize', C.c_uint32), ('ProviderId', C.c_uint32),
                ('HistoricalContext', C.c_uint64), ('TimeStamp', C.c_int64),
                ('Guid', C.c_ubyte * 16), ('ClientContext', C.c_uint32), ('Flags', C.c_uint32)]


class PROPERTIES(C.Structure):
    _fields_ = [('Wnode', WNODE)] + [(n, C.c_uint32) for n in (
        'BufferSize', 'MinimumBuffers', 'MaximumBuffers', 'MaximumFileSize',
        'LogFileMode', 'FlushTimer', 'EnableFlags', 'AgeLimit', 'NumberOfBuffers',
        'FreeBuffers', 'EventsLost', 'BuffersWritten', 'LogBuffersLost', 'RealTimeBuffersLost')]
    _fields_ += [('LoggerThreadId', C.c_void_p), ('LogFileNameOffset', C.c_uint32),
                 ('LoggerNameOffset', C.c_uint32)]


def properties(path=None):
    """Explicit 64-bit Windows layout, UTF16 strings, bounded sequential file."""
    need(C.sizeof(C.c_void_p) == 8 and C.sizeof(WNODE) == 48 and C.sizeof(PROPERTIES) == 120,
         '64-bit ETW controller ABI required')
    buf = C.create_string_buffer(120 + 4096)
    p = PROPERTIES.from_buffer(buf)
    p.Wnode.BufferSize = len(buf)
    p.Wnode.Flags = 0x20000  # WNODE_FLAG_TRACED_GUID
    p.Wnode.Guid[:] = uuid.UUID(SYSTEM_GUID).bytes_le
    p.Wnode.ClientContext = 1  # QPC: recommended common clock for system loggers
    p.LoggerNameOffset = 120
    name = (LOGGER + '\0').encode('utf-16-le')
    C.memmove(C.addressof(buf) + 120, name, len(name))
    if path is not None:
        text = (str(path) + '\0').encode('utf-16-le')
        need(len(text) <= 2048, 'bounded ETL path')
        p.LogFileNameOffset = 120 + 2048
        C.memmove(C.addressof(buf) + p.LogFileNameOffset, text, len(text))
        p.BufferSize = 64
        p.MinimumBuffers = 4
        p.MaximumBuffers = 8  # <=512 KiB configured buffer pool
        p.MaximumFileSize = 4  # MiB; sequential logging stops at maximum
        p.LogFileMode = 1
        p.FlushTimer = 1
        p.EnableFlags = 0x97  # PROCESS | THREAD | IMAGE_LOAD | CSWITCH | SYSTEMCALL
    return buf, p


class Session:
    def __init__(self, advapi, path):
        self.api = advapi
        self.path = path
        self.handle = C.c_uint64()
        self.owned = False
        self.record = dict(logger=LOGGER, owned=False, start_status=None, stop_status=None)

    def start(self):
        buf, p = properties(self.path)
        self.record['requested_properties_hex'] = bytes(p).hex()
        status = int(self.api.StartTraceW(C.byref(self.handle), LOGGER, C.byref(p)))
        self.record['start_status'] = status
        if status == 0:
            self.owned = True
            self.record.update(owned=True, handle=self.handle.value)
        need(status == 0, 'StartTraceW status=' + str(status) + '; existing/denied logger never modified')

    def stop(self):
        if not self.owned:
            return self.record
        buf, p = properties()
        # The documented kernel-logger API requires KERNEL_LOGGER_NAME; retain
        # the exact acquired nonzero handle as well. Never stop after failed start.
        status = int(self.api.ControlTraceW(self.handle.value, LOGGER, C.byref(p), 1))
        self.record.setdefault('stop_attempts', []).append(status)
        self.record.update(stop_status=status, statistics={name: int(getattr(p, name)) for name in (
            'EventsLost', 'LogBuffersLost', 'RealTimeBuffersLost', 'BuffersWritten', 'NumberOfBuffers')})
        self.record['returned_stop_properties_hex'] = bytes(p).hex()
        # ERROR_MORE_DATA is documented as stopped; NOT_FOUND may be a full
        # sequential log. Neither supplies a successful complete statistics set.
        self.owned = status not in (0, 234, 4201)
        self.record['stopped'] = status == 0
        # Failed stops are explicit blockers, never silently called successful.
        return self.record


def qualify():
    from devtools.native_input_isolation import require_qualified_guest
    return require_qualified_guest()


def bind_windows():
    need(sys.platform == 'win32', 'Windows guest required')
    k = C.WinDLL('kernel32', use_last_error=True)
    signatures = {
        'GetCurrentThreadId': (C.c_uint32, []),
        'CreateEventW': (C.c_void_p, [C.c_void_p, C.c_int, C.c_int, C.c_wchar_p]),
        'SetEvent': (C.c_int, [C.c_void_p]),
        'WaitForSingleObject': (C.c_uint32, [C.c_void_p, C.c_uint32]),
        'CloseHandle': (C.c_int, [C.c_void_p]),
        'GetSystemTimePreciseAsFileTime': (None, [C.POINTER(C.c_uint64)]),
    }
    for name, (restype, args) in signatures.items():
        f = getattr(k, name); f.restype = restype; f.argtypes = args
    a = C.WinDLL('advapi32', use_last_error=True)
    a.StartTraceW.restype = a.ControlTraceW.restype = C.c_uint32
    a.StartTraceW.argtypes = [C.POINTER(C.c_uint64), C.c_wchar_p, C.POINTER(PROPERTIES)]
    a.ControlTraceW.argtypes = [C.c_uint64, C.c_wchar_p, C.POINTER(PROPERTIES), C.c_uint32]
    return k, a


def fixture():
    """Owned helper only: readiness before trace, two waits, all handles closed."""
    qualify()
    k, unused = bind_windows()
    tid = k.GetCurrentThreadId()
    events = [k.CreateEventW(None, False, False, None) for _ in range(2)]
    report = dict(pid=os.getpid(), tid=tid, rows=[], closed=[], error=None)
    def utc_now_ns():
        ticks = C.c_uint64()
        k.GetSystemTimePreciseAsFileTime(C.byref(ticks))
        return (ticks.value - 116444736000000000) * 100
    signal = None
    try:
        need(all(events), 'fixture CreateEventW error=' + str(C.get_last_error()))
        print(json.dumps(dict(ready=True, pid=os.getpid(), tid=tid)), flush=True)
        command = queue.Queue()
        threading.Thread(target=lambda: command.put(sys.stdin.buffer.readline(16)), daemon=True).start()
        need(command.get(timeout=10) == b'GO\n', 'owned controller GO required within ten seconds')
        signal_result = []
        def signal_later():
            time.sleep(.05)
            signal_result.append(bool(k.SetEvent(events[0])))
        signal = threading.Thread(target=signal_later, daemon=True)
        signal.start()
        for label, handle, timeout, expected in (
                ('success', events[0], 500, 0), ('timeout', events[1], 80, 258)):
            begin = utc_now_ns()
            value = k.WaitForSingleObject(handle, timeout)
            end = utc_now_ns()
            report['rows'].append(dict(label=label, begin_ns=begin, end_ns=end,
                timeout_ms=timeout, Win32_result=value, expected_NTSTATUS=expected,
                tid=tid, handle=int(handle)))
            need(value == expected, 'fixture wait result mismatch')
        signal.join(1)
        need(not signal.is_alive() and signal_result == [True], 'fixture signaling completed')
    except Exception as exc:
        report['error'] = repr(exc)
    finally:
        if signal is not None:
            signal.join(1)
        for handle in events:
            if handle:
                report['closed'].append(bool(k.CloseHandle(handle)))
    print(json.dumps(report), flush=True)
    return 1 if report['error'] or report['closed'] != [True, True] else 0


def local(tag):
    return tag.rsplit('}', 1)[-1]


def decode_event(element):
    """Only documented GUID/opcode/payload schemas; unfamiliar XML blocks."""
    system = next((x for x in element if local(x.tag) == 'System'), None)
    if system is None:
        return None
    fields = {local(x.tag): x for x in system}
    provider = fields.get('Provider')
    if provider is None:
        return None
    guid = provider.attrib.get('Guid', '').strip('{}').lower()
    if guid not in (PERF_GUID, THREAD_GUID):
        return None
    opcode = number(fields['Opcode'].text)
    if (guid, opcode) not in ((PERF_GUID, 51), (PERF_GUID, 52), (THREAD_GUID, 36)):
        return None
    execution = fields['Execution'].attrib
    data = {x.attrib['Name']: x.text for x in element.iter()
            if local(x.tag) == 'Data' and 'Name' in x.attrib}
    # Some tracerpt schema renderers use named UserData leaves instead.
    for x in element.iter():
        name = local(x.tag)
        if name in ('SysCallAddress', 'SysCallNtStatus', 'NewThreadId', 'OldThreadId'):
            need(name not in data or data[name] == x.text, 'conflicting ETW payload representations')
            data[name] = x.text
    timestamp = utc_ns(fields['TimeCreated'].attrib['SystemTime'])
    cpu = execution.get('ProcessorID', execution.get('ProcessorNumber'))
    return dict(guid=guid, opcode=opcode, ns=timestamp,
        tid=number(execution.get('ThreadID', '-1')), pid=number(execution.get('ProcessID', '-1')),
        cpu=number(cpu) if cpu is not None else None, data=data)


def analyze_events(events, helper, statistics, diagnostics=None):
    """Conservative syscall pairing, no invented TID or completion events."""
    need(helper['error'] is None and helper['closed'] == [True, True], 'owned helper failed cleanup/waits')
    need(all(statistics.get(k) == 0 for k in ('EventsLost', 'LogBuffersLost', 'RealTimeBuffersLost')),
         'all three ETW loss counters must be present and zero')
    tid = helper['tid']; pid = helper['pid']; cpu_current = {}; open_calls = {}
    pairs = []; unmatched = []; switches = 0; last_ns = -1
    history = deque(maxlen=16)
    def mismatch(message, current, prior=None):
        if diagnostics is not None and not diagnostics:
            compact = lambda x: {k: x[k] for k in ('index', 'opcode', 'ns', 'cpu', 'tid', 'pid', 'data',
                'decoder_cpu_tid_before') if k in x}
            diagnostic = dict(reason=message, current_event=current, prior_open=prior,
                CPU_current_threads=dict(cpu_current), last_selected_records=list(history),
                helper=dict(pid=pid, tid=tid), fixture_intervals=helper['rows'],
                current_inside_fixture=[r['label'] for r in helper['rows']
                    if r['begin_ns'] <= current['ns'] <= r['end_ns']],
                completed_target_pairs=len(pairs), unmatched_target_exits=len(unmatched),
                strict_rejection_preserved=True)
            diagnostic['last_selected_records'] = [compact(x) for x in history]
            while len(json.dumps(diagnostic,separators=(',',':')).encode()) > 8192 and diagnostic['last_selected_records']:
                diagnostic['last_selected_records'].pop(0)
            need(len(json.dumps(diagnostic,separators=(',',':')).encode()) <= 8192, 'bounded first mismatch diagnostic')
            diagnostics.update(diagnostic)
        raise ValueError(message)
    for e in events:
        history.append(e)
        if e['ns'] < last_ns:
            mismatch('kernel records not monotonic; no guessed reorder', e)
        last_ns = e['ns']; data = e['data']; cpu = e['cpu']
        if e['opcode'] == 36:
            switches += 1
            if cpu is not None:
                cpu_current[cpu] = number(data['NewThreadId'])
            continue
        event_tid = e['tid']
        if event_tid in (-1, 0, 0xffffffff):
            event_tid = cpu_current.get(cpu)
            method = 'CSwitch_current_thread'
        else:
            method = 'event_header'
            if cpu in cpu_current:
                if cpu_current[cpu] != event_tid:
                    mismatch('header/current-CPU TID conflict', e)
        if event_tid != tid:
            continue
        need(e['pid'] in (-1, 0, 0xffffffff, pid), 'target TID reused by another PID')
        if e['opcode'] == 51:
            if tid in open_calls:
                mismatch('overlapping/unclosed target syscall', e, open_calls[tid])
            open_calls[tid] = dict(ns=e['ns'], address=number(data['SysCallAddress']), method=method, event=e)
        else:
            before = open_calls.pop(tid, None)
            if before is None:
                unmatched.append(dict(kind='exit_without_entry', ns=e['ns']))
                continue
            pairs.append(dict(tid=tid, begin_ns=before['ns'], end_ns=e['ns'],
                syscall_address=before['address'], NTSTATUS=number(data['SysCallNtStatus']),
                entry_tid_method=before['method'], exit_tid_method=method))
    matches = []
    for row in helper['rows']:
        need(row['tid'] == tid and row['begin_ns'] <= row['end_ns'], 'fixture identity/time window')
        need(row['Win32_result'] == row['expected_NTSTATUS']
             and row['expected_NTSTATUS'] in (0, 258), 'actual helper success/timeout result')
        candidates = [p for p in pairs if row['begin_ns'] <= p['begin_ns'] <= p['end_ns'] <= row['end_ns']
                      and p['NTSTATUS'] == row['expected_NTSTATUS']]
        matches.append((row, candidates))
        need(not any(row['begin_ns'] <= x['ns'] <= row['end_ns'] for x in unmatched),
             'unpaired syscall inside fixture wait window')
    need([x[0]['label'] for x in matches] == ['success', 'timeout'], 'both fixture wait outcomes required')
    need(matches[0][0]['end_ns'] <= matches[1][0]['begin_ns'], 'ordered fixture wait intervals')
    need([x[0]['expected_NTSTATUS'] for x in matches] == [0, 258], 'success then timeout statuses')
    common = set(p['syscall_address'] for p in matches[0][1]) & set(p['syscall_address'] for p in matches[1][1])
    need(len(common) == 1 and 0 not in common, 'no unique common syscall address for both outcomes')
    address = next(iter(common)); selected = []
    for row, candidates in matches:
        candidates = [p for p in candidates if p['syscall_address'] == address]
        need(len(candidates) == 1, 'ambiguous target syscall in fixture interval')
        selected.append(dict(label=row['label'], **candidates[0]))
    need(switches > 0, 'CSwitch event capability absent')
    return dict(capability_observed=True, selected_pairs=selected, context_switch_records=switches,
        target_pairs=len(pairs), unmatched_target_exits=len(unmatched),
        correlation='unique same-address kernel syscall spans inside owned wait intervals',
        kernel_symbol_identity_verified=False, argument_handles_in_ETW=False,
        original_game_observed=False, full_ABI_verified=False, accepted=False)


def read_events(path):
    need(path.stat().st_size <= XML_LIMIT, 'bounded tracerpt XML exceeded')
    # Reject entities/DTD rather than expanding arbitrary XML declarations.
    with path.open('rb') as f:
        previous = b''
        for chunk in iter(lambda: f.read(65536), b''):
            scan = (previous + chunk).replace(b'\0', b'')
            need(b'<!DOCTYPE' not in scan and b'<!ENTITY' not in scan, 'DTD is not tracerpt event data')
            previous = scan[-32:]
    count = 0
    for event, element in ET.iterparse(path, events=('end',)):
        if local(element.tag) == 'Event':
            count += 1
            need(count <= EVENT_LIMIT, 'bounded decoded event count')
            row = decode_event(element)
            if row is not None:
                yield row
            element.clear()


# Offline EVENT_RECORD decoder. No logger control, game attachment, fixture or
# uncompressed XML is involved. Fixed-width fields avoid host wchar/long drift.
class DESCRIPTOR(C.Structure):
    _fields_ = [('Id', C.c_uint16), ('Version', C.c_uint8), ('Channel', C.c_uint8),
                ('Level', C.c_uint8), ('Opcode', C.c_uint8), ('Task', C.c_uint16),
                ('Keyword', C.c_uint64)]


class EVENT_HEADER(C.Structure):
    _fields_ = [('Size', C.c_uint16), ('HeaderType', C.c_uint16), ('Flags', C.c_uint16),
                ('EventProperty', C.c_uint16), ('ThreadId', C.c_uint32), ('ProcessId', C.c_uint32),
                ('TimeStamp', C.c_int64), ('ProviderId', C.c_ubyte * 16),
                ('EventDescriptor', DESCRIPTOR), ('ProcessorTime', C.c_uint64),
                ('ActivityId', C.c_ubyte * 16)]


class BUFFER_CONTEXT(C.Structure):
    _fields_ = [('ProcessorIndex', C.c_uint16), ('LoggerId', C.c_uint16)]


class EVENT_RECORD(C.Structure):
    _fields_ = [('EventHeader', EVENT_HEADER), ('BufferContext', BUFFER_CONTEXT),
                ('ExtendedDataCount', C.c_uint16), ('UserDataLength', C.c_uint16),
                ('ExtendedData', C.c_void_p), ('UserData', C.c_void_p), ('UserContext', C.c_void_p)]


class LEGACY_EVENT(C.Structure):
    _fields_ = [('Header', C.c_ubyte * 48), ('InstanceId', C.c_uint32),
                ('ParentInstanceId', C.c_uint32), ('ParentGuid', C.c_ubyte * 16),
                ('MofData', C.c_void_p), ('MofLength', C.c_uint32), ('ClientContext', C.c_uint32)]


class LOG_HEADER(C.Structure):
    _fields_ = [(n, C.c_uint32) for n in ('BufferSize', 'Version', 'ProviderVersion', 'NumberOfProcessors')]
    _fields_ += [('EndTime', C.c_int64)]
    _fields_ += [(n, C.c_uint32) for n in ('TimerResolution', 'MaximumFileSize', 'LogFileMode', 'BuffersWritten',
                                        'StartBuffers', 'PointerSize', 'EventsLost', 'CPUSpeed')]
    _fields_ += [('LoggerName', C.c_void_p), ('LogFileName', C.c_void_p), ('TimeZone', C.c_ubyte * 172),
                 ('BootTime', C.c_int64), ('PerfFreq', C.c_int64), ('StartTime', C.c_int64),
                 ('ReservedFlags', C.c_uint32), ('BuffersLost', C.c_uint32)]


class LOGFILE(C.Structure):
    _fields_ = [('LogFileName', C.c_wchar_p), ('LoggerName', C.c_wchar_p), ('CurrentTime', C.c_int64),
                ('BuffersRead', C.c_uint32), ('ProcessTraceMode', C.c_uint32), ('CurrentEvent', LEGACY_EVENT),
                ('LogfileHeader', LOG_HEADER), ('BufferCallback', C.c_void_p), ('BufferSize', C.c_uint32),
                ('Filled', C.c_uint32), ('EventsLost', C.c_uint32), ('EventRecordCallback', C.c_void_p),
                ('IsKernelTrace', C.c_uint32), ('Context', C.c_void_p)]


class PROPERTY_DESCRIPTOR(C.Structure):
    _fields_ = [('PropertyName', C.c_uint64), ('ArrayIndex', C.c_uint32), ('Reserved', C.c_uint32)]


def decoder_layout():
    checks = [(DESCRIPTOR, 16), (EVENT_HEADER, 80), (BUFFER_CONTEXT, 4), (EVENT_RECORD, 112),
              (LEGACY_EVENT, 88), (LOG_HEADER, 280), (LOGFILE, 448), (PROPERTY_DESCRIPTOR, 16)]
    need(C.sizeof(C.c_void_p) == 8 and all(C.sizeof(t) == n for t, n in checks), 'x64 ETW decoder ABI sizes')
    offsets = [(EVENT_RECORD.UserData, 96), (EVENT_HEADER.TimeStamp, 16), (EVENT_HEADER.EventDescriptor, 40),
               (LOG_HEADER.StartTime, 264), (LOG_HEADER.PerfFreq, 256), (LOGFILE.LogfileHeader, 120),
               (LOGFILE.BufferCallback, 400), (LOGFILE.EventRecordCallback, 424), (LOGFILE.Context, 440)]
    need(all(field.offset == value for field, value in offsets), 'x64 ETW decoder ABI offsets')
    return {t.__name__: n for t, n in checks}


def filetime_ns(ticks):
    need(type(ticks) is int and ticks >= 116444736000000000, 'ProcessTrace must supply converted FILETIME UTC')
    return (ticks - 116444736000000000) * 100


def validate_decode_source(source, etl_identity):
    need(source.get('kind') == 'owned_ETW_capability_fixture', 'exact fixture source type')
    trace = source['trace']
    need(trace['start_status'] == trace['stop_status'] == 0 and trace['stopped'] is True,
         'source must have acquired and stopped its own trace successfully')
    statistics = trace['statistics']
    need(all(statistics[k] == 0 for k in ('EventsLost', 'LogBuffersLost', 'RealTimeBuffersLost')),
         'source lost events cannot be repaired by decoding')
    stop = bytes.fromhex(trace['returned_stop_properties_hex'])
    need(len(stop) == C.sizeof(PROPERTIES), 'complete original StopTrace statistics')
    original = PROPERTIES.from_buffer_copy(stop)
    need(all(getattr(original, k) == value for k, value in statistics.items()), 'source loss statistics agree with original bytes')
    h = source['helper']; ready = source['helper_ready']
    need(source['helper_exit'] == 0 and h['error'] is None and h['closed'] == [True, True]
         and source['cleanup']['owned_helper_forced'] is False, 'original fixture completed naturally')
    need((ready['pid'], ready['tid']) == (h['pid'], h['tid']), 'source helper lifetime identity')
    artifacts = [x for x in source['artifacts'] if x['path'].lower().endswith('trace.etl')]
    need(len(artifacts) == 1 and all(artifacts[0][k] == etl_identity[k] for k in ('bytes', 'sha256')),
         'ETL is the exact artifact bound by the original source')
    need(0 < etl_identity['bytes'] < ETL_LIMIT, 'original ETL within strict sequential limit')


def validate_log_header(header, source):
    helper = source['helper']; rows = helper['rows']
    need(header['NumberOfProcessors'] == source['qualification']['current_guest_resources']['logical_processors'],
         'ETL processor count matches qualified fixture')
    need(header['PointerSize'] == 8 and header['PerfFreq'] > 0, 'actual 64-bit kernel trace clock')
    need(header['EventsLost'] == header['BuffersLost'] == 0, 'ETL header losses')
    need(header['BuffersWritten'] == source['trace']['statistics']['BuffersWritten'], 'same original stopped ETL buffer count')
    start = filetime_ns(header['StartTime']); end = filetime_ns(header['EndTime'])
    need(start <= rows[0]['begin_ns'] <= rows[0]['end_ns'] <= rows[1]['begin_ns'] <= rows[1]['end_ns'] <= end,
         'actual ETL FILETIME interval contains exact fixture UTC intervals; no tolerance')


def verify_wait_window_records(records_source, decode_report):
    """Pure, narrow review of authenticated helper records, never re-signs status.

    An enter-minus-exit prefix count is recorded without assigning meanings or
    LIFO pairings to nested calls outside the two original fixture intervals.
    """
    need(decode_report['status'] == 'blocked' and any('overlapping/unclosed target syscall' in x
         for x in decode_report['errors']), 'retain original global single-open rejection')
    need(decode_report['process_trace_status'] == decode_report['close_trace_status'] == 0
         and not decode_report['callback_errors'], 'completed authenticated offline decode')
    need(all(records_source['ETL'][k] == decode_report['ETL'][k] for k in ('bytes','sha256')), 'same complete ETL')
    helper = records_source['helper']; rows = records_source['records']; tid = helper['tid']; pid = helper['pid']
    need(helper['error'] is None and helper['closed'] == [True, True], 'original fixture result and cleanup')
    need(len(rows) == decode_report['retained_helper_records'] and 0 < len(rows) <= 4096, 'all retained helper records')
    need(any((b['pid'], b['tid']) == (pid,tid) for b in decode_report['helper_thread_bindings']), 'actual ETL PID/TID binding')
    active_cpu = None; previous_index = -1; previous_ns = -1; enters = exits = depth = 0
    min_depth = 0; outside_overlaps = []; prefix = []
    for row in rows:
        prefix.append(dict(enters=enters, exits=exits, balance=depth))
        h = bytes.fromhex(row['record_header_hex']); bc = bytes.fromhex(row['buffer_context_hex'])
        raw = bytes.fromhex(row['payload_hex'])
        need(len(h) == 80 and len(bc) == 4 and len(raw) <= 512, 'complete bounded original record bytes')
        need(filetime_ns(struct.unpack_from('<q',h,16)[0]) == row['ns'], 'raw FILETIME and decoded time agree')
        need(h[45] == row['opcode'] and str(uuid.UUID(bytes_le=h[24:40])) == row['guid'], 'raw event class and opcode')
        need(struct.unpack_from('<II',h,8) == (row['tid'],row['pid']), 'raw header IDs')
        flags = struct.unpack_from('<H',h,4)[0]
        cpu = struct.unpack('<H',bc[:2])[0] if flags & 0x200 else bc[0]
        need(cpu == row['cpu'] and row['index'] > previous_index and row['ns'] >= previous_ns,
             'actual CPU and complete monotonic helper sequence')
        previous_index = row['index']; previous_ns = row['ns']; op = row['opcode']
        if op == 36:
            need(row['guid'] == THREAD_GUID and len(raw) >= 8, 'original CSwitch payload')
            new,old = struct.unpack_from('<II',raw)
            need((new,old) == (row['data']['NewThreadId'],row['data']['OldThreadId'])
                 and row['decoder_cpu_tid_before'] == old, 'raw CSwitch and full-decoder CPU seed agree')
            need(tid in (new,old), 'only complete helper switch transitions retained')
            if old == tid:
                need(active_cpu == cpu, 'helper switches off actual occupied CPU')
                active_cpu = None
            if new == tid:
                need(active_cpu is None, 'helper cannot execute on two CPUs')
                active_cpu = cpu
        else:
            need(row['guid'] == PERF_GUID and op in (51,52) and active_cpu == cpu
                 and row['decoder_cpu_tid_before'] == tid, 'syscall attributed by actual helper CPU switches')
            need(row['tid'] in (tid,0xffffffff) and row['pid'] in (pid,0xffffffff), 'no conflicting raw owner')
            if op == 51:
                need(len(raw) == (8 if flags & 0x40 else 4)
                     and int.from_bytes(raw,'little') == row['data']['SysCallAddress'], 'original syscall entry payload')
                if depth:
                    outside_overlaps.append(dict(index=row['index'],ns=row['ns'],observed_prior_balance=depth))
                enters += 1; depth += 1
            else:
                need(len(raw) == 4 and int.from_bytes(raw,'little') == row['data']['SysCallNtStatus'], 'original syscall exit payload')
                exits += 1; depth -= 1; min_depth = min(min_depth, depth)
    prefix.append(dict(enters=enters, exits=exits, balance=depth))
    windows = helper['rows']
    need([x['label'] for x in windows] == ['success','timeout']
         and [x['Win32_result'] for x in windows] == [0,258], 'two unchanged original fixture outcomes')
    need(windows[0]['end_ns'] <= windows[1]['begin_ns'] and min_depth >= 0, 'ordered windows and observed prefix conservation')
    results = []
    for window in windows:
        need(window['tid'] == tid and window['expected_NTSTATUS'] == window['Win32_result'], 'fixture wait owner/status')
        indices = [i for i,x in enumerate(rows) if window['begin_ns'] <= x['ns'] <= window['end_ns']]
        need(len(indices) == 4 and indices == list(range(indices[0],indices[0]+4)), 'exactly four events, no discarded window event')
        a,b,c,d = [rows[i] for i in indices]
        need([x['opcode'] for x in (a,b,c,d)] == [51,36,36,52], 'strict enter/switch-out/switch-in/exit')
        need(prefix[indices[0]]['balance'] == prefix[indices[-1]+1]['balance'] == 0,
             'no observed outstanding entry count crosses either window boundary')
        need(b['data']['OldThreadId'] == c['data']['NewThreadId'] == tid
             and b['data']['NewThreadId'] != tid and c['data']['OldThreadId'] != tid
             and a['cpu'] == b['cpu'] and c['cpu'] == d['cpu'], 'actual helper waits and resumes on recorded CPU')
        need(a['ns'] < b['ns'] < c['ns'] < d['ns'] and d['data']['SysCallNtStatus'] == window['expected_NTSTATUS'],
             'strict event order and true NT return status')
        results.append(dict(label=window['label'],fixture_interval=[window['begin_ns'],window['end_ns']],
            selected_indices=indices,global_indices=[x['index'] for x in (a,b,c,d)],
            syscall_address=a['data']['SysCallAddress'],NTSTATUS=d['data']['SysCallNtStatus'],
            prefix_before=prefix[indices[0]],prefix_after=prefix[indices[-1]+1],
            original_records=[a,b,c,d]))
    need(results[0]['syscall_address'] == results[1]['syscall_address'] != 0, 'unique same syscall address across waits')
    return dict(scope='two owned fixture wait windows only',accepted=False,window_capability_observed=True,
        fixture_architecture='64-bit guest Python helper; not original game WOW64',
        original_game=False,fullABI=False,fullglobalpairing=False,kernel_symbol_identity=False,
        original_global_status=decode_report['status'],original_global_errors=decode_report['errors'],
        raw_records_checked=len(rows),helper_pid=pid,helper_tid=tid,windows=results,
        observed_prefix_ledger=dict(enters=enters,exits=exits,final_balance=depth,minimum_balance=min_depth,
                                    overlap_entries=outside_overlaps),
        limits=['Every event in each window is retained and strictly paired; no window event is dropped.',
                'Prefix balances are observed enter-minus-exit counts, not a proof of outside nesting semantics or of absent unrecorded events.',
                'No LIFO interpretation is assigned to outside overlaps; the original global single-open rejection remains blocked.',
                'Zero ETW loss counters do not by themselves establish a globally complete syscall pairing.'])


def _decode_etl(path, source, result, deadline, helper_records_path=None):
    """Private: both callers qualify before reaching any WinAPI here."""
    result['ABI'] = decoder_layout()
    api = C.WinDLL('advapi32', use_last_error=True); tdh = C.WinDLL('tdh', use_last_error=True)
    api.OpenTraceW.argtypes = [C.POINTER(LOGFILE)]; api.OpenTraceW.restype = C.c_uint64
    api.ProcessTrace.argtypes = [C.POINTER(C.c_uint64), C.c_uint32, C.c_void_p, C.c_void_p]
    api.ProcessTrace.restype = C.c_uint32
    api.CloseTrace.argtypes = [C.c_uint64]; api.CloseTrace.restype = C.c_uint32
    tdh.TdhGetEventInformation.argtypes = [C.POINTER(EVENT_RECORD), C.c_uint32, C.c_void_p, C.c_void_p, C.POINTER(C.c_uint32)]
    tdh.TdhGetEventInformation.restype = C.c_uint32
    tdh.TdhGetPropertySize.argtypes = [C.POINTER(EVENT_RECORD), C.c_uint32, C.c_void_p, C.c_uint32,
                                     C.POINTER(PROPERTY_DESCRIPTOR), C.POINTER(C.c_uint32)]
    tdh.TdhGetPropertySize.restype = C.c_uint32
    tdh.TdhGetProperty.argtypes = [C.POINTER(EVENT_RECORD), C.c_uint32, C.c_void_p, C.c_uint32,
                                 C.POINTER(PROPERTY_DESCRIPTOR), C.c_uint32, C.c_void_p]
    tdh.TdhGetProperty.restype = C.c_uint32
    helper = source['helper']; selected = []; cpu_threads = {}; schemas = {}; digest = hashlib.sha256()
    errors = []; bindings = []; samples = {}; counts = {}; buffers = []; event_count = 0
    first_ticks = None

    def property_value(record, name):
        text = C.create_unicode_buffer(name)
        desc = PROPERTY_DESCRIPTOR(C.cast(text, C.c_void_p).value, 0xffffffff, 0)
        size = C.c_uint32()
        status = int(tdh.TdhGetPropertySize(record, 0, None, 1, C.byref(desc), C.byref(size)))
        need(status == 0, 'TdhGetPropertySize ' + name + ' status=' + str(status))
        need(size.value in ((4, 8) if name == 'SysCallAddress' else (4,)), 'strict TDH scalar width: ' + name)
        raw = C.create_string_buffer(size.value)
        status = int(tdh.TdhGetProperty(record, 0, None, 1, C.byref(desc), size.value, raw))
        need(status == 0, 'TdhGetProperty ' + name + ' status=' + str(status))
        return int.from_bytes(raw.raw, 'little')

    def schema(record):
        h = record.contents.EventHeader
        key = (bytes(h.ProviderId), bytes(h.EventDescriptor), h.Flags & 0x60)
        if key not in schemas:
            need(len(schemas) < 128, 'bounded ETW schema count')
            size = C.c_uint32()
            status = int(tdh.TdhGetEventInformation(record, 0, None, None, C.byref(size)))
            need(status == 122 and 112 <= size.value <= 65536, 'bounded TDH metadata size/status=' + str(status))
            buf = C.create_string_buffer(size.value)
            need(tdh.TdhGetEventInformation(record, 0, None, buf, C.byref(size)) == 0, 'TDH metadata retrieval')
            raw = buf.raw[:size.value]
            schemas[key] = dict(provider_guid=str(uuid.UUID(bytes_le=raw[:16])),
                event_guid=str(uuid.UUID(bytes_le=raw[16:32])), metadata_sha256=hashlib.sha256(raw).hexdigest(),
                metadata_prefix_hex=raw[:112].hex(), metadata_bytes=len(raw))
        return schemas[key]

    def event_callback(record):
        nonlocal event_count, first_ticks
        if errors:
            return
        try:
            need(time.monotonic() < deadline, 'offline decode deadline')
            e = record.contents; h = e.EventHeader; event_count += 1
            need(event_count <= EVENT_LIMIT, 'bounded complete ETL event count')
            need(e.UserDataLength <= 65535 and (e.UserData or not e.UserDataLength), 'valid bounded ETW payload')
            payload = C.string_at(e.UserData, e.UserDataLength) if e.UserDataLength else b''
            digest.update(struct.pack('<I', len(payload))); digest.update(bytes(h)); digest.update(bytes(e.BufferContext)); digest.update(payload)
            if first_ticks is None:
                first_ticks = h.TimeStamp
                result['first_record'] = dict(header_hex=bytes(h).hex(), payload_prefix_hex=payload[:512].hex(),
                    payload_bytes=len(payload), FILETIME=h.TimeStamp)
            provider = str(uuid.UUID(bytes_le=bytes(h.ProviderId))); op = h.EventDescriptor.Opcode
            if provider not in (SYSTEM_GUID, PERF_GUID, THREAD_GUID) or op not in (1, 2, 3, 4, 36, 51, 52):
                return
            info = schema(record); guid = info['event_guid']
            # No assumption that EventHeader.ProviderId is the MOF EventGuid.
            if guid not in (PERF_GUID, THREAD_GUID):
                return
            cpu = e.BufferContext.ProcessorIndex if h.Flags & 0x200 else e.BufferContext.ProcessorIndex & 0xff
            row = dict(index=event_count, guid=guid, opcode=op, ns=filetime_ns(h.TimeStamp), tid=h.ThreadId, pid=h.ProcessId,
                       cpu=cpu, decoder_cpu_tid_before=cpu_threads.get(cpu), data={})
            if guid == THREAD_GUID and op in (1, 2, 3, 4):
                pid = property_value(record, 'ProcessId'); tid = property_value(record, 'TThreadId')
                if tid == helper['tid']:
                    need(pid == helper['pid'], 'ETL thread lifetime bound to another PID')
                    need(len(bindings) < 16, 'bounded helper lifetime events')
                    need(len(payload) <= 512, 'bounded original helper lifetime payload')
                    bindings.append(dict(opcode=op, pid=pid, tid=tid, ns=row['ns'],
                        header_hex=bytes(h).hex(), payload_hex=payload.hex(), schema=info))
                return
            if (guid, op) not in ((PERF_GUID, 51), (PERF_GUID, 52), (THREAD_GUID, 36)):
                return
            fields = ('NewThreadId', 'OldThreadId') if op == 36 else ('SysCallAddress',) if op == 51 else ('SysCallNtStatus',)
            row['data'] = {name: property_value(record, name) for name in fields}
            label = guid + ':' + str(op); counts[label] = counts.get(label, 0) + 1
            if label not in samples:
                need(len(payload) <= 512, 'bounded original syscall/context-switch payload')
                samples[label] = dict(header_provider_guid=provider, schema=info, record_header_hex=bytes(h).hex(),
                    buffer_context_hex=bytes(e.BufferContext).hex(), payload_hex=payload.hex(), decoded=row)
            retain = False
            if op == 36:
                cpu_threads[cpu] = row['data']['NewThreadId']
                retain = helper['tid'] in row['data'].values()
            else:
                current = h.ThreadId if h.ThreadId not in (0, 0xffffffff) else cpu_threads.get(cpu)
                retain = current == helper['tid']
            if retain:
                need(len(selected) < 4096, 'bounded helper-only event sequence')
                need(len(payload) <= 512, 'bounded retained helper event payload')
                row.update(record_header_hex=bytes(h).hex(), buffer_context_hex=bytes(e.BufferContext).hex(),
                           payload_hex=payload.hex())
                selected.append(row)
        except Exception as exc:
            errors.append(repr(exc))  # Never unwind across the ctypes callback ABI.

    def buffer_callback(log):
        try:
            need(time.monotonic() < deadline, 'offline buffer deadline')
            need(log.contents.EventsLost == 0, 'ProcessTrace buffer events lost')
            need(len(buffers) < 128, 'bounded ETL buffers')
            buffers.append(int(log.contents.BuffersRead))
            return 0 if errors else 1
        except Exception as exc:
            errors.append(repr(exc)); return 0

    event_cb = C.WINFUNCTYPE(None, C.POINTER(EVENT_RECORD))(event_callback)
    buffer_cb = C.WINFUNCTYPE(C.c_uint32, C.POINTER(LOGFILE))(buffer_callback)
    log = LOGFILE(); log.LogFileName = str(path); log.ProcessTraceMode = 0x10000000  # EVENT_RECORD, NOT RAW_TIMESTAMP
    log.EventRecordCallback = C.cast(event_cb, C.c_void_p).value
    log.BufferCallback = C.cast(buffer_cb, C.c_void_p).value
    handle = int(api.OpenTraceW(C.byref(log)))
    result['open_trace_handle'] = handle
    need(handle != 0xffffffffffffffff, 'OpenTraceW error=' + str(C.get_last_error()))
    try:
        header = {n: int(getattr(log.LogfileHeader, n)) for n in (
            'StartTime', 'EndTime', 'BootTime', 'PerfFreq', 'NumberOfProcessors', 'PointerSize',
            'EventsLost', 'BuffersLost', 'BuffersWritten', 'ReservedFlags', 'LogFileMode')}
        result['ETL_header'] = header
        result['ETL_header_raw_hex'] = bytes(log.LogfileHeader).hex()
        validate_log_header(header, source)
        handles = (C.c_uint64 * 1)(handle)
        status = int(api.ProcessTrace(handles, 1, None, None))
        result.update(process_trace_status=status, callback_errors=errors, total_records=event_count,
            buffer_reads=buffers, matching_schema_counts=counts, first_schema_records=list(samples.values()),
            helper_thread_bindings=bindings, retained_helper_records=len(selected),
            complete_record_digest=digest.hexdigest(),
            digest_coverage='uint32 payload-length + converted EVENT_HEADER80 + BUFFER_CONTEXT4 + UserData, per record; original complete ETL remains SHA-bound',
            retained_sequence_scope='helper syscall records plus every helper switch on/off CPU; not a stored whole-system event array')
        need(not errors and status == 0, 'complete ProcessTrace failed: ' + str(status) + ' ' + repr(errors))
        need(first_ticks == header['StartTime'], 'first native timestamp equals ETL StartTime; no local-time calibration')
        need(buffers and buffers[-1] == header['BuffersWritten'], 'all original ETL buffers consumed')
        need(bindings, 'actual ETL PID/TID lifetime binding absent')
        diagnostic = {}
        try:
            result['analysis'] = analyze_events(selected, helper, source['trace']['statistics'], diagnostic)
        except ValueError:
            result['first_mismatch'] = diagnostic
            if helper_records_path is not None:
                raw = json.dumps(dict(schema_version=1, ETL=identity(path), helper=helper,
                    scope='all retained helper records including every helper switch on/off CPU; not whole-system events',
                    records=selected), separators=(',',':')).encode()
                packed = gzip.compress(raw, mtime=0)
                result['helper_records_diagnostic'] = dict(records=len(selected), uncompressed_bytes=len(raw),
                    uncompressed_sha256=hashlib.sha256(raw).hexdigest(), compressed_bytes=len(packed), retained=False)
                if len(packed) <= 65536:
                    with helper_records_path.open('xb') as f: f.write(packed)
                    result['helper_records_diagnostic'].update(retained=True, artifact=identity(helper_records_path))
                else:
                    result['helper_records_diagnostic']['reason'] = '64 KiB cap; sequence not truncated or retained'
            raise
    finally:
        result['close_trace_status'] = int(api.CloseTrace(handle))
        need(result['close_trace_status'] == 0, 'CloseTrace failed for owned offline reader')


def decode_only(source_path, source_sha, etl_path, etl_sha, out):
    begun = time.monotonic()
    qualification = qualify()  # Must precede OpenTrace/TDH and all other WinAPIs.
    out = out.resolve(); source_path = source_path.resolve(); etl_path = etl_path.resolve()
    need(out.parent == ROOT / 'analysis' and out.suffix == '.json' and not out.exists(), 'new guest decode result path')
    helper_records_path = out.with_suffix('.helper.json.gz')
    need(not helper_records_path.exists(), 'new helper diagnostic path required')
    result = dict(kind='offline_ETW_capability_decode', accepted=False, status='blocked',
        qualification=qualification, implementation=identity(Path(__file__)), errors=[],
        original_game_observed=False, full_ABI_verified=False, new_native_capture=False,
        timestamp_method='ProcessTrace FILETIME conversion; no tracerpt timezone, tolerance or inferred offset')
    try:
        need(source_path.stat().st_size <= 128*1024 and etl_path.stat().st_size < ETL_LIMIT, 'bounded source artifacts')
        result['source'] = identity(source_path); result['ETL'] = identity(etl_path)
        need(result['source']['sha256'] == source_sha and result['ETL']['sha256'] == etl_sha, 'explicit original source and ETL SHA')
        source = json.loads(source_path.read_bytes())
        validate_decode_source(source, result['ETL'])
        _decode_etl(etl_path, source, result, begun + WALL_SECONDS, helper_records_path)
        need(identity(source_path) == result['source'] and identity(etl_path) == result['ETL'], 'source artifacts remained unchanged')
        result['status'] = 'capability_observed'
    except Exception as exc:
        result['errors'].append(repr(exc))
    finally:
        result['elapsed_seconds'] = time.monotonic()-begun
        result['implementation_after'] = identity(Path(__file__))
        if result['implementation_after'] != result['implementation']:
            result['status'] = 'blocked'; result['errors'].append('decoder implementation changed during observation')
        if result['elapsed_seconds'] > WALL_SECONDS:
            result['status'] = 'blocked'; result['errors'].append('offline decode wall budget exceeded')
        raw = json.dumps(result, ensure_ascii=False, indent=2).encode('utf8')
        need(len(raw) <= 128*1024, 'small decoder summary only')
        with out.open('xb') as f: f.write(raw + b'\n')
    return result


def run(out):
    begun = time.monotonic(); deadline = begun + WALL_SECONDS
    qualification = qualify()  # Before output creation, kernel API or helper launch.
    out = out.resolve()
    need(out.parent == ROOT / 'analysis' and not out.exists() and out.suffix == '.json', 'new guest analysis JSON required')
    folder = out.with_suffix('')
    need(not folder.exists(), 'new bounded evidence directory required')
    folder.mkdir()
    etl = folder / 'trace.etl'
    result = dict(kind='owned_ETW_capability_fixture', accepted=False, status='blocked',
        original_game_observed=False, full_ABI_verified=False, qualification=qualification,
        implementation=identity(Path(__file__)), references=REFERENCES, errors=[],
        limits=dict(trace_bytes=ETL_LIMIT, decoded_summary_bytes=128*1024, wall_seconds=WALL_SECONDS),
        clock='ETW QPC converted to FILETIME by ProcessTrace; helper precise FILETIME; no matching tolerance',
        trace=None, helper=None, analysis=None, cleanup={})
    child = None; session = None
    def remaining(cap):
        value = min(cap, deadline-time.monotonic())
        need(value > 0, '30-second ETW fixture budget exhausted')
        return value
    try:
        k, advapi = bind_windows()
        child = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', '-m',
            'devtools.terminal_wait_etw_probe', '--fixture'], cwd=ROOT,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        lines = queue.Queue()
        threading.Thread(target=lambda: lines.put(child.stdout.readline(65536)), daemon=True).start()
        ready = json.loads(lines.get(timeout=remaining(22)))
        need(ready.get('ready') is True and ready['pid'] == child.pid, 'exact owned fixture ready')
        result['helper_ready'] = ready
        session = Session(advapi, etl)
        try:
            session.start()
            output, error = child.communicate(b'GO\n', timeout=remaining(3))
            need(len(output) <= 65536 and len(error) <= 8192, 'bounded helper output')
            result['helper_exit'] = child.returncode
            result['helper_stderr'] = error.decode('utf8', errors='replace')
            result['helper'] = json.loads(output)
            need(child.returncode == 0 and result['helper']['pid'] == child.pid
                 and result['helper']['tid'] == ready['tid'], 'same successful owned helper')
        finally:
            result['trace'] = session.stop()
        need(result['trace'].get('stop_status') == 0, 'owned ETW stop failed or trace already exhausted')
        need(etl.exists() and 0 < etl.stat().st_size <= ETL_LIMIT, '4 MiB ETL limit')
        need(etl.stat().st_size < ETL_LIMIT, 'trace reached sequential limit; completeness not assumed')
        result['decoder'] = {}
        _decode_etl(etl, result, result['decoder'], deadline)
        result['analysis'] = result['decoder']['analysis']
        result['status'] = 'capability_observed'
    except Exception as exc:
        result['errors'].append(repr(exc))
    finally:
        if session is not None and session.owned:
            result['trace'] = session.stop()
        if session is not None and session.owned:
            result['errors'].append('owned trace stop unresolved; retained exact logger handle in trace receipt')
            result['status'] = 'blocked'
        if child is not None:
            forced = child.poll() is None
            if forced:
                child.kill(); child.wait(timeout=2)
            result['cleanup']['owned_helper_forced'] = forced
            for pipe in (child.stdin, child.stdout, child.stderr):
                if pipe is not None:
                    pipe.close()
        result['elapsed_seconds'] = time.monotonic()-begun
        result['implementation_after'] = identity(Path(__file__))
        if result['implementation_after'] != result['implementation']:
            result['status'] = 'blocked'; result['errors'].append('fixture implementation changed during observation')
        result['artifacts'] = [identity(p) for p in folder.iterdir() if p.is_file()]
        if result['elapsed_seconds'] > WALL_SECONDS:
            result['status'] = 'blocked'; result['errors'].append('wall budget exceeded')
        with out.open('x', encoding='utf8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2); f.write('\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--fixture', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--decode-source', type=Path, help='Decode an existing fixture report; no collection')
    parser.add_argument('--source-sha')
    parser.add_argument('--etl', type=Path)
    parser.add_argument('--etl-sha')
    args = parser.parse_args()
    if args.fixture:
        raise SystemExit(fixture())
    parser.error('--out is required') if args.out is None else None
    if args.decode_source:
        if not (args.source_sha and args.etl and args.etl_sha):
            parser.error('--decode-source requires --source-sha, --etl and --etl-sha')
        result = decode_only(args.decode_source, args.source_sha, args.etl, args.etl_sha, args.out)
    else:
        if args.source_sha or args.etl or args.etl_sha:
            parser.error('decode arguments require --decode-source')
        result = run(args.out)
    print(json.dumps(dict(status=result['status'], errors=result['errors'], accepted=False)))
    raise SystemExit(0 if result['status'] == 'capability_observed' else 1)
