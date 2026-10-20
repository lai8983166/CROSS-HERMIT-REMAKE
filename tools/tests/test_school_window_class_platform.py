import copy
import json
import unittest
from tools.school_window_class import class_bytes,NAME_BYTES
from tools.school_window_class_platform import *
from tools.tests.test_school_window_module_platform import ready


def complete_class(p):
    ready(p);icons=[p.request('load_icon',module=p.module,id_value=157)['result'] for _ in range(2)]
    cursor=p.request('load_cursor',module=0,id_value=32512)['result'];brush=p.request('stock_brush',id_value=4)['result']
    return class_bytes(p.module,icons,cursor,brush)


class PlatformTests(unittest.TestCase):
    def test_real_class_registration_both_queries_explicit_unregister_and_dormant_callback(self):
        with ClassPlatform() as p:
            b=complete_class(p);r=p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            self.assertEqual(verify_registration(r,b)['pointer_translations'],2)
            u=p.request('unregister_class',atom=r['atom'],module=p.module);verify_unregistration(u,r['atom'])
            self.assertEqual(p.callback_packets,[])
        self.assertEqual(p.cleanup['registration_calls'],1);self.assertEqual(p.cleanup['inspection_calls'],4)
        self.assertEqual(p.cleanup['unregistration_calls'],1);self.assertEqual(p.cleanup['callback_calls'],0)
        self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_refuses_early_changed_class_foreign_unregister_duplicate_and_creation(self):
        with ClassPlatform() as p:
            with self.assertRaises(ValueError):p.request('register_class',class_hex='00'*48,class_name_hex=NAME_BYTES.hex())
            b=complete_class(p)
            for offset in (0,8,20,24,36,40,44):
                changed=bytearray(b);changed[offset]^=1
                with self.subTest(offset=offset),self.assertRaises(ValueError):p.request('register_class',class_hex=changed.hex(),class_name_hex=NAME_BYTES.hex())
            with self.assertRaises(ValueError):p.request('register_class',class_hex=b.hex(),class_name_hex=b'Other\0'.hex())
            r=p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex());verify_registration(r,b)
            with self.assertRaises(ValueError):p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            with self.assertRaises(ValueError):p.request('unregister_class',atom=r['atom'],module=0)
            with self.assertRaises(ValueError):p.request('unregister_class',atom=0,module=p.module)
            with self.assertRaises(ValueError):p.request('create_window')
        verify_unregistration(p.cleanup['unregistration'],r['atom'])

    def test_partial_cleanup_and_immutable_x86_build_and_resources(self):
        pin=json.loads((ROOT/'analysis/school-window-class-platform-v1-20261020.json').read_text(encoding='utf8'))
        self.assertEqual(pin['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER)))
        for stage in (0,1,2):
            with ClassPlatform() as p:
                self.assertEqual(p.provenance,pin['system_modules'])
                if stage:b=complete_class(p)
                if stage==2:r=p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            self.assertEqual(p.cleanup['registration_calls'],int(stage==2));self.assertEqual(p.cleanup['unregistration_calls'],int(stage==2))
            self.assertEqual(p.cleanup['callback_calls'],0);self.assertTrue(p.cleanup['all_owned_resources_released'])
            self.assertEqual(p.cleanup['shared_icons_destroyed'],0);self.assertFalse(p.cleanup['shared_cursor_destroyed'] or p.cleanup['stock_brush_deleted'])

    def test_registration_verifier_refuses_pointer_atom_query_or_lifetime_corruption(self):
        with ClassPlatform() as p:
            b=complete_class(p);original=p.request('register_class',class_hex=b.hex(),class_name_hex=NAME_BYTES.hex())
            for mutation in ('callback','third','atom','query','shared','callback_count'):
                r=copy.deepcopy(original)
                if mutation=='callback':r['pointer_translations'][0]['guest']=0
                elif mutation=='third':r['pointer_translations'].append(dict(offset=20,guest=p.module,host=p.module))
                elif mutation=='atom':r['atom']^=1
                elif mutation=='query':r['by_atom']['class_name']='Other'
                elif mutation=='shared':r['host_hex']='00'*48
                else:r['callback_calls']=1
                with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_registration(r,b)


if __name__=='__main__':unittest.main()
