"""Independent frame contracts and exact original world/event digest replay."""
import argparse,copy,gzip,json,struct,types
from concurrent.futures import ProcessPoolExecutor
from types import SimpleNamespace
from tools.battle_live_terminal_emulation import *
from tools import battle_live_terminal_model as model
from tools import battle_lethal_combat_verification as previous
from tools.battle_lethal_combat import expand,validate_pages
from tools.battle_hit_damage_verification import root,full_cpu,platform

IMPLEMENTATIONS=tuple('tools/battle_live_terminal'+s+'.py' for s in ('_emulation','_model','_verification'))
ownership=types.FunctionType(previous.ownership.__code__,dict(previous.ownership.__globals__,LethalMachine=LiveMachine,REGIONS=REGIONS))


def verify_case(row,replay=True):
 c=row['input'];validate(c);fixture=LiveMachine(c);blobs=row['blobs'];frames=row['world_frames'];events=row['events']
 need(row['initial']==fixture.snapshot(),'fresh complete initial state without combat snapshot restore')
 need(row['image_before']==row['image_after']==fixture.image_identity(),'original code/IAT bytes unchanged')
 need(row['combat_input']==fixture.cycle_input,'exact fresh lethal combat declarations')
 for h,b in blobs.items():need(0<len(bytes.fromhex(b))<=4096 and sha(bytes.fromhex(b))==h,'lossless live state page identity')
 validate_pages(row,blobs);ownership(row)
 root(row['target_bind']['call'],0x467020,CTRL,[TARGET,fixture.combat_input['job']]);root(row['bind'],0x467020,CTRL,[UNIT,fixture.combat_input['job']])
 need(len(row['roots'])==4,'four original packet initialization roots')
 for call,(u,off) in zip(row['roots'],[(u,o) for u in (UNIT,TARGET) for o in (0x2F4,0x3E0)]):root(call,0x437C90,FINE,[u+off])
 need(1<=len(frames)==len(events)<=c['budget'],'same instance world/event pairs')
 outcomes=[];lastcalls=0;code=SOURCE.read_bytes()
 for i,(f,e) in enumerate(zip(frames,events)):
  need(f['index']==i and not f['controls'],'continuous worlds without host combat command');root(f['call'],0x46B470,CTRL,[]);root(e['call'],0x432100,CTRL,[])
  full_cpu(f['call']);full_cpu(e['call']);need(f['call']['result']==0,'natural full world return')
  need(f['scanned_slots']==[UNIT+j*0x520 for j in range(250)],'all 250 ordered slot predicates')
  need([(u['unit'],u['index'],u['caller']) for u in f['unit_calls']]==[(UNIT,0,0x46B584),(TARGET,1,0x46B584)],'both natural complete unit roots')
  need(f['entries']==previous.EXPECTED_ENTRIES,'entire existing world helper order')
  need([s['name'] for s in f['stages']]==['before_units','after_units','world_return'],'all original world frontiers')
  for s in f['stages']:full_cpu(dict(cpu_before=s['CPU'],cpu_after=s['CPU']))
  for u in f['unit_calls']:
   full_cpu(u);need(u['cpu_before']['EIP']==0x46B760 and u['cpu_after']['EIP']==0x46B584 and u['cpu_after']['ESP']==u['cpu_before']['ESP']+12,'natural original unit ret8')
   for k in ('EBX','ESI','EDI','EBP'):need(u['cpu_before'][k]==u['cpu_after'][k],'natural unit callee-saved '+k)
  gated=[x for x in f['gated_calls'] if x['entry'] in (0x495220,0x4727F0,0x472960,0x458580,0x458BE0,0x457890,0x458180)]
  need([x['entry'] for x in gated]==[0x495220,0x4727F0,0x472960,0x458580,0x458BE0,0x457890,0x458180],'all original gated popup/preview/input bodies in order')
  clocks=[x for x in f['gated_calls'] if x['entry']==0x415040 and x['caller']==0x467BD2];need(len(clocks)==1 and clocks[0]['args']==[1],'one original world clock step with actual argument1')
  for x in f['gated_calls']:
   off=x['caller']-5-0x400000;need(code[off]==0xE8 and x['caller']+struct.unpack_from('<i',code,off+1)[0]==x['entry'],'genuine original gated direct call')
  need(f['trace_after']==e['trace_before'],'uninterrupted original world/event trace chain')
  for phase in (f,e):
   need(phase['call']['instructions']==phase['trace_after']['instructions']-phase['trace_before']['instructions']>0,'exact original root instruction interval')
   need(phase['trace_after']['writes']>phase['trace_before']['writes'],'original root writes are retained in cumulative interval')
   for stamp in (phase['trace_before'],phase['trace_after']):
    for key in ('code_sha256','write_sha256'):need(len(stamp[key])==64 and all(ch in '0123456789abcdef' for ch in stamp[key]),'original digest encoding')
  if i:
   need(frames[i-1]['trace_after']['instructions']<events[i-1]['trace_after']['instructions'] and events[i-1]['trace_after']==f['trace_before'],'continuous event to following world trace')
   need(expand(f['before'],blobs)['terminal_state']==expand(events[i-1]['after'],blobs),'same task/VM/records enter following world')
  need(e['calls'][0]==lastcalls and e['calls'][1]>lastcalls,'complete contiguous observed event call range');lastcalls=e['calls'][1]
  outcomes.append(model.event_contract(row,i))
  need(outcomes[-1]['selector']==0 or i==len(frames)-1,'stop at first original selector, without delayed terminal injection')
 need(outcomes[-1]['selector']!=0 or c['name']=='threshold_running' and len(frames)==192,'only survival control exhausts declared budget')
 if not outcomes[-1]['selector']:need(not row['commands'],'no condition VM for unselected live control')
 summary=model.world_contracts(row);result=model.finalization_contract(row,outcomes[-1])
 root(row['finalization']['call'],0x473860,CTRL,[]);full_cpu(row['finalization']['call'])
 need(len(row['APIs'])==2*int(outcomes[-1]['selector']!=0),'only selected condition API leaves')
 for i,e in enumerate(row['APIs']):
  need(e['actual_API_executed'] is True,'actual first-capture Windows leaf')
  if i%2==0:need(e['name']=='lstrcmpA' and e['caller']==0x45521C and e['args'][1]==0x59A60C and e['strings']==[fixture.string(a).hex() for a in e['args']] and e['result']!=0,'original condition strings and actual comparison')
  else:need(e['name']=='GetTickCount' and e['args']==[] and e['caller']==0x45528D and type(e['result']) is int and 0<=e['result']<=0xFFFFFFFF,'actual timestamp source')
 for x in row['calls']:
  full_cpu(x);need('after' in x and x['entry'] in terminal.OBSERVED,'complete terminal observer contract')
  need(x['cpu_before']['EIP']==x['entry'] and x['cpu_before']['ECX']==x['receiver'] and x['cpu_after']['EIP']==x['caller'] and x['cpu_after']['ESP']==x['return_ESP'] and x['cpu_after']['EAX']==x['result'],'original observer entry/return full CPU')
  for k in ('EBX','ESI','EDI','EBP'):need(x['cpu_before'][k]==x['cpu_after'][k],'event nested callee-saved '+k)
  if x['caller']==0x12100000:need(x['entry']==0x432100,'only event observer root')
  else:
   off=x['caller']-5-0x400000;need(code[off]==0xE8 and x['caller']+struct.unpack_from('<i',code,off+1)[0]==x['entry'],'actual direct terminal call site')
 platform(row['platform'],SimpleNamespace(crt_draws=summary['CRT_draws']))
 need(row['entries'].get('0x570fe0',0)==summary['CRT_draws'] and row['entries'].get('0x467e00',0)==summary['battle_draws'],'all original RNG bodies')
 need(row['original_coordinate_writes']==0 and all(row[k] is False for k in ('game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization')),'no host-derived battle changes or external input')
 for call in row['cleanup']+row['popup_cleanup']:full_cpu(call)
 if replay:
  ticks=[e['result'] for e in row['APIs'] if e['name']=='GetTickCount'];other=LiveMachine(c,ticks).run();platform(other['platform'],SimpleNamespace(crt_draws=summary['CRT_draws']));a,b=copy.deepcopy(row),other
  for r in (a,b):
   r.pop('platform')
   for e in r['APIs']:e.pop('actual_API_executed');e.pop('captured_platform_input',None)
  need(a==b,'fresh complete owned memory/57-register CPU/whole world and event trace digest replay')
 return dict(name=c['name'],frames=len(frames),slot_predicates=250*len(frames),natural_unit_updates=2*len(frames),**summary,**outcomes[-1],**result,
  instructions=row['instructions'],writes=row['writes'],actual_TLS_API_leaves=len(row['platform']['trace']),actual_condition_API_leaves=len(row['APIs']),all_owned_memory_CPU_trace_replayed=replay)


