"""Reject source/state/ownership/timing changes in unsuspended observations."""
import copy,gzip,json,unittest
from tools import school_native_dialogue_handoff_verification as proof


class HandoffTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((proof.ROOT/'analysis/school-native-dialogue-76-v10-20261022.json.gz').read_bytes()))
 def test_OS_event_is_not_a_game_confirmation(self):
  r=proof.verify(self.report);self.assertEqual(len(r['OS_space_events']),1);self.assertEqual(r['keyboard_pressed_samples'],[]);self.assertFalse(r['system_input_transition_verified'])
 def test_unaccepted_input_transition(self):
  with self.assertRaises(ValueError):proof.verify(self.report,{},True)
 def reject(self,edit):
  r=copy.deepcopy(self.report);edit(r['case']['probe']['input_handoff'])
  with self.assertRaises(ValueError):proof.verify(r)
 def test_wrong_PID(self):self.reject(lambda h:h['window_after'].update(pid=1))
 def test_foreign_desktop(self):self.reject(lambda h:h['window_before'].update(window_desktop='Other'))
 def test_cloaked_window(self):self.reject(lambda h:h['window_before'].update(cloaked=2))
 def test_suspended_thread_overclaim(self):self.reject(lambda h:h.update(thread_suspension_used=True))
 def test_missing_input_bytes(self):self.reject(lambda h:h['samples'][0]['input'].update(hex='00'))
 def test_invalid_VM_base(self):self.reject(lambda h:h['samples'][0].update(VM_hex=bytes(128).hex()))
 def test_fake_pressed_boundary(self):self.reject(lambda h:h.update(press_index=1))
 def test_unordered_time(self):self.reject(lambda h:h['samples'][-1].update(wall_time_ns=1))
 def test_OS_event_from_foreign_foreground(self):
  def edit(h):
   for s in h['samples']:
    if s['os_space_state']:s['foreground_hwnd']=1
  self.reject(edit)


if __name__=='__main__':unittest.main()
