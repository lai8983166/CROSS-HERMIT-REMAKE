import struct
import unittest
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import patch
from devtools import terminal_debug_relay as relay


class DebugOwnershipTests(unittest.TestCase):
    def context(self,dr7):
        b=bytearray(716);struct.pack_into('<I',b,24,dr7);return b
    def test_reserved_control_bits_are_not_enabled_breakpoints(self):
        self.assertTrue(relay.unused_debug_registers(self.context(0x400)))
        self.assertTrue(relay.unused_debug_registers(self.context(0)))
    def test_any_enabled_local_global_slot_or_general_detect_rejected(self):
        for bit in (*range(8),13):
            with self.subTest(bit=bit):self.assertFalse(relay.unused_debug_registers(self.context(0x400|(1<<bit))))
        self.assertFalse(relay.unused_debug_registers(b''))
    def test_exact_null_slots_require_actual_free_zero_page(self):
        c=self.context(0x155);region=dict(base=0,size=65536,state=0x10000,protect=0)
        self.assertTrue(relay.null_execution_slots(c,region))
        for altered in (dict(region,state=0x1000),dict(region,base=4096),dict(region,size=4096)):
            self.assertFalse(relay.null_execution_slots(c,altered))
        for offset,value in ((4,0x422360),(24,0x155|0x10000),(24,0x155|0x2000)):
            b=bytearray(c);struct.pack_into('<I',b,offset,value)
            self.assertFalse(relay.null_execution_slots(b,region))
    def test_only_our_enabled_execution_stop_claimed(self):
        b=self.context(0x401)
        for offset,value in ((4,0x70001000),(20,1),(184,0x70001000)):struct.pack_into('<I',b,offset,value)
        targets=(0x70001000,0,0,0)
        self.assertTrue(relay.own_hardware_stop(b,targets,1))
        for offset,value in ((4,0x70002000),(20,0x4001),(20,0x2001),(24,0x400),(184,0x70002000)):
            with self.subTest(offset=offset,value=value):
                c=bytearray(b);struct.pack_into('<I',c,offset,value)
                self.assertFalse(relay.own_hardware_stop(c,targets,1))


class RelayFailureTests(unittest.TestCase):
    def simulate(self,overflow=False):
        calls=[];contexts={};events=[]
        def context(h):
            if h not in contexts:
                b=bytearray(716);struct.pack_into('<I',b,24,0x400);contexts[h]=bytes(b)
            return contexts[h]
        native_break=relay.C.cast(relay.C.WinDLL('ntdll').DbgBreakPoint,relay.C.c_void_p).value
        events.append((3,0))
        if overflow:events.extend([(6,0)]*263+[(1,0xC0000005)])
        else:events.append((1,0x80000003))
        def wait_event(pointer,ms):
            e=pointer._obj;code,exception=events.pop(0);e.code=code;e.pid=99;e.tid=300
            if code==3:e.u.create.thread=101;e.u.create.process=102;e.u.create.file=0
            elif code==1:
                e.u.exception.record.code=exception;e.u.exception.record.address=native_break;e.u.exception.first=1
            else:e.u.file=0
            return True
        def instrument(h,targets,mask):
            calls.append(('instrument',h,mask));old=context(h);b=bytearray(old)
            for off,value in zip((4,8,12,16,20,24),(*targets,0,mask)):struct.pack_into('<I',b,off,value)
            contexts[h]=bytes(b)
            if h==501 and mask==1:raise ValueError('readback failed after real DR write')
            return dict(before_context_hex=old.hex(),after_context_hex=bytes(b).hex())
        replacements={
            (relay.debug,'attach'):lambda p:True,(relay.debug,'context'):context,
            (relay.debug,'wait_event'):wait_event,
            (relay.debug,'continue_event'):lambda p,t,s:calls.append(('continue',p,t,s))or True,
            (relay.debug,'required'):lambda h,a,n:b'\xcc'*n,
            (relay.win,'threads'):lambda p:[200],(relay.win,'opent'):lambda *a:501,
            (relay.win,'suspend'):lambda h:calls.append(('suspend',h))or 0,
            (relay.win,'resume'):lambda h:calls.append(('resume',h))or 1,
            (relay.win,'close'):lambda h:calls.append(('close',h))or True,
            (relay,'own_duplicate'):lambda h:h+1000,
            (relay,'instrument'):instrument,(relay,'detach'):lambda p:True,
            (relay,'kill_on_exit'):lambda enabled:True,
            (relay,'get_thread_id'):lambda h:300,(relay,'get_process_id'):lambda h:99,
            (relay,'resolve'):lambda p,m,s:dict(target=0x70003000 if s=='NtDebugContinue'else 0x70002000),
        }
        with ExitStack()as stack:
            stack.enter_context(patch('devtools.terminal_wait_observer_gate.require_supported_relay'))
            stack.enter_context(patch('devtools.native_input_isolation.require_qualified_guest',return_value={}))
            for (obj,name),value in replacements.items():stack.enter_context(patch.object(obj,name,value))
            result=relay.observe(SimpleNamespace(pid=100),SimpleNamespace(pi=SimpleNamespace(pid=99),members=lambda:[99,100]),
                200,0x422360,lambda c:({},None),seconds=1,maximum_hits=1)
        return result,calls
    def test_failed_first_child_readback_still_restores_debug_state(self):
        r,calls=self.simulate()
        self.assertIn('readback failed',r['error'])
        self.assertTrue(r['cleanup']['child_debug_registers_restored'])
        self.assertIn(('instrument',501,0x400),calls)
        self.assertEqual(sum(c[0]=='suspend'for c in calls),sum(c[0]=='resume'for c in calls))
        self.assertNotIn(('close',101),calls) # borrowed event handle is never manually closed
        self.assertIn(('close',1101),calls) # only our duplicate
    def test_over_budget_pending_exception_is_forwarded(self):
        r,calls=self.simulate(overflow=True)
        self.assertIn('bounded parent debug events',r['error'])
        continuations=[c for c in calls if c[0]=='continue']
        self.assertEqual(continuations[-1],('continue',99,300,0x80010001))


if __name__=='__main__':unittest.main()
