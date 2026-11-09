"""Extend the frozen v1 static audit with actual kernel class40 dispatch.

Reads only files. No process, callback registration, DLL load or VM operation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import capstone
import pefile
from devtools import terminal_wait_return_callback_review as v1

KERNEL='ntoskrnl-5669b9b8bfcf.exe'
KERNEL_SHA='5669b9b8bfcf20f08b7d1d65dc2deccbf836279c0e3f66722d72ad33ee7f672a'


def audit(dll_dir,source):
 r=v1.audit(dll_dir,source)
 raw=(dll_dir/KERNEL).read_bytes()
 v1.need(hashlib.sha256(raw).hexdigest()==KERNEL_SHA,'fixed actual guest kernel')
 pe=pefile.PE(data=raw)
 exports={s.name.decode():s.address for s in pe.DIRECTORY_ENTRY_EXPORT.symbols if s.name}
 v1.need(exports['NtSetInformationProcess']==0x6f4170,'actual exported class40 setter')
 v1.need(exports['PsGetCurrentProcess']==0x3292b0 and exports['PsGetProcessWow64Process']==0x2bb740,
         'export-backed process identity helpers')
 v1.need(pe.get_data(0x6f8638+39,1)==b'\x1a' and pe.get_dword_at_rva(0x6f8538+26*4)==0x6f5ce5,
         'information class40 actual two-level dispatch')
 checks={
  0x6f5daa:'e80135c3ff488bf8', # call exported PsGetCurrentProcess; RDI=current
  0x6f5e05:'4883b98005000000', # target Wow64 pointer
  0x6f5e0f:'440fb7816c090000', # target machine type
  0x6f5e2b:'4c8b8780050000', # R8=current process Wow64 pointer
  0x6f5e32:'4584c90f85e3000000', # target WOW64 -> alternate branch
  0x6f5f1e:'4d85c00f84b5000000', # current not WOW64 -> NOT_SUPPORTED
  0x6f5fdc:'41bebb0000c0',
  0x6f5fae:'898190040000', # same-bitness branch writes PEB32+490 only
  0x6f5eab:'488998d8030000', # native-target branch writes KPROCESS+3d8
 }
 for address,expected in checks.items():
  v1.need(pe.get_data(address,len(bytes.fromhex(expected)))==bytes.fromhex(expected),'exact kernel branch '+hex(address))
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
 excerpts=[]
 for start,end in [(0x6f4461,0x6f448c),(0x6f5ce5,0x6f5efd),(0x6f5f1e,0x6f5ff3),
                   (0x3292b0,0x3292c1),(0x2bb740,0x2bb752)]:
  data=pe.get_data(start,end-start);rows=list(cs.disasm(data,start))
  v1.need(sum(i.size for i in rows)==len(data),'complete kernel bounded decode')
  excerpts.append(dict(start_rva=start,end_rva=end,hex=data.hex(),instructions=[
   dict(rva=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)for i in rows]))
 r['kind']='owned_wow64_wait_callback_static_failure_review_v2'
 r['kernel_identity']=dict(path=str(dll_dir/KERNEL),bytes=len(raw),sha256=KERNEL_SHA)
 r['kernel_excerpts']=excerpts
 r['native64_callback_for_this_wow64_target_supported']=False
 r['native64_rejection']=dict(method='static actual-kernel original bytes; not a new native registration attempt',
  process_information_class=40,version=0,native_target_store_rva=0x6f5eab,
  wow64_target_branch_rva=0x6f5e32,native_caller_reject_branch_rva=0x6f5f1e,
  status_rva=0x6f5fdc,status=0xc00000bb,
  target_conditions='target +0x580 nonzero and Machine +0x96c is 0x14c or 0x1c4',
  caller_condition='PsGetCurrentProcess +0x580 is zero for native x64 caller',
  same_wow64_caller='writes target PEB32+0x490, not KPROCESS+0x3d8',
  no_alternate_version_or_length_attempted=True)
 r['next_mechanism_requirement']=(
  'Find and independently qualify an observation mechanism at the unchanged real wow64cpu NtWait return '
  'that captures and restores the required full original x86 state and real stack without #DB, '
  'the rejected WOW64 callback route, original code/IAT/selector changes, disabling turbo thunks, '
  'or fabricated return values/contexts. Start only with an owned bounded helper; sparse native '
  'returns, synthetic reconstruction and this diagnosis do not satisfy original A2/A3 or full replay.')
 return r


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--dll-dir',type=Path,default=v1.WORKER/'guest-system-dlls')
 p.add_argument('--source',type=Path,default=v1.WORKER/'wait-return-self-v1-20261109/report.json')
 p.add_argument('--out',type=Path)
 a=p.parse_args();r=audit(a.dll_dir,a.source)
 if a.out:
  with a.out.open('x',encoding='utf-8')as f:json.dump(r,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in r.items()if k not in ('excerpts','kernel_excerpts','dlls','forbidden_substitutions')},indent=2))
