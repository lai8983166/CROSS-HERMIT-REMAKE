"""Continue frame sprite bodies and rectangle prefix to the real null-owner read boundary."""
import argparse,gzip,hashlib,pickle,struct
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_ECX
from tools.school_vm_graphics import *
from tools.school_vm_draw_emulation import DrawEmulator,report_text,architectural_cpu
from tools.school_world_life_codec import pack

class GraphicsEmulator(DrawEmulator):
 def draw_regions(self):return [dict(pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for a,n in REGIONS]

 def _hook(self,uc,address,size,context):
  if self.draw_loading:
   sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX)
   if address==self.draw_stop:
    if self.graphics_phase=='rectangle':
     c=dict(va=hex(address),return_va=hex(self.read(sp)),sp=sp,receiver=recv,args=[self.read(sp+4+i*4) for i in range(4)]);self.draw_calls.append(c);self.graphics_pending=dict(**c,first_instruction_executed=False)
    elif self.graphics_phase=='owner_read':self.graphics_read=dict(va=hex(address),base_register='ECX',base=recv,offset=0xB278,effective_address=(recv+0xB278)&0xFFFFFFFF,bytes=4,instruction_executed=False,target_read=False,requires_original_renderer_initialization=True)
    uc.emu_stop();return
   if address==0x407AD0:self.graphics_packets.append(dict(pointer=recv,bytes=128,hex=bytes(uc.mem_read(recv,128)).hex(),seh=self.read(0)))
   if address in (0x4CA711,0x4CBEF6,0x4CD8CB):self.draw_returns.append(dict(va=hex(address),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX),ecx=recv))
  return super()._hook(uc,address,size,context)

 def graphics_cpu(self):
  c=architectural_cpu(self.uc);return {k:c[k] for k in ('EIP','ESP','EBP','EAX','ECX')}

 def run_graphics(self,phase):
  ptr=self.read(TACT+0x64);tex=self.read(BANK);table=bytes(self.uc.mem_read(FRAME,50));inputs=dict(script_pointer=ptr,script_sha256=SCRIPT_SHA,driver='continuous_original_graphics_VM_task',texture_record=dict(pointer=tex,bytes=84,hex=bytes(self.uc.mem_read(tex,84)).hex()),frame_table=dict(pointer=FRAME,bytes=50,hex=table.hex(),rows=[list(struct.unpack_from('<6h',table,i*12)) for i in range(4)]),manager_owner=self.read(MANAGER))
  if self.graphics_cpu()!=cpu_expected(PREVIOUS.get(phase,'parent'),inputs) or self.read(0x7A49FC)!=TASK or self.read(0x7A49F8)!=WORK or bytes(self.uc.mem_read(ptr,SCRIPT.stat().st_size))!=SCRIPT.read_bytes():raise RuntimeError('VM graphics original retained CPU/owners/script required')
  before=self.draw_regions();expected=project(phase,inputs,before);self.draw_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];retained=self.capture_scene_memory(self.draw_allowed);self.draw_args={int(r['va'],16):r['args'] for r in source_contract()['functions']};self.draw_entries=set(self.draw_args);self.draw_ranges=native_ranges();self.draw_stop=STOP[phase];self.draw_calls=[];self.draw_returns=[];self.draw_visited=set();self.graphics_phase=phase;self.graphics_packets=[];self.graphics_pending=None;self.graphics_read=None;prior=self._function_ranges;self._function_ranges=prior+self.draw_ranges;self.draw_loading=True
  try:
   self.uc.emu_start(START[phase],RETURN,timeout=10_000_000,count=100000);after=self.draw_regions();cpu=self.graphics_cpu();packet=dict(pointer=positions()['packet'],bytes=128,hex=bytes(self.uc.mem_read(positions()['packet'],128)).hex()) if phase=='graphics' else None
   if after!=expected['after'] or cpu!=expected['CPU'] or packet!=expected['packet'] or self.graphics_packets!=expected['packets'] or self.graphics_pending!=expected['pending'] or self.graphics_read!=expected['blocked_read']:
    bad=[hex(a['pointer']) for a,b in zip(after,expected['after']) if a!=b];raise RuntimeError('VM graphics source/native '+phase+' '+repr(bad)+' CPU '+repr(cpu)+' expected '+repr(expected['CPU'])+' packets '+repr(self.graphics_packets)+' expected '+repr(expected['packets']))
   return dict(phase=phase,inputs=inputs,before=before,**expected,calls=self.draw_calls,returns=self.draw_returns,visited=sorted(self.draw_visited),owned_bodies_stubbed=False,platform_adapters=[],debug_stack_check_adapter=True,new_root_calls=0,**self.verify_scene_memory(retained))
  finally:self.draw_loading=False;self._function_ranges=prior

 def save_graphics(self,name,phase,parent_sha):
  p=ROOT/f'.venv-audit/vm-graphics-{phase}-{name}.pkl'
  if p.exists():raise ValueError('VM graphics immutable fresh checkpoint required')
  payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=parent_sha,case_name=name,phase=phase,evidence_kind='private_original_vm_graphics_'+phase,pending_eip=self.uc.reg_read(UC_X86_REG_EIP),state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith(('_audit_','draw_','graphics_'))},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save());raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);p.write_bytes(raw);return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(payload['pending_eip']),runtime_or_original_save=False)

def restore(payload):
 e=GraphicsEmulator();e.__dict__.update(payload['state'])
 for at,buf in payload['memory']:
  if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
  e.uc.mem_write(at,buf)
 e.uc.context_restore(payload['cpu']);return e

def generate(phases):
 from tools.school_vm_graphics_verification import load_verified_checkpoint,PARENT,PARENT_SHA,REPORTS
 from tools.school_vm_character_verification import load_verified_checkpoint as parent_loader
 engines={};cps={};first=phases[0]
 for name in ('initial','student9_waiting','fifth_class'):
  payload,cp=parent_loader(name,'layer_entry') if first=='graphics' else load_verified_checkpoint(name,PREVIOUS[first]);engines[name]=restore(payload);cps[name]=cp
 for phase in phases:
  path=REPORTS[phase]
  if path.exists():raise ValueError('VM graphics immutable report exists')
  rows=[]
  for name,e in engines.items():
   a=e.run_graphics(phase);rows.append(dict(name=name,prior_checkpoint=cps[name],actual=pack(a)));print(name+': native '+phase+' full source packets/state/CPU verified',flush=True)
  for c in rows:c['continuation_checkpoint']=engines[c['name']].save_graphics(c['name'],phase,PARENT_SHA);cps[c['name']]=c['continuation_checkpoint']
  r=dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=rows,queue_executed=False,clipping_returned=False,GPU_executed=False,dialogue_executed=False,VM_returned=False,task_returned=False,full_outer_frame_executed=False,persistent_write_authority=False,new_root_calls=0);path.write_bytes(gzip.compress(report_text(r).encode('utf-8'),compresslevel=6,mtime=0));print('Wrote '+path.name,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--phase',choices=PHASES);g.add_argument('--all',action='store_true');a=p.parse_args();generate(PHASES if a.all else (a.phase,))
