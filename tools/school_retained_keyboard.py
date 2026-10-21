"""Offline original-task continuation driven by pinned native keyboard captures.

No process launch, window action, OS input or new native rendering occurs here.
Recorded platform outputs are replayed only under their original empty-input
preconditions. Every game instruction runs from the pinned original image.
"""
import copy,gzip,hashlib,json,struct
from functools import lru_cache
from collections import Counter
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools.school_task_frame_verification import TaskReplay,INPUT,IME_SLOT
from tools.school_vm_graphics_verification import load_verified_checkpoint
from tools.school_retained_render_pipeline import VM,ROOT_RETURN
from tools.school_retained_rendering_verification import ROOT,SOURCE,BASE,SOURCE_SHA256,need,sha,word,canonical
from tools.school_renderer_init_emulation import REGISTERS
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_native_dialogue_verification import predict_keyboard

KEYBOARD=0x10010b8
STACK=0x21000000
PINS={
 'analysis/school-task-frame-acceptance-v1-20261021.json':'1c935c644cb114f0ee24eea374a9efef98ad024428221775f8508d6bfb2aecac',
 'analysis/school-native-dialogue-acceptance-v1-20261022.json':'54d126f535ec9d0ff55968121bcb48423ac589e8bfcd3f49c202b025d81c05d8',
}

def pinned(path,digest):
 b=(ROOT/path).read_bytes();need(sha(b)==digest,'pinned evidence '+path);return b


def inputs():
 need(sha(SOURCE.read_bytes())==SOURCE_SHA256,'original source image')
 task,native=[json.loads(pinned(p,h)) for p,h in PINS.items()]
 parents={}
 for c in task['cases']:
  b=pinned(c['report'],c['report_sha256']);name=json.loads(gzip.decompress(b))['case']['name']
  parents[name]=dict(path=c['report'],sha256=c['report_sha256'])
 manifest={r['path']:r['sha256'] for r in native['artifact_manifest']};streams={}
 from tools.school_native_dialogue_handoff_verification import verify
 for c in native['native_cases']:
  b=pinned(c['report'],manifest[c['report']]);r=json.loads(gzip.decompress(b));checked=verify(r,require_transition=True);h=r['case']['probe']['input_handoff'];indices=[0,checked['derived_boundary']['press_index'],checked['derived_boundary']['release_index']]
  captures=[]
  for label,index in zip(('idle','press','release'),indices):
   body=bytes.fromhex(h['samples'][index]['input']['hex']);raw=body[12:268]
   need(len(raw)==256 and [(i,v) for i,v in enumerate(raw) if v]==([(57,128)] if label=='press' else []),'source captured device bytes')
   captures.append(dict(label=label,index=index,keyboard_sha256=sha(body),raw_device_hex=raw.hex()))
  streams[c['scene']]=dict(report=c['report'],report_sha256=sha(b),independent_proof=c['independent_proof'],captures=captures)
 need(set(parents)=={'initial','student9_waiting','fifth_class'} and set(streams)=={76,77},'three retained cases and two native streams')
 return dict(source_sha256=SOURCE_SHA256,acceptance_pins=PINS,parents=parents,streams=streams,mode='offline recorded platform and captured device replay; no new OS input or GPU')


def memory_rows(u):
 return [dict(pointer=a,bytes=b-a+1,sha256=sha(bytes(u.mem_read(a,b-a+1)))) for a,b,_ in u.mem_regions()]


@lru_cache(maxsize=3)
def prefix(name,path,digest):
 c=json.loads(gzip.decompress(pinned(path,digest)))['case'];need(c['name']==name,'parent logical case')
 payload,cp=load_verified_checkpoint(name,'rectangle');runner=TaskReplay(c,payload);count=steps=0
 for step in c['steps']:
  if step['label']=='original_BeginScene_Clear_states':break
  count+=runner.step(step);steps+=1
 need(runner.read(VM+28,8)==struct.pack('<IHH',248,1,50),'retained complete-task text wait')
 memory=tuple((a,bytes(runner.u.mem_read(a,b-a+1))) for a,b,_ in runner.u.mem_regions())
 return memory,runner.u.context_save(),dict(parent=dict(path=path,sha256=digest),checkpoint=cp,steps=steps,original_instructions_replayed=count,full_memory=memory_rows(runner.u),architectural_cpu=architectural_cpu(runner.u))


