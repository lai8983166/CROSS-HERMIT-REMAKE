"""Independent captured-key confirmation, fourth glyphs and old texture retirement."""
import copy,gzip,hashlib,json,struct,types
from collections import Counter
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_third_confirmation as work
from tools import school_retained_third_dialogue_verification as previous
from tools.school_font_raster_catalog import geometry
from tools.school_gdi_platform import WindowsGDI

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;sha=work.sha;canonical=work.canonical
GDI_WORK=types.SimpleNamespace(**dict(vars(work.previous),RASTER=work.RASTER))

def ordered(e):
 return [e['bindings'][0]['step'],*e['enter']['steps'],*[s for f in e['controls'] for s in f['steps']],e['bindings'][1]['step'],*e['confirmed']['steps'],e['bindings'][2]['step'],*e['activation']['steps'],*e['clearing']['steps'],*e['prefix']['steps'],e['raster_step']]

def protocol(c):
 previous.protocol(c);e=c['third_confirmation'];contract=work.contracts();stream=contract['streams'][str(c['scene_capture'])];need(e['contract']==contract and e['stream']==stream,'all source captures and command identities pinned');need(e['derived_input_host_writes']==e['PC_or_wait_host_writes']==e['new_VM_roots']==0 and e['texture_create_executed']is e['fourth_task_completed']is False,'no derived input/PC/wait or new VM roots; honest fourth boundary');need((e['before']['PC'],e['before']['wait'],e['before']['opcode'])==(290,0,50),'source-ready third parent');need(len(e['bindings'])==3 and [b['capture'] for b in e['bindings']]==stream['captures'],'idle press release in exact original capture order')
 for b in e['bindings']:
  need(b['binding']==dict(pointer=work.KEYBOARD+12,bytes=256) and b['fragment']==dict(va=0x4113d5,bp=work.STACK+0x800,sp=work.STACK+0x800-0x70,receiver_slot=work.STACK+0x800-4,receiver=work.KEYBOARD,stop=0x4116a4) and b['step']['root']is None and b['step']['result']['boundary']==0x4116a4,'only source raw-device bytes and declared original keyboard fragment')
  old=bytes.fromhex(b['before_hex']);bound=bytearray(old);bound[12:268]=bytes.fromhex(b['capture']['raw_device_hex']);need(len(old)==0xa00 and bytes(bound).hex()==b['bound_hex'] and base.predict_keyboard(bytes(bound)).hex()==b['after_hex'],'full A00h keyboard binding and independently derived bytes')
 need([b['state']['space_current'] for b in e['bindings']]==[0,128,0],'source normalization stores high down bit, not boolean 1');need(len(e['controls'])==2,'two held no-input control tasks')
 for f in [e['enter'],*e['controls']]:need((f['state']['PC'],f['state']['wait'],f['state']['opcode'],f['state']['space_current'])==(294,1,51,0),'confirmation held without input')
 need((e['confirmed']['state']['PC'],e['confirmed']['state']['wait'],e['confirmed']['state']['opcode'],e['confirmed']['state']['space_current'])==(294,0,51,128),'captured down bit satisfies original read-only key query');need((e['activation']['state']['PC'],e['activation']['state']['selected_layer'],e['activation']['state']['opcode'],e['clearing']['state']['PC'],e['clearing']['state']['opcode'],e['clearing']['state']['fourth_text_count'])==(302,7,43,306,44,0),'config4 selects layer7, original activation and clear');need((e['prefix']['state']['PC'],e['prefix']['state']['opcode'],e['final']['PC'],e['final']['opcode'],e['final']['selected_layer'])==(306,17,306,17,7),'original fourth text prefix')
 for f in [e['enter'],*e['controls'],e['confirmed'],e['activation'],e['clearing'],e['prefix']]:
  need(len(f['steps'])==4,'four complete request/reset/task intervals')
  for s,va,recv in zip(f['steps'],(0x425de0,0x40db90,0x40dc80,0x454cf0),(work.previous.parent.INPUT,work.previous.parent.MANAGER,work.previous.parent.MANAGER,work.previous.parent.TACT)):previous.previous.root_check(s,va,recv)
 need(e['raster_step']['root']is None and e['raster_step']['result']['boundary']==0x403bd0 and e['pending_texture']['first_instruction_executed']is False,'continuous original fourth raster to unexecuted texture');need(e['pending_font']['first_instruction_executed']is False and e['pending_font']['return_va']==0x4cad09,'natural font entry snapshot');need(e['supplemental_GDI_cleanup']==dict(fonts=1,bitmaps=1,dcs=2,all_resources_released=True),'explicit supplemental pending fourth GDI ownership cleanup');need(e['existing_resource']==work.existing_texture(c['name']) and e['replaced_texture_bytes']==16384 and e['accounting_before']-e['accounting_after']==16384,'legitimate old first-text release and original byte accounting decrease')
 need(len(ordered(e))==32 and all('queue' in s and 'full_memory' in s and 'architectural_cpu' in s for s in ordered(e)),'all source intervals, original queues and complete state');need([a['kind'] for a in e['raster_step']['result']['api_calls']].count('actual_owned_fourth_GDI')==23 and [a['slot'] for a in e['raster_step']['result']['api_calls'] if a['kind']=='recorded_replaced_text_GPU']==[56,8],'23 fresh fourth GDI/string calls and exact old descriptor/release')

