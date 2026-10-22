"""Independent source execution of character tasks, complete queues and third font."""
import bisect,copy,gzip,hashlib,json,struct
from collections import Counter
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_character_task as work
from tools import school_retained_image_return_verification as previous

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;canonical=work.canonical;sha=work.sha

def protocol(c,reference=False):
 need(c['name'] in ('initial','student9_waiting','fifth_class') and c['scene_capture'] in (76,77),'six source branches');need([s['label'] for s in c['steps']]==previous.LABELS,'two original CRT init/teardown roots');need(c['helper_exit_code']==0 and c['helper_cleanup']==dict(all_owned_resources_released=True,heap_destroyed=True,critical_deleted=True,open_files=0,allocations=0,depth=0,forced_cleanup=False),'normal source-owned native cleanup')
 h=c['initial_native_hello'];need(h['heap']==h['critical']==0 and h['pointer_bytes']==4 and h['window_created'] is h['GPU_created'] is False,'new headless native owner without precreated CRT state');b=c['helper_build'];p=__import__('pathlib').Path(b['helper_path']);need(b['source_sha256']==sha(work.parent.old.init.platform.SOURCE.read_bytes()) and b['compiler_sha256']==sha(work.parent.old.init.platform.old.COMPILER.read_bytes()) and b['helper_sha256']==sha(p.read_bytes()) and b['machine']==work.parent.old.init.platform.old.machine(p)==0x14c,'helper source/compiler/x86 binary identity');need([f['index'] for f in c['frames']]==list(range(78)) and [len(f['steps']) for f in c['frames']]==[1]+[4]*77 and len(c['activation'])==len(c['third'])==4,'78 animation updates, activation and partial third full task')
 for i,t in enumerate(c['native_trace']):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok']is True,'successful exact native operation order')
 p=c['projection'];need(p['historical_heap_restored']is p['game_accounting_reset']is False and p['all_other_retained_bytes_unchanged']is True and [(r['pointer'],r['bytes'],r['role']) for r in p['rows']]==list(work.parent.old.DOMAIN),'source-backed CRT domain only, no game/CPU reset')
 for f in c['frames']:
  index=f['index'];mode=6 if index<30 else 3 if index<76 else 2;expected=dict(pc=272,wait=int(index<77),mode=mode,previous_mode=mode,fade_count=index-30 if 30<=index<76 else 0,fade_limit=45,delay_count=index+1 if index<30 else 0,delay_limit=30,background_mode=3 if index<61 else 2,background_count=index+1 if index<61 else 0,background_limit=60,instruction_count=int(index==0),waiting_count=index);need(f['animation_state']==f['steps'][-1]['state']==expected,'independent source timing/readiness sequence')
  for j,s in enumerate(f['steps']):
   if not reference:need('queue' in s,'complete original queue evidence after each source interval')
   if not index:need(s['root']is None,'continuous original first task stack')
   else:root_check(s,(0x425de0,0x40db90,0x40dc80,0x454cf0)[j],(work.INPUT,work.MANAGER,work.MANAGER,work.TACT)[j])
 font=c['pending_font'];need(font['import_slot']==work.FONT_SLOT and font['return_va']==0x4cad09 and font['first_instruction_executed']is False and font['args']==work.model.text_rules()['first_font_arguments'],'unexecuted third-font source ABI')
 if not reference:
  bp=work.STACK-4;expected=[dict(label='font',bp=bp-100-144-2704,return_va=0x4c4d04),dict(label='text',bp=bp-100-144,return_va=0x4cec2b),dict(label='vm',bp=bp-100,return_va=0x454d90),dict(label='task',bp=bp,return_va=work.ROOT_RETURN)];need(font['frames']==expected,'four original third-font/task frames')

