"""Assemble an immutable corpus from a retained complete case and a new case.

Cases always own independent native lifetimes.  This resumes corpus production,
never a guest CPU, stack, memory snapshot or native handle.
"""
import hashlib,importlib,json,os,re,struct,sys,tempfile,types,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools import terminal_battle_exit_process as host
from tools import terminal_battle_exit_emulation as e
ROOT=e.ROOT
PRIOR='analysis/terminal-battle-exit-prefix-source-process-review-v3-20261102.json'
CATALOG='analysis/terminal-battle-exit-prefix-source-local-evidence-v3-20261102.json'

def normalized_managed_image(raw):
 """Exclude build IDs only; compare all IL, data, resources and metadata."""
 data=bytearray(raw);u16=lambda p:struct.unpack_from('<H',data,p)[0];u32=lambda p:struct.unpack_from('<I',data,p)[0]
 pe=u32(0x3C);e.need(data[pe:pe+4]==b'PE\0\0' and u16(pe+24)==0x10B,'original x86 PE32 managed helper')
 table=pe+24+u16(pe+20);sections=[(u32(p+12),max(u32(p+8),u32(p+16)),u32(p+20)) for p in range(table,table+40*u16(pe+6),40)]
 def offset(rva):
  hits=[pos+rva-va for va,size,pos in sections if va<=rva<va+size];e.need(len(hits)==1,'unique managed image RVA');return hits[0]
 cli=offset(u32(pe+24+96+14*8));metadata=offset(u32(cli+8));e.need(data[metadata:metadata+4]==b'BSJB','CLI metadata signature')
 cursor=(metadata+16+u32(metadata+12)+3)&~3;count=u16(cursor+2);cursor+=4;streams={}
 for _ in range(count):
  start,size=u32(cursor),u32(cursor+4);end=data.index(0,cursor+8);name=bytes(data[cursor+8:end]).decode('ascii');streams[name]=(metadata+start,size);cursor=(end+4)&~3
 guid,guid_size=streams['#GUID'];tables,_=streams['#~'];valid=struct.unpack_from('<Q',data,tables+8)[0];cursor=tables+24;rows={}
 for bit in range(64):
  if valid&(1<<bit):rows[bit]=u32(cursor);cursor+=4
 e.need(rows.get(0)==1 and guid_size==16 and not(data[tables+6]&3),'one Module row and sole small-heap build MVID')
 e.need(u16(cursor)==0 and u16(cursor+4)==1 and u16(cursor+6)==0 and u16(cursor+8)==0,'Module MVID is sole GUID; no EnC identifiers')
 # This compiler also spells the same MVID in its synthesized static-array
 # holder type name. Normalize only that exact full #Strings entry.
 strings,size=streams['#Strings'];heap=bytes(data[strings:strings+size]);name=b'<PrivateImplementationDetails>{'+str(uuid.UUID(bytes_le=bytes(data[guid:guid+16]))).upper().encode()+b'}'+bytes(1)
 matches=[m.start() for m in re.finditer(re.escape(name),heap)]
 e.need(len(matches)<=1,'at most one compiler-generated MVID type name')
 if matches:
  at=matches[0];e.need(at==0 or heap[at-1]==0,'complete generated type name entry boundary');begin=strings+at+len(b'<PrivateImplementationDetails>{');data[begin:begin+36]=b'0'*36
 data[pe+8:pe+12]=bytes(4);data[guid:guid+16]=bytes(16)
 return bytes(data)

def helper_identity(exe,src):
 directory=Path(tempfile.mkdtemp(prefix='bex-helper-equivalence-',dir=ROOT/'.venv-audit'))
 prefix=directory.relative_to(ROOT/'.venv-audit').as_posix()+'/'+exe.stem
 fresh,build=e.overlay.platform.build(ROOT/src,prefix)
 old=normalized_managed_image(exe.read_bytes());new=normalized_managed_image(fresh.read_bytes());e.need(old==new,'every helper byte matches frozen source rebuild except timestamp and MVID '+src)
 return dict(rebuilt_helper=host.ref(fresh),build=build,normalized_sha256=hashlib.sha256(old).hexdigest(),excluded_fields=['PE_COFF_TimeDateStamp','sole_Module_MVID','same_MVID_in_compiler_generated_type_name_if_present'],all_other_bytes_equal=True,historical_executable_hash_recorded=False)

def scan_case(path,block_bytes=1048576):
 """Hash exact serialized bytes and collect only new forward write PCs."""
 h=hashlib.sha256();state=0;tail=b'';pcs=set();head=b'';last=b'';size=0
 markers=(b'"terminal_battle_exit_prefix":',b'"writes":[')
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(block_bytes),b''):
   h.update(block);size+=len(block);head=(head+block)[:4096];last=(last+block)[-16:]
   if state==3:continue
   buf=tail+block;tail=b''
   while state<2:
    token=markers[state];at=buf.find(token)
    if at<0:tail=buf[-len(token):];break
    buf=buf[at+len(token):];state+=1
   if state==2:
    end=buf.find(b']');part=buf if end<0 else buf[:end]
    pcs.update(int(m.group(1)) for m in re.finditer(rb'"pc":([0-9]+)(?=,)',part))
    if end>=0:state=3
    else:tail=buf[-128:]
 match=re.match(rb'\{"input":(\{[^{}]*\})',head)
 e.need(match and last.rstrip().endswith(b'}') and state==3 and pcs,'complete retained case serialization and scoped forward writes')
 return dict(path=Path(path).resolve().relative_to(ROOT).as_posix(),bytes=size,sha256=h.hexdigest()),pcs,json.loads(match.group(1))

