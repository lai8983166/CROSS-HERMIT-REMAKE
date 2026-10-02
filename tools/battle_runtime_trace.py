#!/usr/bin/env python3
"""Read-only, bounded polling of the original game; never authorizes save writes.

python tools/battle_runtime_trace.py --pid PID --seconds 30 --out NEW.jsonl
The state slot is a REQUEST/DISPATCH slot, not proof that a task ran.
Equal endpoint reads do not make a snapshot atomic or prove call provenance.
"""
import argparse
import csv
import ctypes
import ctypes.wintypes as wt
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
BASE = 0x400000
SOURCE = ROOT / 'analysis/hermit_game.exe'
GAME = ROOT / 'CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
SCENE5_SCRIPT = GAME.parent / 'DATA/TACTICS/SCRIPT/T0005.BIN'
PROBES = ((0x439EAC, 13), (0x49E2B0, 32), (0x454A7A, 6),
          (0x4CE5C4, 4), (0x4DA93A, 7), (0x73C3D0, 20))


class TraceError(Exception):
    pass


def unpack(data, fmt, offset=0):
    return struct.unpack_from('<' + fmt, data, offset)[0]


def verify_image(read, source):
    """Require all source probes; the packer may erase the live PE header."""
    header = read(BASE, 0x1000)
    if header[:2] != b'MZ':
        raise TraceError('expected fixed image base 0x400000 (MZ missing)')
    pe = unpack(header, 'I', 0x3c)
    has_pe = pe <= len(header) - 84 and header[pe:pe+4] == b'PE\0\0'
    if has_pe:
        if (unpack(header, 'H', pe + 4) != 0x14c or
                unpack(header, 'H', pe + 24) != 0x10b or
                unpack(header, 'I', pe + 52) != BASE):
            raise TraceError('expected fixed-base x86 PE32')
        if unpack(header, 'I', pe + 80) < 0x7F4492 - BASE:
            raise TraceError('image does not cover audited globals')
    for address, size in PROBES:
        expected = source[address-BASE:address-BASE+size]
        if len(expected) != size or read(address, size) != expected:
            raise TraceError(f'unpacked source probe mismatch at {address:#x}')
    return {'source_sha256': hashlib.sha256(source).hexdigest(),
            'header_status': 'pe32' if has_pe else 'pe_header_unavailable',
            'probes': [{'va': hex(a), 'size': n} for a, n in PROBES],
            'coverage': 'selected probes only, not a full live-image hash'}


def resolve_scene5_script(take, file_pointer, vm, source):
    """Match the whole loaded file, then both subrecord and code pointers.

    This identifies the selected record, NOT the call that selected it.
    """
    unresolved = {'status': 'unresolved', 'authorizes_persistent_write': False}
    if not file_pointer or not vm or source is None:
        return unresolved
    if not 8 <= len(source) <= 0x10000:
        raise TraceError('scene5 source file size outside collector bound')
    if take(file_pointer, len(source)) != source:
        return {**unresolved, 'reason': 'loaded_script_differs_from_T0005'}
    block_count = unpack(source, 'I', 4)
    if not 0 < block_count <= 128 or 8 + block_count*4 > len(source):
        raise TraceError('invalid scene5 block table')
    matches = []
    for block in range(block_count):
        start = unpack(source, 'I', 8 + block*4)
        if start + 8 > len(source):
            raise TraceError('invalid scene5 block offset')
        count = unpack(source, 'I', start+4)
        if count > 1024 or start + 8 + count*4 > len(source):
            raise TraceError('invalid scene5 subrecord table')
        for sub in range(count):
            offset = unpack(source, 'I', start+8+sub*4)
            record = start+offset
            if not offset or record + 8 > len(source) or unpack(source, 'I', record) != 4:
                continue
            code = record + unpack(source, 'I', record+4)
            if not record <= code < len(source):
                continue
            if (int(vm['subrecord_pointer'], 0) == file_pointer+record and
                    int(vm['code_pointer'], 0) == file_pointer+code):
                matches.append({'block': block, 'sub': sub, 'subrecord_file_offset': record,
                                'code_file_offset': code})
    if len(matches) != 1:
        return {**unresolved, 'reason': 'subrecord_and_code_pointers_not_unique_match'}
    return {'status': 'selected_record_observed', **matches[0],
            'script_sha256': hashlib.sha256(source).hexdigest(),
            'is_terminal_candidate': matches[0]['block'] == 0 and matches[0]['sub'] in (2, 5, 8, 11, 14),
            'call_site_proven': False, 'authorizes_persistent_write': False}


