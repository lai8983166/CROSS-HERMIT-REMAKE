"""Original task-slot setup, class title and live duplicate-window branch."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools import school_main_context as parent
from tools.school_main_context import ROOT,SOURCE,SOURCE_SHA256,BASE,Cs,CS_ARCH_X86,CS_MODE_32,dword,store

ENTRY=0x49DE15
TITLE=0x7A2628
TITLE_BYTES=256
INSTANCE=0x7A2728
HINSTANCE=0x12340000  # Explicit inherited scalar, not a live Windows module.
FIND_SLOT=0x59232C
WINDOW_ENTRY=0x450350
EXIT_ENTRY=0x49E092
RANGES={ENTRY:0x49DECB,0x421660:0x4216BB,0x4293E0:0x429436,0x450290:0x4502C2,0x56CE80:0x56CE83}
STOPS={'tasks':0x49DE2C,'query':0x49DE53}
TITLE_TEXT=b'Cross Hermit\0'


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('window original source SHA')
    checks={0x49DE1E:('call','0x421660'),0x49DE26:('mov','dword ptr [0x7a2728], edx'),
        0x49DE38:('call','dword ptr [0x592294]'),0x49DE4E:('call','0x4293e0'),
        0x429406:('call','dword ptr [0x59232c]'),0x49DE55:('je','0x49de5c'),
        0x49DE57:('jmp','0x49e092'),0x49DE66:('call','0x450290'),
        0x4502B3:('mov','dword ptr [eax + 0x1108], ecx'),0x49DEC6:('call','0x450350')}
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    for at,op in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=op:raise ValueError('window original instruction')
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    desc=struct.unpack_from('<5I',raw,0x5FD5E0-BASE);thunk=dword(raw,desc[0]+FIND_SLOT-BASE-desc[4])
    if raw[thunk+2:].split(b'\0',1)[0]!=b'FindWindowA':raise ValueError('window actual import descriptor')
    if raw[0x598748-BASE:0x598748-BASE+len(TITLE_TEXT)]!=TITLE_TEXT:raise ValueError('window original class literal')
    return dict(source_image_sha256=SOURCE_SHA256,parent_source_contract=parent.source_contract(),instructions=proof,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        import_identity=dict(slot=hex(FIND_SLOT),descriptor='0x5fd5e0',dll='USER32.dll',symbol='FindWindowA',arguments=2,return_va='0x42940c'),
        declared_instance_scalar=HINSTANCE,instance_is_live_module=False,class_literal_hex=TITLE_TEXT.hex(),
        task_slots=dict(offset=0x64,count=32,stride=8,zero_bytes=256),title_buffer=dict(va=hex(TITLE),bytes=TITLE_BYTES),
        no_duplicate_pending=dict(va=hex(WINDOW_ENTRY),return_va='0x49decb',receiver=parent.OWNER,args=[0,0,1024,768,0x90000000,1]),
        duplicate_pending=dict(va=hex(EXIT_ENTRY),instruction_executed=False),
        actual_query_is_read_only=True,returned_HWND_not_owned=True,query_result_fabricated=False,
        full_WinMain=False,window_creation_body_executed=False,retained_VM_advanced=False)


def project_owner(before,phase,duplicate):
    if len(before)!=parent.BACKING:raise ValueError('window complete main-context backing')
    raw=bytearray(before);raw[0x64:0x164]=bytes(256)
    if phase=='branch' and not duplicate:
        store(raw,0x1108,0)  # Inherited declared command-line scalar, never dereferenced here.
        store(raw,0x5C,0x69);store(raw,0x60,0x67)
    return bytes(raw)


def project_image(before,phase):
    raw=bytearray(before);store(raw,INSTANCE-BASE,HINSTANCE)
    if phase!='tasks':raw[TITLE-BASE:TITLE-BASE+len(TITLE_TEXT)]=TITLE_TEXT
    return bytes(raw)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable window source required')
    path.write_text(json.dumps(source_contract(),indent=2)+'\n',encoding='utf8',newline='\n')
