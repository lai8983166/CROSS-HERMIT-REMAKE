"""Independent terminal task admission rules and full pending-state replay."""
import argparse,copy,gzip,json
from types import SimpleNamespace
from tools import terminal_task_emulation as e
from tools import terminal_task_model as model
from tools.battle_hit_damage_verification import full_cpu,root,platform
from tools.battle_lethal_combat import expand,validate_pages

IMPLEMENTATIONS=('tools/terminal_task_emulation.py','tools/terminal_task_model.py','tools/terminal_task_verification.py')


def ownership(row,fixture):
 for k in ('initial','final'):
  e.need([(r['pointer'],r['bytes']) for r in row[k]]==list(e.REGIONS),'all 50 complete owned regions')
  e.need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[k]),'all raw owned bytes')
 for b,a in zip(row['initial'],row['final']):
  before,after=bytes.fromhex(b['hex']),bytes.fromhex(a['hex']);base=b['pointer'];cursor=0
  for lo,hi in sorted((max(0,lo-base),min(len(before),hi-base)) for lo,hi in fixture.mutable if lo<base+len(before) and base<hi):
   e.need(before[cursor:lo]==after[cursor:lo],'unchanged original readonly owned bytes');cursor=max(cursor,hi)
  e.need(before[cursor:]==after[cursor:],'unchanged owned readonly tail')


