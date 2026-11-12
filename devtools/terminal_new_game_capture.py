"""Bounded MAIN-first menu observer; no input, game calls or process writes.

Only MAIN and the currently registered menu/NEW_GAME/ADV workers are suspended.
This is sampled ownership evidence, not atomic whole-process state or a trace.
Imports are inert; native APIs are loaded only when NativeAPI is constructed.
"""
from contextlib import contextmanager
import json
import time
from types import SimpleNamespace

MENU, NEW_GAME, ADV = 0x59B060, 0x5A0824, 0x5C306C
CONTROLLER = None
LIMITS = dict(polls=2048, samples=512, reads=200000, read_bytes=16*1024*1024,
              pause_seconds=.25, total_pause_seconds=5., observer_seconds=40.,
              post_input_seconds=20., interval_seconds=.01)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def word(raw, offset=0):
    return int.from_bytes(raw[offset:offset+4], 'little')


def generation(node):
    h = bytes.fromhex(node['head_hex'])
    need(len(h) == 48, 'complete scheduler node')
    return (node['pointer'], word(h), word(h, 0x24), word(h, 0x20), word(h, 0x1C))


class Capture:
    def __init__(self, c, owned, main_tid, api, clock=time.monotonic):
        self.c, self.owned, self.api, self.clock = c, owned, api, clock
        self.started = clock()
        self.reads = self.read_bytes = 0
        self.workers, self.handles, self.generations, self.polls = [], {}, {}, []
        self.pause_total = 0.
        self.local = SimpleNamespace(**vars(c))
        self.local.get = self.read
        self.main_tid = main_tid
        self.main = api.open_thread(main_tid)
        self.closed = False

    def read(self, address, size):
        need(0 < size <= 4096, 'bounded individual read')
        self.reads += 1
        self.read_bytes += size
        need(self.reads <= LIMITS['reads'] and self.read_bytes <= LIMITS['read_bytes'],
             'capture read budget')
        self.check_time()
        data = self.c.get(address, size)
        need(len(data) == size, 'complete capture read')
        return data

    def check_time(self):
        now = self.clock()
        need(now-self.started <= LIMITS['observer_seconds'], 'observer wall budget')
        if getattr(self, 'pause_start', None) is not None:
            span = now-self.pause_start
            need(span <= LIMITS['pause_seconds'] and
                 self.pause_total+span <= LIMITS['total_pause_seconds'], 'capture pause budget')

    def snapshot(self):
        need(not self.closed and len(self.polls) < LIMITS['polls'], 'bounded open observer')
        self.check_time()
        held = []
        poll = dict(index=len(self.polls), begin=self.owned.elapsed(), suspended=[], resumed=[],
                    inactive_workers=[], error=None)
        self.polls.append(poll)
        self.pause_start = None
        def hold(handle, tid):
            previous = self.api.suspend(handle)
            held.append((handle, tid))  # Even an unexpected prior count needs our increment removed.
            if self.pause_start is None:
                self.pause_start = self.clock()
            poll['suspended'].append(dict(tid=tid, previous=previous))
            need(previous == 0, 'no concurrent freezer or externally suspended thread')
        try:
            hold(self.main, self.main_tid)
            _, nodes = self.api.graph(self.local)
            keys = [generation(n) for n in nodes]
            need(len(keys) <= 3 and all(k[1] in (MENU, NEW_GAME, ADV) for k in keys),
                 'only bounded menu NEW_GAME ADV graph')
            active = [(self.main, self.main_tid)]
            new = []
            for key in keys:
                node, vt, tid, remote, event = key
                if not tid or not remote:
                    continue
                need(tid != self.main_tid, 'distinct original worker')
                short = (node, tid)
                need(self.generations.get(short, key) == key, 'node/TID reused with changed generation')
                if short not in self.handles:
                    handle = self.api.duplicate_thread(remote, tid)
                    self.handles[short] = handle
                    self.generations[short] = key
                    worker = dict(pointer=node, thread_id=tid, vtable=vt, original_handle=remote,
                                  first_elapsed=poll['begin'], generation=list(key))
                    self.workers.append(worker)
                    new.append(short)
                handle = self.handles[short]
                status = self.api.status(handle)
                if status is None:
                    hold(handle, tid)
                    # It may have exited between the zero-time status query and suspend.
                    need(self.api.status(handle) is None, 'worker exited during capture entry')
                    active.append((handle, tid))
                else:
                    need(status == 0, 'abnormal current worker exit')
                    poll['inactive_workers'].append(dict(generation=list(key), code=status,
                                                        elapsed=self.owned.elapsed()))
            _, again = self.api.graph(self.local)
            need([generation(n) for n in again] == keys, 'same graph generation after worker suspension')
            for worker in self.workers:
                short = (worker['pointer'], worker['thread_id'])
                if short in new:
                    worker['event'] = self.api.event(self.local, worker['generation'][4])
            frames = [self.api.frame(self.local, h, tid) for h, tid in active]
            row = self.api.row(self.local, self.owned, frames)
            need([generation(n) for n in row['registered_tasks']] == keys,
                 'same generation in full raw sample')
            # First-seen timestamps must bind to a retained raw sample, including exited nodes.
            for worker in self.workers:
                if (worker['pointer'], worker['thread_id']) in new:
                    worker['first_elapsed'] = row['elapsed']
                if 'exit' not in worker:
                    code = self.api.status(self.handles[(worker['pointer'],worker['thread_id'])])
                    if code is not None:
                        worker['exit'] = dict(code=code, wait_status=0, elapsed=self.owned.elapsed(),
                                              before_WM_CLOSE=True)
                        need(code == 0, 'abnormal retained worker exit')
            poll.update(sample_elapsed=row['elapsed'], generations=[list(k) for k in keys],
                        new_workers=[list(k) for k in new])
            self.check_time()
            return row
        except BaseException as exc:
            poll['error'] = repr(exc)
            raise
        finally:
            errors = []
            for handle, tid in reversed(held):
                try:
                    previous = self.api.resume(handle)
                    poll['resumed'].append(dict(tid=tid, previous=previous))
                    if previous != 1:
                        errors.append('unexpected resume count for '+str(tid))
                except BaseException as exc:
                    errors.append(repr(exc))
            span = self.clock()-self.pause_start if self.pause_start is not None else 0.
            self.pause_total += span
            self.pause_start = None
            poll.update(end=self.owned.elapsed(), pause_seconds=span,
                        reads=self.reads, read_bytes=self.read_bytes, cleanup_errors=errors)
            need(not errors, 'failed to restore all captured threads: '+repr(errors))
            need(span <= LIMITS['pause_seconds'] and self.pause_total <= LIMITS['total_pause_seconds'],
                 'capture pause budget including cleanup')

    def close(self):
        if not self.closed:
            errors = []
            for key, handle in list(self.handles.items()):
                try:
                    self.api.close(handle)
                    del self.handles[key]
                except Exception as exc:
                    errors.append(repr(exc))
            if self.main is not None:
                try:
                    self.api.close(self.main)
                    self.main = None
                except Exception as exc:
                    errors.append(repr(exc))
            self.closed = not errors
            need(not errors, 'observer handle close failed: '+repr(errors))

    def receipt(self):
        return dict(contract='main_first_new_game_v1', limits=LIMITS.copy(), polls=self.polls,
                    reads=self.reads, read_bytes=self.read_bytes, pause_seconds=self.pause_total,
                    handles_closed=self.closed, full_process_atomic=False, accepted=False)


