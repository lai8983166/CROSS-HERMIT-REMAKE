"""Authenticate MAP21's runtime actors, route tables, scripts and frame references."""
import json
import struct
import unittest

from tools.school_sortie_export import BASE, GAME, ROOT, SOURCE, digest, record_rules, expected_record


class TwentyOneExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=json.loads((ROOT/'prototype/assets/school_twenty_one/catalog.json').read_text(encoding='utf8'))
        cls.scene=cls.catalog['scenes']['21']

    def test_source_actor_records_and_patrol_routes(self):
        image=SOURCE.read_bytes()
        rules=record_rules(21,image)
        actors=self.scene['actors']
        self.assertEqual(len(actors),91)
        for index,template in enumerate(rules['templates']):
            self.assertEqual(actors[index]['instance_id'],1249-index)
            self.assertEqual(actors[index]['record_hex'],expected_record(template,rules=rules)['record_hex'])
        routes=struct.unpack_from('<I',image,0x6acb88-BASE+21*4)[0]
        for number,rows in self.scene['patrol_routes'].items():
            count,pointer=struct.unpack_from('<II',image,routes-BASE+int(number)*8)
            self.assertEqual(rows,[list(struct.unpack_from('<BB2xIb3x',image,pointer-BASE+i*12)) for i in range(count)])
        self.assertEqual(self.scene['grade_groups'],[list(range(1,5)),list(range(5,18))])

    def test_asset_identity_and_reachable_dialogue(self):
        files={self.scene['atlas']:self.scene['atlas_sha256']}
        for skin in self.catalog['skins'].values():
            for frame in skin['frames'].values():
                self.assertEqual(files.setdefault(frame['file'],frame['file_sha256']),frame['file_sha256'])
        for path,sha in files.items():
            self.assertEqual(digest((ROOT/'prototype'/path.removeprefix('res://')).read_bytes()),sha,path)
        source=(GAME/'DATA/TACTICS/SCRIPT/T0021.BIN').read_bytes()
        self.assertEqual(self.scene['script_sha256'],digest(source))
        self.assertEqual(struct.unpack_from('<HHI',source,0x1f8),(11,8,0xba))
        self.assertEqual(struct.unpack_from('<H',source,0x1c4+0xba)[0],124)
        self.assertEqual([(s['sub'],len(s['pages'])) for s in self.scene['scripts']],
                         [(1,0),(2,1),(5,1),(8,1),(11,1),(14,1),(20,0)])
