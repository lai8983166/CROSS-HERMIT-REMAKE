"""Offline resource/cleanup checks of the fixed native window source, not full replay.

Does not import or launch a collector, call Win32, or reclassify older failures.
The separate independent review covers original instruction/ABI/callback details.
"""
from __future__ import annotations
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'.venv-audit/terminal-window-destruction-build-v2-20261114/native-window-case-v2-host.json.gz'
SOURCE_SHA = '00f48951f7781697207bcfab046cd62b1f69325942ef3eefb436505a791e35c5'
ZERO = 'ui_gate window_modules window_classes windows callback_depth allocations memory_bytes dcs fonts retired_fonts heaps handles criticals tls_slots worker_created worker_resumed'.split()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def identity(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def audit(r, desktop):
    need(r['accepted'] and r['native_executed'] and r['desktop_restored'] and 'failure' not in r, 'successful actual source')
    for key in ('formal_acceptance', 'GAME_published', 'scene_started', 'wait_return', 'first_result_consumption', 'screenshots', 'host_input_sent'):
        need(r[key] is False, 'limited component scope '+key)
    need(not r['outcome']['WinMain_completed'] and not r['outcome']['pending_WinMain_resumable_after_cleanup'], 'supplemental cleanup is not WinMain natural return')
    ready, = r['events']
    need(ready['event'] == 'READY' and ready['pointer_bits'] == 32 and ready['main_tid'] != ready['reader_tid'], 'one actual MAIN owner')
    requests, replies, request_at, reply_at = {}, {}, {}, {}
    for index, row in enumerate(r['native_trace']):
        if row['direction'] == 'request':
            need(row['id'] == len(requests)+1 and row['lane'] == 0, 'sequential MAIN requests')
            requests[row['id']] = row
            request_at[row['id']] = index
        elif 'id' in row and row['direction'] == 'response':
            need(row['id'] in requests and row['id'] not in replies and row['ok'] == 1, 'one successful reply per request')
            need(row['lane'] == 0 and row['tid'] == ready['main_tid'] and row['teb'] == ready['main_teb'], 'fixed real MAIN identity')
            replies[row['id']] = row
            reply_at[row['id']] = index
    need(len(requests) == 519 and requests.keys() == replies.keys(), 'all519 actual requests answered')
    byop = lambda op: [i for i,q in requests.items() if q['op'] == op]
    need(not any(byop(op) for op in ('CreateThread', 'ResumeThread', 'WaitForSingleObject', 'ShowWindow', 'UpdateWindow', 'GetDC')), 'no worker/wait/device expansion')
    heaps, allocations, virtuals, locks, events, tls, modules, classes, windows = set(), {}, set(), set(), set(), {}, set(), {}, set()
    ptd_free, clear, zero_read, main_free = [], [], [], []
    main = r['checkpoints'][0]['MAIN']
    native_main = r['checkpoints'][0]['allocations'][str(main-32)]['native']
    roots = r['roots']
    need([x['entry'] for x in roots] == [0x57b9d0,0x5752d0,0x49dd70,0x44fe60,0x428ad0,0x575450,0x575360,0x57ba60], 'exact construction and supplemental original cleanup roots')
    need(roots[3]['receiver'] == main and roots[3]['callee'] and roots[4]['args'] == [main], 'matching MAIN destructor and free')
    for root in roots[3:]:
        need(root['declared_independent_function_root'] and root['stop_before'] is None and root['after']['cpu']['EIP'] == 0x32000000, 'original cleanup root returned naturally')
        need(root['after']['cpu']['ESP'] == root['stack']['stack_pointer']+4+(4*len(root['args']) if root['callee'] else 0), 'cleanup root stack balance')
    for i in sorted(replies, key=reply_at.get):
        q, s = requests[i], replies[i]
        a, op, value = q['args'], q['op'], s['result']
        if op == 'HeapCreate': need(value and value not in heaps, 'new heap'); heaps.add(value)
        elif op == 'HeapAlloc': need(a[0] in heaps and value and value not in allocations, 'owned allocation'); allocations[value] = (a[0],a[2])
        elif op == 'HeapFree':
            need(value == 1 and a[2] in allocations and allocations[a[2]][0] == a[0], 'successful matching HeapFree')
            references = [p for p in tls.values() if a[2] <= p < a[2]+allocations[a[2]][1]]
            if references:
                need(len(references) == 1 and references[0] == a[2]+32 and s.get('tls_reference_pending_clear') == 1, 'real PTD free pending original clear')
                ptd_free.append(i)
            if a[2] == native_main: main_free.append(i)
            del allocations[a[2]]
        elif op == 'HeapDestroy':
            need(value == 1 and a[0] in heaps and not any((allocations,tls,locks,events)), 'heap destroyed after dependent cleanup')
            heaps.remove(a[0])
        elif op == 'MEM_ALLOC': need(value and value not in virtuals, 'new temporary storage'); virtuals.add(value)
        elif op == 'MEM_FREE': need(value == 1 and a[0] in virtuals and a[0] not in locks, 'temporary freed after lock deletion'); virtuals.remove(a[0])
        elif op == 'InitializeCriticalSection': need(a[0] in virtuals and a[0] not in locks, 'owned native lock'); locks.add(a[0])
        elif op == 'DeleteCriticalSection': need(a[0] in locks and s['void'] == 1, 'actual lock deletion'); locks.remove(a[0])
        elif op == 'CreateEventA': need(value and value not in events, 'new original event'); events.add(value)
        elif op == 'CloseHandle': need(value == 1 and a[0] in events, 'original event closed'); events.remove(a[0])
        elif op == 'TlsAlloc': need(value != 0xffffffff and value not in tls, 'new TLS slot'); tls[value] = 0
        elif op == 'TlsSetValue':
            need(value == 1 and a[0] in tls, 'actual same-thread TLS update')
            if a[1]: need(any(p <= a[1] < p+n for p,(_,n) in allocations.items()), 'live native PTD installed')
            else: need(ptd_free and tls[a[0]], 'PTD free before clear'); clear.append(i)
            tls[a[0]] = a[1]
        elif op == 'TlsGetValue':
            need(a[0] in tls and value == tls[a[0]] == s['tracked_value'], 'actual TLS matches tracked value')
            if clear and not value: zero_read.append(i)
        elif op == 'TlsFree': need(value == 1 and a[0] in tls and tls[a[0]] == 0 and zero_read, 'slot freed after real zero readback'); del tls[a[0]]
        elif op == 'WINDOW_MODULE': need(value and not modules and s['file_closed'] == 1, 'owned resource module'); modules.add(value)
        elif op == 'RegisterClassExA': need(value and not classes, 'new owned class'); classes[value] = next(iter(modules))
        elif op == 'CreateWindowExA': need(value and a[10] in modules and a[11] == main, 'window bound to current MAIN/module'); windows.add(value)
        elif op == 'CB_DESTROY_WINDOW': need(value == 1 and a[1] in windows and s['is_window_after'] == 0 and s['ncdestroy_observed'] == 1, 'actual HWND destruction'); windows.remove(a[1])
        elif op == 'WINDOW_CLOSE':
            need(not windows and s['is_window_after'] == 0 and all(s[k] == 1 for k in ('ncdestroy_observed','quit_posted','property_removed')), 'complete original close')
            need(r['outcome']['close'] == {k:v for k,v in s.items() if k != 'direction'}, 'close receipt binding')
        elif op == 'UnregisterClassA': need(value == 1 and not windows and classes.get(a[0]) == a[1], 'class unregistered after actual HWND death'); del classes[a[0]]
        elif op == 'WINDOW_MODULE_CLOSE': need(value == 1 and not classes and not windows and a[0] in modules, 'module freed after class'); modules.remove(a[0])
        elif op in ('STATUS','Shutdown'):
            need(all(s[k] == 0 for k in ZERO) and not any((heaps,allocations,virtuals,locks,events,tls,modules,classes,windows)), 'native and independently rebuilt resources empty')
    need(main_free == [454] and ptd_free == [479] and clear == [481] and zero_read == [482], 'actual MAIN/PTD free-clear-readback chain')
    need(byop('UnregisterClassA') == [404] and byop('WINDOW_MODULE_CLOSE') == [405] and byop('TlsFree') == [516] and byop('HeapDestroy') == [517], 'ordered window/TLS/heap release')
    clear_api, = [a for a in r['API_calls'] if a['name'] == 'TlsSetValue' and a['args'][1] == 0]
    need(clear_api['ret'] == 0x575555 and clear_api['TLS_readback'] == {k:v for k,v in replies[482].items() if k != 'direction'}, 'original TLS clear and zero read receipt')
    need(clear_api['wire_start'] <= request_at[481] < reply_at[482] < clear_api['wire_end'], 'readback inside original clear API boundary')
    need(r['outcome']['status'] == {k:v for k,v in replies[518].items() if k != 'direction'} and replies[519]['result'] == 1, 'normal empty-resource shutdown')
    cleanup = r['cleanup']
    need(not cleanup['forced'] and not cleanup['deadline_fired'] and not cleanup['errors'] and cleanup['job_empty'] and cleanup['handles_closed'], 'normal bounded cleanup, not containment')
    need(cleanup['exits'] == {str(ready['pid']):dict(wait=0,code=0)} and cleanup['wall_seconds'] <= 20, 'actual owner exit0 within20s')
    need(len(r['parent_CloseHandle_receipts']) == 7 and all(x['result'] == 1 for x in r['parent_CloseHandle_receipts']), 'all seven parent closes succeeded')
    need(desktop['restored'] and desktop['action_started'] and desktop['action_error'] is None and desktop['checks'] == [[],[]] and not desktop['recovery_actions'], 'recorded two stable desktop checks')
    before = desktop['before']
    need(before['input_desktop']['ready'] and before['input_desktop']['input_desktop'] == before['input_desktop']['observer_desktop'] == 'Default', 'actual host desktop baseline')
    need(len(desktop['after']) == 2 and len(desktop['bounded_desktop_processes']) == 4, 'two final reads and four bounded observations')
    for after in desktop['after']:
        for key in ('monitors','taskbars','appbar_state','metrics','shell_window','foreground_identity','taskbar_identities','system_work_area','mode_bytes','last_input_tick'):
            need(before[key] == after[key], 'desktop baseline restored: '+key)
        need(after['input_desktop'] == before['input_desktop'] and after['game_window'] == 0 and not after['desktop_state_written'], 'same unlocked host desktop; no remaining game window')
    need(all(p['mode'] == '--read' and p['completed'] and p['returncode'] == 0 and p['seconds'] <= 5 for p in desktop['bounded_desktop_processes']), 'bounded read-only desktop operations')
    return dict(native_requests=519,MAIN_free=454,PTD_free=479,TLS_clear=481,TLS_zero_readback=482,
        class_unregister=404,module_free=405,TLS_slot_free=516,heap_destroy=517,
        resource_ledgers_empty=True,natural_owner_exit0=True,desktop_restored=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = (ROOT/args.out).resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(), 'fresh small validation report')
    need(identity(SOURCE)['sha256'] == SOURCE_SHA, 'fixed successful source')
    r = json.loads(gzip.decompress(SOURCE.read_bytes()))
    receipt = Path(str(SOURCE)+'.desktop.json')
    desktop = json.loads(receipt.read_text())
    for row in [r['implementation'],r['versioned_entrypoint'],r['original'],*r['implementation_pins']]:
        need(identity(ROOT/row['path']) == row, 'unchanged source '+row['path'])
    checked = audit(r, desktop)
    def reply(data, number):
        return next(x for x in data['native_trace'] if x['direction'] == 'response' and x.get('id') == number)
    mutations = [('MAIN_free_failed',lambda x,d:reply(x,454).update(result=0)),
        ('wrong_MAIN_identity',lambda x,d:reply(x,479).update(tid=1)),
        ('PTD_free_failed',lambda x,d:reply(x,479).update(result=0)),
        ('TLS_still_live',lambda x,d:reply(x,482).update(result=1,tracked_value=1)),
        ('class_unregister_failed',lambda x,d:reply(x,404).update(result=0)),
        ('module_free_failed',lambda x,d:reply(x,405).update(result=0)),
        ('remaining_resource',lambda x,d:reply(x,518).update(allocations=1)),
        ('forced_exit',lambda x,d:x['cleanup'].update(forced=True)),
        ('desktop_geometry_changed',lambda x,d:d['after'][1]['monitors'][0]['mode'].update(width=640))]
    rejections = []
    for name, change in mutations:
        altered, desk = copy.deepcopy(r), copy.deepcopy(desktop)
        change(altered, desk)
        try: audit(altered, desk)
        except ValueError as exc: rejections.append(dict(case=name,reason=str(exc),rejected=True))
        else: raise ValueError('mutation not rejected: '+name)
    report = dict(kind='window_lifetime_resource_validation',source=identity(SOURCE),desktop_receipt=identity(receipt),
        verifier=identity(__file__),native_executed_by_verifier=False,formal_acceptance=False,
        implementation_pins_checked=len(r['implementation_pins']),checks=checked,rejections=rejections,
        limitations='Resource/receipt audit, not independent instruction/memory/digest replay. Original WinMain remains incomplete; no GAME, worker, wait, result consumption or battle acceptance.')
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(report=identity(out),passed=True,rejections=len(rejections))))


if __name__ == '__main__':
    main()
