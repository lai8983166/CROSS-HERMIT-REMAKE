"""Export owned preparation inputs from the continuous scene5 CPU evidence."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct

from tools.battle_preparation_fixture import fixture as score_fixture
from tools.campaign_scene5_fixture import NATIVE_SHA256
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, report_text


def fixture():
    image = SOURCE.read_bytes()
    raw = (ROOT / 'analysis/campaign-scene5-v1-20261004.json').read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256 or hashlib.sha256(raw).hexdigest() != NATIVE_SHA256:
        raise ValueError('source image or continuous native report changed')
    native = json.loads(raw)

    def shorts(va, count):
        return list(struct.unpack_from('<' + 'h' * count, image, va - 0x400000))

    rules = {'score': score_fixture()['rules'],
        'job_rate_classes': [image[0x6B2D8A + job * 0x40 - 0x400000] for job in range(31)],
        'item_types': [shorts(0x6D5120 + item * 0x38, 1)[0] for item in range(1, 361)],
        'loot_quotas': [shorts(0x73BF1A + 5 * 0x100 + grade * 14, 7) for grade in range(5)],
        'fixed_items': shorts(0x73BF60 + 5 * 0x100, 8),
        'objective_rewards': [shorts(0x73BF70 + 5 * 0x100 + slot * 6, 3) for slot in range(16)]}
    cases = []
    for case in native['cases']:
        declared = case['preparation']['synthetic_inputs']
        summary = case['preparation']['result_summary']
        cases.append({'name': case['name'], 'before_world': case['before_world'],
            'inputs': {'task_id': declared['task_id'], 'mode': declared['mode'], 'cap_mode': 0,
                'initial_grade': declared['initial_grade'], 'group_bonus': declared['group_bonus'],
                'clock_seed': declared['clock_seed'],
                'objective_slots': declared['unit_inputs']['objective_slots'],
                'result_inputs': case['state11_entry_inputs']},
            'expected_after': case['campaign']['upstream']['before_result'],
            'expected_summary': {key: deepcopy(summary[key]) for key in
                ['grade_index', 'time_display', 'unit_display', 'total_delta', 'total_after', 'loot_groups']},
            'expected_task_grade': case['preparation']['after']['task_grade'],
            'expected_loot_rand_state': case['preparation']['native_rand_state']})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'native_report_sha256': NATIVE_SHA256,
        'source_rules': {'score': '4bbd40/4d58e0/4d5850', 'job_rate_classes_va': '0x6b2d8a, stride64',
            'item_types_va': '0x6d5120, stride56', 'loot_quotas_va': '0x73c41a',
            'fixed_items_va': '0x73c460', 'objective_rewards_va': '0x73c470',
            'loot_function': '0x4bca40', 'skill_reward_task_guard': '4bd210: task_id==37',
            'rng': '4d1c60->571020/570fd0; 4d1cb0->_rand'},
        'rules': rules, 'cases': cases,
        'limitations': ['Initial grade, group bonus, clock seed, cap mode and objective slots are declared inputs.',
            'Tactical result keys and unit records are captured at the native state11 entry.',
            'Task5 does not execute the task37 skill reward branch.',
            'These isolated calculations do not authorize original process or save writes.'],
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    payload = report_text(fixture())
    output = ROOT / args.out
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{output}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
