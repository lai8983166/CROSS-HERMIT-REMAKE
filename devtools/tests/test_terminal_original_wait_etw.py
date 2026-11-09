import ctypes as C
import struct
from pathlib import Path
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from devtools import terminal_original_wait_etw as probe


class OriginalWaitCollectorTests(unittest.TestCase):
    def test_host_rejected_before_kernel_API_or_output(self):
        with patch('devtools.native_input_isolation.require_qualified_guest',side_effect=ValueError('not guest')):
            with patch.object(probe,'kernel_wait_identity',side_effect=AssertionError('native must not run')):
                with self.assertRaisesRegex(ValueError,'not guest'):
                    probe.run(Path('not-created.json.gz'))
            with self.assertRaisesRegex(ValueError,'not guest'):
                probe.kernel_wait_identity()

    def test_kernel_path_is_exact_not_generic_driver(self):
        self.assertEqual(probe.kernel_path(r'\SystemRoot\system32\ntoskrnl.exe','C:/Windows'),
                         Path('C:/Windows/System32/ntoskrnl.exe').resolve())
        for value in ('C:/other/ntoskrnl.exe','C:/Windows/System32/drivers/other.sys',
                      r'\SystemRoot\..\other\ntoskrnl.exe'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                probe.kernel_path(value,'C:/Windows')

    def test_clock_uses_precise_FILETIME_without_offset_guess(self):
        class Kernel:
            @staticmethod
            def GetSystemTimePreciseAsFileTime(p):
                C.cast(p,C.POINTER(C.c_uint64)).contents.value=116444736012345678
        self.assertEqual(probe.utc_now_ns(Kernel()),1234567800)

    def test_trace_keeps_thread_syscall_switch_and_original_loss_limits(self):
        buf, p = probe.trace_properties(Path('C:/owned/trace.etl'))
        self.assertEqual(p.EnableFlags,0x92)
        self.assertEqual((p.MaximumFileSize,p.MinimumBuffers,p.MaximumBuffers),(4,4,8))
        self.assertEqual(p.Wnode.ClientContext,1)

    def test_raw_stack_ranges_preserve_links_and_original_wait_parameters(self):
        reads=[]
        class Reader:
            @staticmethod
            def get(p,n):
                reads.append((p,n));return bytes(n)
        frame=dict(ESP=0x1000,chain=[dict(bp=0x1100,saved_bp=0x1200,return_va=0x42240D),
                                  dict(bp=0x1200,saved_bp=0x1300,return_va=0x45E9D0)])
        rows=probe.stack_regions(Reader(),frame)
        self.assertIn((0x1100,16),reads)
        self.assertIn((0x11A0,0x70),reads)
        self.assertIn((0x1200,8),reads)
        self.assertEqual(sum(len(bytes.fromhex(r['hex']))for r in rows),sum(n for p,n in reads))

    def test_wait_for_actual_registration_instead_of_ready_main(self):
        self.assertIsNone(probe.startup_candidate([],0x599020))
        head=bytearray(48);struct.pack_into('<I',head,0,0x599020)
        row=dict(pointer=0x50000,head_hex=head.hex())
        self.assertIsNone(probe.startup_candidate([row],0x599020))
        struct.pack_into('<III',head,0x1C,100,104,108);row['head_hex']=head.hex()
        self.assertEqual(probe.startup_candidate([row],0x599020),row)
        with self.assertRaisesRegex(ValueError,'ambiguous'):
            probe.startup_candidate([row,dict(row,pointer=0x60000)],0x599020)

    def thread_backend(self, foreign=False, context_error=False):
        calls=[]
        def check(ok,message):
            if not ok:raise OSError(message)
        def suspend(h):calls.append(('suspend',h));return 2
        def resume(h):calls.append(('resume',h));return 3
        def close(h):calls.append(('close',h));return 1
        def context(h,p):
            calls.append(('context',h))
            if context_error:return 0
            data=bytearray(716);struct.pack_into('<I',data,180,0x20000)
            struct.pack_into('<I',data,184,0x422360);struct.pack_into('<I',data,196,0x1FF00)
            C.memmove(p,bytes(data),716);return 1
        api=SimpleNamespace(opent=lambda access,inherit,tid:1000+tid,check=check,
            suspend=suspend,resume=resume,close=close,ctx=context,memory=lambda h,bp,n:None)
        return SimpleNamespace(original=api,get_thread_pid=lambda h:999 if foreign else 7,
            get_thread_id=lambda h:h-1000),calls

    def test_foreign_thread_handle_rejected_before_suspend(self):
        b,calls=self.thread_backend(foreign=True)
        with self.assertRaisesRegex(ValueError,'before suspension'):
            with probe.owned_frames(SimpleNamespace(pid=7,h=77),[8],b):pass
        self.assertEqual(calls,[('close',1008)])

    def test_context_failure_restores_only_owned_suspend_increment(self):
        b,calls=self.thread_backend(context_error=True)
        with self.assertRaisesRegex(OSError,'context'):
            with probe.owned_frames(SimpleNamespace(pid=7,h=77),[8],b):pass
        self.assertEqual(calls,[('suspend',1008),('context',1008),('resume',1008),('close',1008)])

    def test_same_retained_handles_restored_in_reverse_order(self):
        b,calls=self.thread_backend()
        with probe.owned_frames(SimpleNamespace(pid=7,h=77),[8,9],b)as frames:
            self.assertEqual([x['tid']for x in frames],[8,9])
            self.assertTrue(all(x['owner_verified_before_suspend']for x in frames))
        self.assertEqual(calls[-4:],[('resume',1009),('resume',1008),('close',1009),('close',1008)])


if __name__=='__main__':unittest.main()
