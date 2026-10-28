"""Independent original layer7 replacement group and current native ownership."""
import argparse,copy,gc,gzip,hashlib,json,struct,types
from functools import lru_cache
from tools import terminal_followup_verification as previous_stage
from tools import terminal_replacement_emulation as e
from tools.terminal_followup_verification import (need,num,read,equal,guest,sha,node,text_object,text_record,mark_zero,page_keys,capture_list,text_update,helper_contract,original_text,geometry,convert_surface,bands,NAMES,CRT_IMPORTS,HEAP_BASE,SC001_SHA,SCRIPT_SHA,SimpleNamespace,tls_platform,validate_pages,expand,Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,x86,portrait,source_names)
from tools.school_native_dialogue_verification import predict_keyboard

ROOT=e.ROOT;previous=previous_stage.previous
PARENT_ACCEPTANCE='analysis/terminal-followup-acceptance-v1-20261027.json'
PARENT_ACCEPTANCE_SHA='86bb1ed313febc97a715bad7e530335e79a0ea7f527ac28e543274ad0d0ebc5f'
PARENT_SOURCE='analysis/terminal-followup-source-v1-20261027.json.gz'
PARENT_SOURCE_SHA='c46d21d7064224e29de0f25a539dac92f23eecf407c26c4f20df14cac2268779'
PARENT_PROOF='analysis/terminal-followup-proof-v1-20261027.json'
PARENT_PROOF_SHA='94f34f76e60c3eb3f10d9cfefda14c942c10dba4007b883981cf83fc117beb25'
IMPLEMENTATIONS=('tools/terminal_replacement_emulation.py','tools/terminal_replacement_verification.py','tools/terminal_replacement_preservation.py','tools/tests/test_terminal_replacement.py','tools/tests/test_terminal_replacement_source.py')
CAPTURE_KEYS=previous_stage.CAPTURE_KEYS

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original replacement branch');win=name=='neutral_running'
 return dict(segment=2 if win else 11,first_PC=198 if win else 194,final_PC=230 if win else 226,layer=7,text_indices=[3,4] if win else [5,6],role=None)

@lru_cache(maxsize=1)
def parent_report():
 for path,want in ((PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),(PARENT_PROOF,PARENT_PROOF_SHA),(PARENT_SOURCE,PARENT_SOURCE_SHA)):
  h=hashlib.sha256()
  with (ROOT/path).open('rb') as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  need(h.hexdigest()==want,'fixed latest parent '+path)
 with gzip.open(ROOT/PARENT_SOURCE,'rt',encoding='utf8') as f:return json.load(f)

def parent_case(row):return next(x for x in parent_report()['cases'] if x['input']==row['input'])
def accepted_clock_inputs():return {r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in parent_report()['cases']}
def new_resources(row):
 d=row['terminal_replacement'];return [r for r in d['resources'] if r['create_wire_index']>=d['prefix']['GPU_wire']]
def capture_list(value):
 """Inventory this stage; inherited resource captures retain their old clocks.

 The eight full predecessor resource records are immutable forward evidence
 checked by prefix() and its original predecessor replay. Their old local
 traces must never be relabelled as new replacement-stage captures.
 """
 if isinstance(value,dict) and 'resources' in value and 'resources_before' in value and 'prefix' in value:
  value=dict(value,resources={str(i):r for i,r in enumerate(value['resources']) if r['create_wire_index']>=value['prefix']['GPU_wire']},resources_before=[])
 return previous_stage.capture_list(value)
def gpu_calls(row):
 d=row['terminal_replacement'];return [c for c in previous_stage.gpu_calls(row) if c.get('wire_index',-1)<d['prefix']['GPU_wire']]+d['GPU_APIs']