class NativeAPI:
    def __init__(self, c):
        import ctypes as C
        import ctypes.wintypes as W
        from devtools import terminal_menu_handoff as menu
        self.C, self.W, self.menu, self.base, self.c = C, W, menu, menu.base, c

    def owner(self, h, tid):
        need(self.base.get_thread_pid(h) == self.c.pid and self.base.get_thread_id(h) == tid,
             'retained current process/thread identity')

    def open_thread(self, tid):
        h = self.base.original.opent(0x10004A, False, tid)
        self.base.original.check(h, 'open own MAIN thread')
        try:
            self.owner(h, tid)
            return h
        except BaseException:
            self.close(h)
            raise

    def duplicate_thread(self, remote, tid):
        h = self.W.HANDLE()
        b = self.base
        b.original.check(b.parent.duplicate(self.c.h, remote, b.parent.current_process(),
                                           self.C.byref(h), 0, False, 2), 'retain current worker before resume')
        try:
            self.owner(h, tid)
            return h
        except BaseException:
            self.close(h)
            raise

    def suspend(self, h):
        previous = self.base.original.suspend(h)
        need(previous != 0xFFFFFFFF, 'successful owned suspension')
        return previous

    def resume(self, h):
        previous = self.base.original.resume(h)
        need(previous != 0xFFFFFFFF, 'successful owned resume')
        return previous

    def close(self, h):
        self.base.original.check(self.base.original.close(h), 'close retained observer handle')

    def status(self, h):
        status = self.base.original.wait(h, 0)
        need(status in (0, 258), 'non-consuming retained thread status')
        if status == 258:
            return None
        code = self.W.DWORD()
        self.base.original.check(self.base.parent.exit_thread(h, self.C.byref(code)), 'retained thread exit code')
        return code.value

    def graph(self, c):
        return self.menu.startup.graph(c)

    def event(self, c, remote):
        return self.base.event_identity(c, remote)

    def frame(self, c, handle, tid):
        C = self.C
        buf = C.create_string_buffer(736)
        at = (C.addressof(buf)+15) & ~15
        C.memset(at, 0, 716)
        C.c_uint32.from_address(at).value = 0x1003F
        self.base.original.check(self.base.original.ctx(handle, at), 'actual suspended WOW64 context')
        raw = C.string_at(at, 716)
        bp, chain = word(raw, 180), []
        for _ in range(100):
            # Match the original bounded unwind's inaccessible-terminator semantics.
            try:
                data = c.get(bp, 8)
            except ValueError as exc:
                if not str(exc).startswith('unreadable actual object '):
                    raise
                break
            nb, ret = word(data), word(data, 4)
            chain.append(dict(bp=bp, saved_bp=nb, return_va=ret))
            if not bp < nb < bp+0x100000:
                break
            bp = nb
        return dict(tid=tid, context_hex=raw.hex(), EIP=word(raw,184), EBP=word(raw,180),
                    ESP=word(raw,196), chain=chain)

    def row(self, c, owned, frames):
        from devtools.terminal_scene_resources import clone
        @contextmanager
        def already_frozen(*args, **kwargs):
            yield frames
        original = SimpleNamespace(**vars(self.base.original))
        original.frozen = already_frozen
        local_base = SimpleNamespace(**vars(self.base))
        local_base.original = original
        # Reuse the unchanged raw schema and TLS validation inside our held interval.
        return clone(self.menu.snapshot, base=local_base)(c, owned)


