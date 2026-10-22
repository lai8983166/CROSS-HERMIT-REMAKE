"""Unchanged retained allocator provenance; no heap repair or native calls."""
import gzip,json,struct,types
from functools import lru_cache
from tools import school_retained_portrait_file as parent
from tools import school_retained_portrait_file_verification as previous

base=parent.base;ROOT=base.ROOT;need=base.need;word=base.word;sha=base.sha;canonical=base.canonical
ACCEPTANCE='analysis/school-retained-portrait-file-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='f41fa01612d729fa174f10b319f918013251eb3522ced9f77ecee4f50bee8379'
FIELDS={'debug_flag':0x7619c0,'next_request':0x7619c4,'break_request':0x7619c8,'lock9':0x761e14,'allocation_hook':0x762130,'debug_first':0x80a430,'total_bytes':0x80a434,'debug_last':0x80a438,'current_bytes':0x80a43c,'high_water_bytes':0x80a440,'heap_token':0x80ab28,'heap_mode':0x80ab2c}


@lru_cache(maxsize=1)
def inputs():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));m={r['path']:r['sha256'] for r in a['artifact_manifest']};p=a['report'];b=base.pinned(p,m[p]);return json.loads(gzip.decompress(b)),dict(acceptance=ACCEPTANCE,acceptance_sha256=ACCEPTANCE_SHA,report=p,report_sha256=sha(b))


@lru_cache(maxsize=2)
def boundary(branch,scene):
 report,source=inputs();c=next(c for c in report['cases'] if (c['name'],c['scene_capture'])==(branch,scene));observed=[]
 def capture(u):
  rows=base.memory_rows(u);observed.append((tuple((a,bytes(u.mem_read(a,b-a+1))) for a,b,_ in u.mem_regions()),u.context_save()));return rows
 proxy=types.SimpleNamespace(**dict(vars(base),memory_rows=capture));verify=types.FunctionType(previous.verify_case.__code__,dict(previous.verify_case.__globals__,base=proxy),'observe_verified_file_allocation_boundary');checked=verify(c);need(len(observed)==1,'one fully verified original allocator boundary');memory,cpu=observed[0]
 return memory,cpu,dict(source=source,name=branch,scene_capture=scene,independent_parent_proof=checked,pending_allocation=c['pending_allocation'],final_memory=c['final_memory'],final_architectural_cpu=c['final_architectural_cpu'])


def state(g):
 values={name:word(g.read(at)) for name,at in FIELDS.items()};nodes=[]
 for name in ('debug_first','debug_last'):
  p=values[name];mapped=p!=0 and any(a<=p and p+32<=b+1 for a,b,_ in g.u.mem_regions());nodes.append(dict(role=name,pointer=p,bytes=32,mapped=mapped,hex=g.read(p,32).hex() if mapped else None))
 return dict(globals=values,debug_chain_nodes=nodes,critical_section_hex=g.read(values['lock9'],24).hex(),allocation_hook_hex=g.read(values['allocation_hook'],10).hex())


def run_case(branch,scene):
 restored=boundary(branch,scene);g=base.Guest(restored);need(g.cpu()['EIP']==0x428a40,'original unexecuted allocator');before=state(g);target=word(g.read(0x592234));maps=[]
 if not any(a<=target<=b for a,b,_ in g.u.mem_regions()):g.u.mem_map(target&~4095,4096);maps.append(dict(pointer=target&~4095,bytes=4096))
 step=g.execute('continuous_original_allocator_to_unexecuted_lock',target);need(step['platform_replays']==[] and state(g)==before,'no platform response or CRT ledger edits');sp=g.cpu()['ESP'];need(word(g.read(sp))==0x5770d3 and word(g.read(sp+4))==before['globals']['lock9'],'original lock9 call');need(all(not n['mapped'] for n in before['debug_chain_nodes']),'both historical debug nodes absent')
 return dict(name=branch,scene_capture=scene,parent_boundary=restored[2],before=before,after=state(g),entry_maps=maps,step=step,pending_lock=dict(import_slot=0x592234,target=target,return_va=word(g.read(sp)),args=[word(g.read(sp+4))],first_instruction_executed=False),final_memory=base.memory_rows(g.u),final_architectural_cpu=base.architectural_cpu(g.u))


