import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from devtools import isolated_vm_autologon as a


class GuestLogonTests(unittest.TestCase):
    def test_explicit_action_required_before_private_input(self):
        with patch.object(a,'run_script')as run:
            with self.assertRaises(ValueError):a.configure('enable-forever')
        run.assert_not_called()

    def test_single_logon_quotes_secret_and_returns_no_secret(self):
        secret="fixture-only-'quoted-value"
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);(root/'credentials.private.json').write_text(json.dumps(dict(password=secret)))
            reply=json.dumps(dict(AutoAdminLogon='1',AutoLogonCount=1,password_configured=True))
            with patch.object(a,'WORKER',root),patch.object(a,'run_script',return_value=reply)as run:
                result=a.configure('arm-once')
        script=run.call_args.args[0]
        self.assertIn("'fixture-only-''quoted-value'",script)
        self.assertIn("if($busy.Count){throw 'guest busy'}",script)
        self.assertIn("if($desktop.Count -or",script)
        self.assertIn('-Name AutoLogonCount -Value 1',script)
        self.assertNotIn(secret,json.dumps(result))

    def test_clear_refuses_success_when_password_remains(self):
        reply=json.dumps(dict(AutoAdminLogon='0',AutoLogonCount=None,password_configured=True))
        with patch.object(a,'run_script',return_value=reply):
            with self.assertRaisesRegex(ValueError,'not cleared'):a.configure('clear')


if __name__=='__main__':unittest.main()