def gpu_mappings(row):
 """Opaque native tokens are owned by a projection lifetime, not globally.

 A driver may reissue a retired address. Each new text has a separate typed
 domain, while the accepted predecessor domain remains byte-for-byte intact.
 No surface, heap or guest-memory byte is address-normalized here.
 """
 allowed={'overlay','overlay-replacement-0','overlay-replacement-1'};out={};keys=set();guests=set()
 for r in row['typed_GPU_projection']:
  need(set(r)=={'domain','native','guest'} and r['domain'] in allowed and type(r['native']) is int and 0<r['native']<2**32 and type(r['guest']) is int and 0<r['guest']<2**32,'bounded declared typed projection entry')
  key=(r['domain'],r['native']);need(key not in keys and r['guest'] not in guests,'unique lifetime/native key and disjoint guest identities');keys.add(key);guests.add(r['guest']);out.setdefault(r['domain'],{})[r['native']]=r['guest']
 need('overlay' in out,'accepted predecessor projection domain');return out

def resource_domain(row,r):
 d=row['terminal_replacement']
 if r['create_wire_index']<d['prefix']['GPU_wire']:return 'overlay'
 index=r['record_index'];need(type(index)is int and index in (0,1) and r['record']==text_record(7,index),'only the two count-derived replacement lifetimes');domain='overlay-replacement-'+str(index);need(r['projection_domain']==domain,'explicit resource lifetime domain independently derived from original record');return domain

def forward_only(row):
 d=row['terminal_followup'];end=row['followup_cleanup'][0]['leaves'][0];out=dict(d)
 out['leaves']=d['leaves'][:end];out['GPU_APIs']=[c for c in d['GPU_APIs'] if c['wire_index']<d['forward_wire_end']]
 return out

