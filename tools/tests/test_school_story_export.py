import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest

from PIL import Image
from tools.school_story_export import export,instructions,GAME
from tools.tactics_exit_emulation import ROOT


class SchoolStoryExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = ROOT/'prototype/assets/school_story'
        cls.data = json.loads((cls.directory/'catalog.json').read_text(encoding='utf-8'))

    def test_regeneration_is_byte_exact(self):
        with tempfile.TemporaryDirectory() as path:
            regenerated = Path(path)
            export(regenerated)
            for file in self.directory.iterdir():
                if file.suffix in ('.json','.png'):
                    self.assertEqual(file.read_bytes(),(regenerated/file.name).read_bytes(),file.name)
        for file,sha in self.data['outputs_sha256'].items():
            self.assertEqual(hashlib.sha256((self.directory/file).read_bytes()).hexdigest(),sha)

    def test_dialogue_coverage_speakers_and_strict_decoding(self):
        self.assertEqual([len(s['pages']) for s in self.data['scenes']],[66,43])
        self.assertEqual([len(s['text_pool']) for s in self.data['scenes']],[103,59])
        for scene in self.data['scenes']:
            sequence = [i for page in scene['pages'] for i in page['text_indices']]
            self.assertEqual(sequence,list(range(len(scene['text_pool']))))
            for page in scene['pages']:
                self.assertNotIn('\ufffd',page['text'])
                self.assertIn(str(page['speaker']),self.data['actors'])
                self.assertIn(str(page['background']),self.data['backgrounds'])
                self.assertEqual(page['text'],'\n'.join(scene['text_pool'][i]['text'] for i in page['text_indices']))
        self.assertEqual(self.data['scenes'][0]['pages'][0]['speaker'],4)
        self.assertEqual(self.data['scenes'][0]['pages'][1]['speaker'],101)
        self.assertEqual(self.data['scenes'][1]['pages'][0]['speaker'],130)
        self.assertEqual(self.data['scenes'][1]['normalized_fullwidth_space_indices'],[32,33,34,35,51,53])
        self.assertEqual(self.data['actors']['130']['name'],'夏朧')
        self.assertEqual(self.data['actors']['7']['name'],'羅沙麗亞')

    def test_atlas_dimensions_expression_and_background_resources(self):
        for identity in (4,7,130):
            actor = self.data['actors'][str(identity)]
            x,y = actor['expression_destination']
            with Image.open(self.directory/actor['image']) as image:
                self.assertEqual(image.size,(512,768))
                self.assertGreater(image.getpixel((x+64,y+64))[3],0)
        self.assertEqual(self.data['backgrounds']['8']['source'],'ADV/BIN/BG002_D.BIN')
        self.assertEqual(self.data['backgrounds']['52']['source'],'ADV/BIN/BG013_D.BIN')

    def test_unsupported_control_and_malformed_container_refused(self):
        raw = bytearray((GAME/'DAT/CHAPTER016.YBC').read_bytes())
        struct.pack_into('<H',raw,20,8) # A conditional branch cannot become linear dialogue.
        with self.assertRaisesRegex(ValueError,'unsupported presentation'):
            list(instructions(raw))
        struct.pack_into('<I',raw,4,30)
        with self.assertRaisesRegex(ValueError,'offsets'):
            list(instructions(raw))


if __name__ == '__main__':
    unittest.main()
