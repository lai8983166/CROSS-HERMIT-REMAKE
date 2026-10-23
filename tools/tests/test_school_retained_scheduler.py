"""Whole retained registration/dispatch and adversarial source/owner checks."""
import copy,gzip,json,os,unittest
import struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unittest.mock import patch
from tools import school_retained_scheduler_verification as v
from tools.tests.test_school_retained_fog import isolated as parent_isolated

def isolated(seed):
 r=parent_isolated(seed)
 for key in ('scheduler_events','scheduler_closed_events'):
  if hasattr(seed,key):setattr(r,key,copy.deepcopy(getattr(seed,key)))
 return r

class CrtOrderTests(unittest.TestCase):
 """Recorded-source API-only preflight; the complete source is verified separately."""
 @classmethod
 def setUpClass(cls):cls.c=json.loads(gzip.decompress((v.ROOT/'analysis/school-retained-scheduler-single-v1-20261024.json.gz').read_bytes()))
 def seed(self):
  c=self.c;r=v.Replay.__new__(v.Replay);r.u=Uc(UC_ARCH_X86,UC_MODE_32);image=v.base.SOURCE.read_bytes();r.u.mem_map(v.base.BASE,(len(image)+4095)&~4095);r.u.mem_write(v.base.BASE,image);r.u.mem_map(v.work.STACK-0xf000,65536);r.history=copy.deepcopy(c['allocation_history'][:4]);r.blocks={};r.depth=1;r.case=dict(c,native_hello=dict(heap=c['source_heap_created'],critical=0))
  for i,b in enumerate(r.history):
   b['freed']=i in (0,2)
   if not b['freed']:r.blocks[b['guest']]=b
  a=copy.deepcopy(next(x for x in c['scheduler']['steps'][-1]['result']['api_calls'] if x['name']=='HeapAlloc'));r.wire=a['wire_start'];self.frame(r,a);return r,a
 def frame(self,r,a):
  r.u.mem_write(a['sp'],struct.pack('<'+'I'*(1+len(a['args'])),a['return_va'],*a['args']));r.u.reg_write(v.base.REGISTERS['ESP'],a['sp']);r.u.reg_write(v.base.REGISTERS['EIP'],a['target']);a['va']=a['target']
 def test_exact_fifth_thread_allocation_and_third_debug_free(self):
  r,a=self.seed();r.api(a);self.assertEqual(len(r.history),5);p=self.c['scheduler']['new_allocations'][0];self.assertEqual(r.history[-1]['guest'],p);self.assertEqual(r.blocks[p]['bytes'],160);a=copy.deepcopy(next(x for x in self.c['scheduler']['cleanup'][0]['result']['api_calls'] if x['name']=='HeapFree'));q=self.c['native_trace'][a['wire_start']]['request'];self.assertEqual(q['op'],'sync');r.u.mem_write(p,bytes.fromhex(q['hex']));r.wire=a['wire_start'];self.frame(r,a);r.api(a);self.assertNotIn(p,r.blocks);self.assertTrue(r.history[-1]['freed']);self.assertEqual(r.wire,a['wire_end'])
 def test_wrong_thread_raw_allocation_size_refuses(self):
  r,a=self.seed();a['args'][2]=176;self.frame(r,a)
  with self.assertRaises(ValueError):r.api(a)
 def test_thread_free_poisoned_bytes_must_match_actual_receipt(self):
  r,a=self.seed();r.api(a);p=self.c['scheduler']['new_allocations'][0];a=copy.deepcopy(next(x for x in self.c['scheduler']['cleanup'][0]['result']['api_calls'] if x['name']=='HeapFree'));raw=bytearray.fromhex(self.c['native_trace'][a['wire_start']]['request']['hex']);raw[32]^=1;r.u.mem_write(p,bytes(raw));r.wire=a['wire_start'];self.frame(r,a)
  with self.assertRaises(ValueError):r.api(a)

class SchedulerTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path='analysis/school-retained-scheduler-single-v1-20261024.json.gz';raw=(v.ROOT/cls.path).read_bytes();cls.c=json.loads(gzip.decompress(raw));cls.e=cls.c['scheduler'];cls.seeds={};cls.api_seeds={};old=v.Replay.loop_step;old_api=v.Replay.api
  def step(r,s):
   if s['label'] in [x['label'] for x in cls.e['steps']+cls.e['cleanup']]:cls.seeds[s['label']]=isolated(r)
   return old(r,s)
  def api(r,a):
   if a.get('kind')=='actual_scheduler_platform':cls.api_seeds[(a['name'],a['return_va'])]=(isolated(r),copy.deepcopy(a))
   return old_api(r,a)
  with patch.object(v.Replay,'loop_step',step),patch.object(v.Replay,'api',api):cls.proof=v.verify_case(cls.c)
  # Tests are repeatable by default; only an explicit fresh destination persists a proof.
  destination=os.environ.get('SCHOOL_RETAINED_SCHEDULER_PROOF_OUT')
  if destination:
   out=v.ROOT/destination;assert not out.exists();out.write_text(json.dumps(dict(schema_version=1,source_case=dict(name=cls.c['name'],scene_capture=cls.c['scene_capture'],path=cls.path,bytes=len(raw),sha256=v.sha(raw)),verification_source_sha256=v.sha((v.ROOT/'tools/school_retained_scheduler_verification.py').read_bytes()),proof=cls.proof),indent=2)+chr(10),encoding='utf8',newline=chr(10))
 def reject(self,edit):
  c=dict(self.c,scheduler=copy.deepcopy(self.e));edit(c['scheduler'])
  with self.assertRaises((ValueError,RuntimeError,KeyError,IndexError)):v.protocol(c)
 def step_reject(self,label,edit):
  r=isolated(self.seeds[label]);s=copy.deepcopy(next(x for x in self.e['steps']+self.e['cleanup'] if x['label']==label));edit(s)
  with self.assertRaises((ValueError,RuntimeError,KeyError,IndexError)):r.loop_step(s)
 def api_reject(self,key,edit):
  r,a=self.api_seeds[key];r=isolated(r);a=copy.deepcopy(a);edit(r,a)
  with self.assertRaises((ValueError,RuntimeError,KeyError,IndexError)):r.api(a)
 def test_whole_source_registration_and_real_thread_boundary(self):
  p=self.proof['scheduler'];self.assertEqual((p['original_instructions'],p['original_writes']),(3304,956));self.assertTrue(p['original_registration_verified'] and p['first_scan_started'] and p['ordinary_loop_context_preserved'] and p['normal_source_cleanup']);self.assertFalse(p['first_scan_returned'] or p['cooperative_yield_executed'] or p['original_CRT_worker_created'] or p['original_MAIN_scheduler_connected']);self.assertEqual(p['current_native_event_count'],2);self.assertEqual(p['new_CRT_allocations'],1);self.assertEqual(p['thread_creation']['CRT_wrapper'],0x56e110);self.assertEqual(p['independent_fresh_platform']['exit_code'],0)
 def test_wrong_parent_pin_refuses(self):self.reject(lambda e:e['contract'].update(parent_acceptance_sha256='0'*64))
 def test_wrong_native_source_refuses(self):self.reject(lambda e:e['native_build'].update(source_sha256='0'*64))
 def test_fallback_cleanup_refuses(self):self.reject(lambda e:e['native_cleanup'].update(forced_cleanup=True))
 def test_counterfeit_native_thread_refuses(self):self.reject(lambda e:e['native_cleanup'].update(thread_created=True))
 def test_wrong_declared_manager_refuses(self):self.reject(lambda e:e['declaration'][0].update(pointer=v.work.TACT))
 def test_reused_original_stack_refuses(self):self.reject(lambda e:e['declaration'][1].update(pointer=v.work.previous.STACK-0xf000))
 def test_truncated_original_stack_refuses(self):self.reject(lambda e:e.update(retained_stack_hex=e['retained_stack_hex'][:-2]))
 def test_wrong_manager_root_refuses(self):self.reject(lambda e:e['steps'][0]['root'].update(va=0x421660))
 def test_wrong_registration_task_refuses(self):self.reject(lambda e:e['steps'][2]['root']['args'].__setitem__(0,0))
 def test_wrong_registration_bucket_refuses(self):self.reject(lambda e:e['steps'][2]['root']['args'].__setitem__(1,31))
 def test_wrong_registration_parameter_refuses(self):self.reject(lambda e:e['steps'][2]['root']['args'].__setitem__(2,1))
 def test_extra_business_root_refuses(self):self.reject(lambda e:e['steps'].append(copy.deepcopy(e['steps'][-1])))
 def test_early_thread_boundary_refuses(self):self.reject(lambda e:e['frontier'].update(import_slot=0x59226c))
 def test_fake_wait_success_refuses(self):self.reject(lambda e:e['frontier'].update(name='WaitForSingleObject'))
 def test_wrong_caller_frame_refuses(self):self.reject(lambda e:e['frontier'].update(return_va=0x421ed8))
 def test_wrong_registration_instruction_hash_refuses(self):self.step_reject('original_retained_task_registration',lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_wrong_manager_memory_refuses(self):self.step_reject('original_manager_constructor',lambda s:s['full_memory'][0].update(sha256='0'*64))
 def test_wrong_architectural_CPU_refuses(self):self.step_reject('original_manager_empty_lists',lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_wrong_original_queue_refuses(self):self.step_reject('original_manager_empty_lists',lambda s:s['queue'].update(used_bytes=123))
 def test_wrong_thread_allocation_write_refuses(self):self.step_reject('original_first_scheduler_scan',lambda s:s['result'].update(write_sha256='0'*64))
 def test_wrong_original_event_arguments_refuses(self):self.api_reject(('CreateEventA',0x42194d),lambda r,a:a['args'].__setitem__(1,1))
 def test_wrong_original_event_caller_refuses(self):self.api_reject(('CreateEventA',0x421585),lambda r,a:a.update(return_va=0x42194d))
 def test_wrong_event_token_refuses(self):self.api_reject(('CreateEventA',0x42194d),lambda r,a:a.update(value=a['value']+16))
 def test_wrong_native_event_cursor_refuses(self):self.api_reject(('CreateEventA',0x42194d),lambda r,a:a.update(native_wire_index=0))
 def test_wrong_native_event_receipt_refuses(self):self.api_reject(('CreateEventA',0x42194d),lambda r,a:a['native_result'].update(handle=0))
 def test_wrong_native_critical_output_refuses(self):self.api_reject(('InitializeCriticalSection',0x42156e),lambda r,a:a['memory_outputs'][0].update(hex='00'*24))
 def test_foreign_manager_critical_refuses(self):self.api_reject(('DeleteCriticalSection',0x421626),lambda r,a:a['args'].__setitem__(0,0x80a4b0))
 def test_wrong_event_close_owner_refuses(self):self.api_reject(('CloseHandle',0x42163f),lambda r,a:a['args'].__setitem__(0,0))
 def test_wrong_unlink_write_refuses(self):self.step_reject('supplemental_original_task_unlink',lambda s:s['result'].update(write_sha256='0'*64))

class PlatformTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.helper,cls.build=v.work.platform.build(v.ROOT/('.venv-audit/scheduler-platform-tests-'+str(os.getpid())+'.exe'))
 def run_owner(self,fn):
  live=v.work.platform.Live(self.helper)
  try:fn(live);self.assertEqual(live.close()['forced_cleanup'],False);self.assertEqual(live.exit_code,0)
  finally:
   if not live.closed:live._terminate()
 def test_actual_auto_reset_event(self):
  def check(l):
   h=l.request('create_event')['handle'];self.assertEqual(l.request('wait',handle=h,milliseconds=0),dict(value=258));l.request('set',handle=h);self.assertEqual(l.request('wait',handle=h,milliseconds=0),dict(value=0));self.assertEqual(l.request('wait',handle=h,milliseconds=0),dict(value=258));l.request('set',handle=h);l.request('reset',handle=h);self.assertEqual(l.request('wait',handle=h,milliseconds=0),dict(value=258));l.request('close_event',handle=h)
  self.run_owner(check)
 def test_foreign_event_refuses(self):
  def check(l):
   with self.assertRaises(ValueError):l.request('set',handle=0x65010000)
  self.run_owner(check)
 def test_closed_event_refuses(self):
  def check(l):
   h=l.request('create_event')['handle'];l.request('close_event',handle=h)
   with self.assertRaises(ValueError):l.request('reset',handle=h)
  self.run_owner(check)
 def test_foreign_critical_refuses(self):
  def check(l):
   with self.assertRaises(ValueError):l.request('initialize',guest=0x80a4b0)
  self.run_owner(check)
 def test_uninitialized_critical_refuses(self):
  def check(l):
   with self.assertRaises(ValueError):l.request('enter',guest=v.work.MANAGER+256)
  self.run_owner(check)
 def test_actual_recursive_critical(self):
  def check(l):
   p=v.work.MANAGER+256;l.request('initialize',guest=p);self.assertEqual(l.request('enter',guest=p)['depth'],1);self.assertEqual(l.request('enter',guest=p)['depth'],2)
   with self.assertRaises(ValueError):l.request('delete',guest=p)
   self.assertEqual(l.request('leave',guest=p)['depth'],1);self.assertEqual(l.request('leave',guest=p)['depth'],0);l.request('delete',guest=p)
  self.run_owner(check)
 def test_game_thread_substitute_refuses(self):
  def check(l):
   with self.assertRaises(ValueError):l.request('create_thread',entry=0x56e110)
  self.run_owner(check)
