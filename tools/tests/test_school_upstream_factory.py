import unittest
from tools.school_upstream_factory import *


class SourceTests(unittest.TestCase):
    def test_two_original_factories_same_owner_size_and_different_actual_mode_inputs(self):
        s=source_contract();self.assertEqual(s['allocation_bytes'],47648)
        self.assertEqual(s['window_startup_middle_args'],[1,1]);self.assertEqual(s['game_startup_middle_args'],[0,1])
        self.assertEqual(len(s['constructor_calls']),42)

    def test_both_inherited_missing_heaps_are_checkpoint_bound(self):
        s=source_contract();self.assertEqual([r['captured_pointer'] for r in s['inherited_missing_heaps']],['0x4d61d08','0x4d60b38'])
        self.assertTrue(all(r['mapped_in_retained_checkpoint'] is False for r in s['inherited_missing_heaps']))

    def test_full_owner_projection_uses_CD_allocation_and_preserves_outside_bytes(self):
        api=dict(GetDC=dict(result=1),QueryPerformanceCounter=dict(result=1,hex='01'+'00'*7),QueryPerformanceFrequency=dict(result=1,hex='02'+'00'*7))
        for fill in (0xA5,0xCC):
            initial=initial_owner(fill);after=project_constructor(initial,api)
            self.assertEqual(after[OWNER_BYTES:],bytes([fill])*(0xC000-OWNER_BYTES))
            self.assertEqual(after[0xB1A4:0xB1A8],b'\xcd'*4)
        with self.assertRaises(ValueError):initial_owner(0)

    def test_cache_and_unexecuted_output_boundaries_remain_explicit(self):
        s=source_contract();self.assertFalse(s['cache_head_reset_by_factory_prefix'])
        self.assertFalse(s['original_factory_output_published']);self.assertFalse(s['original_device_startup_executed'])
