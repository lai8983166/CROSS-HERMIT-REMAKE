import json
import unittest
from tools.school_sortie_week_story_export import build, ROOT


class SortieWeekStoryTests(unittest.TestCase):
    def test_shipped_routes_and_export_match_the_checked_in_catalog(self):
        data = build()
        expected = (ROOT / 'prototype/data/school_sortie_week_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode(), expected)
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4b8,0x650,0x6d0])
        self.assertEqual([s['chapter'] for s in data['scenes']], [23,24])
        for scene in data['scenes']:
            self.assertEqual([i for p in scene['pages'] for i in p['text_indices']], list(range(scene['text_count'])))
