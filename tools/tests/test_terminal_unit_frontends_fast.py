import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn import x86_const as x86
from tools import terminal_unit_frontends_fast as fast
from tools import terminal_unit_frontends_fast_proof as proof


class ScalarObservationTests(unittest.TestCase):
    def test_all57_register_values_and_types_equal_frozen_complete_cpu(self):
        machine = object.__new__(fast.FastUnitFrontendMachine)
        machine.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        for reg, value in ((x86.UC_X86_REG_EAX, 0xDEADBEEF), (x86.UC_X86_REG_EIP, 0x56CF01),
                           (x86.UC_X86_REG_XMM0, (1 << 127) + 123)):
            machine.uc.reg_write(reg, value)
        before = machine.cpu()
        for name in fast.REGISTER_IDS:
            with self.subTest(register=name):
                self.assertEqual(machine.getreg(name), before[name])
                self.assertIs(type(machine.getreg(name)), type(before[name]))
        self.assertEqual(machine.cpu(), before)
        with self.assertRaises(KeyError):
            machine.getreg('NOT_A_REGISTER')

    def test_scalar_query_makes_one_read_and_does_not_call_full_cpu(self):
        calls = []
        machine = object.__new__(fast.FastUnitFrontendMachine)
        machine.uc = SimpleNamespace(reg_read=lambda reg: calls.append(reg) or 17)
        machine.cpu = lambda: self.fail('scalar query unexpectedly captured full CPU')
        self.assertEqual(machine.getreg('EIP'), 17)
        self.assertEqual(calls, [x86.UC_X86_REG_EIP])

    def test_only_getreg_changes_and_binding_restores_on_exception(self):
        for name in ('cpu', 'code', 'write_hook', 'snapshot', 'prepare_and_run', 'resource_root'):
            self.assertIs(getattr(fast.FastUnitFrontendMachine, name), getattr(fast.ORIGINAL_MACHINE, name))
        with self.assertRaisesRegex(ValueError, 'probe'):
            with fast.scalar_observations():
                self.assertIs(fast.source.UnitFrontendMachine, fast.FastUnitFrontendMachine)
                with self.assertRaisesRegex(ValueError, 'nested'):
                    with fast.scalar_observations():
                        pass
                raise ValueError('probe')
        self.assertIs(fast.source.UnitFrontendMachine, fast.ORIGINAL_MACHINE)

    def test_adapter_and_orchestrator_are_bound_by_actual_implementation_inventory(self):
        inventory = proof.corpus.implementation_files()
        for name in ('fast', 'fast_proof'):
            key = 'tools/terminal_unit_frontends_' + name + '.py'
            self.assertIn(key, inventory)
            self.assertEqual(inventory[key], proof.corpus.identity(proof.corpus.ROOT / key))


class ProofPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / '.venv-audit').mkdir()
        self.output = self.root / 'proof.json'
        self.case = proof.source.previous.overlay.parent.corpus()[0]
        self.data = dict(case=self.case, artifacts=[], authenticated_helpers={})
        self.other = dict(input=self.case, platform=dict(creation={}), CRT_cleanup={}, GPU_cleanup={})

    def run_proof(self, failure=None, fingerprint_change=False):
        self.events = []
        def mark(name, value):
            def run(*args, **kwargs):
                self.events.append(name)
                if failure == name:
                    raise ValueError('injected ' + name)
                if name == 'fresh':
                    self.assertIs(fast.source.UnitFrontendMachine, fast.FastUnitFrontendMachine)
                if name == 'replay':
                    self.assertIs(fast.source.UnitFrontendMachine, fast.ORIGINAL_MACHINE)
                return value
            return run
        start = {'tools/proof.py': {'sha256': 'same'}}
        end = {'tools/proof.py': {'sha256': 'changed'}} if fingerprint_change else start
        with patch.object(proof.corpus, 'ROOT', self.root), \
             patch.object(proof.corpus, 'implementation_files', side_effect=[start, end]), \
             patch.object(proof.frozen, 'authenticate_source', side_effect=mark('authenticate', (self.data, {}))), \
             patch.object(proof.corpus, 'read_case', side_effect=mark('decode', {'input': self.case})), \
             patch.object(proof.frozen, 'resume_source_proof', side_effect=mark('resume', ({'full': True}, {}))), \
             patch.object(proof.source.images, 'CORE_helpers', side_effect=mark('helpers', ('crt', 'gpu', {}))), \
             patch.object(proof.source, 'run_case', side_effect=mark('fresh', self.other)), \
             patch.object(proof.corpus, 'compact_case', side_effect=lambda row: row), \
             patch.object(proof.frozen, 'compare_fresh', side_effect=mark('compare', {'full': True})), \
             patch.object(proof.frozen, 'verify_case', side_effect=mark('replay', {'full': True})):
            return proof.prove(self.root / 'source', 0, self.output, self.root / 'checkpoint', 'sha')

    def test_full_native_compare_and_independent_replay_are_mandatory(self):
        result = self.run_proof()
        self.assertEqual(self.events, ['authenticate', 'decode', 'resume', 'helpers', 'fresh', 'compare', 'replay'])
        self.assertTrue(result['source_and_fresh_case_verified'])
        self.assertFalse(result['accepted'])
        self.assertTrue(all(row['complete'] for row in result['stages']))
        self.assertTrue(all(row['wall_seconds'] >= 0 for row in result['stages']))

    def test_bad_checkpoint_prevents_any_native_lifetime(self):
        with self.assertRaisesRegex(ValueError, 'resume'):
            self.run_proof('resume')
        self.assertNotIn('helpers', self.events)
        self.assertFalse(json.loads(self.output.read_bytes())['source_and_fresh_case_verified'])

    def test_state_mismatch_and_replay_failure_never_pass(self):
        for failure in ('fresh', 'compare', 'replay'):
            with self.subTest(stage=failure):
                self.output = self.root / (failure + '.json')
                with self.assertRaisesRegex(ValueError, failure):
                    self.run_proof(failure)
                self.assertFalse(json.loads(self.output.read_bytes())['source_and_fresh_case_verified'])
                self.assertIs(fast.source.UnitFrontendMachine, fast.ORIGINAL_MACHINE)

    def test_changed_implementation_is_not_a_successful_proof(self):
        with self.assertRaisesRegex(ValueError, 'unchanged'):
            self.run_proof(fingerprint_change=True)
        self.assertFalse(json.loads(self.output.read_bytes())['source_and_fresh_case_verified'])


if __name__ == '__main__':
    unittest.main()
