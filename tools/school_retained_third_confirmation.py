"""Captured original keyboard confirmation and fourth offscreen text handoff."""
import copy,gzip,json,struct,types,inspect,textwrap
from functools import lru_cache
from tools import school_retained_third_dialogue as previous
from tools.school_retained_portrait_file_verification import chain
from tools.school_text_preparation_catalog import source_catalog as text_rules

ROOT=previous.ROOT;base=previous.base;need=previous.need;word=previous.word;sha=previous.sha;canonical=previous.canonical
ACCEPTANCE='analysis/school-retained-third-dialogue-acceptance-v1-20261023.json'
ACCEPTANCE_SHA='5fe7ab87f55545ccc2df693d46887efe9e1288b401920e7adcfdbb1b6930bccd'
KEYBOARD=base.KEYBOARD;VM=base.VM;STACK=previous.STACK;RETURN=previous.RETURN;RASTER=0x3d000000
NODE=VM+0x6f60+7*0xe0;OBJECT=VM+0x430+7*0xab8;TEXTURE=OBJECT+0x28

def adapt_validation(fn,replacements,**overrides):
 """Extend only Python accounting checks for an additional original resource free."""
 source=textwrap.dedent(inspect.getsource(fn))
 for before,after in replacements:
  need(source.count(before)==1,'exact frozen validation adaptation '+before);source=source.replace(before,after)
 namespace=dict(fn.__globals__,**overrides);exec(compile(source,fn.__code__.co_filename+'[additional_original_free]','exec'),namespace);return namespace[fn.__name__]

@lru_cache(maxsize=3)
def existing_texture(name):
 p=base.inputs()['parents'][name];c=json.loads(gzip.decompress(base.pinned(p['path'],p['sha256'])))['case'];creates=[r for r in c['device_proxy_trace'] if r['op']=='text_create'];need(len(creates)==2 and c['device_cleanup']['text_texture_release_counts']==[0,0] and c['device_cleanup']['all_owned_resources_released'],'two source-owned R2 textures released at zero references');t=creates[0]['result']['texture'];descriptor=next(r for r in c['device_proxy_trace'] if r['op']=='text_desc' and r['request']['pointer']==t['pointer']);need(bytes.fromhex(descriptor['result']['hex'])==struct.pack('<8I',25,1,0,1,16384,0,256,32),'source first text full descriptor');return dict(source=p,texture=t,descriptor=descriptor,release_count=0,source_cleanup=c['device_cleanup'],bytes=16384)

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['final_PC']==290 and a['final_wait']==0 and a['tasks_complete']==3 and not a['next_confirmation_instruction_executed'],'accepted source third readiness');native=base.inputs();script,_=previous.rules.script_layout();commands=[]
 for pc,expected in [(290,'33000400'),(294,'2b00080004000020'),(302,'2c000400'),(306,'110006000300'),(312,'1e0014000700002009000020000000201e000020')]:
  b=bytes.fromhex(expected);need(script[452+pc:452+pc+len(b)]==b,'original next script instruction');commands.append(dict(PC=pc,file_offset=452+pc,hex=b.hex()))
 return dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,native_capture_acceptance_pins=native['acceptance_pins'],streams={str(k):v for k,v in native['streams'].items()},commands=commands,fourth_text=text_rules()['entries'][3],mode='recorded source device bytes through original keyboard and complete tasks; fresh owned fourth offscreen GDI; no new GPU or OS input')

class Offscreen(previous.Offscreen):
 call_raster=types.FunctionType(previous.Offscreen.call_raster.__code__,dict(previous.Offscreen.call_raster.__globals__,RASTER=RASTER),'owned_fourth_raster_API')

