"""Export school snapshot projection and primitive rules from audited source bytes.

The expected snapshots come from one native CPU chain. Template inputs come from
the executable, never from those expected snapshots. Teacher lecture work tables
and menu interaction are outside this explicitly named projection.
"""
import argparse
import hashlib
import json
import struct

from tools.school_dispatch_fixture import RULES_SHA256
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, report_text

NATIVE_SHA256 = '1537a81c4d92732464a1ce8182628b1e07a9b85ce469598784707da86514359a'


def source_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('school source image changed')
    adventures, lectures = [], []
    for identity in range(1, 101):
        base = 0x73BED0 + identity * 0x100 - 0x400000
        adventures.append({'id': identity, 'present': image[base+1],
            'month': image[base+2], 'week': image[base+3], 'duration': image[base+5],
            'kind': image[base+6], 'subkind': struct.unpack_from('<b', image, base+7)[0],
            'gate': image[base+14]})
        base = 0x74BED0 + identity * 0x60 - 0x400000
        lectures.append({'id': identity, 'month': image[base+2], 'week': image[base+3],
            'kind': struct.unpack_from('<h', image, base+6)[0],
            'subkind': struct.unpack_from('<h', image, base+8)[0]})
    return {'adventures': adventures, 'lectures': lectures}


def fixture(native_report):
    if native_report['source_image_sha256'] != SOURCE_SHA256:
        raise ValueError('native school source differs')
    path = ROOT / 'prototype/data/adv_week_handoff_evidence.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != RULES_SHA256:
        raise ValueError('school validation rules changed')
    cases = []
    for c in native_report['cases']:
        upstream = c['upstream']
        tasks = [{k: task[k] for k in ('size', 'vtable', 'active', 'source_wrapper_va', 'source_constructor_va')}
                 for task in upstream['school_tasks']] if upstream['school_constructed'] else []
        cases.append({'name': c['name'], 'context': {
            'task_state': upstream['pending_state'], 'pending_flag': upstream['pending_flag'],
            'school_constructed': upstream['school_constructed'], 'tasks': tasks},
            'before': c['before'], 'expected_after': c['after'],
            'expected_supported': c['group_initialized'] and c['person_resource_initialized']})
    return {'schema_version': 1, 'projection': 'captured_school_boot_fields',
        'source_image_sha256': SOURCE_SHA256, 'native_report_sha256': NATIVE_SHA256,
        'validation_rules_sha256': RULES_SHA256,
        'source_template_ranges': [{'va': '0x73bfd0', 'count': 100, 'stride': 256},
                                   {'va': '0x74bf30', 'count': 100, 'stride': 96}],
        'role_rules': json.loads(path.read_text(encoding='utf-8'))['rules']['week'],
        'boot_rules': source_rules(), 'cases': cases,
        'limitations': ['Only the captured school_control fields and class student IDs/indices are projected.',
            'The supported input is the audited fresh 5/1 four-student roster with no teachers or existing work lists.',
            'Teacher lecture work tables, uncaptured UI controls, rendering and menu interaction are not projected.',
            'No resource readiness or live/persistent authority is inferred from a successful data projection.'],
        'school_initialized': False, 'interactive_school_ready': False,
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    native_path = ROOT / 'analysis/school-boot-v1-20261003.json'
    if hashlib.sha256(native_path.read_bytes()).hexdigest() != NATIVE_SHA256:
        raise ValueError('native school report changed')
    payload = report_text(fixture(json.loads(native_path.read_text(encoding='utf-8'))))
    path = ROOT / args.out
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
