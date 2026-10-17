import json
import unittest

from tools.school_owner_platform import OwnerPlatform, ROOT, HELPER, sha
from tools.school_owner_startup import FONT_ARGS


class PlatformTests(unittest.TestCase):
    def test_live_screen_dc_timer_font_and_cleanup(self):
        with OwnerPlatform() as platform:
            self.assertTrue(platform.request('GetDC')['result'])
            self.assertEqual(platform.request('QueryPerformanceCounter')['result'], 1)
            self.assertEqual(platform.request('QueryPerformanceFrequency')['result'], 1)
            font = platform.request('CreateFontA', args=FONT_ARGS[:-1], face_hex='b2d3a9fac5e920')['result']
            info = platform.request('GetObjectA', pointer=font, before_hex='cc'*60)
            self.assertEqual(info['result'], 60)
            self.assertEqual(len(bytes.fromhex(info['hex'])), 60)
        self.assertEqual(platform.cleanup, dict(fonts_released=1, dcs_released=1, all_owned_resources_released=True))

    def test_foreign_font_bad_buffer_duplicate_dc_and_closed_requests_refused(self):
        with OwnerPlatform() as platform:
            platform.request('GetDC')
            with self.assertRaises(ValueError):
                platform.request('GetDC')
            with self.assertRaises(ValueError):
                platform.request('GetObjectA', pointer=1, before_hex='a5'*60)
            font = platform.request('CreateFontA', args=FONT_ARGS[:-1], face_hex='b2d3a9fac5e920')['result']
            with self.assertRaises(ValueError):
                platform.request('GetObjectA', pointer=font, before_hex='00')
        with self.assertRaises(ValueError):
            platform.request('QueryPerformanceCounter')

    def test_fixed_current_and_archived_v1_source_identities(self):
        current = json.loads((ROOT/'analysis/school-owner-startup-platform-v2-20261017.json').read_text(encoding='utf-8'))
        old = json.loads((ROOT/'analysis/school-owner-startup-platform-v1-20261017.json').read_text(encoding='utf-8'))
        self.assertEqual(sha(HELPER.read_bytes()), current['build']['helper_sha256'])
        self.assertEqual(sha((ROOT/'tools/school_owner_platform.cs').read_bytes()), current['build']['source_sha256'])
        self.assertEqual(sha((ROOT/'analysis/school-owner-startup-platform-v1.cs').read_bytes()), old['build']['source_sha256'])
