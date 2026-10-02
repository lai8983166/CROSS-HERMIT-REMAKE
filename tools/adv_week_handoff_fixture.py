"""Export joint native ADV/roster/week snapshots, never compose old outputs."""
import argparse
import hashlib
import json

from tools.roster_join_fixture import fixture as join_fixture, snapshot
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

REPORT = ROOT / 'analysis/adv-week-handoff-v1-20261002.json'
REPORT_SHA256 = 'bb33d56f93c05ce2adef77d75e540d0e98d9ec52e7e2f620c5bbc24911a23655'


def fixture():
    raw = REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError('joint handoff differs from audited bytes')
    joined = join_fixture()  # Source EXE, chapter, rules and native report hash guards.
    native = json.loads(raw)
    cases = []
    for c in native['cases']:
        requests = [{'path': 'Data\\Adv\\dat\\CH001.ybc', 'next_task_state': e['next_task_state']}
                    for e in c['week_start_events'] if e['kind'] == 'script_load']
        cases.append({'name': c['name'], 'join_context': joined['cases'][0]['context'],
            'week_context': {'task_state': 7, 'adv_completed': c['chapter']['chapter_completed']},
            'before': snapshot(c['chapter']['before']), 'expected_after_adv': snapshot(c['after_adv']),
            'expected_after_week': snapshot(c['after']), 'week_fade_ready': c['week_fade_ready'],
            'expected_week_executed': c['week_executed'], 'expected_script_requests': requests,
            'native_adv_state_requests': c['chapter']['state_requests'],
            'native_consumed_request': c['consumed_request'],
            'native_week_events': c['week_events'], 'ch001_body_executed': False,
            'authorizes_persistent_write': False})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'source_report_sha256': REPORT_SHA256, 'rules': joined['rules'],
        'evidence_kind': 'shared_native_adv_and_week_projection_fixture',
        'limitations': native['limitations'], 'cases': cases,
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT / args.out
    if path.exists():
        parser.error('output already exists; use a new path')
    payload = report_text(fixture())
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