class Guest:
 def __init__(self,restored):
  memory,cpu,self.provenance=restored;self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.source=SOURCE.read_bytes()
  for at,b in memory:self.u.mem_map(at,len(b));self.u.mem_write(at,b)
  self.u.context_restore(cpu);self.steps=[];self.bindings=[]
 def read(self,at,n=4):return bytes(self.u.mem_read(at,n))
 def cpu(self):return {k:self.u.reg_read(r) for k,r in REGISTERS.items()}
 def state(self):
  b=self.read(VM+28,8);pc,wait,op=struct.unpack('<IHH',b)
  return dict(PC=pc,wait=wait,opcode=op,space_current=self.read(KEYBOARD+0x4b9,1)[0],IME_request=self.read(INPUT+0x630,1)[0])
 def execute(self,label,stop,kind='task'):
  before=self.cpu();counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;apis=[]
  def code(u,at,n,_):
   if at==stop:u.emu_stop();return
   if at>=0x592000:
    sp=u.reg_read(REGISTERS['ESP']);ret=word(self.read(sp));arg=word(self.read(sp+4))
    if at==word(self.read(IME_SLOT)):
     need(ret==0x425c99 and arg==word(self.read(INPUT+8))==0,'recorded null IMM input')
     name='ImmGetOpenStatus';slot=IME_SLOT
    else:
     from tools.school_font_raster_emulation import IMPORTS
     slots=[slot for slot,(name,caller,pop) in IMPORTS.items() if name=='lstrlenA'];need(len(slots)==1,'source string import');slot=slots[0];name='lstrlenA'
     need(at==word(self.read(slot)) and ret==0x425a7e and self.read(arg,1)==bytes(1),'recorded empty input string query')
    apis.append(dict(name=name,import_slot=slot,target=at,sp=sp,return_va=ret,args=[arg],result=0,origin='frozen complete-task platform output under identical null/empty input; not a fresh OS call'))
    u.reg_write(REGISTERS['EAX'],0);u.reg_write(REGISTERS['ESP'],sp+8);u.reg_write(REGISTERS['EIP'],ret);return
   need(BASE<=at<0x592000 and self.read(at,n)==self.source[at-BASE:at-BASE+n],'original game instruction identity')
   counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not BASE<=at<0x592000,'no original code writes')
   if kind=='keyboard':need(KEYBOARD<=at and at+n<=KEYBOARD+0xa00 or STACK<=at and at+n<=STACK+65536,'keyboard fragment finite writes')
   writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.emu_start(before['EIP'],0,count=2000000,timeout=120000000)
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.u.reg_read(REGISTERS['EIP'])==stop,'natural declared source boundary')
  r=dict(label=label,kind=kind,before_cpu=before,cpu=self.cpu(),boundary=stop,instruction_counts=[dict(va=a,count=n) for a,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),platform_replays=apis,state=self.state());self.steps.append(r);return r
 def root(self,label,va,receiver,stop=ROOT_RETURN):
  sp=STACK+0xf000;self.u.mem_write(sp,struct.pack('<I',ROOT_RETURN))
  for k,v in dict(EIP=va,ESP=sp,ECX=receiver,EFLAGS=0x202).items():self.u.reg_write(REGISTERS[k],v)
  r=self.execute(label,stop);r['root']=dict(va=va,receiver=receiver,sp=sp,return_va=ROOT_RETURN);return r
 def frame(self,label,stop=ROOT_RETURN):
  self.root(label+'_IME',0x425de0,INPUT)
  for va in (0x40db90,0x40dc80):self.root(label+'_queue_'+hex(va),va,0x1001058)
  r=self.root(label,0x454cf0,0xe000000,stop)
  if stop==ROOT_RETURN:need(r['cpu']['EAX']==0 and r['cpu']['ESP']==STACK+0xf004,'complete original task natural return')
  return r
 def capture(self,capture):
  raw=bytes.fromhex(capture['raw_device_hex']);need(len(raw)==256,'captured full device extent');before=self.read(KEYBOARD,0xa00);bound=bytearray(before);bound[12:268]=raw
  self.u.mem_write(KEYBOARD+12,raw);bp=STACK+0xf800;self.u.mem_write(bp-4,struct.pack('<I',KEYBOARD))
  for k,v in dict(EIP=0x4113d5,EBP=bp,ESP=bp-0x70,EFLAGS=0x202).items():self.u.reg_write(REGISTERS[k],v)
  r=self.execute('captured_'+capture['label'],0x4116a4,'keyboard');after=self.read(KEYBOARD,0xa00)
  need(after==predict_keyboard(bytes(bound)),'independent entire original keyboard update')
  binding=dict(capture=copy.deepcopy(capture),only_device_output_written=dict(pointer=KEYBOARD+12,bytes=256),before_hex=before.hex(),bound_hex=bound.hex(),after_hex=after.hex(),step_index=len(self.steps)-1)
  self.bindings.append(binding);return binding