def state(g):
 pc,wait,op,size=struct.unpack('<I3H',g.read(VM+28,10));return dict(PC=pc,wait=wait,opcode=op,opcode_size=size,space_current=g.read(KEYBOARD+0x4b9,1)[0],selected_layer=g.read(VM+0x1cc,1)[0],input_words=[word(g.read(previous.parent.TACT+x)) for x in (0x198c,0x1990,0x19a0)],fourth_text_count=struct.unpack('<H',g.read(OBJECT+22,2))[0])

class Guest(previous.Guest):
 continue_third=adapt_validation(previous.Guest.continue_third,[("word(self.read(0x765720))==account","word(self.read(0x765720))==account-getattr(self,'replaced_texture_bytes',0)")])
 fourth_api=types.FunctionType(previous.Guest.new_api.__code__,dict(previous.Guest.new_api.__globals__,RASTER=RASTER),'original_fourth_GDI')
 def new_api(self,slot):
  if getattr(self,'fourth_running',False):
   result=self.fourth_api(slot)
   if self.api_calls[-1]['kind']=='actual_owned_third_GDI':self.api_calls[-1]['kind']='actual_owned_fourth_GDI'
   return result
  return super().new_api(slot)
 def new_gpu(self,at):
  resource=getattr(self,'existing_resource',None)
  if resource is None or at not in (resource['texture']['methods']['8'],resource['texture']['methods']['56']):return super().new_gpu(at)
  i=self.existing_gpu_count;need(i in (0,1),'one descriptor and release for replaced first text');t=resource['texture'];slot=(56,8)[i];pop=(12,4)[i];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+n)) for n in range(0,pop,4)];need(at==t['methods'][str(slot)] and ret==(0x403a44,0x40378d)[i],'original replaced-text method and caller');outputs=[]
  if i==0:
   need(args==[t['pointer'],0,self.cpu()['EBP']-36],'original replaced-text descriptor destination');result=copy.deepcopy(resource['descriptor']['result']);outputs=[dict(pointer=args[2],hex=result['hex'])];self.u.mem_write(args[2],bytes.fromhex(result['hex']));self.memory_evidence.mark(args[2],32);value=result['hr']
  else:need(args==[t['pointer']],'only first original text texture released');result=dict(count=resource['release_count']);value=result['count']
  self.api_calls.append(dict(kind='recorded_replaced_text_GPU',target=at,slot=slot,index=i,sp=sp,return_va=ret,pop=pop,args=args,value=value,result=result,source=resource['source'],new_mappings=[],memory_outputs=outputs));self.existing_gpu_count+=1;self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def captured(self,capture):
  raw=bytes.fromhex(capture['raw_device_hex']);need(len(raw)==256,'source capture full device extent');before=self.read(KEYBOARD,0xa00);bound=bytearray(before);bound[12:268]=raw;self.u.mem_write(KEYBOARD+12,raw);self.memory_evidence.mark(KEYBOARD+12,256);bp=STACK+0x800;self.u.mem_write(bp-4,struct.pack('<I',KEYBOARD));self.memory_evidence.mark(bp-4,4)
  for k,v in dict(EIP=0x4113d5,EBP=bp,ESP=bp-0x70,EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  step=self.advance_new('captured_fourth_'+capture['label'],0x4116a4);after=self.read(KEYBOARD,0xa00);need(after==base.predict_keyboard(bytes(bound)),'independent whole original keyboard processing');return dict(capture=copy.deepcopy(capture),binding=dict(pointer=KEYBOARD+12,bytes=256),fragment=dict(va=0x4113d5,bp=bp,sp=bp-0x70,receiver_slot=bp-4,receiver=KEYBOARD,stop=0x4116a4),before_hex=before.hex(),bound_hex=bytes(bound).hex(),after_hex=after.hex(),step=step,state=state(self))
 def confirmation_frame(self,label,stop=RETURN):
  steps=[self.new_root(label+'_request',0x425de0,previous.parent.INPUT),self.new_root(label+'_queue_a',0x40db90,previous.parent.MANAGER),self.new_root(label+'_queue_b',0x40dc80,previous.parent.MANAGER)];root=dict(va=0x454cf0,receiver=previous.parent.TACT,args=[],sp=STACK,return_va=RETURN);steps.append(self.advance_new(label+'_complete_task',stop,root));result=dict(label=label,steps=steps,state=state(self));print(label,result['state'],flush=True);return result
 def continue_confirmation(self,scene):
  contract=contracts();stream=contract['streams'][str(scene)];before=state(self);need((before['PC'],before['wait'],before['opcode'])==(290,0,50),'natural third readiness before confirmation');bindings=[self.captured(stream['captures'][0])];enter=self.confirmation_frame('third_enter_confirmation');controls=[self.confirmation_frame('third_no_input_'+str(i)) for i in range(2)];need(all((f['state']['PC'],f['state']['wait'],f['state']['opcode'],f['state']['space_current'])==(294,1,51,0) for f in [enter,*controls]),'held complete original confirmation without input');bindings.append(self.captured(stream['captures'][1]));confirmed=self.confirmation_frame('third_captured_press');need((confirmed['state']['PC'],confirmed['state']['wait'],confirmed['state']['opcode'],confirmed['state']['space_current'])==(294,0,51,128),'original task consumes captured space press bit while retaining down bit');bindings.append(self.captured(stream['captures'][2]));need(state(self)['space_current']==0,'captured release through source keyboard');activation=self.confirmation_frame('fourth_activate_layer');clearing=self.confirmation_frame('fourth_clear_layer');need((activation['state']['PC'],activation['state']['selected_layer'],clearing['state']['PC'])==(302,7,306),'config4 selects original layer7 and clears text');font_target=word(self.read(previous.parent.FONT_SLOT));prefix=self.confirmation_frame('fourth_text_prefix',font_target);sp=self.cpu()['ESP'];font=dict(target=font_target,import_slot=previous.parent.FONT_SLOT,args=[word(self.read(sp+4+i*4)) for i in range(14)],return_va=word(self.read(sp)),frames=chain(self,[('font',0x4c4d04),('text',0x4cec2b),('vm',0x454d90),('task',RETURN)]),cpu=self.cpu(),first_instruction_executed=False);need(font['return_va']==0x4cad09 and (prefix['state']['PC'],prefix['state']['opcode'])==(306,17),'natural fourth font ABI and partial task');self.existing_resource=existing_texture(self.confirm_branch);self.existing_gpu_count=0;old_identity=self.existing_resource['texture'];need(word(self.read(TEXTURE+44))==old_identity['pointer'] and word(self.read(old_identity['pointer']))==old_identity['vtable'],'retained first text identity matches pinned R2 owner');self.third_methods.update(old_identity['methods'][str(k)] for k in (8,56));existing_record=self.read(TEXTURE,84).hex();account_before=word(self.read(0x765720));old_service=self.offscreen;service=Offscreen(word(self.read(self.renderer+0xb208)));out=None
  try:
   self.offscreen=service;self.fourth_running=True;raster_step=self.advance_new('continuous_original_fourth_font_raster',previous.FONT_STOP);raw=service.gdi.raster(service.bitmap);sp=self.cpu()['ESP'];pending=dict(va=previous.FONT_STOP,receiver=self.cpu()['ECX'],args=[word(self.read(sp+4)),word(self.read(sp+8))],return_va=word(self.read(sp)),cpu=self.cpu(),frames=chain(self,[('raster',0x408e81),('texture_wrapper',0x4cad7c),('font',0x4c4d04),('text',0x4cec2b),('vm',0x454d90),('task',RETURN)]),first_instruction_executed=False);need(pending['receiver']==TEXTURE and pending['return_va']==0x405779 and pending['args']==[self.device,0],'natural fourth texture input and full original task stack');need(self.existing_gpu_count==2 and word(self.read(0x765720))==account_before-self.existing_resource['bytes'] and word(self.read(TEXTURE+44))==0,'original old first-text destruction and actual counter decrease');self.replaced_texture_bytes=self.existing_resource['bytes'];memory=base.memory_rows(self.u);need(memory==raster_step['full_memory'],'fresh full byte rehash agrees with source writes and GDI outputs');out=dict(contract=contract,before=before,stream=stream,bindings=bindings,enter=enter,controls=controls,confirmed=confirmed,activation=activation,clearing=clearing,prefix=prefix,pending_font=font,raster_step=raster_step,raster=dict(ACP=service.gdi.acp,measured=service.measured,selected_face=service.face,font=service.font,bitmap=service.bitmap,raster_dc=service.raster_dc,logical_measurement_dc=service.logical,fresh_owned_measurement_dc=service.actual,stages=copy.deepcopy(service.stages),raster_hex=raw.hex(),raster_sha256=sha(raw)),pending_texture=pending,final=state(self),fourth_object_hex=self.read(OBJECT,previous.rules.BYTES).hex(),fourth_node_hex=self.read(NODE,224).hex(),final_memory=memory,final_architectural_cpu=base.architectural_cpu(self.u),derived_input_host_writes=0,PC_or_wait_host_writes=0,new_VM_roots=0,texture_create_executed=False,fourth_task_completed=False)
   out.update(existing_resource=self.existing_resource,existing_record_before=existing_record,replaced_texture_bytes=self.replaced_texture_bytes,accounting_before=account_before,accounting_after=word(self.read(0x765720)))
  finally:
   self.fourth_running=False;self.offscreen=old_service;cleanup=service.close()
  out['supplemental_GDI_cleanup']=cleanup;return out

def run_case(helper,build,name,scene):
 captured=[];instances=[]
 class Attached(Guest):
  def __init__(self,*args):super().__init__(*args);self.confirm_branch=name;instances.append(self)
  def new_root(self,label,va,recv):
   if label=='supplemental_original_third_texture_destructor':captured.append(self.continue_confirmation(scene))
   return super().new_root(label,va,recv)
 char_run=adapt_validation(previous.parent.run_case,[("word(g.read(0x765720))==accounting","word(g.read(0x765720))==accounting-getattr(g,'replaced_texture_bytes',0)")]);parent_proxy=types.SimpleNamespace(**dict(vars(previous.parent),run_case=char_run));call=types.FunctionType(previous.run_case.__code__,dict(previous.run_case.__globals__,Guest=Attached,parent=parent_proxy),'original_third_with_confirmation_before_cleanup')
 try:c=call(helper,build,name,scene)
 except BaseException as exc:
  if instances:
   g=instances[0];out=ROOT/('analysis/school-retained-third-confirmation-failed-run-'+helper.stem+'-'+name+'-'+str(scene)+'-20261023.json.gz');need(not out.exists(),'preserve immutable failure trace');failure=dict(accepted=False,error=repr(exc),state=state(g),native_trace=g.live.trace,helper_closed=g.live.closed,helper_returncode=g.live.process.returncode,helper_cleanup=g.live.cleanup,allocations=g.allocations);out.write_bytes(gzip.compress(json.dumps(failure,separators=(',',':')).encode(),mtime=0))
  raise
 need(len(captured)==1,'one source confirmation in original resource lifetime');c['third_confirmation']=captured[0];return c

def run(helper,build):return dict(schema_version=1,contract=contracts(),cases=[run_case(helper,build,n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],new_forward_VM_roots=0,game_function_substitutions=0,IAT_rebindings=0,new_OS_input=False,new_window=False,new_GPU=False,original_outer_scheduler=False,historical_heap_restored=False,fourth_font_created=True,fourth_texture_created=False,fourth_task_completed=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report')
 helper,build=previous.parent.parent.old.init.platform.build(ROOT/a.helper);r=run(helper,build);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('six captured third confirmations and fourth glyph handoffs',flush=True)
