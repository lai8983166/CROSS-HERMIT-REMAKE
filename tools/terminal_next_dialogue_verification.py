"""Independent original next dialogue, role2 resources and full native ownership."""
import argparse,copy,gc,gzip,hashlib,json,struct,sys,time,types
from functools import lru_cache
from pathlib import Path
from tools import terminal_replacement_verification as previous_stage
from tools import terminal_next_dialogue_emulation as e
from tools.terminal_replacement_verification import (need,num,read,equal,guest,sha,node,text_object,text_record,mark_zero,page_keys,capture_list,text_update,helper_contract,original_text,geometry,convert_surface,bands,NAMES,CRT_IMPORTS,HEAP_BASE,SC001_SHA,SCRIPT_SHA,SimpleNamespace,tls_platform,validate_pages,expand,Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,x86,portrait,source_names)
from tools.school_native_dialogue_verification import predict_keyboard
from tools.terminal_followup_verification import raster_name,NameABI
SC002_SHA="f28023a264a9281a098ded0a595553b488b1412656453c83ba7121f8e0aa9419"
ROLE2_NAME_HEX="ae4cc467"

ROOT=e.ROOT;previous=previous_stage.previous
PARENT_ACCEPTANCE='analysis/terminal-replacement-acceptance-v1-20261028.json'
PARENT_ACCEPTANCE_SHA='c08c51bbcf42e9b47b806ec6c846da8e55492838752c57374a0bfe7969b11df5'
PARENT_SOURCE='analysis/terminal-replacement-source-v2-20261028.json.gz'
PARENT_SOURCE_SHA='5da2c1cb00c57102113e5310ec71a623f86ff31946d5350b81b508913c1c0abd'
PARENT_PROOF='analysis/terminal-replacement-proof-v2-20261028.json'
PARENT_PROOF_SHA='d336834093a4706efd11d68004acf58abb6e21ea649de051aecf641062899980'
IMPLEMENTATIONS=('tools/terminal_next_dialogue_emulation.py','tools/terminal_next_dialogue_verification.py','tools/terminal_next_dialogue_preservation.py','tools/tests/test_terminal_next_dialogue.py','tools/tests/test_terminal_next_dialogue_source.py')
CAPTURE_KEYS=previous_stage.CAPTURE_KEYS
FOLLOWUP_POINTER_DOMAIN='overlay-followup-text-pointer'
FOLLOWUP_BITS_DOMAIN='overlay-followup-text-bits'

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original next dialogue branch');win=name=='neutral_running'
 return dict(segment=2 if win else 11,first_PC=230 if win else 226,final_PC=256 if win else 268,layer=4,text_index=5 if win else 7,text_PC=242 if win else 254,role=None if win else 2)

@lru_cache(maxsize=1)
def parent_report():
 for path,want in ((PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),(PARENT_PROOF,PARENT_PROOF_SHA),(PARENT_SOURCE,PARENT_SOURCE_SHA)):
  h=hashlib.sha256()
  with (ROOT/path).open('rb') as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  need(h.hexdigest()==want,'fixed latest parent '+path)
 return load_report(ROOT/PARENT_SOURCE)

def load_report(path):
 """Share identical immutable strings without changing any decoded value."""
 path=Path(path);pool={}
 def strings(obj):
  for key,value in obj.items():
   if type(value)is str and len(value)>=4096:obj[key]=pool.setdefault(value,value)
  return obj
 opener=gzip.open if path.suffix=='.gz' else open
 with opener(path,'rt',encoding='utf8') as stream:return json.load(stream,object_hook=strings)

def parent_case(row):return next(x for x in parent_report()['cases'] if x['input']==row['input'])

@lru_cache(maxsize=1)
def parent_trace_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed compact parent proof before expensive replay')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def prefix_trace(row):
 name=row['input']['name'];d=row['terminal_next_dialogue'];expected=parent_trace_summaries()[name];actual=d['before']['trace']
 need(actual==expected,'all cumulative parent original instruction/write counters and digests before replay '+name+' expected='+repr(expected)+' actual='+repr(actual))
 need(d['prefix_preflight']==dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual),'source preflight metadata equals independently fixed full cumulative summary')
 return True
def accepted_clock_inputs():return {r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in parent_report()['cases']}
def new_resources(row):
 d=row['terminal_next_dialogue'];return [r for r in d['resources'] if r['create_wire_index']>=d['prefix']['GPU_wire']]
def capture_list(value):
 """Inventory this stage; inherited resource captures retain their old clocks.

 The eight full predecessor resource records are immutable forward evidence
 checked by prefix() and its original predecessor replay. Their old local
 traces must never be relabelled as new replacement-stage captures.
 """
 if isinstance(value,dict) and 'resources' in value and 'resources_before' in value and 'prefix' in value:
  value=dict(value,resources={str(i):r for i,r in enumerate(value['resources']) if r['create_wire_index']>=value['prefix']['GPU_wire']},resources_before=[])
 return previous_stage.previous_stage.capture_list(value)
def gpu_calls(row):
 d=row['terminal_next_dialogue'];return [c for c in previous_stage.gpu_calls(row) if c.get('wire_index',-1)<d['prefix']['GPU_wire']]+d['GPU_APIs']

def gpu_mappings(row):
 allowed={'overlay','overlay-replacement-0','overlay-replacement-1','overlay-next-dialogue-name','overlay-next-dialogue-portrait','overlay-next-dialogue-text',FOLLOWUP_POINTER_DOMAIN,FOLLOWUP_BITS_DOMAIN};out={};keys=set();guests={};aliases=0
 for r in row['typed_GPU_projection']:
  need(set(r)=={'domain','native','guest'} and r['domain'] in allowed and type(r['native']) is int and 0<r['native']<2**32 and type(r['guest']) is int and 0<r['guest']<2**32,'finite typed native ownership entry')
  key=(r['domain'],r['native']);need(key not in keys,'distinct lifetime/native key')
  if r['domain']==FOLLOWUP_BITS_DOMAIN:
   need(r['guest'] in guests and guests[r['guest']]['domain']=='overlay' and aliases==0,'only one declared old-overlay surface guest alias');aliases+=1
  else:need(r['guest'] not in guests,'all other guest identities remain distinct');guests[r['guest']]=r
  keys.add(key);out.setdefault(r['domain'],{})[r['native']]=r['guest']
 need('overlay' in out,'original predecessor projection');return out