def verify_reference(ref):
 raw=(ROOT/ref['path']).read_bytes();need(len(raw)==ref['bytes'] and sha(raw)==ref['sha256'],'immutable live case');d=json.loads(gzip.decompress(raw));need(d['source_contract']==source_contract() and len(d['cases'])==1,'exact live case source contract')
 r=d['cases'][0];need(r['input']['name']==ref['name'],'exact referenced live case');s=verify_case(r);print('verified',ref['name'],s['frames'],flush=True);return s


def verify(path,jobs=3):
 raw=path.read_bytes();d=json.loads(raw);need(d['source_contract']==source_contract() and [r['name'] for r in d['case_reports']]==[c['name'] for c in corpus()],'all seven exact fresh live cases')
 need(all(d[k] is False for k in ('R3_complete','R4_complete','R5_complete','R6_complete')),'global milestones remain incomplete');need(1<=jobs<=3,'bounded fresh replay processes')
 with ProcessPoolExecutor(max_workers=jobs) as pool:rows=list(pool.map(verify_reference,d['case_reports']))
 return dict(schema_version=1,source_report=terminal.ref(path.relative_to(ROOT).as_posix()),case_count=7,cases=rows,implementation_sha256={n:sha((ROOT/n).read_bytes()) for n in IMPLEMENTATIONS},
  world_frames=sum(r['frames'] for r in rows),original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
  independent_frame_clock_combat_event_and_result_contracts=True,all_original_PC_and_write_digests_replayed=True,independent_whole_VM_world_byte_model=False,
  combat_world_events_same_instance=True,original_outer_scheduler_connected=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);p.add_argument('--jobs',type=int,default=3);a=p.parse_args();terminal.save(a.out,verify(ROOT/a.report,a.jobs))