def reproduce_pixels(c):
 e=c['third_confirmation'];o=e['raster'];raw=bytes.fromhex(work.contracts()['fourth_text']['hex']);args=e['pending_font']['args'];image=base.SOURCE.read_bytes();face=image[args[-1]-base.BASE:];face=face[:face.index(0)];gd=WindowsGDI()
 try:
  dc=gd.dc();font=gd.font(args[:-1],face);gd.select(dc,font);measured,selected=gd.measure(dc,raw);need((gd.acp,measured,selected)==(o['ACP'],o['measured'],o['selected_face']),'independent fourth ANSI metrics/face');cfg=geometry(measured);bm=gd.dib(dc,bytes.fromhex(cfg['header_hex']));gd.select(dc,bm);gd.select(dc,gd.handle(gd.g.GetStockObject(4)));w,h=cfg['raster_size'];p=cfg['padding']
  for name,a in [('SetMapMode',[dc,1]),('PatBlt',[dc,0,0,w,h,0xf00021]),('SetBkMode',[dc,1]),('SetBkColor',[dc,0]),('SetTextAlign',[dc,0])]:
   v=int(getattr(gd.g,name)(*a));need(v!=0xffffffff and (name not in ('SetMapMode','PatBlt','SetBkMode') or v!=0),'fresh independent fourth GDI state')
  stages=[gd.raster(bm)]
  for color,xy in [(0x080808,[2*p,2*p]),(0xffffff,[p,p])]:need(int(gd.g.SetTextColor(dc,color))!=0xffffffff and int(gd.g.TextOutA(dc,*xy,raw,len(raw)))==1,'fresh independent fourth glyph output');stages.append(gd.raster(bm))
 finally:cleanup=gd.close()
 need(cleanup==dict(fonts=1,bitmaps=1,dcs=1,all_resources_released=True) and [x.hex() for x in stages]==[x['hex'] for x in o['stages']] and stages[-1].hex()==o['raster_hex'] and sha(stages[-1])==o['raster_sha256'],'all three independent fresh pixel stages and ownership');return dict(raw=raw,face=face,cfg=cfg,stages=stages)

def frames(r,expected):
 rows=[];bp=r.cpu()['EBP']
 for label,ret in expected:need(word(r.read(bp+4))==ret,'original '+label+' frame');rows.append(dict(label=label,bp=bp,return_va=ret));bp=word(r.read(bp))
 return rows