def retained_inputs():
 prior=json.loads((ROOT/PRIOR).read_text());catalog=json.loads((ROOT/CATALOG).read_text())
 e.need(prior['exit_code']!=0 and prior['implementation_unchanged'],'preserved prior corpus run failed without changing inputs')
 for path,identity in prior['implementation_end'].items():e.need(host.ref(path)==identity,'unchanged actual retained-case runtime input '+path)
 candidates=[x for x in catalog['entries'] if x['path'].endswith('/case-0.json')]
 e.need(len(candidates)==1 and candidates[0]['byte_equal'],'one exact backed-up complete retained case')
 original=candidates[0];path=ROOT/original['path'];identity,pcs,case=scan_case(path)
 e.need(identity=={k:original[k] for k in ('path','bytes','sha256')} and case==e.overlay.parent.corpus()[0],'exact retained first selected case bytes and identity')
 e.need(Path(original['backup_path']).stat().st_size==identity['bytes'],'retained external backup still exists')
 helpers={}
 for kind,suffix in [('CRT','crt'),('GPU','gpu')]:
  exe=ROOT/'.venv-audit'/('terminal-battle-exit-'+suffix+'.exe');src='tools/terminal_battle_exit_'+('crt_platform.cs' if kind=='CRT' else 'd3d8_platform.cs')
  e.need(exe.is_file() and exe.stat().st_mtime_ns<=path.stat().st_mtime_ns and e.overlay.platform.crt.old.machine(exe)==0x14C,'existing x86 helper predates retained case '+kind)
  helpers[kind]=dict(source=src,source_sha256=host.ref(src)['sha256'],helper_sha256=host.ref(exe)['sha256'],machine=0x14C,existing_binary_reused=True,source_equivalence=helper_identity(exe,src))
 return path,identity,pcs,helpers

def produce():
 e.need(sys.argv[1]=='--out' and len(sys.argv)==3,'explicit immutable resume output');out=sys.argv[2];e.need(not(ROOT/out).exists(),'fresh resumed corpus')
 path,identity,pcs,build=retained_inputs();case_root=ROOT/'.venv-audit';work=Path(tempfile.mkdtemp(prefix='bex-cases-'+Path(out).name.replace('.json.gz','')+'-',dir=case_root));complete=False
 version=Path(out).name.removeprefix('terminal-battle-exit-prefix-source-').removesuffix('-20261102.json.gz')
 inputs='analysis/terminal-battle-exit-prefix-source-resume-input-'+version+'-20261102.json'
 host.save(ROOT/inputs,dict(retained_case=identity,prior_process=host.ref(PRIOR),prior_catalog=host.ref(CATALOG),retained_forward_write_PCs=sorted(pcs),runtime_source=host.ref('tools/terminal_battle_exit_emulation.py'),helper_build=build,guest_or_native_state_restored=False))
 try:
  print('retained complete native case verified; running missing timeout case from construction',flush=True)
  row=e.run_case(e.overlay.parent.corpus()[1],ROOT/'.venv-audit/terminal-battle-exit-crt.exe',ROOT/'.venv-audit/terminal-battle-exit-gpu.exe');pcs.update(w['pc'] for w in row['terminal_battle_exit_prefix']['writes']);second=work/'case-1.json';encoder=json.JSONEncoder(ensure_ascii=False,separators=(',',':'))
  with second.open('xb') as f:
   for text in encoder.iterencode(row):f.write(text.encode('utf8'))
  del row
  e.recorded_write_PCs[:]=sorted(pcs)
  provenance=[dict(name='neutral_running',kind='retained_complete_native_case',retained_artifact=identity,prior_process=host.ref(PRIOR),prior_catalog=host.ref(CATALOG)),dict(name='timeout_before_combat',kind='new_complete_native_case',runtime_source=host.ref('tools/terminal_battle_exit_emulation.py'))]
  e.save_source_cases(out,dict(schema_version=1,source_contract=e.source_contract(),helper_build=build,case_provenance=provenance,resume_inputs=host.ref(inputs),guest_or_native_state_restored=False),[str(path),str(second)],dict(R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False));complete=True
 finally:
  e.finish_case_files(work,complete)
  if not complete:print('incomplete resume cases retained locally',work,flush=True)

def prepare(mode):
 e.need(mode=='source','resume only produces source corpus');implementation=host.prepare(mode);importlib.import_module('tools.terminal_battle_exit_resume');return implementation

def run_module(module,run_name):
 e.need(module=='tools.terminal_battle_exit_emulation' and run_name=='__main__','exact resumed original source producer');produce()

if __name__=='__main__':
 # Reuse the exact supervisor, receipts, import inventory and external byte
 # preservation algorithm; bind only this producer and its actual script path.
 scope=dict(host.main.__globals__,__file__=__file__,prepare=prepare,runpy=types.SimpleNamespace(run_module=run_module))
 types.FunctionType(host.main.__code__,scope)()
