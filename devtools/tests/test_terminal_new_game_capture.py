"""Offline state-machine, recorded source and fault tests. No desktop/native launch."""
import copy
import gzip
import hashlib
import json
import struct
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from devtools import terminal_new_game_capture as c
from devtools import terminal_new_game_verification as v
from devtools import terminal_host_menu_preflight_v6 as host

SOURCE = host.ROOT/'analysis/terminal-host-menu-state-native-v1-20261112.json.gz'
DIGEST = '92fc2084af0e9208e53afb087c84d063a284e61a0e765cd4aeb7a324b9bf11e8'


def source():
    packed = SOURCE.read_bytes()
    assert hashlib.sha256(packed).hexdigest() == DIGEST
    return json.loads(gzip.decompress(packed))


class Clock:
    def __init__(self): self.now = 0.
    def __call__(self): self.now += .00001; return self.now
    def elapsed(self): return self()


class API:
    """Inert handle simulation using recorded MENU/ADV raw schemas."""
    def __init__(self, row, main):
        self.current = copy.deepcopy(row)
        self.main = main
        self.log, self.held, self.handles, self.dead = [], [], {}, set()
        self.error = None

    def open_thread(self, tid):
        self.handles[tid] = tid
        return tid

    def duplicate_thread(self, remote, tid):
        assert self.held == [self.main]
        self.log.append(('duplicate', tid))
        self.handles[tid] = tid
        return tid

    def suspend(self, h):
        if self.error == 'suspend' and h != self.main:
            raise OSError('suspend failed')
        self.held.append(h)
        self.log.append(('suspend',h))
        return 1 if self.error == 'prior' and h != self.main else 0

    def resume(self, h):
        assert self.held.pop() == h
        self.log.append(('resume',h))
        if self.error == 'resume' and h != self.main:
            raise OSError('resume failed')
        return 1

    def close(self, h):
        self.log.append(('close',h))
        if self.error == 'close' and h != self.main:
            raise OSError('close failed')

    def status(self, h): return 0 if h in self.dead else None
    def event(self, ctx, remote):
        assert len(self.held) == 2 or self.current['tasks'][0]['thread_id'] in self.dead
        if self.error == 'event': raise ValueError('event identity failed')
        return dict(remote_handle=remote,owner_pid=15300,duplicate_succeeded=True,
                    query_status=0,type_name='Event',wait_or_signal_called=False)

    def graph(self, ctx):
        assert self.held[0] == self.main
        ctx.get(0x10000,48)
        nodes = copy.deepcopy(self.current['registered_tasks'])
        if self.error == 'generation' and len(self.held)>1:
            b=bytearray.fromhex(nodes[0]['head_hex']);struct.pack_into('<I',b,0x1C,999)
            nodes[0]['head_hex']=b.hex()
        return bytes(0x120), nodes

    def frame(self, ctx, h, tid):
        assert tid in self.held
        if self.error == 'frame': raise ValueError('context failure')
        return copy.deepcopy(next(f for f in self.current['frames'] if f['tid']==tid))

    def row(self, ctx, owned, frames):
        if self.error == 'row': raise ValueError('raw read failure')
        if self.error == 'budget': ctx.get(0x10000,4097)
        row=copy.deepcopy(self.current)
        row['elapsed']=owned.elapsed();row['frames']=frames
        for task in row['tasks']:
            if task['thread_id'] not in self.held:task.pop('TLS',None)
        return row


