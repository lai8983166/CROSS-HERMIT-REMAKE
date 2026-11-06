"""Development orchestration only. Never replaces or declares final acceptance.

report/plan read small receipts without importing the reverse-engineering stack.
pair --execute requires an idle Windows host and calls the existing full proof.
"""
import argparse
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
MAX_RECEIPT = 2 * 1024 * 1024
PROOF_MODULE = 'tools.terminal_unit_frontends_proof'
SCALAR_PROOF_MODULE = 'tools.terminal_unit_frontends_fast_proof'
BUSY_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$rows = @(Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -match '^python(w)?\.exe$' -and
     $_.CommandLine -match '(tools[.\\/](terminal|battle|school)_|unit_frontends)') -or
    $_.Name -match '^(terminal|battle|school)[-_].*\.exe$'
} | Select-Object ProcessId,Name)
ConvertTo-Json -InputObject $rows -Compress
"""


def small_json(path):
    # Read cap also applies if a concurrently written file grows after stat().
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_RECEIPT + 1)
    if len(raw) > MAX_RECEIPT:
        raise ValueError('receipt exceeds 2 MiB: ' + str(path))
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError('receipt is not an object: ' + str(path))
    return data


def report(root):
    """No full corpora, recursive historical manifests, native APIs or imports."""
    groups = defaultdict(lambda: dict(runs=0, process_seconds=0.0, runs_with_duration=0,
                                      runs_without_duration=0, receipts=[], reports=[]))
    sources, proofs, skipped, retired = [], [], [], {}
    paths = set((root / 'analysis').glob('terminal-unit-frontends-source-*.process.json'))
    paths.update((root / 'analysis').glob('terminal-unit-frontends-proof-*.json'))
    paths.update((root / 'analysis').glob('terminal-unit-frontends-fast-proof-*.json'))
    paths = {path.resolve() for path in paths if not path.name.endswith('.progress.json')}

    def duration(value):
        if value is not None and (type(value) not in (float, int) or not math.isfinite(value) or value < 0):
            raise ValueError('invalid duration')
        return value  # Null/missing is unknown, never a measured zero.

    def stage_for(path):
        if path.name.endswith('.process.json'):
            return 'source'
        return 'proof' if '-proof-' in path.name else 'development_probe'

    def add_failure(path, data, provenance):
        seconds = duration(data.get('duration_seconds'))
        error = str(data.get('error') or '')
        if not error:
            return
        row = groups[(stage_for(path), error)]
        row['runs'] += 1
        row['process_seconds'] += seconds if seconds is not None else 0
        row['runs_with_duration' if seconds is not None else 'runs_without_duration'] += 1
        row['receipts'].append(path.name)
        row['reports'].append(dict(path=path.relative_to(root.resolve()).as_posix(),
                                   duration_seconds=seconds, **provenance))

    # Only explicit small retirement summaries; never follow arbitrary report trees.
    for summary in sorted((root / 'analysis').glob('terminal-unit-frontends-development-*.json')):
        try:
            data = small_json(summary)
            if (data.get('selected_fields_from_retired_current_change_reports') is not True or
                    data.get('full_original_reports_recoverable') is not False or
                    not isinstance(data.get('failures'), list)):
                raise ValueError('not an explicit retired-report summary')
            for entry in data['failures']:
                try:
                    original = entry.get('original') or {key: entry[key] for key in ('path', 'bytes', 'sha256') if key in entry}
                    if not isinstance(original, dict) or not isinstance(original.get('path'), str):
                        raise ValueError('missing original report path')
                    path = (root / original['path']).resolve()
                    if (path.parent != (root / 'analysis').resolve() or path.suffix != '.json' or
                            not path.name.startswith('terminal-unit-frontends-')):
                        raise ValueError('retired report path must be a project analysis receipt')
                    duration(entry.get('duration_seconds'))
                    if path.exists():
                        paths.add(path)  # The actual receipt wins, even when too large or unreadable.
                    else:
                        retired.setdefault(path, (entry, dict(
                            reported_from_retired_summary=True, original_report_recoverable=False,
                            original={key: original[key] for key in ('path', 'bytes', 'sha256') if key in original},
                            summary=summary.relative_to(root).as_posix())))
                except (OSError, ValueError, TypeError, AttributeError) as error:
                    skipped.append(dict(receipt=summary.name, reason=str(error)))
        except (OSError, ValueError, TypeError) as error:
            skipped.append(dict(receipt=summary.name, reason=str(error)))
    for path in sorted(paths):
        try:
            data = small_json(path)
            seconds = duration(data.get('duration_seconds'))
            stage = stage_for(path)
            error = str(data.get('error') or '')
            if error:
                # Preserve address/transaction numbers; different failures stay distinct.
                add_failure(path, data, dict(reported_from_retired_summary=False, original_report_recoverable=True))
            elif stage == 'source' and data.get('source_execution_complete') is True:
                sources.append(dict(receipt=path.name, process_seconds=seconds,
                                    implementation_unchanged=data.get('implementation_unchanged') is True,
                                    reuse_requires_authentication=True))
            elif (stage == 'proof' and data.get('source_and_fresh_case_verified') is True and
                  data.get('implementation_unchanged') is True and all(data.get(key) for key in
                  ('source_proof', 'fresh_proof', 'fresh_comparison'))):
                stages = []
                for item in data.get('stages', []):
                    if not isinstance(item, dict) or item.get('complete') is not True:
                        raise ValueError('successful proof contains an incomplete or invalid timing stage')
                    stages.append(dict(name=item.get('name'), complete=True, started_at=item.get('started_at'),
                                       ended_at=item.get('ended_at'), wall_seconds=duration(item.get('wall_seconds')),
                                       process_CPU_seconds=duration(item.get('process_CPU_seconds'))))
                scalar = data.get('observer_adapter', {}).get('name') == 'single-register-observation-v1'
                proofs.append(dict(receipt=path.name, engine='scalar' if scalar else 'original',
                                   process_seconds=seconds, stages=stages, accepted=False,
                                   started_at=data.get('started_at'), ended_at=data.get('ended_at'),
                                   CPU_timing_excludes_native_helper_processes=data.get('CPU_timing_excludes_native_helper_processes'),
                                   reuse_requires_authentication=True))
        except (OSError, ValueError, TypeError, AttributeError) as error:
            skipped.append(dict(receipt=path.name, reason=str(error)))
    for path, (entry, provenance) in sorted(retired.items()):
        if path not in paths:
            add_failure(path, entry, provenance)
    return dict(development_only=True, accepted=False,
                timing_basis='sum of known individual process durations; NOT elapsed wall time; null durations are unknown',
                completed_sources=sources, completed_proofs=proofs,
                failures=[dict(stage=stage, error=error, **value)
                          for (stage, error), value in sorted(groups.items())],
                unreadable_or_oversized=skipped,
                advice='Use an authenticated bounded failure checkpoint for local diagnosis; '
                       'reuse successful sources only if their existing authentication passes. '
                       'No source regeneration, retry, deletion or acceptance is automatic.')


def busy_processes():
    if sys.platform != 'win32':
        raise RuntimeError('execution requires Windows process inventory; use report/plan here')
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', BUSY_SCRIPT],
                            capture_output=True, text=True, timeout=15, check=True)
    rows = json.loads(result.stdout)
    if not isinstance(rows, list):
        raise RuntimeError('invalid process inventory; refusing execution')
    return rows


def require_idle():
    rows = busy_processes()
    if rows:
        raise RuntimeError('reverse work is active; no tasks started or stopped: ' + json.dumps(rows))


def local_prefix(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to((root / 'analysis').resolve()):
        raise ValueError('source prefix must be inside project analysis/')
    return path


def resume_options(root, checkpoint=None, sha256=None, prior_orchestrator=None):
    if bool(checkpoint) != bool(sha256):
        raise ValueError('source-proof checkpoint requires its explicit SHA-256')
    if prior_orchestrator and not checkpoint:
        raise ValueError('prior orchestrator requires a source-proof checkpoint')
    if not checkpoint:
        return []
    if not re.fullmatch(r'[0-9a-fA-F]{64}', sha256):
        raise ValueError('checkpoint SHA-256 must have exactly 64 hexadecimal characters')
    # Do not open a corpus or import the verifier during a read-only plan.
    path = (root / checkpoint).resolve()
    if not path.is_file():
        raise ValueError('explicit source-proof checkpoint is missing: ' + str(path))
    args = ['--source-proof-checkpoint', str(path),
            '--source-proof-checkpoint-sha256', sha256.lower()]
    if prior_orchestrator:
        prior = (root / prior_orchestrator).resolve()
        if not prior.is_file():
            raise ValueError('explicit prior orchestrator is missing: ' + str(prior))
        args.extend(['--prior-orchestrator', str(prior)])
    return args


def plan(root, neutral, timeout, label, *, engine='original', neutral_checkpoint=None, neutral_checkpoint_sha256=None,
         neutral_prior_orchestrator=None, timeout_checkpoint=None, timeout_checkpoint_sha256=None,
         timeout_prior_orchestrator=None):
    if engine not in ('original', 'scalar'):
        raise ValueError('proof engine must be original or scalar')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', label):
        raise ValueError('run label must be 1-64 ASCII letters/digits, hyphen or underscore')
    python = root / '.venv-audit/Scripts/python.exe'
    if not python.is_file():
        raise ValueError('project audit Python is missing')
    prefixes = [local_prefix(root, neutral), local_prefix(root, timeout)]
    if prefixes[0] == prefixes[1]:
        raise ValueError('two distinct source cases required')
    resumes = [resume_options(root, neutral_checkpoint, neutral_checkpoint_sha256, neutral_prior_orchestrator),
               resume_options(root, timeout_checkpoint, timeout_checkpoint_sha256, timeout_prior_orchestrator)]
    if engine == 'scalar' and not all(resumes):
        raise ValueError('scalar engine requires explicit source-proof checkpoint and SHA-256 for BOTH cases')
    proof_module = SCALAR_PROOF_MODULE if engine == 'scalar' else PROOF_MODULE
    steps = []
    for index, (prefix, case) in enumerate(zip(prefixes, ('neutral_running', 'timeout_before_combat'))):
        receipt = small_json(str(prefix) + '.process.json')
        if (receipt.get('source_execution_complete') is not True or
                receipt.get('implementation_unchanged') is not True or receipt.get('error') or
                receipt.get('case', {}).get('name') != case):
            raise ValueError('incomplete, changed, or wrong source case: ' + str(prefix))
        # The existing authentication owns all authoritative identity checks.
        if resumes[index]:
            argv = [str(python), '-B', '-X', 'utf8', '-m', 'devtools.terminal_proof_resume',
                    '--source', str(prefix), '--case', str(index)] + resumes[index]
        else:
            code = ('from tools.terminal_unit_frontends_proof import authenticate_source; '
                    'import sys; authenticate_source(sys.argv[1])')
            argv = [str(python), '-B', '-X', 'utf8', '-c', code, str(prefix)]
        steps.append(dict(name='authenticate-' + str(index),
                          argv=argv, timeout=120,
                          source_replay='authenticated_resume' if resumes[index] else 'full_replay'))
    steps.append(dict(name='regressions', argv=[str(python), '-B', '-X', 'utf8', '-m', 'unittest',
                      'discover', '-s', 'tools/tests', '-p', 'test_terminal_unit_frontends_*.py'], timeout=180))
    for index, prefix in enumerate(prefixes):
        helper = root / '.venv-audit' / (prefix.name + '-' + str(index) + '-gpu.exe')
        steps.append(dict(name='device-probe-' + str(index), argv=[str(helper)], timeout=20,
                          input='{"id":1,"op":"close"}\n', gpu_probe=True))
    outputs = []
    for index, prefix in enumerate(prefixes):
        output = root / 'analysis' / ('terminal-unit-frontends-proof-' + label + '-' + str(index) + '.json')
        if output.exists():
            raise ValueError('proof output already exists: ' + str(output))
        if engine == 'scalar' and output.with_suffix('.progress.json').exists():
            raise ValueError('scalar proof progress output already exists: ' + str(output.with_suffix('.progress.json')))
        # Existing proof also builds helpers using output.stem + "-fresh".
        if any((root / '.venv-audit').glob(output.stem + '-fresh*')):
            raise ValueError('fresh helper prefix already used: ' + output.stem)
        outputs.append(str(output))
        steps.append(dict(name='full-proof-' + str(index),
                          argv=[str(python), '-B', '-X', 'utf8', '-m', proof_module,
                                '--case', str(index), '--source', str(prefix), '--out', str(output)] + resumes[index],
                          engine=engine,
                          source_replay='authenticated_resume' if resumes[index] else 'full_replay',
                          fresh_native_execution_and_replay=True, proof_output=str(output)))
    run_dir = root / '.venv-audit/reverse-iteration' / label
    if run_dir.exists():
        raise ValueError('run label already used: ' + label)
    return dict(development_only=True, accepted=False, run_dir=str(run_dir), steps=steps,
                engine=engine, default_engine='original',
                observer_adapter=('explicit opt-in single-register-observation-v1; not the existing default'
                                  if engine == 'scalar' else 'unchanged original observer'),
                proof_outputs=outputs, scheduling='representative first; stop on any failure; no automatic retries',
                final_acceptance='full source replay or authenticated resume, fresh native execution, frozen '
                                 'comparison and independent replay for BOTH cases, then independent review, '
                                 'preservation, strict specification checks and sealing')


def fingerprints(root):
    # Small implementation files only; never read historical multi-GiB witnesses.
    paths = sorted(p for directory in ('tools', 'devtools') for p in (root / directory).rglob('*')
                   if p.is_file() and p.suffix in ('.py', '.cs'))
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


@contextmanager
def execution_lock(root):
    path = root / '.venv-audit/reverse-iteration.lock'
    # Exclusive lock coordinates this wrapper, NOT arbitrary external launchers.
    with path.open('x', encoding='utf8') as stream:
        stream.write(json.dumps(dict(pid=os.getpid(), started=datetime.now(timezone.utc).isoformat())))
    try:
        yield
    finally:
        path.unlink()


def run_step(step, root):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    if step.get('gpu_probe'):
        result = subprocess.run(step['argv'], cwd=root, env=env, input=step['input'],
                                text=True, capture_output=True, timeout=step['timeout'], check=True)
        rows = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        if (len(rows) != 2 or rows[0].get('ok') is not True or 'hello' not in rows[0] or
                rows[1].get('ok') is not True or rows[1].get('id') != 1 or
                rows[1].get('result', {}).get('all_owned_resources_released') is not True):
            raise RuntimeError('device probe failed or did not release all owned resources')
        return
    # Full proof has no wrapper time limit and its original checks are untouched.
    subprocess.run(step['argv'], cwd=root, env=env, timeout=step.get('timeout'), check=True)
    if step.get('proof_output'):
        proof = small_json(step['proof_output'])
        if (proof.get('source_and_fresh_case_verified') is not True or
                proof.get('implementation_unchanged') is not True or proof.get('error') or
                not proof.get('source_proof') or not proof.get('fresh_proof') or
                not proof.get('fresh_comparison')):
            raise RuntimeError('exit zero without a complete unchanged full proof')


def execute(root, planned):
    require_idle()  # Refusal must not even create a run directory or lock.
    wall_started = datetime.now(timezone.utc).isoformat()
    pipeline_started = time.monotonic()
    ledger = dict(development_only=True, accepted=False, pipeline_complete=False, steps=[],
                  engine=planned['engine'], observer_adapter=planned['observer_adapter'],
                  started_at_utc=wall_started, timing_basis='UTC wall timestamps; monotonic elapsed seconds')
    with execution_lock(root):
        require_idle()
        destination = Path(planned['run_dir'])
        destination.mkdir(parents=True, exist_ok=False)
        initial = fingerprints(root)
        try:
            for step in planned['steps']:
                require_idle()
                if fingerprints(root) != initial:
                    raise RuntimeError('implementation changed since preflight; do not reuse the gate')
                record = dict(name=step['name'], argv=step['argv'], completed=False,
                              started_at_utc=datetime.now(timezone.utc).isoformat())
                if 'source_replay' in step:
                    record['source_replay'] = step['source_replay']
                if 'engine' in step:
                    record['engine'] = step['engine']
                ledger['steps'].append(record)
                started = time.monotonic()
                print('reverse-iteration: ' + step['name'], flush=True)
                try:
                    run_step(step, root)
                    record['completed'] = True
                except BaseException as error:
                    record['error'] = repr(error)
                    raise
                finally:
                    record['duration_seconds'] = round(time.monotonic() - started, 3)
                    record['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
            if fingerprints(root) != initial:
                raise RuntimeError('implementation changed during execution')
            ledger['pipeline_complete'] = True
        except BaseException as error:
            ledger['error'] = repr(error)
            raise
        finally:
            ledger['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
            ledger['duration_seconds'] = round(time.monotonic() - pipeline_started, 3)
            with (destination / 'run.json').open('x', encoding='utf8') as stream:
                json.dump(ledger, stream, indent=2, ensure_ascii=False)
                stream.write('\n')
    return ledger


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('report', help='read-only small-receipt failure/timing summary')
    pair = sub.add_parser('pair', help='plan by default; explicit execution only on an idle Windows host')
    pair.add_argument('--neutral', required=True, help='source prefix, without .process.json')
    pair.add_argument('--timeout', required=True, help='source prefix, without .process.json')
    pair.add_argument('--label', required=True, help='unused run/output label')
    pair.add_argument('--engine', choices=('original', 'scalar'), default='original',
                      help='original by default; scalar explicitly opts into the observation adapter and requires both checkpoints')
    for case in ('neutral', 'timeout'):
        pair.add_argument('--' + case + '-checkpoint', help='explicit completed source-replay checkpoint')
        pair.add_argument('--' + case + '-checkpoint-sha256', help='explicit immutable checkpoint SHA-256')
        pair.add_argument('--' + case + '-prior-orchestrator', help='explicit archived orchestration bytes')
    pair.add_argument('--execute', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'report':
            value = report(ROOT)
        else:
            options = {case + '_' + key: getattr(args, case + '_' + key)
                       for case in ('neutral', 'timeout')
                       for key in ('checkpoint', 'checkpoint_sha256', 'prior_orchestrator')}
            value = plan(ROOT, args.neutral, args.timeout, args.label, engine=args.engine, **options)
            if args.execute:
                value = execute(ROOT, value)
        print(json.dumps(value, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('reverse-iteration: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