def sample(read, scene5_source=None):
    """Capture audited raw fields, rejecting endpoint changes/partial reads."""
    observed = []

    def take(address, size):
        data = read(address, size)
        if len(data) != size:
            raise TraceError(f'partial read at {address:#x}')
        observed.append((address, data))
        return data

    try:
        controller = unpack(take(0x7A4A00, 4), 'I')
        if not 0x10000 <= controller < 0xFFFF0000:
            raise TraceError('controller absent or invalid')
        control = take(controller + 0x2c, 8)
        state = unpack(control, 'I', 4)
        calendar = take(0x7A528E, 12)
        scene = take(0x7F4488, 10)
        count = unpack(take(0x7A5260, 2), 'H')
        # The audited ID table occupies 0x50 bytes before its count field.
        if count > 40:
            raise TraceError('participant count exceeds audited table extent')
        ids = list(struct.unpack('<' + 'h' * count, take(0x7A5210, count*2)))
        groups = [list(struct.unpack('<4h', take(0x7AAA22 + g*0x1c, 8)))
                  for g in range(5)]
        indexes = list(struct.unpack('<20h', take(0x7AAAE0, 40)))
        first_round = take(0x7A52D0, 0x3a)
        first_count = unpack(first_round, 'H', 0x28)
        if first_count > 20:
            raise TraceError('first-round count exceeds audited table extent')
        result = {'controller_pointer': hex(controller),
                  'request_pending': unpack(control, 'I'),
                  'request_dispatch_state': state,
                  'month': unpack(calendar, 'h'), 'week': unpack(calendar, 'h', 2),
                  'current_round': unpack(calendar, 'h', 8),
                  'total_rounds': unpack(calendar, 'h', 10),
                  'scene_id': unpack(scene, 'H'), 'mode_flag': scene[9],
                  'selected_task_id': unpack(take(0x7AAB16, 2), 'h'),
                  'participant_ids': ids, 'group_member_ids': groups,
                  'group_participant_indexes': [indexes[i:i+4] for i in range(0, 20, 4)],
                  'first_round_config_id': unpack(first_round, 'h', 0x38),
                  'first_round_member_ids': list(struct.unpack(
                      '<' + 'h'*first_count, first_round[:first_count*2])),
                  'tactics': None}
        # Outside slot 16 the old global may refer to a destroyed task.
        if state == 16:
            task = unpack(take(0x7A4174, 4), 'I')
            if not 0x10000 <= task < 0xFFFF0000:
                raise TraceError('tactics pointer absent or invalid in slot 16')
            data = take(task, 0x178)
            if unpack(data, 'I') != 0x59A430:
                raise TraceError('tactics vtable mismatch')
            vm = unpack(data, 'I', 0x60)
            tactics = {'pointer': hex(task), 'task_phase': unpack(data, 'I', 0x34),
                       'transition_phase': unpack(data, 'I', 0x38),
                       'script_control_active': data[0x43],
                       'script_phase': data[0x44],
                       'execute_vm': unpack(data, 'I', 0x48),
                       'exit_flag': unpack(data, 'I', 0x4c),
                       'control_phase': data[0x58],
                       'script_completion_phase': data[0x59],
                       'finish_flags': list(data[0x170:0x173]),
                       'result_selector': unpack(data, 'I', 0x174),
                       'script_file_pointer': hex(unpack(data, 'I', 0x64)),
                       'vm': None}
            if vm:
                if not 0x10000 <= vm < 0xFFFF0000:
                    raise TraceError('invalid VM pointer')
                v = take(vm, 0x26)
                tactics['vm'] = {'pointer': hex(vm), 'active': v[4],
                                 'subrecord_pointer': hex(unpack(v, 'I', 0xc)),
                                 'code_pointer': hex(unpack(v, 'I', 0x10)),
                                 'pc': unpack(v, 'I', 0x1c),
                                 'wait_state': unpack(v, 'H', 0x20),
                                 'opcode_slot': unpack(v, 'H', 0x22),
                                 'script_work_wait': take(vm + 0x92e0, 1)[0]}
            result['tactics'] = tactics
            if result['scene_id'] == 5:
                tactics['scene5_script_selection'] = resolve_scene5_script(
                    take, unpack(data, 'I', 0x64), tactics['vm'], scene5_source)
        for address, data in reversed(observed):
            if read(address, len(data)) != data:
                raise TraceError(f'endpoint changed at {address:#x}')
        return {'valid': True, 'observation': result,
                'consistency': 'equal_endpoints_not_atomic',
                'authorizes_persistent_write': False}
    except (OSError, TraceError, struct.error) as error:
        return {'valid': False, 'error': str(error),
                'authorizes_persistent_write': False}


