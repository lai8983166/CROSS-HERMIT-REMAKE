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

class FontReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-cache-return-v1-20261018.json').read_text(encoding='utf-8'))

    def test_original_cache_GDI_and_first_font_return_store(self):
        self.assertTrue(verify_report(self.report)['first_static_font_completed'])

    def test_fresh_original_font_factories_with_real_GDI_and_device_references(self):
        from tools.school_font_cache_emulation import generate
        self.assertEqual(verify_report(generate('font'))['cases'], 2)

    def test_GDI_header_LOGFONT_returns_owner_boundary_and_lifetime_corruptions_refused(self):
        changes = [lambda c: c['font_return']['before_cpu'].update(ESP=0),
                   lambda c: c['font_return']['gdi_calls'][1]['request'].update(header_hex='00'*40),
                   lambda c: c['font_return']['gdi_calls'][1]['result'].update(bits=0),
                   lambda c: c['font_return']['gdi_calls'][5]['args'].__setitem__(1, 0),
                   lambda c: c['font_return']['gdi_calls'][6]['request'].update(logfont_hex='00'*60),
                   lambda c: c['font_return']['gdi_calls'][6]['result']['inspection'].update(native_requested=True),
                   lambda c: c['font_return']['device_calls'][0]['result'].update(count=4),
                   lambda c: c['font_return']['returns'][3].update(return_va='0x0'),
                   lambda c: c['font_return']['cpu'].update(EAX=0),
                   lambda c: c['font_return']['output_slot'].update(value=0),
                   lambda c: c['font_return']['pending'].update(first_instruction_executed=True),
                   lambda c: c['font_return'].update(full415F50_returned=True),
                   lambda c: c['font_return'].update(DIB_bits_target_read=True),
                   lambda c: c['platform_cleanup'].update(cache_selection_restored=False),
                   lambda c: c['device_cleanup'].update(extra_reference_release_counts=[2, 1]),
                   lambda c: c['platform_trace'][-2]['reply'].update(id=0)]
        for index, change in enumerate(changes):
            with self.subTest(change=index):
                bad = deepcopy(self.report)
                change(bad['cases'][0])
                with self.assertRaises(ValueError):
                    verify_report(bad)

    def test_rehashed_complete_font_cache_sprite_and_owner_corruptions_refused(self):
        from tools.school_device_init_verification import unpack
        from tools.school_renderer_init_emulation import buffer_evidence
        for index, offsets in ((0, (4104, 4108, 4140, 4166, 4168, 4172)),
                               (1, (4204, 4216, 4248, 4252, 4256)), (2, (4120, 4124, 4128))):
            for offset in offsets:
                bad = deepcopy(self.report)
                row = bad['cases'][0]['font_return']['heaps'][index]
                raw = bytearray(unpack(row))
                raw[offset] ^= 1
                row.update(buffer_evidence(bytes(raw)))
                with self.assertRaises(ValueError):
                    verify_report(bad)
        bad = deepcopy(self.report)
        row = bad['cases'][0]['font_return']['state']['owner']
        raw = bytearray(unpack(row))
        raw[0xB270:0xB274] = bytes(4)
        row.update(buffer_evidence(bytes(raw)))
        with self.assertRaises(ValueError):
            verify_report(bad)