def resource_domain(row,r):
 if 'terminal_next_dialogue' not in row:return previous_stage.resource_domain(row,r)
 d=row['terminal_next_dialogue']
 if r['create_wire_index']<d['prefix']['GPU_wire']:return previous_stage.resource_domain(row,r)
 kind=r['kind'];need(kind in ('name','portrait','text'),'finite new kind');cfg=branch(row['input']['name'])
 expected={'name':node(4)+0x60,'text':text_record(4),'portrait':num(read(r['constructed']['memory'],e.MAIN+0x844+30*8,4),0)} if kind=='portrait' else {'name':node(4)+0x60,'text':text_record(4)}
 need(r['record']==expected[kind] and (kind=='text' or cfg['role']==2),'original record and branch creation identity');domain='overlay-next-dialogue-'+kind;need(r['projection_domain']==domain,'domain from independent original resource kind/record');return domain

def bridged_followup_pointer(row,r):
 return row['input']['name']=='timeout_before_combat' and r['kind']=='text' and r['record']==text_record(5) and r['label']=='followup_text' and r['create_wire_index']<row['terminal_replacement']['prefix']['GPU_wire']

def resource_context(row,r,contexts):
 context=contexts[resource_domain(row,r)]
 if bridged_followup_pointer(row,r) and FOLLOWUP_POINTER_DOMAIN in contexts:
  need(set(contexts[FOLLOWUP_POINTER_DOMAIN])=={r['native_pointer']},'one actual old followup texture pointer in isolated lifetime domain')
  context=context|contexts[FOLLOWUP_POINTER_DOMAIN]
  if FOLLOWUP_BITS_DOMAIN in contexts:
   locks=[c for c in r['GPU_APIs'] if c['op']=='lock'];need(len(locks)==1 and set(contexts[FOLLOWUP_BITS_DOMAIN])=={locks[0]['native_result']['bits']},'one actual current followup surface native identity');context=context|contexts[FOLLOWUP_BITS_DOMAIN]
 return context

def legacy_surface_binding(row):
 """Audit the only permitted guest alias against actual released ownership."""
 d=row['terminal_followup'];resources=d['resources'];old=next(r for r in resources if r['label']=='text5');new=next(r for r in resources if r['label']=='followup_text');record=text_record(5)
 need(row['input']['name']=='timeout_before_combat' and old['kind']==new['kind']=='text' and old['record']==new['record']==record and not old['alive'] and new['alive'] and old['release_wire_index']<new['create_wire_index'] and old['generation']!=new['generation'],'original released old record before exactly this new FU creation')
 guest_bits=old['lock']['bits'];size=8192
 need(old['size']==new['size']==[128,32] and old['lock']['pitch']==new['lock']['pitch']==256 and len(bytes.fromhex(old['lock']['hex']))==len(bytes.fromhex(new['lock']['hex']))==size and new['lock']['bits']==guest_bits,'same complete original 128x32 retired guest surface span')
 for r in resources:
  if r['alive'] and r is not new:
   lo=r['lock']['bits'];hi=lo+len(bytes.fromhex(r['lock']['hex']));need(guest_bits+size<=lo or hi<=guest_bits,'no other live resource aliases the retired span')
 trace=row['GPU_trace']
 release=trace[old['release_wire_index']];creation=trace[new['create_wire_index']]
 need(release['request']['op']=='release' and release['request']['pointer']==old['native_pointer'] and release['reply']['result']['count']==0 and creation['request']['op']=='create' and [creation['request']['width'],creation['request']['height']]==[128,32] and creation['reply']['result']['texture']['pointer']==new['native_pointer'],'actual successful original release and same-extent current native creation')
 def lock(r,end):
  matches=[(i,t) for i,t in enumerate(trace) if r['create_wire_index']<i<end and t['request']['op']=='lock' and t['request']['pointer']==r['native_pointer']];need(len(matches)==1,'one actual original LockRect during this creation lifetime');return matches[0]
 old_i,old_t=lock(old,old['release_wire_index']);i,t=lock(new,d['forward_wire_end']);native=t['reply']['result'];need(native['pitch']==256 and len(bytes.fromhex(native['hex']))==size and native['hex']==new['lock']['hex'],'all current actual surface input bytes retained')
 binding=dict(domain=FOLLOWUP_BITS_DOMAIN,native=native['bits'],guest=guest_bits,retired_surface_identity=dict(native=old_t['reply']['result']['bits']),retired_generation=old['generation'],record=record,pitch=256,bytes=size,size=[128,32],retired_release_wire_index=old['release_wire_index'],current_create_wire_index=new['create_wire_index'])
 need(row['terminal_next_dialogue']['historical_surface_alias']==binding,'entire declared alias provenance equals actual original release and native LockRect')
 want=dict(domain=FOLLOWUP_BITS_DOMAIN,native=native['bits'],guest=guest_bits);need([r for r in row['typed_GPU_projection'] if r['domain']==FOLLOWUP_BITS_DOMAIN]==[want],'only this current native surface maps the retired guest span')
 need(dict(domain='overlay',native=old_t['reply']['result']['bits'],guest=guest_bits) in row['typed_GPU_projection'],'retired guest span has exact original overlay native identity')
 return binding

def fixed_projection_role_view(row):
 """Only a platform domain label differs; every guest address still compares.

 Both current native bindings are checked against original retired ownership.
 The explicit extra alias entry represents an already present guest span.
 No guest-memory byte, CPU field or native surface payload is transformed.
 """
 forward=forward_only(row);projection=forward['GPU_projection_before'];ledger=[]
 if any(r['domain']==FOLLOWUP_BITS_DOMAIN for r in projection['ledger']):legacy_surface_binding(row)
 for entry in projection['ledger']:
  if entry['domain']==FOLLOWUP_BITS_DOMAIN:continue
  ledger.append(dict(entry,domain='overlay') if entry['domain']==FOLLOWUP_POINTER_DOMAIN else entry)
 return dict(forward,GPU_projection_before=dict(projection,ledger=ledger))

def forward_only(row):
 d=row['terminal_replacement'];end=row['replacement_cleanup'][0]['leaves'][0];out=dict(d)
 out['leaves']=d['leaves'][:end];out['GPU_APIs']=[c for c in d['GPU_APIs'] if c['wire_index']<d['forward_wire_end']]
 return out

