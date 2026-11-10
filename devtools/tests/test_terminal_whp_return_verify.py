import copy
import json
from pathlib import Path
import unittest
from devtools.terminal_whp_return_verify import verify


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('F:/project/chaomofa/.venv-audit/native-worker')
        cls.sources=[json.loads((root/('whp-return-v%d-20261110'%v)/'report.json').read_text())for v in(1,2)]
    def load(self,row):return Path(row['path']).read_bytes()
    def test_both_native_sources_have_only_partial_qualification(self):
        for r in self.sources:
            result=verify(r,self.load);self.assertTrue(result['fixture_boundary_and_raw_fp_checks_passed']);self.assertFalse(result['fullstate']);self.assertFalse(result['rflags_transparent'])
    def test_fullstate_promotion_refused(self):
        r=copy.deepcopy(self.sources[1]);r['fullstate']=True
        with self.assertRaises(ValueError):verify(r,self.load)
    def test_wrong_return_pc_refused(self):
        r=copy.deepcopy(self.sources[1]);r['phases'][1]['exits'][0]['rip']+=1
        with self.assertRaises(ValueError):verify(r,self.load)
    def test_early_consumer_refused(self):
        r=copy.deepcopy(self.sources[1]);path=r['phases'][1]['memory']['path']
        def corrupt(row):
            b=bytearray(self.load(row))
            if row['path']==path:b[0x8200]=1
            return bytes(b)
        with self.assertRaises(ValueError):verify(r,corrupt)
    def test_cleared_rf_refused(self):
        r=copy.deepcopy(self.sources[1]);p=r['phases'][1];p['registers'][0]['17']='46000000000000000000000000000000'
        with self.assertRaises(ValueError):verify(r,self.load)
    def test_fabricated_fp_pointer_refused(self):
        r=copy.deepcopy(self.sources[1]);reg=r['phases'][1]['registers'][0];reg[str(0x1019)]='00'*16
        with self.assertRaises(ValueError):verify(r,self.load)
    def test_unjoined_vp_refused(self):
        r=copy.deepcopy(self.sources[1]);r['phases'][1]['all_run_threads_joined']=False
        with self.assertRaises(ValueError):verify(r,self.load)


if __name__=='__main__':unittest.main()
