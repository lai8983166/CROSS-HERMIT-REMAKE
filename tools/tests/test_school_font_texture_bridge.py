import json
import os
import struct
import unittest
from pathlib import Path
import pefile
from tools.school_font_texture_bridge import *


class BridgeTests(unittest.TestCase):
    def test_fixed_x86_build_and_parent_source_identity(self):
        report = json.loads((ROOT/'analysis/school-font-texture-bridge-v1-20261018.json').read_text(encoding='utf-8'))
        for key, path in (('source_sha256', SOURCE), ('helper_sha256', HELPER), ('compiler_sha256', COMPILER)):
            self.assertEqual(report['build'][key], sha(path.read_bytes()))
        self.assertEqual(machine(HELPER), 0x14C)
        parent = json.loads((ROOT/'analysis/school-font-startup-bridge-v1-20261018.json').read_text())['build']
        self.assertEqual(parent['source_sha256'], sha((ROOT/'tools/school_font_device_bridge.cs').read_bytes()))
        with self.assertRaises(ValueError):
            build()

    def test_live_debug_factory_texture_surface_and_complete_cleanup(self):
        result = probe()
        self.assertEqual(result['texture']['hr'], 0)
        desc = result['surface']['inspection']
        self.assertFalse(desc['native_requested'])
        self.assertEqual(struct.unpack('<8I', bytes.fromhex(desc['result']['hex'])), (21, 1, 512, 0, 4096, 0, 64, 16))
        runtime = pefile.PE(str(Path(os.environ['WINDIR'])/'SysWOW64/d3d8.dll'))
        rva = next(s.address for s in runtime.DIRECTORY_ENTRY_EXPORT.symbols if s.name == b'DebugSetMute')
        for row in result['trace']:
            if row['request']['op'] == 'debug_mute':
                value = row['reply']['result']
                self.assertEqual(value['export_pointer']-value['module_pointer'], rva)
                self.assertFalse(value['return_value_defined'])
        self.assertEqual(result['cleanup'], dict(texture_surface_release_count=1, texture_release_count=0,
                         extra_reference_release_counts=[1], device_release_count=0, factory_release_count=0,
                         window_destroyed=True, all_owned_resources_released=True))

    def test_foreign_bad_size_level_and_order_refused(self):
        def run(bridge):
            device, factory = setup(bridge)
            for op, args in [('debug_mute', dict(value=0)), ('texture_factory', dict(pointer=1)),
                             ('texture_factory_release', dict(pointer=factory)),
                             ('texture_create', dict(pointer=device, width=65, height=16, levels=1, usage=512, format=21, pool=0))]:
                with self.assertRaises(ValueError):
                    bridge.request(op, **args)
            tex = bridge.request('texture_create', pointer=device, width=64, height=16, levels=1, usage=512, format=21, pool=0)
            with self.assertRaises(ValueError):
                bridge.request('texture_surface', pointer=tex['texture']['pointer'], level=1)
        result = owned_run(run)
        self.assertEqual(result['cleanup']['texture_release_count'], 0)
        self.assertTrue(result['cleanup']['all_owned_resources_released'])

    def test_partial_borrowed_factory_reference_is_released(self):
        def run(bridge):
            device, factory = setup(bridge)
            bridge.request('debug_mute', value=1)
            actual = bridge.request('texture_factory', pointer=device)
            self.assertEqual(actual['factory']['pointer'], factory)
        result = owned_run(run)
        self.assertEqual(result['cleanup']['borrowed_factory_release_count'], 2)
        self.assertTrue(result['cleanup']['all_owned_resources_released'])
