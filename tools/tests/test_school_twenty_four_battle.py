"""Execute the original MAP24 objective branch and authenticate the exported resources."""
import hashlib
import json
import struct
import unittest

from tools.school_adventure_scene_rules import catalog
from tools.school_sortie_export import GAME, ROOT, SOURCE, expected_record, record_rules
from tools.tactics_exit_emulation import TASK
from tools.tests.test_school_twenty_two_battle import Objective


class RescueObjective(Objective):
    def __init__(self):
        super().__init__()
        self._function_ranges += (
            (0x435410, 0x435598), (0x431d40, 0x431dca), (0x469170, 0x469220),
            (0x4e2760, 0x4e2990), (0x4e29a0, 0x4e2c20))

    def result(self, bosses, protected, owned, losses, down):
        self.sub = -1
        self.write(TASK+0x174, 0)
        self.write(TASK+0x2ef34, losses, 'B')
        active = [self.actor(0, 3, 0, 4 if down else 1)]
        for ordinal, role, side, state in [
                (56, 460, 5, bosses[0]), (57, 460, 5, bosses[1]),
                (9, 461, 4, protected[0]), (10, 462, 4, protected[1])]:
            active.append(self.actor(250-ordinal, role, side, state))
        for ordinal in range(2, 7):
            active.append(self.actor(250-ordinal, 388 if ordinal<4 else 394,
                                     0 if ordinal-2<owned else 7, 1))
        self.write(TASK+0xdc8ec, len(active))
        for i, work in enumerate(active):
            self.write(TASK+0xdc8f0+i*4, work)
        self.call(0x435410)
        return self.sub, self.read(TASK+0x174)


class TwentyFourSource(unittest.TestCase):
    def test_original_branch_priority_and_selectors(self):
        machine = RescueObjective()
        for inputs, expected in [
                (((4,4),(4,4),5,0,True),(2,1)),
                (((4,4),(1,1),5,1,False),(5,2)),
                (((4,4),(1,4),4,0,True),(8,3)),
                (((4,3),(1,1),5,0,False),(-1,0)),
                (((3,4),(4,1),5,0,True),(11,4)),
                (((4,1),(1,4),5,0,True),(11,4)),
                (((0,0),(3,1),0,0,True),(14,5))]:
            with self.subTest(inputs=inputs):
                self.assertEqual(machine.result(*inputs), expected)

    def test_source_records_region_and_art(self):
        data = json.loads((ROOT/'prototype/assets/school_twenty_four/catalog.json').read_bytes())
        scene = data['scenes']['24']
        image = SOURCE.read_bytes()
        self.assertEqual(struct.unpack_from('<6h',image,0x5ff83c-0x400000),(2,3,4,5,6,-1))
        source = catalog((24,), (112,146,159))['scenes']['24']
        self.assertEqual(scene['scripts'],source['scripts'])
        logical = (GAME/'DATA/TACTICS/MAP/MAP24.BIN').read_bytes()
        self.assertEqual(scene['regions']['1'],[i for i in range(96*144) if logical[18+i*6]==1])
        rules = record_rules(24,image)
        self.assertEqual(len(scene['actors']),74)
        for template, actor in zip(rules['templates'],scene['actors'],strict=True):
            self.assertEqual(actor['record_hex'],expected_record(template,rules=rules)['record_hex'])
        frames = [f for skin in data['skins'].values() for f in skin['frames'].values()]
        for ref in frames+[dict(file=scene['atlas'],file_sha256=scene['atlas_sha256'])]:
            path = ROOT/'prototype'/ref['file'].removeprefix('res://')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),ref['file_sha256'])
