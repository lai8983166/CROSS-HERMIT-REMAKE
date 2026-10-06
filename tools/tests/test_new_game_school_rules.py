import json
import unittest

from tools.new_game_school_rules import ROOT, rules, report_text


class SchoolRuntimeRulesTests(unittest.TestCase):
    def test_runtime_input_regenerates_from_source_without_expected_snapshots(self):
        path = ROOT/'prototype/data/new_game_school_rules.json'
        expected = rules()
        self.assertEqual(report_text(expected).encode(),path.read_bytes())
        self.assertEqual(set(expected),{'origin_rules','course_rules','sort_rules','work_rules'})
        def walk(value):
            if isinstance(value,dict):
                self.assertTrue(set(value).isdisjoint({'after','before','cases','canonical_after','ratings'}))
                for child in value.values():
                    walk(child)
            elif isinstance(value,list):
                for child in value:
                    walk(child)
        walk(json.loads(path.read_text('utf-8')))


if __name__ == '__main__':
    unittest.main()
