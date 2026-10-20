"""Original450350 geometry and partial WNDCLASSEXA before unexecuted LoadIconA."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
import pefile
from tools import school_main_window as window
from tools.school_main_window import ROOT,SOURCE,SOURCE_SHA256,BASE,Cs,CS_ARCH_X86,CS_MODE_32,dword,store

parent=window.parent
ENTRY=0x450350
ENTRY_SP=parent.SP-28
FRAME_BP=ENTRY_SP-4
FRAME_SP=ENTRY_SP-148
RECT_AT=FRAME_BP-20
CLASS_AT=FRAME_BP-68
CLIENT_OFFSET=0x8BC
CLIENT_RECT=struct.pack('<4i',0,0,1024,768)
STYLE=0x90000000
STOPS={'rect':0x45039C,'adjust':0x4503D5,'class':0x450416}
RANGES={ENTRY:STOPS['class'],0x56CE80:0x56CE83}
IMPORTS={0x5923F8:('SetRect',5,0x450395),0x5923FC:('AdjustWindowRect',3,0x4503CE)}
ORIGINAL='CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
ORIGINAL_SHA='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7'


@lru_cache(maxsize=1)
def resource_contract():
    rows=[]
    for path in ('analysis/hermit_game.exe',ORIGINAL):
        raw=(ROOT/path).read_bytes();expected=SOURCE_SHA256 if path.startswith('analysis/') else ORIGINAL_SHA
        if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('geometry original module identity')
        pe=pefile.PE(data=raw);icons=[]
        for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if t.id not in (3,14):continue
            for e in t.directory.entries:
                for lang in e.directory.entries:
                    data=lang.data.struct;blob=pe.get_data(data.OffsetToData,data.Size)
                    icons.append(dict(type=t.id,id=e.id,language=lang.id,rva=hex(data.OffsetToData),bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest()))
                    if path.startswith('analysis/') and t.id==14 and e.id==157:
                        group=blob
        rows.append(dict(path=path,bytes=len(raw),sha256=expected,machine=pe.FILE_HEADER.Machine,icons=icons))
    if rows[0]['icons']!=rows[1]['icons']:raise ValueError('geometry source/original icon resource identity')
    if struct.unpack_from('<3H',group)!=(0,1,1):raise ValueError('geometry original icon group header')
    width,height,colors,reserved,planes,bpp,size,image_id=struct.unpack_from('<4B2HIH',group,6)
    if (width,height,planes,bpp,size,image_id)!=(32,32,1,8,2216,5):raise ValueError('geometry original group157 image5')
    return dict(modules=rows,group_id=157,language=1041,image_id=image_id,width=width,height=height,
        bits_per_pixel=bpp,image_bytes=size,group_hex=group.hex(),module_loaded=False,icon_loaded=False,
        inherited_instance_scalar_is_not_a_module=True)


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('geometry original source SHA')
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    checks={0x45038F:('call','dword ptr [0x5923f8]'),0x4503C8:('call','dword ptr [0x5923fc]'),
        0x4503D5:('mov','dword ptr [ebp - 0x44], 0x30'),0x4503EA:('mov','dword ptr [ebp - 0x3c], 0x424980'),
        0x4503F1:('mov','ecx, dword ptr [0x7a2728]'),0x45040A:('push','0x9d'),
        0x450416:('call','dword ptr [0x5923cc]')}
    for at,op in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=op:raise ValueError('geometry original instruction')
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    imports=[];desc=struct.unpack_from('<5I',raw,0x5FD5E0-BASE)
    for slot,(name,count,ret) in IMPORTS.items():
        t=dword(raw,desc[0]+slot-BASE-desc[4])
        if raw[t+2:].split(b'\0',1)[0]!=name.encode():raise ValueError('geometry original import')
        imports.append(dict(slot=hex(slot),descriptor='0x5fd5e0',dll='USER32.dll',symbol=name,arguments=count,return_va=hex(ret)))
    return dict(source_image_sha256=SOURCE_SHA256,parent_source_contract=window.source_contract(),instructions=proof,imports=imports,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        client_rectangle_hex=CLIENT_RECT.hex(),style=STYLE,menu=0,frame=dict(entry_SP=ENTRY_SP,EBP=FRAME_BP,ESP=FRAME_SP,local_rectangle=RECT_AT,class_structure=CLASS_AT),
        stops={k:hex(v) for k,v in STOPS.items()},WNDCLASSEXA_bytes=48,initialized_class_dwords=7,
        uninitialized_class_dwords=5,original_callback='0x424980',icon_resource=resource_contract(),
        LoadIconA_executed=False,window_registered=False,window_created=False,retained_VM_advanced=False)


def partial_class():
    raw=bytearray(b'\xcc'*48)
    for offset,value in {0:48,4:0,8:0x424980,12:0,16:0,20:window.HINSTANCE,40:window.TITLE}.items():store(raw,offset,value)
    return bytes(raw)


def project_owner(before):
    if len(before)!=parent.BACKING:raise ValueError('geometry complete owner backing')
    after=bytearray(before);after[CLIENT_OFFSET:CLIENT_OFFSET+16]=CLIENT_RECT
    return bytes(after)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable geometry source required')
    path.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
