import unittest
from devtools.terminal_cr2_receipt_poll import poll


def receipt(value):
    return dict(host_job_active_after=0, host_exit_code=0, remote_completion='observed',
                response=dict(ok=True, value=value))


class ReceiptPoll(unittest.TestCase):
    def test_absent_then_durable_no_resubmission(self):
        clock = [0]
        seen = []
        def query(index):
            seen.append(index)
            return receipt({'prepared': True} if index == 2 else {'file_present': False})
        value, rows = poll(query, lambda v: v.get('prepared') is True, 10,
                           clock=lambda: clock[0], sleep=lambda n: clock.__setitem__(0, clock[0]+n))
        self.assertTrue(value['response']['value']['prepared'])
        self.assertEqual(seen, [0, 1, 2])

    def test_late_success_refused(self):
        clock = [0]
        def query(index):
            clock[0] = 11
            return receipt({'prepared': True})
        with self.assertRaises(ValueError):
            poll(query, lambda v: True, 10, clock=lambda: clock[0])

    def test_wrong_identity_or_unknown_read_refused(self):
        for response in (receipt({'pid': 1}), {'timed_out': True}):
            calls = []
            with self.assertRaises(ValueError):
                poll(lambda index: calls.append(index) or response, lambda v: v.get('pid') == 2, 10)
            self.assertEqual(calls, [0])


if __name__ == '__main__':
    unittest.main()
