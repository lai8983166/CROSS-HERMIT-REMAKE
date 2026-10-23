"""Independent third dialogue instructions, GDI pixels and source-owned cleanup."""
import bisect,copy,gzip,json,struct,types,hashlib
from collections import Counter
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_third_dialogue as work
from tools import school_retained_character_task_verification as previous
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_second_live_text_catalog import bands
from tools.school_gdi_platform import WindowsGDI

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;sha=work.sha;canonical=work.canonical

def reproduce_pixels(c):
 e=c['third_dialogue'];o=e['raster'];raw=bytes.fromhex(work.rules.source_rules()['text']['hex']);args=c['pending_font']['args'];image=base.SOURCE.read_bytes();face=image[args[-1]-base.BASE:];face=face[:face.index(0)];gd=WindowsGDI()
 try:
  dc=gd.dc();font=gd.font(args[:-1],face);gd.select(dc,font);measured,selected=gd.measure(dc,raw);need((gd.acp,measured,selected)==(o['ACP'],o['measured'],o['selected_face']),'independent actual third glyph metrics/face/ACP');cfg=geometry(measured);bm=gd.dib(dc,bytes.fromhex(cfg['header_hex']));gd.select(dc,bm);gd.select(dc,gd.handle(gd.g.GetStockObject(4)));w,h=cfg['raster_size'];p=cfg['padding']
  for name,a in [('SetMapMode',[dc,1]),('PatBlt',[dc,0,0,w,h,0xf00021]),('SetBkMode',[dc,1]),('SetBkColor',[dc,0]),('SetTextAlign',[dc,0])]:
   value=int(getattr(gd.g,name)(*a));need(value!=0xffffffff and (name not in ('SetMapMode','PatBlt','SetBkMode') or value!=0),'actual independent GDI setup')
  stages=[gd.raster(bm)]
  for color,xy in [(0x080808,[2*p,2*p]),(0xffffff,[p,p])]:
   need(int(gd.g.SetTextColor(dc,color))!=0xffffffff and int(gd.g.TextOutA(dc,*xy,raw,len(raw)))==1,'actual independent third glyph draw');stages.append(gd.raster(bm))
 finally:cleanup=gd.close()
 need(cleanup==dict(fonts=1,bitmaps=1,dcs=1,all_resources_released=True),'independent fresh glyph resources closed');need([b.hex() for b in stages]==[s['hex'] for s in o['stages']] and stages[-1].hex()==o['raster_hex'] and sha(stages[-1])==o['raster_sha256'],'all three independently redrawn original third glyph stages');return dict(raw=raw,face=face,cfg=cfg,stages=stages)

