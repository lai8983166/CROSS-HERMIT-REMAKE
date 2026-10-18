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
