"""Project native shared-memory workroom cases into isolated Godot inputs."""
import hashlib
import json

from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256

NATIVE_SHA256 = '75bec06bce23826fb89228ab466b603c64cd030232fac05764df519f3d215bae'
RULES_SHA256 = '57d44c34919f20a82276bfdc442dff174eb59ff15fcbc544dc9d09155cf68472'


def fixture(native_report):
    path = ROOT / 'prototype/data/adv_week_handoff_evidence.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != RULES_SHA256:
        raise ValueError('shared validation rules changed')
    # Expected snapshots come only from this native run, never old case outputs.
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'native_report_sha256': NATIVE_SHA256, 'validation_rules_sha256': RULES_SHA256,
        'rules': json.loads(path.read_text(encoding='utf-8'))['rules']['week'],
        'cases': [{'name': c['name'], 'before': c['before_workroom'],
            'context': {'task_state': c['consumed_request']['state'],
                'pending_flag': c['consumed_request']['pending_flag'],
                'vm_active': c['consumed_request']['adv_active'],
                'adv_completed': c['upstream']['ch001_completed'],
                'script_path': 'chapter208.ybc', 'end_file_offset': 0x1B0, 'opcode': 19,
                'next_task_state': c['upstream']['stored_next_task_state']},
            'continue_ready': c['synthetic_continue_ready'],
            'visited_override': c['synthetic_visited_override'],
            'ch002_context': dict(c['ch002_consumed_request'], vm_active=1, vm_pc=0)
                if c['ch002_consumed_request'] is not None else None,
            'ch002_end_ready': c['ch002_completed'],
            'native_ch002_end': c['ch002_commands'][-1] if c['ch002_completed'] else None,
            'expected_after_workroom': c['after_workroom'], 'expected_after': c['after'],
            'expected_work_requests': [v['state'] for v in c['work_state_requests']],
            'expected_ch002_requests': [v['state'] for v in c['ch002_state_requests']],
            'expected_pending_flag': c['pending_flag'], 'expected_pending_state': c['pending_state']}
            for c in native_report['cases']],
        'limitations': ['Task completion/readiness remains a declared replay input.',
            'Only native 5/1 workroom and CH002 control writes are projected; no VM or school task implementation.',
            'Visited override is an explicit alternate branch; no live BattleReturn or save authority.'],
        'school_initialized': False, 'live_witness': False, 'authorizes_persistent_write': False}
