import json
import unittest
from tools.school_sortie_week_story_export import build, build_week3, build_week4, build_week5, build_june_week1, build_june_week2, ROOT


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

    def test_may_week5_uses_dated_030b_registers_two_members_and_returns(self):
        data = build_week5()
        expected = (ROOT / 'prototype/data/school_may_week5_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode(), expected)
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4d0, 0x668, 0x6d0])
        self.assertEqual([(s['chapter'], len(s['pages'])) for s in data['scenes']], [('030B', 71), (31, 55)])
        self.assertEqual([p['member_id'] for p in data['join_profiles']], [6, 115])
        self.assertEqual(data['candidate']['attributes'], [64,14,7,25,2,55,18])
        self.assertEqual(len(data['join_relationships']), 30)
        for scene in data['scenes']:
            self.assertEqual([i for p in scene['pages'] for i in p['text_indices']], list(range(scene['text_count'])))

    def test_june_week1_registers_student_before_first_page_and_routes_to_mandatory_school(self):
        data = build_june_week1()
        expected = (ROOT / 'prototype/data/school_june_week1_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode(), expected)
        self.assertEqual([r['date'] for r in data['routes']], [[5,5],[6,1],[6,1]])
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4d8,0x670,0x6d0])
        self.assertEqual([(s['chapter'], len(s['pages']), s['text_count']) for s in data['scenes']],
                         [(32, 68, 85), (33, 58, 83)])
        scene = data['scenes'][1]
        self.assertLess(scene['effects'][0]['offset'], scene['pages'][0]['source_offset'])
        self.assertEqual([p['member_id'] for p in data['join_profiles']], [1])
        self.assertEqual(data['candidate']['equipped_items'], [189] + [0]*7)
        existing = [101,3,4,9,5,8,110,6,115]
        self.assertCountEqual([(r['from'],r['to']) for r in data['join_relationships']],
                              [(1,i) for i in existing]+[(i,1) for i in existing])

    def test_june_week2_chapter_chains_registration_and_workroom_entry(self):
        data = build_june_week2()
        actual = (ROOT / 'prototype/data/school_june_week2_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode(), actual)
        self.assertEqual([r['date'] for r in data['routes']], [[6,1],[6,2],[6,2]])
        self.assertEqual([(s['chapter'], len(s['pages']), s['text_count']) for s in data['scenes']],
                         [(35,81,108),(36,20,47),(37,79,119),(38,71,96),(39,128,163)])
        pre, join, week, workroom, entry = data['scenes']
        self.assertEqual(pre['effects'][0]['target'], 'data/adv/dat/Chapter036.ybc')
        self.assertEqual(week['effects'][0]['target'], 'data/adv/dat/Chapter038.ybc')
        self.assertLess(join['effects'][0]['offset'], join['pages'][0]['source_offset'])
        self.assertEqual(data['candidate']['character_id'], 2)
        self.assertEqual(data['candidate']['attributes'], [7,42,3,18,24,27,32])
        self.assertEqual(len(data['join_relationships']), 20)
        self.assertEqual([e['operands'] for e in workroom['effects']], [[6,1],[7,2]])
        self.assertEqual(entry['effects'][0]['operands'], [11,0])
