"""Independent byte models for native scheduler snapshots; no native API stubs."""
import hashlib,json,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_startup_lifetime_verification import (ROOT,SOURCE,SOURCE_SHA256,source_contract as startup_contract,verify_snapshot,verify_lifetime,chain_has,native_loop,epilogue)

RANGES=((0x421540,0x421be3),(0x421bf0,0x422289),(0x422290,0x422354),(0x422560,0x42260a),(0x42b2d0,0x42b2ef),(0x56e050,0x56e1e0),(0x56e1e0,0x56e230),(0x4539b0,0x453cfc),(0x594a54,0x594a5c))
IAT=(0x592228,0x59222c,0x592230,0x592234,0x592238,0x592260,0x592264,0x592268,0x59226c,0x592270,0x592274,0x59227c,0x592280)
THUNK=bytes.fromhex('558bec5356578b75088966208b5e0885db74094bff749e0c85db75f78b4e04ff1689461c896624c7462843414c4c31c05f5e5b5dc20400')
def need(v,msg):
 if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def word(b,p=0):return struct.unpack_from('<I',b,p)[0]
def put(b,p,v):struct.pack_into('<I',b,p,v)

def verify_source(r):
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA256==r['source_sha256'],'source SHA identity')
 need(r['ranges']==[dict(va=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES],'complete source ranges and base vtable')
 need(struct.unpack_from('<2I',raw,0x594a54-0x400000)==(0x422330,0x422300),'original callback vtable')
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 for row in r['instructions']:
  at=row['va'];i=next(md.disasm(raw[at-0x400000:at-0x400000+16],at))
  need((row['hex'],row['mnemonic'],row['operands'])==(i.bytes.hex(),i.mnemonic,i.op_str),'original operand bytes')
 need(bytes.fromhex(r['call_thunk_hex'])==THUNK and r['original_IAT_slots']==list(IAT),'declared fixed thunk/import slots')
 need((r['base_task_vtable'],r['base_callback'],r['worker'],r['runtime_beginthreadex'],r['runtime_endthreadex'])==(0x594a54,0x422330,0x421f50,0x56e050,0x56e1e0),'native callback and CRT source')
 need(r['source_callbacks_replaced'] is False and r['retained_scene_or_world_execution'] is False,'honest independent scheduler scope')
 return raw

def verify_lifecycle(c):
 need(c['error'] is None and c['native_execution'] is True and c['duplicate'] is None,'owned initialized native lifecycle')
 need(all(c[k] is False for k in ('original_code_written','original_registers_written','original_IAT_written','retained_VM_advanced','resumable_checkpoint')),'frozen observer scope')
 contract=startup_contract();initial=c['factory'];ready=c['ready'];shutdown=c['shutdown']
 for s in [initial,ready,*shutdown]:verify_snapshot(s,contract)
 need(initial['pid']==ready['pid'] and initial['elapsed']<ready['elapsed'] and chain_has(initial,0x45060f,0x49df8a,0x5714e6) and native_loop(ready),'same actual factory-to-loop ancestry')
 g=ready['globals'];main=g['0x7a4a00'];hwnd=g['0x7a0bb4'];w=ready['window'];req=c['close_request']
 need(all(g[k] for k in ('0x7a49fc','0x7a4a00','0x80a398','0x7a0bb4')),'original initialized object publications')
 need(w['is_window'] and w['pid']==ready['pid'] and w['hwnd']==w['find_window']==hwnd and w['property']==main,'original initialized window ownership')
 need(req['posted'] and req['pid']==ready['pid'] and req['pid'] in req['job_members'] and req['hwnd']==hwnd and req['property']==main and (req['message'],req['wParam'],req['lParam'])==(16,0,0) and req['elapsed']>ready['elapsed'],'owned normal WM_CLOSE')
 need(any(chain_has(s,0x49e0de,0x450797,0x412df5) for s in shutdown),'original destruction ancestry')
 terminal=[s for s in shutdown if all(s['globals'][k]==0 for k in ('0x7a49fc','0x7a4a00','0x80a398')) and (any(0x49e11a<=r['return_va']<0x49e131 for f in s['frames'] for r in f['chain']) or chain_has(s,0x5714f2) and 'crt_exit' in s)]
 need(terminal and c['window_after']==dict(is_window=False,property=0),'original globals/window cleanup')
 verify_lifetime(c['lifetime']);s=terminal[-1]
 if 'winmain_frame' in s:epilogue(s)
 if 'crt_exit' in s:need(s['crt_exit']['WinMain_result_hex']==s['crt_exit']['exit_argument_hex']=='00000000','actual CRT zero return')
 return dict(pid=ready['pid'],normal_original_game_cleanup=True,forced_termination=False,protector_process_statuses=c['lifetime']['exits'],protector_status_is_not_WinMain_return=True)

def verify_probe(p,raw):
 fill=p['fill'];buckets=p['buckets'];disabled=p['disabled'];nodes=p['nodes'];manager=p['manager'];allocations=p['private_allocations']
 need((fill,buckets,disabled) in [(0,[0],None),(165,[0,0,31],1),(204,[31,5,5],0)],'declared native input cases')
 need(len(allocations)==2 and [a['bytes'] for a in allocations]==[65536,4096],'fresh data/code allocations')
 data,code=[a['pointer'] for a in allocations]
 need(all(0<a['pointer']<a['pointer']+a['bytes']<=0x100000000 for a in allocations) and (data+65536<=code or code+4096<=data),'nonoverlapping x86 private buffers')
 need(manager==data+0x1000 and nodes==[data+0x2000+i*0x1000 for i in range(len(buckets))],'exact private object addresses')
 identity=dict(code=[dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES],IAT=p['source_before']['IAT'])
 need(p['source_before']==p['source_after']==identity and [r['slot'] for r in identity['IAT']]==list(IAT) and all(word(bytes.fromhex(r['hex'])) for r in identity['IAT']),'actual before/after full code/vtable/IAT identity')
 close=next(word(bytes.fromhex(r['hex'])) for r in identity['IAT'] if r['slot']==0x592270)
 stages=iter(p['stages']);calls=iter(p['calls']);state=bytearray([fill]*512);nb=[bytearray([fill]*128) for _ in nodes];checks=[];expected_writes=[dict(pointer=code,bytes=len(THUNK),sha256=sha(THUNK)),dict(pointer=manager,bytes=512,sha256=sha(state))]+[dict(pointer=a,bytes=128,sha256=sha(b)) for a,b in zip(nodes,nb)]
 def snapshot(label,external_cs=False):
  s=next(stages);need(s['label']==label and [r['pointer'] for r in s['nodes']]==nodes,'exact stage order/object set')
  actual=bytes.fromhex(s['manager_hex']);need(len(actual)==512,'complete manager extent')
  if external_cs:
   # Actual opaque OS CRITICAL_SECTION output, never a simulated API result.
   state[0x100:0x118]=actual[0x100:0x118]
  need(actual==state and [bytes.fromhex(r['hex']) for r in s['nodes']]==nb,'full manager/node/guard byte model at '+label)
  checks.append(dict(stage=label,compared_bytes=512+128*len(nodes),opaque_actual_OS_CS_bytes=24 if external_cs else 0))
  return s
 def call(va,receiver,args=(),eax=None):
  c=next(calls);need((c['va'],c['receiver'],c['args'],c['label'])==(va,receiver,list(args),'supplemental_CloseHandle' if va==close else 'source'),'exact original call order/receiver/args')
  before=struct.pack('<11I',va,receiver,len(args),*(list(args)+[0]*(3-len(args))),0,0xcccccccc,0xcccccccc,0xcccccccc,0)
  after=bytes.fromhex(c['parameter_after_hex']);need(c['parameter_before_hex']==before.hex() and len(after)==44 and after[:28]==before[:28],'complete call input block')
  need(word(after,40)==0x4c4c4143 and word(after,32)==word(after,36) and word(after,32)!=0 and word(after,28)==c['eax'] and c['thread_id'] and c['wait_status']==c['thread_exit_code']==0,'actual call thread completion/ESP/output')
  if eax is not None:need(c['eax']==eax,'original EAX return')
  expected_writes.append(dict(pointer=data,bytes=44,sha256=sha(before)))
  return c
 snapshot('declared_fresh_buffers');call(0x421540,manager,eax=manager);call(0x421660,manager,eax=0)
 state[:256]=bytes(256);init=p['stages'][1];put(state,0x118,word(bytes.fromhex(init['manager_hex']),0x118));need(word(state,0x118) not in (0,fill*0x1010101),'actual created manager event')
 snapshot('original_manager_initialized',external_cs=True);chains=[[] for _ in range(32)]
 for i,(node,bucket) in enumerate(zip(nodes,buckets)):
  call(0x422290,node,eax=node);put(nb[i],0,0x594a54);nb[i][0x28]=0;call(0x4216c0,manager,(node,bucket,0x12340000+i),eax=0)
  for off,val in [(4,0),(8,manager),(12,0),(0x14,0),(0x18,0x12340000+i)]:put(nb[i],off,val)
  if chains[bucket]:put(nb[chains[bucket][-1]],12,node)
  else:put(state,bucket*8,node)
  chains[bucket].append(i);snapshot('registered_'+str(i))
 if disabled is not None:
  call(0x422560,nodes[disabled],(2,),eax=nodes[disabled]);put(nb[disabled],4,2);snapshot('original_disabled_flag')
 workers=p['worker_threads'];expected_workers=[];expected_events=[]
 def dispatch(label,phase):
  call(0x4217c0,manager,eax=0);s=next(x for x in p['stages'] if x['label']==label);completed=[]
  for bucket,chain in enumerate(chains):
   for i in list(chain):
    if word(nb[i],4)&2:continue
    observed=bytes.fromhex(s['nodes'][i]['hex'])
    for off in (0x1c,0x20,0x24):
     value=word(observed,off);need(value not in (0,fill*0x1010101),'actual node event/thread/threadid');put(nb[i],off,value)
    position=chain.index(i)
    if position:put(nb[chain[position-1]],12,word(nb[i],12))
    else:put(state,bucket*8,word(nb[i],12))
    chain.remove(i);put(nb[i],4,0);completed.append(i)
  snapshot(label)
  # Host observations use node index order; source dispatch scans buckets.
  for i in sorted(completed):
   expected_workers.append(dict(index=i,handle=word(nb[i],0x20),thread_id=word(nb[i],0x24),wait_status=0,exit_code=0))
   expected_events.append(dict(label=phase+'_node_'+str(i),handle=word(nb[i],0x1c),duplicate_succeeded=False,error=6))
   call(close,0,(word(nb[i],0x20),),eax=1)
 dispatch('first_original_dispatch','first')
 if disabled is not None:
  call(0x4225a0,nodes[disabled],(2,),eax=nodes[disabled]);put(nb[disabled],4,0);snapshot('original_reenabled_flag');dispatch('second_original_dispatch','second')
 need(workers==expected_workers,'actual original CRT workers/waits/exit/handle association')
 call(0x4215f0,manager)
 for node in nodes:call(0x4222d0,node,eax=node)
 snapshot('original_destructors_returned',external_cs=True)
 expected_events.append(dict(label='manager_after_destructor',handle=word(state,0x118),duplicate_succeeded=False,error=6));need(p['closed_events']==expected_events,'actual closed source event handles')
 need(list(stages)==[] and list(calls)==[],'no omitted or additional stages/calls')
 need(p['private_writes']==expected_writes,'all private process writes accounted for')
 need(p['private_frees']==[dict(**a,released=True) for a in reversed(allocations)],'all private allocations released after real thread completion')
 return dict(full_buffer_checks=checks,source_callbacks_replaced=False,actual_CRT_workers=len(workers),source_closed_events_observed=len(expected_events),supplemental_exited_worker_handles_closed=len(workers),independent_full_buffer_bytes=sum(r['compared_bytes'] for r in checks),native_per_instruction_or_API_trace=False,retained_scene_execution=False)

def verify_report(report):
 need(report['schema_version']==1 and report['R3_complete'] is False and report['retained_VM_or_world_advanced'] is False and len(report['cases'])==3,'report scope/three cases')
 raw=verify_source(report['source_contract']);results=[]
 for c in report['cases']:
  need(c['private_process_buffers_written'] is True and all(c[k] is False for k in ('original_code_or_IAT_written','original_general_registers_replaced','retained_scene_execution')),'explicit private-write/native scope')
  p=c['native_scheduler_probe'];need(all(c[k]==p[k] for k in ('fill','buckets','disabled')),'same declared native input')
  results.append(dict(fill=c['fill'],buckets=c['buckets'],disabled=c['disabled'],scheduler=verify_probe(p,raw),lifecycle=verify_lifecycle(c['original_lifecycle'])))
 need(len({r['lifecycle']['pid'] for r in results})==3,'independent process runs')
 return dict(schema_version=1,cases=results,R3_complete=False,retained_scene_or_world_execution=False,full_native_instruction_trace=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable verification output required')
 report_path=ROOT/a.report;r=verify_report(json.loads(report_path.read_text(encoding='utf8')));r['report']=dict(path=a.report,sha256=sha(report_path.read_bytes()))
 out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');print('Verified 3 native scheduler lifetimes, 7 original workers, normal original teardown; R3 incomplete')
