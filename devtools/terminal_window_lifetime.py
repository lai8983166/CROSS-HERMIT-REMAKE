"""One bounded original window lifetime; plan-only without fresh desktop consent.

This is a window component qualification, not GAME publication or battle exit.
Original WinMain remains paused at4504E1. WM_CLOSE runs the original destruction
callbacks; independent original MAIN/CRT cleanup roots use a separate stack.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import time

from devtools.terminal_window_destruction import DestructionEngine, DestructionOwner, base, need
from devtools.terminal_scene_dc_probe import Owner as CloseObserved
from devtools import terminal_window_desktop as desktop

ROOT = base.ROOT
NATIVE_SECONDS = 20


class Owner(DestructionOwner, CloseObserved):
    def __setattr__(self, name, value):
        # Tighten the inherited watchdog before it is created. This leaves
        # 3s Job containment +20.5s bounded desktop recovery within the60s slot.
        if name == 'deadline' and hasattr(self, 'start'):
            value = min(value, self.start + NATIVE_SECONDS)
        super().__setattr__(name, value)


def execute(engine, owner):
    engine.owner = owner
    owner.callback_handler = engine.callback
    need(owner.call('WINDOW_GATE', 1)['result'] == 1, 'explicit window gate enabled')
    module = owner.call('WINDOW_MODULE')['result']
    need(module, 'current owner resource HINSTANCE before original WinMain')
    engine.root('original_heap_init', 0x57b9d0, (1,))
    need(engine.root('original_MAIN_TLS_init', 0x5752d0) == 1, 'actual original MAIN TLS init')
    # A declared empty WinMain command line, separate from every retained stack.
    command_line = 0x65600000
    engine.u.mem_map(command_line, 4096)
    engine.md.topology()
    engine.put(command_line, b'\0')
    engine.root('original_WinMain_to_MAIN_publication', 0x49dd70,
                (module, 0, command_line, 1), stop=0x49de23)
    main = engine.word(0x7a4a00)
    need(main and engine.word(main) == 0x5986a0, 'original MAIN allocation/vtable/publication')
    need(engine.read(main + 0x64, 256) == bytes(256), 'original empty scheduler buckets')
    engine.bind_window(main, module)
    engine.checkpoint('original_MAIN_before_window_preparation')
    engine.stop, engine.done[0] = 0x4504e1, False
    engine.drive()
    engine.stop = None
    hwnd = engine.window_handle
    need(hwnd and engine.word(0x7a0bb4) == hwnd and engine.class_atom, 'original current HWND publication')
    need(engine.word(0x7a49fc) == 0 and not engine.worker_handle, 'no GAME publication or worker')
    engine.checkpoint('original_HWND_published_before_ShowWindow_or_GAME')
    pending_stack = engine.read(base.cold.old.STACK, 65536)
    pending_cpu = engine.state()['cpu']
    close = owner.call('WINDOW_CLOSE', hwnd)
    engine.assert_closed(close)
    need(engine.state()['cpu'] == pending_cpu and engine.read(base.cold.old.STACK, 65536) == pending_stack,
         'original WinMain remains intact after native close callbacks')
    need(owner.call('UnregisterClassA', engine.class_atom, module)['result'] == 1, 'owned class unregister after HWND destruction')
    need(owner.call('WINDOW_MODULE_CLOSE', module)['result'] == 1, 'owned resource module free after class unregister')
    need(owner.call('WINDOW_GATE', 0)['result'] == 1, 'window gate closed after all window resources')
    engine.stack = base.WORK_STACK
    engine.root('supplemental_original_MAIN_destructor', 0x44fe60, receiver=main, callee=True)
    engine.root('supplemental_original_MAIN_free', 0x428ad0, (main,))
    engine.root('supplemental_original_MAIN_PTD_free_TLS_clear', 0x575450, (0,))
    engine.root('supplemental_original_lock_TLS_teardown', 0x575360)
    engine.root('supplemental_original_heap_teardown', 0x57ba60)
    need(engine.read(base.cold.old.STACK, 65536) == pending_stack, 'pending original WinMain stack never overwritten')
    need(not any((engine.allocations, engine.events, engine.locks, engine.fonts, engine.dcs, engine.heap)), 'original allocations/CRT resources empty')
    status = owner.call('STATUS')
    for field in ('ui_gate', 'window_modules', 'window_classes', 'windows', 'callback_depth', 'allocations',
                  'memory_bytes', 'heaps', 'handles', 'criticals', 'tls_slots', 'fonts', 'dcs'):
        need(status[field] == 0, 'native resource ledger zero: ' + field)
    need(owner.call('Shutdown')['result'] == 1, 'normal resource-empty helper shutdown')
    need(owner.wait(min(1000, max(0, int((owner.deadline-time.monotonic())*1000)))) == 0, 'normal helper exit within hard native budget')
    return dict(close=close, status=status, pending_WinMain_stack_sha256=base.sha(pending_stack),
                WinMain_completed=False, pending_WinMain_resumable_after_cleanup=False)


def run_native(engine, helper, folder, build, gate):
    report = dict(schema_version=1, kind='same_owner_original_window_lifetime', accepted=False,
        formal_acceptance=False, GAME_published=False, scene_started=False, wait_return=False, first_result_consumption=False,
        screenshots=False, host_input_sent=False, native_executed=False, build=build, offline_gate=gate,
        native_hard_limit_seconds=NATIVE_SECONDS,
        implementation=base.identity(__file__), original=base.identity(base.cold.base.SOURCE),
        implementation_pins=base.implementation_pins(), roots=engine.roots, API_calls=engine.records,
        callbacks=engine.callbacks, checkpoints=engine.checkpoints, initial=engine.state())
    marker = folder / 'native-attempt.once'
    with marker.open('x', encoding='utf8') as stream:
        json.dump(dict(helper=base.identity(helper), started_utc=datetime.now(timezone.utc).isoformat()), stream)
    owner = None
    try:
        owner = Owner.__new__(Owner)
        Owner.__init__(owner, helper, folder)
        report['outcome'] = execute(engine, owner)
        report['accepted'] = True
    except BaseException as exc:
        report['failure'] = repr(exc)
        report['first_failure_state'] = engine.state()
    finally:
        if owner is not None and hasattr(owner, 'receipt'):
            owner.finish()
            report.update(native_executed=owner.resumed, native_trace=owner.trace, events=owner.events,
                          cleanup=owner.receipt, parent_CloseHandle_receipts=owner.parent_closes)
            clean = owner.receipt
            if (clean['forced'] or owner.expired or clean['errors'] or not clean['job_empty'] or not clean['handles_closed'] or
                clean['exits'].get(str(clean['parent_pid'])) != dict(wait=0, code=0) or
                len(owner.parent_closes) != 7 or not all(q['result'] == 1 for q in owner.parent_closes)):
                report['accepted'] = False
        report['final'] = engine.state()
        # Callback API states are retained once inside their owning callback.
        report['API_calls'] = [r for r in engine.records if 'callback_id' not in r]
        report['instruction_sites'] = [dict(pc=p, hex=engine.image[p-0x400000:p-0x400000+n].hex(), count=c)
                                       for p, (n, c) in sorted(engine.sites.items())]
    return report


def admission(helper, gate_path):
    from devtools import terminal_window_native_v2 as native
    build = json.loads((helper.parent / 'static-report.json').read_text(encoding='utf8'))
    # The generation check covers the pinned original owner and both extensions.
    need(base.identity(helper) == build['helper'], 'exact current unexecuted helper')
    for key in ('generator', 'parent_generator', 'parent_include', 'resource', 'generated_source'):
        need(base.identity(ROOT/build[key]['path']) == build[key], 'exact build input ' + key)
    need((ROOT / build['generated_source']['path']).read_bytes() == native.source().encode(), 'exact reviewed native generation')
    gate = json.loads(gate_path.read_text(encoding='utf8'))
    need(gate['route_closed'] and not gate['native_executed'] and gate['collector'] == base.identity(__file__), 'bounded complete offline collector gate')
    need(gate['native_helper'] == base.identity(helper), 'offline gate exact native helper')
    for row in gate['pins']:
        need(base.identity(ROOT / row['path']) == row, 'unchanged admitted implementation ' + row['path'])
    need(not (helper.parent/'native-attempt.once').exists(), 'this exact bounded native attempt has not already run')
    return build, gate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--desktop-until')
    parser.add_argument('--helper')
    parser.add_argument('--gate')
    parser.add_argument('--out')
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps(dict(mode='plan_only', desktop_used=False, native_executed=False,
            native_hard_limit_seconds=NATIVE_SECONDS, desktop_total_limit_seconds=60,
            route='originalCRT/MAIN->originalwindow->4504E1->nativeWM_CLOSE->originalDestroy/quit/property->class/module->originalMAIN/PTD/CRT cleanup',
            excluded=['GAME','ShowWindow/UpdateWindow','D3D/gamma/input','battle','screenshots'])))
        return 0
    need(all((args.desktop_until, args.helper, args.gate, args.out)), 'fresh authorization deadline, helper, offline gate and output required')
    end = datetime.fromisoformat(args.desktop_until)
    need(end.tzinfo is not None, 'explicit authorization timezone')
    remaining = (end-datetime.now(timezone.utc)).total_seconds()
    need(55 <= remaining <= 60, 'fresh at-most60-second desktop authorization required')
    deadline = time.monotonic() + remaining
    helper, gate_path, output = [(ROOT / p).resolve() for p in (args.helper, args.gate, args.out)]
    need(helper.is_relative_to(ROOT / '.venv-audit') and gate_path.is_relative_to(ROOT) and output.is_relative_to(ROOT / '.venv-audit'), 'F workspace runtime evidence only')
    need(not output.exists() and not Path(str(output)+'.desktop.json').exists(), 'fresh immutable output')
    build, gate = admission(helper, gate_path)
    engine = DestructionEngine()
    report = {}
    def action():
        need(deadline-time.monotonic() >= 45, 'reserve native20 plus containment3 and desktop20.5 before launch')
        report.update(run_native(engine, helper, helper.parent, build, gate))
        return report
    try:
        desktop.guarded_run(action, str(output)+'.desktop.json', backend=desktop.BoundedDesktop(helper.parent, deadline))
        report['desktop_restored'] = True
    except BaseException as exc:
        report.update(accepted=False, desktop_restored=False, desktop_error=repr(exc))
    report['authorization_deadline'] = end.isoformat()
    payload = gzip.compress(json.dumps(report, separators=(',', ':')).encode(), mtime=0)
    need(len(payload) < 16*1024*1024, 'bounded16MiB new evidence')
    output.write_bytes(payload)
    print(json.dumps(dict(output=base.identity(output), accepted=report.get('accepted', False), failure=report.get('failure'), desktop_error=report.get('desktop_error'))))
    return 0 if report.get('accepted') else 1


if __name__ == '__main__':
    raise SystemExit(main())
