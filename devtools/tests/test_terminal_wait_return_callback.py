"""Synthetic machine-code tests; never execute any native Windows callback."""
import struct
import unittest
import unicorn
from unicorn import x86_const as x
from devtools import terminal_wait_return_callback as c

CODE=0x100000
DATA=0x200000
STACK=0x400000
SP=STACK+0x800
PC=CODE+0x800
TID=17
REGS=[x.UC_X86_REG_EAX,x.UC_X86_REG_ECX,x.UC_X86_REG_EDX,x.UC_X86_REG_EBX,
      x.UC_X86_REG_ESP,x.UC_X86_REG_EBP,x.UC_X86_REG_ESI,x.UC_X86_REG_EDI]


def emulated(tid=TID,pc=PC,count=0,low=STACK,high=STACK+0x2000,status=0,caller=None,stackcaller=None):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_32)
    for start,size in [(0,4096),(CODE,4096),(DATA,c.ALLOCATION),(STACK,0x2000)]:u.mem_map(start,size)
    u.mem_write(CODE,c.emit_callback(DATA,TID,PC,caller))
    u.mem_write(4,struct.pack('<II',high,low));u.mem_write(0x24,struct.pack('<I',tid))
    u.mem_write(DATA,struct.pack('<I',count))
    u.mem_write(SP,bytes(range(256))*3)
    if stackcaller is not None:u.mem_write(SP,struct.pack("<I",stackcaller))
    values=[status,pc,0x3456,0x4567,SP,0x5678,0x6789,0x789a]
    for reg,val in zip(REGS,values):u.reg_write(reg,val)
    u.reg_write(x.UC_X86_REG_EFLAGS,0xed7) # includes DF, no TF; callback must restore
    u.reg_write(x.UC_X86_REG_XMM0,0x123456789abcdef0123456789abcdef0)
    before=[u.reg_read(r)for r in REGS+[x.UC_X86_REG_EFLAGS,x.UC_X86_REG_XMM0]]
    u.emu_start(CODE,pc,count=10000)
    after=[u.reg_read(r)for r in REGS+[x.UC_X86_REG_EFLAGS,x.UC_X86_REG_XMM0]]
    return before,after,bytes(u.mem_read(DATA,c.ALLOCATION))


class CallbackTests(unittest.TestCase):
    def test_complete_decode_and_no_call(self):
        image,meta=c.build_image()
        c.audit_image(image,meta)
        self.assertLess(len(image),4096)
        self.assertEqual(c.emit_callback(DATA,TID,PC)[:2],b'\x9c\x60')

    def test_preservation_and_real_entry_snapshot(self):
        for status in [0,0x102,0xc0000008]:
            before,after,data=emulated(status=status)
            self.assertEqual(before,after)
            r=data[64:64+c.SLOT]
            self.assertEqual(c.u32(data,0),1)
            self.assertEqual([c.u32(r,i)for i in (4,8,12,24,28)],[TID,PC,SP,768,0])
            self.assertEqual(c.u32(r,60),status)
            self.assertEqual(r[c.STACK_OFFSET:c.STACK_OFFSET+768],bytes(range(256))*3)

    def test_filters_restore_even_when_df_set(self):
        for kwargs in [dict(tid=99),dict(pc=PC+16)]:
            before,after,data=emulated(**kwargs)
            self.assertEqual(before,after)
            self.assertEqual(data,bytes(c.ALLOCATION))

    def test_overflow_and_stack_bounds(self):
        before,after,data=emulated(count=8)
        self.assertEqual(before,after)
        self.assertEqual([c.u32(data,i)for i in (0,4)],[8,1])
        self.assertEqual(data[64:],bytes(c.ALLOCATION-64))
        before,after,data=emulated(low=SP+1)
        self.assertEqual(before,after)
        self.assertEqual([c.u32(data,i)for i in (0,8,64+24,64+28)],[1,1,0,1])
        before,after,data=emulated(high=SP+128)
        self.assertEqual(before,after)
        self.assertEqual(c.u32(data,64+24),128)
        self.assertEqual(data[64+c.STACK_OFFSET+128:64+c.STACK_OFFSET+768],bytes(640))

    def test_actual_caller_filter(self):
        for stackcaller,expected in [(1234,1),(5678,0)]:
            before,after,data=emulated(caller=1234,stackcaller=stackcaller)
            self.assertEqual(before,after)
            self.assertEqual(c.u32(data,0),expected)
        before,after,data=emulated(caller=1234,stackcaller=1234,high=SP+3)
        self.assertEqual(before,after)
        self.assertEqual(c.u32(data,0),0)

    def test_alignment_rejected(self):
        with self.assertRaises(ValueError):c.emit_callback(DATA+1,TID,PC)


if __name__=='__main__':unittest.main()
