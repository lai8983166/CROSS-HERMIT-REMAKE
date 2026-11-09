"""Read-only original-worker ETW interpretation; no game/VM/input operations.

The frozen fixture reader is reused only below its fixture interface.  Its
``helper`` local receives PID/TID, never invented fixture outcomes.  A successful
result is one observed wait, not full state/ABI/resource-lifetime acceptance.
"""
import argparse
import ctypes as C
import gzip
import hashlib
import json
from pathlib import Path
import struct
import time
import types
import uuid

from devtools import terminal_wait_etw_probe as etw
from devtools.terminal_wait_native_verification import verify_current_tls

ROOT = Path(__file__).resolve().parents[1]
READER_SHA = '60af4a1e487fff1e738808804be36cf7223b2843a365b123b49b1784087a31f6'
TLS_VALIDATOR_SHA = '89508caa40398d847ebb6b0a25a3b6d845730c3ab4aca835924b3c0ac228003e'
IMAGE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
LIMIT = 64 * 1024
need = etw.need
word = lambda raw, off=0: struct.unpack_from('<I', raw, off)[0]


def blob(value, size, label):
    raw = bytes.fromhex(value)
    need(len(raw) == size, 'complete ' + label)
    return raw


def check_source(source, etl_identity, diagnostic_only=False):
    need(source['kind'] == 'original_worker_ETW_wait', 'explicit original worker source kind')
    need('helper' not in source, 'original source must not impersonate fixture')
    subject = source['subject']
    need(all(type(subject[k]) is int and 0 < subject[k] < 0xffffffff for k in ('pid', 'tid')),
         'actual original worker PID/TID')
    trace = source['trace']; stats = trace['statistics']
    requested = etw.PROPERTIES.from_buffer_copy(blob(trace['requested_properties_hex'],120,'requested ETW properties'))
    need(source['trace_flags'] == requested.EnableFlags == 0x92
         and requested.MaximumFileSize == 4 and requested.LogFileMode == 1
         and requested.BufferSize == 64 and requested.MaximumBuffers == 8,
         'exact bounded original worker trace configuration')
    need(trace['start_status'] == trace['stop_status'] == 0 and trace['stopped'] is True,
         'successfully owned and stopped trace')
    need(all(stats[k] == 0 for k in ('EventsLost', 'LogBuffersLost', 'RealTimeBuffersLost')),
         'no reported trace loss')
    original = etw.PROPERTIES.from_buffer_copy(blob(trace['returned_stop_properties_hex'], 120, 'StopTrace properties'))
    need(all(getattr(original, k) == stats[k] for k in
             ('EventsLost', 'LogBuffersLost', 'RealTimeBuffersLost', 'BuffersWritten', 'NumberOfBuffers')),
         'raw stopped trace statistics')
    need(stats['BuffersWritten'] > 0, 'nonempty stopped ETL')
    need(all(source['ETL'][k] == etl_identity[k] for k in ('bytes', 'sha256'))
         and 0 < etl_identity['bytes'] < etw.ETL_LIMIT, 'exact bounded complete ETL')
    window = source['capture_interval']
    need(type(window['begin_ns']) is int and type(window['end_ns']) is int
         and window['begin_ns'] < window['end_ns'], 'precise ordered capture interval')
    need(source['error'] is None, 'successful original observer source')
    lifecycle=verify_lifecycle(source,require_crt=not diagnostic_only)
    need(source['mutable_private_runtime_files'] and all(x['restored_exact'] is True
         for x in source['mutable_private_runtime_files']), 'private mutable bytes restored exactly')
    need(all(source[k] is False for k in
             ('source_memory_written', 'general_registers_written', 'debug_registers_written',
              'debug_object_modified', 'debugger_reply_substituted'))
         and all(source[k] == [] for k in ('host_game_calls','host_memory_writes','host_input_actions')),
         'read-only observer with no injected exception or game input')
    return lifecycle


