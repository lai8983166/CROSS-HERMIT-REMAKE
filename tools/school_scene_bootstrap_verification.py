"""Independent native scene registry/object and cooperative wait evidence checks."""
import gzip,json,struct,hashlib
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_startup_lifetime_verification import ROOT,SOURCE,SOURCE_SHA256
from tools.school_scheduler_lifetime_verification import verify_lifecycle,THUNK
SIZE=0x1194f0
def need(v,msg):
 if not v:raise ValueError(msg)
def word(b,p=0):return struct.unpack_from('<I',b,p)[0]
def put(b,p,v):struct.pack_into('<I',b,p,v)
def sha(b):return hashlib.sha256(b).hexdigest()

def source(report):
 raw=SOURCE.read_bytes();s=report['source_contract'];need(sha(raw)==SOURCE_SHA256==s['source_sha256'],'source identity');need((s['object_bytes'],s['vtable'],s['thread_callback'],s['state_dispatch'],s['world_loop'])==(SIZE,0x59a430,0x451670,0x451a60,0x4539b0),'original scene source graph')
 need(struct.unpack_from('<2I',raw,0x59a430-0x400000)==(0x451670,0x451630),'actual derived vtable')
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 for row in s['instructions']:
  at=row['va'];i=next(md.disasm(raw[at-0x400000:at-0x400000+16],at));need((row['hex'],row['mnemonic'],row['operands'])==(i.bytes.hex(),i.mnemonic,i.op_str),'source instruction operands')
 need(s['original_scene_callback_executed'] is False and s['original_factory_invoked'] is False,'independent scope')
 for row in s['ranges']:need(sha(raw[row['pointer']-0x400000:row['pointer']-0x400000+row['bytes']])==row['sha256'],'source range digest')
 return raw

def common(r):
 need(r['schema_version']==1 and r['R3_complete'] is False,'honest R3 scope');raw=source(r);c=r['case'];p=c['probe'];need(c['private_buffers_written'] is True and c['source_code_or_IAT_replaced'] is False and c['retained_scene_advanced'] is False,'private source scope')
 need(p is not None,'accepted native probe must complete');lifetime=verify_lifecycle(c['lifecycle']);alloc=p['allocations'];need([a['bytes'] for a in alloc]==[0x200000,4096],'fresh allocation extents')
 data,code=[a['pointer'] for a in alloc];need(all(0<a['pointer']<a['pointer']+a['bytes']<=0x100000000 for a in alloc) and (data+0x200000<=code or code+4096<=data),'nonoverlapping x86 buffers');need((p['manager'],p['node'])==(data+0x1000,data+0x2000),'exact private objects')
 expected=dict(code=r['source_contract']['ranges'],IAT=p['source_before']['IAT']);need(p['source_before']==p['source_after']==expected and [x['slot'] for x in expected['IAT']]==r['source_contract']['IAT_slots'] and all(word(bytes.fromhex(x['hex'])) for x in expected['IAT']),'actual source/vtable/IAT identity')
 need(p['frees']==[dict(**a,released=True) for a in reversed(alloc)],'all native calls ended and private allocations freed')
 calls=sorted(p['calls'],key=lambda c:c['sequence']);need([c['sequence'] for c in calls]==list(range(len(calls))),'all source call sequence')
 for c in calls:
  args=c['args'];before=struct.pack('<11I',c['va'],c['receiver'],len(args),*(args+[0]*(3-len(args))),0,0xcccccccc,0xcccccccc,0xcccccccc,0);after=bytes.fromhex(c['parameter_after_hex'])
  need(c['parameter_before_hex']==before.hex() and len(after)==44 and after[:28]==before[:28] and word(after,28)==c['eax'] and word(after,32)==word(after,36)!=0 and word(after,40)==0x4c4c4143 and c['wait_status']==c['exit_code']==0 and c['thread_id'],'full call parameters/ESP/actual exit')
 # Every process write is either the fixed private bridge, declared object seed,
 # an explicitly supplied actual event handle, font query buffer, or parameter.
 writes=p['writes'];need(writes[0]==dict(pointer=code,bytes=len(THUNK),sha256=sha(THUNK)),'fixed private bridge write')
 permitted={(data+c['slot'],44,sha(bytes.fromhex(c['parameter_before_hex']))) for c in calls}
 for w in writes:need(any(a['pointer']<=w['pointer'] and w['pointer']+w['bytes']<=a['pointer']+a['bytes'] for a in alloc),'all writes private')
 return p,raw,lifetime,calls,writes,permitted

