"""Independent original multiline replay and complete current native ownership."""
# Frozen primitives remain unchanged; this module adds the next bounded stage.
from tools.terminal_multiline_verification import *
from tools import terminal_multiline_verification as previous_stage
from tools import terminal_last_dialogue_emulation as e
import re
from tools import terminal_last_dialogue_gdi_verification as gdi_audit
ROOT=e.ROOT
PARENT_ACCEPTANCE=e.PARENT_ACCEPTANCE;PARENT_ACCEPTANCE_SHA=e.PARENT_ACCEPTANCE_SHA
PARENT_SOURCE=e.PARENT_SOURCE;PARENT_SOURCE_SHA=e.PARENT_SOURCE_SHA
PARENT_PROOF=e.PARENT_PROOF;PARENT_PROOF_SHA=e.PARENT_PROOF_SHA
IMPLEMENTATIONS=('tools/terminal_last_dialogue_emulation.py','tools/terminal_last_dialogue_verification.py','tools/terminal_last_dialogue_preservation.py','tools/terminal_last_dialogue_d3d8_platform.cs','tools/terminal_last_dialogue_gdi.py','tools/terminal_last_dialogue_gdi_verification.py','analysis/terminal-last-dialogue-gdi-plan-v1-20261029.json','tools/tests/test_terminal_last_dialogue.py','tools/tests/test_terminal_last_dialogue_source.py')

def gdi_prefix_blocks(row):
 return [row['terminal_name'],row['terminal_dialogue']]+row['terminal_panel_dialogue']['sentences']+[r for stage in (previous_stage.previous_stage.previous_stage.previous_stage,previous_stage.previous_stage.previous_stage,previous_stage.previous_stage,previous_stage) for r in stage.new_resources(row) if r['kind'] in ('name','text')]

def gdi_native(row,old):
 d=row['terminal_last_dialogue'];blocks=gdi_prefix_blocks(row)+new_resources(row);calls=[c for b in blocks for c in b['calls']];traces=[t for b in blocks for t in b['GDI_trace']]
 need(all(len(b['calls'])==len(b['GDI_trace'])==27 for b in blocks),'every actual original GDI call has current receipt')
 need(d['calls']==[c for b in new_resources(row) for c in b['calls']] and d['GDI_trace']==[t for b in new_resources(row) for t in b['GDI_trace']],'nonduplicated complete new GDI ledger')
 report=row['last_dialogue_GDI_lifetimes'];need(report['owner_cleanup']['native_result']==row['name_cleanup']['GDI']==dict(fonts=0,bitmaps=0,dcs=1,all_resources_released=True),'actual measurement DC cleanup with no fallback font/bitmap release')
 path='analysis/terminal-last-dialogue-gdi-plan-v1-20261029.json';old_calls=[c for b in gdi_prefix_blocks(old) for c in b['calls']]
 return gdi_audit.audit(calls,traces,report,d['GDI_handle_projection'],old_calls,(ROOT/path).read_bytes(),path,dict(path=PARENT_SOURCE,bytes=(ROOT/PARENT_SOURCE).stat().st_size,sha256=PARENT_SOURCE_SHA),row['input']['name'])

class StreamingJSON:
 """Decode one complete JSON value with bounded input buffering.

 Each string/number still uses the standard JSON decoder. Only identical
 immutable long strings share storage; no field, byte string or number changes.
 """
 special=re.compile(r'["\\\x00-\x1f]')
 delimiter=re.compile(r'[ \t\r\n,\]}:]')
 def __init__(self,stream,chunk_size=1048576):
  need(type(chunk_size)is int and chunk_size>0,'positive JSON input chunk');self.stream=stream;self.chunk_size=chunk_size;self.buffer='';self.position=0;self.pool={}
 def peek(self):
  if self.position==len(self.buffer):self.buffer=self.stream.read(self.chunk_size);self.position=0
  return self.buffer[self.position:self.position+1]
 def take(self):
  value=self.peek();need(bool(value),'complete JSON token');self.position+=1;return value
 def whitespace(self):
  while self.peek():
   end=self.position
   while end<len(self.buffer) and self.buffer[end] in ' \t\r\n':end+=1
   self.position=end
   if end<len(self.buffer):break
 def string(self):
  need(self.take()=='"','JSON string opening quote');parts=[]
  while True:
   need(bool(self.peek()),'complete JSON string');match=self.special.search(self.buffer,self.position)
   if match is None:parts.append(self.buffer[self.position:]);self.position=len(self.buffer);continue
   parts.append(self.buffer[self.position:match.start()]);char=match.group();self.position=match.end()
   if char=='"':break
   need(char=='\\','no unescaped JSON control character');escape=self.take();parts.append('\\'+escape)
   if escape=='u':parts.append(''.join(self.take() for _ in range(4)))
  value=json.loads('"'+''.join(parts)+'"');return self.pool.setdefault(value,value) if len(value)>=4096 else value
 def value(self):
  self.whitespace();char=self.peek();need(bool(char),'complete JSON value')
  if char=='"':return self.string()
  if char=='{':
   self.take();out={};self.whitespace()
   if self.peek()=='}':self.take();return out
   while True:
    self.whitespace();key=self.string();self.whitespace();need(self.take()==':','JSON member colon');out[key]=self.value();self.whitespace();end=self.take()
    if end=='}':return out
    need(end==',','JSON object separator')
  if char=='[':
   self.take();out=[];self.whitespace()
   if self.peek()==']':self.take();return out
   while True:
    out.append(self.value());self.whitespace();end=self.take()
    if end==']':return out
    need(end==',','JSON array separator')
  parts=[]
  while self.peek():
   match=self.delimiter.search(self.buffer,self.position)
   if match is not None:parts.append(self.buffer[self.position:match.start()]);self.position=match.start();break
   parts.append(self.buffer[self.position:]);self.position=len(self.buffer)
  token=''.join(parts);need(bool(token),'nonempty JSON primitive');return json.loads(token)
 def decode(self):
  result=self.value();self.whitespace();need(not self.peek(),'no trailing JSON data');return result

def load_report(path):
 path=Path(path);opener=gzip.open if path.suffix=='.gz' else open
 with opener(path,'rt',encoding='utf8') as stream:return StreamingJSON(stream).decode()

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original last-dialogue branch');win=name=='neutral_running'
 lines=[dict(PC=p,text_index=t,layer=l,record_index=i) for p,t,l,i in ([(306,9,4,0)] if win else [(324,10,7,0),(330,11,7,1),(336,12,7,2)])]
 return dict(first_PC=294 if win else 312,segment=2 if win else 11,role=None,lines=lines,ready_PC=316 if win else 346,final_PC=320 if win else 350,scene_capture=76 if win else 77,final_layer=4 if win else 7)

def helper_contract():return e.helper_contract()

@lru_cache(maxsize=1)
def parent_report():
 for path,want in ((PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),(PARENT_PROOF,PARENT_PROOF_SHA),(PARENT_SOURCE,PARENT_SOURCE_SHA)):
  h=hashlib.sha256()
  with (ROOT/path).open('rb') as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  need(h.hexdigest()==want,'fixed accepted next-dialogue '+path)
 return load_report(ROOT/PARENT_SOURCE)