def verify_lifecycle(source,require_crt=True):
    """Existing protected exit contract; process status is not WinMain's result."""
    life=source['lifecycle']; lifetime=life['lifetime']; subject=source['subject']
    need(life['error'] is None and lifetime['forced_termination'] is False
         and lifetime['members_before_cleanup']==lifetime['members_after_cleanup']==[], 'natural owned cleanup with empty Job')
    need(str(subject['pid']) in lifetime['exits'] and str(lifetime['parent_pid']) in lifetime['exits']
         and len(lifetime['exits'])>=2 and lifetime['parent_pid']!=subject['pid'], 'actual separate protector and child exits')
    need(lifetime['exits'][str(lifetime['parent_pid'])]['code']==0
         and all(x['signaled'] is True and x['code'] in (0,0xc0000354) for x in lifetime['exits'].values()),
         'existing original protection-layer process status contract')
    need(lifetime['membership'][-1]['pids']==[]
         and {int(x) for x in lifetime['exits']}=={p for x in lifetime['membership'] for p in x['pids']}
         and lifetime['child_status_is_not_WinMain_return'] is True, 'complete owned Job membership and explicit process-status boundary')
    need(life['window_after']==dict(is_window=False,property=0), 'actual original window/property ended')
    request=life['close_request']
    need(request['posted'] is True and request['pid']==subject['pid'] and request['pid'] in request['job_members']
         and (request['message'],request['wParam'],request['lParam'])==(16,0,0), 'owned original WM_CLOSE cleanup')
    terminal=[]
    for snap in life['shutdown']:
        if not all(snap['globals'][k]==0 for k in ('0x7a49fc','0x7a4a00','0x80a398')):
            continue
        ce=snap.get('crt_exit')
        if not ce:
            continue
        need(ce['WinMain_result_hex']==ce['exit_argument_hex']=='00000000', 'actual source WinMain/CRT zero return receipts')
        need(any(r['bp']==ce['callee_bp'] and r['saved_bp']==ce['caller_bp'] and r['return_va']==0x5714f2
                 for f in snap['frames'] for r in f['chain']), 'actual original CRT exit caller ancestry')
        terminal.append(snap)
    if not terminal and not require_crt:
        # This is a separate observation class, never an alternative success
        # contract. Reject contradictory CRT data and require the exact earlier
        # teardown/WinMain stack witness before exposing a diagnostic-only path.
        need(not any('crt_exit' in x for x in life['shutdown']), 'diagnostic requires absent CRT observation, not contradictory CRT data')
        need(not any(r['return_va']==0x5714f2 for x in life['shutdown'] for f in x['frames'] for r in f['chain']),
             'diagnostic requires absent CRT-exit frame, not an incomplete CRT receipt')
        candidates=[x for x in life['shutdown'] if
            all(x['globals'][k]==0 for k in ('0x7a49fc','0x7a4a00','0x80a398'))
            and any(0x49e11a<=r['return_va']<0x49e131 for f in x['frames'] for r in f['chain'])
            and 'winmain_frame' in x]
        need(candidates, 'diagnostic requires observed original cleanup ancestry and cleared globals')
        snap=candidates[-1];f=snap['winmain_frame'];bp=f['bp'];raw=blob(f['stack_hex'],0xd0,'sampled original WinMain stack')
        need(f['stack_start']==bp-0xac and raw[0x10:0xac].hex()==f['locals_hex']
             and raw[0xb4:0xc4].hex()==f['args_hex'], 'actual WinMain stack receipt overlaps')
        need(word(raw,0xb0)==0x5714e6 and any(r['bp']==bp and r['return_va']==0x5714e6
             for frame in snap['frames'] for r in frame['chain']), 'still original WinMain frame, not sampled CRT exit')
        need(word(raw,0xa8)==0, 'actual sampled WinMain return local is zero but not yet a CRT return observation')
        return dict(process_status_is_not_WinMain_return=True,window_and_global_cleanup_observed=True,
            source_CRT_zero_result_observed=False,diagnostic_only=True,PTDcleanup=False,
            full_resource_lifetime_proved=False,strict_source_cleanup_verified=False,
            missing_observation='No crt_exit receipt or original 5714F2 CRT-exit frame; WinMain frame remains on sampled stack.',
            pre_CRT_cleanup_witness=dict(shutdown_index=life['shutdown'].index(snap),elapsed=snap['elapsed'],
                WinMain_bp=bp,WinMain_return_local=0,WinMain_caller=0x5714e6,
                sampled_return_local_is_CRT_return=False))
    need(terminal, 'original globals cleared and source CRT zero result observed before protection exit')
    return dict(process_status_is_not_WinMain_return=True,window_and_global_cleanup_observed=True,
                source_CRT_zero_result_observed=True,PTDcleanup=False,full_resource_lifetime_proved=False,
                strict_source_cleanup_verified=True)


def native_header_check(header, source):
    need(header['NumberOfProcessors'] == source['input_isolation']['current_guest_resources']['logical_processors'],
         'actual qualified guest CPU count')
    need(header['PointerSize'] == 8 and header['PerfFreq'] > 0, 'actual 64-bit kernel clock')
    need(header['EventsLost'] == header['BuffersLost'] == 0, 'ETL header loss counters')
    need(header['BuffersWritten'] == source['trace']['statistics']['BuffersWritten'], 'stopped ETL buffer count')
    lo, hi = (etw.filetime_ns(header[k]) for k in ('StartTime', 'EndTime'))
    window = source['capture_interval']
    need(lo <= window['begin_ns'] < window['end_ns'] <= hi, 'actual capture interval inside ETL API interval')
    snap = source['owner_snapshots']['observed_wait']
    need(window['begin_ns'] <= snap['snapshot_begin_ns'] <= snap['snapshot_end_ns'] <= window['end_ns'],
         'complete wait snapshot inside exact ETL FILETIME interval')


