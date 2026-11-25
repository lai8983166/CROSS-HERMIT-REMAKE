import json
import unittest

from tools.school_november_four import ROOT, build, july_date_card


class NovemberFourStoryTests(unittest.TestCase):
    def test_full_chapter_exports_and_date_card_match_shipped_sources(self):
        data = build()
        encoded = (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(encoded,(ROOT/'prototype/data/school_november_four_story.json').read_bytes())
        self.assertEqual(july_date_card(4,11)[1],(ROOT/'prototype/assets/school_story/tc1104.png').read_bytes())
        self.assertEqual([len(scene['pages']) for scene in data['scenes']],[118,58,74,32])
        for scene in data['scenes']:
            self.assertEqual([i for page in scene['pages'] for i in page['text_indices']],
                             list(range(scene['text_count'])))
