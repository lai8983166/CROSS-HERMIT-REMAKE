"""Original third dialogue, owned offscreen GDI and recorded texture interfaces."""
import copy,ctypes as C,gzip,hashlib,json,struct,types
from collections import Counter
from functools import lru_cache
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_character_task as parent
from tools import school_retained_name_raster as raster
from tools import school_third_live_text_catalog as rules
from tools import school_third_live_text_verification as historical
from tools.school_retained_rendering import AddressSpace

ROOT=parent.ROOT;base=parent.base;need=parent.need;word=parent.word;sha=parent.sha;canonical=parent.canonical
ACCEPTANCE='analysis/school-retained-character-task-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='146914735f517313c08d8827d19a7f04a114fdb81b38b8e95d792f7b8e60ba52'
NATIVE_ACCEPTANCE='analysis/school-third-live-text-acceptance-20261013.json'
NATIVE_ACCEPTANCE_SHA='165e4cea45dfeec11e69a85e1d58bc8af49bda64619669341025a06fbe2b1ddf'
NATIVE='analysis/school-third-live-text-v4-20261013.json'
NATIVE_SHA=historical.EVIDENCE_SHA256
RASTER=0x3e000000;TEXTURE=rules.TEXTURE;FONT_STOP=0x403bd0
GDI=dict(raster.IMPORTS);GDI.update({0x5920c4:('DeleteObject',None,4),0x592060:('DeleteDC',0x40596a,4)})
IMPORTS=dict(parent.IMPORTS);IMPORTS.update({s:(v[0],v[2]) for s,v in GDI.items()})
DISPLAY=parent.DISPLAY;RETURN=parent.ROOT_RETURN;STACK=parent.STACK

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['tasks_complete']==3 and a['final_PC']==280 and not a['third_font_created'],'accepted original third font boundary');raw=base.pinned(NATIVE,NATIVE_SHA);r=json.loads(raw);proof=[historical.compare_live(c) for c in r['cases']];n=json.loads(base.pinned(NATIVE_ACCEPTANCE,NATIVE_ACCEPTANCE_SHA));need(n['native']['path']==NATIVE and n['native']['sha256']==NATIVE_SHA,'accepted native third texture');return r['cases'][0]['third_live_text'],r['cases'][0]['first_live_text']['COM_process_cleanup']['texture_releases'][0],dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,native_acceptance=NATIVE_ACCEPTANCE,native_acceptance_sha256=NATIVE_ACCEPTANCE_SHA,native_report=NATIVE,native_report_sha256=NATIVE_SHA,historical_texture_proof=proof,mode='fresh owned offscreen GDI; recorded GPU only; original complete tasks; retained input unchanged')

def mapped_texture():
 n,release,c=contracts();s=AddressSpace();s.next=0x6c001000;return s.result('recorded_third',n['COM_calls'][0]['result']),s.result('recorded_third',n['COM_calls'][2]['result']),s.ledger()

class Offscreen(raster.Offscreen):
 call_raster=types.FunctionType(raster.Offscreen.call.__code__,dict(raster.Offscreen.call.__globals__,RASTER=RASTER),'owned_third_raster_API')
 def __init__(self,logical):
  super().__init__(logical);self.gdi.k.lstrlenA.argtypes=[C.c_char_p];self.gdi.k.lstrlenA.restype=C.c_int;self.stages=[]
 def call(self,g,name,args,ret):
  if name=='DeleteObject':
   wanted=self.bitmap if ret==0x405921 else self.font;need(ret in (0x405921,0x4d1c1b) and args==[wanted],'original owned bitmap/font deletion');row=dict(name=name,args=args,dc_translated_args=list(args),result=self.gdi.delete_object(wanted),memory_outputs=[])
  elif name=='DeleteDC':need(ret==0x40596a and args==[self.raster_dc],'original owned raster DC deletion');row=dict(name=name,args=args,dc_translated_args=list(args),result=self.gdi.delete_dc(args[0]),memory_outputs=[])
  else:row=self.call_raster(g,name,args)
  if name in ('PatBlt','TextOutA'):self.stages.append(dict(name=name,return_va=ret,hex=self.gdi.raster(self.bitmap).hex()))
  return row

def text_state(g):
 return dict(animation=parent.state(g),object_hex=g.read(rules.OBJECT,rules.BYTES).hex(),node_hex=g.read(rules.NODE,224).hex(),input_words=[word(g.read(parent.TACT+x)) for x in (0x198c,0x1990,0x19a0)],space=g.read(parent.INPUT+0x480+57,1).hex())

