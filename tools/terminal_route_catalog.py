"""Source-derived terminal playback routes; never executes a game callback."""
import argparse, gzip, json, struct
from collections import Counter
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_retained_portrait_catalog import commands, dispatch, SCRIPTS
from tools.battle_live_terminal_emulation import ROOT, SOURCE, need, sha, terminal

PARENT = 'analysis/battle-live-terminal-acceptance-v1-20261025.json'
PARENT_SHA = '60aaec25daa77241399b39cef372758a5ad90877479ad8654ce7107e717522bb'
SLOTS = (2, 5, 8, 11, 14)
SCOPE = 'Static candidate protocol routes; not scene reachability, callback execution, task exit or rewards completion'
FUNCTIONS = ((0x4539B0, 0x453D00), (0x453F10, 0x4547C2),
 (0x454AF0, 0x454BB0), (0x454CF0, 0x454EC2), (0x454EE0, 0x454F50),
 (0x4678C0, 0x467AB0), (0x4978C0, 0x497980), (0x497980, 0x497AA0),
 (0x497AA0, 0x497DF0), (0x497C50, 0x497C90), (0x4998B0, 0x499910), (0x499910, 0x499B5D))
# These are dependency families, not claims that every instruction blocks.
FAMILIES = {
 'VM_control': (8, 11, 19, 166, 167), 'VM_timer': (12,),
 'text_and_font': (17, 43, 44, 47, 48, 49, 50), 'confirmation_input': (51, 146),
 'presentation_objects': (20, 21, 23, 24, 26, 27, 29, 30, 31, 32, 33, 36, 40, 42, 55, 56),
 'world_script_work': (117, 118, 120, 136, 139, 140, 141, 142),
 'world_query_or_command': (113, 114, 129, 130, 137, 159),
 'global_state': (96, 100), 'unresolved_result_read': (148,)}
# Exact handler read spans independently corroborated by the disassembly below.
READS = {30: (0x4C61C0, 0x4C6330, 20), 129: (0x42E240, 0x42E340, 20),
 137: (0x42EBC0, 0x42EEF0, 32), 148: (0x4D0FB0, 0x4D1060, 16)}
KEYS = {
 0x4539EC: ('call', '0x454cf0'), 0x4539FB: ('call', '0x453f10'),
 0x453A0C: ('call', '0x46b470'), 0x453A1A: ('call', '0x432100'),
 0x454D8B: ('call', '0x4ce8f0'), 0x454E4B: ('mov', 'byte ptr [edx + 0x171], 1'),
 0x454E55: ('mov', 'byte ptr [eax + 0x172], 1'),
 0x454293: ('movsx', 'edx, byte ptr [ecx + 0x171]'),
 0x4542AD: ('mov', 'dword ptr [ecx + 0x38], 0xf'),
 0x454470: ('call', '0x415040'), 0x454636: ('call', '0x499910'),
 0x454793: ('call', '0x473860'), 0x4547A1: ('mov', 'eax, 1'),
 0x4679D3: ('mov', 'byte ptr [ecx + 0x108b3a], 0'),
 0x42D9BC: ('call', '0x4978c0'), 0x42D9C7: ('mov', 'byte ptr [ecx + 0x92e0], 1'),
 0x42DA56: ('call', '0x497980'), 0x42DA45: ('mov', 'byte ptr [edx + 0x92e0], 1'),
 0x4D0FD6: ('mov', 'edx, dword ptr [ecx + 8]'),
 0x4D1005: ('mov', 'eax, dword ptr [edx + 0xc]')}


def family(op):
 return next((k for k, v in FAMILIES.items() if op in v), 'unclassified')


def cell(data, offset):
 return struct.unpack_from('<I', data, offset)[0]


