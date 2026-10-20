import json
import struct
import unittest
from tools.school_window_create_platform import *
from tools.school_window_create import rectangle,geometry
from tools.school_window_create_emulation import generate
from tools.school_window_class import NAME_BYTES,creation_args
from tools.tests.test_school_window_class_platform import complete_class


class PlatformTests(unittest.TestCase):
    def test_real_client_RECT_before_after_and_ordinary_creation_struct_capture(self):
        r=generate()
        for c in r['cases']:
            self.assertEqual([n['setup']['packet']['message'] for n in c['callbacks']],[129,131,1])
            client=c['callbacks'][1];packet=client['setup']['packet'];self.assertEqual(packet['data_kind'],'RECT')
            before=bytes.fromhex(packet['data_hex']);self.assertEqual(rectangle(before,packet['wParam']),[16,16,1040,784])
            call=client['platform_calls'][-1];self.assertEqual(call['result']['before_hex'],before.hex())
            self.assertEqual(rectangle(bytes.fromhex(call['result']['after_hex']),0),[16,16,1040,784]);self.assertEqual(call['result']['result'],0)
            create=c['callbacks'][2]['setup']['packet'];self.assertEqual(create['data_kind'],'CREATESTRUCTA')
            self.assertEqual(len(bytes.fromhex(create['data_hex'])),48)
            self.assertTrue(c['platform_abort']['owned_process_exited']);self.assertIsNone(c['platform_cleanup'])

    def test_refuses_early_foreign_creation_and_inactive_default_context(self):
        with CreatePlatform() as p:
            with self.assertRaises(ValueError):p.request('create_window',args=creation_args(p.module))
            b=complete_class(p);p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            for index in (1,3,6,10,11):
                a=creation_args(p.module);a[index]^=1
                with self.subTest(index=index),self.assertRaises(ValueError):p.request('create_window',args=a)
            with self.assertRaises(ValueError):p.request('default_window',callback_id=1,args=[0,131,0,0])
        self.assertTrue(p.cleanup['all_owned_resources_released']);self.assertEqual(p.cleanup['unregistration_calls'],1)

    def test_immutable_new_x86_helper_and_actual_system_resource_provenance(self):
        pin=json.loads((ROOT/'analysis/school-window-create-platform-v1-20261020.json').read_text(encoding='utf8'))
        self.assertEqual(pin['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER)))
        with CreatePlatform() as p:self.assertEqual(p.provenance,pin['system_modules'])
        self.assertTrue(p.cleanup['all_owned_resources_released'])


if __name__=='__main__':unittest.main()
