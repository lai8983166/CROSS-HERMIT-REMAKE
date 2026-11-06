"""Fault diagnosis must reject a different process, DLL, instruction or register."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import struct
import unittest
from devtools.terminal_scene_owner_failure import ROOT,diagnose


class FailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        packed=(ROOT/'analysis/terminal-scene-owner-v4-20261107.json.gz').read_bytes()
        if hashlib.sha256(packed).hexdigest()!='5b0c15243e68dd8c474605a8409ef5d41f8a4bdea2fa7fdd63bb08e5d16e5286':
            raise ValueError('fixed unique native failure fixture')
        cls.report=json.loads(gzip.decompress(packed))
        cls.wer=json.loads((ROOT/'analysis/terminal-scene-owner-failure-v4-analysis-v2-20261107.json').read_text('utf8'))['OS_record']
        cls.source=(ROOT/'analysis/hermit_game.exe').read_bytes()
        cls.dll=Path('C:/Windows/SysWOW64/d3d8.dll').read_bytes()

    def test_correlated_failure(self):
        r=diagnose(self.report,self.wer,self.dll,self.source)
        self.assertEqual(r['attempted_write_address'],0xDDDDDD9D)
        self.assertEqual(r['inferred_nonnull_resource_argument'],0xDDDDDDDD)
        self.assertFalse(r['complete_battle_exit'])
        self.assertEqual(r['first_fault_sample'],135)

    def test_foreign_or_wrong_os_record(self):
        for key,value in (('AppSessionGuid','00000001-x'),('Sig[5].Value','0'),
                          ('Sig[6].Value','0'),('Sig[7].Value','0004d8e9'),('AppPath','foreign.exe')):
            with self.subTest(key=key),self.assertRaises(ValueError):
                diagnose(self.report,dict(self.wer,**{key:value}),self.dll,self.source)

    def test_wrong_register_or_success_assertion(self):
        r=copy.deepcopy(self.report)
        for sample in r['probe']['samples']:
            for frame in sample['frames']:
                raw=bytearray.fromhex(frame['context_hex'])
                struct.pack_into('<I',raw,156,0)
                frame['context_hex']=raw.hex()
        with self.assertRaises(ValueError):diagnose(r,self.wer,self.dll,self.source)
        r=copy.deepcopy(self.report);r['probe']['native_retreat_observed']=True
        with self.assertRaises(ValueError):diagnose(r,self.wer,self.dll,self.source)
        r=copy.deepcopy(self.report);r['probe']['worker_exit']['exit_code']=0
        with self.assertRaises(ValueError):diagnose(r,self.wer,self.dll,self.source)

    def test_source_or_fault_instruction_tamper(self):
        raw=bytearray(self.source);raw[0xE244]^=1
        with self.assertRaises(ValueError):diagnose(self.report,self.wer,self.dll,raw)
        import pefile
        raw=bytearray(self.dll);raw[pefile.PE(data=self.dll).get_offset_from_rva(0x4D8E8)]^=1
        with self.assertRaises(ValueError):diagnose(self.report,self.wer,raw,self.source)


if __name__=='__main__':unittest.main()
