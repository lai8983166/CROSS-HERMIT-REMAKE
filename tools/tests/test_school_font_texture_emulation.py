import json
import unittest
from copy import deepcopy
from tools.school_font_texture import ROOT, DEBUG_TARGET
from tools.school_font_texture_verification import verify_report


class RequirementsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-texture-requirements-v1-20261018.json').read_text(encoding='utf-8'))

    def test_complete_original_requirements_return_to_creation(self):
        self.assertEqual(verify_report(self.report)['native_calls_each'], 6)

    def test_fresh_native_requirements_use_real_interfaces(self):
        from tools.school_font_texture_emulation import generate
        self.assertFalse(verify_report(generate('requirements'))['texture_created'])

    def test_debug_format_caps_native_ABI_pending_and_owner_corruptions_refused(self):
        changes = [lambda c: c['requirements']['before_cpu'].update(EIP=0),
                   lambda c: c['requirements']['entries'][1].update(edx=0),
                   lambda c: c['requirements']['returns'][0].update(eax=0),
                   lambda c: c['requirements']['api_calls'][0]['result'].update(return_value_defined=True),
                   lambda c: c['requirements']['api_calls'][0]['result'].update(eax=0),
                   lambda c: c['requirements']['api_calls'][2]['result'].update(hex='00'*212),
                   lambda c: c['requirements']['api_calls'][4]['request'].update(usage=1),
                   lambda c: c['requirements']['api_calls'][4]['result'].update(hr=0),
                   lambda c: c['requirements']['api_calls'][6]['result'].update(count=1),
                   lambda c: c['requirements']['pending'].update(first_instruction_executed=True),
                   lambda c: c['requirements']['cpu'].update(ESP=0),
                   lambda c: c['requirements']['state']['owner'].update(sha256='0'*64),
                   lambda c: c['requirements']['state'].update(image_sha256='0'*64)]
        for index, change in enumerate(changes):
            with self.subTest(change=index):
                bad = deepcopy(self.report)
                change(bad['cases'][0])
                with self.assertRaises(ValueError):
                    verify_report(bad)

    def test_rehashed_inherited_debug_trap_corruption_refused(self):
        from tools.school_device_init_verification import unpack
        from tools.school_renderer_init_emulation import buffer_evidence
        bad = deepcopy(self.report)
        page = next(r for r in bad['cases'][0]['requirements']['state']['foreign_maps'] if r['pointer'] == DEBUG_TARGET & ~4095)
        raw = bytearray(unpack(page))
        raw[DEBUG_TARGET & 4095] ^= 1
        page.update(buffer_evidence(bytes(raw)))
        with self.assertRaises(ValueError):
            verify_report(bad)


class TextureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-texture-native-v1-20261018.json').read_text(encoding='utf-8'))

    def test_original_texture_surface_and_cache_return_to_sprite_entry(self):
        self.assertTrue(verify_report(self.report)['texture_created'])

    def test_fresh_native_texture_and_surface_with_owned_reference_lifetime(self):
        from tools.school_font_texture_emulation import generate
        self.assertEqual(verify_report(generate('texture'))['actual_texture_calls_each'], 20)

    def test_actual_resources_pending_sprite_full_state_and_cleanup_corruptions_refused(self):
        changes = [lambda c: c['texture']['before_cpu'].update(ESP=0),
                   lambda c: c['texture']['api_calls'][9]['args'].__setitem__(3, 7),
                   lambda c: c['texture']['api_calls'][9]['result'].update(hr=-1),
                   lambda c: c['texture']['api_calls'][10]['request'].update(level=1),
                   lambda c: c['texture']['api_calls'][10]['result']['inspection'].update(native_requested=True),
                   lambda c: c['texture']['api_calls'][10]['result']['inspection']['result'].update(hex='00'*32),
                   lambda c: c['texture']['pending']['args'].__setitem__(1, 0),
                   lambda c: c['texture']['pending'].update(first_instruction_executed=True),
                   lambda c: c['texture']['cpu'].update(EDX=0),
                   lambda c: c['texture']['returns'][-1].update(eax=1),
                   lambda c: c['texture']['state'].update(SEH=0),
                   lambda c: c['texture'].update(sprite_body_executed=True),
                   lambda c: c['texture'].update(font_initialization_complete=True),
                   lambda c: c['device_cleanup'].update(texture_release_count=1),
                   lambda c: c['device_cleanup'].update(extra_reference_release_counts=[0]),
                   lambda c: c['device_trace'][-2]['reply'].update(id=0)]
        for index, change in enumerate(changes):
            with self.subTest(change=index):
                bad = deepcopy(self.report)
                change(bad['cases'][0])
                with self.assertRaises(ValueError):
                    verify_report(bad)

    def test_rehashed_texture_cache_fields_padding_and_guards_refused(self):
        from tools.school_device_init_verification import unpack
        from tools.school_renderer_init_emulation import buffer_evidence
        for index, offsets in ((0, (4095, 4108, 4168, 4176, 12287)),
                               (1, (4095, 4108, 4112, 4144, 4180, 4272, 12287))):
            for offset in offsets:
                with self.subTest(heap=index, offset=offset):
                    bad = deepcopy(self.report)
                    row = bad['cases'][0]['texture']['heaps'][index]
                    raw = bytearray(unpack(row))
                    raw[offset] ^= 1
                    row.update(buffer_evidence(bytes(raw)))
                    with self.assertRaises(ValueError):
                        verify_report(bad)
