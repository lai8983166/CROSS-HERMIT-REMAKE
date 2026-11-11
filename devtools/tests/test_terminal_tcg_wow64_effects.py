"""Replay the retained native observations; reject changes outside exact effects."""
import copy
import json
from pathlib import Path
import unittest
import zipfile

from devtools.terminal_tcg_wow64_effects_v3 import verify


class NativeEffects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2]
        capsule = root / 'analysis/terminal-wait-tcg-wow64-source-v1-20261111.zip'
        with zipfile.ZipFile(capsule) as archive:
            cls.trace = json.loads(archive.read('tcg-wait-native-v4/wow64-trace.json'))
            cls.plan = json.loads(archive.read('tcg-wow64-path-v1/trace-plan.json'))

    def test_actual_local_effects_not_acceptance(self):
        result = verify(self.trace, self.plan)
        self.assertTrue(result['local_effects_verified'])
        for name in ('accepted', 'cr2_explained', 'consumer_connected_in_this_trace'):
            self.assertFalse(result[name])

    def test_state_and_source_tampering_rejected(self):
        for mutation in ('cr2', 'hflags', 'opcode', 'return', 'missing', 'thread', 'xmm', 'cpu', 'duplicate', 'schema', 'bits_type', 'stopped_type'):
            with self.subTest(mutation=mutation):
                trace = copy.deepcopy(self.trace)
                step = next(s for s in trace['steps'] if s['label'] == 'load-r9d')
                if mutation == 'cr2':
                    step['after'][0]['cr0_cr2_cr3_cr4'][1] = '0000000000000001'
                elif mutation == 'hflags':
                    state = step['after'][0]
                    state[mutation] = f'{int(state[mutation], 16) ^ 1:016x}'
                elif mutation == 'opcode':
                    step['bytes_hex'] = '90' + step['bytes_hex'][2:]
                elif mutation == 'return':
                    next(p for p in trace['points'] if p['label'] == 'return-branch')['extra']['saved_return'] = '00000000'
                elif mutation == 'missing':
                    trace['steps'].remove(step)
                elif mutation == 'thread':
                    step['reply'] = 'T05thread:02;'
                elif mutation == 'cpu':
                    step['before'][0]['cpu'] = step['after'][0]['cpu'] = 1
                    next(p for p in trace['points'] if p['label'] == 'return-branch')['states'][0]['cpu'] = 1
                elif mutation == 'duplicate':
                    trace['steps'].insert(0, copy.deepcopy(step))
                elif mutation in ('bits_type', 'stopped_type', 'schema'):
                    def mutate(state):
                        if mutation == 'schema':
                            state.pop('cr0_cr2_cr3_cr4')
                        elif mutation == 'bits_type':
                            state['target_bits'] = 64.0
                        else:
                            state['vp_stopped'][0]['stopped'] = 1
                    for point in trace['points']:
                        for state in point['states']:
                            mutate(state)
                    for item in trace['steps']:
                        for state in item['before'] + item['after']:
                            mutate(state)
                else:
                    next(s for s in trace['steps'] if s['label'] == 'pxor-2')['after'][0]['xmm_low64_high64'][2][0] = '0000000000000001'
                self.assertFalse(verify(trace, self.plan)['local_effects_verified'])


if __name__ == '__main__':
    unittest.main()
