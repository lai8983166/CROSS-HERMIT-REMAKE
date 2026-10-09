import copy
import json
import struct
import unittest
from PIL import Image
from tools.school_scene_map_catalog import (source_catalog, logical_cells, map_textures,
    atlas_image, decode_rgb555, native_fixture)
from tools.school_unitctrl_map_emulation import map_resource
from tools.tactics_exit_emulation import ROOT


class SceneMapCatalogTests(unittest.TestCase):
    def test_saved_source_and_separate_native_fixture(self):
        data=source_catalog();fixture=native_fixture()
        self.assertEqual(data,json.loads((ROOT/'prototype/data/school_scene_map_rules.json').read_text('utf-8')))
        self.assertEqual(fixture,json.loads((ROOT/'prototype/data/school_scene_map_evidence.json').read_text('utf-8')))
        for c in fixture['cases'][:3]:
            m=c['logical_map'];self.assertEqual(m['scene_id'],data['scene_id'])
            self.assertEqual(m['header'][:2],data['logical']['pixel_size'])
            self.assertEqual(m['header'][2:4],data['logical']['cell_size'])
            self.assertEqual(m['source'],data['logical_source'])
            self.assertEqual(c['scene_graphics_request']['source'],data['graphics_source'])
        self.assertNotIn('cases',data)

    def test_original_table_and_all_cell_triples(self):
        data=source_catalog();raw,_=map_resource('map05.bin')
        self.assertEqual([s['filename'] for s in data['selections']],
                         ['map05.bin','map05.map','map05.bmp','map05.vpt'])
        logical=data['logical']
        self.assertEqual(logical['cell_size'],[64,96]);self.assertEqual(logical['pixel_size'],[2048,1536])
        self.assertEqual(logical['object_nonzero_count'],0)
        self.assertEqual(b''.join(struct.pack('<3H',*c) for c in logical['cells']),raw[16:])

    def test_every_texture_page_and_saved_preview_pixel_provenance(self):
        data=source_catalog();raw,_=map_resource('map05.map');logical=data['logical']
        atlas=atlas_image(raw,logical,data['textures'])
        saved=Image.open(ROOT/'analysis/school-scene5-source-atlas-20261009.png').convert('RGB')
        self.assertEqual(atlas.tobytes(),saved.tobytes())
        self.assertEqual(len(data['textures']),48)
        for e in data['textures']:
            ox,oy=e['atlas_origin']
            for x,y in ((0,0),(255,0),(0,255),(255,255),(127,128)):
                word=struct.unpack_from('<H',raw,e['pixel_file_offset']+2*(y*256+x))[0]
                channels=[(word>>shift)&31 for shift in (10,5,0)]
                expected=tuple((c*255)//31 if c in (0,31) else (c<<3)|(c>>2) for c in channels)
                self.assertEqual(atlas.getpixel((ox+x,oy+y)),expected)

    def test_rgb555_channels_and_high_bit(self):
        self.assertEqual(decode_rgb555(struct.pack('<5H',0,0x7c00,0x03e0,0x001f,0xffff)),
                         bytes([0,0,0,255,0,0,0,255,0,0,0,255,255,255,255]))
        with self.assertRaises(ValueError):decode_rgb555(b'\0')

    def test_rejects_logical_header_size_and_dimensions(self):
        raw,_=map_resource('map05.bin')
        for damaged in (raw[:15],raw[:-1],raw+b'\0',bytes(16)+raw[16:]):
            with self.assertRaises(ValueError):logical_cells(damaged)
        for offset in (0,4,8,12):
            damaged=bytearray(raw);struct.pack_into('<H',damaged,offset,1)
            with self.assertRaises(ValueError):logical_cells(damaged)

    def test_rejects_texture_grid_offsets_count_and_page_dimensions(self):
        raw,_=map_resource('map05.map');logical=source_catalog()['logical']
        for offset,value,fmt in ((0,7,'<H'),(0x404,1,'<I'),(0x408,49,'<I'),
                                 (0x40c,0,'<I'),(0x404+200+4,255,'<H')):
            damaged=bytearray(raw);struct.pack_into(fmt,damaged,offset,value)
            with self.assertRaises(ValueError):map_textures(damaged,logical)
        with self.assertRaises(ValueError):map_textures(raw[:-1],logical)
        other=copy.deepcopy(logical);other['texture_page_size']=[128,256]
        with self.assertRaises(ValueError):map_textures(raw,other)


if __name__=='__main__':unittest.main()
