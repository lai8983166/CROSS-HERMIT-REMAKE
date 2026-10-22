"""Independent corpus byte walk, dependency checks and continuous prefix replay."""
import gzip,json,struct
from collections import Counter
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from tools import school_retained_portrait as work
from tools import school_retained_keyboard as parent
from tools.school_retained_portrait_catalog import INSTALLED,PRIVATE,SCRIPTS

ROOT=work.ROOT;need=work.need;word=work.word;sha=work.sha;canonical=work.canonical;VM=work.VM


def verify_catalog(r):
 raw=parent.SOURCE.read_bytes();need(r['schema_version']==1 and r['source_sha256']==sha(raw)==parent.SOURCE_SHA256,'catalog original executable identity');files=sorted(SCRIPTS.glob('*.BIN'));need([s['name'] for s in r['scripts']]==[p.name for p in files],'all installed scripts exactly once');counts=Counter();portrait=[];total_segments=total_empty=0
 def ints(b,at,n):return list(struct.unpack_from('<'+'I'*n,b,at))
 def cstring(at):
  need(parent.BASE<=at<parent.BASE+len(raw),'bounded source string pointer');b=raw[at-parent.BASE:at-parent.BASE+256];z=b.find(bytes(1));need(z>=0,'terminated source string');return b[:z]
 for s,path in zip(r['scripts'],files):
  b=path.read_bytes();need(s['path']==path.relative_to(ROOT).as_posix() and s['bytes']==len(b) and s['sha256']==sha(b) and b==(PRIVATE/path.relative_to(INSTALLED)).read_bytes(),'complete source script/private identity')
  size,ng=struct.unpack_from('<II',b);need(size==len(b) and ng==2,'source root package');groups=ints(b,8,ng);g=groups[0];group_size,ns=struct.unpack_from('<II',b,g);need(g+group_size==groups[1],'source VM group extent');offsets=ints(b,g+8,ns);segments=[];commands=[];empty=0
  for i,start in enumerate(offsets):
   z=g+(offsets[i+1] if i+1<ns else group_size);start+=g
   if z-start==4:need(b[start:z]==b'dmf\0','actual four-byte dmf marker');empty+=1;continue
   n=ints(b,start,1)[0];v=ints(b,start+4,n);need(n>=2 and v==sorted(v) and v[0]>=4+4*n and v[-1]<=z-start,'source VM header bounds');a=start+v[0];end=start+v[1];first=len(commands)
   while a<end:
    need(a+4<=end,'source instruction header');op,step=struct.unpack_from('<HH',b,a);need(step>=4 and step%2==0 and a+step<=end,'source instruction declared extent');commands.append(dict(segment=i,offset=a,PC=a-start-v[0],opcode=op,bytes=step,sha256=sha(b[a:a+step])));counts[op]+=1
    if op==30:
     need(step in (12,20),'source portrait variant');cells=ints(b,a+4,(step-4)//4);expr=[dict(raw=x,type=x>>28,payload=x&0xfffffff,literal=x&0xfffffff if x>>28==2 else None) for x in cells];need(expr[0]['literal'] is not None and expr[1]['literal'] is not None,'literal role/configuration source')
     portrait.append(dict(script=path.name,segment=i,offset=a,PC=a-start-v[0],source_handler_read_window_hex=b[a:a+20].hex(),expressions=expr,configuration=expr[0]['literal'],role=expr[1]['literal'],expression_is_dynamic=any(x['type']!=2 for x in expr),declared_bytes=step,missing_declared_operands=4-len(cells),encoding_status='complete_four_operands' if step==20 else 'short_two_operands; original fixed handler reads beyond declared command; runtime unresolved'))
    a+=step
   need(a==end,'exact source VM instruction end');segments.append(dict(index=i,start=start,end=z,offsets=v,code_start=start+v[0],code_end=end,first_command=first,command_count=len(commands)-first))
  need(s['commands']==commands and s['segments']==segments and s['empty_segments']==empty,'independent complete command/segment byte walk');total_segments+=len(segments);total_empty+=empty
 need(r['opcode_counts']=={str(k):counts[k] for k in sorted(counts)} and r['portraits']==portrait,'all static instruction/portrait occurrences and short-encoding flags')
 need(set(r['configurations'])=={str(c['configuration']) for c in portrait} and set(r['roles'])=={str(c['role']) for c in portrait},'all and only referenced source dependencies')
 for key,c in r['configurations'].items():
  index=int(key);at=0x624520+index*38;body=raw[at-parent.BASE:at-parent.BASE+38];w=list(struct.unpack('<19h',body));need(c==dict(index=index,pointer=at,hex=body.hex(),words=w,layer=w[0]),'source configuration table bytes')
 for key,c in r['roles'].items():
  index=int(key);at=0x622668+index*60;body=raw[at-parent.BASE:at-parent.BASE+60];np=ints(raw,0x621f2c-parent.BASE+index*4,1)[0];name=cstring(np);filename=cstring(word(body)).decode('ascii');path=INSTALLED/'DATA/ADV/BIN'/filename;image=path.read_bytes();need(image==(PRIVATE/path.relative_to(INSTALLED)).read_bytes(),'private image identity')
  need(c==dict(index=index,name_pointer=np,name_hex=name.hex(),name_big5=name.decode('big5'),resource_row=at,resource_row_hex=body.hex(),filename=filename,image_path=path.relative_to(ROOT).as_posix(),image_bytes=len(image),image_sha256=sha(image)),'all source name/image dependencies')
 md=Cs(CS_ARCH_X86,CS_MODE_32);need([d['opcode'] for d in r['dispatch']]==sorted(counts),'all original dispatch entries')
 for d in r['dispatch']:
  if d['opcode']==19:
   need(d==dict(opcode=19,kind='END special before switch',entry=0x4cea19,direct_call_targets=[0x4ce090,0x4ce800]),'original END special dispatch');continue
  slot=0x4d03cf+4*(d['opcode']-5);at=word(raw,slot-parent.BASE);rows=[];calls=[]
  for ins in md.disasm(raw[at-parent.BASE:at-parent.BASE+128],at):
   rows.append(dict(va=ins.address,hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
   if ins.mnemonic=='call' and ins.op_str.startswith('0x'):calls.append(int(ins.op_str,16))
   if ins.mnemonic in ('jmp','ret'):break
  need(d==dict(opcode=d['opcode'],kind='original switch block; not full handler semantics',table_slot=slot,entry=at,direct_call_targets=calls,instructions=rows),'original dispatch source table/block')
 summary=dict(script_files=len(files),VM_segments=total_segments,empty_segments=total_empty,commands=sum(counts.values()),opcode_classes=len(counts),portrait_commands=len(portrait),portrait_configurations=len(r['configurations']),portrait_roles=len(r['roles']),dynamic_portrait_expressions=sum(c['expression_is_dynamic'] for c in portrait),short_portrait_commands=sum(bool(c['missing_declared_operands']) for c in portrait))
 need(r['summary']==summary and r['scope']=='All installed script bytes statically parsed; not dynamic reachability, full opcode semantics or R6 completion','honest full corpus summary/scope')
 return dict(schema_version=1,independent_byte_walk_verified=True,summary=summary,short_encoding_followup=[dict(script=c['script'],segment=c['segment'],offset=c['offset'],declared_bytes=c['declared_bytes'],source_handler_read_window_hex=c['source_handler_read_window_hex']) for c in portrait if c['missing_declared_operands']],R6_complete=False)


def verify_case(c):
 need(c['name'] in ('initial','student9_waiting','fifth_class') and c['scene_capture'] in (76,77),'known source branch');memory,cpu,provenance=work.boundary(c['name'],c['scene_capture']);need(canonical(c['parent_boundary'])==canonical(provenance),'entire verified parent source boundary')
 r=work.proof.Replay.__new__(work.proof.Replay);r.u=Uc(UC_ARCH_X86,UC_MODE_32);r.image=parent.SOURCE.read_bytes();r.objects={};r.locks={}
 for at,b in memory:r.u.mem_map(at,len(b));r.u.mem_write(at,b)
 r.u.context_restore(cpu);need(r.cpu()['EIP']==0x4c61c0,'same retained original instruction/stack');before=work.regions(r);need(before==c['before'] and c['selected_source']==work.selected_source(),'independent pre-state and original configuration contract');expected=work.expected_prefix(before);s=c['step'];target=word(r.read(0x5920a0))
 need(s['label']=='continuous_original_portrait_name_prefix' and s['kind']=='task' and 'root' not in s and s['platform_replays']==[] and s['boundary']==target,'continuous no-root/no-platform prefix')
 n=r.step(dict(label=s['label'],root=None,result=dict(s,api_calls=[])))
 need(work.regions(r)==c['after']==expected['after'],'independent entire prefix source projection');need(work.pending(r)==c['pending_font'],'independent natural complete task/VM/font stack')
 need(parent.memory_rows(r.u)==c['final_memory'] and canonical(parent.architectural_cpu(r.u))==canonical(c['final_architectural_cpu']),'complete final mappings and architectural CPU')
 need(work.proof.state(r)==s['state'] and not any(i['va']==target for i in s['instruction_counts']),'source state and font API first instruction unexecuted')
 return dict(name=c['name'],scene_capture=c['scene_capture'],new_original_instructions_replayed=n,new_roots=0,new_platform_responses=0,configuration=8,layer=5,role=4,name_big5=c['selected_source']['name']['text_big5'],font_height=c['pending_font']['args'][0],font_weight=c['pending_font']['args'][4],font_API_executed=False,image_dependency='data/adv/bin/sc004.bin',image_loader_executed=False,full_memory_regions=len(c['final_memory']),R3_complete=False)


def verify(r):
 need(r['schema_version']==1 and r['new_roots']==r['new_platform_responses']==0,'continuous report scope')
 for k in ('font_API_executed','image_loader_executed','new_OS_input','new_GPU_or_window','R3_complete'):need(r[k] is False,'honest prefix scope '+k)
 need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'six complete retained branches')
 return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],six_continuous_portrait_prefixes_verified=True,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);p.add_argument('--catalog',action='store_true');a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof path required')
 b=(ROOT/a.report).read_bytes();r=json.loads(b if a.catalog else gzip.decompress(b));checked=verify_catalog(r) if a.catalog else verify(r);out.write_text(json.dumps(checked,ensure_ascii=False,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('catalog verified' if a.catalog else 'six continuous portrait prefixes verified')
