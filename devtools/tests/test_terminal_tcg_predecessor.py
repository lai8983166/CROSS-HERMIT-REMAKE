from pathlib import Path
import unittest
from devtools.terminal_tcg_predecessor_verify import verify

class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d=Path(__file__).resolve().parents[2]/'.venv-audit/native-worker/tcg-predecessor-v3-20261110'
        cls.elf=(d/'guest.elf').read_bytes();cls.trace=(d/'trace.log').read_text();cls.output=(d/'guest.txt').read_bytes()
    def test_actual_path_only_partial(self):
        r=verify(self.elf,self.trace,self.output);self.assertTrue(r['finite_TCG_predecessor_event_observed']);self.assertFalse(r['fullstate'])
    def test_wrong_frame(self):
        out=bytearray(self.output);out[3]^=1
        with self.assertRaises(ValueError):verify(self.elf,self.trace,bytes(out))
    def test_lost_event(self):
        with self.assertRaises(ValueError):verify(self.elf,self.trace.replace('v=01','v=02'),self.output)
    def test_wrong_vp(self):
        with self.assertRaises(ValueError):verify(self.elf,self.trace.replace('Trace 0:','Trace 1:'),self.output)
    def test_ret_replaced_by_nop(self):
        elf=bytearray(self.elf);elf[4096+0x384]=0x90
        with self.assertRaises(ValueError):verify(bytes(elf),self.trace,self.output)
    def test_aborted_tb(self):
        with self.assertRaises(ValueError):verify(self.elf,self.trace+'\nStopped execution of TB\n',self.output)

if __name__=='__main__':unittest.main()