def verify_object(r):
 p,raw,lifetime,calls,writes,allowed=common(r);need(p['kind']=='derived_object' and p['fill'] in (0,165,204),'declared scene case');fill=p['fill'];node=p['node'];manager=p['manager'];data=manager-0x1000;stages=p['stages']
 labels=['declared_fresh_buffers','original_scene_constructed','original_registered','original_disabled','original_disabled_scan','original_unlinked','original_scene_destructed','original_manager_destructed'];need([s['label'] for s in stages]==labels,'complete native object stages')
 def buffers(s):
  m=bytes.fromhex(s['manager_hex']);b=bytes.fromhex(s['node_hex']);need(len(m)==512 and len(b)==SIZE+32 and b[SIZE:]==bytes([fill])*32,'full source object extent/tail guard');return m,b
 stage=[buffers(s) for s in stages];need(stage[0]==(bytes([fill])*512,bytes([fill])*(SIZE+32)),'declared fresh object bytes')
 manager_state=bytearray(stage[1][0]);need(manager_state[:256]==bytes(256) and word(manager_state,0x118) not in (0,fill*0x1010101) and manager_state[0x11c:]==bytes([fill])*(512-0x11c),'source manager initialization/guard')
 b=bytearray(stage[1][1]);need(word(b)==0x59a430 and b[0x28]==0 and all(b[x]==0 for x in (0x30,0x31,0x170,0x171,0x172,0x18c,0x18d,0x117f20)) and all(word(b,x)==v for x,v in ((0x34,0),(0x64,0),(0x178,0),(0x17c,0),(0x180,4),(0x184,0),(0x188,0))) and b[0x44:0x60]==bytes(28) and b[0x117dd8:0x117f18]==bytes(0x140),'source-derived scene constructor fields')
 font=p['source_font_handle'];need(font and word(b,0x117f24)==font and word(b,0x60),'actual constructor resource fields')
 fonts=p['font_states'];need([x['label'] for x in fonts]==['source_constructor_font','after_source_destructor'],'font observation order');lf=bytearray(b'\xa5'*76);struct.pack_into('<5i8B',lf,0,10,0,0,0,400,0,0,0,1,5,0,0,1);face=raw[0x592c9c-0x400000:].split(b'\0')[0]+b'\0';lf[28:28+len(face)]=face
 need(fonts[0]==dict(label='source_constructor_font',handle=font,bytes_returned=60,before_hex='a5'*76,after_hex=lf.hex()) and fonts[1]==dict(label='after_source_destructor',handle=font,bytes_returned=0,before_hex='a5'*76,after_hex='a5'*76),'actual font metadata and invalidity after original DeleteObject')
 for off,value in [(4,0),(8,manager),(12,0),(0x14,0),(0x18,0)]:put(b,off,value)
 put(manager_state,0,node);need(stage[2]==(manager_state,b),'full registered scene bytes');put(b,4,2);need(stage[3]==stage[4]==(manager_state,b),'disabled scan must leave every byte unchanged')
 put(manager_state,0,0);need(stage[5]==(manager_state,b),'full original unlink state')
 # Source cleanup: world-owned arrays/GDI resources, ten 2Ch containers,
 # LOGFONT/embedded text owner and the final 4222D0 base vtable reset.
 for off in (0x194,0x192c,0x2c14,0x2a2b0,0x2a2b4,0x2f2f8,0xdb99c,0xdb9a0,0xde5f4,0x117f24,*[0x116230+i*0x2c for i in range(10)]):put(b,off,0)
 b[0x118040:0x118047]=bytes(7);put(b,0x118048,0);put(b,0,0x594a54);need(stage[6]==(manager_state,b),'complete source scene destructor byte model')
 manager_state[0x100:0x118]=stage[7][0][0x100:0x118];need(stage[7]==(manager_state,b),'source manager destructor full unchanged fields')
 query=next(word(bytes.fromhex(i['hex'])) for i in p['source_before']['IAT'] if i['slot']==0x592068)
 wanted=[(0x421540,manager,[]),(0x421660,manager,[]),(0x451170,node,[]),(query,0,[font,60,data+0x400]),(0x4216c0,manager,[node,0,0]),(0x422560,node,[2]),(0x4217c0,manager,[]),(0x421d50,manager,[node]),(0x451470,node,[]),(query,0,[font,60,data+0x400]),(0x4215f0,manager,[])]
 need([(c['va'],c['receiver'],c['args']) for c in calls]==wanted and all(c['slot']==0 for c in calls),'exact original constructor/register/destructor and query ABI')
 expected_writes=[dict(pointer=p['allocations'][1]['pointer'],bytes=len(THUNK),sha256=sha(THUNK))]+[dict(pointer=a,bytes=n,sha256=sha(bytes([fill])*n)) for a,n in [(manager,512),(node,SIZE+32)]]
 for c in calls:
  if c['va']==query:expected_writes.append(dict(pointer=data+0x400,bytes=76,sha256=sha(b'\xa5'*76)))
  expected_writes.append(dict(pointer=data+c['slot'],bytes=44,sha256=sha(bytes.fromhex(c['parameter_before_hex']))))
 need(writes==expected_writes,'all exact private constructor writes')
 return dict(kind=p['kind'],fill=fill,lifecycle=lifetime,object_bytes=SIZE,captured_stage_object_bytes=len(stages)*(SIZE+32+512),fully_modelled_stages_excluding_constructor=7,constructor_outputs_are_native_observations=True,whole_constructor_independently_replayed=False,registry_disabled_unlink_and_destructor_full_byte_models=True,actual_font_created_and_original_deleted=True,original_scene_callback_executed=False)