class ProcessReader:
    """Explicit 64-bit-safe Win32 prototypes; no write/debug/suspend rights."""
    def __init__(self, pid):
        if os.name != 'nt':
            raise TraceError('live capture requires Windows')
        self.k = ctypes.WinDLL('kernel32', use_last_error=True)
        signatures = {
            'OpenProcess': ([wt.DWORD, wt.BOOL, wt.DWORD], wt.HANDLE),
            'CloseHandle': ([wt.HANDLE], wt.BOOL),
            'ReadProcessMemory': ([wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p,
                                   ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)], wt.BOOL),
            'QueryFullProcessImageNameW': ([wt.HANDLE, wt.DWORD, wt.LPWSTR,
                                           ctypes.POINTER(wt.DWORD)], wt.BOOL),
            'GetProcessTimes': ([wt.HANDLE] + [ctypes.POINTER(wt.FILETIME)]*4, wt.BOOL)}
        for name, (args, result) in signatures.items():
            fn = getattr(self.k, name)
            fn.argtypes, fn.restype = args, result
        self.handle = self.k.OpenProcess(0x10 | 0x400, False, pid)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            buf, size = ctypes.create_unicode_buffer(32768), wt.DWORD(32768)
            if not self.k.QueryFullProcessImageNameW(self.handle, 0, buf, ctypes.byref(size)):
                raise ctypes.WinError(ctypes.get_last_error())
            if Path(buf.value).resolve() != GAME.resolve():
                raise TraceError('PID is not the original executable in this workspace')
            times = [wt.FILETIME() for _ in range(4)]
            if not self.k.GetProcessTimes(self.handle, *(ctypes.byref(t) for t in times)):
                raise ctypes.WinError(ctypes.get_last_error())
            creation = times[0].dwLowDateTime | (times[0].dwHighDateTime << 32)
            self.identity = {'pid': pid, 'creation_filetime': creation, 'exe': buf.value}
        except Exception:
            self.close()
            raise

    def read(self, address, size):
        if not 0 <= size <= 0x10000:
            raise TraceError('read exceeds collector bound')
        if not size:
            return b''
        buf, got = ctypes.create_string_buffer(size), ctypes.c_size_t()
        if (not self.k.ReadProcessMemory(self.handle, address, buf, size, ctypes.byref(got))
                or got.value != size):
            raise OSError(f'failed/partial read at {address:#x}, error {ctypes.get_last_error()}')
        return buf.raw

    def close(self):
        if self.handle:
            self.k.CloseHandle(self.handle)
            self.handle = None


def select_pid(requested=None):
    if os.name != 'nt':
        raise TraceError('live capture requires Windows')
    if requested is not None:
        if requested <= 0:
            raise TraceError('PID must be positive')
        return requested
    rows = csv.reader(subprocess.check_output(
        ['tasklist', '/FO', 'CSV', '/NH'], text=True, errors='replace').splitlines())
    pids = [int(row[1]) for row in rows if row and row[0].lower() == 'cross hermit.exe']
    if len(pids) != 1:
        raise TraceError(f'expected one original process, found {pids}; supply --pid')
    return pids[0]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int)
    parser.add_argument('--seconds', type=float, default=10)
    parser.add_argument('--interval-ms', type=int, default=50)
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--out', type=Path, help='new JSONL file; refuses overwrite')
    args = parser.parse_args(argv)
    if not 0 < args.seconds <= 3600 or not 10 <= args.interval_ms <= 10000:
        parser.error('seconds must be (0,3600], interval-ms 10..10000')
    reader = None
    try:
        reader = ProcessReader(select_pid(args.pid))
        verification = verify_image(reader.read, SOURCE.read_bytes())
        scene5_source = SCENE5_SCRIPT.read_bytes()
        metadata = {'kind': 'trace_metadata', 'schema_version': 2,
                    'trace_id': str(uuid.uuid4()), 'process': reader.identity,
                    'started_utc': datetime.now(timezone.utc).isoformat(),
                    'verification': verification, 'interval_ms': args.interval_ms,
                    'scene5_script_sha256': hashlib.sha256(scene5_source).hexdigest(),
                    'limitations': ['non-atomic polling', 'short states may be missed',
                                    'no call-site provenance', 'no task-instance lifetime proof'],
                    'authorizes_persistent_write': False}
        # Verification precedes file creation, and x mode protects existing traces.
        out = args.out.open('x', encoding='utf-8') if args.out else sys.stdout
        try:
            def emit(value):
                out.write(json.dumps(value, ensure_ascii=False) + '\n')
                out.flush()
            emit(metadata)
            start, sequence, valid, invalid = time.monotonic(), 0, 0, 0
            while True:
                before = time.monotonic()
                observation = sample(reader.read, scene5_source)
                valid += observation['valid']
                invalid += not observation['valid']
                emit({'kind': 'sample', 'sequence': sequence,
                      'started_elapsed_ms': round((before-start)*1000, 3),
                      'ended_elapsed_ms': round((time.monotonic()-start)*1000, 3),
                      **observation})
                sequence += 1
                if args.once or time.monotonic() - start >= args.seconds:
                    break
                time.sleep(min(args.interval_ms/1000, max(0, args.seconds-(time.monotonic()-start))))
            emit({'kind': 'trace_end', 'valid_samples': valid, 'invalid_samples': invalid})
            return 0 if valid else 2
        finally:
            if args.out:
                out.close()
    except (TraceError, OSError) as error:
        print(f'capture refused: {error}', file=sys.stderr)
        return 2
    finally:
        if reader:
            reader.close()


if __name__ == '__main__':
    sys.exit(main())
