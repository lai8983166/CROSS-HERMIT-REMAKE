"""MAP31 resources, all five outcomes, and the source state tests at 4356B0."""
import hashlib
import json
import unittest

from tools.school_adventure_scene_rules import catalog
from tools.school_sortie_export import GAME, ROOT, SOURCE, expected_record, record_rules
from tools.school_thirty_one_rules import rules
from tools.tactics_exit_emulation import TASK
from tools.tests.test_school_twenty_two_battle import Objective


class RescueObjective(Objective):
    def __init__(self):
        super().__init__()
        self._function_ranges += ((0x4356b0, 0x43583c), (0x431d40, 0x431dca),
                                  (0x432040, 0x432100), (0x469220, 0x4692d4),
                                  (0x469480, 0x4694f6), (0x43bb90, 0x43bd00))
        logical = (GAME/'DATA/TACTICS/MAP/MAP31.BIN').read_bytes()
        self.uc.mem_write(TASK+0x10000, logical)
        self.write(TASK+0x3d68+0x2659c, TASK+0x10000)

    def rescue(self, states, arrived, losses, down):
        self.sub = -1
        self.write(TASK+0x174, 0)
        self.write(TASK+0x2ef34, losses, 'B')
        self.actor(0, 3, 0, 4 if down else 1)
        for i, (state, inside) in enumerate(zip(states, arrived, strict=True)):
            work = self.actor(237-i, 172+i, 0, state)
            self.write(work+0x2ec, (10 if inside else 77)*32*65536)
            self.write(work+0x2f0, (87 if inside else 51)*16*65536)
        self.call(0x4356b0)
        return self.sub, self.read(TASK+0x174)


class ThirtyOneBattle(unittest.TestCase):
    def test_original_priority_and_states(self):
        m = RescueObjective()
        for states, arrived, losses, down, result in (
                ((1,1,1),(1,1,1),0,True,(2,1)), ((1,1,1),(1,1,1),1,True,(5,2)),
                ((2,1,1),(1,1,1),0,True,(8,3)), ((3,4,1),(0,0,1),1,True,(8,3)),
                ((2,3,4),(0,1,0),0,True,(11,4)), ((1,1,1),(0,1,1),0,True,(14,5)),
                ((1,1,1),(0,1,1),0,False,(-1,0)), ((0,1,1),(1,1,1),0,False,(-1,0))):
            with self.subTest(states=states, arrived=arrived):
                self.assertEqual(m.rescue(states, arrived, losses, down), result)

    def test_records_map_scripts_and_assets(self):
        mission = json.loads((ROOT/'prototype/data/school_mandatory_thirty_one.json').read_bytes())
        self.assertEqual(mission, rules())
        catalog_data = json.loads((ROOT/'prototype/assets/school_thirty_one/catalog.json').read_bytes())
        scene = catalog_data['scenes']['31']
        source = catalog((31,), (146,))['scenes']['31']
        self.assertEqual(scene['scripts'], source['scripts'])
        self.assertEqual(scene['regions']['1'], [y*96+x for x,y in source['event1_cells']])
        originals = record_rules(31, SOURCE.read_bytes())
        for actor, template in zip(scene['actors'], originals['templates'], strict=True):
            self.assertEqual(actor['record_hex'], expected_record(template, rules=originals)['record_hex'])
        self.assertEqual([a['identity'] for a in scene['actors'][12:15]], [172,173,174])
        self.assertEqual(set(map(int,scene['player_skins'])), {1,2,3,5,6,7,8,9,11,13,14,15,16,17,18,28,32})
        refs = {f['file']: f['file_sha256'] for skin in catalog_data['skins'].values() for f in skin['frames'].values()}
        refs[scene['atlas']] = scene['atlas_sha256']
        for path, digest in refs.items():
            self.assertEqual(hashlib.sha256((ROOT/'prototype'/path.removeprefix('res://')).read_bytes()).hexdigest(), digest)
