"""Offline, source-bound ADV-to-battle preparation; no native execution entry.

Revalidate the retained guest route, then replay only its input predicates.
Old handles/receipts are evidence, never permission or inputs for a new lifetime.
The host wait observer is not qualified, so this report cannot authorize launch.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'analysis/terminal-school-handoff-guest-v5-20261109.json.gz'
SOURCE_SHA = '64976ca051fa42ae2e1e97561cc998ec85bacd11526810c8ec9f01fc7ac08ce6'
WAIT_AUDIT = 'analysis/terminal-wait-host-boundary-audit-v1-20261113.json'
WAIT_SHA = '3021021e64c630df5a1e76d644af5fa2b8eb5149da13f60553a13e0fb1463f19'
MODULES = '.venv-audit/native-worker/guest-system-modules-guest-v5-20261109.json'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def identity(path):
    path = Path(path)
    data = path.read_bytes()
    return dict(path=path.resolve().relative_to(ROOT).as_posix(), bytes=len(data),
                sha256=hashlib.sha256(data).hexdigest())


def extract_route(report):
    """Called after full independent source verification; never sends input."""
    from devtools import terminal_story_input as story
    from devtools import terminal_workroom_input as workroom
    from devtools import terminal_school_input as school
    from devtools import terminal_battle_input as battle
    from devtools import terminal_battle_notice as notice
    from devtools.terminal_scene_resources import clone

    p = report['probe']
    phases = p['story_phases']
    need([x['name'] for x in phases] ==
         ['opening_ADV', 'after_workroom_ADV', 'battle_dialogue'], 'three original story phases')
    need([len(x['actions']) for x in phases] == [178, 141, 25], 'fixed source confirmation counts')
    need([len(p[x]) for x in ('workroom_inputs', 'school_inputs', 'notice_inputs', 'battle_inputs')]
         == [1, 2, 1, 2], 'complete original mouse route')
    entries = []
    for phase, expected_owner in zip(phases, (story.ADV, story.ADV, battle.BATTLE)):
        key_function = clone(story.confirmation_key, ADV=expected_owner)
        for action in phase['actions']:
            row = action['before_sample']
            need(key_function(row) == tuple(action['key']), 'actual current original dialogue key')
            need(row['program_code']['matched'] is True, 'fixed original script catalog match')
            need(action['error'] is None and action['transition']['transition_observed'] is True
                 and action['backend']['receipt']['released'] is True, 'completed original confirmation')
        entries.append(dict(stage=phase['name'], input_count=len(phase['actions']),
                            maximum=phase['maximum'],
                            start=phase['actions'][0]['before_elapsed'],
                            end=phase['actions'][-1]['after_elapsed']))
    controls = [(p['workroom_inputs'][0], 'workroom_exit', workroom.ready),
                (p['school_inputs'][0], 'departure', lambda r: school.ready(r, 'departure')),
                (p['school_inputs'][1], 'confirmation', lambda r: school.ready(r, 'confirmation')),
                (p['notice_inputs'][0], 'opening_notice', lambda r: notice.ready(r, 'opening_notice')),
                (p['battle_inputs'][0], 'request', lambda r: battle.ready(r, 'request')),
                (p['battle_inputs'][1], 'confirmation', lambda r: battle.ready(r, 'confirmation'))]
    names = ('workroom_exit', 'school_departure', 'school_confirmation',
             'opening_notice', 'retreat_request', 'retreat_confirmation')
    for (action, stage, predicate), name in zip(controls, names):
        need(action['stage'] == stage, 'original mouse stage')
        need(all(predicate(action[key]) for key in ('ready_start_sample', 'ready_decision_sample')),
             'original input predicate at both stable observations: ' + name)
        need(action['error'] is None and action['action']['error'] is None
             and action['action']['released'] is True, 'completed original mouse input')
        entries.append(dict(stage=name, input_count=1, maximum=1,
                            start=action['before_elapsed'], end=action['after_elapsed']))
    entries.sort(key=lambda e: e['start'])
    need([e['stage'] for e in entries] == ['opening_ADV', 'workroom_exit', 'after_workroom_ADV',
         'school_departure', 'school_confirmation', 'battle_dialogue', 'opening_notice',
         'retreat_request', 'retreat_confirmation'], 'legal chronological route without skipped controls')
    need(all(a['end'] < b['start'] for a, b in zip(entries, entries[1:])), 'non-overlapping input stages')

    # The short preparation owner is a real intervening node, not a school/battle alias.
    expected = (0x59B060, 0x5C306C, 0x5A0904, 0x5C306C, 0x5A0A40,
                0x5A0C18, 0x5A0C38, 0x59A430, 0x59B060)
    workers = p['workers']
    need(tuple(w['vtable'] for w in workers) == expected, 'complete observed owner sequence including preparation')
    owners = []
    for worker in workers:
        rows = [(r, t) for r in p['samples'] for t in r['tasks']
                if (t['pointer'], t['thread_id']) == (worker['pointer'], worker['thread_id'])
                and 'TLS' in t]
        need(rows, 'at least one live TLS observation for each retained owner')
        owners.append(dict(vtable=hex(worker['vtable']), pointer=worker['pointer'],
                           thread_id=worker['thread_id'], first=worker['first_elapsed'],
                           first_TLS_sample=rows[0][0]['index'], exit=worker.get('exit')))
    prep, battle_worker = workers[6:8]
    prep_rows = [r for r in p['samples'] if any(t['pointer'] == prep['pointer'] and
                 t['thread_id'] == prep['thread_id'] and 'TLS' in t for t in r['tasks'])]
    need(any(any(f['tid'] == prep['thread_id'] and
         {0x42240D, 0x4B90FE, 0x421F8A, 0x56E183} <= {c['return_va'] for c in f['chain']}
         for f in r['frames']) for r in prep_rows), 'original preparation worker wait ancestry')
    need(entries[4]['end'] < prep['first_elapsed'] < battle_worker['first_elapsed']
         <= entries[5]['start'], 'school confirmation precedes preparation and battle dialogue')
    need(prep['exit']['code'] == 0 and prep['exit']['before_WM_CLOSE'] is True,
         'retained preparation worker exit before cleanup')
    need(not battle.ready(p['notice_inputs'][0]['ready_decision_sample'], 'request'),
         'opening notice cannot be treated as an ordinary retreat gate')
    return dict(stages=entries, observed_owners=owners,
                input_predicates_replayed=344 + 2 * 6,
                post_ADV_input_actions=350, total_mouse_actions_including_title=7,
                battle_first_observed_seconds=battle_worker['first_elapsed'],
                retreat_confirmation_finished_seconds=entries[-1]['end'],
                ten_minute_window_covers_retained_route=False,
                timing_scope='one guest lifetime; no host speed prediction or desktop authorization')


def prepare():
    from devtools.terminal_school_handoff_verification import verify_file
    before = {p: identity(ROOT / p) for p in (SOURCE, WAIT_AUDIT, MODULES)}
    need(before[SOURCE]['sha256'] == SOURCE_SHA, 'fixed guest source identity')
    need(before[WAIT_AUDIT]['sha256'] == WAIT_SHA, 'fixed rejected wait migration audit')
    verification = verify_file(ROOT / SOURCE, SOURCE_SHA, ROOT / MODULES)
    report = json.loads(gzip.decompress((ROOT / SOURCE).read_bytes()))
    route = extract_route(report)
    need(before == {p: identity(ROOT / p) for p in before}, 'all preparation sources unchanged')
    return dict(schema_version=1, kind='offline_ADV_battle_route_preparation', accepted=False,
        sources=list(before.values()), implementation=identity(Path(__file__)),
        predicate_implementations=[identity(ROOT / ('devtools/' + name + '.py')) for name in (
            'terminal_story_input', 'terminal_workroom_input', 'terminal_school_input',
            'terminal_battle_input', 'terminal_battle_notice', 'terminal_scene_resources')],
        independent_source_revalidation={k: verification[k] for k in ('status', 'samples',
            'TLS_observations', 'school_UI_to_battle_owner_observed', 'wait_return_proved',
            'result_consumption_proved', 'full_battle_exit_accepted')},
        verification_dependencies=verification['current_verification_dependencies'],
        route=route, wait_observer_qualified=False, game_acquisition_allowed=False,
        host_continuation_qualified=False, fresh_desktop_window_authorized=False,
        desktop_touched=False, screenshots_taken=False, native_processes_started=0,
        limitations=[
            'Guest route and separate host NEW_GAME evidence are not one continuous lifetime.',
            'Retained predicates/owners do not authorize reuse of native handles or input receipts.',
            'Existing school input driver requires a qualified guest; do not remove that guard.',
            'Host input must stop on foreground loss and use a fresh bounded desktop window.',
            'A future host run must include asset checks, input release, Job cleanup and desktop recovery in its deadline.',
            'The retained route exceeds 600 seconds before battle; do not skip story waits to fit an old menu budget.',
            'No precise post-wait full-state observer is qualified; no new game capture until that precheck passes.',
            'No result consumption, resource/PTD cleanup, three handshakes or formal task completion added.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    need(out.parent == ROOT / 'analysis' and not out.exists(), 'fresh small analysis report only')
    result = prepare()
    with out.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps(dict(report=identity(out), offline_route_checked=True, game_acquisition_allowed=False)))


if __name__ == '__main__':
    main()
