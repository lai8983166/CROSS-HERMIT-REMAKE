"""Source rules for normal display reset, text mode, timer and next character entry."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_vm_flow import ROOT,SOURCE,SOURCE_SHA256,SCRIPT,SCRIPT_SHA,BASE,TASK,TACT,WORK,VM,STACK,RETURN,BASE_SP,BANK,INPUT,MAIN,REGIONS,layout,data,typed,packet_project,source_contract as flow_source,call_protocol as flow_calls

PANEL=VM+0x9248;ENTRY=0x4C5EA0
PHASES=('display','release','text_mode','timer_start','timer_finish','character_entry')
PREVIOUS=dict(zip(PHASES[1:],PHASES[:-1]))
KINDS={'display':('display',),'release':('release',),'text_mode':('text_mode',),'timer_start':('timer_start',),'timer_finish':('timer_poll',)*31,'character_entry':('character_entry',)}
COMMANDS={'display':(184,56,8,1,0x4C5430,0x4CF09F),'text_mode':(192,20,8,0,0x4C5500,0x4CEC6A),'timer_start':(200,12,8,1,0x4C2670,0x4CEB6D),'character_entry':(208,27,16,1,ENTRY,0x4CED48)}
ADDED=(0x4C5430,0x4C76B0,0x4C7AB0,0x4C5500,0x4C2670,0x4C1E20,0x4CCB90,ENTRY)

@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes();script=SCRIPT.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(script).hexdigest()!=SCRIPT_SHA:raise ValueError('VM panel source/script SHA')
    checks={0x4C5495:('call','0x4c76b0'),0x4C76D4:('mov','word ptr [eax + 2], cx'),0x4C771A:('mov','word ptr [eax], 0'),0x4C76EC:('mov','word ptr [ecx + 6], 0x10'),0x4C7AD9:('mov','al, 1'),0x4C555E:('mov','byte ptr [edx + 0x9228], cl'),0x4C26FC:('call','0x4c1e20'),0x4C1E40:('mov','byte ptr [eax + 0x1cd], 1'),0x4C1E57:('mov','word ptr [edx + ecx + 0x26], ax'),0x4C1E6C:('mov','word ptr [edx + ecx + 0x28], ax'),0x4C1E81:('mov','word ptr [edx + ecx + 0x2a], ax'),0x4C1E95:('mov','dword ptr [edx + ecx + 0x2c], eax'),0x4CCC2C:('mov','word ptr [edi + ecx + 0x28], ax'),0x4CCC31:('cmp','edx, esi'),0x4CCC33:('jle','0x4ccc39'),0x4CCDFF:('mov','byte ptr [ecx + 0x1cd], 0'),0x4D01B5:('mov','word ptr [eax + edx + 0x20], 0'),0x4CED43:('call','0x4c5ea0')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('VM panel source operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    if struct.unpack_from('<I',raw,0x4C7756-BASE)[0]!=0x4C7717:raise ValueError('VM panel source type2 dispatch')
    commands=[]
    for kind,(pc,op,n,wait,va,ret) in COMMANDS.items():
        if struct.unpack_from('<HH',script,452+pc)!=(op,n):raise ValueError('VM panel original command bytes')
        target=struct.unpack_from('<I',raw,0x4D03CF-BASE+(op-5)*4)[0];commands.append(dict(kind=kind,PC=pc,opcode=op,advance=n,handler_call=hex(ret-5),handler=hex(va),dispatch=hex(target),hex=script[452+pc:452+pc+n].hex()))
    functions=deepcopy(flow_source()['functions'])
    for a in ADDED:
        seq=[]
        for i in md.disasm(raw[a-BASE:a-BASE+20000],a):
            seq.append(i)
            if i.mnemonic=='ret':break
        ret=seq[-1];b=ret.address+ret.size;local=next(i for i in seq[:18] if i.mnemonic=='sub' and i.op_str.startswith('esp, '));frame=4+int(local.op_str.split(', ')[1],0)+12
        if ret.mnemonic!='ret':raise ValueError('VM panel finite original function')
        functions.append(dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest(),frame=frame,args=int(ret.op_str,0)//4 if ret.op_str else 0,ret=hex(ret.address)))
    return dict(source_image_sha256=SOURCE_SHA256,script_sha256=SCRIPT_SHA,parent_source=flow_source(),functions=functions,instructions=proof,commands=commands,timer=dict(duration=30,initial_count=0,polls=31,comparison='old_count > duration - 1',final_count=31),scope='Original56 type2/state0 and wait query,20 text-mode9228,12 timer and31 polls, then natural unexecuted27 handler; declared reset/task driver, inherited adapters, no character-body/text/GPU/outer-world/persistent completion')

def native_ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])

def project_step(kind,inputs,before):
    source_contract();d=data(before);v=d[VM];t=d[TACT];k=d[INPUT];w=d[WORK+0x2490];ptr=inputs.get('script_pointer');tex=inputs.get('texture_record')
    if inputs.get('driver')!='explicit_original_reset_and_selected_task_calls_after_verified_return' or inputs.get('script_sha256')!=SCRIPT_SHA or not ptr or not tex or tex['bytes']!=84 or len(bytes.fromhex(tex['hex']))!=84 or tex['pointer']!=int.from_bytes(d[BANK][:4],'little') or not inputs.get('ime_target') or not inputs.get('strlen_target'):raise ValueError('VM panel actual captured inputs')
    if t[0x43]!=1 or t[0x44]!=2 or t[0x59]!=1 or struct.unpack_from('<I',t,0x48)[0]!=1 or struct.unpack_from('<I',t,0x64)[0]!=ptr or struct.unpack_from('<I',t,0x60)[0]!=WORK or v[4:6]!=b'\x01\x01' or struct.unpack_from('<I',v,0x10)[0]!=ptr+452 or struct.unpack_from('<I',v,0x3C)[0] or v[0x1CC]!=255:raise ValueError('VM panel selected task/VM/variable/speaker')
    if any(d[0]) or any(d[TASK+0xB28E]) or any(d[WORK+0x2434]) or any(v[o] for o in (0x92E0,0x92E1,0x93E2)) or k[0x630]!=255 or any(k[8:12]) or k[0x528] or w[9] or struct.unpack_from('<I',w)[0]!=38880 or struct.unpack_from('<I',w,12)[0] or w[10]!=2 or w[0x18]:raise ValueError('VM panel captured input/render/menu/fade guards')
    for i in range(10):
        o=0x6F60+i*0xE0
        if any(v[o+j] for j in (2,3,4,5,0x22,0x23,0x30,0x31)):raise ValueError('VM panel captured inactive layers')
    if any(v[0x1CF+i*0x12] for i in range(5)) or any(v[0x228+i*0x1A] for i in range(20)):raise ValueError('VM panel inactive secondary/resource maintenance')
    pc=struct.unpack_from('<I',v,0x1C)[0];wait=struct.unpack_from('<H',v,0x20)[0];command=None;pending=None;old_count=None;completed=False
    if kind in COMMANDS:
        wanted,op,n,nextwait,handler,ret=COMMANDS[kind]
        if (pc,wait)!=(wanted,0):raise ValueError('VM panel exact command admission')
        command=dict(PC=pc,file_offset=452+pc,opcode=op,advance=n);struct.pack_into('<HH',v,0x22,op,n);count=struct.unpack_from('<I',d[0x7A4E18])[0];struct.pack_into('<II',d[0x7A4E18],0,(count+1)&0xFFFFFFFF,0)
        if kind=='character_entry':
            sp=layout()['vm']-128-12-4;pending=dict(va=hex(ENTRY),return_va=hex(ret),sp=sp,receiver=VM,args=[0,ptr+452+pc,1],first_instruction_executed=False);cpu=dict(EIP=ENTRY,ESP=sp,EBP=layout()['vm']-4,EAX=ptr+452+pc,ECX=VM)
        else:
            value=typed(struct.unpack_from('<I',SCRIPT.read_bytes(),452+pc+4)[0],v);struct.pack_into('<I',v,0x9250,value)
            if kind=='display':
                if value!=2 or any(v[0x9248:0x9250]):raise ValueError('VM panel captured initial display state')
                struct.pack_into('<4H',v,0x9248,0,2,0,16)
            elif kind=='text_mode':
                if value:raise ValueError('VM panel exact text mode0')
                v[0x9228]=0
            elif kind=='timer_start':
                if value!=30:raise ValueError('VM panel source timer30')
                v[0x1CD]=1;struct.pack_into('<HHHI',v,0x26,12,0,30,0)
            struct.pack_into('<I',v,0x1C,pc+n);struct.pack_into('<H',v,0x20,nextwait)
    else:
        if kind not in ('release','timer_poll') or wait!=1 or pc!=(192 if kind=='release' else 208):raise ValueError('VM panel actual wait1 branch')
        struct.pack_into('<II',d[0x7A4E18],0,0,(struct.unpack_from('<I',d[0x7A4E18],4)[0]+1)&0xFFFFFFFF)
        if kind=='release':
            if struct.unpack_from('<4H',v,0x9248)!=(0,2,0,16):raise ValueError('VM panel actual inactive type2 query')
            struct.pack_into('<H',v,0x20,0);completed=True
        else:
            opcode,old_count,limit=struct.unpack_from('<HHH',v,0x26)
            if opcode!=12 or limit!=30 or not 0<=old_count<=30 or v[0x1CD]!=1:raise ValueError('VM panel captured timer poll')
            struct.pack_into('<H',v,0x28,old_count+1);completed=old_count>limit-1
            if completed:v[0x1CD]=0;struct.pack_into('<H',v,0x20,0)
    k[0x428:0x628]=bytes(512);k[0x63C:0x67C]=bytes(64);k[0x634:0x638]=bytes(4);d[TACT+0x117F20][0]=0
    if pending is None:cpu=dict(EIP=RETURN,ESP=BASE_SP+4,EBP=BASE_SP-4,EAX=0,ECX=0)
    out=deepcopy(before)
    for r in out:r['hex']=d[r['pointer']].hex()
    return dict(kind=kind,after=out,command=command,CPU=cpu,reset_CPU=dict(EIP=RETURN,ESP=BASE_SP+4,EBP=BASE_SP-4,EAX=0,ECX=INPUT),packet=None if pending else dict(pointer=layout()['packet'],bytes=128,hex=packet_project(0xC0,tex,int.from_bytes(d[TASK+0xB210],'little'))),pending=pending,PC=struct.unpack_from('<I',v,0x1C)[0],wait=struct.unpack_from('<H',v,0x20)[0],old_timer_count=old_count,timer_count=struct.unpack_from('<H',v,0x28)[0],wait_completed=completed,VM_return=None if pending else 1,task_return=None if pending else 0,task_phase=2,task_status=1,GPU_executed=False,full_outer_frame_executed=False,persistent_write_authority=False)

def call_protocol(kind,inputs,before):
    common=flow_calls('wait',inputs,before,False);middle=[];ptr=inputs['script_pointer']
    if kind in COMMANDS:
        pc,op,n,wait,va,ret=COMMANDS[kind];middle.append((va,ret,VM,[0,ptr+452+pc,wait]))
        if kind=='character_entry':return common[:17]+middle
        value=struct.unpack_from('<I',SCRIPT.read_bytes(),452+pc+4)[0];getret={'display':0x4C5479,'text_mode':0x4C5549,'timer_start':0x4C26C5}[kind];middle.append((0x4C1EB0,getret,VM,[0,value>>28,value&0xFFFFFFF]))
        if kind=='display':middle.append((0x4C76B0,0x4C549A,PANEL,[2]))
        if kind=='timer_start':middle.append((0x4C1E20,0x4C2701,VM,[0,12,0,30,0]))
    elif kind=='release':middle.append((0x4C7AB0,0x4D0138,PANEL,[]))
    elif kind=='timer_poll':middle.append((0x4CCB90,0x4CFFCA,VM,[0]))
    else:raise ValueError('VM panel known call path')
    return common[:17]+middle+common[17:]