def parent_case(row):return next(x for x in parent_report()['cases'] if x['input']==row['input'])

@lru_cache(maxsize=1)
def parent_trace_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed compact next-dialogue proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def prefix_trace(row):
 name=row['input']['name'];d=row['terminal_last_dialogue'];want=parent_trace_summaries()[name];actual=d['before']['trace'];need(actual==want,'exact full cumulative parent counters and digests '+name+' expected='+repr(want)+' actual='+repr(actual));need(d['prefix_preflight']==dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=want,actual=actual),'source parent preflight independently bound');return True

def accepted_clock_inputs():return {r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in parent_report()['cases']}
def new_resources(row):
 d=row['terminal_last_dialogue'];return [r for r in d['resources'] if r['create_wire_index']>=d['prefix']['GPU_wire']]
def capture_list(value):return previous_stage.capture_list(value)
def gpu_calls(row):
 d=row['terminal_last_dialogue'];return [c for c in previous_stage.gpu_calls(row) if c.get('wire_index',-1)<d['prefix']['GPU_wire']]+d['GPU_APIs']
def gpu_mappings(row):
 allowed={'overlay',FOLLOWUP_POINTER_DOMAIN,FOLLOWUP_BITS_DOMAIN,'overlay-replacement-0','overlay-replacement-1','overlay-next-dialogue-name','overlay-next-dialogue-portrait','overlay-next-dialogue-text'}|set(e.parent.PROJECTION_DOMAINS)|set(e.PROJECTION_DOMAINS);out={};keys=set();guests={};aliases=0
 for r in row['typed_GPU_projection']:
  need(set(r)=={'domain','native','guest'} and r['domain'] in allowed and type(r['native'])is int and 0<r['native']<2**32 and type(r['guest'])is int and 0<r['guest']<2**32,'finite typed lifetime/native entry');key=(r['domain'],r['native']);need(key not in keys,'unique domain/native identity')
  if r['domain']==FOLLOWUP_BITS_DOMAIN:need(r['guest'] in guests and guests[r['guest']]['domain']=='overlay' and aliases==0,'only independently bound retired FU surface alias');aliases+=1
  else:need(r['guest'] not in guests,'all other guest identities distinct');guests[r['guest']]=r
  keys.add(key);out.setdefault(r['domain'],{})[r['native']]=r['guest']
 need('overlay' in out,'original device namespace');return out
def resource_domain(row,r):
 if 'terminal_last_dialogue' not in row or r['create_wire_index']<row['terminal_last_dialogue']['prefix']['GPU_wire']:return previous_stage.resource_domain(row,r)
 cfg=branch(row['input']['name']);i=r['creation_index'];need(type(i)is int and 0<=i<len(cfg['lines']),'bounded actual new creation');line=cfg['lines'][i];domain='overlay-last-dialogue-'+str(i)
 need(r['kind']=='text' and r['record']==text_record(line['layer'],line['record_index']) and all(r[k]==v for k,v in line.items()) and r['projection_domain']==domain,'new domain tied to independently derived original command/layer/count record');return domain
def resource_context(row,r,contexts):
 context=contexts[resource_domain(row,r)]
 if previous_stage.bridged_followup_pointer(row,r) and FOLLOWUP_POINTER_DOMAIN in contexts:
  need(set(contexts[FOLLOWUP_POINTER_DOMAIN])=={r['native_pointer']},'exact retained FU texture pointer binding');context=context|contexts[FOLLOWUP_POINTER_DOMAIN]
  lock=next(c for c in r['GPU_APIs'] if c['op']=='lock');need(set(contexts[FOLLOWUP_BITS_DOMAIN])=={lock['native_result']['bits']},'exact retained FU surface binding');context=context|contexts[FOLLOWUP_BITS_DOMAIN]
 return context

def forward_only(row):
 d=row['terminal_multiline'];end=row['multiline_cleanup'][0]['leaves'][0];out=dict(d,leaves=d['leaves'][:end],GPU_APIs=[c for c in d['GPU_APIs'] if c['wire_index']<d['forward_wire_end']]);return out
def prefix(row,old=None,replay=True):
 old=parent_case(row) if old is None else old;d=row['terminal_last_dialogue'];fixed=old['terminal_multiline']['final'];cfg=branch(row['input']['name'])
 for key in ('memory','CPU','state','queue','trace'):need(d['before'][key]==fixed[key]==row['terminal_multiline']['final'][key],'entire frozen next-dialogue boundary '+key)
 need(d['before']['local_trace']==mark_zero() and vw(d['before']['state'])==(cfg['first_PC'],1),'new clock starts at original confirmation');need(guest(forward_only(row))==guest(forward_only(old)),'complete next-dialogue forward excluding its historical cleanup')
 need(all(row['blobs'].get(k)==old['blobs'][k] for k in page_keys(forward_only(old))),'all latest parent intermediate pages exact')
 p=d['prefix'];need((p['GPU_wire'],p['CRT_wire'])==(old['terminal_multiline']['forward_wire_end'],old['terminal_multiline']['CRT_forward_wire_end']),'exact accepted platform cursors')
 n=sum(a['wire_end']<=p['CRT_wire'] for a in old['CRT_APIs'])
 for key,length in dict(CRT_APIs=n,task_APIs=len(old['task_APIs']),task_calls=len(old['task_calls']),task_writes=len(old['task_writes']),APIs=len(old['APIs'])).items():need(p[key]==length and guest(row[key][:length])==guest(old[key][:length]),'complete parent ledger '+key)
 need(p['resource_steps']==len(old['resource_initialization']) and guest(row['resource_initialization'][:p['resource_steps']])==guest(old['resource_initialization']) and p['extra_counts']==old['extra_original_instruction_counts'] and len(row['APIs'])==p['APIs'],'unchanged resource initialization/accounting and no new clocks')
 earlier=previous_stage.prefix(row,replay=replay);counts=None
 if replay:counts=previous_stage.Replay(row,previous_stage.pixels(row)[1]).execute()
 return dict(fixed_acceptance_sha256=PARENT_ACCEPTANCE_SHA,fixed_source_sha256=PARENT_SOURCE_SHA,fixed_proof_sha256=PARENT_PROOF_SHA,parent_full_memory_CPU_queue_and_trace_equal=True,earlier=earlier,independent_next_dialogue_forward=counts,no_historical_cleanup_projection=True)