class Replay(previous.Replay):
 extension=work.adapt_validation(previous.Replay.extension,[("word(self.read(0x765720))==e['accounting_before']==before-32768","word(self.read(0x765720))==e['accounting_before']-self.replaced_texture_bytes and e['accounting_before']==before-32768")])
 fourth_gdi=types.FunctionType(previous.Replay.gdi.__code__,dict(previous.Replay.gdi.__globals__,work=GDI_WORK),'independent_original_fourth_GDI')
 def replay_new(self,s):
  if s['label']=='supplemental_original_third_texture_destructor':
   self.confirmation_extension();self.region_hashes.clear()
  return super().replay_new(s)
 def next_gdi(self,a):
  old=(self.third_case,self.reference,self.case);self.third_case=self.confirmation_case;self.reference=self.fourth_reference;self.case=dict(self.case,pending_font=self.confirmation_case['pending_font'])
  try:return self.fourth_gdi(a)
  finally:self.third_case,self.reference,self.case=old
 def existing_gpu(self,a):
  e=self.confirmation_case;resource=work.existing_texture(self.case['name']);i=self.existing_gpu_count;need(i in (0,1) and a['index']==i,'two ordered old first-text interfaces');t=resource['texture'];slot=(56,8)[i];pop=(12,4)[i];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];need(a['target']==t['methods'][str(slot)] and a['slot']==slot and a['pop']==pop and a['sp']==sp and a['return_va']==ret==(0x403a44,0x40378d)[i] and a['args']==args and a['source']==resource['source'],'original existing texture method/object/full ABI');out=[]
  if i==0:need(args==[t['pointer'],0,self.cpu()['EBP']-36],'old original descriptor output');result=copy.deepcopy(resource['descriptor']['result']);value=result['hr'];out=[dict(pointer=args[2],hex=result['hex'])]
  else:need(args==[t['pointer']],'old original Release only this object');result=dict(count=resource['release_count']);value=result['count']
  need(a['new_mappings']==[] and a['memory_outputs']==out and a['result']==result and a['value']==value,'exact historical existing texture responses');self.apply_outputs(a);self.api_return(value,pop,ret,sp);self.existing_gpu_count+=1
 def next_step(self,s):
  maps=[]
  for slot in work.previous.IMPORTS:
   at=word(self.read(slot))
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  need(maps==s['entry_mappings'],'only missing source platform pages');a=s['result'];root=s['root']
  if root:
   self.u.mem_write(root['sp'],struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']))
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  need(self.cpu()==a['before_cpu'],'all original source registers before continuation');calls=iter(a['api_calls']);next_api=next(calls,None);ih=hashlib.sha256();wh=hashlib.sha256();counts=Counter();writes=0;display=[]
  def code(u,at,n,_):
   nonlocal next_api
   if at==a['boundary']:u.emu_stop();return
   if next_api and at==next_api['target']:
    q=dict(next_api,va=next_api['target'],key='next_source_platform');kind=q['kind'];need(kind in ('actual_owned_fourth_GDI','recorded_replaced_text_GPU','recorded_task_platform'),'no game or CRT substitutes')
    if kind=='actual_owned_fourth_GDI':self.next_gdi(q)
    elif kind=='recorded_replaced_text_GPU':self.existing_gpu(q)
    else:self.api(q)
    next_api=next(calls,None);return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'every fourth original instruction byte');counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
   if at in work.previous.DISPLAY:sp=self.cpu()['ESP'];display.append(dict(va=at,receiver=self.cpu()['ECX'],return_va=word(self.read(sp))))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no code patch')
   if s['label'].startswith('captured_'):need(work.KEYBOARD<=at and at+n<=work.KEYBOARD+0xa00 or 0x21000000<=at and at+n<=0x21010000,'keyboard source finite writes')
   writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  ch=self.u.hook_add(UC_HOOK_CODE,code);wr=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.ctl_remove_cache(a['before_cpu']['EIP'],a['before_cpu']['EIP']+1);self.u.emu_start(a['before_cpu']['EIP'],0,count=2000000,timeout=120000000)
  finally:self.u.hook_del(ch);self.u.hook_del(wr)
  need(next_api is None and self.cpu()==a['cpu'] and ih.hexdigest()==a['instruction_sha256'] and [dict(va=p,count=n) for p,n in sorted(counts.items())]==a['instruction_counts'],'all new source instructions, APIs and natural CPU boundary');need(writes==a['writes'] and wh.hexdigest()==a['write_sha256'] and display==s['display_calls'] and s['conversions']==[],'all original writes and display calls');need(base.memory_rows(self.u)==s['full_memory'] and canonical(base.architectural_cpu(self.u))==canonical(s['architectural_cpu']),'fresh complete all-memory and CPU comparison after every new interval');need(work.previous.text_state(self)==s['state'] and work.previous.parent.parent.old.init.old.ledger(self)==s['ledger'],'original state and CRT accounting');b=self.read(work.previous.parent.MANAGER,96);head=word(b,16);arena=word(b,20);end=word(b,48);need(word(b,8)==4096 and word(b,12)==1048576 and arena<=end<=arena+1048576,'bounded original draw queue');need(s['queue']==dict(manager_hex=b.hex(),head_pointer=head,head_hex=self.read(head,32768).hex(),arena_pointer=arena,used_bytes=end-arena,arena_hex=self.read(arena,end-arena).hex()),'all original queue heads and live arena bytes');return sum(counts.values())
 def capture_step(self,b):
  need(self.read(work.KEYBOARD,0xa00).hex()==b['before_hex'],'source keyboard before binding');self.u.mem_write(work.KEYBOARD+12,bytes.fromhex(b['capture']['raw_device_hex']));f=b['fragment'];self.u.mem_write(f['receiver_slot'],struct.pack('<I',work.KEYBOARD))
  for k,v in dict(EIP=f['va'],EBP=f['bp'],ESP=f['sp'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  n=self.next_step(b['step']);need(self.read(work.KEYBOARD,0xa00).hex()==b['after_hex'] and work.state(self)==b['state'],'whole independently predicted source keyboard and derived state');return n
 def next_frame(self,f,partial=False):
  count=0
  for i,s in enumerate(f['steps']):
   count+=self.next_step(s)
   if not partial or i<3:need(self.cpu()['EIP']==work.RETURN and self.cpu()['ESP']==work.STACK+4,'complete original request/reset/task natural return')
  need(work.state(self)==f['state'],'each original confirmation/control state');return count
 def confirmation_extension(self):
  e=self.case['third_confirmation'];self.confirmation_case=e;self.fourth_reference=reproduce_pixels(self.case);self.existing_gpu_count=0;need(work.state(self)==e['before'],'actual source confirmation entry');count=self.capture_step(e['bindings'][0]);count+=self.next_frame(e['enter'])
  for f in e['controls']:count+=self.next_frame(f)
  count+=self.capture_step(e['bindings'][1]);count+=self.next_frame(e['confirmed']);count+=self.capture_step(e['bindings'][2]);count+=self.next_frame(e['activation']);count+=self.next_frame(e['clearing']);count+=self.next_frame(e['prefix'],True);sp=self.cpu()['ESP'];font=dict(target=word(self.read(work.previous.parent.FONT_SLOT)),import_slot=work.previous.parent.FONT_SLOT,args=[word(self.read(sp+4+i*4)) for i in range(14)],return_va=word(self.read(sp)),frames=frames(self,[('font',0x4c4d04),('text',0x4cec2b),('vm',0x454d90),('task',work.RETURN)]),cpu=self.cpu(),first_instruction_executed=False);need(font==e['pending_font'] and self.cpu()['EIP']==font['target'],'original fourth font ABI and four task frames');resource=work.existing_texture(self.case['name']);t=resource['texture'];need(word(self.read(work.TEXTURE+44))==t['pointer'] and word(self.read(t['pointer']))==t['vtable'] and self.read(work.TEXTURE,84).hex()==e['existing_record_before'] and word(self.read(0x765720))==e['accounting_before'],'retained R2 texture and original accounting source');count+=self.next_step(e['raster_step']);sp=self.cpu()['ESP'];pending=dict(va=0x403bd0,receiver=self.cpu()['ECX'],args=[word(self.read(sp+4)),word(self.read(sp+8))],return_va=word(self.read(sp)),cpu=self.cpu(),frames=frames(self,[('raster',0x408e81),('texture_wrapper',0x4cad7c),('font',0x4c4d04),('text',0x4cec2b),('vm',0x454d90),('task',work.RETURN)]),first_instruction_executed=False);need(pending==e['pending_texture'] and pending['receiver']==work.TEXTURE and pending['args']==[self.device,0] and pending['return_va']==0x405779 and self.cpu()['EIP']==0x403bd0,'natural fourth texture ABI and six original frames');need(self.existing_gpu_count==2 and word(self.read(0x765720))==e['accounting_after']==e['accounting_before']-16384 and word(self.read(work.TEXTURE+44))==0,'original existing first texture free and exact accounting delta');self.replaced_texture_bytes=16384
  need(work.state(self)==e['final'] and self.read(work.OBJECT,work.previous.rules.BYTES).hex()==e['fourth_object_hex'] and self.read(work.NODE,224).hex()==e['fourth_node_hex'] and base.memory_rows(self.u)==e['final_memory']==e['raster_step']['full_memory'] and canonical(base.architectural_cpu(self.u))==canonical(e['final_architectural_cpu']),'all final original bytes, object, node, CPU and queue boundary');need(self.read(work.RASTER,len(self.fourth_reference['stages'][-1]))==self.fourth_reference['stages'][-1],'whole actual fourth glyph pixels');writes=sum(s['result']['writes'] for s in ordered(e));need((count,writes)==(338281,164822),'all new source instruction and write totals');self.confirmation_proof=dict(new_original_instructions=count,new_original_writes=writes,new_source_intervals=32,complete_original_tasks=6,partial_original_tasks=1,captured_keyboard_fragments=3,no_input_controls=2,confirmation_PC=294,confirmation_wait_after_press=0,final_PC=306,final_opcode=17,selected_layer=7,old_original_texture_bytes_freed=16384,old_original_descriptor_and_release_verified=True,independent_fresh_GDI_pixels_verified=True,complete_memory_and_CPU_verified=True,full_queue_verified=True,natural_stack_layers=6,fourth_texture_created=False,fourth_task_completed=False,new_OS_input=False,new_GPU=False)

def verify_case(c,boundary_observer=None):
 protocol(c);char=previous.previous;char_verify=work.adapt_validation(char.verify_case,[("word(r.read(0x765720))==c['accounting_before']","word(r.read(0x765720))==c['accounting_before']-getattr(r,'replaced_texture_bytes',0)")]);char_proxy=types.SimpleNamespace(**dict(vars(char),verify_case=char_verify));observed=[]
 class Observed(Replay):
  def confirmation_extension(self):
   if boundary_observer is not None:boundary_observer(self)
   super().confirmation_extension();observed.append(self.confirmation_proof)
 call=types.FunctionType(previous.verify_case.__code__,dict(previous.verify_case.__globals__,Replay=Observed,previous=char_proxy),'verify_all_original_stages_with_source_texture_retirement');parent=call(c);need(len(observed)==1,'single independently verified confirmation continuation');return dict(name=c['name'],scene_capture=c['scene_capture'],parent=parent,confirmation=observed[0])

def verify(r):
 need(r['schema_version']==1 and r['contract']==work.contracts() and r['new_forward_VM_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0,'source/capture identities and no substitutes')
 for k in ('new_OS_input','new_window','new_GPU','original_outer_scheduler','historical_heap_restored','fourth_texture_created','fourth_task_completed','R3_complete','R6_complete'):need(r[k]is False,'honest scope '+k)
 need(r['fourth_font_created']is True,'actual owned fourth font');need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six original branches');proofs=[]
 for c in r['cases']:
  proofs.append(verify_case(c));print('independent confirmation verified',c['name'],c['scene_capture'],flush=True)
 return dict(schema_version=1,cases=proofs,six_captured_third_confirmations_and_fourth_rasters_verified=True,new_OS_input=False,new_GPU=False,interactive_desktop_required=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 raw=(ROOT/a.report).read_bytes();r=verify(json.loads(gzip.decompress(raw)));r['source_report_sha256']=sha(raw);out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six source confirmations and fourth rasters independently verified',flush=True)
