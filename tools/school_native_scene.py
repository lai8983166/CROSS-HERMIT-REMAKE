"""Original MAIN event/factory/CRT scene loop in an isolated full runtime copy."""
import ctypes as C,ctypes.wintypes as W,gzip,hashlib,json,struct,time,types
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools import school_scene_bootstrap as previous

parent=previous.parent;original=parent.original
ROOT=previous.ROOT;SOURCE=previous.SOURCE;SOURCE_SHA=previous.SOURCE_SHA
RUNTIME=ROOT/'.venv-audit/scene-callback-runtime'
APP=RUNTIME/'CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
INSTALLED=ROOT/'CROSS HERMIT/CROSS HERMIT'
SIZE=previous.SIZE;VM=0x7d7c28
RANGES=previous.RANGES+((0x4e1b60,0x4e1c63),(0x49e930,0x49f570),(0x4da860,0x4dab50),(0x439e30,0x439ef0),(0x49dfd1,0x49e834),(0x451b10,0x4539b0),(0x4ce8f0,0x4d03b7),(0x46b470,0x46b663))
IAT=previous.IAT
need=previous.need;sha=previous.sha;word=previous.word
image_name=original.bind('QueryFullProcessImageNameW',W.BOOL,[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)])

def cdecl_thunk():return parent.call_thunk().replace(bytes.fromhex('8b4e04ff16'),bytes.fromhex('8b4e04ff1683c404'))