class Replay(previous.Replay):
 def api(self,a):
  if a.get('kind')!='recorded_task_platform':return super().api(a)
  sp=self.cpu()['ESP'];slot=a['import_slot'];need(slot in (work.IME_SLOT,work.LENGTH_SLOT),'only frozen null/empty task platform leaves');name,pop=work.IMPORTS[slot];args=[word(self.read(sp+4))];ret=word(self.read(sp));need(a['va']==a['target']==word(self.read(slot)) and a['sp']==sp and a['return_va']==ret and a['args']==args and a['name']==name and a['pop']==4 and a['value']==0 and a['new_mappings']==a['memory_outputs']==[] and a['origin']=='pinned actual complete-task/null/empty source output; not a fresh OS call','exact frozen original task API contract')
  if slot==work.IME_SLOT:need(ret==0x425c99 and args==[word(self.read(work.INPUT+8))]==[0],'null original IME context')
  else:need(ret==0x425a7e and self.read(args[0],1)==bytes(1),'original empty input string caller')
  self.u.reg_write(base.REGISTERS['EAX'],0);self.u.reg_write(base.REGISTERS['ESP'],sp+8);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def task_step(self,s,reference=False):
  maps=[]
  for slot in work.IMPORTS:
   at=word(self.read(slot))
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  need(maps==s['entry_mappings'],'only missing original platform entry pages');root=s['root'];a=s['result']
  if not hasattr(self,'task_code'):
   need(self.read(0x401000,0x191000)==self.image[0x1000:0x192000],'complete original text before instruction cache');self.task_code={};self.region_hashes={}
  dirty=set()
  if root:
   self.u.mem_write(root['sp'],struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']));dirty.add(root['sp']>>12)
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  need(self.cpu()==a['before_cpu'],'full original continuation CPU before task');calls=iter(a['api_calls']);next_api=next(calls,None);ih=hashlib.sha256();wh=hashlib.sha256();counts=Counter();writes=0;display=[]
  def code(u,at,n,_):
   nonlocal next_api
   if at==a['boundary']:u.emu_stop();return
   if next_api and at==next_api['target']:
    q=next_api;self.api(dict(q,va=q['target'],key='recorded_task_platform'));need(q.get('kind')=='recorded_task_platform','task continuation has no unplanned graphics/native calls');next_api=next(calls,None);return
   key=(at,n)
   if key not in self.task_code:
    need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'only unchanged original task/display bytes');self.task_code[key]=struct.pack('<I',at)+self.read(at,n)
   if at in work.DISPLAY:sp=self.cpu()['ESP'];display.append(dict(va=at,receiver=self.cpu()['ECX'],return_va=word(self.read(sp))))
   ih.update(self.task_code[key]);counts[at]+=1
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original text write');dirty.update(range(at>>12,((at+n-1)>>12)+1));writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  ch=self.u.hook_add(UC_HOOK_CODE,code);wr=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.emu_start(a['before_cpu']['EIP'],0,count=2000000,timeout=120000000)
  except BaseException as exc:raise RuntimeError(s['label']+' at '+hex(self.cpu()['EIP'])) from exc
  finally:self.u.hook_del(ch);self.u.hook_del(wr)
  need(next_api is None and self.cpu()==a['cpu'] and ih.hexdigest()==a['instruction_sha256'] and [dict(va=p,count=n) for p,n in sorted(counts.items())]==a['instruction_counts'],'every original instruction, all APIs and natural CPU return');need(writes==a['writes'] and wh.hexdigest()==a['write_sha256'] and display==s['display_calls'],'every original write and display call without substitution');pages=sorted(dirty);rows=[]
  for lo,hi,_ in self.u.mem_regions():
   key=(lo,hi);i=bisect.bisect_left(pages,lo>>12)
   if key not in self.region_hashes or i<len(pages) and pages[i]<=hi>>12:self.region_hashes[key]=dict(pointer=lo,bytes=hi-lo+1,sha256=sha(self.read(lo,hi-lo+1)))
   rows.append(self.region_hashes[key])
  need(rows==s['full_memory'] and canonical(base.architectural_cpu(self.u))==canonical(s['architectural_cpu']),'all memory regions and entire architectural CPU after every source interval');need(work.parent.old.init.old.ledger(self)==s['ledger'] and work.state(self)==s['state'],'original CRT accounting and animation/task state')
  if not reference:
   b=self.read(work.MANAGER,96);slots=word(b,8);capacity=word(b,12);head=word(b,16);arena=word(b,20);end=word(b,48);need(slots==4096 and capacity==1048576 and arena<=end<=arena+capacity,'original draw arena bounds');q=dict(manager_hex=b.hex(),head_pointer=head,head_hex=self.read(head,32768).hex(),arena_pointer=arena,used_bytes=end-arena,arena_hex=self.read(arena,end-arena).hex());need(q==s['queue'],'complete original 4096 head/tail pairs and every live draw record')
  return sum(counts.values())

