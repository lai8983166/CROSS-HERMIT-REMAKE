"""Independent source/cdecl/native MAIN graph, script, context and lifetime checks."""
import gzip,json,struct,hashlib
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EFLAGS
from tools.school_startup_lifetime_verification import ROOT,SOURCE,SOURCE_SHA256
from tools.school_scheduler_lifetime_verification import THUNK,verify_lifecycle
from tools.school_scene_bootstrap_verification import RANGES as BOOTSTRAP_RANGES,BASE_IAT

SIZE=0x1194f0;VM=0x7d7c28
RANGES=BOOTSTRAP_RANGES+((0x4e1b60,0x4e1c63),(0x49e930,0x49f570),(0x4da860,0x4dab50),(0x439e30,0x439ef0),(0x49dfd1,0x49e834),(0x451b10,0x4539b0),(0x4ce8f0,0x4d03b7),(0x46b470,0x46b663))
IAT=BASE_IAT+(0x5920a0,0x592068,0x5920c4)
ENTRIES={0x4e1bb4,0x4e1c4b,0x4da87e,0x448b18,0x46330e,0x46331e,0x463321,0x439eac,0x439eb2,0x49e39e,0x49e4b8,0x49e60f,0x4510ee,0x451148,0x421f88,0x4516d0,0x451ab7,0x4539ec,0x453a0c,0x453cb0,0x454d8b,0x46b49a,0x4220dd}
CDECL=THUNK.replace(bytes.fromhex('8b4e04ff16'),bytes.fromhex('8b4e04ff1683c404'))
APP='.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
def need(v,msg):
 if not v:raise ValueError(msg)
def word(b,p=0):return struct.unpack_from('<I',b,p)[0]
def sha(b):return hashlib.sha256(b).hexdigest()
def has(frames,*addresses):return any(all(a in [x['return_va'] for x in f['chain']] for a in addresses) for f in frames)

def source(s):
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA256==s['source_sha256'],'source SHA identity')
 ranges=[dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES]
 need(s['ranges']==ranges and s['IAT_slots']==list(IAT),'all fixed native source/vtable/import ranges');need(len(s['instructions'])==len(ENTRIES) and {i['va'] for i in s['instructions']}==ENTRIES,'all source graph operands')
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 for row in s['instructions']:
  at=row['va'];i=next(md.disasm(raw[at-0x400000:at-0x400000+16],at));need((row['hex'],row['mnemonic'],row['operands'])==(i.bytes.hex(),i.mnemonic,i.op_str),'actual original operand bytes')
 need(s['cdecl_thunk_hex']==CDECL.hex() and s['source_scenarios']==[76,77] and (s['event'],s['thread_vtable'],s['callback'],s['VM'])==(16,0x59a430,0x451670,VM),'exact native graph and cdecl bridge')
 need(all(s[k] is False for k in ('retained_checkpoint_rehydrated','physical_input_injected','complete_native_instruction_or_API_trace')),'source scope')
 return raw,ranges

def scenario_replay(raw,scene,before):
 need(scene in (76,77) and len(before)==80,'declared scenario inputs');u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(raw)+4095)&~4095);u.mem_write(0x400000,raw);u.mem_write(0x7f4488,before)
 for at,n in ((0x31000000,65536),(0x32000000,4096),(0x33000000,4096),(0x34000000,4096)):u.mem_map(at,n)
 u.mem_write(0x32000000,CDECL);u.mem_write(0x33000000,struct.pack('<11I',0x4da860,0,1,scene,0,0,0,0,0,0,0));u.mem_write(0x3100ff00,struct.pack('<2I',0x34000000,0x33000000));u.reg_write(UC_X86_REG_ESP,0x3100ff00);u.reg_write(UC_X86_REG_EFLAGS,0x202)
 counts=[];u.hook_add(UC_HOOK_CODE,lambda uc,at,n,_:counts.append(at));u.emu_start(0x32000000,0x34000000,count=50000);block=bytes(u.mem_read(0x33000000,44));need(u.reg_read(UC_X86_REG_ESP)==0x3100ff08 and word(block,32)==word(block,36) and word(block,40)==0x4c4c4143,'independent original cdecl ABI')
 return bytes(u.mem_read(0x7f4488,80)),len(counts)

def verify_frame(f):
 b=bytes.fromhex(f['context_hex']);need(len(b)==716 and (f['EBP'],f['EIP'],f['ESP'])==tuple(word(b,p) for p in (180,184,196)),'complete actual WOW64 frame scalars')
 chain=f['chain']
 if chain:need(chain[0]['bp']==f['EBP'],'actual sampled frame root')
 for a,b in zip(chain,chain[1:]):need(a['saved_bp']==b['bp'] and a['bp']<b['bp']<a['bp']+0x100000,'bounded actual original chain')

