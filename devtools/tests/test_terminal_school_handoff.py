import unittest
from unittest.mock import Mock
from devtools import terminal_school_handoff as collector


class ContinuationTests(unittest.TestCase):
    def test_explicit_declared_new_game_plan_only(self):
        for args in ((1,True,192),(0,False,192),(0,True,300)):
            with self.assertRaises(ValueError):collector.SchoolController(*args)
        c=collector.SchoolController(0,True,192)
        self.assertEqual([x.maximum for x in c.story_phases],[192,192,64])
        self.assertEqual(c.count(),0)
    def test_uncertain_action_never_retried(self):
        send=Mock();a=collector.OwnedAction('test',lambda r:True,send);a.attempted=True
        a.observe(None,None,{})
        send.assert_not_called()
    def test_school_and_battle_cannot_skip_their_real_predecessor_controls(self):
        c=collector.SchoolController(0,True);c.title.done=True
        for vt in (collector.school.GROUP,collector.battle.BATTLE):
            with self.assertRaises(ValueError):c.observe(None,None,dict(tasks=[dict(vtable=vt)]))
    def test_receipt_scopes_and_empty_phases_are_explicit(self):
        r=collector.SchoolController(0,True).reports()
        self.assertEqual(r['collector_input_actions_scope'],'title_menu_only')
        self.assertEqual(r['maximum_mouse_actions'],7);self.assertEqual(r['maximum_story_actions'],448)
        self.assertEqual(r['notice_inputs'],[])
        self.assertEqual(r['workroom_inputs'],[]);self.assertEqual(r['school_inputs'],[]);self.assertEqual(r['battle_inputs'],[])
    def test_only_retreat_confirmation_captures_after_release(self):
        c=collector.SchoolController(0,True)
        self.assertFalse(c.workroom.post_release_snapshots)
        self.assertTrue(c.battle[1].post_release_snapshots)
        self.assertFalse(c.battle[0].post_release_snapshots)


if __name__=='__main__':unittest.main()