def continue_menu(pid, owned, progress, duration):
    """Replacement continuation only; original startup, input and cleanup stay frozen."""
    import traceback
    from pathlib import Path
    from devtools import terminal_menu_handoff as menu
    from devtools.terminal_scene_resources import clone
    base = menu.base
    report = dict(pid=pid, error=None, samples=[], workers=[], host_game_calls=[], host_memory_writes=[],
                  collector_input_actions=[], full_battle_exit_accepted=False, full_native_instruction_trace=False)
    c = capture = None
    try:
        report['startup'] = menu.startup_gate.probe(pid, owned, progress, min(duration-30,720))
        need(report['startup']['error'] is None and report['startup']['native_handoff_observed'],
             'current original startup retirement')
        h = base.original.openp(0x100450, False, pid)
        base.original.check(h, 'read-only current menu process')
        c = SimpleNamespace(h=h, pid=pid, owned=owned, get=lambda p,n:base.original.required(h,p,n))
        c.main = word(c.get(0x7A4A00,4))
        report['main'] = c.main
        identity = clone(base.source_identity, RANGES=menu.RANGES, IAT=menu.startup.IAT)
        report['source_before'] = identity(c)
        report['TLS_implementation'] = base.tls_contract(c)
        report['manager_event'] = base.event_identity(c, word(c.get(c.main+0x17C,4)))
        capture = Capture(c, owned, report['startup']['window']['main_tid'], NativeAPI(c))
        report['workers'] = capture.workers
        stop = Path(str(progress).removesuffix('.progress.json')+'.stop.json')
        last_signature, last_saved, post_deadline = None, 0., None
        while True:
            if post_deadline is not None:
                need(time.monotonic() < post_deadline, 'post-input 20 second budget')
            row = capture.snapshot()
            signature = (tuple((t['pointer'], t['vtable'], t['thread_id'], 'TLS' in t) for t in row['tasks']),
                         row['MAIN_event_hex'], tuple('exit' in w for w in capture.workers))
            now = time.monotonic()
            if (signature != last_signature or stop.exists()
                    or now-last_saved >= (0.1 if CONTROLLER.done else 1.)):
                need(len(report['samples']) < LIMITS['samples'], 'raw sample retention budget')
                row['index'] = len(report['samples'])
                report['samples'].append(row)
                capture.polls[-1]['saved_index'] = row['index']
                last_signature, last_saved = signature, now
                progress.write_text(json.dumps(dict(status='main_first_menu_capture', pid=pid,
                    elapsed=owned.elapsed(), samples=len(report['samples']), polls=len(capture.polls))), encoding='utf8')
            if stop.exists():
                raw = stop.read_bytes()
                need(len(raw) <= 1024 and json.loads(raw) == {'stop': True}, 'owned observation stop')
                report['stop_reason'] = 'controller_finished_observation'
                break
            CONTROLLER.observe(c, owned, row)  # No capture thread runs concurrently with input guards.
            if CONTROLLER.done and post_deadline is None:
                post_deadline = time.monotonic()+LIMITS['post_input_seconds']
            time.sleep(LIMITS['interval_seconds'] if CONTROLLER.done else .05)
        report['source_after'] = identity(c)
        need(report['source_before'] == report['source_after'], 'original live code unchanged')
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc(limit=8))
    finally:
        report.setdefault('stop_reason', 'bounded_menu_deadline')
        report['mouse_controller'] = dict(attempted=CONTROLLER.done, receipt=CONTROLLER.receipt,
                                         user_override_required=True, maximum_clicks=1)
        if CONTROLLER.receipt is not None:
            report['collector_input_actions'].append(CONTROLLER.receipt)
        if capture:
            try:
                capture.close()
            except Exception as exc:
                report['error'] = repr(exc)
            report['targeted_capture'] = capture.receipt()
        if c:
            base.original.close(c.h)
    return report
