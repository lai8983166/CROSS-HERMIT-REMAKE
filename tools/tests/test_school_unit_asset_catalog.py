import hashlib
import json
import struct
import unittest
from tools.school_unit_asset_catalog import source_catalog,original_text_tables,effect_metadata,native_fixture,EVIDENCE
from tools.school_unit_assets_emulation import effect_resource,UNITCTRL
from tools.tactics_exit_emulation import ROOT,SOURCE
from tools.dxanim_lib import DxAnimError


class UnitAssetCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = source_catalog()
        cls.native = json.loads(EVIDENCE.read_text('utf-8'))

    def test_every_native_text_pointer_string_destination_and_color(self):
        expected = [(table,entry) for table in self.source['text_tables'] for entry in table['entries']]
        self.assertEqual(len(expected),1344)
        for c in self.native['cases'][:3]:
            for t,(table,entry) in zip(c['text_requests'],expected):
                self.assertEqual([t['table_va'],t['index'],t['text_hex']],
                                 [table['table_va'],entry['index'],entry['text_hex']])
                self.assertEqual(t['destination'],UNITCTRL+entry['destination_offset'])
                self.assertEqual(t['args'][2:], [entry['pointer'],1])
                self.assertEqual(t['source_color_hex'],'ffffffff')
            self.assertEqual(c['unit_reset_snapshot']['relation_hex'],self.source['default_relation_hex'])

    def test_native_effect_copied_bytes_and_section_pointers(self):
        raw,_ = effect_resource()
        rules = self.source['effect']
        self.assertEqual(rules['program_counts'],[47,169,115,155])
        self.assertEqual(rules['instructions'],3497)
        self.assertEqual(rules['metadata_bytes'],77212)
        for c in self.native['cases'][:3]:
            effect = c['unit_assets']
            self.assertEqual(effect['metadata_sha256'],hashlib.sha256(raw[:77212]).hexdigest())
            self.assertEqual(effect['section_pointers'],[effect['metadata_pointer']+s['offset'] for s in rules['sections'][:5]])
            self.assertEqual(effect['animation_table'],self.source['effect_animation_table'])
            self.assertEqual(effect['position_table'],self.source['effect_position_table'])
            self.assertEqual(effect['texture_binding']['receiver'],effect['controller']+24)
            self.assertEqual(effect['texture_binding']['args'][2:],[effect['metadata_pointer']+rules['sections'][5]['offset'],
                c['asset_requests'][0]['buffer_pointer']+rules['sections'][6]['offset'],0])

    def test_independent_rules_and_separate_fixture_reproduce(self):
        self.assertEqual(json.loads((ROOT/'prototype/data/school_unit_assets_rules.json').read_text('utf-8')),self.source)
        self.assertEqual(json.loads((ROOT/'prototype/data/school_unit_assets_evidence.json').read_text('utf-8')),native_fixture())
        self.assertNotIn('cases',self.source)

    def test_malformed_original_text_and_effect_input_refused(self):
        image = bytearray(SOURCE.read_bytes())
        image[0] ^= 1
        with self.assertRaises(ValueError):
            original_text_tables(bytes(image))
        raw,_ = effect_resource()
        variants = [raw[:16]]
        for offset,value in [(0,16),(4,8),(8,0),(32,len(raw)+4),(12,35)]:
            bad = bytearray(raw)
            struct.pack_into('<I',bad,offset,value)
            variants.append(bytes(bad))
        for bad in variants:
            with self.assertRaises((ValueError,DxAnimError)):
                effect_metadata(bad)


if __name__ == '__main__':
    unittest.main()
