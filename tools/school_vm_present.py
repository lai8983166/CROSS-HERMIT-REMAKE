"""Source rules for first normal VM opcode and native overlay resource binding."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_task_cycle import REGIONS as PARENT_REGIONS
from tools.school_world_script import ROOT,SOURCE,SOURCE_SHA256,BASE,TASK,TACT,VM,WORK,SCRIPT,SCRIPT_SHA

STACK=0x2000000;RETURN=0x3000000;BASE_SP=STACK+0xFF00;OVERLAY=VM+0x94E8;BANK=TASK+0x844+20*8
REGIONS=PARENT_REGIONS+((0,4),(BANK,8),(TASK+0x196C,2),(TASK+0x1970,2),(TASK+0xB210,4))
PHASES=('command','packet','draw');PREVIOUS={'packet':'command','draw':'packet'}
NATIVE=((0x4CE8F0,0x4D03B7),(0x42FC60,0x42FCCA),(0x496DC0,0x496DE7),(0x4C1F40,0x4C1FAD),(0x4D29E0,0x4D2B86),(0x4D2CA0,0x4D2DD0),(0x4075E0,0x40770E),(0x403620,0x4036C0),(0x41F930,0x41F9D5),(0x420990,0x4209B7),(0x408C00,0x408C27),(0x4077C0,0x40782A),(0x407870,0x4079C0),(0x41F5A0,0x41F66A),(0x56CEC0,0x56CF18),(0x4142B0,0x4142DD),(0x4079C0,0x407A0E),(0x407A50,0x407AC3))

@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes();script=SCRIPT.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(script).hexdigest()!=SCRIPT_SHA:raise ValueError('VM present source/script identity')
    if struct.unpack_from('<HHI',script,452)!=(167,8,0):raise ValueError('VM present first source command')
    if struct.unpack_from('<I',raw,0x4D03CF-BASE+(167-5)*4)[0]!=0x4CFE22 or struct.unpack_from('<I',raw,0x4D2B86-BASE+4)[0]!=0x4D2A45:raise ValueError('VM present native dispatch tables')
    checks={0x4CFE35:('call','0x42fc60'),0x4C1F89:('mov','dword ptr [ecx + edx*4 + 0x38], eax'),0x4CFEE0:('mov','edx, dword ptr [ebp - 0x14]'),0x4D024A:('call','0x4d29e0'),0x4D2A78:('call','0x4d2ca0'),0x4D2CDE:('call','0x4075e0'),0x4D2D52:('call','0x407870'),0x4078FF:('call','0x41f5a0'),0x41F5DA:('jg','0x41f5e0'),0x41F5DC:('xor','eax, eax'),0x4D2D3E:('mov','eax, dword ptr [ebp + 0x10]'),0x4D2D36:('mov','dx, word ptr [ebp + 0xc]'),0x407AAB:('call','0x407ad0')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('VM present source operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    functions=[]
    for a,b in NATIVE:
        if a==0x56CEC0:frame=0;args=3
        else:
            seq=list(md.disasm(raw[a-BASE:b-BASE],a));ret=next(i for i in seq if i.mnemonic=='ret');local=next(i for i in seq[:18] if i.mnemonic=='sub' and i.op_str.startswith('esp, '));seh=12 if a in (0x4D2CA0,0x4075E0) else 0;frame=4+int(local.op_str.split(', ')[1],0)+12+seh;args=int(ret.op_str,0)//4 if ret.op_str else 0
        functions.append(dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest(),frame=frame,args=args))
    return dict(source_image_sha256=SOURCE_SHA256,script_sha256=SCRIPT_SHA,command=dict(offset=452,opcode=167,advance=8,variable=0),functions=functions,instructions=proof,resource_request=dict(group=20,index=0,layer=51,captured_count=1),scope='Original first VM command and native overlay/constructor/resource binding to unexecuted draw request; no fabricated resource or original helper stub, no VM/task/render completion')


def layout():
    f={int(r['va'],16):r['frame'] for r in source_contract()['functions']};vm=BASE_SP-100;overlay=vm-f[0x4CE8F0]-64-4;kind=overlay-f[0x4D29E0]-36-4;resource=kind-f[0x4D2CA0]-8-4
    return dict(vm=vm,overlay=overlay,kind=kind,packet=kind-4-0x90,seh=kind-4-12,resource=resource,draw=resource-f[0x4079C0]-12-f[0x407A50]-12,drawbp=resource-f[0x4079C0]-16)


def call_protocol(phase):
    if phase=='command':return [0x454D90,0x4CFE3A,0x42FC88,0x42FCB4,0x4D024F]
    if phase=='packet':return [0x4D024F,0x4D2A7D,0x4D2CE3,0x40761A,0x403645,0x41F955,0x41F9BE,0x40762C,0x4D2CFB,0x4D2D57]
    if phase=='draw':return [0x4D2D57,0x407904,0x4079A5,0x4D2D9E,0x4079FB,0x407AB0]
    raise ValueError('VM present known phase')


def packet_project(flag=0x40,texture=None,clock=0):
    if flag not in (0x40,0xC0):raise ValueError('VM present finite packet flag')
    p=bytearray([204])*128;p[:0x34]=bytes(0x34);struct.pack_into('<I',p,0x34,25)
    for o in range(0x38,0x46,2):struct.pack_into('<H',p,o,0)
    for o in (0x48,0x4C,0x50,0x54,0x5C,0x60,0x68,0x6C):struct.pack_into('<I',p,o,0)
    struct.pack_into('<I',p,0x4C,TASK);struct.pack_into('<H',p,0x58,flag);struct.pack_into('<I',p,0x5C,1);p[0x64:0x68]=bytes([128,128,128,255])
    struct.pack_into('<HH',p,0x70,100,100)
    for o in range(0x74,0x80,2):struct.pack_into('<H',p,o,0)
    struct.pack_into('<H',p,0x76,51)
    if flag==0xC0:
        if not texture or texture['bytes']!=84 or len(bytes.fromhex(texture['hex']))!=84:raise ValueError('VM present complete captured texture input')
        t=bytes.fromhex(texture['hex']);p[0x34:0x38]=t[0x34:0x38];p[0x3C:0x40]=t[0x3C:0x40];struct.pack_into('<I',p,0x48,texture['pointer']);struct.pack_into('<I',p,0x28,clock);struct.pack_into('<HH',p,0x38,20,30);struct.pack_into('<4H',p,0x78,424,24,444,54)
    return p.hex()


def project(phase,inputs,before):
    source_contract();l=layout()
    if phase not in PHASES or [(r['pointer'],r['bytes']) for r in before]!=list(REGIONS) or any(len(bytes.fromhex(r['hex']))!=r['bytes'] for r in before):raise ValueError('VM present full owned buffers/phase')
    d={r['pointer']:bytearray.fromhex(r['hex']) for r in before};vm=d[VM];task=d[TACT];bank=d[BANK];pointer=struct.unpack_from('<I',task,0x64)[0];texture=inputs.get('texture_record')
    expected=dict(script_pointer=pointer,script_sha256=SCRIPT_SHA,driver='continuous_original_task_VM',texture_record=texture)
    if inputs!=expected or not isinstance(texture,dict) or set(texture)!={'pointer','bytes','hex'} or texture['pointer']!=int.from_bytes(bank[:4],'little') or texture['bytes']!=84 or len(bytes.fromhex(texture['hex']))!=84 or bytes.fromhex(texture['hex'])[0x2C:0x30]==b'\xcd'*4:raise ValueError('VM present captured source texture input')
    if struct.unpack_from('<I',vm,0x10)[0]!=pointer+452 or bytes(vm[4:6])!=b'\x01\x01' or task[0x43]!=1 or task[0x44]!=2 or task[0x59]!=1 or vm[0x92E0] or vm[0x92E1] or vm[0x93E2]:raise ValueError('VM present selected VM/task provenance')
    if struct.unpack_from('<I',bank,4)[0]!=1 or d[WORK][0]!=1 or struct.unpack_from('<I',vm,0x1C)[0]!=(0 if phase=='command' else 8) or struct.unpack_from('<H',vm,0x20)[0]:raise ValueError('VM present finite command/resource state')
    if int.from_bytes(d[0],'little')!=(0 if phase in ('command','packet') else l['seh']):raise ValueError('VM present actual SEH chain')
    out=deepcopy(before)
    if phase=='command':
        struct.pack_into('<I',vm,0x3C,1);struct.pack_into('<I',vm,0x1C,8);struct.pack_into('<HH',vm,0x22,167,8);old=struct.unpack_from('<I',d[0x7A4E18])[0];struct.pack_into('<II',d[0x7A4E18],0,(old+1)&0xFFFFFFFF,0)
    else:d[0][:]=struct.pack('<I',l['seh'])
    for r in out:r['hex']=d[r['pointer']].hex()
    x=int.from_bytes(d[TASK+0x196C],'little');y=int.from_bytes(d[TASK+0x1970],'little')
    if phase=='command':pending=dict(va='0x4d29e0',receiver=OVERLAY,return_va='0x4d024f',sp=l['overlay'],ebp=l['vm']-4,eax=TASK,args=[20,0,1,51,(TASK&0xFFFF0000)|x,(VM&0xFFFF0000)|y,424,24,20,30,100,100,255,128,128,128],first_instruction_executed=False)
    elif phase=='packet':pending=dict(va='0x407870',receiver=l['packet'],return_va='0x4d2d57',sp=l['resource'],ebp=l['kind']-4,eax=0,args=[20,0],first_instruction_executed=False)
    else:pending=dict(va='0x407ad0',receiver=l['packet'],return_va='0x407ab0',sp=l['draw'],ebp=l['drawbp'],eax=l['packet'],args=[0,0],first_instruction_executed=False)
    packet=None if phase=='command' else dict(pointer=l['packet'],bytes=128,hex=packet_project(0x40 if phase=='packet' else 0xC0,texture,int.from_bytes(d[TASK+0xB210],'little')))
    return dict(after=out,packet=packet,pending=pending,normal_opcode167_executed=True,VM_returned=False,render_completed=False,resource_lookup_return=texture['pointer'] if phase=='draw' else None,assertion_executed=False)