class CaptureTests(unittest.TestCase):
    def setup_capture(self):
        p=source()['probe'];row=p['samples'][4]
        clock=Clock();api=API(row,p['startup']['window']['main_tid'])
        context=SimpleNamespace(pid=p['pid'],get=lambda p,n:bytes(n))
        cap=c.Capture(context,clock,api.main,api,clock)
        return p,cap,api,clock

    def test_reuses_real_raw_sample_with_only_main_and_current_worker(self):
        p,cap,api,_=self.setup_capture()
        row=cap.snapshot();cap.close()
        old=api.current
        for k in old:
            if k not in ('elapsed','frames'):self.assertEqual(row[k],old[k])
        self.assertEqual([f['tid'] for f in row['frames']], [api.main,old['tasks'][0]['thread_id']])
        self.assertEqual([s[0] for s in api.log[:5]], ['suspend','duplicate','suspend','resume','resume'])
        self.assertFalse(api.held)
        self.assertTrue(cap.receipt()['handles_closed'])

    def test_all_faults_restore_worker_then_main_and_close_handles(self):
        for fault in ('suspend','prior','generation','event','frame','row','budget','resume'):
            with self.subTest(fault=fault):
                _,cap,api,_=self.setup_capture();api.error=fault
                with self.assertRaises((ValueError,OSError)):cap.snapshot()
                cap.close()
                self.assertFalse(api.held)
                self.assertIn(('resume',api.main),api.log)
                self.assertEqual(len([x for x in api.log if x[0]=='close']),2)

    def test_close_failure_attempts_every_handle_and_cannot_claim_closed(self):
        _,cap,api,_=self.setup_capture();cap.snapshot();api.error='close'
        with self.assertRaises(ValueError):cap.close()
        self.assertFalse(cap.receipt()['handles_closed'])
        self.assertEqual(api.log[-1],('close',api.main))
        main_closes=api.log.count(('close',api.main))
        api.error=None;cap.close()
        self.assertTrue(cap.receipt()['handles_closed'])
        self.assertEqual(api.log.count(('close',api.main)),main_closes)

    def test_resume_time_counts_toward_pause_budget(self):
        _,cap,api,clock=self.setup_capture()
        resume=api.resume
        def delayed(h): clock.now+=.2;return resume(h)
        api.resume=delayed
        with self.assertRaisesRegex(ValueError,'pause budget'):cap.snapshot()
        cap.close();self.assertFalse(api.held)

    def test_cumulative_and_wall_budgets(self):
        for budget in ('reads','read_bytes','pause','wall','polls'):
            _,cap,api,clock=self.setup_capture()
            if budget=='reads':cap.reads=c.LIMITS['reads']
            if budget=='read_bytes':cap.read_bytes=c.LIMITS['read_bytes']
            if budget=='pause':cap.pause_total=c.LIMITS['total_pause_seconds']
            if budget=='wall':clock.now=41
            if budget=='polls':cap.polls=[{}]*c.LIMITS['polls']
            with self.assertRaises(ValueError):cap.snapshot()
            cap.close();self.assertFalse(api.held)

    def fixture(self):
        p,cap,api,clock=self.setup_capture();rows=[]
        for original in (p['samples'][4],p['samples'][7]):
            api.current=copy.deepcopy(original)
            if rows:api.dead.add(rows[0]['tasks'][0]['thread_id'])
            row=cap.snapshot();row['index']=len(rows);rows.append(row)
            cap.polls[-1]['saved_index']=row['index']
        cap.close()
        result=dict(startup=p['startup'],samples=rows,workers=cap.workers,
                    targeted_capture=cap.receipt(),mouse_controller=dict(receipt=dict(after_elapsed=0.)))
        return result

    def test_address_and_event_reuse_keep_distinct_retained_threads(self):
        p=self.fixture();a,b=p['workers']
        self.assertEqual(a['pointer'],b['pointer'])
        self.assertEqual(a['event']['remote_handle'],b['event']['remote_handle'])
        self.assertNotEqual(a['generation'],b['generation'])
        self.assertEqual(a['exit']['code'],0)
        self.assertNotIn('exit',b)
        self.assertEqual(v.verify_capture(p)['retained_samples'],2)

    def test_already_exited_current_worker_has_no_context_or_tls(self):
        p,cap,api,clock=self.setup_capture()
        api.dead.add(api.current['tasks'][0]['thread_id'])
        row=cap.snapshot();row['index']=0;cap.polls[-1]['saved_index']=0;cap.close()
        self.assertEqual([f['tid'] for f in row['frames']],[api.main])
        self.assertNotIn('TLS',row['tasks'][0])
        self.assertGreaterEqual(cap.workers[0]['exit']['elapsed'],row['elapsed'])
        fixture=dict(startup=p['startup'],samples=[row],workers=cap.workers,
                     targeted_capture=cap.receipt(),mouse_controller=dict(receipt=dict(after_elapsed=0.)))
        v.verify_capture(fixture)
        fixture['targeted_capture']['polls'][0]['inactive_workers']=[]
        with self.assertRaises(ValueError):v.verify_capture(fixture)

    def test_same_node_tid_changed_handle_rejected(self):
        _,cap,api,_=self.setup_capture();cap.snapshot()
        row=api.current
        for entry,field in ((row['registered_tasks'][0],'head_hex'),(row['tasks'][0],'header_hex')):
            raw=bytearray.fromhex(entry[field]);struct.pack_into('<I',raw,0x20,999)
            entry[field]=raw.hex()
        with self.assertRaisesRegex(ValueError,'generation'):cap.snapshot()
        cap.close();self.assertFalse(api.held)

    def test_independent_audit_rejects_incomplete_or_spliced_capture(self):
        mutations=[lambda p:p['targeted_capture'].update(handles_closed=False),
            lambda p:p['targeted_capture']['polls'][0]['resumed'].reverse(),
            lambda p:p['targeted_capture']['polls'][0].pop('saved_index'),
            lambda p:p['targeted_capture']['polls'][0].update(error='read failed'),
            lambda p:p['targeted_capture']['polls'][0].update(pause_seconds=1),
            lambda p:p['workers'][1]['generation'].__setitem__(2,999),
            lambda p:p['workers'][1].update(first_elapsed=0),
            lambda p:p['samples'][0]['frames'].reverse(),
            lambda p:p['targeted_capture'].update(reads=1),
            lambda p:p['workers'][1].update(exit=dict(code=0,elapsed=0))]
        for mutation in mutations:
            p=self.fixture();mutation(p)
            with self.assertRaises((ValueError,KeyError)):v.verify_capture(p)

    def test_unsaved_poll_cannot_change_handle_or_invent_worker(self):
        p,cap,api,clock=self.setup_capture();rows=[]
        for i in range(2):
            row=cap.snapshot()
            if i==0:
                row['index']=0;rows.append(row);cap.polls[-1]['saved_index']=0
        cap.close()
        fixture=dict(startup=p['startup'],samples=rows,workers=cap.workers,
                     targeted_capture=cap.receipt(),mouse_controller=dict(receipt=dict(after_elapsed=0.)))
        v.verify_capture(fixture)
        for field in (0,1,2,3,4):
            changed=copy.deepcopy(fixture)
            changed['targeted_capture']['polls'][1]['generations'][0][field]+=1
            with self.assertRaises(ValueError):v.verify_capture(changed)
        changed=copy.deepcopy(fixture);poll=changed['targeted_capture']['polls'][1]
        poll['suspended']=poll['suspended'][:1];poll['resumed']=poll['resumed'][-1:]
        with self.assertRaisesRegex(ValueError,'every registered worker'):v.verify_capture(changed)

    def test_real_source_still_fails_strict_missing_new_game(self):
        report=source()
        with self.assertRaisesRegex(ValueError,'NEW_GAME'):
            v.old.verify_report(report,(host.ROOT/'analysis/hermit_game.exe').read_bytes())

    def test_no_implicit_launch_and_exact_new_manifest(self):
        with self.assertRaises(PermissionError):host.run('unused',0)
        with self.assertRaises(ValueError):host.run('unused',0,True)
        self.assertEqual(host.IMPLEMENTATIONS,v.PATHS)

    def test_controller_is_bound_as_a_private_global(self):
        from devtools.terminal_scene_resources import clone
        marker=object();bound=clone(c.continue_menu,CONTROLLER=marker)
        self.assertIs(bound.__globals__['CONTROLLER'],marker)
        self.assertNotIn('CONTROLLER',bound.__code__.co_varnames)
        self.assertIsNone(c.CONTROLLER)


if __name__=='__main__':unittest.main()
