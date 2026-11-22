"""MAP22/T0022 bytes, art and bounded original objective/grade dispatch."""
import hashlib
import json
import struct
import unittest

from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_adventure_scene_rules import catalog
from tools.school_sortie_export import GAME, ROOT, SOURCE, expected_record, record_rules
from tools.tactics_exit_emulation import ExitEmulator, TASK


class Objective(ExitEmulator):
    """Original predicates on a declared work list. Only script presentation is stubbed."""
    def __init__(self):
        super().__init__()
        self._function_ranges = (
            (0x4352f0, 0x435410), (0x4307b0, 0x430978), (0x430ba0, 0x430c28),
            (0x430df0, 0x430f60), (0x431cc0, 0x431d34), (0x431dd0, 0x431e83),
            (0x454ab0, 0x454bb0), (0x456b20, 0x456b60), (0x468d10, 0x468d80),
            (0x468e10, 0x468ea8), (0x4695d0, 0x469656), (0x469ad0, 0x469d26),
            (0x46a430, 0x46a5db), (0x46a950, 0x46aa22))
        self._stubs = {0x56ce80: ('debug_stack_check', 0), 0x454bb0: ('presentation', 12)}
        self.write(TASK+0x117c38, TASK)
        self.write(TASK+0x115aac+5, 1, 'B')  # faction 5 hostile to player 0
        self.write(0x7f4491, 0, 'B')  # single player

    def _hook(self, uc, address, size, data):
        if address == 0x454bb0:
            self.sub = self.read(uc.reg_read(UC_X86_REG_ESP)+12)
        super()._hook(uc, address, size, data)

    def actor(self, slot, role, side, state):
        work = TASK+0x80aec+slot*0x520
        record = TASK+0x30000+slot*0xb0
        self.write(work, 1, 'H')
        self.write(work+0x258, record)
        self.write(record+2, role, 'H')
        self.write(record+0xa4, side, 'B')
        self.write(record+0xf, state, 'B')
        return work

    def grade(self, elapsed, remaining, hostile, owned, losses, down):
        self.sub = -1
        self.write(TASK+0x174, 0)
        self.write(TASK+0x2e6f8, elapsed)
        self.write(TASK+0x2e6f4, remaining)
        self.write(TASK+0x2ef34, losses, 'B')
        # Give the chest the *opposite* ownership. A hostile spring is
        # active in every case, even when no rival student remains.
        active = [self.actor(0, 3, 0, 4 if down else 1),
                  self.actor(249, 406, 7 if owned else 0, 1),
                  self.actor(248, 388, 0 if owned else 7, 1),
                  self.actor(247, 394, 5, 1)]
        enemy = self.actor(242, 11, 5, 1 if hostile else 4)
        if hostile:
            active.append(enemy)
        self.write(TASK+0xdc8ec, len(active))
        for i, work in enumerate(active):
            self.write(TASK+0xdc8f0+i*4, work)
        self.call(0x4352f0)
        return self.sub, self.read(TASK+0x174)


class TwentyTwoSource(unittest.TestCase):
    def test_original_predicates_and_selector(self):
        machine = Objective()
        for inputs, expected in [
                ((18000,18000,False,False,0,True),(2,1)),
                ((18000,18000,False,True,1,False),(5,2)),
                ((18001,17999,False,True,0,False),(8,3)),
                ((36000,0,False,False,1,True),(8,3)),
                ((35998,2,True,True,0,False),(-1,0)),
                ((35998,2,True,True,1,True),(14,5)),
                ((36000,0,True,False,0,True),(11,4)),
                ((36000,0,True,True,0,True),(3,1)),
                ((36000,0,True,True,1,True),(6,2))]:
            with self.subTest(inputs=inputs):
                self.assertEqual(machine.grade(*inputs), expected)

    def test_templates_maps_scripts_and_art(self):
        source = catalog((22,))['scenes']['22']
        data = json.loads((ROOT/'prototype/assets/school_twenty_two/catalog.json').read_bytes())
        scene = data['scenes']['22']
        self.assertEqual(scene['scripts'],source['scripts'])
        self.assertEqual(scene['script_sha256'],source['script_sha256'])
        self.assertEqual([(s['sub'],len(s['pages'])) for s in scene['scripts']],
                         [(1,5),(2,0),(3,0),(5,0),(6,0),(8,0),(11,0),(14,0)])
        image = SOURCE.read_bytes()
        self.assertEqual(struct.unpack_from('<hh',image,0x5ff838-0x400000),(2,-1))
        self.assertEqual(scene['grade_objects'],[2])
        rules = record_rules(22,image)
        for template, actor in zip(rules['templates'],scene['actors'],strict=True):
            self.assertEqual(actor['record_hex'],expected_record(template,rules=rules)['record_hex'])
            self.assertEqual(image[0x6b2daa-0x400000+64*actor['job']],0)
            if actor['category']==5:
                ai = bytes.fromhex(template)[0x14:]
                self.assertEqual((ai[0x10],ai[0x11],ai[0x1c]),(0,9,0))
        self.assertEqual([a['identity'] for a in scene['actors']],[406,388,394,394,394,394,394,11,18,19,20,21])
        self.assertEqual(len(scene['player_skins']),11)
        logical = (GAME/'DATA/TACTICS/MAP/MAP22.BIN').read_bytes()
        self.assertEqual(struct.unpack_from('<HH',logical,4),(64,96))
        self.assertEqual(len(scene['cells']),64*96)
        frames = [f for skin in data['skins'].values() for f in skin['frames'].values()]
        delta = json.loads((ROOT/'prototype/assets/school_twenty_two_actions/catalog.json').read_bytes())
        self.assertEqual(set(delta),{'job9_v4','job388_v0','job394_v0'})
        for key, extra in delta.items():
            merged = {**data['skins'][key]['frames'], **extra['frames']}
            self.assertEqual(set(extra['actions']),{'basic_cast','basic_attack','basic_recover'})
            self.assertTrue(any(step['layers'] for step in extra['actions']['basic_attack']['N']['steps']))
            for action in extra['actions'].values():
                for facing in action.values():
                    for step in facing['steps']:
                        self.assertTrue(all(str(layer['frame']) in merged for layer in step['layers']))
            frames.extend(extra['frames'].values())
        for ref in frames+[dict(file=scene['atlas'],file_sha256=scene['atlas_sha256'])]:
            self.assertEqual(hashlib.sha256((ROOT/'prototype'/ref['file'].removeprefix('res://')).read_bytes()).hexdigest(),ref['file_sha256'])
