"""System-input dialogue observation; original game objects remain read-only to host."""
import ctypes as C,ctypes.wintypes as W,json,struct,time,types,hashlib
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_native_scene import (ROOT,SOURCE,SOURCE_SHA,APP,INSTALLED,SIZE,VM,word,sha,need,
 original,parent,OwnedRuntime,NativeSceneCalls,source_contract,save,has,identity as native_identity)

class VisibleOwnedRuntime(OwnedRuntime):
 def start(self):
  # Same frozen owned launch, explicit normal initial show for targetable OS input.
  app=APP.resolve();need(sha(app.read_bytes())==original.ORIGINAL_SHA,'private executable identity')
  si=original.SI();si.cb=C.sizeof(si);si.flags=1;si.show=1
  original.check(original.create(str(app),None,None,None,False,0x08000004,None,str(app.parent),C.byref(si),C.byref(self.pi)),'visible owned original create')
  self.created=True;original.check(original.assign(self.job,self.pi.process),'visible owned original assign');self.assigned=True
  need(original.resume(self.pi.thread)!=0xffffffff,'visible owned original resume')

INPUT_RANGES=((0x411290,0x411cf0),(0x4128f0,0x412a70),(0x4cce20,0x4cd060))

def identity(c):
 r=native_identity(c);raw=SOURCE.read_bytes();r['input_code']=[]
 for a,b in INPUT_RANGES:
  actual=c.get(a,b-a);need(actual==raw[a-0x400000:b-0x400000],'unchanged original input source');r['input_code'].append(dict(pointer=a,bytes=b-a,sha256=sha(actual)))
 return r

