"""Independent scene/condition/result rules and full original fresh replay."""
import argparse,copy,gzip,json,struct
from tools.battle_terminal_selection_emulation import *
from tools.battle_terminal_selection_model import verify as rules
from tools.battle_hit_damage_verification import root,full_cpu

IMPLEMENTATIONS=('tools/battle_terminal_selection_emulation.py','tools/battle_terminal_selection_model.py','tools/battle_terminal_selection_verification.py')


def memory(snapshot,at,n):
 r=next(r for r in snapshot if r['pointer']<=at and at+n<=r['pointer']+r['bytes']);return bytes.fromhex(r['hex'])[at-r['pointer']:at-r['pointer']+n]


def verify_case(r,replay=True):
 c=r['input'];validate(c);fixture=TerminalMachine(c)
 need(r['initial']==fixture.snapshot(),'all initial owned bytes from fixed combat source and explicit declarations')
 need(r['declarations']==[dict(address=a,value=v,format=f) for a,v,f in declarations(c)],'exact pre-root declaration list')
 need(r['parent_case']==next(x for x in accepted()['source_cases'] if x['name']==c['combat']),'fixed input combat source reference')
 need(r['image_before']==r['image_after']==fixture.image_identity(),'entire original code and IAT page remain unchanged')
 need(r['event']['before']==fixture.selected_state(),'actual event input bytes bound to complete initial memory')
 root(r['event']['call'],0x432100,CTRL,[]);root(r['finalization']['call'],0x473860,CTRL,[])
 for phase in ('event','finalization'):full_cpu(r[phase]['call'])
 need([(x['pointer'],x['bytes']) for x in r['final']]==list(REGIONS),'all final owned areas in exact order')
 for a,b in zip(r['initial'],r['final']):
  first,last=bytes.fromhex(a['hex']),bytes.fromhex(b['hex']);need(len(first)==len(last)==a['bytes'],'complete owned area bytes');base=a['pointer'];cursor=0
  for lo,hi in sorted((max(0,lo-base),min(len(first),hi-base)) for lo,hi in fixture.mutable if lo<base+len(first) and base<hi):
   need(first[cursor:lo]==last[cursor:lo],'read-only original bytes '+hex(base+cursor));cursor=max(cursor,hi)
  need(first[cursor:]==last[cursor:],'read-only original tail '+hex(base+cursor))
 need(memory(r['final'],TASK,0x190).hex()==r['finalization']['after']['task'],'final task output bound to whole memory')
 need(memory(r['final'],0x7F4000,0x1000)+memory(r['final'],0x7F5000,0x1000)==bytes.fromhex(r['finalization']['after']['result']),'final result pages bound to whole memory')
 for i in (0,1):need(memory(r['initial'],RECORD+i*256,256)==memory(r['final'],RECORD+i*256,256),'all combat record bytes preserved')
 code=SOURCE.read_bytes();trace=r['code_trace'];need(len(trace)==r['instructions'] and trace[0]==0x432100 and 0x473860 in trace,'full original instruction trace from both roots')
 need(all(type(at) is int and at in ALLOWED and code[at-0x400000]!=0xCC for at in set(trace)),'only declared original instruction bytes, no assertion')
 need(sha(b''.join(struct.pack('<I',at) for at in trace))==r['code_trace_sha256'],'complete original instruction digest')
 writes=r['write_trace'];need(len(writes)==r['writes'],'every original write captured')
 for w in writes:
  at,n=w['address'],w['bytes'];need(w['pc'] in ALLOWED and n in (1,2,4,8),'original write PC and size')
  need(any(a<=at and at+n<=b for a,b in fixture.mutable),'write in declared mutable area')
  need(any(a<=at and at+n<=a+size for a,size in REGIONS),'write in complete owned area')
 need(sha(b''.join(struct.pack('<IIQ',w['address'],w['bytes'],w['value']) for w in writes))==r['write_trace_sha256'],'complete original write digest')
 code=SOURCE.read_bytes()
 for e in r['calls']:
  full_cpu(e);at=e['entry'];need(at in OBSERVED and len(e['args'])==OBSERVED[at],'exact observed original entry ABI')
  need(e['cpu_before']['EIP']==at and e['cpu_before']['ECX']==e['receiver'],'actual original observed entry CPU')
  need(e['cpu_after']['EIP']==e['caller'] and e['cpu_after']['ESP']==e['return_ESP'] and e['cpu_after']['EAX']==e['result'],'actual original observed return CPU')
  for k in ('EBX','ESI','EDI','EBP'):need(e['cpu_before'][k]==e['cpu_after'][k],'observed callee-saved '+k)
  if e['caller']!=0x12100000:
   offset=e['caller']-5-0x400000;need(code[offset]==0xE8 and e['caller']+struct.unpack_from('<i',code,offset+1)[0]==at,'genuine original direct call target')
  else:need(at==0x432100,'sole explicit observed event root')
 expected=rules(r);selected=expected['sub'] is not None;need(len(r['APIs'])==2*int(selected),'only actual selected condition API leaves')
 for i,e in enumerate(r['APIs']):
  need(e['actual_API_executed'] is True,'source report actual native API')
  if i%2==0:
   need(e['name']=='lstrcmpA' and e['caller']==0x45521C and len(e['args'])==2 and e['args'][1]==0x59A60C,'original string API ABI')
   need(e['strings']==[fixture.string(a).hex() for a in e['args']] and e['strings'][0]!=e['strings'][1] and e['result']!=0,'actual source strings and condition marker inequality')
  else:need(e['name']=='GetTickCount' and e['args']==[] and e['caller']==0x45528D and type(e['result']) is int and 0<=e['result']<=0xFFFFFFFF,'actual original timestamp input')
 need(all(r[k] is False for k in ('game_function_results_stubbed','OS_input_submitted','derived_host_writes_after_first_root','original_outer_scheduler_connected')),'honest runtime boundaries')
 if replay:
  ticks=[e['result'] for e in r['APIs'] if e['name']=='GetTickCount'];other=TerminalMachine(c,ticks).run();a,b=copy.deepcopy(r),other
  for x in (a,b):
   for e in x['APIs']:e.pop('actual_API_executed');e.pop('captured_platform_input',None)
  need(a==b,'fresh all owned memory, 57-register CPU, calls and every original PC/write replay with explicit captured platform time')
 return dict(name=c['name'],**expected,original_instructions=r['instructions'],original_writes=r['writes'],condition_commands=len(r['commands']),actual_source_API_leaves=len(r['APIs']),all_owned_memory_CPU_trace_replayed=replay)


def verify(path):
 raw=path.read_bytes();d=json.loads(gzip.decompress(raw));need(d['source_contract']==source_contract(),'exact terminal source contract')
 need([r['input'] for r in d['cases']]==corpus(),'all eight exact source cases');need(all(d[k] is False for k in ('R3_complete','R4_complete','R5_complete','R6_complete')),'global milestones remain incomplete')
 rows=[]
 for r in d['cases']:rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
 return dict(schema_version=1,source_report=ref(path.relative_to(ROOT).as_posix()),cases=rows,case_count=len(rows),implementation_sha256={n:sha((ROOT/n).read_bytes()) for n in IMPLEMENTATIONS},
  original_instructions=sum(r['original_instructions'] for r in rows),original_writes=sum(r['original_writes'] for r in rows),
  independent_scene_condition_and_result_contracts=True,independent_whole_VM_or_world_byte_model=False,platform_tick_replay_explicit=True,combat_same_lifetime=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();save(a.out,verify(ROOT/a.report))
