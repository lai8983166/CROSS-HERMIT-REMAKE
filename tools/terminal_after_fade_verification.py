"""Full current-native replay plus independent post-fade task, timer and pending font rules."""
import argparse,copy,gzip,json
from tools import terminal_after_fade_emulation as e
from tools import terminal_after_fade_model as model
from tools import terminal_overlay_verification as old
from tools.battle_hit_damage_verification import root,full_cpu
IMPLEMENTATIONS=('tools/terminal_after_fade_emulation.py','tools/terminal_after_fade_model.py','tools/terminal_after_fade_verification.py')

def verify_case(row,replay=False,helpers=None):
 prefix=model.prefix_view(row);previous=old.verify_case(prefix);result=model.verify(row);f=row['after_fade'];e.need(previous['VM_PC']==52,'accepted source prefix rules remain satisfied')
 e.need(row['image_before']==row['image_after']==prefix['image_before'],'unchanged original code and IAT')
 old.memory_equal(row['final'],f['memory'],'entire current pending forward boundary')
 for key,address,n in [('VM',e.VM,0x9400),('work',e.WORK,0x24C0),('task',e.TASK,0x190),('owner',e.MAIN,65536)]:e.need(model.read(row['final'],address,n).hex()==f['final'][key],'whole final '+key+' matches actual mappings')
 e.need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==(f['trace']['instructions'],f['trace']['writes'],f['trace']['code_sha256'],f['trace']['write_sha256']),'all forward original instruction and write digests')
 e.need(len(row['task_APIs'])==201,'101 empty resets and100 real null-IME queries')
 for frame in f['frames']:
  root(frame['reset']['call'],0x425DE0,e.INPUT,[])
  t=frame['task'];r=t['root'];e.need(r==dict(entry=0x454CF0,receiver=e.TASK,args=[],SP=e.STACK+0xF000,return_address=e.RETURN),'only complete original task root setup')
  if t['returned']:
   for k in ('EBP','EBX','ESI','EDI'):e.need(t['CPU'][k]==t['cpu_before_setup'][k],'full task preserves original callee-saved '+k)
  a,b=frame['APIs'];leaves=row['task_APIs'][a:b];e.need([x['name'] for x in leaves]==['ImmGetOpenStatus','lstrlenA'],'original pending IME consumed then empty text reset')
  for x in leaves:
   e.need(x['actual_API_executed'] is True and x['result']==0,'new actual task query result')
   target=next(p for p,v in e.parent.parent.APIS.items() if v[0]==x['name']);name,slot,ret=e.parent.parent.APIS[target]
   e.need((x['target'],x['import_slot'],x['caller'])==(target,slot,ret),'unchanged original task import and caller')
   if name=='ImmGetOpenStatus':e.need(x['args']==[0] and x['observed']['args']==[0] and x['observed']['actual_OS_observed'] is True and x['observed']['result']==0,'actual current null-context IME query')
   else:e.need(x['args']==[e.INPUT+0x528] and x['string_hex']=='','actual empty declared buffer')
 e.need(row['IME_identity']==e.parent.parent.ActualIME().identity,'actual IMM32 source identity and host/guest widths')
 opened=set(f['pending']['open_calls']);code=e.CODE
 for i,x in enumerate(f['calls']):
  e.need(x['entry'] in e.OBSERVED and x['cpu_before']['EIP']==x['entry'] and x['cpu_before']['ECX']==x['receiver'],'actual source nested entry CPU')
  if i in opened:e.need('after' not in x and 'cpu_after' not in x,'pending original frames not returned')
  else:
   full_cpu(x);cpu=x['cpu_after'];e.need((cpu['EIP'],cpu['ESP'],cpu['EAX'])==(x['caller'],x['return_ESP'],x['result']),'full original nested return ABI')
   for k in ('EBP','EBX','ESI','EDI'):e.need(cpu[k]==x['cpu_before'][k],'nested original callee-saved '+k)
  if x['caller']!=e.RETURN:
   off=x['caller']-5-0x400000;e.need(code[off]==0xE8 and x['caller']+int.from_bytes(code[off+1:off+5],'little',signed=True)==x['entry'],'actual original nested direct call source')
 e.need([x['entry'] for x in f['calls']].count(0x4977A0)==1,'one original fade completion wait-clear call')
 e.need(row['cleanup_state']==prefix['cleanup_state'] and row['CRT_cleanup']['all_owned_resources_released'] and row['GPU_cleanup']['all_owned_resources_released'],'source original supplemental resource cleanup remains complete')
 if replay:
  ch,gh=helpers[:2];other=e.run_case(row['input'],ch,gh,[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']);model.verify(other);old.verify_case(model.prefix_view(other))
  for key in ('initial','final'):old.memory_equal(row[key],other[key],'fresh current-native full '+key)
  for key in ('admission','task_calls','task_writes','pending_CPU','final_state','world_frames','events','commands','instructions','writes','code_trace_sha256','write_trace_sha256','extra_original_instruction_counts','resource_initialization','cleanup_steps','cleanup_state','accounting_baseline','overlay_continuation','after_fade'):
   e.need(row[key]==other[key],'all exact source states,57CPU,stack and digest replay '+key)
  old.memory_equal(row['resource_loaded']['memory'],other['resource_loaded']['memory'],'fresh current source-loaded resources')
 result.pop('source_rules');result['all_owned_memory_CPU_and_trace_replayed']=replay;return result

def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));e.need(d['source_contract']==e.source_contract() and [r['input'] for r in d['cases']]==e.parent.parent.corpus(),'exact current source and two cases')
 ch,cb=e.parent.platform.build(e.ROOT/'tools/terminal_overlay_crt_platform.cs','terminal-after-fade-proof-crt');gh,gb=e.parent.platform.build(e.ROOT/'tools/terminal_overlay_d3d8_platform.cs','terminal-after-fade-proof-gpu');helpers=(ch,gh,dict(CRT=cb,GPU=gb));rows=[]
 for row in d['cases']:rows.append(verify_case(row,True,helpers));print('verified after-fade',row['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),cases=rows,source_rules=model.source_rules(),implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},independent_full_task_state_fade_timer_and_font_rules=True,all_current_native_resources_recreated_for_replay=True,all_owned_memory_CPU_and_trace_replayed=True,new_forward_VM_or_work_update_roots=0,font_executed=False,actual_draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();e.need(not(e.ROOT/a.out).exists(),'fresh immutable proof');e.terminal.save(a.out,verify(e.ROOT/a.report))
