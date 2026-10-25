"""Original scene-4 event/condition VM from explicit accepted combat memory inputs."""
import argparse,ctypes,gzip,hashlib,json,struct,types
from functools import lru_cache
from pathlib import Path
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EIP
from tools import battle_lethal_combat_emulation as parent
from tools.school_script_preflight_catalog import RANGES as CONDITION_RANGES,package_offsets,vm_offsets

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,TARGET,RECORD=parent.CTRL,parent.UNIT,parent.TARGET,parent.RECORD
TASK,VM,WORK,SCRIPT=CTRL-0x190,0x7D7C28,0x12800000,0x12900000
PARENT='analysis/battle-lethal-combat-acceptance-v1-20261025.json'
PARENT_SHA='35034fa4c5f704769cb7eab14190f9c52a89906572cc191b6e41ddb31ab9d997'
SCRIPT_PATH='CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0004.BIN'
SCRIPT_SHA='dfeffff8e6a7e1582797af89c9836058596b65b2fe91049f2466754a8a86eae0'
EXTRA_REGIONS=((0x7D7000,0x1D000),(0x7F6000,0x8000),(0x10FFF000,0x1000),(WORK,0x1000),(SCRIPT,0x2000),(0x7701F000,0x1000),(0x77022000,0x1000))
REGIONS=parent.REGIONS+EXTRA_REGIONS
EXTRA_RANGES=((0x432100,0x432480),(0x433720,0x4337F0),(0x430BA0,0x430C30),(0x430DF0,0x4313F0),
 (0x4549D0,0x454CF0),(0x467850,0x4678C0),(0x46A4C0,0x46A550),(0x4695D0,0x469660),(0x40D120,0x40D330))
RANGES=parent.RANGES+EXTRA_RANGES+CONDITION_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
APIS={0x7701F780:('lstrcmpA',2,0x45521C),0x77022640:('GetTickCount',0,0x45528D)}
OBSERVED={0x432100:0,0x433720:0,0x4307B0:0,0x430BA0:0,0x430DF0:0,0x454AB0:1,
 0x454AF0:2,0x454BB0:3,0x4551C0:2,0x455060:2,0x4549D0:7,0x4CE460:3,0x4CE8F0:0,0x467850:2}


def ref(path):
 b=(ROOT/path).read_bytes();return dict(path=path,bytes=len(b),sha256=sha(b))


@lru_cache(maxsize=1)
def accepted():
 raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted lethal parent')
 return json.loads(raw)


@lru_cache(maxsize=4)
def combat(name):
 r=next(r for r in accepted()['source_cases'] if r['name']==name);raw=(ROOT/r['path']).read_bytes()
 need(len(raw)==r['bytes'] and sha(raw)==r['sha256'],'fixed complete combat snapshot identity')
 return json.loads(gzip.decompress(raw))['cases'][0]


def corpus():
 return [dict(name=n+('_expired' if t==0 else '_running'),combat=n,remaining=t) for n in
  ('enemy_dies_job1','player_dies_job1','player_threshold_survives','neutral_living_control') for t in (36000,0)]


def validate(c):need(c in corpus() and all(type(c[k]) is type(v) for k,v in corpus()[0].items()),'exact terminal corpus input')


def declarations(c):
 return [(0x7F4488,4,'h'),(0x7A49F8,WORK,'I'),(0x7A4A00,0,'I'),(CTRL+0x117C38,TASK,'I'),(TASK+0x60,VM,'I'),(TASK+0x64,SCRIPT,'I'),
  (TASK+0x38,5,'I'),(TASK+0x43,0,'B'),(TASK+0x59,0,'B'),(TASK+0x174,0,'I'),
  (CTRL+0x2E6F4,c['remaining'],'i'),(CTRL+0x2E6FC,c['remaining'],'i'),(CTRL+0x2E6F8,0,'i')]


def source_contract():
 raw=SOURCE.read_bytes();script=(ROOT/SCRIPT_PATH).read_bytes();need(sha(script)==SCRIPT_SHA,'original T0004 identity')
 return dict(parent_acceptance=dict(path=PARENT,sha256=PARENT_SHA),script=ref(SCRIPT_PATH),scene=4,
  snapshot_input_not_retained_CPU_resume=True,world_or_scheduler_same_lifetime=False,
  full_original_event_root=0x432100,explicit_result_input_root=0x473860,
  extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES+CONDITION_RANGES],
  original_IAT_unchanged=True,original_game_functions_stubbed=False,owned_regions=len(REGIONS),CPU_registers=57,
  first_run_actual_native_APIs=True,fresh_replay_uses_captured_tick_input=True,rewards_complete=False)


