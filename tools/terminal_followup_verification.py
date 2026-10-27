"""Independent original follow-up groups, current platform bytes and lifetimes.

Historical receipts never substitute for the current resource owner.  The
accepted parent is a forward reference; no historical cleanup CPU is projected.
"""
import argparse,copy,gc,gzip,hashlib,json,struct,types
from functools import lru_cache
from types import SimpleNamespace
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_followup_emulation as e
from tools import terminal_panel_dialogue_verification as previous
from tools import terminal_portrait_verification as portrait
from tools.school_retained_name_verification import Replay as NameABI,NAMES
from tools.school_retained_name_corpus import source_names,raster_name
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_second_live_text_catalog import bands
from tools.school_native_dialogue_verification import predict_keyboard
from tools.school_retained_crt_fixture import HEAP as HEAP_BASE
from tools.school_crt_init_fixture import IMPORTS as CRT_IMPORTS
from tools.battle_lethal_combat import validate_pages
from tools.battle_world_combat import expand
from tools.battle_hit_damage_verification import platform as tls_platform

need=e.need;num=previous.num;read=previous.read;equal=previous.equal;guest=previous.guest
ROOT=e.ROOT
IMPLEMENTATIONS=('tools/terminal_followup_emulation.py','tools/terminal_followup_verification.py','tools/terminal_followup_preservation.py','tools/terminal_followup_d3d8_platform.cs','tools/tests/test_terminal_followup.py')
PARENT_ACCEPTANCE='analysis/terminal-panel-dialogue-acceptance-v1-20261027.json'
PARENT_ACCEPTANCE_SHA='ac1937ef900d1ebb2bae5d70ca60f6ea7ae0949e8fc093af867fb6fcea27beab'
PARENT_SOURCE='analysis/terminal-panel-dialogue-source-v1-20261026.json.gz'
PARENT_SOURCE_SHA='d2be32fc2c14d47f4824aa456956c568f7cf86bc9adbf6b8a3207a692074edd3'
PARENT_PROOF='analysis/terminal-panel-dialogue-proof-v2-20261027.json'
PARENT_PROOF_SHA='7f1a8df210b6cc9fe7bbff76a8756000d083faba79543671d75c8b2c65082f7b'
SCRIPT_SHA='dfeffff8e6a7e1582797af89c9836058596b65b2fe91049f2466754a8a86eae0'
SC001_SHA='afee760213b1a62c0e2e86fef2a186bcbf0db46d28dcf73994990dcde7114b6b'
EXTRA_RANGE=(0x4C4EB0,0x4C4F23)
CAPTURE_KEYS=frozenset(('memory','CPU','state','queue','trace','local_trace'))

def sha(data):return hashlib.sha256(data).hexdigest()
def node(layer):return e.VM+0x6F60+layer*0xE0
def text_object(layer):return e.VM+0x430+layer*0xAB8
def text_record(layer,index=0):return text_object(layer)+0x28+index*0x110
def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original follow-up branch')
 return dict(segment=2 if name=='neutral_running' else 11,first_PC=156 if name=='neutral_running' else 168,final_PC=198 if name=='neutral_running' else 194,layer=4 if name=='neutral_running' else 5,text_index=2 if name=='neutral_running' else 4,role=1 if name=='neutral_running' else None)

def helper_contract():
 old=(ROOT/'tools/terminal_portrait_d3d8_platform.cs').read_bytes();new=(ROOT/'tools/terminal_followup_d3d8_platform.cs').read_bytes()
 before=b'if(retired.Contains(key) || resources.ContainsKey(key)){Method<Release>(ptr,2)(ptr);throw new ArgumentException("retired or duplicate texture address; new session required");}'
 after=b'if(resources.ContainsKey(key)){Method<Release>(ptr,2)(ptr);throw new ArgumentException("duplicate live texture address");}'
 need(old.count(before)==1 and new==old.replace(before,after),'sole helper change admits only a released native texture address, never duplicate live ownership')
 need(b'resources.Count>=10 || issued>=32' in new and b'Resource t=Owned(r)' in new and b'resources.Remove(key);order.Remove(key);retired.Add(key)' in new,'all original bounded live ownership and teardown checks remain')
 return dict(previous_sha256=sha(old),current_sha256=sha(new),only_released_address_reuse_admitted=True,duplicate_live_address_refused=True)

@lru_cache(maxsize=1)
def parent_report():
 for path,want in ((PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),(PARENT_PROOF,PARENT_PROOF_SHA)):
  need(sha((ROOT/path).read_bytes())==want,'fixed latest parent '+path)
 digest=hashlib.sha256()
 with (ROOT/PARENT_SOURCE).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
 need(digest.hexdigest()==PARENT_SOURCE_SHA,'fixed latest parent source bytes')
 with gzip.open(ROOT/PARENT_SOURCE,'rt',encoding='utf8') as f:return json.load(f)

def parent_case(row):return next(x for x in parent_report()['cases'] if x['input']==row['input'])
def accepted_clock_inputs():
 """Unchanged method inputs from the latest fixed real forward, not old trees."""
 result={r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in parent_report()['cases']};need(set(result)=={'neutral_running','timeout_before_combat'} and all(v and all(type(x)is int for x in v) for v in result.values()),'two full fixed latest-parent captured clock streams');return result

def fresh_case(case,crt_helper,gpu_helper,ticks):
 # Execute the unchanged public runner code object with only its readonly
 # time-input provider bound to the exact same accepted latest-parent inputs.
 # No machine class, instruction, cleanup CPU, result or digest is replaced.
 runner=types.FunctionType(e.run_case.__code__,dict(e.run_case.__globals__,fixed_parent_times=accepted_clock_inputs),closure=e.run_case.__closure__)
 return runner(case,crt_helper,gpu_helper,ticks)
def mark_zero():return dict(instructions=0,writes=0,code_sha256=sha(b''),write_sha256=sha(b''))
def page_keys(value):
 if isinstance(value,dict):
  if set(value)=={'bytes','pages'}:return set(value['pages'])
  return set().union(*(page_keys(v) for v in value.values())) if value else set()
 if isinstance(value,list):return set().union(*(page_keys(v) for v in value)) if value else set()
 return set()