def prefix(row,old=None,replay=True):
 old=parent_case(row) if old is None else old;d=row['terminal_next_dialogue'];p=d['prefix'];before=d['before'];fixed=old['terminal_replacement']['final'];cfg=branch(row['input']['name'])
 for key in ('memory','CPU','state','queue','trace'):need(before[key]==fixed[key]==row['terminal_replacement']['final'][key],'fixed entire replacement boundary '+key)
 need(before['local_trace']==mark_zero() and vw(before['state'])==(cfg['first_PC'],1),'new stage starts at accepted confirmation')
 keys=('initial','input','combat_input','initialization','target_bind','roots','bind_before','bind','bind_after','world_frames','events','commands','hit','hit_sides','contracts','both_hp_writes','calls','ownership','popped','entries','improved','reopened','original_coordinate_writes','action_events','resource_domain','IME_identity','game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization','accounting_baseline','image_before','image_after','resource_loaded','overlay_continuation','after_fade','terminal_name','terminal_portrait','terminal_dialogue','terminal_confirmation','terminal_panel_dialogue','admission')
 for key in keys:
  if key in old:need(guest(row[key])==guest(old[key]),'unchanged earlier forward '+key)
 need(guest(previous_stage.forward_only(row))==guest(previous_stage.forward_only(old)),'entire earlier followup forward')
 need(guest(fixed_projection_role_view(row))==guest(fixed_projection_role_view(old)),'entire latest replacement forward; exact guest values with explicitly bound platform domain role')
 retained=set().union(*(page_keys(old[k]) for k in keys if k in old),page_keys(forward_only(old)),page_keys(previous_stage.forward_only(old)))
 need(all(row['blobs'].get(k)==old['blobs'][k] for k in retained),'all predecessor intermediate pages remain exact')
 need(all(sha(bytes.fromhex(v))==k for k,v in row['blobs'].items()),'all content pages independently rehashed');validate_pages(row,row['blobs'])
 n=sum(a['wire_end']<=old['terminal_replacement']['CRT_forward_wire_end'] for a in old['CRT_APIs']);lengths=dict(CRT_APIs=n,task_APIs=len(old['task_APIs']),resource_steps=len(old['resource_initialization']),task_calls=len(old['task_calls']),task_writes=len(old['task_writes']),APIs=len(old['APIs']))
 for field,n in lengths.items():
  key='resource_initialization' if field=='resource_steps' else field;need(p[field]==n and guest(row[key][:n])==guest(old[key][:n]),'fixed prefix records '+field)
 need(len(row['APIs'])==p['APIs'] and p['extra_counts']==old['extra_original_instruction_counts'],'no new clocks')
 need((p['GPU_wire'],p['CRT_wire'])==(old['terminal_replacement']['forward_wire_end'],old['terminal_replacement']['CRT_forward_wire_end']),'accepted full platform cursors')
 counts=None
 if replay:
  earlier=previous_stage.prefix(row);parent=previous_stage.Replay(row,previous_stage.pixels(row)[1]).execute();counts=dict(earlier=earlier,replacement=parent)
 return dict(fixed_acceptance_sha256=PARENT_ACCEPTANCE_SHA,fixed_source_sha256=PARENT_SOURCE_SHA,fixed_proof_sha256=PARENT_PROOF_SHA,parent_full_memory_CPU_queue_and_trace_equal=True,independent_current_parent_forward=counts,no_historical_cleanup_projection=True)

def source(row):
 d=row['terminal_next_dialogue'];cfg=branch(row['input']['name']);raw=(ROOT/e.terminal.SCRIPT_PATH).read_bytes();need(sha(raw)==SCRIPT_SHA,'whole original T0004 identity');segment=next(s for s in previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);at=segment['code_start'];pc=cfg['first_PC'];base=num(read(d['before']['memory'],e.VM+16,4),0);commands=[]
 expected=[(230,43,8),(238,44,4),(242,17,6),(248,50,4),(252,51,4)] if cfg['role'] is None else [(226,30,20),(246,43,8),(254,17,6),(260,50,4),(264,51,4)]
 for want in expected:
  op,n=struct.unpack_from('<HH',raw,at+pc);need((pc,op,n)==want and read(d['before']['memory'],base+pc,n)==raw[at+pc:at+pc+n],'every original next command byte/declared length');commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
 need(pc==cfg['final_PC'] and d['commands']==commands and struct.unpack_from('<HHI',raw,at+pc)==(43,8,0x20000004),'next config4 unexecuted')
 if cfg['role'] is not None:need(struct.unpack_from('<4I',raw,at+230)==tuple(0x20000000+x for x in (7,2,0,30)),'all four original role2 literal parameters')
 config_pc=246 if cfg['role'] else 230;need(num(raw,at+config_pc+4)==0x20000007 and num(raw,at+cfg['text_PC']+4,'H')==cfg['text_index'],'original config7 and text index')
 config=list(struct.unpack_from('<19h',e.CODE,0x624520-0x400000+7*38));need(config[0]==4,'original config7 selects layer4')
 end=segment['code_end'];packed=num(raw,end+4+cfg['text_index']*4);span=packed>>20;off=end+(packed&0xFFFFF);text=raw[off:off+span];need(len(text)==span and 2<=span<=512 and span%2==0 and text[-2:]==bytes(2) and 0 not in text[:-2] and (off,text[:-2].hex())==((1306 if cfg['role'] is None else 3444),'a14ba14ba14ba14b'),'entire exact original ANSI text')
 need(e.ALLOWED==previous_stage.e.ALLOWED and e.NextDialogueMachine.source_code.__code__ is previous_stage.e.ReplacementMachine.source_code.__code__,'no additional guest code or changed original source guard')
 return dict(segment=cfg['segment'],script_sha256=SCRIPT_SHA,commands=commands,final_PC=pc,next_opcode=43,selected_layer=4,text=dict(index=cfg['text_index'],source_offset=off,hex=text[:-2].hex()),configuration=config)

