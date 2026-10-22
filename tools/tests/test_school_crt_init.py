"""Native early-state provenance and original debug-graph corruption rejection."""
import copy,gzip,json,unittest
from tools import school_crt_init_verification as v

class InitializationCaptureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(gzip.decompress((v.ROOT/'analysis/school-crt-init-probe-v2-20261022.json.gz').read_bytes()))
 def reject(self,edit,full=False,index=5):
  c=copy.deepcopy(self.r['cases'][index]);edit(c)
  with self.assertRaises((ValueError,KeyError,IndexError)):(v.verify_case if full else v.protocol)(c)
 def test_00_all_eight_original_snapshots(self):
  r=v.verify(self.r);self.assertEqual((r['native_probes'],r['native_pre_WinMain_blocks']),(8,284));self.assertFalse(r['retained_integration'])
 def test_native_error(self):self.reject(lambda c:c.update(error='failed'))
 def test_fake_memory_write_scope(self):self.reject(lambda c:c.update(source_memory_written=True))
 def test_fake_parent_reply(self):self.reject(lambda c:c.update(debugger_reply_substituted=True))
 def test_probe_termination_as_game_shutdown(self):self.reject(lambda c:c['cleanup'].update(original_game_normal_shutdown=True))
 def test_remaining_child(self):self.reject(lambda c:c['cleanup'].update(members_after_cleanup=[1]))
 def test_unclosed_private_desktop(self):self.reject(lambda c:c['cleanup'].update(private_desktop_closed=False))
 def test_active_desktop_switch(self):self.reject(lambda c:c['desktop'].update(switched=True))
 def test_retained_restore_claim(self):self.reject(lambda c:c.update(retained_heap_restored=True))
 def test_general_register_request(self):
  def edit(c):
   a=c['debug_register_instrumentation'][0];b=bytearray.fromhex(a['requested_debug_context_hex']);b[184]^=1;a['requested_debug_context_hex']=b.hex()
  self.reject(edit)
 def test_non_debug_context_flag(self):
  def edit(c):
   a=c['debug_register_instrumentation'][0];b=bytearray.fromhex(a['requested_debug_context_hex']);b[0]=0x3f;a['requested_debug_context_hex']=b.hex()
  self.reject(edit)
 def test_changed_architectural_EFLAGS(self):
  def edit(c):
   a=c['debug_register_instrumentation'][0];b=bytearray.fromhex(a['after_context_hex']);b[192]^=0x40;a['after_context_hex']=b.hex()
  self.reject(edit)
 def test_reserved_flag_raw_difference_must_match(self):self.reject(lambda c:c['debug_register_instrumentation'][0].update(returned_EFLAGS_reserved_bit1_xor=3))
 def test_pending_source_entry_executed(self):self.reject(lambda c:c['captures'][0].update(first_instruction_executed=True),True)
 def test_original_text_digest(self):self.reject(lambda c:c['captures'][0]['source_text'].update(sha256='0'*64),True)
 def test_original_data_digest(self):self.reject(lambda c:c['captures'][0]['original_data'].update(sha256='0'*64),True)
 def test_derived_global_counter(self):self.reject(lambda c:c['captures'][0]['globals'].update(current_bytes=0),True)
 def test_missing_native_block(self):self.reject(lambda c:c['captures'][0]['debug_graph'].pop(),True)
 def test_native_debug_link_corruption(self):self.reject(lambda c:c['captures'][0]['debug_graph'][0].update(next=0),True)
 def test_native_request_sequence(self):self.reject(lambda c:c['captures'][0]['debug_graph'][0].update(request=0),True)
 def test_native_guard_corruption(self):
  def edit(c):
   a=c['captures'][0]['debug_graph'][0];b=bytearray.fromhex(a['raw_hex']);b[-1]=0;a['raw_hex']=b.hex()
  self.reject(edit,True)
 def test_fake_cold_inputs(self):self.reject(lambda c:c['captures'][0]['globals'].update(next_request=105),True,index=4)
 def test_wrong_parent_wait_exception(self):
  def edit(c):
   s=c['captures'][0];w=c['parent_waits'][s['parent_wait_index']];b=bytearray.fromhex(w['state_hex']);b[24]^=1;w['state_hex']=b.hex()
  self.reject(edit,True)

if __name__=='__main__':unittest.main()
