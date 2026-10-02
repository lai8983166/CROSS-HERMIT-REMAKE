"""Export joint native snapshots; expectations never come from Godot projections."""
import argparse
import hashlib
import json

from tools.role_application_fixture import fixture as role_fixture, snapshot as role_snapshot
from tools.week_settlement_fixture import fixture as week_fixture
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

REPORT = ROOT / 'analysis/result-transaction-v1-20261002.json'
REPORT_SHA256 = '92662631d86f36b07b1af6ab4847bfb37856b73fe408ba7368d68b231aa63a0e'


def snapshot(raw):
    result = role_snapshot(raw)
    for key in ('flags', 'availability', 'item_flags'):
        result[key] = raw[key]
    for record, source in zip(result['characters'], raw['characters']):
        if record['character_id'] != source['character_id']:
            raise ValueError('native snapshot identity mismatch')
        for key in ('unlock_flags', 'equipped_skills', 'equipped_items'):
            record[key] = source[key]
    return result


def fixture():
    raw = REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError('joint native report differs from audited bytes')
    native = json.loads(raw)
    if native['source_image_sha256'] != SOURCE_SHA256:
        raise ValueError('unexpected native source image')
    roles, week = role_fixture(), week_fixture()
    contexts = {c['name']: c['context'] for c in roles['cases']}
    cases = []
    for case in native['cases']:
        context_name = 'special_week_boundary' if case['name'] == 'special_complete_week' else case['name']
        cases.append({'name': case['name'], 'context': contexts[context_name],
            'confirmed': case['synthetic_inputs']['confirm'], 'mvp_ready': case['synthetic_inputs']['mvp_ready'],
            'before': snapshot(case['before']), 'expected_after': snapshot(case['after']),
            'expected_before_week': snapshot(case['before_week']) if case['before_week'] else None,
            'expected_branch': case['branch'], 'expected_requested_state': case['requested_state'],
            'expected_week_executed': case['native_week_body_executed'],
            'expected_learning_draws': [d['rand'] for d in case['learning_draws']],
            'expected_rand_state': case['native_rand_state'],
            'expected_school_script': [{'path': e['path'], 'subroutine': e['sub']}
                for e in case['events'] if e.get('path') == 'Data\\Adv\\dat\\CH003.ybc'],
            'school_task_executed': False, 'authorizes_persistent_write': False})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'source_report_sha256': REPORT_SHA256,
        'source_role_rules_report_sha256': roles['source_report_sha256'],
        'source_week_rules_report_sha256': week['source_report_sha256'],
        'evidence_kind': native['evidence_kind'], 'limitations': native['limitations'],
        'rules': {'role': roles['rules'], 'week': week['rules']}, 'cases': cases,
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
