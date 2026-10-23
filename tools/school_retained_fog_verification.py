"""Independent full parent/ordinary-loop replay and real current fog texture bytes."""
import copy,gzip,json,struct,types,os
from functools import lru_cache
from unicorn import UcError
from tools import school_retained_fog as work
from tools import school_retained_world_loop_verification as previous

ROOT=work.ROOT;base=work.base;need=work.need;sha=work.sha;word=work.word;canonical=work.canonical

class Replay(previous.Replay):
 loop_code=work.previous.previous.adapt(previous.previous.Replay.source_step,[("if at==a['boundary']:","if at==a['boundary'] and not s['fault']:"),("'actual_opening_CRT','actual_role9_CRT','recorded_task_platform'","'actual_opening_CRT','actual_role9_CRT','recorded_task_platform','actual_world_static_lock','actual_fog_GPU'"),("count=2000000,timeout=120000000","count=8000000,timeout=240000000"),("finally:self.u.hook_del(ch);self.u.hook_del(wr)","except UcError as exc:need(s['fault'] is not None and str(exc)==s['unicorn_error'],'exact independently observed original memory fault')\n finally:self.u.hook_del(ch);self.u.hook_del(wr)")],UcError=UcError)
 def api(self,a):
  if a.get('kind')!='actual_fog_GPU':return super().api(a)
  e=self.case['fog_texture'];phase=a['phase'];need(type(phase)is int and 0<=phase<6,'bounded fog source COM phase');slot=[80,56,64,68,56,8][phase];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];need(a['index']==self.fog_calls and a['slot']==slot and a['target']==a['va'] and a['sp']==sp and a['pop']==pop and a['args']==args and a['return_va']==ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][phase],'entire original fog COM caller/ABI/order');i=self.fog_wire;need(a['native_wire_index']==i and i<len(e['GPU_trace']),'exact fog native operation cursor');trace=e['GPU_trace'][i];native=trace['reply']['result'];need(trace['request']==dict(id=i+1,op=a['native_op'],**a['native_request']) and a['native_result']==native and trace['reply']['id']==i+1 and trace['reply']['ok']is True,'actual current fog request/reply identity');self.fog_wire+=1;out=[];maps=[]
  def put(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if phase==0:
   need(self.fog_calls==0 and a['target']==self.device_method and args==[self.device,256,128,1,0,25,1,work.FOG+44] and a['native_op']=='create' and a['native_request']==dict(width=256,height=128,levels=1,usage=0,format=25,pool=1),'original source fog geometry/device/output and actual own creation');result=self.fog_space.result('fog',native);self.fog_texture=result['texture'];self.fog_pointer=native['texture']['pointer'];need(self.fog_texture==e['texture'],'typed current fog texture identity')
   for p in (self.fog_texture['pointer'],self.fog_texture['vtable'],*self.fog_texture['methods'].values()):
    lo=p&~4095
    if (lo,4096) not in maps:maps.append((lo,4096))
   put(self.fog_texture['pointer'],struct.pack('<I',self.fog_texture['vtable']))
   for k,p in self.fog_texture['methods'].items():put(self.fog_texture['vtable']+int(k),struct.pack('<I',p))
   put(work.FOG+44,struct.pack('<I',self.fog_texture['pointer']))
  else:
   t=self.fog_texture;p=self.fog_pointer;need(a['target']==t['methods'][str(slot)] and args[0]==t['pointer'],'same live fog native interface and receiver')
   if phase in (1,4):
    need(args==[t['pointer'],0,bp-(52 if phase==1 else 36)] and a['native_op']=='describe' and a['native_request']==dict(pointer=p),'original fog descriptor destination');result=copy.deepcopy(native);raw=struct.pack('<8I',25,1,0,1,65536,0,256,128);need(result['hex']==raw.hex() and (result['width'],result['height'],result['size'])==(256,128,65536),'complete independently derived actual fog descriptor');put(args[2],raw)
   elif phase==2:
    need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048] and a['native_op']=='lock' and a['native_request']==dict(pointer=p,flags=2048),'original whole unlocked fog LockRect');result=self.fog_space.result('fog',native);need(result==e['lock'] and result['pitch']>=512 and result['pitch']<=4096 and result['pitch']%2==0 and len(bytes.fromhex(result['hex']))==128*result['pitch'],'entire actual fog lock and row pitch');self.fog_lock=result;raw=bytes.fromhex(result['hex']);lo=result['bits']&~4095;maps=[(lo,(result['bits']-lo+len(raw)+4095)&~4095)];put(result['bits'],raw);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   elif phase==3:
    need(args==[t['pointer'],0] and a['native_op']=='unlock','original fog UnlockRect caller');source=self.read(word(self.read(work.MAP+0x2658c)),44032);raw=bytearray.fromhex(self.fog_lock['hex']);pitch=self.fog_lock['pitch']
    for y in range(128):raw[y*pitch:y*pitch+344]=source[y*344:(y+1)*344]
    raw=bytes(raw);need(a['source_hex']==source.hex() and a['uploaded_hex']==raw.hex() and a['native_request']==dict(pointer=p,hex=raw.hex()) and self.read(self.fog_lock['bits'],len(raw))==raw,'every independently computed fog row and unchanged native padding');result=copy.deepcopy(native);need(result['uploaded_sha256']==sha(raw),'whole actual fog native upload receipt');rb=e['GPU_trace'][self.fog_wire];need(rb['request']==dict(id=self.fog_wire+1,op='readback',pointer=p) and rb['reply']['id']==self.fog_wire+1 and rb['reply']['ok']is True and rb['reply']['result']==e['readback'] and e['readback']['hex']==raw.hex() and e['readback']['sha256']==sha(raw) and e['readback']['pitch']==pitch,'entire actual current fog GPU readback');self.fog_wire+=1;self.fog_pixels=raw;self.fog_source_pixels=source
   else:need(args==[t['pointer']] and a['native_op']=='release' and a['native_request']==dict(pointer=p) and native==dict(count=0),'original actual zero-reference fog release');result=copy.deepcopy(native)
  value=result['count'] if phase==5 else result['hr'];need(a['value']==value==0 and a['result']==result and a['memory_outputs']==out and sorted((m['pointer'],m['bytes']) for m in a['new_mappings'])==sorted(maps),'every independent current fog COM output and all fresh mapped extents');self.apply_outputs(a);self.api_return(value,pop,ret,sp);self.fog_calls+=1

