"""Synthetic schemas and recorded failures only; never native input evidence."""
import copy
import gzip
import json
import struct
import unittest
from unittest.mock import patch
from devtools import terminal_host_menu_verification as v
from devtools.tests import test_terminal_menu_handoff_verification as old
from devtools.tests import test_terminal_school_handoff_verification as school
from devtools.tests.test_terminal_host_desktop import healthy


class HostVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        old.MenuVerificationTests.setUpClass()
        cls.fixture=old.MenuVerificationTests()
        cls.raw=cls.fixture.raw

    def input(self):
        p,game,hwnd,worker=self.fixture.synthetic_input()
        receipt=p['mouse_controller']['receipt'];a=receipt['action'];wall=10**12
        feedback=school.SchoolHandoffVerificationTests.feedback_action(None)
        # Deliberately synthetic clocks, no claim these are captured OS events.
        feedback.pop('down_wall_time_ns')
        a.update(feedback)
        a.update(screenshot_required=False,accepted=False,release_guard_failed=False,
                 release_guard_error=None,down_wall_time_ns=wall+400_000_000,
                 up_wall_time_ns=wall+480_000_000)
        geometry=a['click_geometry'];geometry.update(point_window=hwnd,coordinate_mode=1)
        def cursor(s,offset):
            s['geometry']=copy.deepcopy(geometry)
            s['wall_time_ns']=wall+offset;s['monotonic_ns']=offset+1_000_000_000
        for i,move in enumerate(a['moves']):
            move['geometry']=copy.deepcopy(geometry)
            for j,s in enumerate(move['settling']):cursor(s,(50+i*100+j*25)*1_000_000)
        for j,s in enumerate(a['before_click_settling']):cursor(s,(250+j*25)*1_000_000)
        cursor(a['pre_down_cursor'],350_000_000)
        a['button_edge_checks']=[]
        for flags,offset in ((2,405_000_000),(4,475_000_000)):
            s=copy.deepcopy(a['pre_down_cursor']);cursor(s,offset)
            a['button_edge_checks'].append(dict(flags=flags,guard=copy.deepcopy(a['guard_observations'][0]),cursor=s))
        receipt['after_elapsed']=300.6
        for s,ms in zip(receipt['input_samples'],(0,410,440,490,550)):
            s['wall_time_ns']=wall+ms*1_000_000;s['elapsed']=300+ms/1000
        row=next(r for r in p['samples'] if any(f['tid']==worker['thread_id'] and
            any(c['return_va']==0x45F065 for c in f['chain']) for f in r['frames']))
        receipt['ready_start_sample']=copy.deepcopy(row);receipt['ready_start_sample']['elapsed']=298.9
        receipt['ready_decision_sample']=copy.deepcopy(row);receipt['ready_decision_sample']['elapsed']=299.95
        return p,game,hwnd,worker

    def verify(self,fixture):
        p,game,hwnd,worker=fixture
        return v.verify_input(p,self.raw,game,hwnd,worker,check_disk=False)

    def mutate_action(self,fn):
        f=self.input();fn(f[0]['mouse_controller']['receipt']['action'])
        with self.assertRaises((ValueError,KeyError)):self.verify(f)

    def test_synthetic_input_verified_without_mutating_original(self):
        f=self.input();before=copy.deepcopy(f);r=self.verify(f)
        self.assertEqual(f,before);self.assertTrue(r['input_edges_observed'])
        self.assertTrue(r['button_edges_independently_verified'])
        self.assertEqual(r['feedback_corrections'][0]['error'],[0,1])

    def test_missing_reordered_or_extra_button_edges_rejected(self):
        for fn in (lambda a:a.pop('button_edge_checks'),lambda a:a['button_edge_checks'].reverse(),
                   lambda a:a['button_edge_checks'].append(a['button_edge_checks'][1])):
            self.mutate_action(fn)

    def test_failed_release_cannot_claim_success(self):
        for name,val in (('release_guard_failed',True),('release_guard_error','lost focus'),('accepted',True)):
            self.mutate_action(lambda a:a.update({name:val}))

    def test_os_frozen_and_live_cursor_all_required(self):
        for name in ('os_game_point','game_point','screen_point'):
            self.mutate_action(lambda a:a['button_edge_checks'][1]['cursor'][name].__setitem__(0,319))
        self.mutate_action(lambda a:a['button_edge_checks'][1]['guard'].update(cursor_hex='00'*8))

    def test_guard_source_and_generation_tampering_rejected(self):
        self.mutate_action(lambda a:a['button_edge_checks'][1]['guard']['code'].pop())
        self.mutate_action(lambda a:a['button_edge_checks'][1]['guard'].update(selector_pointer=123))
        self.mutate_action(lambda a:a['button_edge_checks'][1]['guard'].update(coordinate_mode_hex='00000000'))
        def changed(a,offset,value):
            g=a['button_edge_checks'][1]['guard'];b=bytearray.fromhex(g['head_hex'])
            struct.pack_into('<I',b,offset,value);g['head_hex']=b.hex()
        for offset in (0x1C,0x20,0x24):self.mutate_action(lambda a:changed(a,offset,1))

    def test_countdown_low_and_restart_rejected(self):
        for value in (299,3001,3660):
            def mutate(a):
                g=a['button_edge_checks'][1]['guard'];b=bytearray.fromhex(g['selector_hex'])
                struct.pack_into('<I',b,0,value);g['selector_hex']=b.hex()
            self.mutate_action(mutate)

    def test_geometry_feedback_and_clock_tampering_rejected(self):
        self.mutate_action(lambda a:a['moves'][1]['normalized'].__setitem__(1,23182))
        self.mutate_action(lambda a:a['button_edge_checks'][1]['cursor'].update(monotonic_ns=1))
        self.mutate_action(lambda a:a['button_edge_checks'][0]['cursor'].update(wall_time_ns=a['down_wall_time_ns']-1))
        self.mutate_action(lambda a:a['moves'][1]['settling'][0].update(wall_time_ns=1))

    def test_cursor_history_cannot_predate_input_or_shift_between_clocks(self):
        def old(a):
            for m in a['moves']:
                for s in m['settling']:
                    s['wall_time_ns']-=1_000_000_000;s['monotonic_ns']-=1_000_000_000
        self.mutate_action(old)
        def drift(a):
            for m in a['moves']:
                for s in m['settling']:s['monotonic_ns']-=50_000_000
        self.mutate_action(drift)

    def test_raw_release_required_even_when_submission_succeeds(self):
        f=self.input();s=f[0]['mouse_controller']['receipt']['input_samples'][3]
        b=bytearray.fromhex(s['mouse_hex']);struct.pack_into('<I',b,0x30,0);s['mouse_hex']=b.hex()
        with self.assertRaisesRegex(ValueError,'real original'):self.verify(f)

    def test_readiness_stale_or_too_short_and_reacquire_rejected(self):
        for key,value in (('ready_start_sample',299.5),('ready_decision_sample',298)):
            f=self.input();f[0]['mouse_controller']['receipt'][key]['elapsed']=value
            with self.assertRaises(ValueError):self.verify(f)
        f=self.input();f[0]['mouse_controller']['receipt']['activation']['operations']=[dict(name='SetForegroundWindow',result=True)]
        with self.assertRaisesRegex(ValueError,'reacquire'):self.verify(f)

    def outcome(self):
        report=dict(host_preflight=dict(successor_observed=True),probe=dict(
            workers=[dict(vtable=v.menu.NEW_GAME,exit=dict(code=0,wait_status=0,before_WM_CLOSE=True,elapsed=301))],
            stop_reason='controller_finished_observation',mouse_controller=dict(receipt=dict(after_elapsed=300))))
        result=dict(native_menu_handoff_observed=True,menu_ready_one_second_independently_sampled=True,
            successor_observations=[dict(vtable=v.menu.ADV,TLS_verified=True,elapsed=302)])
        return report,result

    def test_outcome_needs_original_new_game_retirement_then_adv(self):
        report,result=self.outcome();r=v.verify_outcome(report,result)
        self.assertFalse(r['accepted']);self.assertTrue(r['host_menu_observation_verified'])
        for change in (lambda p,r:r.update(native_menu_handoff_observed=False),
                       lambda p,r:r.update(menu_ready_one_second_independently_sampled=False),
                       lambda p,r:p['probe']['workers'][0]['exit'].update(code=1),
                       lambda p,r:r['successor_observations'][0].update(vtable=0x5CAA48),
                       lambda p,r:r['successor_observations'][0].update(TLS_verified=False),
                       lambda p,r:r['successor_observations'][0].update(elapsed=299),
                       lambda p,r:r['successor_observations'][0].update(elapsed=321)):
            p,r=self.outcome();change(p,r)
            with self.assertRaises(ValueError):v.verify_outcome(p,r)

    def desktop_fixture(self):
        before=healthy();before['time_ns']=1_000_000_000_000
        after=[copy.deepcopy(before),copy.deepcopy(before)]
        after[0]['time_ns']+=400_000_000_000;after[1]['time_ns']+=401_000_000_000
        report=dict(desktop=before['input_desktop'],host_preflight=dict(deadline_utc=1500,
            implementations=[dict(path='devtools/terminal_host_desktop.py',sha256='a'*64)]),
            probe=dict(mouse_controller=dict(receipt=dict(input_samples=[dict(wall_time_ns=1_100_000_000_000),dict(wall_time_ns=1_200_000_000_000)]))))
        receipt=dict(before=before,after=after,observer_sha256='a'*64,action_error=None,restored=True,checks=[[],[]])
        return report,receipt

    def test_desktop_recomputed_not_trusted_boolean(self):
        p,r=self.desktop_fixture();self.assertTrue(v.verify_desktop(p,r)['restored'])
        r['after'][0]['taskbars'][0]['rect'][1]+=8
        with self.assertRaises(ValueError):v.verify_desktop(p,r)

    def test_desktop_wrong_baseline_observer_time_rejected(self):
        for change in (lambda p,r:r.update(observer_sha256='b'*64),
                       lambda p,r:p['desktop'].update(foreground_pid=99),
                       lambda p,r:r['after'][1].update(time_ns=1_600_000_000_000),
                       lambda p,r:r['after'][1].update(time_ns=r['after'][0]['time_ns'])):
            p,r=self.desktop_fixture();p=copy.deepcopy(p);change(p,r)
            with self.assertRaises(ValueError):v.verify_desktop(p,r)

    def test_original_failed_desktop_can_only_use_same_baseline_recovery(self):
        p,r=self.desktop_fixture();good=copy.deepcopy(r['after'])
        r['after'][0]['taskbars'][0]['rect'][1]+=8
        r['restored']=False;r['checks']=[['taskbar_geometry_changed'],[]]
        for s in good:s['time_ns']+=3_000_000_000
        final=copy.deepcopy(good)
        for s in final:s['time_ns']+=3_000_000_000
        recovery=dict(before=r['before'],restored=True,after=good,checks=[[],[]],
                      final_after=final,final_checks=[[],[]])
        self.assertTrue(v.verify_desktop(p,r,recovery)['recovery_used'])
        for rows in (r['after'],recovery['after'],recovery['final_after']):
            saved=rows[0]['time_ns'];rows[0]['time_ns']=-1
            with self.assertRaises(ValueError):v.verify_desktop(p,r,recovery)
            rows[0]['time_ns']=saved
        recovery['before']=copy.deepcopy(r['before']);recovery['before']['time_ns']+=1
        with self.assertRaises(ValueError):v.verify_desktop(p,r,recovery)

    def test_host_manifest_is_exact_and_old_source_cannot_upgrade(self):
        p=v.ROOT/'analysis/terminal-host-menu-dxgi-v2-20261112.json.gz'
        r=json.loads(gzip.decompress(p.read_bytes()))
        with self.assertRaises((ValueError,KeyError)):v.verify_host_envelope(r)
        valid=dict(probe={},host_preflight=dict(implementations=[v.identity(p) for p in v.HOST_PATHS],
            accepted=False,full_graphics_qualification=False,screenshot_required=False,image_review_wait=False,
            requires_independent_handoff_verification=True,input_mode='original_native_menu_state',
            budget_events=[],deadline_utc=1500,successor_observed=True))
        v.verify_host_envelope(valid)
        for change in (lambda r:r['host_preflight']['implementations'][0].update(sha256='0'*64),
                       lambda r:r['host_preflight'].update(budget_events=[{'reason':'hard_deadline'}]),
                       lambda r:r['probe'].update(collector_story_input_actions=[])):
            changed=copy.deepcopy(valid);change(changed)
            with self.assertRaises(ValueError):v.verify_host_envelope(changed)

    def test_file_dispatch_uses_new_input_verifier(self):
        # Composition only: a sentinel prevents any file/native operation.
        def report(path,digest):
            self.assertIs(report_clone.__globals__['verify_input'],v.verify_input)
            return {'ok':True}
        report_clone=v.bind(v.menu.verify_report,verify_input=v.verify_input)
        self.assertIs(v.bind(v.menu.verify_file,verify_report=report).__globals__['verify_report'],report)


if __name__=='__main__':unittest.main()
