import hashlib
import json
import struct
import unittest
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

from tools.campaign_preparation_fixture import fixture
from tools.tactics_exit_emulation import ROOT, SOURCE, report_text


class CampaignPreparationFixtureTests(unittest.TestCase):
    def test_export_is_byte_exact_and_keeps_continuous_native_before_and_after(self):
        exported = fixture()
        raw = report_text(exported).encode('utf-8')
        self.assertEqual((ROOT / 'prototype/data/campaign_preparation_evidence.json').read_bytes(), raw)
        native = json.loads((ROOT / 'analysis/campaign-scene5-v1-20261004.json').read_bytes())
        for case, source in zip(exported['cases'], native['cases']):
            self.assertEqual(case['before_world'], source['before_world'])
            self.assertEqual(case['expected_after'], source['campaign']['upstream']['before_result'])
            self.assertEqual(case['inputs']['result_inputs'], source['state11_entry_inputs'])
        self.assertEqual(exported['native_report_sha256'], hashlib.sha256(
            (ROOT / 'analysis/campaign-scene5-v1-20261004.json').read_bytes()).hexdigest())

    def test_loot_and_job_rules_are_actual_image_bytes(self):
        rules = fixture()['rules']
        image = SOURCE.read_bytes()
        for job in range(31):
            self.assertEqual(rules['job_rate_classes'][job], image[0x6B2D8A + job*64 - 0x400000])
        for item in range(1, 361):
            self.assertEqual(rules['item_types'][item-1], struct.unpack_from('<h', image,
                0x6D5120 + item*56 - 0x400000)[0])
        for grade in range(5):
            self.assertEqual(rules['loot_quotas'][grade], list(struct.unpack_from('<7h', image,
                0x73BF1A + 5*256 + grade*14 - 0x400000)))
        self.assertEqual(rules['fixed_items'], [0]*8)
        self.assertEqual(rules['objective_rewards'][0], [0, 3, 1])

    def test_native_preparation_order_and_task37_skill_guard_are_source_instructions(self):
        image = SOURCE.read_bytes()
        instructions = Cs(CS_ARCH_X86, CS_MODE_32).disasm(
            image[0x4BBCC0-0x400000:0x4BBD40-0x400000], 0x4BBCC0)
        calls = [int(ins.op_str, 16) for ins in instructions if ins.mnemonic == 'call' and ins.op_str.startswith('0x')]
        relevant = [call for call in calls if call in (0x4BD210, 0x4BCA40, 0x4BBD40)]
        self.assertEqual(relevant, [0x4BD210, 0x4BCA40, 0x4BBD40])
        self.assertEqual(image[0x4BD28A-0x400000:0x4BD28D-0x400000], bytes.fromhex('83fa25'))
        self.assertEqual(image[0x4BD28D-0x400000:0x4BD28F-0x400000], bytes.fromhex('7405'))

    def test_full_preparation_diff_contains_only_packages_total_and_actual_loot(self):
        for case, expected_items in zip(fixture()['cases'], ([14, 41], [8, 14, 38, 65])):
            before, after = case['before_world'], case['expected_after']
            original = {r['character_id']: r for r in before['characters']}
            for record in after['characters']:
                normalized = dict(record)
                old = original[record['character_id']]
                for field in ['staged_package', 'staged_total']:
                    normalized[field] = old[field]
                self.assertEqual(normalized, old)
                if record['character_id'] == 5:
                    self.assertEqual(record, old)
            self.assertEqual([i+1 for i,(a,b) in enumerate(zip(before['item_flags'],after['item_flags']))
                if a != b], expected_items)
            normalized = dict(after)
            for field in ['characters', 'item_flags', 'global_total_511c']:
                normalized[field] = before[field]
            self.assertEqual(normalized, before)
            self.assertFalse(fixture()['live_witness'])
            self.assertFalse(fixture()['authorizes_persistent_write'])


if __name__ == '__main__':
    unittest.main()
