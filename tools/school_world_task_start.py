"""Original first selected-task setup with bounded existing text-length adapter."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_world_script import ROOT,SOURCE,SOURCE_SHA256,BASE,TACT,TASK,WORK

MAIN=0x1080000;INPUT=MAIN+0x180
TASK_REGIONS=((TACT,400),(INPUT,0x680),(TACT+0x117F20,1),(WORK+0x2490,64))
TASK_NATIVE=((0x454CF0,0x454EC2),(0x457830,0x45788C),(0x425ED0,0x425F50),(0x425A10,0x425A48),(0x425A50,0x425ABB),(0x426250,0x4262A0),(0x426110,0x426156),(0x426190,0x4261D6),(0x497AA0,0x497C43),(0x498310,0x498739))

@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('task start original source SHA')
    checks={0x4539EC:('call','0x454cf0'),0x4539FB:('call','0x453f10'),0x453A0C:('call','0x46b470'),0x454D19:('call','0x454c40'),0x454D2F:('call','0x457830'),0x425F34:('mov','byte ptr [ecx + 0x630], 0xff'),0x425A78:('call','dword ptr [0x5922c4]'),0x454D65:('mov','byte ptr [ecx], al'),0x497AC6:('je','0x497c2d'),0x498339:('je','0x498725')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('task start source operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    from tools.school_tactical_resources_emulation import FILE_IMPORTS
    if FILE_IMPORTS[0x5922C4]!=('lstrlenA',4):raise ValueError('task start inherited import identity')
    return dict(source_image_sha256=SOURCE_SHA256,functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in TASK_NATIVE],instructions=proof,platform_adapter=dict(name='lstrlenA',slot='0x5922c4',callsite='0x425a78',return_va='0x425a7e',callee_pop_bytes=4,reads_existing_buffer_only=True),scope='One declared454CF0 after world185; native phase0 setup/empty buffer reset/inactive fade and board; no OS input sampling, playback or complete outer task')


def call_protocol():return [0x3000000,0x454D1E,0x454D34,0x457860,0x457871,0x425A35,0x425A91,0x42627F,0x425A99,0x426142,0x425AA1,0x4261C2,0x454EAA,0x454EAF]


def project(inputs,before):
    source_contract();expected={'main_owner':MAIN,'input_pointer':INPUT,'strlen_slot':0x5922C4,'text_pointer':INPUT+0x528,'work_pointer':WORK,'driver':'declared_next_454CF0_after_original_world185'}
    if set(inputs)!=set(expected)|{'strlen_target'} or any(inputs[k]!=v for k,v in expected.items()) or type(inputs['strlen_target']) is not int or not 0<inputs['strlen_target']<=0xFFFFFFFF:raise ValueError('task start finite captured inputs')
    if [(r['pointer'],r['bytes']) for r in before]!=list(TASK_REGIONS) or any(len(bytes.fromhex(r['hex']))!=r['bytes'] for r in before):raise ValueError('task start complete owned buffers')
    d={r['pointer']:bytearray.fromhex(r['hex']) for r in before};task=d[TACT];keyboard=d[INPUT];work=d[WORK+0x2490]
    if task[0x43]!=1 or task[0x44] or task[0x59]!=1 or struct.unpack_from('<I',task,0x48)[0]!=1 or keyboard[0x630] or keyboard[0x528] or work[9] or work[0x18]:raise ValueError('task start phase0 empty captured text and inactive effects required')
    keyboard[0x630]=255;keyboard[0x428:0x628]=bytes(512);keyboard[0x63C:0x67C]=bytes(64);keyboard[0x634:0x638]=bytes(4);d[TACT+0x117F20][0]=0;task[0x5C:0x60]=bytes(4);task[0x44]=1
    out=deepcopy(before)
    for r in out:r['hex']=d[r['pointer']].hex()
    return dict(after=out,task_phase=1,task_status=1,task_return=0,VM_playback_executed=False,input_sampled=False,strlen_result=0)
