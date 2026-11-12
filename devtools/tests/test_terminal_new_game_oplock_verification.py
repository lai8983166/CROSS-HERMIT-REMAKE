import copy
import unittest
from devtools import terminal_new_game_oplock_verification as v


class ClockTests(unittest.TestCase):
    def setUp(self):
        report,_=v.native.read_source(v.host.ROOT/'analysis/terminal-oplock-controls-v2-20261112.json.gz')
        self.lock=copy.deepcopy(report['cases'][1]['oplock'])
        self.clock={'qpc_frequency':report['cases'][1]['meta']['frequency']}

    def test_real_source_clock_and_frequency_tamper(self):
        v.verify_clock(self.clock,self.lock)
        self.clock['qpc_frequency']*=100
        with self.assertRaisesRegex(ValueError,'frequency'):v.verify_clock(self.clock,self.lock)

    def test_inconsistent_ticks_rejected(self):
        self.lock['break_qpc']+=200_000
        with self.assertRaisesRegex(ValueError,'cross-check'):v.verify_clock(self.clock,self.lock)


if __name__=='__main__':unittest.main()