class TerminalMachine(parent.LethalMachine):
 source_code=types.FunctionType(parent.LethalMachine.source_code.__code__,dict(parent.LethalMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 snapshot=types.FunctionType(parent.LethalMachine.snapshot.__code__,dict(parent.LethalMachine.snapshot.__globals__,REGIONS=REGIONS))
 base_call=types.FunctionType(parent.LethalMachine.base_call.__code__,dict(parent.LethalMachine.base_call.__globals__,ROOTS=parent.LethalMachine.base_call.__globals__['ROOTS']|{0x432100}))

 def __init__(self,c,tick_inputs=None):
  validate(c);source_contract();p=combat(c['combat']);super().__init__(p['input']);self.terminal_input=c
  for r in p['final']:self.uc.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  for at,n in EXTRA_REGIONS:
   if at in (0x7D7000,0x7F6000):self.uc.mem_protect(at,n,UC_PROT_READ|UC_PROT_WRITE)
   else:self.uc.mem_map(at,n)
  self.uc.mem_write(TASK,bytes(self.uc.mem_read(0x12700000,0x190)))
  self.uc.mem_write(VM,bytes(0x9400));self.uc.mem_write(SCRIPT,(ROOT/SCRIPT_PATH).read_bytes())
  for at,v,f in declarations(c):self.put(at,v,f)
  self.mutable += [(VM,VM+0x9400),(0x7A4E18,0x7A4E20),(WORK,WORK+3),(TASK+0x43,TASK+0x60),(TASK+0x174,TASK+0x178),
   (CTRL+0x115CBA,CTRL+0x115CEC),(CTRL+0x108B3B,CTRL+0x108B3D)]+[(VM+0x446+j*0xAB8,VM+0x448+j*0xAB8) for j in range(14,56)]
  self.calls=[];self.pending=[];self.returns=set();self.api_trace=[];self.tick_inputs=tick_inputs;self.tick_index=0
  self.code_trace=[];self.original_write_trace=[];self.commands=[];self.active=False
  self.kernel=ctypes.WinDLL('kernel32',use_last_error=True)
  self.kernel.lstrcmpA.argtypes=[ctypes.c_char_p,ctypes.c_char_p];self.kernel.lstrcmpA.restype=ctypes.c_int
  self.kernel.GetTickCount.argtypes=[];self.kernel.GetTickCount.restype=ctypes.c_uint32
  self.instructions=0;self.writes=0;self.code_hash=hashlib.sha256();self.write_hash=hashlib.sha256()

 def image_identity(self):
  source=SOURCE.read_bytes();out={}
  for label,at,n in [('code',0x401000,0x191000),('IAT_page',0x592000,0x1000)]:
   b=bytes(self.uc.mem_read(at,n));need(b==source[at-0x400000:at-0x400000+n],'original '+label+' bytes unchanged');out[label]=dict(pointer=at,bytes=n,sha256=sha(b))
  return out

 def selected_state(self):
  return dict(task=bytes(self.uc.mem_read(TASK,0x190)).hex(),records=[bytes(self.uc.mem_read(RECORD+i*256,256)).hex() for i in (0,1)],
   counters=bytes(self.uc.mem_read(CTRL+0x2EF14,0x31)).hex(),remaining=self.get(CTRL+0x2E6F4,'i'),elapsed=self.get(CTRL+0x2E6F8,'i'),
   result=bytes(self.uc.mem_read(0x7F4000,0x2000)).hex(),work=bytes(self.uc.mem_read(WORK,3)).hex(),VM=bytes(self.uc.mem_read(VM,0x9400)).hex())

 def string(self,at):
  b=bytearray()
  for i in range(4096):
   v=self.get(at+i,'B')
   if v==0:return bytes(b)
   b.append(v)
  raise ValueError('bounded original API string')

 def code(self,uc,at,size,context):
  if at in APIS:
   name,n,ret=APIS[at];sp=uc.reg_read(UC_X86_REG_ESP);need(self.get(sp)==ret,'exact original terminal API caller');args=[self.get(sp+4+j*4) for j in range(n)]
   if name=='lstrcmpA':
    strings=[self.string(p) for p in args];value=self.kernel.lstrcmpA(*strings);extra=dict(strings=[s.hex() for s in strings],actual_API_executed=True)
   else:
    if self.tick_inputs is None:value=int(self.kernel.GetTickCount());extra=dict(actual_API_executed=True)
    else:
     need(self.tick_index<len(self.tick_inputs),'captured tick available');value=self.tick_inputs[self.tick_index];extra=dict(actual_API_executed=False,captured_platform_input=True)
    self.tick_index+=1
   self.api_trace.append(dict(name=name,args=args,result=value,caller=ret,**extra));uc.reg_write(UC_X86_REG_EAX,value&0xFFFFFFFF);uc.reg_write(UC_X86_REG_ESP,sp+4+n*4);uc.reg_write(UC_X86_REG_EIP,ret);return
  super().code(uc,at,size,context)
  if not self.active:return
  if at!=0x12100000:self.code_trace.append(at)
  if at==0x4CE8F0 and self.get(VM+4,'B') and not self.get(VM+0x93E2,'B') and self.get(VM+0x20,'H')==0:
   instruction=self.get(VM+0x10)+self.get(VM+0x1C);need(SCRIPT<=instruction<SCRIPT+len((ROOT/SCRIPT_PATH).read_bytes())-3,'source condition VM instruction')
   opcode,advance=struct.unpack('<HH',uc.mem_read(instruction,4));self.commands.append(dict(pointer=instruction,opcode=opcode,advance=advance,pc=self.get(VM+0x1C),work=bytes(uc.mem_read(WORK,3)).hex()))
  sp=uc.reg_read(UC_X86_REG_ESP)
  while self.pending and (at,sp)==(self.pending[-1]['caller'],self.pending[-1]['return_ESP']):
   e=self.pending.pop();e.update(result=uc.reg_read(UC_X86_REG_EAX),after=self.selected_state(),cpu_after=self.cpu())
  if at in OBSERVED:
   n=OBSERVED[at];e=dict(entry=at,receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(n)],return_ESP=sp+4+n*4,before=self.selected_state(),cpu_before=self.cpu())
   self.calls.append(e);self.pending.append(e);self.returns.add(e['caller'])

 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.active:self.original_write_trace.append(dict(pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))

 def run(self):
  initial=self.snapshot();image_before=self.image_identity();self.active=True
  try:
   before=self.selected_state();event=self.call(0x432100);after=self.selected_state()
   need(len(self.pending)==1 and self.pending[0]['entry']==0x432100,'only original root awaits until-address observation')
   root=self.pending.pop();need((self.cpu()['EIP'],self.cpu()['ESP'])==(root['caller'],root['return_ESP']),'actual event root return boundary')
   root.update(result=self.cpu()['EAX'],after=after,cpu_after=self.cpu())
   result_before=self.selected_state();finalization=self.call(0x473860);result_after=self.selected_state();need(not self.pending,'all original result contracts returned')
  except Exception as error:
   self.failure=dict(error=str(error),CPU=self.cpu(),state=self.selected_state(),calls=self.calls[-12:],instructions=self.instructions,writes=self.original_write_trace[-64:],original_PC_trace_tail=self.code_trace[-64:]);raise
  finally:self.active=False
  need(self.tick_inputs is None or self.tick_index==len(self.tick_inputs),'all captured time inputs consumed')
  return dict(input=self.terminal_input,parent_case=next(r for r in accepted()['source_cases'] if r['name']==self.terminal_input['combat']),declarations=[dict(address=a,value=v,format=f) for a,v,f in declarations(self.terminal_input)],image_before=image_before,image_after=self.image_identity(),
   initial=initial,event=dict(before=before,call=event,after=after),finalization=dict(before=result_before,call=finalization,after=result_after),final=self.snapshot(),calls=self.calls,APIs=self.api_trace,
   commands=self.commands,code_trace=self.code_trace,write_trace=self.original_write_trace,instructions=self.instructions,writes=self.writes,code_trace_sha256=self.code_hash.hexdigest(),write_trace_sha256=self.write_hash.hexdigest(),
   game_function_results_stubbed=False,OS_input_submitted=False,derived_host_writes_after_first_root=False,original_outer_scheduler_connected=False)


def save(path,data):
 p=ROOT/path;need(not p.exists(),'fresh terminal evidence path');raw=(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode()
 p.write_bytes(gzip.compress(raw,mtime=0) if p.suffix=='.gz' else raw)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case');a=p.parse_args();cs=[c for c in corpus() if a.case is None or c['name']==a.case];need(bool(cs),'known terminal cases');rows=[]
 for c in cs:
  m=TerminalMachine(c)
  try:r=m.run()
  except Exception:
   if hasattr(m,'failure'):save(a.out+'.failure.json.gz',dict(accepted=False,input=c,source_contract=source_contract(),failure=m.failure))
   raise
  rows.append(r);print(c['name'],r['instructions'],r['event']['after']['task'][0x174*2:0x178*2],flush=True)
 save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
