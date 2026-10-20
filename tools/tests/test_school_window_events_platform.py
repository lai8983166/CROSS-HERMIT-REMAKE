import json
import unittest
from tools.school_window_events_platform import *
from tools.school_window_events import windowpos
from tools.school_window_events_emulation import generate
from tools.school_window_class import NAME_BYTES,creation_args
from tools.tests.test_school_window_class_platform import complete_class


class PlatformTests(unittest.TestCase):
    def test_real_WINDOWPOS_and_scalar_protocol(self):
        report=generate()
        for c in report['cases']:
            self.assertEqual([n['setup']['packet']['message'] for n in c['callbacks']],[129,131,1,5,3,24,70])
            packet=c['callbacks'][-1]['setup']['packet'];self.assertEqual(packet['data_kind'],'WINDOWPOS')
            fields=windowpos(bytes.fromhex(packet['data_hex']),packet['hwnd'])
            self.assertEqual(fields['flags'],0x43)
            call=c['callbacks'][-1]['platform_calls'][-1]
            self.assertEqual(call['result']['before_hex'],packet['data_hex'])
            self.assertEqual(call['result']['after_hex'],packet['data_hex'])
            self.assertEqual(call['result']['host_args'],[packet[k] for k in ('hwnd','message','wParam','lParam')])
            pending=c['pending_callback']['packet'];self.assertEqual(pending['message'],70)
            self.assertEqual(windowpos(bytes.fromhex(pending['data_hex']),pending['hwnd'])['flags'],3)
            self.assertTrue(c['platform_abort']['owned_process_exited']);self.assertIsNone(c['platform_cleanup'])

    def test_refuses_early_foreign_creation_and_inactive_default_context(self):
        with EventsPlatform() as p:
            with self.assertRaises(ValueError):p.request('create_window',args=creation_args(p.module))
            b=complete_class(p);p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            for index in (1,3,6,10,11):
                a=creation_args(p.module);a[index]^=1
                with self.subTest(index=index),self.assertRaises(ValueError):p.request('create_window',args=a)
            with self.assertRaises(ValueError):p.request('default_window',callback_id=1,args=[0,70,0,0])
        self.assertTrue(p.cleanup['all_owned_resources_released']);self.assertEqual(p.cleanup['unregistration_calls'],1)

    def test_immutable_x86_helper_and_actual_system_resource_provenance(self):
        pin=json.loads((ROOT/'analysis/school-window-events-platform-v1-20261020.json').read_text(encoding='utf8'))
        self.assertEqual(pin['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER)))
        with EventsPlatform() as p:self.assertEqual(p.provenance,pin['system_modules'])
        self.assertTrue(p.cleanup['all_owned_resources_released'])


if __name__=='__main__':unittest.main()
