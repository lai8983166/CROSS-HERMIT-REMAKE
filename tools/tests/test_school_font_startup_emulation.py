import json
import unittest
from copy import deepcopy
from tools.school_font_startup import ROOT
from tools.school_font_startup_verification import verify_report


class InheritedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-startup-inherited-v1-20261018.json').read_text(encoding='utf-8'))

    def test_complete_original_factory_to_actual_missing_node_boundary(self):
        self.assertEqual(verify_report(self.report)['original_factory_calls'], 5)

    def test_fresh_inherited_state_does_not_read_or_patch_missing_node(self):
        from tools.school_font_startup_emulation import generate
        self.assertEqual(verify_report(generate('inherited'))['cases'], 2)

    def test_cache_input_actual_read_CPU_allocations_and_full_memory_corruptions_refused(self):
        changes = [lambda c: c['factory']['declared'].update(initial_head=0),
                   lambda c: c['factory']['pending'].update(target_read=True),
                   lambda c: c['factory']['pending'].update(target_memory_mapped=True),
                   lambda c: c['factory']['cpu'].update(EAX=0),
                   lambda c: c['factory']['allocations'][0]['args'].__setitem__(0, 79),
                   lambda c: c['factory']['entries'][1].update(sp=0),
                   lambda c: c['factory']['returns'][0].update(eax=0),
                   lambda c: c['factory']['state'].update(image_sha256='0'*64),
                   lambda c: c['factory']['state']['owner'].update(sha256='0'*64),
                   lambda c: c['factory']['heaps'][0].update(sha256='0'*64),
                   lambda c: c['factory']['heaps'][1].update(sha256='0'*64),
                   lambda c: c['factory']['output_slot'].update(value=0)]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                bad = deepcopy(self.report)
                change(bad['cases'][0])
                with self.assertRaises(ValueError):
                    verify_report(bad)

    def test_authority_build_identity_and_cleanup_corruptions_refused(self):
        for key in ('retained_VM_advanced', 'original_IAT_changed', 'game_helpers_stubbed'):
            bad = deepcopy(self.report)
            bad[key] = True
            with self.assertRaises(ValueError):
                verify_report(bad)
        bad = deepcopy(self.report)
        bad['device_build']['helper_sha256'] = '0'*64
        with self.assertRaises(ValueError):
            verify_report(bad)
        bad = deepcopy(self.report)
        bad['cases'][0]['device_cleanup']['device_release_count'] = 1
        with self.assertRaises(ValueError):
            verify_report(bad)


class EmptyCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-startup-empty-v1-20261018.json').read_text(encoding='utf-8'))

    def test_explicit_empty_cache_original_construction_to_texture_requirements(self):
        self.assertEqual(verify_report(self.report)['original_factory_calls'], 9)

    def test_fresh_native_empty_cache_with_live_device_references(self):
        from tools.school_font_startup_emulation import generate
        self.assertEqual(verify_report(generate('empty'))['heap_guard_bytes'], 24576)

    def test_device_cache_outputs_original_texture_args_trace_and_authority_refused(self):
        changes = [lambda c: c['factory']['declared'].update(empty_cache_explicitly_declared=False),
                   lambda c: c['factory']['cache_calls'][0]['result'].update(count=1),
                   lambda c: c['factory']['cache_calls'][1]['result'].update(hex='00'*212),
                   lambda c: c['factory']['cache_calls'][2]['result'].update(hex='00'*16),
                   lambda c: c['factory']['cache_calls'][1]['args'].__setitem__(1, 0),
                   lambda c: c['factory']['pending']['args'].__setitem__(4, 123),
                   lambda c: c['factory']['pending'].update(first_instruction_executed=True),
                   lambda c: c['factory']['cpu'].update(ESP=0),
                   lambda c: c['factory']['visited'].append(0x52755E),
                   lambda c: c['factory'].update(texture_body_executed=True),
                   lambda c: c['factory'].update(font_initialization_complete=True),
                   lambda c: c['device_cleanup'].update(extra_reference_release_counts=[0]),
                   lambda c: c['device_trace'][-2]['reply'].update(id=0)]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                bad = deepcopy(self.report)
                change(bad['cases'][0])
                with self.assertRaises(ValueError):
                    verify_report(bad)

    def test_rehashed_heap_fields_padding_and_guard_corruptions_refused(self):
        from tools.school_device_init_verification import unpack
        from tools.school_renderer_init_emulation import buffer_evidence
        for index, offsets in ((0, (4095, 4096, 4108, 4168, 4176, 12287)),
                               (1, (4095, 4096, 4100, 4176, 4208, 4268, 4272, 12287))):
            for offset in offsets:
                with self.subTest(heap=index, offset=offset):
                    bad = deepcopy(self.report)
                    row = bad['cases'][0]['factory']['heaps'][index]
                    raw = bytearray(unpack(row))
                    raw[offset] ^= 1
                    row.update(buffer_evidence(bytes(raw)))
                    with self.assertRaises(ValueError):
                        verify_report(bad)
