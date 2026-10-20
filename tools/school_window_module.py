"""Owned code-free PE resource module and original icon/class initialization source."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
import pefile
from tools import school_window_geometry as geometry
from tools.school_window_geometry import ROOT,SOURCE,SOURCE_SHA256,BASE,Cs,CS_ARCH_X86,CS_MODE_32,dword,store

RESOURCE_DLL=ROOT/'.venv-audit/school-window-icons-v1.dll'
RESOURCE_RVA=0x1000
STOPS={'icons':0x450443,'class_ready':0x45047D}
RANGES={0x450416:0x45047D,0x56CE80:0x56CE83}
IMPORTS={0x5923CC:('LoadIconA',2,[0x45041C,0x450439]),
    0x5923C8:('LoadCursorA',2,[0x450452]),0x592084:('GetStockObject',1,[0x450466])}


@lru_cache(maxsize=1)
def resource_bytes():
    geometry.resource_contract()
    pe=pefile.PE(data=SOURCE.read_bytes());result={}
    for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if t.id in (3,14):
            for n in t.directory.entries:
                for lang in n.directory.entries:
                    d=lang.data.struct;result[(t.id,n.id,lang.id)]=pe.get_data(d.OffsetToData,d.Size)
    if set(result)!={(3,5,1041),(14,157,1041)}:raise ValueError('module exact original icon resources')
    return result


def build_bytes():
    resources=resource_bytes();icon=resources[(3,5,1041)];group=resources[(14,157,1041)]
    section=bytearray(160+len(icon)+len(group))
    def directory(at,count):struct.pack_into('<IIHHHH',section,at,0,0,0,0,0,count)
    for at,count in ((0,2),(32,1),(56,1),(80,1),(104,1)):directory(at,count)
    for at,key,value in ((16,3,0x80000020),(24,14,0x80000038),(48,5,0x80000050),
            (72,157,0x80000068),(96,1041,128),(120,1041,144)):struct.pack_into('<II',section,at,key,value)
    struct.pack_into('<4I',section,128,RESOURCE_RVA+160,len(icon),0,0)
    struct.pack_into('<4I',section,144,RESOURCE_RVA+160+len(icon),len(group),0,0)
    section[160:160+len(icon)]=icon;section[160+len(icon):]=group
    raw_size=(len(section)+511)&~511;image_size=(RESOURCE_RVA+len(section)+4095)&~4095
    header=bytearray(512);header[:2]=b'MZ';store(header,0x3C,0x80);header[0x80:0x84]=b'PE\0\0'
    struct.pack_into('<HHIIIHH',header,0x84,0x14C,1,0,0,0,224,0x2102)
    o=0x98;struct.pack_into('<H',header,o,0x10B)
    store(header,o+8,raw_size);store(header,o+24,RESOURCE_RVA);store(header,o+28,0x10000000)
    store(header,o+32,4096);store(header,o+36,512)
    struct.pack_into('<HH',header,o+40,6,0);struct.pack_into('<HH',header,o+48,6,0)
    store(header,o+56,image_size);store(header,o+60,512);struct.pack_into('<HH',header,o+68,2,0x100)
    for offset,value in ((72,0x100000),(76,0x1000),(80,0x100000),(84,0x1000),(92,16)):store(header,o+offset,value)
    struct.pack_into('<II',header,o+96+2*8,RESOURCE_RVA,len(section))
    struct.pack_into('<8s6I2HI',header,o+224,b'.rsrc\0\0\0',len(section),RESOURCE_RVA,raw_size,512,0,0,0,0,0x40000040)
    return bytes(header)+bytes(section)+bytes(raw_size-len(section))


def inspect_module(raw):
    if raw!=build_bytes():raise ValueError('module deterministic PE bytes')
    pe=pefile.PE(data=raw)
    if pe.OPTIONAL_HEADER.AddressOfEntryPoint or pe.OPTIONAL_HEADER.SizeOfCode or len(pe.sections)!=1 or pe.sections[0].Characteristics&0x20000000:
        raise ValueError('module must have no entry or executable section')
    if any(d.VirtualAddress or d.Size for i,d in enumerate(pe.OPTIONAL_HEADER.DATA_DIRECTORY) if i!=2):raise ValueError('module no imports/exports/TLS/other directories')
    rows=[]
    for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        for n in t.directory.entries:
            for lang in n.directory.entries:
                d=lang.data.struct;b=pe.get_data(d.OffsetToData,d.Size)
                if b!=resource_bytes()[(t.id,n.id,lang.id)]:raise ValueError('module exact source resource bytes')
                rows.append(dict(type=t.id,id=n.id,language=lang.id,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
    return dict(machine=0x14C,entry_point=0,executable_sections=0,sections=1,resource_entries=rows,
        bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),builder='deterministic resource-only PE32; original code and imports omitted')


def build_resource():
    if RESOURCE_DLL.exists():raise ValueError('fresh immutable resource DLL required')
    raw=build_bytes();proof=inspect_module(raw);RESOURCE_DLL.write_bytes(raw)
    return proof


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('module original source SHA')
    proof=[];md=Cs(CS_ARCH_X86,CS_MODE_32)
    for at,op in {0x450416:('call','dword ptr [0x5923cc]'),0x450423:('mov','dword ptr [ebp - 0x2c], eax'),
            0x450433:('call','dword ptr [0x5923cc]'),0x450440:('mov','dword ptr [ebp - 0x18], eax'),
            0x45044C:('call','dword ptr [0x5923c8]'),0x450460:('call','dword ptr [0x592084]'),
            0x450470:('mov','dword ptr [ebp - 0x20], 0'),0x45047D:('call','dword ptr [0x592408]')}.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=op:raise ValueError('module original instruction')
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,parent_source_contract=geometry.source_contract(),instructions=proof,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        resource_module=inspect_module(build_bytes()),original_resource=geometry.resource_contract(),
        declared_instance='fresh owned actual module handle before first49DDC9 instruction',
        legacy_validation_view='Explicit scalar substitution at enumerated input-derived locations only; raw actual snapshots retained and checked before validation view; no CPU/runtime patch',
        icon_id=157,cursor_args=[0,32512],stock_brush_id=4,stops={k:hex(v) for k,v in STOPS.items()},
        class_registration_executed=False,window_created=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable module source evidence required')
    out.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
