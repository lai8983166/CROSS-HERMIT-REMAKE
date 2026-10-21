"""Pinned captures and whole-object source keyboard processing without GUI use."""
import unittest
from tools import school_retained_keyboard as work
from tools.school_native_dialogue_verification import keyboard_update,predict_keyboard


class SourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.contract=work.inputs()
 def test_three_logical_cases_two_actual_capture_streams(self):
  self.assertEqual(set(self.contract['parents']),{'initial','student9_waiting','fifth_class'});self.assertEqual(set(self.contract['streams']),{76,77})
 def test_native_full_device_waveform(self):
  for stream in self.contract['streams'].values():
   self.assertEqual([c['label'] for c in stream['captures']],['idle','press','release'])
   self.assertEqual([bytes.fromhex(c['raw_device_hex'])[57] for c in stream['captures']],[0,128,0])
 def test_full_original_keyboard_matches_independent_model(self):
  for stream in self.contract['streams'].values():
   state=bytes(0xa00)
   for capture in stream['captures']:
    before=bytearray(state);before[12:268]=bytes.fromhex(capture['raw_device_hex']);state=keyboard_update(bytes(before));self.assertEqual(state,predict_keyboard(bytes(before)))
   self.assertEqual((state[0x4b9],state[0x7b9]),(0,128))
 def test_wrong_parent_digest_refused(self):
  row=self.contract['parents']['initial']
  with self.assertRaisesRegex(ValueError,'pinned evidence'):work.pinned(row['path'],'0'*64)
 def test_incomplete_capture_refused_before_any_guest_access(self):
  guest=work.Guest.__new__(work.Guest)
  with self.assertRaisesRegex(ValueError,'full device extent'):guest.capture({'raw_device_hex':'00'})


if __name__=='__main__':unittest.main()