def source(row):
 cfg=branch(row['input']['name']);d=row['terminal_last_dialogue'];raw=(ROOT/e.terminal.SCRIPT_PATH).read_bytes();need(sha(raw)==SCRIPT_SHA,'whole original T0004');s=next(s for s in previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);at=s['code_start'];pc=cfg['first_PC'];base=num(read(d['before']['memory'],e.VM+16,4),0)
 expected=[(294,43,8),(302,44,4),(306,17,6),(312,50,4),(316,51,4)] if cfg['segment']==2 else [(312,43,8),(320,44,4),(324,17,6),(330,17,6),(336,17,6),(342,50,4),(346,51,4)];commands=[]
 for want in expected:
  op,n=struct.unpack_from('<HH',raw,at+pc);need((pc,op,n)==want and read(d['before']['memory'],base+pc,n)==raw[at+pc:at+pc+n],'entire original multiline command bytes and length');commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
 need(pc==cfg['final_PC'] and d['commands']==commands and struct.unpack_from('<HH',raw,at+pc)==(44,4),'only bounded multiline group; successor unexecuted')
 configs=[(294,7,4)] if cfg['segment']==2 else [(312,4,7)]
 for p,i,layer in configs:need(num(raw,at+p+4)==0x20000000+i and num(e.CODE,0x624520-0x400000+i*38,'h')==layer,'original source configuration selects expected layer')
 identities={2: {9: (1418, 'b6e2a149')}, 11: {10: (3488, 'a65ea6e3bab8a8a9aca5a5cba761a143'), 11: (3506, 'a8bab8cca6b3ac58b36eaabaa4f2b4e0a142b7c5b778aabaa4f5c46ca14ba14b'), 12: (3540, 'a6dca4d6a662bff4a8d3a548ab65a141c5fda66fa66ea66ec052be69a440a455a761a143')}};texts=[]
 for line in cfg['lines']:
  i=line['text_index'];need(num(raw,at+line['PC']+4,'H')==i,'original line text index');packed=num(raw,s['code_end']+4+i*4);span=packed>>20;off=s['code_end']+(packed&0xFFFFF);b=raw[off:off+span];need(2<=span<=512 and span%2==0 and b[-2:]==bytes(2) and 0 not in b[:-2] and (off,b[:-2].hex())==identities[cfg['segment']][i],'entire original ANSI text identity');texts.append(dict(line,index=i,source_offset=off,hex=b[:-2].hex()))
 need(e.ALLOWED is e.parent.ALLOWED and e.LastDialogueMachine.source_code is e.parent.MultilineMachine.source_code,'no new original code ranges or changed source guard');return dict(segment=cfg['segment'],script_sha256=SCRIPT_SHA,commands=commands,final_PC=pc,next_opcode=44,configurations=configs,texts=texts)

def pixels(row):
 provenance=source(row);resources=new_resources(row);refs={};need(len(resources)==len(provenance['texts']) and all(r['kind']=='text' for r in resources),'exact original new text creations')
 for r,text in zip(resources,provenance['texts']):
  layer=text['layer'];b=r['font_boundary'];sp=b['CPU']['ESP'];args=[num(read(b['memory'],sp+4+i*4,4),0) for i in range(14)];need(r['pending_font']==dict(entry=num(read(b['memory'],0x5920A0,4),0),caller=0x4CAD09,args=args,CPU=b['CPU'],first_instruction_executed=False) and b['CPU']['EIP']==r['pending_font']['entry'] and num(read(b['memory'],sp,4),0)==0x4CAD09,'entire original font ABI at natural unexecuted entry')
  obj=read(b['memory'],text_object(layer),0x18);alt=bool(obj[0x14]);width=num(obj,0xE if alt else 0xC,'h')&0xFFFFFFFF;height=num(obj,0x12 if alt else 0x10,'h')&0xFFFFFFFF
  need(args==[height,width,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C] and r['record']==text_record(layer,text['record_index']) and all(r[k]==text[k] for k in ('PC','text_index','layer','record_index')),'original per-layer count/font and source index')
  reference=previous.dialogue.raster_dialogue(bytes.fromhex(text['hex']),args[:-1],original_text(args[-1]));raster=r['raster'];g=geometry(reference['measured']);need(r['geometry']==g and (raster['ACP'],raster['measured'],raster['selected_face'],raster['raster_hex'])==(reference['ACP'],reference['measured'],reference['selected_face'],reference['raster_hex']),'independent GDI metrics/face/entire DIB');need([a['name'] for a in raster['stages']]==['PatBlt','TextOutA','TextOutA'] and [a['hex'] for a in raster['stages']]==[a['hex'] for a in reference['stages']],'all clear/shadow/foreground bytes');need([a['name'] for a in r['calls']]==NAMES+['SelectObject','DeleteObject','DeleteDC','DeleteObject'] and raster['calls']==r['calls'][:23],'all27 original GDI calls and cleanup')
  lock=r['lock'];w,h=[1<<(v-1).bit_length() for v in g['texture_size']];out=bytes.fromhex(lock['hex']);need(lock['pitch']==w*2 and len(out)==w*h*2,'whole actual initial lock span and untouched padding');expected=bands(g);need([dict(rect=c['rect'],point=c['point']) for c in r['conversions']]==expected,'original complete conversion band geometry')
  for band in expected:out=convert_surface(bytes.fromhex(reference['raster_hex']),g['raster_size'],band['rect'],out,lock['pitch'],band['point'])
  need(r['upload_hex']==r['readback']['hex']==out.hex() and r['readback']['sha256']==sha(out) and r['readback']['pitch']==lock['pitch'],'every independent converted texel with actual untouched native bytes');need(num(read(r['completion']['memory'],text_object(layer)+22,2),0,'H')==text['record_index']+1,'original complete line count');refs[r['generation']]=dict(reference=reference,geometry=g)
 return provenance,refs

def bind_replay(fn):
 routing={'terminal_multiline':'terminal_last_dialogue','multiline_cleanup':'last_dialogue_cleanup'}
 def constants(code):return code.replace(co_consts=tuple(constants(v) if isinstance(v,types.CodeType) else routing.get(v,v) if type(v)is str else v for v in code.co_consts))
 scope=dict(fn.__globals__,**globals());scope['Uc']=source_image_uc
 if fn.__name__=='execute':scope['need']=replay_need
 return types.FunctionType(constants(fn.__code__),scope,closure=fn.__closure__)

