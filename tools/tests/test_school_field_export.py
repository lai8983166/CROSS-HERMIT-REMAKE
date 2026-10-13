import json
import struct
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from PIL import Image
from tools.school_field_export import source_inputs, export, skin_inputs, digest, ROOT
from tools.school_formation_placement_catalog import native_fixture, source_catalog as formation_source
from tools.school_current_units_catalog import source_catalog as unit_source


class FieldExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.images = source_inputs()

    def test_entire_source_map_passability_and_formation_match_native_inputs(self):
        source = formation_source()
        raw = bytes.fromhex(source['map_hex'])
        terrain = bytes.fromhex(source['terrain_hex'])
        self.assertEqual(self.catalog['cells'], [list(c) for c in struct.iter_unpack('<3H', raw[16:])])
        for mode, values in enumerate(self.catalog['passability']):
            self.assertEqual(values, [int(mode == 4 or struct.unpack_from('<i', terrain, c[0]*76+mode*16+12)[0] != 0) for c in self.catalog['cells']])
        self.assertEqual(self.catalog['formation_grid'], [list(row[:3]) for row in struct.iter_unpack('<bbHH', bytes.fromhex(source['grid_hex']))])
        for case in native_fixture()['cases'][:3]:
            inputs = case['formation_placement']['inputs']
            self.assertEqual(self.catalog['origin'], inputs['origin'])
            self.assertEqual(self.catalog['formation_radius'], inputs['formation_radius'])
            self.assertEqual(self.catalog['initial_rotation'], inputs['before_rotation'])
            cm = bytes.fromhex(inputs['before_cm_hex'])
            # The only additional occupied cell is the undeployed current students at0,0.
            expected = {tuple(v['cell']) for v in self.catalog['static_occupancy']} | {(0, 0)}
            self.assertEqual(expected, {(i % 64, i // 64) for i in range(6144) if cm[2*i+1]})

    def test_current_palettes_all_directional_layers_and_pixel_provenance(self):
        source = unit_source()
        for identity, skin in self.catalog['skins'].items():
            rules = source['jobs'][str(skin['job'])]
            self.assertEqual(skin['palette_variant'], rules['job_input']['palettes_by_character'][int(identity)]+1)
            self.assertEqual(skin['movement_type'], 0)
            for directions in skin['actions'].values():
                self.assertEqual(set(directions), {'N', 'S', 'E', 'W', 'NW', 'NE', 'SW', 'SE'})
                for timeline in directions.values():
                    self.assertTrue(timeline['steps'])
                    for step in timeline['steps']:
                        for layer in step['layers']:
                            self.assertIn(str(layer['frame']), skin['frames'])
            for frame in skin['frames'].values():
                image = self.images[frame['file']]
                self.assertEqual(image.size, (frame['w'], frame['h']))
                self.assertEqual(digest(image.tobytes()), frame['rgba_sha256'])
                self.assertEqual(image.mode, 'RGBA')

    def test_export_is_deterministic_and_all_saved_pixels_match_source(self):
        checked_in = json.loads((ROOT/'prototype/assets/school_field/catalog.json').read_text('utf-8'))
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary)
            self.assertEqual(export(out), checked_in)
            self.assertEqual((out/'catalog.json').read_bytes(), (ROOT/'prototype/assets/school_field/catalog.json').read_bytes())
            for skin in checked_in['skins'].values():
                for frame in skin['frames'].values():
                    original = ROOT/'prototype/assets/school_field'/frame['file']
                    self.assertEqual(digest(original.read_bytes()), frame['file_sha256'])
                    with Image.open(original) as image:
                        self.assertEqual(digest(image.tobytes()), frame['rgba_sha256'])

    def test_wrong_archive_and_palette_refuse(self):
        source = unit_source()['jobs']['10']
        corrupt = deepcopy(source)
        corrupt['source']['sha256'] = 'bad'
        with self.assertRaisesRegex(ValueError, 'identity'):
            skin_inputs(3, 10, corrupt)
        corrupt = deepcopy(source)
        corrupt['job_input']['palettes_by_character'][3] = 255
        with self.assertRaisesRegex(ValueError, 'palette'):
            skin_inputs(3, 10, corrupt)

    def test_palette_selection_matches_actual_original_role_bindings(self):
        # Frozen outputs are comparisons only; exporter never loads these cases.
        current = json.loads((ROOT/'prototype/data/school_current_units_evidence.json').read_text('utf-8'))
        first = json.loads((ROOT/'prototype/data/school_first_unit_work_evidence.json').read_text('utf-8'))
        native = {u['role']: u['variant'] for u in current['cases'][0]['current_units'] if 'variant' in u}
        native[3] = first['cases'][0]['first_unit_work']['resource_request']['args'][1]
        self.assertEqual(native, {3:3, 4:4, 9:2})
        self.assertEqual({int(k):s['palette_variant'] for k,s in self.catalog['skins'].items()}, native)


if __name__ == '__main__':
    unittest.main()
