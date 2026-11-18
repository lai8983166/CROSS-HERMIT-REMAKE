import json
import unittest
from tools.school_sortie_week_story_export import build, build_week3, ROOT


class SortieWeekStoryTests(unittest.TestCase):
    def test_shipped_routes_and_export_match_the_checked_in_catalog(self):
        data = build()
        expected = (ROOT / 'prototype/data/school_sortie_week_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode(), expected)
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4b8,0x650,0x6d0])
        self.assertEqual([s['chapter'] for s in data['scenes']], [23,24])
        for scene in data['scenes']:
            self.assertEqual([i for p in scene['pages'] for i in p['text_indices']], list(range(scene['text_count'])))

    def test_may_week3_routes_chain_and_all_source_text(self):
        data = build_week3()
        expected = (ROOT / 'prototype/data/school_may_week3_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode(), expected)
        self.assertEqual([r['date'] for r in data['routes']], [[5,2],[5,3],[5,3]])
        self.assertEqual([len(s['pages']) for s in data['scenes']], [20,103,233])
        self.assertEqual(data['scenes'][1]['effects'][0]['target'], 'data/adv/dat/Chapter027.ybc')
        self.assertEqual(data['routes'][2]['effects'][0]['operands'], [11,1])
        for scene in data['scenes']:
            self.assertEqual([i for p in scene['pages'] for i in p['text_indices']], list(range(scene['text_count'])))
