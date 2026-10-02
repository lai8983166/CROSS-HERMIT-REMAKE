"""Native skill/post-field boundary probes and independent fixture provenance."""
import hashlib
import importlib.util
import json
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.role_application_emulation import report, RoleApplicationEmulator
    from tools.role_application_fixture import fixture, REPORT, REPORT_SHA256
    from tools.tactics_exit_emulation import SOURCE, ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class RoleApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.tasks = {c['name']: c for c in cls.report['task_cases']}
        cls.probes = {c['name']: c for c in cls.report['skill_probes']}

    def test_native_report_reexecutes_exactly(self):
        self.assertEqual(REPORT.read_bytes().decode('utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', REPORT.read_bytes())

    def test_zero_task_teacher_slots_have_real_relation_writes(self):
        case = self.tasks['ordinary_confirm']
        self.assertEqual(case['school_setup']['teacher_ids'], [-1]*5)
        self.assertEqual(case['school_setup']['task_teacher_slots'], [0]*5)
        self.assertEqual(len(case['after']['relationships']), 12)
        for relation in case['after']['relationships']:
            self.assertEqual(relation['value'], 51 if 0 in (relation['from'], relation['to']) else 54)
        for name in ('ordinary_unconfirmed', 'mvp_boundary_busy', 'mode1_flag0', 'mode1_flag1'):
            c = self.tasks[name]
            self.assertEqual(c['before']['relationships'], c['after']['relationships'])

    def test_skill_random_attribute_pending_and_job_boundaries(self):
        expected = [('skill8_candidate', 8, 2), ('skill8_random_reject', 8, 0),
            ('skill8_attribute_reject', 8, 0), ('skill8_already_pending', 8, 2),
            ('skill61_job_below', 61, 0), ('skill61_job_exact', 61, 2)]
        for name, sid, status in expected:
            c = self.probes[name]
            self.assertEqual(c['after']['characters'][0]['skill_statuses'][sid-1], status)
            changed = name in ('skill8_candidate', 'skill61_job_exact')
            self.assertEqual(c['skill_display_needed'], int(changed))
            for key in ('job_progress_values', 'week_records_hex', 'recipient_count'):
                self.assertEqual(c['before']['characters'][0][key], c['after']['characters'][0][key])
            self.assertFalse(c['state12_executed'])
            self.assertFalse(c['authorizes_persistent_write'])

    def test_random_state_is_original_crt_and_blocked_candidate_consumes_none(self):
        for c in self.report['skill_probes']:
            state = c['synthetic_probe']['clock_seed']
            for draw in c['learning_draws']:
                state = (state*214013+2531011) & 0xFFFFFFFF
                self.assertEqual(draw['native_rand_state'], state)
                self.assertEqual(draw['rand'], (state >> 16) & 32767)
                self.assertEqual(draw['modulo101'], draw['rand'] % 101)
            self.assertEqual(c['native_rand_state'], state)
        self.assertEqual(self.probes['skill8_already_pending']['learning_draws'], [])
        self.assertEqual(self.probes['skill8_random_reject']['learning_draws'][0]['modulo101'], 94)

    def test_signed_progress_wrap_sentinel_and_cap_are_native_outputs(self):
        c = self.report['post_field_probes'][0]
        self.assertEqual([r['job_progress'] for r in c['before']['characters']], [127, 100, 99])
        self.assertEqual([r['job_progress'] for r in c['after']['characters']], [0, 100, 99])
        self.assertFalse(c['state12_executed'])
        self.assertIn('0x4c16c0', c['visited_original_addresses'])

    def test_source_tables_and_fixture_are_not_model_generated(self):
        f = fixture()
        stored = ROOT / 'prototype/data/role_application_evidence.json'
        self.assertEqual(stored.read_text(encoding='utf-8'), report_text(f))
        self.assertEqual(hashlib.sha256(stored.read_bytes()).hexdigest(),
            'b0c1f014711dabe3a70482967f58761d8915779da1bbcfcf2eadb18969d38055')
        image = SOURCE.read_bytes()
        req = struct.unpack_from('<13h', image, 0x74F686+61*0x32-0x400000)
        self.assertEqual(f['rules']['skills'][60]['minimum_job_sums'], list(req[8:13]))
        self.assertEqual(f['rules']['skills'][60]['minimum_job_sums'], [0, 0, 0, 0, 9])
        self.assertEqual(f['rules']['skill_grid'][1], [8, 10, 9, 11, 12, 78, 14])
        self.assertEqual(f['rules']['job_skill_caps'][10], [0, 1, 0, 1, 0, 0, 7, 7, 7, 7, 7])
        self.assertFalse(f['authorizes_persistent_write'])

    def test_full_progress_snapshot_and_nonparticipants_are_preserved(self):
        for c in self.report['task_cases']:
            for record in c['after']['characters']:
                self.assertEqual(len(record['job_progress_values']), 31)
                self.assertEqual(len(record['learning_job_sums']), 5)
            for key in ('month', 'week', 'global_total_511c',
                        'nonparticipant_character_sha256', 'nonparticipant_package_hex'):
                self.assertEqual(c['before'][key], c['after'][key])
            self.assertFalse(c['live_witness'])
            self.assertFalse(c['authorizes_persistent_write'])

    def test_undeclared_skill_probe_inputs_fail(self):
        emulator = RoleApplicationEmulator()
        for kwargs in ({'skill_id': 0}, {'skill_id': 85}, {'seed': 1}, {'job_progress': 10}):
            with self.assertRaises(ValueError):
                emulator.probe_skill('invalid', **kwargs)


if __name__ == '__main__':
    unittest.main()
