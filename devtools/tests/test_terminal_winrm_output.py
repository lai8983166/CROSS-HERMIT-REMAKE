import tempfile
import base64
import json
import unittest
from pathlib import Path
from devtools.terminal_winrm_output_v2 import receive

S = '11111111-1111-1111-1111-111111111111'
C = '22222222-2222-2222-2222-222222222222'
TEMP = Path(__file__).resolve().parents[2] / '.venv-audit' / 'winrm-output-tests'


def temporary():
    TEMP.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=TEMP)


class Fake:
    def __init__(self, rows):
        self.rows = iter(rows)
    def get_command_output_raw(self, *ids):
        value = next(self.rows)
        if isinstance(value, Exception):
            raise value
        return value


class Receipts(unittest.TestCase):
    def test_resume_after_durable_partial_output(self):
        with temporary() as d:
            row = dict(shell=S, command=C, stdout=base64.b64encode(b'{"value":').decode(),
                       stderr='', code=-1, done=False)
            (Path(d) / ('receive-' + C + '-000000.json')).write_text(json.dumps(row))
            result = receive(Fake([(b'42}', b'', 0, True)]), d, S, C)
            self.assertEqual(result, (b'{"value":42}', b'', 0))
            self.assertEqual(receive(Fake([]), d, S, C), result)

    def test_lost_reply_rejects_resume(self):
        with temporary() as d:
            with self.assertRaises(ConnectionError):
                receive(Fake([(b'partial', b'', -1, False), ConnectionError()]), d, S, C)
            with self.assertRaisesRegex(ValueError, 'outcome unknown'):
                receive(Fake([]), d, S, C)

    def test_partial_receipt_rejected_without_network(self):
        with temporary() as d:
            (Path(d) / ('receive-' + C + '-000000.json')).write_text('{')
            with self.assertRaises(ValueError):
                receive(Fake([]), d, S, C)

    def test_wrong_owner_rejected(self):
        with temporary() as d:
            receive(Fake([(b'ok', b'', 0, True)]), d, S, C)
            with self.assertRaises(ValueError):
                receive(Fake([]), d, C, C)
