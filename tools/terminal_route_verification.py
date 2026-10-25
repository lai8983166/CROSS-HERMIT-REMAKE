"""Independent raw-container, local-CFG and frozen handoff validation."""
import argparse, gzip, json, struct
from collections import Counter
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools import terminal_route_catalog as catalog

ROOT,SOURCE,need,sha=catalog.ROOT,catalog.SOURCE,catalog.need,catalog.sha


def scan(raw):
 """Do not use the catalog's frozen container/instruction parser."""
 def directory(at, limit):
  need(0<=at<=limit-8<=len(raw)-8,'independent directory bounds')
  size,n=struct.unpack_from('<II',raw,at)
  need(n>0 and size>=8+n*4 and at+size<=limit,'independent directory extent')
  offsets=list(struct.unpack_from('<'+'I'*n,raw,at+8))
  need(offsets==sorted(offsets) and 8+n*4<=offsets[0] and offsets[-1]<=size,'independent directory entries')
  return size,offsets
 size,groups=directory(0,len(raw));need(size==len(raw) and len(groups)==2,'independent complete script')
 g=groups[0];n,subs=directory(g,groups[1]);need(g+n==groups[1],'independent VM package boundary')
 result={};first=0
 for j,rel in enumerate(subs):
  start=g+rel;end=g+(subs[j+1] if j+1<len(subs) else n)
  need(start<end,'nonempty independently bounded subrecord')
  if end-start==4:
   need(raw[start:end]==b'dmf\0','independent empty marker');result[j]=None;continue
  need(start+4<=end,'independent VM header');count=struct.unpack_from('<I',raw,start)[0]
  need(count>=2 and start+4+4*count<=end,'independent VM offset count')
  offsets=list(struct.unpack_from('<'+'I'*count,raw,start+4))
  need(offsets==sorted(offsets) and 4+4*count<=offsets[0] and offsets[-1]<=end-start,'independent VM sections')
  lo,hi=start+offsets[0],start+offsets[1];pc=lo;rows=[]
  while pc<hi:
   need(pc+4<=hi,'independent command header');op,step=struct.unpack_from('<HH',raw,pc)
   need(step>=4 and step%2==0 and pc+step<=hi,'independent command span');b=raw[pc:pc+step]
   minimum=catalog.READS[op][2] if op in catalog.READS else 4
   rows.append(dict(segment=j,offset=pc,PC=pc-lo,opcode=op,bytes=step,sha256=sha(b),hex=b.hex(),
    family=catalog.family(op),short_handler_read=step<minimum,handler_required_bytes=minimum if op in catalog.READS else None));pc+=step
  need(pc==hi,'independent exact code end')
  seg=dict(index=j,start=start,end=end,offsets=offsets,code_start=lo,code_end=hi,first_command=first,command_count=len(rows))
  result[j]=(seg,rows);first+=len(rows)
 return result


def control(rows, code_size):
 pcs={c['PC'] for c in rows};edges=[];issues=[]
 for c in rows:
  p,o,n=c['PC'],c['opcode'],c['bytes'];data=bytes.fromhex(c['hex'])
  if c['short_handler_read']:issues.append(dict(PC=p,kind='handler_reads_beyond_declared_command'));continue
  if o==19:continue
  if o in (8,11) and n!={8:20,11:8}[o]:
   issues.append(dict(PC=p,kind='unsupported_conditional_encoding' if o==8 else 'unsupported_jump_encoding'));continue
  if o in (0,1,2,3,4,9,10,15,16,52,53,54,172):issues.append(dict(PC=p,kind='unsupported_control_opcode'));continue
  dests=([('condition_true',struct.unpack_from('<I',data,16)[0]),('condition_false',p+n)] if o==8 else
   [('jump',struct.unpack_from('<I',data,4)[0])] if o==11 else [('advance',p+n)])
  for kind,d in dests:
   if d in pcs:edges.append(dict(source=p,target=d,kind=kind))
   else:issues.append(dict(PC=p,kind='falloff' if d==code_size else 'invalid_target',target=d))
 return edges,issues


def closure(rows, edges, start):
 seen={start} if start in {c['PC'] for c in rows} else set()
 while True:
  more={e['target'] for e in edges if e['source'] in seen}-seen
  if not more:return sorted(seen)
  seen.update(more)


