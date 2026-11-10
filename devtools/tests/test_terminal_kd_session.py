import unittest
from pathlib import Path
from devtools.terminal_kd_session import at_prompt,pending_debug_break


class PromptTests(unittest.TestCase):
    def test_echo_before_go_is_not_a_prompt(self):
        self.assertFalse(at_prompt('OWNED_CLI_ARMED\n'))

    def test_prompt_can_be_unterminated(self):
        self.assertTrue(at_prompt('output\n1: kd> '))

    def test_embedded_prompt_is_not_current_state(self):
        self.assertFalse(at_prompt('0: kd> .echo begin\nbegin\n'))

    def test_old_recovery_requires_second_continue(self):
        p=Path('F:/project/chaomofa/.venv-audit/native-worker/kd-worker/cli-recovery-v1.log')
        self.assertTrue(pending_debug_break(p.read_text()))

    def test_hardware_wait_stop_is_not_debugger_break(self):
        self.assertFalse(pending_debug_break('nt!NtWaitForSingleObject+0x6a:\nfffff806`208fcc6a 4883c438 add rsp,38h\n0: kd> '))

    def test_break_without_prompt_is_not_auto_continued(self):
        self.assertFalse(pending_debug_break('nt!DbgBreakPointWithStatus:\nfffff806`2061edc0 cc int 3\n'))


if __name__=='__main__':unittest.main()
