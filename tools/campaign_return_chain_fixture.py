"""Export full-catalog checkpoints only from one native continuation report."""
import argparse
import hashlib
import json

from tools.campaign_school_layout_fixture import fixture as layout_fixture
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

NATIVE_SHA256 = '639b76faacecb652f4db5a0663592e0ecbd9e9e8063b2a1b7d5cf8153f045b9a'
LAYOUT_SHA256 = 'cb4c7be643e05f29e657b4f552a65de543f614755a6710b5c510c698ed7a09e0'


def fixture(native):
    if native['source_image_sha256'] != SOURCE_SHA256 or len(native['cases']) != 5:
        raise ValueError('unexpected native continuation source/cases')
    path = ROOT / 'analysis/campaign-school-layout-v1-20261004.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != LAYOUT_SHA256:
        raise ValueError('layout rule input changed')
    rules = layout_fixture(json.loads(path.read_text(encoding='utf-8')))
    cases = []
    for c in native['cases']:
        checkpoints = {b['phase']: b['canonical_layout'] for b in c['boundaries']}
        cases.append({'name': c['name'], 'context': rules['cases'][0]['context'],
            'confirmed': c['declared_inputs']['result']['confirm'],
            'chapter_key_ready': c['declared_inputs']['chapter']['key_ready'],
            'continue_ready': c['declared_inputs']['continue_ready'],
            'school_fade_ready': c['declared_inputs']['school_fade_ready'],
            'before_result': c['before_result'], 'after_result': c['after_result'],
            'after_chapter': c['after_chapter'], 'checkpoints': checkpoints,
            'expected_after': c['after'], 'expected_school_after': c['school_after'],
            'expected_controller': c['controller'], 'native_result_controller': c['result_controller'],
            'expected_school_constructed': c['continuation'].get('school_constructed', False),
            'expected_tasks': [{k: task[k] for k in ('size', 'vtable', 'active',
                'source_wrapper_va', 'source_constructor_va')} for task in c['continuation'].get('school_tasks', [])]
                if c['continuation'].get('school_constructed') else [],
            'native_state_requests': c['state_requests'],
            'native_result_return_load': c['native_result_return_load'],
            'source_loads': c['resource_loads']})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'native_report_sha256': NATIVE_SHA256, 'rules': rules['rules'], 'cases': cases,
        'limitations': native['limitations'], 'school_initialized': False,
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    native = ROOT / 'analysis/campaign-return-chain-v1-20261004.json'
    if hashlib.sha256(native.read_bytes()).hexdigest() != NATIVE_SHA256:
        raise ValueError('native continuation report changed')
    payload = report_text(fixture(json.loads(native.read_text(encoding='utf-8'))))
    path = ROOT / args.out
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
