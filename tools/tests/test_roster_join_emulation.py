"""Native opcode144 side effects, availability gate and independent fixture."""
import hashlib
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.roster_join_emulation import CHAPTER, report
    from tools.roster_join_fixture import REPORT, REPORT_SHA256, fixture
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class RosterJoinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def candidate(self, snapshot):
        return next(c for c in snapshot['participants'] if c['character_id'] == 5)

    def test_report_and_fixture_reproduce_exact_native_bytes(self):
        self.assertEqual(REPORT.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(), REPORT_SHA256)
        path = ROOT / 'prototype/data/roster_join_evidence.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(fixture()))
        self.assertNotIn(b'\r', REPORT.read_bytes())
        self.assertNotIn(b'\r', path.read_bytes())

    def test_sourced_opcode_runs_all_join_helpers_without_completion_stub(self):
        chapter = CHAPTER.read_bytes()
        self.assertEqual(struct.unpack_from('<II', chapter, 20), (0x00080090, 0x20000005))
        self.assertEqual(hashlib.sha256(chapter).hexdigest(), self.report['source_chapter020_sha256'])
        for c in self.cases.values():
            self.assertEqual(c['commands'], [{'frame': -1, 'offset': 20, 'opcode': 144, 'advance': 8}]
                             * (2 if c['repeat_opcode'] else 1))
            self.assertEqual(c['join_entries'][0], {'va': '0x4d3e90', 'caller_return_va': '0x4d096b',
                'character_id': 5, 'group': -1, 'slot': -1})
            self.assertEqual((c['vm_active'], c['vm_pc']), (1, 8))
            self.assertNotIn('vm_update', c['stub_calls'])
        c = self.cases['chapter020_join5']
        for address in ('0x4d0900', '0x4d3e90', '0x4d4730', '0x4d58e0', '0x4d3aa0'):
            self.assertIn(address, c['visited_original_addresses'])

    def test_join_resets_unlocks_but_preserves_progress_growth_and_calendar(self):
        c = self.cases['chapter020_join5']
        b, a = self.candidate(c['before']), self.candidate(c['after'])
        self.assertEqual(a['job_progress'], list(range(-15, 16)))
        self.assertEqual(a['unlock_reserved_bytes'], [0, 0])
        self.assertEqual(a['unlock_flags'], [1]*10+[0]*20)
        self.assertEqual((b['level_50'], a['level_50']), (47, 28))
        for key in ('job', 'attributes', 'growth_pools', 'job_progress'):
            self.assertEqual(a[key], b[key])
        for key in ('month', 'week', 'flags', 'teacher_count', 'teacher_ids',
                    'group_student_ids', 'group_student_indices'):
            self.assertEqual(c['after'][key], c['before'][key])
        self.assertEqual(c['after']['student_ids'], [3, 4, 9, 5]+[-1]*16)
        self.assertEqual(c['after']['student_count'], 4)
        self.assertEqual(c['after']['availability'][5], 1)
        for b, a in zip(c['before']['participants'], c['after']['participants']):
            if b['character_id'] != 5:
                self.assertEqual(a, b)

    def test_claims_free_item_and_removes_occupied_and_duplicate_equipment(self):
        for name in ('chapter020_join5', 'difficulty2_clears_equipped_skills'):
            c = self.cases[name]
            self.assertEqual(self.candidate(c['after'])['equipped_items'], [6]+[0]*7)
            flags = c['before']['item_flags'].copy()
            flags[5] = 0x30b
            self.assertEqual(c['after']['item_flags'], flags)

    def test_skill_updates_use_skill_id_and_difficulty_branch(self):
        low = self.candidate(self.cases['chapter020_join5']['after'])
        high = self.candidate(self.cases['difficulty2_clears_equipped_skills']['after'])
        self.assertEqual(low['skill_statuses'][:3], [6, 6, 0])
        self.assertEqual(low['equipped_skills'], [1, 2, 1]+[0]*5)
        self.assertEqual(high['skill_statuses'], self.candidate(
            self.cases['difficulty2_clears_equipped_skills']['before'])['skill_statuses'])
        self.assertEqual(high['equipped_skills'], [0]*8)

    def test_existing_and_duplicate_join_are_native_noops(self):
        c = self.cases['already_available_noop']
        self.assertEqual(c['before'], c['after'])
        self.assertNotIn('0x4d3aa0', c['visited_original_addresses'])
        c = self.cases['duplicate_join_opcode']
        self.assertEqual(c['after_once'], c['after'])
        self.assertEqual(len(c['join_entries']), 2)
        self.assertEqual(c['after']['student_count'], 4)

    def test_prefix_evidence_never_claims_chapter_school_or_persistent_completion(self):
        self.assertFalse(self.report['live_witness'])
        self.assertFalse(self.report['authorizes_persistent_write'])
        for c in self.cases.values():
            for key in ('chapter_completed', 'school_initialized', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(c[key])


if __name__ == '__main__':
    unittest.main()