prepare=types.FunctionType(previous.prepare.__code__,dict(previous.prepare.__globals__,Replay=Replay),'independent_parent_into_fog_capable_replay')
verify_loop=work.previous.previous.adapt(previous.verify_loop,[("c['opening']['final_memory']","c['fog_texture']['creation'][-1]['full_memory']"),("c['opening']['final_architectural_cpu']","c['fog_texture']['creation'][-1]['architectural_cpu']")])

def protocol(c):
 previous.protocol(c);e=c['fog_texture'];need(e['contract']==work.contracts(),'all accepted fog/parent/source identities');need(len(e['creation'])==2,'only two declared original resource roots');renderer=e['entry']['parent']['renderer'];device=e['creation'][0]['result']['cpu']['EAX']
 for s,va,receiver,args,label in zip(e['creation'],(0x4142b0,0x403bd0),(renderer,work.FOG),([0],[device,0]),('original_fog_device_query','original_fog_texture_creation')):need(s['label']==label and s['root']==dict(va=va,receiver=receiver,args=args,sp=work.STACK,return_va=work.RETURN) and s['requested_boundary']==work.RETURN and s['fault'] is s['pending'] is None,'only exact original fog query/creation roots and natural returns')
 need((e['entry']['source_width'],e['entry']['source_height'],e['entry']['texture'])==(172,128,0) and len(bytes.fromhex(e['entry']['source_hex']))==44032,'source initialized fog record and existing owned logical source buffer');need(e['GPU_build']['source_sha256']==work.contracts()['GPU_source_sha256'] and e['GPU_build']['machine']==0x14c,'unchanged actual current multi-texture helper source');need(e['GPU_exit']==0 and e['GPU']==dict(texture_releases=[],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True),'original fog destructor then normal native close without fallback release');need(e['source_COM_calls']==6 and [r['request']['op'] for r in e['GPU_trace']]==['create','describe','lock','unlock','readback','describe','release','close'],'all source fog COM and native readback/close operations');need(e['cleanup']['label']=='supplemental_original_fog_texture_destructor' and e['cleanup']['root']==dict(va=0x403730,receiver=work.FOG,args=[],sp=work.STACK,return_va=work.RETURN),'explicit original supplemental fog destructor')

@lru_cache(maxsize=1)
def proof_helper():
 path=ROOT/('.venv-audit/fog-independent-'+str(os.getpid())+'.exe');need(not path.exists(),'fresh independent native fog helper');return work.build_gpu(path)

