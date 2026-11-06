"""Original-byte branch tests; no native APIs, process, or GPU."""
import unittest

from devtools import terminal_startup_handoff_contract as c


class StartupHandoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (c.ROOT/'analysis/hermit_game.exe').read_bytes()

    def test_fixed_original_contract_and_scope(self):
        report = c.source_contract(self.raw)
        self.assertEqual(report['startup']['threshold'],16204)
        self.assertEqual(report['startup']['initial_stage'],0)
        self.assertTrue(all(v is False for v in report['acceptance'].values()))

    def test_image_mutation_rejected(self):
        changed = bytearray(self.raw)
        changed[0x10A00D] ^= 1
        with self.assertRaisesRegex(ValueError,'identity'):
            c.source_contract(bytes(changed))

    def test_truncated_image_rejected(self):
        with self.assertRaisesRegex(ValueError,'identity'):
            c.source_contract(self.raw[:-1])

    def test_before_threshold_yields_without_stage_change(self):
        row = c.local_counter_dispatch(self.raw,16202,22)
        self.assertEqual((row['counter'],row['stage'],row['stop']), (16203,22,0x50A026))

    def test_exact_threshold_sets_stage_but_still_yields(self):
        row = c.local_counter_dispatch(self.raw,16203,22)
        self.assertEqual((row['counter'],row['stage'],row['stop']), (16204,100,0x50A026))
        self.assertNotIn(0x50A04D,row['instructions'])

    def test_next_iteration_reaches_tail(self):
        row = c.local_counter_dispatch(self.raw,16204,100)
        self.assertEqual((row['counter'],row['stage'],row['stop']), (16205,100,0x50A04D))
        self.assertFalse(row['native_lifetime_proved'])

    def test_missed_equality_is_not_greater_than_threshold(self):
        row = c.local_counter_dispatch(self.raw,16204,22)
        self.assertEqual((row['counter'],row['stage'],row['stop']), (16205,22,0x50A026))

    def test_initial_dispatch(self):
        row = c.local_counter_dispatch(self.raw,0,0)
        self.assertEqual((row['counter'],row['stage'],row['stop']), (1,0,0x50673A))

    def test_invalid_stage_goes_to_yield(self):
        row = c.local_counter_dispatch(self.raw,10,255)
        self.assertEqual((row['counter'],row['stage'],row['stop']), (11,255,0x50A026))

    def test_original_uint32_wrap(self):
        row = c.local_counter_dispatch(self.raw,0xFFFFFFFF,22)
        self.assertEqual(row['counter'],0)
        self.assertEqual(row['stage'],22)

    def test_invalid_fixture_inputs(self):
        for counter,stage in [(-1,22),(2**32,22),(False,22),(0,-1),(0,256),(0,True)]:
            with self.subTest(counter=counter,stage=stage):
                with self.assertRaises(ValueError):
                    c.local_counter_dispatch(self.raw,counter,stage)


if __name__ == '__main__':
    unittest.main()