def validate_records(rows, subject, cpu_count):
    """Authenticate raw fields and CPU transitions before considering pairs."""
    need(0 < len(rows) <= 4096, 'bounded complete selected sequence')
    pid, tid = subject['pid'], subject['tid']
    active_cpu = None; prior_index = -1; prior_ns = -1
    calls = []; pending = None; boundary_exits = []; final_pending = None
    for pos, row in enumerate(rows):
        h = blob(row['record_header_hex'], 80, 'EVENT_HEADER')
        bc = blob(row['buffer_context_hex'], 4, 'BUFFER_CONTEXT')
        raw = bytes.fromhex(row['payload_hex'])
        need(len(raw) <= 512, 'bounded complete selected payload')
        need(etw.filetime_ns(struct.unpack_from('<q', h, 16)[0]) == row['ns'], 'raw record timestamp')
        need(h[45] == row['opcode'] and str(uuid.UUID(bytes_le=h[24:40])) == row['guid'], 'raw event identity')
        need(struct.unpack_from('<II', h, 8) == (row['tid'], row['pid']), 'raw owner IDs')
        flags = struct.unpack_from('<H', h, 4)[0]
        cpu = struct.unpack_from('<H', bc)[0] if flags & 0x200 else bc[0]
        need(cpu == row['cpu'] and 0 <= cpu < cpu_count and type(row['index']) is int and row['index'] > prior_index
             and row['ns'] >= prior_ns, 'complete monotonic raw CPU sequence')
        prior_index, prior_ns = row['index'], row['ns']; op = row['opcode']
        if op == 36:
            need(row['guid'] == etw.THREAD_GUID and len(raw) >= 8, 'raw CSwitch class/payload')
            new, old = struct.unpack_from('<II', raw)
            need((new, old) == (row['data']['NewThreadId'], row['data']['OldThreadId'])
                 and row['decoder_cpu_tid_before'] == old, 'full-reader CPU attribution agrees with CSwitch bytes')
            need(tid in (new, old) and new != old, 'actual target CPU transition')
            if old == tid:
                need(active_cpu == cpu, 'target switched off its actual CPU')
                active_cpu = None
            if new == tid:
                need(active_cpu is None, 'target not simultaneously running on another CPU')
                active_cpu = cpu
        else:
            need(row['guid'] == etw.PERF_GUID and op in (51, 52) and active_cpu == cpu
                 and row['decoder_cpu_tid_before'] == tid, 'syscall attributed by full CPU flow')
            need(row['tid'] in (tid, 0xffffffff) and row['pid'] in (pid, 0xffffffff), 'no conflicting raw owner')
            if op == 51:
                need(len(raw) == (8 if flags & 0x40 else 4)
                     and int.from_bytes(raw, 'little') == row['data']['SysCallAddress'], 'raw syscall address')
                need(pending is None, 'overlapping target syscalls; no inferred nesting or discarded entry')
                pending = pos
            else:
                need(len(raw) == 4 and int.from_bytes(raw, 'little') == row['data']['SysCallNtStatus'], 'raw NTSTATUS')
                if pending is None:
                    need(not calls and not boundary_exits, 'unmatched syscall exit inside retained sequence')
                    boundary_exits.append(pos)  # Only the trace's initial partial call; never a candidate.
                else:
                    calls.append((pending, pos)); pending = None
    if pending is not None:
        final_pending = pending  # Trace may stop during a later wait; this is never selected.
    return calls, dict(initial_unpaired_exits=boundary_exits, final_unpaired_entry=final_pending,
                       closed_calls=len(calls), full_global_pairing=not boundary_exits and final_pending is None)


def analyze_original_events(rows, source):
    anchor = source['owner_snapshots']['observed_wait']
    calls, boundaries = validate_records(rows, source['subject'],
        source['input_isolation']['current_guest_resources']['logical_processors'])
    candidates = [(a,b) for a,b in calls
                  if rows[a]['ns'] < anchor['snapshot_begin_ns'] <= anchor['snapshot_end_ns'] < rows[b]['ns']]
    need(len(candidates) == 1, 'one closed syscall strictly contains complete suspended snapshot')
    a, b = candidates[0]; selected = rows[a:b+1]
    need(selected[0]['data']['SysCallAddress'] == source['kernel_wait_export']['target'],
         'actual kernel NtWaitForSingleObject export address')
    need(selected[-1]['data']['SysCallNtStatus'] == 0, 'actual successful NT wait return')
    need(all(x['opcode'] == 36 for x in selected[1:-1]), 'no unpaired syscall inside selected wait')
    tid = source['subject']['tid']; suspended = []
    for left, right in zip(selected[1:-1], selected[2:-1]):
        if left['data']['OldThreadId'] == tid and right['data']['NewThreadId'] == tid:
            if left['ns'] < anchor['snapshot_begin_ns'] <= anchor['snapshot_end_ns'] < right['ns']:
                suspended.append((left['index'], right['index']))
    need(len(suspended) == 1, 'complete paused snapshot inside one actual switched-out interval')
    return dict(scope='one original WOW64 worker wait only', accepted=False,
        wait_observed=True, fullABI=False, fullstate=False, PTDcleanup=False,
        fullglobalpairing=False, boundary_ledger=boundaries,
        subject=source['subject'], selected_indices=[a,b], global_indices=[rows[a]['index'],rows[b]['index']],
        syscall_address=selected[0]['data']['SysCallAddress'], NTSTATUS=0,
        snapshot_interval=[anchor['snapshot_begin_ns'],anchor['snapshot_end_ns']],
        switched_out_interval_indices=list(suspended[0]), selected_records_count=len(selected),
        original_entry_exit=[selected[0],selected[-1]],
        limits=['No inference of omitted events from zero loss counters.',
                'Initial/final partial calls are explicit boundaries and never selected.',
                'Overlapping target entries fail closed; no inferred LIFO semantics.',
                'Wait observation does not establish full CPU/RAM/ABI or PTD cleanup.'])