def source_contract():
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA,'original source SHA');md=Cs(CS_ARCH_X86,CS_MODE_32)
 checks={0x4e1bb4:('call','0x4e1be0'),0x4e1c4b:('call','0x49e930'),0x4da87e:('call','0x4da8a0'),0x448b18:('add','esp, 4'),0x46330e:('call','0x4da860'),0x46331e:('add','ecx, 0x10'),0x463321:('call','0x439e30'),0x439eac:('mov','dword ptr [ecx + 0x20], edx'),0x439eb2:('mov','dword ptr [eax + 0x1c], 1'),0x49e39e:('call','0x451080'),0x49e4b8:('call','0x49e540'),0x49e60f:('call','0x4217c0'),0x4510ee:('mov','dword ptr [0x7a4174], ecx'),0x451148:('call','0x4216c0'),0x421f88:('call','dword ptr [eax]'),0x4516d0:('call','0x422360'),0x451ab7:('call','0x4539b0'),0x4539ec:('call','0x454cf0'),0x453a0c:('call','0x46b470'),0x453cb0:('call','0x422360'),0x454d8b:('call','0x4ce8f0'),0x46b49a:('movsx','ecx, word ptr [eax + 0x108b32]'),0x4220dd:('call','dword ptr [0x592260]')}
 rows=[]
 for at,want in checks.items():
  i=next(md.disasm(raw[at-0x400000:at-0x400000+16],at));need((i.mnemonic,i.op_str)==want,'native scene operand '+hex(at));rows.append(dict(va=at,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 need(word(raw,0x49e4d3-0x400000+16*4)==0x49e39e,'actual scene event16 dispatch')
 return dict(source_sha256=SOURCE_SHA,ranges=[dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES],IAT_slots=list(IAT),instructions=rows,cdecl_thunk_hex=cdecl_thunk().hex(),source_scenarios=[76,77],event=16,thread_vtable=0x59a430,callback=0x451670,VM=VM,retained_checkpoint_rehydrated=False,physical_input_injected=False,complete_native_instruction_or_API_trace=False)

def hash_file(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def runtime_audit():
 private=APP.parent.resolve();need(ROOT.resolve() in private.parents and '.venv-audit' in private.parts and private!=INSTALLED.resolve(),'bounded private runtime root')
 files=[];writable=[]
 for source in sorted(p for p in INSTALLED.rglob('*') if p.is_file()):
  rel=source.relative_to(INSTALLED);target=private/rel;need(target.is_file() and not source.samefile(target),'separate complete private runtime file '+str(rel))
  mutable=rel.parts[0].upper()=='SAVEDATA' or rel.name.upper()=='OPTION.BIN'
  if mutable:writable.append(dict(path=rel.as_posix(),original_sha256=hash_file(source),private_sha256=hash_file(target)));continue
  a=hash_file(source);b=hash_file(target);need(a==b and source.stat().st_size==target.stat().st_size,'identical private immutable asset '+str(rel));files.append(dict(path=rel.as_posix(),bytes=source.stat().st_size,sha256=a))
 source_names={p.relative_to(INSTALLED).as_posix() for p in INSTALLED.rglob('*') if p.is_file()}
 extras=[p.relative_to(private).as_posix() for p in private.rglob('*') if p.is_file() and p.relative_to(private).as_posix() not in source_names and p.relative_to(private).parts[0].upper()!='SAVEDATA']
 need(not extras,'no unexpected private non-save files');need(files and any(f['path']=='CROSS HERMIT.EXE' for f in files),'complete private source executable')
 return dict(private_root=private.relative_to(ROOT).as_posix(),installed_root=INSTALLED.relative_to(ROOT).as_posix(),immutable_files=files,immutable_bytes=sum(f['bytes'] for f in files),separate_file_identity_verified=True,private_writable_files=writable,installed_files_written=False)

class OwnedRuntime(original.OwnedOriginal):pass
OwnedRuntime.start=types.FunctionType(original.OwnedOriginal.start.__code__,dict(original.OwnedOriginal.start.__globals__,ROOT=RUNTIME),'start_owned_runtime_copy')

class NativeSceneCalls(previous.SceneCalls):
 def __init__(self,pid,owned,scene):
  need(scene in (76,77),'source selected scenarios only');self.scene=scene;super().__init__(pid,owned)
  name=C.create_unicode_buffer(32768);n=W.DWORD(len(name));original.check(image_name(self.h,0,name,C.byref(n)),'actual private executable image name');need(Path(name.value).resolve()==APP.resolve(),'actual owned process must run private source copy');self.process_image=name.value
  self.standard_code=self.code;self.cdecl_code=self.reserve(4096);self.put(self.cdecl_code,cdecl_thunk());old=W.DWORD();original.check(parent.protect(self.h,self.cdecl_code,4096,0x20,C.byref(old)),'private cdecl bridge RX');original.check(parent.flush(self.h,self.cdecl_code,len(cdecl_thunk())),'private cdecl cache')
  self.main=word(self.get(0x7a4a00,4));need(self.main and word(self.get(self.main,4))==0x5986a0,'actual original MAIN owner');self.phase=0
 def validate(self,va,receiver,args):
  need(self.pid in self.owned.members(),'only owned native runtime process')
  protocol=((0x4e1b60,0,()),(0x4da860,0,(self.scene,)),(0x439e30,self.main+0x10,(16,)))
  need(self.phase<len(protocol) and (va,receiver,args)==protocol[self.phase],'only ordered exact initializer/scenario/MAIN event roots')
 def call(self,va,receiver,args=(),slot=0):
  self.code=self.cdecl_code if va==0x4da860 else self.standard_code
  result=super().call(va,receiver,args,slot);self.phase+=1;return result

def identity(c):
 raw=SOURCE.read_bytes();code=[]
 for a,b in RANGES:
  value=c.get(a,b-a);need(value==raw[a-0x400000:b-0x400000],'live native scene source');code.append(dict(pointer=a,bytes=b-a,sha256=sha(value)))
 return dict(code=code,IAT=[dict(slot=a,hex=c.get(a,4).hex()) for a in IAT])

def has(frames,at):return any(any(r['return_va']==at for r in f['chain']) for f in frames)

class ScriptBoundary:
 def __init__(self):self.started=None;self.PCs=set()
 def observe(self,head,vm,now):
  active=bool(head[0x43] and head[0x44]==2 and head[0x59] and vm[4] and word(vm,28)>0)
  if not active:return False,False
  self.PCs.add(word(vm,28))
  if self.started is None:self.started=now
  return True,now-self.started>=.5 and len(self.PCs)>=2

def run_case(scene):
 owners=[];results=[];worker_handles=[]
 def own():x=OwnedRuntime();owners.append(x);return x
 def probe(pid,owned):
  c=NativeSceneCalls(pid,owned,scene);r=dict(scene=scene,main=c.main,process_image=c.process_image,allocations=[dict(pointer=a,bytes=n) for a,n in c.blocks],source_before=identity(c),samples=[],full_objects=[],error=None);results.append(r)
  try:
   need(word(c.get(0x7a4174,4))==0,'fresh original scene publication');r['scenario_before_hex']=c.get(0x7f4488,80).hex();c.call(0x4e1b60,0);r['scenario_before_selection_hex']=c.get(0x7f4488,80).hex();c.call(0x4da860,0,(scene,));r['scenario_selected_hex']=c.get(0x7f4488,80).hex()
   event_before=c.get(c.main+0x2c,8);need(word(event_before)==0,'no pending original MAIN event');r['event_before_hex']=event_before.hex();c.call(0x439e30,c.main+0x10,(16,))
   window=original.findwindow(b'Cross Hermit',None);owner=W.DWORD();main_tid=original.ownerpid(window,C.byref(owner));need(owner.value==pid,'owned native window thread')
   deadline=time.monotonic()+30;loop_started=None;boundary=ScriptBoundary();worker=None;node_seen=None
   while time.monotonic()<deadline and len(r['samples'])<1600:
    node=word(c.get(0x7a4174,4));initial=c.get(node,48) if node else bytes(48);tid=word(initial,0x24) if word(initial,4)&1 else 0
    tids=[main_tid]+([tid] if tid and tid!=main_tid else [])
    with original.frozen(c.h,pid,tids) as frames:
     node=word(c.get(0x7a4174,4));row=dict(index=len(r['samples']),elapsed=owned.elapsed(),frames=frames,scene_global=node,main_event_hex=c.get(c.main+0x2c,8).hex(),manager_heads_hex=c.get(c.main+0x64,256).hex(),VM_hex=c.get(VM,128).hex(),registered_tasks=[])
     heads=bytes.fromhex(row['manager_heads_hex'])
     for bucket in range(32):
      task=word(heads,bucket*8);seen=set()
      while task:
       need(task not in seen and len(seen)<128,'bounded original registered graph');seen.add(task);task_head=c.get(task,48);row['registered_tasks'].append(dict(bucket=bucket,pointer=task,head_hex=task_head.hex()));task=word(task_head,12)
     done=False
     if node:
      head=c.get(node,0x200);row.update(node_head_hex=head.hex(),world_gate_hex=c.get(node+0x190+0x108b20,80).hex(),first_world_unit_hex=c.get(node+0x190+0x80aec,0x520).hex())
      if not node_seen:node_seen=node
      need(node==node_seen,'same original published scene object')
      thread_id=word(head,0x24);handle=word(head,0x20)
      if handle and thread_id and word(head,4)&1 and worker is None:
       local=W.HANDLE();original.check(parent.duplicate(c.h,handle,parent.current_process(),C.byref(local),0,False,2),'actual original scene worker duplicate');worker=(thread_id,local);worker_handles.append(worker);r['worker']=dict(thread_id=thread_id,remote_handle=handle,event=word(head,0x1c),observed_entry='original421F50 through original_beginthreadex')
      if has(frames,0x453cb5) and head[0x30]==0 and word(head,0x34)==2:
       row['ordinary_scene_loop_wait']=True
       if loop_started is None:loop_started=time.monotonic();r['full_objects'].append(dict(label='first_ordinary_scene_loop',pointer=node,hex=c.get(node,SIZE).hex()))
       vm=bytes.fromhex(row['VM_hex'])
       active,done=boundary.observe(head,vm,time.monotonic())
       if active:
        row['active_original_script']=True
       if active and 'script_file' not in r:
        script=word(head,0x64);header=c.get(script,452);matches=[]
        for candidate in (APP.parent/'DATA/TACTICS/SCRIPT').glob('*.BIN'):
         data=candidate.read_bytes()
         if data[:452]==header:matches.append((candidate,data))
        need(len(matches)==1,'unique loaded original script file identity');candidate,data=matches[0];memory=c.get(script,len(data));need(memory==data,'complete native loaded script bytes equal private source file')
        r['script_file']=dict(path=candidate.relative_to(ROOT).as_posix(),installed_path=(INSTALLED/candidate.relative_to(APP.parent)).relative_to(ROOT).as_posix(),bytes=len(data),sha256=sha(data),loaded_pointer=script,loaded_memory_hex=memory.hex())
       if done:r['full_objects'].append(dict(label='active_script_ordinary_scene_loop',pointer=node,hex=c.get(node,SIZE).hex()))
      if word(head,0x64):
       script=word(head,0x64);row['loaded_script_header']=dict(pointer=script,hex=c.get(script,452).hex())
       vm=bytes.fromhex(row['VM_hex']);pc=word(vm,28);base=word(vm,16)
       if base and pc<0x400000:row['VM_current_bytes']=dict(pointer=base+pc,hex=c.get(base+pc,32).hex())
     r['samples'].append(row)
    if done:break
    time.sleep(.008)
   need(loop_started is not None and boundary.started is not None and len(r['full_objects'])==2 and worker is not None,'actual scene loading must reach ordinary loop and active original script')
   code=W.DWORD();original.check(parent.exit_thread(worker[1],C.byref(code)),'actual scene worker before close');r['worker_before_close']=dict(wait_status=original.wait(worker[1],0),exit_code=code.value);r['source_after']=identity(c);need(r['source_before']==r['source_after'],'unchanged actual source/IAT')
  except Exception as e:r['error']=repr(e);raise
  finally:r.update(calls=c.calls,writes=c.writes,frees=c.close())
  return r
 def post(hwnd,msg,w,l):
  need(msg==16 and len(owners)==1,'only owned normal close boundary');pid=W.DWORD();original.ownerpid(hwnd,C.byref(pid));need(pid.value in owners[0].members(),'own scene close/probe');probe(pid.value,owners[0]);return original.post(hwnd,msg,w,l)
 fn=types.FunctionType(original.observe.__code__,dict(original.observe.__globals__,OwnedOriginal=own,post=post),'observe_native_scene',original.observe.__defaults__)
 lifecycle=fn(False);ended=[]
 for tid,h in worker_handles:
  try:
   status=original.wait(h,5000);code=W.DWORD();original.check(parent.exit_thread(h,C.byref(code)),'actual scene worker after original close');ended.append(dict(thread_id=tid,wait_status=status,exit_code=code.value,callback_natural_return_claimed=False))
  finally:original.close(h)
 observed=bool(results and any(any(has(s['frames'],a) for a in (0x4516d5,0x45170e,0x451716)) for s in results[0]['samples']))
 return dict(scene=scene,probe=results[0] if results else None,lifecycle=lifecycle,worker_after_close=ended,original_scene_callback_executed=observed,source_code_IAT_or_existing_registers_replaced=False,retained_checkpoint_rehydrated=False,physical_input_injected=False,full_native_instruction_or_API_trace=False)

def save(path,result):
 p=ROOT/path;need(not p.exists(),'fresh immutable native scene output');p.write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--scene',required=True,type=int,choices=[76,77]);p.add_argument('--out',required=True);a=p.parse_args()
 if (ROOT/a.out).exists():p.error('fresh immutable path required before native launch')
 contract=source_contract();case=run_case(a.scene);save(a.out,dict(schema_version=1,source_contract=contract,case=case,R3_complete=False));print('original scene',a.scene,'error',case['lifecycle']['error'],'samples',len(case['probe']['samples']) if case['probe'] else 0)
 if case['lifecycle']['error'] or case['probe'] is None:raise SystemExit(1)