def continue_case(name,scene,contract):
 parent=contract['parents'][name];g=Guest(prefix(name,parent['path'],parent['sha256']));stream=contract['streams'][scene]
 g.capture(stream['captures'][0]);readiness=[]
 for i in range(80):
  s=g.frame('readiness_'+str(i))['state'];readiness.append(s)
  if (s['PC'],s['wait'],s['opcode'])==(252,1,51):break
 else:raise ValueError('source text readiness and confirmation limit')
 controls=[g.frame('no_input_control_'+str(i))['state'] for i in range(2)]
 need(all((s['PC'],s['wait'],s['opcode'],s['space_current'])==(252,1,51,0) for s in controls),'held confirmation under no input')
 g.capture(stream['captures'][1]);confirmed=g.frame('captured_space_confirmation')['state'];need((confirmed['PC'],confirmed['wait'],confirmed['opcode'])==(252,0,51),'original complete task consumes captured space')
 g.capture(stream['captures'][2]);need(g.state()['space_current']==0,'original keyboard release')
 g.frame('next_original_task_handler_boundary',0x4c61c0);sp=g.cpu()['ESP'];args=[word(g.read(sp+4+4*i)) for i in range(3)]
 need(g.cpu()['ECX']==VM and args==[0,word(g.read(0xe000064))+704,1] and word(g.read(sp))==0x4ceda7,'next opcode30 original natural stack')
 return dict(name=name,scene_capture=scene,parent_replay=g.provenance,stream=stream,bindings=g.bindings,readiness=readiness,no_input_controls=controls,confirmation=confirmed,next_handler=dict(va=0x4c61c0,args=args,return_va=word(g.read(sp)),sp=sp,first_instruction_executed=False,state=g.state()),steps=g.steps,final_memory=memory_rows(g.u),final_architectural_cpu=architectural_cpu(g.u))


def run():
 contract=inputs();cases=[]
 for name in ('initial','student9_waiting','fifth_class'):
  for scene in (76,77):
   cases.append(continue_case(name,scene,contract));print(name,scene,'captured source keyboard -> complete task confirmation -> opcode30 boundary',flush=True)
 return dict(schema_version=1,contract=contract,cases=cases,new_OS_input=False,new_GPU_or_window=False,independent_VM_roots=0,original_outer_scheduler=False,full_world_loop=False,R3_complete=False,Godot_changed=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable output required')
 result=run();out.write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0));print('offline retained keyboard report bytes',out.stat().st_size,flush=True)
