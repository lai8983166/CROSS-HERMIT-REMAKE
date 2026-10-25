"""Independent battle/work contracts and complete fresh-instance replay."""
import argparse,copy,gzip,json,types
from types import SimpleNamespace
from tools import terminal_work_emulation as e
from tools import terminal_work_model as model
from tools.battle_live_terminal_verification import ownership as old_ownership
from tools.battle_hit_damage_verification import root,full_cpu,platform
from tools.battle_lethal_combat import expand,validate_pages

ownership=types.FunctionType(old_ownership.__code__,dict(old_ownership.__globals__,LethalMachine=e.WorkMachine,REGIONS=e.REGIONS))
IMPLEMENTATIONS=('tools/terminal_work_emulation.py','tools/terminal_work_model.py','tools/terminal_work_verification.py')


def steps(row):
 w=row['work'];out=[row['initialization'],w['pause']]+w['idle']
 for x in w['experiments']:out += [x['handler']]+[s for tick in x['ticks'] for s in tick]
 return out


def verify_case(row,replay=True):
 c=row['input'];e.need(c in e.corpus(),'exact two finite work inputs');fixture=e.WorkMachine(c);blobs=row['blobs']
 e.need(row['initial']==fixture.snapshot() and row['initialization']['before']==fixture.work_state(),'fresh complete initial buffers and correct pre-root task work pointer')
 e.need(row['combat_input']==fixture.cycle_input,'exact fresh combat declaration');ownership(row);validate_pages(row,blobs)
 for h,b in blobs.items():e.need(0<len(bytes.fromhex(b))<=4096 and e.sha(bytes.fromhex(b))==h,'every lossless page bound')
 e.need(row['image_before']==row['image_after']==fixture.image_identity(),'original code and IAT preserved')
 root(row['target_bind']['call'],0x467020,e.CTRL,[e.TARGET,fixture.combat_input['job']]);root(row['bind'],0x467020,e.CTRL,[e.UNIT,fixture.combat_input['job']])
 e.need(len(row['roots'])==4,'four natural packet initialization roots')
 for call,(u,o) in zip(row['roots'],[(u,o) for u in (e.UNIT,e.TARGET) for o in (0x2F4,0x3E0)]):root(call,0x437C90,e.FINE,[u+o]);full_cpu(call)
 frames=row['world_frames'];events=row['events'];e.need(len(frames)==len(events)==(1 if c['name']=='neutral_running' else 3),'first original selection without delayed event')
 previous=None
 for i,(f,event) in enumerate(zip(frames,events)):
  root(f['call'],0x46B470,e.CTRL,[]);root(event['call'],0x432100,e.CTRL,[]);full_cpu(f['call']);full_cpu(event['call'])
  e.need(f['index']==i and not f['controls'] and f['scanned_slots']==[e.UNIT+j*0x520 for j in range(250)],'entire natural world and all ordered slot checks')
  e.need(len(f['unit_calls'])==2 and [u['unit'] for u in f['unit_calls']]==[e.UNIT,e.TARGET],'two natural full unit roots per pre-pause world')
  for u in f['unit_calls']:full_cpu(u)
  e.need(f['trace_after']==event['trace_before'],'unbroken world/event digest chain')
  if previous is not None:e.need(previous==f['trace_before'],'same logical instance through next world')
  previous=event['trace_after']
  model.combat.event_contract(row,i)
 summary=model.combat.world_contracts(row);outcome=model.combat.event_contract(row,len(events)-1)
 e.need(row['work']['pause']['trace_before']==events[-1]['trace_after'],'actual selected state immediately enters original pause world')
 work=model.verify_work(row);model.finalization(row,outcome)
 root(row['finalization']['call'],0x473860,e.CTRL,[]);full_cpu(row['finalization']['call'])
 trace=steps(row);first=0;write_first=0;code=e.SOURCE.read_bytes()
 for j,s in enumerate(trace):
  call=s['call'];full_cpu(call);receiver=e.CTRL if j==1 else e.VM if call['entry'] in (0x42D960,0x42D9F0) else e.WORK
  args=call['args'] if call['entry'] in (0x42D960,0x42D9F0) else [];root(call,call['entry'],receiver,args)
  e.need(call['entry'] in ({0x46B470}|set(e.ROOTS)-set(e.parent.LiveMachine.base_call.__globals__['ROOTS'])),'only declared supplemental work roots')
  e.need(s['calls'][0]==first and s['writes'][0]==write_first,'complete contiguous original work call/store intervals');first=s['calls'][1];write_first=s['writes'][1]
  e.need(s['trace_after']['instructions']-s['trace_before']['instructions']==call['instructions']>0 and s['trace_after']['writes']>s['trace_before']['writes'],'full original root trace interval')
  if j>=2:e.need(trace[j-1]['trace_after']==s['trace_before'],'continuous supplemental work root digest intervals')
  if j>1:e.need(trace[j-1]['after']==s['before'],'continuous work state between supplemental roots')
 e.need(first==len(row['work_calls']) and write_first==len(row['key_writes']),'no omitted tail observations')
 expected_entries=[0x497800,0x46B470,0x497AA0,0x498310,0x497C50]
 for entry in (0x42D960,0x42D9F0):expected_entries += [entry]+[x for _ in range(61) for x in (0x497AA0,0x498310,0x497C50)]
 e.need([s['call']['entry'] for s in trace]==expected_entries,'all supplemental roots in declared order')
 for call in row['work_calls']:
  full_cpu(call);e.need(call['entry'] in e.OBSERVED and 'after' in call,'every original work observation complete')
  cpu=call['cpu_after'];e.need((call['cpu_before']['EIP'],cpu['EIP'],cpu['ESP'],cpu['EAX'])==(call['entry'],call['caller'],call['return_ESP'],call['result']),'real nested original return CPU/ABI')
  for k in ('EBX','ESI','EDI','EBP'):e.need(call['cpu_before'][k]==cpu[k],'real work callee-saved '+k)
  if call['caller']!=0x12100000:
   p=call['caller']-5-0x400000;e.need(code[p]==0xE8 and call['caller']+int.from_bytes(code[p+1:p+5],'little',signed=True)==call['entry'],'genuine direct original work caller')
 pauses=[x for x in row['work_calls'] if x['entry']==0x43B250];e.need(len(pauses)==1 and pauses[0]['receiver']==e.CTRL+0x3D68 and pauses[0]['args']==[1],'actual original world controller pause target')
 menus=[x for x in row['work_calls'] if x['entry'] in (0x4553E0,0x4558A0,0x455D00)]
 e.need(len(menus)==3 and all(x['receiver']==e.TASK and x['args']==[0] for x in menus),'three original menu owners and pause arguments')
 releases=[x for x in row['work_calls'] if x['entry']==0x4977A0];e.need(len(releases)==2 and all(x['caller']==0x497C16 for x in releases),'two natural wait releases from completion, never supplied callback')
 ftol=[x for x in row['work_calls'] if x['entry']==0x56CFCC];e.need(len(ftol)==2 and all(x['result']==648 and x['cpu_before']['FPCW']==x['cpu_after']['FPCW'] for x in ftol),'actual x87 truncation and original control-word restore')
 platform(row['platform'],SimpleNamespace(crt_draws=summary['CRT_draws']))
 e.need(all(row[k] is False for k in ('game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization')),'no game stub, OS input or host-derived battle changes')
 e.need(len(row['APIs'])==2 and all(x['actual_API_executed'] is True for x in row['APIs']),'actual first-capture condition Windows leaves')
 e.need(row['APIs'][0]['name']=='lstrcmpA' and row['APIs'][1]['name']=='GetTickCount','unchanged native condition leaf protocol')
 for call in row['cleanup']+row['popup_cleanup']:full_cpu(call)
 if replay:
  other=e.WorkMachine(c,[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']).run()
  platform(other['platform'],SimpleNamespace(crt_draws=summary['CRT_draws']));a,b=copy.deepcopy(row),other
  for r in (a,b):
   r.pop('platform')
   for x in r['APIs']:x.pop('actual_API_executed');x.pop('captured_platform_input',None)
  e.need(a==b,'fresh full 46-region memory/57-register CPU/original trace digest replay')
 return dict(name=c['name'],combat_worlds=len(frames),pause_worlds=1,selector=outcome['selector'],sub=outcome['sub'],remaining=outcome['remaining'],elapsed=outcome['elapsed'],
  work=work,observed_original_work_calls=len(row['work_calls']),key_original_stores=len(row['key_writes']),instructions=row['instructions'],writes=row['writes'],
  all_owned_memory_CPU_and_trace_replayed=replay,normal_VM_or_task_playback_connected=False)


def verify(path,replay=True):
 d=json.loads(gzip.decompress(path.read_bytes()));e.need(d['schema_version']==1 and d['source_contract']==e.source_contract(),'exact work source contract')
 e.need([r['input'] for r in d['cases']]==e.corpus() and all(d[k] is False for k in ('R3_complete','R4_complete','R5_complete','R6_complete')),'both finite cases; global milestones still incomplete')
 rows=[]
 for row in d['cases']:rows.append(verify_case(row,replay));print('verified',row['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),cases=rows,
  implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},owned_regions=46,CPU_registers=57,
  independent_pause_and_exact_work_rules=True,all_owned_memory_CPU_and_trace_replayed=replay,
  normal_VM_or_task_playback_connected=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,
  R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();e.terminal.save(a.out,verify(e.ROOT/a.report))
