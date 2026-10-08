import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from PIL import Image

from tools.school_workroom_export import export,BACKGROUND
from tools.school_fifth_story_export import sc_atlas
from tools.tactics_exit_emulation import ROOT


class WorkroomExportTests(unittest.TestCase):
    def test_byte_exact_regeneration_and_complete_text(self):
        original = ROOT/'prototype/assets/school_workroom'
        with tempfile.TemporaryDirectory() as temp:
            catalog = export(Path(temp))
            for p in Path(temp).iterdir():
                self.assertEqual(p.read_bytes(),(original/p.name).read_bytes(),p.name)
        story = catalog['scenes'][0]
        self.assertEqual(len(story['pages']),32)
        self.assertEqual(len(story['text_pool']),62)
        self.assertEqual([i for p in story['pages'] for i in p['text_indices']],list(range(62)))
        self.assertEqual(story['pages'][0]['speaker'],'narrator')
        self.assertEqual(set(catalog['actors']),{'narrator','portrait:101','portrait:117'})

    def test_original_background_pixel_and_hash(self):
        raw = (ROOT/'CROSS HERMIT/CROSS HERMIT'/BACKGROUND).read_bytes()
        image = Image.open(ROOT/'prototype/assets/school_workroom/background.png')
        self.assertEqual(image.size,(1024,768))
        for x,y in [(0,0),(512,384),(1023,767),(739,640)]:
            value = struct.unpack_from('<H',raw,24+2*(y*1024+x))[0]
            self.assertEqual(image.getpixel((x,y)),(((value>>10)&31)*255//31,
                ((value>>5)&31)*255//31,(value&31)*255//31,255 if value&0x8000 else 0))
        catalog = json.loads((ROOT/'prototype/assets/school_workroom/catalog.json').read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256(raw).hexdigest(),catalog['source_sha256'])

    def test_portrait_geometry_and_native_rgb555_body(self):
        catalog = json.loads((ROOT/'prototype/assets/school_workroom/catalog.json').read_text(encoding='utf-8'))
        for identity in (101,117):
            data = catalog['actors'][f'portrait:{identity}']
            atlas = sc_atlas(ROOT/'CROSS HERMIT/CROSS HERMIT/DATA'/data['source'])
            expected = atlas.crop(tuple(data['body_crop']))
            expected.alpha_composite(atlas.crop(tuple(data['expression_crop'])),tuple(data['expression_destination']))
            image = Image.open(ROOT/'prototype/assets/school_workroom'/data['image'])
            self.assertEqual(image.size,(256,296))
            self.assertEqual(image.tobytes(),expected.tobytes())


if __name__ == '__main__':
    unittest.main()
