"""Explicitly authorized host preflight: natural startup, image review, one click.

Default invocation prints a plan only. Requires authenticated DXGI pattern qualification and mandatory desktop restoration checks.
No game, desktop query or input on import.
This is development evidence, never a complete battle/graphics acceptance.
"""
import argparse
from datetime import datetime
import gzip
import json
from pathlib import Path
import threading
import time
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = None  # supplied only in the frozen runner's private function globals


def validate_window(deadline, now):
    remaining = deadline - now
    if not 360 <= remaining <= 600:
        raise ValueError('fresh explicit desktop window of 360..600 seconds required')
    return remaining


def approval_matches(path, preview):
    if not path.exists():
        return False
    if path.stat().st_size > 1024:
        raise ValueError('oversized image review receipt')
    value = json.loads(path.read_text(encoding='utf8'))
    if value != {'sha256': preview['sha256'], 'image_visually_confirmed': True}:
        raise ValueError('review must identify this exact menu image')
    return True


def _run(out, deadline_utc, capture_override, qualification):
    if capture_override is not True:
        raise PermissionError('native screenshot override required before launch')
    deadline = time.monotonic() + validate_window(deadline_utc, time.time())
    from devtools import terminal_menu_handoff as menu
    from devtools.terminal_scene_resources import clone
    from functools import partial
    from devtools.terminal_dxgi_game_capture import capture_owned as dxgi_capture, qualify_current
    qualify_current(qualification)
    capture_owned = partial(dxgi_capture, qualification=qualification)
    base = menu.base
    implementation_paths = [Path(__file__), ROOT/'devtools/terminal_dxgi_game_capture.py']
    implementations = [base.identity(p) for p in implementation_paths]
    suffixes = ('', '.progress.json', '.stop.json', '.png', '.preview.json', '.review.json',
                '.startup.png', '.startup-preview.json', '.startup-review.json')
    if not out.resolve().is_relative_to(ROOT / 'analysis') or any(
            Path(str(out)+s).exists() for s in suffixes):
        raise ValueError('fresh output family under analysis required')
    preview_path = Path(str(out)+'.preview.json')
    review_path = Path(str(out)+'.review.json')
    budget_events = []
    observations = {'successor_observed': False}

    class BudgetRuntime(base.VisibleOwnedRuntime):
        def __init__(self):
            super().__init__()
            self.budget_lock = threading.Lock()
            self.budget_timer = None
            self.budget_closed = False

        def start(self):
            # Full asset audit already ran. Never start a game when its natural
            # 273-second startup plus observation/cleanup cannot fit the window.
            remaining = deadline-time.monotonic()
            if remaining < 410:
                raise ValueError('asset audit consumed launch budget; no game started')
            def expire():
                with self.budget_lock:
                    if self.budget_closed: return
                    budget_events.append({'reason': 'hard_deadline', 'at': time.time()})
                    base.original.check(base.original.terminate(self.job, 1), 'own Job deadline')
            self.budget_timer = threading.Timer(remaining-15, expire)
            self.budget_timer.daemon = True
            self.budget_timer.start()
            super().start()

        def finish(self):
            with self.budget_lock:
                self.budget_closed = True
                if self.budget_timer: self.budget_timer.cancel()
                return super().finish()

    class ReviewedSelection(menu.OneMenuSelection):
        def __init__(self, *args):
            super().__init__(*args)
            self.preview = None

        def observe(self, c, owned, row):
            if time.monotonic() >= deadline-25:
                raise TimeoutError('reserved cleanup budget reached')
            tasks = row['tasks']
            ready = (len(tasks) == 1 and tasks[0]['vtable'] == menu.startup.MENU
                     and menu.word(bytes.fromhex(tasks[0]['header_hex']), 0x30) == 1
                     and menu.word(bytes.fromhex(row['MAIN_event_hex'])) == 0)
            frame = next((f for f in row['frames']
                          if ready and f['tid'] == tasks[0]['thread_id']), None)
            ready = bool(ready and frame and any(x['return_va'] == 0x45F065 for x in frame['chain']))
            if not self.preview:
                if not ready: return
                self.preview = capture_owned(c, base.original.findwindow(b'Cross Hermit', None),
                    Path(str(out)+'.png'), explicit_capture_override=True)
                preview_path.write_text(json.dumps(self.preview), encoding='utf8')
                return
            if not approval_matches(review_path, self.preview): return
            super().observe(c, owned, row)
            # Stop at the actual ADV successor; collector still records worker
            # exits before calling us. Verification must establish causality.
            if self.done and self.receipt and not self.receipt.get('error'):
                if any(t['vtable'] == 0x5C306C for t in tasks) and not any(
                        t['vtable'] == menu.startup.MENU for t in tasks):
                    observations['successor_observed'] = True
                    Path(str(out)+'.stop.json').write_text('{"stop":true}', encoding='utf8')

    local_base = SimpleNamespace(**vars(base))
    local_base.VisibleOwnedRuntime = BudgetRuntime
    def image_first(pid, owned, progress, duration):
        # Discover a broken capture backend BEFORE waiting through the animation.
        handle = None
        try:
            handle = base.original.openp(0x100450, False, pid)
            base.original.check(handle, 'read-only early preview owner')
            c = SimpleNamespace(h=handle, pid=pid, owned=owned,
                                get=lambda p, n: base.original.required(handle, p, n))
            c.main = menu.word(c.get(0x7A4A00, 4))
            preview = capture_owned(c, base.original.findwindow(b'Cross Hermit', None),
                Path(str(out)+'.startup.png'), explicit_capture_override=True)
            Path(str(out)+'.startup-preview.json').write_text(json.dumps(preview), encoding='utf8')
            review = Path(str(out)+'.startup-review.json')
            review_until = min(deadline-350, time.monotonic()+30)
            while not approval_matches(review, preview):
                if time.monotonic() >= review_until:
                    raise TimeoutError('early image review absent; do not wait through startup')
                time.sleep(.1)
        except Exception as exc:
            return dict(error=repr(exc), accepted=False, early_capture_failed=True,
                        host_game_calls=[], host_memory_writes=[], collector_input_actions=[])
        finally:
            if handle: base.original.close(handle)
        return clone(menu.continue_menu, CONTROLLER=CONTROLLER)(pid, owned, progress, duration)
    # Frozen functions execute with a private globals mapping, not hot patches.
    run_menu = clone(menu.run, base=local_base, OneMenuSelection=ReviewedSelection,
                     continue_menu=image_first)
    result = run_menu(out, 330, 0, True, 0)
    if implementations != [base.identity(p) for p in implementation_paths]:
        raise ValueError('host preflight implementation changed during run')
    result['host_preflight'] = dict(deadline_utc=deadline_utc, budget_events=budget_events,
        **observations,
        image_review_path=str(review_path), source_implementation=base.identity(Path(__file__)),
        capture_implementation=base.identity(ROOT/'devtools/terminal_dxgi_game_capture.py'),
        full_graphics_qualification=False, accepted=False)
    payload = gzip.compress(json.dumps(result, separators=(',', ':')).encode(), mtime=0)
    if len(payload) > 6*1024*1024: raise ValueError('compressed preflight evidence budget')
    with out.open('xb') as stream: stream.write(payload)
    p = result.get('probe') or {}
    return dict(report=base.identity(out), probe_error=p.get('error'),
                lifecycle_error=result['lifecycle']['error'], budget_events=budget_events,
                **observations,
                accepted=False)