class Guest(parent.Guest):
 def new_api(self,slot):
  sp=self.cpu()['ESP'];ret=word(self.read(sp))
  if slot not in GDI or slot==parent.LENGTH_SLOT and ret==0x425a7e:return self.task_api(slot)
  name,caller,pop=GDI[slot];args=[word(self.read(sp+4+i)) for i in range(0,pop,4)]
  if caller is not None:need(ret==caller,'exact original third GDI caller '+name)
  row=self.offscreen.call(self,name,args,ret);row.update(kind='actual_owned_third_GDI',import_slot=slot,target=word(self.read(slot)),sp=sp,return_va=ret,pop=pop,new_mappings=[])
  if name=='CreateDIBSection':row['new_mappings']=[dict(pointer=RASTER,bytes=row['mapped_bytes'])]
  self.memory_evidence.refresh()
  for o in row['memory_outputs']:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  self.api_calls.append(row);self.u.reg_write(base.REGISTERS['EAX'],row['result']);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def new_gpu(self,at):
  i=self.third_gpu_count;need(i<6,'four recorded third texture and two cleanup calls');slot=[80,56,64,68,56,8][i];t=self.third_texture;need(at==(self.device_method if i==0 else t['methods'][str(slot)]),'original third COM method/object');sp=self.cpu()['ESP'];ret=word(self.read(sp));need(ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][i],'original third COM return');pop={80:32,56:12,64:20,68:8,8:4}[slot];args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];outputs=[];maps=[];extra={};bp=self.cpu()['EBP']
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if i==0:
   need(args==[self.device,256,64,1,0,25,1,TEXTURE+44],'source third CreateTexture ABI');result=copy.deepcopy(self.third_creation);maps=list(dict.fromkeys((p&~4095,4096) for p in (t['pointer'],t['vtable'],*t['methods'].values())));put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  elif i in (1,4):
   need(args==[t['pointer'],0,bp-(52 if i==1 else 36)],'source third descriptor output');result=copy.deepcopy(self.third_native['COM_calls'][1]['result']);put(args[2],bytes.fromhex(result['hex']))
  elif i==2:
   need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048],'source third lock ABI');result=copy.deepcopy(self.third_lock);b=bytes.fromhex(result['hex']);p=result['bits']&~4095;maps=[(p,(result['bits']-p+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
  elif i==3:
   need(args==[t['pointer'],0],'source third unlock');result=copy.deepcopy(self.third_native['COM_calls'][3]['result']);pixels=self.read(self.third_lock['bits'],self.third_lock['pitch']*64);need(sha(pixels)==result['uploaded_sha256'],'all original converted third pixels equal historical native upload');extra['uploaded_hex']=pixels.hex()
  else:need(args==[t['pointer']] and self.third_release==dict(pointer=self.third_native['texture']['pointer'],unlock_hr=0,count=0),'only owned logical third texture released');result=copy.deepcopy(self.third_release)
  value=result['count'] if i==5 else result['hr'];row=dict(kind='recorded_third_GPU_only',index=i,slot=slot,target=at,sp=sp,return_va=ret,pop=pop,args=args,value=value,result=result,historical_report_sha256=NATIVE_SHA,new_mappings=[dict(pointer=p,bytes=n) for p,n in maps],memory_outputs=outputs,**extra)
  for p,n in maps:need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'fresh typed third COM output pages');self.u.mem_map(p,n)
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  self.memory_evidence.refresh()
  for o in outputs:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  self.api_calls.append(row);self.third_gpu_count+=1;self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def advance_new(self,label,stop=RETURN,root=None):
  if root:
   self.u.mem_write(root['sp'],struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']))
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  before=self.cpu();counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;self.api_calls=[];maps=[];calls=[];conversions=[];targets={word(self.read(s)):s for s in IMPORTS};iat={s:self.read(s) for s in IMPORTS}
  need(len(targets)==len(IMPORTS),'distinct original platform bindings')
  for at in targets:
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  self.memory_evidence.refresh()
  if root:self.memory_evidence.mark(root['sp'],4*(len(root['args'])+1))
  def code(u,at,n,_):
   if at==stop:u.emu_stop();return
   if at in targets:self.new_api(targets[at]);return
   if at==self.device_method or at in self.third_methods:self.new_gpu(at);return
   key=(at,n)
   if key not in self.code_chunks:need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'only original third source '+hex(at));self.code_chunks[key]=struct.pack('<I',at)+self.read(at,n)
   if at in DISPLAY:sp=self.cpu()['ESP'];calls.append(dict(va=at,receiver=self.cpu()['ECX'],return_va=word(self.read(sp))))
   if at==0x405869:
    sp=self.cpu()['ESP'];args=[word(self.read(sp+j)) for j in range(0,24,4)];conversions.append(dict(va=at,args=args,lock_hex=self.read(args[1],8).hex(),rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   counts[at]+=1;ih.update(self.code_chunks[key])
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original text modification');self.memory_evidence.mark(at,n);writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.ctl_remove_cache(before['EIP'],before['EIP']+1);self.u.emu_start(before['EIP'],0,count=2000000,timeout=120000000)
  except BaseException as exc:raise RuntimeError(label+' at '+hex(self.cpu()['EIP'])) from exc
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.cpu()['EIP']==stop and iat=={s:self.read(s) for s in IMPORTS},'natural third boundary and unchanged IAT');return dict(label=label,root=root,result=dict(before_cpu=before,cpu=self.cpu(),boundary=stop,instruction_counts=[dict(va=a,count=n) for a,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=self.api_calls),entry_mappings=maps,display_calls=calls,conversions=conversions,full_memory=self.memory_evidence.snapshot(),architectural_cpu=base.architectural_cpu(self.u),ledger=parent.parent.old.init.old.ledger(self),state=text_state(self),queue=parent.queue(self))
 def new_root(self,label,va,recv):return self.advance_new(label,RETURN,dict(va=va,receiver=recv,args=[],sp=STACK,return_va=RETURN))
 def new_frame(self,index):return [self.new_root('third_request_'+str(index),0x425de0,parent.INPUT),self.new_root('third_queue_a_'+str(index),0x40db90,parent.MANAGER),self.new_root('third_queue_b_'+str(index),0x40dc80,parent.MANAGER),self.new_root('third_complete_task_'+str(index),0x454cf0,parent.TACT)]
 def continue_third(self):
  self.third_native,self.third_release,contract=contracts();self.third_creation,self.third_lock,translation=mapped_texture();self.third_texture=self.third_creation['texture'];self.third_methods=set(self.third_texture['methods'].values());self.third_gpu_count=0;logical=word(self.read(self.renderer+0xb208));self.offscreen=Offscreen(logical);before=text_state(self);account=word(self.read(0x765720));font_sp=self.cpu()['ESP'];font_bp=self.cpu()['EBP'];entry=dict(cpu=self.cpu(),font_args=[word(self.read(font_sp+4+i*4)) for i in range(14)],input_words=before['input_words']);out=None
  try:
   first=self.advance_new('continuous_original_third_font_raster',FONT_STOP);raw=self.offscreen.gdi.raster(self.offscreen.bitmap);raster_record=dict(measured=self.offscreen.measured,selected_face=self.offscreen.face,ACP=self.offscreen.gdi.acp,font=self.offscreen.font,bitmap=self.offscreen.bitmap,raster_dc=self.offscreen.raster_dc,logical_measurement_dc=logical,fresh_owned_measurement_dc=self.offscreen.actual,stages=copy.deepcopy(self.offscreen.stages),raster_hex=raw.hex(),raster_sha256=sha(raw),pending_cpu=self.cpu());second=self.advance_new('continuous_original_third_texture_handler_and_task');need(parent.state(self)['pc']==286 and self.cpu()['ESP']==STACK+4,'third handler and full original task natural return');completed=text_state(self);frames=[]
   for i in range(80):
    s=self.new_frame(i);frames.append(dict(index=i,steps=s,state=text_state(self)));pc=parent.state(self)['pc'];wait=parent.state(self)['wait'];print('third wait',i,'PC',pc,'wait',wait,flush=True)
    need(pc==290,'third original opcode50 before next confirmation')
    if not wait:break
   else:raise ValueError('bounded original third readiness')
   final_memory=base.memory_rows(self.u);need(final_memory==frames[-1]['steps'][-1]['full_memory'],'fresh full rehash of every source mapping');final_cpu=base.architectural_cpu(self.u);final=text_state(self);pixels=self.read(self.third_lock['bits'],self.third_lock['pitch']*64);cleanup=self.new_root('supplemental_original_third_texture_destructor',0x403730,TEXTURE);need(self.third_gpu_count==6 and word(self.read(0x765720))==account,'original third texture descriptor/release and byte accounting balanced');out=dict(contract=contract,typed_texture_projection=translation,entry=entry,before=before,raster_step=first,raster=raster_record,completion=second,completed=completed,frames=frames,final=final,final_memory=final_memory,final_architectural_cpu=final_cpu,converted_hex=pixels.hex(),converted_sha256=sha(pixels),accounting_before=account,cleanup=cleanup,source_GPU_calls=self.third_gpu_count,retained_input_host_writes=0,new_VM_roots=0)
  finally:cleanup=self.offscreen.close()
  out['offscreen_cleanup']=cleanup;return out

def run_case(helper,build,name,scene):
 captured=[]
 class Attached(Guest):
  def execute(self,label,stop,root=None):
   if label=='supplemental_original_character_container_cleanup':captured.append(self.continue_third())
   return super().execute(label,stop,root)
 call=types.FunctionType(parent.run_case.__code__,dict(parent.run_case.__globals__,Guest=Attached),'original_parent_with_continuation_before_cleanup');c=call(helper,build,name,scene);need(len(captured)==1,'single third continuation in original CRT lifetime');c['third_dialogue']=captured[0];return c

def run(helper,build):return dict(schema_version=1,contract=contracts()[2],cases=[run_case(helper,build,n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],new_forward_VM_roots=0,game_function_substitutions=0,IAT_rebindings=0,new_OS_input=False,new_window=False,new_GPU=False,original_outer_scheduler=False,historical_heap_restored=False,third_font_created=True,fresh_owned_offscreen_GDI=True,new_GPU_draw_or_Present=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report')
 helper,build=parent.parent.old.init.platform.build(ROOT/a.helper);r=run(helper,build);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('six original third dialogues completed',flush=True)
