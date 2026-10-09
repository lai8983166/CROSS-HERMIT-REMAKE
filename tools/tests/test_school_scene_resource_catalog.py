import hashlib
import json
import struct
import unittest
from PIL import Image
from tools.school_scene_resource_catalog import (ROOT,ART,source_catalog,native_fixture,
    minimap_input,pathfinding_input,relocated_pathfinding,map_resource)


class SceneResourceCatalogTests(unittest.TestCase):
    def test_native_vpt_relocations_against_all_original_offsets(self):
        data=source_catalog();fixture=native_fixture();raw,_=map_resource('map05.vpt')
        self.assertEqual([e['relocation_count'] for e in data['pathfinding_sections'][:4]],[120,120,96,120])
        for c in fixture['cases'][:3]:
            p=c['scene_resources']['pathfinding'];entries=data['pathfinding_sections']
            self.assertEqual(p['section_pointers'],[p['pointer']+e['offset'] for e in entries])
            expected=relocated_pathfinding(raw,p['pointer'],entries)
            self.assertEqual(hashlib.sha256(expected).hexdigest(),p['relocated_sha256'])
            for e in entries[4:]:self.assertEqual(expected[e['offset']:e['offset']+e['bytes']],raw[e['offset']:e['offset']+e['bytes']])
        self.assertEqual(data,json.loads((ROOT/'prototype/data/school_scene_resources_rules.json').read_text('utf-8')))
        self.assertEqual(fixture,json.loads((ROOT/'prototype/data/school_scene_resources_evidence.json').read_text('utf-8')))

    def test_runtime_art_pixels_file_hashes_and_independent_minimap(self):
        bmp,_=map_resource('map05.bmp');mini,image=minimap_input(bmp)
        self.assertEqual([mini['width'],mini['height']],[172,128])
        manifest=json.loads((ART/'catalog.json').read_text('utf-8'))
        saved=Image.open(ART/'map05_minimap.png').convert('RGB');self.assertEqual(saved.tobytes(),image.tobytes())
        atlas=Image.open(ART/'map05.png').convert('RGB')
        historical=Image.open(ROOT/'analysis/school-scene5-source-atlas-20261009.png').convert('RGB')
        self.assertEqual(atlas.tobytes(),historical.tobytes())
        for name,label,pixels in [('map05.png','atlas',atlas.tobytes()),('map05_minimap.png','minimap',image.tobytes())]:
            self.assertEqual(hashlib.sha256((ART/name).read_bytes()).hexdigest(),manifest[label+'_file_sha256'])
            self.assertEqual(hashlib.sha256(pixels).hexdigest(),manifest[label+'_rgb_sha256'])

    def test_all_native_map_texture_fields_match_source_entries(self):
        data=source_catalog()
        native=json.loads((ROOT/'analysis/school-scene-resources-v1-20261009.json').read_text('utf-8'))
        for c in native['cases'][:3]:
            entries=[e for e in c['texture_entries'] if e['resource']==5]
            self.assertEqual(len(entries),48)
            for original,actual in zip(data['texture_entries'],entries):
                for key in ('index','offset','file_offset','bytes','header_hex','width','height'):
                    self.assertEqual(actual[key],original[key])

    def test_refuses_malformed_vpt_counts_offsets_marker_and_cell_layers(self):
        raw,_=map_resource('map05.vpt')
        for offset,fmt,value in [(0,'<I',1),(4,'<I',7),(8,'<I',0),(40+16,'<I',1),
                (40+20,'<I',0),(40+24,'<I',0),(40+28,'<I',0xFFFFFFFF)]:
            damaged=bytearray(raw);struct.pack_into(fmt,damaged,offset,value)
            with self.assertRaises(ValueError):pathfinding_input(damaged)
        damaged=bytearray(raw);damaged[40]=0
        with self.assertRaises(ValueError):pathfinding_input(damaged)
        with self.assertRaises(ValueError):pathfinding_input(raw,cells=6143)

    def test_refuses_malformed_minimap_sizes_dimensions_and_format(self):
        raw,_=map_resource('map05.bmp')
        for offset,fmt,value in [(2,'<I',1),(10,'<I',54),(18,'<i',0),(22,'<i',-128),
                (28,'<H',24),(30,'<I',1),(46,'<I',16)]:
            damaged=bytearray(raw);struct.pack_into(fmt,damaged,offset,value)
            with self.assertRaises(ValueError):minimap_input(damaged)
        for damaged in (raw[:-1],raw[:30],bytes(1078)):
            with self.assertRaises(ValueError):minimap_input(damaged)


if __name__=='__main__':unittest.main()
