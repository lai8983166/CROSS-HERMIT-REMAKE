"""Offline ABI and preparation contracts; never execute the native fixture."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import capstone

from devtools import terminal_tcg_wait_fixture as fixture
from devtools.terminal_vm_wait_fixture import image as frozen_image


class FixtureTests(unittest.TestCase):
    def test_exact_frozen_machine_and_natural_return_frame(self):
        raw, meta = fixture.image()
        self.assertEqual((raw, meta), frozen_image())
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         '671774f8ea30c622791f1bae1cd5f005936f6c2e2389e0e4ef3f26c9732cc99a')
        instructions = list(capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32).disasm(raw, 0))
        self.assertEqual(sum(i.size for i in instructions), len(raw))
        by_address = {i.address: i for i in instructions}
        self.assertEqual(meta['postcall_offset'], 0x71)
        self.assertEqual(by_address[0x6f].mnemonic, 'call')
        self.assertEqual(by_address[0x71].mnemonic, 'pushfd')
        self.assertEqual(by_address[0x72].mnemonic, 'pushal')
        self.assertEqual(raw[0x62:0x6a], bytes.fromhex('ff750c6a00ff7508'))
        self.assertEqual(raw[0xab:0xae], bytes.fromhex('c20800'))
        self.assertLess(meta['post_record_start']+3*meta['post_record_stride']+
                        meta['post_frame_offset']+36, meta['data_bytes'])

    def test_prepare_authenticates_exact_source_and_refuses_overwrite(self):
        root = Path(__file__).resolve().parents[2]/'.venv-audit/native-worker'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='wait-fixture-test-', dir=root) as tmp:
            path = Path(tmp)/'prepared'
            meta = fixture.prepare(path)
            self.assertEqual(meta, json.loads((path/'manifest.json').read_bytes()))
            for name, key in [('fixture.bin', 'template_sha256'),
                              ('terminal_tcg_wait_fixture.cs', 'source_sha256')]:
                self.assertEqual(hashlib.sha256((path/name).read_bytes()).hexdigest(), meta[key])
            self.assertEqual((path/'terminal_tcg_wait_fixture.cs').read_bytes(),
                             Path(fixture.__file__).with_suffix('.cs').read_bytes())
            with self.assertRaises(ValueError):
                fixture.prepare(path)

    def test_cleanup_and_budget_source_contract(self):
        # Structural guard only: actual CloseHandle/Join results require guest evidence.
        source = Path(fixture.__file__).with_suffix('.cs').read_text()
        for contract in ['done.WaitOne(300000)', 'clock.Elapsed.TotalSeconds<240',
                         'counter startup handshake', 'peer startup handshake',
                         'if(!closed)cleanup.Add(', 'if(!released)cleanup.Add(',
                         'if(!affinityRestored)cleanup.Add(',
                         'if(!watchdogStopped)cleanup.Add(',
                         'report["error"]==null&&cleanup.Count==0?0:1',
                         'stub[14]==0', 'NtWait bytes changed', 'private code unchanged']:
            self.assertIn(contract, source)
        self.assertIn('report["accepted"]=false', source)
        self.assertIn('report["original_game_observed"]=false', source)


if __name__ == '__main__':
    unittest.main()
