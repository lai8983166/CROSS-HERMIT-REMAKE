import unittest
from devtools.terminal_kd_session_v3 import Session,marker_complete


class StateTests(unittest.TestCase):
    def session(self,text):
        s=Session.__new__(Session);s.output=text;s.text=lambda:s.output
        s.state='stopped';s.cursor=len(text);s.stopped_text=text;s.transitions=[];s.seen_length=len(text);s.sent=[];s.send=s.sent.append
        return s

    def test_go_rejects_stale_prompt_and_does_not_queue_cleanup(self):
        s=self.session('stop\n1: kd> ');s.go()
        self.assertIsNone(s.poll_stop())
        with self.assertRaisesRegex(ValueError,'confirmed current stop'):s.execute('bc *')
        with self.assertRaisesRegex(ValueError,'confirmed current stop'):s.go()
        self.assertEqual(s.sent,['g'])

    def test_new_breakpoint_prompt_is_observed_once_as_stop(self):
        s=self.session('stop\n1: kd> ');s.go()
        s.output+='Breakpoint 0 hit\nnt!NtWaitForSingleObject+0x6a:\nfffff804`3aafcc6a 4883c438 add rsp,38h\n1: kd> '
        self.assertIn('Breakpoint 0 hit',s.poll_stop());self.assertEqual(s.state,'stopped')
        s.go();self.assertIsNone(s.poll_stop())

    def test_partial_prompt_does_not_authorize_query(self):
        s=self.session('stop\n1: kd> ');s.go();s.output+='Breakpoint 0 hit\n1: kd'
        self.assertIsNone(s.poll_stop())

    def test_marker_can_follow_prompt_from_transcript(self):
        self.assertTrue(marker_complete('1: kd> OWNED_QUERY_END_6\n1: kd> ','OWNED_QUERY_END_6'))
        self.assertTrue(marker_complete('OWNED_QUERY_END_6\n1: kd> ','OWNED_QUERY_END_6'))

    def test_marker_requires_exact_fresh_completion(self):
        for t in ('prefixOWNED_QUERY_END_6\n1: kd> ','OWNED_QUERY_END_60\n1: kd> ','OWNED_QUERY_END_6\n'):
            self.assertFalse(marker_complete(t,'OWNED_QUERY_END_6'))

    def test_unknown_query_state_cannot_be_continued(self):
        s=self.session('old\n1: kd> ');s.state='unknown'
        with self.assertRaises(ValueError):s.go()


if __name__=='__main__':unittest.main()
