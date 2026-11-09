import copy
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from devtools import terminal_battle_wait_gap_audit as audit


class ActualGapEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for key in ('school','window'):
            if not (audit.WORKER/audit.PARENTS[key][0]).exists():
                raise unittest.SkipTest('retained local battle-v6 raw source unavailable')
        name,sha=audit.PARENTS['school']
        source,_=audit.read_bound(audit.WORKER/name,sha,24*1024*1024)
        name,sha=audit.PARENTS['window']
        cls.window,_=audit.read_bound(audit.WORKER/name,sha,2*1024*1024)
        cls.rows=source['probe']['battle_inputs'][1]['post_release_snapshots']

    def check(self,row):
        return audit.endpoint(row,self.window['subject'],self.window['before'])

    def task(self,row):
        return next(t for t in row['tasks']if t['thread_id']==self.window['subject']['tid'])

    def frame(self,row):
        return next(f for f in row['frames']if f['tid']==self.window['subject']['tid'])

    def test_actual_endpoints_have_raw_wait_but_no_invented_API_frame(self):
        for index,site,field,value in ((0,'0x453cb5','inner_result',1),(2,'0x451758','tail_counter',0)):
            result=self.check(self.rows[index])
            self.assertEqual((result['site'],result['locals'][field]),(site,value))
            self.assertTrue(result['raw_wait_frame'])
            self.assertTrue(result['decoded_API_to_wait_adjacency_checked'])
            self.assertIsNone(result['raw_API_frame']);self.assertFalse(result['api_link_raw_proved'])
            self.assertFalse(result['ETW_wait_return_proved'])

    def test_actual_saved_wait_return_and_saved_bp_corruptions_rejected(self):
        for index in (0,2):
            for offset in (0,4):
                row=copy.deepcopy(self.rows[index]);frame=self.frame(row)
                wait=next(f for f in frame['chain']if f['return_va']in audit.verify.WAIT_SITES)
                for region in self.task(row)['terminal_frames']:
                    raw=bytearray.fromhex(region['hex']);off=wait['bp']+offset-region['pointer']
                    if 0<=off<=len(raw)-4:
                        struct.pack_into('<I',raw,off,0x41414141);region['hex']=raw.hex()
                with self.assertRaisesRegex(ValueError,'raw wait/API saved frame'):self.check(row)

    def test_actual_decoded_wait_site_and_API_adjacency_cannot_diverge(self):
        row=copy.deepcopy(self.rows[0]);frame=self.frame(row)
        next(f for f in frame['chain']if f['return_va']==0x453cb5)['return_va']=0x453cdd
        with self.assertRaisesRegex(ValueError,'raw wait/API saved frame'):self.check(row)
        row=copy.deepcopy(self.rows[2]);frame=self.frame(row)
        next(f for f in frame['chain']if f['return_va']==0x42240d)['saved_bp']+=4
        with self.assertRaises(ValueError):self.check(row)

    def test_actual_TLS_context_result_and_overlap_corruptions_rejected(self):
        for index in (0,2):
            for kind in ('PTD','slot','context','result'):
                row=copy.deepcopy(self.rows[index]);task=self.task(row)
                if kind=='PTD':task['TLS']['PTD_hex']='00'*116
                elif kind=='slot':task['TLS']['TLS_slot_hex']='00'*4
                elif kind=='context':
                    frame=self.frame(row);raw=bytearray.fromhex(frame['context_hex']);raw[184]^=1;frame['context_hex']=raw.hex()
                else:
                    region=task['terminal_frames'][-1];raw=bytearray.fromhex(region['hex']);raw[0x80]^=1;region['hex']=raw.hex()
                with self.assertRaises(ValueError):self.check(row)
        row=copy.deepcopy(self.rows[0]);regions=self.task(row)['terminal_frames']
        raw=bytearray.fromhex(regions[1]['hex']);raw[0]^=1;regions[1]['hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'overlapping original stack bytes agree'):self.check(row)


class GapExecutionIdentityTests(unittest.TestCase):
    def test_dependency_drift_refuses_output(self):
        with tempfile.TemporaryDirectory(dir=audit.WORKER,prefix='gap-audit-unit-')as directory:
            out=Path(directory)/'proof.json'
            with patch.object(audit,'execution_paths',return_value=[Path(__file__)]),\
                 patch.object(audit,'identity',side_effect=[{'sha256':'before'},{'sha256':'after'}]),\
                 patch.object(audit,'audit_result',return_value={'accepted':False}):
                with self.assertRaisesRegex(ValueError,'execution dependencies unchanged'):audit.audit(out)
            self.assertFalse(out.exists())


if __name__=='__main__':unittest.main()
