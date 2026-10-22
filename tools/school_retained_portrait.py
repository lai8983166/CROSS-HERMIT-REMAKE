"""Continue the retained complete task to the original unexecuted name font API."""
import copy,gzip,json,struct,types
from functools import lru_cache
from tools import school_retained_keyboard as parent
from tools import school_retained_keyboard_verification as proof
from tools.school_character_prefix_catalog import REGIONS,expected_prefix,source_catalog as selected_source

ROOT=parent.ROOT;VM=parent.VM;need=parent.need;sha=parent.sha;word=parent.word;canonical=parent.canonical
ACCEPTANCE='analysis/school-retained-keyboard-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='241d7c7de00918ea44763c0c2c9161814dfc4fcd9775d0ddae6a3bf3733157fc'


def inputs():
 accepted=json.loads(parent.pinned(ACCEPTANCE,ACCEPTANCE_SHA));manifest={r['path']:r['sha256'] for r in accepted['artifact_manifest']};path=accepted['report'];raw=parent.pinned(path,manifest[path]);r=json.loads(gzip.decompress(raw));need(canonical(r['contract'])==canonical(parent.inputs()),'frozen keyboard source contract')
 return r,dict(acceptance=ACCEPTANCE,acceptance_sha256=ACCEPTANCE_SHA,report=path,report_sha256=sha(raw),contract=r['contract'])


@lru_cache(maxsize=2)
def boundary(name,scene):
 r,provenance=inputs();c=next(c for c in r['cases'] if (c['name'],c['scene_capture'])==(name,scene));captured=[]
 def capture(u):
  rows=parent.memory_rows(u);captured.append((tuple((a,bytes(u.mem_read(a,b-a+1))) for a,b,_ in u.mem_regions()),u.context_save()));return rows
 # Read-only observation in a private Python globals copy; no frozen module or
 # game routine is patched. The frozen verifier still checks every old write.
 validate=types.FunctionType(proof.verify_case.__code__,dict(proof.verify_case.__globals__,memory_rows=capture),'capture_verified_keyboard_boundary')
 checked=validate(c,parent.inputs());need(len(captured)==1,'one fully verified retained boundary');memory,cpu=captured[0]
 return memory,cpu,dict(source=provenance,name=name,scene_capture=scene,parent_case_proof=checked,final_memory=c['final_memory'],final_architectural_cpu=c['final_architectural_cpu'])


def regions(g):return [dict(pointer=a,bytes=n,hex=g.read(a,n).hex()) for a,n in REGIONS]


def pending(g):
 sp=g.cpu()['ESP'];bp=g.cpu()['EBP'];chain=[]
 for label,ret in (('name',0x4cc1de),('layer',0x4c62d4),('handler',0x4ceda7),('VM',0x454d90),('task',parent.ROOT_RETURN)):
  need(word(g.read(bp+4))==ret,'natural original '+label+' frame');chain.append(dict(label=label,bp=bp,return_va=ret));bp=word(g.read(bp))
 args=[word(g.read(sp+4+i*4)) for i in range(14)];source=selected_source();need(args==source['font_args'] and word(g.read(sp))==0x4ca7cb,'exact original 14 font arguments/return')
 need(sp==chain[0]['bp']-0x148-12-56-4,'original font prologue and argument stack extent')
 return dict(import_slot=0x5920a0,target=word(g.read(0x5920a0)),sp=sp,args=args,return_va=word(g.read(sp)),frames=chain,first_instruction_executed=False)


def run_case(name,scene):
 restored=boundary(name,scene);g=parent.Guest(restored);need(g.cpu()['EIP']==0x4c61c0,'unexecuted original handler continuation');before=regions(g);expected=expected_prefix(before);stop=word(g.read(0x5920a0));step=g.execute('continuous_original_portrait_name_prefix',stop)
 after=regions(g);need(after==expected['after'],'independent complete source prefix state projection');need(step['platform_replays']==[],'no platform result in name resource prefix')
 return dict(name=name,scene_capture=scene,parent_boundary=restored[2],before=before,after=after,selected_source=selected_source(),pending_font=pending(g),step=step,final_memory=parent.memory_rows(g.u),final_architectural_cpu=parent.architectural_cpu(g.u))


def run():
 rows=[]
 for name in ('initial','student9_waiting','fifth_class'):
  for scene in (76,77):rows.append(run_case(name,scene));print(name,scene,'original task continuation -> original name CreateFontA boundary',flush=True)
 return dict(schema_version=1,cases=rows,new_roots=0,new_platform_responses=0,font_API_executed=False,image_loader_executed=False,new_OS_input=False,new_GPU_or_window=False,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report path required')
 r=run();out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('retained portrait report bytes',out.stat().st_size,flush=True)
