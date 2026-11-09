import struct
import unittest
from devtools import terminal_battle_result_inventory as m


class ResultCoverageTests(unittest.TestCase):
    def frame(self,pc):
        raw=bytearray(716);struct.pack_into('<I',raw,0,0x1003f);struct.pack_into('<I',raw,184,pc)
        return dict(EIP=pc,context_hex=raw.hex(),chain=[dict(return_va=0x453cb5)])
    def test_saved_consumer_site_does_not_count_as_current_execution(self):
        row=m.classify(self.frame(0x77d13bfc))
        self.assertEqual(row['saved_consumer_return_sites'],[0x453cb5])
        self.assertFalse(row['actual_consumer_PC'])
    def test_actual_consumer_pc_requires_original_context_word(self):
        frame=self.frame(0x453cb5);self.assertTrue(m.classify(frame)['actual_consumer_PC'])
        frame['EIP']=0x453cc4
        with self.assertRaisesRegex(ValueError,'raw actual'):m.classify(frame)
    def test_incomplete_or_partial_context_not_counted(self):
        for change in ('short','flags'):
            frame=self.frame(0x4967b0);raw=bytearray.fromhex(frame['context_hex'])
            if change=='short':raw=raw[:-1]
            else:struct.pack_into('<I',raw,0,0x10007)
            frame['context_hex']=raw.hex()
            with self.assertRaisesRegex(ValueError,'complete original'):m.classify(frame)


if __name__=='__main__':unittest.main()
