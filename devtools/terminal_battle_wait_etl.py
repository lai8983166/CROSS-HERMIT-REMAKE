"""Bounded offline ETW reader for explicit battle-window sources.

Derived from frozen terminal_wait_etw_probe._decode_etl SHA60af4a1e... with
explicit subject naming and declared larger limits. No existing module changed.
Every original ETL event contributes to the cumulative raw-record digest; only
subject syscall/switch records are retained. This is not a CPU/RAM state trace.
"""
import ctypes as C
import hashlib
from pathlib import Path
import struct
import time
import uuid
from devtools import terminal_wait_etw_probe as frozen

FROZEN_READER_SHA='60af4a1e487fff1e738808804be36cf7223b2843a365b123b49b1784087a31f6'
EVENT_LIMIT=2_000_000
MAX_BUFFERS=1024
MAX_SELECTED=16384
ETL_LIMIT=64*1024*1024
SELECTED_GZIP_LIMIT=512*1024
SOURCE_GZIP_LIMIT=2*1024*1024
SOURCE_EXPANDED_LIMIT=8*1024*1024
DECODE_SECONDS=180
LIMITS=dict(maximum_file_mib=64,buffer_kib=64,minimum_buffers=4,maximum_buffers=8,
            max_events=EVENT_LIMIT,max_buffers=MAX_BUFFERS,max_selected_records=MAX_SELECTED,
            max_selected_gzip_bytes=SELECTED_GZIP_LIMIT,decode_seconds=DECODE_SECONDS)
need=frozen.need
filetime_ns=frozen.filetime_ns
PERF_GUID=frozen.PERF_GUID
THREAD_GUID=frozen.THREAD_GUID
SYSTEM_GUID=frozen.SYSTEM_GUID
EVENT_RECORD=frozen.EVENT_RECORD
LOGFILE=frozen.LOGFILE
PROPERTY_DESCRIPTOR=frozen.PROPERTY_DESCRIPTOR


def decoder_layout():
    need(hashlib.sha256(Path(frozen.__file__).read_bytes()).hexdigest()==FROZEN_READER_SHA,
         'unchanged frozen ETW ABI definitions and qualification helper')
    return frozen.decoder_layout()


def validate_log_header(header,source):
    need(source['trace_limits']==LIMITS,'explicit source trace/reader budgets')
    need(header['NumberOfProcessors']==source['input_isolation']['current_guest_resources']['logical_processors'],
         'same qualified processor count')
    need(header['PointerSize']==8 and header['PerfFreq']>0,'actual x64 kernel timestamp conversion')
    need(header['EventsLost']==header['BuffersLost']==0,'zero reported ETL header losses')
    need(0<header['BuffersWritten']<=MAX_BUFFERS and header['BuffersWritten']==source['trace']['statistics']['BuffersWritten'],
         'all original stopped ETL buffers within declared limit')
    start=filetime_ns(header['StartTime']);end=filetime_ns(header['EndTime'])
    interval=source['capture_interval']
    need(start<=interval['begin_ns']<interval['end_ns']<=end,'actual API interval inside original ETL FILETIME')
    for row in source['window_snapshots']:
        need(start<=row['snapshot_begin_ns']<=row['snapshot_end_ns']<=end,
             'each complete owner snapshot inside the retained original ETL')


def decode_etl(path, source, result, deadline, consume_records):
    """Qualified guest only; reads one existing ETL, never controls a logger."""
    result['reader_qualification'] = frozen.qualify()
    need(deadline <= time.monotonic() + 180, 'bounded reader deadline')
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
    subject = source['subject']; selected = []; cpu_threads = {}; schemas = {}; digest = hashlib.sha256()
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
                if tid == subject['tid']:
                    need(pid == subject['pid'], 'ETL thread lifetime bound to another PID')
                    need(len(bindings) < 16, 'bounded subject lifetime events')
                    need(len(payload) <= 512, 'bounded original subject lifetime payload')
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
                retain = subject['tid'] in row['data'].values()
            else:
                current = h.ThreadId if h.ThreadId not in (0, 0xffffffff) else cpu_threads.get(cpu)
                retain = current == subject['tid']
            if retain:
                need(len(selected) < MAX_SELECTED, 'bounded subject-only event sequence')
                need(len(payload) <= 512, 'bounded retained subject event payload')
                row.update(record_header_hex=bytes(h).hex(), buffer_context_hex=bytes(e.BufferContext).hex(),
                           payload_hex=payload.hex())
                selected.append(row)
        except Exception as exc:
            errors.append(repr(exc))  # Never unwind across the ctypes callback ABI.

    def buffer_callback(log):
        try:
            need(time.monotonic() < deadline, 'offline buffer deadline')
            need(log.contents.EventsLost == 0, 'ProcessTrace buffer events lost')
            need(len(buffers) < MAX_BUFFERS, 'bounded ETL buffers')
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
            subject_thread_bindings=bindings, retained_subject_records=len(selected),
            complete_record_digest=digest.hexdigest(),
            digest_coverage='uint32 payload-length + converted EVENT_HEADER80 + BUFFER_CONTEXT4 + UserData, per record; original complete ETL remains SHA-bound',
            retained_sequence_scope='subject syscall records plus every subject switch on/off CPU; not a stored whole-system event array')
        need(not errors and status == 0, 'complete ProcessTrace failed: ' + str(status) + ' ' + repr(errors))
        need(first_ticks == header['StartTime'], 'first native timestamp equals ETL StartTime; no local-time calibration')
        need(buffers and buffers[-1] == header['BuffersWritten'], 'all original ETL buffers consumed')
        need(bindings, 'actual ETL PID/TID lifetime binding absent')
        result['analysis'] = consume_records(selected)
    finally:
        result['close_trace_status'] = int(api.CloseTrace(handle))
        need(result['close_trace_status'] == 0, 'CloseTrace failed for owned offline reader')
