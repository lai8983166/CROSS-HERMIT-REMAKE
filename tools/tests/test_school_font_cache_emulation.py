import json
import unittest
from copy import deepcopy
from tools.school_font_cache import ROOT
from tools.school_font_cache_verification import verify_report


class SpriteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-cache-sprite-v1-20261018.json').read_text(encoding='utf-8'))

    def test_full_original_sprite_returns_to_pending_GDI(self):
        self.assertFalse(verify_report(self.report)['first_static_font_completed'])

    def test_fresh_original_sprite_with_real_device_queries(self):
        from tools.school_font_cache_emulation import generate
        self.assertEqual(verify_report(generate('sprite'))['heap_guard_bytes'], 36864)

    def test_source_alloc_device_buffers_CPU_and_GDI_admission_corruptions_refused(self):
        changes = [lambda c: c['sprite']['before_cpu'].update(EIP=0),
                   lambda c: c['sprite']['allocations'][0]['args'].__setitem__(0, 31),
                   lambda c: c['sprite']['entries'][1].update(sp=0),
                   lambda c: c['sprite']['returns'][-1].update(eax=1),
                   lambda c: c['sprite']['device_calls'][0]['result'].update(count=3),
                   lambda c: c['sprite']['device_calls'][1]['result'].update(hex='00'*212),
                   lambda c: c['sprite']['device_calls'][2]['result'].update(hex='00'*16),
                   lambda c: c['sprite']['pending'].update(platform_call_executed=True),
                   lambda c: c['sprite']['pending']['args'].__setitem__(0, 1),
                   lambda c: c['sprite']['cpu'].update(ESP=0),
                   lambda c: c['sprite']['state'].update(image_sha256='0'*64),
                   lambda c: c['sprite']['state']['foreign_maps'][0].update(sha256='0'*64)]
        for index, change in enumerate(changes):
            with self.subTest(change=index):
                bad = deepcopy(self.report)
                change(bad['cases'][0])
                with self.assertRaises(ValueError):
                    verify_report(bad)

    def test_rehashed_sprite_flags_padding_header_and_guard_corruptions_refused(self):
        from tools.school_device_init_verification import unpack
        from tools.school_renderer_init_emulation import buffer_evidence
        for index, offsets in ((1, (4108, 4208, 4216, 4222, 4260)), (2, (4095, 4096, 4100, 4104, 4120, 4124, 4128, 12287))):
            for offset in offsets:
                bad = deepcopy(self.report)
                row = bad['cases'][0]['sprite']['heaps'][index]
                raw = bytearray(unpack(row))
                raw[offset] ^= 1
                row.update(buffer_evidence(bytes(raw)))
                with self.assertRaises(ValueError):
                    verify_report(bad)
