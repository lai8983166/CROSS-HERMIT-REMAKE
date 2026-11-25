"""Compare MAP41, the wave script, actor records and frames with the source projection."""
import hashlib
import json
import struct
import unittest

from tools.school_adventure_scene_rules import catalog
from tools.school_sortie_export import BASE, GAME, ROOT, SOURCE, expected_record, record_rules


class FortyOneBattle(unittest.TestCase):
    def test_map_actors_animations_and_factions(self):
        source = SOURCE.read_bytes()
        data = json.loads((ROOT / 'prototype/assets/school_forty_one/catalog.json').read_bytes())
        scene = data['scenes']['41']
        logical = (GAME / 'DATA/TACTICS/MAP/MAP41.BIN').read_bytes()
        self.assertEqual(struct.unpack_from('<HH', logical, 4), (128, 192))
        self.assertEqual(len(scene['cells']), 128 * 192)
        self.assertEqual(scene['origin'], [8, 183])
        rules = record_rules(41, source)
        self.assertEqual(len(scene['actors']), 106)
        for actor, template in zip(scene['actors'], rules['templates'], strict=True):
            self.assertEqual(actor['record_hex'], expected_record(template, rules=rules)['record_hex'])
        self.assertEqual(set(map(int, scene['player_skins'])),
                         {1,3,4,5,6,8,9,11,13,14,15,16,17,18,32})
        # 468BC0 initializes single-player relations; 46A6A0 admits both 1 and 2.
        self.assertEqual(source[0x618568-BASE+5:0x618568-BASE+8], bytes([1, 2, 3]))
        self.assertEqual(scene['actors'][27]['identity'], 413)
        self.assertEqual(bytes.fromhex(scene['actors'][27]['record_hex'])[0xa4], 6)
        refs = {frame['file']: frame['file_sha256'] for skin in data['skins'].values()
                for frame in skin['frames'].values()}
        refs[scene['atlas']] = scene['atlas_sha256']
        for path, digest in refs.items():
            self.assertEqual(hashlib.sha256((ROOT / 'prototype' / path.removeprefix('res://')).read_bytes()).hexdigest(), digest)

    def test_script_pages_routes_and_independent_entrance_draw(self):
        data = json.loads((ROOT / 'prototype/assets/school_forty_one/catalog.json').read_bytes())
        scene = data['scenes']['41']
        self.assertEqual(scene['scripts'], catalog((41,), (146,))['scenes']['41']['scripts'])
        self.assertEqual([(s['sub'],len(s['pages'])) for s in scene['scripts']],
                         [(1,3),(2,2),(5,2),(8,2),(11,2),(14,2),(20,0),(21,0)])
        for script, centers, delay in zip(scene['scripts'][-2:],
                ([(13,29),(9,145),(39,189)], [(62,3),(114,115)]), (7200,1800), strict=True):
            values = [(cmd['opcode'],cmd['values']) for cmd in script['commands']]
            self.assertEqual([tuple(v[1:3]) for op,v in values if op==130], centers)
            self.assertEqual([v[:4] for op,v in values if op==146 and v[1]==2],
                             [[4,2,1,3],[5,2,1,len(centers)],[1,2,900,delay]])
        self.assertEqual(scene['patrol_routes'], {'1':[[110,28,0,-1]],
                         '2':[[110,23,0,-1]],'3':[[117,29,0,-1]]})
