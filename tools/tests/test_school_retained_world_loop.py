"""Independent original loop/world/fault and ownership tamper rejection."""
import copy,gzip,json,unittest
from unittest.mock import patch
from tools import school_retained_world_loop_verification as v
from tools.tests.test_school_retained_opening import isolated

class WorldLoopTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path='analysis/school-retained-world-loop-single-v4-20261023.json.gz'
  with gzip.open(v.ROOT/cls.path,'rt',encoding='utf8') as f:cls.c=json.load(f)
  cls.e=cls.c['world_loop'];cls.seeds={};cls.api_seeds={};step=v.Replay.loop_step;api=v.Replay.api
  def observe(r,s):
   if s['label'] in ('loop_request_or_queue_0x425de0','continuous_original_world_return','supplemental_original_lock13_release_after_fault'):cls.seeds[s['label']]=isolated(r)
   return step(r,s)
  def observe_api(r,a):
   if a.get('kind')=='actual_world_static_lock':cls.api_seeds[a['name']]=(isolated(r),copy.deepcopy(a))
   return api(r,a)
  with patch.object(v.Replay,'loop_step',observe),patch.object(v.Replay,'api',observe_api):cls.proof=v.verify_case(cls.c)
  raw=(v.ROOT/cls.path).read_bytes();out=v.ROOT/'analysis/school-retained-world-loop-single-proof-v1-20261023.json';assert not out.exists();out.write_text(json.dumps(dict(schema_version=1,source_case=dict(name=cls.c['name'],scene_capture=cls.c['scene_capture'],path=cls.path,bytes=len(raw),sha256=v.sha(raw)),verification_source_sha256=v.sha((v.ROOT/'tools/school_retained_world_loop_verification.py').read_bytes()),proof=cls.proof),indent=2)+chr(10),encoding='utf8',newline=chr(10))
 def reject(self,edit):
  c=dict(self.c,world_loop=copy.deepcopy(self.e));edit(c['world_loop'])
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def step(self,label):return next(s for s in self.e['steps']+self.e['supplemental_lock_cleanup'] if s['label']==label)
 def step_reject(self,label,edit):
  r=isolated(self.seeds[label]);s=copy.deepcopy(self.step(label));edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.loop_step(s)
 def api_reject(self,edit,leave=False):
  seed,a=self.api_seeds['LeaveCriticalSection' if leave else 'EnterCriticalSection'];r=isolated(seed);a=copy.deepcopy(a);edit(r,a)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.api(a)
 def test_full_source_world_and_exact_fault(self):
  p=self.proof['world_loop'];self.assertEqual(p['new_original_instructions'],2920860);self.assertEqual(p['new_original_writes'],1295376);self.assertTrue(p['natural_world_return']);self.assertEqual(p['world_unit_entries'],38);self.assertEqual(p['world_enabled_at_entry'],1);self.assertFalse(p['natural_pre_yield_boundary']);self.assertFalse(p['balanced_lock13']);self.assertTrue(p['normal_source_lock13_cleanup']);self.assertEqual(p['supplemental_original_lock_release_instructions'],[8]);self.assertEqual(p['exact_dependency']['address'],0x4d686d8);self.assertEqual(p['exact_dependency']['cpu']['EIP'],0x56e3c5)
 def test_wrong_acceptance_refuses(self):self.reject(lambda e:e['contract'].update(parent_acceptance_sha256='0'*64))
 def test_wrong_platform_identity_refuses(self):self.reject(lambda e:e['contract'].update(platform_source_sha256='0'*64))
 def test_extra_world_root_refuses(self):self.reject(lambda e:e.update(new_VM_or_world_roots=1))
 def test_extra_loop_root_refuses(self):self.reject(lambda e:e.update(new_declared_loop_roots=2))
 def test_control_write_claim_refuses(self):self.reject(lambda e:e.update(host_game_control_writes=1))
 def test_input_claim_refuses(self):self.reject(lambda e:e.update(new_OS_input=True))
 def test_scheduler_claim_refuses(self):self.reject(lambda e:e.update(original_outer_scheduler=True))
 def test_wait_execution_claim_refuses(self):self.reject(lambda e:e.update(cooperative_yield_executed=True))
 def test_missing_segment_refuses(self):self.reject(lambda e:e['steps'].pop(1))
 def test_wrong_root_receiver_refuses(self):self.reject(lambda e:e['steps'][3]['root'].update(receiver=v.work.CONTROL))
 def test_wrong_root_stack_refuses(self):self.reject(lambda e:e['steps'][3]['root'].update(sp=v.work.STACK-4))
 def test_wrong_root_return_refuses(self):self.reject(lambda e:e['steps'][3]['root'].update(return_va=0x4539f1))
 def test_direct_world_root_refuses(self):self.reject(lambda e:e['steps'][4].update(root=copy.deepcopy(e['steps'][3]['root'])))
 def test_wrong_natural_world_target_refuses(self):self.reject(lambda e:e['steps'][3].update(requested_boundary=0x46b471))
 def test_wrong_frontier_refuses(self):self.reject(lambda e:e['frontier'].update(address=0))
 def test_missing_memory_refuses(self):self.reject(lambda e:e['steps'][0].pop('full_memory'))
 def test_wrong_before_cpu_refuses(self):self.step_reject('loop_request_or_queue_0x425de0',lambda s:s['result']['before_cpu'].update(EAX=0xbad))
 def test_wrong_instruction_hash_refuses(self):self.step_reject('loop_request_or_queue_0x425de0',lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_wrong_write_hash_refuses(self):self.step_reject('loop_request_or_queue_0x425de0',lambda s:s['result'].update(write_sha256='0'*64))
 def test_wrong_memory_refuses(self):self.step_reject('loop_request_or_queue_0x425de0',lambda s:s['full_memory'][0].update(sha256='0'*64))
 def test_wrong_architectural_cpu_refuses(self):self.step_reject('loop_request_or_queue_0x425de0',lambda s:s['architectural_cpu'].update(EAX=0xbad))
 def test_wrong_queue_refuses(self):self.step_reject('loop_request_or_queue_0x425de0',lambda s:s['queue'].update(used_bytes=0xbad))
 def test_wrong_scene_state_refuses(self):self.step_reject('loop_request_or_queue_0x425de0',lambda s:s['loop_state'].update(world_enabled=0))
 def test_wrong_world_caller_frame_refuses(self):self.step_reject('continuous_original_world_return',lambda s:s['calls'][0]['frames'][0].update(return_va=0xbad))
 def test_false_world_early_return_refuses(self):self.step_reject('continuous_original_world_return',lambda s:s['result'].update(boundary=0x46b4a5))
 def test_foreign_static_lock_pointer_refuses(self):self.api_reject(lambda r,a:a.update(args=[0x80a4b0]))
 def test_wrong_static_lock_caller_refuses(self):self.api_reject(lambda r,a:a.update(return_va=0x5770d4))
 def test_wrong_static_lock_index_refuses(self):self.api_reject(lambda r,a:a.update(lock_index=9))
 def test_wrong_static_lock_depth_refuses(self):self.api_reject(lambda r,a:a.update(depth=0))
 def test_missing_static_lock_ownership_refuses(self):self.api_reject(lambda r,a:r.criticals.pop(0x80a4c8))
 def test_wrong_static_lock_native_cursor_refuses(self):self.api_reject(lambda r,a:a.update(wire_start=a['wire_start']+1))
 def test_wrong_static_lock_output_refuses(self):self.api_reject(lambda r,a:a['memory_outputs'][0].update(hex='00'*24))
 def test_wrong_static_lock_native_pointer_refuses(self):self.api_reject(lambda r,a:r.criticals.update({0x80a4c8:r.criticals[0x80a4c8]+4}))
 def test_wrong_static_unlock_depth_refuses(self):self.api_reject(lambda r,a:a.update(depth=1),leave=True)
 def test_original_unlock_full_replay(self):
  label='supplemental_original_lock13_release_after_fault';r=isolated(self.seeds[label]);self.assertEqual(r.loop_step(self.step(label)),8);self.assertEqual(r.world_lock_depth,0)
 def test_wrong_original_unlock_write_refuses(self):self.step_reject('supplemental_original_lock13_release_after_fault',lambda s:s['result'].update(write_sha256='0'*64))
 def test_wrong_original_unlock_fault_refuses(self):self.step_reject('supplemental_original_lock13_release_after_fault',lambda s:s.update(fault=dict(address=0),unicorn_error='bad'))
