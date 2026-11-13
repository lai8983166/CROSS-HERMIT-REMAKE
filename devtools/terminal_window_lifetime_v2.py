"""Versioned entry point for the property fix; original execution and desktop code reused."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import time
from devtools import terminal_window_lifetime as previous
from devtools import terminal_window_native_v3 as native

ROOT, base, need = previous.ROOT, previous.base, previous.need
PARENT_GATE = ROOT/'analysis/terminal-window-lifetime-gate-v1-20261114.json'
PARENT_GATE_SHA = 'e1ae4592be21340811cac8fd4eb3407e264abfc7c0a15d52746a1b15c39afa74'


def build_contract(helper):
    build = json.loads((helper.parent/'static-report.json').read_text(encoding='utf8'))
    for row in [build['generator'], build['generated_source'], build['helper'], *build['inputs']]:
        need(base.identity(ROOT/row['path']) == row, 'exact corrected build input '+row['path'])
    need(build['generator'] == base.identity(native.__file__) and build['helper'] == base.identity(helper), 'current corrected build identity')
    need((ROOT/build['generated_source']['path']).read_bytes() == native.source().encode(), 'exact narrow corrected native generation')
    need(base.identity(PARENT_GATE)['sha256'] == PARENT_GATE_SHA, 'fixed complete symbolic route gate')
    parent = json.loads(PARENT_GATE.read_text(encoding='utf8'))
    need(parent['route_closed'] and not parent['native_executed'], 'previous bounded symbolic route only')
    for row in parent['pins']:
        need(base.identity(ROOT/row['path']) == row, 'unchanged original executor and desktop '+row['path'])
    return build, parent


def prepare(helper, output):
    need(not output.exists() and output.is_relative_to(ROOT/'analysis'), 'fresh F gate output')
    build, parent = build_contract(helper)
    gate = dict(kind='window_property_fix_admission', native_executed=False, formal_acceptance=False,
        collector=base.identity(__file__), native_helper=base.identity(helper),
        parent_symbolic_gate=base.identity(PARENT_GATE), route_model_reused_without_native_claim=True,
        correction=native.self_check(),
        pins=[*parent['pins'], base.identity(__file__), base.identity(native.__file__),
              base.identity(helper.parent/'static-report.json')],
        original_execution_and_desktop_unchanged=True, normal_native_cleanup_proven=False)
    output.write_text(json.dumps(gate, indent=2)+'\n', encoding='utf8', newline='\n')
    return gate


def admission(helper, gate_path):
    build, _ = build_contract(helper)
    gate = json.loads(gate_path.read_text(encoding='utf8'))
    need(gate['collector'] == base.identity(__file__) and gate['native_helper'] == base.identity(helper) and
         not gate['native_executed'] and gate['parent_symbolic_gate'] == base.identity(PARENT_GATE), 'exact corrected offline gate')
    need(gate['correction'] == native.self_check(), 'recorded regression and exact source delta unchanged')
    for row in gate['pins']:
        need(base.identity(ROOT/row['path']) == row, 'unchanged versioned admission '+row['path'])
    need(not (helper.parent/'native-attempt.once').exists(), 'single new native attempt only')
    return build, gate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--execute', action='store_true')
    modes.add_argument('--prepare-gate', action='store_true')
    parser.add_argument('--desktop-until')
    parser.add_argument('--helper')
    parser.add_argument('--gate')
    parser.add_argument('--out')
    args = parser.parse_args()
    if args.prepare_gate:
        need(args.helper and args.gate, 'helper and gate paths required')
        prepare((ROOT/args.helper).resolve(), (ROOT/args.gate).resolve())
        print(json.dumps(dict(gate=base.identity(ROOT/args.gate), native_executed=False)))
        return 0
    if not args.execute:
        print(json.dumps(dict(mode='plan_only', native_executed=False, desktop_used=False,
            native_hard_limit_seconds=20, desktop_total_limit_seconds=60,
            previous_failed_case_unchanged=True, new_desktop_authorization_required=True)))
        return 0
    need(all((args.desktop_until, args.helper, args.gate, args.out)), 'fresh authorization, helper, gate, output required')
    end = datetime.fromisoformat(args.desktop_until)
    need(end.tzinfo is not None, 'explicit authorization timezone')
    remaining = (end-datetime.now(timezone.utc)).total_seconds()
    need(55 <= remaining <= 60, 'fresh at-most60-second desktop authorization required')
    deadline = time.monotonic()+remaining
    helper, gate_path, output = [(ROOT/p).resolve() for p in (args.helper, args.gate, args.out)]
    need(helper.is_relative_to(ROOT/'.venv-audit') and gate_path.is_relative_to(ROOT) and output.is_relative_to(ROOT/'.venv-audit'), 'F workspace evidence only')
    need(not output.exists() and not Path(str(output)+'.desktop.json').exists(), 'fresh immutable output')
    build, gate = admission(helper, gate_path)
    engine, report = previous.DestructionEngine(), {}
    def action():
        need(deadline-time.monotonic() >= 45, 'native20 + containment3 + desktop20.5 reserve')
        report.update(previous.run_native(engine, helper, helper.parent, build, gate))
        report['versioned_entrypoint'] = base.identity(__file__)
        return report
    try:
        previous.desktop.guarded_run(action, str(output)+'.desktop.json', backend=previous.desktop.BoundedDesktop(helper.parent, deadline))
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
