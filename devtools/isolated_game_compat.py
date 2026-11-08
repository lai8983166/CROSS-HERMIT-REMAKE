"""Thirty-second original startup observation in the qualified guest only."""
import argparse
import gzip
import json
from pathlib import Path
from types import SimpleNamespace
from devtools.native_input_isolation import require_qualified_guest


def run(output):
    qualification = require_qualified_guest()  # Before importing/launching original runtime.
    from devtools import terminal_menu_handoff as menu
    from devtools import terminal_startup_handoff as startup
    from devtools.terminal_scene_resources import clone
    original = Path(__file__).read_bytes()
    # This reuses only menu.run's owned launch/activation and fixed asset audit.
    # startup.probe does not call a controller, send input or invoke scene roots.
    from devtools.isolated_guest_dep_observer import DepObserver
    from devtools.isolated_guest_focus import guest_focus_scope, focus_owned_window
    support_paths = [Path(__file__).with_name(name) for name in
                     ('isolated_guest_dep_observer.py', 'isolated_guest_focus.py')]
    support = [menu.base.identity(path) for path in support_paths]
    activations = []
    def focused_probe(pid, owned, progress, duration):
        # This callback is reached only after the original factory + WinMain
        # readiness have been sampled. Avoid perturbing that brief startup gate.
        h = menu.base.original.openp(0x100450, False, pid)
        menu.base.original.check(h, 'read/query-only owned focus handle')
        try:
            c = SimpleNamespace(pid=pid, h=h, owned=owned,
                                get=lambda p,n:menu.base.original.required(h,p,n))
            hwnd = menu.base.original.findwindow(b'Cross Hermit', None)
            activations.append(dict(elapsed=owned.elapsed(), **focus_owned_window(c, hwnd)))
        finally:
            menu.base.original.close(h)
        return startup.probe(pid, owned, progress, duration)
    with guest_focus_scope(), DepObserver() as dep:
        result = clone(menu.run, continue_menu=focused_probe)(output, 30, None, False, 0)
    menu.need(not result['startup_activation'], 'no activation during original factory observation')
    result['startup_activation'] = activations
    result['activation_phase'] = 'after_original_factory_and_WinMain_ready'
    menu.need(support == [menu.base.identity(path) for path in support_paths], 'guest compatibility support stayed frozen')
    menu.need(Path(__file__).read_bytes() == original, 'compatibility observer stayed frozen')
    probe = result.get('probe') or {}
    lifecycle = result['lifecycle']
    counters = [r.get('callback_locals', {}).get('counter') for r in probe.get('samples', [])]
    counters = [c for c in counters if type(c) is int]
    process_ids = {int(pid) for pid in lifecycle['lifetime']['exits']}
    policies_complete = (dep.error is None and {row['pid'] for row in dep.rows} == process_ids and
                         bool(process_ids) and all(row['query_ok'] for row in dep.rows))
    good = (policies_complete and probe.get('error') is None and lifecycle['error'] is None and
            lifecycle.get('ready') is not None and not lifecycle['lifetime']['members_after_cleanup'] and
            not lifecycle['lifetime']['forced_termination'] and
            all(r['restored_exact'] for r in result['mutable_private_runtime_files']) and
            len(counters) >= 2 and counters[-1] > counters[0] and
            not probe.get('host_input_actions') and not probe.get('host_original_calls') and
            not probe.get('host_memory_writes') and bool(result['startup_activation']) and
            all('error' not in a for a in result['startup_activation']))
    result.update(kind='isolated_original_startup_compatibility', input_isolation=qualification,
                  compatibility_observer=menu.base.identity(Path(__file__)),
                  original_startup_compatible=bool(good), original_game_fully_compatible=False,
                  full_battle_exit_accepted=False, accepted=False,
                  startup_counter_range=[counters[0], counters[-1]] if counters else [],
                  collector_keyboard_mouse_actions=0,
                  actual_process_dep_observations=dep.rows, dep_observer_error=dep.error,
                  compatibility_support=support, actual_process_dep_queries_complete=policies_complete)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    output = args.out.resolve()
    root = Path(__file__).resolve().parents[1]
    if not output.is_relative_to(root / 'analysis') or output.exists():
        raise ValueError('new owned bounded report required')
    result = run(output)
    raw = json.dumps(result, separators=(',', ':')).encode()
    if len(raw) > 32 * 1024 * 1024:
        raise ValueError('bounded raw startup observation')
    packed = gzip.compress(raw, mtime=0)
    if len(packed) > 4 * 1024 * 1024:
        raise ValueError('bounded compressed startup observation')
    with output.open('xb') as stream:
        stream.write(packed)
    if not result['original_startup_compatible']:
        raise SystemExit(1)
