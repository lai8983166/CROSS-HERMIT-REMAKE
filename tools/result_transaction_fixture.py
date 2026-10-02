"""Export joint native snapshots; expectations never come from Godot projections."""
import argparse
import hashlib
import json

from tools.role_application_fixture import fixture as role_fixture, snapshot as role_snapshot
from tools.week_settlement_fixture import fixture as week_fixture
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

REPORT = ROOT / 'analysis/result-transaction-v1-20261002.json'
REPORT_SHA256 = '92662631d86f36b07b1af6ab4847bfb37856b73fe408ba7368d68b231aa63a0e'
ADV_REPORT = ROOT / 'analysis/adv-return-state-v1-20261002.json'
ADV_REPORT_SHA256 = 'b8b93554b9a459b0c01bab7d21c70d2fca31aacd09ee0157b8aa360c0eb09ef6'


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


def fixture(schema_version=2):
    if schema_version not in (1, 2):
        raise ValueError('unknown transaction fixture schema')
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
            # V1 is retained only to reproduce the historical artifact exactly.
            # Original raw `sub` is the 4CE210 second argument, not a subroutine.
            'expected_school_script': [{'path': e['path'],
                ('subroutine' if schema_version == 1 else 'next_task_state'): e['sub']}
                for e in case['events'] if e.get('path') == 'Data\\Adv\\dat\\CH003.ybc'],
            'school_task_executed': False, 'authorizes_persistent_write': False})
    result = {'schema_version': schema_version, 'source_image_sha256': SOURCE_SHA256,
        'source_report_sha256': REPORT_SHA256,
        'source_role_rules_report_sha256': roles['source_report_sha256'],
        'source_week_rules_report_sha256': week['source_report_sha256'],
        'evidence_kind': native['evidence_kind'], 'limitations': native['limitations'],
        'rules': {'role': roles['rules'], 'week': week['rules']}, 'cases': cases,
        'live_witness': False, 'authorizes_persistent_write': False}
    if schema_version == 2:
        proof_bytes = ADV_REPORT.read_bytes()
        if hashlib.sha256(proof_bytes).hexdigest() != ADV_REPORT_SHA256:
            raise ValueError('ADV parameter proof differs from audited bytes')
        proof = json.loads(proof_bytes)
        if proof['source_image_sha256'] != SOURCE_SHA256:
            raise ValueError('unexpected ADV parameter proof image')
        result['script_request_parameter_semantics'] = {
            'source_report_sha256': ADV_REPORT_SHA256, 'loader_va': '0x4ce210',
            'initializer_va': '0x4ce560', 'next_task_field_va': proof['next_task_field_va'],
            'adv_task_body_va': proof['adv_task_body_vtable_entry'],
            'code_file_offset': proof['cases'][0]['initialized']['code_file_offset'],
            'meaning': 'next task state requested after ADV VM completion'}
    return result


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