def pixels(row):
 d=row['terminal_next_dialogue'];cfg=branch(row['input']['name']);provenance=source(row);catalog,_=source_names();refs={}
 for r in new_resources(row):
  if r['kind']=='portrait':
   entry=catalog['roles']['2'];raw=(ROOT/entry['image_path']).read_bytes();need(len(raw)==262168 and sha(raw)==SC002_SHA==entry['image_sha256'],'entire original SC002 identity')
   need(r['upload_hex']==r['readback']['hex']==raw[24:].hex() and r['readback']['sha256']==sha(raw[24:]),'every original SC002 texel equals actual complete current readback')
   need(len(r['copy_rows'])==512,'all512 original portrait copy calls')
   for i,c in enumerate(r['copy_rows']):need(c==dict(row=i,args=[r['lock']['bits']+i*512,r['constructed']['file_pointer']+24+i*512,512],caller=0x40483F),'original full row copy ABI')
   need(r['lock']['pitch']==512 and len(bytes.fromhex(r['lock']['hex']))==262144,'whole native portrait lock extent');refs[r['generation']]=dict(portrait=raw);continue
  need(r['kind'] in ('name','text'),'known new source resource kind')
  b=r['font_boundary'];sp=b['CPU']['ESP'];args=[num(read(b['memory'],sp+4+i*4,4),0) for i in range(14)];caller=0x4CA7CB if r['kind']=='name' else 0x4CAD09
  need(r['pending_font']==dict(entry=num(read(b['memory'],0x5920A0,4),0),caller=caller,args=args,CPU=b['CPU'],first_instruction_executed=False) and b['CPU']['EIP']==r['pending_font']['entry'] and num(read(b['memory'],sp,4),0)==caller,'whole original live font ABI and unexecuted entry')
  if r['kind']=='name':
   raw=original_text(catalog['roles']['2']['name_pointer']);need(raw.hex()==ROLE2_NAME_HEX and args==[20,0,0,0,700,0,0,0,1,5,0,0,0,0x5BF62C],'source role1 name and original height20/weight700 font')
   reference=raster_name(raw,args[:-1],original_text(args[-1]));need(r['record']==node(4)+0x60,'source new layer4 name record')
  else:
   raw=bytes.fromhex(provenance['text']['hex']);obj=read(b['memory'],text_object(cfg['layer']),0x18);alt=bool(obj[0x14]);width=num(obj,0xE if alt else 0xC,'h')&0xFFFFFFFF;height=num(obj,0x12 if alt else 0x10,'h')&0xFFFFFFFF
   need(args==[height,width,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C] and r['record']==text_record(cfg['layer']) and r['record_index']==0 and r['text_index']==cfg['text_index'],'original text font fields and count-derived record, not template font-size')
   reference=previous.dialogue.raster_dialogue(raw,args[:-1],original_text(args[-1]))
  raster=r['raster'];g=geometry(reference['measured']);need(r['geometry']==g and (raster['ACP'],raster['measured'],raster['selected_face'],raster['raster_hex'])==(reference['ACP'],reference['measured'],reference['selected_face'],reference['raster_hex']),'independent actual original glyph metrics/face/all DIB bytes')
  need([a['name'] for a in raster['stages']]==['PatBlt','TextOutA','TextOutA'] and [a['hex'] for a in raster['stages']]==[a['hex'] for a in reference['stages']],'all three independent original clear/shadow/foreground surfaces')
  need([a['name'] for a in r['calls']]==NAMES+['SelectObject','DeleteObject','DeleteDC','DeleteObject'] and raster['calls']==r['calls'][:23],'all27 original per-resource GDI calls and natural cleanup')
  lock=r['lock'];w,h=[1<<(v-1).bit_length() for v in g['texture_size']];out=bytes.fromhex(lock['hex']);need(lock['pitch']==w*2 and len(out)==w*h*2,'whole actual current lock input, including undefined initial padding')
  expected=bands(g);need([dict(rect=c['rect'],point=c['point']) for c in r['conversions']]==expected,'original complete conversion band geometry')
  for band in expected:out=convert_surface(bytes.fromhex(reference['raster_hex']),g['raster_size'],band['rect'],out,lock['pitch'],band['point'])
  need(r['upload_hex']==r['readback']['hex']==out.hex() and r['readback']['sha256']==sha(out) and r['readback']['pitch']==lock['pitch'],'every independently converted texel, preserving actual untouched initial bytes')
  refs[r['generation']]=dict(reference=reference,geometry=g)
 need(sorted(r['kind'] for r in new_resources(row))==(['name','portrait','text'] if cfg['role'] else ['text']),'exact new resource set per original branch')
 return provenance,refs

def bind_replay(fn):
 """Reuse frozen independent engine, replacing only report routing strings.

 No guest instructions, API outputs, numeric addresses or trace values change.
 """
 routing={'terminal_followup':'terminal_next_dialogue','followup_cleanup':'next_dialogue_cleanup'}
 def constants(code):
  def value(v):
   if isinstance(v,types.CodeType):return constants(v)
   if fn.__name__=='__init__':
    if type(v)is str and v=='1':return '2'
    if type(v)is str and v=='data\\adv\\bin\\sc001.bin':return 'data\\adv\\bin\\sc002.bin'
    if type(v)is bytes and v==b'data\\adv\\bin\\sc001.bin':return b'data\\adv\\bin\\sc002.bin'
   return routing.get(v,v) if type(v)is str else v
  return code.replace(co_consts=tuple(value(v) for v in code.co_consts),co_names=tuple('SC002_SHA' if fn.__name__=='__init__' and n=='SC001_SHA' else n for n in code.co_names))
 scope=dict(fn.__globals__,**globals())
 if fn.__name__=='execute':scope['need']=replay_need
 if fn.__name__=='__init__':scope['Uc']=source_image_uc
 return types.FunctionType(constants(fn.__code__),scope,closure=fn.__closure__)

def replay_need(ok,message):
 if ok:return
 local=sys._getframe(1).f_locals;machine=local.get('self');segment=local.get('s',{});diagnostic=dict(schema_version=1,error=message)
 if machine is not None:
  actual=machine.cpu();expected=segment.get('CPU',{});mark=local.get('mark')
  diagnostic.update(case=machine.row['input']['name'],segment_index=local.get('i'),segment={k:segment.get(k) for k in ('label','kind','entry','stop','root')},actual_CPU=actual,expected_CPU=expected,CPU_differences={k:dict(actual=actual.get(k),expected=expected.get(k)) for k in actual.keys()|expected.keys() if actual.get(k)!=expected.get(k)},actual_mark=mark() if callable(mark) else None,expected_mark=segment.get('local_after'),actual_leaf_cursor=local.get('index'),expected_leaf_cursor=segment.get('leaves'),original_segments_unchanged=True)
 path=ROOT/('analysis/terminal-next-dialogue-replay-diagnostic-'+str(time.time_ns())+'-20261028.json')
 with path.open('x',encoding='utf8',newline='\n') as out:json.dump(diagnostic,out,separators=(',',':'));out.write('\n')
 need(False,message+'; diagnostic='+path.relative_to(ROOT).as_posix())

