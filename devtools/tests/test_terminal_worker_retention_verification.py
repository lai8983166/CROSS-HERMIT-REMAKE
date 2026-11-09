"""Pure synthetic contracts: no native calls and no generated proof sources."""
import copy
import struct
import unittest
from unittest.mock import patch
from devtools import terminal_worker_retention_verification as v


def frame(tid,returns=()):
    data=bytearray(716);struct.pack_into('<I',data,0,0x1003F)
    bp=0x110000;ip=0x401000;sp=0x10FF00
    for at,value in ((180,bp),(184,ip),(196,sp)):struct.pack_into('<I',data,at,value)
    return dict(tid=tid,context_hex=data.hex(),EBP=bp,EIP=ip,ESP=sp,
        chain=[dict(bp=bp+i*16,saved_bp=bp+(i+1)*16,return_va=ret)for i,ret in enumerate(returns)],
        owner_verified_before_suspend=True,previous_suspend_count=0)


def fixture():
    raw=v.frozen.menu.contract.read_source();main=0x210000;ptr=0x220000;tid=22;vt=v.frozen.UI
    head=bytearray(64)
    for at,value in ((0,vt),(8,main+0x64),(0x1C,0xCDCDCDCD),(0x20,0xCDCDCDCD),(0x24,tid)):
        struct.pack_into('<I',head,at,value)
    task=dict(pointer=ptr,thread_id=tid,vtable=vt,header_hex=head.hex(),
              vtable_hex=raw[vt-0x400000:vt-0x400000+8].hex())
    manager=bytearray(0x120);struct.pack_into('<I',manager,0,ptr);struct.pack_into('<I',manager,0x118,44)
    row=dict(elapsed=1.0,game=0x230000,frames=[frame(11),frame(tid)],tasks=[task],manager_hex=manager.hex(),
        registered_tasks=[dict(pointer=ptr,bucket=0,head_hex=head[:48].hex())],MAIN_event_hex=bytes(8).hex())
    for name,size in [('keyboard_hex',0xA00),('mouse_hex',0x58),('scenario_hex',80),('VM_hex',128),('group90_hex',8)]:
        row[name]=bytes(size).hex()
    row['worker_retention']=dict(version=1,pid=99,main_tid=11,capture_begin_perf_ns=100,capture_end_perf_ns=200,
        cohort_tids=[11,tid],retained_while_suspended=True,tasks=[dict(pointer=ptr,thread_id=tid,
        remote_handle=0xCDCDCDCD,event=0xCDCDCDCD,observed_context_present=True,status='pending_callback_ancestry')])
    p=dict(pid=99,main=main,startup=dict(window=dict(main_tid=11)),manager_event=dict(remote_handle=44))
    return row,p,raw