def mode_contract(rows, edges, issues):
 prefix=[(c['PC'],c['opcode'],c['bytes']) for c in rows[:4]]
 standard=prefix==[(0,167,8),(8,8,20),(28,166,8),(36,11,8)]
 if standard:
  standard=(bytes.fromhex(rows[0]['hex'])[4:]==b'\0'*4 and
   bytes.fromhex(rows[1]['hex'])[4:]==bytes.fromhex('0100000000000000010000202c000000') and
   bytes.fromhex(rows[2]['hex'])[4:] in (bytes.fromhex('00000020'),bytes.fromhex('01000020')))
 if not standard:return dict(kind='nonstandard_unresolved',conservative_reachable=closure(rows,edges,0))
 # Interpret the mode0 path and solve the one mode1 equality without executing UI.
 bypc={r['PC']:r for r in rows};end=struct.unpack_from('<I',bytes.fromhex(rows[3]['hex']),4)[0]
 need(end in bypc and bypc[end]['opcode']==19,'independent genuine condition END')
 playing=closure(rows,edges,44)
 return dict(kind='standard_WORK_prefix',condition_mode=0,playback_mode=1,condition_path=[0,8,28,36,end],
  condition_accepts=bytes.fromhex(rows[2]['hex'])[4:]==bytes.fromhex('01000020'),playback_entry=44,
  playback_reachable=playing,playback_ENDs=[p for p in playing if bypc[p]['opcode']==19],
  playback_issues=[i for i in issues if i['PC'] in playing],
  playback_dependency_families=sorted({catalog.family(bypc[p]['opcode']) for p in playing}))


