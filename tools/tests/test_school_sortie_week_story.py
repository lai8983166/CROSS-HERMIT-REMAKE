import json
import unittest
from tools.school_sortie_week_story_export import build, build_week3, build_week4, ROOT


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

    def test_may_week4_routes_page_groups_and_join_order(self):
        data = build_week4()
        expected = (ROOT / 'prototype/data/school_may_week4_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode(), expected)
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4c8, 0x660, 0x4b8])
        self.assertEqual([len(s['pages']) for s in data['scenes']], [46, 140, 17])
        beginning = data['scenes'][1]
        self.assertEqual([e['operands'] for e in beginning['effects'][:2]], [[8], [110]])
        self.assertLess(beginning['effects'][1]['offset'], beginning['pages'][0]['source_offset'])
        for scene in data['scenes']:
            self.assertEqual([i for p in scene['pages'] for i in p['text_indices']], list(range(scene['text_count'])))

    def test_may_week4_join_templates_and_directed_relationships(self):
        data = build_week4()
        student, teacher = data['join_profiles']
        self.assertEqual((student['member_id'], student['job'], student['template_sha256']),
                         (8, 8, '619c963874926481cd610f4bf4fe386970aac5da380e1be362b63051cd03b324'))
        self.assertEqual((teacher['member_id'], teacher['job'], teacher['template_sha256']),
                         (110, 1, 'bc3a30a04ca4e32a3d40c50f9beb18d65354006d9246e43858049bd9cd84cabc'))
        self.assertEqual(data['candidate']['growth_pools'], [100] * 7)
        self.assertEqual(data['candidate']['equipped_items'], [0] * 8)
        self.assertEqual(data['candidate']['job_sums'], [1] * 5)
        self.assertEqual(data['history']['week_records'], [0] * 177)
        members = [101, 3, 4, 9, 5, 8, 110]
        expected = {(a, b) for a in members for b in members if a != b and ({a, b} & {8, 110})}
        self.assertCountEqual([(row['from'], row['to']) for row in data['join_relationships']], expected)
