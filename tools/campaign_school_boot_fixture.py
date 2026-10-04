"""Export canonical school boot expectations from the continuing native CPU."""
import argparse
import hashlib
import json

from tools.school_boot_fixture import source_rules
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

NATIVE_SHA256 = 'dd3984123588743ac43354692cadc4f95b6a9034e6f20d3747db02eb34f2dd67'
CHAIN_FIXTURE_SHA256 = '76f2cd6ef371840db07a383f067ae8002c28602389f3bc81eec4dbb85a4c2a1e'


def fixture(native):
    if native['source_image_sha256'] != SOURCE_SHA256 or len(native['cases']) != 2:
        raise ValueError('unexpected campaign boot source/cases')
    path = ROOT / 'prototype/data/campaign_return_chain_evidence.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != CHAIN_FIXTURE_SHA256:
        raise ValueError('campaign validation rules/context changed')
    previous = json.loads(path.read_text(encoding='utf-8'))
    rules = previous['rules']
    rules['school_boot'] = source_rules()
    cases = []
    for case in native['cases']:
        upstream = case['upstream']
        constructed = upstream['continuation']['school_constructed']
        cases.append({'name': case['name'], 'context': previous['cases'][0]['context'],
            'school_fade_ready': upstream['declared_inputs']['school_fade_ready'],
            'before_result': upstream['before_result'], 'after_result': upstream['after_result'],
            'after_chapter': upstream['after_chapter'], 'before_boot': case['before'],
            'expected_school_before_boot': case['school_before'],
            'expected_after': case['after'], 'expected_school_after': case['school_after'],
            'expected_school_constructed': constructed,
            'expected_boot_projected': case['group_initialized'] and case['person_resource_initialized'],
            'expected_tasks': [{k: task[k] for k in ('size', 'vtable', 'active',
                'source_wrapper_va', 'source_constructor_va')}
                for task in upstream['continuation']['school_tasks']] if constructed else [],
            'boot_checkpoints': case['boot_checkpoints'], 'boot_events': case['boot_events']})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'native_report_sha256': NATIVE_SHA256, 'rules': rules, 'cases': cases,
        'projection': 'captured_school_boot_fields', 'limitations': native['limitations'],
        'school_initialized': False, 'interactive_school_ready': False,
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT / 'analysis/campaign-school-boot-v1-20261004.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != NATIVE_SHA256:
        raise ValueError('native campaign boot report changed')
    payload = report_text(fixture(json.loads(path.read_text(encoding='utf-8'))))
    output = ROOT / args.out
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{output}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
