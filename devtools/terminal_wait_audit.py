"""Small-report audit and frozen-file preservation; never a functional seal."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess

from devtools.terminal_wait_probe import ROOT, identity, need

BASELINE = 'ea60fcfdc8820fe36c2f7322b0a6acd1b4f83662'
PRESERVATION = 'analysis/reverse-validation-preservation-v1-20261106.json'
STATIC = 'analysis/terminal-wait-static-contract-v2-20261106.json'
REGISTRATION = 'analysis/terminal-wait-registration-v4-20261106.json.gz'


def load(name):
    raw = (ROOT/name).read_bytes()
    need(len(raw) < 2*1024*1024, 'small reports only')
    return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)


def audit():
    fixed = subprocess.check_output(['git', 'show', BASELINE+':'+PRESERVATION], cwd=ROOT)
    need(fixed == (ROOT/PRESERVATION).read_bytes(), 'baseline preservation manifest unchanged')
    prior = json.loads(fixed)
    failures = []
    for item in prior['small_frozen_fresh_SHA']:
        if not (ROOT/item['path']).is_file() or identity(ROOT/item['path']) != item:
            failures.append(item['path'])
    need(not failures, 'frozen small evidence changed: '+repr(failures))
    for item in prior['large_size_only']:
        need((ROOT/item['path']).stat().st_size == item['bytes'], 'retained large extent: '+item['path'])
    baseline_attributes = subprocess.check_output(['git', 'show', BASELINE+':.gitattributes'], cwd=ROOT)
    need((ROOT/'.gitattributes').read_bytes().startswith(baseline_attributes), 'attributes append only')

    cases = []
    for name in ('neutral', 'timeout'):
        path = 'analysis/terminal-wait-probe-v1-'+name+'-20261106.json'
        row = load(path)
        need(row['implementation'] == identity(ROOT/'devtools/terminal_wait_probe.py'), 'current probe bytes match report')
        result = row['result']
        need(row['accepted'] is False and row['identical_second_execution'] is True
             and row['fresh_native_lifetime'] is False and row['independent_platform_proof'] is False,
             'diagnostic has no functional/native acceptance')
        need(result['trace']['instructions'] == 85 and result['trace']['writes'] == 53
             and result['frontier']['PC'] == 0x4223A8 and result['frontier']['args'] == [0x100]
             and result['frontier']['instruction_executed'] is False
             and result['frontier']['native_API_called'] is False, 'exact bounded first OS dependency')
        need(result['before_fields']['task_header_hex'] == bytes(0x30).hex()
             and result['before_fields']['original_MAIN_scheduler_hex'] == bytes(0x120).hex()
             and result['before_fields']['pending_scene_result'] == 1
             and result['after_fields']['flags'] == 0x10000
             and result['after_fields']['pending_scene_result'] == 1,
             'actual missing task/scheduler owners and still-unconsumed result')
        need(all(result[k] is False for k in ('wait_body_completed', 'outer_result_consumed',
             'complete_battle_exit', 'native_execution', 'native_handles_restored_as_live')),
             'all remaining functional boundaries honest')
        checkpoint = row['reused_parent_proof']['checkpoint']
        need(identity(ROOT/checkpoint['path']) == checkpoint, 'fixed completed source replay retained')
        for item in (row['source_process'], row['original'], *row['source_artifacts']):
            need(identity(ROOT/item['path']) == item, 'current source identity retained')
        cases.append(dict(report=identity(ROOT/path), instructions=85, writes=53,
                          source_regions=result['parent']['source_regions'],
                          diagnostic_regions=result['parent']['diagnostic_regions'],
                          duration_seconds=row['duration_seconds']))

    registration = load(REGISTRATION)
    need(registration['error'] is None and registration['normal_cleanup'] is True
         and registration['mechanism_to_CreateThread_verified'] is True
         and registration['supplemental_cleanup_preserved_suspended_stack'] is True
         and registration['implementation_unchanged'] is True, 'registration mechanism and normal cleanup')
    need(registration['frontier']['PC'] == 0x56E0BE
         and registration['frontier']['instruction_executed'] is False
         and registration['frontier']['API_called'] is False, 'CreateThread not yet called')
    for key in ('accepted', 'current_terminal_state_loaded', 'retained_heap_restored',
                'original_CRT_worker_created', 'original_MAIN_scheduler_connected',
                'cooperative_wait_executed', 'outer_result_consumed', 'complete_battle_exit',
                'rewards_or_school_executed', 'independent_full_replay'):
        need(registration[key] is False, 'honest registration scope: '+key)
    for path, item in registration['implementation_end'].items():
        need(identity(ROOT/path) == item, 'unchanged registration dependency: '+path)
    for key in ('CRT', 'scheduler'):
        need(registration[key+'_exit'] == 0
             and registration[key+'_cleanup']['all_owned_resources_released'] is True
             and registration[key+'_cleanup']['forced_cleanup'] is False, 'normal actual native owner exit')
        build = registration['native_builds'][key]
        binary = Path(build['helper_path'])
        need(identity(binary)['sha256'] == build['helper_sha256'], 'actual retained helper identity')
    retired = load('analysis/terminal-wait-registration-development-v1-20261106.json')
    for item in retired['retired']:
        need(not (ROOT/item['path']).exists(), 'retired new development file absent')
    need(sum(item['bytes'] for item in retired['retired']) == retired['retired_bytes'], 'retirement totals')
    static = load(STATIC)
    need(static['checked_instructions'] == 26 and static['accepted'] is False
         and static['dynamic_execution'] is False, 'static contract remains static only')
    reports = sorted((ROOT/'analysis').glob('terminal-wait-*'))
    helpers = sorted((ROOT/'.venv-audit').glob('terminal-wait-registration-v4-20261106-*.exe'))
    evidence = [identity(path) for path in reports+helpers if path.is_file()]
    return dict(schema_version=1, accepted=False, kind='progress_audit_not_functional_acceptance',
                baseline_commit=BASELINE, auditor=identity(Path(__file__)),
                preservation=dict(parent=identity(ROOT/PRESERVATION),
                    small_frozen_files_freshly_hashed=len(prior['small_frozen_fresh_SHA']),
                    large_files_size_only=len(prior['large_size_only']),
                    large_hashes_not_freshly_recomputed=True, old_attributes_preserved_as_prefix=True,
                    inherited_inventory_small_files_exact_and_large_extents_preserved=True,
                    all_assets_rehashed=False),
                cases=cases, registration=identity(ROOT/REGISTRATION),
                registration_original_instructions=sum(s['instructions'] for s in registration['steps']),
                registration_original_writes=sum(s['writes'] for s in registration['steps']),
                new_evidence_before_this_audit=evidence,
                new_local_evidence_bytes_before_this_audit=sum(i['bytes'] for i in evidence),
                newly_retired_files=len(retired['retired']), newly_retired_bytes=retired['retired_bytes'],
                backups_created=0, completed_change_tasks=2, total_change_tasks=8,
                wait_returned=False, result_consumed=False, complete_battle_exit=False,
                full_new_source_or_independent_replay_started=False,
                next_dependency='original derived scene construction and unified current native image/CRT/TLS/event/worker ownership')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = Path(args.out).resolve()
    need(path.is_relative_to(ROOT/'analysis') and not path.exists(), 'fresh local small audit report')
    row = audit()
    raw = json.dumps(row, ensure_ascii=False, indent=2).encode('utf8')+b'\n'
    need(len(raw) < 1024*1024, 'bounded audit')
    with path.open('xb') as stream:
        stream.write(raw)
    print(json.dumps(identity(path)), flush=True)


if __name__ == '__main__':
    main()
