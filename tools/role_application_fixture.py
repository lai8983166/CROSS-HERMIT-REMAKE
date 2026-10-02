"""Source tables and native expectations for isolated state12 role application."""
import argparse
import hashlib
import json
import struct

from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, report_text

REPORT = ROOT / 'analysis/role-application-v1-20261002.json'
REPORT_SHA256 = '3f83ad1337309c70e1f9154569a7f9267ef205bcdf7a83e4d8ff538b6c03385f'


def snapshot(raw):
    result = {key: raw[key] for key in ('month', 'week', 'global_total_511c',
        'recipient_id', 'relationships', 'nonparticipant_character_sha256',
        'nonparticipant_package_hex')}
    result['characters'] = []
    for record in raw['characters']:
        result['characters'].append({**{key: record[key] for key in (
            'character_id', 'job', 'attributes', 'growth_pools', 'level_50',
            'skill_statuses', 'staged_package', 'staged_total', 'recipient_count')},
            'job_progress': record['job_progress_values'],
            'week_records': list(bytes.fromhex(record['week_records_hex']))})
    return result


def fixture():
    image, raw = SOURCE.read_bytes(), REPORT.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256 or hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError('source image or native role report differs from audited bytes')
    def integers(va, count):
        return list(struct.unpack_from('<'+str(count)+'i', image, va-0x400000))
    grid = [[0]*7 for _ in range(12)]
    skills = []
    for sid in range(1, 85):
        at = 0x6C2DCC+sid*0x48-0x400000
        category, position = image[at], image[at+3]
        grid[category-1][position-1] = sid
        req = 0x74F686+sid*0x32-0x400000
        skills.append({'minimum_attributes': list(struct.unpack_from('<7h', image, req)),
            'minimum_total': struct.unpack_from('<h', image, req+14)[0],
            'minimum_job_sums': list(struct.unpack_from('<5h', image, req+16)),
            'learned_points': integers(0x6C2E08+sid*0x48, 1)[0]})
    rules = {'attribute_increments': integers(0x6E4308, 136),
        'level_thresholds': integers(0x625300, 50), 'skill_grid': grid,
        'job_skill_caps': [list(image[0x6E4159+j*13-0x400000:0x6E4159+j*13-0x400000+11])
                           for j in range(31)], 'skills': skills}
    native = json.loads(raw)
    context = {'task_state': 12, 'current': 1, 'total': 1, 'participant_ids': [3, 4, 9],
        'group0_activity_type': 2, 'group0_record_data': [5, 7],
        'group_slots': [[0, 1, 2, -1]]+[[-1]*4 for _ in range(4)],
        'round_ids': [3, 4, 9], 'round_grade': 0, 'support_count': 0,
        'teacher_ids': [-1]*5, 'task_teacher_slots': [0]*5,
        'task_allocation_initial_contents': 'explicit_zero_memory', 'clock_seed': 4660}
    cases = []
    for case in native['task_cases']:
        cases.append({'name': case['name'], 'context': {**context,
            'mode': case['synthetic_inputs']['mode'], 'result_flag': case['synthetic_inputs']['result_flag']},
            'confirmed': case['synthetic_inputs']['confirm'], 'mvp_ready': case['synthetic_inputs']['mvp_ready'],
            'before': snapshot(case['before']), 'expected_after': snapshot(case['after']),
            'expected_branch': case['branch'], 'expected_requested_state': case['requested_state'],
            'expected_learning_draws': [d['rand'] for d in case['learning_draws']],
            'expected_rand_state': case['native_rand_state'],
            'expected_skill_display_needed': case['skill_display_needed'],
            'expected_boundary': case['stop_reason'], 'authorizes_persistent_write': False})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'source_report_sha256': REPORT_SHA256, 'rules': rules, 'cases': cases,
        'source_tables': {'attribute_increments': '0x6e4308', 'level_thresholds': '0x625300',
            'job_skill_caps': '0x6e4159, stride13', 'skill_grid': '0x6c2dcc, stride72',
            'skill_requirements': '0x74f686, stride50', 'learned_points': '0x6c2e08, stride72'},
        'skill_probes': [{'name': c['name'], 'character_id': 3,
            'clock_seed': c['synthetic_probe']['clock_seed'], 'before': snapshot(c['before']),
            'expected_after': snapshot(c['after']),
            'expected_learning_draws': [d['rand'] for d in c['learning_draws']],
            'expected_rand_state': c['native_rand_state'],
            'expected_skill_display_needed': c['skill_display_needed'],
            'state12_executed': False} for c in native['skill_probes']],
        'post_field_probes': [{'name': c['name'], 'context': context,
            'before': snapshot(c['before']), 'expected_after': snapshot(c['after']),
            'state12_executed': False} for c in native['post_field_probes']],
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
