import unittest

from devtools import terminal_menu_transition_contract as c


class MenuContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = c.read_source()

    def test_fixed_original_instruction_contract(self):
        report = c.contract(self.raw)
        self.assertFalse(report['validation']['full_battle_acceptance'])
        self.assertEqual(report['load']['save_fields']['schedule_count'], 0)
        self.assertEqual(report['load']['file_copy_bytes'], 198356)

    def test_source_tamper_rejected(self):
        raw = bytearray(self.raw)
        raw[0x45F019-c.BASE] ^= 1
        with self.assertRaisesRegex(ValueError, 'SHA'):
            c.authenticate(raw)

    def test_source_truncation_rejected(self):
        with self.assertRaisesRegex(ValueError, 'size'):
            c.authenticate(self.raw[:-1])

    def test_all_six_original_centers(self):
        for i, (x,y,w,h) in enumerate(c.RECTANGLES):
            with self.subTest(i=i):
                self.assertEqual(c.original_hit_test(self.raw,x+w//2,y+h//2)['selection'],i)

    def test_original_open_edges(self):
        for x,y in [(215,508),(422,508),(318,492),(318,524),
                    (318,557),(0,16),(207,16),(103,0),(103,32)]:
            with self.subTest(x=x,y=y):
                self.assertEqual(c.original_hit_test(self.raw,x,y)['selection'],-1)

    def test_outside_signed_coordinates(self):
        for x,y in [(-1,508),(2**31-1,508),(-2**31,508),(318,-1),(1024,768)]:
            self.assertEqual(c.original_hit_test(self.raw,x,y)['selection'],-1)

    def test_unrepresentable_or_boolean_coordinates_rejected(self):
        for x in [2**31,-2**31-1,True,1.5]:
            with self.assertRaises(ValueError):
                c.original_hit_test(self.raw,x,508)

    def test_title_consumes_release_not_held(self):
        self.assertFalse(c.original_selection_gate(self.raw,0,0,1)['accepted'])
        self.assertTrue(c.original_selection_gate(self.raw,0,1,0)['accepted'])
        self.assertFalse(c.original_selection_gate(self.raw,0,2,0)['accepted'])

    def test_no_hit_does_not_consume_release(self):
        self.assertFalse(c.original_selection_gate(self.raw,-1,1)['accepted'])

    def test_original_edge_arithmetic_all_masks(self):
        for previous in range(8):
            for current in range(8):
                result = c.original_input_edges(self.raw,previous,current)
                with self.subTest(previous=previous,current=current):
                    self.assertEqual(result['held'],current)
                    self.assertEqual(result['pressed'],(previous^current)&current)
                    self.assertEqual(result['released'],(previous^current)&previous)

    def test_original_dispatch_every_selection(self):
        for i,address in enumerate(c.DISPATCH):
            self.assertEqual(c.original_dispatch(self.raw,i)['stop'],hex(address))
        for i in [-1,7]:
            self.assertEqual(c.original_dispatch(self.raw,i)['stop'],'0x45ed89')

    def test_invalid_masks_fail_before_execution(self):
        for mask in [-1,8,True]:
            with self.assertRaises(ValueError):
                c.original_input_edges(self.raw,0,mask)


if __name__ == '__main__':
    unittest.main()
