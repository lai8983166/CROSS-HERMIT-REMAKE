import hashlib
import json
import struct
import unittest
from tools.school_tactical_resource_catalog import (
    source_catalog,native_fixture,container_sections,texture_inputs,EVIDENCE,EVIDENCE_SHA256,
    ROOT,RESOURCE_NAMES,original_resource,report_text)


class SchoolTacticalResourceCatalogTests(unittest.TestCase):
    def test_independent_source_export_and_frozen_native_fixture(self):
        rules=source_catalog();fixture=native_fixture()
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        for name,value in [('rules',rules),('evidence',fixture)]:
            self.assertEqual((ROOT/f'prototype/data/school_tactical_resources_{name}.json').read_bytes(),report_text(value).encode())
        self.assertEqual([s['filename'] for s in rules['selections']],['TactStart05.bin','t0005.bin'])
        self.assertEqual([s['scene_id'] for s in rules['selections']],[5,5])
        self.assertNotIn('cases',rules);self.assertNotIn('record_pointer',report_text(rules))
        self.assertEqual([len(r['sections']) for r in rules['resources']],[580,2,1,2])

    def test_every_native_texture_matches_independent_original_bytes(self):
        catalog=source_catalog();cases=json.loads(EVIDENCE.read_text('utf-8'))['cases']
        inputs=catalog['resources'][:3]
        entries=[(i,e) for i,r in enumerate(inputs) for e in r['texture_entries']]
        self.assertEqual(len(entries),583)
        self.assertEqual(sum(e['kind']=='indexed_bmp' for _,e in entries),461)
        self.assertEqual(sum(e['kind']=='no_texture' for _,e in entries),119)
        self.assertEqual(sum(e['kind']=='rgb555_dx' for _,e in entries),3)
        for c in cases[:3]:
            for actual,(resource,expected) in zip(c['texture_entries'],entries):
                self.assertEqual(actual['resource'],resource)
                for field in ['index','offset','bytes','header_hex','width','height']:
                    self.assertEqual(actual[field],expected[field],(c['name'],resource,expected['index'],field))
                self.assertEqual(actual['format'],expected['native_format'])
                gpu=[e for e in c['gpu_boundaries'] if e['boundary']=='texture_creation'
                     and e['entry']['resource']==resource and e['entry']['index']==expected['index']]
                self.assertEqual(len(gpu),0 if expected['kind']=='no_texture' else 1)
                if gpu:self.assertEqual([gpu[0]['width'],gpu[0]['height']],[expected['width'],expected['height']])
            self.assertEqual(c['scene_script']['source'],catalog['resources'][3]['source'])

    def test_malformed_container_and_texture_layout_refused(self):
        original,_=original_resource(RESOURCE_NAMES[0])
        mutations=[(0,len(original)-1),(4,0),(4,581),(8,0),(12,2328),(8,len(original))]
        for at,value in mutations:
            raw=bytearray(original);struct.pack_into('<I',raw,at,value)
            for decoder in [container_sections,texture_inputs]:
                with self.assertRaises(ValueError):decoder(raw)
        for at,fmt,value in [(2328+14,'I',108),(2328+18,'i',-1),(2328+28,'H',24),
                             (2328+30,'I',1),(2328+46,'I',512)]:
            raw=bytearray(original);struct.pack_into('<'+fmt,raw,at,value)
            with self.assertRaises(ValueError):texture_inputs(raw)
        raw=bytearray(original);raw[2328:2330]=b'XX'
        with self.assertRaises(ValueError):texture_inputs(raw)
        raw=bytearray(original);at=container_sections(raw)[8]['offset'];raw[at+15]=1
        with self.assertRaises(ValueError):texture_inputs(raw)
        raw=bytearray(original_resource(RESOURCE_NAMES[1])[0]);struct.pack_into('<H',raw,16+8,256)
        with self.assertRaises(ValueError):texture_inputs(raw)
        for raw in [b'',b'\0'*11]:
            with self.assertRaises(ValueError):container_sections(raw)


if __name__=='__main__':unittest.main()