def native(row,old=None):
 """Audit current receipts by creation ordinal, with no byte identity masks."""
 d=row['terminal_next_dialogue'];old=parent_case(row) if old is None else old;helper_contract();contexts=gpu_mappings(row);m=contexts['overlay'];gt=row['GPU_trace'];ct=row['CRT_trace'];ledger=row['next_dialogue_resources_after_cleanup'];by_create={r['create_wire_index']:r for r in ledger};by_gen={r['generation']:r for r in ledger}
 need(set(contexts)=={'overlay','overlay-replacement-0','overlay-replacement-1','overlay-next-dialogue-text'}|({'overlay-next-dialogue-name','overlay-next-dialogue-portrait',FOLLOWUP_POINTER_DOMAIN,FOLLOWUP_BITS_DOMAIN} if branch(row['input']['name'])['role'] else set()),'exact inherited, bridged pointer/surface and new resource lifetimes')
 if branch(row['input']['name'])['role']:legacy_surface_binding(row)
 else:need(d['historical_surface_alias'] is None,'victory has no retired surface alias')
 projection=row['typed_GPU_projection'];prefix_rows=[r for r in projection if not r['domain'].startswith('overlay-next-dialogue-')];ordinal_rows=[r for r in prefix_rows if r['domain']!=FOLLOWUP_BITS_DOMAIN];first=0x64001000+len(ordinal_rows)*0x100000
 need(first<=0x66601000 and d['GPU_projection_before']==dict(next=first,ledger=prefix_rows) and projection[:len(prefix_rows)]==prefix_rows and d['GPU_projection']==projection[len(prefix_rows):],'complete ordered preserved parent domains and explicit new ledger')
 parent_prefix=[r for r in prefix_rows if r['domain'] in ('overlay',FOLLOWUP_POINTER_DOMAIN,FOLLOWUP_BITS_DOMAIN)];parent_projection=row['terminal_replacement']
 need(parent_projection['GPU_projection_before']==dict(next=0x64001000+sum(r['domain']!=FOLLOWUP_BITS_DOMAIN for r in parent_prefix)*0x100000,ledger=parent_prefix) and parent_projection['GPU_projection']==[r for r in prefix_rows if r['domain'] in ('overlay-replacement-0','overlay-replacement-1')],'entire actual predecessor projection metadata bound to current native ledger, including declared pointer/surface bindings')
 need([r['guest'] for r in ordinal_rows]==[0x64001000+i*0x100000 for i in range(len(ordinal_rows))],'all predecessor new allocations retain exact ordinals; explicit retired-span alias adds no slot')
 def interface_ids(v):return [v['pointer'],v['vtable']]+list(v['methods'].values())
 oldledger=row['replacement_resources_after_cleanup'];identities={k:set() for k in contexts if not k.startswith('overlay-next-dialogue-')};identities['overlay'].update(interface_ids(row['current_GPU_hello']['device']))
 for r in oldledger:
  domain=resource_domain(row,r);create=gt[r['create_wire_index']]['reply']['result']['texture'];ids=interface_ids(create)
  bridged=bridged_followup_pointer(row,r)
  if bridged:identities[FOLLOWUP_POINTER_DOMAIN].add(ids.pop(0))
  identities[domain].update(ids);bits=next(t['reply']['result']['bits'] for i,t in enumerate(gt) if r['create_wire_index']<i<=r['release_wire_index'] and t['request']['op']=='lock' and t['request']['pointer']==r['native_pointer']);identities[FOLLOWUP_BITS_DOMAIN if bridged else domain].add(bits)
 for domain,values in identities.items():need(set(contexts[domain])==values,'all inherited identities tied to actual creation/lock/device wire')
 for index,r in enumerate(new_resources(row)):
  domain=resource_domain(row,r);native_texture=gt[r['create_wire_index']]['reply']['result']['texture'];lock=next(c['native_result'] for c in r['GPU_APIs'] if c['op']=='lock');need(list(native_texture['methods'])==['8','56','64','68'],'original texture ABI')
  sequence=interface_ids(native_texture)+[lock['bits']];need(len(sequence)==len(set(sequence))==7,'seven actual identities per new creation')
  need([v for v in projection if v['domain']==domain]==[dict(domain=domain,native=p,guest=first+(7*index+j)*0x100000) for j,p in enumerate(sequence)],'independent new generation allocation sequence')
 need(first+7*len(new_resources(row))*0x100000<=0x67B01000<0x6A001000,'bounded GPU namespace below current GDI identities')
 need(row['current_CRT_hello']['pointer_bytes']==row['current_GPU_hello']['pointer_bytes']==4 and row['current_GPU_hello']['window_visible'] is False and row['current_GPU_hello']['image_size']==[512,512] and row['current_CRT_hello']['GPU_created'] is False,'actual bounded headless x86 CRT/GPU owners')
 need(len(by_create)==len(by_gen)==len(ledger)==(11 if branch(row['input']['name'])['role'] is None else 13),'every old and new creation generation')
 need(len(d['resources'])==len(ledger) and len(d['resources_before'])==10,'complete eight-generation prefix and two new text generations')
 need(d['resources_before']==row['terminal_replacement']['resources'],'each seeded generation bound to complete actual parent ledger, including already retired timeout text5')
 for before,after in zip(d['resources_before'],d['resources'][:10]):
  for k,v in before.items():
   if k not in ('alive','release_wire_index','released_phase','alive_after_forward'):need(after[k]==v,'unchanged original seeded metadata '+k)
  if not before['alive']:need(all(after.get(k)==before.get(k) for k in ('alive','release_wire_index','released_phase')),'an already retired generation never revived or released twice')
 need(d['GPU_APIs']==[x['call'] for x in d['leaves'] if x['kind']=='GPU'] and d['calls']==[x['call'] for x in d['leaves'] if x['kind']=='GDI'] and row['CRT_APIs'][d['prefix']['CRT_APIs']:]==[x['call'] for x in d['leaves'] if x['kind']=='CRT'],'every original platform leaf belongs once to its full current receipt ledger')
 for r in new_resources(row):
  a,z=r['leaves'];leaves=d['leaves'][a:z];need(0<=a<z<=row['next_dialogue_cleanup'][0]['leaves'][0] and r['GPU_APIs']==[x['call'] for x in leaves if x['kind']=='GPU'] and r['calls']==[x['call'] for x in leaves if x['kind']=='GDI'] and r['conversions']==[c for c in d['conversions'] if c['resource_label']==r['label']],'complete actual original resource leaf/conversion interval')
 live={};logical={};ci=readbacks=peak=0;calls=gpu_calls(row);observers={o['wire_index']:o for o in d['readback_observers']}
 need(len(observers)==len(d['readback_observers']),'every current follow-up observer classified once')
 for label,tr in (('GPU',gt),('CRT',ct)):
  for i,t in enumerate(tr):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok'] is True,'complete ordered successful actual '+label+' wire')
 oldcontexts=gpu_mappings(old);oldledger=old['replacement_resources_after_cleanup']
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
 need(ci==len(calls) and peak==(9 if row['input']['name']=='neutral_running' else 10),'all original COM calls and exact bounded simultaneous texture peak')
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
 constructed=[row['terminal_portrait']['constructed']]+[r['constructed'] for r in previous_stage.previous_stage.new_resources(row) if r['kind']=='portrait']+[r['constructed'] for r in new_resources(row) if r['kind']=='portrait']
 for b in constructed:
  for x in b['native_allocation_readbacks']:
   i=x['wire_index'];covered.extend((i-1,i));a=ct[i-1];z=ct[i];need(a['request']['op']=='sync' and a['request']['hex']==a['reply']['result']['hex']==x['result']['hex'] and z['request']==dict(id=i+1,op='readback',pointer=x['result']['pointer']) and z['reply']['result']==x['result'] and len(bytes.fromhex(x['result']['hex']))==x['bytes'],'entire original file/vector current native observer and preceding full mirror')
 need(sorted(covered)==list(range(len(ct)-1)),'every current CRT wire classified exactly once')
 # Every opaque owner token is checked by the frozen raw-owner audit; payload
 # masks in its returned comparison view are never used as proof of bytes.
 need(previous.crt_semantics(row)[:d['prefix']['CRT_wire']]==previous.crt_semantics(old)[:d['prefix']['CRT_wire']],'every current fixed-prefix CRT control request and complete initialized data; actual uninitialized inputs independently executed')
 blocks=[row['terminal_name'],row['terminal_dialogue']]+row['terminal_panel_dialogue']['sentences']+[r for r in previous_stage.previous_stage.new_resources(row) if r['kind'] in ('name','text')]+[r for r in previous_stage.new_resources(row) if r['kind'] in ('name','text')]+[r for r in new_resources(row) if r['kind'] in ('name','text')];gm={x['guest']:x['native'] for x in d['GDI_handle_projection']}
 need(len(gm)==len(d['GDI_handle_projection']) and len(set(gm.values()))==len(gm) and all(x['domain']=='GDI' for x in d['GDI_handle_projection']),'unambiguous complete current GDI owner ledger')
 flat=[];traces=[];GDI_index=0
 for b in blocks:
  need(len(b['calls'])==len(b['GDI_trace'])==27,'every actual original GDI call has current receipt')
  for c,t in zip(b['calls'],b['GDI_trace']):
   if 'GDI_trace_index' in c:need(c['GDI_trace_index']==GDI_index,'actual absolute current GDI receipt ordinal')
   GDI_index+=1
   args=c['args'];nm=c['name'];na=list(args)
   if nm not in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):na[0]=gm[args[0]]
   if nm=='SelectObject':na[1]=gm[args[1]]
   result=gm[c['result']] if nm in ('CreateFontA','CreateCompatibleDC','CreateDIBSection','GetStockObject','SelectObject') else c['result'];nr=t['native_result'];need(t['name']==nm and t['args']==args and t['native_args']==nr['args']==na and t['logical_result']==c['result'] and nr['result']==result and c['actual_API_executed'] is True,'complete current GDI native ABI, outputs and typed handle owner')
   output=copy.deepcopy(nr);output.pop('dc_translated_args',None);output.pop('native_bits',None);output.update(args=args,result=c['result'],actual_API_executed=True);need(all(c[k]==v for k,v in output.items()),'every actual current GDI output preserved')
  if b in new_resources(row):flat+=b['calls'];traces+=b['GDI_trace']
 need(flat==d['calls'] and traces==d['GDI_trace'],'nonduplicated complete new GDI ledger')
 task_leaves=[x['call'] for x in d['leaves'] if x['kind']=='TASK'];actual=row['task_APIs'][d['prefix']['task_APIs']:];need(len(task_leaves)==len(actual) and all(all(c[k]==value for k,value in a.items()) for c,a in zip(task_leaves,actual)),'each actual current task platform receipt belongs to exactly one original forward leaf')
 need(row['CRT_exit']==row['GPU_exit']==0 and ct[-1]['request']==dict(id=len(ct),op='close') and ct[-1]['reply']['result']==row['CRT_cleanup'] and row['CRT_cleanup']['all_owned_resources_released'] and not row['CRT_cleanup']['forced_cleanup'],'all original current native owners normally closed')
 return dict(current_COM_calls=ci,texture_generations=len(ledger),peak_live_textures=peak,whole_readbacks=readbacks,current_CRT_operations=len(ct)-1,current_GDI_calls=sum(len(b['calls']) for b in blocks),released_native_address_reuse_permitted=True,raw_heap_and_surface_hex_never_address_normalized=True)

