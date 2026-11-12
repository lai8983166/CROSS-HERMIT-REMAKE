"""Offline verification of the owned x86 RW-oplock fixture, never the game.

No native APIs are imported or called. The collector's success flags are not
proof: the returned context, stack, descriptor, TLS and oplock bytes are decoded
again. This source does not establish a current ntdll file identity, CRT PTD,
fault-path qualification, or original-game compatibility.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path, PureWindowsPath
import struct

ROOT = Path(__file__).resolve().parents[1]
MAX_SOURCE = 2 * 1024 * 1024
PAYLOAD = bytes((i * 17 + 3) & 255 for i in range(64))
# Exact frozen files independently read for this review. Never import collectors.
DEPENDENCIES = {
    'devtools/terminal_oplock.py': (7991, 'b7b834d038522993deccb3a8684c7a7361f208aa32f2e6de4323b38456d66ada'),
    'devtools/terminal_oplock_probe.py': (18446, 'cbea3861e6a94a883ad42177ca3d79855272667efbd52cf2328bdfc51bd9f778'),
    'devtools/terminal_oplock_probe_v2.py': (19525, 'e84369233125cfbad3ba0d3dc8a380eb9ddc1168d0a4d726c72423e9db1794c9'),
    'devtools/terminal_oplock_fixture.cs': (8910, '8ee034d29352e3c53003698cfe3b07cdb49ba65d45823a047b43b7c4e5440eff'),
    'devtools/terminal_host_desktop.py': (8215, 'c2e5781af633e83db4d93e507971ef7a04ddf3601b0313f54698360110d24b76'),
    'tools/school_native_dialogue_desktop.py': (2420, '962ab2a19dc40482778b74d60099464c1b0be3181b30d28f4a2ee4e72568c7ee'),
}
FAULT_DEPENDENCIES = dict(DEPENDENCIES, **{
    'devtools/terminal_oplock_fault_precheck.py': (3757, 'b318c79ddafc31d1c6a8791552a7a4d0435e55b1b6571c009631d542a6518c42'),
})
FAULT_BINARY = (23552, 'dd3ec3b8c449050093db4dd769867b8d0ab4faeee74897cfd432be50ea98e4e8')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def raw(value, size=None):
    need(isinstance(value, str) and len(value) <= MAX_SOURCE * 2, 'bounded hex field')
    data = bytes.fromhex(value)
    need(size is None or len(data) == size, 'complete raw field')
    return data


def u32(data, offset=0):
    return struct.unpack_from('<I', data, offset)[0]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_identity(path):
    path = Path(path)
    need(path.stat().st_size <= 16 * 1024 * 1024, 'bounded identity file')
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=digest(data))


def same_file(record):
    current = file_identity(record['path'])
    need((current['bytes'], current['sha256']) == (record['bytes'], record['sha256']),
         'authenticated file changed: ' + record['path'])


def windows_path(value):
    return str(PureWindowsPath(value)).casefold()


def verify_desktop(report):
    # Pure comparisons, deliberately independent of collector health flags.
    baseline = report['desktop_before']
    after = report['desktop_after']
    need(len(after) == 2, 'two desktop restoration observations')
    for state in [baseline] + after:
        need(state['desktop_state_written'] is False and state['game_window'] == 0
             and state['shell_window'] and state['monitors'] and state['taskbars'],
             'healthy untouched desktop')
        desk = state['input_desktop']
        need(desk['ready'] is True and desk['open_input_desktop_error'] == 0
             and desk['desktop_or_window_state_written'] is False
             and desk['input_submitted'] is False, 'ready desktop without input')
        for monitor in state['monitors']:
            l, t, r, b = monitor['screen']; wl, wt, wr, wb = monitor['work']
            need(l <= wl < wr <= r and t <= wt < wb <= b, 'valid desktop work area')
            need(state['auto_hide'] or not monitor['primary'] or monitor['work'] != monitor['screen'],
                 'primary taskbar work area')
        for bar in state['taskbars']:
            l, t, r, b = bar['rect']
            need(not bar['hung'] and (state['auto_hide'] or (bar['visible'] and min(r-l, b-t) > 1)),
                 'healthy taskbar')
            need(any(l < m['screen'][2] and r > m['screen'][0] and t < m['screen'][3]
                     and b > m['screen'][1] for m in state['monitors']), 'onscreen taskbar')
    for state in after:
        for key in ('monitors', 'metrics', 'appbar_state', 'auto_hide'):
            need(state[key] == baseline[key], 'desktop changed: ' + key)
        geometry = lambda s: sorted((tuple(x['rect']), x['visible']) for x in s['taskbars'])
        need(geometry(state) == geometry(baseline), 'taskbar geometry restored')
        for key in ('input_desktop', 'observer_desktop', 'foreground_hwnd', 'foreground_pid', 'foreground_image'):
            need(state['input_desktop'][key] == baseline['input_desktop'][key], 'desktop identity restored: ' + key)
    need(baseline['time_ns'] < after[0]['time_ns'] < after[1]['time_ns']
         and after[1]['time_ns'] - after[0]['time_ns'] >= 900_000_000, 'separate desktop checks')
    need(report['desktop_checks'] == [[], []], 'collector desktop receipt consistent')


def verify_case(case):
    need(case['error'] is None and case['accepted'] is False
         and not case.get('oplock_cleanup_error') and case['read_handle_cleanup_errors'] == [], 'clean fixture case')
    child = case['child']['result']; meta = case['meta']; parent = case['parent']
    debugger = case['debugger']; owner = case['owner']
    pid, tid, index, pointer = (child[k] for k in ('pid', 'tid', 'index', 'pointer'))
    need(0 < pid < 2**32 and 0 < tid < 2**32 and 0 <= index < 64 and 0 < pointer < 2**32,
         'bounded fixture owner')
    need(all(meta[k] == child[k] for k in ('pid', 'tid', 'index', 'pointer', 'frequency')), 'metadata worker generation')
    need(meta['debug_port'] == 0xffffffff and child['frequency'] == 10_000_000, 'fixture debug port and recorded QPC frequency')
    need(parent['child_pid'] == pid == debugger['child_pid']
         and parent['parent_pid'] == debugger['parent_pid'] == owner['parent_pid'] != pid
         and parent['child_main_tid'] != tid, 'fixture debugger parent binding')
    need(child['error'] is None and child['cleared'] is True and child['freed'] is True
         and case['child']['tls_freed'] is True, 'reported normal fixture TLS cleanup')
    need(child['got'] == 64 and raw(child['data_hex'], 64) == PAYLOAD, 'exact ordinary read result')
    need(0 < child['ready'] <= child['before'] < child['after'] <= child['ended'], 'worker QPC order')
    need(case['input'] == case['input_after'] and case['input']['bytes'] == 64
         and case['input']['sha256'] == digest(PAYLOAD), 'unchanged file bytes')
    need(debugger['error'] is None and debugger['cleanup'] == [] and debugger['exited'] is True
         and debugger['forced'] is False and debugger['exit_code'] == 0, 'original owner normal debug completion')
    need(owner['forced'] is False and owner['job_empty'] is True and owner['handles_closed'] is True
         and owner['errors'] == [] and owner['exits'] == {str(parent['parent_pid']): {'wait': 0, 'code': 0}},
         'normal Job, parent and owned handle cleanup')
    events = debugger['events']; need(2 <= len(events) <= 512, 'bounded original debug ledger')
    active = set(); created = set(); worker_create = worker_exit = None; last = 0
    for i, event in enumerate(events):
        code, etid = event['code'], event['tid']
        need(event['pid'] == pid and 1 <= code <= 9 and event['qpc'] >= last
             and not event.get('drain'), 'owned monotonic normal debug ledger')
        last = event['qpc']
        expected = (0x10002 if event['value'] in (0x80000003, 0x4000001f) else 0x80010001) if code == 1 else 0x10002
        need(event['status'] == expected, 'original debugger continuation policy')
        if code in (2, 3):
            need(etid not in created and (code != 3 or (i == 0 and etid == parent['child_main_tid'])), 'thread creation generation')
            created.add(etid); active.add(etid)
            if etid == tid: worker_create = event['qpc']
        else:
            need(etid in active, 'debug event belongs to live original thread')
        if code == 4:
            need(event['value'] == 0, 'normal thread exit event')
            active.remove(etid)
            if etid == tid: worker_exit = event['qpc']
        if code == 5:
            need(i == len(events)-1 and event['value'] == 0, 'final original process exit0')
            active.discard(etid)
    need(events[0]['code'] == 3 and events[-1]['code'] == 5 and not active, 'complete debug thread lifecycle')
    need(worker_create is not None and worker_exit is not None
         and worker_create < child['ready'] <= child['ended'] <= worker_exit, 'same worker creation and exit around TLS')
    need(not any(child['ready'] <= e['qpc'] <= child['ended'] for e in events),
         'no debug notification in worker TLS execution interval')
    if not case['gated']:
        need('capture' not in case and 'oplock' not in case and 'worker_exit' not in case, 'ordinary baseline without observer hold')
    return dict(pid=pid, tid=tid, parent_pid=parent['parent_pid'], frequency=child['frequency'],
                worker_create_qpc=worker_create, worker_exit_qpc=worker_exit,
                open_ticks=child['after']-child['before'], debug_events=len(events))


def verify_capture(case):
    cap = case['capture']; meta = case['meta']; child = case['child']['result']; lock = case['oplock']
    ctx = raw(cap['context_hex'], 716)
    need(ctx == raw(cap['context_after_hex'], 716) and u32(ctx) == 0x1003f, 'full unchanged WOW64 context')
    need(cap['suspend_previous'] == 0 and cap['resume_previous'] == 1 and 0 < cap['suspend_ns'] < 250_000_000,
         'single bounded owned suspend increment restored')
    descriptor = raw(cap['descriptor_hex'], 8)
    teb = struct.unpack_from('<H', descriptor, 2)[0] | descriptor[4] << 16 | descriptor[7] << 24
    need(u32(ctx, 144) == cap['FS'] and cap['FS'] & 3 == 3 and teb == cap['TEB'], 'actual FS selector and descriptor')
    head = raw(cap['TEB_hex'], 48)
    need(u32(head, 24) == teb and struct.unpack_from('<2I', head, 32) == (meta['pid'], meta['tid']), 'actual TEB owner')
    need(cap['slot'] == teb + 0xe10 + 4 * meta['index']
         and u32(raw(cap['slot_hex'], 4)) == meta['pointer'], 'actual live TLS slot')
    payload = bytearray((i * 13 + 7) & 255 for i in range(116))
    struct.pack_into('<6I', payload, 0, 0x544c5350, meta['pid'], meta['tid'], meta['index'], 0x1234abcd, meta['pointer'])
    need(raw(cap['payload_hex'], 116) == payload, 'entire 116-byte TLS payload')
    process = cap['process']; basic = raw(process['basic_hex'], 48)
    need(process['debug_port'] == 0xffffffffffffffff
         and process['pid'] == meta['pid'] == struct.unpack_from('<Q', basic, 32)[0]
         and process['parent_pid'] == case['parent']['parent_pid'] == struct.unpack_from('<Q', basic, 40)[0],
         'current process and original debugger parent')
    esp, eip = u32(ctx, 196), u32(ctx, 184)
    stack = raw(cap['stack_hex']); stackbase, stacklimit = struct.unpack_from('<2I', head, 4)
    need(stacklimit <= esp < stackbase and cap['stack_address'] == esp
         and len(stack) == min(4096, stackbase-esp) and len(stack) >= 48, 'actual bounded original stack')
    stub = raw(cap['nt_create_code_hex'], 32); code = raw(cap['code_hex'], 32)
    nt = meta['nt_create_file']
    need(cap['nt_create_file'] == nt and cap['EIP'] == eip == nt + 12
         and stub[0] == 0xb8 and stub[5] == 0xba and stub[10:16] == bytes.fromhex('ffd2c22c0090')
         and code[:20] == stub[12:], 'observed WOW64 syscall CALL then RET 2c stub')
    frames = [f for f in cap['syscall_frames'] if f.get('layout') == 'wow64_saved_after_transition']
    need(len(frames) == 1, 'one actual original syscall filename frame required')
    frame = frames[0]; args = struct.unpack_from('<11I', stack, 4)
    need(frame['offset'] == 0 and frame['argument_skip'] == 4 and not frame.get('error')
         and frame['caller_return'] == u32(stack) and frame['args'] == list(args), 'syscall arguments from original stack')
    # NtCreateFile args: HANDLE*, ACCESS, OA*, IOSB*, allocation, attributes,
    # share, disposition, options, EA*, EA length. The observed Win32 call uses
    # GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING, FILE_ATTRIBUTE_READONLY.
    need(args[1] == 0x80100080 and args[4:] == (0, 1, 1, 1, 0x60, 0, 0)
         and stacklimit <= args[0] <= stackbase-4 and stacklimit <= args[3] <= stackbase-8,
         'original read-only open arguments without complete-if-oplocked')
    oa = raw(frame['object_attributes_hex'], 24); us = raw(frame['unicode_string_hex'], 8)
    need(u32(oa) == 24 and u32(oa, 4) == 0 and u32(oa, 12) == 0x40 and u32(oa, 16) == 0,
         'original absolute case-insensitive object attributes')
    # Both structures are inside the captured stack: bind separate memory
    # reads to the actual pointers, not merely to collector-provided labels.
    def stack_slice(address, size):
        offset = address-esp
        need(0 <= offset <= len(stack)-size, 'object structure within recorded original stack')
        return stack[offset:offset+size]
    need(stack_slice(args[2], 24) == oa and stack_slice(u32(oa, 8), 8) == us,
         'OBJECT_ATTRIBUTES and UNICODE_STRING pointer binding')
    length, maximum, nameptr = struct.unpack('<HHI', us)
    name = raw(frame['name_hex'])
    need(0 < length <= maximum <= 2048 and length % 2 == 0 and len(name) == length and 0 < nameptr < 2**32,
         'complete bounded original Unicode name')
    decoded = name.decode('utf-16-le')
    need(decoded.startswith('\\??\\') and windows_path(decoded[4:]) == windows_path(case['input']['path'])
         == windows_path(lock['path']), 'original NtCreateFile names exact locked payload')
    output = raw(lock['output_hex'], 24)
    need(struct.unpack('<HHIIIIH2x', output) == (1, 24, 5, 1, 1, 0, 0), 'raw RW-to-R break requiring ACK')
    need(lock['access'] == 0x80000000 and lock['share'] == 7 and lock['flags'] == 0x40000000
         and lock['requested_level'] == 5 and lock['request_error'] == 997 and lock['internal'] == 0,
         'actual read-only asynchronous RW grant and normal break')
    need(lock['watchdog_release'] is False and all(lock[k] is True for k in ('file_closed', 'async_completed', 'event_closed')),
         'normal implicit close ACK and completed async lifetime')
    need(lock['arm_qpc'] < child['ready'] <= child['before'] <= lock['break_qpc']
         <= cap['captured_qpc'] < lock['release_begin_qpc'] <= child['after'], 'original I/O held across live capture')
    need(lock['arm_ns'] < lock['break_ns'] <= cap['captured_ns'] <= case['before_release_ns'] <= lock['release_ns']
         <= case['worker_exit']['qpc_ns'] and case['return_file_before_release'] is False, 'observer clock and release order')
    frequency = child['frequency']
    # Same QPC basis, allowing only bounded time between sequential API reads.
    for ticks, ns in ((lock['arm_qpc'], lock['arm_ns']), (lock['break_qpc'], lock['break_ns']),
                      (cap['captured_qpc'], cap['captured_ns'])):
        need(0 <= ticks * 1_000_000_000 // frequency - ns <= 10_000_000, 'QPC/perf-counter cross-check')
    need(0 < lock['release_ns']-lock['arm_ns'] < 15_000_000_000
         and case['worker_exit']['wait'] == 0 and case['worker_exit']['code'] == 0, 'bounded lock and retained worker exit0')
    need(case['worker_exit']['qpc_ns'] >= child['ended'] * 1_000_000_000 // frequency,
         'retained exit follows actual worker execution')
    return dict(filename=decoded, EIP=eip, nt_create_file=nt, TLS_bytes=116,
                hold_ticks=lock['release_begin_qpc']-lock['break_qpc'], suspend_ns=cap['suspend_ns'])


def verify(report, *, check_disk=True):
    need(report['kind'] == 'owned_original_debugger_RW_oplock_preflight' and report['accepted'] is False
         and report['error'] is None, 'owned fixture source only')
    need(all(report[k] is False for k in ('game_started', 'observer_debug_attachment', 'game_or_thread_memory_writes')),
         'no game, external debugger or target writes')
    need(report['build']['code'] == 0 and report['implementations_unchanged'] is True, 'frozen successful fixture build')
    need(len(report['cases']) == 2 and [c['gated'] for c in report['cases']] == [False, True], 'baseline then one gated fixture')
    cases = [verify_case(c) for c in report['cases']]
    need(len({c['pid'] for c in cases}) == 2 and len({c['parent_pid'] for c in cases}) == 2, 'two distinct owned process lifetimes')
    capture = verify_capture(report['cases'][1])
    verify_desktop(report)
    expected = {windows_path(str(ROOT / p)): value for p, value in DEPENDENCIES.items()}
    actual = {windows_path(r['path']): (r['bytes'], r['sha256']) for r in report['implementations']}
    need(len(report['implementations']) == len(expected) and actual == expected, 'complete frozen implementation provenance')
    if check_disk:
        for record in report['implementations'] + [report['compiler'], report['binary']]:
            same_file(record)
        for case in report['cases']:
            same_file(case['input'])
            directory = Path(case['input']['path']).parent
            for name, field in (('worker.json', 'meta'), ('parent.json', 'parent'),
                                ('child.json', 'child'), ('debugger.json', 'debugger')):
                need(json.loads((directory/name).read_text(encoding='utf-8-sig')) == case[field], 'original helper sidecar: ' + name)
        binary = Path(report['binary']['path']).read_bytes(); pe = u32(binary, 0x3c)
        need(binary[:2] == b'MZ' and binary[pe:pe+4] == b'PE\0\0'
             and struct.unpack_from('<H', binary, pe+4)[0] == 0x14c
             and struct.unpack_from('<H', binary, pe+24)[0] == 0x10b
             and struct.unpack_from('<H', binary, pe+24+68)[0] == 2, 'actual PE32 GUI-subsystem helper')
    return dict(schema_version=1, kind='independent_owned_RW_oplock_verification', accepted=False,
                fixture_capture_passed=True, original_game_adaptation_eligible=False,
                full_game_acceptance=False, fault_cleanup_qualified=False,
                native_api_module_file_authenticated=False, recorded_QPC_frequency=10_000_000,
                disk_identity_checked=check_disk, cases=cases, capture=capture,
                limits=['Self-owned 116-byte TLS payload is not game CRT PTD.',
                        'TLS clear/free is helper-reported and followed by original debug exit and retained-handle exit0.',
                        'Current ntdll export bytes are recorded; complete ntdll image/file identity was not collected.',
                        'Normal fixture cleanup is verified; fault qualification and game adapter remain separate.'])


def verify_faults(report, *, check_disk=True):
    """Verify only the three recorded faults, not all failure paths.

    The injected observer fails before SuspendThread/capture, and its Job is
    force-terminated. Never upgrade that containment to normal worker exit or
    to recovery from a failure while a target thread is suspended.
    """
    need(report['kind'] == 'RW_oplock_fault_precheck' and report['error'] is None
         and report['accepted'] is False and report['game_started'] is False
         and report['sources_unchanged'] is True, 'frozen bounded fault source')
    names = ['no_opener_cancel', 'watchdog_close', 'capture_failure']
    need([c['name'] for c in report['cases']] == names, 'exact three bounded fault cases')
    expected = {windows_path(str(ROOT/p)): value for p, value in FAULT_DEPENDENCIES.items()}
    actual = {windows_path(r['path']): (r['bytes'], r['sha256']) for r in report['sources']}
    need(len(report['sources']) == len(expected) and actual == expected, 'complete frozen fault provenance')
    need((report['binary']['bytes'], report['binary']['sha256']) == FAULT_BINARY,
         'same qualified owned fixture binary')
    verify_desktop(dict(desktop_before=report['before'], desktop_after=report['after'],
                        desktop_checks=report['desktop_checks']))
    summaries = []; previous_end = 0
    for position, case in enumerate(report['cases']):
        if position < 2:
            before, after, lock = case['before'], case['after'], case['oplock']
        else:
            result = case['result']
            before, after, lock = result['input'], result['input_after'], result['oplock']
        need(before == after and before['bytes'] == 64 and before['sha256'] == digest(PAYLOAD)
             and windows_path(before['path']) == windows_path(lock['path']), 'fault file bytes and owner unchanged')
        need(lock['access'] == 0x80000000 and lock['share'] == 7 and lock['flags'] == 0x40000000
             and lock['requested_level'] == 5 and lock['request_error'] == 997, 'fault real asynchronous RW grant')
        need(all(lock[k] is True for k in ('file_closed', 'async_completed', 'event_closed')),
             'fault close ACK and async/event cleanup')
        need(previous_end < lock['arm_ns'] < lock['release_ns'] and lock['arm_qpc'] < lock['release_begin_qpc'],
             'sequential fault lifetime')
        need(0 <= lock['arm_qpc'] * 100 - lock['arm_ns'] <= 10_000_000
             and 0 <= lock['release_ns'] - lock['release_begin_qpc'] * 100 <= 10_000_000,
             'fault QPC/perf-counter cross-check at recorded 10MHz')
        previous_end = lock['release_ns']
        duration = lock['release_ns'] - lock['arm_ns']
        summary = dict(name=case['name'], lock_lifetime_ns=duration, normal_worker_exit_proved=False)
        if position < 2:
            need(lock['break_ns'] is None and all(k not in lock for k in ('break_qpc', 'internal', 'output_hex')),
                 'no fabricated external break without opener')
            need(lock['watchdog_release'] is (position == 1), 'correct fault release owner')
            low, high = (50_000_000, 2_000_000_000) if position == 0 else (200_000_000, 1_000_000_000)
            need(low <= duration < high, 'bounded no-opener or watchdog completion')
            need(PureWindowsPath(before['path']).name == case['name']+'.bin', 'own fault file')
            summary['pending_close_completed'] = True
        else:
            need(result['gated'] is True and result['accepted'] is False
                 and result['error'] == "RuntimeError('injected owned observer failure after real break')"
                 and result['read_handle_cleanup_errors'] == [] and not result.get('oplock_cleanup_error'),
                 'exact pre-capture fault and clean observer handles')
            need(all(k not in result for k in ('capture', 'worker_exit', 'child', 'debugger')),
                 'failed capture must not invent normal capture or exit evidence')
            need(lock['watchdog_release'] is False and lock['internal'] == 0
                 and struct.unpack('<HHIIIIH2x', raw(lock['output_hex'], 24)) == (1, 24, 5, 1, 1, 0, 0),
                 'fault follows actual RW-to-R ACK-required break')
            need(lock['arm_qpc'] < lock['break_qpc'] < lock['release_begin_qpc']
                 and lock['arm_ns'] < lock['break_ns'] < lock['release_ns']
                 and 0 <= lock['break_qpc']*100-lock['break_ns'] <= 10_000_000
                 and duration < 15_000_000_000, 'bounded actual break then exceptional close')
            owner = result['owner']; parent = owner['parent_pid']; exits = owner['exits']
            need(owner['forced'] is True and owner['job_empty'] is True and owner['handles_closed'] is True
                 and owner['errors'] == [] and len(exits) == 2
                 and exits[str(parent)] == {'wait': 0, 'code': 94}, 'explicit forced Job containment')
            child = next(key for key in exits if key != str(parent))
            need(0 < int(child) < 2**32 and exits[child] == {'wait': 0}, 'other retained Job member actually signaled')
            summary.update(parent_pid=parent, child_pid=int(child), forced_job_containment_verified=True,
                           failure_before_target_suspend=True)
            if check_disk:
                directory = Path(before['path']).parent
                p = json.loads((directory/'parent.json').read_text(encoding='utf-8-sig'))
                m = json.loads((directory/'worker.json').read_text(encoding='utf-8-sig'))
                need(p['parent_pid'] == parent and p['child_pid'] == int(child) == m['pid']
                     and m['debug_port'] == 0xffffffff and m['frequency'] == 10_000_000,
                     'forced Job members bound to original helper sidecars')
        if check_disk:
            same_file(before)
        summaries.append(summary)
    if check_disk:
        for record in report['sources'] + [report['binary']]:
            same_file(record)
    return dict(schema_version=1, kind='independent_RW_oplock_fault_prechecks', accepted=False,
                fault_prechecks_passed=True, all_fault_paths_qualified=False,
                original_game_adaptation_eligible=False, disk_identity_checked=check_disk,
                cases=summaries,
                limits=['Close/event completion is recorded; no-opener final NTSTATUS bytes were not collected.',
                        'capture_failure is pre-suspend injected failure with forced Job containment, not natural exit.',
                        'Suspended-thread failures, failed OS cleanup APIs and original-game behavior remain outside these three cases.'])


def read_source(path):
    path = Path(path); need(path.stat().st_size <= MAX_SOURCE, 'bounded source file')
    original = path.read_bytes()
    if path.suffix == '.gz':
        with gzip.open(path, 'rb') as stream:
            data = stream.read(MAX_SOURCE+1)
    else:
        data = original
    need(len(data) <= MAX_SOURCE, 'bounded uncompressed source')
    return json.loads(data), dict(path=str(path), bytes=len(original), sha256=digest(original),
                                 uncompressed_bytes=len(data), uncompressed_sha256=digest(data))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--fault-source', type=Path)
    parser.add_argument('--fault-source-sha256')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh proof output required')
    report, source = read_source(args.source)
    need(source['sha256'] == args.source_sha256.lower(), 'exact supplied source digest')
    need(bool(args.fault_source) == bool(args.fault_source_sha256), 'fault source and digest supplied together')
    faults = fault_source = None
    if args.fault_source:
        faults, fault_source = read_source(args.fault_source)
        need(fault_source['sha256'] == args.fault_source_sha256.lower(), 'exact supplied fault source digest')
    try:
        proof = verify(report)
        if faults is not None:
            proof['schema_version'] = 2
            proof['faults'] = verify_faults(faults)
            proof['faults']['source'] = fault_source
            proof['limits'][-1] = 'Normal cleanup and the three named fault prechecks passed; other faults and the game adapter remain separate.'
    except (ValueError, KeyError, TypeError, IndexError, struct.error, OSError) as exc:
        proof = dict(schema_version=1, kind='independent_owned_RW_oplock_verification', accepted=False,
                     fixture_capture_passed=False, original_game_adaptation_eligible=False,
                     full_game_acceptance=False, error=str(exc))
    proof['source'] = source
    proof['verifier'] = file_identity(__file__)
    with args.out.open('x', encoding='utf-8') as stream:
        json.dump(proof, stream, indent=2)
    print(json.dumps({'fixture_capture_passed': proof['fixture_capture_passed'], 'error': proof.get('error')}))
    return 0 if proof['fixture_capture_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
