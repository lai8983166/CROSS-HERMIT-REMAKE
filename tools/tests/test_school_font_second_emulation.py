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