SOURCE_IMAGE_BASE=0x400000
# Source RegionRouting/animation/hit/aftermath/world/terminal/CRT constructors.
SOURCE_IMAGE_WRITABLE=((0x7A3000,0x2000),(0x765000,0x2D000),(0x761000,0x1000),(0x618000,0x1000),(0x7F4000,0x2000),(0x7A2000,0x1000),(0x7D7000,0x1D000),(0x7F6000,0x8000),(0x7A0000,0x1000),(0x79F000,0x1000),(0x762000,0x1000),(0x80A000,0x1000))

def source_image_partitions(memory):
 end=SOURCE_IMAGE_BASE+((len(e.CODE)+4095)&~4095);regions=sorted((r['pointer'],r['bytes']) for r in memory if r['pointer']<end and SOURCE_IMAGE_BASE<r['pointer']+r['bytes']);cursor=SOURCE_IMAGE_BASE;out=[]
 for address,size in regions:
  need(address==cursor and address%4096==size%4096==0 and size>0 and address+size<=end,'complete disjoint original image snapshot partitions')
  overlaps=[(p,n) for p,n in SOURCE_IMAGE_WRITABLE if p<address+size and address<p+n]
  need(not overlaps or any(p<=address and address+size<=p+n for p,n in overlaps),'snapshot retains source image permission boundaries')
  out.append((address,size,3 if overlaps else 5));cursor=address+size
 need(cursor==end,'entire original image covered without invented regions');return out

def source_image_uc(architecture,mode):
 need((architecture,mode)==(UC_ARCH_X86,UC_MODE_32),'original x86 source architecture')
 engine=Uc(architecture,mode);mapping=engine.mem_map;end=SOURCE_IMAGE_BASE+((len(e.CODE)+4095)&~4095)
 # Source maps the complete image once before any other guest RAM, then uses
 # mem_protect to partition it. Mapping each snapshot fragment separately loses
 # this RAM backing topology and can introduce pre-commit REP/SMC hook retries.
 mapping(SOURCE_IMAGE_BASE,end-SOURCE_IMAGE_BASE)
 def snapshot_map(address,size,perms=7):
  if SOURCE_IMAGE_BASE<=address and address+size<=end:return
  return mapping(address,size,perms)
 engine._original_snapshot_map=mapping;engine.mem_map=snapshot_map;return engine

