import json
import unittest
from copy import deepcopy
from tools.school_font_slots import ROOT, SLOT
from tools.school_font_slots_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class ConstructorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-slots-constructor-v1-20261018.json').read_text())

    def test_original_constructor_and_caller_binding(self):
        self.assertEqual(verify_report(self.report)['full_slot_bytes'], 1656)

    def test_fresh_owned_original_constructor_chain(self):
        from tools.school_font_slots_emulation import generate
        self.assertEqual(verify_report(generate('constructor'))['cases'], 2)

    def test_constructor_allocation_source_ABI_CPU_and_authority_corruptions_refused(self):
        changes = [lambda s: s['before_cpu'].update(EIP=0),
                   lambda s: s['entries'][1]['args'].__setitem__(0, 0x592C9C),
                   lambda s: s['entries'][2].update(sp=0),
                   lambda s: s['returns'][2].update(eax=0),
                   lambda s: s['allocations'][0]['args'].__setitem__(0, 1655),
                   lambda s: s['allocations'][0].update(pointer=0),
                   lambda s: s['cpu'].update(ECX=0),
                   lambda s: s['pending'].update(receiver=0),
                   lambda s: s['pending'].update(first_instruction_executed=True),
                   lambda s: s['visited'].remove(0x56CE21),
                   lambda s: s['state'].update(image_sha256='0'*64),
                   lambda s: s['state'].update(SEH=0),
                   lambda s: s['state'].update(stack_guards_unchanged=False),
                   lambda s: s.update(native_CRT_face_copy_executed=False),
                   lambda s: s.update(additional_fonts_completed=True),
                   lambda s: s.update(second_slot_bound=True)]
        for n, mutate in enumerate(changes):
            with self.subTest(change=n):
                bad = deepcopy(self.report)
                mutate(bad['cases'][0]['slot_constructor'])
                with self.assertRaises(ValueError): verify_report(bad)

    def test_rehashed_slot_fields_padding_guard_parent_heap_and_owner_corruptions_refused(self):
        for field, offsets in (('slot_heap', (0, 4095, 4096, 4104, 4105, 4176, 4180, 4184, 4188, 4192, 4196, 5744, 5748, 5752, 12287)),
                               ('owner', (0x1090, 0x1094, 0xB270))):
            for offset in offsets:
                with self.subTest(field=field, offset=offset):
                    bad = deepcopy(self.report)
                    s = bad['cases'][0]['slot_constructor']
                    row = s['slot_heap'] if field == 'slot_heap' else s['state']['owner']
                    raw = bytearray(unpack(row)); raw[offset] ^= 1
                    row.update(buffer_evidence(bytes(raw)))
                    with self.assertRaises(ValueError): verify_report(bad)
        bad = deepcopy(self.report)
        row = bad['cases'][0]['slot_constructor']['heaps'][0]
        raw = bytearray(unpack(row)); raw[4104] ^= 1
        row.update(buffer_evidence(bytes(raw)))
        with self.assertRaises(ValueError): verify_report(bad)

    def test_native_read_and_write_guards_refuse_scratch_overflow_and_old_heap_writes(self):
        from tools.school_font_slots_emulation import SlotEmulator
        e = SlotEmulator.__new__(SlotEmulator)
        e.slot_running, e.image, e.foreign = True, b'', {}
        for at, size in ((SLOT-1, 1), (SLOT+1656, 1), (SLOT+1655, 2), (0x23001000, 4), (0x80A398, 4)):
            with self.subTest(at=at, size=size):
                with self.assertRaises(RuntimeError): e._write(None, None, at, size, 0, None)
        for at, size in ((SLOT-1, 1), (SLOT+1656, 1), (SLOT+1655, 2)):
            with self.assertRaises(RuntimeError): e._slot_read(None, None, at, size, 0, None)


class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-slots-atlas-v1-20261018.json').read_text())

    def test_real_caps_and_unexecuted_atlas_texture_call(self):
        result = verify_report(self.report)
        self.assertTrue(result['real_caps_queried'])
        self.assertFalse(result['atlas_texture_created'])

    def test_fresh_original_atlas_admission(self):
        from tools.school_font_slots_emulation import generate
        self.assertEqual(verify_report(generate('atlas'))['heap_guard_bytes'], 49152)

    def test_actual_caps_ABI_trace_CPU_texture_args_and_completion_corruptions_refused(self):
        changes = [lambda c: c['atlas_admission']['before_cpu'].update(ESP=0),
                   lambda c: c['atlas_admission']['api_calls'][0].update(va='0x0'),
                   lambda c: c['atlas_admission']['api_calls'][0]['args'].__setitem__(1, 0),
                   lambda c: c['atlas_admission']['api_calls'][0]['result'].update(hex='00'*212),
                   lambda c: c['atlas_admission']['returns'][0].update(eax=1),
                   lambda c: c['atlas_admission']['cpu'].update(EDX=0),
                   lambda c: c['atlas_admission']['pending']['args'].__setitem__(5, 21),
                   lambda c: c['atlas_admission']['pending'].update(platform_call_executed=True),
                   lambda c: c['atlas_admission']['pending'].update(method_target=0),
                   lambda c: c['atlas_admission'].update(atlas_texture_created=True),
                   lambda c: c['atlas_admission'].update(full415F50_returned=True),
                   lambda c: c['atlas_admission'].update(state_blocks_created=True),
                   lambda c: c['device_trace'][-2]['reply'].update(id=0),
                   lambda c: c['device_cleanup'].update(device_release_count=1)]
        for n, mutate in enumerate(changes):
            with self.subTest(change=n):
                bad = deepcopy(self.report)
                mutate(bad['cases'][0])
                with self.assertRaises(ValueError): verify_report(bad)

    def test_rehashed_atlas_dimensions_scale_texture_pointer_and_padding_corruptions_refused(self):
        for offset in (4184, 4188, 4192, 4196, 4200, 4204, 4208, 5744, 5752):
            bad = deepcopy(self.report)
            row = bad['cases'][0]['atlas_admission']['slot_heap']
            raw = bytearray(unpack(row)); raw[offset] ^= 1
            row.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError): verify_report(bad)