class Replay(previous_stage.Replay):
 _initialize=bind_replay(previous_stage.Replay._initialize)
 def __init__(self,row,refs):
  partitions=source_image_partitions(row['terminal_last_dialogue']['before']['memory']);self._initialize(row,refs);self.u.mem_map=self.u._original_snapshot_map;del self.u._original_snapshot_map;self.u.mem_protect(SOURCE_IMAGE_BASE,(len(e.CODE)+4095)&~4095,5)
  for address,size in SOURCE_IMAGE_WRITABLE:self.u.mem_protect(address,size,3)
  for address,size,perms in partitions:self.u.mem_protect(address,size,perms)
  self.image_layout=dict(complete_image_mapped_first=True,one_original_image_RAM_backing=True,source_RX_RW_permissions=True,snapshot_partitions_preserved=True,original_events_filtered=False)
 execute=bind_replay(previous_stage.Replay.execute)

 def cleanup(self):
  d=self.d;rows=self.row['last_dialogue_cleanup'];steps=self.row['cleanup_steps'];keys=('label','entry','args','receiver','cdecl');old=parent_case(self.row);expected=[{k:s[k] for k in keys} for s in old['cleanup_steps']]
  need([{k:r[k] for k in keys} for r in rows]==expected==[{k:s[k] for k in keys} for s in steps],'all actual current original teardown roots without historical CPU projection');self.cleaning=True;index=self.forward_end;total_i=total_w=0;ih=hashlib.sha256();wh=hashlib.sha256();last=d['final']['trace']
  def code(u,at,size,_):
   nonlocal index,total_i
   if at==e.RETURN:u.emu_stop();return
   if index<len(d['leaves']) and at==d['leaves'][index]['call']['target']:
    item=d['leaves'][index];need(item['kind'] in ('GPU','CRT') and item['phase']=='cleanup','only actual owned teardown platform leaves');self.leaf(item);index+=1;return
   need(at in e.ALLOWED and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only finite unchanged original teardown instructions');total_i+=1;ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):
   nonlocal total_w
   need(not 0x400000<=at<0x593000,'original teardown cannot change code or IAT');total_w+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
  hooks=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)]
  try:
   for c,s in zip(rows,steps):
    self.capture(c['before']);need(c['before']['CPU']==s['before_cpu'] and c['before']['trace']==s['trace_before']==last and c['before']['local_trace']==d['final']['local_trace'] and index==c['leaves'][0],'actual full current memory/57CPU/queue at each teardown entry');before_i,before_w=total_i,total_w;sp=e.STACK+0xF000;self.put(sp,struct.pack('<I',e.RETURN))
    for j,a in enumerate(c['args']):self.put(sp+4+j*4,struct.pack('<I',a))
    self.u.reg_write(x86.UC_X86_REG_ESP,sp);self.u.reg_write(x86.UC_X86_REG_ECX,c['receiver']);self.u.emu_start(c['entry'],0,count=4_000_000,timeout=60_000_000);self.capture(c['after'])
    need(self.cpu()==s['cpu_after'] and self.cpu()['EIP']==e.RETURN and self.cpu()['ESP']==sp+4+(0 if c['cdecl'] else 4*len(c['args'])),'every actual original teardown root complete57CPU and natural stack return')
    need(c['after']['trace']==s['trace_after'] and c['after']['local_trace']==d['final']['local_trace'] and total_i-before_i==s['trace_after']['instructions']-last['instructions'] and total_w-before_w==s['trace_after']['writes']-last['writes'] and index==c['leaves'][1],'all actual original teardown counts and platform leaves');last=s['trace_after']
    leaves=d['leaves'][c['leaves'][0]:c['leaves'][1]];need(c['GPU_APIs']==[x['call'] for x in leaves if x['kind']=='GPU'] and c['CRT_APIs']==[x['call'] for x in leaves if x['kind']=='CRT'],'each actual teardown platform operation owned once by its original root')
  finally:
   for h in hooks:self.u.hook_del(h)
  need(index==len(d['leaves']) and self.wire==len(self.row['CRT_trace'])-1 and not self.blocks and not self.criticals and not self.files and self.depth==0,'all actual current original releases and full native buffer mirrors consumed')
  state=self.row['cleanup_state'];need(num(self.read(0x765720,4),0)==state['texture_bytes']==self.row['accounting_baseline']['texture_bytes'] and num(self.read(0x79FC74,4),0)==state['game_bytes']==self.row['accounting_baseline']['game_bytes'],'all original current texture and CRT accounting restored')
  for group in (20,32,30):need(self.read(e.MAIN+0x844+group*8,8)==bytes(8),'every current source resource bank originally cleared')
  for r in d['resources']:
   if e.VM<=r['record']<e.VM+0x9400:need(num(self.read(r['record']+44,4),0)==0,'every embedded old/new texture record naturally cleared')
  return dict(instructions=total_i,writes=total_w,independent_local_code_sha256=ih.hexdigest(),independent_local_write_sha256=wh.hexdigest(),CPU_registers=57,all_actual_original_roots=len(rows),all_root_full_memory_and_native_sync_verified=True,no_historical_CPU_or_SHA_projection=True)

def replay_need(ok,message):
 if ok:return
 local=sys._getframe(1).f_locals;machine=local.get('self');segment=local.get('s',{});diagnostic=dict(schema_version=1,error=message)
 if machine is not None:
  actual=machine.cpu();expected=segment.get('CPU',{});mark=local.get('mark')
  diagnostic.update(case=machine.row['input']['name'],segment_index=local.get('i'),segment={k:segment.get(k) for k in ('label','kind','entry','stop','root')},actual_CPU=actual,expected_CPU=expected,CPU_differences={k:dict(actual=actual.get(k),expected=expected.get(k)) for k in actual.keys()|expected.keys() if actual.get(k)!=expected.get(k)},actual_mark=mark() if callable(mark) else None,expected_mark=segment.get('local_after'),actual_leaf_cursor=local.get('index'),expected_leaf_cursor=segment.get('leaves'),original_segments_unchanged=True)
 path=ROOT/('analysis/terminal-last-dialogue-replay-diagnostic-'+str(time.time_ns())+'-20261029.json')
 with path.open('x',encoding='utf8',newline='\n') as out:json.dump(diagnostic,out,separators=(',',':'));out.write('\n')
 need(False,message+'; diagnostic='+path.relative_to(ROOT).as_posix())