class Replay(previous_stage.Replay):
 _initialize=bind_replay(previous_stage.previous_stage.Replay.__init__)
 def __init__(self,row,refs):
  partitions=source_image_partitions(row['terminal_next_dialogue']['before']['memory']);self._initialize(row,refs)
  self.u.mem_map=self.u._original_snapshot_map;del self.u._original_snapshot_map
  self.u.mem_protect(SOURCE_IMAGE_BASE,(len(e.CODE)+4095)&~4095,5)
  for address,size in SOURCE_IMAGE_WRITABLE:self.u.mem_protect(address,size,3)
  for address,size,perms in partitions:self.u.mem_protect(address,size,perms)
  self.image_layout=dict(complete_image_mapped_first=True,one_original_image_RAM_backing=True,source_RX_RW_permissions=True,snapshot_partitions_preserved=True,original_events_filtered=False)
 execute=bind_replay(previous_stage.previous_stage.Replay.execute)
 def crt_leaf(self,call):
  before=self.cpu();super().crt_leaf(call);expected=dict(before,EAX=call['value'],ESP=call['sp']+4+call['pop'],EIP=call['return_va'])
  need(self.cpu()==expected,'independent CRT leaf preserves every recorded non-return register '+call['name'])
  for output in call['memory_outputs']:need(self.read(output['pointer'],len(bytes.fromhex(output['hex']))).hex()==output['hex'],'independent CRT leaf writes exact current captured output '+call['name'])
 def cleanup(self):
  d=self.d;rows=self.row['next_dialogue_cleanup'];steps=self.row['cleanup_steps'];keys=('label','entry','args','receiver','cdecl');old=parent_case(self.row);expected=[{k:s[k] for k in keys} for s in old['cleanup_steps']]
  if self.row['input']['name']=='timeout_before_combat':expected=[dict(label='supplemental_original_next_dialogue_text_destructor',entry=0x403730,args=[],receiver=text_record(4),cdecl=False),dict(label='supplemental_original_next_dialogue_portrait_container_destructor',entry=0x41F4E0,args=[30],receiver=e.MAIN+0x844,cdecl=False),dict(label='supplemental_original_next_dialogue_name_destructor',entry=0x403730,args=[],receiver=node(4)+0x60,cdecl=False)]+expected
  need([{k:r[k] for k in keys} for r in rows]==expected==[{k:s[k] for k in keys} for s in steps],'only actual new resources then inherited original teardown roots/args, without old CPU projection');self.cleaning=True;index=self.forward_end;total_i=total_w=0;ih=hashlib.sha256();wh=hashlib.sha256();last=d['final']['trace']
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


vw=previous_stage.vw

def protocol(row):
 d=row['terminal_next_dialogue'];cfg=branch(row['input']['name']);scene=76 if row['input']['name']=='neutral_running' else 77;stream=previous.confirmation.captured_contract()['streams'][scene];bindings=d['bindings'];need(d['branch']==e.branch(row['input']['name']) and len(bindings)==3 and [b['capture'] for b in bindings]==stream['captures'],'separate exact captured76/77 idle/press/release cycle')
 need(len(row['terminal_confirmation']['bindings'])==3,'accepted first cycle never cleared or reused')
 for b in bindings:
  raw=bytes.fromhex(b['capture']['raw_device_hex']);before=bytes.fromhex(b['before_hex']);bound=bytearray(before);bound[12:268]=raw;bp=e.STACK+0xF800
  need(len(raw)==256 and len(before)==0xA00 and b['cycle']=='next_dialogue_confirmation' and b['bound_hex']==bound.hex() and b['after_hex']==predict_keyboard(bytes(bound)).hex(),'every byte of independently updated original A00 keyboard object')
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
 final=d['final']['memory'];need(num(read(final,text_object(cfg['layer'])+22,2),0,'H')==1 and num(read(final,e.VM+0x1CC,1),0,'B')==cfg['layer'],'original selected target retains exactly one new text record')
 if cfg['role']:
  need(d['clear'] is None and not d['replacements'] and d['role_container']==portrait.parse((ROOT/source_names()[0]['roles']['2']['image_path']).read_bytes()),'win appends role resources without clearing or replacing old text')
  role=d['role'];p=role['pending_image'];catalog=source_names()[0]['roles']['2'];q=next(r for r in new_resources(row) if r['kind']=='portrait');need(role['role']==2 and role['configuration']==7 and role['node']==node(4) and role['name_record']==node(4)+0x60 and role['source']==catalog,'entire original role1 and configuration7 provenance')
  need(p['entry']==0x4CDE10 and p['receiver']==e.VM and p['caller']==0x4CC0D2 and p['CPU']['EIP']==p['entry'] and p['first_instruction_executed'] is False and p['path']=='data\\adv\\bin\\sc002.bin' and p['group_words']==[30,31] and p['side_byte']==0 and p['side_pointer']==node(4)+0x32 and p['side_getter']==0x4CA9B0 and p['args'][1]==30,'actual first side getter and original2*layer+22/+23 formula select registered group30')
  n=bytes.fromhex(p['node_hex']);need(list(struct.unpack_from('<2H',n,0x40))==p['group_words'] and n[0x32]==p['side_byte'] and q['label']=='portrait30' and q['constructed']['file_hex']==(ROOT/catalog['image_path']).read_bytes().hex() and q['constructed']['bank_hex']==struct.pack('<II',q['record'],1).hex(),'actual new side bank and complete original file at natural constructor boundary')
  readiness=[f for f in frames if f['phase']=='role_readiness'];need(role['readiness_frames']==len(readiness)==77 and role['name_resource_label']==next(r['label'] for r in new_resources(row) if r['kind']=='name') and vw(role['ready']['state'])==(246,0),'strict original delay/fade/background readiness requires77 complete tasks')
  for f in readiness:
   a=bytes.fromhex(f['before']['VM'])[node(4)-e.VM:];z=bytes.fromhex(f['after']['VM'])[node(4)-e.VM:];mode,fade,delay,bg,bgcount=[num(a,o,'H') for o in (2,6,18,34,36)];need([num(a,o,'H') for o in (16,20,38)]==[45,30,60],'original independent role timing limits')
   ready=mode not in range(3,8) and bg not in range(3,9)
   if mode==6:
    delay+=1
    if delay>30:delay=0;mode=3
   elif mode==3:
    fade+=1
    if fade>45:fade=0;mode=2
   if bg==3:
    old_count=bgcount;bgcount+=1
    if old_count>60:bgcount=0;bg=2
   need([num(z,o,'H') for o in (2,6,18,34,36)]==[mode,fade,delay,bg,bgcount] and vw(f['after'])==(246,0 if ready else 1),'independent role strict-counter transition and pre-update readiness')
 else:
  need(d['role'] is None and d['role_container'] is None and len(d['replacements'])==1,'timeout uses only original44 and same-record text replacement');clear=d['clear'];record=text_record(4);old=next(r for r in d['resources_before'] if r['record']==record and r['alive']);replacement=d['replacements'][0];new=next(r for r in new_resources(row) if r['kind']=='text')
  need(vw(clear['before']['state'])==(238,0) and vw(clear['after']['state'])==(242,0) and clear['GPU_wire_before']==clear['GPU_wire_after'] and num(read(clear['before']['memory'],text_object(4)+22,2),0,'H')==1 and num(read(clear['after']['memory'],text_object(4)+22,2),0,'H')==0 and read(clear['before']['memory'],record+44,4)==read(clear['after']['memory'],record+44,4)==struct.pack('<I',old['texture']['pointer']),'original44 clears count without GPU release or texture-pointer rewrite')
  need((replacement['entry'],replacement['caller'],replacement['record'],replacement['generation'],replacement['ledger_index'])==(0x403730,0x4051AE,record,old['generation'],d['resources_before'].index(old)) and replacement['before']['CPU']['EIP']==0x403730 and replacement['after']['CPU']['EIP']==0x4051AE and replacement['return_ESP']==replacement['before']['CPU']['ESP']+4==replacement['after']['CPU']['ESP'],'original405160 calls its own403730 and returns naturally before text raster')
  need(read(replacement['before']['memory'],record+44,4)==struct.pack('<I',old['texture']['pointer']) and read(replacement['after']['memory'],record+44,4)==bytes(4) and [c['op'] for c in replacement['GPU_APIs']]==['describe','release'] and all(c['generation']==old['generation'] and c['phase']=='forward' for c in replacement['GPU_APIs']) and replacement['GPU_APIs'][-1]['wire_index']<new['create_wire_index'] and new['record']==record and new['generation']!=old['generation'],'old generation released by original forward destructor before same-record new texture')
 for r in d['resources']:
  if r['alive']:need(num(read(final,r['record']+44,4),0)==r['texture']['pointer'],'every retained current record owns its correct live generation')
 need(d['accounting']==num(read(final,0x765720,4),0)==row['accounting_baseline']['texture_bytes']+sum(r['size'][0]*r['size'][1]*2 for r in d['resources'] if r['alive']),'all and only simultaneously live textures are accounted')
 return dict(VM_PC=cfg['final_PC'],VM_wait=1,selected_layer=cfg['layer'],new_text_index=cfg['text_index'],role=cfg['role'],actual_group=30 if cfg['role'] else None,no_input_hold_tasks=2,next43_unexecuted=True)

