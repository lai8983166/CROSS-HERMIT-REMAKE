"""Time and prove the scalar observer against frozen source witnesses and checkers."""
import time
IMPORT_STARTED = time.perf_counter()

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import gc
import json
from pathlib import Path
import traceback

from tools import terminal_unit_frontends_proof as frozen
from tools import terminal_unit_frontends_fast as fast

IMPORT_SECONDS = time.perf_counter() - IMPORT_STARTED
corpus, source = frozen.corpus, frozen.source


def utc():
    return datetime.now(timezone.utc).isoformat()


class Timing:
    def __init__(self, report, progress):
        self.report, self.progress = report, progress

    def save(self):
        value = dict(accepted=False, case_index=self.report['case_index'],
                     stages=self.report['stages'], updated_at=utc())
        self.progress.write_text(json.dumps(value, indent=2) + '\n', encoding='utf8')

    @contextmanager
    def stage(self, name):
        row = dict(name=name, started_at=utc(), complete=False)
        self.report['stages'].append(row)
        self.save()
        wall, cpu = time.perf_counter(), time.process_time()
        print('stage start ' + name, flush=True)
        try:
            yield
            row['complete'] = True
        finally:
            row.update(ended_at=utc(), wall_seconds=round(time.perf_counter() - wall, 4),
                       process_CPU_seconds=round(time.process_time() - cpu, 4))
            self.save()
            print('stage end ' + name + ' ' + str(row['wall_seconds']) + 's', flush=True)


def prove(prefix, index, output, checkpoint, checkpoint_sha, prior_orchestrator=None):
    output = Path(output)
    progress = output.with_suffix('.progress.json')
    frozen.need(not output.exists() and not progress.exists(), 'fresh optimized proof output and progress')
    frozen.need(bool(checkpoint) and bool(checkpoint_sha), 'explicit authenticated source replay checkpoint required')
    frozen.need(index in (0, 1), 'fixed original case')
    helper_prefix = output.stem + '-fresh'
    frozen.need(not any((corpus.ROOT / '.venv-audit').glob(helper_prefix + '*')), 'fresh native helper namespace')
    report = dict(schema_version=1, accepted=False, case_index=index,
                  source_and_fresh_case_verified=False, observer_adapter=fast.contract(),
                  stages=[], started_at=utc(), import_wall_seconds=IMPORT_SECONDS,
                  CPU_timing_excludes_native_helper_processes=True)
    timing = Timing(report, progress)
    started = time.perf_counter()
    try:
        report['implementation_start'] = corpus.implementation_files()
        with timing.stage('authenticate_source'):
            data, identity = frozen.authenticate_source(prefix)
            frozen.need(data['case'] == source.previous.overlay.parent.corpus()[index], 'fixed source case identity')
            report.update(source_process=identity, source_artifacts=data['artifacts'],
                          source_helpers=data['authenticated_helpers'])
        with timing.stage('decode_source'):
            row = corpus.read_case(prefix, index)
        with timing.stage('authenticate_completed_source_replay'):
            report['source_proof'], report['resumed_source_proof'] = frozen.resume_source_proof(
                checkpoint, checkpoint_sha, data, identity, row, index, prior_orchestrator)
        with timing.stage('build_fresh_helpers'):
            ch, gh, build = source.images.CORE_helpers(helper_prefix)
        with timing.stage('fresh_original_execution'):
            with fast.scalar_observations():
                full = source.run_case(row['input'], ch, gh)
        with timing.stage('compact_fresh_and_collect'):
            other = corpus.compact_case(full)
            del full
            gc.collect()
        with timing.stage('compare_full_fresh_state_and_raw_traces'):
            report['fresh_comparison'] = frozen.compare_fresh(row, other)
        with timing.stage('independent_fresh_replay'):
            report['fresh_proof'] = frozen.verify_case(other)
        report.update(fresh_helper_build=build, fresh_native_creation=other['platform']['creation'],
                      fresh_CRT_cleanup=other['CRT_cleanup'], fresh_GPU_cleanup=other['GPU_cleanup'])
        with timing.stage('release_witnesses_and_collect'):
            del row, other
            gc.collect()
        frozen.need(source.UnitFrontendMachine is fast.ORIGINAL_MACHINE, 'source construction binding restored')
        report['source_and_fresh_case_verified'] = True
    except Exception as error:
        report.update(error=repr(error), context=getattr(error, 'unit_frontends_context', None),
                      traceback=traceback.format_exc(limit=12))
        raise
    finally:
        report['implementation_end'] = corpus.implementation_files()
        report['implementation_unchanged'] = bool(report.get('implementation_start')) and all(
            report['implementation_end'].get(k) == v for k, v in report.get('implementation_start', {}).items())
        if not report['implementation_unchanged']:
            report['source_and_fresh_case_verified'] = False
        report.update(ended_at=utc(), duration_seconds=round(time.perf_counter() - started, 3))
        with output.open('x', encoding='utf8', newline='\n') as stream:
            json.dump(report, stream, separators=(',', ':'))
            stream.write('\n')
    frozen.need(report['implementation_unchanged'], 'all actual optimized proof implementations unchanged')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--case', type=int, choices=(0, 1), required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--source-proof-checkpoint', required=True)
    parser.add_argument('--source-proof-checkpoint-sha256', required=True)
    parser.add_argument('--prior-orchestrator')
    args = parser.parse_args()
    result = prove(corpus.ROOT / args.source, args.case, corpus.ROOT / args.out,
                   corpus.ROOT / args.source_proof_checkpoint, args.source_proof_checkpoint_sha256,
                   corpus.ROOT / args.prior_orchestrator if args.prior_orchestrator else None)
    # Small console result; full proof remains in its immutable output file.
    print(json.dumps(dict(source_and_fresh_case_verified=result['source_and_fresh_case_verified'],
                          duration_seconds=result['duration_seconds'], stages=result['stages'])), flush=True)
