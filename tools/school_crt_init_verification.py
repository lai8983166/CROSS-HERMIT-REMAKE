"""Independent full native CRT snapshots, instrumentation and debug-graph audit."""
import gzip,json,struct,os
from functools import lru_cache
from pathlib import Path
import pefile
from tools import school_crt_init_capture as source

ROOT=source.ROOT;need=source.need;sha=source.sha;word=source.word
ACCEPTANCE='analysis/school-retained-crt-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='4433b1e2299794fa9e11a45003f12838d5cddb97694050f073beb478e688efed'

@lru_cache(maxsize=32)
def exported_entry(path,name,target):
 p=pefile.PE(str(path));need(p.FILE_HEADER.Machine==0x14c,'real x86 OS module');e=next(e for e in p.DIRECTORY_ENTRY_EXPORT.symbols if e.name==name.encode());need(e.forwarder is None,'actual direct native export');base=target-e.address;need(base>0 and base%65536==0,'actual module base and export RVA');return bytes(p.get_memory_mapped_image(ImageBase=base)[e.address:e.address+16]),e.address,base

def instrument(a):
 before,request,after=[bytes.fromhex(a[k]) for k in ('before_context_hex','requested_debug_context_hex','after_context_hex')];need(len(before)==len(request)==len(after)==716,'complete WOW64 contexts');need(word(request)==0x10010,'only debug context requested');need(request[28:]==before[28:],'no requested GPR/FPU/segment/EFLAGS write');need(before[28:192]==after[28:192] and before[196:]==after[196:],'all architectural non-debug registers unchanged');d=word(before,192)^word(after,192);need(d in (0,2) and a['returned_EFLAGS_reserved_bit1_xor']==d,'only returned reserved bit1 normalization');need([word(request,o) for o in (4,8,12,16)]==a['targets'] and word(request,20)==0 and word(request,24)==a['mask'],'exact bounded hardware-register request');need(a['general_state_unchanged']is True,'honest register instrumentation')

def protocol(c):
 need(c['error']is None and c['target'] in source.BREAKPOINTS and len(c['captures'])==1,'successful one-boundary original probe')
 for k in ('source_memory_written','general_registers_written','debugger_reply_substituted','retained_heap_restored','R3_complete'):need(c[k]is False,'no fake initialized/retained/native state '+k)
 need(c['original_sha256']==source.ORIGINAL_SHA and c['source_sha256']==source.SOURCE_SHA,'original source identity');need(c['parent_pid']!=c['child_pid'] and c['parent_pid']>0 and c['child_pid']>0,'two exclusively owned original processes');need(c['desktop']['private'] and c['desktop']['switched']is c['desktop']['input_sent']is False,'private non-interactive desktop')
 cleanup=c['cleanup'];need(cleanup['explicit_probe_termination'] and cleanup['parent_signaled'] and cleanup['all_debug_process_exits_observed'] and cleanup['private_desktop_closed'] and sorted(cleanup['members_before_probe_termination'])==sorted([c['parent_pid'],c['child_pid']]) and cleanup['members_after_cleanup']==[] and cleanup['original_game_normal_shutdown']is False,'probe termination is explicit and all owned resources close')
 for a in c['debug_register_instrumentation']:instrument(a)
 child=[a for a in c['debug_register_instrumentation'] if a['role']=='child'];need(child and all(a['pid']==c['child_pid'] and a['targets']==[c['target'],0,0,0] and a['mask']==1 and word(bytes.fromhex(a['before_context_hex']),24)==0 for a in child),'only unused child hardware slots armed')

