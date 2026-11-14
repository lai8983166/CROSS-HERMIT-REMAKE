import json
import struct
import unittest

from tools.school_postbattle_story_export import catalog, GAME, CHAPTERS
from tools.tactics_exit_emulation import ROOT


class PostbattleStoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = catalog()

    def test_export_is_exact_and_all_source_text_occurs_once(self):
        encoded = (json.dumps(self.data, ensure_ascii=False, indent=2)+'\n').encode('utf8')
        self.assertEqual(encoded, (ROOT/'prototype/data/school_postbattle_story.json').read_bytes())
        self.assertEqual([len(s['pages']) for s in self.data['scenes']], [281,43,79,8])
        for scene in self.data['scenes']:
            self.assertEqual([i for p in scene['pages'] for i in p['text_indices']], list(range(scene['text_count'])))
            for page in scene['pages']:
                self.assertTrue(page['text'])
                self.assertNotIn('\ufffd', page['text'])
                self.assertTrue(page['speaker'])

    def test_join_immediate_operands_and_terminal_effects(self):
        scenes={s['chapter']:s for s in self.data['scenes']}
        self.assertEqual(scenes[20]['effects'][0], {'offset':20,'opcode':144,'operands':[5]})
        self.assertIn({'offset':0xba8,'opcode':153,'operands':[1,6,0]}, scenes[20]['effects'])
        self.assertEqual([e['operands'] for e in scenes[208]['effects'] if e['opcode']==151], [[9,1]])
        self.assertEqual([e['operands'] for e in scenes[208]['effects'] if e['opcode']==91], [[8,2]])

    def test_linear_script_has_no_unresolved_conditional_or_dynamic_text(self):
        # Independent instruction scan: source branch/choice instructions may
        # not silently turn into a linear presentation. op13 is VWAITKB.
        for chapter in CHAPTERS:
            raw=(GAME/f'DAT/CHAPTER{chapter:03}.YBC').read_bytes()
            at,end=struct.unpack_from('<2I',raw,4)
            instructions=[]
            while at<end:
                opcode,size=struct.unpack_from('<2H',raw,at)
                self.assertNotIn(opcode,{8,9,10,11,16,18})
                self.assertGreaterEqual(size,4)
                instructions.append(opcode)
                at+=size
            self.assertEqual(at,end)
            self.assertEqual(instructions[-1],19)  # CODE_END, see ybc32_opcodes.md


if __name__=='__main__':unittest.main()
