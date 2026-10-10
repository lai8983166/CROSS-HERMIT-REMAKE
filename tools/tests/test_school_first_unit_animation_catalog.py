from copy import deepcopy
import json
import struct
import unittest
from tools.school_first_unit_animation_catalog import (
    source_catalog,native_fixture,expected_binding,animation_inputs,normalize_palette,ROOT)
from tools.school_first_unit_animation_emulation import unit_resource
from tools.dxanim_lib import DxAnimError


class FirstUnitAnimationSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules,cls.fixture = source_catalog(),native_fixture()

    def test_all_native_records_pixels_palettes_metadata_and_controller_against_source(self):
        for c in self.fixture['cases'][:3]:
            w = c['first_unit_animation']
            allocations = {a['kind']:a['pointer'] for a in w['allocations']}
            expected = expected_binding(w['graphics_input']['controller_before_hex'],allocations['unit_file_buffer'],
                allocations['unit_metadata'],allocations['unit_texture_array'],w['texture_table'],rules=self.rules)
            for key in ('controller_hex','metadata_hex','metadata_sha256','section_pointers','texture_records','texture_count','mode_field'):
                self.assertEqual(expected[key],w[key],key)
            self.assertEqual(expected['binding_args'],w['binding']['args'])
            self.assertEqual(expected['source_sha256_at_release'],w['file_release']['sha256_at_release'])
            for actual,e in zip(c['unit_texture_entries'],expected['texture_entries']):
                for key in e:
                    if key!='upload_args':
                        self.assertEqual(actual[key],e[key],(actual['index'],key))
            for actual,e in zip([b for b in c['unit_animation_boundaries'] if b['kind']=='pixel_upload'],expected['texture_entries']):
                self.assertEqual(actual['args'],e['upload_args'])

    def test_archive_shape_palettes_masks_and_native_black_normalization(self):
        a = self.rules['animation']
        self.assertEqual(a['program_counts'],[121,6,0,13])
        self.assertEqual(a['instructions'],545)
        self.assertEqual(len(a['palettes']),40)
        self.assertEqual(len(a['texture_entries']),193)
        self.assertEqual(bytes.fromhex(a['mask_hex']).count(0),123)
        # Source preserves color0, copies all four bytes only for later black RGB entries.
        palette = bytearray(1024)
        palette[:4] = bytes([1,2,3,4])
        palette[4:8] = bytes([0,0,0,9])
        palette[8:12] = bytes([0,0,1,9])
        result = normalize_palette(bytes(palette))
        self.assertEqual(result[:8],bytes([1,2,3,4])*2)
        self.assertEqual(result[8:12],bytes([0,0,1,9]))
        self.assertEqual(palette[4:8],bytes([0,0,0,9]))

    def test_malformed_archive_and_unsupported_binding_refusal(self):
        raw,_ = unit_resource()
        changed = []
        for at,value in ((0,len(raw)-1),(4,10),(32,40),(36,len(raw)+1)):
            bad = bytearray(raw)
            struct.pack_into('<I',bad,at,value)
            changed.append(bytes(bad))
        bad = bytearray(raw);bad[916784]=2;changed.append(bytes(bad))
        bad = bytearray(raw);bad[-1]=1;changed.append(bytes(bad))
        bad = bytearray(raw);bad[12256:12258]=b'XX';changed.append(bytes(bad))
        for bad in (b'',raw[:20],*changed):
            with self.assertRaises((ValueError,DxAnimError)):
                animation_inputs(bad)
        before = self.fixture['cases'][0]['first_unit_animation']['graphics_input']['controller_before_hex']
        for variant in (0,1,40,41,True,'3'):
            with self.assertRaises(ValueError):
                expected_binding(before,1,2,3,4,variant,self.rules)
        for value in ('zz','00'*83):
            with self.assertRaises(ValueError):
                expected_binding(value,1,2,3,4,rules=self.rules)
        with self.assertRaises(ValueError):
            expected_binding(before,-1,2,3,4,rules=self.rules)
        with self.assertRaises(ValueError):
            expected_binding(before,0x15000000,0x15000004,0x15100000,0x1000844,rules=self.rules)
        with self.assertRaises(ValueError):
            expected_binding(None,0x15000000,0x150E0000,0x150F0000,0x1000844,rules=self.rules)
        with self.assertRaises(ValueError):
            normalize_palette(bytes(1023))

    def test_independent_rules_and_fixed_native_exports_are_exact(self):
        rules = json.loads((ROOT/'prototype/data/school_first_unit_animation_rules.json').read_text('utf-8'))
        fixture = json.loads((ROOT/'prototype/data/school_first_unit_animation_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules)
        self.assertEqual(fixture,self.fixture)
        self.assertNotIn('cases',rules)
        self.assertNotIn('animation',fixture)
        before = deepcopy(self.rules)
        fixture['cases'][0]['first_unit_animation']['metadata_hex']=''
        self.assertEqual(self.rules,before)


if __name__=='__main__':
    unittest.main()
