"""Pure symbolic blob/identity checks. No helper or desktop APIs are invoked."""
import struct
import unittest
from devtools.terminal_display_model import model_blob,DEVICE
from devtools.terminal_display_platform import decode_snapshot,wide
from devtools import terminal_display_native as native

class DisplayTests(unittest.TestCase):
    def test_three_actual_phase_shapes(self):
        for phase in range(3):
            d=decode_snapshot(model_blob(phase,123,456 if phase==1 else 0,789))
            self.assertEqual(d['target_device'],DEVICE)
            self.assertEqual(d['display_identity']['adapter']['name'],DEVICE)
            self.assertEqual(len(bytes.fromhex(d['gamma_hex'])),1536)
    def test_truncation_and_failed_api(self):
        good=model_blob(0,123,0,789)
        for field in (3,5,6,7,8,9,10,11,14,15):
            bad=bytearray(good);struct.pack_into('<I',bad,field*4,0)
            with self.assertRaises(ValueError):decode_snapshot(bad)
        with self.assertRaises(ValueError):decode_snapshot(good[:-1])
    def test_wrong_phase_and_device(self):
        with self.assertRaises(ValueError):decode_snapshot(model_blob(0,123,456,789))
        with self.assertRaises(ValueError):decode_snapshot(model_blob(1,123,0,789))
    def test_identity_termination_and_private_mode(self):
        with self.assertRaises(ValueError):wide(b'A\0'*32)
        raw=bytearray(model_blob(0,123,0,789));struct.pack_into('<H',raw,14448+70,2)
        with self.assertRaises(ValueError):decode_snapshot(raw)
    def test_unused_slots_rejected(self):
        raw=bytearray(model_blob(0,123,0,789));raw[1848]=1
        with self.assertRaises(ValueError):decode_snapshot(raw)
    def test_source_is_closed_and_parent_unchanged(self):
        report=native.self_check();self.assertFalse(report['native_executed']);self.assertFalse(report['native_admission'])
        source=native.source()
        self.assertIn('D3D_DEVICE_REQUIRES_CURRENT_DISPLAY_BINDING',source)
        self.assertIn('SHUTDOWN_DISPLAY_OBLIGATION',source)

if __name__=='__main__':unittest.main()
