import unittest

from devtools import terminal_school_preparation_contract as school


class OriginalSchoolContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=school.original.read_source()

    def test_static_contract_and_original_task1(self):
        report=school.contract(self.raw)
        self.assertEqual(report['task1']['scene_id'],1)
        self.assertFalse(report['native_school_preparation_observed'])
        self.assertFalse(report['full_battle_exit_accepted'])

    def test_wrong_source_rejected(self):
        raw=bytearray(self.raw);raw[0xA714D]^=1
        with self.assertRaisesRegex(ValueError,'SHA'):school.contract(bytes(raw))

    def test_original_date_filter(self):
        result=school.original_task_registration(self.raw,4,0)
        self.assertEqual((result['ledger_count'],result['gate'],result['selected']),(0,0,0))

    def test_original_duplicate_registration_filter(self):
        result=school.original_task_registration(self.raw,already_registered=True)
        self.assertEqual((result['ledger_count'],result['gate']),(0,0))

    def test_depart_press(self):
        self.assertEqual(school.original_depart_hit(self.raw,*school.DEPART_TARGET,pressed=1)['control'],0)

    def test_depart_held_release_not_press(self):
        for masks in ({'held':1},{'released':1},{}):
            with self.subTest(masks=masks):
                self.assertEqual(school.original_depart_hit(self.raw,*school.DEPART_TARGET,**masks)['control'],-1)

    def test_depart_original_collision_edges(self):
        for x,y,expected in ((222,41,0),(524,71,0),(525,71,-1),(223,72,-1),(221,42,-1)):
            with self.subTest(x=x,y=y):
                self.assertEqual(school.original_depart_hit(self.raw,x,y,pressed=1)['control'],expected)

    def test_confirm_press(self):
        self.assertTrue(school.original_confirm_hit(self.raw,*school.CONFIRM_TARGET,pressed=1)['selected'])

    def test_confirm_release_not_press(self):
        self.assertFalse(school.original_confirm_hit(self.raw,*school.CONFIRM_TARGET,released=1,held=1)['selected'])

    def test_confirm_inclusive_edges(self):
        for x,y,expected in ((405,390,True),(507,419,True),(508,419,False),(507,420,False)):
            with self.subTest(x=x,y=y):
                self.assertEqual(school.original_confirm_hit(self.raw,x,y,pressed=1)['selected'],expected)

    def test_bounded_inputs(self):
        for operation in (lambda:school.original_task_registration(self.raw,True,1),
                          lambda:school.original_depart_hit(self.raw,32768,0),
                          lambda:school.original_confirm_hit(self.raw,456,404,pressed=8)):
            with self.assertRaises(ValueError):operation()


if __name__=='__main__':unittest.main()