def graph(row,main):
 heads=bytes.fromhex(row['manager_heads_hex']);need(len(heads)==256,'complete 32-bucket manager heads');mapping={x['pointer']:x for x in row['registered_tasks']};need(len(mapping)==len(row['registered_tasks']),'no duplicate native registered objects');order=[]
 for bucket in range(32):
  task=word(heads,bucket*8);seen=set()
  while task:
   need(task not in seen and task in mapping and len(seen)<128,'complete bounded native registered graph');seen.add(task);x=mapping[task];b=bytes.fromhex(x['head_hex']);need(x['bucket']==bucket and len(b)==48 and word(b,8)==main+0x64,'actual original registered task manager');order.append(x);task=word(b,12)
 need(order==row['registered_tasks'],'all native task links accounted for')
 node=row['scene_global']
 if node:
  need(node in mapping and mapping[node]['bucket']==0,'source factory registered scene in actual MAIN bucket0');h=bytes.fromhex(row['node_head_hex']);need(len(h)==512 and h[:48]==bytes.fromhex(mapping[node]['head_hex']) and word(h)==0x59a430 and word(h,8)==main+0x64 and word(h,0x18)==0 and h[0x28]==1,'original published scene vtable/owner/parameter/autoDelete')

def verify_report(report):
 need(report['schema_version']==1 and report['R3_complete'] is False,'honest milestone envelope');raw,ranges=source(report['source_contract']);c=report['case'];p=c['probe'];need(p is not None and p['error'] is None,'complete successful native scene probe')
 need(c['scene']==p['scene'] and c['scene'] in (76,77) and c['original_scene_callback_executed'] is True and all(c[k] is False for k in ('source_code_IAT_or_existing_registers_replaced','retained_checkpoint_rehydrated','physical_input_injected','full_native_instruction_or_API_trace')),'native scene/scope integrity')
 life=verify_lifecycle(c['lifecycle']);main=p['main'];need(main==c['lifecycle']['ready']['main']['pointer'] and Path(p['process_image']).resolve()==(ROOT/APP).resolve(),'actual private executable/MAIN provenance')
 need(sha((ROOT/APP).read_bytes())=='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7','unchanged private original executable')
 expected=dict(code=ranges,IAT=p['source_before']['IAT']);need(p['source_before']==p['source_after']==expected and [i['slot'] for i in expected['IAT']]==list(IAT) and all(word(bytes.fromhex(i['hex'])) for i in expected['IAT']),'live original code/vtable/IAT unchanged')
 allocations=p['allocations'];need([a['bytes'] for a in allocations]==[0x200000,4096,4096],'all private call allocation extents')
 for i,a in enumerate(allocations):
  need(0<a['pointer']<a['pointer']+a['bytes']<=0x100000000,'x86 allocation bounds')
  for b in allocations[i+1:]:need(a['pointer']+a['bytes']<=b['pointer'] or b['pointer']+b['bytes']<=a['pointer'],'nonoverlapping private buffers')
 need(p['frees']==[dict(**a,released=True) for a in reversed(allocations)],'actual private allocation cleanup')
 calls=p['calls'];protocol=[(0x4e1b60,0,[]),(0x4da860,0,[p['scene']]),(0x439e30,main+0x10,[16])];need(len(calls)==3 and [(x['va'],x['receiver'],x['args']) for x in calls]==protocol,'only actual context/scenario/MAIN event roots; no task or VM shortcut')
 data,std,cdecl=[a['pointer'] for a in allocations];writes=[dict(pointer=std,bytes=len(THUNK),sha256=sha(THUNK)),dict(pointer=cdecl,bytes=len(CDECL),sha256=sha(CDECL))]
 for i,x in enumerate(calls):
  before=struct.pack('<11I',x['va'],x['receiver'],len(x['args']),*(x['args']+[0]*(3-len(x['args']))),0,0xcccccccc,0xcccccccc,0xcccccccc,0);after=bytes.fromhex(x['parameter_after_hex'])
  need(x['sequence']==i and x['slot']==0 and x['parameter_before_hex']==before.hex() and len(after)==44 and after[:28]==before[:28] and word(after,28)==x['eax'] and word(after,32)==word(after,36)!=0 and word(after,40)==0x4c4c4143 and x['wait_status']==x['exit_code']==0 and x['thread_id'],'actual complete native call input/ESP/exit')
  writes.append(dict(pointer=data,bytes=44,sha256=sha(before)))
 need(p['writes']==writes,'every process write restricted to declared bridge/parameter bytes')
 selected,replay_count=scenario_replay(raw,p['scene'],bytes.fromhex(p['scenario_before_selection_hex']));need(p['scenario_selected_hex']==selected.hex() and len(bytes.fromhex(p['scenario_before_hex']))==80 and word(bytes.fromhex(p['event_before_hex']))==0,'original scenario output and fresh event input')
 script=p['script_file'];file=ROOT/script['installed_path'];private=ROOT/script['path'];contents=file.read_bytes();need(private.resolve().parent==((ROOT/APP).parent/'DATA/TACTICS/SCRIPT').resolve() and file.resolve().parent==(ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT').resolve() and private.name==file.name and contents==private.read_bytes()==bytes.fromhex(script['loaded_memory_hex']) and len(contents)==script['bytes'] and sha(contents)==script['sha256'],'complete loaded native script/source/private file bytes')
 # Windows monotonic timestamps can share a clock tick; indexes order snapshots.
 samples=p['samples'];need(1<=len(samples)<=1600 and [s['index'] for s in samples]==list(range(len(samples))) and all(a['elapsed']<=b['elapsed'] for a,b in zip(samples,samples[1:])) and samples[-1]['elapsed']>samples[0]['elapsed'],'bounded ordered actual native observations')
 worker=p['worker'];need(worker['thread_id'] and worker['remote_handle'] and worker['event'],'original source-created worker/event identities');world=[];active=[];published=set();outer=False;loading=False;factory=False
 for s in samples:
  for f in s['frames']:verify_frame(f)
  graph(s,main);node=s['scene_global'];factory|=has(s['frames'],0x49e3a3);outer|=has(s['frames'],0x49e614,0x49e4bd,0x49e058)
  if not node:continue
  published.add(node);h=bytes.fromhex(s['node_head_hex']);vm=bytes.fromhex(s['VM_hex']);need(len(vm)==128 and len(bytes.fromhex(s['world_gate_hex']))==80 and len(bytes.fromhex(s['first_world_unit_hex']))==0x520,'complete sampled scene/VM/world extents')
  wf=[f for f in s['frames'] if f['tid']==worker['thread_id']];loading|=has(wf,0x45170e)
  if word(h,4)&1:need((word(h,0x20),word(h,0x24),word(h,0x1c))==(worker['remote_handle'],worker['thread_id'],worker['event']),'same original worker handles throughout')
  ordinary=has(wf,0x42240d,0x453cb5,0x451abc,0x451716,0x421f8a,0x56e183) and h[0x30]==0 and word(h,0x34)==2
  need(bool(s.get('ordinary_scene_loop_wait'))==ordinary,'actual ordinary original CRT callback/wait ancestry')
  if ordinary:
   need(struct.unpack_from('<h',bytes.fromhex(s['world_gate_hex']),0x12)[0]!=0,'source world-update gate enabled');world.append(s)
  if s.get('active_original_script'):
   need(ordinary and h[0x43] and h[0x44]==2 and vm[4] and word(vm,28)>0 and word(vm,16)==script['loaded_pointer']+452,'original active task/VM script origin');active.append(s)
  if 'loaded_script_header' in s:need(s['loaded_script_header']==dict(pointer=word(h,0x64),hex=contents[:452].hex()),'loaded original script header')
  if 'VM_current_bytes' in s:
   pc=word(vm,28);need(word(vm,16)==script['loaded_pointer']+452 and s['VM_current_bytes']==dict(pointer=word(vm,16)+pc,hex=contents[452+pc:484+pc].hex()),'every actual VM PC/command byte matches original script')
 need(len(published)==1 and outer and loading and len(world)>=2 and len(active)>=2 and len({word(bytes.fromhex(s['VM_hex']),28) for s in active})>=2,'actual outer scheduler/loading/world/advancing script integration')
 objects=p['full_objects'];need([x['label'] for x in objects]==['first_ordinary_scene_loop','active_script_ordinary_scene_loop'],'two complete original scene states')
 for obj,s in zip(objects,[world[0],samples[-1]]):
  body=bytes.fromhex(obj['hex']);need(obj['pointer']==s['scene_global'] and len(body)==SIZE and body[:512].hex()==s['node_head_hex'] and body[0x108cb0:0x108d00].hex()==s['world_gate_hex'] and body[0x80c7c:0x8119c].hex()==s['first_world_unit_hex'],'complete object agrees with sampled scene/world windows')
 need(p['worker_before_close']==dict(wait_status=258,exit_code=259) and c['worker_after_close']==[dict(thread_id=worker['thread_id'],wait_status=0,exit_code=0,callback_natural_return_claimed=False)],'actual worker lives until original cleanup; no natural-return claim')
 return dict(scene=p['scene'],lifecycle=life,source_scenario_replay_instructions=replay_count,source_event_roots=3,actual_factory_ancestry_observed=factory,actual_original_outer_scheduler=True,actual_CRT_scene_loading_and_world_loop=True,world_gate_enabled=True,script=dict(path=script['installed_path'],bytes=len(contents),sha256=sha(contents),observed_positive_PCs=sorted({word(bytes.fromhex(s['VM_hex']),28) for s in active})),ordinary_loop_observations=len(world),active_script_observations=len(active),full_native_scene_states=2,full_scene_semantics_independently_replayed=False,native_per_instruction_or_API_trace=False,worker_natural_return_claimed=False,R3_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.report;out=ROOT/a.out;need(not out.exists(),'fresh native verification output');r=verify_report(json.loads(gzip.decompress(path.read_bytes())));r['report']=dict(path=a.report,sha256=sha(path.read_bytes()));out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');print('Verified original MAIN/CRT/world/script loop',r['scene'],'R3 incomplete')
