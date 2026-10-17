"""Resume original character command without additional root calls or platform responses."""
import argparse,gzip,hashlib,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_ECX
from tools.school_vm_character import *
from tools.school_vm_draw_emulation import DrawEmulator,report_text,architectural_cpu
from tools.school_world_life_codec import pack

CRITICAL=(0x4C1F26,0x4CC7A5,0x4CC3C0,0x4CC80B,0x4C5FBB,0x4CD8CB)
class CharacterEmulator(DrawEmulator):
 def draw_regions(self):return [dict(pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for a,n in REGIONS]

 def _hook(self,uc,address,size,context):
  if self.draw_loading:
   sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX)
   if address==self.draw_stop and self.char_phase in ('template','layer_entry'):
    n=3 if self.char_phase=='template' else 5;c=dict(va=hex(address),return_va=hex(self.read(sp)),sp=sp,receiver=recv,args=[self.read(sp+4+i*4) for i in range(n)]);self.draw_calls.append(c);self.char_pending=dict(**c,first_instruction_executed=False);uc.emu_stop();return
   if address in CRITICAL:self.draw_returns.append(dict(va=hex(address),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX),ecx=recv))
  return super()._hook(uc,address,size,context)

 def char_cpu(self):
  c=architectural_cpu(self.uc);return {k:c[k] for k in ('EIP','ESP','EBP','EAX','ECX')}

 def run_character(self,phase):
  ptr=self.read(TACT+0x64);tex=self.read(BANK);inputs=dict(script_pointer=ptr,script_sha256=SCRIPT_SHA,driver='continuous_original_character_VM_task',texture_record=dict(pointer=tex,bytes=84,hex=bytes(self.uc.mem_read(tex,84)).hex()),template=dict(pointer=TABLE,bytes=38,hex=bytes(self.uc.mem_read(TABLE,38)).hex(),index=4,layer=7))
  wanted=cpu_expected(PREVIOUS.get(phase,'parent'),inputs)
  if self.char_cpu()!=wanted or bytes(self.uc.mem_read(ptr,SCRIPT.stat().st_size))!=SCRIPT.read_bytes() or self.read(0x7A4A00)!=MAIN or self.read(0x7A49F8)!=WORK or self.read(0x7A49FC)!=TASK:raise RuntimeError('VM character actual original continuation CPU/owners/script')
  before=self.draw_regions();expected=project(phase,inputs,before);self.draw_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];retained=self.capture_scene_memory(self.draw_allowed);self.draw_args={int(r['va'],16):r['args'] for r in source_contract()['functions']};self.draw_entries=set(self.draw_args);self.draw_ranges=native_ranges();self.draw_stop=STOP[phase];self.draw_calls=[];self.draw_returns=[];self.draw_visited=set();self.char_phase=phase;self.char_pending=None;prior=self._function_ranges;self._function_ranges=prior+self.draw_ranges;self.draw_loading=True
  try:
   self.uc.emu_start(START[phase],RETURN,timeout=10_000_000,count=100000);after=self.draw_regions();cpu=self.char_cpu();packet=dict(pointer=layout()['packet'],bytes=128,hex=bytes(self.uc.mem_read(layout()['packet'],128)).hex()) if phase=='overlay' else None
   if after!=expected['after'] or cpu!=expected['CPU'] or packet!=expected['packet'] or self.char_pending!=expected['pending']:
    bad=[(hex(a['pointer']),[(i,x,y) for i,(x,y) in enumerate(zip(bytes.fromhex(a['hex']),bytes.fromhex(b['hex']))) if x!=y][:12]) for a,b in zip(after,expected['after']) if a!=b];raise RuntimeError('VM character source/native '+phase+' '+repr(bad)+' CPU '+repr(cpu)+' expected '+repr(expected['CPU'])+' pending '+repr(self.char_pending))
   return dict(phase=phase,inputs=inputs,before=before,**expected,calls=self.draw_calls,returns=self.draw_returns,visited=sorted(self.draw_visited),owned_bodies_stubbed=False,platform_adapters=[],debug_stack_check_adapter=True,new_root_calls=0,**self.verify_scene_memory(retained))
  finally:self.draw_loading=False;self._function_ranges=prior

 def save_character(self,name,phase,parent_sha):
  p=ROOT/f'.venv-audit/vm-character-{phase}-{name}.pkl'
  if p.exists():raise ValueError('VM character fresh immutable checkpoint required')
  payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=parent_sha,case_name=name,phase=phase,evidence_kind='private_original_vm_character_'+phase,pending_eip=self.uc.reg_read(UC_X86_REG_EIP),state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith(('_audit_','draw_','char_'))},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save());raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);p.write_bytes(raw);return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(payload['pending_eip']),runtime_or_original_save=False)

def restore(payload):
 e=CharacterEmulator();e.__dict__.update(payload['state'])
 for at,buf in payload['memory']:
  if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
  e.uc.mem_write(at,buf)
 e.uc.context_restore(payload['cpu']);return e

def generate(phases):
 from tools.school_vm_character_verification import load_verified_checkpoint,PARENT,PARENT_SHA,REPORTS
 from tools.school_vm_panel_verification import load_verified_checkpoint as parent_loader
 engines={};cps={};first=phases[0]
 for name in ('initial','student9_waiting','fifth_class'):
  payload,cp=parent_loader(name,'character_entry') if first=='template' else load_verified_checkpoint(name,PREVIOUS[first]);engines[name]=restore(payload);cps[name]=cp
 for phase in phases:
  path=REPORTS[phase]
  if path.exists():raise ValueError('VM character immutable report exists')
  rows=[]
  for name,e in engines.items():
   a=e.run_character(phase);rows.append(dict(name=name,prior_checkpoint=cps[name],actual=pack(a)));print(name+': native '+phase+' full source state/CPU verified',flush=True)
  for c in rows:c['continuation_checkpoint']=engines[c['name']].save_character(c['name'],phase,PARENT_SHA);cps[c['name']]=c['continuation_checkpoint']
  r=dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=rows,graphics_list_executed=False,GPU_executed=False,dialogue_executed=False,VM_returned=False,task_returned=False,full_outer_frame_executed=False,persistent_write_authority=False,new_root_calls=0);path.write_bytes(gzip.compress(report_text(r).encode('utf-8'),compresslevel=6,mtime=0));print('Wrote '+path.name,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--phase',choices=PHASES);g.add_argument('--all',action='store_true');a=p.parse_args();generate(PHASES if a.all else (a.phase,))
