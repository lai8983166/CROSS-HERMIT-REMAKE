from copy import deepcopy
import hashlib
import json
import struct
import unittest
from tools.school_effect_initialization_catalog import (
    source_catalog,native_fixture,effect_texture_inputs,EVIDENCE_SHA256,ROOT)
from tools.school_unit_assets_emulation import effect_resource
from tools.school_tactical_resource_catalog import container_sections


class EffectSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules,cls.fixture = source_catalog(),native_fixture()

    def test_all_native_headers_against_independent_original_entries(self):
        entries = self.rules['texture_entries']
        self.assertEqual(len(entries),1959)
        self.assertEqual(set(e['kind'] for e in entries),{'indexed_bmp'})
        for c in self.fixture['cases'][:3]:
            for source,native in zip(entries,c['effect_entries']):
                for field in ('index','offset','file_offset','bytes','header_hex','width','height'):
                    self.assertEqual(source[field],native[field])
                self.assertEqual(source['native_format'],native['format'])
        raw,_ = effect_resource()
        for entry in entries:
            at = entry['file_offset']
            self.assertEqual(entry['sha256'],hashlib.sha256(raw[at:at+entry['bytes']]).hexdigest())

    def test_first_animation_and_groups_against_native_work(self):
        initial = self.rules['initial_animation']
        for c in self.fixture['cases'][:3]:
            effect = c['effect_initialization']
            self.assertEqual(effect['texture_slot'],self.rules['texture_slot'])
            for source,native in zip(self.rules['work_groups'],effect['groups']):
                for field in ('offset','count','stride','prefix'):
                    self.assertEqual(source[field],native[field])
            aw = effect['initial_animation']
            self.assertEqual(aw['metadata_offset'],initial['metadata_offset'])
            self.assertEqual(aw['instruction_hex'],initial['instruction']['raw'])
            self.assertEqual(aw['duration'],initial['instruction']['duration_ticks'])
            self.assertEqual(aw['descriptor_value'],initial['descriptor_value'])
            self.assertEqual(effect['animation_request']['args'][1:],[initial['block'],initial['animation'],initial['flags']])
            self.assertEqual(effect['metadata_sha256'],self.rules['metadata_sha256'])

    def test_bad_containers_and_image_headers_rejected_historical_parser_retained(self):
        raw,_ = effect_resource()
        images = raw[77212:]
        cases = [b'',images[:-1]]
        for offset,value in ((4,580),(8,0),(12,8+1959*4),(8,len(images))):
            changed = bytearray(images)
            struct.pack_into('<I',changed,offset,value)
            cases.append(changed)
        start = struct.unpack_from('<I',images,8)[0]
        for offset,value in ((start,0),(start+28,24),(start+30,1)):
            changed = bytearray(images)
            changed[offset] = value
            cases.append(changed)
        for case in cases:
            with self.assertRaises(ValueError):
                effect_texture_inputs(case)
        with self.assertRaises(ValueError):
            container_sections(images)

    def test_exports_and_fixed_native_fixture_are_separate_and_exact(self):
        rules = json.loads((ROOT/'prototype/data/school_effect_initialization_rules.json').read_text('utf-8'))
        fixture = json.loads((ROOT/'prototype/data/school_effect_initialization_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules)
        self.assertEqual(fixture,self.fixture)
        self.assertEqual(fixture['source_report_sha256'],EVIDENCE_SHA256)
        self.assertNotIn('cases',rules)
        self.assertNotIn('texture_entries',fixture)
        original = deepcopy(self.rules)
        fixture['cases'][0]['effect_entries'][0]['width'] = 9999
        self.assertEqual(self.rules,original)


if __name__ == '__main__':
    unittest.main()
