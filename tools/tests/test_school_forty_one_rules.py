"""Compare the exported MAP41 outcomes with bounded original x86 on declared inputs."""
import json
import unittest

from tools.school_forty_one_rules import ROOT, rules
from tools.tactics_exit_emulation import TASK
from tools.tests.test_school_twenty_two_battle import Objective


class FortyOneObjective(Objective):
    def __init__(self):
        super().__init__()
        self._function_ranges += ((0x435cd0, 0x435dc0), (0x431d40, 0x431dca), (0x469170, 0x469220))

    def result(self, state, owned, losses, remaining, party_down):
        self.sub = -1
        self.write(TASK + 0x174, 0)
        self.write(TASK + 0x2ef34, losses, 'B')
        self.write(TASK + 0x2e6f4, remaining)
        actors = [self.actor(0, 3, 0, 4 if party_down else 1),
                  self.actor(249, 446, 5, state), self.actor(248, 389, 0 if owned else 7, 1)]
        self.write(TASK + 0xdc8ec, len(actors))
        for index, work in enumerate(actors):
            self.write(TASK + 0xdc8f0 + index * 4, work)
        self.call(0x435cd0)
        return self.sub, self.read(TASK + 0x174)


class FortyOneRules(unittest.TestCase):
    def test_catalog_and_source_priority(self):
        data = json.loads((ROOT / 'prototype/data/school_mandatory_forty_one.json').read_bytes())
        self.assertEqual(data, rules())
        self.assertEqual(data['adventure']['rounds'], [{'scene_id': 41, 'selection_word': 1}])
        self.assertEqual(data['scene']['template_count'], 106)
        self.assertEqual([t['sub'] for t in data['opening_timers']], [20] * 5 + [21] * 5)
        machine = FortyOneObjective()
        for row, inputs in zip(data['objective']['priority'], [
                (4, True, 0, 0, True), (4, True, 1, 0, True), (4, False, 0, 0, True),
                (3, True, 0, 0, True), (1, True, 0, 1, True)], strict=True):
            with self.subTest(inputs=inputs):
                self.assertEqual(machine.result(*inputs), (row['ending_sub'], row['selector']))
        self.assertEqual(machine.result(3, True, 0, 1, False), (-1, 0))
