"""Two actual native keyboard transitions and rejection of altered evidence."""
import copy,gzip,json,unittest
from tools import school_native_dialogue_handoff_verification as proof


class TransitionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.reports=[json.loads(gzip.decompress((proof.ROOT/('analysis/school-native-dialogue-held-'+name+'-20261022.json.gz')).read_bytes())) for name in ('76-v4','77-v2')]
 def test_two_independent_original_runs(self):
  pids=set()
  for report,pc in zip(self.reports,(1164,152)):
   checked=proof.verify(report,require_transition=True);self.assertTrue(checked['system_input_transition_verified']);self.assertFalse(checked['R3_complete']);pids.add(report['case']['lifecycle']['ready']['pid']);self.assertEqual(report['case']['probe']['dialogue_boundary']['wait_PC'],pc)
  self.assertEqual(len(pids),2)
 def reject(self,edit):
  r=copy.deepcopy(self.reports[0]);edit(r['case']['probe']);
  with self.assertRaises((ValueError,KeyError)):proof.verify(r,require_transition=True)
 def receipt(self,**changes):self.reject(lambda p:p['input_handoff']['action_receipt'].update(changes))
 def test_missing_receipt(self):self.reject(lambda p:p['input_handoff'].pop('action_receipt'))
 def test_failed_input(self):self.receipt(input_returned=False)
 def test_unreleased_key(self):self.receipt(released=False)
 def test_wrong_scan(self):self.receipt(scan_code=32)
 def test_wrong_hold(self):self.receipt(hold_ms=1)
 def test_failed_keyup(self):self.receipt(up_results=[0])
 def test_foreign_receipt_window(self):self.receipt(hwnd=1)
 def test_foreign_receipt_process(self):self.receipt(pid=1)
 def test_foreign_image(self):self.receipt(process_image='C:/foreign.exe')
 def test_memory_write_claim(self):self.receipt(existing_process_memory_written=True)
 def test_fake_duration(self):
  self.reject(lambda p:p['input_handoff']['action_receipt'].update(up_ns=p['input_handoff']['action_receipt']['down_ns']+1))
 def test_action_outside_observation(self):self.receipt(start_wall_time_ns=1)
 def test_foreground_loss_at_release(self):
  self.reject(lambda p:p['input_handoff']['samples'][p['input_handoff']['release_index']].update(foreground_hwnd=1))
 def test_fake_cached_PC_crossing(self):self.reject(lambda p:p['input_handoff'].update(advanced_index=0))
 def test_missing_actual_keyboard_press(self):
  def edit(p):
   for row in p['input_handoff']['samples']:
    body=bytearray.fromhex(row['input']['hex']);body[0x4b9]=0;row['input']['hex']=body.hex()
  self.reject(edit)
 def test_post_input_PC_still_waiting(self):
  def edit(p):
   vm=bytearray.fromhex(p['samples'][-1]['VM_hex']);vm[28:32]=p['dialogue_boundary']['wait_PC'].to_bytes(4,'little');p['samples'][-1]['VM_hex']=vm.hex()
  self.reject(edit)
 def test_foreign_activation(self):self.reject(lambda p:p['owned_window_activation'].update(after=1))
 def test_unsupported_activation_method(self):self.reject(lambda p:p['owned_window_activation'].update(operations=[{'name':'foreign input attachment'}]))
 def test_keyboard_backend_must_be_explicit(self):self.reject(lambda p:p['input_handoff'].update(backend='computer-use JS API'))


if __name__=='__main__':unittest.main()