def memory_at(regions, address, size):
    """Read exact original bytes, rejecting contradictory overlapping receipts."""
    need(0 < size <= 716 and len(regions) <= 104, 'bounded raw stack query')
    matches = []
    for region in regions:
        raw = bytes.fromhex(region['hex']); start = region['pointer']
        need(0 < len(raw) <= 716 and 0x10000 <= start < 0x80000000, 'bounded raw stack region')
        if start <= address and address+size <= start+len(raw):
            matches.append(raw[address-start:address-start+size])
    need(matches and all(x == matches[0] for x in matches), 'complete consistent original stack bytes')
    return matches[0]


def verify_owners(source, image):
    need(hashlib.sha256(image).hexdigest() == IMAGE_SHA, 'fixed original image SHA')
    ranges = ((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98))
    need(len(source['original_code']) == len(ranges), 'all original wait code ranges')
    for row, (lo,hi) in zip(source['original_code'], ranges):
        need(row['pointer'] == lo and bytes.fromhex(row['hex']) == image[lo-0x400000:hi-0x400000],
             'actual original wait instructions')
    need(image[0x22407:0x2240D] == bytes.fromhex('ff156c225900'), 'original wait IAT call instruction')
    subject = source['subject']; node = subject['node']; pid = subject['pid']; tid = subject['tid']
    snapshots = source['owner_snapshots']
    need(set(snapshots) == {'before','observed_wait','after'}, 'three original ownership snapshots')
    baseline = snapshots['before']['current_TLS']; heads = []; manager_events=[]; previous_end = -1
    for label in ('before','observed_wait','after'):
        snap = snapshots[label]; frame = snap['frame']; context = blob(frame['context_hex'],716,'WOW64 context')
        need(previous_end <= snap['snapshot_begin_ns'] <= snap['snapshot_end_ns'], 'ordered nonoverlapping owner samples')
        previous_end = snap['snapshot_end_ns']
        need(snap['node_pointer'] == node and snap['manager_pointer'] == subject['main']+0x64,
             'same actual node and manager')
        need(snap['source_memory_written'] is False and snap['debug_registers_written'] is False,
             'read-only owner sample')
        head = blob(snap['node_hex'],64,'actual node'); manager = blob(snap['manager_hex'],0x120,'manager')
        manager_events.append(word(manager,0x118))
        need(word(head,8) == snap['manager_pointer'] and word(head,0x24) == tid
             and word(head,0x1C) and word(head,0x20), 'actual node manager, event and native thread')
        heads.append(tuple(word(head,k) for k in (0,8,0x18,0x1C,0x20,0x24)))
        need(frame['tid'] == tid and frame['EIP'] == word(context,184)
             and frame['ESP'] == word(context,196) and frame['EBP'] == word(context,180), 'actual worker registers')
        need(snap['scheduler_frame']['tid'] == subject['main_tid'] != tid, 'distinct frozen current scheduler')
        verify_current_tls(snap['current_TLS'],context,baseline,node,pid,tid)
        chain = frame['chain']; need(0 < len(chain) <= 100 and chain[0]['bp'] == frame['EBP'], 'actual frame-chain start')
        regions = snap['stack_regions']
        for i,r in enumerate(chain):
            need(struct.unpack('<II',memory_at(regions,r['bp'],8)) == (r['saved_bp'],r['return_va']),
                 'original stack frame links')
            if i+1 < len(chain):
                need(r['saved_bp'] == chain[i+1]['bp'] and r['bp'] < r['saved_bp'] < r['bp']+0x100000,
                     'continuous bounded original EBP chain')
        def unique_return(va):
            candidates = [x for x in chain if x['return_va'] == va]
            need(len(candidates) == 1, 'unique original ancestor ' + hex(va))
            return candidates[0]
        worker = unique_return(0x56E183); callback = unique_return(0x421F8A)
        tls = snap['current_TLS']; ptrs = dict(worker_argument=worker['bp']+8,
            wrapper_argument=worker['saved_bp']+8,callback_this=callback['bp']-4,
            callback_argument=callback['bp']+8,node_argument=node+0x18)
        vals = {}
        for name,pointer in ptrs.items():
            mem = tls['ancestry_memory'][name]
            need(mem['pointer'] == pointer, 'actual ancestry address')
            vals[name] = word(blob(mem['hex'],4,'actual ancestry word'))
            need(vals[name] == tls['ancestry'][name], 'raw ancestry value')
        need(vals['worker_argument'] == vals['callback_this'] == node
             and vals['wrapper_argument'] == tls['PTD']
             and vals['callback_argument'] == vals['node_argument'] == word(head,0x18), 'same CRT callback lifetime')
        registered = snap['registered_nodes']; seen = set(); found = False
        for bucket in range(32):
            pointer = word(manager,bucket*8)
            while pointer:
                need(pointer not in seen and len(seen)<32, 'acyclic actual manager node graph')
                seen.add(pointer); candidates = [x for x in registered if x['pointer'] == pointer]
                need(len(candidates) == 1 and candidates[0]['bucket'] == bucket, 'complete current manager graph')
                raw = blob(candidates[0]['head_hex'],48,'registered node')
                need(word(raw,8) == snap['manager_pointer'], 'registered node backpointer')
                if pointer == node:
                    need(raw == head[:48], 'actual current owner is registered'); found = True
                pointer = word(raw,12)
        need(found and seen == {x['pointer'] for x in registered} and len(seen)==len(registered), 'all current registered nodes')
        if label == 'observed_wait':
            api = unique_return(0x42240D); args = memory_at(regions,api['bp'],16)
            need(struct.unpack('<IIII',args) == (api['saved_bp'],0x42240D,word(head,0x1C),0xffffffff),
                 'original WaitForSingleObject return and two actual stack parameters')
            local = memory_at(regions,api['saved_bp']-8,8)
            need(struct.unpack('<II',local) == (snap['manager_pointer'],node), 'original wait node/manager locals')
            need(word(head,4)&0x10000, 'original wait flag set during paused wait')
    need(heads[0] == heads[1] == heads[2], 'stable node/event/thread/manager across observed wait')
    need(manager_events[0] == manager_events[1] == manager_events[2] != 0, 'stable actual manager event')
    for name,handle in (('node_event',heads[1][3]),('manager_event',manager_events[1])):
        event=source['event_owners'][name]
        need(event['owner_pid']==pid and event['remote_handle']==handle and event['duplicate_succeeded'] is True
             and event['query_status']==0 and event['type_name']=='Event' and event['wait_or_signal_called'] is False,
             'current owned non-consuming Event query')
    need(snapshots['before']['snapshot_end_ns'] <= source['capture_interval']['begin_ns']
         and snapshots['after']['snapshot_begin_ns'] >= source['capture_interval']['end_ns'], 'owner snapshots bracket trace interval')
    return dict(owner_stable=True,current_TLS_verified=True,original_wait_arguments_verified=True,
                original_wait_return=0x42240D,wait_timeout=0xffffffff,wait_handle=heads[1][3],
                PTDcleanup=False,fullABI=False,original_IAT_raw_verified=False)


