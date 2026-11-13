"""Independent read-only audit of the successful bounded DC/MAIN/PTD cleanup component.

No collector or project validator is imported. This checks source bytes, ABI,
PTD/native receipts and normal resource cleanup; it is not a full replay.
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
    need(r['accepted'] is True and r['native_executed'] is True and r['native_process_created'] is True,
         'successful actual bounded component')
    for key in ('formal_acceptance', 'GAME_published', 'scene_constructed', 'full_GAME_factory_executed',
                'worker_started', 'cooperative_wait_executed',
                'first_result_consumption', 'independent_full_replay', 'full_WinMain_executed',
                'window_created', 'pixels_read', 'host_input_sent'):
        need(r[key] is False, 'limited scope: ' + key)
    need('failure' not in r and 'status' in r, 'normal component completion recorded')
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    sites = {}
    for row in r['instruction_sites']:
        pc, raw = row['pc'], bytes.fromhex(row['hex'])
        need(pc not in sites and 0x400000 <= pc < 0x592000 and row['count'] > 0, 'unique original instruction site')
        need(raw == image[pc - 0x400000:pc - 0x400000 + len(raw)], 'source instruction bytes ' + hex(pc))
        decoded = list(decoder.disasm(raw, pc))
        need(len(decoded) == 1 and decoded[0].size == len(raw), 'complete original instruction')
        sites[pc] = row
    need(sum(v['count'] for v in sites.values()) == r['final']['instructions'] == 175031, 'actual bounded instruction total')
    required = (0x49dd70, 0x49dde7, 0x49de01, 0x49de1e, 0x421660, 0x412c70, 0x412cbd,
                0x412cc2, 0x412d01, 0x412e30, 0x412dd0, 0x412df0, 0x412e03, 0x413150, 0x413417, 0x413427, 0x44fe60, 0x575450, 0x57553e, 0x57554f, 0x575360, 0x575377, 0x57ba60, 0x57bb3e, 0x56f7c6)
    need(all(p in sites for p in required), 'original construction and GAME destruction chain')
    need(all(p not in sites for p in (0x413450, 0x412d1c, 0x451080, 0x451670, 0x422360, 0x453cb5,
                                    0x450570, 0x49e2b0)), 'no device/GAME publication/scene/wait parent executed')

    roots = r['roots']
    expected = [(0x57b9d0, [1], None), (0x5752d0, [], None),
                (0x49dd70, [0, 0, 0, 0], 0x49de23), (0x412c70, None, 0x413450),
                (0x412dd0, [1], None), (0x44fe60, [], None), (0x428ad0, None, None),
                (0x575450, [0], None), (0x575360, [], None), (0x57ba60, [], None)]
    need(len(roots) == len(expected), 'exact ten declared roots including supplementary cleanup')
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
    need(requests.keys() == replies.keys() and len(requests) == 457, 'all 457 actual native requests answered')
    byop = lambda op: [i for i, q in requests.items() if q['op'] == op]
    need(not any(byop(op) for op in ('CreateThread', 'ResumeThread', 'WaitForSingleObject', 'ReleaseDC')),
         'no worker/wait or duplicate screen DC release')

    mirrors = 0; poisoned = []
    for index, api in enumerate(r['API_calls']):
        need(api['name'] in ARGC and api['lane'] == 0, 'declared original API')
        argc = ARGC[api['name']]; before, after = api['before']['cpu'], api['after']['cpu']
        need(len(api['args']) == argc and before['ESP'] == api['sp'] and before['EIP'] == api['target'], 'original API entry ABI')
        need(struct.unpack_from('<I', image, api['slot'] - 0x400000)[0] == api['target'], 'unchanged original IAT')
        need(image[api['ret'] - 6 - 0x400000:api['ret'] - 0x400000] == b'\xff\x15' + struct.pack('<I', api['slot']), 'original import CALL bytes')
        need(after['ESP'] == api['sp'] + 4 + 4 * argc and after['EIP'] == api['ret'] and after['EAX'] == api['value'], 'original stdcall return ABI')
        need(all(before[k] == after[k] for k in CPU57 - {'EAX', 'ESP', 'EIP'}), 'preserved executor registers at native leaf')
        states += [api['before'], api['after']]
        if 11 <= index <= 91:
            need('current_native_PTD' in api, 'every API after TLS installation has PTD mirror')
        if 'current_native_PTD' in api:
            ptd = api['current_native_PTD']; content = bytes.fromhex(ptd['hex'])
            need(len(content) == 116, 'complete PTD extent')
            if content == bytes([0xdd]) * 116:
                need(api['name'] == 'HeapFree' and api['ret'] == 0x578915 and
                     api['args'][2] + 32 == ptd['guest'] and image[0x7619cd-0x400000] == 0xdd and
                     0x56f7c6 in sites, 'only original PTD debug-free may poison all116 bytes')
                poisoned.append(dict(api_index=index, native=ptd['native'], guest=ptd['guest']))
            else:
                need(struct.unpack_from('<I', content)[0] in (0, ready['main_tid']), 'live PTD native thread identity')
            reads = [i for i in byop('MEM_READ') if requests[i]['args'] == [ptd['native'], 116] and
                     api['wire_start'] <= request_at[i] < reply_at[i] < api['wire_end'] and replies[i]['hex'] == ptd['hex']]
            need(reads, 'PTD bound to actual native readback within this API boundary')
            writes = [q for q in trace[:request_at[reads[0]]] if q['direction'] == 'request' and q['op'] == 'MEM_WRITE' and
                      q['args'][0] <= ptd['native'] and ptd['native'] + 116 <= q['args'][0] + len(bytes.fromhex(q['args'][1]))]
            need(writes, 'PTD has a prior actual native write')
            last = writes[-1]; offset = ptd['native'] - last['args'][0]
            need(bytes.fromhex(last['args'][1])[offset:offset + 116] == content, 'PTD readback equals source bytes')
            mirrors += 1
    need(len(r['API_calls']) == 114, '114 completed original APIs')
    for state in states:
        need(set(state['cpu']) == CPU57 and state['cpu']['FS'] == 24, 'complete guest CPU57 on MAIN selector')
        for key in ('GDTR', 'IDTR', 'LDTR', 'TR'):
            need(isinstance(state['cpu'][key], list) and len(state['cpu'][key]) == 4, 'descriptor tuple')
        for i in range(8):
            need(isinstance(state['cpu'][f'FP{i}'], list) and len(state['cpu'][f'FP{i}']) == 2, 'physical FP tuple')
        for key in ('instruction_sha256', 'write_sha256'):
            need(len(bytes.fromhex(state[key])) == 32, 'cumulative digest recorded')
        need(state['memory']['bytes'] > 0 and len(bytes.fromhex(state['memory']['sha256'])) == 32, 'memory digest recorded')

    need(len(poisoned) == 1 and mirrors == 81, 'one original PTD poison among81 complete native readbacks')
    heaps = {}; allocations = {}; virtuals = {}; locks = {}; handles = {}; tls = {}; last_error = 0
    pending_ptd_free = []; cleared = []; tls_reads = []
    for i, q in requests.items():
        a, op, result = q['args'], q['op'], replies[i]; value = result['result']
        if op in ('MEM_ALLOC', 'MEM_FREE', 'MEM_WRITE', 'MEM_READ', 'DC_INFO', 'STATUS', 'Shutdown'):
            need(result['last_error'] == last_error, 'infrastructure preserves original LastError')
        if op == 'GetLastError': need(value == last_error, 'GetLastError continuity')
        if op == 'SetLastError': need(result['last_error'] == a[0], 'SetLastError original argument')
        last_error = result['last_error']
        if op == 'HeapCreate': need(value and value not in heaps, 'fresh native heap'); heaps[value] = True
        elif op == 'HeapAlloc': need(a[0] in heaps and value not in allocations and value, 'owned native allocation'); allocations[value] = (a[0], a[2])
        elif op == 'HeapFree':
            need(value == 1 and a[2] in allocations and allocations[a[2]][0] == a[0], 'actual original HeapFree')
            size = allocations[a[2]][1]
            refs = [p for p in tls.values() if a[2] <= p < a[2]+size]
            if refs:
                need(refs == [poisoned[0]['native']] and result.get('tls_reference_pending_clear') == 1,
                     'only same-lane original PTD free precedes clear')
                pending_ptd_free.append(i)
            del allocations[a[2]]
        elif op == 'HeapDestroy':
            need(value == 1 and a[0] in heaps and not allocations and not tls and not locks and not handles,
                 'heap destroyed only after source allocations/TLS/locks/events are empty')
            del heaps[a[0]]
        elif op == 'MEM_ALLOC': need(value and value not in virtuals, 'owned temporary storage'); virtuals[value] = a[0]
        elif op == 'MEM_FREE': need(value == 1 and a[0] in virtuals and a[0] not in locks, 'temporary explicitly freed after lock deletion'); del virtuals[a[0]]
        elif op == 'InitializeCriticalSection': need(a[0] in virtuals and a[0] not in locks, 'owned native lock'); locks[a[0]] = True
        elif op in ('EnterCriticalSection', 'LeaveCriticalSection'): need(a[0] in locks and len(bytes.fromhex(result['hex'])) == 24, 'actual initialized lock snapshot')
        elif op == 'DeleteCriticalSection': need(a[0] in locks and result.get('void') == 1, 'actual original lock deletion'); del locks[a[0]]
        elif op == 'CreateEventA': need(value and value not in handles, 'original event handle'); handles[value] = True
        elif op == 'CloseHandle': need(value == 1 and a[0] in handles, 'actual event close'); del handles[a[0]]
        elif op == 'TlsAlloc': need(value != 0xffffffff and value not in tls, 'current TLS slot'); tls[value] = 0
        elif op == 'TlsSetValue':
            need(value == 1 and a[0] in tls, 'native TLS installation/clear')
            if a[1]: need(any(p <= a[1] < p+n for p,(_,n) in allocations.items()), 'live actual PTD installed')
            else: need(pending_ptd_free and tls[a[0]] == poisoned[0]['native'], 'source PTD freed before original TLS clear'); cleared.append(i)
            tls[a[0]] = a[1]
        elif op == 'TlsGetValue':
            need(a[0] in tls and value == tls[a[0]] == result['tracked_value'], 'same-thread actual TLS readback')
            if not value and cleared: tls_reads.append(i)
        elif op == 'TlsFree': need(value == 1 and a[0] in tls and tls[a[0]] == 0 and tls_reads, 'actual empty TLS slot freed after zero readback'); del tls[a[0]]
    need(not any((heaps, allocations, virtuals, locks, handles, tls)), 'independently reconstructed native resource ledgers all empty')
    need(pending_ptd_free == [417] and cleared == [419] and tls_reads == [420], 'exact original PTD free/clear/readback requests')
    clear_api = next(a for a in r['API_calls'] if a['name'] == 'TlsSetValue' and a['args'][1] == 0)
    need(clear_api['ret'] == 0x575555 and clear_api['TLS_readback'] == {k:v for k,v in replies[420].items() if k != 'direction'}, 'original TLS clear ABI and independent actual zero readback')
    need(byop('GetDC') == [272] and byop('DeleteDC') == [296] and not byop('ReleaseDC') and byop('DC_INFO') == [344],
         'one original GetDC/DeleteDC pair with later metadata query and no duplicate release')
    get_id, delete_id = 272, 296
    dc = replies[get_id]['result']; live = replies[get_id]; dead = replies[delete_id]
    need(dc and requests[get_id]['args'] == [0] and requests[delete_id]['args'] == [dc], 'same owner DC unchanged')
    need(live['baseline_gdi_count'] == 0 and live['baseline_gdi_error'] == 0 and live['live_flush'] == 1 and
         live['live_type'] == 3 and live['live_font'] and live['live_gdi_count'] == 1 and live['live_gdi_error'] == 0,
         'actual OBJ_DC3 current selected font and process GDI rise0to1')
    need(dead['result'] == 1 and dead['dc_retired'] == 1 and dead['before_flush'] == 1 and
         dead['before_type'] == 3 and dead['before_font'] == live['live_font'] and dead['before_gdi_count'] == 1 and
         dead['after_flush'] == 1 and dead['after_type'] == 0 and dead['after_font'] == 0 and
         dead['after_gdi_count'] == dead['baseline_gdi_count'] == 0 and
         all(dead[k] == 0 for k in ('baseline_gdi_error','before_gdi_error','after_gdi_error')),
         'actual original DeleteDC success with lost handle validity and process GDI baseline restored')
    need(dead['last_error'] == live['last_error'] == 0, 'captured original DC LastError remains zero')
    api_get = next(x for x in r['API_calls'] if x['name'] == 'GetDC')
    api_delete = next(x for x in r['API_calls'] if x['name'] == 'DeleteDC')
    leaf_reply = lambda i: {k: v for k, v in replies[i].items() if k != 'direction'}
    need(api_get['ret'] == 0x412fcb and api_get['value'] == dc and api_get['native_leaf'] == leaf_reply(get_id), 'original GetDC binding')
    need(api_delete['ret'] == 0x41341d and api_delete['value'] == 1 and api_delete['native_leaf'] == leaf_reply(delete_id), 'original DeleteDC binding and real return')
    point = r['checkpoints'][1]; game = point['GAME_object']; raw_game = game - 32
    need(point['GAME'] == point['scene'] == 0 and point['GAME_bytes'] == 0xba20 and point['GAME_DC'] == dc and
         point['GAME_drawing_gate'] == '0100' and point['factory_output'] == 0xa5a5a5a5 and point['original_DeleteDC_result'] == 1,
         'constructed GAME remains unpublished')
    need(roots[4]['receiver'] == game and roots[4]['callee'] is True, 'scalar deleting destructor thiscall')
    allocation = point['allocations'][str(raw_game)]
    frees = [i for i in byop('HeapFree') if requests[i]['args'][2] == allocation['native']]
    need(len(frees) == 1 and replies[frees[0]]['result'] == 1 and delete_id < frees[0], 'GAME allocation freed after original DeleteDC')
    follow = replies[344]
    need(requests[344]['args'] == [dc] and follow['result'] == 1 and follow['dc_retired'] == 1 and
         follow['now_flush'] == 1 and follow['now_type'] == follow['now_font'] == 0 and
         follow['now_gdi_count'] == follow['baseline_gdi_count'] == 0 and follow['now_gdi_error'] == follow['baseline_gdi_error'] == 0,
         'follow-up after original GAME free still proves invalid DC and baseline count')
    need(point['DC_after_original_GAME_free'] == {k:v for k,v in follow.items() if k != 'direction'} and
         point['DeleteDC_observations'] == api_delete['native_leaf'] and point['DC_retirement'] == 'original_DeleteDC_with_object_evidence',
         'checkpoint binds original deletion and independent later DC observation')
    main = r['checkpoints'][0]['MAIN']; main_raw = main-32
    need(roots[5]['receiver'] == main and roots[5]['callee'] and roots[6]['args'] == [main], 'original MAIN destructor then matching free')
    main_native = r['checkpoints'][0]['allocations'][str(main_raw)]['native']
    main_frees = [i for i in byop('HeapFree') if requests[i]['args'][2] == main_native]
    need(main_frees == [392] and frees == [340] and 296 < 340 < 344 < 392 < 417 < 419 < 420 < 454 < 455,
         'original GAME/DC/MAIN/PTD/TLS/heap teardown order')
    final_point = r['checkpoints'][2]
    need(not final_point['allocations'] and final_point['MAIN'] == main and final_point['GAME'] == final_point['scene'] == 0,
         'supplementary cleanup leaves original MAIN global unchanged, no fabricated GAME publication')
    need(byop('STATUS') == [456] and byop('Shutdown') == [457], 'normal explicit final status and shutdown')
    empty_keys = ('allocations','memory_bytes','dcs','fonts','retired_fonts','heaps','handles','criticals','tls_slots',
                  'worker_created','worker_resumed','exit_requested','termination_observed','worker_handle_closed')
    for i in (456,457): need(all(replies[i][k] == 0 for k in empty_keys), 'all native resources zero and no worker created')
    need(replies[457]['result'] == 1 and r['status'] == {k:v for k,v in replies[456].items() if k != 'direction'}, 'normal explicit shutdown response')
    closes = r['parent_CloseHandle_receipts']
    need(len(closes) == 7 and all(q['result'] == 1 and q['handle'] for q in closes) and
         [q['before_resume'] for q in closes] == [True, True] + [False] * 5,
         'actual seven successful parent closes in normal empty-Job path')
    cleanup = r['cleanup']; pid = ready['pid']
    need(cleanup['parent_pid'] == pid and cleanup['forced'] is False and cleanup['exits'][str(pid)] == {'wait':0,'code':0} and
         cleanup['deadline_fired'] is False and cleanup['job_empty'] is True and cleanup['handles_closed'] is True and
         cleanup['errors'] == [] and 0 < cleanup['wall_seconds'] <= 30, 'real normal exit0 with empty Job and no forced termination')
    return dict(original_instruction_count=r['final']['instructions'], original_instruction_sites=len(sites), original_API_calls=114,
        CPU57_snapshots=len(states), PTD_readbacks=mirrors, native_requests=len(requests), owner_pid=pid,
        native_MAIN_tid=ready['main_tid'], native_MAIN_teb=ready['main_teb'], native_reader_tid=ready['reader_tid'],
        DC=dict(GetDC_request=get_id, DeleteDC_request=delete_id, DeleteDC_result=1, ReleaseDC_executed=False,
                handle=dc, live_type=3, after_type=0, before_GDI_count=1, baseline_and_after_GDI_count=0,
                original_DeleteDC_resource_retirement_observed=True, independent_followup_DC_INFO_executed=True, DC_INFO_request=344),
        original_PTD_poison=poisoned, PTD_free_request=417, TLS_clear_request=419, actual_zero_TLS_readback_request=420,
        parent_CloseHandle_receipts=closes,
        GAME_allocation_native_free_request=frees[0], original_GAME_constructed=True, original_GAME_destructor_completed=True,
        original_MAIN_destructor_completed=True, original_CRT_teardown_completed=True,
        remaining_tracked_resources_before_normal_exit=dict(heaps=len(heaps), allocations=len(allocations),
            virtual_allocations=len(virtuals), criticals=len(locks), handles=len(handles), TLS_slots=len(tls), live_TLS_values=sum(bool(v) for v in tls.values())),
        cleanup=cleanup)


def review(path):
    need(path.stat().st_size <= 16 * 1024 * 1024, 'bounded compressed source')
    with gzip.open(path, 'rb') as stream:
        raw = stream.read(64 * 1024 * 1024 + 1)
    need(len(raw) <= 64 * 1024 * 1024, 'bounded uncompressed source')
    r = json.loads(raw)
    pins = [r['original'], r['implementation'], r['helper'], *r['implementation_pins']]
    pins += [r['build'][key] for key in ('base_source', 'parent_generator', 'generator', 'generated_source', 'helper')]
    # Reproducible compiler objects may be retired by a separate size/hash
    # manifest. Runtime/source identities above and exact build recipe remain.
    pins += [p for p in r['build']['artifacts'] if Path(p['path']).suffix in ('.cmd', '.log')]
    pins += r['build']['dependencies']
    pins += [r['parent_source'], r['offline_gate'], r['build']['parent_build_report'], r['build']['parent_helper']]
    sdk = Path('C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/um/wingdi.h')
    need('#define OBJ_DC              3' in sdk.read_text(encoding='utf-8'), 'actual pinned SDK OBJ_DC definition')
    for pin in pins:
        p = Path(pin['path']); p = p if p.is_absolute() else ROOT / p
        need(identity(p) == pin, 'unchanged source/build dependency: ' + pin['path'])
    image = (ROOT / r['original']['path']).read_bytes()
    need(len(image) == 5980160 and sha(image) == IMAGE_SHA, 'fixed original game image')
    result = audit(r, image)
    mutations = []; cases = []
    bad = copy.deepcopy(r); code = bytearray.fromhex(bad['instruction_sites'][0]['hex']); code[0] ^= 1
    bad['instruction_sites'][0]['hex'] = code.hex(); cases.append(('original_instruction_byte_changed', bad))
    for label, request, key, value in [('live_DC_after_cleanup',344,'now_type',3),
                                      ('wrong_actual_TLS_zero_readback',420,'result',123),
                                      ('PTD_HeapFree_failed',417,'result',0),
                                      ('DeleteDC_real_return_changed',296,'result',0)]:
        bad=copy.deepcopy(r)
        next(x for x in bad['native_trace'] if x.get('direction')=='response' and x.get('id')==request)[key]=value
        cases.append((label,bad))
    bad=copy.deepcopy(r)
    next(x for x in bad['native_trace'] if x.get('direction')=='request' and x.get('id')==417)['op']='HeapValidate'
    cases.append(('original_PTD_free_omitted',bad))
    bad=copy.deepcopy(r);bad['cleanup']['exits'][str(bad['cleanup']['parent_pid'])]['code']=94
    cases.append(('nonzero_native_process_exit',bad))
    for label, bad in cases:
        try:
            audit(bad, image)
        except ValueError as error:
            mutations.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('tampered evidence accepted: ' + label)
    return dict(schema_version=1, kind='independent_successful_DC_component_record_review_not_replay', review_passed=True,
        component_accepted=True, formal_acceptance=False, independent_full_replay=False, scene_or_wait_accepted=False,
        no_native_execution_by_reviewer=True, no_collector_or_project_module_imports=True,
        source=identity(path), reviewer=identity(__file__), verified_file_pins=len(pins), SDK_OBJ_DC_definition=identity(sdk), checks=result, tamper_rejections=mutations,
        limitations=[
            'This is an independent record/source/build/ABI/resource audit, not an independent complete instruction replay; instruction order and cumulative memory/write digests were not recomputed.',
            'Actual API and metadata observations are supported by pinned helper code/build and same-owner TID/TEB receipts; no independent kernel observer was used.',
            'The original MAIN prefix and complete GAME constructor ran on separate declared guest roots. GAME remained unpublished and413450 was never executed.',
            'Original destructors/CRT cleanup ran as supplementary roots while the WinMain and factory guest stacks remained pending. This is not natural WinMain return or complete factory return.',
            'One fresh no-window component lifetime passed. Two-case formal acceptance, GAME publication, scene worker/cooperative wait and first-result consumption remain unproved.',
            'The source instruction count175031 is the actual record; prior symbolic model175028 is not substituted for the observed count.'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True); parser.add_argument('--out', required=True)
    args = parser.parse_args(); source = (ROOT / args.source).resolve(); out = (ROOT / args.out).resolve()
    need(source.is_relative_to(ROOT) and out.is_relative_to(ROOT) and not out.exists(), 'fresh workspace review output')
    result = review(source)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(out=str(out), review_passed=True, component_accepted=True, native_executed=False)))
