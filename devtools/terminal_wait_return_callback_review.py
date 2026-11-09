"""Read-only, bounded audit of the frozen self-helper failure and guest DLLs."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import capstone
import pefile

ROOT=Path(__file__).resolve().parents[1]
WORKER=ROOT/'.venv-audit/native-worker'
HASHES={
 'ntdll.dll':'2761f133cac12188ed380666104527884b2f89dab918bc5082692ca1b7f341e6',
 'wow64.dll':'0724e69cd73787d56011bbf958265761ccb4878754b0d4752282efccf7c7e656',
 'wow64cpu.dll':'6d3e9d039c22b58c577435ef0209d43668ef2003e284be9980e4ad1289045a66',
}

def need(v,m):
 if not v:raise ValueError(m)

def audit(dll_dir, source):
 images={};identities=[]
 for name,expected in HASHES.items():
  p=dll_dir/name;b=p.read_bytes();digest=hashlib.sha256(b).hexdigest()
  need(digest==expected,'fixed actual guest DLL '+name)
  images[name]=pefile.PE(data=b)
  identities.append(dict(path=str(p),bytes=len(b),sha256=digest))
 excerpts=[]
 def excerpt(name,start,end):
  p=images[name];raw=p.get_data(start,end-start)
  mode=capstone.CS_MODE_32 if name=='ntdll.dll' else capstone.CS_MODE_64
  rows=list(capstone.Cs(capstone.CS_ARCH_X86,mode).disasm(raw,start))
  need(sum(x.size for x in rows)==len(raw),'complete bounded decode')
  excerpts.append(dict(module=name,start_rva=start,end_rva=end,hex=raw.hex(),
   instructions=[dict(rva=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)for i in rows]))
  return rows
 n=images['ntdll.dll'];need(n.get_data(0x73bf0,5)==bytes.fromhex('b804000d00'),'unaltered wait turbo selector 13')
 excerpt('ntdll.dll',0x73bf0,0x73bff)
 cpu=images['wow64cpu.dll'];need(cpu.get_qword_at_rva(0x36d0+13*8)-cpu.OPTIONAL_HEADER.ImageBase==0x1b46,'actual table[13] target')
 need(cpu.get_data(0x1669,7)==bytes.fromhex('4c8d3d60200000'),'r15 points at actual table RVA36d0')
 excerpt('wow64cpu.dll',0x1669,0x1670)
 excerpt('wow64cpu.dll',0x1779,0x17af)
 path=excerpt('wow64cpu.dll',0x1b46,0x1bc6)
 need([(i.address,i.op_str)for i in path if i.mnemonic=='call']==[(0x1b51,'0x1ce0')],'fast path only calls native syscall trampoline')
 need([i.op_str for i in path if i.mnemonic=='jb']==['0x1b91'],'both return paths inside audited bytes')
 need(path[-1].mnemonic=='iretq','alternate state-reset returns through IRET')
 trampoline=excerpt('wow64cpu.dll',0x1ce0,0x1cf7)
 need(any(i.address==0x1cf1 and i.mnemonic=='syscall' for i in trampoline),'real kernel syscall')
 excerpt('wow64.dll',0xd6d2,0xd6ff)
 excerpt('wow64.dll',0x6f02,0x6f18)
 excerpt('wow64.dll',0x1ca79,0x1ca98)
 excerpt('wow64.dll',0x21f5c,0x2202e)
 wow=images['wow64.dll']
 need(wow.get_data(0xd6e2,6)==bytes.fromhex('480588040000'),'actual PEB32+488 Wow64Info')
 need(wow.get_data(0x6f09,3)==bytes.fromhex('8b4808'),'callback is Wow64Info+8 = PEB32+490')
 raw=source.read_bytes();need(len(raw)<262144,'bounded self-helper source')
 r=json.loads(raw.decode('utf-8-sig'));data=bytes.fromhex(r['records_hex'])
 need(r['kind']=='owned_wow64_wait_callback_preflight' and r['accepted'] is False,'self-helper only')
 need(r['source_sha256']=='d5c7b832ea6f084efc0f1448aa483b52ce98605f436df43ce4c6fda565de750a','frozen v1 helper')
 need(r['template_sha256']=='7c6d229240478a8f15427df9360ca1ff718147b31e8a712900d710f03e6feb74','frozen v1 machine code')
 need(r['registration_status']==r['unregistration_status']==0 and r['returns']==[0,0,0,258],'real self-helper native results')
 need(r['nt_wait_before']==r['nt_wait_after'] and r['code_before']==r['code_after'],'frozen original stub and owned code')
 need(r['error'] is None and not r['cleanup_errors'] and r['handles_closed'] and r['buffers_released'] and r['watchdog_disarmed'],'normal bounded cleanup')
 need(len(data)==32768 and struct.unpack_from('<5I',data)==(0,0,0,4,0),'zero matching callback records; four real post-return records')
 post=[struct.unpack_from('<9I',data,20480+k*1024+32)for k in range(4)]
 need([p[7]for p in post]==[0,0,0,258],'actual post-return EAX')
 return dict(kind='owned_wow64_wait_callback_static_failure_review',accepted=False,
  self_helper_preflight_passed=False,original_program_observed=False,full_original_abi=False,
  native_wait_relay_supported=False,dlls=identities,
  source=dict(path=str(source),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),
  matched_callback_records=0,actual_self_helper_post_returns=[0,0,0,258],
  expected_pc_rva=0x73bfc,wow64_info_peb32_offset=0x488,callback_peb32_offset=0x490,
  wow64_info_pointer_global_rva=0x4e280,teb64_wow64_info_pointer_offset=0x14d0,
  turbo_selector=13,turbo_table_rva=0x36d0,turbo_path_rva=0x1b46,native_syscall_rva=0x1cf1,
  callback_setup_rva=0x21f5c,post_return_ecx=[p[6]for p in post],
  loaded_wow64cpu_base_authenticated=False,
  post_ecx_used_only_as_consistency_hint=True,
  conclusion='The fixed NtWait selector13 uses the audited direct wow64cpu syscall/return path; it bypasses the wow64.dll callback dispatcher. Successful registration and native EAX returns do not establish a callback observation.',
  forbidden_substitutions=['changing the original NtWait selector/stub','disabling turbo thunks to claim original equivalence','inferring full context from sparse returns'],
  excerpts=excerpts)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--dll-dir',type=Path,default=WORKER/'guest-system-dlls')
 p.add_argument('--source',type=Path,default=WORKER/'wait-return-self-v1-20261109/report.json')
 p.add_argument('--out',type=Path)
 a=p.parse_args();r=audit(a.dll_dir,a.source);text=json.dumps(r,indent=2)
 if a.out:
  with a.out.open('x',encoding='utf-8')as f:f.write(text+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in ('excerpts','dlls','forbidden_substitutions')},indent=2))