def verify_kernel_export(source, kernel_image):
    import pefile
    row = source['kernel_wait_export']; info = row['module']
    need(len(kernel_image) == info['bytes'] and hashlib.sha256(kernel_image).hexdigest() == info['sha256'], 'actual guest kernel file identity')
    pe = pefile.PE(data=kernel_image)
    need(pe.FILE_HEADER.Machine == 0x8664 and pe.OPTIONAL_HEADER.SizeOfImage == row['image_size'], 'actual x64 kernel image size')
    exports = [x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name == b'NtWaitForSingleObject']
    need(len(exports) == 1 and not exports[0].forwarder and exports[0].address == row['RVA'], 'actual unforwarded kernel export')
    need(row['symbol'] == 'NtWaitForSingleObject' and row['base'] >= 0xffff800000000000
         and row['base'] % 0x10000 == 0 and row['target'] == row['base']+row['RVA']
         and 0 < row['RVA'] < row['image_size'], 'enumerated kernel base plus original export RVA')
    need(blob(row['export_disk_bytes'],64,'kernel disk export') == pe.get_data(row['RVA'],64), 'raw kernel export bytes')
    need(row['live_kernel_code_read'] is False and row['kernel_symbol_downloaded'] is False,
         'no claimed live kernel instruction identity')
    need(row['method'] == 'EnumDeviceDrivers + GetDeviceDriverFileNameW + actual guest PE export', 'explicit actual module enumeration method')
    return dict(kernel_export_address_verified=True,live_kernel_code_verified=False,target=row['target'],
                module_sha256=info['sha256'])


