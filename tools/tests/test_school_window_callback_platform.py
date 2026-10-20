import json
import unittest
from tools.school_window_callback_platform import *
from tools.school_window_class import NAME_BYTES,creation_args
from tools.tests.test_school_window_class_platform import complete_class


class PlatformTests(unittest.TestCase):
    def test_genuine_first_callback_is_left_unanswered_and_owned_process_exits(self):
        with CallbackPlatform() as p:
            b=complete_class(p);p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            with self.assertRaises(CallbackBoundary) as caught:p.request('create_window',args=creation_args(p.module))
            packet=caught.exception.packet;self.assertEqual(packet['guest_entry'],0x424980);self.assertEqual(packet['depth'],1)
            self.assertGreater(packet['hwnd'],0);self.assertTrue(p.abort_proof['owned_process_exited'])
            self.assertFalse(p.abort_proof['explicit_cleanup_performed'] or p.abort_proof['CreateWindowExA_return_received'])
            self.assertEqual(p.wire[-1]['value'],packet);self.assertFalse(any(r['direction']=='callback_return' for r in p.wire))
        self.assertTrue(p.closed);self.assertIsNone(p.cleanup)

    def test_refuses_foreign_changed_or_early_creation_and_nested_calls(self):
        with CallbackPlatform() as p:
            with self.assertRaises(ValueError):p.request('create_window',args=creation_args(p.module))
            b=complete_class(p);p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            for index in (0,1,3,4,6,10,11):
                args=creation_args(p.module);args[index]^=1
                with self.subTest(index=index),self.assertRaises(ValueError):p.request('create_window',args=args)
            with self.assertRaises(ValueError):p.request('get_prop',callback_id=1,hwnd=0,name_hex=b'CPP_CLASS\0'.hex())
        self.assertTrue(p.cleanup['all_owned_resources_released']);self.assertEqual(p.cleanup['unregistration_calls'],1)

    def test_fresh_immutable_x86_source_build_and_resource_module(self):
        r=json.loads((ROOT/'analysis/school-window-callback-platform-v1-20261020.json').read_text(encoding='utf8'))
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER)))
        with CallbackPlatform() as p:self.assertEqual(p.provenance,r['system_modules'])
        self.assertTrue(p.cleanup['all_owned_resources_released'])


if __name__=='__main__':unittest.main()