def function(raw, start, limit):
 rows = []
 for i in Cs(CS_ARCH_X86, CS_MODE_32).disasm(raw[start-0x400000:limit-0x400000], start):
  rows.append(dict(va=i.address, hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
  if i.mnemonic == 'ret': break
 need(rows and rows[-1]['mnemonic'] == 'ret', 'complete bounded function through original ret')
 end = rows[-1]['va'] + len(bytes.fromhex(rows[-1]['hex']))
 return dict(start=start, end=end, sha256=sha(raw[start-0x400000:end-0x400000]), instructions=rows,
  direct_calls=[dict(va=i['va'], target=int(i['operands'], 16)) for i in rows if i['mnemonic']=='call' and i['operands'].startswith('0x')])


def source_rules(raw):
 need(sha(raw) == '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005', 'fixed original executable')
 md = Cs(CS_ARCH_X86, CS_MODE_32); keys = []
 for va, pair in KEYS.items():
  i = next(md.disasm(raw[va-0x400000:va-0x400000+16], va, count=1))
  need((i.mnemonic, i.op_str) == pair, 'original exit contract instruction '+hex(va))
  keys.append(dict(va=va, hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
 table = [cell(raw, 0x60CA7C-0x400000+s*4) for s in SLOTS]
 need(table == [1, 2, 3, 4, 5], 'original selector protocol table')
 return dict(image=terminal.ref(SOURCE.relative_to(ROOT).as_posix()), key_instructions=keys,
  functions=[function(raw, *r) for r in FUNCTIONS],
  handler_reads=[dict(opcode=op, required_bytes=n, function=function(raw, a, b)) for op,(a,b,n) in READS.items()],
  selector_table=dict(pointer=0x60CA7C, slots=list(SLOTS), selectors=table),
  script_phase_table=dict(pointer=0x454EC2, targets=list(struct.unpack_from('<6I', raw, 0x454EC2-0x400000))),
  task_phase_table=dict(pointer=0x4547C2, targets=list(struct.unpack_from('<21I', raw, 0x4547C2-0x400000))))


def graph(rows, code_size):
 """Conservative local CFG. Runtime waits do not imply permanent termination."""
 valid={r['PC'] for r in rows}; edges=[]; issues=[]
 for r in rows:
  pc, op, n = r['PC'], r['opcode'], r['bytes']; b=bytes.fromhex(r['hex']); targets=[]
  if r['short_handler_read']:
   issues.append(dict(PC=pc, kind='handler_reads_beyond_declared_command')); continue
  if op == 19: continue
  if op == 8:
   if n != 20: issues.append(dict(PC=pc, kind='unsupported_conditional_encoding')); continue
   targets=[('condition_true', cell(b,16)), ('condition_false',pc+n)]
  elif op == 11:
   if n != 8: issues.append(dict(PC=pc, kind='unsupported_jump_encoding')); continue
   targets=[('jump',cell(b,4))]
  elif op in (0,1,2,3,4,9,10,15,16,52,53,54,172):
   issues.append(dict(PC=pc, kind='unsupported_control_opcode')); continue
  else: targets=[('advance',pc+n)]
  for kind,target in targets:
   if target not in valid: issues.append(dict(PC=pc, kind='falloff' if target==code_size else 'invalid_target', target=target))
   else: edges.append(dict(source=pc, target=target, kind=kind))
 return edges, issues


def reachable(rows, edges, start=0):
 seen=set(); todo=[start]; adjacency={r['PC']:[] for r in rows}
 for e in edges: adjacency[e['source']].append(e['target'])
 while todo:
  pc=todo.pop()
  if pc in seen or pc not in adjacency: continue
  seen.add(pc);todo.extend(adjacency[pc])
 return sorted(seen)


def modes(rows, edges, issues):
 """Precisely solve only the sourced four-command WORK protocol prefix."""
 standard=(len(rows)>=4 and [r['opcode'] for r in rows[:4]]==[167,8,166,11]
  and [r['bytes'] for r in rows[:4]]==[8,20,8,8]
  and bytes.fromhex(rows[0]['hex'])[4:]==bytes(4)
  and bytes.fromhex(rows[1]['hex'])[4:]==struct.pack('<4I',1,0,0x20000001,44)
  and cell(bytes.fromhex(rows[2]['hex']),4) in (0x20000000,0x20000001))
 if not standard: return dict(kind='nonstandard_unresolved', conservative_reachable=reachable(rows,edges))
 end=cell(bytes.fromhex(rows[3]['hex']),4);by_pc={r['PC']:r for r in rows}
 need(end in by_pc and by_pc[end]['opcode']==19, 'standard condition jump to genuine END')
 playback=reachable(rows,edges,44);condition=[0,8,28,36,end]
 return dict(kind='standard_WORK_prefix', condition_mode=0, playback_mode=1,
  condition_path=condition, condition_accepts=bool(cell(bytes.fromhex(rows[2]['hex']),4)&0xFFFFFFF),
  playback_entry=44, playback_reachable=playback,
  playback_ENDs=[pc for pc in playback if by_pc[pc]['opcode']==19],
  playback_issues=[i for i in issues if i['PC'] in playback],
  playback_dependency_families=sorted({family(by_pc[pc]['opcode']) for pc in playback}))


def route(raw, decoded, sub, selector):
 seg=next((s for s in decoded['segments'] if s['index']==sub),None)
 if seg is None:
  _,groups=terminal.package_offsets(raw);_,subs=terminal.package_offsets(raw,groups[0])
  return dict(sub=sub,selector=selector,status='empty_dmf' if sub<len(subs) else 'missing',dynamic_scene_reachability_proven=False)
 rows=[]
 for c in decoded['commands'][seg['first_command']:seg['first_command']+seg['command_count']]:
  b=raw[c['offset']:c['offset']+c['bytes']];op=c['opcode'];required=READS.get(op,(0,0,4))[2]
  rows.append(dict(c,hex=b.hex(),family=family(op),short_handler_read=len(b)<required,
   handler_required_bytes=required if op in READS else None))
 edges,issues=graph(rows,seg['code_end']-seg['code_start'])
 return dict(sub=sub,selector=selector,status='present',dynamic_scene_reachability_proven=False,
  segment=seg,commands=rows,edges=edges,issues=issues,modes=modes(rows,edges,issues))


def frozen_handoff():
 raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed live terminal acceptance');a=json.loads(raw)
 ref=a['independent_proof'];b=(ROOT/ref['path']).read_bytes();need(len(b)==ref['bytes'] and sha(b)==ref['sha256'],'frozen proof identity')
 proof=json.loads(b);rows=[]
 for c in proof['cases']:
  rows.append({k:c[k] for k in ('name','frames','selector','sub')})
 return dict(acceptance=dict(path=PARENT,sha256=PARENT_SHA),proof=ref,cases=rows,
  evidence_kind='frozen prior execution only; no new runtime execution',
  continuation=['consume original 4678C0 pause request; keep world/event state alive',
   'run original 454CF0 with real world-script work 497AA0/498310',
   'complete original VM presentation and confirmation waits to END',
   'observe original 454CF0 phase5 writing task171/172',
   'continue original 453F10 phases15..20, real result animation and overlay',
   'observe natural 473860 then original outer task exit, reward and school handoff'],
  new_runtime_execution=False,original_outer_scheduler_connected=False,terminal_playback_complete=False,
  task_exit_complete=False,rewards_complete=False)


def summarize(scripts):
 routes=[r for s in scripts for r in s['routes']];present=[r for r in routes if r['status']=='present']
 rows=[c for r in present for c in r['commands']];stand=[r for r in present if r['modes']['kind']=='standard_WORK_prefix']
 return dict(script_files=len(scripts),candidate_slots=len(routes),present=len(present),
  empty_dmf=sum(r['status']=='empty_dmf' for r in routes),missing=sum(r['status']=='missing' for r in routes),
  commands=len(rows),opcode_classes=len({c['opcode'] for c in rows}),
  standard_prefixes=len(stand),condition_accepts=sum(r['modes']['condition_accepts'] for r in stand),
  condition_rejects=sum(not r['modes']['condition_accepts'] for r in stand),nonstandard=len(present)-len(stand),
  short_handler_reads=sum(c['short_handler_read'] for c in rows),
  CFG_issues=sum(len(r['issues']) for r in present),
  opcode_counts={str(k):v for k,v in sorted(Counter(c['opcode'] for c in rows).items())})


def build():
 raw=SOURCE.read_bytes();source=source_rules(raw);scripts=[]
 for path in sorted(SCRIPTS.glob('*.BIN')):
  data=path.read_bytes();decoded=commands(data)
  scripts.append(dict(name=path.name,source=terminal.ref(path.relative_to(ROOT).as_posix()),
   routes=[route(data,decoded,s,i+1) for i,s in enumerate(SLOTS)]))
 need(len(scripts)==45,'all 45 installed battle scripts')
 summary=summarize(scripts)
 return dict(schema_version=1,scope=SCOPE,source=source,scripts=scripts,summary=summary,
  dispatch=[dispatch(raw,int(op)) for op in summary['opcode_counts']],handoff=frozen_handoff(),
  R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args()
 r=build();terminal.save(a.out,r);print(json.dumps(r['summary'],ensure_ascii=False))