def native(row,old=None):
 """Audit current receipts by creation ordinal, with no byte identity masks."""
 d=row['terminal_last_dialogue'];old=parent_case(row) if old is None else old;helper_contract();contexts=gpu_mappings(row);m=contexts['overlay'];gt=row['GPU_trace'];ct=row['CRT_trace'];ledger=row['last_dialogue_resources_after_cleanup'];by_create={r['create_wire_index']:r for r in ledger};by_gen={r['generation']:r for r in ledger}
 parent_contexts=previous_stage.gpu_mappings(old);wanted=set(parent_contexts)|{'overlay-last-dialogue-'+str(i) for i in range(len(branch(row['input']['name'])['lines']))};need(set(contexts)==wanted,'exact retained parent and new creation domains')
 if row['input']['name']=='timeout_before_combat':previous_stage.legacy_surface_binding(row)
 else:need(row['terminal_next_dialogue']['historical_surface_alias'] is None,'victory has no FU surface alias')
 projection=row['typed_GPU_projection'];prefix_rows=[r for r in projection if not r['domain'].startswith('overlay-last-dialogue-')];ordinal_rows=[r for r in prefix_rows if r['domain']!=FOLLOWUP_BITS_DOMAIN];prefix_next=0x64001000+len(ordinal_rows)*0x100000;first=e.GPU_GUEST_START
 need(prefix_next<=e.PREFIX_NEXT_MAX and d['GPU_projection_before']==dict(next=prefix_next,ledger=prefix_rows) and projection[:len(prefix_rows)]==prefix_rows and d['GPU_projection']==projection[len(prefix_rows):],'entire ordered parent ledger and explicit new identities')
 parent_prefix=[r for r in prefix_rows if not r['domain'].startswith('overlay-multiline-')];p=row['terminal_multiline'];need(p['GPU_projection_before']==dict(next=0x64001000+sum(r['domain']!=FOLLOWUP_BITS_DOMAIN for r in parent_prefix)*0x100000,ledger=parent_prefix) and p['GPU_projection']==[r for r in prefix_rows if r['domain'].startswith('overlay-multiline-')],'entire current parent projection metadata bound to actual raw ledger')
 need([r['guest'] for r in ordinal_rows]==[0x64001000+i*0x100000 for i in range(len(ordinal_rows))],'all parent guest ordinals exact; one declared retired-surface alias adds no slot')
 def interface_ids(v):return [v['pointer'],v['vtable']]+list(v['methods'].values())
 oldledger=row['multiline_resources_after_cleanup'];identities={k:set() for k in contexts if not k.startswith('overlay-last-dialogue-')};identities['overlay'].update(interface_ids(row['current_GPU_hello']['device']))
 for r in oldledger:
  domain=resource_domain(row,r);create=gt[r['create_wire_index']]['reply']['result']['texture'];ids=interface_ids(create);bridged=previous_stage.bridged_followup_pointer(row,r)
  if bridged:identities[FOLLOWUP_POINTER_DOMAIN].add(ids.pop(0))
  identities[domain].update(ids);bits=next(t['reply']['result']['bits'] for i,t in enumerate(gt) if r['create_wire_index']<i<=r['release_wire_index'] and t['request']['op']=='lock' and t['request']['pointer']==r['native_pointer']);identities[FOLLOWUP_BITS_DOMAIN if bridged else domain].add(bits)
 for domain,values in identities.items():need(set(contexts[domain])==values,'all inherited current identities tied to exact device/create/lock wire')
 for index,r in enumerate(new_resources(row)):
  domain=resource_domain(row,r);native_texture=gt[r['create_wire_index']]['reply']['result']['texture'];lock=next(c['native_result'] for c in r['GPU_APIs'] if c['op']=='lock');need(list(native_texture['methods'])==['8','56','64','68'],'original texture ABI');sequence=interface_ids(native_texture)+[lock['bits']];need(len(sequence)==len(set(sequence))==7,'seven actual identities per current creation');need([v for v in projection if v['domain']==domain]==[dict(domain=domain,native=p,guest=first+(7*index+j)*0x100000) for j,p in enumerate(sequence)],'independent new creation allocation sequence')
 need(first+7*len(new_resources(row))*0x100000<=e.LAST_DIALOGUE_NEXT_MAX<e.GDI_GUEST_START,'bounded current GPU namespace below GDI')
 namespace=dict(prefix_next=prefix_next,new_start=e.GPU_GUEST_START,new_end=e.LAST_DIALOGUE_NEXT_MAX,all_before_mappings_disjoint=True,before_mapping_count=len(d['before']['memory']),parent_ledger_unchanged=True,original_AddressSpace_guest_code_unchanged=True)
 need(d['GPU_namespace']==namespace,'entire new namespace declaration equals actual frozen parent and independent extent')
 for region in d['before']['memory']:need(region['pointer']+region['bytes']<=e.GPU_GUEST_START or e.LAST_DIALOGUE_NEXT_MAX<=region['pointer'],'new whole GPU span disjoint from every complete before mapping')
 need(all(not(e.GPU_GUEST_START<=r['guest']<e.LAST_DIALOGUE_NEXT_MAX) for r in prefix_rows) and e.LAST_DIALOGUE_NEXT_MAX<=HEAP_BASE and all(g['guest']>=e.GDI_GUEST_START for g in d['GDI_handle_projection']),'no retired/live parent, CRT heap or current GDI guest identity overlaps new GPU span')
 need(row['current_GPU_hello']['max_textures']==10 and row['current_GPU_hello']['max_creates']==32,'actual unchanged capacity10 owner')
 need(row['current_CRT_hello']['pointer_bytes']==row['current_GPU_hello']['pointer_bytes']==4 and row['current_GPU_hello']['window_visible'] is False and row['current_GPU_hello']['image_size']==[512,512] and row['current_CRT_hello']['GPU_created'] is False,'actual bounded headless x86 CRT/GPU owners')
 need(len(by_create)==len(by_gen)==len(ledger)==(15 if row['input']['name']=='neutral_running' else 18),'every old and new creation generation')
 need(len(d['resources'])==len(ledger) and len(d['resources_before'])==(14 if row['input']['name']=='neutral_running' else 15),'complete eight-generation prefix and two new text generations')
 need(d['resources_before']==row['terminal_multiline']['resources'],'each seeded generation bound to complete actual parent ledger, including already retired timeout text5')
 for before,after in zip(d['resources_before'],d['resources'][:len(d['resources_before'])]):
  for k,v in before.items():
   if k not in ('alive','release_wire_index','released_phase','alive_after_forward'):need(after[k]==v,'unchanged original seeded metadata '+k)
  if not before['alive']:need(all(after.get(k)==before.get(k) for k in ('alive','release_wire_index','released_phase')),'an already retired generation never revived or released twice')
 need(d['GPU_APIs']==[x['call'] for x in d['leaves'] if x['kind']=='GPU'] and d['calls']==[x['call'] for x in d['leaves'] if x['kind']=='GDI'] and row['CRT_APIs'][d['prefix']['CRT_APIs']:]==[x['call'] for x in d['leaves'] if x['kind']=='CRT'],'every original platform leaf belongs once to its full current receipt ledger')
 for r in new_resources(row):
  a,z=r['leaves'];leaves=d['leaves'][a:z];need(0<=a<z<=row['last_dialogue_cleanup'][0]['leaves'][0] and r['GPU_APIs']==[x['call'] for x in leaves if x['kind']=='GPU'] and r['calls']==[x['call'] for x in leaves if x['kind']=='GDI'] and r['conversions']==[c for c in d['conversions'] if c['resource_label']==r['label']],'complete actual original resource leaf/conversion interval')
 live={};logical={};ci=readbacks=peak=0;calls=gpu_calls(row);observers={o['wire_index']:o for o in d['readback_observers']}
 need(len(observers)==len(d['readback_observers']),'every current follow-up observer classified once')
 for label,tr in (('GPU',gt),('CRT',ct)):
  for i,t in enumerate(tr):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok'] is True,'complete ordered successful actual '+label+' wire')
 oldcontexts=gpu_mappings(old);oldledger=old['multiline_resources_after_cleanup']
 for i,t in enumerate(gt[:d['prefix']['GPU_wire']]):
  q=t['request'];op=q['op'];ptr=t['reply']['result']['texture']['pointer'] if op=='create' else q.get('pointer');matches=[r for r in ledger if r['native_pointer']==ptr and r['create_wire_index']<=i<=r['release_wire_index']];need(len(matches)==1,'one actual generation at every inherited wire')
  r=matches[0];o=next(r0 for r0 in oldledger if r0['generation']==r['generation']);domain=resource_domain(row,r);old_domain=previous_stage.resource_domain(old,o)
  need(previous.gpu_value(t,resource_context(row,r,contexts))==previous.gpu_value(old['GPU_trace'][i],resource_context(old,o,oldcontexts)),'whole inherited GPU wire in original resource lifetime and exact fixed guest identity')
 for i,t in enumerate(gt):
  q=t['request'];result=t['reply']['result'];op=q['op']
  if op=='close':
   need(i==len(gt)-1 and not live and result==row['GPU_cleanup'] and not result['texture_releases'],'normal close after every original release, no helper fallback');continue
  if op=='readback':
   need(q['pointer'] in live,'observer never reads a retired generation');r=live[q['pointer']];raw=bytes.fromhex(r['upload_hex']);need(result['hex']==raw.hex() and result['sha256']==sha(raw) and result['pitch']==r['size'][0]*2,'every live generation whole current readback')
   if i>=d['prefix']['GPU_wire']:
    need(i in observers,'every new raw readback has explicit observer provenance');o=observers[i];need((o['generation'],o['record'],o['result'])==(r['generation'],r['record'],result),'observer belongs to this creation generation and record')
   readbacks+=1;continue
  need(ci<len(calls),'no unclassified original COM operation');c=calls[ci];ci+=1
  generation=by_create[i]['generation'] if op=='create' else c.get('generation')
  if generation is None:
   matches=[r for r in ledger if r['native_pointer']==q['pointer'] and r['create_wire_index']<i<=r['release_wire_index']];need(len(matches)==1,'one live native lifetime for each inherited original operation');generation=matches[0]['generation']
  need(generation in by_gen,'original operation identifies an existing creation generation');context=resource_context(row,by_gen[generation],contexts)
  need(c.get('wire_index',i)==i and c['op']==op and c['native_result']==result and c['result']==previous.gpu_value(result,context) and c['actual_API_executed'] is True,'original COM call bound to exact current raw wire and lifetime domain')
  expected=dict(id=i+1,op=op)
  if op=='create':
   need(i in by_create,'every texture creation recorded once');r=by_create[i];a=c['args'];p=result['texture']['pointer'];need(r['generation']==i+1 and r['native_pointer']==p and r['texture']==c['result']['texture'] and r['record']==a[-1]-44 and r['size']==a[1:3] and p not in live and r['texture']['pointer'] not in logical,'creation ordinal/record and simultaneous native and guest ownership')
   live[p]=r;logical[r['texture']['pointer']]=r;expected.update(width=a[1],height=a[2],levels=a[3],usage=a[4],format=a[5],pool=a[6]);peak=max(peak,len(live))
  else:
   need(c['args'][0] in logical,'original COM receiver has a live generation');r=logical[c['args'][0]];need(live.get(q['pointer']) is r,'current native pointer projects to the same live generation');expected['pointer']=r['texture']['pointer']
   if op=='lock':expected['flags']=c['args'][-1];need(c['result']==r['lock'],'whole actual LockRect input bound to this generation')
   elif op=='unlock':expected['hex']=r['upload_hex']
   elif op=='release':
    need(r['release_wire_index']==i and c['value']==result['count']==0,'last original release closes exactly this generation');del live[q['pointer']];del logical[r['texture']['pointer']]
   else:need(op=='describe','only original finite COM methods')
  need(previous.gpu_value(q,context)==expected,'entire independently translated current original COM request in its ownership lifetime')
  if i>=d['prefix']['GPU_wire']:
   need((c['generation'],c['record'],c['resource_kind'],c['resource_label'],c['phase'])==(r['generation'],r['record'],r['kind'],r['label'],'forward' if i<d['forward_wire_end'] else 'cleanup'),'current leaf has exact generation, record and execution phase')
  if i==d['forward_wire_end']-1:need(False,'last forward wire is an observer, never an original COM call')
 need(ci==len(calls) and peak==10,'all original COM calls and exact bounded simultaneous texture peak')
 need(sorted(observers)==[i for i,t in enumerate(gt) if i>=d['prefix']['GPU_wire'] and t['request']['op']=='readback'],'no missing/extra new observer wires')
 declared=[]
 for r in new_resources(row):
  i=r['readback_wire_index'];need(observers[i]==dict(label='unlock_'+r['label'],generation=r['generation'],record=r['record'],wire_index=i,result=r['readback']) and gt[i]['reply']['result']==r['readback'],'entire actual new upload observer receipt and unique provenance');declared.append(i)
  retain=[o for o in d['readback_observers'] if o['label']==r['label']+'_complete'];need(r['retained_readbacks']==retain and len({o['generation'] for o in retain})==len(retain) and bool(retain),'each completed original resource observes every current surviving generation once')
  for o in retain:
   live_here={g['generation'] for g in ledger if g['create_wire_index']<o['wire_index']<g['release_wire_index']};need({v['generation'] for v in retain}==live_here,'all old/new surfaces actually survive this natural completion')
  declared.extend(o['wire_index'] for o in retain)
 declared.extend(o['wire_index'] for o in d['readbacks']);need(sorted(declared)==sorted(observers),'each follow-up raw observer belongs once to unlock, natural completion or final live set')
 for r,f in zip(ledger,d['resources']):
  need(r['alive'] is False and r['release_wire_index'] is not None,'every actual texture generation released')
  want=copy.deepcopy(r);want['alive']=r['create_wire_index']<d['forward_wire_end'] and r['release_wire_index']>=d['forward_wire_end']
  if want['alive']:want['release_wire_index']=None;want.pop('released_phase',None)
  need(f==want and f['alive']==r['alive_after_forward'],'forward ledger frozen before actual late cleanup')
 need({o['generation'] for o in d['readbacks']}=={r['generation'] for r in d['resources'] if r['alive']} and all(o==observers[o['wire_index']] and o['label']=='final' for o in d['readbacks']),'every surviving old/new surface observed through final confirmation')
 covered=[]
 for a in row['CRT_APIs']:
  need(0<=a['wire_start']<a['wire_end']<len(ct) and CRT_IMPORTS[a['import_slot']]==(a['name'],a['pop']) and e.CODE[a['import_slot']-0x400000:a['import_slot']-0x400000+4]==struct.pack('<I',a['target']),'actual original CRT IAT and declared bounded wire interval');covered.extend(range(a['wire_start'],a['wire_end']));r=ct[a['wire_end']-1]['reply']['result'];nm=a['name'];outputs=[]
  if nm in ('InitializeCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
   raw=r['hex'] if nm=='InitializeCriticalSection' else r['critical_hex'];b=bytearray.fromhex(raw);need(len(b)==24,'whole actual critical section')
   for off in (0,12,16):
    if num(b,off) not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off+(a['args'][0]-0x80A480)*0x100)
   outputs=[dict(pointer=a['args'][0],hex=b.hex(),native_hex=raw)];value=0
  elif nm=='HeapAlloc':outputs=[dict(pointer=a['value'],hex=r['hex'])];value=a['value'];need(len(bytes.fromhex(r['hex']))==a['args'][2] and a['new_mappings']==[dict(pointer=value,bytes=(a['args'][2]+4095)&~4095)],'all actual allocation input bytes, including uninitialized alignment padding')
  elif nm=='ReadFile':outputs=[dict(pointer=a['memory_outputs'][0]['pointer'],hex=r['after_hex']),dict(pointer=a['args'][3],hex=struct.pack('<I',r['read']).hex())];value=r['value']
  elif nm in ('GetVersionExA','GetCurrentDirectoryA'):outputs=[dict(pointer=a['args'][0 if nm=='GetVersionExA' else 1],hex=r['hex'])];value=r['value']
  elif nm=='CreateFileA':value=0x62001000;need(a['native_handle']==r['handle'],'exact current read-only native file owner')
  elif nm=='HeapCreate':value=0x61001000
  elif nm=='DeleteCriticalSection':value=0
  else:value=r['value']
  need(a['memory_outputs']==outputs and a['value']==value,'every original CRT complete output equals current native bytes')
 constructed=[row['terminal_portrait']['constructed']]+[r['constructed'] for stage in (previous_stage.previous_stage.previous_stage.previous_stage,previous_stage.previous_stage) for r in stage.new_resources(row) if r['kind']=='portrait']
 for b in constructed:
  for x in b['native_allocation_readbacks']:
   i=x['wire_index'];covered.extend((i-1,i));a=ct[i-1];z=ct[i];need(a['request']['op']=='sync' and a['request']['hex']==a['reply']['result']['hex']==x['result']['hex'] and z['request']==dict(id=i+1,op='readback',pointer=x['result']['pointer']) and z['reply']['result']==x['result'] and len(bytes.fromhex(x['result']['hex']))==x['bytes'],'entire original file/vector current native observer and preceding full mirror')
 need(sorted(covered)==list(range(len(ct)-1)),'every current CRT wire classified exactly once')
 # Every opaque owner token is checked by the frozen raw-owner audit; payload
 # masks in its returned comparison view are never used as proof of bytes.
 need(previous.crt_semantics(row)[:d['prefix']['CRT_wire']]==previous.crt_semantics(old)[:d['prefix']['CRT_wire']],'every current fixed-prefix CRT control request and complete initialized data; actual uninitialized inputs independently executed')
 GDI=gdi_native(row,old)
 task_leaves=[x['call'] for x in d['leaves'] if x['kind']=='TASK'];actual=row['task_APIs'][d['prefix']['task_APIs']:];need(len(task_leaves)==len(actual) and all(all(c[k]==value for k,value in a.items()) for c,a in zip(task_leaves,actual)),'each actual current task platform receipt belongs to exactly one original forward leaf')
 need(row['CRT_exit']==row['GPU_exit']==0 and ct[-1]['request']==dict(id=len(ct),op='close') and ct[-1]['reply']['result']==row['CRT_cleanup'] and row['CRT_cleanup']['all_owned_resources_released'] and not row['CRT_cleanup']['forced_cleanup'],'all original current native owners normally closed')
 return dict(current_COM_calls=ci,texture_generations=len(ledger),peak_live_textures=peak,whole_readbacks=readbacks,current_CRT_operations=len(ct)-1,current_GDI_calls=GDI['calls'],GDI_lifetime_audit=GDI,released_native_address_reuse_permitted=True,raw_heap_and_surface_hex_never_address_normalized=True)

