"""Reproduce the narrow original-byte plan from locally retained PE modules."""
import argparse
import hashlib
import json
from pathlib import Path
import pefile


def make(directory):
    extraction=json.loads((directory/'extraction.json').read_bytes())
    for row in extraction['modules']:
        path=directory/Path(row['path']).name
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('module identity')
    kernel_path=directory/'System32-ntoskrnl.exe'
    kernel=kernel_path.read_bytes()
    expected=json.loads((directory/'kernel-extraction.json').read_bytes())
    if hashlib.sha256(kernel).hexdigest()!=expected['sha256']:
        raise ValueError('kernel identity')
    wow=pefile.PE(str(directory/'System32-wow64cpu.dll'))
    nt=pefile.PE(str(directory/'SysWOW64-ntdll.dll'))
    kp=pefile.PE(data=kernel)
    wait=next(x for x in nt.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'NtWaitForSingleObject')
    entry=0x96710
    if nt.get_data(entry,2)!=b'\xff\x25':raise ValueError('transition opcode')
    if int.from_bytes(wow.get_data(0x3738,8),'little')-wow.OPTIONAL_HEADER.ImageBase!=0x1b46:
        raise ValueError('selector13 target')
    if any(0x1650<=x.rva<0x1cf7 and x.type for b in wow.DIRECTORY_ENTRY_BASERELOC for x in b.entries):
        raise ValueError('trace range unexpectedly relocated')
    clears=[0x41a2b6,0x428e72]
    code=bytes.fromhex('660fefc0660fefc9660fefd2660fefdb660fefe4660fefed')
    if any(kp.get_data(a,len(code))!=code for a in clears):raise ValueError('PXOR candidates')
    return dict(accepted=False,wow_text_rva=0x1650,wow_text_hex=wow.get_data(0x1650,0x1cf7-0x1650).hex(),
        wow_table_rva=0x36d0,ntwait_rva=wait.address,nt_entry_rva=entry,
        nt_slot_rva=int.from_bytes(nt.get_data(entry+2,4),'little')-nt.OPTIONAL_HEADER.ImageBase,
        kernel_sections=[dict(raw=s.PointerToRawData,size=s.SizeOfRawData,rva=s.VirtualAddress)for s in kp.sections],
        kernel_clear_rvas=clears,kernel_sha256=expected['sha256'],kernel_path=kernel_path.as_posix())


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    with a.out.open('x',encoding='utf8')as f:json.dump(make(a.directory),f,indent=2)
