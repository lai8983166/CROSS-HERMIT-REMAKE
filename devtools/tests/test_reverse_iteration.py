import ast
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from devtools import reverse_iteration as iteration
from devtools import terminal_proof_resume as resume


class IterationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'analysis').mkdir()
        (self.root / 'tools').mkdir()
        python = self.root / '.venv-audit/Scripts/python.exe'
        python.parent.mkdir(parents=True)
        python.touch()
        self.prefixes = ['analysis/source-neutral', 'analysis/source-timeout']
        for prefix, case in zip(self.prefixes, ('neutral_running', 'timeout_before_combat')):
            self.write(prefix + '.process.json', dict(source_execution_complete=True,
                       implementation_unchanged=True, case=dict(name=case)))

    def write(self, relative, data):
        path = self.root / relative
        path.write_text(json.dumps(data), encoding='utf8')
        return path

    def plan(self, **options):
        return iteration.plan(self.root, *self.prefixes, 'test-run', **options)

    def scalar_options(self):
        return dict(engine='scalar', neutral_checkpoint=str(self.write('analysis/neutral-proof.json', {})),
                    neutral_checkpoint_sha256='a' * 64,
                    timeout_checkpoint=str(self.write('analysis/timeout-proof.json', {})),
                    timeout_checkpoint_sha256='b' * 64)

    def test_scalar_is_explicit_and_keeps_both_authenticated_full_proofs(self):
        options = self.scalar_options()
        before = set(self.root.rglob('*'))
        planned = self.plan(**options)
        self.assertEqual(before, set(self.root.rglob('*')))
        self.assertEqual(planned['engine'], 'scalar')
        self.assertEqual(planned['default_engine'], 'original')
        self.assertIn('not the existing default', planned['observer_adapter'])
        for index, step in enumerate(planned['steps'][-2:]):
            self.assertIn(iteration.SCALAR_PROOF_MODULE, step['argv'])
            self.assertNotIn(iteration.PROOF_MODULE, step['argv'])
            self.assertEqual(step['engine'], 'scalar')
            self.assertEqual(step['source_replay'], 'authenticated_resume')
            self.assertTrue(step['fresh_native_execution_and_replay'])
            self.assertNotIn('timeout', step)
            auth = planned['steps'][index]
            self.assertIn('devtools.terminal_proof_resume', auth['argv'])
            self.assertEqual(step['argv'][-4:], auth['argv'][-4:])

    def test_scalar_rejects_missing_checkpoint_for_either_case(self):
        options = self.scalar_options()
        for case in ('neutral', 'timeout'):
            partial = dict(options)
            del partial[case + '_checkpoint']
            del partial[case + '_checkpoint_sha256']
            with self.subTest(case=case), self.assertRaisesRegex(ValueError, 'BOTH cases'):
                self.plan(**partial)
        with self.assertRaisesRegex(ValueError, 'BOTH cases'):
            self.plan(engine='scalar')
        with self.assertRaisesRegex(ValueError, 'engine'):
            self.plan(engine='automatic')

    def test_scalar_progress_collision_rejected_during_plan(self):
        options = self.scalar_options()
        output = Path(self.plan(**options)['proof_outputs'][0])
        output.with_suffix('.progress.json').write_bytes(b'previous progress')
        with self.assertRaisesRegex(ValueError, 'progress output already exists'):
            self.plan(**options)

    def test_scalar_busy_refusal_still_precedes_all_launches(self):
        planned = self.plan(**self.scalar_options())
        before = set(self.root.rglob('*'))
        with patch.object(iteration, 'busy_processes', return_value=[{'ProcessId': 1}]), \
                patch.object(iteration, 'run_step') as run:
            with self.assertRaisesRegex(RuntimeError, 'active'):
                iteration.execute(self.root, planned)
        run.assert_not_called()
        self.assertEqual(before, set(self.root.rglob('*')))

    def test_scalar_incomplete_first_proof_stops_before_second_case(self):
        planned = self.plan(**self.scalar_options())
        first = planned['steps'][-2]
        Path(first['proof_output']).write_text(json.dumps(dict(source_and_fresh_case_verified=False)), encoding='utf8')
        seen = []
        original_run_step = iteration.run_step
        def simulated(step, root):
            seen.append(step['name'])
            if step['name'] == 'full-proof-0':
                with patch.object(iteration.subprocess, 'run'):
                    original_run_step(step, root)
        with patch.object(iteration, 'busy_processes', return_value=[]), \
                patch.object(iteration, 'run_step', side_effect=simulated):
            with self.assertRaisesRegex(RuntimeError, 'complete unchanged full proof'):
                iteration.execute(self.root, planned)
        self.assertEqual(seen[-1], 'full-proof-0')
        self.assertNotIn('full-proof-1', seen)
        ledger = iteration.small_json(self.root / '.venv-audit/reverse-iteration/test-run/run.json')
        self.assertEqual(ledger['engine'], 'scalar')
        self.assertFalse(ledger['pipeline_complete'])

    def test_cli_engine_selection_and_original_default(self):
        options = self.scalar_options()
        base = ['pair', '--neutral', self.prefixes[0], '--timeout', self.prefixes[1], '--label', 'test-run']
        for engine in ('original', 'scalar'):
            argv = list(base)
            if engine == 'scalar':
                for key, value in options.items():
                    argv.extend(['--' + key.replace('_', '-'), value])
            output = io.StringIO()
            with patch.object(iteration, 'ROOT', self.root), patch('sys.stdout', output):
                self.assertEqual(iteration.main(argv), 0)
            result = json.loads(output.getvalue())
            self.assertEqual(result['engine'], engine)
            for step in result['steps'][-2:]:
                expected = iteration.SCALAR_PROOF_MODULE if engine == 'scalar' else iteration.PROOF_MODULE
                self.assertIn(expected, step['argv'])

    def test_resume_is_explicit_per_case_and_keeps_original_fresh_proof(self):
        checkpoint = self.write('analysis/checkpoint.json', {})
        prior = self.write('analysis/prior.json', {})
        before = set(self.root.rglob('*'))
        planned = self.plan(neutral_checkpoint=str(checkpoint), neutral_checkpoint_sha256='A' * 64,
                            neutral_prior_orchestrator=str(prior))
        self.assertEqual(before, set(self.root.rglob('*')))
        auth, fresh, other = planned['steps'][0], planned['steps'][-2], planned['steps'][-1]
        self.assertIn('devtools.terminal_proof_resume', auth['argv'])
        expected = ['--source-proof-checkpoint', str(checkpoint), '--source-proof-checkpoint-sha256',
                    'a' * 64, '--prior-orchestrator', str(prior)]
        self.assertEqual(auth['argv'][-6:], expected)
        self.assertEqual(fresh['argv'][-6:], expected)
        self.assertIn(iteration.PROOF_MODULE, fresh['argv'])
        self.assertEqual(fresh['source_replay'], 'authenticated_resume')
        self.assertTrue(fresh['fresh_native_execution_and_replay'])
        self.assertEqual(other['source_replay'], 'full_replay')
        self.assertNotIn('--source-proof-checkpoint', other['argv'])

    def test_missing_or_invalid_explicit_resume_inputs_rejected(self):
        checkpoint = str(self.write('analysis/checkpoint.json', {}))
        for options in (dict(neutral_checkpoint=checkpoint), dict(neutral_checkpoint_sha256='a' * 64),
                        dict(neutral_prior_orchestrator=checkpoint),
                        dict(neutral_checkpoint=checkpoint, neutral_checkpoint_sha256='invalid'),
                        dict(neutral_checkpoint='missing.json', neutral_checkpoint_sha256='a' * 64),
                        dict(neutral_checkpoint=checkpoint, neutral_checkpoint_sha256='a' * 64,
                             neutral_prior_orchestrator='missing.json')):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.plan(**options)

    def test_resume_preflight_failure_short_circuits_before_native_steps(self):
        checkpoint = str(self.write('analysis/checkpoint.json', {}))
        planned = self.plan(timeout_checkpoint=checkpoint, timeout_checkpoint_sha256='a' * 64)
        seen = []
        def run(step, root):
            seen.append(step['name'])
            if step['name'] == 'authenticate-1':
                raise subprocess.CalledProcessError(1, step['argv'])
        with patch.object(iteration, 'busy_processes', return_value=[]), \
                patch.object(iteration, 'run_step', side_effect=run):
            with self.assertRaises(subprocess.CalledProcessError):
                iteration.execute(self.root, planned)
        self.assertEqual(seen, ['authenticate-0', 'authenticate-1'])

    def test_busy_resume_does_not_authenticate_or_launch(self):
        checkpoint = str(self.write('analysis/checkpoint.json', {}))
        planned = self.plan(neutral_checkpoint=checkpoint, neutral_checkpoint_sha256='a' * 64)
        with patch.object(iteration, 'busy_processes', return_value=[{'ProcessId': 1}]), \
                patch.object(iteration, 'run_step') as run:
            with self.assertRaisesRegex(RuntimeError, 'active'):
                iteration.execute(self.root, planned)
        run.assert_not_called()

    def test_plan_has_no_side_effect_and_preserves_full_proof_for_both_cases(self):
        before = set(self.root.rglob('*'))
        result = self.plan()
        self.assertEqual(before, set(self.root.rglob('*')))
        self.assertFalse(result['accepted'])
        self.assertEqual(result['engine'], 'original')
        self.assertEqual([s['name'] for s in result['steps']], [
            'authenticate-0', 'authenticate-1', 'regressions', 'device-probe-0',
            'device-probe-1', 'full-proof-0', 'full-proof-1'])
        for index, step in enumerate(result['steps'][-2:]):
            argv = step['argv']
            self.assertIn(iteration.PROOF_MODULE, argv)
            self.assertEqual(argv[argv.index('--case') + 1], str(index))
            self.assertNotIn('timeout', step)

    def test_active_work_refused_without_creating_or_launching_anything(self):
        before = set(self.root.rglob('*'))
        with patch.object(iteration, 'busy_processes', return_value=[{'ProcessId': 123}]), \
                patch.object(iteration, 'run_step') as run:
            with self.assertRaisesRegex(RuntimeError, 'active'):
                iteration.execute(self.root, self.plan())
            run.assert_not_called()
        self.assertEqual(before, set(self.root.rglob('*')))

    def test_inventory_failure_is_not_treated_as_idle(self):
        with patch.object(iteration, 'busy_processes', side_effect=OSError('inventory failed')), \
                patch.object(iteration, 'run_step') as run:
            with self.assertRaises(OSError):
                iteration.execute(self.root, self.plan())
            run.assert_not_called()

    def test_task_started_between_steps_prevents_next_launch(self):
        # Initial check, lock check, first step, then a foreign task appears.
        with patch.object(iteration, 'busy_processes', side_effect=[[], [], [], [{'ProcessId': 456}]]), \
                patch.object(iteration, 'run_step') as run:
            with self.assertRaisesRegex(RuntimeError, 'active'):
                iteration.execute(self.root, self.plan())
            self.assertEqual(run.call_count, 1)

    def test_representative_failure_never_starts_second_case_or_retries(self):
        seen = []
        def run(step, root):
            seen.append(step['name'])
            if step['name'] == 'full-proof-0':
                raise subprocess.CalledProcessError(1, step['argv'])
        with patch.object(iteration, 'busy_processes', return_value=[]), \
                patch.object(iteration, 'run_step', side_effect=run):
            with self.assertRaises(subprocess.CalledProcessError):
                iteration.execute(self.root, self.plan())
        self.assertEqual(seen[-1], 'full-proof-0')
        self.assertNotIn('full-proof-1', seen)
        ledger = iteration.small_json(self.root / '.venv-audit/reverse-iteration/test-run/run.json')
        self.assertFalse(ledger['pipeline_complete'])
        self.assertFalse(ledger['accepted'])
        self.assertIn('error', ledger['steps'][-1])
        self.check_times(ledger)
        self.assertFalse((self.root / '.venv-audit/reverse-iteration.lock').exists())

    def test_preflight_failure_prevents_all_long_proofs(self):
        seen = []
        def run(step, root):
            seen.append(step['name'])
            if step['name'] == 'regressions':
                raise subprocess.TimeoutExpired(step['argv'], 180)
        with patch.object(iteration, 'busy_processes', return_value=[]), \
                patch.object(iteration, 'run_step', side_effect=run):
            with self.assertRaises(subprocess.TimeoutExpired):
                iteration.execute(self.root, self.plan())
        self.assertEqual(seen, ['authenticate-0', 'authenticate-1', 'regressions'])

    def test_code_change_invalidates_preflight_before_next_step(self):
        def change(step, root):
            (root / 'tools/current.py').write_text('changed = True', encoding='utf8')
        with patch.object(iteration, 'busy_processes', return_value=[]), \
                patch.object(iteration, 'run_step', side_effect=change) as run:
            with self.assertRaisesRegex(RuntimeError, 'implementation changed'):
                iteration.execute(self.root, self.plan())
            self.assertEqual(run.call_count, 1)

    def test_successful_pipeline_still_does_not_declare_final_acceptance(self):
        with patch.object(iteration, 'busy_processes', return_value=[]), \
                patch.object(iteration, 'run_step') as run:
            result = iteration.execute(self.root, self.plan())
        self.assertEqual(run.call_count, 7)
        self.assertTrue(result['pipeline_complete'])
        self.assertFalse(result['accepted'])
        self.check_times(result)

    def check_times(self, result):
        for row in [result] + result['steps']:
            started = datetime.fromisoformat(row['started_at_utc'])
            finished = datetime.fromisoformat(row['finished_at_utc'])
            self.assertIsNotNone(started.tzinfo)
            self.assertIsNotNone(finished.tzinfo)
            self.assertGreaterEqual(row['duration_seconds'], 0)

    def test_devtools_change_also_invalidates_preflight(self):
        (self.root / 'devtools').mkdir()
        def change(step, root):
            (root / 'devtools/terminal_proof_resume.py').write_text('changed = True', encoding='utf8')
        with patch.object(iteration, 'busy_processes', return_value=[]), \
                patch.object(iteration, 'run_step', side_effect=change) as run:
            with self.assertRaisesRegex(RuntimeError, 'implementation changed'):
                iteration.execute(self.root, self.plan())
        self.assertEqual(run.call_count, 1)

    def test_existing_lock_not_removed_or_overwritten(self):
        lock = self.root / '.venv-audit/reverse-iteration.lock'
        lock.write_bytes(b'other owner')
        with patch.object(iteration, 'busy_processes', return_value=[]):
            with self.assertRaises(FileExistsError):
                iteration.execute(self.root, self.plan())
        self.assertEqual(lock.read_bytes(), b'other owner')

    def test_source_case_or_implementation_mismatch_rejected(self):
        for values in (dict(source_execution_complete=False), dict(implementation_unchanged=False),
                       dict(case=dict(name='timeout_before_combat')), dict(error='failed')):
            with self.subTest(values=values):
                data = dict(source_execution_complete=True, implementation_unchanged=True,
                            case=dict(name='neutral_running'))
                data.update(values)
                self.write(self.prefixes[0] + '.process.json', data)
                with self.assertRaises(ValueError):
                    self.plan()

    def test_output_and_native_helper_collisions_refused(self):
        output = Path(self.plan()['proof_outputs'][0])
        output.touch()
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.plan()
        output.unlink()
        (self.root / '.venv-audit' / (output.stem + '-fresh-gpu.exe')).touch()
        with self.assertRaisesRegex(ValueError, 'helper prefix'):
            self.plan()

    def test_labels_and_source_paths_cannot_escape_workspace(self):
        for label in ('../escape', 'a/b', 'x; command', ''):
            with self.assertRaises(ValueError):
                iteration.plan(self.root, *self.prefixes, label)
        with self.assertRaises(ValueError):
            iteration.plan(self.root, '../outside', self.prefixes[1], 'safe')

    def test_exit_zero_is_insufficient_for_full_proof_gate(self):
        output = self.write('analysis/proof.json', dict(source_and_fresh_case_verified=False))
        with patch.object(iteration.subprocess, 'run'):
            with self.assertRaisesRegex(RuntimeError, 'exit zero'):
                iteration.run_step(dict(argv=['fake'], proof_output=str(output)), self.root)

    def test_completed_full_proof_is_not_replaced_by_a_partial_result(self):
        data = dict(source_and_fresh_case_verified=True, implementation_unchanged=True,
                    source_proof={'complete': True}, fresh_proof={'complete': True},
                    fresh_comparison={'complete': True})
        output = self.write('analysis/proof.json', data)
        with patch.object(iteration.subprocess, 'run') as run:
            iteration.run_step(dict(argv=['fake'], proof_output=str(output)), self.root)
            self.assertIsNone(run.call_args.kwargs['timeout'])
            for missing in ('source_proof', 'fresh_proof', 'fresh_comparison'):
                partial = dict(data)
                del partial[missing]
                self.write('analysis/proof.json', partial)
                with self.assertRaisesRegex(RuntimeError, 'exit zero'):
                    iteration.run_step(dict(argv=['fake'], proof_output=str(output)), self.root)

    def test_probe_requires_normal_explicit_resource_release(self):
        for close in ({'ok': True, 'id': 1, 'result': {}}, {'ok': False, 'id': 1}):
            result = subprocess.CompletedProcess([], 0, stdout=json.dumps({'ok': True, 'hello': {}})
                                                 + '\n' + json.dumps(close))
            with patch.object(iteration.subprocess, 'run', return_value=result):
                with self.assertRaisesRegex(RuntimeError, 'release'):
                    iteration.run_step(dict(argv=['fake'], input='', gpu_probe=True, timeout=20), self.root)

    def test_report_groups_identical_failures_and_bounds_receipt_reads(self):
        for index in (1, 2):
            self.write('analysis/terminal-unit-frontends-proof-v' + str(index) + '.json',
                       dict(duration_seconds=10 * index, error='same boundary'))
        path = self.root / 'analysis/terminal-unit-frontends-proof-large.json'
        path.write_bytes(b' ' * (iteration.MAX_RECEIPT + 1))
        result = iteration.report(self.root)
        self.assertEqual(len(result['failures']), 1)
        self.assertEqual(result['failures'][0]['runs'], 2)
        self.assertEqual(result['failures'][0]['process_seconds'], 30)
        self.assertEqual(len(result['unreadable_or_oversized']), 1)
        self.assertIn('NOT elapsed wall time', result['timing_basis'])

    def retirement_summary(self, entries, label='v1'):
        return self.write('analysis/terminal-unit-frontends-development-' + label + '.json', dict(
            selected_fields_from_retired_current_change_reports=True,
            full_original_reports_recoverable=False, failures=entries))

    def test_retired_failure_summary_preserves_identity_and_deduplicates_paths(self):
        original = dict(path='analysis/terminal-unit-frontends-proof-retired.json', bytes=123, sha256='a' * 64)
        entry = dict(original=original, duration_seconds=42, error='retired failure')
        self.retirement_summary([entry, entry])
        self.retirement_summary([entry], 'v2')
        before = set(self.root.rglob('*'))
        result = iteration.report(self.root)
        self.assertEqual(before, set(self.root.rglob('*')))
        self.assertFalse(result['accepted'])
        row = result['failures'][0]
        self.assertEqual(row['runs'], 1)
        self.assertEqual(row['process_seconds'], 42)
        provenance = row['reports'][0]
        self.assertEqual(provenance['original'], original)
        self.assertTrue(provenance['reported_from_retired_summary'])
        self.assertFalse(provenance['original_report_recoverable'])
        self.assertFalse((self.root / original['path']).exists())

    def test_existing_original_wins_over_summary_including_nonstandard_probe_name(self):
        path = 'analysis/terminal-unit-frontends-minimap-smoke-fixture.json'
        self.write(path, dict(duration_seconds=0, error='actual original'))
        self.retirement_summary([dict(original=dict(path=path, bytes=77, sha256='b' * 64),
                                      duration_seconds=100, error='outdated summary')])
        result = iteration.report(self.root)
        self.assertEqual(len(result['failures']), 1)
        row = result['failures'][0]
        self.assertEqual((row['stage'], row['error'], row['runs'], row['process_seconds']),
                         ('development_probe', 'actual original', 1, 0))
        self.assertFalse(row['reports'][0]['reported_from_retired_summary'])
        self.assertTrue(row['reports'][0]['original_report_recoverable'])

    def test_zero_and_unknown_failure_durations_are_distinguished(self):
        self.retirement_summary([
            dict(path='analysis/terminal-unit-frontends-proof-zero.json', duration_seconds=0, error='same'),
            dict(path='analysis/terminal-unit-frontends-proof-null.json', duration_seconds=None, error='same'),
            dict(path='analysis/terminal-unit-frontends-proof-missing.json', error='same')])
        result = iteration.report(self.root)
        row = result['failures'][0]
        self.assertEqual(row['runs'], 3)
        self.assertEqual(row['runs_with_duration'], 1)
        self.assertEqual(row['runs_without_duration'], 2)
        self.assertEqual(row['process_seconds'], 0)
        self.assertEqual(sum(r['duration_seconds'] is None for r in row['reports']), 2)
        self.assertEqual(result['unreadable_or_oversized'], [])

    def test_existing_oversized_original_is_not_claimed_retired(self):
        path = 'analysis/terminal-unit-frontends-proof-large.json'
        (self.root / path).write_bytes(b' ' * (iteration.MAX_RECEIPT + 1))
        self.retirement_summary([dict(original=dict(path=path), duration_seconds=12, error='summary')])
        result = iteration.report(self.root)
        self.assertEqual(result['failures'], [])
        self.assertEqual(len(result['unreadable_or_oversized']), 1)

    def test_successful_fast_proof_reports_stages_and_excludes_progress_files(self):
        stage = dict(name='fresh_original_execution', complete=True, started_at='2026-11-06T00:00:00+00:00',
                     ended_at='2026-11-06T00:00:01+00:00', wall_seconds=1, process_CPU_seconds=0)
        proof = dict(source_and_fresh_case_verified=True, implementation_unchanged=True,
                     source_proof={'complete': True}, fresh_proof={'complete': True}, fresh_comparison={'complete': True},
                     duration_seconds=5, observer_adapter={'name': 'single-register-observation-v1'},
                     CPU_timing_excludes_native_helper_processes=True, stages=[stage])
        self.write('analysis/terminal-unit-frontends-fast-proof-complete.json', proof)
        self.write('analysis/terminal-unit-frontends-fast-proof-complete.progress.json', dict(error='not a proof'))
        partial = dict(proof, source_and_fresh_case_verified=False)
        self.write('analysis/terminal-unit-frontends-fast-proof-partial.json', partial)
        result = iteration.report(self.root)
        self.assertEqual(result['failures'], [])
        self.assertEqual(len(result['completed_proofs']), 1)
        row = result['completed_proofs'][0]
        self.assertEqual(row['engine'], 'scalar')
        self.assertEqual(row['stages'], [stage])
        self.assertFalse(row['accepted'])
        self.assertTrue(row['CPU_timing_excludes_native_helper_processes'])
        self.assertIn('NOT elapsed wall time', result['timing_basis'])

    def test_summary_cannot_follow_paths_outside_analysis(self):
        self.retirement_summary([dict(original=dict(path='../outside.json'), duration_seconds=10, error='bad')])
        result = iteration.report(self.root)
        self.assertEqual(result['failures'], [])
        self.assertEqual(len(result['unreadable_or_oversized']), 1)