def prefix(row,old=None,replay=True):
 """Use the accepted forward only; current native data has its own audit."""
 old=parent_case(row) if old is None else old;d=row['terminal_followup'];p=d['prefix'];before=d['before'];fixed=old['terminal_panel_dialogue']['final'];cfg=branch(row['input']['name'])
 for key in ('memory','CPU','state','queue','trace'):need(before[key]==fixed[key]==row['terminal_panel_dialogue']['final'][key],'entire accepted parent boundary '+key)
 need(before['local_trace']==mark_zero(),'new follow-up trace starts at zero')
 v=bytes.fromhex(before['state']['VM']);need((num(v,28),num(v,32,'H'),num(v,34,'H'))==(cfg['first_PC'],1,51),'accepted original confirmation boundary')
 common=('initial','input','combat_input','initialization','target_bind','roots','bind_before','bind','bind_after','world_frames','events','commands','hit','hit_sides','contracts','both_hp_writes','calls','ownership','popped','entries','improved','reopened','original_coordinate_writes','action_events','resource_domain','IME_identity','game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization','accounting_baseline','image_before','image_after','resource_loaded','overlay_continuation','after_fade','terminal_name','terminal_portrait','terminal_dialogue','terminal_confirmation','terminal_panel_dialogue','admission')
 for key in common:
  if key in old:need(guest(row[key])==guest(old[key]),'every accepted original forward record '+key)
 retained=set().union(*(page_keys(old[k]) for k in common if k in old));need(all(row['blobs'].get(k)==old['blobs'][k] for k in retained),'all accepted intermediate pages retained byte for byte')
 need(all(sha(bytes.fromhex(v))==k for k,v in row['blobs'].items()),'every current content-addressed page rehashed');validate_pages(row,row['blobs'])
 lengths=dict(CRT_APIs=old['terminal_panel_dialogue']['prefix']['CRT_APIs'],task_APIs=len(old['task_APIs']),resource_steps=len(old['resource_initialization']),task_calls=len(old['task_calls']),task_writes=len(old['task_writes']),APIs=len(old['APIs']))
 for field,n in lengths.items():
  key='resource_initialization' if field=='resource_steps' else field
  need(p[field]==n and guest(row[key][:n])==guest(old[key][:n]),'exact accepted forward prefix length and bytes '+field)
 need(len(row['APIs'])==p['APIs'],'follow-up adds no uncaptured world clock or new base platform leaves')
 need(p['extra_counts']==old['extra_original_instruction_counts'],'frozen original-code accounting at the accepted boundary')
 expected_wire=max(old['terminal_panel_dialogue']['new_observer_wire_indices'])+1
 need(p['GPU_wire']==expected_wire and p['CRT_wire']==old['CRT_APIs'][lengths['CRT_APIs']-1]['wire_end'],'actual forward platform cursors, excluding old cleanup')
 ticks=[a for a in row['APIs'][:p['APIs']] if a['name']=='GetTickCount'];fixed_ticks=[a['result'] for a in old['APIs'] if a['name']=='GetTickCount']
 need([a['result'] for a in ticks]==fixed_ticks and all(a['actual_API_executed'] is False and a['captured_platform_input'] is True for a in ticks),'same captured parent clock stream with honest provenance')
 tls_platform(row['platform'],SimpleNamespace(crt_draws=len(old['platform']['trace'])//3))
 def tls_guest(value):
  value=copy.deepcopy(value)
  for name in ('creation','cleanup'):
   for key in ('thread','native_index'):value[name].pop(key)
  for a in value['trace']:a.pop('actual_native_index')
  return value
 need(tls_guest(row['platform'])==tls_guest(old['platform']),'original TLS token semantics with independently checked current ownership')
 counts=None
 if replay:
  initialization=previous.ResourceInitializationReplay(row).execute();fixed_initialization=previous.ResourceInitializationReplay(old).execute()
  need(initialization['roots']==fixed_initialization['roots'],'actual original resource-constructor local traces equal fixed accepted source')
  old_portrait=portrait.Replay(row).execute();old_confirmation=previous.confirmation.Replay(row).execute();refs=previous.pixels(row)[1];old_group=previous.Replay(row,refs).execute()
  counts=dict(resource_initialization=initialization,portrait=old_portrait,confirmation=old_confirmation,layer7_group=old_group)
 return dict(fixed_acceptance_sha256=PARENT_ACCEPTANCE_SHA,fixed_source_sha256=PARENT_SOURCE_SHA,fixed_proof_sha256=PARENT_PROOF_SHA,parent_full_memory_CPU_queue_and_trace_equal=True,all_fixed_intermediate_pages_verified=True,independent_current_parent_forward=counts,no_historical_cleanup_projection=True)

def original_text(pointer):return previous.dialogue.namecheck.original_text(pointer)

def source(row):
 d=row['terminal_followup'];cfg=branch(row['input']['name']);raw=(ROOT/e.terminal.SCRIPT_PATH).read_bytes();need(sha(raw)==SCRIPT_SHA,'original T0004 identity')
 segment=next(s for s in previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);at=segment['code_start'];pc=cfg['first_PC'];base=num(read(d['before']['memory'],e.VM+16,4),0);commands=[]
 expected=[(156,30,20),(176,43,8),(184,17,6),(190,50,4),(194,51,4)] if cfg['role'] else [(168,43,8),(176,44,4),(180,17,6),(186,50,4),(190,51,4)]
 for want in expected:
  op,n=struct.unpack_from('<HH',raw,at+pc);need((pc,op,n)==want and read(d['before']['memory'],base+pc,n)==raw[at+pc:at+pc+n],'every original command byte/declared length')
  commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
 need(pc==cfg['final_PC'] and struct.unpack_from('<HH',raw,at+pc)==(43,8) and num(raw,at+pc+4)==0x20000004,'next original43/config4 remains beyond this new confirmation')
 if cfg['role']:
  need(struct.unpack_from('<4I',raw,at+160)==tuple(0x20000000+x for x in (7,1,0,30)) and num(raw,at+180)==0x20000007,'complete four literal role operands and config7 text selector')
 else:need(num(raw,at+172)==0x20000008,'original config8 text selector')
 need(num(raw,at+(188 if cfg['role'] else 184),'H')==cfg['text_index'],'original text table index')
 need(d['commands']==commands,'only intended original follow-up dispatches')
 end=segment['code_end'];packed=num(raw,end+4+cfg['text_index']*4);span=packed>>20;text_at=end+(packed&0xFFFFF);text=raw[text_at:text_at+span]
 need(text[-2:]==bytes(2) and len(text)==span and 0 not in text[:-2] and 2<=span<=512 and span%2==0,'bounded original complete single ANSI text')
 need((text_at,text[:-2].hex())==((1260,'a6d1ae76a14ba14ba148') if cfg['role'] else (3366,'a14ba14ba14ba14b')),'independent exact next text identity')
 configs={i:list(struct.unpack_from('<19h',e.CODE,0x624520-0x400000+i*38)) for i in (7,8)}
 need(configs[7][0]==4 and configs[8][0]==5,'configuration indices independently select layer4/layer5')
 md=Cs(CS_ARCH_X86,CS_MODE_32);rules=[]
 for va,want in {0x4051A9:('call','0x403730'),0x4CC196:('lea','edx, [ecx + ecx + 0x16]')}.items():
  ins=next(md.disasm(e.CODE[va-0x400000:va-0x400000+16],va,count=1));need((ins.mnemonic,ins.op_str)==want,'original replacement/side-bank source rule');rules.append(dict(va=va,hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
 body=list(md.disasm(e.CODE[EXTRA_RANGE[0]-0x400000:EXTRA_RANGE[1]-0x400000],EXTRA_RANGE[0]));need(body and body[-1].address+body[-1].size==EXTRA_RANGE[1] and body[-1].mnemonic=='ret','finite whole original44 body')
 need(tuple(e.EXTRA_RANGES)==(EXTRA_RANGE,),'only original44 finite source range added')
 return dict(segment=cfg['segment'],script_sha256=SCRIPT_SHA,commands=commands,final_PC=pc,selected_layer=cfg['layer'],text=dict(index=cfg['text_index'],source_offset=text_at,hex=text[:-2].hex()),configurations=configs,original_rules=rules,original44=dict(start=EXTRA_RANGE[0],end=EXTRA_RANGE[1],sha256=sha(e.CODE[EXTRA_RANGE[0]-0x400000:EXTRA_RANGE[1]-0x400000])))

def capture_list(value):
 out=[]
 def visit(x,path):
  if isinstance(x,dict):
   if CAPTURE_KEYS<=x.keys():out.append((path,x));return
   for k,v in x.items():visit(v,path+'/'+str(k))
  elif isinstance(x,list):
   for i,v in enumerate(x):visit(v,path+'/'+str(i))
 visit(value,'');return out

def new_resources(row):
 d=row['terminal_followup'];return [r for r in d['resources'] if r['create_wire_index']>=d['prefix']['GPU_wire']]

def text_update(raw,origin,obj):
 need(isinstance(raw,bytes) and len(raw)==0xAB8 and isinstance(origin,list) and len(origin)==2 and all(type(v)is int and 0<=v<=65535 for v in origin),'whole original text update input')
 count=num(raw,22,'H');need(0<=count<=10,'bounded original text update count')
 if count==0:
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  for va,want in {0x4CB254:('mov','cx, word ptr [eax + 0x16]'),0x4CB262:('mov','word ptr [ebp - 0x14], 0'),0x4CB287:('cmp','eax, ecx'),0x4CB289:('jge','0x4cb5c5'),0x4CB5C5:('mov','al, 1'),0x4CB5D7:('ret','8')}.items():
   i=next(md.disasm(e.CODE[va-0x400000:va-0x400000+16],va,count=1));need((i.mnemonic,i.op_str)==want,'finite original empty-group loop and natural return')
  return dict(after_hex=raw.hex(),draws=[],readiness=True)
 predict=types.FunctionType(previous.text_update.__code__,dict(previous.text_update.__globals__,OBJECT=obj));return predict(raw,origin)

def pixels(row):
 d=row['terminal_followup'];cfg=branch(row['input']['name']);provenance=source(row);catalog,_=source_names();refs={}
 for r in new_resources(row):
  if r['kind']=='portrait':
   entry=catalog['roles']['1'];raw=(ROOT/entry['image_path']).read_bytes();need(len(raw)==262168 and sha(raw)==SC001_SHA==entry['image_sha256'],'entire original SC001 identity')
   need(r['upload_hex']==r['readback']['hex']==raw[24:].hex() and r['readback']['sha256']==sha(raw[24:]),'every original SC001 texel equals actual complete current readback')
   need(len(r['copy_rows'])==512,'all512 original portrait copy calls')
   for i,c in enumerate(r['copy_rows']):need(c==dict(row=i,args=[r['lock']['bits']+i*512,r['constructed']['file_pointer']+24+i*512,512],caller=0x40483F),'original full row copy ABI')
   need(r['lock']['pitch']==512 and len(bytes.fromhex(r['lock']['hex']))==262144,'whole native portrait lock extent');refs[r['generation']]=dict(portrait=raw);continue
  need(r['kind'] in ('name','text'),'known new source resource kind')
  b=r['font_boundary'];sp=b['CPU']['ESP'];args=[num(read(b['memory'],sp+4+i*4,4),0) for i in range(14)];caller=0x4CA7CB if r['kind']=='name' else 0x4CAD09
  need(r['pending_font']==dict(entry=num(read(b['memory'],0x5920A0,4),0),caller=caller,args=args,CPU=b['CPU'],first_instruction_executed=False) and b['CPU']['EIP']==r['pending_font']['entry'] and num(read(b['memory'],sp,4),0)==caller,'whole original live font ABI and unexecuted entry')
  if r['kind']=='name':
   raw=original_text(catalog['roles']['1']['name_pointer']);need(raw.hex()=='b3cdaca5af53' and args==[20,0,0,0,700,0,0,0,1,5,0,0,0,0x5BF62C],'source role1 name and original height20/weight700 font')
   reference=raster_name(raw,args[:-1],original_text(args[-1]));need(r['record']==node(4)+0x60,'source new layer4 name record')
  else:
   raw=bytes.fromhex(provenance['text']['hex']);obj=read(b['memory'],text_object(cfg['layer']),0x18);alt=bool(obj[0x14]);width=num(obj,0xE if alt else 0xC,'h')&0xFFFFFFFF;height=num(obj,0x12 if alt else 0x10,'h')&0xFFFFFFFF
   need(args==[height,width,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C] and r['record']==text_record(cfg['layer']),'original text font fields and count-derived record, not template font-size')
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

def gpu_calls(row):
 return row['GPU_APIs'][:4]+row['terminal_name']['GPU_APIs']+row['terminal_portrait']['GPU_APIs']+row['terminal_dialogue']['GPU_APIs']+row['terminal_panel_dialogue']['GPU_APIs']+row['terminal_followup']['GPU_APIs']

def native(row,old=None):
 """Audit current receipts by creation ordinal, with no byte identity masks."""
 d=row['terminal_followup'];old=parent_case(row) if old is None else old;helper_contract();m=previous.gpu_mapping(row);gt=row['GPU_trace'];ct=row['CRT_trace'];ledger=row['followup_resources_after_cleanup'];by_create={r['create_wire_index']:r for r in ledger};by_gen={r['generation']:r for r in ledger}
 need(row['current_CRT_hello']['pointer_bytes']==row['current_GPU_hello']['pointer_bytes']==4 and row['current_GPU_hello']['window_visible'] is False and row['current_GPU_hello']['image_size']==[512,512] and row['current_CRT_hello']['GPU_created'] is False,'actual bounded headless x86 CRT/GPU owners')
 need(len(by_create)==len(by_gen)==len(ledger)==8,'eight distinct creation generations in either complete branch')
 need(len(d['resources'])==len(ledger) and len(d['resources_before'])==(5 if branch(row['input']['name'])['role'] else 7),'complete prefix, forward and teardown resource ledgers')
 seeded=[]
 for r in d['resources']:
  if r['create_wire_index']<d['prefix']['GPU_wire']:
   before=copy.deepcopy(r);before.update(alive=True,release_wire_index=None);before.pop('alive_after_forward',None);before.pop('released_phase',None);seeded.append(before)
 need(seeded==d['resources_before'],'every seeded retained resource is the exact original current creation generation')
 oldblocks={'GYBC':row['resource_loaded'],'name5':row['terminal_name'],'portrait32':row['terminal_portrait'],'text5':row['terminal_dialogue']};oldblocks.update({'text7_'+str(s['text_index']):s for s in row['terminal_panel_dialogue']['sentences']})
 for r in seeded:
  b=oldblocks[r['label']];need(all(r[k]==b[k] for k in ('texture','lock','upload_hex','readback')),'all retained resource metadata bound to original current prefix captures')
 need(d['GPU_APIs']==[x['call'] for x in d['leaves'] if x['kind']=='GPU'] and d['calls']==[x['call'] for x in d['leaves'] if x['kind']=='GDI'] and row['CRT_APIs'][d['prefix']['CRT_APIs']:]==[x['call'] for x in d['leaves'] if x['kind']=='CRT'],'every original platform leaf belongs once to its full current receipt ledger')
 for r in new_resources(row):
  a,z=r['leaves'];leaves=d['leaves'][a:z];need(0<=a<z<=row['followup_cleanup'][0]['leaves'][0] and r['GPU_APIs']==[x['call'] for x in leaves if x['kind']=='GPU'] and r['calls']==[x['call'] for x in leaves if x['kind']=='GDI'] and r['conversions']==[c for c in d['conversions'] if c['resource_label']==r['label']],'complete actual original resource leaf/conversion interval')
 live={};logical={};ci=readbacks=peak=0;calls=gpu_calls(row);observers={o['wire_index']:o for o in d['readback_observers']}
 need(len(observers)==len(d['readback_observers']),'every current follow-up observer classified once')
 for label,tr in (('GPU',gt),('CRT',ct)):
  for i,t in enumerate(tr):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok'] is True,'complete ordered successful actual '+label+' wire')
 oldmap=previous.gpu_mapping(old)
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
  need(c.get('wire_index',i)==i and c['op']==op and c['native_result']==result and c['result']==previous.gpu_value(result,m) and c['actual_API_executed'] is True,'original COM call bound to exact current raw wire')
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
  need(previous.gpu_value(q,m)==expected,'entire independently translated current original COM request')
  if i>=d['prefix']['GPU_wire']:
   need((c['generation'],c['record'],c['resource_kind'],c['resource_label'],c['phase'])==(r['generation'],r['record'],r['kind'],r['label'],'forward' if i<d['forward_wire_end'] else 'cleanup'),'current leaf has exact generation, record and execution phase')
  if i==d['forward_wire_end']-1:need(False,'last forward wire is an observer, never an original COM call')
 need(ci==len(calls) and peak==(8 if branch(row['input']['name'])['role'] else 7),'all original COM calls and exact bounded simultaneous texture peak')
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
 constructed=[row['terminal_portrait']['constructed']]+[r['constructed'] for r in new_resources(row) if r['kind']=='portrait']
 for b in constructed:
  for x in b['native_allocation_readbacks']:
   i=x['wire_index'];covered.extend((i-1,i));a=ct[i-1];z=ct[i];need(a['request']['op']=='sync' and a['request']['hex']==a['reply']['result']['hex']==x['result']['hex'] and z['request']==dict(id=i+1,op='readback',pointer=x['result']['pointer']) and z['reply']['result']==x['result'] and len(bytes.fromhex(x['result']['hex']))==x['bytes'],'entire original file/vector current native observer and preceding full mirror')
 need(sorted(covered)==list(range(len(ct)-1)),'every current CRT wire classified exactly once')
 # Every opaque owner token is checked by the frozen raw-owner audit; payload
 # masks in its returned comparison view are never used as proof of bytes.
 need(previous.crt_semantics(row)[:d['prefix']['CRT_wire']]==previous.crt_semantics(old)[:d['prefix']['CRT_wire']],'every current fixed-prefix CRT control request and complete initialized data; actual uninitialized inputs independently executed')
 blocks=[row['terminal_name'],row['terminal_dialogue']]+row['terminal_panel_dialogue']['sentences']+[r for r in new_resources(row) if r['kind'] in ('name','text')];gm={x['guest']:x['native'] for x in d['GDI_handle_projection']}
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

class Replay(previous.Replay):
 """Independent x86 execution of the new forward and its actual late roots."""
 def __init__(self,row,refs):
  self.row=row;self.d=row['terminal_followup'];self.n=self.p=dict(before=self.d['before']);self.refs=refs;self.image=e.CODE;self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.objects={};self.locks={};self.cleaning=False;self.current_resource=None;self.GDI_cursors={};self.by_gen={r['generation']:r for r in self.d['resources']};self.by_label={r['label']:r for r in self.d['resources']}
  for r in self.d['before']['memory']:
   need(len(bytes.fromhex(r['hex']))==r['bytes'],'complete declared before region');self.u.mem_map(r['pointer'],r['bytes']);self.u.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  self.restore(self.d['before']['CPU']);need(self.cpu()==self.d['before']['CPU'] and len(self.cpu())==57,'all57 architectural pending registers restored')
  self.blocks={};self.history=[];self.files=set();self.depth=0;self.native_file=None;self.user_sizes={};self.wire=self.d['prefix']['CRT_wire'];self.criticals={}
  for t in row['CRT_trace'][:self.wire]:
   if t['request']['op']=='initialize':self.criticals[t['request']['guest']]=t['reply']['result']['pointer']
  for a in row['CRT_APIs'][:self.d['prefix']['CRT_APIs']]:
   if a['name']=='HeapAlloc':
    r=row['CRT_trace'][a['wire_end']-1]['reply']['result'];p=a['value'];need(p==HEAP_BASE+len(self.history)*0x200000,'original ordinal guest heap addresses');b=dict(guest=p,native=r['pointer'],bytes=a['args'][2],freed=False);self.history.append(b);self.blocks[p]=b
   elif a['name']=='HeapFree':b=self.blocks.pop(a['args'][2]);b['freed']=True
  self.crt_case=dict(native_trace=row['CRT_trace'],native_hello=row['current_CRT_hello'],fixture_inputs=dict(heap_token_translation=dict(guest=num(self.read(0x80AB28,4),0))))
  self.filebytes=(ROOT/source_names()[0]['roles']['1']['image_path']).read_bytes();need(sha(self.filebytes)==SC001_SHA,'current independent SC001 native-read input')
  original=portrait.crtcheck.Replay.api
  sizes=tuple(b['bytes'] for b in self.history)+(262208,128)
  def constants(code):
   vals=[]
   for v in code.co_consts:
    if isinstance(v,types.CodeType):v=constants(v)
    elif v==(262208,128,262208):v=sizes
    elif v==b'data\\adv\\bin\\sc004.bin':v=b'data\\adv\\bin\\sc001.bin'
    elif v=='data\\adv\\bin\\sc004.bin':v='data\\adv\\bin\\sc001.bin'
    vals.append(v)
   return code.replace(co_consts=tuple(vals))
  self.crt_api=types.FunctionType(constants(original.__code__),original.__globals__)
 def locate(self,p,n=1):return portrait.crtcheck.Replay.locate(self,p,n)
 def sync(self,p):return portrait.crtcheck.Replay.sync(self,p)
 def consume(self,op,**kw):
  if 'handle' in kw:need(kw['handle']==0x62001000 and self.native_file is not None,'live current logical file owner');kw['handle']=self.native_file
  need(self.wire<len(self.row['CRT_trace']),'bounded current native cursor');t=self.row['CRT_trace'][self.wire];need(t['request']==dict(id=self.wire+1,op=op,**kw),'independent entire native request '+op);need(t['reply']['id']==self.wire+1 and t['reply']['ok'] is True,'actual ordered successful native response');self.wire+=1;r=copy.deepcopy(t['reply']['result'])
  if op=='open':need(0<r['handle']<0xFFFFFFFF,'actual current native file');self.native_file=r['handle'];r['handle']=0x62001000
  elif op=='file_close':self.native_file=None
  elif op in ('enter','leave'):
   b=bytearray.fromhex(r['critical_hex']);need(len(b)==24,'entire actual current critical output')
   for off in (0,12,16):
    if num(b,off) not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off+(0x80A4B0-0x80A480)*0x100)
   r['critical_hex']=b.hex()
  return r
 def crt_leaf(self,c):
  sp=self.cpu()['ESP'];args=c['args'];nm=c['name'];slot=c['import_slot'];need(CRT_IMPORTS.get(slot)==(nm,c['pop']) and num(self.read(slot,4),0)==c['target'] and c['wire_start']==self.wire,'unchanged original CRT IAT/ABI and exact native cursor')
  if nm=='HeapValidate':
   p,b=self.locate(args[2]);raw=self.read(p,b['bytes']);size=num(raw,16);need(p==args[2] and (size+51)&~15==b['bytes'] and raw[28:32]==bytes([0xFD])*4,'original complete debug header and aligned size before validation');self.user_sizes[p]=size
  if nm not in ('HeapFree','DeleteCriticalSection','HeapDestroy'):
   a=copy.deepcopy(c);a['va']=a['target'];a['void_return_normalized']=a.get('void_return_normalized',False)
   for out in a['memory_outputs']:
    if 'native_hex' in out:need(out['native_hex']==self.row['CRT_trace'][c['wire_end']-1]['reply']['result']['critical_hex'],'entire current native critical provenance');out.pop('native_hex')
   saved=getattr(self,'case',None);self.case=self.crt_case
   try:self.crt_api(self,a)
   finally:self.case=saved
   if nm=='CreateFileA':need(c['native_handle']==self.native_file,'actual native file handle projection')
   return
  need(not c['new_mappings'] and not c['memory_outputs'],'original release leaves cannot create or modify guest buffers')
  if nm=='HeapFree':
   need(c['return_va']==0x578915 and args[:2]==[0x61001000,0] and self.depth>0,'original native heap free ABI and held source lock');p,b=self.locate(args[2]);need(p==args[2] and p in self.user_sizes,'exact owned debug allocation validated before free');raw=self.sync(p);need(raw[:self.user_sizes[p]+36]==bytes([0xDD])*(self.user_sizes[p]+36),'all original user/header/guard poison before native free');need(self.consume('free',heap=self.row['current_CRT_hello']['heap'],flags=0,pointer=b['native'])==dict(value=1,pointer=b['native'],before_hex=raw.hex()),'entire actual native free buffer including untouched alignment');b['freed']=True;del self.blocks[p];value=1
  elif nm=='DeleteCriticalSection':
   need(self.cleaning and len(args)==1 and args[0] in self.criticals and self.depth==0,'original teardown deletes a currently owned source critical section');p=self.criticals.pop(args[0]);need(self.consume('delete',guest=args[0],pointer=p)==dict(value=1),'actual current original critical deletion');value=0
  else:
   need(self.cleaning and args==[0x61001000] and not self.blocks and not self.criticals and self.depth==0 and not self.files,'original heap destroy after every live block/file/lock release');need(self.consume('heap_destroy',heap=self.row['current_CRT_hello']['heap'])==dict(value=1),'actual original owned heap destruction');value=1
  need(c['value']==value and c['wire_end']==self.wire,'complete actual release native cursor and result');self.return_leaf(c,value)
 def return_leaf(self,c,value):
  self.u.reg_write(x86.UC_X86_REG_EAX,value);self.u.reg_write(x86.UC_X86_REG_ESP,c['sp']+4+c['pop']);self.u.reg_write(x86.UC_X86_REG_EIP,c['return_va'])
 def setup_raster(self,label):
  r=self.by_label[label];self.current_resource=label;self.cfg=self.refs[r['generation']]['geometry'];self.reference=self.refs[r['generation']]['reference'];calls=r['calls'];self.raw=bytes.fromhex(self.reference['text_hex']);self.local_text=self.cpu()['EBP']-0x108 if r['kind']=='name' else None;self.old_font=self.brush=0
  o=dict(logical_measurement_dc=num(self.read(e.MAIN+0xB208,4),0),font=calls[0]['result'],raster_dc=calls[6]['result'],bitmap=calls[7]['result'],ACP=self.reference['ACP'],measured=self.reference['measured'],selected_face=self.reference['selected_face']);o['fresh_owned_measurement_dc']=o['logical_measurement_dc'];self.case=dict(offscreen=o,parent_boundary=dict(pending_font=r['pending_font']))
  from tools import school_retained_name_raster as work
  proxy=SimpleNamespace(**dict(vars(work),RASTER=r['raster_address'],IMPORTS=e.GDI))
  def constants(code):
   vals=[]
   for v in code.co_consts:
    if isinstance(v,types.CodeType):v=constants(v)
    elif v==0x4CA7CB and r['kind']=='text':v=0x4CAD09
    vals.append(v)
   return code.replace(co_consts=tuple(vals))
  self.check_raster_API=types.FunctionType(constants(NameABI.api.__code__),dict(NameABI.api.__globals__,work=proxy))
 def leaf(self,item):
  c=item['call'];kind=item['kind'];sp=self.cpu()['ESP'];ret=num(self.read(sp,4),0);args=[num(self.read(sp+4+i,4),0) for i in range(0,c['pop'],4)];need((sp,ret,args)==(c['sp'],c['return_va'],c['args']),'entire original platform stack and return ABI')
  if kind=='CRT':self.crt_leaf(c);return
  if kind=='GDI':
   label=item['resource_label'];r=self.by_label[label];idx=self.GDI_cursors.get(label,0);need(idx<len(r['calls']) and c==r['calls'][idx],'sequential original GDI call belongs to exactly this resource');self.GDI_cursors[label]=idx+1
   if idx==0:self.setup_raster(label)
   need(self.current_resource==label and num(self.read(c['import_slot'],4),0)==c['target'],'unchanged current original GDI IAT')
   if idx<23:
    if c['name']=='lstrlenA' and self.local_text is None:self.local_text=args[0]
    call=copy.deepcopy(c);call['dc_translated_args']=call['args']
    if c['name']=='CreateDIBSection':call['native_bits']=r['GDI_trace'][idx]['native_result']['native_bits']
    self.check_raster_API(self,dict(key='retained_name_GDI',va=c['target'],call=call));return
   o=self.case['offscreen'];want=[('SelectObject',0x4058D8,[o['raster_dc'],r['calls'][8]['result']]),('DeleteObject',0x405921,[o['bitmap']]),('DeleteDC',0x40596A,[o['raster_dc']]),('DeleteObject',0x4D1C1B,[o['font']])][idx-23];need((c['name'],ret,args)==want and not c['memory_outputs'] and c['result']==(o['bitmap'] if idx==23 else 1),'natural original GDI cleanup of this actual raster');self.return_leaf(c,c['result']);return
  if kind=='TASK':
   name,slot,caller=previous.dialogue.e.parent.TASK_APIS[c['target']];need((c['name'],c['import_slot'],ret)==(name,slot,caller) and num(self.read(slot,4),0)==c['target'] and c['value']==c['result']==0 and c['actual_API_executed'] is True and c['memory_outputs']==[] and c['new_mappings']==[] and args==([0] if name=='ImmGetOpenStatus' else [e.INPUT+0x528]),'only current actual null IME/empty task input leaves');self.return_leaf(c,0);return
  need(kind=='GPU' and c['generation'] in self.by_gen,'only a declared current generation COM leaf');r=self.by_gen[c['generation']];t=r['texture'];slot=c['slot'];bp=self.cpu()['EBP'];w,h=r['size'];out=[]
  need(c['target']==(self.row['resource_loaded']['owner_device']['methods']['80'] if slot==80 else t['methods'][str(slot)]) and c['record']==r['record'],'current COM method and original record identity')
  def output(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   need(not self.cleaning and args==[self.row['resource_loaded']['owner_device']['pointer'],w,h,1,0,25,1,r['record']+44] and ret==0x403C8A and num(self.read(r['record']+44,4),0)==0,'original current generation creation after prior record release');self.identities(c['result']);output(args[-1],struct.pack('<I',t['pointer']))
  else:
   need(num(self.read(r['record']+44,4),0)==t['pointer'],'original record currently owns this COM receiver')
   if slot==56:
    releasing=ret==0x403A44;desc=struct.pack('<8I',25,1,0,1,w*h*2,0,w,h);need(ret in (0x403A44,0x403CBE) and args==[t['pointer'],0,bp-(36 if releasing else 52)] and c['result']['hex']==desc.hex(),'whole independent original descriptor and natural release/create caller');output(args[-1],desc)
   elif slot==64:need(not self.cleaning and args==[t['pointer'],0,num(self.read(bp+8,4),0),0,2048] and ret==0x40395E,'original new generation LockRect');output(r['lock']['bits'],bytes.fromhex(r['lock']['hex']));output(args[2],struct.pack('<II',r['lock']['pitch'],r['lock']['bits']))
   elif slot==68:need(not self.cleaning and args==[t['pointer'],0] and ret==0x4039D3 and self.read(r['lock']['bits'],len(bytes.fromhex(r['upload_hex']))).hex()==r['upload_hex'],'every independently executed original upload byte')
   else:need(slot==8 and args==[t['pointer']] and ret==0x40378D,'only original current generation Release')
  need(out==c['memory_outputs'] and c['value']==0,'all and only independently derived original COM outputs')
  for x in out:self.put(x['pointer'],bytes.fromhex(x['hex']))
  self.return_leaf(c,0)
 def allocation_observers(self,capture):
  for x in capture.get('native_allocation_readbacks',[]):
   p=x['guest'];need(p in self.blocks and x['bytes']==self.blocks[p]['bytes'] and self.wire==x['wire_index']-1,'only this actual original constructor full native allocation observers');raw=self.sync(p);b=self.blocks[p];r=self.consume('readback',pointer=b['native']);need(r==x['result']==dict(pointer=b['native'],hex=raw.hex()),'entire original constructor file/vector native buffers including uninitialized padding')
 def execute(self):
  d=self.d;index=count=writes=roots=0;ih=hashlib.sha256();wh=hashlib.sha256();observed=[];commands=[];conversions=[];queries=[];copies=[];updates=[];last=d['before']['trace'];current=None;boundaries=capture_list(d);seen=set();observer_seen=set();self.forward_end=self.row['followup_cleanup'][0]['leaves'][0]
  def mark():return dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())
  boundary_counts={b['local_trace']['instructions'] for path,b in boundaries}
  def check_boundaries():
   if count not in boundary_counts:return
   for path,b in boundaries:
    if path not in seen and b['local_trace']==mark() and b['CPU']['EIP']==self.cpu()['EIP']:
     self.capture(b)
     need(b['trace']['instructions']==d['before']['trace']['instructions']+count and b['trace']['writes']==d['before']['trace']['writes']+writes,'actual cumulative counters extend fixed complete forward boundary');seen.add(path)
     if 'native_allocation_readbacks' in b and id(b) not in observer_seen:self.allocation_observers(b);observer_seen.add(id(b))
  def code(u,at,size,_):
   nonlocal index,count
   if at==self.stop:u.emu_stop();return
   check_boundaries()
   if index<self.forward_end and at==d['leaves'][index]['call']['target']:self.leaf_cursor=index;self.leaf(d['leaves'][index]);index+=1;return
   if at==0x4CE9C5:
    pc=num(self.read(e.VM+28,4),0);p=num(self.read(e.VM+16,4),0)+pc;op,n=struct.unpack('<HH',self.read(p,4));commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=p));need(pc<branch(self.row['input']['name'])['final_PC'],'next43 after new confirmation is never dispatched')
   if at==0x405869:
    sp=self.cpu()['ESP'];args=[num(self.read(sp+i,4),0) for i in range(0,24,4)];need(self.current_resource is not None,'original conversion belongs to actual current raster');r=self.by_label[self.current_resource];conversions.append(dict(entry=at,args=args,resource_label=r['label'],record=r['record'],rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at==0x56D4D0 and num(self.read(self.cpu()['ESP'],4),0)==0x40483F:
    sp=self.cpu()['ESP'];copies.append(dict(row=len(copies),args=[num(self.read(sp+4+i,4),0) for i in (0,4,8)],caller=0x40483F))
   if at in e.QUERIES:
    cpu=self.cpu();queries.append(dict(entry=at,CPU=cpu,receiver=cpu['ECX'],stack_hex=self.read(cpu['ESP'],68).hex(),selected_layer=num(self.read(e.VM+0x1CC,1),0,'B'),nodes={str(i):self.read(node(i),0xE0).hex() for i in (4,5,7)},objects={str(i):self.read(text_object(i),0xAB8).hex() for i in (4,5,7)}))
   if at==0x4CB220 and self.cpu()['ECX'] in (text_object(4),text_object(5),text_object(7)):
    layer=next(i for i in (4,5,7) if self.cpu()['ECX']==text_object(i));obj=text_object(layer);origin=[num(self.read(node(layer)+30,2),0,'H'),num(self.read(node(layer)+32,2),0,'H')];updates.append(dict(object=obj,expected=text_update(self.read(obj,0xAB8),origin,obj),draw_returns=0))
   if at==0x4CD541 and updates and not updates[-1].get('complete'):
    x=updates[-1];need(self.read(x['object'],0xAB8).hex()==x['expected']['after_hex'],'independent complete original AB8 timing and draw metadata');x['complete']=True
   if at==0x4CBF00 and updates and not updates[-1].get('complete'):
    sp=self.cpu()['ESP'];updates[-1].setdefault('draws',[]).append(dict(va='0x4cbf00',receiver=self.cpu()['ECX'],args=[num(self.read(sp+4+j*4,4),0) for j in range(9)],return_va=hex(num(self.read(sp,4),0))))
   if at==0x4CB4B2 and updates and not updates[-1].get('complete'):need(self.cpu()['EAX']&255==1,'original draw metadata body naturally returns AL1');updates[-1]['draw_returns']+=1
   need(at in e.ALLOWED and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only finite unchanged original follow-up instruction '+hex(at));count+=1;ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):
   nonlocal writes
   need(not 0x400000<=at<0x593000,'no original code/IAT mutation')
   if current['kind']=='keyboard':need(e.KEYBOARD<=at and at+size<=e.KEYBOARD+0xA00 or e.STACK<=at and at+size<=e.STACK+0x20000,'finite original keyboard fragment writes')
   writes+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if e.VM<=at<e.VM+0x9400 or e.KEYBOARD<=at<e.KEYBOARD+0xA00 or e.TASK<=at<e.TASK+0x190 or at==0:observed.append(dict(pc=self.cpu()['EIP'],address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
  frames={f['segments'][1]-1:f for f in d['frames']};starts={f['segments'][0]:f for f in d['frames']};bindings={b['segment_index']:b for b in d['bindings']};covered=[];shapes={}
  for f in d['frames']:
   a,z=f['segments'];need(z-a>=4 and f['complete'] is True,'whole completed task frame with exactly four normal roots');covered.extend(range(a,z))
   for j,(va,receiver) in enumerate(((0x40DB90,e.MANAGER),(0x40DC80,e.MANAGER),(0x425DE0,e.INPUT),(0x454CF0,e.TASK))):shapes[a+j]=(va,receiver)
   for j in range(a+4,z):need(d['segments'][j]['root'] is None and d['segments'][j]['kind']=='task','resource continuation is part of its existing task')
  need(sorted(covered+list(bindings))==list(range(len(d['segments']))) and len(bindings)==3,'all segments partitioned into complete frames and three independent captured inputs')
  check_boundaries();hooks=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)]
  try:
   for i,s in enumerate(d['segments']):
    current=s;need(self.cpu()==s['before_CPU'] and mark()==s['local_before'] and index==s['leaves'][0] and last==s['trace_before'],'continuous complete CPU, original trace and leaf input')
    if i in starts:need(self.state()==starts[i]['before'] and self.queue()==starts[i]['queue_before'],'every frame complete pre-state and queue')
    if i in bindings:
     b=bindings[i];need(s['kind']=='keyboard' and s['root'] is None and (s['entry'],s['stop'])==(0x4113D5,0x4116A4) and b['before_CPU']==s['before_CPU'] and b['trace_before']==last and b['local_before']==mark() and self.read(e.KEYBOARD,0xA00).hex()==b['before_hex'],'exact new captured keyboard entry')
     self.put(e.KEYBOARD+12,bytes.fromhex(b['capture']['raw_device_hex']));self.put(e.STACK+0xF800-4,struct.pack('<I',e.KEYBOARD))
     for key,value in dict(EBP=e.STACK+0xF800,ESP=e.STACK+0xF790,EFLAGS=0x202).items():self.u.reg_write(getattr(x86,'UC_X86_REG_'+key),value)
     need(self.cpu()==s['bound_CPU'] and self.read(e.KEYBOARD,0xA00).hex()==b['bound_hex'],'only complete raw device sample and finite input-root context bound')
    elif i in shapes:
     va,receiver=shapes[i];need(s['kind']=='task' and s['entry']==va and s['root']==dict(receiver=receiver,args=[]),'only four existing task frame roots');roots+=1;self.put(e.STACK+0xF000,struct.pack('<I',e.RETURN));self.u.reg_write(x86.UC_X86_REG_ESP,e.STACK+0xF000);self.u.reg_write(x86.UC_X86_REG_ECX,receiver)
     need(s['stop']==e.RETURN or va==0x454CF0 and s['stop']==num(self.read(0x5920A0,4),0),'only task may pause at natural original font entry')
    else:need(s['entry']==self.cpu()['EIP']==d['segments'][i-1]['stop'] and s['entry'] in (num(self.read(0x5920A0,4),0),0x403BD0,0x4CDE10,0x4CC0D2),'resource resumes exact pending original PC and stack')
    need(s['stop'] in (e.RETURN,0x4116A4,num(self.read(0x5920A0,4),0),0x403BD0,0x4CDE10,0x4CC0D2),'finite admitted natural stop points');self.stop=s['stop'];self.u.emu_start(s['entry'],0,count=4_000_000,timeout=60_000_000)
    need(self.cpu()==s['CPU'] and mark()==s['local_after'] and index==s['leaves'][1],'all57 CPU and independent original PC/store digest per segment')
    if s['stop']==e.RETURN:need(self.cpu()['ESP']==e.STACK+0xF004,'natural complete original frame root stack return')
    for key in ('instructions','writes'):need(s['trace_after'][key]-last[key]==s['local_after'][key]-s['local_before'][key],'actual cumulative original count delta')
    last=s['trace_after'];check_boundaries()
    if i in frames:
     f=frames[i];self.capture(f['capture']);need(f['after']==f['capture']['state'] and f['queue_after']==f['capture']['queue'] and f['capture']['trace']==last and f['capture']['local_trace']==mark(),'every frame all mapped-region SHA and complete CPU/queue/trace, including its after-state metadata')
  finally:
   for h in hooks:self.u.hook_del(h)
  need(index==self.forward_end and roots==4*len(d['frames']) and observed==d['writes'] and commands==d['commands'] and conversions==d['conversions'] and queries==d['queries'] and seen=={p for p,b in boundaries},'all current original roots, writes, commands, queries, conversions and full boundaries consumed')
  need(copies==sum((r['copy_rows'] for r in new_resources(self.row) if r['kind']=='portrait'),[]) and self.wire==d['CRT_forward_wire_end'],'all512 original SC001 copy ABIs and all current forward CRT operations')
  for x in updates:need(x.get('complete') and x.get('draws',[])==x['expected']['draws'] and x['draw_returns']==len(x['expected']['draws']),'independent full original text timing and every real draw return')
  need(all(self.GDI_cursors.get(r['label'])==27 for r in new_resources(self.row) if r['kind'] in ('name','text')),'all current original GDI calls consumed once')
  return dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest(),CPU_registers=57,complete_frames=len(d['frames']),new_forward_roots=0,full_memory_boundaries=len(seen),all_frame_region_SHA_verified=True,all_original_text_updates=len(updates))
 def cleanup(self):
  d=self.d;rows=self.row['followup_cleanup'];steps=self.row['cleanup_steps'];keys=('label','entry','args','receiver','cdecl');old=parent_case(self.row);expected=[{k:s[k] for k in keys} for s in old['cleanup_steps']]
  if branch(self.row['input']['name'])['role']:
   group=d['role']['pending_image']['args'][1];expected=[dict(label='supplemental_original_followup_text_destructor',entry=0x403730,args=[],receiver=text_record(4),cdecl=False),dict(label='supplemental_original_followup_portrait_container_destructor',entry=0x41F4E0,args=[group],receiver=e.MAIN+0x844,cdecl=False),dict(label='supplemental_original_followup_name_destructor',entry=0x403730,args=[],receiver=node(4)+0x60,cdecl=False)]+expected
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
  for group in (20,32)+((d['role']['pending_image']['args'][1],) if d['role'] else ()):need(self.read(e.MAIN+0x844+group*8,8)==bytes(8),'every current source resource bank originally cleared')
  for r in d['resources']:
   if e.VM<=r['record']<e.VM+0x9400:need(num(self.read(r['record']+44,4),0)==0,'every embedded old/new texture record naturally cleared')
  return dict(instructions=total_i,writes=total_w,independent_local_code_sha256=ih.hexdigest(),independent_local_write_sha256=wh.hexdigest(),CPU_registers=57,all_actual_original_roots=len(rows),all_root_full_memory_and_native_sync_verified=True,no_historical_CPU_or_SHA_projection=True)

def vw(state):
 v=bytes.fromhex(state['VM']);return num(v,28),num(v,32,'H')

def protocol(row):
 d=row['terminal_followup'];cfg=branch(row['input']['name']);scene=76 if cfg['role'] else 77;stream=previous.confirmation.captured_contract()['streams'][scene];bindings=d['bindings'];need(d['branch']==e.branch(row['input']['name']) and len(bindings)==3 and [b['capture'] for b in bindings]==stream['captures'],'separate exact captured76/77 idle/press/release cycle')
 need(len(row['terminal_confirmation']['bindings'])==3,'accepted first cycle never cleared or reused')
 for b in bindings:
  raw=bytes.fromhex(b['capture']['raw_device_hex']);before=bytes.fromhex(b['before_hex']);bound=bytearray(before);bound[12:268]=raw;bp=e.STACK+0xF800
  need(len(raw)==256 and len(before)==0xA00 and b['cycle']=='followup_confirmation' and b['bound_hex']==bound.hex() and b['after_hex']==predict_keyboard(bytes(bound)).hex(),'every byte of independently updated original A00 keyboard object')
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
  need(d['clear'] is None and not d['replacements'] and d['role_container']==portrait.parse((ROOT/source_names()[0]['roles']['1']['image_path']).read_bytes()),'win appends role resources without clearing or replacing old text')
  role=d['role'];p=role['pending_image'];catalog=source_names()[0]['roles']['1'];q=next(r for r in new_resources(row) if r['kind']=='portrait');need(role['role']==1 and role['configuration']==7 and role['node']==node(4) and role['name_record']==node(4)+0x60 and role['source']==catalog,'entire original role1 and configuration7 provenance')
  need(p['entry']==0x4CDE10 and p['receiver']==e.VM and p['caller']==0x4CC0D2 and p['CPU']['EIP']==p['entry'] and p['first_instruction_executed'] is False and p['path']=='data\\adv\\bin\\sc001.bin' and p['group_words']==[30,31] and p['side_byte']==0 and p['side_pointer']==node(4)+0x32 and p['side_getter']==0x4CA9B0 and p['args'][1]==30,'actual first side getter and original2*layer+22/+23 formula select registered group30')
  n=bytes.fromhex(p['node_hex']);need(list(struct.unpack_from('<2H',n,0x40))==p['group_words'] and n[0x32]==p['side_byte'] and q['label']=='portrait30' and q['constructed']['file_hex']==(ROOT/catalog['image_path']).read_bytes().hex() and q['constructed']['bank_hex']==struct.pack('<II',q['record'],1).hex(),'actual new side bank and complete original file at natural constructor boundary')
  readiness=[f for f in frames if f['phase']=='role_readiness'];need(len(readiness)==77 and vw(role['ready']['state'])==(176,0),'strict original delay/fade/background readiness requires77 complete tasks')
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
   need([num(z,o,'H') for o in (2,6,18,34,36)]==[mode,fade,delay,bg,bgcount] and vw(f['after'])==(176,0 if ready else 1),'independent role strict-counter transition and pre-update readiness')
 else:
  need(d['role'] is None and d['role_container'] is None and len(d['replacements'])==1,'timeout uses only original44 and same-record text replacement');clear=d['clear'];record=text_record(5);old=next(r for r in d['resources_before'] if r['label']=='text5');replacement=d['replacements'][0];new=next(r for r in new_resources(row) if r['kind']=='text')
  need(vw(clear['before']['state'])==(176,0) and vw(clear['after']['state'])==(180,0) and clear['GPU_wire_before']==clear['GPU_wire_after'] and num(read(clear['before']['memory'],text_object(5)+22,2),0,'H')==1 and num(read(clear['after']['memory'],text_object(5)+22,2),0,'H')==0 and read(clear['before']['memory'],record+44,4)==read(clear['after']['memory'],record+44,4)==struct.pack('<I',old['texture']['pointer']),'original44 clears count without GPU release or texture-pointer rewrite')
  need((replacement['entry'],replacement['caller'],replacement['record'],replacement['generation'],replacement['ledger_index'])==(0x403730,0x4051AE,record,old['generation'],d['resources_before'].index(old)) and replacement['before']['CPU']['EIP']==0x403730 and replacement['after']['CPU']['EIP']==0x4051AE and replacement['return_ESP']==replacement['before']['CPU']['ESP']+4==replacement['after']['CPU']['ESP'],'original405160 calls its own403730 and returns naturally before text raster')
  need(read(replacement['before']['memory'],record+44,4)==struct.pack('<I',old['texture']['pointer']) and read(replacement['after']['memory'],record+44,4)==bytes(4) and [c['op'] for c in replacement['GPU_APIs']]==['describe','release'] and all(c['generation']==old['generation'] and c['phase']=='forward' for c in replacement['GPU_APIs']) and replacement['GPU_APIs'][-1]['wire_index']<new['create_wire_index'] and new['record']==record and new['generation']!=old['generation'],'old generation released by original forward destructor before same-record new texture')
 for r in d['resources']:
  if r['alive']:need(num(read(final,r['record']+44,4),0)==r['texture']['pointer'],'every retained current record owns its correct live generation')
 need(d['accounting']==num(read(final,0x765720,4),0)==row['accounting_baseline']['texture_bytes']+sum(r['size'][0]*r['size'][1]*2 for r in d['resources'] if r['alive']),'all and only simultaneously live textures are accounted')
 return dict(VM_PC=cfg['final_PC'],VM_wait=1,selected_layer=cfg['layer'],new_text_index=cfg['text_index'],role=cfg['role'],actual_group=30 if cfg['role'] else None,no_input_hold_tasks=2,next43_unexecuted=True)

def final_summary(row):
 d=row['terminal_followup'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs']);want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'every current final-state page and selected summary field equals independently replayed final full memory');return True

def verify_case(row,old=None):
 p=prefix(row,old);provenance,refs=pixels(row);platform=native(row,old);timed=protocol(row);replay=Replay(row,refs);counts=replay.execute();d=row['terminal_followup'];equal(row['final'],d['final']['memory'],'all actual final mapped bytes');need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'all actual final57 CPU and unchanged original image/IAT')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'actual full cumulative source digests retained without reconstructing a SHA state from old hexdigest')
 summary=final_summary(row);cleanup=replay.cleanup();return dict(name=row['input']['name'],prefix=p,source=provenance,helper=helper_contract(),native=platform,timing=timed,added=counts,cleanup=cleanup,current_terminal_summary_pages_equal_verified_final_memory=summary,independent_whole_memory_CPU_and_new_original_trace=True,no_historical_cleanup_CPU_or_SHA_projection=True)

def verify(path):
 accepted_clock_inputs()
 with gzip.open(path,'rt',encoding='utf8') as f:data=json.load(f)
 need(data['schema_version']==1 and data['source_contract']==e.source_contract() and [r['input'] for r in data['cases']]==e.overlay.parent.corpus(),'exact source contract and both original branches');helpers=e.helpers('terminal-followup-proof');rows=[]
 for row in data['cases']:
  old=parent_case(row);proof=verify_case(row,old);ticks=[a['result'] for a in old['APIs'] if a['name']=='GetTickCount'];other=fresh_case(row['input'],helpers[0],helpers[1],ticks);verify_case(other,old)
  for key in ('initial','final'):equal(row[key],other[key],'fresh current owners every complete '+key+' region')
  for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'fresh complete original forward/cumulative digest/teardown '+key)
  for key in ('terminal_followup','followup_cleanup','followup_resources_after_cleanup'):need(guest(row[key])==guest(other[key]),'fresh current resources all full memory/57CPU/native inputs/local digests/frames/lifetimes '+key)
  proof['current_native_resources_recreated']=True;proof['complete_cumulative_digests_reproduced_by_new_full_original_instance']=True;rows.append(proof);print('independent followup',row['input']['name'],'all current resources and original roots verified',flush=True);del other;gc.collect()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,next_confirmation_released=False,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable independent proof');e.terminal.save(a.out,verify(ROOT/a.report))

