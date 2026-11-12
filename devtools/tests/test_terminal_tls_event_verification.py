"""Actual retained controls and tamper rejection only; no native execution."""
import copy
import gzip
import hashlib
import json
import struct
import unittest
from pathlib import Path
from devtools import terminal_tls_event_verification as v


class EventVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=v.ROOT/'analysis/terminal-tls-event-controls-v1-20261112.json.gz'
        raw=path.read_bytes()
        cls.digest=hashlib.sha256(raw).hexdigest()
        cls.report=json.loads(gzip.decompress(raw))

    def mutate(self,fn):
        r=copy.deepcopy(self.report);fn(r)
        with self.assertRaises((ValueError,KeyError,StopIteration,IndexError)):
            v.verify(r,check_disk=False)

    def test_actual_controls_keep_original_and_fault_qualification_false(self):
        result=v.verify(self.report,check_disk=False)
        self.assertTrue(result['fixture_capture_passed'])
        self.assertFalse(result['without_notification_TLS_capture_passed'])
        self.assertFalse(result['original_adaptation_eligible'])
        self.assertFalse(result['fault_cleanup_qualified'])
        self.assertFalse(result['accepted'])

    def test_wrong_owner_and_generation_rejected(self):
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(tid=1234))
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(index=8))
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(pointer=1))

    def test_context_or_descriptor_change_rejected(self):
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(context_after_hex='00'*716))
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(selector_hex='00'*8))

    def test_no_stale_or_cleared_tls_as_live(self):
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(slot_hex='00000000'))
        self.mutate(lambda r:r['cases'][0]['captures'][1].update(slot_hex=r['cases'][0]['captures'][0]['slot_hex']))
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(live_wait_after=0))

    def test_payload_raw_bytes_not_labels(self):
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(payload_hex='00'*116))
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(TEB_head_hex='00'*64))

    def test_create_is_not_initialized_tls(self):
        self.mutate(lambda r:r['cases'][0]['event_attempts'][0]['capture'].update(slot_hex='01000000'))

    def test_missing_or_wrong_event_association_rejected(self):
        self.mutate(lambda r:r['cases'][0]['captures'].pop())
        self.mutate(lambda r:r['cases'][0]['captures'][0].update(event_index=48))
        self.mutate(lambda r:r['cases'][0]['events'][49].update(continued=False))

    def test_forced_or_incomplete_cleanup_rejected(self):
        self.mutate(lambda r:r['cases'][0].update(forced_termination=True))
        self.mutate(lambda r:r['cases'][0].update(job_members_after=[1]))
        self.mutate(lambda r:r['cases'][0].update(all_owned_handles_closed=False))
        self.mutate(lambda r:r['cases'][0].update(process_signaled_after_cleanup=False))

    def test_exit_must_be_same_retained_worker(self):
        def mutate(r):
            c=r['cases'][0];w=next(w for w in c['threads'] if w['tid']==c['done'][1]);w['queried_exit']=259
        self.mutate(mutate)

    def test_negative_control_cannot_be_upgraded(self):
        self.mutate(lambda r:r['cases'][1].update(captures=copy.deepcopy(r['cases'][0]['captures'])))
        self.mutate(lambda r:r.update(original_adaptation_eligible=True))

    def test_bad_clock_and_desktop_rejected(self):
        self.mutate(lambda r:r['clock']['perf_counter'].update(resolution=.015625))
        self.mutate(lambda r:r['desktop_after'][1].update(game_window=123))

    def test_review_identity_and_exit_forgery_rejected(self):
        self.mutate(lambda r:r.update(implementations=[]))
        self.mutate(lambda r:r['cases'][0]['events'][-1].update(exit_code=9))
        self.mutate(lambda r:r['cases'][0]['threads'][0].update(final_wait=258,queried_exit=259))

    def test_review_config_and_qpc_forgery_rejected(self):
        def shift(r):
            for e in r['cases'][0]['events']:
                e['qpc']+=1000000000000;e['continued_qpc']+=1000000000000
        self.mutate(shift)
        def config(r):
            e=next(e for e in r['cases'][0]['events'] if e.get('text','').startswith('TLS1 config '))
            fields=e['text'].split();fields[4]='8';e['text']=' '.join(fields)
        self.mutate(config)

    def test_other_thread_event_is_not_silently_ignored(self):
        def insert(r):
            c=r['cases'][1];d=c['done'];i=next(w['exit_event'] for w in c['threads'] if w['tid']==d[1])
            ticks=(d[6]+d[9])//2;ns=ticks*1000000000//d[5]
            e=dict(code=6,pid=c['pid'],tid=c['main_tid'],raw_qpc=ticks,qpc=ns,
                   continued_qpc=ns+100,continued=True,continue_status=0x10002)
            c['events'].insert(i,e)
            for w in c['threads']:
                for field in ('create_event','exit_event'):
                    if field in w and w[field]>=i:w[field]+=1
        self.mutate(insert)

    def test_source_hash_refuses_wrong_digest(self):
        p=v.ROOT/'analysis/terminal-tls-event-controls-v1-20261112.json.gz'
        with self.assertRaises(ValueError):v.verify_file(p,'0'*64)


if __name__=='__main__':unittest.main()
