import json
import struct
import unittest

from tools.school_december_two import december_two, ROOT, july_date_card
from tools.school_story_export import GAME, immediate


class DecemberTwoStoryTests(unittest.TestCase):
    def test_each_original_jump_path_matches_exported_speakers_text_and_joins(self):
        data = december_two()
        scene, = data['scenes']
        self.assertEqual((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode(),
                         (ROOT/'prototype/data/school_year_december_two.json').read_bytes())
        self.assertEqual(july_date_card(2,12)[1], (ROOT/'prototype/assets/school_story/tc1202.png').read_bytes())
        raw = (GAME/'DAT/CHAPTER309.YBC').read_bytes()
        _, start, end, pool, _ = struct.unpack_from('<5I',raw)
        for choice, first, last, joins in ((0,49,92,[20,21]),(1,93,141,[19])):
            board, lines, joined = {}, [], []
            at = start
            while at < end:
                op, size = struct.unpack_from('<HH',raw,at)
                buf = raw[at+4:at+size]
                at += size
                if op in (22,27,29,30,33):
                    key, speaker, *_ = immediate(buf)
                    board[key] = speaker
                elif op == 26:
                    _, key, speaker, _ = immediate(buf)
                    board[key] = speaker
                elif op == 43:
                    active, = immediate(buf)
                elif op == 17:
                    index, = struct.unpack('<H',buf)
                    lines.append((index,board[active]))
                elif op == 61:
                    reg, count, *indices = struct.unpack('<4I',buf)
                    self.assertEqual((reg,count),(0,2))
                    for i,index in enumerate(indices):
                        offset = pool+struct.unpack_from('<H',raw,pool+4+index*4)[0]
                        self.assertEqual(scene['choice_labels'][i],raw[offset:raw.index(0,offset)].decode('cp950'))
                elif op == 8:
                    comparison, reg, value, target = struct.unpack('<4I',buf)
                    self.assertEqual((comparison,reg),(1,0))
                    if value == 0x20000000+choice:
                        at = start+target
                elif op == 11:
                    at = start+struct.unpack('<I',buf)[0]
                elif op == 144:
                    joined.extend(immediate(buf))
            expected = [(index,p['speaker_id']) for p in scene['pages'] for index in p['text_indices']
                        if index < 47 or first <= index <= last]
            self.assertEqual(expected,lines)
            self.assertEqual(joins,joined)