def prefix(row,old=None,replay=True):
 old=parent_case(row) if old is None else old;d=row['terminal_replacement'];p=d['prefix'];before=d['before'];fixed=old['terminal_followup']['final'];cfg=branch(row['input']['name'])
 for key in ('memory','CPU','state','queue','trace'):need(before[key]==fixed[key]==row['terminal_followup']['final'][key],'fixed entire followup boundary '+key)
 need(before['local_trace']==mark_zero() and previous_stage.vw(before['state'])==(cfg['first_PC'],1),'new trace zero at original confirmation')
 keys=('initial','input','combat_input','initialization','target_bind','roots','bind_before','bind','bind_after','world_frames','events','commands','hit','hit_sides','contracts','both_hp_writes','calls','ownership','popped','entries','improved','reopened','original_coordinate_writes','action_events','resource_domain','IME_identity','game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization','accounting_baseline','image_before','image_after','resource_loaded','overlay_continuation','after_fade','terminal_name','terminal_portrait','terminal_dialogue','terminal_confirmation','terminal_panel_dialogue','admission')
 for key in keys:
  if key in old:need(guest(row[key])==guest(old[key]),'all fixed forward records '+key)
 need(guest(forward_only(row))==guest(forward_only(old)),'entire latest parent forward excluding its historical teardown')
 retained=set().union(*(page_keys(old[k]) for k in keys if k in old));need(all(row['blobs'].get(k)==old['blobs'][k] for k in retained),'all accepted intermediate pages unchanged')
 need(all(sha(bytes.fromhex(v))==k for k,v in row['blobs'].items()),'all current content pages rehashed');validate_pages(row,row['blobs'])
 n=sum(a['wire_end']<=old['terminal_followup']['CRT_forward_wire_end'] for a in old['CRT_APIs']);lengths=dict(CRT_APIs=n,task_APIs=len(old['task_APIs']),resource_steps=len(old['resource_initialization']),task_calls=len(old['task_calls']),task_writes=len(old['task_writes']),APIs=len(old['APIs']))
 for field,n in lengths.items():
  key='resource_initialization' if field=='resource_steps' else field;need(p[field]==n and guest(row[key][:n])==guest(old[key][:n]),'all fixed prefix lengths and records '+field)
 need(len(row['APIs'])==p['APIs'] and p['extra_counts']==old['extra_original_instruction_counts'],'no new clocks and fixed original source accounting')
 need((p['GPU_wire'],p['CRT_wire'])==(old['terminal_followup']['forward_wire_end'],old['terminal_followup']['CRT_forward_wire_end']),'actual accepted platform forward cursors')
 ticks=[a for a in row['APIs'] if a['name']=='GetTickCount'];need([a['result'] for a in ticks]==[a['result'] for a in old['APIs'] if a['name']=='GetTickCount'] and all(a['actual_API_executed'] is False and a['captured_platform_input'] is True for a in ticks),'fixed captured clocks and honest provenance')
 tls_platform(row['platform'],SimpleNamespace(crt_draws=len(old['platform']['trace'])//3))
 def tls_guest(v):
  v=copy.deepcopy(v)
  for part in ('creation','cleanup'):
   for k in ('thread','native_index'):v[part].pop(k)
  for a in v['trace']:a.pop('actual_native_index')
  return v
 need(tls_guest(row['platform'])==tls_guest(old['platform']),'actual TLS original owner semantics')
 counts=None
 if replay:
  init=previous.ResourceInitializationReplay(row).execute();por=portrait.Replay(row).execute();conf=previous.confirmation.Replay(row).execute();pd=previous.Replay(row,previous.pixels(row)[1]).execute();fu=previous_stage.Replay(row,previous_stage.pixels(row)[1]).execute();counts=dict(initialization=init,portrait=por,confirmation=conf,panel_dialogue=pd,followup=fu)
 return dict(fixed_acceptance_sha256=PARENT_ACCEPTANCE_SHA,fixed_source_sha256=PARENT_SOURCE_SHA,fixed_proof_sha256=PARENT_PROOF_SHA,parent_full_memory_CPU_queue_and_trace_equal=True,independent_current_parent_forward=counts,no_historical_cleanup_projection=True)

def source(row):
 d=row['terminal_replacement'];cfg=branch(row['input']['name']);raw=(ROOT/e.terminal.SCRIPT_PATH).read_bytes();need(sha(raw)==SCRIPT_SHA,'original complete T0004 identity');segment=next(s for s in previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);at=segment['code_start'];pc=cfg['first_PC'];base=num(read(d['before']['memory'],e.VM+16,4),0);commands=[]
 expected=[(pc,43,8),(pc+8,44,4),(pc+12,17,6),(pc+18,17,6),(pc+24,50,4),(pc+28,51,4)]
 for want in expected:
  op,n=struct.unpack_from('<HH',raw,at+pc);need((pc,op,n)==want and read(d['before']['memory'],base+pc,n)==raw[at+pc:at+pc+n],'whole original replacement command/declared bytes');commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
 need(pc==cfg['final_PC'] and d['commands']==commands and num(raw,at+cfg['first_PC']+4)==0x20000004,'only original config4/44/two17/50/51 dispatches')
 next_op,next_n=struct.unpack_from('<HH',raw,at+pc);need((next_op,next_n)==((43,8) if cfg['segment']==2 else (30,20)),'original next command remains beyond confirmation')
 config=list(struct.unpack_from('<19h',e.CODE,0x624520-0x400000+4*38));need(config[0]==7,'configuration4 independently selects layer7')
 texts=[];identities={3:(1272,'a74fbee1a4dfa14ba14b'),4:(1284,'a66fa575ac4fbaceb16fabdcbcf4a6d3a477a143'),5:(3376,'acb0a446b1cfa66fa141a662a66fa8adc3e4a5b4b67daac5b6a1a4a7aaf9a141'),6:(3410,'c1f6b54dac4fa6b3c249b2cabe7ca141a4a3b94cb36fa45da853bfecaa6ba143')}
 for j,i in enumerate(cfg['text_indices']):
  need(num(raw,at+cfg['first_PC']+16+6*j,'H')==i,'original per-line text table index');end=segment['code_end'];packed=num(raw,end+4+i*4);span=packed>>20;off=end+(packed&0xFFFFF);text=raw[off:off+span];need(len(text)==span and 2<=span<=512 and span%2==0 and text[-2:]==bytes(2) and 0 not in text[:-2] and (off,text[:-2].hex())==identities[i],'bounded exact original ANSI dialogue bytes');texts.append(dict(index=i,record_index=j,source_offset=off,hex=text[:-2].hex()))
 need(e.ALLOWED==previous_stage.e.ALLOWED and e.ReplacementMachine.source_code.__code__ is previous_stage.e.FollowupMachine.source_code.__code__,'no extra guest range or replacement source guard')
 return dict(segment=cfg['segment'],script_sha256=SCRIPT_SHA,commands=commands,final_PC=pc,next_opcode=next_op,selected_layer=7,texts=texts,configuration=config)

def pixels(row):
 provenance=source(row);refs={};resources=new_resources(row);need(len(resources)==2 and all(r['kind']=='text' for r in resources),'exact two new original text textures')
 for r,text in zip(resources,provenance['texts']):
  b=r['font_boundary'];sp=b['CPU']['ESP'];args=[num(read(b['memory'],sp+4+i*4,4),0) for i in range(14)];need(r['pending_font']==dict(entry=num(read(b['memory'],0x5920A0,4),0),caller=0x4CAD09,args=args,CPU=b['CPU'],first_instruction_executed=False) and b['CPU']['EIP']==r['pending_font']['entry'] and num(read(b['memory'],sp,4),0)==0x4CAD09,'whole original pending text font ABI')
  obj=read(b['memory'],text_object(7),0x18);alt=bool(obj[0x14]);width=num(obj,0xE if alt else 0xC,'h')&0xFFFFFFFF;height=num(obj,0x12 if alt else 0x10,'h')&0xFFFFFFFF
  need(args==[height,width,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C] and r['record']==text_record(7,text['record_index']) and r['record_index']==text['record_index'] and r['text_index']==text['index'],'original count-derived record/font and script text')
  reference=previous.dialogue.raster_dialogue(bytes.fromhex(text['hex']),args[:-1],original_text(args[-1]));raster=r['raster'];g=geometry(reference['measured']);need(r['geometry']==g and (raster['ACP'],raster['measured'],raster['selected_face'],raster['raster_hex'])==(reference['ACP'],reference['measured'],reference['selected_face'],reference['raster_hex']),'independent actual original metrics/face/full raster')
  need([a['name'] for a in raster['stages']]==['PatBlt','TextOutA','TextOutA'] and [a['hex'] for a in raster['stages']]==[a['hex'] for a in reference['stages']],'all three original raster stages');need([a['name'] for a in r['calls']]==NAMES+['SelectObject','DeleteObject','DeleteDC','DeleteObject'] and raster['calls']==r['calls'][:23],'all27 original GDI calls')
  lock=r['lock'];w,h=[1<<(v-1).bit_length() for v in g['texture_size']];out=bytes.fromhex(lock['hex']);need(lock['pitch']==w*2 and len(out)==w*h*2,'entire actual native initial surface and padding');expected=bands(g);need([dict(rect=c['rect'],point=c['point']) for c in r['conversions']]==expected,'all original conversion bands')
  for band in expected:out=convert_surface(bytes.fromhex(reference['raster_hex']),g['raster_size'],band['rect'],out,lock['pitch'],band['point'])
  need(r['upload_hex']==r['readback']['hex']==out.hex() and r['readback']['sha256']==sha(out) and r['readback']['pitch']==lock['pitch'],'every converted texel preserves actual untouched bytes');need(num(read(r['completion']['memory'],text_object(7)+22,2),0,'H')==text['record_index']+1,'original completed line increments count');refs[r['generation']]=dict(reference=reference,geometry=g)
 return provenance,refs

def bind_replay(fn):
 """Reuse frozen independent engine, replacing only report routing strings.

 No guest instructions, API outputs, numeric addresses or trace values change.
 """
 routing={'terminal_followup':'terminal_replacement','followup_cleanup':'replacement_cleanup'}
 def constants(code):return code.replace(co_consts=tuple(constants(v) if isinstance(v,types.CodeType) else routing.get(v,v) if type(v)is str else v for v in code.co_consts))
 return types.FunctionType(constants(fn.__code__),dict(fn.__globals__,**globals()),closure=fn.__closure__)

def native(row,old=None):
 """Audit current receipts by creation ordinal, with no byte identity masks."""
 d=row['terminal_replacement'];old=parent_case(row) if old is None else old;helper_contract();contexts=gpu_mappings(row);m=contexts['overlay'];gt=row['GPU_trace'];ct=row['CRT_trace'];ledger=row['replacement_resources_after_cleanup'];by_create={r['create_wire_index']:r for r in ledger};by_gen={r['generation']:r for r in ledger}
 need(set(contexts)=={'overlay','overlay-replacement-0','overlay-replacement-1'},'exact predecessor and two independent replacement projection lifetimes')
 projection=row['typed_GPU_projection'];prefix_rows=[r for r in projection if r['domain']=='overlay'];first=0x64001000+len(prefix_rows)*0x100000
 need(first<=0x65801000 and d['GPU_projection_before']==dict(next=first,ledger=prefix_rows) and projection[:len(prefix_rows)]==prefix_rows and d['GPU_projection']==projection[len(prefix_rows):],'complete ordered unchanged prefix and explicit new projection ledger')
 prefix_ids=set()
 def interface_ids(v):return [v['pointer'],v['vtable']]+list(v['methods'].values())
 prefix_ids.update(interface_ids(row['current_GPU_hello']['device']))
 for t in gt[:d['prefix']['GPU_wire']]:
  result=t['reply']['result']
  if t['request']['op']=='create':prefix_ids.update(interface_ids(result['texture']))
  elif t['request']['op']=='lock':prefix_ids.add(result['bits'])
 need(set(m)==prefix_ids and [r['guest'] for r in prefix_rows]==[0x64001000+i*0x100000 for i in range(len(prefix_rows))],'every predecessor identity bound to actual device/create/lock inputs and original deterministic allocation')
 for index,r in enumerate(new_resources(row)):
  domain=resource_domain(row,r);native_texture=gt[r['create_wire_index']]['reply']['result']['texture'];lock=next(c['native_result'] for c in r['GPU_APIs'] if c['op']=='lock');need(list(native_texture['methods'])==['8','56','64','68'],'frozen helper original texture ABI enumeration')
  sequence=interface_ids(native_texture)+[lock['bits']];need(len(sequence)==len(set(sequence))==7,'six actual interface identities and one actual surface identity per lifetime')
  expected=[dict(domain=domain,native=p,guest=first+(7*index+j)*0x100000) for j,p in enumerate(sequence)]
  need([v for v in projection if v['domain']==domain]==expected,'independent exact per-creation projection allocation from native wire')
 need(first+14*0x100000<=0x66601000<0x6A001000,'all new interface/surface pages remain below existing GDI namespace')
 need(row['current_CRT_hello']['pointer_bytes']==row['current_GPU_hello']['pointer_bytes']==4 and row['current_GPU_hello']['window_visible'] is False and row['current_GPU_hello']['image_size']==[512,512] and row['current_CRT_hello']['GPU_created'] is False,'actual bounded headless x86 CRT/GPU owners')
 need(len(by_create)==len(by_gen)==len(ledger)==10,'ten distinct creation generations in either complete branch')
 need(len(d['resources'])==len(ledger) and len(d['resources_before'])==8,'complete eight-generation prefix and two new text generations')
 need(d['resources_before']==row['terminal_followup']['resources'],'each seeded generation bound to complete actual parent ledger, including already retired timeout text5')
 for before,after in zip(d['resources_before'],d['resources'][:8]):
  for k,v in before.items():
   if k not in ('alive','release_wire_index','released_phase','alive_after_forward'):need(after[k]==v,'unchanged original seeded metadata '+k)
  if not before['alive']:need(all(after.get(k)==before.get(k) for k in ('alive','release_wire_index','released_phase')),'an already retired generation never revived or released twice')
 need(d['GPU_APIs']==[x['call'] for x in d['leaves'] if x['kind']=='GPU'] and d['calls']==[x['call'] for x in d['leaves'] if x['kind']=='GDI'] and row['CRT_APIs'][d['prefix']['CRT_APIs']:]==[x['call'] for x in d['leaves'] if x['kind']=='CRT'],'every original platform leaf belongs once to its full current receipt ledger')
 for r in new_resources(row):
  a,z=r['leaves'];leaves=d['leaves'][a:z];need(0<=a<z<=row['replacement_cleanup'][0]['leaves'][0] and r['GPU_APIs']==[x['call'] for x in leaves if x['kind']=='GPU'] and r['calls']==[x['call'] for x in leaves if x['kind']=='GDI'] and r['conversions']==[c for c in d['conversions'] if c['resource_label']==r['label']],'complete actual original resource leaf/conversion interval')
 live={};logical={};ci=readbacks=peak=0;calls=gpu_calls(row);observers={o['wire_index']:o for o in d['readback_observers']}
 need(len(observers)==len(d['readback_observers']),'every current follow-up observer classified once')
 for label,tr in (('GPU',gt),('CRT',ct)):
  for i,t in enumerate(tr):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok'] is True,'complete ordered successful actual '+label+' wire')
 oldmap=gpu_mappings(old)['overlay']
 need(previous.gpu_value(gt[:d['prefix']['GPU_wire']],m)==previous.gpu_value(old['GPU_trace'][:d['prefix']['GPU_wire']],oldmap),'every current fixed forward GPU request/result and observer byte')
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
  need(generation in by_gen,'original operation identifies an existing creation generation');context=contexts[resource_domain(row,by_gen[generation])]
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
 need(ci==len(calls) and peak==(9 if row['input']['name']=='neutral_running' else 7),'all original COM calls and exact bounded simultaneous texture peak')
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
 constructed=[row['terminal_portrait']['constructed']]+[r['constructed'] for r in previous_stage.new_resources(row) if r['kind']=='portrait']+[r['constructed'] for r in new_resources(row) if r['kind']=='portrait']
 for b in constructed:
  for x in b['native_allocation_readbacks']:
   i=x['wire_index'];covered.extend((i-1,i));a=ct[i-1];z=ct[i];need(a['request']['op']=='sync' and a['request']['hex']==a['reply']['result']['hex']==x['result']['hex'] and z['request']==dict(id=i+1,op='readback',pointer=x['result']['pointer']) and z['reply']['result']==x['result'] and len(bytes.fromhex(x['result']['hex']))==x['bytes'],'entire original file/vector current native observer and preceding full mirror')
 need(sorted(covered)==list(range(len(ct)-1)),'every current CRT wire classified exactly once')
 # Every opaque owner token is checked by the frozen raw-owner audit; payload
 # masks in its returned comparison view are never used as proof of bytes.
 need(previous.crt_semantics(row)[:d['prefix']['CRT_wire']]==previous.crt_semantics(old)[:d['prefix']['CRT_wire']],'every current fixed-prefix CRT control request and complete initialized data; actual uninitialized inputs independently executed')
 blocks=[row['terminal_name'],row['terminal_dialogue']]+row['terminal_panel_dialogue']['sentences']+[r for r in previous_stage.new_resources(row) if r['kind'] in ('name','text')]+[r for r in new_resources(row) if r['kind'] in ('name','text')];gm={x['guest']:x['native'] for x in d['GDI_handle_projection']}
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

class Replay(previous_stage.Replay):
 __init__=bind_replay(previous_stage.Replay.__init__)
 execute=bind_replay(previous_stage.Replay.execute)
 def cleanup(self):
  d=self.d;rows=self.row['replacement_cleanup'];steps=self.row['cleanup_steps'];keys=('label','entry','args','receiver','cdecl');old=parent_case(self.row);expected=[{k:s[k] for k in keys} for s in old['cleanup_steps']]
  if self.row['input']['name']=='neutral_running':expected=[dict(label='supplemental_original_replacement_extra_line_destructor',entry=0x403730,args=[],receiver=text_record(7,1),cdecl=False)]+expected
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
  for group in (20,32)+((30,) if self.row['input']['name']=='neutral_running' else ()):need(self.read(e.MAIN+0x844+group*8,8)==bytes(8),'every current source resource bank originally cleared')
  for r in d['resources']:
   if e.VM<=r['record']<e.VM+0x9400:need(num(self.read(r['record']+44,4),0)==0,'every embedded old/new texture record naturally cleared')
  return dict(instructions=total_i,writes=total_w,independent_local_code_sha256=ih.hexdigest(),independent_local_write_sha256=wh.hexdigest(),CPU_registers=57,all_actual_original_roots=len(rows),all_root_full_memory_and_native_sync_verified=True,no_historical_CPU_or_SHA_projection=True)


vw=previous_stage.vw

def protocol(row):
 d=row['terminal_replacement'];cfg=branch(row['input']['name']);scene=76 if row['input']['name']=='neutral_running' else 77;stream=previous.confirmation.captured_contract()['streams'][scene];bindings=d['bindings'];need(d['branch']==e.branch(row['input']['name']) and len(bindings)==3 and [b['capture'] for b in bindings]==stream['captures'],'separate exact captured76/77 idle/press/release cycle')
 need(len(row['terminal_confirmation']['bindings'])==3,'accepted first cycle never cleared or reused')
 for b in bindings:
  raw=bytes.fromhex(b['capture']['raw_device_hex']);before=bytes.fromhex(b['before_hex']);bound=bytearray(before);bound[12:268]=raw;bp=e.STACK+0xF800
  need(len(raw)==256 and len(before)==0xA00 and b['cycle']=='replacement_confirmation' and b['bound_hex']==bound.hex() and b['after_hex']==predict_keyboard(bytes(bound)).hex(),'every byte of independently updated original A00 keyboard object')
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
 final=d['final']['memory'];need(num(read(final,text_object(cfg['layer'])+22,2),0,'H')==2 and num(read(final,e.VM+0x1CC,1),0,'B')==7,'original selected target retains exactly one new text record')
 clear=d['clear'];old_count=1 if row['input']['name']=='neutral_running' else 3;record=text_record(7)
 need(vw(clear['before']['state'])==(cfg['first_PC']+8,0) and vw(clear['after']['state'])==(cfg['first_PC']+12,0) and clear['GPU_wire_before']==clear['GPU_wire_after'] and num(read(clear['before']['memory'],text_object(7)+22,2),0,'H')==old_count and num(read(clear['after']['memory'],text_object(7)+22,2),0,'H')==0,'original44 clears actual old count without COM calls')
 for i in range(old_count):need(read(clear['before']['memory'],text_record(7,i)+44,4)==read(clear['after']['memory'],text_record(7,i)+44,4),'44 never rewrites any retained old record texture pointer')
 retired=[r for r in d['resources_before'] if r['record'] in [text_record(7,i) for i in range(min(old_count,2))] and r['alive']]
 need(len(retired)==len(d['replacements'])==min(old_count,2),'each overwritten old layer7 record destructed once')
 for old,replacement,new in zip(retired,d['replacements'],new_resources(row)):
  record=old['record'];need((replacement['entry'],replacement['caller'],replacement['record'],replacement['generation'],replacement['ledger_index'])==(0x403730,0x4051AE,record,old['generation'],d['resources_before'].index(old)) and replacement['before']['CPU']['EIP']==0x403730 and replacement['after']['CPU']['EIP']==0x4051AE and replacement['return_ESP']==replacement['before']['CPU']['ESP']+4==replacement['after']['CPU']['ESP'],'actual original405160 constructor calls403730 and naturally returns on same stack')
  need(read(replacement['before']['memory'],record+44,4)==struct.pack('<I',old['texture']['pointer']) and read(replacement['after']['memory'],record+44,4)==bytes(4) and [c['op'] for c in replacement['GPU_APIs']]==['describe','release'] and all(c['generation']==old['generation'] and c['phase']=='forward' for c in replacement['GPU_APIs']) and replacement['GPU_APIs'][-1]['wire_index']<new['create_wire_index'] and new['record']==record and new['generation']!=old['generation'],'old exact generation released before same-record new texture creation')
 if old_count==3:
  old=next(r for r in d['resources_before'] if r['record']==text_record(7,2));current=next(r for r in d['resources'] if r['generation']==old['generation']);need(current['alive'] and current['release_wire_index'] is None and num(read(final,text_record(7,2)+44,4),0)==old['texture']['pointer'],'out-of-count third old texture remains physically live through final boundary')
 for r in d['resources']:
  if r['alive']:need(num(read(final,r['record']+44,4),0)==r['texture']['pointer'],'every retained current record owns its correct live generation')
 need(d['accounting']==num(read(final,0x765720,4),0)==row['accounting_baseline']['texture_bytes']+sum(r['size'][0]*r['size'][1]*2 for r in d['resources'] if r['alive']),'all and only simultaneously live textures are accounted')
 return dict(VM_PC=cfg['final_PC'],VM_wait=1,selected_layer=7,new_text_indices=cfg['text_indices'],forward_replacements=len(retired),no_input_hold_tasks=2,next_opcode_unexecuted=43 if row['input']['name']=='neutral_running' else 30)

def final_summary(row):
 d=row['terminal_replacement'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs']);want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'every current final-state page and selected summary field equals independently replayed final full memory');return True

def verify_case(row,old=None):
 provenance,refs=pixels(row);timed=protocol(row);platform=native(row,old);replay=Replay(row,refs);counts=replay.execute();p=prefix(row,old);d=row['terminal_replacement'];equal(row['final'],d['final']['memory'],'every final mapped byte');need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'complete final57 CPU and unchanged original image/IAT')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'full cumulative source digests retained from actual original execution')
 summary=final_summary(row);cleanup=replay.cleanup();facts=dict(full_cumulative=d['final']['trace'],mapped_regions=len(d['final']['memory']),CPU_registers=len(d['final']['CPU']),complete_tasks=(402 if row['input']['name']=='neutral_running' else 349)+len(d['frames']),pending_tasks=0,live_textures=sum(r['alive'] for r in d['resources']),new_textures=[dict(text_index=r['text_index'],record=r['record'],generation=r['generation'],size=r['size'],font_args=r['pending_font']['args'],measured=r['raster']['measured'],nonzero_upload_bytes=sum(b!=0 for b in bytes.fromhex(r['upload_hex']))) for r in new_resources(row)])
 return dict(name=row['input']['name'],prefix=p,source=provenance,helper=helper_contract(),native=platform,timing=timed,added=counts,cleanup=cleanup,forward_summary=facts,current_terminal_summary_pages_equal_verified_final_memory=summary,independent_whole_memory_CPU_and_new_original_trace=True,no_historical_cleanup_CPU_or_SHA_projection=True)

def fresh_case(case,crt_helper,gpu_helper,ticks):
 need(ticks==accepted_clock_inputs()[case['name']],'fresh full original instance uses exact latest-parent clocks');return e.run_case(case,crt_helper,gpu_helper,ticks)

def verify(path):
 accepted_clock_inputs()
 with gzip.open(path,'rt',encoding='utf8') as f:data=json.load(f)
 need(data['schema_version']==1 and data['source_contract']==e.source_contract() and [r['input'] for r in data['cases']]==e.overlay.parent.corpus(),'exact source contract and both original branches');helpers=e.helpers('terminal-replacement-proof');rows=[]
 for row in data['cases']:
  old=parent_case(row);proof=verify_case(row,old);ticks=[a['result'] for a in old['APIs'] if a['name']=='GetTickCount'];other=fresh_case(row['input'],helpers[0],helpers[1],ticks);verify_case(other,old)
  for key in ('initial','final'):equal(row[key],other[key],'fresh complete '+key+' region')
  for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'fresh original forward/cumulative digest/actual cleanup '+key)
  for key in ('terminal_replacement','replacement_cleanup','replacement_resources_after_cleanup'):need(guest(row[key])==guest(other[key]),'fresh whole memory/57CPU/native inputs/local digests/frames/lifetimes '+key)
  proof['current_native_resources_recreated']=True;proof['complete_cumulative_digests_reproduced_by_new_full_original_instance']=True;rows.append(proof);print('independent replacement',row['input']['name'],'all current resources and original roots verified',flush=True);del other;gc.collect()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,next_confirmation_released=False,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable independent replacement proof');e.terminal.save(a.out,verify(ROOT/a.report))