def protocol(row):
 d=row['terminal_last_dialogue'];cfg=branch(row['input']['name']);scene=76 if row['input']['name']=='neutral_running' else 77;stream=previous.confirmation.captured_contract()['streams'][scene];bindings=d['bindings'];need(d['branch']==e.branch(row['input']['name']) and len(bindings)==3 and [b['capture'] for b in bindings]==stream['captures'],'separate exact captured76/77 idle/press/release cycle')
 need(len(row['terminal_confirmation']['bindings'])==3,'accepted first cycle never cleared or reused')
 for b in bindings:
  raw=bytes.fromhex(b['capture']['raw_device_hex']);before=bytes.fromhex(b['before_hex']);bound=bytearray(before);bound[12:268]=raw;bp=e.STACK+0xF800
  need(len(raw)==256 and len(before)==0xA00 and b['cycle']=='last_dialogue_confirmation' and b['bound_hex']==bound.hex() and b['after_hex']==predict_keyboard(bytes(bound)).hex(),'every byte of independently updated original A00 keyboard object')
  need(b['only_device_output_written']==dict(pointer=e.KEYBOARD+12,bytes=256) and b['fragment']==dict(va=0x4113D5,bp=bp,sp=bp-0x70,receiver_slot=bp-4,receiver=e.KEYBOARD,stop=0x4116A4),'only raw device output and bounded declared original keyboard fragment')
 need([bytes.fromhex(b['after_hex'])[0x4B9] for b in bindings]==[0,128,0] and [b['segment_index'] for b in bindings]==[0,9,14],'independent new idle/press/release and exact frame interleaving')
 frames=d['frames'];need([f['phase'] for f in frames[:3]]==['held_parent_confirmation','held_parent_confirmation','captured_press'] and [f['phase'] for f in frames[-3:]]==['enter_new_confirmation','held_new_confirmation','held_new_confirmation'],'two parent holds, captured press, new confirmation and two new holds')
 need(vw(d['before']['state'])==(cfg['first_PC'],1) and vw(d['confirmed']['state'])==(cfg['first_PC'],0) and vw(d['ready']['state'])==(cfg['final_PC']-4,0) and vw(d['confirmation']['state'])==vw(d['final']['state'])==(cfg['final_PC'],1),'natural old confirmation release, readiness and next original wait')
 need(bytes.fromhex(d['confirmed']['state']['VM'])==bytes.fromhex(frames[2]['after']['VM']) and read(d['confirmed']['memory'],e.KEYBOARD+0x4B9,1)==bytes([128]),'current task actually consumed captured press')
 for i,f in enumerate(frames):
  need(f['index']==i and f['complete'] is True and f['capture']['state']==f['after'] and f['capture']['queue']==f['queue_after'],'every complete frame has original state/queue and index')
  prior=frames[i-1]['capture'] if i else d['before'];start=frames[i-1]['segments'][1] if i else 0;stop=f['segments'][0];state=prior['state'];queue=prior['queue'];cpu=prior['CPU'];trace=prior['trace'];local=prior['local_trace']
  for b in (b for b in bindings if start<=b['segment_index']<stop):
   offset=e.KEYBOARD-e.MAIN;owner=bytearray.fromhex(state['owner']);need(0<=offset and offset+0xA00<=len(owner) and owner[offset:offset+0xA00].hex()==b['before_hex'] and b['before_CPU']==cpu and b['trace_before']==trace and b['local_before']==local,'complete keyboard bridge starts at exact previous full owner/CPU/trace')
   owner[offset:offset+0xA00]=bytes.fromhex(b['after_hex']);expected=dict(state,owner=owner.hex());need(b['after']['state']==expected and b['after']['queue']==queue,'original keyboard fragment changes only independently predicted A00 within complete owner, with every other state/queue byte preserved');state=b['after']['state'];queue=b['after']['queue'];cpu=b['after']['CPU'];trace=b['after']['trace'];local=b['after']['local_trace']
  need(f['before']==state and f['queue_before']==queue,'continuous full paused task states and queues through exact original keyboard bridges')
  need(f['after']['remaining']==d['before']['state']['remaining'] and f['after']['elapsed']==d['before']['state']['elapsed'],'world remains paused throughout follow-up')
 for f in frames[:2]:need(vw(f['before'])==vw(f['after'])==(cfg['first_PC'],1),'two complete no-input parent holds')
 for f in frames[-2:]:need(vw(f['before'])==vw(f['after'])==(cfg['final_PC'],1),'two complete no-input new confirmation holds')
 need(d['final']['CPU']['EIP']==e.RETURN and d['final']['CPU']['ESP']==e.STACK+0xF004 and read(d['final']['memory'],e.KEYBOARD+0x4B9,1)==bytes(1),'complete original task and released key at the new boundary')
 final=d['final']['memory'];expected_clears=[(7,4,302,306,1)] if cfg['segment']==2 else [(4,7,320,324,1)];need(len(d['clears'])==len(expected_clears),'all and only original clear operations')
 for c,(configuration,layer,start,stop,count) in zip(d['clears'],expected_clears):
  need(c['configuration']==configuration and c['layer']==layer and vw(c['before']['state'])==(start,0) and vw(c['after']['state'])==(stop,0) and c['GPU_wire_before']==c['GPU_wire_after'] and num(read(c['before']['memory'],text_object(layer)+22,2),0,'H')==count and num(read(c['after']['memory'],text_object(layer)+22,2),0,'H')==0,'original44 clears count with no original GPU operation')
  for i in range(3):need(read(c['before']['memory'],text_record(layer,i)+44,4)==read(c['after']['memory'],text_record(layer,i)+44,4),'44 retains every old record pointer')
 replacements=d['replacements'];replacement_count=1 if cfg['segment']==2 else 3;need(len(replacements)==replacement_count,'exact branch-specific actual prior-generation replacements');expected=[]
 for r in new_resources(row):
  old=[q for q in d['resources_before'] if q['alive'] and q['record']==r['record']]
  if old:expected.append((r,old[0]))
 need(len(expected)==replacement_count,'all expected existing current records actually replaced')
 for q,(r,old) in zip(replacements,expected):
  record=r['record'];need((q['entry'],q['caller'],q['record'],q['generation'],q['ledger_index'])==(0x403730,0x4051AE,record,old['generation'],d['resources_before'].index(old)) and q['before']['CPU']['EIP']==0x403730 and q['after']['CPU']['EIP']==0x4051AE and q['return_ESP']==q['before']['CPU']['ESP']+4==q['after']['CPU']['ESP'],'original405160/403730 exact record, generation and natural return')
  need(read(q['before']['memory'],record+44,4)==struct.pack('<I',old['texture']['pointer']) and read(q['after']['memory'],record+44,4)==bytes(4) and [c['op'] for c in q['GPU_APIs']]==['describe','release'] and all(c['generation']==old['generation'] and c['phase']=='forward' for c in q['GPU_APIs']) and q['GPU_APIs'][-1]['wire_index']<r['create_wire_index'] and r['generation']!=old['generation'],'old native generation actually released before same-record creation')
 need(d['role'] is None and d['role_container'] is None,'no new role or file loading in multiline group')
 counts={line['layer']:line['record_index']+1 for line in cfg['lines']}
 for layer,count in counts.items():need(num(read(final,text_object(layer)+22,2),0,'H')==count,'original final per-layer text count')
 need(num(read(final,e.VM+0x1CC,1),0,'B')==cfg['final_layer'],'original final selected layer')
 for r in d['resources']:
  if r['alive']:need(num(read(final,r['record']+44,4),0)==r['texture']['pointer'],'every surviving original record owns its exact generation')
 need(d['accounting']==num(read(final,0x765720,4),0)==row['accounting_baseline']['texture_bytes']+sum(r['size'][0]*r['size'][1]*2 for r in d['resources'] if r['alive']),'all and only live textures accounted')
 return dict(VM_PC=cfg['final_PC'],VM_wait=1,selected_layer=cfg['final_layer'],new_text_indices=[x['text_index'] for x in cfg['lines']],no_input_hold_tasks=2,next44_unexecuted=True)