def verify_function(f, raw, start, limit):
 need(f['start']==start and start<f['end']<=limit,'exact original function bounds')
 actual=[]
 for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[start-0x400000:limit-0x400000],start):
  actual.append(dict(va=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
  if i.mnemonic=='ret':break
 need(actual and actual[-1]['mnemonic']=='ret','independent ret boundary')
 end=actual[-1]['va']+len(bytes.fromhex(actual[-1]['hex']))
 expected=dict(start=start,end=end,sha256=sha(raw[start-0x400000:end-0x400000]),instructions=actual,
  direct_calls=[dict(va=i['va'],target=int(i['operands'],16)) for i in actual if i['mnemonic']=='call' and i['operands'].startswith('0x')])
 need(f==expected,'complete original function bytes, calls and canonical instructions')


def verify(d):
 need(set(d)=={'schema_version','scope','source','scripts','summary','dispatch','handoff','R3_complete','R4_complete','R5_complete','R6_complete'},'exact atlas envelope')
 need(d['schema_version']==1 and d['scope']==catalog.SCOPE,'honest static atlas scope')
 need(all(d[k] is False for k in ('R3_complete','R4_complete','R5_complete','R6_complete')),'incomplete global milestones')
 raw=SOURCE.read_bytes();need(sha(raw)=='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005','fixed original executable')
 source=d['source'];need(source['image']==catalog.terminal.ref(SOURCE.relative_to(ROOT).as_posix()),'exact image reference')
 need(len(source['functions'])==len(catalog.FUNCTIONS),'all task and continuation function records')
 for f,(a,b) in zip(source['functions'],catalog.FUNCTIONS):verify_function(f,raw,a,b)
 need(len(source['handler_reads'])==len(catalog.READS),'all audited fixed handler read spans')
 for h,(op,(a,b,n)) in zip(source['handler_reads'],catalog.READS.items()):
  need(set(h)=={'opcode','required_bytes','function'} and (h['opcode'],h['required_bytes'])==(op,n),'audited handler contract identity');verify_function(h['function'],raw,a,b)
 need(len(source['key_instructions'])==len(catalog.KEYS),'all exact handshake/clock/finalizer contracts')
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 for k,(va,pair) in zip(source['key_instructions'],catalog.KEYS.items()):
  i=next(md.disasm(raw[va-0x400000:va-0x400000+16],va,count=1))
  need((i.mnemonic,i.op_str)==pair and k==dict(va=va,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str),'key original instruction bytes')
 table=dict(pointer=0x60CA7C,slots=[2,5,8,11,14],selectors=[struct.unpack_from('<I',raw,0x20CA7C+s*4)[0] for s in (2,5,8,11,14)])
 need(source['selector_table']==table and table['selectors']==[1,2,3,4,5],'sourced selector table')
 need(source['script_phase_table']==dict(pointer=0x454EC2,targets=list(struct.unpack_from('<6I',raw,0x54EC2))),'original script phase jump table')
 need(source['task_phase_table']==dict(pointer=0x4547C2,targets=list(struct.unpack_from('<21I',raw,0x547C2))),'original 21-phase task jump table')
 need(source['task_phase_table']['targets'][20]==0x4547A1,'phase20 reaches original return1')
 need(set(source)=={'image','key_instructions','functions','handler_reads','selector_table','script_phase_table','task_phase_table'},'exact source proof fields')
 files=sorted(catalog.SCRIPTS.glob('*.BIN'));need(len(files)==len(d['scripts'])==45,'all original battle scripts')
 present=[];counts=Counter();statuses=Counter();standard=[];all_rows=[]
 for script,path in zip(d['scripts'],files):
  need(set(script)=={'name','source','routes'} and script['name']==path.name and script['source']==catalog.terminal.ref(path.relative_to(ROOT).as_posix()),'exact script identity')
  scanned=scan(path.read_bytes());need(len(script['routes'])==5,'all five candidate protocol slots')
  for r,(sub,selector) in zip(script['routes'],zip((2,5,8,11,14),(1,2,3,4,5))):
   base=dict(sub=sub,selector=selector,dynamic_scene_reachability_proven=False)
   if sub not in scanned:expected=dict(base,status='missing')
   elif scanned[sub] is None:expected=dict(base,status='empty_dmf')
   else:
    seg,rows=scanned[sub];edges,issues=control(rows,seg['code_end']-seg['code_start']);m=mode_contract(rows,edges,issues)
    expected=dict(base,status='present',segment=seg,commands=rows,edges=edges,issues=issues,modes=m)
    present.append(r);all_rows.extend(rows);counts.update(c['opcode'] for c in rows)
    if m['kind']=='standard_WORK_prefix':standard.append(m)
   need(r==expected,'independent raw script commands, control edges and dual-mode paths '+path.name+':'+str(sub));statuses[r['status']]+=1
 summary=dict(script_files=45,candidate_slots=225,present=statuses['present'],empty_dmf=statuses['empty_dmf'],missing=statuses['missing'],
  commands=len(all_rows),opcode_classes=len(counts),standard_prefixes=len(standard),condition_accepts=sum(m['condition_accepts'] for m in standard),
  condition_rejects=sum(not m['condition_accepts'] for m in standard),nonstandard=len(present)-len(standard),
  short_handler_reads=sum(c['short_handler_read'] for c in all_rows),CFG_issues=sum(len(r['issues']) for r in present),
  opcode_counts={str(k):v for k,v in sorted(counts.items())})
 need(d['summary']==summary,'independent corpus totals')
 need(d['dispatch']==[catalog.dispatch(raw,op) for op in sorted(counts)],'original opcode dispatcher provenance')
 handoff=catalog.frozen_handoff();need(d['handoff']==handoff,'frozen execution only and honest pending handoff')
 t4=next(s for s in d['scripts'] if s['name']=='T0004.BIN')
 for c in handoff['cases']:
  if c['selector']:
   r=next(r for r in t4['routes'] if r['sub']==c['sub']);need(r['selector']==c['selector'] and r['modes']['condition_accepts'],'actual predecessor selections bound to sourced playback')
 return dict(schema_version=1,summary=summary,independent_raw_container_and_CFG=True,complete_original_instruction_bytes_checked=True,
  inherited_execution_not_repeated=True,new_runtime_execution=False,task_exit_complete=False,rewards_complete=False,
  R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 data=(ROOT/a.report).read_bytes();d=json.loads(gzip.decompress(data) if a.report.endswith('.gz') else data)
 r=verify(d);r['source_report']=catalog.terminal.ref(a.report);catalog.terminal.save(a.out,r);print('verified 45 scripts / 225 candidate slots; no runtime completion claimed')
