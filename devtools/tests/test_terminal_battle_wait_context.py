import ctypes as C
import itertools
import struct
import unittest
from types import SimpleNamespace
from devtools import terminal_battle_wait_context as m


class HeldContextTests(unittest.TestCase):
    def backend(self,foreign=False,fail_after=False,change_after=False,bad_restore=False):
        calls=[];counts={}
        def check(ok,msg):
            if not ok:raise OSError(msg)
        def ctx(h,p):
            calls.append(('ctx',h));counts[h]=counts.get(h,0)+1
            if fail_after and counts[h]==2:return 0
            raw=bytearray(716);struct.pack_into('<I',raw,0,0x1003f)
            struct.pack_into('<I',raw,180,0x20000);struct.pack_into('<I',raw,184,0x422360)
            struct.pack_into('<I',raw,196,0x1ff00)
            if change_after and counts[h]==2:raw[600]=1
            C.memmove(p,bytes(raw),716);return 1
        def op(name,result):
            def f(h):calls.append((name,h));return result
            return f
        api=SimpleNamespace(opent=lambda a,b,tid:1000+tid,ctx=ctx,check=check,
            suspend=op('suspend',2),resume=op('resume',2 if bad_restore else 3),
            close=op('close',1),memory=lambda h,p,n:None)
        b=SimpleNamespace(original=api,get_thread_pid=lambda h:9 if foreign else 7,get_thread_id=lambda h:h-1000)
        return b,calls

    def run_context(self,b,record,body=None):
        ticks=itertools.count(1)
        with m.observed_owned_frames(SimpleNamespace(pid=7,h=77),[8,9],record,lambda:next(ticks),b)as frames:
            if body:body(frames)

    def test_same_handles_full_extended_bytes_and_exact_restore(self):
        b,calls=self.backend();r={};self.run_context(b,r)
        self.assertTrue(r['complete'])
        self.assertTrue(all(x['all_716_bytes_equal']for x in r['threads']))
        self.assertEqual([x['handle']for x in r['threads']],[1008,1009])
        self.assertEqual(calls[-6:],[('ctx',1008),('ctx',1009),('resume',1009),('resume',1008),('close',1009),('close',1008)])
        for x in r['threads']:
            a,z=x['contexts'];self.assertLessEqual(a['qpc_end'],r['data_scope_begin_qpc'])
            self.assertLessEqual(r['data_scope_end_qpc'],z['qpc_begin'])

    def test_extended_register_change_is_never_masked(self):
        b,_=self.backend(change_after=True);r={};self.run_context(b,r)
        self.assertTrue(r['complete'])
        self.assertFalse(any(x['all_716_bytes_equal']for x in r['threads']))
        self.assertEqual(bytes.fromhex(r['threads'][0]['contexts'][1]['raw_hex'])[600],1)

    def test_ending_context_failure_still_restores_both_owned_increments(self):
        b,calls=self.backend(fail_after=True);r={}
        with self.assertRaisesRegex(OSError,'ending context'):self.run_context(b,r)
        self.assertFalse(r['complete']);self.assertEqual(calls[-4:],[('resume',1009),('resume',1008),('close',1009),('close',1008)])

    def test_body_failure_has_no_fabricated_ending_context(self):
        b,calls=self.backend();r={}
        with self.assertRaisesRegex(RuntimeError,'read failed'):
            self.run_context(b,r,lambda _:(_ for _ in ()).throw(RuntimeError('read failed')))
        self.assertFalse(r['complete']);self.assertTrue(all(len(x['contexts'])==1 for x in r['threads']))
        self.assertEqual(calls[-4:],[('resume',1009),('resume',1008),('close',1009),('close',1008)])

    def test_foreign_owner_never_suspended(self):
        b,calls=self.backend(foreign=True);r={}
        with self.assertRaisesRegex(ValueError,'before suspension'):self.run_context(b,r)
        self.assertEqual(calls,[('close',1008)]);self.assertFalse(r['complete'])

    def test_restore_failure_cannot_be_complete(self):
        b,calls=self.backend(bad_restore=True);r={}
        with self.assertRaisesRegex(ValueError,'restore count'):self.run_context(b,r)
        self.assertFalse(r['complete']);self.assertEqual(calls[-2:],[('close',1009),('close',1008)])


if __name__=='__main__':unittest.main()
