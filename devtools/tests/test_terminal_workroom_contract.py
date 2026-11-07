import unittest
from devtools import terminal_workroom_contract as workroom
from devtools import terminal_menu_transition_contract as menu


class WorkroomContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw=menu.read_source()
    def test_original_exit_contract(self):
        self.assertFalse(workroom.contract(self.raw)['full_battle_exit_accepted'])
    def test_source_mutation_refused(self):
        raw=bytearray(self.raw);raw[0x49FEC3-menu.BASE]^=1
        with self.assertRaises(ValueError):workroom.contract(raw)
    def test_actual_press_and_stack_cleanup(self):
        r=workroom.original_hit(self.raw,*workroom.TARGET,pressed=1)
        self.assertEqual((r['inside'],r['pressed'],r['exit_press_observed']),(1,1,True))
    def test_held_or_release_does_not_select(self):
        for fields in ({'held':1},{'released':1},{'auxiliary':1},{'pressed':2},{'pressed':4}):
            self.assertFalse(workroom.original_hit(self.raw,*workroom.TARGET,**fields)['exit_press_observed'])
    def test_all_four_rectangle_edges_are_inclusive(self):
        for x,y in ((847,726),(988,726),(847,756),(988,756)):
            self.assertTrue(workroom.original_hit(self.raw,x,y,pressed=1)['exit_press_observed'])
    def test_one_pixel_outside_clears_all_output_fields(self):
        for x,y in ((846,741),(989,741),(917,725),(917,757)):
            r=workroom.original_hit(self.raw,x,y,held=7,pressed=7,released=7,auxiliary=7)
            self.assertEqual([r[k] for k in ('held','pressed','auxiliary','inside')],[0,0,0,0])


if __name__=='__main__':unittest.main()