def verify_api_exports(source, module_loader):
    """module_loader reads explicit retained guest DLLs, never host substitutes."""
    import pefile
    rows = source['API_exports']
    need([x['name'] for x in rows] == ['WaitForSingleObject','NtWaitForSingleObject'], 'both actual WOW64 wait exports')
    receipts = []
    for row in rows:
        data = module_loader(row)
        need(hashlib.sha256(data).hexdigest() == row['module_sha256'], 'actual guest API module SHA')
        pe = pefile.PE(data=data)
        need(pe.FILE_HEADER.Machine == 0x14c, 'actual WOW64 API module')
        matches = [x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name == row['symbol'].encode()]
        need(len(matches)==1 and not matches[0].forwarder and matches[0].address==row['RVA'], 'actual resolved unforwarded API')
        need(row['target']==row['base']+row['RVA'] and row['symbol']==row['name'], 'actual relocated wait entry')
        need(row['slot']==(0x59226C if row['name']=='WaitForSingleObject' else None), 'original wait IAT slot')
        image = pe.get_memory_mapped_image(ImageBase=row['base'])
        need(blob(row['entry_hex'],64,'live API entry')==image[row['RVA']:row['RVA']+64], 'live API bytes match actual relocated DLL')
        iat_verified=False
        if row['slot'] is not None and row.get('IAT_hex') is not None:
            need(word(blob(row['IAT_hex'],4,'actual original IAT'))==row['target'], 'raw original IAT target')
            iat_verified=True
        receipts.append(dict(symbol=row['symbol'],target=row['target'],module_sha256=row['module_sha256'],
                             original_IAT_raw_verified=iat_verified))
    return receipts


def verify_tls_implementation(source,module_loader):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    row=source['TLS_implementation']; data=module_loader(row)
    need(hashlib.sha256(data).hexdigest()==row['module_sha256'], 'actual TLS implementation guest module')
    pe=pefile.PE(data=data);need(pe.FILE_HEADER.Machine==0x14c, 'actual x86 TLS implementation')
    exports=[x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'TlsGetValue']
    need(len(exports)==1 and not exports[0].forwarder and exports[0].address==row['RVA']
         and row['target']==row['base']+row['RVA'], 'actual unforwarded TlsGetValue')
    raw=blob(row['code_hex'],64,'actual live TLS implementation')
    image=pe.get_memory_mapped_image(ImageBase=row['base'])
    need(raw==image[row['RVA']:row['RVA']+64], 'actual relocated TLS bytes')
    instructions=[x.op_str for x in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw,row['target'])]
    need(all(any(value in instruction for instruction in instructions) for value in
             ('fs:[0x18]','0xe10]','0xf94]')), 'actual native FS/TEB/fixed/expansion TLS access')
    return dict(actual_TLS_code_verified=True,module_sha256=row['module_sha256'])


def verify_Nt_wait_context(source,module_loader):
    """Bind the suspended WOW64 stub/stack without interpreting EAX as return.

    The kernel wait's later ETW exit supplies NTSTATUS.  The sampled user context
    is at the call's return PC while the thread is still switched out, so its
    register value must not be promoted to an already completed syscall result.
    """
    import pefile
    matches=[r for r in source['API_exports'] if r['name']=='NtWaitForSingleObject']
    need(len(matches)==1, 'unique actual NtWaitForSingleObject export')
    entry=matches[0];data=module_loader(entry)
    need(hashlib.sha256(data).hexdigest()==entry['module_sha256'], 'actual NtWait guest DLL bytes')
    pe=pefile.PE(data=data);need(pe.FILE_HEADER.Machine==0x14c, 'actual WOW64 NtWait module')
    exports=[x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'NtWaitForSingleObject']
    need(len(exports)==1 and not exports[0].forwarder and exports[0].address==entry['RVA']
         and entry['target']==entry['base']+entry['RVA'], 'actual unforwarded NtWait entry')
    code=blob(entry['entry_hex'],64,'live NtWait stub')
    image=pe.get_memory_mapped_image(ImageBase=entry['base'])
    need(code==image[entry['RVA']:entry['RVA']+64], 'live NtWait bytes match actual relocated DLL')
    return verify_Nt_wait_stack(source,entry,code)


def verify_Nt_wait_stack(source,entry,code):
    """Pure bounded interpretation of the authenticated x86 stub and raw stack."""
    need(len(code)==64 and code[0]==0xb8 and code[5]==0xba and code[10:15]==bytes.fromhex('ffd2c20c00'),
         'actual mov eax/service; mov edx/transition; call edx; ret 12 stub')
    need(0x10000<=word(code,6)<0x80000000, 'actual user-mode WOW64 transition target')
    snap=source['owner_snapshots']['observed_wait'];frame=snap['frame']
    context=blob(frame['context_hex'],716,'suspended WOW64 NtWait context')
    need(frame['tid']==source['subject']['tid'] and frame['EIP']==word(context,184)==entry['target']+12,
         'actual suspended EIP is exact NtWait call return PC')
    esp=word(context,196);need(frame['ESP']==esp, 'actual sampled NtWait ESP')
    raw=memory_at(snap['stack_regions'],esp,16)
    ret,handle,alertable,timeout=struct.unpack('<IIII',raw)
    node=blob(snap['node_hex'],64,'actual wait node')
    need(handle==word(node,0x1c)!=0 and alertable==timeout==0,
         'actual native NT wait arguments: owned event, FALSE, NULL timeout')
    need(0x10000<=ret<0x80000000, 'actual bounded user return address')
    return dict(suspended_Nt_wait_context_verified=True,stub_entry=entry['target'],return_PC=entry['target']+12,
        stub_instruction_bytes_hex=code[:15].hex(),service_number=word(code,1),transition_target=word(code,6),
        stack_pointer=esp,stack_return_address=ret,stack_parameter_bytes_hex=raw[4:].hex(),
        EventHandle=handle,Alertable=alertable,Timeout=timeout,snapshot_EAX=word(context,176),
        snapshot_EAX_is_syscall_result=False,NTSTATUS_source='later ETW SysCallExit, not the suspended snapshot EAX',
        caller_callsite_instruction_verified=False,fullABI=False)