def final_summary(row):
 d=row['terminal_last_dialogue'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs']);want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'every current final-state page and selected summary field equals independently replayed final full memory');return True

def verify_case(row,old=None):
 prefix_trace(row);provenance,refs=pixels(row);timed=protocol(row);platform=native(row,old);replay=Replay(row,refs);counts=replay.execute();p=prefix(row,old);d=row['terminal_last_dialogue'];equal(row['final'],d['final']['memory'],'every final mapped byte');need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'complete final57 CPU and unchanged original image/IAT')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'full cumulative source digests retained from actual original execution')
 summary=final_summary(row);cleanup=replay.cleanup();facts=dict(full_cumulative=d['final']['trace'],mapped_regions=len(d['final']['memory']),CPU_registers=len(d['final']['CPU']),complete_tasks=(543 if row['input']['name']=='neutral_running' else 546)+len(d['frames']),pending_tasks=0,live_textures=sum(r['alive'] for r in d['resources']),new_textures=[dict(text_index=r['text_index'],record=r['record'],generation=r['generation'],size=r['size'],font_args=r['pending_font']['args'],measured=r['raster']['measured'],nonzero_upload_bytes=sum(b!=0 for b in bytes.fromhex(r['upload_hex']))) for r in new_resources(row) if r['kind']=='text'])
 return dict(name=row['input']['name'],prefix=p,source=provenance,helper=helper_contract(),native=platform,timing=timed,added=counts,cleanup=cleanup,forward_summary=facts,independent_source_image_layout=replay.image_layout,current_terminal_summary_pages_equal_verified_final_memory=summary,independent_whole_memory_CPU_and_new_original_trace=True,no_historical_cleanup_CPU_or_SHA_projection=True)

