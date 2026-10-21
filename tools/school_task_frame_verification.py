"""Independent complete-task replay reusing the immutable R2 proof implementation."""
import gzip,json,struct,types
from tools import school_retained_render_pipeline_verification as rendering
from tools.school_task_frame import INPUT,IME_SLOT,ActualIME,source_contract,ROOT
from tools.school_retained_rendering_verification import need,sha,word
from tools.school_renderer_init_emulation import REGISTERS

class TaskReplay(rendering.Replay):
 def step(self,step):
  for a in step['result']['api_calls']:
   if a['key']=='system':
    need(a['import_slot']==IME_SLOT and word(self.read(IME_SLOT))==a['va'],'original IMM IAT target')
    self.put(a['va'],b'\xc3')
  return super().step(step)
 def api(self,a):
  if a['key']!='system':return super().api(a)
  sp=self.u.reg_read(REGISTERS['ESP']);r=a['call'];args=[word(self.read(sp+4))]
  need(a['sp']==sp and a['return_va']==word(self.read(sp))==0x425c99,'original IMM caller/stack')
  need(r['name']=='ImmGetOpenStatus' and r['args']==args==[word(self.read(INPUT+8))]==[0] and r['actual_OS_observed'] and type(r['result'])is int and r['result']==0,'recorded real null IMM response and source context')
  self.u.reg_write(REGISTERS['EAX'],r['result']);self.u.reg_write(REGISTERS['ESP'],sp+8);self.u.reg_write(REGISTERS['EIP'],a['return_va'])

def verify_protocol(c):
 need(c['task_frame_source']==source_contract(),'source request/assertion/frame ordering contract')
 frames=c['frames'];need(len(frames)==67 and [f['index'] for f in frames]==list(range(67)),'complete task update count')
 for f in frames:need((f['flag_before'],f['flag_after_original_reset'],f['flag_after_task'],f['task_phase'],f['reset_APIs'])==(255,0,255,2,1),'natural pending request/reset/re-request per full task')
 need(frames[0]['PC']==224 and frames[-1]['PC']==248,'original panel/text/wait progression')
 tasks=[s for s in c['steps'] if s['label'].startswith('complete_original_task_')];resets=[s for s in c['steps'] if s['label'].startswith('original_input_request_reset_')]
 need(len(tasks)==len(resets)==67 and not any(s['root'] and s['root']['va']==0x4ce8f0 for s in c['steps']),'complete tasks replace independent VM roots')
 for i,(task,reset) in enumerate(zip(tasks,resets)):
  need(task['root']['va']==0x454cf0 and task['root']['receiver']==0xe000000 and reset['root']['va']==0x425de0 and reset['root']['receiver']==INPUT,'source task/reset receiver/root')
  visited={x['va'] for x in task['result']['instruction_counts']}
  need({0x454cf0,0x454d8b,0x4ce8f0,0x454ec1,0x425f34,0x4563d0}<=visited and 0x424f80 not in visited and task['result']['cpu']['EAX']==0,'complete task/VM/reset/auxiliary guard original bodies and natural return')
  need(len(reset['result']['api_calls'])==1 and reset['result']['api_calls'][0]['key']=='system','one actual source IMM query per reset')
 observations=[a['call'] for s in c['steps'] for a in s['result']['api_calls'] if a['key']=='system']
 need(observations==c['actual_IME_trace'] and len(observations)==67,'all observed IMM calls retained')
 current=ActualIME();need(current.identity==c['actual_IME_identity'] and current.query(0)['result']==0,'same loaded actual IMM32 module and fresh null query')
 return dict(full_original_tasks=67,actual_IME_queries=67)

def verify(c):
 protocol=verify_protocol(c)
 # Reuse the exact archived R2 verifier with a private function globals copy.
 # No shared module/class or frozen source is patched.
 validate=types.FunctionType(rendering.verify.__code__,dict(rendering.verify.__globals__,Replay=TaskReplay),'verify_complete_task_resources')
 result=validate(c)
 result.update(**protocol,pending_IME_request_consumed_by_original=True,independent_VM_roots=0,original_outer_thread_scheduler=False,physical_keyboard_mouse_capture=False,R3_complete=False)
 return result

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args()
 c=json.loads(gzip.decompress((ROOT/a.report).read_bytes()))['case'];result=verify(c);out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof path required')
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print(result)
