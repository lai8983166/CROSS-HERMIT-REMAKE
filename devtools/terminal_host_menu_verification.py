"""Independent verifier for native-state host menu receipts, generation v5.

Reads evidence only. Never imports the collector or input implementation. Old
verifiers stay unchanged; feedback coordinates are normalized in a private view
only AFTER their actual arithmetic and cursor observations have been verified.
"""
import argparse
import copy
import hashlib
import json
import struct
from pathlib import Path
from types import FunctionType
from devtools import terminal_menu_handoff_verification as menu
from devtools import terminal_school_handoff_verification as feedback
from devtools import terminal_host_desktop as desktop

ROOT = menu.ROOT
need, word, blob, number = menu.need, menu.word, menu.blob, menu.number
HOST_PATHS = ('devtools/terminal_host_menu_preflight_v5.py',
    'devtools/terminal_menu_state_gate.py', 'devtools/terminal_host_menu_input.py',
    'devtools/terminal_owned_mouse.py', 'devtools/terminal_host_desktop.py')


def identity(path):
    data = (ROOT/path).read_bytes()
    return dict(path=path, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def bind(fn, **changes):
    return FunctionType(fn.__code__, dict(fn.__globals__, **changes), fn.__name__,
                        fn.__defaults__, fn.__closure__)


def generation(g):
    head = blob(g['head_hex'],64,'host guard head')
    return (g['pid'],g['main'],g['game'],g['hwnd'],g['node'],word(head,0x24),
            word(head,0x1C),word(head,0x20),g['selector_pointer'],g['coordinate_mode_hex'])


def verify_input(p, raw, game, hwnd, worker, check_disk=True):
    controller = p['mouse_controller']
    need(controller['attempted'] is True, 'host preflight requires actual input attempt')
    receipt = controller['receipt']; action = receipt['action']; target = (318,508)
    need(receipt['index'] == 0 and type(receipt['index']) is int, 'host new-game only')
    need(p['collector_input_actions'] == [receipt], 'one unchanged host input receipt')
    need(action['screenshot_required'] is False and action['accepted'] is False
         and action['release_guard_failed'] is False and action['release_guard_error'] is None,
         'host release guard succeeded without acceptance claim')
    need(receipt['activation'] == dict(hwnd=hwnd,before=hwnd,after=hwnd,operations=[]),
         'host input does not reacquire user foreground')
    before=number(receipt['before_elapsed'],'host input start')
    after=number(receipt['after_elapsed'],'host input end')
    need(0 < after-before <= 3, 'complete observed host input within three seconds')
    guards=action['guard_observations']
    need(isinstance(guards,list) and 4 <= len(guards) <= 12, 'bounded host guard observations')
    edges=action['button_edge_checks']
    need(isinstance(edges,list) and len(edges)==2
         and [e['flags'] for e in edges]==[2,4]
         and all(type(e['flags']) is int for e in edges), 'exact DOWN and UP guard checks')
    all_guards=guards+[e['guard'] for e in edges]
    expected=generation(guards[0]); counters=[]
    for g in all_guards:
        menu.verify_guard(g,raw,p['pid'],p['main'],game,hwnd,
                          worker['pointer'],worker['thread_id'],check_disk)
        need(generation(g)==expected, 'same original host selector generation')
        head=bytes.fromhex(g['head_hex'])
        need(word(head,0x20)==worker['original_handle']
             and word(head,0x1C)==worker['event']['remote_handle'], 'retained worker/event binding')
        need(word(bytes.fromhex(g['manager_hex']),0x118)==p['manager_event']['remote_handle'],
             'host guard same manager Event')
        counters.append(word(blob(g['selector_hex'],28,'host selector')))
    need(all(300 <= n < 3660 for n in counters)
         and all(a>=b for a,b in zip(counters,counters[1:])), 'remaining selector iterations never restart')
    first,last=receipt['ready_start_sample'],receipt['ready_decision_sample']
    for row in (first,last):
        menu.verify_ready_owner(row,p,raw,game,worker,menu.MENU,0x45F065)
        frame=next(f for f in row['frames'] if f['tid']==worker['thread_id'])
        wait=next(f for f in frame['chain'] if f['return_va']==0x45F065)
        need(wait['saved_bp']==expected[8], 'readiness and live input same selector stack')
    a,b=number(first['elapsed'],'host first ready'),number(last['elapsed'],'host decision')
    need(1 <= b-a <= 15 and 0 <= before-b <= 1, 'fresh one-second readiness before input')
    mode=word(bytes.fromhex(guards[0]['coordinate_mode_hex']))
    corrections,canonical=feedback.verify_absolute_moves(action,target,hwnd,mode)
    geometry=action['click_geometry']; previous=None
    for group in [m['settling'] for m in action['moves']]+[action['before_click_settling']]:
        need(all(s['geometry']==geometry for s in group), 'same geometry across all movements')
        if previous:
            need(group[0]['monotonic_ns']>=previous['monotonic_ns']
                 and group[0]['wall_time_ns']>=previous['wall_time_ns'], 'ordered movement segments')
        previous=group[-1]
    cursors=[action['pre_down_cursor']]+[e['cursor'] for e in edges]
    for s in cursors:
        feedback.verify_cursor_sample(s,geometry,target,hwnd,mode)
        need(s['os_game_point']==s['game_point']==list(target), 'exact OS/game button-edge target')
    walls=[s['wall_time_ns'] for s in cursors]; ticks=[s['monotonic_ns'] for s in cursors]
    need(walls[0] <= action['down_wall_time_ns'] <= walls[1] <= walls[2] <= action['up_wall_time_ns'],
         'DOWN guard follows recorded submit request and precedes UP')
    need(all(a<=b for a,b in zip(ticks,ticks[1:]))
         and abs((walls[-1]-walls[0])-(ticks[-1]-ticks[0]))<=25_000_000,
         'ordered consistent edge clocks')
    observed=[s for m in action['moves'] for s in m['settling']]
    observed+=action['before_click_settling']+cursors
    samples=receipt['input_samples']
    need(len(samples)>=2,'raw input observation brackets cursor evidence')
    need(all(samples[0]['wall_time_ns']<=s['wall_time_ns']<=samples[-1]['wall_time_ns']
             for s in observed), 'all cursor evidence inside actual input observation')
    origin=observed[0]
    need(all(abs((s['wall_time_ns']-origin['wall_time_ns'])-
                 (s['monotonic_ns']-origin['monotonic_ns']))<=25_000_000 for s in observed),
         'whole cursor sequence has consistent wall and monotonic clocks')
    for e in edges:
        need(list(struct.unpack('<ii',bytes.fromhex(e['guard']['cursor_hex'])))==list(target),
             'frozen button-edge game coordinates match live cursor')
    # Only geometry-policy fields change in this private schema view. Original
    # guards, edges, raw producer samples and report identity stay untouched.
    view_receipt=copy.deepcopy(receipt); view_action=view_receipt['action']
    view_action['movement_mode']='absolute_virtual_desktop'
    for move,normalized in zip(view_action['moves'],canonical):
        move['normalized']=normalized;move.pop('feedback_correction',None)
    view=dict(p,mouse_controller=dict(controller,receipt=view_receipt),collector_input_actions=[view_receipt])
    result=menu.verify_input(view,raw,game,hwnd,worker,check_disk)
    need(result['input_edges_observed'] is True, 'real original press held and release samples required')
    result.update(movement_mode='absolute_virtual_desktop_feedback',feedback_corrections=corrections,
                  button_edges_independently_verified=True,minimum_selector_iterations=min(counters))
    return result


def verify_host_envelope(report):
    hp=report['host_preflight']
    need(hp.get('implementations')==[identity(p) for p in HOST_PATHS], 'exact host v5 implementation manifest')
    need(hp['accepted'] is False and hp['full_graphics_qualification'] is False
         and hp['screenshot_required'] is False and hp['image_review_wait'] is False
         and hp['requires_independent_handoff_verification'] is True,
         'explicit native-state host scope')
    need(hp['input_mode']=='original_native_menu_state' and hp['budget_events']==[], 'host input mode and budget')
    number(hp['deadline_utc'],'host authorization deadline')
    need(type(hp['successor_observed']) is bool, 'host successor flag type')
    need(not any('story' in key for key in report['probe']), 'no hidden host story inputs')
    return hp


def verify_outcome(report,result):
    hp=report['host_preflight'];p=report['probe']
    need(result['native_menu_handoff_observed'] is True
         and result['menu_ready_one_second_independently_sampled'] is True,
         'independent input and menu retirement to NEW_GAME required')
    new_workers=[w for w in p['workers'] if w['vtable']==menu.NEW_GAME]
    need(len(new_workers)==1 and 'exit' in new_workers[0], 'actual NEW_GAME worker retirement required')
    exit=new_workers[0]['exit']
    need(exit['code']==0 and exit['wait_status']==0 and exit['before_WM_CLOSE'] is True,
         'NEW_GAME exit0 before cleanup')
    adv=[s for s in result['successor_observations'] if s['vtable']==menu.ADV
         and s['TLS_verified'] and s['elapsed']>=exit['elapsed']]
    need(adv and hp['successor_observed'] is True, 'actual TLS-owned ADV after NEW_GAME exit')
    need(p['stop_reason']=='controller_finished_observation', 'stop after observed ADV only')
    after=p['mouse_controller']['receipt']['after_elapsed']
    need(0 <= adv[0]['elapsed']-after <= 20, 'ADV within bounded post-input window')
    result.update(host_menu_observation_verified=True,host_ADV_observations=adv,
                  full_graphics_qualification=False,accepted=False)
    return result


def verify_report(report,raw,check_disk=True):
    verify_host_envelope(report)
    result=bind(menu.verify_report,verify_input=verify_input)(report,raw,check_disk)
    samples=report['probe']['samples']
    first_menu=next(s['elapsed'] for s in samples if any(t['vtable']==menu.MENU for t in s['tasks']))
    before=report['probe']['mouse_controller']['receipt']['before_elapsed']
    need(0<=before-first_menu<15,'input within first native menu readiness budget')
    return verify_outcome(report,result)


def read_small(path,digest):
    path=Path(path);need(path.stat().st_size<=1024*1024,'bounded desktop receipt')
    data=path.read_bytes();need(hashlib.sha256(data).hexdigest()==digest,'desktop receipt SHA')
    return json.loads(data)


def verify_desktop(report,receipt,recovery=None):
    expected=next(x['sha256'] for x in report['host_preflight']['implementations']
                  if x['path']=='devtools/terminal_host_desktop.py')
    need(receipt['observer_sha256']==expected and receipt['action_error'] is None
         and 'audit_error' not in receipt,'authenticated desktop observer completed')
    before=receipt['before']
    need(before['input_desktop']==report['desktop'] and not desktop.health(before),
         'same healthy original desktop baseline')
    after=receipt['after']
    start=before['time_ns']; end=report['host_preflight']['deadline_utc']*1e9
    samples=report['probe']['mouse_controller']['receipt']['input_samples']
    need(type(start) is int and 360e9 <= end-start <= 600e9,
         'desktop baseline within authorized window')
    def ordered(rows,lower):
        need(isinstance(rows,list) and len(rows)==2,'exact two desktop samples')
        a,b=[s['time_ns'] for s in rows]
        need(type(a) is int and type(b) is int and lower<a<b<=end and b-a>=900_000_000,
             'desktop observations within authorized window and separated by one second')
        return b
    need(start <= samples[0]['wall_time_ns'] <= samples[-1]['wall_time_ns'],
         'desktop baseline precedes actual input')
    original_end=ordered(after,samples[-1]['wall_time_ns'])
    checks=[desktop.differences(before,s) for s in after]
    need(len(after)==2 and checks==receipt['checks']
         and receipt['restored'] is (not any(checks)), 'recomputed original restoration result')
    if recovery is not None:
        need(recovery['before']==before and recovery['restored'] is True, 'recovery retains original baseline')
        need('final_after' in recovery and 'final_checks' in recovery,
             'explicit initial and final recovery samples required')
        initial=recovery['after']
        initial_end=ordered(initial,original_end)
        need([desktop.differences(before,s) for s in initial]==recovery['checks'],
             'recomputed initial recovery checks')
        after=recovery['final_after']
        ordered(after,initial_end)
        checks=[desktop.differences(before,s) for s in after]
        need(checks==recovery['final_checks'], 'recomputed recovery checks')
    need(len(after)==2 and not any(checks),'two restored desktop samples')
    return dict(restored=True,recovery_used=recovery is not None,checks=checks)


def verify_file(path,digest,desktop_digest,recovery_path=None,recovery_digest=None):
    path=Path(path).resolve()
    report=menu.read_menu_report(path,digest)
    verify_host_envelope(report)
    result=bind(menu.verify_file,verify_report=verify_report)(path,digest)
    sidecar=Path(str(path)+'.desktop.json')
    receipt=read_small(sidecar,desktop_digest)
    need((recovery_path is None)==(recovery_digest is None),'explicit recovery path and SHA together')
    recovery=read_small(recovery_path,recovery_digest) if recovery_path else None
    if recovery:
        need((ROOT/recovery['source']).resolve()==sidecar,'recovery for this exact desktop receipt')
    result['desktop']=verify_desktop(report,receipt,recovery)
    result['host_verifier']=identity('devtools/terminal_host_menu_verification.py')
    result['host_dependencies']=[identity(p) for p in (
        'devtools/terminal_menu_handoff_verification.py',
        'devtools/terminal_school_handoff_verification.py','devtools/terminal_host_desktop.py')]
    result['desktop_source']=dict(path=str(sidecar),sha256=desktop_digest)
    if recovery:result['recovery_source']=dict(path=str(recovery_path),sha256=recovery_digest)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);parser.add_argument('--sha256',required=True)
    parser.add_argument('--desktop-sha256',required=True)
    parser.add_argument('--recovery');parser.add_argument('--recovery-sha256')
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    result=verify_file(args.report,args.sha256,args.desktop_sha256,args.recovery,args.recovery_sha256)
    need(args.out.resolve().is_relative_to(ROOT/'analysis'),'project-local verification output')
    with args.out.open('x',encoding='utf8') as stream:json.dump(result,stream,indent=2)
    print(json.dumps(dict(host_menu_observation_verified=result['host_menu_observation_verified'],accepted=False)))
