"""Independent original terminal script stop and complete current native lifetime."""
from tools.terminal_last_dialogue_verification import *
from tools import terminal_last_dialogue_verification as previous_stage
from tools import terminal_script_exit_emulation as e
from tools import terminal_followup_verification as followup_stage
from tools import terminal_next_dialogue_verification as next_stage
import ast,inspect,textwrap
ROOT=e.ROOT
PARENT_ACCEPTANCE=e.PARENT_ACCEPTANCE;PARENT_ACCEPTANCE_SHA=e.PARENT_ACCEPTANCE_SHA
PARENT_SOURCE=e.PARENT_SOURCE;PARENT_SOURCE_SHA=e.PARENT_SOURCE_SHA
PARENT_PROOF=e.PARENT_PROOF;PARENT_PROOF_SHA=e.PARENT_PROOF_SHA
IMPLEMENTATIONS=('tools/terminal_script_exit_emulation.py','tools/terminal_script_exit_verification.py','tools/terminal_script_exit_preservation.py','tools/tests/test_terminal_script_exit.py','tools/tests/test_terminal_script_exit_source.py')
load_report=previous_stage.load_report
gpu_mappings=previous_stage.gpu_mappings
resource_domain=previous_stage.resource_domain
resource_context=previous_stage.resource_context

def new_resources(row):
 d=row['terminal_script_exit'];return [r for r in d['resources'] if r['create_wire_index']>=d['prefix']['GPU_wire']]

def helper_contract():return previous_stage.helper_contract()

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'two original terminal script cases')
 delta=0 if name=='neutral_running' else 30
 values=((320,44,4),(324,43,8),(332,44,4),(336,43,8),(344,44,4),(348,31,12),(360,31,12),(372,24,12),(384,12,8),(392,21,4),(396,118,8),(404,19,4))
 return dict(first_PC=320+delta,final_PC=404+delta,segment=2 if delta==0 else 11,scene_capture=76 if delta==0 else 77,role=None,commands=[dict(PC=p+delta,opcode=op,bytes=n) for p,op,n in values])

@lru_cache(maxsize=1)
def parent_report():
 for path,want in ((PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),(PARENT_PROOF,PARENT_PROOF_SHA),(PARENT_SOURCE,PARENT_SOURCE_SHA)):
  h=hashlib.sha256()
  with (ROOT/path).open('rb') as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  need(h.hexdigest()==want,'fixed accepted last-dialogue '+path)
 return load_report(ROOT/PARENT_SOURCE)

def parent_case(row):return next(x for x in parent_report()['cases'] if x['input']==row['input'])
def accepted_clock_inputs():return {r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in parent_report()['cases']}

@lru_cache(maxsize=1)
def parent_trace_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed compact last-dialogue proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def prefix_trace(row):
 name=row['input']['name'];d=row['terminal_script_exit'];want=parent_trace_summaries()[name];actual=d['before']['trace']
 need(actual==want,'exact parent cumulative counters and digests '+name)
 need(d['prefix_preflight']==dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=want,actual=actual),'entire source prefix preflight independently bound')

def forward_only(row):
 d=row['terminal_last_dialogue'];end=row['last_dialogue_cleanup'][0]['leaves'][0]
 return dict(d,leaves=d['leaves'][:end],GPU_APIs=[c for c in d['GPU_APIs'] if c['wire_index']<d['forward_wire_end']])

def prefix(row,old=None,replay=True):
 old=parent_case(row) if old is None else old;d=row['terminal_script_exit'];fixed=old['terminal_last_dialogue']['final'];cfg=branch(row['input']['name'])
 for key in ('memory','CPU','state','queue','trace'):need(d['before'][key]==fixed[key]==row['terminal_last_dialogue']['final'][key],'entire fixed last-dialogue boundary '+key)
 need(d['before']['local_trace']==mark_zero() and vw(d['before']['state'])==(cfg['first_PC'],1),'new stage begins at original parent confirmation')
 need(guest(forward_only(row))==guest(forward_only(old)),'whole last-dialogue forward without historical cleanup')
 need(all(row['blobs'].get(k)==old['blobs'][k] for k in page_keys(forward_only(old))),'every fixed parent intermediate page retained exactly')
 p=d['prefix'];need((p['GPU_wire'],p['CRT_wire'])==(old['terminal_last_dialogue']['forward_wire_end'],old['terminal_last_dialogue']['CRT_forward_wire_end']),'exact fixed native forward cursors')
 n=sum(a['wire_end']<=p['CRT_wire'] for a in old['CRT_APIs'])
 for key,length in dict(CRT_APIs=n,task_APIs=len(old['task_APIs']),task_calls=len(old['task_calls']),task_writes=len(old['task_writes']),APIs=len(old['APIs'])).items():need(p[key]==length and guest(row[key][:length])==guest(old[key][:length]),'entire original parent ledger '+key)
 need(p['resource_steps']==len(old['resource_initialization']) and guest(row['resource_initialization'][:p['resource_steps']])==guest(old['resource_initialization']) and p['extra_counts']==old['extra_original_instruction_counts'] and len(row['APIs'])==p['APIs'],'fixed initialization/accounting and no new clocks')
 earlier=previous_stage.prefix(row,replay=replay);counts=None
 if replay:counts=previous_stage.Replay(row,previous_stage.pixels(row)[1]).execute()
 return dict(fixed_acceptance_sha256=PARENT_ACCEPTANCE_SHA,fixed_source_sha256=PARENT_SOURCE_SHA,fixed_proof_sha256=PARENT_PROOF_SHA,parent_full_memory_CPU_queue_and_trace_equal=True,earlier=earlier,independent_last_dialogue_forward=counts,no_historical_cleanup_projection=True)

