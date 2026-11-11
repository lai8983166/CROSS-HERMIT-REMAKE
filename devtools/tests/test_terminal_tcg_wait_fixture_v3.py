"""Offline ABI and preparation contracts; never execute the native fixture."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import capstone

from devtools import terminal_tcg_wait_fixture_v3 as fixture
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
                              ('terminal_tcg_wait_fixture_v3.cs', 'source_sha256')]:
                self.assertEqual(hashlib.sha256((path/name).read_bytes()).hexdigest(), meta[key])
            self.assertEqual((path/'terminal_tcg_wait_fixture_v3.cs').read_bytes(),
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

    def test_go_gates_native_counter_and_peer_request(self):
        # Static ordering guard, not evidence of guest execution or CPU savings.
        source = Path(fixture.__file__).with_suffix('.cs').read_text()
        self.assertIn('ManualResetEvent workGate=new ManualResetEvent(false);', source)
        self.assertIn('counterReady[index].Set();workGate.WaitOne();if(Interlocked.CompareExchange(ref stop,0,0)!=0)return;counterNativeEntered[index]=true;counter();', source)
        self.assertIn('peerReady.Set();workGate.WaitOne();if(Interlocked.CompareExchange(ref stop,0,0)!=0)return;for(int i=0;i<3;i++)', source)
        self.assertIn('Gate(Path.Combine(dir,"go"));goReceived=true;workGate.Set();', source)
        self.assertEqual(source.count('workGate.Set();'), 2)
        cleanup = source[source.rindex('finally{'):]
        self.assertLess(cleanup.index('Interlocked.Exchange(ref stop,1)'), cleanup.index('workGate.Set();'))
        self.assertLess(cleanup.index('Marshal.WriteInt32(data,0x308,1)'), cleanup.index('workGate.Set();'))
        self.assertLess(cleanup.index('workGate.Set();'), cleanup.index('peer.Join(2500)'))
        self.assertLess(cleanup.index('workGate.Set();'), cleanup.index('c.Join(2500)'))
        self.assertIn('if(workersStopped){foreach(ManualResetEvent e in counterReady)e.Dispose();peerReady.Dispose();workGate.Dispose();}', cleanup)
        for field in ['counter_native_started', 'peer_request_wait_started']:
            self.assertIn('ready["'+field+'"]=false;', source)
        self.assertIn('ready["workers_gated_until_go"]=true;', source)

    def test_build_contract_and_failure_without_host_execution(self):
        root = Path(__file__).resolve().parents[2]/'.venv-audit/native-worker'
        with tempfile.TemporaryDirectory(prefix='wait-v2-build-test-', dir=root) as tmp:
            path = Path(tmp)/'prepared'
            meta = fixture.prepare(path)
            self.assertEqual(meta['fixture_version'], 3)
            self.assertEqual(meta['wait_timeout_100ns'], -300000000)
            self.assertTrue(meta['private_data_pages_pretouched'])
            self.assertIn('not game parameters', meta['timeout_scope'])
            self.assertTrue(meta['workers_gated_until_go'])
            self.assertEqual(meta['startup_confirms'], 'live_affinitized_threads_only')
            self.assertFalse(meta['accepted'])
            self.assertFalse(meta['original_game_observed'])
            self.assertEqual(len((path/'fixture.bin').read_bytes()), 214)
            with patch.object(fixture.subprocess, 'run', return_value=SimpleNamespace(returncode=1, stdout='failed', stderr='')) as run:
                with self.assertRaisesRegex(RuntimeError, 'fixture compile failed'):
                    fixture.compile_fixture(path)
                args = run.call_args.args[0]
                self.assertTrue(args[0].endswith('csc.exe'))
                self.assertIn('/platform:x86', args)
                self.assertEqual(Path(args[-1]).name, 'terminal_tcg_wait_fixture_v3.cs')
                self.assertEqual(run.call_count, 1)
            (path/'fixture.exe').write_bytes(b'not executed')
            with patch.object(fixture.subprocess, 'run') as run:
                with self.assertRaises(ValueError):
                    fixture.compile_fixture(path)
                run.assert_not_called()

    def test_all_private_pages_pretouched_and_explicit_test_timeout(self):
        source = Path(fixture.__file__).with_suffix('.cs').read_text()
        touch = source.index('Marshal.Copy(new byte[16384],0,data,16384);')
        self.assertLess(source.index('private fixture buffers'), touch)
        self.assertLess(touch, source.index('counters[j].Start()'))
        self.assertIn('ready["wait_timeout_100ns"]=-300000000L;', source)
        self.assertIn('ready["private_data_pages_pretouched"]=true;', source)
        self.assertIn('Marshal.WriteInt64(timeout,i==3?0:-300000000L);', source)
        self.assertIn('Need(SetEvent(response),"peer response")', source)


if __name__ == '__main__':
    unittest.main()
