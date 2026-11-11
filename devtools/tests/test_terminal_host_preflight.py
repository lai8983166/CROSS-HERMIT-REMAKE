"""Offline rejection and pixel tests. Never query a desktop or launch a game."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
from devtools import terminal_host_capture as capture
from devtools import terminal_host_menu_preflight as menu


class HostPreflightTests(unittest.TestCase):
    def test_capture_disabled_before_any_native_import_or_action(self):
        with patch.object(capture.subprocess, 'run', side_effect=AssertionError('must not execute')):
            with self.assertRaises(PermissionError):
                capture.capture_owned(None, 0, 'unused.png')

    def test_capture_timeout_cannot_be_extended(self):
        with self.assertRaises(ValueError):
            capture.capture_owned(None, 0, 'unused.png', explicit_capture_override=True, timeout=6)

    def test_alpha_noise_is_not_visual_content(self):
        pixels = b''.join(bytes((0, 0, 0, i % 256)) for i in range(64*64))
        with self.assertRaisesRegex(ValueError, 'uniform'):
            capture.pixels_to_png(64, 64, pixels)

    def test_untouched_capture_rejected(self):
        with self.assertRaisesRegex(ValueError, 'uniform'):
            capture.pixels_to_png(64, 64, bytes([0xA5]) * (64*64*4))

    def test_bgrx_orientation_and_pixels_preserved(self):
        pixels = bytes((0, 0, 255, 0))*64 + bytes((255, 0, 0, 0))*(63*64)
        png = capture.pixels_to_png(64, 64, pixels)
        with Image.open(io.BytesIO(png)) as image:
            self.assertEqual(image.getpixel((0, 0)), (255, 0, 0))
            self.assertEqual(image.getpixel((0, 63)), (0, 0, 255))

    def test_truncated_and_oversized_frames_refused(self):
        with self.assertRaises(ValueError): capture.pixels_to_png(64, 64, b'')
        for shape in ((0, 768), (True, 768), (4096, 4096)):
            with self.assertRaises(ValueError): capture.image_shape(*shape)

    def test_stale_or_overlong_desktop_window_refused(self):
        for deadline in (99, 200, 701):
            with self.assertRaises(ValueError): menu.validate_window(deadline, 100)
        self.assertEqual(menu.validate_window(700, 100), 600)

    def test_run_disabled_before_native_import_or_game_launch(self):
        with self.assertRaises(PermissionError): menu.run(Path('unused'), 0, False)

    def test_image_review_must_match_exact_capture(self):
        # Temporary synthetic receipts stay on F, no screenshots or native calls.
        with tempfile.TemporaryDirectory(dir=menu.ROOT / '.venv-audit') as directory:
            path = Path(directory)/'review.json'
            preview = {'sha256': 'a'*64}
            self.assertFalse(menu.approval_matches(path, preview))
            path.write_text(json.dumps({'sha256': 'b'*64, 'image_visually_confirmed': True}))
            with self.assertRaises(ValueError): menu.approval_matches(path, preview)
            path.write_text(json.dumps({'sha256': 'a'*64, 'image_visually_confirmed': True}))
            self.assertTrue(menu.approval_matches(path, preview))


if __name__ == '__main__': unittest.main()
