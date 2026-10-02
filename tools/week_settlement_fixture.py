"""Export source week rules and independently executed native expectations."""
import argparse
import hashlib
import json
import struct

from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, report_text

REPORT = ROOT / 'analysis/week-settlement-v1-20261002.json'
REPORT_SHA256 = 'f4d954f44de9b0c95a4747e8a92bbb0c55a42f047c4123ca20ec28a9019a2364'


def fixture():
    image, raw = SOURCE.read_bytes(), REPORT.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256 or hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError('source image or week report differs from audited bytes')
    rules = []
    for category in range(1, 31):
        at = 0x738CD3+category*0x32-0x400000
        rules.append({'month': image[at], 'week': image[at+1],
            'minimum_attributes': list(struct.unpack_from('<7h', image, at+3)),
            'minimum_total': struct.unpack_from('<h', image, at+17)[0],
            'job_requirements': [{'type': image[at+19+j*2], 'count': image[at+20+j*2]}
                                 for j in range(3)]})
    cases = [{'name': c['name'], 'evidence_kind': c['evidence_kind'],
              'before': c['before_week'], 'expected_after': c['after_week'],
              'context': {'task_state': 12, 'mode': 0, 'current': 1, 'total': 1,
                          'result_fields_completed': True} if 'all_result' in c else {},
              'authorizes_persistent_write': False} for c in json.loads(raw)['cases']]
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'source_report_sha256': REPORT_SHA256,
        'evidence_kind': 'native_week_settlement_projection_fixture',
        'source_rules': {'unlock_base_va': '0x738cd3', 'stride': '0x32',
            'week_body_va': '0x4d3510', 'unlock_va': '0x4d3aa0',
            'item_cleanup_va': '0x4d31f0', 'skill_cleanup_va': '0x4d34a0'},
        'rules': {'unlock_rules': rules}, 'cases': cases,
        'authorizes_persistent_write': False}


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
