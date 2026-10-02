"""Export both native state9 constructors for the isolated Godot dispatcher."""
import hashlib
import json
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256

NATIVE_SHA256 = '2a12cb13114c9b372da7ce565bdddb811c1c97ebcc943b9dee0ce626fa2774dd'
RULES_SHA256 = '57d44c34919f20a82276bfdc442dff174eb59ff15fcbc544dc9d09155cf68472'


def fixture(native_report):
    path = ROOT / 'prototype/data/adv_week_handoff_evidence.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != RULES_SHA256:
        raise ValueError('school validation rules changed')
    cases = []
    for c in native_report['cases']:
        request = c['consumed_request']
        descriptors = [{k: task[k] for k in ('size','vtable','active','source_wrapper_va','source_constructor_va')}
                       for task in c['school_tasks']] if c['school_constructed'] else []
        cases.append({'name': c['name'], 'context': {
            'task_state': c['upstream']['pending_state'], 'pending_flag': c['upstream']['pending_flag'],
            'adv_active': request['adv_active'] if request else None,
            'source_request_va': '0x439e30' if request else None},
            'before': c['before'], 'expected_after': c['after'],
            'expected_supported': c['school_constructed'], 'expected_tasks': descriptors,
            'expected_pending_flag': c['pending_flag'], 'expected_pending_state': c['pending_state']})
    return {'schema_version':1, 'source_image_sha256':SOURCE_SHA256,
        'native_report_sha256':NATIVE_SHA256, 'validation_rules_sha256':RULES_SHA256,
        'rules':json.loads(path.read_text(encoding='utf-8'))['rules']['week'], 'cases':cases,
        'limitations':['This projects state9 task descriptors and request consumption, not task initialization.',
            'Task pointers are source-emulator addresses and are deliberately absent from Godot descriptors.',
            'All completion/request inputs remain declared replay inputs, without live or persistent authority.'],
        'school_initialized':False, 'live_witness':False, 'authorizes_persistent_write':False}
