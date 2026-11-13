"""Read-only independent review of one owner report; never launches native code.

Does not import the collector, its validator, or any project module. This checks
recorded byte/ABI/resource evidence, not a replay of the original execution.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_32

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
CPU57 = set(('EAX EBX ECX EDX ESI EDI EBP ESP EIP EFLAGS FPCW FPSW FPTAG '
    'FIP FDP FCS FDS FOP MXCSR CS DS ES FS GS SS CR0 CR2 CR3 CR4 GDTR IDTR '
    'LDTR TR').split()) | {f'FP{i}' for i in range(8)} | {f'XMM{i}' for i in range(8)} | {f'DR{i}' for i in range(8)}
ARGC = dict(HeapCreate=3, HeapAlloc=3, HeapFree=3, HeapValidate=3, HeapDestroy=1,
    InitializeCriticalSection=1, EnterCriticalSection=1, LeaveCriticalSection=1,
    DeleteCriticalSection=1, CreateEventA=4, ResetEvent=1, SetEvent=1, CloseHandle=1,
    WaitForSingleObject=2, CreateThread=6, ResumeThread=1, GetExitCodeThread=2,
    TlsAlloc=0, TlsFree=1, TlsGetValue=1, TlsSetValue=2, GetCurrentThreadId=0,
    GetLastError=0, SetLastError=1, ExitThread=1, IsBadReadPtr=2, IsBadWritePtr=2,
    GetVersionExA=1, GetCurrentDirectoryA=2, GetTickCount=0, Sleep=1)


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=path.stat().st_size,
                sha256=sha(path.read_bytes()))


def review(path):
    need(path.stat().st_size <= 16 * 1024 * 1024, 'bounded compressed report')
    with gzip.open(path, 'rb') as stream:
        raw = stream.read(64 * 1024 * 1024 + 1)
    need(len(raw) <= 64 * 1024 * 1024, 'bounded decompressed report')
    report = json.loads(raw)
    for key in ('formal_acceptance', 'scene_first_yield', 'first_result_consumption',
                'complete_battle_exit', 'independent_full_replay', 'physical_native_context_import',
                'desktop_used', 'screenshot'):
        need(report[key] is False, 'required limited-scope declaration: ' + key)
    need(report['accepted'] is True and report['native_executed'] is True and
         report['native_process_created'] is True, 'reported one actual owner mechanism case')
    pins = [report['original'], report['helper'], report['implementation'],
            report['build_gate']['source'], report['build_gate']['report'], *report['implementation_pins']]
    for pin in pins:
        p = (ROOT / pin['path']).resolve()
        need(p.is_relative_to(ROOT) and p.is_file() and identity(p) == pin, 'unchanged pinned file: ' + pin['path'])
    image = (ROOT / report['original']['path']).read_bytes()
    need(len(image) == 5980160 and sha(image) == ORIGINAL_SHA, 'original image exact identity')

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    sites = {}
    for item in report['instruction_sites']:
        pc, code, count = item['pc'], bytes.fromhex(item['hex']), item['count']
        need(pc not in sites and 0x400000 <= pc < 0x592000 and count > 0, 'unique bounded original instruction site')
        need(code == image[pc - 0x400000:pc - 0x400000 + len(code)], 'original bytes at ' + hex(pc))
        decoded = list(md.disasm(code, pc))
        need(len(decoded) == 1 and decoded[0].size == len(code), 'one complete decoded original instruction')
        sites[pc] = item
    need(sum(x['count'] for x in sites.values()) == report['final']['instructions'], 'aggregate original instruction count')
    required = (0x5752d0, 0x576f60, 0x57531a, 0x575334, 0x422290, 0x56e0be,
                0x56e110, 0x56e11f, 0x56e126, 0x56e141, 0x56e155, 0x56e180,
                0x421f50, 0x421f88, 0x422330, 0x421a5a, 0x421a8e, 0x421fed,
                0x422021, 0x56e1e0, 0x5753b0, 0x575450, 0x57553e, 0x57554f,
                0x56e21b, 0x575360, 0x576fa0, 0x57ba60)
    need(all(pc in sites for pc in required), 'original worker/CRT/manager path instruction coverage')
    need(all(pc not in sites for pc in (0x422360, 0x453cb5, 0x451670, 0x4539b0)), 'no scene yield or result-consumer coverage claimed')

    states = [('initial', report['initial']), ('final', report['final'])]
    for index, root in enumerate(report['roots']):
        states.append((f'root:{index}:before', root['before']))
        if 'after' in root:
            states.append((f'root:{index}:after', root['after']))
            need(root['after']['cpu']['EIP'] == 0x32000000, 'natural declared MAIN root return')
    for index, api in enumerate(report['API_calls']):
        states.extend(((f'api:{index}:before', api['before']), (f'api:{index}:after', api['after'])))
        before, after = api['before']['cpu'], api['after']['cpu']
        argc = ARGC[api['name']]
        need(len(api['args']) == argc and before['ESP'] == api['sp'] and before['EIP'] == api['target'], 'original imported API entry ABI')
        need(struct.unpack_from('<I', image, api['slot'] - 0x400000)[0] == api['target'], 'original immutable IAT target')
        need(image[api['ret'] - 6 - 0x400000:api['ret'] - 0x400000] == b'\xff\x15' + struct.pack('<I', api['slot']), 'original FF15 import call bytes')
        need(before['FS'] == after['FS'] == (24 if api['lane'] == 0 else 32), 'separate declared guest FS selector')
        if api['name'] != 'ExitThread':
            need(after['ESP'] == api['sp'] + 4 + 4 * argc and after['EIP'] == api['ret'] and after['EAX'] == api['value'], 'declared stdcall return ABI')
            need(all(before[k] == after[k] for k in CPU57 - {'EAX', 'ESP', 'EIP'}), 'preserved executor registers across platform import')
        else:
            need(api['lane'] == 1 and api['args'] == [0] and before == after, 'nonreturning original worker ExitThread boundary')
    for label, state in states:
        need(set(state['cpu']) == CPU57 and len(CPU57) == 57, 'complete executor CPU57 fields: ' + label)
        for key in ('GDTR', 'IDTR', 'LDTR', 'TR'):
            need(isinstance(state['cpu'][key], list) and len(state['cpu'][key]) == 4, 'descriptor shape')
        for index in range(8):
            need(isinstance(state['cpu'][f'FP{index}'], list) and len(state['cpu'][f'FP{index}']) == 2, 'physical FP tuple shape')
        for key in ('instruction_sha256', 'write_sha256'):
            need(len(state[key]) == 64 and bytes.fromhex(state[key]), 'present cumulative digest field')
        need(len(state['memory']['sha256']) == 64 and state['memory']['bytes'] > 0, 'present memory digest field')

    trace = report['native_trace']
    requests, replies, request_at, reply_at = {}, {}, {}, {}
    ready, start = report['events']
    need(ready['event'] == 'READY' and start['event'] == 'WORKER_START' and ready['pointer_bits'] == 32, 'one READY and one WORKER_START')
    tids = {0: ready['main_tid'], 1: start['worker_tid']}
    tebs = {0: ready['main_teb'], 1: start['teb']}
    need(len({*tids.values(), ready['reader_tid']}) == 3 and tebs[0] != tebs[1], 'distinct actual native threads and TEBs')
    for index, row in enumerate(trace):
        if row['direction'] == 'request':
            need(row['id'] == len(requests) + 1 and row['lane'] in (0, 1), 'unique sequential native request')
            requests[row['id']] = row; request_at[row['id']] = index
        elif 'id' in row:
            need(row['id'] in requests and row['id'] not in replies, 'unique response to existing request')
            q = requests[row['id']]
            need(row['lane'] == q['lane'] and row['tid'] == tids[q['lane']] and row['teb'] == tebs[q['lane']] and row['ok'] == 1, 'fixed same-owner lane/TID/TEB response')
            replies[row['id']] = row; reply_at[row['id']] = index
    need(requests.keys() == replies.keys(), 'all native requests answered')

    def ids(op, lane=None):
        return [i for i, q in requests.items() if q['op'] == op and (lane is None or q['lane'] == lane)]

    heaps, allocations, virtuals, handles, locks, tls = {}, {}, {}, {}, {}, {}
    last_error = {0: 0, 1: 0}; pending_tls_free = []
    resource_counts = Counter()
    for row in trace:
        if row['direction'] != 'response' or 'id' not in row:
            continue
        q = requests[row['id']]; op, a, lane, value = q['op'], q['args'], q['lane'], row['result']
        resource_counts[op] += 1
        if op in ('MEM_ALLOC', 'MEM_FREE', 'MEM_READ', 'MEM_WRITE', 'STATUS', 'Shutdown'):
            need(row['last_error'] == last_error[lane], 'bridge infrastructure preserves last leaf error')
        if op == 'GetLastError': need(value == last_error[lane], 'native lane LastError continuity')
        if op == 'SetLastError': need(row['last_error'] == a[0], 'native lane LastError restoration')
        if op == 'TlsGetValue': need(row['last_error'] == 0, 'actual successful TlsGetValue error semantics')
        last_error[lane] = row['last_error']
        if op == 'HeapCreate':
            need(value and value not in heaps, 'fresh native heap'); heaps[value] = True
        elif op == 'HeapAlloc':
            need(a[0] in heaps and value and value not in allocations, 'allocation belongs to current heap'); allocations[value] = (a[0], a[2])
        elif op == 'HeapFree':
            need(value == 1 and a[2] in allocations and allocations[a[2]][0] == a[0], 'actual owned HeapFree')
            if row.get('tls_reference_pending_clear'):
                need(any(a[2] <= p < a[2] + allocations[a[2]][1] for p in tls.get(lane, {}).values()), 'PTD free precedes actual TLS clear')
                pending_tls_free.append(dict(lane=lane,request_id=row['id'],base=a[2]))
            del allocations[a[2]]
        elif op == 'HeapDestroy':
            need(value == 1 and a[0] in heaps and not any(h == a[0] for h, _ in allocations.values()), 'empty native heap destroyed'); del heaps[a[0]]
        elif op == 'MEM_ALLOC':
            need(value and value not in virtuals, 'native bridge storage'); virtuals[value] = a[0]
        elif op == 'MEM_FREE':
            need(value == 1 and a[0] in virtuals, 'native bridge storage freed'); del virtuals[a[0]]
        elif op == 'InitializeCriticalSection':
            need(a[0] not in locks and a[0] in virtuals and len(bytes.fromhex(row['hex'])) == 24, 'tracked actual critical section'); locks[a[0]] = True
        elif op in ('EnterCriticalSection', 'LeaveCriticalSection'):
            need(a[0] in locks and len(bytes.fromhex(row['hex'])) == 24, 'actual lock snapshot')
            if op == 'EnterCriticalSection':
                values = struct.unpack('<6I', bytes.fromhex(row['hex']))
                need(values[2] > 0 and values[3] == tids[lane], 'native lock snapshot current owner TID')
        elif op == 'DeleteCriticalSection':
            need(a[0] in locks, 'initialized lock deleted'); del locks[a[0]]
        elif op in ('CreateEventA', 'CreateThread'):
            need(value and value not in handles, 'fresh tracked native handle'); handles[value] = op
        elif op == 'CloseHandle':
            need(value == 1 and a[0] in handles, 'tracked handle explicitly closed'); del handles[a[0]]
        elif op == 'TlsAlloc':
            need(value != 0xffffffff and value not in tls.get(0, {}), 'fresh actual TLS slot')
            for l in (0, 1): tls.setdefault(l, {})[value] = 0
        elif op == 'TlsSetValue':
            need(value == 1 and a[0] in tls[lane], 'actual thread-local TLS update'); tls[lane][a[0]] = a[1]
        elif op == 'TlsGetValue':
            need(value == tls[lane][a[0]] == row['tracked_value'], 'actual TLS readback matches this lane only')
        elif op == 'TlsFree':
            need(value == 1 and all(tls[l][a[0]] == 0 for l in (0, 1)), 'TLS slot cleared on both threads before free')
            for l in (0, 1): del tls[l][a[0]]
    need(not any((heaps, allocations, virtuals, handles, locks, tls[0], tls[1])), 'independently reconciled resource ledger empty')

    create_ids = ids('CreateThread', 0)
    need(len(create_ids) == len(ids('ResumeThread', 0)) == len(ids('ExitThread', 1)) == 1, 'one actual suspended worker lifetime')
    create_id = create_ids[0]; create = replies[create_id]; native_ptd = create['guest_param']
    need(requests[create_id]['args'] == [0, 0, 0x56e110, native_ptd, 4, 0x65002024], 'exact suspended native CreateThread projection')
    expected = bytearray(116)
    for offset, value in ((4, 0xffffffff), (0x14, 1), (0x48, 0x421f50), (0x4c, 0x65002000), (0x50, 0x761d68)):
        struct.pack_into('<I', expected, offset, value)
    need(bytes.fromhex(create['ptd_hex']) == expected, 'complete original worker PTD at actual CreateThread')
    need(create['worker_tid'] == start['worker_tid'] and create['guest_entry'] == start['guest_entry'] == 0x56e110 and
         create['guest_param'] == start['guest_param'] and create['native_entry'] == start['native_entry'] != 0x56e110,
         'explicit guest/native dispatcher mapping')
    need(replies[ids('ResumeThread', 0)[0]]['result'] == 1, 'one real suspended count consumed')

    ptd_mirrors = Counter(); poisoned_PTD_mirrors = []
    for api in report['API_calls']:
        if 'current_native_PTD' not in api:
            continue
        ptd = api['current_native_PTD']; content = bytes.fromhex(ptd['hex'])
        need(len(content) == 116, 'full live PTD mirror extent')
        if api['name'] == 'HeapFree':
            # Original debug CRT fills its block with 0xdd immediately before
            # calling HeapFree. Requiring live fields here would change its ABI.
            need(content == b'\xdd' * 116 and image[0x7619cd-0x400000] == 0xdd and
                 sites[0x56f7c6]['count'] == 2 and api['ret'] == 0x578915,
                 'original debug-free poison of PTD before HeapFree')
            poisoned_PTD_mirrors.append(dict(lane=api['lane'],native=ptd['native'],bytes=116,fill=0xdd))
        else:
            if api['lane'] == 1:
                need(ptd['native'] == native_ptd and struct.unpack_from('<I', content, 0x48)[0] == 0x421f50 and
                     struct.unpack_from('<I', content, 0x4c)[0] == 0x65002000, 'worker PTD retains original callback/node')
            need(struct.unpack_from('<I', content)[0] in (0, tids[api['lane']]), 'PTD real current thread identity after original write')
        end = api.get('wire_end', len(trace))
        matching = [i for i in ids('MEM_READ', api['lane']) if requests[i]['args'] == [ptd['native'],116] and
                    api['wire_start'] <= request_at[i] < reply_at[i] < end and replies[i]['hex'] == ptd['hex']]
        need(matching, 'full native PTD record bound to actual read response')
        read_index = request_at[matching[0]]
        writes = [q for q in trace[:read_index] if q['direction'] == 'request' and q['op'] == 'MEM_WRITE' and
                  q['args'][0] <= ptd['native'] and ptd['native'] + 116 <= q['args'][0] + len(bytes.fromhex(q['args'][1]))]
        need(writes, 'prior actual native memory mirror')
        prior = writes[-1]; offset = ptd['native'] - prior['args'][0]
        need(bytes.fromhex(prior['args'][1])[offset:offset+116] == content, 'complete PTD readback equals last source byte mirror')
        ptd_mirrors[api['lane']] += 1

    waits = [i for i in ids('WaitForSingleObject', 0) if requests[i]['args'][1] == 0xffffffff]
    need(len(waits) == 1, 'one original MAIN INFINITE event wait')
    wait_id = waits[0]; event_handle = requests[wait_id]['args'][0]
    signals = [i for i in ids('SetEvent', 1) if requests[i]['args'] == [event_handle]]
    need(len(signals) == 1, 'worker original signal of same manager event')
    signal_id = signals[0]
    need(request_at[wait_id] < request_at[signal_id] < reply_at[signal_id] < reply_at[wait_id] and
         replies[signal_id]['result'] == 1 and replies[wait_id]['result'] == 0, 'recorded MAIN wait / WORKER signal / wait return order')
    need(any(a['lane'] == 0 and a['name'] == 'WaitForSingleObject' and a['ret'] == 0x421a94 for a in report['API_calls']) and
         any(a['lane'] == 1 and a['name'] == 'SetEvent' and a['ret'] == 0x421ff3 for a in report['API_calls']), 'wait/signal bound to original callsites')
    exit_id = ids('ExitThread', 1)[0]; worker_handle = create['result']
    need(requests[exit_id]['args'] == [0] and replies[exit_id]['exit_requested'] == 1 and
         replies[exit_id]['termination_observed'] == 0, 'exit acknowledgement not conflated with termination')
    worker_free = next(x['request_id'] for x in pending_tls_free if x['lane'] == 1)
    clear_id = next(i for i in ids('TlsSetValue', 1) if requests[i]['args'][1] == 0)
    cleared_read = next(i for i in ids('TlsGetValue', 1) if request_at[i] > reply_at[clear_id] and replies[i]['result'] == 0)
    need(reply_at[worker_free] < request_at[clear_id] < reply_at[cleared_read] < request_at[exit_id], 'original worker PTD free / TLS clear / zero read / ExitThread sequence')
    final_wait = next(i for i in ids('WaitForSingleObject', 0) if requests[i]['args'] == [worker_handle,1000])
    final_query = next(i for i in ids('GetExitCodeThread', 0) if request_at[i] > reply_at[final_wait])
    final_close = next(i for i in ids('CloseHandle', 0) if requests[i]['args'] == [worker_handle])
    need(reply_at[exit_id] < request_at[final_wait] and replies[final_wait]['result'] == 0 and
         replies[final_query]['result'] == 1 and replies[final_query]['exit_code'] == 0 and
         reply_at[final_query] < request_at[final_close], 'actual worker termination/exit0 precedes handle close')
    for state in (report['status'], replies[ids('Shutdown')[0]]):
        need(all(state[key] == 0 for key in ('allocations','memory_bytes','heaps','handles','criticals','tls_slots','worker_exit_code')), 'reported final native tracked resources zero')
        need(all(state[key] == 1 for key in ('worker_created','worker_resumed','exit_requested','termination_observed','worker_handle_closed')), 'reported complete native worker lifetime')
    cleanup = report['cleanup']; pid = ready['pid']
    need(cleanup['parent_pid'] == pid and cleanup['exits'][str(pid)] == {'wait':0,'code':0} and
         cleanup['forced'] is False and cleanup['deadline_fired'] is False and cleanup['job_empty'] is True and
         cleanup['handles_closed'] is True and cleanup['errors'] == [] and 0 < cleanup['wall_seconds'] <= 30,
         'helper normal process exit0, recorded Job empty and bounded owner lifetime')

    return dict(schema_version=1, kind='independent_record_review_not_replay', mechanism_record_checks_passed=True,
        formal_acceptance=False, game_acquisition_allowed=False, first_cooperative_yield_verified=False,
        independent_full_replay=False, source=identity(path), reviewer=identity(Path(__file__)),
        verified_implementation_pins=len(report['implementation_pins']), original_instruction_sites=len(sites),
        original_instruction_count=report['final']['instructions'], original_api_calls=len(report['API_calls']),
        original_root_records=len(report['roots']), executor_CPU57_snapshots=len(states),
        native_requests=len(requests), native_responses=len(replies), owner_pid=pid,
        native_lane_tids=tids,native_lane_tebs=tebs, native_TLS_slot=replies[ids('TlsAlloc')[0]]['result'],
        complete_PTD_mirrors=dict(ptd_mirrors), original_debug_free_PTD_poison=poisoned_PTD_mirrors, current_worker_native_PTD=native_ptd,
        wait_signal_sequence=dict(wait_request_id=wait_id,worker_signal_request_id=signal_id,
            trace_indices=[request_at[wait_id],request_at[signal_id],reply_at[signal_id],reply_at[wait_id]],
            actual_Win32_leaf_calls_verified_from_pinned_implementation_and_receipts=True,
            pre_signal_kernel_blocked_state_independently_observed=False),
        worker_exit=dict(PTD_free_request=worker_free,TLS_clear_request=clear_id,zero_read_request=cleared_read,
            ExitThread_request=exit_id,termination_wait_request=final_wait,exit_code_query=final_query,handle_close=final_close,exit_code=0),
        resources=dict(independent_ledger_empty=True,reported_status=report['status'],operation_counts=dict(resource_counts)),
        helper_cleanup=cleanup, reviewed_native_owner_wall_seconds=cleanup['wall_seconds'],
        no_new_native_execution_by_reviewer=True, no_collector_or_project_validator_imports=True,
        limitations=[
            'This review checks instruction totals/site bytes and did not execute an independent full replay. The compact report does not provide a complete ordered transaction stream directly consumable by the existing replayer; retained cold inputs and implementation remain available for future adapters.',
            'CPU57 values and ABI snapshots are executor records, not imported native CPU/TEB/hidden segment state. Native volatile-register clobbers are not measured by this return-value bridge.',
            'This review shape-checks recorded memory and cumulative instruction/write digests but did not independently recompute them or establish full state equivalence.',
            'MAIN INFINITE request precedes WORKER SetEvent and wait reply follows it. No wait-entry notification, concurrent live context, or kernel wait-state observation proves MAIN had already blocked in the kernel before SetEvent.',
            'Critical-section bytes are actual post-leaf snapshots, not cross-thread atomic snapshots.',
            'Initial CloseHandle BOOL values for parent Python copies of childin/childout were not recorded and are not independently proved; helper tracked resources and parent process/job handles are a separate scope. The reported outer Python exit0 is controller evidence, not a claim of individually observed successful closes.',
            'One native owner lifetime only; no second fresh native case, tamper qualification or independent full replay is established here.',
            'No original 422360 cooperative yield, 453CB5 first result consumption, scene callback 451670, battle chain, game process, screenshot or desktop input is demonstrated.'
        ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True); parser.add_argument('--out', required=True)
    args = parser.parse_args()
    source, out = (ROOT/args.source).resolve(), (ROOT/args.out).resolve()
    need(source.is_relative_to(ROOT) and out.is_relative_to(ROOT) and not out.exists(), 'fresh F-workspace review output')
    result = review(source)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(out=str(out), bytes=out.stat().st_size, passed=result['mechanism_record_checks_passed'], native_executed=False)))


if __name__ == '__main__':
    main()