class ResumeAuthenticationTests(unittest.TestCase):
    """Run the frozen resume function with tiny data, without importing native modules."""
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'tools').mkdir()
        def identity(path):
            path = Path(path)
            raw = path.read_bytes()
            return dict(path=path.relative_to(self.root).as_posix(), bytes=len(raw),
                        sha256=hashlib.sha256(raw).hexdigest())
        self.identity = identity
        def need(condition, message):
            if not condition:
                raise ValueError(message)
        corpus = SimpleNamespace(ROOT=self.root, identity=identity, read_case=Mock())
        # Compile only this unchanged function; no module-level imports/native initialization.
        frozen = ast.parse((iteration.ROOT / 'tools/terminal_unit_frontends_proof.py').read_text(encoding='utf8'))
        function = next(node for node in frozen.body if isinstance(node, ast.FunctionDef)
                        and node.name == 'resume_source_proof')
        namespace = dict(Path=Path, corpus=corpus, need=need, json=json, hashlib=hashlib)
        exec(compile(ast.Module(body=[function], type_ignores=[]), '<frozen-resume-function>', 'exec'), namespace)
        implementations = {}
        for name in ('proof', 'verification', 'trace', 'retries', 'platform_verification',
                     'inputs_verification', 'other_platform_verification', 'projection_verification'):
            path = self.root / ('tools/terminal_unit_frontends_' + name + '.py')
            path.write_bytes(b'original implementation')
            implementations[path.relative_to(self.root).as_posix()] = identity(path)
        self.data = dict(case={'name': 'neutral_running'}, artifacts=[{'digest': 'source'}],
                         authenticated_helpers={'GPU': 'authenticated', 'CRT': 'authenticated'})
        self.process = {'digest': 'source-process'}
        self.row = {'unit_frontends': {'execution': dict(transactions=[{}], final_trace={'hash': 'trace'},
                                                         final_memory_digest='final-memory')}}
        corpus.read_case.return_value = self.row
        self.completed = dict(transactions=1, final_trace={'hash': 'trace'}, final_memory='final-memory',
                              complete_CPU_and_mapped_memory_compared_at_every_transaction=True,
                              all_cumulative_original_digests_reproduced=True, canonical_trace_matches_source=True,
                              original_wait_reached=True, wait_body_executed=False,
                              outer_result_consumed=False, complete_battle_exit=False)
        self.checkpoint = dict(case_index=0, implementation_unchanged=True, source_process=self.process,
                               source_artifacts=self.data['artifacts'], source_helpers=self.data['authenticated_helpers'],
                               implementation_start=implementations, implementation_end=implementations,
                               source_proof=self.completed)
        self.path = self.root / 'checkpoint.json'
        parent = SimpleNamespace(corpus=lambda: [self.data['case'], {'name': 'timeout_before_combat'}])
        self.proof = SimpleNamespace(authenticate_source=Mock(return_value=(self.data, self.process)),
                                     corpus=corpus, source=SimpleNamespace(previous=SimpleNamespace(
                                         overlay=SimpleNamespace(parent=parent))), need=need,
                                     resume_source_proof=namespace['resume_source_proof'])

    def invoke(self, sha=None, index=0, prior=None):
        self.path.write_text(json.dumps(self.checkpoint), encoding='utf8')
        with patch.object(resume.importlib, 'import_module', return_value=self.proof) as imported:
            result = resume.authenticate_resume('explicit-source', index, str(self.path),
                                                sha or self.identity(self.path)['sha256'], prior)
        imported.assert_called_once_with(iteration.PROOF_MODULE)
        self.proof.authenticate_source.assert_called_once_with('explicit-source')
        return result

    def test_exact_completed_replay_is_authenticated_by_original_function(self):
        result, identity = self.invoke()
        self.assertEqual(result, self.completed)
        self.assertFalse(identity['source_replay_reexecuted'])
        self.assertTrue(identity['all_verification_modules_unchanged'])

    def test_wrong_checkpoint_sha_rejected(self):
        with self.assertRaisesRegex(ValueError, 'SHA'):
            self.invoke(sha='0' * 64)

    def test_wrong_checkpoint_case_rejected(self):
        self.checkpoint['case_index'] = 1
        with self.assertRaisesRegex(ValueError, 'exact case'):
            self.invoke()

    def test_source_case_mismatch_rejected_before_read_case(self):
        with self.assertRaisesRegex(ValueError, 'fixed source case'):
            self.invoke(index=1)
        self.proof.corpus.read_case.assert_not_called()

    def test_source_authentication_failure_prevents_checkpoint_processing(self):
        self.proof.authenticate_source.side_effect = ValueError('actual source digest')
        with self.assertRaisesRegex(ValueError, 'source digest'):
            self.invoke()
        self.proof.corpus.read_case.assert_not_called()

    def test_changed_verification_module_rejected(self):
        (self.root / 'tools/terminal_unit_frontends_verification.py').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'verification implementation remains identical'):
            self.invoke()

    def test_changed_orchestrator_requires_exact_explicit_archive(self):
        path = self.root / 'tools/terminal_unit_frontends_proof.py'
        saved = dict(self.identity(path), source_utf8=path.read_text(encoding='utf8'))
        path.write_bytes(b'changed orchestrator')
        with self.assertRaisesRegex(ValueError, 'verification implementation remains identical'):
            self.invoke()
        self.proof.authenticate_source.reset_mock()
        prior = self.root / 'prior.json'
        prior.write_text(json.dumps(saved), encoding='utf8')
        _, provenance = self.invoke(prior=str(prior))
        self.assertEqual(provenance['historical_orchestrator'], self.identity(prior))
        self.proof.authenticate_source.reset_mock()
        saved['source_utf8'] += 'tampered'
        prior.write_text(json.dumps(saved), encoding='utf8')
        with self.assertRaisesRegex(ValueError, 'historical orchestration bytes'):
            self.invoke(prior=str(prior))

    def test_incomplete_replay_boundary_rejected(self):
        self.completed['canonical_trace_matches_source'] = False
        with self.assertRaisesRegex(ValueError, 'fully completed independent source replay'):
            self.invoke()


if __name__ == '__main__':
    unittest.main()
