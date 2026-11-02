"""Independent original exit-prefix execution and complete COMMON ownership."""
import argparse,ast,copy,gc,gzip,hashlib,inspect,json,struct,textwrap,time,types
from functools import lru_cache
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_battle_stage_handoff_verification as parent
from tools import terminal_battle_exit_emulation as e
from tools import terminal_battle_exit_budget as budget
from tools import terminal_battle_exit_contract as contract
from tools.terminal_battle_exit_resume import normalized_managed_image
from tools.terminal_battle_exit_pixels import indexed_bmp_image,original_palette_contract,bitmap_loader_palette
from tools.school_tactical_resource_catalog import texture_inputs
ROOT=e.ROOT;need=e.need;sha=e.sha;read=parent.read;equal=parent.equal;num=parent.num
IMPLEMENTATIONS=('tools/terminal_battle_exit_emulation.py','tools/terminal_battle_exit_verification.py','tools/terminal_battle_exit_contract.py','tools/terminal_battle_exit_pixels.py','tools/terminal_battle_exit_preservation.py','tools/terminal_battle_exit_process.py','tools/terminal_battle_exit_data_guard.py','tools/terminal_battle_exit_budget.py','tools/terminal_battle_exit_resume.py','tools/terminal_battle_exit_crt_platform.cs','tools/terminal_battle_exit_d3d8_platform.cs','tools/tests/test_terminal_battle_exit_source.py','tools/tests/test_terminal_battle_exit_contract.py','tools/tests/test_terminal_battle_exit.py','tools/tests/test_terminal_battle_exit_budget.py')