def verify_decode_receipt(source, rows, receipt):
    need(receipt['process_trace_status']==receipt['close_trace_status']==0
         and receipt['callback_errors']==[], 'complete owned offline decode and close')
    need(receipt['retained_subject_records']==len(rows), 'all decoded selected records retained')
    header = receipt['ETL_header']; native_header_check(header,source)
    raw = blob(receipt['ETL_header_raw_hex'],280,'ETL LOGFILE_HEADER')
    original = etw.LOG_HEADER.from_buffer_copy(raw)
    need(all(int(getattr(original,k))==v for k,v in header.items()), 'original ETL header fields')
    need(receipt['first_record']['FILETIME']==header['StartTime']
         and struct.unpack_from('<q',blob(receipt['first_record']['header_hex'],80,'first event header'),16)[0]==header['StartTime'],
         'first native FILETIME exactly equals trace start')
    need(receipt['buffer_reads']==list(range(1,header['BuffersWritten']+1)), 'all sequential ETL buffers consumed')
    pid,tid = source['subject']['pid'],source['subject']['tid']; bindings=receipt['subject_thread_bindings']
    need(0<len(bindings)<=16, 'bounded actual thread lifetime bindings')
    bound=False; anchor=source['owner_snapshots']['observed_wait']
    for b in bindings:
        h=blob(b['header_hex'],80,'lifetime event header'); raw=bytes.fromhex(b['payload_hex'])
        need(b['opcode'] in (1,2,3,4) and h[45]==b['opcode']
             and str(uuid.UUID(bytes_le=h[24:40]))==etw.THREAD_GUID, 'raw lifetime event class')
        need(len(raw)>=8 and struct.unpack_from('<II',raw)==(pid,tid)==(b['pid'],b['tid']), 'raw ETL thread PID/TID binding')
        need(etw.filetime_ns(struct.unpack_from('<q',h,16)[0])==b['ns'], 'raw lifetime time')
        need(b['schema']['event_guid']==etw.THREAD_GUID and b['schema']['provider_guid']==etw.SYSTEM_GUID, 'actual lifetime TDH schema')
        if b['opcode'] in (1,3):
            need(b['ns']<=anchor['snapshot_begin_ns'], 'thread exists before selected wait')
            bound=True
        else:
            need(b['ns']>=anchor['snapshot_end_ns'], 'no target lifetime end before selected wait completes')
    need(bound, 'actual initial thread lifetime binding')


def verify(source, selected_records, decoder_receipt, original_bytes, kernel_bytes, module_loader,diagnostic_only=False):
    """Pure verifier. The caller authenticates source/ETL/frozen implementation."""
    lifecycle=check_source(source,decoder_receipt['ETL'],diagnostic_only=diagnostic_only)
    verify_decode_receipt(source,selected_records,decoder_receipt)
    owners=verify_owners(source,original_bytes)
    kernel=verify_kernel_export(source,kernel_bytes)
    apis=verify_api_exports(source,module_loader)
    owners['original_IAT_raw_verified']=apis[0]['original_IAT_raw_verified']
    tls_code=verify_tls_implementation(source,module_loader)
    native_wait=verify_Nt_wait_context(source,module_loader)
    result=analyze_original_events(selected_records,source)
    result.update(owner=owners,kernel=kernel,API_exports=apis,TLS_implementation=tls_code,Nt_wait_context=native_wait,
        diagnostic_only=diagnostic_only,source_cleanup=lifecycle,
        original_game_wait_observed=True,kernel_symbol_identity=True,
        interpretation='One ETW NTSTATUS zero wait encloses original WOW64 wait stack and current owner snapshot.',
        full_instruction_trace=False,full_resource_lifetime_proved=False)
    return result


