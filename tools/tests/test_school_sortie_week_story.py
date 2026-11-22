import json
import unittest
from tools.school_sortie_week_story_export import build, build_week3, build_week4, build_week5, build_june_week1, build_june_week2, build_june_week3, build_june_week4, build_june_week5, build_july_week1, build_july_week2, build_july_week3, build_july_week4, build_july_week5, build_august_week1, build_august_week2, build_august_week3, build_august_week4, build_august_week5, build_september_week1, build_september_week2, build_september_week3, build_september_week4, july_date_card, ROOT


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

    def test_june_week3_two_chapter_chains_and_direct_school_entry(self):
        data = build_june_week3()
        expected = (ROOT / 'prototype/data/school_june_week3_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode(), expected)
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4e8,0x680,0x6d0])
        self.assertEqual([(s['chapter'], len(s['pages']), s['text_count']) for s in data['scenes']],
                         [('039A',75,87),(40,65,103),(41,6,11),(210,29,60)])
        first, _, week, final = data['scenes']
        self.assertEqual(first['effects'][0]['target'], 'data/adv/dat/Chapter040.ybc')
        self.assertEqual(week['effects'][0]['target'], 'data/adv/dat/Chapter210.ybc')
        self.assertEqual([e['operands'] for e in final['effects']], [[16,1],[6,2]])
        self.assertNotIn('effects', data['routes'][2])
        self.assertIsNone(data['routes'][2]['target'])
        self.assertFalse(any(e['opcode']==144 for s in data['scenes'] for e in s['effects']))

    def test_june_week4_empty_post_sortie_removal_and_school_music(self):
        data = build_june_week4()
        expected = (ROOT / 'prototype/data/school_june_week4_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode(), expected)
        post, start, school = data['routes']
        self.assertEqual(post['date'], [6,3])
        self.assertEqual(post['offsets'][-3:], [0x5b8,0x5c0,0x5d0])
        self.assertNotIn(0x5c8, post['offsets'])
        self.assertEqual(post['effects'], [{'offset':0x5b8,'opcode':145,'operands':[117]}])
        self.assertIsNone(post['target'])
        self.assertEqual(start['target'], 'data/adv/dat/Chapter213.ybc')
        self.assertIsNone(school['target'])
        self.assertNotIn('effects', school)
        self.assertEqual([(s['chapter'], len(s['pages']), s['text_count']) for s in data['scenes']], [(213,13,25)])

    def test_june_week5_teacher_and_chapter_chain(self):
        data = build_june_week5()
        expected = (ROOT / 'prototype/data/school_june_week5_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode(), expected)
        self.assertEqual(data['routes'][0]['offsets'][-2:], [0x5c8, 0x5d0])
        self.assertEqual([(s['chapter'], len(s['pages']), s['text_count']) for s in data['scenes']],
                         [(42,95,118),(302,60,118)])
        self.assertEqual(data['scenes'][0]['effects'][0]['target'], 'data/adv/dat/Chapter302.ybc')
        self.assertEqual([r['member_id'] for r in data['join_profiles']], [118])
        self.assertEqual(len(data['join_relationships']),22)

    def test_july_week1_both_routes_no_roster_effects(self):
        data = build_july_week1()
        expected = (ROOT / 'prototype/data/school_july_week1_story.json').read_bytes()
        self.assertEqual((json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode(), expected)
        self.assertEqual([r['date'] for r in data['routes']], [[6,5],[7,1],[7,1]])
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x5d0,0x698,0x6d0])
        self.assertEqual([(s['chapter'], len(s['pages']), s['text_count']) for s in data['scenes']],
                         [(303,32,60),(218,19,25)])
        self.assertEqual(data['scenes'][0]['effects'][0]['target'], 'data/adv/dat/Chapter218.ybc')

    def test_july_week2_direct_date_card_and_week3_chapter(self):
        for week, data in ((2, build_july_week2()), (3, build_july_week3())):
            raw = (ROOT/f'prototype/data/school_july_week{week}_story.json').read_bytes()
            self.assertEqual(raw, (json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode())
            self.assertEqual([r['date'] for r in data['routes']], [[7,week-1],[7,week],[7,week]])
            self.assertNotIn('effects', data['routes'][0])
        card = build_july_week2()
        self.assertEqual(card['scenes'], [])
        self.assertEqual(card['date_card']['position'], [0,324])
        self.assertEqual(card['date_card']['source_rect'], [0,0,1024,128])
        self.assertEqual(card['date_card']['wait_ticks'], 600)
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0702.png').read_bytes(), july_date_card()[1])
        chapter = build_july_week3()['scenes'][0]
        self.assertEqual([chapter['chapter'],len(chapter['pages']),chapter['text_count']], [209,52,75])

    def test_july_week4_mandatory_nine_return_and_chapter_card(self):
        data = build_july_week4()
        actual = (ROOT/'prototype/data/school_july_week4_story.json').read_bytes()
        self.assertEqual((json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode(),actual)
        self.assertEqual([r['date'] for r in data['routes']], [[7,3],[7,4],[7,4]])
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x5d0,0x6a8,0x6d0])
        scene = data['scenes'][0]
        self.assertEqual((scene['chapter'],len(scene['pages']),scene['text_count']), (214,30,49))
        self.assertLess(scene['presentation_prefix'][-1]['offset'], scene['pages'][0]['source_offset'])
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0704.png').read_bytes(),july_date_card(4)[1])

    def test_july_week5_chapter304_double_join_and_chapter305_card(self):
        data = build_july_week5()
        actual = (ROOT/'prototype/data/school_july_week5_story.json').read_bytes()
        self.assertEqual((json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode(),actual)
        self.assertEqual([r['date'] for r in data['routes']], [[7,4],[7,5],[7,5]])
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4f0,0x6b0,0x6d0])
        self.assertEqual([(s['chapter'],len(s['pages']),s['text_count']) for s in data['scenes']], [(304,70,100),(305,21,40)])
        self.assertEqual([j['candidate']['character_id'] for j in data['joins']],[16,17])
        self.assertEqual([len(j['join_relationships']) for j in data['joins']],[24,26])
        self.assertLess(data['scenes'][0]['effects'][-1]['offset'],data['scenes'][0]['pages'][0]['source_offset'])
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0705.png').read_bytes(),july_date_card(5)[1])

    def test_july_week5_routes_to_august_card_and_school(self):
        data = build_august_week1()
        self.assertEqual((ROOT/'prototype/data/school_august_week1_story.json').read_bytes(),
                         (json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode())
        self.assertEqual(data['scenes'],[])
        self.assertEqual([r['date'] for r in data['routes']],[[7,5],[8,1],[8,1]])
        self.assertEqual([r['offsets'][-1] for r in data['routes']],[0x5d0,0x10b0,0x6d0])
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0801.png').read_bytes(),july_date_card(1,8)[1])

    def test_august_week2_mandatory20_and_chapter220_card(self):
        data = build_august_week2()
        self.assertEqual((ROOT/'prototype/data/school_august_week2_story.json').read_bytes(),
                         (json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode())
        self.assertEqual([r['offsets'][-1] for r in data['routes']],[0x5d0,0x6b8,0x6d0])
        scene, = data['scenes']
        self.assertEqual((scene['chapter'],len(scene['pages']),scene['text_count']),(220,6,11))
        self.assertLess(scene['presentation_prefix'][-1]['offset'],scene['pages'][0]['source_offset'])
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0802.png').read_bytes(),july_date_card(2,8)[1])

    def test_august_week3_roll_call_and_chapter221_card(self):
        data = build_august_week3()
        self.assertEqual((ROOT/'prototype/data/school_august_week3_story.json').read_bytes(),
                         (json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode())
        self.assertEqual([r['offsets'][-1] for r in data['routes']],[0x5d0,0x6c0,0x6d0])
        scene, = data['scenes']
        self.assertEqual((scene['chapter'],len(scene['pages']),scene['text_count']),(221,34,43))
        self.assertEqual([p['speaker_id'] for p in scene['pages'] if p['text'].strip()=='\u662f\u3002'],
                         [3,4,9,5,6,8,1,2,16,17])
        self.assertLess(scene['presentation_prefix'][-1]['offset'],scene['pages'][0]['source_offset'])
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0803.png').read_bytes(),july_date_card(3,8)[1])

    def test_august_week4_rain_date_card_and_recruits(self):
        data = build_august_week4()
        self.assertEqual((ROOT/'prototype/data/school_august_week4_story.json').read_bytes(),
                         (json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode())
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x4f8,0x10b0,0x4c8])
        self.assertEqual([(s['chapter'],len(s['pages']),s['text_count']) for s in data['scenes']],
                         [('043A',40,78),(45,39,40),(306,38,60)])
        self.assertEqual(data['scenes'][0]['effects'][0]['target'],'data/adv/dat/Chapter045.ybc')
        self.assertEqual([p['member_id'] for p in data['join_profiles']],[13,116])
        self.assertEqual(len(data['join_relationships']),58)
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0804.png').read_bytes(),july_date_card(4,8)[1])

    def test_august_five_both_work_routes_and_chapter235(self):
        data = build_august_week5()
        self.assertEqual((ROOT/'prototype/data/school_august_week5_story.json').read_bytes(),
                         (json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode())
        self.assertEqual([(s['chapter'],len(s['pages']),s['text_count']) for s in data['scenes']],
                         [(46,26,45),(47,24,42),(235,16,28)])
        self.assertEqual(data['scenes'][1]['effects'][0]['target'],'data/adv/dat/Chapter235.ybc')
        for scene in data['scenes']:
            self.assertEqual([i for p in scene['pages'] for i in p['text_indices']],list(range(scene['text_count'])))
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0805.png').read_bytes(),july_date_card(5,8)[1])

    def test_september_chapter049_card_and_school_entry(self):
        data = build_september_week1()
        self.assertEqual((ROOT/'prototype/data/school_september_week1_story.json').read_bytes(),
                         (json.dumps(data,ensure_ascii=False,indent=2)+chr(10)).encode())
        scene, = data['scenes']
        self.assertEqual((scene['chapter'],len(scene['pages']),scene['text_count']),(49,157,264))
        self.assertEqual([i for page in scene['pages'] for i in page['text_indices']],list(range(264)))
        self.assertLess(scene['presentation_prefix'][-1]['offset'],scene['pages'][0]['source_offset'])
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0901.png').read_bytes(),july_date_card(1,9)[1])

    def test_september_courses_to_week_two_school(self):
        data = build_september_week2()
        actual = ROOT/'prototype/data/school_september_week2_story.json'
        self.assertEqual(actual.read_bytes(), (json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode())
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x508, 0x6d8, 0x6d0])
        self.assertEqual([(s['chapter'], len(s['pages']), s['text_count']) for s in data['scenes']],
                         [(50, 88, 116), (51, 51, 65)])
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0902.png').read_bytes(), july_date_card(2, 9)[1])

    def test_september_week_three_chapter052(self):
        data = build_september_week3()
        actual = ROOT/'prototype/data/school_september_week3_story.json'
        self.assertEqual(actual.read_bytes(), (json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode())
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x5d0, 0x6e0, 0x6d0])
        scene, = data['scenes']
        self.assertEqual((scene['chapter'],len(scene['pages']),scene['text_count']), (52,22,29))
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0903.png').read_bytes(), july_date_card(3,9)[1])

    def test_adventure22_postbattle_chain_and_week_four(self):
        data = build_september_week4()
        actual = ROOT/'prototype/data/school_september_week4_story.json'
        self.assertEqual(actual.read_bytes(), (json.dumps(data, ensure_ascii=False, indent=2)+chr(10)).encode())
        self.assertEqual([r['offsets'][-1] for r in data['routes']], [0x510, 0x6e8, 0x6d0])
        self.assertEqual([(s['chapter'],len(s['pages']),s['text_count']) for s in data['scenes']],
                         [(53,64,112),(308,43,90),(224,14,29)])
        self.assertEqual(data['scenes'][0]['effects'][0]['target'],'data/adv/dat/Chapter308.ybc')
        self.assertEqual((ROOT/'prototype/assets/school_story/tc0904.png').read_bytes(), july_date_card(4,9)[1])