@lru_cache(maxsize=1)
def catalog():
 raw=(ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/COMMON.BIN').read_bytes()
 need(len(raw)==1793036 and sha(raw)=='110e230ffa1f3457ab7f5d7d4a31334e933c5edc90962855e921d86b84700d85','complete original COMMON source identity')
 rows=texture_inputs(raw)
 need(len(rows)==580 and sum(r['kind']=='indexed_bmp' for r in rows)==461 and sum(r['kind']=='no_texture' for r in rows)==119,'complete independent COMMON record classification')
 return raw,rows

def state(replay):
 def g(p,f='I'):return num(replay.read(p,struct.calcsize('<'+f)),0,f)
 return dict(task_hex=replay.read(e.TASK,0x190).hex(),VM_PC=g(e.VM+28),VM_wait=g(e.VM+32,'H'),VM_active=g(e.VM+4,'B'),selector=g(e.TASK+0x38),result_type=g(e.TASK+0x174),packet_owner=g(e.TASK+0xB4),time_packet_hex=replay.read(e.CTRL+0xDE730,0x80).hex(),group90=replay.read(e.MAIN+0x844+90*8,8).hex())

def capture(replay,cap,label,full=False):
 need(replay.cpu()==cap['CPU'],label+' all57 CPU')
 need(state(replay)==cap['state'] and parent.staged_queue(replay)==cap['queue'],label+' whole task state and queue')
 if full:parent.stage_state_memory_equal(replay,cap['memory'],label)
 else:need(parent.staged_regions(replay)==sorted(cap['memory'],key=lambda r:r['pointer']),label+' every complete mapped region SHA')

def protocol(row):
 d=row['terminal_battle_exit_prefix'];f=d['freeze'];cap=d['final'];cpu=cap['CPU'];memory=cap['memory']
 need(d['before']['trace']==row['terminal_battle_stage_handoff']['final']['trace'],'new prefix starts at the preserved complete parent boundary')
 need(all(d['before'][k]==row['terminal_battle_stage_handoff']['final'][k] for k in ('memory','CPU','queue')),'parent final full bytes CPU and queue are retained')
 need(d['before']['local_trace']==parent.mark_zero(),'new local counter starts empty')
 expected={'neutral_running':(0x40B2EC,'unavailable_unit_graphics'),'timeout_before_combat':(0x46D3F4,'zero_MP_HUD_input')}
 need((f['entry'],f['kind'])==expected[row['input']['name']] and f['first_instruction_executed'] is False,'declared case-specific original frontend instruction remains unexecuted')
 need(cpu['EIP']==f['entry'] and cpu['EBP']==f['frame_EBP'],'pending original frontend CPU/frame')
 args=None
 if f['kind']=='unavailable_unit_graphics':
  need((f['call_site'],f['call_target'],f['call_instruction_executed'],f['return_address'],f['receiver'])==(0x40B2EC,0x407870,False,0x40B2F1,e.CTRL+0xDE4B0) and cpu['ECX']==f['receiver'] and f['unit_graphics_lookup_reached'] is True,'unexecuted original unit-image query CALL')
  args=[num(read(memory,cpu['ESP']+i*4,4),0) for i in range(2)]
  need(args==f['args'] and args[0]==0 and 0<=args[1]<=65535,'original pushed resource group and frame index')
  need(num(read(memory,f['receiver']+0x4C,4),0)==f['resource_owner']==e.MAIN,'original constructed packet bound to current owner')
  slot=e.MAIN+0x844+args[0]*8
  need(f['resource_slot']==slot and f['resource_slot_hex']==read(memory,slot,8).hex()==bytes(8).hex(),'genuine uninitialized unit resource bank')
 else:
  need(not any(k in f for k in ('call_site','call_target','call_instruction_executed','args','resource_slot')),'MP input frontier must not be mislabeled as unit query CALL')
  bp=cpu['EBP'];unit=num(read(memory,bp+8,4),0);record=num(read(memory,unit+0x258,4),0)
  need(unit==f['unit']==e.terminal.TARGET and record==f['stats_record']==e.terminal.RECORD+0x100,'actual original HUD target and owned record')
  need(read(memory,record,0xB0).hex()==f['stats_record_hex'],'complete actual zero-MP input record')
  need(f['maximum_MP_pointer']==record+0x1A and f['maximum_MP']==num(read(memory,record+0x1A,2),0,'h')==0 and f['current_MP']==num(read(memory,record+0x1C,2),0,'h')==0,'existing maximum/current MP words are genuinely zero')
  need(f['numerator']==cpu['EAX']==cpu['EDX']==f['denominator']==cpu['ECX']==0 and f['idiv_instruction_executed'] is False,'actual zero denominator before original IDIV, not executed or replaced')
  need(f['frame_return_address']==num(read(memory,bp+4,4),0)==0x46CF71 and f['receiver']==num(read(memory,bp-4,4),0)==e.CTRL,'natural original HUD call frame and receiver')
  need(f['HUD_args']==[num(read(memory,bp+8+4*j,4),0) for j in range(4)] and cpu['ESP']==bp-0x5C and f['unit_graphics_lookup_reached'] is False,'all original HUD arguments/prologue stack, unit query not yet reached')
 outer_bp=e.STACK+0xF000-4
 need(f['outer_frame_EBP']==outer_bp and f['local_result']==num(read(memory,outer_bp-8,4),0)==1,'original scene-loop saved stage result remains unconsumed')
 need(f['root_return_address']==e.RETURN==num(read(memory,outer_bp+4,4),0),'explicit root return remains on original outer prologue frame')
 need(f['original_wait_reached'] is False,'no cooperative wait or result consumer has been reached')
 need((f['stack_pointer'],f['stack_bytes'],f['stack_hex'])==(e.STACK,0x20000,read(memory,e.STACK,0x20000).hex()),'complete128KiB original suspended stack')
 for k in ('terminal_battle_exit_executed','outer_result_consumed','rewards_or_school_executed','original_outer_thread_restored','terminal_presentation_complete'):need(d[k] is False,'honest unresolved boundary '+k)
 segs=d['segments'];roots=[s for s in segs if s['root']]
 expected=[('common_read',0x42AE20),('common_register',0x416790),('common_file_free',0x428AD0),('original_scene_packet_constructor',0x4075E0),('original_scene_packet_owner_binding',0x4077C0)]
 expected += [('original_controller_packet_constructor_'+hex(off),0x4075E0) for off in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
 expected += [('original_controller_packet_owner_'+hex(off),0x4077C0) for off in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
 expected += [('heads',0x40DB90),('arena',0x40DC80),('input',0x425DE0),('original_scene_loop',0x4539B0)]
 need([(s['label'],s['entry']) for s in roots]==expected,'all declared initialization and frame roots in original-derived order')
 file=d['common_file']['pointer'];inputs=[(0,[0x59A438],True),(e.MAIN,[file,90],False),(0,[file],True),(e.TASK+0x68,[],False),(e.TASK+0x68,[e.MAIN],False)]
 inputs += [(e.CTRL+off,[],False) for off in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
 inputs += [(e.CTRL+off,[e.MAIN],False) for off in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
 inputs += [(e.MANAGER,[],False),(e.MANAGER,[],False),(e.INPUT,[],False),(e.TASK,[],False)]
 need([(s['root']['receiver'],s['root']['args'],s['root'].get('cdecl',False)) for s in roots]==inputs,'all21 original-derived root receivers, arguments and cdecl ownership')
 need(segs[-1]['stop']==f['entry'] and segs[-1]['root']['receiver']==e.TASK and segs[-1]['root']['args']==[],'one explicit scene-loop root suspends naturally')
 need(all(s['stop']==e.RETURN for s in segs[:-1]),'every preceding original root naturally returns')
 for a,b in zip(segs,segs[1:]):need(a['CPU']==b['before_CPU'] and a['local_after']==b['local_before'] and a['trace_after']==b['trace_before'],'continuous original segments and full CPU')
 need(segs[0]['before_CPU']==d['before']['CPU'] and segs[-1]['CPU']==cpu and segs[-1]['local_after']==cap['local_trace'],'entire new forward spans the declared original boundaries')
 need(cap['trace']['instructions']==d['before']['trace']['instructions']+cap['local_trace']['instructions'] and cap['trace']['writes']==d['before']['trace']['writes']+cap['local_trace']['writes'],'all new original instruction/write events counted')
 accounted=contract.parent_task_accounting(row);texts=contract.strict_parent_text(row)
 new_tasks=[v for v in d['events'] if v['entry']==0x454CF0 and 'after_CPU' in v]
 need(len(new_tasks)==1 and new_tasks[0]['phase']=='prefix','one more complete task nested in the natural scene loop')
 if 'complete_tasks' in d:need(d['complete_tasks']==accounted['complete_tasks']+len(new_tasks),'source complete task count equals observed natural returns')
 return dict(roots=len(roots),frontend_frontier=dict(kind=f['kind'],entry=f['entry']),first_resource_CALL=0x40B2EC if args is not None else None,first_unavailable_resource=args,original_wait_reached=False,original_wait_body_executed=False,outer_result_consumed=False,parent_task_accounting=accounted,strict_text=texts,complete_tasks=accounted['complete_tasks']+len(new_tasks),pending_scene_loops=1)

def task_observations(row):
 d=row['terminal_battle_exit_prefix'];expected=contract.parent_task_accounting(row)['complete_tasks'];obs=d['complete_task_observations']
 need(d['parent_complete_tasks']==expected and len(obs)==d['complete_tasks']==expected+1,'every complete task across the actual full owner lifetime')
 need(all(o['entry']==0x454CF0 and o['return_PC']==0x454EC1 for o in obs),'only original complete entry and actual RET instruction observations')
 need(all(o['phase']=='parent' for o in obs[:-1]) and obs[-1]['phase']=='prefix' and obs[-1]['caller']==0x4539F1,'one added task naturally returns to original outer caller')
 return dict(complete_parent=expected,complete_current=len(obs),pending=0,observed_original_RET=0x454EC1)

def projection(row):
 d=row['terminal_battle_exit_prefix'];before=d['common_projection_before'];after=d['common_projection_after'];ledger=after['ledger']
 need(after['next']==before['next'] and ledger[:len(before['ledger'])]==before['ledger'],'all parent logical identities and allocation cursor unchanged')
 need(ledger==row['typed_GPU_projection'],'full current projection ledger is retained')
 out={};old_guests={v['guest'] for v in before['ledger']};new=[]
 for r in d['common_resources']:
  i=r['source']['index'];domain='overlay-battle-exit-common-'+str(i);need(r['projection_domain']==domain,'one logical identity domain per original resource lifetime')
  create=row['GPU_trace'][r['create_wire_index']]['reply']['result']['texture'];lock=next(x['call'] for x in d['leaves'] if x['kind']=='GPU' and x['call']['index']==i and x['call']['op']=='lock')['native_result']
  raw=[create['pointer'],create['vtable'],*create['methods'].values(),lock['bits']];unique=list(dict.fromkeys(raw));need(len(unique)==len(raw),'distinct current texture, interface methods and locked storage')
  base=0x20000000+i*0x80000;expected={p:base+((j+1)*4096 if j<len(raw)-1 else 0x20000) for j,p in enumerate(raw)}
  rows=[x for x in ledger[len(before['ledger']):] if x['domain']==domain]
  need([(x['native'],x['guest']) for x in rows]==list(expected.items()),'independently derived deterministic per-record projection '+str(i))
  need(not old_guests.intersection(expected.values()),'no current new identity aliases a parent identity')
  maximum=len(bytes.fromhex(r['lock']['hex']));need(maximum<=0x40000,'whole current surface fits its independently bounded resource slot')
  intervals=[(base+4096,base+0x20000),(base+0x20000,base+0x20000+maximum)]
  for lo,hi in intervals:need(all(not(lo<p['pointer']+p['bytes'] and p['pointer']<hi) for p in d['before']['memory']),'new projection pool disjoint from every original mapped region')
  out[domain]=expected;new.extend(rows)
 need(len(new)==len(ledger)-len(before['ledger']) and len({x['guest'] for x in new})==len(new),'every added identity classified once and no cross-lifetime alias')
 return out

def map_native(value,context):
 if isinstance(value,dict):return {k:map_native(v,context) for k,v in value.items()}
 if isinstance(value,list):return [map_native(v,context) for v in value]
 return context.get(value,value) if type(value)is int else value

def common_native(row):
 d=row['terminal_battle_exit_prefix'];raw,rows=catalog();contexts=projection(row)
 need(d['common_file']['bytes']==len(raw) and d['common_file']['sha256']==sha(raw) and d['common_file']['hex']==raw.hex(),'actual complete read-only COMMON file bytes')
 need([r['source']['index'] for r in d['common_resources_after_cleanup']]==[r['source']['index'] for r in d['common_resources']],'all actual COMMON cleanup generations accounted for exactly once')
 need(len(d['common_entries'])==580 and len(d['common_resources'])==461 and d['common_record_count']==580,'all original records and texture generations')
 base=d['common_record_base'];memory=d['dependencies']['memory'];need(read(memory,e.MAIN+0x844+90*8,8)==struct.pack('<II',base,580),'original group90 full pointer/count publication')
 need(read(memory,base,580*84).hex()==d['common_records_forward_hex'],'all580 original complete record bytes')
 by_index={r['source']['index']:r for r in d['common_resources']};need(set(by_index)=={r['index'] for r in rows if r['kind']=='indexed_bmp'},'one actual resource for every BM input and no marker texture')
 for expected,r in zip(rows,d['common_entries']):
  s=r['source'];i=expected['index'];need(s['index']==i and s['offset']==expected['offset'] and s['bytes']==expected['bytes'] and s['sha256']==expected['sha256'] and s['marker']==(expected['kind']=='no_texture'),'independent full source record identity '+str(i))
  record=base+i*84;need(r['record']==record and read(memory,record,84).hex()==r['record_forward_hex'],'complete original record placement '+str(i))
  if expected['kind']=='no_texture':need(num(read(memory,record+44,4),0)==0,'original no-texture marker has no COM object');continue
  res=by_index[i];w,h=expected['width'],expected['height'];tw,th=1<<(w-1).bit_length(),1<<(h-1).bit_length()
  need(res['record']==record and res['size']==[tw,th] and list(struct.unpack('<4h',read(memory,record+0x38,8)))==[w,h,tw,th],'original bitmap and texture geometry '+str(i))
  conv=res['conversion'];need(conv['entry']==0x404150 and conv['receiver']==record and conv['args'][0]==d['common_file']['pointer']+expected['offset'],'original complete bitmap conversion input')
  need(conv['args'][3]==0,'original default file palette rather than a host replacement')
  loader=res['bitmap_loader'];need(loader['entry']==0x4048D0 and loader['receiver']==record and len(loader['args'])==7,'original complete BMP loader ABI')
  prepared=bitmap_loader_palette(raw,expected['offset'],loader['args'][4],loader['args'][6])
  lock=res['lock'];reference=indexed_bmp_image(prepared,expected['offset'],bytes.fromhex(lock['hex']),lock['pitch'],tw,th,conv['args'][1])
  need(res['upload_hex']==reference.hex()==res['readback']['hex'] and sha(reference)==res['expected_sha256']==res['readback']['sha256'] and res['readback']['pitch']==lock['pitch'],'entire independent palette conversion and actual native full-pitch readback '+str(i))
  after=next(v for v in d['common_resources_after_cleanup'] if v['source']['index']==i)
  need(res['alive'] is True and after['alive'] is False and after['release_wire_index']>res['create_wire_index'],'forward generation retained then naturally released by supplemental original cleanup')
  need(all(after[k]==v for k,v in res.items() if k not in ('alive','release_wire_index')),'unchanged resource identity and bytes through actual cleanup')
 leaves=[x['call'] for x in d['leaves']+d['cleanup']['leaves'] if x['kind']=='GPU'];indices=[]
 for c in leaves:
  i=c['wire_index'];indices.append(i);r=by_index[c['index']];context=contexts[r['projection_domain']];wire=row['GPU_trace'][i];q=wire['request'];result=wire['reply']['result'];op=c['op'];need(wire['reply']['ok'] is True and wire['reply']['id']==q['id']==i+1,'actual sequential successful current GPU wire')
  need(c['native_result']==result and c['result']==map_native(result,context) and c['actual_API_executed'] is True,'all actual native results and precise typed identity projection')
  need(c['record']==r['record'] and c['generation']==r['generation'] and r['generation']==r['create_wire_index']+1,'original COM leaf tied to its actual creation lifetime')
  want=dict(id=i+1,op=op)
  if op=='create':
   want.update(width=r['size'][0],height=r['size'][1],levels=1,usage=0,format=25,pool=1);need(c['slot']==80 and c['return_va']==0x403C8A and c['args'][1:]==[r['size'][0],r['size'][1],1,0,25,1,r['record']+44],'full original texture creation ABI')
  else:
   want['pointer']=r['native_pointer'];need(c['args'][0]==r['texture']['pointer'] and c['target']==r['texture']['methods'][str(c['slot'])],'current original COM receiver and method')
   if op=='lock':want['flags']=2048;need(c['return_va']==0x40395E and c['args'][1:]==[0,c['args'][2],0,2048],'original level0 NO_SYSLOCK lock')
   elif op=='unlock':want['hex']=r['upload_hex'];need(c['return_va']==0x4039D3 and c['args'][1:]==[0],'original unlock arguments')
   elif op=='describe':need(c['return_va'] in (0x403CBE,0x403A44) and c['args'][1]==0,'original creation/destruction descriptor')
   else:need(op=='release' and c['return_va']==0x40378D and c['args']==[r['texture']['pointer']] and result==dict(count=0),'original single final Release')
  need(q==want,'entire actual current GPU request '+op)
 for r in d['common_resources']:
  i=r['readback_wire_index'];indices.append(i);wire=row['GPU_trace'][i];need(wire['request']==dict(id=i+1,op='readback',pointer=r['native_pointer']) and wire['reply']['result']==r['readback'],'every full readback is an explicit real observer')
 start=d['prefix']['GPU_wire'];end=max(indices)+1;need(sorted(indices)==list(range(start,end)),'every new GPU operation classified once without omitted wires')
 # Audit all current native lifetimes together, including the eight inherited
 # survivors, instead of relying on a historic live/peak number.
 live={};locked=set();peak=creates=0
 for i,t in enumerate(row['GPU_trace']):
  q=t['request'];z=t['reply']['result'];op=q['op']
  if op=='create':
   p=z['texture']['pointer'];need(p not in live,'no duplicate live native pointer');live[p]=i;creates+=1;peak=max(peak,len(live))
  elif op=='close':need(i==len(row['GPU_trace'])-1 and not live and not locked and not z['texture_releases'],'actual normal GPU close after every original release')
  else:
   p=q['pointer'];need(p in live,'native operation belongs to currently live generation')
   if op=='lock':need(p not in locked,'one live lock');locked.add(p)
   elif op=='unlock':need(p in locked,'unlock a real held surface');locked.remove(p)
   elif op=='release':need(p not in locked and z['count']==0,'unlocked actual final Release');del live[p]
 need(peak==469 and creates in (476,479),'actual inherited and new creation totals and peak')
 return dict(new_records=580,new_textures=461,markers=119,current_peak_live=peak,current_total_creates=creates,all_palette_and_padding_bytes_verified=True,GPU_wire_interval=[start,end],all_current_lifetimes_closed=True)


def current_intervals(row):
 d=row['terminal_battle_exit_prefix'];items=d['leaves']+d['cleanup']['leaves'];crt=[];gpu=[]
 for item in items:
  c=item['call']
  if item['kind']=='CRT':crt.extend(range(c['wire_start'],c['wire_end']))
  elif item['kind']=='GPU':gpu.append(c['wire_index'])
 gpu.extend(r['readback_wire_index'] for r in d['common_resources'])
 out={}
 for name,values in [('CRT',crt),('GPU',gpu)]:
  need(values,'actual added '+name+' interval');start=d['prefix'][name+'_wire'];end=max(values)+1
  need(sorted(set(values))==list(range(start,end)),'every added '+name+' wire has declared actual provenance')
  out[name]=(start,end)
 return out

def compact_terminal(memory):
 t=e.terminal
 return dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])

def parent_view(row):
 """An explicit local protocol view of actual old-lifetime wires only.

 The complete current trace is audited separately. The inserted COMMON wires
 form one closed interval, so old-lifetime indices can be translated exactly.
 No historical CPU, cleanup state, memory or digest is supplied here.
 """
 d=row['terminal_battle_exit_prefix'];intervals=current_intervals(row)
 def index(value,kind):
  if value is None:return None
  a,b=intervals[kind]
  need(not a<=value<b,'an old-lifetime reference cannot point inside COMMON '+kind)
  return value if value<a else value-(b-a)
 def edge(value,kind):
  a,b=intervals[kind]
  need(not a<value<b,'an old boundary cannot split the COMMON '+kind+' interval')
  return value if value<=a else value-(b-a)
 def rebuild(obj,path=()):
  if isinstance(obj,list):return [rebuild(v,path+(i,)) for i,v in enumerate(obj)]
  if not isinstance(obj,dict):return obj
  if path and path[-1]=='blobs':return obj
  out={k:rebuild(v,path+(k,)) for k,v in obj.items()}
  for k in ('wire_start','wire_end'):
   if k in out:out[k]=edge(out[k],'CRT')
  for k in ('create_wire_index','release_wire_index','readback_wire_index'):
   if k in out:out[k]=index(out[k],'GPU')
  if 'wire_index' in out:
   if 'slot' in out and 'op' in out or isinstance(out.get('result'),dict) and 'pitch' in out['result']:out['wire_index']=index(out['wire_index'],'GPU')
   elif 'native_allocation_readbacks' in path:out['wire_index']=index(out['wire_index'],'CRT')
  return out
 shallow={k:v for k,v in row.items() if k!='terminal_battle_exit_prefix'}
 for name in ('CRT','GPU'):
  a,b=intervals[name];trace=row[name+'_trace'];kept=trace[:a]+trace[b:]
  shallow[name+'_trace']=[dict(t,request=dict(t['request'],id=i+1),reply=dict(t['reply'],id=i+1)) for i,t in enumerate(kept)]
 a,b=intervals['CRT'];shallow['CRT_APIs']=[r for r in row['CRT_APIs'] if not a<=r['wire_start']<b]
 # Rebuild the indexed metadata using the original indices, not the already
 # renumbered wire arrays (their payloads have no metadata indices).
 trace_fields={k:shallow.pop(k) for k in ('CRT_trace','GPU_trace')};out=rebuild(shallow);out.update(trace_fields)
 cap=d['before'];out.update(final=cap['memory'],pending_CPU=cap['CPU'],instructions=cap['trace']['instructions'],writes=cap['trace']['writes'],code_trace_sha256=cap['trace']['code_sha256'],write_trace_sha256=cap['trace']['write_sha256'],entries=d['parent_entries'],extra_original_instruction_counts=d['prefix']['extra_counts'],typed_GPU_projection=d['common_projection_before']['ledger'])
 out['final_state']=dict(out['final_state'],terminal_state=compact_terminal(cap['memory']))
 return out,dict(current_inserted_intervals={k:list(v) for k,v in intervals.items()},old_payloads_are_actual_current_wires=True,historical_cleanup_CPU_or_SHA_projection=False)

def adapted_parent_native():
 """Only the two actual helper capacity assertions differ for parent lifetimes."""
 original=parent.previous_stage.native;text=textwrap.dedent(inspect.getsource(original));tree=ast.parse(text);changed=copy.deepcopy(tree);edits=[]
 for n in ast.walk(changed):
  if not isinstance(n,ast.Compare):continue
  expr=ast.unparse(n)
  if expr=="row['current_GPU_hello']['max_textures'] == 10":n.comparators=[ast.Constant(value=500)];edits.append('max_textures')
  elif expr=="row['current_GPU_hello']['max_creates'] == 32":n.comparators=[ast.Constant(value=512)];edits.append('max_creates')
 need(sorted(edits)==['max_creates','max_textures'],'exactly two current capacity assertion adaptations')
 scope=dict(original.__globals__);exec(compile(ast.fix_missing_locations(changed),__file__+':parent-capacity','exec'),scope)
 return scope['native'],dict(original_source_sha256=sha(text.encode()),declared_assertion_changes=sorted(edits),parent_machine_algorithm_changed=False)

def validate_current_CRT(row):
 """Audit actual current heap/file/critical owners across all inserted work."""
 blocks={};files={};criticals={};depth=0;heap=None;operations=0;paths={}
 # Original and new complete source files, never a source-emulator output.
 for name in ('data/adv/bin/Gybc_00.bin','data/adv/bin/sc001.bin','data/adv/bin/sc002.bin','data/Tactics/common.bin'):
  path=ROOT/'CROSS HERMIT/CROSS HERMIT'/name.upper();paths[name.lower().replace('/',chr(92))]=path.read_bytes()
 for i,t in enumerate(row['CRT_trace']):
  q=t['request'];r=t['reply'];need(q['id']==r['id']==i+1 and r['ok'] is True,'ordered actual complete CRT wire');z=r['result'];op=q['op'];operations+=1
  if op=='heap_create':need(heap is None and z['pointer']>0,'one actual owned current heap');heap=z['pointer']
  elif op=='alloc':
   p=z['pointer'];n=q['bytes'];need(q['heap']==heap and depth>0 and p not in blocks and 0<n<=2097152 and len(bytes.fromhex(z['hex']))==n,'actual bounded owned allocation with all initial native bytes');blocks[p]=bytes.fromhex(z['hex'])
  elif op=='sync':
   p=q['pointer'];raw=bytes.fromhex(q['hex']);need(p in blocks and len(raw)==len(blocks[p]) and z==dict(pointer=p,hex=q['hex']),'whole actual original buffer synchronized');blocks[p]=raw
  elif op=='readback':need(q['pointer'] in blocks and z==dict(pointer=q['pointer'],hex=blocks[q['pointer']].hex()),'whole current native buffer readback')
  elif op in ('validate','free'):
   p=q['pointer'];need(p in blocks and q['heap']==heap and depth>0 and z==dict(value=1,pointer=p,before_hex=blocks[p].hex()),'actual complete native validation/free of owned current buffer')
   if op=='free':del blocks[p]
  elif op in ('badread','badwrite'):
   p=q['pointer'];need(p in blocks and q['offset']>=0 and q['offset']+q['bytes']<=len(blocks[p]) and z==dict(value=0,pointer=p,offset=q['offset'],bytes=q['bytes']),'actual bounded current owned memory query')
  elif op=='initialize':need(q['guest'] not in criticals and len(bytes.fromhex(z['hex']))==24,'real unique complete critical section');criticals[q['guest']]=z['pointer']
  elif op in ('enter','leave'):
   need(q['critical'] in criticals.values(),'actual current critical owner');depth+=1 if op=='enter' else -1;need(0<=depth<=4 and z['depth']==depth and len(bytes.fromhex(z['critical_hex']))==24,'real balanced source lock depth and raw critical bytes')
  elif op=='delete':need(depth==0 and criticals.pop(q['guest'])==q['pointer'] and z==dict(value=1),'actual original lock deletion')
  elif op=='open':
   path=q['path'].lower();need(path in paths and z['handle'] not in files and not files,'one exact original read-only current file');files[z['handle']]=paths[path]
   need([q[k] for k in ('access','share','security','disposition','attributes','template')]==[0x80000000,1,0,3,1,0],'original read-only file flags')
  elif op=='size':need(q['handle'] in files and q['high']==0 and z==dict(value=len(files[q['handle']])),'actual complete original source file size')
  elif op=='read':
   p=q['pointer'];need(p in blocks and q['handle'] in files and q['bytes']==len(files[q['handle']]) and q['overlapped']==0,'actual full source read into current owned buffer')
   before=blocks[p];off=q['offset'];expected=before[:off]+files[q['handle']]+before[off+q['bytes']:]
   need(off+q['bytes']<=len(before) and z==dict(value=1,read=q['bytes'],pointer=p,before_hex=before.hex(),after_hex=expected.hex()),'actual full original file changes user bytes only');blocks[p]=expected
  elif op=='file_close':need(q['handle'] in files and z==dict(value=1),'actual original file close');del files[q['handle']]
  elif op=='heap_destroy':need(q['heap']==heap and not blocks and not files and not criticals and depth==0 and z==dict(value=1),'actual original heap destruction after all resources');heap=None
  elif op=='close':need(i==len(row['CRT_trace'])-1 and heap is None and not blocks and not files and not criticals and depth==0 and z['all_owned_resources_released'] and not z['forced_cleanup'],'actual normal CRT close without fallback')
  else:need(op in ('directory','version'),'only original independently classified CRT service operation '+op)
 need(row['CRT_exit']==row['GPU_exit']==0,'both actual native owners exit normally')
 return dict(actual_current_operations=operations-1,all_current_buffer_bytes_and_file_reads_verified=True,all_owners_released_without_fallback=True)


EXPECTED_ABI={0x46D340:(4,16),0x4075E0:(0,0),0x4077C0:(1,4),0x467C20:(1,4),0x472F40:(8,32),0x4539B0:(0,0),0x454CF0:(0,0),0x453F10:(0,0),0x46B470:(0,0),0x432100:(0,0),0x457AA0:(0,0),0x454C40:(0,0),0x453E10:(0,0),0x407870:(2,8),0x41F5A0:(2,8),0x41F340:(6,24),0x403BD0:(2,8),0x4048D0:(7,28),0x404150:(4,16),0x41F4E0:(1,4)}

def current_terminal_state(replay):
 # The portrait-era reader inherited immutable gates/flags/clocks/units from
 # self.p['before']. The new real world prefix changes these fields. Rebuild
 # every field of the original task_state schema from independently run RAM;
 # neither a cached historical state nor a source expected value supplies data.
 return dict(work=replay.read(e.overlay.WORK,0x24C0).hex(),VM=replay.read(e.VM,0x9400).hex(),gates=replay.read(e.CTRL+0x108B32,12).hex(),owner_flags=replay.read(e.CTRL+0x2A2FD,4).hex(),task=replay.read(e.TASK,0x190).hex(),remaining=num(replay.read(e.CTRL+0x2E6F4,4),0,'i'),elapsed=num(replay.read(e.CTRL+0x2E6F8,4),0,'i'),units=[replay.read(p,0x520).hex() for p in (e.terminal.UNIT,e.terminal.TARGET)],owner=replay.read(e.MAIN,0x10000).hex(),SEH=replay.read(0,4).hex(),task_input_flag=replay.read(e.TASK+0x117F20,1)[0],VM_counter=replay.read(0x7A4E18,8).hex())

def current_terminal_capture(replay,expected):
 try:parent.Replay.capture(replay,expected)
 except Exception as error:
  report='analysis/terminal-battle-exit-prefix-capture-mismatch-'+replay.row['input']['name']+'-'+str(time.time_ns())+'.json'
  e.terminal.save(report,dict(schema_version=1,acceptance=False,error=repr(error),actual_CPU=replay.cpu(),expected_CPU=expected['CPU'],actual_state=replay.state(),expected_state=expected['state'],actual_queue=replay.queue(),expected_queue=expected['queue'],verifier=file_ref(ROOT/'tools/terminal_battle_exit_verification.py')))
  print('independent inherited capture mismatch',report,flush=True)
  raise

def attach_current_protocol(replay,row):
 # Rebind every retained receipt/resource lookup to the complete actual current
 # protocol.  Ownership state, native cursors, CPU and RAM stay independently run.
 replay.row=row;replay.d=row['terminal_task_completion']
 replay.by_gen={r['generation']:r for r in replay.d['resources']};replay.by_label={r['label']:r for r in replay.d['resources']}
 replay.crt_case['native_trace']=row['CRT_trace'];replay.crt_case['native_hello']=row['current_CRT_hello']
 replay.state=types.MethodType(current_terminal_state,replay);replay.capture=types.MethodType(current_terminal_capture,replay)

def corrected_parent_summary(proof,row):
 # This is a newly generated in-memory proof, not the preserved historical JSON.
 # Retain its legacy number explicitly while reporting the independently counted
 # completed task roots, so the known omission is not propagated unqualified.
 summary=proof['forward_summary'];legacy=summary['complete_tasks'];count=contract.parent_task_accounting(row)
 need(legacy==count['accepted_task_completion'] and count['complete_tasks']==legacy+349,'only the proven349 original parent task returns correct the reused summary')
 summary.update(legacy_reported_complete_tasks=legacy,complete_tasks=count['complete_tasks'],additional_naturally_completed_stage_tasks=349)
 return count

def bind_original(function,scope):
 # Rebinding globals must retain the original Python call interface as well as
 # its machine-checking code. In particular verify_case(row,old=None) keeps the
 # unchanged accepted-witness lookup when the caller supplies only row.
 bound=types.FunctionType(function.__code__,scope,function.__name__,function.__defaults__,function.__closure__)
 bound.__kwdefaults__=copy.copy(function.__kwdefaults__)
 return bound

def replay_parent(row):
 view,view_audit=parent_view(row);instances=[];native,adaptation=adapted_parent_native()
 proxy=types.SimpleNamespace(**vars(parent.previous_stage));proxy.native=native
 scope=dict(vars(parent));scope['previous_stage']=proxy
 class CapturedReplay(parent.Replay):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 scope['Replay']=CapturedReplay;scope['native']=bind_original(parent.native,scope)
 verify=bind_original(parent.verify_case,scope)
 # Check the entire current parent protocol before spending time replaying its
 # original machine.  The same unchanged checks still run inside verify_case.
 native_preflight=scope['native'](view,proxy.parent_case(view))
 proof=verify(view);accounting=corrected_parent_summary(proof,row);need(len(instances)==1,'one unchanged original parent replay instance')
 replay=instances[0];capture(replay,row['terminal_battle_exit_prefix']['before'],'exact current parent boundary before new initialization',True)
 # Restore only references to the complete actual current protocol; all machine
 # memory and all57 architectural registers remain the independently run result.
 attach_current_protocol(replay,row)
 return replay,dict(parent_proof=proof,parent_task_accounting_correction=accounting,parent_native_preflight=native_preflight,protocol_view=view_audit,helper_assertion_adaptation=adaptation)

def common_crt_algorithm(replay):
 # Resolve the fixed original API machine explicitly; no source callback or
 # recorded result is used as the algorithm.
 from tools import terminal_followup_verification as follow
 original=follow.portrait.crtcheck.Replay.api
 sizes=tuple(b['bytes'] for b in replay.history)+(((1793036+51)&~15),((580*84+4+51)&~15))
 text=textwrap.dedent(inspect.getsource(original));tree=ast.parse(text);changed=copy.deepcopy(tree);replacements=[]
 for n in ast.walk(changed):
  if isinstance(n,ast.List) and all(isinstance(v,ast.Constant) for v in n.elts) and [v.value for v in n.elts]==[262208,128,262208]:
   n.elts=[ast.Constant(value=v) for v in sizes];replacements.append('source_allocation_sizes')
  if isinstance(n,ast.Constant) and n.value in (b'data'+bytes((92,))+b'adv'+bytes((92,))+b'bin'+bytes((92,))+b'sc004.bin','data'+chr(92)+'adv'+chr(92)+'bin'+chr(92)+'sc004.bin'):
   n.value=e.COMMON_NAME.encode() if isinstance(n.value,bytes) else e.COMMON_NAME;replacements.append('complete_common_path')
 need(replacements.count('source_allocation_sizes')==1 and replacements.count('complete_common_path')==2,'only independent complete COMMON size/path method inputs adapted')
 scope=dict(original.__globals__);exec(compile(ast.fix_missing_locations(changed),__file__+':common-crt-inputs','exec'),scope)
 replay.crt_api=scope['api'];replay.filebytes=catalog()[0]
 return dict(original_algorithm_sha256=sha(text.encode()),input_adaptations=replacements,additional_raw_allocation_sizes=list(sizes[-2:]),machine_algorithm_changed=False)

def map_span(replay,address,size):
 lo=address&~4095;end=(address+size+4095)&~4095
 for p in range(lo,end,4096):
  if not any(a<=p<=b for a,b,_ in replay.u.mem_regions()):replay.u.mem_map(p,4096)

def apply_gpu(replay,item,resources):
 c=item['call'];r=resources[c['index']];u=replay.u;slot=c['slot'];args=c['args'];result=c['result']
 need(c['pop']=={80:32,56:12,64:20,68:8,8:4}[slot],'original exact GPU stdcall pop')
 if c['op']=='create':
  t=r['texture']
  for pointer in (t['pointer'],t['vtable'],*t['methods'].values()):map_span(replay,pointer,4)
  u.mem_write(t['pointer'],struct.pack('<I',t['vtable']))
  for off,pointer in t['methods'].items():u.mem_write(t['vtable']+int(off),struct.pack('<I',pointer))
  outputs=[dict(pointer=r['record']+44,hex=struct.pack('<I',t['pointer']).hex())]
 elif c['op']=='describe':outputs=[dict(pointer=args[-1],hex=result['hex'])]
 elif c['op']=='lock':
  need(result==r['lock'],'the actual complete original lock output')
  outputs=[dict(pointer=result['bits'],hex=result['hex']),dict(pointer=args[2],hex=struct.pack('<II',result['pitch'],result['bits']).hex())]
 elif c['op']=='unlock':
  need(replay.read(r['lock']['bits'],len(bytes.fromhex(r['upload_hex']))).hex()==r['upload_hex'],'all actual original pixel stores before upload')
  outputs=[]
 else:need(c['op']=='release','one declared owned GPU operation');outputs=[]
 need(outputs==c['memory_outputs'] and c['value']==(result['count'] if slot==8 else result['hr'])==0,'every complete actual COM memory output and return')
 for out in outputs:
  raw=bytes.fromhex(out['hex']);map_span(replay,out['pointer'],len(raw));u.mem_write(out['pointer'],raw)
 replay.return_leaf(c,c['value'])

def leaf_entry(item):
 c=item['call'];kind=item['kind']
 need(kind in ('CRT','GPU','COMMON_STRING'),'only original finite platform leaf kind')
 return c['entry'] if kind=='COMMON_STRING' else c['target']

def common_strings(row):
 items=[i for i in row['terminal_battle_exit_prefix']['leaves'] if i['kind']=='COMMON_STRING']
 need(len(items)==119,'all original no-texture marker string calls')
 for item in items:
  c=item['call']
  need((c['name'],c['entry'],c['import_slot'],c['caller'],c['return_va'],c['args'],c['pop'],c['value'],c['result'],c['string_hex'])==('lstrlenA',0x770206E0,0x5922C4,0x41F416,0x41F416,[0x594734],4,13,13,b'Dm-No-MakeTex'.hex()),'complete original marker receipt schema and ABI')
  need(c['actual_API_executed'] is True and c['memory_outputs']==[] and c['new_mappings']==[],'actual marker API has no guest output buffers')
 return dict(actual_marker_string_calls=len(items),entry=0x770206E0,caller=0x41F416)

def apply_platform(replay,item,resources):
 c=item['call'];sp=replay.u.reg_read(x86.UC_X86_REG_ESP);args=[num(replay.read(sp+4+i,4),0) for i in range(0,c['pop'],4)]
 need(c['sp']==sp and c['return_va']==num(replay.read(sp,4),0) and c['args']==args,'entire actual original leaf stack/return ABI')
 if item['kind']=='CRT':replay.crt_leaf(c)
 elif item['kind']=='GPU':apply_gpu(replay,item,resources)
 else:
  need(item['kind']=='COMMON_STRING' and (c['entry'],c['return_va'],c['args'],c['value'],c['pop'])==(0x770206E0,0x41F416,[0x594734],13,4),'original COMMON marker length IAT leaf')
  need(replay.read(0x594734,14)==b'Dm-No-MakeTex'+bytes(1) and num(replay.read(0x5922C4,4),0)==c['entry'],'original readonly marker bytes and unchanged IAT')
  replay.return_leaf(c,13)

def current_cleanup_driver():
 # Keep the inherited independent instruction/leaf/capture algorithm.  Its
 # initial cumulative boundary now follows the verified current COMMON teardown;
 # neither the parent final capture nor any historical cleanup row is rewritten.
 original=parent.Replay.cleanup;text=textwrap.dedent(inspect.getsource(original));tree=ast.parse(text);changed=copy.deepcopy(tree);edits=0
 for n in ast.walk(changed):
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='last' and ast.unparse(n.value)=="d['final']['trace']":
   n.value=ast.parse("self.row['terminal_battle_exit_prefix']['cleanup']['capture']['trace']",mode='eval').body;edits+=1
 need(edits==1,'exactly one inherited cleanup starting-boundary adaptation')
 scope=dict(original.__globals__);exec(compile(ast.fix_missing_locations(changed),__file__+':current-cleanup-boundary','exec'),scope)
 bound=parent.previous_stage.bind_replay(scope['cleanup'],'cleanup')
 return bound,dict(original_algorithm_sha256=sha(text.encode()),declared_boundary_changes=1,starting_boundary='independently verified current COMMON cleanup capture',parent_final_not_rewritten=True,historical_cleanup_projection=False)

def check_segment_result(replay,segment,trace,case,entries=None,expected_entries=None):
 actual_CPU=replay.cpu();expected_CPU=segment['CPU'];expected_trace=segment['local_after']
 if actual_CPU!=expected_CPU or trace!=expected_trace:
  cpu_diff={k:dict(actual=actual_CPU.get(k),expected=expected_CPU.get(k)) for k in sorted(set(actual_CPU)|set(expected_CPU)) if actual_CPU.get(k)!=expected_CPU.get(k)}
  report='analysis/terminal-battle-exit-prefix-replay-mismatch-'+case+'-'+segment['label']+'-'+str(time.time_ns())+'.json'
  e.terminal.save(report,dict(schema_version=1,acceptance=False,case=case,segment=segment['label'],actual_CPU=actual_CPU,expected_CPU=expected_CPU,CPU_differences=cpu_diff,actual_trace=trace,expected_trace=expected_trace,actual_entries=entries,expected_full_forward_entries=expected_entries,verifier=file_ref(ROOT/'tools/terminal_battle_exit_verification.py')))
  print('independent segment mismatch',report,'CPU differences',cpu_diff,'actual trace',trace,'expected trace',expected_trace,flush=True)
 need(actual_CPU==expected_CPU and trace==expected_trace,'all57 CPU and complete original segment instruction/write digest '+segment['label'])

def check_forward_write(expected,index,actual):
 if index>=len(expected) or actual!=expected[index]:
  need(False,'first original forward write mismatch '+str(dict(index=index,actual=actual,expected=expected[index] if index<len(expected) else None)))

def execute_current(replay,row):
 """All new original instructions/writes and actual supplemental teardown."""
 need(e.EVENT_ABI==EXPECTED_ABI,'independently declared finite original ABI set')
 d=row['terminal_battle_exit_prefix'];u=replay.u;u.ctl_flush_tb();u.mem_protect(0x791000,0x3000,3);resources={r['source']['index']:r for r in d['common_resources']};crt_audit=common_crt_algorithm(replay)
 events=[];pending=[];writes_seen=[];entries={};counter=written=0;slice_first=0;ih=hashlib.sha256();wh=hashlib.sha256();leaf_index=text_index=0;stop=label=None;phase=None;items=d['leaves'];texts=d['strict_text_receipts']
 def mark():return dict(instructions=counter,writes=written,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())
 def hook(uc,at,size,_):
  nonlocal counter,leaf_index,text_index
  if budget.yield_before_observation(uc,at,stop,counter,slice_first):return
  sp=uc.reg_read(x86.UC_X86_REG_ESP)
  while pending and (at,sp)==(pending[-1]['caller'],pending[-1]['return_ESP']):
   v=pending.pop();v.update(after_CPU=replay.cpu(),result=uc.reg_read(x86.UC_X86_REG_EAX),after=state(replay))
  if at==stop:uc.emu_stop();return
  need(at not in (0x424F80,0x4CE9C5,0x454E18,0x4967B0),'no asserted/successor/consumer code before original wait')
  if leaf_index<len(items) and at==leaf_entry(items[leaf_index]):
   item=items[leaf_index];apply_platform(replay,item,resources);leaf_index+=1
   # COMMON string leaves return before the source's instruction-entry counter.
   if item['kind']!='COMMON_STRING':entries[hex(at)]=entries.get(hex(at),0)+1
   return
  if at in e.TEXT_APIS:
   need(text_index<len(texts),'declared current original task text receipt');c=texts[text_index];text_index+=1
   caller=num(replay.read(sp,4),0);arg=num(replay.read(sp+4,4),0);name,slot,expected=e.TEXT_APIS[at]
   need((c['entry'],c['segment'],c['caller'],c['args'])==(at,label,caller,[arg]) and caller==expected and num(replay.read(slot,4),0)==at,'strict actual original task input stack and IAT')
   need(c['actual_API_executed'] is True and c['result']==c['value']==0,'actual bounded task input result')
   if name=='lstrlenA':need(arg==e.INPUT+0x528 and replay.read(arg,1)==bytes(1),'only fixed empty owned input buffer')
   else:need(arg==num(replay.read(e.INPUT+8,4),0)==0,'only owned null IME context')
   replay.return_leaf(c,0);return
  need(at in e.ALLOWED and replay.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'unchanged original finite exit-prefix instruction '+hex(at))
  if at in EXPECTED_ABI:
   cpu=replay.cpu();n,pop=EXPECTED_ABI[at];v=dict(entry=at,caller=num(replay.read(sp,4),0),receiver=cpu['ECX'],args=[num(replay.read(sp+4+j*4,4),0) for j in range(n)],return_ESP=sp+4+pop,before_CPU=cpu,before=state(replay),phase=phase);events.append(v);pending.append(v)
  entries[hex(at)]=entries.get(hex(at),0)+1;counter+=1;ih.update(struct.pack('<I',at))
 def write(uc,access,at,size,value,_):
  nonlocal written
  need(not 0x400000<=at<0x593000,'original machine cannot alter code or IAT')
  written+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
  if not e.STACK<=at<e.STACK+0x20000:
   actual=dict(pc=uc.reg_read(x86.UC_X86_REG_EIP),address=at,bytes=size,value=value&((1<<min(64,size*8))-1))
   if phase!='cleanup':check_forward_write(d['writes'],len(writes_seen),actual)
   writes_seen.append(actual)
 hc=u.hook_add(UC_HOOK_CODE,hook);hw=u.hook_add(UC_HOOK_MEM_WRITE,write)
 def run(segments,cleanup=False):
  nonlocal stop,label,phase,slice_first
  for s in segments:
   label=s['label'];phase='cleanup' if cleanup else 'dependency' if label in ('common_read','common_register','common_file_free') else 'prefix';stop=s['stop']
   need(replay.cpu()==s['before_CPU'] and mark()==s['local_before'],'exact original continuous segment start '+label)
   root=s['root'];need(root is not None,'every new segment is an explicit independently admitted root')
   sp=e.STACK+0xF000;u.mem_write(sp,struct.pack('<I',e.RETURN))
   for j,value in enumerate(root['args']):u.mem_write(sp+4+4*j,struct.pack('<I',value))
   u.reg_write(x86.UC_X86_REG_ESP,sp);u.reg_write(x86.UC_X86_REG_ECX,root['receiver']);u.ctl_remove_cache(s['entry'],s['entry']+1)
   for chunk in range(512):
    slice_first=counter;u.emu_start(s['entry'] if chunk==0 else u.reg_read(x86.UC_X86_REG_EIP),0,timeout=0,count=0)
    if u.reg_read(x86.UC_X86_REG_EIP)==stop:break
    print(row['input']['name'],'independent exit',label,chunk+1,flush=True)
   else:need(False,'finite original segment execution budget '+label)
   check_segment_result(replay,s,mark(),row['input']['name'],entries,d['entries'])
   capture(replay,s['capture_after'],'complete segment '+label)
   if stop==e.RETURN:need(u.reg_read(x86.UC_X86_REG_ESP)==sp+4+(0 if root.get('cdecl') else 4*len(root['args'])),'original exact root stack return '+label)
 try:
  run(d['segments']);need(leaf_index==len(items) and text_index==len(texts),'all actual new forward leaves consumed once')
  need(events==d['events'] and entries==d['entries'] and writes_seen==d['writes'],'all original forward call ABI/fullCPU/events/writes/entry counts reexecuted')
  need(mark()==d['final']['local_trace'],'complete independent new forward digest');capture(replay,d['final'],'complete original missing-image CALL freeze',True)
  need([events.index(v) for v in pending]==d['freeze']['open_events'],'all original suspended frames accounted for')
  forward=dict(mark());pending.clear();items=d['cleanup']['leaves'];leaf_index=0;events.clear();replay.cleaning=True
  run(d['cleanup']['segments'],True);need(leaf_index==len(items) and not pending and events==d['cleanup']['events'],'every original supplemental COMMON destructor call naturally returns')
  capture(replay,d['cleanup']['capture'],'actual supplemental COMMON cleanup',True)
 finally:u.hook_del(hc);u.hook_del(hw)
 cleanup,cleanup_binding=current_cleanup_driver();old_cleanup=cleanup(replay)
 return dict(cleanup_binding=cleanup_binding,forward=forward,complete_current_COMMON_cleanup=True,original_parent_cleanup=old_cleanup,independent_CRT_algorithm=crt_audit,no_historical_cleanup_CPU_or_SHA_projection=True)


def source_guard(row):
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 need(e.BattleExitMachine.source_code.__code__ is e.parent.BattleStageMachine.source_code.__code__ and e.REFERENCE.__code__ is e.parent.REFERENCE.__code__,'unchanged original instruction/byte guard algorithms')
 need(e.RANGES==e.parent.RANGES+e.EXTRA_RANGES and e.ALLOWED==frozenset(a for lo,hi in e.RANGES for a in range(lo,hi)),'declared exact original code permission union')
 for lo,hi in e.EXTRA_RANGES:
  seq=list(md.disasm(e.CODE[lo-0x400000:hi-0x400000],lo))
  need(seq and seq[0].mnemonic=='push' and seq[0].op_str=='ebp' and seq[-1].mnemonic=='ret' and seq[-1].address+seq[-1].size==hi,'each newly admitted original function is complete '+hex(lo))
 need(e.NEW_MUTABLE==((e.TASK+0x68,e.TASK+0xE8),(e.CTRL+0xDE4B0,e.CTRL+0xDE7B0),(0x765520,0x765720),(0x791730,0x793734)),'only original packet, palette and bounded sorting globals newly writable')
 need(e.CASE_FRONTIERS=={'neutral_running':0x40B2EC,'timeout_before_combat':0x46D3F4},'both actual frontend boundaries without source-input patching')
 need(e.SORTING_RW_PAGES==(0x791000,0x3000),'only declared original sorting data pages re-exposed after parent capture')
 raw=(ROOT/'analysis/hermit_game.exe').read_bytes();pe=num(raw,0x3C);sections=num(raw,pe+6,'H');table=pe+24+num(raw,pe+20,'H');writable=[]
 for j in range(sections):
  p=table+40*j;size,va=struct.unpack_from('<II',raw,p+8);flags=num(raw,p+36)
  if flags&0xC0000000==0xC0000000:writable.append((0x400000+va,0x400000+va+size))
 need(any(lo<=0x791000 and 0x794000<=hi for lo,hi in writable),'all sorting permission pages lie in original PE read/write data')
 call=e.CODE[0x40B2EC-0x400000:0x40B2F1-0x400000]
 need(call==bytes((0xE8,))+struct.pack('<i',0x407870-0x40B2F1),'unexecuted real unit-image lookup CALL and return address')
 for address,want in {0x40B2D9:('mov','ax, word ptr [ebp + edx*2 - 0x18]'),0x40B2E8:('push','eax'),0x40B2E9:('mov','ecx, dword ptr [ebp + 0xc]'),0x40B7CD:('push','0x2004'),0x40B7D4:('push','0x791730'),0x40B81D:('cmp','dword ptr [0x791730], 0x800')}.items():
  ins=next(md.disasm(e.CODE[address-0x400000:address-0x400000+16],address));need((ins.mnemonic,ins.op_str)==want,'independent new query/sorting instruction '+hex(address))
 for address,want in {0x46D3D9:('mov','ecx, dword ptr [eax + 0x258]'),0x46D3DF:('movsx','eax, word ptr [ecx + 0x1c]'),0x46D3E3:('imul','eax, eax, 0x64'),0x46D3EF:('movsx','ecx, word ptr [ecx + 0x1a]'),0x46D3F3:('cdq',''),0x46D3F4:('idiv','ecx'),0x46D67E:('ret','0x10')}.items():
  ins=next(md.disasm(e.CODE[address-0x400000:address-0x400000+16],address));need((ins.mnemonic,ins.op_str)==want,'original HUD MP ratio and ABI '+hex(address))
 need(e.CODE[0x46CF6C-0x400000:0x46CF71-0x400000]==bytes((0xE8,))+struct.pack('<i',0x46D340-0x46CF71),'original HUD CALL and pushed return address')
 common_chain={0x4516F0:0x451B10,0x451B3E:0x42AE20,0x451B7F:0x416790,0x451BBB:0x428AD0}
 for site,target in common_chain.items():need(e.CODE[site-0x400000:site-0x400000+5]==bytes((0xE8,))+struct.pack('<i',target-site-5),'original COMMON initialization call chain '+hex(site))
 need(e.CODE[0x451B2D-0x400000:0x451B32-0x400000]==bytes((0x68,))+struct.pack('<I',0x59A438) and e.CODE[0x451B73-0x400000:0x451B75-0x400000]==bytes((0x6A,0x5A)),'original COMMON path and group90 arguments')
 sites=((0xDE4B0,0x4654B8,0x4659F9),(0xDE530,0x4654CA,0x465A0E),(0xDE5B0,0x4654DC,0x465A22),(0xDE630,0x4654EE,0x465A37),(0xDE6B0,0x465500,0x465A4C),(0xDE730,0x465512,0x465A60))
 for off,ctor,bind in sites:
  for site,target in ((ctor,0x4075E0),(bind,0x4077C0)):
   need(e.CODE[site-0x400000:site-0x400000+5]==bytes((0xE8,))+struct.pack('<i',target-site-5) and e.CODE[site-0x400000-6:site-0x400000]==bytes((0x81,0xC1))+struct.pack('<I',off),'original six-packet constructor/owner derivation '+hex(site))
 helper=e.helper_contract()
 # Transport keeps the original request/response algorithms; only the bounded
 # complete-buffer string constants change for the 1.8MiB real source file.
 old=e.overlay.platform.crt.Live
 for name,limit in (('_read',16777216),('request',5000000)):
  a=getattr(old,name).__code__;b=getattr(e.CommonCRTLive,name).__code__
  need(a.co_code==b.co_code and a.co_names==b.co_names and tuple(limit if v==3000000 else v for v in a.co_consts)==b.co_consts,'only declared transport bound constant differs '+name)
 return dict(original_exit=contract.original_exit_contract(),original_palette=original_palette_contract(),complete_new_functions=len(e.EXTRA_RANGES),original_COMMON_call_chain={hex(k):hex(v) for k,v in common_chain.items()},helper=helper,original_controller_packet_offsets=[x[0] for x in sites],case_frontiers={'neutral_running':0x40B2EC,'timeout_before_combat':0x46D3F4},freeze_call_site=0x40B2EC,unavailable_resource_group=0,original_wait_reached=False)

def verify_case(row):
 provenance=source_guard(row);data=protocol(row);observed_tasks=task_observations(row);common_strings(row);native=common_native(row);CRT=validate_current_CRT(row)
 replay,prior=replay_parent(row)
 executed=execute_current(replay,row)
 d=row['terminal_battle_exit_prefix'];cap=d['final']
 need(row['pending_CPU']==cap['CPU'] and row['image_before']==row['image_after'],'all final CPU and original code/IAT retained')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(cap['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'complete source cumulative fields bound to frozen original trace')
 equal(row['final'],cap['memory'],'complete actual current frozen memory')
 need(parent.expand(row['final_state']['terminal_state'],row['blobs'])==compact_terminal(cap['memory']),'terminal summary pages equal independently executed complete memory')
 return dict(name=row['input']['name'],source=provenance,protocol=data,task_observations=observed_tasks,native=native,CRT=CRT,parent=prior,original_execution=executed,forward_summary=dict(full_cumulative=cap['trace'],mapped_regions=len(cap['memory']),CPU_registers=len(cap['CPU']),complete_tasks=data['complete_tasks'],pending_scene_loops=1,frontend_frontier=dict(kind=d['freeze']['kind'],entry=d['freeze']['entry']),first_unavailable_resource=d['freeze'].get('args'),original_wait_reached=False,terminal_battle_exit_executed=False),whole_current_original_code_memory_CPU_and_native_protocol_verified=True)

def file_ref(path):
 path=Path(path);h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,sha256=h.hexdigest())

def corpus_provenance(header):
 """Bind resumed corpus assembly to preserved inputs, without restoring state."""
 if 'case_provenance' not in header:
  need('resume_inputs' not in header,'whole-run source cannot carry partial resume metadata')
  return dict(kind='whole_native_corpus_run')
 need(header['guest_or_native_state_restored'] is False,'corpus assembly never restores guest or native state')
 def document(identity):
  path=ROOT/identity['path'];need(file_ref(path)==identity,'actual immutable corpus provenance '+identity['path']);return json.loads(path.read_text(encoding='utf8'))
 inputs=document(header['resume_inputs']);need(inputs['guest_or_native_state_restored'] is False,'resume input manifest forbids snapshot/handle restoration')
 provenance=header['case_provenance'];need(len(provenance)==2,'exact two independently owned native cases')
 retained,fresh=provenance
 need(retained['name']=='neutral_running' and retained['kind']=='retained_complete_native_case' and fresh['name']=='timeout_before_combat' and fresh['kind']=='new_complete_native_case','retained and newly constructed case identities')
 for key in ('prior_process','prior_catalog'):need(retained[key]==inputs[key],'same actual preserved prior source '+key)
 prior=document(retained['prior_process']);catalog=document(retained['prior_catalog'])
 need(prior['exit_code']!=0 and prior['implementation_unchanged'],'retained case belongs to failed corpus with unchanged runtime')
 for path,identity in prior['implementation_end'].items():need(file_ref(ROOT/path)==identity,'retained runtime inputs still exact '+path)
 candidates=[x for x in catalog['entries'] if x['path'].endswith('/case-0.json')]
 need(len(candidates)==1 and candidates[0]['byte_equal'],'one previously byte-preserved full first case')
 old=candidates[0];identity={k:old[k] for k in ('path','bytes','sha256')}
 need(retained['retained_artifact']==inputs['retained_case']==identity,'retained raw case identity binds prior exact backup catalog')
 need((ROOT/old['path']).stat().st_size==Path(old['backup_path']).stat().st_size==old['bytes'],'both retained raw case copies remain present at original size')
 runtime=file_ref(ROOT/'tools/terminal_battle_exit_emulation.py')
 need(inputs['runtime_source']==fresh['runtime_source']==runtime,'new case uses same unchanged complete original source')
 need(inputs['helper_build']==header['helper_build'],'exact helper provenance across both independent cases')
 for kind,suffix in (('CRT','crt'),('GPU','gpu')):
  helper=header['helper_build'][kind]
  need(helper['existing_binary_reused'] is True and helper['helper_sha256']==file_ref(ROOT/'.venv-audit'/('terminal-battle-exit-'+suffix+'.exe'))['sha256'],'same retained native helper binary '+kind)
  equivalence=helper['source_equivalence'];rebuilt=equivalence['rebuilt_helper'];need(file_ref(ROOT/rebuilt['path'])==rebuilt,'actual independently rebuilt helper identity '+kind)
  a=normalized_managed_image((ROOT/'.venv-audit'/('terminal-battle-exit-'+suffix+'.exe')).read_bytes());b=normalized_managed_image((ROOT/rebuilt['path']).read_bytes())
  need(a==b and sha(a)==equivalence['normalized_sha256'] and equivalence['all_other_bytes_equal'] is True and equivalence['historical_executable_hash_recorded'] is False,'full helper code/data identity with explicit historical hash limitation '+kind)
 return dict(kind='retained_complete_case_plus_new_complete_case',retained_case=identity,prior_process=retained['prior_process'],prior_catalog=retained['prior_catalog'],resume_inputs=header['resume_inputs'],guest_or_native_state_restored=False)

def verify(path,helper_prefix='terminal-battle-exit-prefix-proof'):
 path=Path(path);need(path.is_file(),'immutable full source report exists');source_identity=file_ref(path);e.fixed_parents();helpers=e.helpers(helper_prefix);proofs=[];pcs=set();stream=parent.stream_report(path);declared=None;footer=None
 try:
  kind,header=next(stream);need(kind=='header' and header['schema_version']==1,'complete source report header')
  assembly=corpus_provenance(header);declared=header['source_contract'];static=copy.deepcopy(declared)
  for item in static['new_mutable']:item['write_PCs']=[]
  need(static==e.source_contract(),'complete declared original source/helper/input contract')
  gpu=header['helper_build']['GPU'];crt=header['helper_build']['CRT']
  need(Path(gpu['source']).as_posix()=='tools/terminal_battle_exit_d3d8_platform.cs' and gpu['source_sha256']==e.helper_contract()['GPU']['sha256'] and gpu['machine']==0x14C,'actual exact current bounded GPU helper source')
  need(Path(crt['source']).as_posix()=='tools/terminal_battle_exit_crt_platform.cs' and crt['source_sha256']==e.helper_contract()['CRT']['sha256'] and crt['machine']==0x14C,'actual exact current bounded CRT helper source')
  corpus=e.overlay.parent.corpus()
  for kind,row in stream:
   if kind=='footer':footer=row;break
   index=len(proofs);need(index<len(corpus) and row['input']==corpus[index],'both selected full original cases in order')
   print('independent exit-prefix case',row['input']['name'],'data checks',flush=True);proof=verify_case(row);old=parent.accepted_case_witness()[row['input']['name']]
   other=None
   try:
    other=e.run_case(row['input'],helpers[0],helpers[1],old['ticks'])
    # Independent machine execution of the source already checks every new byte.
    # A second full fresh owner executes the complete lifetime from construction;
    # its actual native protocol/bytes are separately audited before comparison.
    protocol(other);source_guard(other);task_observations(other);common_strings(other);common_native(other);validate_current_CRT(other)
    for key in ('initial','final'):equal(row[key],other[key],'new full original instance entire '+key+' memory')
    for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'new full original instance complete cumulative '+key)
    for key in ('terminal_battle_stage_handoff','terminal_battle_exit_prefix','task_completion_cleanup'):need(parent.guest(row[key])==parent.guest(other[key]),'new instance entire guest/current native-validated stage '+key)
   except Exception as error:
    if other is not None:
     diagnostic='analysis/terminal-battle-exit-diagnostic-fresh-'+row['input']['name']+'-'+str(time.time_ns())+'.json.gz'
     e.save_source(diagnostic,dict(schema_version=1,acceptance=False,source_report=source_identity,error=repr(error),fresh_original_case=other));print('full fresh failure preserved',diagnostic,flush=True)
    raise
   pcs.update(v['pc'] for v in row['terminal_battle_exit_prefix']['writes']);proof.update(new_complete_current_native_instance=True,all_cumulative_original_digests_reproduced=True);proofs.append(proof)
   print('independent exit-prefix case',row['input']['name'],'whole native lifetime reproduced',flush=True);del row,other;gc.collect()
  need(len(proofs)==len(corpus) and footer is not None,'both complete selected original cases')
  need(all(footer[k] is False for k in ('R3_complete','R4_complete','R5_complete','R6_complete')),'declared unresolved milestones')
  need(all(item['write_PCs']==sorted(pcs) for item in declared['new_mutable']),'all declared write PCs equal actual observed original writes')
 finally:stream.close()
 return dict(schema_version=1,source_report=source_identity,corpus_assembly=assembly,implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=proofs,whole_current_native_protocol_independently_verified=True,two_new_full_native_instances=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,terminal_battle_exit_prefix_executed=True,original_wait_reached=False,outer_result_consumed=False,terminal_battle_exit_executed=False,rewards_complete=False,draw_or_Present=False,terminal_presentation_complete=False,original_outer_thread_restored=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable independent exit-prefix proof');e.terminal.save(a.out,verify(ROOT/a.report,Path(a.out).stem))
