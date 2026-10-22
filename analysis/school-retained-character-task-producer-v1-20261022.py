"""Original character handler/task animation, without display or VM substitutes."""
import copy,gzip,hashlib,json,struct
from collections import Counter
from functools import lru_cache
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_image_return as parent
from tools import school_character_animation_catalog as model
from tools.school_task_frame import INPUT,IME_SLOT
from tools.school_font_raster_emulation import IMPORTS as GDI_IMPORTS

ROOT=parent.ROOT;base=parent.base;need=parent.need;word=parent.word;sha=parent.sha;canonical=parent.canonical
ACCEPTANCE='analysis/school-retained-image-return-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='b48c9afb108ba32c0a5f0f6bf256e86e0b239de97ede9cd585208a028a989e10'
LENGTH_SLOT=next(s for s,(name,caller,pop) in GDI_IMPORTS.items() if name=='lstrlenA')
FONT_SLOT=0x5920a0
IMPORTS=dict(parent.old.init.IMPORTS);IMPORTS.update({IME_SLOT:('ImmGetOpenStatus',4),LENGTH_SLOT:('lstrlenA',4)})
ROOT_RETURN=0x32000000;STACK=0x2100f000;TACT=0xe000000;MANAGER=0x1001058
DISPLAY=(0x4cbdb0,0x410310,0x408f90,0x4cbf00,0x4d29e0,0x4c7770,0x4cba60)

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['original_IMAGE_natural_return']==0x4cc0d2 and a['game_function_substitutions']==0,'accepted original IMAGE source');keyboard=base.inputs();return dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,source_task_platform_pins=keyboard['acceptance_pins'],mode='original game/task instructions; frozen null/empty task platform and texture responses; no new GPU or input',animation_rules=model.source_rules())

def regions(g):return [dict(pointer=p,bytes=n,hex=g.read(p,n).hex()) for p,n in model.REGIONS]

def state(g):return model.state(regions(g))

def queue(g):
 rows=[]
 for pointer,size,name in ((MANAGER+0x10,0x30000,'rectangles'),(MANAGER+0x18,0x60000,'textured')):
  p=word(g.read(pointer));count=word(g.read(pointer+4));need(count<=4096,'bounded original draw queue count');rows.append(dict(name=name,pointer=p,count=count))
 return rows