def protocol(c):
 previous.protocol(c);e=c['third_dialogue'];need(e['contract']==work.contracts()[2] and e['retained_input_host_writes']==e['new_VM_roots']==0,'pinned historical platform and no input/VM substitution');need(e['raster_step']['root']is e['completion']['root']is None and e['raster_step']['result']['boundary']==work.FONT_STOP and e['completion']['result']['boundary']==work.RETURN,'continuous original font/texture/task stack');need(e['entry']['cpu']==c['third'][-1]['result']['cpu'] and e['entry']['font_args']==c['pending_font']['args'],'original unmodified third font CPU and arguments');need(e['source_GPU_calls']==6 and e['offscreen_cleanup']==dict(fonts=0,bitmaps=0,dcs=1,all_resources_released=True),'original font/bitmap/raster DC deletion and supplemental owned measurement DC cleanup');need(e['completed']['animation']['pc']==286 and e['final']['animation']['pc']==290 and e['final']['animation']['wait']==0,'original third handler and readiness before next confirmation');need(e['frames'] and [f['index'] for f in e['frames']]==list(range(len(e['frames']))) and all(len(f['steps'])==4 for f in e['frames']),'complete bounded original task updates')
 need(len(e['frames'])==26 and e['before']['input_words']==e['entry']['input_words']==[0,0,0],'26 original readiness updates with preserved zero input, no isolated reset')
 for f in e['frames']:
  i=f['index'];a=f['state']['animation'];need(a['wait']==int(i<25) and a['pc']==290 and a['instruction_count']==(3 if i==0 else 0) and a['waiting_count']==i and f['state']['input_words']==[0,0,0],'exact original no-input readiness boundary')
  counts={r['va']:r['count'] for r in f['steps'][-1]['result']['instruction_counts']};need([counts.get(at,0) for at in (0x4cb5f0,0x4d5ec0,0x4128f0,0x4c5260)]==([0,0,0,1] if i==0 else [10,1,1,0]),'all ten source readiness predicates and real mouse/keyboard query bodies')
  for s,va,recv in zip(f['steps'],(0x425de0,0x40db90,0x40dc80,0x454cf0),(work.parent.INPUT,work.parent.MANAGER,work.parent.MANAGER,work.parent.TACT)):previous.root_check(s,va,recv)
 need(e['cleanup']['root']==dict(va=0x403730,receiver=work.TEXTURE,args=[],sp=work.STACK,return_va=work.RETURN),'explicit original third texture destruction')
 for s in [e['raster_step'],e['completion'],*[s for f in e['frames'] for s in f['steps']],e['cleanup']]:need('queue' in s and 'full_memory' in s and 'architectural_cpu' in s,'complete original queue, CPU and memory evidence')

