import threading
import unittest
from unittest.mock import patch
from devtools import terminal_battle_wait_clock_settled as s


class HeldSettlingTests(unittest.TestCase):
    def window(self):
        w=object.__new__(s.SettledWindow);w.lock=threading.RLock()
        values=iter((100,16000));w.qpc=lambda:next(values)
        return w

    def test_actual_elapsed_is_preserved_without_descheduling_claim(self):
        w=self.window()
        with patch.object(s.time,'sleep')as sleep:w.settle_held()
        sleep.assert_called_once_with(.001)
        self.assertEqual((w._settling['qpc_begin'],w._settling['qpc_end']),(100,16000))
        self.assertFalse(w._settling['descheduling_assumed'])
        self.assertFalse(w._settling['ETL_records_discarded'])

    def test_interrupted_settling_cannot_fabricate_completed_interval(self):
        w=self.window()
        with patch.object(s.time,'sleep',side_effect=RuntimeError('interrupted')):
            with self.assertRaisesRegex(RuntimeError,'interrupted'):w.settle_held()
        self.assertNotIn('qpc_end',w._settling)

    def test_parent_drift_is_rejected_before_native_run(self):
        with patch.object(s,'CLOCK_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'fixed diagnostic parents'):s.settled_template()


if __name__=='__main__':unittest.main()
