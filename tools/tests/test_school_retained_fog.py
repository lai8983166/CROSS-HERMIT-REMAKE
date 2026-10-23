"""Full original fog creation/upload/wait and adversarial current-ownership checks."""
import copy,gzip,json,unittest
from unittest.mock import patch
from tools import school_retained_fog_verification as v
from tools.tests.test_school_retained_opening import isolated as parent_isolated

def isolated(seed):
 r=parent_isolated(seed)
 for k in ('fog_space','fog_texture','fog_lock'):
  if hasattr(seed,k):setattr(r,k,copy.deepcopy(getattr(seed,k)))
 return r

class FogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path='analysis/school-retained-fog-single-v1-20261023.json.gz'
  with gzip.open(v.ROOT/cls.path,'rt',encoding='utf8') as f:cls.c=json.load(f)
  cls.e=cls.c['fog_texture'];cls.seeds={};cls.api_seeds={};old=v.Replay.loop_step;old_api=v.Replay.api
  def observe(r,s):
   if s['label'] in ('original_fog_device_query','original_fog_texture_creation','supplemental_original_fog_texture_destructor'):cls.seeds[s['label']]=isolated(r)
   return old(r,s)
  def observe_api(r,a):
   if a.get('kind')=='actual_fog_GPU':cls.api_seeds[a['phase']]=(isolated(r),copy.deepcopy(a))
   return old_api(r,a)
  with patch.object(v.Replay,'loop_step',observe),patch.object(v.Replay,'api',observe_api):cls.proof=v.verify_case(cls.c)
  raw=(v.ROOT/cls.path).read_bytes();out=v.ROOT/'analysis/school-retained-fog-single-proof-v1-20261023.json';assert not out.exists();out.write_text(json.dumps(dict(schema_version=1,source_case=dict(name=cls.c['name'],scene_capture=cls.c['scene_capture'],path=cls.path,bytes=len(raw),sha256=v.sha(raw)),verification_source_sha256=v.sha((v.ROOT/'tools/school_retained_fog_verification.py').read_bytes()),proof=cls.proof),indent=2)+chr(10),encoding='utf8',newline=chr(10))
 def reject(self,edit):
  c=dict(self.c,fog_texture=copy.deepcopy(self.e));edit(c['fog_texture'])
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def step(self,label):return next(s for s in self.e['creation']+[self.e['cleanup']] if s['label']==label)
 def step_reject(self,label,edit):
  r=isolated(self.seeds[label]);s=copy.deepcopy(self.step(label));edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.loop_step(s)
 def api_reject(self,phase,edit):
  seed,a=self.api_seeds[phase];r=isolated(seed);a=copy.deepcopy(a);edit(r,a)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.api(a)
 def test_full_fog_source_and_natural_pre_wait(self):
  p=self.proof['fog_texture'];w=self.proof['world_loop'];self.assertEqual((p['new_resource_instructions'],p['new_resource_writes']),(501,185));self.assertTrue(w['natural_world_return'] and w['natural_pre_yield_boundary']);self.assertIsNone(w['exact_dependency']);self.assertFalse(w['cooperative_yield_executed']);self.assertEqual((w['new_original_instructions'],w['new_original_writes']),(2941432,1308706));self.assertEqual(w['actual_lock13_operations'],0);self.assertEqual(p['source_size'],[172,128]);self.assertEqual(p['native_size'],[256,128]);self.assertEqual(p['native_bytes'],65536);self.assertEqual(p['source_original_destructor_instructions'],149);self.assertTrue(p['all_rows_and_unchanged_padding_verified'] and p['normal_source_cleanup']);self.assertEqual(p['independent_fresh_GPU']['exit_code'],0)
 def test_wrong_parent_pin_refuses(self):self.reject(lambda e:e['contract'].update(parent_acceptance_sha256='0'*64))
 def test_wrong_resource_source_refuses(self):self.reject(lambda e:e['contract'].update(original_resource_call_hex='00'))
 def test_extra_resource_root_refuses(self):self.reject(lambda e:e['creation'].append(copy.deepcopy(e['creation'][0])))
 def test_wrong_query_receiver_refuses(self):self.reject(lambda e:e['creation'][0]['root'].update(receiver=0))
 def test_wrong_creation_receiver_refuses(self):self.reject(lambda e:e['creation'][1]['root'].update(receiver=v.work.FOG+4))
 def test_wrong_creation_arguments_refuses(self):self.reject(lambda e:e['creation'][1]['root'].update(args=[0,0]))
 def test_wrong_creation_return_refuses(self):self.reject(lambda e:e['creation'][1]['root'].update(return_va=0x440563))
 def test_wrong_source_dimensions_refuses(self):self.reject(lambda e:e['entry'].update(source_width=256))
 def test_wrong_initial_texture_refuses(self):self.reject(lambda e:e['entry'].update(texture=1))
 def test_wrong_GPU_source_refuses(self):self.reject(lambda e:e['GPU_build'].update(source_sha256='0'*64))
 def test_fallback_native_release_refuses(self):self.reject(lambda e:e['GPU'].update(texture_releases=[1]))
 def test_missing_native_readback_refuses(self):self.reject(lambda e:e['GPU_trace'].pop(4))
 def test_wrong_destructor_refuses(self):self.reject(lambda e:e['cleanup']['root'].update(va=0x403620))
 def test_wrong_creation_CPU_refuses(self):self.step_reject('original_fog_texture_creation',lambda s:s['result']['before_cpu'].update(EAX=0xbad))
 def test_wrong_creation_instruction_hash_refuses(self):self.step_reject('original_fog_texture_creation',lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_wrong_query_memory_refuses(self):self.step_reject('original_fog_device_query',lambda s:s['full_memory'][0].update(sha256='0'*64))
 def test_wrong_query_architectural_CPU_refuses(self):self.step_reject('original_fog_device_query',lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_wrong_query_queue_refuses(self):self.step_reject('original_fog_device_query',lambda s:s['queue'].update(used_bytes=0xbad))
 def test_wrong_source_row_copy_refuses(self):self.api_reject(3,lambda r,a:a.update(source_hex='00'*44032))
 def test_wrong_uploaded_pixel_refuses(self):self.api_reject(3,lambda r,a:a.update(uploaded_hex='00'*65536))
 def test_wrong_locked_padding_refuses(self):
  def edit(r,a):
   p=r.fog_lock['bits']+344;r.u.mem_write(p,bytes([r.read(p,1)[0]^1]))
  self.api_reject(3,edit)
 def test_wrong_native_current_pointer_refuses(self):self.api_reject(2,lambda r,a:a['native_request'].update(pointer=r.fog_pointer+4))
 def test_wrong_original_lock_caller_refuses(self):self.api_reject(2,lambda r,a:a.update(return_va=0x40395f))
 def test_wrong_original_lock_flags_refuses(self):self.api_reject(2,lambda r,a:a['args'].__setitem__(4,0))
 def test_wrong_creation_device_refuses(self):self.api_reject(0,lambda r,a:a['args'].__setitem__(0,0))
 def test_wrong_descriptor_output_refuses(self):self.api_reject(1,lambda r,a:a['memory_outputs'][0].update(hex='00'*32))
 def test_wrong_source_native_cursor_refuses(self):self.api_reject(3,lambda r,a:a.update(native_wire_index=a['native_wire_index']+1))
 def test_cross_owner_texture_refuses(self):self.api_reject(4,lambda r,a:a['args'].__setitem__(0,r.role_objects[0]['texture']['pointer']))
 def test_wrong_release_result_refuses(self):self.api_reject(5,lambda r,a:a['result'].update(count=1))
 def test_wrong_original_destructor_write_refuses(self):self.step_reject('supplemental_original_fog_texture_destructor',lambda s:s['result'].update(write_sha256='0'*64))
 def test_real_original_destructor(self):
  label='supplemental_original_fog_texture_destructor';r=isolated(self.seeds[label]);self.assertEqual(r.loop_step(self.step(label)),149);self.assertEqual(v.word(r.read(v.work.FOG+44)),0)
