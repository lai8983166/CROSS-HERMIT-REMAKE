import copy
import gzip
import json
from pathlib import Path
import struct
import unittest
from devtools import terminal_heap_etw_verification as v


class ActualHeapCapabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        w=v.ROOT/'.venv-audit/native-worker'
        cls.source=json.loads((w/'terminal-heap-capability-v2-20261109.json').read_bytes())
        cls.report=json.loads((w/'terminal-heap-decode-v3-20261109.json').read_bytes())
        cls.records=json.loads(gzip.decompress((w/'terminal-heap-decode-v3-20261109.records.json.gz').read_bytes()))
        cls.schemas=json.loads(gzip.decompress((w/'terminal-heap-decode-v3-20261109.schemas.json.gz').read_bytes()))
    def data(self):return copy.deepcopy((self.source,self.report,self.records,self.schemas))
    def check(self,args):return v.verify_objects(*args)
    def rejected(self,mutate):
        data=self.data();mutate(*data)
        with self.assertRaises(ValueError):self.check(data)

    def test_fixed_actual_full_file_authentication_and_positive_match(self):
        r=v.verify_files(v.ROOT/'.venv-audit/native-worker')
        self.assertTrue(r['finite_owned_WOW64_heap_capability'])
        self.assertEqual([x['index']for x in r['owned_heap_events']],[117,226,228,338])
        self.assertFalse(r['event_HeapFree_BOOL_present']);self.assertFalse(r['original_game']);self.assertFalse(r['PTDcleanup'])
        self.assertEqual({x['header_pid']for x in r['foreign_snapshot_statistics']},{6000})
        self.assertEqual({x['payload_process_id']for x in r['foreign_snapshot_statistics']},{6092})

    def test_missing_or_duplicate_heap_event_rejected(self):
        self.rejected(lambda s,r,a,b:a['records'].pop())
        self.rejected(lambda s,r,a,b:a['records'].__setitem__(1,copy.deepcopy(a['records'][0])))

    def test_raw_payload_and_TDH_value_disagreement_rejected(self):
        def change(s,r,a,b):
            row=next(x for x in a['records']if x['index']==226);payload=bytearray.fromhex(row['payload_hex']);payload[8]^=1;row['payload_hex']=payload.hex()
        self.rejected(change)

    def test_false_live_free_rejected_even_when_raw_and_TDH_agree(self):
        def change(s,r,a,b):
            row=next(x for x in a['records']if x['index']==338);address=s['helper']['live']['live_address'];payload=bytearray.fromhex(row['payload_hex']);struct.pack_into('<I',payload,4,address);row['payload_hex']=payload.hex()
            next(p for p in row['TDH_properties']if p['name']=='FreeAddress')['hex']=struct.pack('<I',address).hex()
        self.rejected(change)

    def test_foreign_alloc_free_rejected(self):
        for index in (226,338):
            def change(s,r,a,b):
                row=next(x for x in a['records']if x['index']==index);h=bytearray.fromhex(row['header_hex']);struct.pack_into('<I',h,12,6000);row.update(header_hex=h.hex(),pid=6000,target_pid=False)
            self.rejected(change)

    def test_statistics_wrong_payload_process_rejected(self):
        def change(s,r,a,b):
            row=next(x for x in a['records']if not x['target_pid']);offset=0;payload=bytearray.fromhex(row['payload_hex'])
            for prop in row['TDH_properties']:
                if prop['name']=='ProcessId':prop['hex']=struct.pack('<I',999).hex();struct.pack_into('<I',payload,offset,999)
                offset+=prop['bytes']
            row['payload_hex']=payload.hex()
        self.rejected(change)

    def test_foreign_header_relabeling_rejected(self):
        def change(s,r,a,b):
            row=next(x for x in a['records']if not x['target_pid']);h=bytearray.fromhex(row['header_hex']);struct.pack_into('<I',h,12,6092);row.update(header_hex=h.hex(),pid=6092,target_pid=True)
        self.rejected(change)

    def test_unknown_opcode_version_not_ignored(self):
        for offset in (42,45):
            def change(s,r,a,b):
                row=a['records'][0];h=bytearray.fromhex(row['header_hex']);h[offset]=99;row['header_hex']=h.hex();row['version'if offset==42 else'opcode']=99
            self.rejected(change)

    def test_raw_schema_and_field_width_tamper_rejected(self):
        self.rejected(lambda s,r,a,b:b['schemas'][0]['fields'][0].update(flags=1))
        self.rejected(lambda s,r,a,b:a['records'][0]['TDH_properties'][0].update(bytes=True))

    def test_loss_incomplete_buffers_or_false_helper_BOOL_rejected(self):
        self.rejected(lambda s,r,a,b:r.update(buffer_reads=[1,2,3]))
        self.rejected(lambda s,r,a,b:s['helper']['live'].update(free_result=False))
        def loss(s,r,a,b):
            h=v.reader.abi.LOG_HEADER.from_buffer_copy(bytes.fromhex(r['ETL_header_raw_hex']));h.EventsLost=1;r['ETL_header_raw_hex']=bytes(h).hex()
        self.rejected(loss)

    def test_cleanup_overlap_and_false_raw_owner_rejected(self):
        self.rejected(lambda s,r,a,b:s['helper']['closed'].update(begin_filetime=s['helper']['live']['end_filetime']))
        self.rejected(lambda s,r,a,b:a['records'][0].update(tid=1))


if __name__=='__main__':unittest.main()