EXTRA_RANGES=((0x4C5590,0x4C56BE),(0x4C5BC0,0x4C5CEC),(0x4C9590,0x4C9610),(0x4CB120,0x4CB175),(0x4CC8D0,0x4CC90E),(0x4CC910,0x4CC9D1),(0x4C7130,0x4C718A),(0x4C6DA0,0x4C6DCB))

def source(row):
 d=row['terminal_script_exit'];cfg=branch(row['input']['name']);raw=(ROOT/e.terminal.SCRIPT_PATH).read_bytes();need(sha(raw)==SCRIPT_SHA,'whole original T0004')
 s=next(s for s in previous_stage.previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);start=s['code_start'];base=num(read(d['before']['memory'],e.VM+16,4),0);commands=[]
 for c in cfg['commands']:
  p=c['PC'];n=c['bytes'];data=raw[start+p:start+p+n]
  need(struct.unpack_from('<HH',data)==(c['opcode'],n) and read(d['before']['memory'],base+p,n)==data,'every original remaining command byte')
  commands.append(dict(c,source_pointer=base+p,raw_hex=data.hex()))
 need(start+cfg['final_PC']+4==s['code_end'] and d['commands']==commands and d['branch']==cfg,'complete original tail ending at special19')
 operands={43:[[7],[8]],31:[[7,30],[8,30]],24:[[4,3]],12:[[60]],118:[[60]]}
 actual={}
 for c in commands:
  words=list(struct.unpack('<'+'I'*((c['bytes']-4)//4),bytes.fromhex(c['raw_hex'])[4:]));need(all(w>>28==2 for w in words),'original literal operand tags')
  if words:actual.setdefault(c['opcode'],[]).append([w&0xFFFFFFF for w in words])
 need(actual==operands,'all exact original remaining operands')
 need(e.EXTRA_RANGES==EXTRA_RANGES and e.RANGES==e.parent.RANGES+EXTRA_RANGES and e.ALLOWED==frozenset(a for lo,hi in e.RANGES for a in range(lo,hi)),'only independently identified original function ranges added')
 need(e.ScriptExitMachine.source_code.__code__ is e.parent.LastDialogueMachine.source_code.__code__,'original source guard instruction algorithm unchanged')
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 for a,b in EXTRA_RANGES:
  seq=list(md.disasm(e.CODE[a-0x400000:b-0x400000],a));need(seq[0].mnemonic=='push' and seq[0].op_str=='ebp' and seq[-1].mnemonic=='ret' and seq[-1].address+seq[-1].size==b,'exact original prologue-through-ret function extent')
 return dict(segment=cfg['segment'],script_sha256=SCRIPT_SHA,commands=commands,operands=operands,termination_PC=cfg['final_PC'],special19_not_advanced=True)

def capture_query(replay,at,cpu):
 return dict(entry=at,CPU=cpu,receiver=cpu['ECX'],stack_hex=replay.read(cpu['ESP'],68).hex(),state=dict(VM_PC=num(replay.read(e.VM+28,4),0),VM_wait=num(replay.read(e.VM+32,2),0,'H'),VM_active=num(replay.read(e.VM+4,1),0,'B'),accounting=num(replay.read(0x765720,4),0),task_hex=replay.read(e.TASK+0x44,0x20).hex(),work_hex=replay.read(e.overlay.WORK,0x2500).hex()))

def capture_command(replay,p,op,n):
 return dict(PC=num(replay.read(e.VM+28,4),0),opcode=op,bytes=n,source_pointer=p,raw_hex=replay.read(p,n).hex())

def replay_branch(name):
 # The inherited dispatch guard takes an exclusive code end. Special19 keeps
 # the architectural PC at its own instruction, four bytes before that end.
 cfg=branch(name);return dict(cfg,final_PC=cfg['final_PC']+4)

def observation_payload_code(fn,scope):
 """Change only query/command observation payloads for the current contract.

 Original execution, APIs, guards, counters, writes and event ordering are the
 frozen engine's exact AST. No machine instruction/event is removed or added.
 """
 text=textwrap.dedent(inspect.getsource(fn));original=ast.parse(text);changed=copy.deepcopy(original);counts=dict(queries=0,commands=0)
 def target(n):return n.func.value.id if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id in counts and n.func.attr=='append' else None
 for n in ast.walk(changed):
  kind=target(n)
  if kind:
   need(len(n.args)==1 and not n.keywords,'single frozen observation payload');args=('self','at','cpu') if kind=='queries' else ('self','p','op','n');function='capture_query' if kind=='queries' else 'capture_command';n.args=[ast.copy_location(ast.Call(func=ast.Name(id=function,ctx=ast.Load()),args=[ast.Name(id=a,ctx=ast.Load()) for a in args],keywords=[]),n.args[0])];counts[kind]+=1
 need(counts==dict(queries=1,commands=1),'only one query and one command observation builder adapted')
 normalized=[]
 for tree in (original,changed):
  tree=copy.deepcopy(tree)
  for n in ast.walk(tree):
   if target(n):n.args=[ast.Constant(value='ONLY_DECLARED_OBSERVATION_PAYLOAD')]
  normalized.append(ast.dump(tree,include_attributes=False))
 need(normalized[0]==normalized[1],'entire replay AST equal outside only declared observation data')
 scope.update(capture_query=capture_query,capture_command=capture_command);exec(compile(ast.fix_missing_locations(changed),__file__+':observation-payloads','exec'),scope)
 audit=dict(frozen_source_sha256=sha(text.encode('utf8')),unchanged_execution_AST_sha256=sha(normalized[0].encode('utf8')),query_payload_builders_changed=counts['queries'],command_payload_builders_changed=counts['commands'],only_declared_observation_payloads_changed=True,original_machine_events_filtered=False)
 return scope[fn.__name__].__code__,audit

def bind_replay(fn):
 routing={'terminal_last_dialogue':'terminal_script_exit','last_dialogue_cleanup':'script_exit_cleanup','terminal_followup':'terminal_script_exit','followup_cleanup':'script_exit_cleanup'}
 def constants(code):return code.replace(co_consts=tuple(constants(v) if isinstance(v,types.CodeType) else routing.get(v,v) if type(v)is str else v for v in code.co_consts))
 scope=dict(fn.__globals__,**globals());scope['Uc']=source_image_uc
 code=fn.__code__
 if fn.__name__=='execute':
  scope['need']=replay_need;scope['branch']=replay_branch;code,audit=observation_payload_code(fn,scope);scope['OBSERVER_SCHEMA_AUDIT']=audit
 return types.FunctionType(constants(code),scope,closure=fn.__closure__)

class Replay(previous_stage.Replay):
 _initialize=bind_replay(previous_stage.Replay._initialize)
 def __init__(self,row,refs=None):
  partitions=source_image_partitions(row['terminal_script_exit']['before']['memory']);self._initialize(row,{} if refs is None else refs);self.u.mem_map=self.u._original_snapshot_map;del self.u._original_snapshot_map;self.u.mem_protect(SOURCE_IMAGE_BASE,(len(e.CODE)+4095)&~4095,5)
  for address,size in SOURCE_IMAGE_WRITABLE:self.u.mem_protect(address,size,3)
  for address,size,perms in partitions:self.u.mem_protect(address,size,perms)
  self.image_layout=dict(complete_image_mapped_first=True,one_original_image_RAM_backing=True,source_RX_RW_permissions=True,snapshot_partitions_preserved=True,original_events_filtered=False)

def replay_need(ok,message):
 if ok:return
 local=sys._getframe(1).f_locals;machine=local.get('self');segment=local.get('s',{});diagnostic=dict(schema_version=1,error=message)
 if machine is not None:
  actual=machine.cpu();expected=segment.get('CPU',{});mark=local.get('mark')
  diagnostic.update(case=machine.row['input']['name'],segment_index=local.get('i'),segment={k:segment.get(k) for k in ('label','kind','entry','stop','root')},actual_CPU=actual,expected_CPU=expected,CPU_differences={k:dict(actual=actual.get(k),expected=expected.get(k)) for k in actual.keys()|expected.keys() if actual.get(k)!=expected.get(k)},actual_mark=mark() if callable(mark) else None,expected_mark=segment.get('local_after'),actual_leaf_cursor=local.get('index'),expected_leaf_cursor=segment.get('leaves'),original_segments_unchanged=True)
 path=ROOT/('analysis/terminal-script-exit-replay-diagnostic-'+str(time.time_ns())+'-20261030.json')
 with path.open('x',encoding='utf8',newline='\n') as out:json.dump(diagnostic,out,separators=(',',':'));out.write('\n')
 need(False,message+'; diagnostic='+path.relative_to(ROOT).as_posix())

Replay.execute=bind_replay(previous_stage.Replay.execute)
Replay.cleanup=bind_replay(previous_stage.Replay.cleanup)

def native(row,old=None):
 """Classify every current wire and original leaf by its actual lifetime."""
 old=parent_case(row) if old is None else old;d=row['terminal_script_exit'];gt=row['GPU_trace'];ct=row['CRT_trace'];contexts=gpu_mappings(row);oldcontexts=gpu_mappings(old);ledger=row['script_exit_resources_after_cleanup'];by_create={r['create_wire_index']:r for r in ledger};by_gen={r['generation']:r for r in ledger};legacy=previous_stage.previous
 need(helper_contract()==e.helper_contract(),'unchanged original native helper contract')
 need([(r['domain'],r['guest']) for r in row['typed_GPU_projection']]==[(r['domain'],r['guest']) for r in old['typed_GPU_projection']],'all parent GPU identities and their original order unchanged')
 next_guest=max(r['guest'] for r in row['typed_GPU_projection'] if r['domain'].startswith('overlay-last-dialogue-'))+0x100000
 need(d['GPU_projection_before']==dict(next=next_guest,ledger=row['typed_GPU_projection']) and d['GPU_projection']==row['typed_GPU_projection'] and not any(c['op']=='create' for c in d['GPU_APIs']),'complete unchanged allocation cursor/ledger and no new native texture')
 actual_identities={k:set() for k in contexts}
 def ids(t):return [t['pointer'],t['vtable']]+list(t['methods'].values())
 actual_identities['overlay'].update(ids(row['current_GPU_hello']['device']))
 for r in ledger:
  domain=resource_domain(row,r);t=gt[r['create_wire_index']]['reply']['result']['texture'];values=ids(t);bridged=previous_stage.bridged_followup_pointer(row,r)
  if bridged:actual_identities[FOLLOWUP_POINTER_DOMAIN].add(values.pop(0))
  actual_identities[domain].update(values)
  locks=[t['reply']['result']['bits'] for i,t in enumerate(gt) if r['create_wire_index']<i<r['release_wire_index'] and t['request']['op']=='lock' and t['request']['pointer']==r['native_pointer']]
  need(len(locks)==1,'one actual original surface lock per creation');actual_identities[FOLLOWUP_BITS_DOMAIN if bridged else domain].add(locks[0])
 need(all(set(contexts[k])==v for k,v in actual_identities.items()),'each typed native identity belongs to its real device/create/lock receipt')
 need(row['current_GPU_hello']['max_textures']==10 and row['current_GPU_hello']['max_creates']==32 and row['current_GPU_hello']['window_visible'] is False and row['current_GPU_hello']['pointer_bytes']==row['current_CRT_hello']['pointer_bytes']==4 and row['current_GPU_hello']['image_size']==[512,512] and row['current_CRT_hello']['GPU_created'] is False,'actual bounded headless x86 native owners')
 n=15 if row['input']['name']=='neutral_running' else 18
 need(len(by_create)==len(by_gen)==len(ledger)==len(d['resources'])==len(d['resources_before'])==n,'all inherited creation generations without additions')
 need(d['resources_before']==row['terminal_last_dialogue']['resources'] and sum(r['alive'] for r in d['resources_before'])==10,'complete current parent resource ledger')
 for before,after in zip(d['resources_before'],d['resources']):
  for k,v in before.items():
   if k not in ('alive','release_wire_index','released_phase','alive_after_forward'):need(after[k]==v,'unchanged inherited generation metadata '+k)
  if not before['alive']:need(all(after.get(k)==before.get(k) for k in ('alive','release_wire_index','released_phase')),'no revival or repeated release of retired generation')
 need(d['GPU_APIs']==[x['call'] for x in d['leaves'] if x['kind']=='GPU'] and d['calls']==[] and d['GDI_trace']==[] and not any(x['kind']=='GDI' for x in d['leaves']),'each new original GPU leaf once; no new GDI calls')
 need(row['CRT_APIs'][d['prefix']['CRT_APIs']:]==[x['call'] for x in d['leaves'] if x['kind']=='CRT'],'complete current CRT leaves including actual late cleanup')
 for label,trace in (('GPU',gt),('CRT',ct)):
  for i,t in enumerate(trace):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok'] is True,'complete ordered successful actual '+label+' wire')
 for i,t in enumerate(gt[:d['prefix']['GPU_wire']]):
  q=t['request'];ptr=t['reply']['result']['texture']['pointer'] if q['op']=='create' else q.get('pointer');matches=[r for r in ledger if r['native_pointer']==ptr and r['create_wire_index']<=i<=r['release_wire_index']]
  need(len(matches)==1,'one actual inherited lifetime at every prefix wire');r=matches[0];o=next(r0 for r0 in old['last_dialogue_resources_after_cleanup'] if r0['generation']==r['generation'])
  need(legacy.gpu_value(t,resource_context(row,r,contexts))==legacy.gpu_value(old['GPU_trace'][i],resource_context(old,o,oldcontexts)),'entire fixed parent GPU wire and guest identity in actual creation lifetime')
 live={};logical={};ci=readbacks=peak=0;calls=previous_stage.gpu_calls(row)+d['GPU_APIs'];observers={o['wire_index']:o for o in d['readback_observers']}
 need(len(observers)==len(d['readback_observers']),'unique current observer provenance')
 for i,t in enumerate(gt):
  q=t['request'];result=t['reply']['result'];op=q['op']
  if op=='close':need(i==len(gt)-1 and not live and result==row['GPU_cleanup'] and not result['texture_releases'],'normal native close after all actual original releases');continue
  if op=='readback':
   need(q['pointer'] in live,'no observer reads a retired generation');r=live[q['pointer']];raw=bytes.fromhex(r['upload_hex']);need(result['hex']==raw.hex() and result['sha256']==sha(raw) and result['pitch']==r['size'][0]*2,'every surviving surface retains every original texel')
   if i>=d['prefix']['GPU_wire']:
    need(i in observers and (observers[i]['generation'],observers[i]['record'],observers[i]['result'])==(r['generation'],r['record'],result),'actual new observer tied to exact live creation')
   readbacks+=1;continue
  need(ci<len(calls),'no unclassified original COM operation');c=calls[ci];ci+=1;generation=by_create[i]['generation'] if op=='create' else c.get('generation')
  if generation is None:
   matches=[r for r in ledger if r['native_pointer']==q['pointer'] and r['create_wire_index']<i<=r['release_wire_index']];need(len(matches)==1,'one live inherited native generation');generation=matches[0]['generation']
  need(generation in by_gen,'known original generation');context=resource_context(row,by_gen[generation],contexts)
  need(c.get('wire_index',i)==i and c['op']==op and c['native_result']==result and c['result']==legacy.gpu_value(result,context) and c['actual_API_executed'] is True,'entire original COM output bound to exact current native wire and lifetime')
  expected=dict(id=i+1,op=op)
  if op=='create':
   need(i<d['prefix']['GPU_wire'] and i in by_create,'creation belongs entirely to frozen parent');r=by_create[i];a=c['args'];p=result['texture']['pointer']
   need(r['generation']==i+1 and r['native_pointer']==p and r['texture']==c['result']['texture'] and r['record']==a[-1]-44 and r['size']==a[1:3] and p not in live and r['texture']['pointer'] not in logical,'original creation and simultaneous native/guest ownership')
   live[p]=r;logical[r['texture']['pointer']]=r;expected.update(width=a[1],height=a[2],levels=a[3],usage=a[4],format=a[5],pool=a[6]);peak=max(peak,len(live))
  else:
   need(c['args'][0] in logical,'original receiver has a live generation');r=logical[c['args'][0]];need(live.get(q['pointer']) is r,'native and guest select the same live generation');expected['pointer']=r['texture']['pointer']
   if op=='lock':expected['flags']=c['args'][-1];need(c['result']==r['lock'],'whole actual original lock input')
   elif op=='unlock':expected['hex']=r['upload_hex']
   elif op=='release':need(r['release_wire_index']==i and c['value']==result['count']==0,'exact original last release');del live[q['pointer']];del logical[r['texture']['pointer']]
   else:need(op=='describe','only original finite COM operations')
  need(legacy.gpu_value(q,context)==expected,'entire actual translated original COM request')
  if i>=d['prefix']['GPU_wire']:
   need(op in ('describe','release') and (c['generation'],c['record'],c['resource_kind'],c['resource_label'],c['phase'])==(r['generation'],r['record'],r['kind'],r['label'],'forward' if i<d['forward_wire_end'] else 'cleanup'),'actual destruction ABI and exact generation/record/phase')
 need(ci==len(calls) and peak==10,'every actual COM call and original capacity peak classified')
 need(sorted(observers)==[i for i,t in enumerate(gt) if i>=d['prefix']['GPU_wire'] and t['request']['op']=='readback'] and d['readbacks']==d['readback_observers'],'all new readbacks are the final surviving set')
 for r,f in zip(ledger,d['resources']):
  need(r['alive'] is False and r['release_wire_index'] is not None,'every actual generation eventually originally released');want=copy.deepcopy(r);want['alive']=r['release_wire_index']>=d['forward_wire_end']
  if want['alive']:want['release_wire_index']=None;want.pop('released_phase',None)
  need(f==want and f['alive']==r['alive_after_forward'],'complete forward resource ledger frozen before actual supplemental cleanup')
 need({o['generation'] for o in d['readbacks']}=={r['generation'] for r in d['resources'] if r['alive']} and all(o['label']=='final' for o in d['readbacks']),'every actual survivor observed, with no preselected surviving count')
 covered=[]
 for a in row['CRT_APIs']:
  need(0<=a['wire_start']<a['wire_end']<len(ct) and CRT_IMPORTS[a['import_slot']]==(a['name'],a['pop']) and e.CODE[a['import_slot']-0x400000:a['import_slot']-0x400000+4]==struct.pack('<I',a['target']),'original CRT IAT and exact actual wire interval');covered.extend(range(a['wire_start'],a['wire_end']));r=ct[a['wire_end']-1]['reply']['result'];nm=a['name'];outputs=[]
  if nm in ('InitializeCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
   raw=r['hex'] if nm=='InitializeCriticalSection' else r['critical_hex'];b=bytearray.fromhex(raw);need(len(b)==24,'whole current critical section')
   for off in (0,12,16):
    if num(b,off) not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off+(a['args'][0]-0x80A480)*0x100)
   outputs=[dict(pointer=a['args'][0],hex=b.hex(),native_hex=raw)];value=0
  elif nm=='HeapAlloc':outputs=[dict(pointer=a['value'],hex=r['hex'])];value=a['value'];need(len(bytes.fromhex(r['hex']))==a['args'][2] and a['new_mappings']==[dict(pointer=value,bytes=(a['args'][2]+4095)&~4095)],'whole actual heap buffer including uninitialized bytes')
  elif nm=='ReadFile':outputs=[dict(pointer=a['memory_outputs'][0]['pointer'],hex=r['after_hex']),dict(pointer=a['args'][3],hex=struct.pack('<I',r['read']).hex())];value=r['value']
  elif nm in ('GetVersionExA','GetCurrentDirectoryA'):outputs=[dict(pointer=a['args'][0 if nm=='GetVersionExA' else 1],hex=r['hex'])];value=r['value']
  elif nm=='CreateFileA':value=0x62001000;need(a['native_handle']==r['handle'],'current actual read-only file owner')
  elif nm=='HeapCreate':value=0x61001000
  elif nm=='DeleteCriticalSection':value=0
  else:value=r['value']
  need(a['memory_outputs']==outputs and a['value']==value,'every actual complete CRT output retained')
 constructed=[row['terminal_portrait']['constructed']]+[r['constructed'] for stage in (followup_stage,next_stage) for r in stage.new_resources(row) if r['kind']=='portrait']
 for b in constructed:
  for x in b['native_allocation_readbacks']:
   i=x['wire_index'];covered.extend((i-1,i));a=ct[i-1];z=ct[i];need(a['request']['op']=='sync' and a['request']['hex']==a['reply']['result']['hex']==x['result']['hex'] and z['request']==dict(id=i+1,op='readback',pointer=x['result']['pointer']) and z['reply']['result']==x['result'] and len(bytes.fromhex(x['result']['hex']))==x['bytes'],'whole actual original file/vector mirror and current observer')
 need(sorted(covered)==list(range(len(ct)-1)),'each current CRT operation classified once')
 need(legacy.crt_semantics(row)[:d['prefix']['CRT_wire']]==legacy.crt_semantics(old)[:d['prefix']['CRT_wire']],'complete fixed parent CRT control and initialized data; raw inputs independently executed')
 GDI=previous_stage.gdi_native(row,previous_stage.parent_case(row));need(d['prefix']['GDI_trace']==GDI['calls'] and d['GDI_handle_projection']==row['terminal_last_dialogue']['GDI_handle_projection'],'whole current parent GDI lifetimes with no new call or handle')
 task_leaves=[x['call'] for x in d['leaves'] if x['kind']=='TASK'];actual=row['task_APIs'][d['prefix']['task_APIs']:]
 need(len(task_leaves)==len(actual) and all(all(c[k]==value for k,value in a.items()) for c,a in zip(task_leaves,actual)),'one actual current task API leaf per platform receipt')
 need(row['CRT_exit']==row['GPU_exit']==0 and ct[-1]['request']==dict(id=len(ct),op='close') and ct[-1]['reply']['result']==row['CRT_cleanup'] and row['CRT_cleanup']['all_owned_resources_released'] and not row['CRT_cleanup']['forced_cleanup'],'all current native owners close normally without fallback')
 return dict(current_COM_calls=ci,texture_generations=len(ledger),peak_live_textures=peak,forward_live_textures=sum(r['alive'] for r in d['resources']),whole_readbacks=readbacks,current_CRT_operations=len(ct)-1,current_GDI_calls=GDI['calls'],GDI_lifetime_audit=GDI,no_new_texture_or_GDI_creation=True,all_native_ownership_and_protocol_verified=True,raw_heap_and_surface_hex_never_address_normalized=True)

EVENT_ABI={0x4C2670:(3,12),0x4C4DC0:(3,12),0x4C4EB0:(3,12),0x497C50:(0,0),0x403730:(0,0),0x4CADE0:(0,0),0x4C6DA0:(0,0),0x4C6330:(3,12),0x4C5BC0:(3,12),0x4C5590:(3,12),0x42D9F0:(3,12),0x4CE090:(1,4),0x4CE800:(0,0),0x4CE8F0:(0,0),0x4563D0:(0,0),0x497980:(1,0),0x4CC8D0:(1,4),0x4CC910:(2,8),0x4CC540:(2,8),0x4C9590:(0,0),0x4CB120:(2,8),0x4C7130:(0,0)}

def execute_with_events(replay):
 """Observe the unchanged replay engine; neither hook changes machine state."""
 need(e.EVENTS==EVENT_ABI,'exact independently identified observed original ABI')
 observed=[];stack=[]
 def state():return dict(VM_PC=num(replay.read(e.VM+28,4),0),VM_wait=num(replay.read(e.VM+32,2),0,'H'),VM_active=num(replay.read(e.VM+4,1),0,'B'),accounting=num(replay.read(0x765720,4),0),task_hex=replay.read(e.TASK+0x44,0x20).hex(),work_hex=replay.read(e.overlay.WORK,0x2500).hex())
 def observe(u,at,size,_):
  sp=u.reg_read(x86.UC_X86_REG_ESP)
  while stack and (at,sp)==(stack[-1]['caller'],stack[-1]['return_ESP']):
   cpu=replay.cpu();r=stack.pop();r.update(after_CPU=cpu,after=state(),result=cpu['EAX'])
  if at in EVENT_ABI:
   cpu=replay.cpu();n,pop=EVENT_ABI[at];r=dict(entry=at,caller=num(replay.read(sp,4),0),receiver=cpu['ECX'],args=[num(replay.read(sp+4+j*4,4),0) for j in range(n)],return_ESP=sp+4+pop,before_CPU=cpu,before=state());observed.append(r);stack.append(r)
 hook=replay.u.hook_add(UC_HOOK_CODE,observe)
 try:counts=replay.execute()
 finally:replay.u.hook_del(hook)
 need(not stack and observed==replay.row['terminal_script_exit']['events'],'every original nested call, full57 CPU/stack ABI and complete event bytes independently reexecuted')
 return dict(counts,original_call_events=len(observed),all_original_call_event_bytes_CPU_and_ABI_verified=True)

def work_fields(state):
 w=bytes.fromhex(state['work']);need(len(w)==0x24C0,'complete original work object')
 return dict(value=num(w,0x2490,'i'),step=num(w,0x2494,'i'),direction=w[0x2498],active=w[0x2499],status=w[0x249A],remaining=num(w,0x249C,'i'))

def work_after(before,start=False):
 w=bytearray.fromhex(before['work']);gate=bytes.fromhex(before['VM'])[0x92E0]
 if start:
  struct.pack_into('<ii',w,0x2490,38912,648);w[0x2498:0x249B]=bytes((0,1,1));struct.pack_into('<i',w,0x249C,60);gate=1
 if w[0x2499]:
  need(w[0x2498]==0 and num(w,0x2494,'i')==648 and 1<=num(w,0x249C,'i')<=60,'only original terminal decreasing60 fade')
  struct.pack_into('<i',w,0x2490,max(0,num(w,0x2490,'i')-648));left=num(w,0x249C,'i')-1;struct.pack_into('<i',w,0x249C,left)
  if left==0:w[0x2499]=0;w[0x249A]=0;gate=0
  else:w[0x249A]=1
 return w.hex(),gate

def protocol(row):
 d=row['terminal_script_exit'];cfg=branch(row['input']['name']);bindings=d['bindings'];frames=d['frames'];stream=previous.confirmation.captured_contract()['streams'][cfg['scene_capture']]
 need(len(bindings)==3 and [b['capture'] for b in bindings]==stream['captures'] and [b['segment_index'] for b in bindings]==[0,9,14],'one distinct exact captured idle/press/release cycle')
 for b in bindings:
  raw=bytes.fromhex(b['capture']['raw_device_hex']);before=bytes.fromhex(b['before_hex']);bound=bytearray(before);bound[12:268]=raw;bp=e.STACK+0xF800
  need(len(raw)==256 and len(before)==0xA00 and b['cycle']=='terminal_script_exit_confirmation' and b['bound_hex']==bound.hex() and b['after_hex']==predict_keyboard(bytes(bound)).hex(),'entire original A00 keyboard result from only declared raw device output')
  need(b['only_device_output_written']==dict(pointer=e.KEYBOARD+12,bytes=256) and b['fragment']==dict(va=0x4113D5,bp=bp,sp=bp-0x70,receiver_slot=bp-4,receiver=e.KEYBOARD,stop=0x4116A4),'only accepted original keyboard fragment and raw output')
 need([bytes.fromhex(b['after_hex'])[0x4B9] for b in bindings]==[0,128,0] and len(frames)>15 and [f['phase'] for f in frames[:3]]==['held_parent_confirmation','held_parent_confirmation','captured_press'] and all(f['phase']=='remaining_original_script' for f in frames[3:]),'two no-input holds, actual captured press, then continuous original tail')
 need(vw(d['before']['state'])==(cfg['first_PC'],1) and vw(d['confirmed']['state'])==(cfg['first_PC'],0),'original confirmation alone releases parent wait')
 fetched=[];timer=[];fade=[]
 for i,f in enumerate(frames):
  need(f['index']==i and f['complete'] is True and f['capture']['state']==f['after'] and f['capture']['queue']==f['queue_after'],'every complete original frame and whole current queue captured')
  prior=frames[i-1]['capture'] if i else d['before'];start=frames[i-1]['segments'][1] if i else 0;stop=f['segments'][0];state=prior['state'];queue=prior['queue'];cpu=prior['CPU'];trace=prior['trace'];local=prior['local_trace']
  for b in (b for b in bindings if start<=b['segment_index']<stop):
   offset=e.KEYBOARD-e.MAIN;owner=bytearray.fromhex(state['owner']);need(owner[offset:offset+0xA00].hex()==b['before_hex'] and b['before_CPU']==cpu and b['trace_before']==trace and b['local_before']==local,'keyboard bridge begins at full exact prior owner/CPU/trace')
   owner[offset:offset+0xA00]=bytes.fromhex(b['after_hex']);need(b['after']['state']==dict(state,owner=owner.hex()) and b['after']['queue']==queue,'only original predicted keyboard object changed in full owner');state=b['after']['state'];queue=b['after']['queue'];cpu=b['after']['CPU'];trace=b['after']['trace'];local=b['after']['local_trace']
  need(f['before']==state and f['queue_before']==queue,'whole state and queue remain continuous through raw input bridges')
  a=bytes.fromhex(f['before']['VM']);z=bytes.fromhex(f['after']['VM']);pc=num(a,28);wait=num(a,32,'H');op=None
  need(a[4]==1 and (z[4]==0)==(i==len(frames)-1),'slot remains active until only the final original19 task')
  if i<2:need((pc,wait)==vw(f['after'])==(cfg['first_PC'],1),'two complete no-input parent holds')
  elif i==2:need(vw(f['after'])==(cfg['first_PC'],0),'captured press only clears confirmation')
  elif wait==0:
   cmd=cfg['commands'][len(fetched)];need(pc==cmd['PC'],'original next command order without host PC changes');op=cmd['opcode'];fetched.append(cmd)
   if op==19:need(num(z,28)==pc and z[4]==0,'special19 stops slot without advancing PC')
   else:need(num(z,28)==pc+cmd['bytes'] and num(z,32,'H')==({12:1,24:1,118:4}.get(op,0)),'one complete original dispatch and actual wait kind')
   if op==12:need(num(z,0x26,'H')==12 and (num(z,0x28,'H'),num(z,0x2A,'H'))==(0,60),'original60 timer initialized without host countdown')
  else:
   need(num(z,28)==pc and num(z,32,'H') in (0,wait),'a wait poll never dispatches another command')
   if wait==1 and num(a,0x22,'H')==12:
    count=num(a,0x28,'H');need(num(a,0x2A,'H')==60 and num(z,0x28,'H')==(count+1)&0xFFFF and num(z,32,'H')==(0 if count>59 else 1),'original timer compares the old count strictly after increment');timer.append(count)
  w,gate=work_after(f['before'],start=op==118);need(f['after']['work']==w and z[0x92E0]==gate,'entire work object and VM gate match original integer fade update')
  if op==118 or work_fields(f['before'])['active']:fade.append(work_fields(f['after']))
  need(f['after']['remaining']==d['before']['state']['remaining'] and f['after']['elapsed']==d['before']['state']['elapsed'],'world clock stays paused through original script stop')
 need(fetched==cfg['commands'] and timer==list(range(61)),'all twelve commands and strict61 timer polls executed once')
 need(len(fade)==60 and fade==[dict(value=38912-648*i,step=648,direction=0,active=int(i<60),status=int(i<60),remaining=60-i) for i in range(1,61)],'all60 original fade updates, preserving final32 rather than normalizing')
 final=d['final'];vm=bytes.fromhex(final['state']['VM']);task=bytes.fromhex(final['state']['task']);old_task=bytes.fromhex(d['before']['state']['task']);phase=3 if num(old_task,0x50)!=0 else 4
 need(final['state']==frames[-1]['after'] and final['CPU']==frames[-1]['capture']['CPU'] and final['trace']==frames[-1]['capture']['trace'] and final['local_trace']==frames[-1]['capture']['local_trace'],'frozen final equals last full original task')
 need(num(vm,28)==cfg['final_PC'] and vm[4]==0 and num(vm,32,'H')==0 and task[0x44]==phase and task[0x59]==2 and task[0x171:0x173]==old_task[0x171:0x173],'original VM stop hands off to exact next task phase without task-exit execution')
 need(final['CPU']['EIP']==e.RETURN and final['CPU']['ESP']==e.STACK+0xF004,'full task naturally returns at real root ABI')
 for layer in range(10):need(num(read(final['memory'],text_object(layer)+22,2),0,'H')==0,'all original text counts cleared')
 need(d['accounting']==num(read(final['memory'],0x765720,4),0)==row['accounting_baseline']['texture_bytes']+sum(r['size'][0]*r['size'][1]*2 for r in d['resources'] if r['alive']),'all actual surviving native textures accounted')
 need(d['VM_script_stopped'] is True and d['terminal_task_exit_executed'] is False and d['rewards_or_school_executed'] is False,'VM stop and pending later task exit remain distinct')
 return dict(VM_PC=cfg['final_PC'],VM_wait=0,VM_active=0,task_phase=phase,task_status=2,complete_frames=len(frames),commands=12,timer_polls=61,fade_updates=60,fade_final_value=32,successor_task_stage_executed=False)

def final_summary(row):
 d=row['terminal_script_exit'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs'])
 want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'all final terminal summary pages equal independently verified full memory')
 return True

def verify_case(row,old=None):
 prefix_trace(row);provenance=source(row);timed=protocol(row);platform=native(row,old);replay=Replay(row);counts=execute_with_events(replay);p=prefix(row,old);d=row['terminal_script_exit'];equal(row['final'],d['final']['memory'],'entire final mapped memory')
 need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'complete final57 CPU and unchanged source image/IAT')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'actual full cumulative source counters and digests')
 summary=final_summary(row);cleanup=replay.cleanup();facts=dict(full_cumulative=d['final']['trace'],mapped_regions=len(d['final']['memory']),CPU_registers=len(d['final']['CPU']),complete_tasks=(578 if row['input']['name']=='neutral_running' else 605)+len(d['frames']),pending_tasks=0,live_textures=sum(r['alive'] for r in d['resources']),new_textures=[],VM_script_stopped=True,task_phase=timed['task_phase'])
 return dict(name=row['input']['name'],prefix=p,source=provenance,helper=helper_contract(),native=platform,timing=timed,added=counts,cleanup=cleanup,forward_summary=facts,independent_source_image_layout=replay.image_layout,independent_replay_observer_adaptation=Replay.execute.__globals__['OBSERVER_SCHEMA_AUDIT'],current_terminal_summary_pages_equal_verified_final_memory=summary,independent_whole_memory_CPU_and_new_original_trace=True,all_original_call_events_independently_verified=True,no_historical_cleanup_CPU_or_SHA_projection=True,task_exit_complete=False,rewards_complete=False)

def fresh_case(case,crt_helper,gpu_helper,ticks):
 need(ticks==accepted_clock_inputs()[case['name']],'fresh full original instance uses the exact accepted parent clock input')
 return e.run_case(case,crt_helper,gpu_helper,ticks)

def verify(path):
 accepted_clock_inputs();data=load_report(path)
 need(data['schema_version']==1 and data['source_contract']==e.source_contract() and [r['input'] for r in data['cases']]==e.overlay.parent.corpus(),'exact source contract and both selected original terminal cases')
 need(Path(data['helper_build']['GPU']['source']).as_posix()=='tools/terminal_followup_d3d8_platform.cs' and data['helper_build']['GPU']['source_sha256']==helper_contract()['current']['sha256'] and data['helper_build']['GPU']['machine']==0x14C,'actual unchanged original capacity10 x86 helper build')
 helpers=e.helpers('terminal-script-exit-proof');rows=[]
 for row in data['cases']:
  old=parent_case(row);proof=verify_case(row,old);ticks=[a['result'] for a in old['APIs'] if a['name']=='GetTickCount'];other=None
  try:
   other=fresh_case(row['input'],helpers[0],helpers[1],ticks);verify_case(other,old)
   for key in ('initial','final'):equal(row[key],other[key],'fresh entire '+key+' memory')
   for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'fresh original cumulative digests and actual cleanup '+key)
   for key in ('terminal_script_exit','script_exit_cleanup','script_exit_resources_after_cleanup'):need(guest(row[key])==guest(other[key]),'fresh whole new stage bytes/CPU/local trace/frames/lifetimes '+key)
  except Exception as error:
   if other is not None:
    diagnostic='analysis/terminal-script-exit-diagnostic-fresh-'+row['input']['name']+'-20261030-'+str(time.time_ns())+'.json.gz';e.save_source(diagnostic,dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),error_type=type(error).__name__,error=str(error),fresh_original_case=other));print('full failed fresh instance preserved locally',diagnostic,flush=True)
   raise
  proof['current_native_resources_recreated']=True;proof['complete_cumulative_digests_reproduced_by_new_full_original_instance']=True;rows.append(proof);print('independent script exit',row['input']['name'],'original VM stop and all current resources verified',flush=True);del other;gc.collect()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,VM_scripts_stopped=True,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable script-exit proof');e.terminal.save(a.out,verify(ROOT/a.report))
