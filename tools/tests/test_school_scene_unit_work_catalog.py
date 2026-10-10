from copy import deepcopy
import hashlib
import json
import struct
import unittest
from tools.school_scene_unit_work_catalog import (
    ROOT,EVIDENCE,EVIDENCE_SHA256,COUNTER_EVIDENCE,COUNTER_SHA256,source_catalog,expected_prefix,
    archive_inventory,native_fixture)
from tools.school_enemy_records_catalog import source_catalog as record_catalog,expected_record


class SceneUnitWorkSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=source_catalog();cls.full=json.loads(EVIDENCE.read_text('utf-8'))
        cls.counter=json.loads(COUNTER_EVIDENCE.read_text('utf-8'))

    def expected(self,n,**changes):
        values=dict(record_hex=n['before_record_hex'],ordinal=n['ordinal'],cache_hex=n['cache_before_hex'],
            counter=n['counter_before'],renderer=n['renderer'],controller=n['allocation']['pointer'],
            selector=n['classification_selector'],relation_hex=n['relation_hex'],rules=self.rules,template_hex=n['template_hex'])
        values.update(changes);return expected_prefix(**values)

    def match(self,n):
        before=deepcopy(n);x=self.expected(n)
        for k in ('work_hex','record_hex','cache_hex','controller_hex','counter','cache_slot'):self.assertEqual(n[k],x[k],(n['ordinal'],k))
        self.assertEqual(n['resource_request']['args'],x['resource_args']);self.assertEqual(n['resource_request']['relative_path'],x['relative_path'])
        self.assertEqual(n,before)

    def test_original_records_and_every_native_prefix_byte(self):
        records=record_catalog()
        for n in self.full['declared_scene_prefix_diagnostic']['units']+ [c['scene_unit_work'] for c in self.full['cases'][:3]]:
            self.assertEqual(n['before_record_hex'],expected_record(n['template_hex'],rules=records)['record_hex'])
            self.match(n)

    def test_declared_counterfactual_overlay_status_and_relation(self):
        self.assertEqual(hashlib.sha256(COUNTER_EVIDENCE.read_bytes()).hexdigest(),COUNTER_SHA256)
        self.assertFalse(self.counter['school_enemy_loop_executed']);self.assertFalse(self.counter['archives_loaded'])
        for n in self.counter['units']:self.match(n)
        units=self.counter['units'];self.assertEqual([bytes.fromhex(n['work_hex'])[0x28A] for n in units],[2,2,6,9,2,3])
        self.assertEqual(bytes.fromhex(units[1]['work_hex'])[0x290],25)
        record=bytes.fromhex(units[0]['record_hex']);work=bytes.fromhex(units[0]['work_hex'])
        self.assertEqual(struct.unpack_from('<H',record,0xA8)[0],0x1234)
        self.assertEqual(work[0x2AC:0x2D4],bytes(range(1,41)))
        self.assertEqual(work[0x2D4:0x2E4],bytes(16));self.assertEqual(work[0x2E8:0x2EA],bytes(2))
        self.assertEqual(work[0x2EA:0x2EC],bytes((63,64)))

    def test_exact_archives_inventory_and_source_provenance(self):
        self.assertEqual(len(self.rules['jobs']),10);self.assertEqual(len(self.rules['archives']),9)
        self.assertEqual(len(self.rules['source_branch_bodies']),28)
        self.assertGreater(len(self.rules['code_inputs']),90)
        for a in self.rules['archives'].values():
            raw=(ROOT/a['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),a['sha256'])
            self.assertEqual(len(raw),a['bytes']);self.assertFalse(a['native_loaded'])
            self.assertEqual(archive_inventory(raw),{k:a[k] for k in ('offsets','sections','image_count','palette_count','mask_sha256','native_loaded')})

    def test_malformed_archives_and_unsupported_prefix_inputs(self):
        a=next(iter(self.rules['archives'].values()));raw=bytearray((ROOT/a['path']).read_bytes())
        for broken in (bytes(raw[:8]),bytes(raw[:-1])):
            with self.assertRaises(ValueError):archive_inventory(broken)
        struct.pack_into('<I',raw,8,45)
        with self.assertRaises(ValueError):archive_inventory(raw)
        n=self.full['declared_scene_prefix_diagnostic']['units'][0]
        for changes in ({'record_hex':'xx'},{'record_hex':'00'*175},{'ordinal':35},{'ordinal':True},
            {'counter':-1},{'selector':16},{'relation_hex':'00'*255},{'template_hex':'00'*83},
            {'cache_hex':'00'*4095},{'cache_hex':'02'+'00'*4095}):
            with self.assertRaises(ValueError):self.expected(n,**changes)
        for offset,value in ((2,999),(12,999),(0xA4,16),(15,2)):
            record=bytearray.fromhex(n['before_record_hex']);struct.pack_into('<H' if offset in (2,12) else '<B',record,offset,value)
            with self.assertRaises(ValueError):self.expected(n,record_hex=record.hex())
        cache=bytearray(4096);struct.pack_into('<BBHI',cache,0,1,5,4,0x18000000)
        with self.assertRaises(ValueError):self.expected(n,cache_hex=cache.hex())
        for i in range(512):struct.pack_into('<BBHI',cache,i*8,1,5,999,0x18000000)
        with self.assertRaises(ValueError):self.expected(n,cache_hex=cache.hex())

    def test_exports_separate_original_rules_from_frozen_evidence(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual(self.rules,json.loads((ROOT/'prototype/data/school_scene_unit_work_rules.json').read_text('utf-8')))
        self.assertEqual(native_fixture(),json.loads((ROOT/'prototype/data/school_scene_unit_work_evidence.json').read_text('utf-8')))
        self.assertNotIn('cases',self.rules);self.assertNotIn('work_hex',self.rules)


if __name__=='__main__':unittest.main()