def verify_yield(r):
 p,raw,lifetime,calls,writes,allowed=common(r);need(p['kind']=='isolated_yield' and p['original_CRT_callback'] is False and p['experimental_release'] is True and p['event_seed_owner']=='experiment actual CreateEvent/DuplicateHandle; not source callback-created','declared isolated yield/platform seed scope');node=p['node'];manager=p['manager'];event=p['node_event'];data=manager-0x1000
 labels=['source_base_registered','declared_owned_event_and_source_active','original_yield_blocked','original_delay_tick_1','original_delay_tick_2','original_yield_returned','source_base_unlinked_destructed','source_manager_destructed'];need([s['label'] for s in p['stages']]==labels,'all actual yield stages');states=[(bytes.fromhex(s['manager_hex']),bytes.fromhex(s['node_hex'])) for s in p['stages']];m=bytearray(states[0][0]);b=bytearray(128);put(b,0,0x594a54);put(b,8,manager);need(states[0][1]==b and len(m)==512 and word(m)==node and m[4:256]==bytes(252) and m[0x11c:]==bytes(512-0x11c),'original base registration')
 put(b,0x1c,event);put(b,4,1);need(event and states[1]==(m,b),'actual declared event and original active flag');put(b,0x14,2);put(b,4,0x10001);need(states[2]==(m,b),'full actual original yield state')
 for i in range(2):put(b,0x14,1-i);need(states[3+i]==(m,b),'original delay tick full bytes')
 put(b,4,1);need(states[5]==(m,b),'actual yield clears10000 and returns');put(b,4,0);put(m,0,0);need(states[6]==(m,b),'original yield node unlinked/destructed');m[0x100:0x118]=states[7][0][0x100:0x118];need(states[7]==(m,b),'original source manager destruction')
 for s in [p['blocked_before_ticks'],*p['tick_statuses']]:
  need(s['wait_status']==258 and s['exit_code']==259,'actual yield thread remains blocked/STILL_ACTIVE');f=s['frame'];cpu=bytes.fromhex(f['context_hex']);need(len(cpu)==716 and (f['EBP'],f['EIP'],f['ESP'])==tuple(word(cpu,o) for o in (180,184,196)) and f['stack_start']==f['ESP'] and len(bytes.fromhex(f['stack_hex']))==128,'complete actual WOW64 context/stack')
  need(any(x['return_va']==0x42240d for x in f['chain']),'actual source WaitForSingleObject ancestry')
 need(len(p['tick_statuses'])==2 and p['release_SetEvent_result'] is True and p['returned_thread']==dict(wait_status=0,exit_code=0),'explicit native event release and natural return')
 for key,label,h in [('node_event_after_supplemental_close','isolated_node_after_owner_close',event),('manager_event_after_source_destructor','manager_after_source_destructor',word(m,0x118))]:need(p[key]==dict(label=label,handle=h,duplicate_succeeded=False,error=6),'actual event handle invalidity')
 wanted=[(0x421540,manager,[],0),(0x421660,manager,[],0),(0x422290,node,[],0),(0x4216c0,manager,[node,0,0],0),(0x422560,node,[1],0),(0x422360,node,[2],0),(0x4217c0,manager,[],256),(0x4217c0,manager,[],256),(0x4225a0,node,[0xffffffff],0),(0x421d50,manager,[node],0),(0x4222d0,node,[],0),(0x4215f0,manager,[],0)]
 need([(c['va'],c['receiver'],c['args'],c['slot']) for c in calls]==wanted,'exact isolated wait and original delay tick ABI')
 expected_writes=[dict(pointer=p['allocations'][1]['pointer'],bytes=len(THUNK),sha256=sha(THUNK))]+[dict(pointer=a,bytes=n,sha256=sha(bytes(n))) for a,n in [(manager,512),(node,128)]]
 for c in calls:
  if c['sequence']==4:expected_writes.append(dict(pointer=node+0x1c,bytes=4,sha256=sha(struct.pack('<I',event))))
  expected_writes.append(dict(pointer=data+c['slot'],bytes=44,sha256=sha(bytes.fromhex(c['parameter_before_hex']))))
 need(writes==expected_writes,'all exact isolated yield process writes')
 return dict(kind=p['kind'],lifecycle=lifetime,actual_source_wait_ancestry=True,original_delay_ticks=2,delay_sequence=[2,1,0],actual_native_root_thread_returned=True,original_CRT_scene_callback=False,experimental_event_seed_and_release=True,retained_scene_advanced=False)

def verify_report(r):return verify_yield(r) if r['case']['probe'] and r['case']['probe']['kind']=='isolated_yield' else verify_object(r)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.report;out=ROOT/a.out;need(not out.exists(),'fresh proof path');r=verify_report(json.loads(gzip.decompress(path.read_bytes())));r['report']=dict(path=a.report,sha256=sha(path.read_bytes()));out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');print('Verified scene bootstrap',r['kind'],'R3 incomplete')
