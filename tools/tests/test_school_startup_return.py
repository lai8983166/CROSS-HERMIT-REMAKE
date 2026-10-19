import unittest
from tools.school_startup_return import *


class SourceTests(unittest.TestCase):
    def test_original_void_gamma_and_startup_stack_return_source(self):
        c=source_contract();self.assertEqual(c['gamma']['return_type'],'void');self.assertFalse(c['gamma']['HRESULT_available'])
        self.assertEqual(c['startup_ret_bytes'],20);self.assertEqual(c['startup_success'],0)
        self.assertEqual(c['return_trace'][-1],'0x413558')

    def test_owned_x86_capture_forwards_three_arguments_and_retains_actual_EAX(self):
        code=capture_code(0x12345678);self.assertEqual(len(code),25)
        ins=[(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(code,0x30000000)]
        self.assertEqual(ins,[('push','ebp'),('mov','ebp, esp'),('push','dword ptr [ebp + 0x10]'),
            ('push','dword ptr [ebp + 0xc]'),('push','dword ptr [ebp + 8]'),('mov','eax, 0x12345678'),
            ('call','eax'),('mov','esp, ebp'),('pop','ebp'),('ret','0xc')])

    def test_capture_refuses_null_wide_and_noninteger_targets(self):
        for target in (0,-1,0x100000000,'123'):
            with self.assertRaises(ValueError):capture_code(target)

    def test_gamma_channel_payload_and_remaining_upstream_boundary(self):
        self.assertEqual(len(gamma_bytes()),1536)
        self.assertFalse(source_contract()['inherited_cache_repaired']);self.assertFalse(source_contract()['retained_VM_advanced'])
