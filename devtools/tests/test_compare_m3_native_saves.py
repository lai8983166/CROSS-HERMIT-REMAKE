import hashlib
import unittest
from pathlib import Path

from devtools.compare_m3_native_saves import compare, snapshot


ROOT = Path(__file__).resolve().parents[2]
APRIL = ROOT / 'analysis/downloaded_saves/atwiki-all-characters.SAV'
APRIL_SHA = '9e9fe2beb7420f494d0e1b8ace86eaf49fc86380f5126bc13e9f7937b19d14eb'


class NativeSaveComparison(unittest.TestCase):
    def test_pinned_april_snapshot(self):
        state = snapshot(APRIL.read_bytes(), APRIL_SHA)
        self.assertEqual(state['date'], [4, 1])
        self.assertEqual(state['selected_mission'], 1)
        self.assertEqual(len(state['roles']), 35)
        self.assertEqual(compare(state, state)['growth_differences'], {})
        with self.assertRaisesRegex(ValueError, 'January week 2'):
            compare(state, state, require_44=True)

    def test_same_week_is_too_early_for_return(self):
        before = {'date': [13, 2], 'selected_mission': 44}
        after = {'date': [13, 2], 'departure_mission': 44}
        with self.assertRaisesRegex(ValueError, 'January week 3'):
            compare(before, after, require_44=True)

    def test_separate_integrity_checks(self):
        altered = bytearray(APRIL.read_bytes())
        altered[-10] ^= 1
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            snapshot(altered, APRIL_SHA)
        with self.assertRaisesRegex(ValueError, 'signed checksum'):
            snapshot(altered, hashlib.sha256(altered).hexdigest())