def verify_case(c):
 protocol(c);s=c['captures'][0];target=c['target'];need(s['label']==source.LABELS[target] and s['EIP']==target and s['pid']==c['child_pid'] and s['first_instruction_executed']is False,'original child pending boundary');ctx=bytes.fromhex(s['full_context_hex']);need(len(ctx)==716 and word(ctx,184)==target and word(ctx,4)==target and word(ctx,20)&1 and word(ctx,24)&1,'actual child hardware exception before first instruction');w=c['parent_waits'][s['parent_wait_index']];raw=bytes.fromhex(w['state_hex']);need(w['child_context_hex']==s['full_context_hex'] and len(raw)==96 and w['state']==word(raw)==8 and word(raw,4)==s['pid'] and word(raw,8)==s['tid'] and word(raw,12) in (0x80000004,0x4000001e) and word(raw,24)==target,'original parent NtWait return contains exact owned child single-step event');need(word(bytes.fromhex(w['parent_return_context_hex']),176)==0,'actual successful native wait return')
 text=bytes.fromhex(s['source_text']['hex']);data=bytes.fromhex(s['original_data']['hex']);need(s['source_text']==dict(pointer=0x401000,bytes=0x191000,sha256=sha(text),hex=text.hex()) and text==source.SOURCE.read_bytes()[0x1000:0x192000],'entire original text identity');need(s['original_data']==dict(pointer=0x5ff000,bytes=0x20d000,sha256=sha(data),hex=data.hex()) and len(data)==0x20d000,'entire original data identity/extent');g={n:word(data,p-0x5ff000) for n,p in source.FIELDS.items()};need(g==s['globals'],'all captured globals derived from complete data section');need(g['debug_flag']==1 and g['break_request']==0xffffffff and g['lock9']==0x80a4b0 and g['allocation_hook']==0x578120,'source default flags/hook/lock')
 stack=bytes.fromhex(s['stack_hex']);need(s['stack_pointer']==word(ctx,196) and len(stack)==256,'complete original stack input window');table=data[0x761df0-0x5ff000:0x761eb0-0x5ff000];need(table.hex()==s['lock_table_hex'] and [word(table,i*4) for i in (1,9,13,17)]==[0x80a480,0x80a4b0,0x80a4c8,0x80a498],'source static lock table')
 need(s['static_locks']==[dict(pointer=p,hex=data[p-0x5ff000:p-0x5ff000+24].hex()) for p in (0x80a480,0x80a498,0x80a4b0,0x80a4c8)],'all recorded static lock bytes')
 slots=[0x59212c,0x59227c,0x592144,0x59218c,0x592258];names=['HeapCreate','RtlInitializeCriticalSection','RtlAllocateHeap','HeapValidate','HeapFree'];need([i['slot'] for i in s['actual_import_targets']]==slots,'all recorded actual IAT roles')
 for i,name in zip(s['actual_import_targets'],names):
  filename=i['mapped_path'].split(chr(92))[-1].lower();need(filename==('ntdll.dll' if name.startswith('Rtl') else 'kernel32.dll') and (chr(92)+'windows'+chr(92)+'syswow64'+chr(92)) in i['mapped_path'].lower(),'actual owned original x86 OS module');p=Path(os.environ['WINDIR'])/'SysWOW64'/filename;entry,_,_=exported_entry(str(p),name,i['target']);need(entry.hex()==i['entry_hex'],'actual complete native import entry equals relocated OS export')
 for name,e in c['parent_exports'].items():
  need(name in ('NtDebugContinue','NtWaitForDebugEvent') and e['symbol']==name and e['module'].lower()=='ntdll.dll' and sha(Path(e['module_path']).read_bytes())==e['module_sha256'],'original parent API module provenance');_,rva,module=exported_entry(e['module_path'],name,e['target']);need((e['RVA'],e['base'])==(rva,module),'original parent actual export identity')
 entry=w['entry'];ec=bytes.fromhex(entry['parent_context_hex']);es=bytes.fromhex(entry['parent_stack_hex']);rc=bytes.fromhex(w['parent_return_context_hex']);need(word(ec,184)==c['parent_exports']['NtWaitForDebugEvent']['target'] and len(es)==20 and word(es,16)==entry['output'] and word(rc,184)==word(es),'natural parent native wait entry/return and original output pointer')
 nodes=s['debug_graph'];prev=0;count=0;last=0;requests=[];occupied=[]
 for n in nodes:
  raw=bytes.fromhex(n['raw_hex']);header=struct.unpack('<7I',raw[:28]);need(header==(n['prev'],n['next'],n['file'],n['line'],n['size'],n['kind'],n['request']) and len(raw)==n['size']+36 and raw[28:32]==raw[-4:]==bytes([0xfd])*4,'every complete native header/payload/guard');need(n['prev']==prev and n['pointer']>0 and n['size']<=0x200000,'native linked debug allocation');need(all(not (lo<n['pointer']+len(raw) and n['pointer']<hi) for lo,hi in occupied),'nonoverlapping original blocks');occupied.append((n['pointer'],n['pointer']+len(raw)));prev=n['pointer'];last=n['next'];count+=n['size'];requests.append(n['request']);p=n['file'];name=bytes.fromhex(n['source_name_hex']);need(data[p-0x5ff000:p-0x5ff000+len(name)+1]==name+bytes(1) if 0x5ff000<=p<0x80c000 else source.SOURCE.read_bytes()[p-0x400000:p-0x400000+len(name)+1]==name+bytes(1),'original allocation source file name')
 need(not nodes and g['debug_first']==g['debug_last']==0 or nodes and nodes[0]['pointer']==g['debug_first'] and nodes[-1]['pointer']==g['debug_last'] and last==0,'entire first/last debug graph');need(all(nodes[i]['next']==nodes[i+1]['pointer'] for i in range(len(nodes)-1)) and requests==sorted(set(requests)) and count==g['current_bytes'],'all list links/request order/current accounting')
 if target==0x49dd70:
  need((len(nodes),g['next_request'],g['total_bytes'],g['current_bytes'],g['high_water_bytes'],g['heap_mode'])==(142,144,32670,18376,30494,1) and all(n['kind']==2 for n in nodes),'actual pre-WinMain CRT allocation graph, not game initialization');need(requests==[i for i in range(1,144) if i!=3],'complete request sequence, one freed temporary allocation');need(g['heap_token']>0 and all((n['pointer']&~65535)==g['heap_token'] for n in nodes),'captured debug blocks in original fresh heap segment')
 else:
  need(all(g[k]==0 for k in ('debug_first','debug_last','total_bytes','current_bytes','high_water_bytes')) and g['next_request']==1 and nodes==[],'observed original empty cold debug ledger')
  if target in (0x5713c0,0x57b9ea):need(g['heap_token']==g['heap_mode']==0,'heap state before original source store')
  if target==0x57b9ea:need(word(ctx,176)>0 and word(ctx,176)%65536==0,'actual HeapCreate return before original store')
  if target==0x576f60:need(g['heap_token']>0 and g['heap_mode']==1,'original heap init completed before lock init')
  need(all(word(table,i*4)==0 for i in range(48) if i not in (1,9,13,17)) and data[0x80a480-0x5ff000:0x80a4e0-0x5ff000]==bytes(96),'actual cold static locks, not invented lock bytes')
 return dict(round=c['round'],target=target,label=s['label'],pid=s['pid'],source_text_bytes=len(text),source_data_bytes=len(data),native_debug_blocks=len(nodes),native_current_bytes=count,native_request_sequence=requests,cold_ledger_observed=target!=0x49dd70,original_first_instruction_executed=False,parent_debug_reply_changed=False,probe_termination_is_game_shutdown=False)