def final_summary(row):
 d=row['terminal_next_dialogue'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs']);want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'every current final-state page and selected summary field equals independently replayed final full memory');return True

def verify_case(row,old=None):
 prefix_trace(row);provenance,refs=pixels(row);timed=protocol(row);platform=native(row,old);replay=Replay(row,refs);counts=replay.execute();p=prefix(row,old);d=row['terminal_next_dialogue'];equal(row['final'],d['final']['memory'],'every final mapped byte');need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'complete final57 CPU and unchanged original image/IAT')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'full cumulative source digests retained from actual original execution')
 summary=final_summary(row);cleanup=replay.cleanup();facts=dict(full_cumulative=d['final']['trace'],mapped_regions=len(d['final']['memory']),CPU_registers=len(d['final']['CPU']),complete_tasks=(449 if row['input']['name']=='neutral_running' else 396)+len(d['frames']),pending_tasks=0,live_textures=sum(r['alive'] for r in d['resources']),new_textures=[dict(text_index=r['text_index'],record=r['record'],generation=r['generation'],size=r['size'],font_args=r['pending_font']['args'],measured=r['raster']['measured'],nonzero_upload_bytes=sum(b!=0 for b in bytes.fromhex(r['upload_hex']))) for r in new_resources(row) if r['kind']=='text'])
 return dict(name=row['input']['name'],prefix=p,source=provenance,helper=helper_contract(),native=platform,timing=timed,added=counts,cleanup=cleanup,forward_summary=facts,independent_source_image_layout=replay.image_layout,current_terminal_summary_pages_equal_verified_final_memory=summary,independent_whole_memory_CPU_and_new_original_trace=True,no_historical_cleanup_CPU_or_SHA_projection=True)

def fresh_case(case,crt_helper,gpu_helper,ticks):
 need(ticks==accepted_clock_inputs()[case['name']],'fresh full original instance uses exact latest-parent clocks');return e.run_case(case,crt_helper,gpu_helper,ticks)

def verify(path):
 accepted_clock_inputs()
 data=load_report(path)
 need(data['schema_version']==1 and data['source_contract']==e.source_contract() and [r['input'] for r in data['cases']]==e.overlay.parent.corpus(),'exact source contract and both original branches');helpers=e.helpers('terminal-next-dialogue-proof');rows=[]
 for row in data['cases']:
  old=parent_case(row);proof=verify_case(row,old);ticks=[a['result'] for a in old['APIs'] if a['name']=='GetTickCount'];other=None
  try:
   other=fresh_case(row['input'],helpers[0],helpers[1],ticks);verify_case(other,old)
   for key in ('initial','final'):equal(row[key],other[key],'fresh complete '+key+' region')
   for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'fresh original forward/cumulative digest/actual cleanup '+key)
   for key in ('terminal_next_dialogue','next_dialogue_cleanup','next_dialogue_resources_after_cleanup'):need(guest(row[key])==guest(other[key]),'fresh whole memory/57CPU/native inputs/local digests/frames/lifetimes '+key)
  except Exception as error:
   if other is not None:
    diagnostic='analysis/terminal-next-dialogue-diagnostic-fresh-'+row['input']['name']+'-20261028-'+str(time.time_ns())+'.json.gz'
    e.save_source(diagnostic,dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),error_type=type(error).__name__,error=str(error),fresh_original_case=other))
    print('full failed fresh instance preserved locally',diagnostic,flush=True)
   raise
  proof['current_native_resources_recreated']=True;proof['complete_cumulative_digests_reproduced_by_new_full_original_instance']=True;rows.append(proof);print('independent next dialogue',row['input']['name'],'all current resources and original roots verified',flush=True);del other;gc.collect()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,next_confirmation_released=False,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable independent next dialogue proof');e.terminal.save(a.out,verify(ROOT/a.report))
