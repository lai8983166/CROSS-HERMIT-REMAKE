"""Frozen capsule regression and adversarial checks; no native jobs."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
from devtools.terminal_tcg_context_wait_verify_v3 import verify

ROOT = Path(__file__).resolve().parents[2]
CAPSULE = ROOT / 'analysis/terminal-wait-tcg-context-source-v1-20261111.zip'
SOURCE_SHA = '326e61eb38927e835ae2c0af4892233cd88bb67e2093da217176a59ea570818c'

def load():
    with zipfile.ZipFile(CAPSULE) as archive:
        data = gzip.decompress(archive.read('windows/observation.json.gz'))
        if hashlib.sha256(data).hexdigest() != SOURCE_SHA:
            raise ValueError('source identity')
        return json.loads(data), json.loads(archive.read('plan/trace-plan.json'))

def point(x, name):
    return next(p for p in x['points'] if p['label'] == name)

def step(x, name):
    return next(p for p in x['steps'] if p['label'] == name)

def cases():
    return [
      ('ret_cpu0_rax', lambda x: point(x,'ret32')['states'][0]['gpr'].__setitem__(0,'0000000000000001')),
      ('point_teb_owner', lambda x: point(x,'kernel-clear-before').__setitem__('owner_teb_client_id_hex','00'*8)),
      ('pxor_bytes', lambda x: step(x,'pxor-3').__setitem__('bytes_hex','90'*16)),
      ('duplicate_point', lambda x: x['points'].append(copy.deepcopy(x['points'][0]))),
      ('CR2_digest', lambda x: x['ledger_end'].__setitem__('events_sha256','0'*64)),
      ('filter_poison', lambda x: x['context_filter'][3].__setitem__('poisoned',True)),
      ('syscall_wrong_stop_thread', lambda x: step(x,'syscall').__setitem__('reply','T05thread:02;')),
      ('ret12_wrong_stop_thread', lambda x: step(x,'ret12').__setitem__('reply','T05thread:02;')),
      ('remove_selector13_point', lambda x: x.__setitem__('points',[p for p in x['points']if p['label']!='selector13'])),
      ('reverse_point_chronology', lambda x: x['points'].reverse()),
      ('reverse_step_chronology', lambda x: x['steps'].reverse()),
      ('kernel_entry_signature_corrupt', lambda x: point(x,'kernel-entry')['extra'].__setitem__('signature','00'*64)),
      ('filter_negative_rejection_count', lambda x: x['context_filter'][-1].__setitem__('rejected',-1)),
      ('filter_empty_points', lambda x: x['context_filter'][3].__setitem__('points',[])),
      ('filter_bool_counter', lambda x: x['context_filter'][0].__setitem__('accepted',False)),
      ('filter_changed_budget', lambda x: x['context_filter'][0]['budget'].__setitem__('seconds',61)),
      ('filter_over_budget', lambda x: x['context_filter'][-1].__setitem__('rejected',1000001)),
      ('filter_counter_regression', lambda x: x['context_filter'][-1].__setitem__('cpu_rejected',0)),
      ('filter_early_disable', lambda x: x['context_filter'][3].__setitem__('active',False)),
      ('filter_duplicate_point', lambda x: x['context_filter'][0]['points'].append(x['context_filter'][0]['points'][0])),
      ('call_opcode', lambda x: point(x,'call').__setitem__('code_hex','9090'+point(x,'call')['code_hex'][4:])),
      ('selector_saved_return', lambda x: point(x,'selector13')['extra'].__setitem__('saved_return','00000000')),
      ('selector_context_bytes', lambda x: point(x,'selector13')['extra'].__setitem__('context_bytes','00'*0x240)),
      ('wow_original_bytes', lambda x: point(x,'native-return').__setitem__('code_hex','00'*32)),
      ('kernel_original_bytes', lambda x: point(x,'kernel-clear-before').__setitem__('code_hex','00'*32)),
      ('raw_cpu_metadata_bool', lambda x: point(x,'call')['states'][0]['vp_stopped'][0].__setitem__('cpu',False)),
    ]

class ContextWait(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace, cls.plan = load()
    def test_original_capsule(self):
        result = verify(self.trace, self.plan)
        self.assertTrue(result['same_wait_writes_verified'], result['errors'])
        self.assertFalse(result['accepted'])
        self.assertFalse(result['original_game'])
        self.assertFalse(result['full_windows_admission'])
    def test_mutations(self):
        for name, mutate in cases():
            with self.subTest(name=name):
                trace = copy.deepcopy(self.trace); mutate(trace)
                self.assertFalse(verify(trace,self.plan)['same_wait_writes_verified'],name)
    def test_plan_path_tampering(self):
        plan = copy.deepcopy(self.plan); plan['kernel_path'] = '/etc/passwd'
        result = verify(self.trace,plan)
        self.assertFalse(result['same_wait_writes_verified'])
        self.assertEqual(result['errors'], ['ValueError: pinned_plan'])

if __name__ == '__main__':
    unittest.main()
