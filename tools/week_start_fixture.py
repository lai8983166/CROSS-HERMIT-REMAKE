"""Export state7 native expectations and source week rules, preserving old reports."""
import argparse
import hashlib
import json

from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text
from tools.week_settlement_fixture import fixture as week_fixture

REPORT = ROOT / 'analysis/week-start-v1-20261002.json'
REPORT_SHA256 = 'b376fecfa217b578ba37bc42befa3679bb9bd1d60a284cc926ef129e00469506'


def fixture():
    raw = REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError('week-start report differs from audited bytes')
    source = json.loads(raw)
    if source['source_image_sha256'] != SOURCE_SHA256:
        raise ValueError('unexpected native image')
    week = week_fixture()
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
            'source_report_sha256': REPORT_SHA256,
            'source_week_rules_report_sha256': week['source_report_sha256'],
            'rules': week['rules'], 'cases': [{'name': c['name'],
                'context': {'task_state': 7, 'adv_completed': True},
                'before': c['before_week'], 'expected_after': c['after_week'],
                'fade_ready': c['synthetic_fade_ready'], 'expected_requested_state': c['requested_state'],
                'expected_script_requests': [{'path': e['path'], 'next_task_state': e['next_task_state']}
                    for e in c['start_events'] if e['kind'] == 'script_load_boundary']}
                for c in source['cases']], 'limitations': source['limitations'],
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