def verify_case(row,replay=True):
 c=row['input'];e.need(c in e.corpus(),'two exact terminal task cases');fixture=e.TaskMachine(c);e.need(row['initial']==fixture.snapshot(),'fresh complete initial state without snapshot restore')
 e.need(row['image_before']==row['image_after']==fixture.image_identity(),'original code/IAT unchanged');ownership(row,fixture);validate_pages(row,row['blobs'])
 for h,b in row['blobs'].items():e.need(0<len(bytes.fromhex(b))<=4096 and e.sha(bytes.fromhex(b))==h,'lossless source state pages')
 frames=row['world_frames'];events=row['events'];e.need(len(frames)==len(events)==(1 if c['name']=='neutral_running' else 3),'world/event prefix stops at actual first selection')
 for i,(f,event) in enumerate(zip(frames,events)):
  root(f['call'],0x46B470,e.CTRL,[]);root(event['call'],0x432100,e.CTRL,[]);full_cpu(f['call']);full_cpu(event['call'])
  e.need(f['scanned_slots']==[e.UNIT+j*0x520 for j in range(250)] and not f['controls'],'full original pre-selection world with no host action')
  e.need(f['trace_after']==event['trace_before'],'continuous world/event trace interval');model.combat.event_contract(row,i)
 summary=model.combat.world_contracts(row);outcome=model.combat.event_contract(row,len(events)-1);admission=model.verify(row)
 e.need(row['admission']['frames'][0][0]['trace_before']==events[-1]['trace_after'],'live terminal request directly enters original task admission')
 steps=[s for f in row['admission']['frames'] for s in f]+[row['admission']['reset'],row['admission']['partial']]
 e.need([[s['call']['entry'] if 'call' in s else s['event']['call']['entry'] for s in f] for f in row['admission']['frames']]==[[0x425DE0,0x454CF0,0x453F10,0x46B470,0x432100]]*2,'declared original post-terminal root order')
 first_calls=first_writes=first_APIs=0
 for i,s in enumerate(steps):
  if i:e.need(steps[i-1]['trace_after']==s['trace_before'] and steps[i-1]['after']==s['before'],'continuous post-terminal task state and original digest chain')
  if 'event' in s:
   root(s['event']['call'],0x432100,e.CTRL,[]);full_cpu(s['event']['call']);continue
  e.need(s['calls'][0]==first_calls and s['writes'][0]==first_writes and s['APIs'][0]==first_APIs,'complete task observation/API/write intervals')
  first_calls=s['calls'][1];first_writes=s['writes'][1];first_APIs=s['APIs'][1]
  if 'call' in s:
   call=s['call'];entry=call['entry'];receiver=e.INPUT if entry==0x425DE0 else e.CTRL if entry==0x46B470 else e.TASK
   root(call,entry,receiver,[]);full_cpu(call);e.need(call['instructions']==s['trace_after']['instructions']-s['trace_before']['instructions']>0,'entire original full root interval')
  else:
   r=s['root'];e.need((r['entry'],r['receiver'],r['args'],r['ESP_before'],r['return_address'],r['returned'])==(0x454CF0,e.TASK,[],e.STACK+0xF000,e.RETURN,False),'exact pending task root input ABI')
 e.need((first_calls,first_writes,first_APIs)==(len(row['task_calls']),len(row['task_writes']),len(row['task_APIs'])),'all task observations included')
 opened=set(row['admission']['partial']['pending']['open_calls']);code=e.SOURCE.read_bytes()
 for i,call in enumerate(row['task_calls']):
  e.need(call['entry'] in e.OBSERVED,'only sourced task/VM/packet observations');e.need(call['cpu_before']['EIP']==call['entry'] and call['cpu_before']['ECX']==call['receiver'],'genuine original observer entry CPU')
  if i in opened:e.need('after' not in call and 'cpu_after' not in call,'open source frames remain pending')
  else:
   full_cpu(call);cpu=call['cpu_after'];e.need((cpu['EIP'],cpu['ESP'],cpu['EAX'])==(call['caller'],call['return_ESP'],call['result']),'actual original nested call return ABI')
   for k in ('EBX','ESI','EDI','EBP'):e.need(cpu[k]==call['cpu_before'][k],'original callee-saved '+k)
  if call['caller']!=e.RETURN:
   p=call['caller']-5-0x400000;e.need(code[p]==0xE8 and call['caller']+int.from_bytes(code[p+1:p+5],'little',signed=True)==call['entry'],'actual original direct call site')
 e.need(len([x for x in row['task_calls'] if x['entry']==0x4CE8F0])==1 and len([x for x in row['task_calls'] if x['entry']==0x42FC60])==1,'one naturally nested VM and original167 handler, no independent VM roots')
 e.need([x['name'] for x in row['task_APIs']]==['lstrlenA','ImmGetOpenStatus','lstrlenA','ImmGetOpenStatus','lstrlenA'],'three real task text resets and two pending IME queries')
 for x in row['task_APIs']:
  e.need(x['actual_API_executed'] is True and x['result']==0,'actual measured empty/null Windows task leaves')
  target=next(t for t,v in e.APIS.items() if v[0]==x['name']);name,slot,caller=e.APIS[target]
  e.need((x['target'],x['import_slot'],x['caller'])==(target,slot,caller),'original task API target/slot/caller')
  if name=='lstrlenA':e.need(x['args']==[e.INPUT+0x528] and x['string_hex']=='','exact original empty text input')
  else:e.need(x['args']==[0] and x['observed']['args']==[0] and x['observed']['actual_OS_observed'] is True and x['observed']['result']==0,'real null-context query, never physical input')
 e.need(row['IME_identity']==fixture.ime.identity,'actual loaded IME module identity and explicit host/guest pointer widths')
 platform(row['platform'],SimpleNamespace(crt_draws=summary['CRT_draws']))
 e.need(len(row['APIs'])==2 and all(x['actual_API_executed'] is True for x in row['APIs']),'actual first-capture condition API leaves')
 e.need(all(row[k] is False for k in ('game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization')),'no game stub, OS input or host-derived unit edits')
 # Raw end memory must preserve the incomplete original stack and SEH, not a clean exit.
 final={r['pointer']:bytes.fromhex(r['hex']) for r in row['final']};p=row['admission']['partial']['pending']
 e.need(final[e.STACK].hex()==p['stack'] and final[0][:4].hex()==row['admission']['partial']['after']['SEH'],'pending stack and exception chain retained in complete memory')
 if replay:
  other=e.TaskMachine(c,[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']).run();platform(other['platform'],SimpleNamespace(crt_draws=summary['CRT_draws']))
  a,b=copy.deepcopy(row),other
  for r in (a,b):
   r.pop('platform')
   for x in r['APIs']:x.pop('actual_API_executed');x.pop('captured_platform_input',None)
  e.need(a==b,'fresh entire 50-region/57-register/pending-stack/original-digest replay')
 return dict(name=c['name'],selector=outcome['selector'],sub=outcome['sub'],prefix_worlds=len(frames),post_terminal_worlds=2,
  **{k:v for k,v in admission.items() if k not in ('task_frames','source_rules')},original_instructions=row['instructions'],original_writes=row['writes'],
  actual_task_API_leaves=len(row['task_APIs']),original_task_observations=len(row['task_calls']),original_key_writes=len(row['task_writes']),all_owned_memory_CPU_and_trace_replayed=replay)


def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));e.need(d['source_contract']==e.source_contract() and [x['input'] for x in d['cases']]==e.corpus(),'exact terminal task source/case contracts')
 e.need(all(d[k] is False for k in ('R3_complete','R4_complete','R5_complete','R6_complete')),'global milestones remain incomplete')
 rows=[]
 for r in d['cases']:rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),source_rules=model.source_rules()[0],cases=rows,
  implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},owned_regions=50,CPU_registers=57,
  independent_task_input_VM_and_pending_packet_rules=True,all_owned_memory_CPU_and_trace_replayed=True,
  pending_third_task_or_VM_returned=False,resources_queried=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,
  R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();e.terminal.save(a.out,verify(e.ROOT/a.report))
