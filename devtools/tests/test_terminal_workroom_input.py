from devtools.tests.test_terminal_owned_mouse import inert_cursor
import copy
import gzip
import hashlib
import json
from pathlib import Path
import struct
import unittest
from devtools import terminal_workroom_input as workroom
from devtools.tests.test_terminal_menu_input import Api


class WorkroomInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path('analysis/terminal-menu-handoff-v6-20261107.json.gz');data=path.read_bytes()
        if hashlib.sha256(data).hexdigest()!='af9e1d76f665ab06e913288b3e487f25d4777cd27acd98e6828bb1d991de7533':
            raise ValueError('fixed observed workroom source')
        cls.row=json.loads(gzip.decompress(data))['probe']['samples'][-1]
    def test_real_observed_selection_wait_is_ready(self):self.assertTrue(workroom.ready(self.row))
    def test_fade_or_missing_tls_or_pending_event_refused(self):
        for change in ('state','TLS','event','stack','task'):
            r=copy.deepcopy(self.row)
            if change=='state':
                h=bytearray.fromhex(r['tasks'][0]['header_hex']);struct.pack_into('<H',h,0x30,3);r['tasks'][0]['header_hex']=h.hex()
            elif change=='TLS':del r['tasks'][0]['TLS']
            elif change=='event':r['MAIN_event_hex']='0100000006000000'
            elif change=='task':r['tasks'].append(copy.deepcopy(r['tasks'][0]))
            else:
                for f in r['frames']:
                    f['chain']=[x for x in f['chain']if x['return_va']!=0x49FF57]
            self.assertFalse(workroom.ready(r),change)
    def test_disabled_without_explicit_authorization(self):
        with self.assertRaises(PermissionError):workroom.owned_workroom_exit(None,None)
    def api(self):
        api=Api();api.xy=workroom.TARGET
        api.geometry=lambda target:dict(screen_target=list(target),virtual_desktop=[0,0,1024,768])
        return inert_cursor(api)
    def test_exact_exit_click_and_release(self):
        api=self.api();r=workroom.guarded_click(api,lambda:None,lambda _:None)
        self.assertEqual(api.flags,[2,4]);self.assertEqual(r['target'],[917,741]);self.assertTrue(r['released'])
    def test_final_geometry_refusal_before_button_down(self):
        api=self.api()
        def fail(_):raise ValueError('occluded')
        api.geometry=fail;r=workroom.guarded_click(api,lambda:None,lambda _:None)
        self.assertEqual(api.flags,[]);self.assertFalse(r['down_submitted'])
    def test_release_after_exception_during_hold(self):
        api=self.api()
        def fail(delay):
            if delay==.08:raise ValueError('interrupted')
        r=workroom.guarded_click(api,lambda:None,fail)
        self.assertEqual(api.flags,[2,4]);self.assertTrue(r['released']);self.assertIsNotNone(r['error'])


if __name__=='__main__':unittest.main()