class Guest(parent.Guest):
 def task_api(self,slot):
  if slot not in (IME_SLOT,LENGTH_SLOT):return self.api(slot)
  name,pop=IMPORTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4))]
  if slot==IME_SLOT:need(ret==0x425c99 and args==[word(self.read(INPUT+8))]==[0],'frozen original null IME query only')
  else:need(ret==0x425a7e and self.read(args[0],1)==bytes(1),'frozen original empty input string query only')
  self.api_calls.append(dict(kind='recorded_task_platform',name=name,import_slot=slot,target=word(self.read(slot)),sp=sp,return_va=ret,args=args,pop=pop,value=0,memory_outputs=[],new_mappings=[],origin='pinned actual complete-task/null/empty source output; not a fresh OS call'));self.u.reg_write(base.REGISTERS['EAX'],0);self.u.reg_write(base.REGISTERS['ESP'],sp+8);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def advance(self,label,stop=ROOT_RETURN,root=None):
  if root:
   self.u.mem_write(root['sp'],struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']))
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  before=self.cpu();counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;self.api_calls=[];maps=[];calls=[];targets={word(self.read(s)):s for s in IMPORTS};iat={s:self.read(s) for s in IMPORTS}
  for at in targets:
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  def code(u,at,n,_):
   if at==stop:u.emu_stop();return
   if at in targets:self.task_api(targets[at]);return
   if at==self.device_method or at in self.methods:self.gpu(at);return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'only original handler/display/task source '+hex(at))
   if at in DISPLAY:
    sp=self.cpu()['ESP'];calls.append(dict(va=at,receiver=self.cpu()['ECX'],return_va=word(self.read(sp))))
   counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original source code writes');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.ctl_remove_cache(before['EIP'],before['EIP']+1);self.u.emu_start(before['EIP'],0,count=2000000,timeout=120000000)
  except BaseException as exc:raise RuntimeError(label+' at '+hex(self.cpu()['EIP'])) from exc
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.cpu()['EIP']==stop and iat=={s:self.read(s) for s in IMPORTS},'natural original task boundary and unchanged IAT');return dict(label=label,root=root,result=dict(before_cpu=before,cpu=self.cpu(),boundary=stop,instruction_counts=[dict(va=a,count=n) for a,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=self.api_calls),entry_mappings=maps,display_calls=calls,full_memory=base.memory_rows(self.u),architectural_cpu=base.architectural_cpu(self.u),ledger=parent.old.init.old.ledger(self),state=state(self))
 def task_root(self,label,va,receiver,stop=ROOT_RETURN):
  root=dict(va=va,receiver=receiver,args=[],sp=STACK,return_va=ROOT_RETURN);return self.advance(label,stop,root)
 def frame(self,index,stop=ROOT_RETURN):
  steps=[self.task_root('original_request_consumption_'+str(index),0x425de0,INPUT)]
  for va in (0x40db90,0x40dc80):steps.append(self.task_root('original_queue_reset_'+hex(va)+'_'+str(index),va,MANAGER))
  steps.append(self.task_root('complete_original_character_task_'+str(index),0x454cf0,TACT,stop));return steps

def run_case(helper,build,branch,scene):
 memory,cpu,provenance=parent.old.boundary(branch,scene);live=parent.old.init.platform.Live(helper);hello=copy.deepcopy(live.hello)
 try:
  g=Guest(live,0 if scene==76 else 1);g.root('original_heap_initialization',0x57b9d0,[1]);g.root('original_static_lock_initialization',0x576f60);projection=parent.old.project(g,memory,cpu);baseline=word(g.read(0x79fc74));source_fs=g.read(0,4).hex();prefix=g.continuous();pending=parent.old.snapshot(g);g.configure();accounting=word(g.read(0x765720));image=g.execute('continuous_original_IMAGE_return',0x4cc0d2);image_after=parent.state(g);frames=[];before=regions(g)
  expected=model.advance(before,0,g.renderer);first=g.advance('continuous_original_character_handler_and_task_return');need(regions(g)==expected['after'],'original complete first character task equals independent animation source model');need(g.cpu()['ESP']==STACK+4 and g.cpu()['EAX']==0,'natural retained full task return');frames.append(dict(index=0,steps=[first],animation_state=first['state']))
  for index in range(1,78):
   expected=model.advance(regions(g),index,g.renderer);steps=g.frame(index);need(regions(g)==expected['after'],'original full character task equals independent model '+str(index));need(g.cpu()['ESP']==STACK+4 and g.cpu()['EAX']==0,'complete original task return');frames.append(dict(index=index,steps=steps,animation_state=steps[-1]['state']))
  need(state(g)['pc']==272 and state(g)['wait']==0 and state(g)['mode']==state(g)['background_mode']==2,'original animation naturally ready');third_expected=model.third_prefix(regions(g),word(g.read(TACT+0x64)));activation=g.frame(78);need(regions(g)==third_expected['activation']['after'],'original third-text activation complete task');font_target=word(g.read(FONT_SLOT));third=g.frame(79,font_target);need(regions(g)==third_expected['after'],'original third-text prefix source state');sp=g.cpu()['ESP'];font=dict(target=font_target,import_slot=FONT_SLOT,args=[word(g.read(sp+4+i*4)) for i in range(14)],return_va=word(g.read(sp)),first_instruction_executed=False);need(font['return_va']==0x4cad09 and font['args']==third_expected['pending_font']['args'],'natural third CreateFontA ABI');final_memory=base.memory_rows(g.u);final_cpu=base.architectural_cpu(g.u);root=dict(va=0x41f4e0,args=[32],sp=STACK,return_va=ROOT_RETURN,receiver=g.renderer+0x844);cleanup=g.execute('supplemental_original_character_container_cleanup',ROOT_RETURN,root);need(g.gpu_count==6 and not g.allocations and word(g.read(0x765720))==accounting and parent.old.init.old.ledger(g)['game_bytes']==baseline,'source original container and both counters balanced');g.root('original_static_lock_teardown',0x576fa0);g.root('original_heap_teardown',0x57ba60);live.close()
 except BaseException:
  if not live.closed:
   try:live.close()
   except BaseException:pass
  raise
 print(branch,scene,'79 complete tasks and third font boundary; original presentation and readiness',flush=True)
 return dict(name=branch,scene_capture=scene,parent_boundary=provenance,fixture_inputs=g.declaration,initial_native_hello=hello,source_heap_created=g.heap_created,helper_build=build,projection=projection,game_accounting_baseline=baseline,source_entry_SEH_hex=source_fs,prefix=prefix,pending_texture=pending,typed_texture_projection=g.translation,accounting_before=accounting,image=image,image_after=image_after,copy_rows=g.copy_rows,frames=frames,activation=activation,third=third,pending_font=font,final_memory=final_memory,final_architectural_cpu=final_cpu,cleanup=cleanup,steps=g.steps,allocation_history=g.history,native_trace=live.trace,helper_exit_code=live.exit_code,helper_cleanup=live.cleanup)

def run(helper,build):return dict(schema_version=1,contract=contracts(),cases=[run_case(helper,build,n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],new_forward_VM_roots=0,game_function_substitutions=0,IAT_rebindings=0,full_original_task_and_animation=True,new_GPU=False,new_window=False,new_OS_input=False,historical_heap_restored=False,original_outer_scheduler=False,third_font_created=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report')
 helper,build=parent.old.init.platform.build(ROOT/a.helper);r=run(helper,build);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('six original character tasks/animation to third font boundary',flush=True)
