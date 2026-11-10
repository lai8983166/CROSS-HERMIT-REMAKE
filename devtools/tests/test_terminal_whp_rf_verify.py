import json
from pathlib import Path
import unittest
from devtools.terminal_whp_rf_verify import Bundle,verify,key,digest

CAPSULE=Path(__file__).resolve().parents[2]/'analysis/terminal-wait-whp-rf-support-v1-20261110.zip'
SHA='93e34a67c286a1dfe0a9ca6ae25954e2736f9602886588f605f1583e589cfb8b'

class RawContrastTests(unittest.TestCase):
    def setUp(self):
        self.bundle=Bundle(CAPSULE,SHA);self.addCleanup(self.bundle.close)
        self.paths=self.bundle.manifest['reports'];self.overrides={}
    def read(self,p):return self.overrides.get(key(p),self.bundle.read(p))
    def change_report(self,case,mutate):
        p=next(p for p in self.paths if 'v3-'in p and json.loads(self.read(p))['case']==case)
        r=json.loads(self.read(p));mutate(r);self.overrides[key(p)]=json.dumps(r).encode()
    def reject(self):
        with self.assertRaises(ValueError):verify(self.read,self.paths)
    def test_all_real_contrasts_reject_production_normalization(self):
        r=verify(self.read,self.paths)
        self.assertTrue(r['contrast_checks_passed']);self.assertTrue(r['uniform_RF_clear_refuted'])
        self.assertFalse(r['fullstate']);self.assertFalse(r['production_RF_restoration_authorized'])
    def test_wrong_capsule_identity(self):
        with self.assertRaises(ValueError):Bundle(CAPSULE,'0'*64)
    def test_fullstate_promotion(self):
        self.change_report('ret-ept-raw',lambda r:r.update(fullstate=True));self.reject()
    def test_missing_counterexample(self):
        self.paths=[p for p in self.paths if 'iret-ept-unsafe-clear'not in p];self.reject()
    def test_erased_host_flag_write(self):
        self.change_report('ret-ept-unsafe-clear',lambda r:r.update(host_register_writes_after_start=[]));self.reject()
    def test_same_final_cpu_does_not_hide_duplicate_debug_event(self):
        def mutate(r):
            row=r['phases'][-1]['memory'];b=bytearray(self.read(row['path']))
            b[0x8204]=b[0x9204]=1
            self.overrides[key(row['path'])]=bytes(b);row['sha256']=digest(b)
        self.change_report('ret-ept-unsafe-clear',mutate);self.reject()
    def test_return_stack_is_not_a_direct_ret_witness(self):
        def mutate(r):
            row=r['phases'][1]['memory'];b=bytearray(self.read(row['path']))
            b[0x8204]=b[0x9204]=0
            self.overrides[key(row['path'])]=bytes(b);row['sha256']=digest(b)
        self.change_report('ret-ept-raw',mutate);self.reject()
    def test_raw_rf_cannot_be_normalized(self):
        def mutate(r):r['phases'][1]['registers'][0]['17']='46000000000000000000000000000000'
        self.change_report('ret-ept-raw',mutate);self.reject()

if __name__=='__main__':unittest.main()
