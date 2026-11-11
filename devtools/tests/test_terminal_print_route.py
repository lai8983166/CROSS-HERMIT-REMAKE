import copy
import unittest
from unittest.mock import patch
from devtools import terminal_print_route as route
from devtools import terminal_host_menu_preflight_v2 as host


class PrintRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw,cls.record=route.authenticated()

    def test_both_original_messages_stop_before_default_proc(self):
        for message in (0x317,0x318):
            result=route.route(self.raw,self.record,message)
            self.assertEqual(result['stop_before']['pc'],0x424AFD)
            self.assertEqual(result['stop_before']['arguments'][1],message)
            self.assertEqual(result['original_dispatch'],['0x424980','0x450d30','0x4272e0','0x424a90'])
            self.assertFalse(result['native_OS_executed'])
            self.assertFalse(result['pixels_recovered'])

    def test_source_tamper_rejected(self):
        raw=bytearray(self.raw);raw[0x450D30-0x400000]^=1
        with self.assertRaisesRegex(ValueError,'image changed'):route.route(bytes(raw),self.record,0x318)

    def test_mismatched_owner_rejected(self):
        r=copy.deepcopy(self.record);r['lifecycle']['ready']['window']['property']+=4
        with self.assertRaisesRegex(ValueError,'owner'):route.route(self.raw,r,0x318)

    def test_subclass_state_cannot_be_ignored(self):
        r=copy.deepcopy(self.record);body=bytearray.fromhex(r['lifecycle']['ready']['main']['hex'])
        body[8]=1;r['lifecycle']['ready']['main']['hex']=body.hex()
        with self.assertRaisesRegex(ValueError,'route changed'):route.route(self.raw,r,0x318)

    def test_unqualified_backend_never_reaches_desktop_or_game(self):
        with patch.object(host.desktop,'guarded_run',side_effect=AssertionError('no desktop action')):
            with self.assertRaisesRegex(RuntimeError,'unqualified'):
                host.run(None,0,True)


if __name__=='__main__':unittest.main()