def decode_source(source_path, source_sha, etl_path, etl_sha, out,diagnostic_only=False):
    """Guest-only offline reader of an already stopped trace; no new capture."""
    begun=time.monotonic(); qualification=etw.qualify()  # Before every Windows API.
    out=Path(out).resolve(); source_path=Path(source_path).resolve(); etl_path=Path(etl_path).resolve()
    records_path=out.with_suffix('.records.json.gz')
    need(out.parent==ROOT/'analysis' and out.suffix=='.json' and not out.exists()
         and not records_path.exists(), 'fresh guest offline outputs')
    result=dict(kind='original_worker_ETW_wait_decode',status='blocked',accepted=False,
        diagnostic_only=diagnostic_only,
        qualification=qualification,implementation=etw.identity(Path(__file__)),
        reader_implementation=etw.identity(Path(etw.__file__)),errors=[],
        TLS_validator_implementation=etw.identity(ROOT/'devtools/terminal_wait_native_verification.py'),
        new_native_capture=False,fullABI=False,fullstate=False,PTDcleanup=False)
    selected=[]
    try:
        need(result['reader_implementation']['sha256']==READER_SHA, 'frozen low-level reader SHA')
        need(result['TLS_validator_implementation']['sha256']==TLS_VALIDATOR_SHA, 'frozen pure TLS validator SHA')
        need(source_path.stat().st_size<=2*1024*1024 and etl_path.stat().st_size<etw.ETL_LIMIT, 'bounded original source files')
        result['source']=etw.identity(source_path);result['ETL']=etw.identity(etl_path)
        need(result['source']['sha256']==source_sha and result['ETL']['sha256']==etl_sha, 'explicit source/ETL identity')
        raw=source_path.read_bytes()
        if source_path.name.endswith('.gz'):
            with gzip.open(source_path,'rb') as f:raw=f.read(2*1024*1024+1)
        need(len(raw)<=2*1024*1024, 'bounded expanded source')
        source=json.loads(raw); result['source_cleanup']=check_source(source,result['ETL'],diagnostic_only=diagnostic_only)
        def collect(rows, subject, statistics, diagnostics):
            selected.extend(rows)
            return dict(scope='raw original worker records only; no fixture result synthesized')
        globals_=dict(etw._decode_etl.__globals__)
        globals_.update(validate_log_header=native_header_check,analyze_events=collect)
        reader=types.FunctionType(etw._decode_etl.__code__,globals_,etw._decode_etl.__name__,etw._decode_etl.__defaults__)
        adapter=dict(source,helper={k:source['subject'][k] for k in ('pid','tid')})
        reader(etl_path,adapter,result,begun+etw.WALL_SECONDS)
        result['subject_thread_bindings']=result.pop('helper_thread_bindings')
        result['retained_subject_records']=result.pop('retained_helper_records')
        result['retained_sequence_scope']='all original subject syscall records and every subject CSwitch; not full system state'
        packed=gzip.compress(json.dumps(dict(schema_version=1,source=result['source'],ETL=result['ETL'],
            subject=source['subject'],scope=result['retained_sequence_scope'],records=selected),separators=(',',':')).encode(),mtime=0)
        need(len(packed)<=LIMIT, 'all selected raw records must fit 64 KiB; no truncation')
        with records_path.open('xb') as f:f.write(packed)
        result['selected_records']=etw.identity(records_path)
        kernel_path=Path(source['kernel_wait_export']['module']['path'])
        result['analysis']=verify(source,selected,result,(ROOT/'analysis/hermit_game.exe').read_bytes(),
            kernel_path.read_bytes(),lambda row:Path(row['module_path']).read_bytes(),diagnostic_only=diagnostic_only)
        need(etw.identity(source_path)==result['source'] and etw.identity(etl_path)==result['ETL'], 'source artifacts unchanged')
        result['status']=('diagnostic_original_wait_observed_cleanup_unproven' if
            diagnostic_only and not result['source_cleanup']['strict_source_cleanup_verified'] else
            'diagnostic_original_wait_observed' if diagnostic_only else 'single_original_wait_observed')
    except Exception as exc:
        result['errors'].append(repr(exc))
    finally:
        result['elapsed_seconds']=time.monotonic()-begun
        result['implementation_after']=etw.identity(Path(__file__))
        result['reader_implementation_after']=etw.identity(Path(etw.__file__))
        result['TLS_validator_implementation_after']=etw.identity(ROOT/'devtools/terminal_wait_native_verification.py')
        if result['implementation_after']!=result['implementation'] or result['reader_implementation_after']!=result['reader_implementation']:
            result['status']='blocked';result['errors'].append('implementation changed during decode')
        if result['TLS_validator_implementation_after']!=result['TLS_validator_implementation']:
            result['status']='blocked';result['errors'].append('TLS validator changed during decode')
        if result['elapsed_seconds']>etw.WALL_SECONDS:
            result['status']='blocked';result['errors'].append('offline decode deadline exceeded')
        data=json.dumps(result,ensure_ascii=False,indent=2).encode()
        need(len(data)<=128*1024, 'bounded decoder report')
        with out.open('xb') as f:f.write(data+b'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--source-sha',required=True)
    p.add_argument('--etl',type=Path,required=True);p.add_argument('--etl-sha',required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--diagnostic-only',action='store_true',help='Inspect an existing trace with explicitly unobserved CRT exit; never satisfies the strict source cleanup gate.')
    a=p.parse_args()
    r=decode_source(a.source,a.source_sha,a.etl,a.etl_sha,a.out,diagnostic_only=a.diagnostic_only)
    print(json.dumps(dict(status=r['status'],errors=r['errors'],accepted=False)))
    raise SystemExit(0 if r['status']=='single_original_wait_observed' else 2 if r['status'].startswith('diagnostic_') else 1)