class Replay(previous.Replay):
 def gdi(self,a):
  e=self.third_case;o=e['raster'];sp=self.cpu()['ESP'];ret=word(self.read(sp));slot=a['import_slot'];name,caller,pop=work.GDI[slot];args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];bp=self.cpu()['EBP'];out=[];maps=[];translated=list(args);cfg=self.reference['cfg'];raw=self.reference['raw'];local=self.case['pending_font']['frames'][0]['bp']-0x110
  need(a['name']==name and a['pop']==pop and a['sp']==sp and a['return_va']==ret and a['args']==args and a['target']==word(self.read(slot)),'independent original GDI IAT and full source ABI')
  if caller is not None:need(ret==caller,'exact original third GDI caller')
  if name not in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject','DeleteObject','DeleteDC'):
   need(args[0] in (o['logical_measurement_dc'],o['raster_dc']),'only reconstructed measurement or owned raster DC')
   if args[0]==o['logical_measurement_dc']:translated[0]=o['fresh_owned_measurement_dc']
  need(translated==a['dc_translated_args'],'historical measurement DC never sent to Windows')
  def put(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if name=='CreateFontA':need(args==self.case['pending_font']['args'] and work.raster.text(self,args[-1])==self.reference['face'] and a['face_hex']==self.reference['face'].hex() and a['result']==o['font'],'original font and raw ANSI face')
  elif name=='lstrlenA':need(ret in (0x4051ba,0x405230,0x405676,0x4056c7) and args==[local] and self.read(local,len(raw)+1)==raw+bytes(1) and a['result']==len(raw),'original full third text length')
  elif name=='SelectObject':
   choices={0x4051ea:[o['logical_measurement_dc'],o['font']],0x40528a:[o['logical_measurement_dc'],getattr(self,'old_font',0)],0x40541b:[o['raster_dc'],o['bitmap']],0x405485:[o['raster_dc'],getattr(self,'brush',0)],0x4054c6:[o['raster_dc'],o['font']],0x4058d8:[o['raster_dc'],getattr(self,'old_bitmap',0)]};need(ret in choices and args==choices[ret] and 0<a['result']<0xffffffff,'original fresh/stock object selections')
   if ret==0x4051ea:self.old_font=a['result']
   if ret==0x40541b:self.old_bitmap=a['result']
   if ret==0x4058d8:need(a['result']==o['bitmap'],'original bitmap restoration')
  elif name=='GetTextExtentPoint32A':need(args==[o['logical_measurement_dc'],local,len(raw),bp-0x54] and a['measured']==o['measured'] and a['selected_face']==o['selected_face'] and a['text_hex']==raw.hex() and a['result']==1,'actual original measurement');put(args[3],struct.pack('<2i',*o['measured']))
  elif name=='CreateCompatibleDC':need(args==[0] and a['result']==o['raster_dc'],'new owned raster DC')
  elif name=='CreateDIBSection':
   header=bytes.fromhex(cfg['header_hex']);size=len(self.reference['stages'][-1]);extent=(size+4095)&~4095;need(args==[o['raster_dc'],bp-0x38,0,bp-0x3c,0,0] and self.read(args[1],40)==header and a['header_hex']==header.hex() and a['guest_bits']==work.RASTER and a['mapped_bytes']==extent and a['bitmap_bytes']==size and a['native_bits']>0 and a['result']==o['bitmap'],'original complete DIB and bounded owned bits');maps=[dict(pointer=work.RASTER,bytes=extent)];put(args[3],struct.pack('<I',work.RASTER))
  elif name=='GetStockObject':need(args==[4] and 0<a['result']<0xffffffff,'original stock black brush');self.brush=a['result']
  elif name=='TextOutA':
   i=1 if ret==0x40569c else 2;p=cfg['padding'];xy=[2*p,2*p] if i==1 else [p,p];need(ret in (0x40569c,0x4056e7) and args==[o['raster_dc'],*xy,local,len(raw)] and a['text_hex']==raw.hex() and a['result']==1,'original shadow and foreground text output');put(work.RASTER,self.reference['stages'][i])
  elif name=='DeleteObject':need(ret in (0x405921,0x4d1c1b) and args==[o['bitmap'] if ret==0x405921 else o['font']] and a['result']==1,'original bitmap/font deletion')
  elif name=='DeleteDC':need(ret==0x40596a and args==[o['raster_dc']] and a['result']==1,'original raster DC deletion')
  else:
   w,h=cfg['raster_size'];choices={'SetMapMode':([o['raster_dc'],1],1),'PatBlt':([o['raster_dc'],0,0,w,h,0xf00021],1),'SetBkMode':([o['raster_dc'],1],2),'SetBkColor':([o['raster_dc'],0],0xffffff),'SetTextAlign':([o['raster_dc'],0],0),'SetTextColor':([o['raster_dc'],0x80808 if ret==0x405663 else 0xffffff],0 if ret==0x405663 else 0x80808)};need(name in choices and (args,a['result'])==choices[name],'all original GDI state inputs and default-state returns')
   if name=='PatBlt':put(work.RASTER,self.reference['stages'][0])
  need(a['memory_outputs']==out and a['new_mappings']==maps,'all and only independent GDI memory outputs')
  self.apply_outputs(a);self.api_return(a['result'],pop,ret,sp)
 def api_return(self,value,pop,ret,sp):
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def apply_outputs(self,a):
  for m in a['new_mappings']:
   p=m['pointer'];n=m['bytes'];need(all(not(lo<p+n and p<=hi) for lo,hi,_ in self.u.mem_regions()),'fresh independent third platform mappings');self.u.mem_map(p,n)
  for o in a['memory_outputs']:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
 def third_gpu(self,a):
  i=self.third_gpu_count;n,release,_=work.contracts();t=self.third_texture;need(0<=i<6 and a['index']==i,'ordered bounded third texture responses');slot=[80,56,64,68,56,8][i];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];target=self.device_method if i==0 else t['methods'][str(slot)];need(a['target']==target and a['sp']==sp and a['return_va']==ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][i] and a['slot']==slot and a['pop']==pop and a['args']==args,'original third COM method/object/full arguments');out=[];maps=[];bp=self.cpu()['EBP']
  def put(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if i==0:
   need(args==[self.device,256,64,1,0,25,1,work.TEXTURE+44],'original third dimensions/format/pool');result=copy.deepcopy(self.third_creation);maps=[dict(pointer=p,bytes=n) for p,n in dict.fromkeys((p&~4095,4096) for p in (t['pointer'],t['vtable'],*t['methods'].values()))];put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  elif i in (1,4):need(args==[t['pointer'],0,bp-(52 if i==1 else 36)],'original third descriptor destination');result=copy.deepcopy(n['COM_calls'][1]['result']);need(bytes.fromhex(result['hex'])==struct.pack('<8I',25,1,0,1,32768,0,256,64),'complete independent third descriptor');put(args[2],bytes.fromhex(result['hex']))
  elif i==2:
   need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048],'original third lock output/flags');result=copy.deepcopy(self.third_lock);b=bytes.fromhex(result['hex']);need(result['pitch']==512 and len(b)==32768,'historical full lock');p=result['bits']&~4095;maps=[dict(pointer=p,bytes=(result['bits']-p+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',512,result['bits']))
  elif i==3:
   need(args==[t['pointer'],0],'original third unlock');result=copy.deepcopy(n['COM_calls'][3]['result']);pixels=self.read(self.third_lock['bits'],32768);expected=bytes.fromhex(self.third_lock['hex'])
   for band in bands(self.reference['cfg']):expected=convert_surface(self.reference['stages'][-1],self.reference['cfg']['raster_size'],band['rect'],expected,512,band['point'])
   need(pixels==expected and a['uploaded_hex']==pixels.hex() and sha(pixels)==result['uploaded_sha256'],'all original converted pixels equal independent source conversion and historical GPU result')
  else:need(args==[t['pointer']] and release==dict(pointer=n['texture']['pointer'],unlock_hr=0,count=0),'only new logical third texture released');result=copy.deepcopy(release)
  value=result['count'] if i==5 else result['hr'];need(a['result']==result and a['value']==value and a['memory_outputs']==out and a['new_mappings']==maps and a['historical_report_sha256']==work.NATIVE_SHA,'all exact typed historical outputs');self.apply_outputs(a);self.api_return(value,pop,ret,sp);self.third_gpu_count+=1
 def api(self,a):
  if a.get('kind')=='actual_owned_third_GDI':return self.gdi(a)
  if a.get('kind')=='recorded_third_GPU_only':return self.third_gpu(a)
  return super().api(a)
 def replay_new(self,s):
  maps=[]
  for slot in work.IMPORTS:
   at=word(self.read(slot))
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  need(maps==s['entry_mappings'],'only missing source platform entries');root=s['root'];a=s['result'];dirty=set()
  if root:
   self.u.mem_write(root['sp'],struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']));dirty.add(root['sp']>>12)
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  need(self.cpu()==a['before_cpu'],'natural original continuation full CPU');calls=iter(a['api_calls']);next_api=next(calls,None);ih=hashlib.sha256();wh=hashlib.sha256();counts=Counter();writes=0;display=[];conversions=[]
  def code(u,at,n,_):
   nonlocal next_api
   if at==a['boundary']:u.emu_stop();return
   if next_api and at==next_api['target']:
    q=next_api;need(q['kind'] in ('actual_owned_third_GDI','recorded_third_GPU_only','recorded_task_platform'),'no game function or CRT substitution');self.api(dict(q,va=q['target'],key='third_platform'))
    for o in q['memory_outputs']:
     p=o['pointer'];size=len(bytes.fromhex(o['hex']));dirty.update(range(p>>12,((p+size-1)>>12)+1))
    next_api=next(calls,None);return
   key=(at,n)
   if key not in self.task_code:need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'only immutable original third instructions');self.task_code[key]=struct.pack('<I',at)+self.read(at,n)
   if at in work.DISPLAY:sp=self.cpu()['ESP'];display.append(dict(va=at,receiver=self.cpu()['ECX'],return_va=word(self.read(sp))))
   if at==0x405869:
    sp=self.cpu()['ESP'];args=[word(self.read(sp+j)) for j in range(0,24,4)];conversions.append(dict(va=at,args=args,lock_hex=self.read(args[1],8).hex(),rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   counts[at]+=1;ih.update(self.task_code[key])
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original source patch');dirty.update(range(at>>12,((at+n-1)>>12)+1));writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  ch=self.u.hook_add(UC_HOOK_CODE,code);wr=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.ctl_remove_cache(a['before_cpu']['EIP'],a['before_cpu']['EIP']+1);self.u.emu_start(a['before_cpu']['EIP'],0,count=2000000,timeout=120000000)
  finally:self.u.hook_del(ch);self.u.hook_del(wr)
  need(next_api is None and self.cpu()==a['cpu'] and ih.hexdigest()==a['instruction_sha256'] and [dict(va=p,count=n) for p,n in sorted(counts.items())]==a['instruction_counts'],'every original instruction, API and full CPU');need(writes==a['writes'] and wh.hexdigest()==a['write_sha256'] and display==s['display_calls'] and conversions==s['conversions'],'every original write/display/conversion');pages=sorted(dirty);rows=[]
  for lo,hi,_ in self.u.mem_regions():
   key=(lo,hi);i=bisect.bisect_left(pages,lo>>12)
   if key not in self.region_hashes or i<len(pages) and pages[i]<=hi>>12:self.region_hashes[key]=dict(pointer=lo,bytes=hi-lo+1,sha256=sha(self.read(lo,hi-lo+1)))
   rows.append(self.region_hashes[key])
  need(rows==s['full_memory'] and canonical(base.architectural_cpu(self.u))==canonical(s['architectural_cpu']),'all source mappings and complete architectural CPU');need(work.parent.parent.old.init.old.ledger(self)==s['ledger'] and work.text_state(self)==s['state'],'all original state and CRT accounting');b=self.read(work.parent.MANAGER,96);slots=word(b,8);cap=word(b,12);head=word(b,16);arena=word(b,20);end=word(b,48);need(slots==4096 and cap==1048576 and arena<=end<=arena+cap,'original initialized queue');q=dict(manager_hex=b.hex(),head_pointer=head,head_hex=self.read(head,32768).hex(),arena_pointer=arena,used_bytes=end-arena,arena_hex=self.read(arena,end-arena).hex());need(q==s['queue'],'all queue heads/tails and every live draw record');return sum(counts.values())
 def extension(self):
  e=self.case['third_dialogue'];self.third_case=e;self.reference=reproduce_pixels(self.case);self.third_creation,self.third_lock,translation=work.mapped_texture();self.third_texture=self.third_creation['texture'];self.third_gpu_count=0;need(translation==e['typed_texture_projection'] and work.text_state(self)==e['before'] and self.cpu()==e['entry']['cpu'],'independent source entry and typed projection');need(word(self.read(self.renderer+0xb208))==e['raster']['logical_measurement_dc'],'logical measurement DC belongs to original renderer');need(e['raster']['font']!=e['raster']['logical_measurement_dc'] and e['raster']['fresh_owned_measurement_dc']!=e['raster']['logical_measurement_dc'],'fresh owned GDI handles distinct from historical token');count=self.replay_new(e['raster_step']);need(self.read(work.RASTER,len(self.reference['stages'][-1]))==self.reference['stages'][-1],'whole original third raster');need(self.cpu()['EIP']==work.FONT_STOP and self.cpu()['ECX']==work.TEXTURE and word(self.read(self.cpu()['ESP']))==0x405779,'natural original raster-to-texture call');count+=self.replay_new(e['completion']);need(self.cpu()['EIP']==work.RETURN and self.cpu()['ESP']==work.STACK+4 and work.text_state(self)==e['completed'],'complete original third task natural return')
  for f in e['frames']:
   for s in f['steps']:count+=self.replay_new(s);need(self.cpu()['EIP']==work.RETURN and self.cpu()['ESP']==work.STACK+4,'complete original request/reset/task returns')
   need(work.text_state(self)==f['state'] and f['state']['animation']['pc']==290,'each original readiness state before confirmation')
  need(work.text_state(self)==e['final'] and base.memory_rows(self.u)==e['final_memory']==e['frames'][-1]['steps'][-1]['full_memory'] and canonical(base.architectural_cpu(self.u))==canonical(e['final_architectural_cpu']),'final fresh full-byte rehash and complete CPU');pixels=self.read(self.third_lock['bits'],32768);need(pixels.hex()==e['converted_hex'] and sha(pixels)==e['converted_sha256'],'entire original converted surface');before=word(self.read(0x765720));cleanup_count=self.replay_new(e['cleanup']);need(self.third_gpu_count==6 and word(self.read(0x765720))==e['accounting_before']==before-32768,'original source texture destruction/accounting');writes=sum(s['result']['writes'] for s in [e['raster_step'],e['completion'],*[s for f in e['frames'] for s in f['steps']]]);need((count,writes,cleanup_count)==(1408112,690618,149),'all new original source instruction/write/cleanup totals');self.new_proof=dict(new_original_forward_instructions=count,original_cleanup_instructions=cleanup_count,new_original_writes=writes,original_readiness_updates=len(e['frames']),final_PC=290,final_wait=0,independent_native_GDI_pixels_verified=True,full_memory_and_CPU_verified=True,original_queue_verified=True,recorded_texture_calls=6,retained_input_host_writes=0,new_VM_roots=0,new_GPU=False)

def prepare_boundary(c):
 prepare=types.FunctionType(previous.prepare.__code__,dict(previous.prepare.__globals__,Replay=Replay),'prepare_third_test_seed');r,_=prepare(c)
 for f in c['frames']:
  for s in f['steps']:r.task_step(s)
 for s in c['activation']+c['third']:r.task_step(s)
 r.third_case=c['third_dialogue'];r.reference=reproduce_pixels(c);r.third_creation,r.third_lock,_=work.mapped_texture();r.third_texture=r.third_creation['texture'];r.third_gpu_count=0;return r

def verify_case(c):
 protocol(c);observed=[]
 def step(r,s):
  if s['label']=='supplemental_original_character_container_cleanup':r.extension();observed.append(r.new_proof)
  return previous.previous.step(r,s)
 proxy=types.SimpleNamespace(**dict(vars(previous.previous),step=step));prepare=types.FunctionType(previous.prepare.__code__,dict(previous.prepare.__globals__,Replay=Replay),'prepare_independent_third_source');call=types.FunctionType(previous.verify_case.__code__,dict(previous.verify_case.__globals__,Replay=Replay,previous=proxy,prepare=prepare),'verify_parent_and_third_before_original_cleanup');parent_proof=call(c,False);need(len(observed)==1,'one new source continuation before original cleanup');return dict(name=c['name'],scene_capture=c['scene_capture'],parent=parent_proof,third=observed[0])

def verify(r):
 need(r['schema_version']==1 and r['contract']==work.contracts()[2] and r['new_forward_VM_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0,'pinned source, no substitutes or IAT writes')
 for k in ('new_OS_input','new_window','new_GPU','original_outer_scheduler','historical_heap_restored','new_GPU_draw_or_Present','R3_complete','R6_complete'):need(r[k]is False,'honest retained third scope '+k)
 need(r['third_font_created']is r['fresh_owned_offscreen_GDI']is True,'actual owned third font/raster');need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six original branches');return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],six_original_third_dialogues_verified=True,new_GPU=False,new_OS_input=False,interactive_desktop_required=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 raw=(ROOT/a.report).read_bytes();r=verify(json.loads(gzip.decompress(raw)));r['source_report_sha256']=sha(raw);out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six original third dialogues independently verified',flush=True)