def fresh_GPU(e,raw):
 helper,build=proof_helper();gpu=work.ImageD3D8(helper)
 try:
  p=gpu.create(256,128)['texture']['pointer'];d=gpu.describe(p);need((d['width'],d['height'],d['size'])==(256,128,65536),'fresh native fog allocation geometry');lock=gpu.lock(p);need(lock['pitch']==e['lock']['pitch'],'fresh actual native fog row layout');gpu.unlock(p,raw);read=gpu.readback(p);need(read['hex']==raw.hex() and read['sha256']==sha(raw),'fresh independent whole fog GPU pixels');need(gpu.release(p)==dict(count=0),'fresh independent original-equivalent zero-reference release')
 finally:cleanup=gpu.close()
 need(cleanup==e['GPU'] and gpu.process.returncode==0,'normal fresh independent fog device/window cleanup');return dict(build=build,hello=gpu.hello,trace=gpu.trace,cleanup=cleanup,exit_code=gpu.process.returncode)

def verify_fog(r):
 c=r.case;e=c['fog_texture'];need(work.fog_state(r)==e['entry'] and base.memory_rows(r.u)==e['entry_memory']==c['opening']['final_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['entry_architectural_cpu'])==canonical(c['opening']['final_architectural_cpu']),'whole independently replayed opening before any new resource roots');r.fog_space=work.AddressSpace();r.fog_space.next=work.SPACE;r.fog_calls=r.fog_wire=0;creation=0
 for i,s in enumerate(e['creation']):
  if i==1:need(s['root']['args']==[r.cpu()['EAX'],0] and r.cpu()['EAX']==r.device,'actual original device query result flows to original creation')
  creation+=r.loop_step(s);need(r.cpu()['ESP']==work.STACK+(4 if i==0 else 12),'original query bare ret preserves the pre-pushed creation usage; original creator ret8')
 need(work.fog_state(r)==e['created'] and e['created']['accounting']==e['entry']['accounting']+65536 and e['created']['texture']==r.fog_texture['pointer'] and r.fog_calls==2,'original fog creation and byte accounting without host assignment');verify_loop(r);need(work.fog_state(r)==e['business_final'] and base.memory_rows(r.u)==e['business_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['business_architectural_cpu']),'whole original loop business boundary with current fog owner');need(r.fog_calls==4 and r.fog_space.ledger()==e['typed_projection'],'original fog source upload and entire native pointer projection');need(getattr(r,'world_lock_depth',0)==0 and c['world_loop']['supplemental_lock_cleanup']==[],'no CRT exit/unwind workaround after current fog restoration');n=r.loop_step(e['cleanup']);need(n==149 and work.fog_state(r)==e['after_cleanup'] and e['after_cleanup']['texture']==0 and e['after_cleanup']['accounting']==e['entry']['accounting'] and r.fog_calls==6,'complete original supplemental fog release/clear and counter balance');last=e['GPU_trace'][r.fog_wire];need(last['request']==dict(id=r.fog_wire+1,op='close') and last['reply']['result']==e['GPU'] and last['reply']['ok']is True and last['reply']['id']==r.fog_wire+1 and r.fog_wire+1==len(e['GPU_trace']),'entire normal native fog wire consumed');fresh=fresh_GPU(e,r.fog_pixels);r.fog_proof=dict(new_resource_instructions=creation,new_resource_writes=sum(s['result']['writes'] for s in e['creation']),source_size=[172,128],native_size=[256,128],source_bytes=44032,native_bytes=len(r.fog_pixels),upload_sha256=sha(r.fog_pixels),source_sha256=sha(r.fog_source_pixels),all_rows_and_unchanged_padding_verified=True,original_memcpy_body_executed=True,source_COM_calls=6,source_original_destructor_instructions=n,whole_CPU_memory_queue_and_ownership=True,independent_fresh_GPU=fresh,normal_source_cleanup=True,old_exit_callback_workaround=False,new_OS_input=False,interactive_desktop_required=False,actual_D3D_draw_or_Present=False,R3_complete=False,R6_complete=False)

def isolated_worker_builds():previous.isolated_worker_builds();globals()['_builds_ready']=True

def verify_case(c,boundary_observer=None):
 if not globals().get('_builds_ready'):isolated_worker_builds()
 protocol(c);proof=[]
 def observe(r):
  if boundary_observer is not None:boundary_observer(r)
  verify_fog(r);proof.append((r.loop_proof,r.fog_proof))
 call=work.previous.previous.adapt(previous.parent.verify_case,[("glyph_cleanup=[]","verify_fog_resource_and_loop(r);glyph_cleanup=[]")],prepare=prepare,verify_fog_resource_and_loop=observe);opening=call(c);need(len(proof)==1,'one complete independently verified fog scope');return dict(name=c['name'],scene_capture=c['scene_capture'],opening=opening,world_loop=proof[0][0],fog_texture=proof[0][1])

def verify_case_report(row):
 raw=base.pinned(row['path'],row['sha256']);need(len(raw)==row['bytes'],'entire compressed immutable fog case byte length')
 with gzip.open(ROOT/row['path'],'rt',encoding='utf8') as f:c=json.load(f)
 need((c['name'],c['scene_capture'])==(row['name'],row['scene_capture']),'source fog case identity');return verify_case(c)

def verify_group(args):
 import contextlib
 rows,prefix=args;proofs=[]
 with open(ROOT/(prefix+'-'+rows[0]['name']+'.log'),'x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  isolated_worker_builds()
  for row in rows:
   proof=verify_case_report(row);path=prefix+'-'+row['name']+'-'+str(row['scene_capture'])+'.json';out=ROOT/path;need(not out.exists(),'fresh immutable complete independent case proof');r=dict(schema_version=1,source_case=row,verification_source_sha256=sha((ROOT/'tools/school_retained_fog_verification.py').read_bytes()),proof=proof);out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));raw=out.read_bytes();proofs.append(dict(proof,source_case=row,independent_case_proof=dict(path=path,sha256=sha(raw),bytes=len(raw))));print('independent fog source/whole original loop verified',row['name'],row['scene_capture'],flush=True)
 return proofs

def verify_matrix(matrix,proof_prefix,existing_initial_proof=None,jobs=3):
 need(matrix['schema_version']==1 and matrix['contract']==work.contracts() and matrix['new_VM_roots']==matrix['game_function_substitutions']==matrix['IAT_rebindings']==0,'all accepted source fog matrix pins and no substitutes')
 for k in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):need(matrix[k]is False,'honest current fog matrix scope '+k)
 rows=matrix['case_reports'];need([(r['name'],r['scene_capture']) for r in rows]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six source fog branches');need(1<=jobs<=3,'bounded independent source worker count');proofs=[];todo=rows
 if existing_initial_proof:
  raw=(ROOT/existing_initial_proof).read_bytes();r=json.loads(raw);need(r['source_case']==rows[0] and r['verification_source_sha256']==sha((ROOT/'tools/school_retained_fog_verification.py').read_bytes()) and (r['proof']['name'],r['proof']['scene_capture'])==('initial',76),'exact already completed whole independent initial case source/code identity');p=r['proof'];need(p['world_loop']['natural_pre_yield_boundary'] and p['fog_texture']['normal_source_cleanup'] and p['fog_texture']['all_rows_and_unchanged_padding_verified'],'complete independent initial proof including natural wait and actual current fog cleanup');proofs.append(dict(p,source_case=rows[0],independent_case_proof=dict(path=existing_initial_proof,sha256=sha(raw),bytes=len(raw))));todo=rows[1:]
 groups=[([r for r in todo if r['name']==n],proof_prefix) for n in ('initial','student9_waiting','fifth_class')];groups=[g for g in groups if g[0]]
 if jobs==1:
  for group in groups:proofs.extend(verify_group(group))
 else:
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=jobs) as executor:
   for group in executor.map(verify_group,groups):proofs.extend(group)
 need(len(proofs)==6,'all six independently replayed original fog cases');return dict(schema_version=1,cases=proofs,six_original_fog_loops_verified=True,independent_processes=jobs,reused_complete_initial_independent_proof=existing_initial_proof,whole_parent_replayed_each=True,interactive_desktop_required=False,new_OS_input=False,actual_D3D_draw_or_Present=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('matrix');p.add_argument('--out',required=True);p.add_argument('--existing-initial-proof');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable whole fog proof')
 raw=(ROOT/a.matrix).read_bytes();r=verify_matrix(json.loads(raw),'analysis/'+out.stem+'-cases',a.existing_initial_proof,a.jobs);r['source_matrix_sha256']=sha(raw);r['verification_source_sha256']=sha((ROOT/'tools/school_retained_fog_verification.py').read_bytes());out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six whole original fog proofs complete',flush=True)
