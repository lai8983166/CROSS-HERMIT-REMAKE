"""Export independently captured canonical/school snapshots and source rules."""
import argparse
import hashlib
import json

from tools.result_transaction_fixture import fixture as result_fixture
from tools.roster_join_fixture import fixture as join_fixture
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

NATIVE_SHA256 = 'cb4c7be643e05f29e657b4f552a65de543f614755a6710b5c510c698ed7a09e0'


def fixture(native):
    if native['source_image_sha256'] != SOURCE_SHA256:
        raise ValueError('layout source differs')
    historical, join = result_fixture(), join_fixture()
    cases = []
    for c, previous in zip(native['cases'], [historical['cases'][0], historical['cases'][1], historical['cases'][5]]):
        cases.append({**c, 'context': previous['context'],
            'confirmed': c['context_inputs']['confirm'], 'mvp_ready': c['context_inputs']['mvp_ready'],
            'join_context': join['cases'][0]['context'] if c['after_join_probe'] else None})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'native_report_sha256': NATIVE_SHA256, 'rules': historical['rules'],
        'join_rules': join['rules'], 'cases': cases, 'limitations': native['limitations'],
        'chapter_completed': False, 'school_initialized': False, 'live_witness': False,
        'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    native_path = ROOT / 'analysis/campaign-school-layout-v1-20261004.json'
    if hashlib.sha256(native_path.read_bytes()).hexdigest() != NATIVE_SHA256:
        raise ValueError('layout report changed')
    payload = report_text(fixture(json.loads(native_path.read_text(encoding='utf-8'))))
    path = ROOT / args.out
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