def root_check(s,va,recv):need(s['root']==dict(va=va,receiver=recv,args=[],sp=work.STACK,return_va=work.ROOT_RETURN),'exact full task/reset root; never independent VM root')

def prepare(c):
 r=Replay(c);initialization=0
 for s,va,args in zip(c['steps'][:2],(0x57b9d0,0x576f60),([1],[])):
  need(s['root']==dict(va=va,args=args,sp=work.STACK,return_va=work.ROOT_RETURN,receiver=0),'original CRT initialization roots');initialization+=previous.previous.replay_step(r,s)
 previous.previous.project(r,c);need(r.read(0,4).hex()==c['source_entry_SEH_hex'],'source original exception chain');p=c['prefix'];maps=[]
 for slot in work.parent.old.init.IMPORTS:
  at=word(r.read(slot))
  if not any(a<=at<=b for a,b,_ in r.u.mem_regions()):p0=at&~4095;r.u.mem_map(p0,4096);maps.append(dict(pointer=p0,bytes=4096))
 need(maps==p['entry_mappings'],'original CRT API mappings');count=r.step(dict(label=p['label'],root=None,result=dict(p,api_calls=[dict(q,va=q['target'],key='original_CRT_OS') for q in p['api_calls']])));need(count==69440 and base.memory_rows(r.u)==p['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(p['architectural_cpu']),'whole original IMAGE source prefix');previous.previous.snapshot(r,dict(c,boundary=c['pending_texture']));r.configure(c);previous.step(r,c['image']);previous.verify_after(r,dict(c,after=c['image_after']));need(r.copy_rows==c['copy_rows'],'all original memcpy rows retained');return r,initialization

def verify_case(c,reference=False):
 protocol(c,reference);work.contracts();r,initialization=prepare(c);new_count=new_writes=displays=0
 for index,f in enumerate(c['frames']):
  expected=work.model.advance(work.regions(r),index,r.renderer)
  if index==0:need(f['steps'][0]['root'] is None,'first original handler/VM/task return stays on original stack')
  else:
   for s,va,receiver in zip(f['steps'],(0x425de0,0x40db90,0x40dc80,0x454cf0),(work.INPUT,work.MANAGER,work.MANAGER,work.TACT)):root_check(s,va,receiver)
  for s in f['steps']:
   new_count+=r.task_step(s,reference);new_writes+=s['result']['writes'];displays+=len(s['display_calls']);need(r.cpu()['EIP']==work.ROOT_RETURN and r.cpu()['ESP']==work.STACK+4,'complete original root natural return, never a truncated reset')
  need(work.regions(r)==expected['after'] and f['animation_state']==work.state(r) and r.cpu()['EIP']==work.ROOT_RETURN and r.cpu()['ESP']==work.STACK+4 and r.cpu()['EAX']==0,'all original animation state, full task and natural return');visited={i['va'] for s in f['steps'] for i in s['result']['instruction_counts']};required={0x4ca1b0,0x4c99e0,0x4cbdb0,0x4079c0,0x454ec1,0x4563d0}
  if index:required.add(0x425f34)
  need(required<=visited and 0x424f80 not in visited,'original presentation, enqueue and complete task epilogue execute; first task request already preceded IMAGE')
 ready=work.state(r);need(ready['pc']==272 and ready['wait']==0 and ready['mode']==ready['background_mode']==2 and ready['waiting_count']==77,'original readiness after source 30/45/60 updates');expected=work.model.third_prefix(work.regions(r),word(r.read(work.TACT+0x64)))
 for group,label in ((c['activation'],'activation'),(c['third'],'third')):
  for j,(s,va,recv) in enumerate(zip(group,(0x425de0,0x40db90,0x40dc80,0x454cf0),(work.INPUT,work.MANAGER,work.MANAGER,work.TACT))):
   root_check(s,va,recv);new_count+=r.task_step(s,reference);new_writes+=s['result']['writes'];displays+=len(s['display_calls'])
   if label=='activation' or j<3:need(r.cpu()['EIP']==work.ROOT_RETURN and r.cpu()['ESP']==work.STACK+4,'complete task/reset before third-font continuation')
  need(work.regions(r)==(expected['activation']['after'] if label=='activation' else expected['after']),'original third text activation and prefix source state')
 sp=r.cpu()['ESP'];font=dict(target=word(r.read(work.FONT_SLOT)),import_slot=work.FONT_SLOT,args=[word(r.read(sp+4+i*4)) for i in range(14)],return_va=word(r.read(sp)),first_instruction_executed=False);frames=work.parent.old.parent.chain(r,[('font',0x4c4d04),('text',0x4cec2b),('vm',0x454d90),('task',work.ROOT_RETURN)])
 if not reference:font['frames']=frames
 need(font==c['pending_font'] and font['args']==expected['pending_font']['args'] and font['return_va']==0x4cad09 and r.cpu()['EIP']==font['target'],'natural third font arguments and four original task frames');need(base.memory_rows(r.u)==c['final_memory']==c['third'][-1]['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(c['final_architectural_cpu']),'fresh complete byte rehash verifies incremental hashes and all final CPU registers');need(new_count==2962747 and new_writes==1706706 and displays==2945,'complete original task/animation instruction/write/display totals');root=dict(va=0x41f4e0,args=[32],sp=work.STACK,return_va=work.ROOT_RETURN,receiver=r.renderer+0x844);need(c['cleanup']['root']==root,'explicit source-only container cleanup root');previous.step(r,c['cleanup']);need(r.gpu_count==6 and not r.blocks and word(r.read(0x765720))==c['accounting_before'] and work.parent.old.init.old.ledger(r)['game_bytes']==c['game_accounting_baseline'],'original source resource/accounting cleanup')
 for s,va in zip(c['steps'][2:],(0x576fa0,0x57ba60)):
  need(s['root']==dict(va=va,args=[],sp=work.STACK,return_va=work.ROOT_RETURN,receiver=0),'original lock/heap destruction');initialization+=previous.previous.replay_step(r,s)
 need(not r.blocks and not r.files and not r.criticals and r.depth==0 and r.history==c['allocation_history'] and r.consume('close')==c['helper_cleanup'] and r.wire==len(c['native_trace']),'all native resources source-released and normal complete helper transcript');return dict(name=c['name'],scene_capture=c['scene_capture'],new_original_task_instructions=new_count,new_original_task_writes=new_writes,source_display_calls=displays,complete_original_tasks=79,partial_original_task_to_third_font=1,independent_VM_roots=0,animation_updates=78,IME_resets=79,queue_resets=158,final_PC=280,third_font_created=False,full_CPU_and_all_memory_verified=True,source_queue_records_verified=not reference,whole_memory_rehash_verified=True,normal_native_cleanup=True,new_GPU=False,R3_complete=False)

def verify(r):
 need(r['schema_version']==1 and r['contract']==work.contracts() and r['new_forward_VM_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0 and r['full_original_task_and_animation']is True,'pinned original task/animation without display substitutes or VM roots')
 for k in ('new_GPU','new_window','new_OS_input','historical_heap_restored','original_outer_scheduler','third_font_created','R3_complete','R6_complete'):need(r[k]is False,'honest incomplete scope '+k)
 need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six retained branches');return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],six_original_character_tasks_and_animation_verified=True,complete_original_tasks_each=79,full_source_presentation_and_queue_verified=True,new_GPU=False,interactive_desktop_required=False,third_font_created=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 result=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())));out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six original character task/animation/queue and third-font boundaries verified',flush=True)