def verify(r):
 need(r['schema_version']==4 and len(r['cases'])==8 and [(c['round'],c['target']) for c in r['cases']]==[(i,t) for i in range(2) for t in source.BREAKPOINTS],'two rounds/four independent original boundaries');need(r['sampler_source_sha256']==sha((ROOT/'tools/school_crt_init_probe.py').read_bytes()) and r['base_source_sha256']==sha((ROOT/'tools/school_crt_init_capture.py').read_bytes()),'actual capture source identity');need([x['path'] for x in r['source_manifest']]==['tools/school_crt_init_probe.py','tools/school_crt_init_capture.py','tools/school_crt_init_nested.py','tools/school_startup_inputs.py'],'entire capture dependency manifest')
 for x in r['source_manifest']:need(sha((ROOT/x['path']).read_bytes())==x['sha256'],'capture dependency '+x['path'])
 need(sha((ROOT/ACCEPTANCE).read_bytes())==ACCEPTANCE_SHA,'prior accepted lifecycle pin');cases=[verify_case(c) for c in r['cases']];need(r['cases'][0]['captures'][0]['original_data']==r['cases'][4]['captures'][0]['original_data'],'two independent cold data sections identical')
 return dict(schema_version=1,cases=cases,native_probes=8,native_pre_WinMain_blocks=284,original_cold_ledger_and_static_lock_bytes_observed=True,full_original_text_and_data_verified=True,full_native_CRT_startup_instruction_trace=False,retained_heap_restored=False,retained_integration=False,R3_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 result=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())));out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('eight original native CRT boundaries independently verified',flush=True)
