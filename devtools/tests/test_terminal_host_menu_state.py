"""Offline only: frozen native rows and inert input API, no desktop queries."""
import copy
import gzip
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch
from devtools.terminal_menu_state_gate import MenuGate, ready_owner
from devtools import terminal_host_menu_input as mouse
from devtools import terminal_host_menu_preflight_v5 as host
from devtools.tests.test_terminal_owned_mouse import DesktopApi

SOURCE = host.ROOT/'analysis/terminal-host-menu-dxgi-v2-20261112.json.gz'


def native_rows():
    return json.loads(gzip.decompress(SOURCE.read_bytes()))['probe']['samples']


class Api(DesktopApi):
    def submit(self, value):
        result = super().submit(value)
        if result and value.data.mi.dwFlags in (2,4):
            self.held = value.data.mi.dwFlags == 2
        return result


def guard(countdown=3000):
    head = bytearray(64)
    struct.pack_into('<III',head,0x1C,11,12,13)
    return dict(selector_hex=struct.pack('<7I',countdown,0,0,5,0,0x45EE6A,0).hex(),
        head_hex=head.hex(),pid=1,hwnd=2,game=3,main=4,node=5,
        selector_pointer=6,coordinate_mode_hex='01000000')


class NativeMenuTests(unittest.TestCase):
    def click(self, api=None, check=guard, sleep=lambda _:None):
        api = api or Api()
        result = mouse.guarded_click(api,check,(318,508),sleep)
        return api,result

    def test_real_rows_become_eligible_before_menu_expiry(self):
        gate=MenuGate();rows=native_rows()
        eligible=next(s for s in rows if gate.observe(s,s['elapsed']))
        self.assertEqual(eligible['index'],5)
        self.assertAlmostEqual(eligible['elapsed'],281.89,places=2)
        gate.claim()
        self.assertFalse(gate.observe(rows[6],rows[6]['elapsed']))
        with self.assertRaises(ValueError):gate.claim()

    def test_timeout_and_retired_menu_never_rearm(self):
        rows=native_rows();g=MenuGate();g.observe(rows[4],0)
        with self.assertRaises(TimeoutError):g.observe(rows[4],15)
        with self.assertRaises(ValueError):g.observe(rows[63],1)

    def test_same_address_new_thread_rejected(self):
        row=native_rows()[4];g=MenuGate();g.observe(row,0)
        changed=copy.deepcopy(row);task=changed['tasks'][0];old=task['thread_id']
        task['thread_id']=old+1;head=bytearray.fromhex(task['header_hex'])
        struct.pack_into('<I',head,0x24,old+1);task['header_hex']=head.hex()
        for frame in changed['frames']:
            if frame['tid']==old:frame['tid']=old+1
        with self.assertRaisesRegex(ValueError,'generation'):g.observe(changed,1)

    def test_sampling_gap_requires_fresh_stability(self):
        row=native_rows()[4];g=MenuGate();g.observe(row,0)
        self.assertFalse(g.observe(row,3));self.assertTrue(g.observe(row,4))

    def test_no_screenshot_dependency_or_implicit_launch(self):
        with self.assertRaises(PermissionError):host.run('unused',0)
        with self.assertRaises(ValueError):host.run('unused',0,True)
        self.assertNotIn('capture',Path(host.__file__).read_text().split('import argparse')[1])

    def test_both_button_edges_checked_with_exact_cursor(self):
        api,r=self.click()
        self.assertIsNone(r['error']);self.assertTrue(r['released'])
        self.assertEqual([x['flags'] for x in r['button_edge_checks']],[2,4])
        self.assertEqual(r['moves'][1]['feedback_correction']['error'],[0,1])

    def test_low_or_restarted_countdown_refuses_input(self):
        for value in (0,299,3660):
            api,r=self.click(check=lambda:guard(value))
            self.assertFalse(r['down_submitted']);self.assertEqual(api.flags,[])
        values=iter((3000,3001))
        api,r=self.click(check=lambda:guard(next(values)))
        self.assertIn('restarted',r['error']);self.assertFalse(r['down_submitted'])

    def test_release_cursor_change_releases_but_fails(self):
        api=Api()
        def sleep(delay):
            if delay==.08:api.xy=(318,509)
        _,r=self.click(api,sleep=sleep)
        self.assertTrue(r['down_submitted']);self.assertTrue(r['released'])
        self.assertTrue(r['release_guard_failed']);self.assertIsNotNone(r['error'])
        self.assertEqual(api.flags.count(2),1);self.assertEqual(api.flags.count(4),1)

    def test_release_owner_change_releases_but_fails(self):
        api=Api()
        def check():
            r=guard()
            if api.held:r['node']=99
            return r
        _,r=self.click(api,check)
        self.assertTrue(r['released']);self.assertIn('generation',r['error'])

    def test_readiness_owner_mismatch_never_moves(self):
        api=Api();r=mouse.guarded_click(api,guard,(318,508),lambda _:None,
                                       expected_owner=(5,999,11,12,6))
        self.assertEqual(api.flags,[]);self.assertIsNotNone(r['error'])

    def test_stale_game_cursor_and_changed_geometry_refused(self):
        for field in ('os_game_point','geometry'):
            api=Api();api.xy=(318,508);old=api.cursor_snapshot
            def snapshot(target):
                r=old(target)
                if field=='os_game_point':r[field][0]+=1
                elif api.held:r[field]['window_rect'][2]+=1
                return r
            api.cursor_snapshot=snapshot;_,r=self.click(api)
            self.assertIsNotNone(r['error'])
            if field=='geometry':self.assertTrue(r['released'])
            else:self.assertFalse(r['down_submitted'])

    def test_failed_release_retried_for_cleanup_only(self):
        api=Api();api.up_fail=True;_,r=self.click(api)
        self.assertTrue(r['released']);self.assertIsNotNone(r['error'])
        self.assertEqual(api.flags.count(2),1)

    def test_hold_exception_plus_guard_failure_still_releases(self):
        api=Api()
        def check():
            if api.held:raise ValueError('lost foreground during hold')
            return guard()
        def sleep(delay):
            if delay==.08:raise RuntimeError('interrupted hold')
        _,r=self.click(api,check,sleep)
        self.assertTrue(r['released']);self.assertTrue(r['release_guard_failed'])
        self.assertEqual(api.flags[-2:],[2,4]);self.assertIsNotNone(r['error'])

    def test_expired_action_refuses_before_input(self):
        with patch.object(mouse.time,'monotonic',side_effect=[0,4]):
            api,r=self.click()
        self.assertEqual(api.flags,[]);self.assertIn('three seconds',r['error'])

    def test_slow_guard_cannot_cross_deadline_and_submit_down(self):
        clock=[0];api=Api();api.xy=(318,508)
        def check():
            clock[0]=4
            return guard()
        with patch.object(mouse.time,'monotonic',side_effect=lambda:clock[0]):
            _,r=self.click(api,check)
        self.assertEqual(api.flags,[]);self.assertIn('three seconds',r['error'])


if __name__=='__main__':unittest.main()
