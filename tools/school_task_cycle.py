"""Source projection of captured null-IME reset and task playback admission."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_world_task_start import SOURCE,BASE,SOURCE_SHA256,ROOT,TACT,WORK,MAIN,INPUT,TASK_REGIONS,TASK_NATIVE,call_protocol as task_calls,source_contract as task_source
from tools.school_world_script import SCRIPT_REGIONS,VM

REGIONS=TASK_REGIONS+tuple(r for r in SCRIPT_REGIONS if r not in TASK_REGIONS)
RESET_NATIVE=((0x425DE0,0x425E5A),(0x425E60,0x425ECE),(0x425C70,0x425CBC),(0x56CD4A,0x56CD50))
PHASES=('reset1','phase2','reset2','vm_entry')
PREVIOUS={'phase2':'reset1','reset2':'phase2','vm_entry':'reset2'}

@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('task cycle original source SHA')
    desc=struct.unpack_from('<5I',raw,0x1FD6D0);name=raw[desc[3]:].split(b'\0',1)[0]
    if name!=b'IMM32.dll' or desc[4]+BASE!=0x5920CC:raise ValueError('task cycle original IMM32 descriptor')
    thunk=struct.unpack_from('<I',raw,desc[0]+8*4)[0];symbol=raw[thunk+2:].split(b'\0',1)[0]
    if symbol!=b'ImmGetOpenStatus':raise ValueError('task cycle exact original import symbol')
    checks={0x49E5A4:('call','0x425de0'),0x425E1E:('jle','0x425e2f'),0x425E34:('call','0x425e60'),0x425E3F:('mov','byte ptr [ecx + 0x630], 0'),0x425E87:('call','0x425c70'),0x425E8E:('je','0x425ea5'),0x425EA9:('je','0x425eb8'),0x425C94:('call','0x56cd4a'),0x56CD4A:('jmp','dword ptr [0x5920ec]'),0x454D76:('mov','byte ptr [ecx], al'),0x454D8B:('call','0x4ce8f0')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('task cycle exact operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,parent_task_source=task_source(),functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RESET_NATIVE],instructions=proof,import_identity=dict(descriptor='0x5fd6d0',original_thunk=hex(desc[0]+BASE),slot='0x5920ec',symbol=symbol.decode(),dll=name.decode()),platform_response=dict(context=0,ImmGetOpenStatus_result=0,declared_response=True,live_OS_observed=False),scope='Declared reset/task polls from first-task return; unexecuted normal VM entry; no outer/main/OS frame authority')


def call_protocol(phase):
    if phase not in PHASES:raise ValueError('task cycle known phase')
    if phase.startswith('reset'):return [0x3000000,0x425E39,0x425E8C,0x425C99]
    return task_calls() if phase=='phase2' else task_calls()[:-2]+[0x454D90]


def project(phase,before):
    source_contract()
    if phase not in PHASES or [(r['pointer'],r['bytes']) for r in before]!=list(REGIONS) or any(len(bytes.fromhex(r['hex']))!=r['bytes'] for r in before):raise ValueError('task cycle full owned regions/phase')
    out=deepcopy(before);d={r['pointer']:bytearray.fromhex(r['hex']) for r in out};t=d[TACT];k=d[INPUT];w=d[WORK+0x2490]
    want_phase=1 if phase=='reset1' or phase=='phase2' else 2
    if t[0x43]!=1 or t[0x44]!=want_phase or t[0x59]!=1 or struct.unpack_from('<I',t,0x48)[0]!=1 or k[0x630]!=(255 if phase.startswith('reset') else 0) or struct.unpack_from('<I',k,8)[0] or k[0x528] or w[9] or w[0x18]:raise ValueError('task cycle finite null-context/phase/input/effect guard')
    if phase.startswith('reset'):k[0x630]=0
    else:
        k[0x630]=255;k[0x428:0x628]=bytes(512);k[0x63C:0x67C]=bytes(64);k[0x634:0x638]=bytes(4);d[TACT+0x117F20][0]=0
        if phase=='phase2':t[0x44]=2
    for r in out:r['hex']=d[r['pointer']].hex()
    return dict(after=out,task_phase=t[0x44],input_flag=k[0x630],task_return=0 if phase!='vm_entry' else None,normal_VM_executed=False,live_input_sampled=False,platform_response_declared=phase.startswith('reset'))
