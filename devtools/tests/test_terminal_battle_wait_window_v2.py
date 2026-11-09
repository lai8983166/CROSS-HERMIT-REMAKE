import copy
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from devtools import terminal_battle_wait_window_v2 as v


def fixture(cls=v.WaitWindow):
    obj=cls.__new__(cls);memory={10:b'code',20:b'wait',30:b'iat!',40:b'tls!'}
    obj.c=SimpleNamespace(main=100,get=lambda p,n:memory[p][:n]);obj.lock=threading.RLock();obj.kernel=object()
    obj.active=False;obj.finished=False;obj.session=None;obj.thread_handle=None
    obj.result=dict(original_code=[dict(pointer=10,hex=memory[10].hex())],
        API_exports=[dict(target=20,entry_hex=memory[20].hex(),slot=30,IAT_hex=memory[30].hex())],
        TLS_implementation=dict(target=40,code_hex=memory[40].hex()))
    return obj,memory


class PreparedWindowTests(unittest.TestCase):
    def test_fixed_original_split_has_no_prepare_work_in_trigger(self):
        prepare,begin=v.split_original_begin()
        self.assertIn('kernel_wait_identity',prepare.__code__.co_names)
        self.assertNotIn('kernel_wait_identity',begin.__code__.co_names)
        self.assertNotIn('tls_contract',begin.__code__.co_names)
        self.assertIn('snapshot',begin.__code__.co_names)
        self.assertIn('event_identity',begin.__code__.co_names)
        self.assertIn('duplicate',begin.__code__.co_names)
        with patch.object(v,'identity',return_value={'sha256':'0'*64}):
            with self.assertRaises(ValueError):v.split_original_begin()

    def test_prepare_then_live_recheck_then_original_tail(self):
        obj,memory=fixture();calls=[]
        with patch.object(v.original,'utc_now_ns',side_effect=[1,2,3,4]), \
             patch.object(v,'_prepare_original',side_effect=lambda s:calls.append('prepare')), \
             patch.object(v,'_begin_original',side_effect=lambda s:calls.append('begin')):
            obj.prepare();obj.begin()
        self.assertEqual(calls,['prepare','begin'])
        self.assertEqual(obj.result['preparation']['end_ns'],2)
        self.assertEqual(obj.result['prepared_trigger']['begin_ns'],3)
        self.assertFalse(obj.result['preparation']['thread_duplicate_created'])

    def test_missing_preparation_and_changed_live_bytes_reject_before_start(self):
        for address in (None,10,20,30,40):
            obj,memory=fixture()
            if address is not None:obj.prepared=True;memory[address]=b'BAD!'
            with patch.object(v.original,'utc_now_ns',return_value=1),patch.object(v,'_begin_original')as start:
                with self.assertRaises(ValueError):obj.begin()
                start.assert_not_called()

    def test_preparation_is_one_shot_and_cannot_start_resources(self):
        obj,_=fixture()
        with patch.object(v.original,'utc_now_ns',return_value=1),patch.object(v,'_prepare_original'):
            obj.prepare()
            with self.assertRaises(ValueError):obj.prepare()
        obj,_=fixture()
        with patch.object(v.original,'utc_now_ns',return_value=1), \
             patch.object(v,'_prepare_original',side_effect=lambda s:setattr(s,'active',True)):
            with self.assertRaises(ValueError):obj.prepare()

    def test_real_thread_concurrency_rehearsal_keeps_original_deadline(self):
        obj,_=fixture(v.PreflightWindow);obj.c.get=lambda p,n:bytes(n);polls=[];thread_ids=[]
        obj.poll=lambda:polls.append(threading.get_ident())
        def begin(s):thread_ids.append(threading.get_ident());time.sleep(.02)
        with patch.object(v.original,'utc_now_ns',side_effect=[1,2]),patch.object(v.WaitWindow,'begin',begin):
            obj.begin()
        receipt=obj.result['trigger_concurrency_preflight']
        self.assertNotEqual(thread_ids[0],threading.get_ident());self.assertTrue(polls)
        self.assertTrue(receipt['input_window']['complete']);self.assertEqual(receipt['input_window']['maximum_seconds'],11)
        self.assertFalse(receipt['input_submitted']);self.assertIsNone(receipt['trigger_error'])

    def test_failed_real_trigger_is_not_a_successful_preflight(self):
        obj,_=fixture(v.PreflightWindow);obj.c.get=lambda p,n:bytes(n);obj.poll=lambda:None
        with patch.object(v.original,'utc_now_ns',side_effect=[1,2]), \
             patch.object(v.WaitWindow,'begin',side_effect=ValueError('actual trigger rejected')):
            with self.assertRaises(ValueError):obj.begin()
        self.assertIn('actual trigger rejected',obj.result['trigger_concurrency_preflight']['trigger_error'])


if __name__=='__main__':unittest.main()
