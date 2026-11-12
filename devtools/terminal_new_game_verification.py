"""Independent v6 capture audit, followed by every unchanged v5 handoff check.

No collector imports, native calls, input or inference of unsampled NEW_GAME.
"""
import argparse
import json
from pathlib import Path
from devtools import terminal_host_menu_verification as old

need, number = old.need, old.number
PATHS = ('devtools/terminal_host_menu_preflight_v6.py', 'devtools/terminal_new_game_capture.py',
         'devtools/terminal_menu_state_gate.py', 'devtools/terminal_host_menu_input.py',
         'devtools/terminal_owned_mouse.py', 'devtools/terminal_host_desktop.py')
LIMITS = dict(polls=2048, samples=512, reads=200000, read_bytes=16*1024*1024,
              pause_seconds=.25, total_pause_seconds=5., observer_seconds=40.,
              post_input_seconds=20., interval_seconds=.01)
verify_host_envelope = old.bind(old.verify_host_envelope, HOST_PATHS=PATHS)


def verify_capture(p):
    capture = p['targeted_capture']
    need(capture['contract'] == 'main_first_new_game_v1' and capture['limits'] == LIMITS,
         'exact reviewed targeted capture contract and bounds')
    need(capture['handles_closed'] is True and capture['full_process_atomic'] is False
         and capture['accepted'] is False, 'closed sampled observer with no full-state claim')
    polls, samples = capture['polls'], p['samples']
    need(1 <= len(polls) <= LIMITS['polls'] and 1 <= len(samples) <= LIMITS['samples'], 'capture counts')
    main_tid = p['startup']['window']['main_tid']
    previous_end, previous_reads, previous_bytes, total = -1., 0, 0, 0.
    saved, introduced = [], {}
    for i, poll in enumerate(polls):
        begin, end = number(poll['begin'],'poll begin'), number(poll['end'],'poll end')
        elapsed = number(poll['sample_elapsed'],'sample time')
        pause = number(poll['pause_seconds'],'paused span')
        need(poll['index'] == i and previous_end <= begin <= elapsed <= end
             and 0 <= pause <= LIMITS['pause_seconds'] and pause <= end-begin+.001,
             'ordered bounded raw capture interval')
        need(poll['error'] is None and poll['cleanup_errors'] == [], 'successful capture and resume')
        suspended, resumed = poll['suspended'], poll['resumed']
        tids = [s['tid'] for s in suspended]
        need(1 <= len(tids) <= 4 and tids[0] == main_tid and len(set(tids)) == len(tids),
             'MAIN suspended first, only unique current workers')
        need(all(s['previous'] == 0 for s in suspended)
             and resumed == [dict(tid=t,previous=1) for t in reversed(tids)],
             'every owned increment removed, MAIN resumed last')
        keys = poll['generations']
        need(len(keys) <= 3 and all(len(k)==5 and k[1] in (old.menu.MENU,old.menu.NEW_GAME,old.menu.ADV)
                                  for k in keys), 'bounded phase generations')
        need(set(tids[1:]) <= {k[2] for k in keys}, 'only registered workers suspended')
        for tid in tids[1:]:
            gen = next(k for k in keys if k[2]==tid)
            matches = [w for w in p['workers'] if w['generation']==gen]
            need(len(matches)==1 and ('exit' not in matches[0] or
                                      matches[0]['exit']['elapsed'] >= end),
                 'no suspended context after retained worker termination')
        inactive = poll['inactive_workers']
        inactive_tids = []
        for entry in inactive:
            gen = entry['generation']
            matches = [w for w in p['workers'] if w['generation']==gen]
            need(gen in keys and gen[2] and gen[3] and entry['code']==0 and len(matches)==1
                 and begin <= number(entry['elapsed'],'inactive worker query') <= elapsed
                 and 'exit' in matches[0] and matches[0]['exit']['code']==0
                 and matches[0]['exit']['elapsed'] <= end,
                 'unsuspended current worker has retained exit0 query in this poll')
            inactive_tids.append(gen[2])
        need(len(set(inactive_tids))==len(inactive_tids)
             and not set(inactive_tids).intersection(tids)
             and set(tids[1:]+inactive_tids)=={k[2] for k in keys if k[2] and k[3]},
             'every registered worker is suspended or explicitly queried exited')
        need(type(poll['reads']) is int and type(poll['read_bytes']) is int
             and previous_reads <= poll['reads'] <= LIMITS['reads']
             and previous_bytes <= poll['read_bytes'] <= LIMITS['read_bytes'], 'cumulative read budget')
        if 'saved_index' in poll:
            idx = poll['saved_index']
            need(type(idx) is int and idx == len(saved) and idx < len(samples), 'saved poll indices')
            row = samples[idx]
            actual = []
            for task in row['tasks']:
                h = old.blob(task['header_hex'],64,'captured task header')
                actual.append([task['pointer'],old.word(h),old.word(h,0x24),old.word(h,0x20),old.word(h,0x1C)])
            need(row['elapsed'] == elapsed and row['index'] == idx and actual == keys
                 and [f['tid'] for f in row['frames']] == tids, 'raw saved snapshot binds exactly to held generation')
            saved.append(idx)
        for short in poll['new_workers']:
            need('saved_index' in poll and len(short)==2 and tuple(short) not in introduced,
                 'new worker always has an original raw sample')
            matches = [k for k in keys if [k[0],k[2]] == short]
            need(len(matches)==1, 'unique first retained generation')
            introduced[tuple(short)] = (matches[0], elapsed)
        shorts = [(k[0],k[2]) for k in keys if k[2] and k[3]]
        need(len(set(shorts)) == len(shorts), 'unique live generation per poll')
        for key in keys:
            if key[2] and key[3]:
                short = (key[0],key[2])
                need(short in introduced and introduced[short][0] == key,
                     'every poll preserves the retained worker generation')
        total += pause
        previous_end, previous_reads, previous_bytes = end, poll['reads'], poll['read_bytes']
    need(saved == list(range(len(samples))) and total <= LIMITS['total_pause_seconds']
         and abs(total-number(capture['pause_seconds'],'total pause')) < 1e-9
         and capture['reads']==previous_reads and capture['read_bytes']==previous_bytes
         and polls[-1]['end']-polls[0]['begin'] <= LIMITS['observer_seconds'], 'complete capture bookkeeping')
    need(len(introduced)==len(p['workers']), 'every retained worker bound to first sample')
    for worker in p['workers']:
        key = (worker['pointer'],worker['thread_id'])
        need(key in introduced, 'known worker generation')
        gen, first = introduced[key]
        need(worker['generation']==gen and worker['first_elapsed']==first
             and gen==[worker['pointer'],worker['vtable'],worker['thread_id'],
                       worker['original_handle'],worker['event']['remote_handle']], 'unspliced worker lifetime')
    after = p['mouse_controller']['receipt']['after_elapsed']
    need(polls[-1]['end']-after <= LIMITS['post_input_seconds'], 'no extended post-input collection')
    return dict(polls=len(polls), retained_samples=len(samples), pause_seconds=total,
                whole_process_atomic=False, accepted=False)


def verify_report(report, raw, check_disk=True):
    capture = verify_capture(report['probe'])
    result = old.bind(old.verify_report, verify_host_envelope=verify_host_envelope)(report,raw,check_disk)
    result['targeted_capture'] = capture
    return result


def verify_file(path, digest, desktop_digest, recovery_path=None, recovery_digest=None):
    result = old.bind(old.verify_file, verify_host_envelope=verify_host_envelope,
                      verify_report=verify_report)(path,digest,desktop_digest,recovery_path,recovery_digest)
    result['targeted_verifier'] = old.identity('devtools/terminal_new_game_verification.py')
    result['targeted_verifier_parent'] = old.identity('devtools/terminal_host_menu_verification.py')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--desktop-sha256', required=True)
    parser.add_argument('--recovery')
    parser.add_argument('--recovery-sha256')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = verify_file(args.report,args.sha256,args.desktop_sha256,args.recovery,args.recovery_sha256)
    need(args.out.resolve().is_relative_to(old.ROOT/'analysis'), 'project local new report')
    with args.out.open('x',encoding='utf8') as stream:
        json.dump(result,stream,indent=2)
    print(json.dumps(dict(host_menu_observation_verified=True,accepted=False)))
