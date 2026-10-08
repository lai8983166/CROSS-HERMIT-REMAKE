import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest

from PIL import Image
from tools.school_fifth_story_export import export,instructions,GAME,sc_atlas
from tools.tactics_exit_emulation import ROOT


class FifthStoryExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT/'prototype/assets/school_fifth_story'
        cls.data = json.loads((cls.path/'catalog.json').read_text(encoding='utf-8'))

    def test_exact_regeneration_and_source_hashes(self):
        with tempfile.TemporaryDirectory() as path:
            fresh = Path(path);export(fresh)
            for file in self.path.iterdir():
                if file.suffix in ('.json','.png'):
                    self.assertEqual(file.read_bytes(),(fresh/file.name).read_bytes(),file.name)
        for name,sha in self.data['outputs_sha256'].items():
            self.assertEqual(hashlib.sha256((self.path/name).read_bytes()).hexdigest(),sha)
        for name,sha in self.data['source_assets_sha256'].items():
            self.assertEqual(hashlib.sha256((GAME.parent/name).read_bytes()).hexdigest(),sha)

    def test_text_order_cp950_and_slot_replacements(self):
        scene = self.data['scenes'][0]
        self.assertEqual(len(scene['text_pool']),162)
        self.assertEqual(len(scene['pages']),126)
        self.assertEqual([i for p in scene['pages'] for i in p['text_indices']],list(range(162)))
        self.assertEqual(scene['cp950_extension_indices'],[99])
        self.assertEqual(scene['text_pool'][99]['text'],'就是這裏呀。')
        self.assertEqual(scene['pages'][0]['speaker'],'body:9')
        self.assertEqual(scene['pages'][119]['speaker'],'portrait:29')
        self.assertEqual(scene['pages'][121]['speaker'],'portrait:27')
        self.assertEqual([c['asset_key'] for c in scene['pages'][121]['characters']],['portrait:12','portrait:29','portrait:27'])
        self.assertEqual(self.data['actors']['portrait:31']['name'],'莉莉絲')
        self.assertEqual(self.data['actors']['portrait:29']['name'],'瑪貝菈')
        for p in scene['pages']:
            self.assertNotIn('\ufffd',p['text'])
            self.assertIn(p['speaker'],[c['asset_key'] for c in p['characters']])
            self.assertEqual(p['text'],'\n'.join(scene['text_pool'][i]['text'] for i in p['text_indices']))

    def test_source_mc_sc_dimensions_and_expression_pixels(self):
        for actor in self.data['actors'].values():
            expected = (512,768) if actor['kind'] == 'body' else (256,296)
            with Image.open(self.path/actor['image']) as output:
                self.assertEqual(output.size,expected)
                self.assertEqual(output.mode,'RGBA')
                self.assertTrue(any(a[3] for a in output.getdata()))
                if actor['kind'] == 'portrait':
                    atlas = sc_atlas(GAME.parent/actor['source'])
                    x,y = actor['expression_destination'];sx,sy,_,_ = actor['expression_crop']
                    face = atlas.getpixel((sx+50,sy+50))
                    expected_pixel = face if face[3] else atlas.getpixel((x+50,y+50))
                    self.assertEqual(output.getpixel((x+50,y+50)),expected_pixel)
                    self.assertEqual(actor['atlas_size'],[256,512])
        self.assertEqual(len(self.data['outputs_sha256']),9)
        self.assertIn('47',self.data['backgrounds'])

    def test_unknown_control_and_invalid_sc_header_refused(self):
        raw = bytearray((GAME/'DAT/CHAPTER018.YBC').read_bytes())
        struct.pack_into('<H',raw,20,8)
        with self.assertRaisesRegex(ValueError,'unsupported fifth-week'):
            list(instructions(raw))
        with self.assertRaisesRegex(ValueError,'SC atlas header'):
            sc_atlas(GAME/'BIN/TC0405.BIN')


if __name__ == '__main__':
    unittest.main()
