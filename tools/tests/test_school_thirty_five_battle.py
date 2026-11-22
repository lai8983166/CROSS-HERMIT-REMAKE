"""Scene 35 script, statue, terrain and presentation projections."""
import hashlib
import json
import struct
import unittest
from collections import Counter

from tools.school_adventure_scene_rules import catalog
from tools.school_sortie_export import GAME, ROOT, SOURCE, record_rules, expected_record


class ThirtyFiveSource(unittest.TestCase):
    def test_compact_catalog_matches_original_script_and_records(self):
        source = catalog((35,))['scenes']['35']
        data = json.loads((ROOT/'prototype/assets/school_thirty_five/catalog.json').read_bytes())
        scene = data['scenes']['35']
        self.assertEqual(scene['script_sha256'], source['script_sha256'])
        self.assertEqual(scene['scripts'], source['scripts'])
        self.assertEqual([(s['sub'],len(s['pages'])) for s in scene['scripts']],
                         [(1,0),(2,1),(5,1),(8,1),(11,1),(14,1)])
        image = SOURCE.read_bytes()
        for skill in (11,20,31,57,59):
            offset = 0x6c2dc8-0x400000+72*skill
            self.assertEqual(scene['spells']['rows'][str(skill)],image[offset:offset+72].hex())
        for role in (427,428,429,430):
            self.assertEqual(image[0x6b2daa-0x400000+64*role],0)
        for key in scene['player_skins'].values():
            attack = data['skins'][key]['actions']['basic_attack']['N']
            self.assertTrue(any(step['layers'] for step in attack['steps']))
        rules = record_rules(35,image)
        self.assertEqual(len(rules['templates']),36)
        self.assertEqual([r['record_hex'] for r in scene['actors']],
                         [expected_record(t,rules=rules)['record_hex'] for t in rules['templates']])
        self.assertEqual(Counter(r['character_id'] for r in scene['actors']),{427:29,428:4,429:2,430:1})
        self.assertTrue(all(r['combat']['movement_rate']==0 and r['state']==1 for r in scene['actors']))
        logical = (GAME/'DATA/TACTICS/MAP/MAP35.BIN').read_bytes()
        self.assertEqual(struct.unpack_from('<HH',logical,4),(64,96))
        self.assertEqual(len(scene['cells']),64*96)
        for ref in [dict(file=scene['atlas'],file_sha256=scene['atlas_sha256'])] + [
                f for skin in data['skins'].values() for f in skin['frames'].values()]:
            disk = ROOT/'prototype'/ref['file'][6:] if ref['file'].startswith('res://') else ROOT/'prototype/assets/school_thirty_five'/ref['file']
            self.assertEqual(hashlib.sha256(disk.read_bytes()).hexdigest(),ref['file_sha256'])
