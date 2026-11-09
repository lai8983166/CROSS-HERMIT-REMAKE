"""Retiring-state classification and tamper rejection; no native operations."""
import copy
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from devtools import terminal_worker_retention_verification_v2 as v
from devtools.tests.test_terminal_worker_retention_verification import fixture,frame


def retiring():
    row,p,raw=fixture();task=row['tasks'][0];head=bytearray.fromhex(task['header_hex'])
    previous=task['vtable'];struct.pack_into('<I',head,0,v.BASE_VTABLE);struct.pack_into('<I',head,4,4)
    task.update(header_hex=head.hex(),vtable=v.BASE_VTABLE,
                vtable_hex=raw[v.BASE_VTABLE-0x400000:v.BASE_VTABLE-0x400000+8].hex())
    row['registered_tasks'][0]['head_hex']=head[:48].hex()
    main=frame(11,(0x421ACE,0x42182F));main['chain'][0]['saved_bp']=0x110100
    main['chain'][1].update(bp=0x110100,saved_bp=0x110180)
    row['frames']=[main];receipt=row['worker_retention'];receipt.update(version=2,cohort_tids=[11])
    proof=receipt['tasks'][0];proof.update(status=v.TRANSITION,observed_context_present=False)
    stack=bytearray(0x6C)
    for offset,value in ((0x54,4),(0x58,p['main']+0x64),(0x5C,0x110180),(0x60,0x42182F),(0x64,task['pointer'])):
        struct.pack_into('<I',stack,offset,value)
    proof['transition']=dict(previous_vtable=previous,observed_vtable=v.BASE_VTABLE,
        transition_verified=False,full_resource_PTD_cleanup_proved=False,
        thread_query=dict(owner_pid=p['pid'],thread_id=22,wait_status=0,exit_code=0,zero_timeout=True,
            observer_duplicate_only=True,original_cleanup_proved=False),
        scheduler_frame=dict(bp=0x110100,return_va=0x42182F,pointer=0x110100-0x5C,hex=stack.hex()),
        worker_stack_regions=[])
    workers={(task['pointer'],22):dict(first_elapsed=.5,original_handle=0xCDCDCDCD,
                                     vtable=previous,event=dict(remote_handle=0xCDCDCDCD))}
    return row,p,raw,workers


