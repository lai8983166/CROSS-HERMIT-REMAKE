import unittest
from unittest.mock import patch
from devtools import terminal_dxgi_game_capture as capture
from devtools import terminal_host_menu_preflight_v3 as menu


class MenuGateTests(unittest.TestCase):
    def test_no_current_authorization_never_starts(self):
        with patch('devtools.terminal_host_desktop.guarded_run',side_effect=AssertionError('must not run')):
            with self.assertRaises(PermissionError): menu.run(None,0,False,None)

    def test_failed_qualification_never_starts_desktop_or_game(self):
        with patch.object(capture,'qualify_current',side_effect=ValueError('not qualified')):
            with patch('devtools.terminal_host_desktop.guarded_run',side_effect=AssertionError('must not run')):
                with self.assertRaisesRegex(ValueError,'not qualified'):menu.run(None,0,True,None)

    def test_capture_is_disabled_without_specific_authorization(self):
        with self.assertRaises(PermissionError):capture.capture_owned(None,0,None,qualification=None)


if __name__=='__main__':unittest.main()
