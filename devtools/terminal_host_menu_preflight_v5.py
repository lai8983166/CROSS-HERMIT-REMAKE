"""Bounded native-state menu test. Plan-only unless a fresh desktop window is authorized.

No screenshot or asynchronous image receipt in the input path. This is a native
observation, never full graphics, battle exit or resource/PTD acceptance.
"""
import argparse
from datetime import datetime
import gzip
import json
from pathlib import Path
import threading
import time
from types import SimpleNamespace
from devtools.terminal_menu_state_gate import MenuGate, MENU, ADV

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATIONS = ('devtools/terminal_host_menu_preflight_v5.py',
    'devtools/terminal_menu_state_gate.py', 'devtools/terminal_host_menu_input.py',
    'devtools/terminal_owned_mouse.py', 'devtools/terminal_host_desktop.py')


def validate_window(deadline, now):
    if not 360 <= deadline-now <= 600:
        raise ValueError('fresh explicit desktop window of 360..600 seconds required')


def _run(out, deadline_utc):
    from devtools import terminal_menu_handoff as menu
    from devtools.terminal_scene_resources import clone
    from devtools.terminal_host_menu_input import owned_main_menu_click
    from tools.school_native_dialogue_input import owned_target_guard
    base = menu.base
    identities = [base.identity(ROOT/p) for p in IMPLEMENTATIONS]
    deadline = time.monotonic()+deadline_utc-time.time()
    progress = Path(str(out)+'.progress.json')
    stop = Path(str(out)+'.stop.json')
    events = []
    observations = dict(successor_observed=False, screenshot_required=False,
                        image_review_wait=False, input_mode='original_native_menu_state')

    class BudgetRuntime(base.VisibleOwnedRuntime):
        def __init__(self):
            super().__init__()
            self.lock = threading.Lock()
            self.timer = None
            self.closed = False
        def start(self):
            remaining = deadline-time.monotonic()
            if remaining < 410:
                raise ValueError('asset audit consumed launch budget; no game started')
            def expire():
                with self.lock:
                    if self.closed:
                        return
                    events.append(dict(reason='hard_deadline', at=time.time()))
                    base.original.check(base.original.terminate(self.job, 1), 'own Job deadline')
            self.timer = threading.Timer(remaining-15, expire)
            self.timer.daemon = True
            self.timer.start()
            super().start()
        def finish(self):
            with self.lock:
                self.closed = True
                if self.timer:
                    self.timer.cancel()
                return super().finish()

    class StateSelection:
        def __init__(self, index, authorized, story_limit=0):
            if index != 0 or authorized is not True or story_limit != 0:
                raise ValueError('one authorized new-game click; no story input')
            self.done = False
            self.receipt = self.story = self.ready_start = None
            self.gate = MenuGate()
            self.after_deadline = None

        def observe(self, c, owned, row):
            now = time.monotonic()
            if now >= deadline-25:
                raise TimeoutError('reserved desktop cleanup budget reached')
            if self.done:
                if any(t['vtable'] == ADV for t in row['tasks']) and not any(
                        t['vtable'] == MENU for t in row['tasks']):
                    observations['successor_observed'] = True
                    stop.write_text('{"stop":true}', encoding='utf8')
                elif now >= self.after_deadline:
                    raise TimeoutError('no ADV successor within 20 seconds after input')
                return
            eligible = self.gate.observe(row, now)
            if self.gate.since == now:
                self.ready_start = row
            if not eligible:
                return
            self.gate.claim()
            self.done = True  # Includes failed or uncertain attempts: never retry.
            self.receipt = dict(index=0, before_elapsed=owned.elapsed(), error=None,
                ready_start_sample=self.ready_start, ready_decision_sample=row, input_samples=[])
            try:
                hwnd = base.original.findwindow(b'Cross Hermit', None)
                owned_target_guard(c, hwnd)  # Do not reacquire a user-changed foreground.
                self.receipt['activation'] = dict(hwnd=hwnd, before=hwnd, after=hwnd, operations=[])
                game = menu.word(c.get(0x7A49FC, 4))
                outcome = {}
                def sample():
                    self.receipt['input_samples'].append(dict(elapsed=owned.elapsed(),
                        wall_time_ns=time.time_ns(), mouse_hex=c.get(game+0x196C,0x58).hex(),
                        MAIN_event_hex=c.get(c.main+0x2C,8).hex()))
                def send():
                    try:
                        outcome['action'] = owned_main_menu_click(c, hwnd, 0,
                            explicit_user_override=True, expected_owner=self.gate.owner)
                    except BaseException as exc:
                        outcome['error'] = repr(exc)
                sample()
                worker = threading.Thread(target=send, name='owned-menu-input', daemon=False)
                worker.start()
                try:
                    until = time.monotonic()+5
                    finished = None
                    while time.monotonic() < until and len(self.receipt['input_samples']) < 1024:
                        sample()
                        if not worker.is_alive():
                            if finished is None:
                                finished = time.monotonic()
                            if time.monotonic()-finished >= .1:
                                break
                        time.sleep(.005)
                finally:
                    worker.join(timeout=6)
                self.receipt.update(outcome)
                if worker.is_alive() or 'action' not in outcome:
                    raise ValueError('bounded input did not return a complete receipt')
                action = outcome['action']
                if action['error'] or not action['released']:
                    raise ValueError('bounded input failed; do not retry')
                self.after_deadline = time.monotonic()+20
            except Exception as exc:
                self.receipt['error'] = repr(exc)
                raise
            finally:
                self.receipt['after_elapsed'] = owned.elapsed()

    local_base = SimpleNamespace(**vars(base))
    local_base.VisibleOwnedRuntime = BudgetRuntime
    result = clone(menu.run, base=local_base, OneMenuSelection=StateSelection)(out, 330, 0, True, 0)
    if identities != [base.identity(ROOT/p) for p in IMPLEMENTATIONS]:
        raise ValueError('host implementations changed during test')
    result['host_preflight'] = dict(**observations, deadline_utc=deadline_utc,
        budget_events=events, implementations=identities, accepted=False,
        full_graphics_qualification=False, requires_independent_handoff_verification=True)
    payload = gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0)
    if len(payload) > 6*1024*1024:
        raise ValueError('compressed evidence budget exceeded')
    with out.open('xb') as stream:
        stream.write(payload)
    return dict(report=base.identity(out), **observations, budget_events=events,
        probe_error=(result.get('probe') or {}).get('error'),
        lifecycle_error=result['lifecycle']['error'], accepted=False)


