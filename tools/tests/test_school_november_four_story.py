import json
import unittest

from tools.school_november_four import ROOT, build, july_date_card
from tools.school_year_story_export import build as build_routes


class NovemberFourStoryTests(unittest.TestCase):
    def test_week_four_courses_lead_to_chapter_076_before_the_next_card(self):
        data = build_routes({76:206}, {(11,5):(None,76,None)})
        encoded = (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(encoded,(ROOT/'prototype/data/school_year_november_five.json').read_bytes())
        self.assertEqual(july_date_card(5,11)[1],(ROOT/'prototype/assets/school_story/tc1105.png').read_bytes())
        scene, = data['scenes']
        self.assertEqual(scene['effects'][0], {'offset':20,'opcode':145,'operands':[4]})
        self.assertEqual(scene['presentation_prefix'][0]['offset'], 28)
        self.assertEqual([i for page in scene['pages'] for i in page['text_indices']], list(range(206)))
        self.assertEqual(len(scene['pages']),122)

    def test_full_chapter_exports_and_date_card_match_shipped_sources(self):
        data = build()
        encoded = (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(encoded,(ROOT/'prototype/data/school_november_four_story.json').read_bytes())
        self.assertEqual(july_date_card(4,11)[1],(ROOT/'prototype/assets/school_story/tc1104.png').read_bytes())
        self.assertEqual([len(scene['pages']) for scene in data['scenes']],[118,58,74,32])
        for scene in data['scenes']:
            self.assertEqual([i for page in scene['pages'] for i in page['text_indices']],
                             list(range(scene['text_count'])))
