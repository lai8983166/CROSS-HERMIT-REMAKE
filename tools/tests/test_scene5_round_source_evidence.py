"""Pin the conditional scene-5 round source to original EXE bytes."""
import json
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IMAGE_BASE = 0x400000


class Scene5RoundSourceEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((
            ROOT / 'prototype/data/scene5_round_source_evidence.json'
        ).read_text('utf-8'))
        cls.exe = (ROOT / cls.fixture['source']).read_bytes()

    @classmethod
    def at(cls, va, size):
        offset = va - IMAGE_BASE
        return cls.exe[offset:offset + size]

    @classmethod
    def call_target(cls, va):
        instruction = cls.at(va, 5)
        assert instruction[0] == 0xe8
        return va + 5 + struct.unpack_from('<i', instruction, 1)[0]

    def test_task_five_calendar_and_round_record(self):
        f = self.fixture
        self.assertEqual(f['schema_version'], 1)
        self.assertEqual(f['evidence_kind'],
                         'static_task_record_and_conditional_round_source_not_playthrough')
        table = int(f['task_table_va'], 0)
        record = int(f['task_record_va'], 0)
        self.assertEqual(record, table + f['task_id'] * f['task_record_stride'])
        self.assertEqual(self.at(table, 20), bytes(20))  # Empty ID 0 is not ID 5.
        gate = f['calendar_gate']
        for field in ('enabled', 'month', 'week'):
            self.assertEqual(self.at(record + gate[field + '_offset'], 1)[0],
                             gate[field])
        rounds = f['rounds']
        self.assertEqual(self.at(record + rounds['count_offset'], 1)[0],
                         rounds['count'])
        for field in ('first_config', 'first_selector'):
            value, = struct.unpack('<H', self.at(record + rounds[field + '_offset'], 2))
            self.assertEqual(value, rounds[field + ('_id' if field == 'first_config'
                                                       else '_word')])

    def test_selected_task_id_is_the_round_table_index(self):
        # Calendar fields gate task availability, but selection is a separate
        # event. The 0x100-stride task ID is copied through two runtime lists.
        self.assertEqual(self.at(0x4a1833, 11), bytes.fromhex(
            'c1e00833c98a88d1be7300'))
        self.assertEqual(self.at(0x4a1850, 11), bytes.fromhex(
            'c1e20833c08a82d2be7300'))
        self.assertEqual(self.at(0x4a1874, 11), bytes.fromhex(
            'c1e20833c08a82d3be7300'))
        self.assertEqual(self.at(0x4a9db5, 11), bytes.fromhex(
            'c1e00833c98a88d6be7300'))
        self.assertEqual(self.at(0x4aa033, 11), bytes.fromhex(
            '668b4d0866898862567a00'))
        self.assertEqual(self.at(0x4a1dcb, 15), bytes.fromhex(
            '668b9262567a00668994089e597d00'))
        self.assertEqual(self.at(0x4a1f1b, 6), bytes.fromhex(
            '66a316ab7a00'))
        self.assertEqual(self.at(0x4a2290, 6), bytes.fromhex(
            '66a316ab7a00'))
        # No eligible group: both counters are cleared, regardless of the
        # selected task's nonzero static round count.
        self.assertEqual(self.at(0x4a6b0e, 26), bytes.fromhex(
            '0fbf45b085c0751766c70596527a00000066c70598527a000000'))
        self.assertEqual(self.at(0x4a6b4d, 21), bytes.fromhex(
            '0fbf5598c1e208660fb682dfbe730066a398527a00'))
        self.assertEqual(self.at(0x4a6b94, 26), bytes.fromhex(
            '0fbf5598c1e2080fbf45ac0fbf4dac6bc970668b9482e0be7300'))

    def test_first_round_config_selects_scene_five(self):
        f = self.fixture
        config = int(f['config_record_va'], 0)
        self.assertEqual(config, int(f['config_table_va'], 0) +
                         f['rounds']['first_config_id'] * f['config_stride'])
        scene_id, = struct.unpack('<H', self.at(config, 2))
        self.assertEqual(scene_id, f['config_scene_id'])
        self.assertEqual(scene_id, 5)
        # The preparation task passes this ID to the configuration loader.
        self.assertEqual(self.call_target(0x4b9052), 0x4da860)
        self.assertEqual(self.call_target(0x4da87e), 0x4da8a0)
        self.assertEqual(self.call_target(0x4da8bc), 0x4da8e0)
        self.assertEqual(self.at(0x4da8f8, 11), bytes.fromhex(
            '8b45086bc02a05d0d16a00'))
        self.assertEqual(self.at(0x4da913, 6), bytes.fromhex(
            '668b02668901'))
        # Configuration loading resets the mode flag; a later branch may set it.
        self.assertEqual(self.at(0x4da93a, 7), bytes.fromhex(
            '8b55fcc6420900'))

    def test_mode_flag_is_not_a_static_task_record_field(self):
        mode = self.fixture['mode_flag_provenance']
        self.assertEqual(mode['address'], '0x7f4491')
        self.assertEqual(mode['config_loader_reset_va'], '0x4da93a')
        self.assertEqual(self.call_target(int(mode['network_task_caller_va'], 0)),
                         0x448a30)
        self.assertEqual(self.call_target(int(mode['network_config_load_va'], 0)),
                         0x4da860)
        for name in ('network_set_one_va', 'other_set_one_va'):
            self.assertEqual(self.at(int(mode[name], 0), 7),
                             bytes.fromhex('c60591447f0001'))
        self.assertEqual(self.at(int(mode['saved_value_restore_va'], 0), 5),
                         bytes.fromhex('a291447f00'))
        self.assertEqual(self.at(int(mode['conditional_clear_va'], 0), 7),
                         bytes.fromhex('c60591447f0000'))
        self.assertTrue(mode['state12_branch_requires_live_value'])

    def test_first_round_uses_original_group_member_ids(self):
        source = self.fixture['first_round_roster_source']
        self.assertEqual(self.fixture['rounds']['first_selector_word'] & 0x7ff,
                         source['selector_low_11_bits'])
        self.assertEqual(source['selector_low_11_bits'], 1)
        self.assertEqual(source['eligible_group_state'], 2)
        self.assertEqual(self.at(0x4a6bdb, 18), bytes.fromhex(
            '0fbf5598c1e208668b82e2be73006625ff07'))
        self.assertEqual(self.at(0x4a6c60, 3), bytes.fromhex('83fa02'))
        self.assertEqual(self.at(int(source['group_member_id_write_va'], 0), 8),
                         bytes.fromhex('6689845122aa7a00'))
        self.assertEqual(self.at(int(source['round_member_id_read_va'], 0), 8),
                         bytes.fromhex('668b944222aa7a00'))
        self.assertEqual(self.at(int(source['round_member_id_write_va'], 0), 8),
                         bytes.fromhex('66899471d0527a00'))
        self.assertEqual(source['group_member_id_table_va'], '0x7aaa22')
        self.assertEqual(source['round_member_id_table_va'], '0x7a52d0')
        prior = json.loads((ROOT / 'prototype/data/all_result_recipient_evidence.json')
                           .read_text('utf-8'))
        for init in prior['participant_list_builder']['conditional_initial_roster']:
            self.assertEqual(init['character_ids'],
                             source['conditional_initial_group0_ids'])


if __name__ == '__main__':
    unittest.main()
