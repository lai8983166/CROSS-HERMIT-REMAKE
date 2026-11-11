"""Independent first-record consumer review against the frozen capsule."""
import copy
import gzip
import json
from pathlib import Path
import unittest
import zipfile
from devtools.terminal_tcg_context_consume_v1 import verify
from devtools.tests.test_terminal_tcg_context_wait import load, CAPSULE


def load_result():
    with zipfile.ZipFile(CAPSULE) as archive:
        return json.loads(archive.read('windows/result-exit-response.json'))['response']['value']

def byte_flip(result, offset):
    data = bytearray.fromhex(result['data_hex'])
    data[offset] ^= 1
    result['data_hex'] = data.hex()

def mutations():
    return [
        ('saved_eax', lambda r: byte_flip(r,0x1200+7*4)),
        ('saved_flags', lambda r: byte_flip(r,0x1200+8*4)),
        ('saved_xmm0', lambda r: byte_flip(r,0x1000+160)),
        ('result_owner', lambda r: r['ready'].__setitem__('tid',r['ready']['tid']+1)),
        ('handles_not_closed', lambda r: r.__setitem__('handles_closed',False)),
    ]

class ConsumerReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace,_=load();cls.result=load_result()
    def test_original_first_record(self):
        proof=verify(self.trace,self.result)
        self.assertTrue(proof['first_saved_record_verified'],proof)
        self.assertFalse(proof['accepted']);self.assertFalse(proof['original_game'])
    def test_five_meaningful_mutations(self):
        for name,change in mutations():
            with self.subTest(name=name):
                result=copy.deepcopy(self.result);change(result)
                self.assertFalse(verify(self.trace,result)['first_saved_record_verified'],name)

if __name__=='__main__':unittest.main()
