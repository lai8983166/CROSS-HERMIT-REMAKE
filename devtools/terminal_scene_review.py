"""Independent read-only audit of the failed MAIN/GAME constructor component.

No collector or project validator is imported. This checks source bytes, ABI,
PTD/native receipts and the failure boundary; it is not a full replay.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import gzip
import hashlib
import json
from pathlib import Path
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_32

ROOT = Path(__file__).resolve().parents[1]
IMAGE_SHA = "588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005"
CPU57 = set("EAX EBX ECX EDX ESI EDI EBP ESP EIP EFLAGS FPCW FPSW FPTAG FIP FDP FCS FDS FOP MXCSR CS DS ES FS GS SS CR0 CR2 CR3 CR4 GDTR IDTR LDTR TR".split()) | {f"{p}{i}" for p in ("FP", "XMM", "DR") for i in range(8)}
ARGC = dict(HeapCreate=3, HeapAlloc=3, HeapFree=3, HeapValidate=3, HeapDestroy=1,
    InitializeCriticalSection=1, EnterCriticalSection=1, LeaveCriticalSection=1, DeleteCriticalSection=1,
    CreateEventA=4, CloseHandle=1, TlsAlloc=0, TlsFree=1, TlsGetValue=1, TlsSetValue=2,
    GetCurrentThreadId=0, GetLastError=0, SetLastError=1, IsBadReadPtr=2, IsBadWritePtr=2,
    GetVersionExA=1, GetCurrentDirectoryA=2, GetLocalTime=1, GetSystemTime=1,
    GetTimeZoneInformation=1, WideCharToMultiByte=8, PathAddBackslashA=1, lstrcpyA=2, lstrcatA=2,
    GetDC=1, DeleteDC=1, QueryPerformanceCounter=1, QueryPerformanceFrequency=1)


def need(value, why):
    if not value:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix(),
                bytes=len(raw), sha256=sha(raw))


def audit(r, image):
    need(r['accepted'] is False and r['native_executed'] is True and r['native_process_created'] is True,
         'failed actual native component, never accepted')
    for key in ('formal_acceptance', 'GAME_published', 'scene_constructed', 'full_GAME_factory_executed',
                'worker_started', 'scene_callback_executed', 'cooperative_wait_executed',
                'first_result_consumption', 'independent_full_replay', 'full_WinMain_executed',
                'WinMain_to_scene_factory_continuous', 'screenshot'):
        need(r[key] is False, 'limited scope: ' + key)
    need(r['failure'] == "ValueError('supplemental actual matching screen DC release')" and 'status' not in r,
         'the exact ReleaseDC rejection precedes final STATUS and shutdown')
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    sites = {}
    for row in r['instruction_sites']:
        pc, raw = row['pc'], bytes.fromhex(row['hex'])
        need(pc not in sites and 0x400000 <= pc < 0x592000 and row['count'] > 0, 'unique original instruction site')
        need(raw == image[pc - 0x400000:pc - 0x400000 + len(raw)], 'source instruction bytes ' + hex(pc))
        decoded = list(decoder.disasm(raw, pc))
        need(len(decoded) == 1 and decoded[0].size == len(raw), 'complete original instruction')
        sites[pc] = row
    need(sum(v['count'] for v in sites.values()) == r['final']['instructions'] == 169671, 'actual bounded instruction total')
    required = (0x49dd70, 0x49dde7, 0x49de01, 0x49de1e, 0x421660, 0x412c70, 0x412cbd,
                0x412cc2, 0x412d01, 0x412e30, 0x412dd0, 0x412df0, 0x412e03, 0x413150, 0x413417, 0x413427)
    need(all(p in sites for p in required), 'original construction and GAME destruction chain')
    need(all(p not in sites for p in (0x413450, 0x412d1c, 0x451080, 0x451670, 0x422360, 0x453cb5,
                                    0x44fe60, 0x575450, 0x575360, 0x57ba60)), 'stopped before device/scene and remaining teardown')

    roots = r['roots']
    expected = [(0x57b9d0, [1], None), (0x5752d0, [], None),
                (0x49dd70, [0, 0, 0, 0], 0x49de23), (0x412c70, None, 0x413450),
                (0x412dd0, [1], None)]
    need(len(roots) == len(expected), 'only five declared roots before rejection')
    states = [r['initial'], r['final']]
    for root, (entry, args, stop) in zip(roots, expected):
        need(root['entry'] == entry and root['stop_before'] == stop and root['lane'] == 0 and
             root['declared_independent_function_root'] is True, 'exact declared independent root')
        if args is not None:
            need(root['args'] == args, 'original root arguments')
        sp = root['stack']['stack_pointer']
        stack = struct.pack('<' + 'I' * (len(root['args']) + 1), 0x32000000, *root['args'])
        need(root['stack']['stack_after_hex'] == stack.hex(), 'declared stack/return/argument bytes')
        before, after = root['before']['cpu'], root['after']['cpu']
        need(before['ESP'] == sp and before['EIP'] == entry and before['ECX'] == root['receiver'], 'root entrance ABI')
        need(after['EIP'] == (stop or 0x32000000), 'natural return or precise stop before instruction')
        if stop is None:
            need(after['ESP'] == sp + 4 + (4 * len(root['args']) if root['callee'] else 0), 'root natural return stack balance')
        states += [root['before'], root['after']]
    need(len({roots[i]['stack']['stack_pointer'] for i in (2, 3, 4)}) == 3, 'WinMain/factory/cleanup use distinct declared stacks')

    trace = r['native_trace']; requests = {}; replies = {}; request_at = {}; reply_at = {}
    need(len(r['events']) == 1, 'no native worker start notification')
    ready = r['events'][0]
    need(ready['event'] == 'READY' and ready['pointer_bits'] == 32 and ready['main_tid'] != ready['reader_tid'], 'real owner MAIN/reader distinction')
    for index, row in enumerate(trace):
        if row['direction'] == 'request':
            need(row['id'] == len(requests) + 1 and row['lane'] == 0, 'sequential MAIN-only requests')
            requests[row['id']] = row; request_at[row['id']] = index
        elif 'id' in row:
            need(row['id'] in requests and row['id'] not in replies and row['ok'] == 1, 'one native reply per actual request')
            need(row['lane'] == 0 and row['tid'] == ready['main_tid'] and row['teb'] == ready['main_teb'], 'permanent actual MAIN lane/TID/TEB')
            replies[row['id']] = row; reply_at[row['id']] = index
    need(requests.keys() == replies.keys() and len(requests) == 344, 'all 344 actual native requests answered')
    byop = lambda op: [i for i, q in requests.items() if q['op'] == op]
    need(not any(byop(op) for op in ('CreateThread', 'ResumeThread', 'WaitForSingleObject', 'STATUS', 'Shutdown')),
         'no worker, wait or successful shutdown path')

    mirrors = 0
    for index, api in enumerate(r['API_calls']):
        need(api['name'] in ARGC and api['lane'] == 0, 'declared original API')
        argc = ARGC[api['name']]; before, after = api['before']['cpu'], api['after']['cpu']
        need(len(api['args']) == argc and before['ESP'] == api['sp'] and before['EIP'] == api['target'], 'original API entry ABI')
        need(struct.unpack_from('<I', image, api['slot'] - 0x400000)[0] == api['target'], 'unchanged original IAT')
        need(image[api['ret'] - 6 - 0x400000:api['ret'] - 0x400000] == b'\xff\x15' + struct.pack('<I', api['slot']), 'original import CALL bytes')
        need(after['ESP'] == api['sp'] + 4 + 4 * argc and after['EIP'] == api['ret'] and after['EAX'] == api['value'], 'original stdcall return ABI')
        need(all(before[k] == after[k] for k in CPU57 - {'EAX', 'ESP', 'EIP'}), 'preserved executor registers at native leaf')
        states += [api['before'], api['after']]
        if index >= 11:
            need('current_native_PTD' in api, 'every API after TLS installation has PTD mirror')
        if 'current_native_PTD' in api:
            ptd = api['current_native_PTD']; content = bytes.fromhex(ptd['hex'])
            need(len(content) == 116 and struct.unpack_from('<I', content)[0] in (0, ready['main_tid']), 'complete PTD and current native thread identity')
            reads = [i for i in byop('MEM_READ') if requests[i]['args'] == [ptd['native'], 116] and
                     api['wire_start'] <= request_at[i] < reply_at[i] < api['wire_end'] and replies[i]['hex'] == ptd['hex']]
            need(reads, 'PTD bound to actual native readback within this API boundary')
            writes = [q for q in trace[:request_at[reads[0]]] if q['direction'] == 'request' and q['op'] == 'MEM_WRITE' and
                      q['args'][0] <= ptd['native'] and ptd['native'] + 116 <= q['args'][0] + len(bytes.fromhex(q['args'][1]))]
            need(writes, 'PTD has a prior actual native write')
            last = writes[-1]; offset = ptd['native'] - last['args'][0]
            need(bytes.fromhex(last['args'][1])[offset:offset + 116] == content, 'PTD readback equals source bytes')
            mirrors += 1
    need(len(r['API_calls']) == 72, '72 completed original APIs')
    for state in states:
        need(set(state['cpu']) == CPU57 and state['cpu']['FS'] == 24, 'complete guest CPU57 on MAIN selector')
        for key in ('GDTR', 'IDTR', 'LDTR', 'TR'):
            need(isinstance(state['cpu'][key], list) and len(state['cpu'][key]) == 4, 'descriptor tuple')
        for i in range(8):
            need(isinstance(state['cpu'][f'FP{i}'], list) and len(state['cpu'][f'FP{i}']) == 2, 'physical FP tuple')
        for key in ('instruction_sha256', 'write_sha256'):
            need(len(bytes.fromhex(state[key])) == 32, 'cumulative digest recorded')
        need(state['memory']['bytes'] > 0 and len(bytes.fromhex(state['memory']['sha256'])) == 32, 'memory digest recorded')

    heaps = {}; allocations = {}; virtuals = {}; locks = {}; handles = {}; tls = {}; last_error = 0
    for i, q in requests.items():
        a, op, result = q['args'], q['op'], replies[i]; value = result['result']
        if op in ('MEM_ALLOC', 'MEM_FREE', 'MEM_WRITE', 'MEM_READ'):
            need(result['last_error'] == last_error, 'infrastructure preserves original LastError')
        if op == 'GetLastError': need(value == last_error, 'GetLastError continuity')
        if op == 'SetLastError': need(result['last_error'] == a[0], 'SetLastError original argument')
        last_error = result['last_error']
        if op == 'HeapCreate': need(value and value not in heaps, 'fresh native heap'); heaps[value] = True
        elif op == 'HeapAlloc': need(a[0] in heaps and value not in allocations and value, 'owned native allocation'); allocations[value] = (a[0], a[2])
        elif op == 'HeapFree': need(value == 1 and a[2] in allocations and allocations[a[2]][0] == a[0], 'actual original HeapFree'); del allocations[a[2]]
        elif op == 'MEM_ALLOC': need(value and value not in virtuals, 'owned temporary storage'); virtuals[value] = a[0]
        elif op == 'MEM_FREE': need(value == 1 and a[0] in virtuals, 'temporary explicitly freed'); del virtuals[a[0]]
        elif op == 'InitializeCriticalSection': need(a[0] in virtuals and a[0] not in locks, 'owned native lock'); locks[a[0]] = True
        elif op in ('EnterCriticalSection', 'LeaveCriticalSection'): need(a[0] in locks and len(bytes.fromhex(result['hex'])) == 24, 'actual initialized lock snapshot')
        elif op == 'CreateEventA': need(value and value not in handles, 'original event handle'); handles[value] = True
        elif op == 'TlsAlloc': need(value != 0xffffffff and value not in tls, 'current TLS slot'); tls[value] = 0
        elif op == 'TlsSetValue': need(value == 1 and a[0] in tls, 'native TLS installation'); tls[a[0]] = a[1]
        elif op == 'TlsGetValue': need(value == tls[a[0]] == result['tracked_value'], 'same-thread actual TLS readback')
    need(heaps and allocations and locks and handles and any(tls.values()), 'remaining MAIN/CRT resources not normally torn down')
    dc_ids = [byop(op) for op in ('GetDC', 'DeleteDC', 'ReleaseDC')]
    need(dc_ids == [[272], [296], [344]], 'single exact actual DC sequence')
    get_id, delete_id, release_id = (row[0] for row in dc_ids); dc = replies[get_id]['result']
    need(dc and requests[get_id]['args'] == [0] and requests[delete_id]['args'] == [dc] and
         requests[release_id]['args'] == [0, dc], 'same owner screen DC passed unchanged')
    need(replies[delete_id]['result'] == 1 and replies[release_id]['result'] == 0 and
         replies[delete_id]['getdc_release_still_required'] == 1, 'observed DeleteDC1 then ReleaseDC0; ledger not silently cleared')
    api_get = next(x for x in r['API_calls'] if x['name'] == 'GetDC')
    api_delete = next(x for x in r['API_calls'] if x['name'] == 'DeleteDC')
    leaf_reply = lambda i: {k: v for k, v in replies[i].items() if k != 'direction'}
    need(api_get['ret'] == 0x412fcb and api_get['value'] == dc and api_get['native_leaf'] == leaf_reply(get_id), 'original GetDC binding')
    need(api_delete['ret'] == 0x41341d and api_delete['value'] == 1 and api_delete['native_leaf'] == leaf_reply(delete_id), 'original DeleteDC binding and real return')
    point = r['checkpoints'][1]; game = point['GAME_object']; raw_game = game - 32
    need(point['GAME'] == point['scene'] == 0 and point['GAME_bytes'] == 0xba20 and point['GAME_DC'] == dc and
         point['GAME_drawing_gate'] == '0100' and point['factory_output'] == 0xa5a5a5a5 and point['original_DeleteDC_result'] == 1,
         'constructed GAME object remains unpublished with original draw gate')
    need(roots[4]['receiver'] == game and roots[4]['callee'] is True, 'scalar deleting destructor thiscall argument')
    allocation = point['allocations'][str(raw_game)]
    frees = [i for i in byop('HeapFree') if requests[i]['args'][2] == allocation['native']]
    need(len(frees) == 1 and replies[frees[0]]['result'] == 1 and delete_id < frees[0] < release_id, 'GAME source allocation actually freed after original destructor')
    need(all(not (op.startswith('GetObject') or op in ('FONT_INFO', 'GetObjectType')) for op in (q['op'] for q in requests.values())),
         'no independent DC liveness query was acquired')
    cleanup = r['cleanup']; pid = ready['pid']
    need(cleanup['parent_pid'] == pid and cleanup['forced'] is True and cleanup['exits'][str(pid)] == {'wait': 0, 'code': 94} and
         cleanup['deadline_fired'] is False and cleanup['job_empty'] is True and cleanup['handles_closed'] is True and
         cleanup['errors'] == [] and 0 < cleanup['wall_seconds'] <= 30, 'bounded forced cleanup, not native normal exit')
    return dict(original_instruction_count=r['final']['instructions'], original_instruction_sites=len(sites), original_API_calls=72,
        CPU57_snapshots=len(states), PTD_readbacks=mirrors, native_requests=len(requests), owner_pid=pid,
        native_MAIN_tid=ready['main_tid'], native_MAIN_teb=ready['main_teb'], native_reader_tid=ready['reader_tid'],
        DC=dict(GetDC_request=get_id, DeleteDC_request=delete_id, DeleteDC_result=1, ReleaseDC_request=release_id,
                ReleaseDC_result=0, handle=dc, liveness_after_DeleteDC='unresolved', leak_established=False, release_established=False),
        GAME_allocation_native_free_request=frees[0], original_GAME_constructed=True, original_GAME_destructor_completed=True,
        original_MAIN_destructor_completed=False, original_CRT_teardown_completed=False,
        remaining_tracked_resources_before_forced_exit=dict(heaps=len(heaps), allocations=len(allocations),
            virtual_allocations=len(virtuals), criticals=len(locks), handles=len(handles), TLS_slots=len(tls), live_TLS_values=sum(bool(v) for v in tls.values())),
        cleanup=cleanup)


def review(path):
    need(path.stat().st_size <= 16 * 1024 * 1024, 'bounded compressed source')
    with gzip.open(path, 'rb') as stream:
        raw = stream.read(64 * 1024 * 1024 + 1)
    need(len(raw) <= 64 * 1024 * 1024, 'bounded uncompressed source')
    r = json.loads(raw)
    pins = [r['original'], r['implementation'], r['helper'], *r['implementation_pins']]
    pins += [r['build'][key] for key in ('base_source', 'generator', 'generated_source', 'helper')]
    # Reproducible compiler objects may be retired by a separate size/hash
    # manifest. Runtime/source identities above and exact build recipe remain.
    pins += [p for p in r['build']['artifacts'] if Path(p['path']).suffix in ('.cmd', '.log')]
    pins += r['build']['dependencies']
    for pin in pins:
        p = Path(pin['path']); p = p if p.is_absolute() else ROOT / p
        need(identity(p) == pin, 'unchanged source/build dependency: ' + pin['path'])
    image = (ROOT / r['original']['path']).read_bytes()
    need(len(image) == 5980160 and sha(image) == IMAGE_SHA, 'fixed original game image')
    result = audit(r, image)
    mutations = []
    bad = copy.deepcopy(r); code = bytearray.fromhex(bad['instruction_sites'][0]['hex']); code[0] ^= 1
    bad['instruction_sites'][0]['hex'] = code.hex()
    cases = [('original_instruction_byte_changed', bad)]
    bad = copy.deepcopy(r)
    next(x for x in bad['native_trace'] if x.get('direction') == 'response' and x.get('id') == 296)['result'] = 0
    cases.append(('native_DeleteDC_result_changed', bad))
    for label, bad in cases:
        try:
            audit(bad, image)
        except ValueError as error:
            mutations.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('tampered evidence accepted: ' + label)
    return dict(schema_version=1, kind='independent_failed_component_record_review_not_replay', review_passed=True,
        accepted=False, formal_acceptance=False, independent_full_replay=False, scene_or_wait_accepted=False,
        no_native_execution_by_reviewer=True, no_collector_or_project_module_imports=True,
        source=identity(path), reviewer=identity(__file__), verified_file_pins=len(pins), checks=result, tamper_rejections=mutations,
        limitations=[
            'Instruction site bytes/totals, CPU57 shape, original ABI, PTD bytes and native receipts were checked; ordered instructions and cumulative memory/write digests were not independently replayed or recomputed.',
            'Native API authenticity is supported by pinned implementation/build identities and same-owner receipts, not an independent kernel observer.',
            'GAME constructor and scalar deleting destructor completed. MAIN/CRT cleanup did not complete; process exit94 was forced and Job emptiness is not normal resource lifetime evidence.',
            'DeleteDC1 followed by ReleaseDC0 has no independent HDC liveness observation. Neither a DC leak nor successful DC release is established.',
            'GetDC(0) acquires a screen DC handle; no pixel reading, window creation, desktop input or device initialization is demonstrated.',
            'WinMain and GAME factory remain suspended in distinct preserved guest stacks; the separate destructor root is supplemental cleanup, not normal WinMain termination.',
            'Initial parent pipe CloseHandle BOOL values were not recorded by the inherited owner implementation; handles_closed is a separate bounded cleanup receipt.',
            'No GAME publication, scene constructor, worker, cooperative wait, battle result consumption or two-case formal acceptance is established.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True); parser.add_argument('--out', required=True)
    args = parser.parse_args(); source = (ROOT / args.source).resolve(); out = (ROOT / args.out).resolve()
    need(source.is_relative_to(ROOT) and out.is_relative_to(ROOT) and not out.exists(), 'fresh workspace review output')
    result = review(source)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(out=str(out), review_passed=True, accepted=False, native_executed=False)))
