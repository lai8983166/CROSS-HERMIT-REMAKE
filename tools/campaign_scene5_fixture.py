"""Export one-CPU scene condition/task/result/school inputs without old after-images."""
import argparse
from copy import deepcopy
import hashlib
import json

from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

NATIVE_SHA256 = '11b6c1562dc2e9377ce7d03a5f9b6b9ad94ab50db6c07968fdb6abddf3d473a4'
RULES_SHA256 = '96359d3c2fff36a97299312d70828f617c82d762b51d75b59e07e0226b727656'


def fixture(native):
    if native['source_image_sha256'] != SOURCE_SHA256 or len(native['cases']) != 2:
        raise ValueError('unexpected native scene5 campaign')
    path = ROOT / 'prototype/data/campaign_school_boot_evidence.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != RULES_SHA256:
        raise ValueError('source validation rules/context changed')
    source = json.loads(path.read_text(encoding='utf-8'))
    cases = []
    for case in native['cases']:
        campaign = case['campaign']
        upstream = campaign['upstream']
        context = deepcopy(source['cases'][0]['context'])
        context['round_grade'] = case['preparation']['result_summary']['grade_index']
        selected = next(e for e in case['event_trace'] if e.get('va') == '0x454af0')
        exit_frame = case['tactical_frames'][-1]
        cases.append({'name': case['name'], 'event_world': case['event_before'],
            'expected_selector': selected['args'][0], 'expected_sub': selected['args'][1],
            'expected_task_result_selector': case['event_after']['task']['result_selector'],
            'exit_frame': exit_frame,
            'dispatch_context': {'scene_id': 5, 'next_scene': 0, 'network_mode': False,
                'task_phase': 2, 'request_pending': 0, 'exit_to_menu': False},
            'round_before': case['round_before'], 'round_after': case['round_after'], 'round_table': {},
            'context': context, 'before_result': upstream['before_result'],
            'after_result': upstream['after_result'], 'after_chapter': upstream['after_chapter'],
            'before_boot': campaign['before'], 'expected_after': campaign['after'],
            'expected_school_after': campaign['school_after'],
            'state11_entry_inputs': case['state11_entry_inputs'],
            'native_state_requests': campaign['state_requests'],
            # This caller fact is explicitly not a native battle simulation.
            'declared_terminal_snapshot': {'frame': exit_frame['frame'], 'winner': 0,
                'units': [{'battle_index': i, 'character_id': unit['character_id'], 'faction': 0}
                    for i,unit in enumerate(case['state11_entry_inputs']['units'])]}})
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'native_report_sha256': NATIVE_SHA256, 'script_sha256': native['script_sha256'],
        'rules': source['rules'], 'cases': cases, 'limitations': native['limitations']+[
            'Local terminal snapshots are declared caller facts; native tactical dynamics are not simulated.'],
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT / 'analysis/campaign-scene5-v1-20261004.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != NATIVE_SHA256:
        raise ValueError('native scene5 report changed')
    payload = report_text(fixture(json.loads(path.read_text(encoding='utf-8'))))
    output = ROOT / args.out
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{output}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