def run(out, deadline_utc, capture_override, qualification):
    if capture_override is not True:
        raise PermissionError('current native frame capture authorization required')
    from devtools.terminal_dxgi_game_capture import qualify_current
    from devtools.terminal_host_desktop import guarded_run
    qualify_current(qualification)
    validate_window(deadline_utc, time.time())
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT/'analysis'):
        raise ValueError('fresh project-local output required')
    result = guarded_run(lambda: _run(out, deadline_utc, capture_override, qualification),
                         Path(str(out)+'.desktop.json'))
    return dict(result, desktop_restored=True, desktop_receipt=str(out)+'.desktop.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--allow-native-capture', action='store_true')
    parser.add_argument('--desktop-until', help='Explicit current authorization expiry, ISO8601 with timezone')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--qualification', type=Path)
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps(dict(mode='plan_only', desktop_actions=False, accepted=False,
            maximum_window_seconds=600, capture_timeout_seconds=8,
            natural_startup_seconds_approx=273, observation_seconds=330,
            actions=['fresh asset audit', 'early qualified DXGI crop and agent review',
                     'natural startup retirement', 'menu qualified DXGI crop and agent review',
                     'one original new-game menu click', 'ADV observation', 'cleanup']), indent=2))
    else:
        if not args.desktop_until or not args.out or not args.qualification: parser.error('deadline, qualification and output required')
        end = datetime.fromisoformat(args.desktop_until)
        if end.tzinfo is None: parser.error('explicit deadline timezone required')
        receipt = run(args.out.resolve(), end.timestamp(), args.allow_native_capture, args.qualification)
        print(json.dumps(receipt))
        if (receipt['probe_error'] or receipt['lifecycle_error'] or receipt['budget_events']
                or not receipt['successor_observed']):
            raise SystemExit(1)