def input_source_contract():
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA,'input source identity');md=Cs(CS_ARCH_X86,CS_MODE_32)
 checks={0x49e78a:('call','0x412a30'),0x412a50:('call','0x411290'),0x412a58:('call','0x411df0'),0x411310:('call','dword ptr [ecx + 0x24]'),0x4113dd:('add','ecx, 0x480'),0x411444:('mov','byte ptr [edx + 0x480], cl'),0x41149b:('mov','byte ptr [eax + 0x580], dl'),0x4114d5:('mov','byte ptr [eax + 0x780], dl'),0x412935:('mov','cl, byte ptr [eax + edx + 0x480]'),0x4ccff2:('call','0x4128f0'),0x4cd028:('call','0x4ccb30')}
 rows=[]
 for at,want in checks.items():
  i=next(md.disasm(raw[at-0x400000:at-0x400000+16],at));need((i.mnemonic,i.op_str)==want,'input operand '+hex(at));rows.append(dict(va=at,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 return dict(source_sha256=SOURCE_SHA,instructions=rows,ranges=[dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in INPUT_RANGES],input_owner_offset=0x10b8,scan_code=0x39,current_offset=0x480,previous_offset=0x380,press_offset=0x580,release_offset=0x780,query=0x4128f0,confirmation_wait=0x4cce20,confirmation_opcode=51,human_physical_input_claimed=False,host_input_object_writes=False)

class DialogueBoundary:
 def __init__(self,notice,observe_only=False):
  self.observe_only=observe_only;self.notice=Path(notice);self.started=None;self.PCs=set();self.wait_pc=None;self.wait_started=None;self.wait_index=None;self.ready_index=None;self.press_index=None;self.release_index=None;self.advanced_index=None;self.finish_started=None
 def observe(self,head,vm,row,now):
  active=bool(head[0x43] and head[0x44]==2 and head[0x59] and vm[4] and word(vm,28)>0)
  if not active:return False,False
  pc=word(vm,28);wait,op=struct.unpack_from('<HH',vm,32);self.PCs.add(pc)
  if self.started is None:self.started=now
  key=bytes.fromhex(row['input']['hex'])[0x480+0x39]&0x80
  if self.ready_index is None:
   if (wait,op)==(1,51) and not key:
    if pc!=self.wait_pc:self.wait_pc=pc;self.wait_started=now;self.wait_index=row['index']
    if now-self.wait_started>=1:
     self.ready_index=row['index'];self.notice.write_text(json.dumps(dict(status='ready',scene_PC=pc,sample=row['index'],game=row['input']['game'],elapsed=row['elapsed'])),encoding='utf8');print('READY',self.notice,'PC',pc,flush=True)
   else:self.wait_pc=None;self.wait_started=None;self.wait_index=None
  elif key and self.press_index is None:self.press_index=row['index'];print('OBSERVED space',pc,wait,op,flush=True)
  if self.press_index is not None:
   if not key and self.release_index is None:self.release_index=row['index']
   if pc!=self.wait_pc and self.advanced_index is None:self.advanced_index=row['index'];self.finish_started=now
  if self.observe_only and self.ready_index is not None:return True,True
  return True,bool(self.advanced_index is not None and self.release_index is not None and now-self.finish_started>=.5)
 def summary(self):return dict(wait_PC=self.wait_pc,no_input_start=self.wait_index,ready_index=self.ready_index,press_index=self.press_index,release_index=self.release_index,advanced_index=self.advanced_index)

def run_case(scene, notice, observe_only=False):
 owners=[];results=[];worker_handles=[]
 def own():x=VisibleOwnedRuntime();owners.append(x);return x
 def probe(pid,owned):
  c=NativeSceneCalls(pid,owned,scene);r=dict(scene=scene,main=c.main,process_image=c.process_image,allocations=[dict(pointer=a,bytes=n) for a,n in c.blocks],source_before=identity(c),samples=[],full_objects=[],error=None);results.append(r)
  try:
   r['initial_main_samples']=[];idle_started=None;idle_deadline=time.monotonic()+5
   while time.monotonic()<idle_deadline:
    now=time.monotonic();state=c.get(c.main+0x2c,8);r['initial_main_samples'].append(dict(elapsed=owned.elapsed(),event_hex=state.hex()))
    if word(state)==0:
     if idle_started is None:idle_started=now
     if now-idle_started>=.25:break
    else:idle_started=None
    time.sleep(.01)
   need(idle_started is not None and time.monotonic()-idle_started>=.25,'original MAIN event must become stably idle')
   need(word(c.get(0x7a4174,4))==0,'fresh original scene publication');r['scenario_before_hex']=c.get(0x7f4488,80).hex();c.call(0x4e1b60,0);r['scenario_before_selection_hex']=c.get(0x7f4488,80).hex();c.call(0x4da860,0,(scene,));r['scenario_selected_hex']=c.get(0x7f4488,80).hex()
   event_before=c.get(c.main+0x2c,8);r['event_before_hex']=event_before.hex();need(word(event_before)==0,'no pending original MAIN event');r['event_before_hex']=event_before.hex();c.call(0x439e30,c.main+0x10,(16,))
   window=original.findwindow(b'Cross Hermit',None);owner=W.DWORD();main_tid=original.ownerpid(window,C.byref(owner));need(owner.value==pid,'owned native window thread')
   deadline=time.monotonic()+180;loop_started=None;boundary=DialogueBoundary(notice,observe_only);worker=None;node_seen=None
   while time.monotonic()<deadline and len(r['samples'])<12000:
    node=word(c.get(0x7a4174,4));initial=c.get(node,48) if node else bytes(48);tid=word(initial,0x24) if word(initial,4)&1 else 0
    tids=[main_tid]+([tid] if tid and tid!=main_tid else [])
    with original.frozen(c.h,pid,tids) as frames:
     node=word(c.get(0x7a4174,4));row=dict(index=len(r['samples']),elapsed=owned.elapsed(),frames=frames,scene_global=node,main_event_hex=c.get(c.main+0x2c,8).hex(),manager_heads_hex=c.get(c.main+0x64,256).hex(),VM_hex=c.get(VM,128).hex(),registered_tasks=[])
     row['wall_time_ns']=time.time_ns();game=word(c.get(0x7a49fc,4));row['input']=dict(game=game,pointer=game+0x10b8,hex=c.get(game+0x10b8,0xa00).hex(),mouse_hex=c.get(game+0x198c,8).hex())
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
       active,done=boundary.observe(head,vm,row,time.monotonic())
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
   if len(r['full_objects'])==1 and boundary.started is not None:
    r['full_objects'].append(dict(label='active_script_ordinary_scene_loop',pointer=node,hex=c.get(node,SIZE).hex()))
   need(loop_started is not None and boundary.started is not None and len(r['full_objects'])==2 and worker is not None,'actual scene loading must reach ordinary loop and active original script')
   code=W.DWORD();original.check(parent.exit_thread(worker[1],C.byref(code)),'actual scene worker before close');r['worker_before_close']=dict(wait_status=original.wait(worker[1],0),exit_code=code.value);r['dialogue_boundary']=boundary.summary();r['source_after']=identity(c);need(r['source_before']==r['source_after'],'unchanged actual source/IAT')
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
 return dict(scene=scene,probe=results[0] if results else None,lifecycle=lifecycle,worker_after_close=ended,original_scene_callback_executed=observed,source_code_IAT_or_existing_registers_replaced=False,retained_checkpoint_rehydrated=False,physical_input_injected=False,system_input_expected=not observe_only,full_native_instruction_or_API_trace=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--scene',required=True,type=int,choices=[76,77]);p.add_argument('--out',required=True);p.add_argument('--notice',required=True);p.add_argument('--observe-only',action='store_true');a=p.parse_args()
 out=ROOT/a.out;notice=ROOT/a.notice
 if out.exists() or notice.exists():p.error('fresh report and notice paths required before native launch')
 case=run_case(a.scene,notice,a.observe_only);save(a.out,dict(schema_version=1,source_contract=source_contract(),input_source_contract=input_source_contract(),case=case,R3_complete=False,input_method='no input observation' if a.observe_only else 'computer-use sky.press_key space via OS; no host object writes',human_physical_input_claimed=False))
 print('dialogue scene',a.scene,'error',case['lifecycle']['error'],'boundary',case['probe'].get('dialogue_boundary') if case['probe'] else None,flush=True)
 if case['lifecycle']['error'] or not case['probe'] or case['probe'].get('dialogue_boundary',{}).get('ready_index') is None or (not a.observe_only and not case['probe'].get('dialogue_boundary',{}).get('advanced_index')):raise SystemExit(1)
