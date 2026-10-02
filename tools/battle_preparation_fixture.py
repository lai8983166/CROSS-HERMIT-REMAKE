"""Export bounded Godot score inputs/rules from original bytes and native report."""
import argparse
import hashlib
import json
import struct

from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, report_text

REPORT = ROOT / 'analysis/battle-preparation-v1-20261002.json'
REPORT_SHA256 = '4ecaf2ea1295c258f20347ea806ac7633c4f52bc61f7f46239356a9e6a09df2b'


def fixture():
    image = SOURCE.read_bytes()
    raw = REPORT.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256 or hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError('source image or native report differs from audited bytes')
    native = json.loads(raw)
    def values(va, count, fmt='h'):
        return list(struct.unpack_from('<'+fmt*count, image, va-0x400000))
    rules = {'task_id': 5, 'base_points': values(0x73BEF4+5*0x100, 5, 'i'),
        'unit_bonus': values(0x73BF08+5*0x100, 1)[0],
        'time_bonuses': values(0x73BF0A+5*0x100, 3),
        'count_bonuses': values(0x73BF10+5*0x100, 6),
        'contribution_thresholds': values(0x61C50A, 10),
        'rates': [values(0x61C508+i*22, 11) for i in range(6)],
        'distributions': [values(0x61C58C+i*14, 7) for i in range(6)],
        'attribute_thresholds': values(0x6E4308, 136, 'i'),
        'growth_limit': values(0x6253C4, 1, 'i')[0]}
    cases = []
    for case in native['cases']:
        characters = []
        for before, unit in zip(case['before']['characters'], case['native_result_inputs']['units']):
            character = before['character_id']
            record = 0x6F5088+character*0x4A0
            job = values(record+6, 1)[0]
            skill_points = sum(values(0x6C2E08+(i+1)*0x48, 1, 'i')[0] for i in range(84)
                if image[record-0x400000+0xB0+8+i*12] in (3, 5, 6))
            characters.append({'character_id': character, 'rate_class': image[0x6B2D8A+job*0x40-0x400000],
                'growth_pools': before['growth_pools'], 'skill_points': skill_points,
                'group_bonus': case['synthetic_inputs']['group_bonus'],
                'count_field_aa': unit['count_field_aa'],
                'contribution_field_ac': unit['contribution_field_ac'],
                'status_field_ae': unit['status_field_ae']})
        cases.append({'name': case['name'], 'inputs': {'task_id': 5, 'mode': 0, 'cap_mode': 0,
            'result_selector': case['native_result_inputs']['result_selector'],
            'time_key': case['native_result_inputs']['time_key'],
            'unit_key': case['native_result_inputs']['unit_condition_key'],
            'initial_grade': case['before']['task_grade'],
            'initial_total': case['before']['global_total_511c'], 'characters': characters},
            'expected': {'task_grade': case['after']['task_grade'],
                'grade_index': case['result_summary']['grade_index'],
                'time_display': case['result_summary']['time_display'],
                'unit_display': case['result_summary']['unit_display'],
                'total_delta': case['result_summary']['total_delta'],
                'total_after': case['after']['global_total_511c'],
                'characters': [{'character_id': c['character_id'], 'staged_package': c['staged_package'],
                                'staged_total': c['staged_total']} for c in case['after']['characters']]},
            'authorizes_persistent_write': False})
    return {'schema_version': 1, 'evidence_kind': 'native_task5_score_projection_fixture',
        'source_image_sha256': SOURCE_SHA256, 'source_report_sha256': REPORT_SHA256,
        'source_rules': {'base_points_va': '0x73c3f4', 'bonus_va': '0x73c408',
            'rates_va': '0x61c508', 'distributions_va': '0x61c58c',
            'attribute_thresholds_va': '0x6e4308', 'growth_limit_va': '0x6253c4'},
        'rules': rules, 'cases': cases, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT / args.out
    if path.exists():
        parser.error('output exists; use a new path')
    payload = report_text(fixture())
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
