import hashlib
import json
import unittest
from copy import deepcopy
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_world_admission import source_contract, START, END, STACK, UNITCTRL, RETURN, ROOT
from tools.tactics_exit_emulation import SOURCE, BASE


def expected_visits(gate):
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    code = {i.address:i for i in md.disasm(SOURCE.read_bytes()[START-BASE:END-BASE], START)}
    seen, pc = [], START
    for _ in range(100):
        instruction = code[pc]; seen.append(pc)
        if instruction.mnemonic == 'ret': break
        if instruction.mnemonic == 'call' and instruction.op_str == '0x4678c0': break
        if instruction.mnemonic == 'jmp': pc = int(instruction.op_str,16)
        elif instruction.mnemonic == 'jne': pc = int(instruction.op_str,16) if gate else pc+instruction.size
        else: pc += instruction.size
    else: raise ValueError('world expected bounded source path')
    return sorted(seen)


def verify_case(case):
    result = case['world_admission']
    actual, closed = result['actual_captured_entry'], result['declared_zero_gate_return']
    if actual['captured_gate'] != 1 or actual['visited'] != expected_visits(1) or closed['visited'] != expected_visits(0):
        raise ValueError('world gate path')
    if actual['pending'] != {'va':'0x4678c0','receiver':UNITCTRL,'sp':STACK+0xFF00-92,'return_va':'0x46b4b2'}:
        raise ValueError('world natural child stack')
    if actual['before_control_hex'] != actual['after_control_hex'] or closed['return_sp'] != STACK+0xFF04:
        raise ValueError('world control/return')
    for entry in [actual,closed]:
        if not entry['retained_ranges_unchanged'] or entry['retained_bytes'] < 100000000:
            raise ValueError('world retained memory')
    if not result['captured_parent_restored'] or result['full_world_tick_executed'] or result['enemy_AI_executed']:
        raise ValueError('world execution scope')
    return True


class WorldAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-night-world-admission-v2-20261014.json').read_text('utf-8'))

    def test_contract_and_three_actual_source_paths_full_retention(self):
        self.assertEqual(self.report['source_contract'], source_contract())
        self.assertEqual([c['name'] for c in self.report['cases']], ['initial','student9_waiting','fifth_class'])
        for case in self.report['cases']: self.assertTrue(verify_case(case))

    def test_wrong_gate_stack_retention_and_claims_refuse(self):
        case = self.report['cases'][0]
        for key,value in [('captured_gate',0),('visited',[]),('after_control_hex','00'),('retained_ranges_unchanged',False)]:
            bad = deepcopy(case); bad['world_admission']['actual_captured_entry'][key] = value
            with self.assertRaises(ValueError): verify_case(bad)
        bad = deepcopy(case); bad['world_admission']['actual_captured_entry']['pending']['return_va'] = '0x0'
        with self.assertRaises(ValueError): verify_case(bad)
        bad = deepcopy(case); bad['world_admission']['full_world_tick_executed'] = True
        with self.assertRaises(ValueError): verify_case(bad)


if __name__ == '__main__': unittest.main()
