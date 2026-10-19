import json
import unittest
from copy import deepcopy
from tools.school_font_second import ROOT, SECOND
from tools.school_font_second_verification import verify_report
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import buffer_evidence


class LoopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-second-loop-v1-20261019.json').read_text())

    def test_original_success_loop_and_fresh_owned_rerun(self):
        self.assertTrue(verify_report(self.report)['original_success_loop_executed'])
        from tools.school_font_second_emulation import generate
        self.assertFalse(verify_report(generate('loop'))['distinct_second_font_constructed'])

    def test_trace_index_status_CPU_allocation_and_scope_refused(self):
        changes = [lambda c:c['second_loop']['instruction_trace'].pop(4),
            lambda c:c['second_loop']['loop_locals'].update(index=0),
            lambda c:c['second_loop']['loop_locals'].update(status=1),
            lambda c:c['second_loop']['before_cpu'].update(EAX=1),
            lambda c:c['second_loop']['cpu'].update(EFLAGS=6),
            lambda c:c['second_loop']['allocations'].append({}),
            lambda c:c['second_loop'].update(second_additional_font_constructed=True),
            lambda c:c['device_cleanup'].update(font_state_block_delete_results=[])]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad = deepcopy(self.report)
                f(bad['cases'][0])
                with self.assertRaises(ValueError): verify_report(bad)

    def test_rehashed_first_font_owner_maps_and_early_write_refused(self):
        for field,offset in (('slot',4192),('owner',0x1094),('map',0)):
            bad = deepcopy(self.report)
            s = bad['cases'][0]['second_loop']
            r = s['slot_heap'] if field=='slot' else s['state']['owner'] if field=='owner' else s['state']['foreign_maps'][0]
            raw = bytearray(unpack(r))
            raw[offset] ^= 1
            r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError): verify_report(bad)
        from tools.school_font_second_emulation import SecondEmulator
        e = SecondEmulator.__new__(SecondEmulator)
        e.second_running,e.second_phase = True,'loop'
        for at in (SECOND,0x2300D060,0x20001094,0x79FC74):
            with self.assertRaises(RuntimeError): e._write(None,None,at,4,0,None)
        for at in (SECOND-4096,SECOND,SECOND+8191):
            with self.assertRaisesRegex(RuntimeError,'collides with audit ownership'):
                e._map_page(at)
        for pointer in (SECOND-4096,SECOND,SECOND+8192):
            with self.assertRaisesRegex(RuntimeError,'collides with audit ownership'):
                e._shadow('DIB',pointer,bytes(32))


class ConstructorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-second-constructor-v1-20261019.json').read_text())

    def test_original_separate_allocation_ANSI_copy_and_fresh_rerun(self):
        self.assertTrue(verify_report(self.report)['distinct_second_font_constructed'])
        from tools.school_font_second_emulation import generate
        self.assertFalse(verify_report(generate('constructor'))['second_caps_queried'])

    def test_allocator_face_size_flags_counter_image_returns_and_binding_refused(self):
        changes = [lambda c:c['second_constructor']['allocations'][0].update(pointer=0x2300D000),
            lambda c:c['second_constructor']['allocations'][0]['args'].__setitem__(0,1655),
            lambda c:c['second_constructor']['entries'][1]['args'].__setitem__(0,0x592CA4),
            lambda c:c['second_constructor']['entries'][1]['args'].__setitem__(1,12),
            lambda c:c['second_constructor']['entries'][1]['args'].__setitem__(2,1),
            lambda c:c['second_constructor']['state'].update(image_sha256=c['second_loop']['state']['image_sha256']),
            lambda c:c['second_constructor']['returns'][-1].update(sp=0),
            lambda c:c['second_constructor']['pending'].update(receiver=0x2300D000),
            lambda c:c['second_constructor'].update(full415F50_returned=True)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad = deepcopy(self.report)
                f(bad['cases'][0])
                with self.assertRaises(ValueError): verify_report(bad)

    def test_rehashed_full_second_heap_face_padding_fields_guards_owner_refused(self):
        for field,offset in (('heap',4096),('heap',4104),('heap',4176),('heap',4180),
                             ('heap',5744),('heap',5752),('heap',0),('heap',12287),('owner',0x1094)):
            bad = deepcopy(self.report)
            s = bad['cases'][0]['second_constructor']
            r = s['second_heap'] if field=='heap' else s['state']['owner']
            raw = bytearray(unpack(r))
            raw[offset] ^= 1
            r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError): verify_report(bad)


class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-font-second-atlas-v1-20261019.json').read_text())

    def test_original_second_caps_texture_arguments_and_fresh_rerun(self):
        self.assertTrue(verify_report(self.report)['second_caps_queried'])
        from tools.school_font_second_emulation import generate
        self.assertFalse(verify_report(generate('atlas'))['second_atlas_texture_created'])

    def test_caps_identity_ABI_result_CPU_texture_output_trace_and_authority_refused(self):
        changes = [lambda c:c['second_atlas']['api_calls'][0].update(va='0x0'),
            lambda c:c['second_atlas']['api_calls'][0]['args'].__setitem__(1,0),
            lambda c:c['second_atlas']['api_calls'][0]['result'].update(hr=1),
            lambda c:c['second_atlas']['pending']['args'].__setitem__(7,0x2300D05C),
            lambda c:c['second_atlas']['pending'].update(platform_call_executed=True),
            lambda c:c['second_atlas']['cpu'].update(ECX=SECOND),
            lambda c:c['second_atlas']['instruction_trace'].remove(0x401147),
            lambda c:c['second_atlas'].update(second_atlas_texture_created=True),
            lambda c:c['device_trace'][-2]['reply'].update(id=0)]
        for n,f in enumerate(changes):
            with self.subTest(change=n):
                bad = deepcopy(self.report)
                f(bad['cases'][0])
                with self.assertRaises(ValueError): verify_report(bad)

    def test_rehashed_second_atlas_fields_pixel_snapshot_and_ownership_refused(self):
        for offset in (4184,4188,4196,4200,4204,5748):
            bad = deepcopy(self.report)
            r = bad['cases'][0]['second_atlas']['second_heap']
            raw = bytearray(unpack(r))
            raw[offset] ^= 1
            r.update(buffer_evidence(bytes(raw)))
            with self.assertRaises(ValueError): verify_report(bad)
        from tools.school_font_state_emulation import unpack_large
        bad = deepcopy(self.report)
        r = bad['cases'][0]['second_atlas']['external_regions'][0]['buffer']
        raw = bytearray(unpack_large(r))
        raw[-1] ^= 1
        r.update(buffer_evidence(bytes(raw)))
        with self.assertRaises(ValueError): verify_report(bad)
        from tools.school_font_second_emulation import SecondEmulator
        e = SecondEmulator.__new__(SecondEmulator)
        e.second_running,e.second_phase = True,'atlas'
        for at in (SECOND-4,SECOND+1656,0x2300D064,0x20001094,0x79FC74):
            with self.assertRaises(RuntimeError): e._write(None,None,at,4,0,None)
