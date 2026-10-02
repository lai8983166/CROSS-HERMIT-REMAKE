"""Export source join rules and independently executed native expectations."""
import argparse
import hashlib
import json

from tools.roster_join_emulation import CHAPTER
from tools.role_application_fixture import fixture as role_fixture
from tools.week_settlement_fixture import fixture as week_fixture
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

REPORT = ROOT / 'analysis/roster-join-v1-20261002.json'
REPORT_SHA256 = '2bb4b143ab5e282b19d7cf5ac143d0b1016a6ee487c152341174a034eb88b6bc'


def snapshot(raw):
    result = json.loads(json.dumps(raw))
    for record in result['participants']:
        record.pop('character_sha256')
        record.pop('package_sha256')
    return result


def fixture():
    raw = REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError('join report differs from audited bytes')
    native = json.loads(raw)
    chapter_hash = hashlib.sha256(CHAPTER.read_bytes()).hexdigest()
    if chapter_hash != native['source_chapter020_sha256']:
        raise ValueError('chapter source differs from executed bytes')
    roles = role_fixture()['rules']  # Also validates source EXE and role report.
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'source_report_sha256': REPORT_SHA256, 'source_chapter020_sha256': chapter_hash,
        'evidence_kind': 'native_student_join_projection_fixture',
        'rules': {'week': week_fixture()['rules'], 'level_thresholds': roles['level_thresholds'],
                  'learned_points': [skill['learned_points'] for skill in roles['skills']]},
        'cases': [{'name': c['name'], 'context': {'task_state': 6,
            'script_path': 'DATA/ADV/DAT/Chapter020.ybc', 'script_file_offset': 20,
            'opcode': 144, 'character_id': 5, 'group': -1, 'slot': -1,
            'difficulty': c['difficulty']}, 'repeat_opcode': c['repeat_opcode'],
            'before': snapshot(c['before']), 'expected_after': snapshot(c['after']),
            'chapter_completed': False, 'authorizes_persistent_write': False}
            for c in native['cases']],
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