def verify_case(c):
 from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
 from tools.school_retained_render_pipeline_verification import Replay
 protocol(c);memory,cpu,provenance=boundary(c['name'],c['scene_capture']);need(canonical(c['parent_boundary'])==canonical(provenance),'pinned full parent provenance');r=Replay.__new__(Replay);r.u=Uc(UC_ARCH_X86,UC_MODE_32);r.image=base.SOURCE.read_bytes();r.objects={};r.locks={}
 for at,b in memory:r.u.mem_map(at,len(b));r.u.mem_write(at,b)
 r.u.context_restore(cpu);before=state(r);need(before==c['before'] and all(not n['mapped'] and n['pointer'] for n in before['debug_chain_nodes']),'exact historical ledger and absent nonzero chain nodes');target=word(r.read(0x592234));maps=[]
 if not any(a<=target<=b for a,b,_ in r.u.mem_regions()):r.u.mem_map(target&~4095,4096);maps.append(dict(pointer=target&~4095,bytes=4096))
 need(maps==c['entry_maps'] and c['step']['boundary']==target,'only unexecuted OS entry page');count=r.step(dict(label=c['step']['label'],root=None,result=dict(c['step'],api_calls=[])));sp=r.cpu()['ESP'];pending=dict(import_slot=0x592234,target=target,return_va=word(r.read(sp)),args=[word(r.read(sp+4))],first_instruction_executed=False)
 need(pending==c['pending_lock'] and pending['return_va']==0x5770d3 and pending['args']==[before['globals']['lock9']],'natural lock9 API before first instruction');need(state(r)==c['after']==before and base.memory_rows(r.u)==c['final_memory'] and canonical(base.architectural_cpu(r.u))==canonical(c['final_architectural_cpu']),'entire unchanged ledger and final maps/CPU');need(count==73 and c['step']['writes']==49,'complete original allocator prefix')
 return dict(name=c['name'],scene_capture=c['scene_capture'],original_instructions_replayed=count,original_writes=49,missing_debug_chain_nodes=before['debug_chain_nodes'],actual_native_lock_entered=False,retained_heap_restored=False,R3_complete=False)


def protocol(c):
 need(c['name'] in ('initial','student9_waiting','fifth_class') and c['scene_capture'] in (76,77),'known retained branch');need(c['step']['platform_replays']==[] and 'root' not in c['step'],'no platform success or new game root');need(c['pending_lock']['first_instruction_executed']is False,'unexecuted native lock');need(c['before']==c['after'],'unchanged CRT state');need([(n['role'],n['pointer'],n['bytes'],n['mapped'],n['hex']) for n in c['before']['debug_chain_nodes']]==[('debug_first',0x4d605b8,32,False,None),('debug_last',0x4d68fa0,32,False,None)],'exact absent historical chain nodes')


def verify(r):
 need(r['schema_version']==1 and r['new_game_roots']==0 and r['new_native_calls'] is r['retained_heap_restored'] is False,'honest retained dependency scope');need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six retained cases');return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],unchanged_retained_dependency_gap_verified=True,retained_heap_restored=False,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--verify');a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable output required')
 if a.verify:result=verify(json.loads(gzip.decompress((ROOT/a.verify).read_bytes())));out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10))
 else:
  cases=[]
  for branch in ('initial','student9_waiting','fifth_class'):
   for scene in (76,77):cases.append(run_case(branch,scene));print(branch,scene,'original allocator prefix; missing historical debug-chain nodes',flush=True)
  result=dict(schema_version=1,cases=cases,new_game_roots=0,new_native_calls=False,retained_heap_restored=False);out.write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0))
