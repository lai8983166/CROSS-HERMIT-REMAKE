"""Review scheduling only; never launch the game or read the desktop."""
import unittest
from unittest.mock import patch
from devtools import terminal_host_menu_preflight_v4 as menu


class ReviewBudgetTests(unittest.TestCase):
    def test_observed_45_second_review_fits(self):
        end=menu.review_deadline(100,600)
        self.assertEqual(end,190)
        with patch.object(menu,'approval_matches',return_value=True):
            self.assertTrue(menu.review_ready(None,None,145,end))

    def test_total_desktop_budget_not_extended(self):
        end=menu.review_deadline(100,470)
        self.assertEqual(end,120)
        self.assertEqual(470-end,350)

    def test_no_budget_cannot_wait_for_review(self):
        with self.assertRaises(TimeoutError): menu.review_deadline(100,450)

    def test_late_valid_receipt_cannot_bypass_timeout(self):
        with patch.object(menu,'approval_matches',side_effect=AssertionError('must check deadline first')):
            with self.assertRaises(TimeoutError):menu.review_ready(None,None,190,190)

    def test_no_receipt_does_not_grant_approval(self):
        with patch.object(menu,'approval_matches',return_value=False):
            self.assertFalse(menu.review_ready(None,None,110,190))


if __name__=='__main__':unittest.main()
