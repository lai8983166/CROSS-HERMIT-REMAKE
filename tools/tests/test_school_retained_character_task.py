"""Original character task continuity, queue bytes and incremental evidence gates."""
import copy,gzip,json,unittest
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from tools import school_retained_character_task_verification as v

def clone(seed):
 r=copy.copy(seed);r.u=Uc(UC_ARCH_X86,UC_MODE_32)
 for p,end,_ in seed.u.mem_regions():r.u.mem_map(p,end-p+1);r.u.mem_write(p,bytes(seed.u.mem_read(p,end-p+1)))
 r.u.context_restore(seed.u.context_save());r.region_hashes=dict(getattr(seed,'region_hashes',{}))
 if hasattr(seed,'task_code'):r.task_code=dict(seed.task_code)
 return r

class CharacterTaskTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path=v.ROOT/'analysis/school-retained-character-task-v3-20261022.json.gz';cls.r=json.loads(gzip.decompress(cls.path.read_bytes()));cls.c=cls.r['cases'][0];cls.seed,_=v.prepare(cls.c);cls.after=clone(cls.seed);cls.after.task_step(cls.c['frames'][0]['steps'][0])
 def reject(self,edit):
  c=copy.deepcopy(self.c);edit(c)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def task_reject(self,edit,reset=False):
  seed=self.after if reset else self.seed;r=clone(seed);s=copy.deepcopy(self.c['frames'][1 if reset else 0]['steps'][0]);edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.task_step(s)
 def test_00_complete_source_case_and_all_six_bound_proofs(self):
  proof=json.loads((v.ROOT/'analysis/school-retained-character-task-proof-v4-20261022.json').read_bytes());self.assertEqual(proof['source_report_sha256'],v.sha(self.path.read_bytes()));self.assertTrue(proof['six_original_character_tasks_and_animation_verified']);self.assertEqual(len(proof['cases']),6);self.assertTrue(all(c['complete_original_tasks']==79 and c['final_PC']==280 for c in proof['cases']));self.assertEqual(v.verify_case(self.c)['new_original_task_instructions'],2962747)
 def test_vm_root_substitution(self):self.reject(lambda c:c['frames'][1]['steps'][-1]['root'].update(va=0x4ce8f0))
 def test_first_continuation_new_root(self):self.reject(lambda c:c['frames'][0]['steps'][0].update(root=dict(va=0x4ce8f0)))
 def test_missing_animation_update(self):self.reject(lambda c:c['frames'].pop(30))
 def test_missing_queue_reset(self):self.reject(lambda c:c['frames'][1]['steps'].pop(1))
 def test_delay_early_release(self):self.reject(lambda c:c['frames'][29]['animation_state'].update(mode=3))
 def test_fade_early_release(self):self.reject(lambda c:c['frames'][75]['animation_state'].update(mode=2))
 def test_background_early_release(self):self.reject(lambda c:c['frames'][60]['animation_state'].update(background_mode=2))
 def test_wait_early_release(self):self.reject(lambda c:c['frames'][76]['animation_state'].update(wait=0))
 def test_wait_count_corruption(self):self.reject(lambda c:c['frames'][77]['animation_state'].update(waiting_count=0))
 def test_omitted_original_draw_queue_evidence(self):self.reject(lambda c:c['frames'][0]['steps'][0].pop('queue'))
 def test_host_game_accounting_reset(self):self.reject(lambda c:c['projection'].update(game_accounting_reset=True))
 def test_source_overlaid_outside_CRT(self):self.reject(lambda c:c['projection']['rows'][0].update(pointer=0x79fc74))
 def test_driver_precreated_heap(self):self.reject(lambda c:c['initial_native_hello'].update(heap=1))
 def test_forced_native_cleanup(self):self.reject(lambda c:c['helper_cleanup'].update(forced_cleanup=True))
 def test_unordered_native_trace(self):self.reject(lambda c:c['native_trace'][0]['request'].update(id=2))
 def test_third_font_arguments_corruption(self):self.reject(lambda c:c['pending_font']['args'].__setitem__(4,700))
 def test_third_font_frame_corruption(self):self.reject(lambda c:c['pending_font']['frames'][0].update(bp=1))
 def test_false_third_font_created(self):self.reject(lambda c:c['pending_font'].update(first_instruction_executed=True))
 def test_full_original_instruction_corruption(self):self.task_reject(lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_original_write_corruption(self):self.task_reject(lambda s:s['result'].update(write_sha256='0'*64))
 def test_full_CPU_corruption(self):self.task_reject(lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_readonly_mapping_digest_corruption(self):self.task_reject(lambda s:s['full_memory'][-1].update(sha256='0'*64))
 def test_original_display_call_omitted(self):self.task_reject(lambda s:s['display_calls'].pop())
 def test_queue_head_corruption(self):self.task_reject(lambda s:s['queue'].update(head_hex='00'))
 def test_queue_record_corruption(self):self.task_reject(lambda s:s['queue'].update(arena_hex='00'))
 def test_unowned_IME_context(self):self.task_reject(lambda s:s['result']['api_calls'][0]['args'].__setitem__(0,1),True)
 def test_changed_IME_caller(self):self.task_reject(lambda s:s['result']['api_calls'][0].update(return_va=1),True)
 def test_fake_IME_result(self):self.task_reject(lambda s:s['result']['api_calls'][0].update(value=1),True)
 def test_platform_write_into_game_memory(self):self.task_reject(lambda s:s['result']['api_calls'][0].update(memory_outputs=[dict(pointer=v.base.VM,hex='00')]),True)
 def test_scope_overclaims(self):
  for k in ('new_GPU','new_OS_input','historical_heap_restored','original_outer_scheduler','third_font_created','R3_complete','R6_complete'):
   r=dict(self.r);r[k]=True
   with self.assertRaises(ValueError):v.verify(r)
 def test_source_code_corruption_is_rejected(self):
  r=clone(self.seed);r.u.mem_write(0x4cc0d2,b'\x90')
  with self.assertRaises(ValueError):r.task_step(self.c['frames'][0]['steps'][0])

class MemoryEvidenceTests(unittest.TestCase):
 def setUp(self):self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.u.mem_map(0x10000,8192);self.e=v.work.MemoryEvidence(self.u);self.e.snapshot()
 def test_source_write_invalidates_mapping(self):self.u.mem_write(0x10001,b'ab');self.e.mark(0x10001,2);self.assertEqual(self.e.snapshot(),v.base.memory_rows(self.u))
 def test_cross_page_write_preserves_all_bytes(self):self.u.mem_write(0x10fff,b'ab');self.e.mark(0x10fff,2);self.assertEqual(self.e.snapshot(),v.base.memory_rows(self.u))
 def test_fresh_mapping_gets_digest(self):self.u.mem_map(0x20000,4096);self.e.refresh();self.assertEqual(self.e.snapshot(),v.base.memory_rows(self.u))
 def test_old_snapshot_is_immutable(self):
  before=self.e.snapshot();self.u.mem_write(0x10001,b'ab');self.e.mark(0x10001,2);self.assertNotEqual(before,self.e.snapshot())
 def test_untracked_write_cannot_pass_final_full_recheck(self):self.u.mem_write(0x10001,b'ab');self.assertNotEqual(self.e.snapshot(),v.base.memory_rows(self.u))

if __name__=='__main__':unittest.main()