class RetiringVerificationTests(unittest.TestCase):
    def retry_row(self):
        row,p,raw=fixture();row['worker_retention']['version']=2
        row['cohort_observation_retries']=[dict(pid=p['pid'],main_tid=11,attempt=1,before_tids=[11,22],
            after_tids=[11],capture_begin_perf_ns=60,capture_end_perf_ns=80,
            owned_suspend_restored=True,source_snapshot_emitted=False)]
        row['cohort_retry_budget']=dict(maximum_attempts=5,retry_budget_ns=500_000_000,
            started_perf_ns=50,successful_attempt_begin_perf_ns=90,deadline_applies_to_next_attempt_start=True)
        return row,p,raw

    def test_source3_retry_ledger_and_source2_no_hidden_retries(self):
        row,p,raw=self.retry_row()
        self.assertEqual(v.retention_contract(row,p,{},3),{(0x220000,22)})
        self.assertEqual(v.adapted_namespace(3)['verify_task_row'](row,p,raw,row['game'],{}),0)
        with self.assertRaisesRegex(ValueError,'source2 cannot hide'):v.retention_contract(row,p,{})
        del row['cohort_observation_retries']
        with self.assertRaisesRegex(ValueError,'requires explicit retry'):v.retention_contract(row,p,{},3)

    def test_retry_inventory_owner_restore_and_emitted_row_tamper(self):
        mutations=[dict(pid=100),dict(main_tid=22),dict(attempt=2),dict(before_tids=[22]),
                   dict(after_tids=[11,11]),dict(after_tids=[22,11]),dict(owned_suspend_restored=False),
                   dict(source_snapshot_emitted=True),dict(snapshot={}),dict(capture_end_perf_ns=91)]
        for changes in mutations:
            row,p,raw=self.retry_row();row['cohort_observation_retries'][0].update(changes)
            with self.subTest(changes=changes),self.assertRaises(ValueError):v.retention_contract(row,p,{},3)

    def test_retry_budget_limits_start_not_successful_snapshot_completion(self):
        row,p,raw=self.retry_row();row['worker_retention']['capture_end_perf_ns']=1_000_000_000
        self.assertEqual(v.retention_contract(row,p,{},3),{(0x220000,22)})
        row['cohort_retry_budget']['successful_attempt_begin_perf_ns']=500_000_050
        row['worker_retention']['capture_begin_perf_ns']=500_000_060
        with self.assertRaisesRegex(ValueError,'successful retry starts within'):v.retention_contract(row,p,{},3)
        row['cohort_observation_retries']=[]
        self.assertEqual(v.retention_contract(row,p,{},3),{(0x220000,22)})

    def test_retry_count_order_and_later_attempt_start_deadline(self):
        row,p,raw=self.retry_row();one=row['cohort_observation_retries'][0]
        row['cohort_observation_retries']=[copy.deepcopy(one)for _ in range(5)]
        with self.assertRaisesRegex(ValueError,'at most four'):v.retention_contract(row,p,{},3)
        row,p,raw=self.retry_row();second=copy.deepcopy(row['cohort_observation_retries'][0])
        second.update(attempt=2,capture_begin_perf_ns=70,capture_end_perf_ns=85)
        row['cohort_observation_retries'].append(second)
        with self.assertRaisesRegex(ValueError,'nonoverlapping'):v.retention_contract(row,p,{},3)
        second.update(capture_begin_perf_ns=500_000_050,capture_end_perf_ns=500_000_060)
        row['cohort_retry_budget']['successful_attempt_begin_perf_ns']=500_000_070
        row['worker_retention'].update(capture_begin_perf_ns=500_000_080,capture_end_perf_ns=500_000_090)
        with self.assertRaisesRegex(ValueError,'later failed attempt starts within'):v.retention_contract(row,p,{},3)

    def test_source3_exact_three_implementation_layers_and_source2_stays_separate(self):
        report=dict(worker_retention_version=3,
            worker_retention_implementation=v.identity(v.ROOT/'devtools/terminal_worker_retention_v3.py'),
            worker_retention_parent_implementation=v.identity(v.ROOT/'devtools/terminal_worker_retention_v2.py'),
            worker_retention_grandparent_implementation=v.identity(v.ROOT/'devtools/terminal_worker_retention.py'))
        v.verify_layers(report,3)
        for field in ('worker_retention_implementation','worker_retention_parent_implementation',
                      'worker_retention_grandparent_implementation'):
            changed=copy.deepcopy(report);changed[field]['sha256']='0'*64
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'exact executed'):v.verify_layers(changed,3)
        report['worker_retention_version']=2
        with self.assertRaisesRegex(ValueError,'exactly two'):v.verify_layers(report,2)
        report['worker_retention_implementation']=report['worker_retention_parent_implementation']
        report['worker_retention_parent_implementation']=report.pop('worker_retention_grandparent_implementation')
        v.verify_layers(report,2)

    def test_classified_base_state_passes_only_new_vtable_predicate(self):
        row,p,raw,workers=retiring();before=copy.deepcopy(row)
        self.assertEqual(v.retention_contract(row,p,workers),set())
        self.assertEqual(v.adapted_namespace()['verify_task_row'](row,p,raw,row['game'],workers),0)
        self.assertEqual(row,before)
        with self.assertRaisesRegex(ValueError,'input target'):
            v.require_input_owner(row,row['tasks'][0],p,workers)
        with self.assertRaises(ValueError):v.v1.retention_contract(row,p,workers)

    def test_scheduler_raw_arguments_and_link_tamper(self):
        for offset in (0x54,0x58,0x5C,0x60,0x64):
            row,p,raw,workers=retiring();s=row['worker_retention']['tasks'][0]['transition']['scheduler_frame']
            data=bytearray.fromhex(s['hex']);data[offset]^=1;s['hex']=data.hex()
            with self.subTest(offset=offset),self.assertRaises(ValueError):v.retention_contract(row,p,workers)
        row,p,raw,workers=retiring();row['frames'][0]['chain'][0]['return_va']=0x421A94
        with self.assertRaisesRegex(ValueError,'Sleep return'):v.retention_contract(row,p,workers)

    def test_unknown_vtable_and_nonterminal_flag_rejected(self):
        for vt,flags in ((0x595560,4),(v.BASE_VTABLE,0x10004),(v.BASE_VTABLE,0)):
            row,p,raw,workers=retiring();task=row['tasks'][0];data=bytearray.fromhex(task['header_hex'])
            struct.pack_into('<II',data,0,vt,flags);task.update(header_hex=data.hex(),vtable=vt)
            row['worker_retention']['tasks'][0]['transition']['observed_vtable']=vt
            with self.subTest(vt=vt,flags=flags),self.assertRaises(ValueError):v.retention_contract(row,p,workers)

    def test_query_identity_nonzero_exit_or_unsignaled_rejected(self):
        for changes in (dict(owner_pid=100),dict(thread_id=23),dict(wait_status=258,exit_code=259),
                        dict(exit_code=1),dict(zero_timeout=False),dict(observer_duplicate_only=False),
                        dict(original_cleanup_proved=True)):
            row,p,raw,workers=retiring();row['worker_retention']['tasks'][0]['transition']['thread_query'].update(changes)
            with self.subTest(changes=changes),self.assertRaises(ValueError):v.retention_contract(row,p,workers)

    def test_live_frame_tls_and_changed_handle_cannot_be_retiring(self):
        for mutate in (lambda r:r['frames'].append(frame(22)),
                       lambda r:r['tasks'][0].update(TLS={}),
                       lambda r:r['worker_retention']['tasks'][0]['transition'].update(worker_stack_regions=[{'pointer':1,'hex':'00'}])):
            row,p,raw,workers=retiring();mutate(row)
            with self.assertRaises(ValueError):v.retention_contract(row,p,workers)
        row,p,raw,workers=retiring();workers[(0x220000,22)]['original_handle']=88
        with self.assertRaisesRegex(ValueError,'handle and event'):v.retention_contract(row,p,workers)

    def test_ordinary_status_cannot_hide_transition(self):
        row,p,raw,workers=retiring();row['worker_retention']['tasks'][0]['status']='already_retained'
        with self.assertRaisesRegex(ValueError,'unclassified'):v.retention_contract(row,p,workers)
        del row['worker_retention']['tasks'][0]['transition']
        with self.assertRaisesRegex(ValueError,'same retained native'):v.retention_contract(row,p,workers)

    def test_transition_needs_prior_real_tls_observation(self):
        row,p,raw,workers=retiring();probe=dict(p,samples=[row],workers=list(workers.values()))
        # Workers always carry actual node/TID in a complete source.
        probe['workers'][0].update(pointer=0x220000,thread_id=22)
        with self.assertRaisesRegex(ValueError,'earlier real derived'):
            v.verify_transition_history(dict(probe=probe))

    def test_pending_remains_strict_and_parent_hash_is_fixed(self):
        row,p,raw=fixture();row['worker_retention']['version']=2
        self.assertEqual(v.retention_contract(row,p,{}),{(0x220000,22)})
        row['frames'][1]=frame(22,(0x56E183,))
        with self.assertRaisesRegex(ValueError,'partial callback'):v.retention_contract(row,p,{})
        with patch.object(v,'V1_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'first retention verifier SHA'):v.adapted_namespace()

    def test_transition_does_not_claim_cleanup_and_needs_complete_scheduler_bytes(self):
        for field in ('transition_verified','full_resource_PTD_cleanup_proved'):
            row,p,raw,workers=retiring();row['worker_retention']['tasks'][0]['transition'][field]=True
            with self.assertRaisesRegex(ValueError,'no verification or cleanup claim'):
                v.retention_contract(row,p,workers)
        row,p,raw,workers=retiring();s=row['worker_retention']['tasks'][0]['transition']['scheduler_frame']
        s['hex']=s['hex'][:-2]
        with self.assertRaisesRegex(ValueError,'complete original scheduler'):
            v.retention_contract(row,p,workers)

    def test_cli_rehash_blocks_changed_implementation_and_preserves_analysis(self):
        before=[{'path':str(i),'sha256':'a','bytes':1}for i in range(3)]
        after=copy.deepcopy(before);after[1]['sha256']='b'
        with tempfile.TemporaryDirectory(dir=v.ROOT/'.venv-audit/native-worker')as directory:
            out=Path(directory)/'review.json'
            args=['verify','--source','immutable.gz','--source-sha','0'*64,'--out',str(out)]
            with patch('sys.argv',args),patch.object(v,'execution_identities',side_effect=[before,after]), \
                 patch.object(v,'verify_file',return_value=dict(status='partial',accepted=False,
                    worker_retention_verified=True,analysis={'observations':8})):
                self.assertEqual(v.main(),2)
            result=json.loads(out.read_text())
            self.assertEqual(result['status'],'blocked');self.assertFalse(result['worker_retention_verified'])
            self.assertFalse(result['accepted']);self.assertEqual(result['analysis'],{'observations':8})
            self.assertEqual(result['execution_implementations'],before)
            self.assertEqual(result['execution_implementations_after'],after)

    def test_cli_final_hash_failure_preserves_existing_source_failure(self):
        with tempfile.TemporaryDirectory(dir=v.ROOT/'.venv-audit/native-worker')as directory:
            out=Path(directory)/'review.json'
            args=['verify','--source','immutable.gz','--source-sha','0'*64,'--out',str(out)]
            with patch('sys.argv',args),patch.object(v,'execution_identities',side_effect=[[{'sha256':'a'}],OSError('missing')]), \
                 patch.object(v,'verify_file',side_effect=ValueError('original source failure')):
                self.assertEqual(v.main(),2)
            result=json.loads(out.read_text())
            self.assertIn('original source failure',result['error'])
            self.assertIn('final implementation identity check failed',result['execution_implementation_errors'][0])
            self.assertFalse(result['accepted'])

    def test_cli_unchanged_implementation_preserves_limited_success(self):
        with tempfile.TemporaryDirectory(dir=v.ROOT/'.venv-audit/native-worker')as directory:
            out=Path(directory)/'review.json';before=v.execution_identities()
            args=['verify','--source','immutable.gz','--source-sha','0'*64,'--out',str(out)]
            with patch('sys.argv',args),patch.object(v,'verify_file',return_value=dict(
                    status='partial',accepted=False,worker_retention_verified=True)):
                self.assertEqual(v.main(),0)
            result=json.loads(out.read_text())
            self.assertEqual(result['execution_implementations'],before)
            self.assertEqual(result['execution_implementations_after'],before)
            self.assertEqual(result['execution_implementation_errors'],[])
            self.assertFalse(result['accepted'])


if __name__=='__main__':unittest.main()