def run(out, deadline_utc, authorized=False):
    if authorized is not True:
        raise PermissionError('current bounded host desktop authorization required')
    validate_window(deadline_utc, time.time())
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT/'analysis') or any(Path(str(out)+s).exists()
            for s in ('', '.progress.json', '.stop.json', '.desktop.json')):
        raise ValueError('fresh project-local output family required')
    from devtools.terminal_host_desktop import guarded_run
    result = guarded_run(lambda: _run(out,deadline_utc),Path(str(out)+'.desktop.json'))
    return dict(result, desktop_restored=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--allow-host-input', action='store_true')
    parser.add_argument('--desktop-until')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps(dict(mode='plan_only', desktop_actions=False, accepted=False,
            screenshot_required=False, maximum_window_seconds=600,
            menu_ready_seconds=15, post_input_seconds=20,
            actions=['fresh asset audit', 'natural startup retirement',
                     'one live-state guarded click', 'ADV observation', 'desktop restoration'])))
    else:
        if not args.desktop_until or not args.out:
            parser.error('explicit deadline and fresh output required')
        end = datetime.fromisoformat(args.desktop_until)
        if end.tzinfo is None:
            parser.error('deadline timezone required')
        result = run(args.out,end.timestamp(),args.allow_host_input)
        print(json.dumps(result))
        if (result['probe_error'] or result['lifecycle_error'] or result['budget_events']
                or not result['successor_observed']):
            raise SystemExit(1)