def fresh_case(case,crt_helper,gpu_helper,ticks):
 need(ticks==accepted_clock_inputs()[case['name']],'fresh full original instance uses exact latest-parent clocks');return e.run_case(case,crt_helper,gpu_helper,ticks)

def verify(path):
 accepted_clock_inputs()
 data=load_report(path)
 need(data['schema_version']==1 and data['source_contract']==e.source_contract() and [r['input'] for r in data['cases']]==e.overlay.parent.corpus(),'exact source contract and both original branches');need(Path(data['helper_build']['GPU']['source']).as_posix()=='tools/terminal_followup_d3d8_platform.cs' and data['helper_build']['GPU']['source_sha256']==helper_contract()['current']['sha256'] and data['helper_build']['GPU']['machine']==0x14C,'actual source build bound to unchanged current capacity10 helper');helpers=e.helpers('terminal-last-dialogue-proof');rows=[]
 for row in data['cases']:
  old=parent_case(row);proof=verify_case(row,old);ticks=[a['result'] for a in old['APIs'] if a['name']=='GetTickCount'];other=None
  try:
   other=fresh_case(row['input'],helpers[0],helpers[1],ticks);verify_case(other,old)
   for key in ('initial','final'):equal(row[key],other[key],'fresh complete '+key+' region')
   for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'fresh original forward/cumulative digest/actual cleanup '+key)
   for key in ('terminal_last_dialogue','last_dialogue_cleanup','last_dialogue_resources_after_cleanup'):need(guest(row[key])==guest(other[key]),'fresh whole memory/57CPU/native inputs/local digests/frames/lifetimes '+key)
  except Exception as error:
   if other is not None:
    diagnostic='analysis/terminal-last-dialogue-diagnostic-fresh-'+row['input']['name']+'-20261029-'+str(time.time_ns())+'.json.gz'
    e.save_source(diagnostic,dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),error_type=type(error).__name__,error=str(error),fresh_original_case=other))
    print('full failed fresh instance preserved locally',diagnostic,flush=True)
   raise
  proof['current_native_resources_recreated']=True;proof['complete_cumulative_digests_reproduced_by_new_full_original_instance']=True;rows.append(proof);print('independent last dialogue',row['input']['name'],'all current resources and original roots verified',flush=True);del other;gc.collect()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,next_confirmation_released=False,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

Replay.execute=bind_replay(previous_stage.Replay.execute)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable multiline proof');e.terminal.save(a.out,verify(ROOT/a.report))