class WorkerRetentionVerificationTests(unittest.TestCase):
    def setUp(self):self.row,self.p,self.raw=fixture()

    def test_pending_keeps_raw_graph_and_old_verifier_stays_strict(self):
        before=copy.deepcopy(self.row);ns=v.adapted_namespace()
        self.assertEqual(ns['verify_task_row'](self.row,self.p,self.raw,self.row['game'],{}),0)
        self.assertEqual(self.row,before)
        with self.assertRaisesRegex(ValueError,'retained current original worker'):
            v.frozen.verify_task_row(self.row,self.p,self.raw,self.row['game'],{})
        self.row['registered_tasks'][0]['bucket']=1
        with self.assertRaisesRegex(ValueError,'bucket'):
            ns['verify_task_row'](self.row,self.p,self.raw,self.row['game'],{})

    def test_partial_and_complete_ancestry_cannot_be_pending(self):
        for ancestors in ((0x421F8A,),(0x56E183,),(0x421F8A,0x56E183)):
            with self.subTest(ancestors=ancestors):
                row=copy.deepcopy(self.row);row['frames'][1]=frame(22,ancestors)
                with self.assertRaisesRegex(ValueError,'partial callback'):
                    v.retention_contract(row,self.p,{})

    def test_dropped_tls_cannot_be_pending_or_retained(self):
        row=self.row;row['frames'][1]=frame(22,(0x421F8A,0x56E183))
        proof=row['worker_retention']['tasks'][0];proof['status']='already_retained'
        workers={(0x220000,22):dict(first_elapsed=.5,original_handle=0xCDCDCDCD,
            vtable=v.frozen.UI,event=dict(remote_handle=0xCDCDCDCD))}
        with self.assertRaisesRegex(ValueError,'cannot omit TLS'):
            v.retention_contract(row,self.p,workers)
        proof['status']='retained';workers[(0x220000,22)]['first_elapsed']=1.0
        with self.assertRaisesRegex(ValueError,'complete callback ancestry and TLS'):
            v.retention_contract(row,self.p,workers)

    def test_pending_input_target_rejected(self):
        with self.assertRaisesRegex(ValueError,'input target'):
            v.require_input_owner(self.row,self.row['tasks'][0],self.p,{})
        self.row['tasks'][0]['TLS']={}
        with self.assertRaisesRegex(ValueError,'TLS'):
            v.require_input_owner(self.row,self.row['tasks'][0],self.p,{})

    def test_already_retained_partial_crt_frame_is_not_a_pending_or_input_owner(self):
        row=self.row;row['frames'][1]=frame(22,(0x56E183,))
        proof=row['worker_retention']['tasks'][0];proof['status']='already_retained'
        workers={(0x220000,22):dict(first_elapsed=.5,original_handle=0xCDCDCDCD,
            vtable=v.frozen.UI,event=dict(remote_handle=0xCDCDCDCD))}
        self.assertEqual(v.retention_contract(row,self.p,workers),set())
        self.assertEqual(v.adapted_namespace()['verify_task_row'](
            row,self.p,self.raw,row['game'],workers),0)
        with self.assertRaisesRegex(ValueError,'input target'):
            v.require_input_owner(row,row['tasks'][0],self.p,workers)
        proof['status']='pending_callback_ancestry'
        with self.assertRaisesRegex(ValueError,'partial callback'):
            v.retention_contract(row,self.p,workers)
        proof['status']='retained';workers[(0x220000,22)]['first_elapsed']=1.0
        with self.assertRaisesRegex(ValueError,'first retention requires complete'):
            v.retention_contract(row,self.p,workers)

    def test_partial_crt_frame_cannot_claim_current_tls(self):
        row=self.row;row['frames'][1]=frame(22,(0x56E183,))
        row['tasks'][0]['TLS']={}
        row['worker_retention']['tasks'][0]['status']='already_retained'
        workers={(0x220000,22):dict(first_elapsed=.5,original_handle=0xCDCDCDCD,
            vtable=v.frozen.UI,event=dict(remote_handle=0xCDCDCDCD))}
        with self.assertRaisesRegex(ValueError,'one original ancestor'):
            v.retention_contract(row,self.p,workers)
        with self.assertRaisesRegex(ValueError,'one original ancestor'):
            v.require_input_owner(row,row['tasks'][0],self.p,workers)

    def test_identity_cohort_and_raw_context_tamper(self):
        changes=[lambda r:r['worker_retention'].update(pid=100),
                 lambda r:r['worker_retention'].update(cohort_tids=[11]),
                 lambda r:r['worker_retention']['tasks'][0].update(remote_handle=5),
                 lambda r:r['worker_retention']['tasks'][0].update(observed_context_present=False),
                 lambda r:r['frames'][1].update(EIP=0x401001),
                 lambda r:r['frames'][1].update(owner_verified_before_suspend=False)]
        for change in changes:
            row=copy.deepcopy(self.row);change(row)
            with self.assertRaises(ValueError):v.retention_contract(row,self.p,{})

    def test_later_worker_does_not_retroactively_bind_pending_handle(self):
        workers={(0x220000,22):dict(first_elapsed=2.0,original_handle=88,
                                  vtable=v.frozen.UI,event=dict(remote_handle=77))}
        ns=v.adapted_namespace()
        self.assertEqual(ns['verify_task_row'](self.row,self.p,self.raw,self.row['game'],workers),0)
        workers[(0x220000,22)]['first_elapsed']=.5
        with self.assertRaisesRegex(ValueError,'strictly precedes'):
            v.retention_contract(self.row,self.p,workers)

    def test_ordinary_row_cannot_use_supplemental_exemption(self):
        del self.row['worker_retention']
        with self.assertRaisesRegex(ValueError,'requires atomic'):
            v.adapted_namespace()['verify_task_row'](self.row,self.p,self.raw,self.row['game'],{})

    def test_frozen_hash_ast_shape_and_scoped_globals(self):
        with patch.object(v,'PARENT_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'frozen school verifier SHA'):v.adapted_namespace()
        with self.assertRaisesRegex(ValueError,'exact single'):
            v._rewrite(v.frozen.verify_report,'False','True',{})
        ns=v.adapted_namespace()
        self.assertIs(ns['verify_mouse_action'].__globals__,ns)
        self.assertIs(ns['_verify_file'].__globals__,ns)
        self.assertIsNot(ns['verify_ready'],v.frozen.verify_ready)


if __name__=='__main__':unittest.main()
