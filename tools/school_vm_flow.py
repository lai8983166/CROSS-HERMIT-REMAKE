"""Independent source model for the actual normal opening branch and sixty-update fade."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_vm_draw import ROOT,SOURCE,SOURCE_SHA256,SCRIPT,SCRIPT_SHA,BASE,TASK,TACT,WORK,VM,STACK,RETURN,BASE_SP,BANK,layout,source_contract as draw_source,REGIONS as PARENT_REGIONS
from tools.school_vm_present import packet_project
from tools.school_task_cycle import RESET_NATIVE,source_contract as cycle_source
from tools.school_world_task_start import INPUT,MAIN,TASK_NATIVE

GLOBAL=0x809348;SLOTS=WORK+0x18
REGIONS=PARENT_REGIONS+((GLOBAL,160),(SLOTS,12))
PHASES=('branch','assign','globals','slots','poses','fade_start','fade_finish')
PREVIOUS=dict(zip(PHASES[1:],PHASES[:-1]))
KINDS={'branch':('branch',),'assign':('assign',),'globals':('bit','word'),'slots':('hide1','hide2'),'poses':('pose1','wait','pose2','wait'),'fade_start':('fade',),'fade_finish':('wait',)*60}
COMMANDS={'branch':(8,8,20),'assign':(44,5,12),'bit':(56,165,16),'word':(72,163,16),'hide1':(88,113,12),'hide2':(100,113,12),'pose1':(112,136,32),'pose2':(144,136,32),'fade':(176,117,8)}
HANDLERS={'branch':(0x4C23F0,0x4CEB0E),'assign':(0x4C3F40,0x4CEAAF),'bit':(0x42FAF0,0x4CFDBB),'word':(0x42F910,0x4CFD7C),'hide1':(0x42D460,0x4CF74D),'hide2':(0x42D460,0x4CF74D),'pose1':(0x42E9E0,0x4CFA25),'pose2':(0x42E9E0,0x4CFA25),'fade':(0x42D960,0x4CF7CB)}
ADDED=(0x454C40,0x4C23F0,0x4C1EB0,0x4C2060,0x4C3F40,0x42FAF0,0x42F910,0x4E29E0,0x42D460,0x497210,0x42E9E0,0x499560,0x4972B0,0x4977A0,0x42D960,0x4978C0,0x56CFCC)
CDECL_ARGS={0x56CEC0:3,0x4E29E0:4,0x497210:2,0x499560:7,0x4972B0:2,0x4978C0:1}

@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes();s=SCRIPT.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(s).hexdigest()!=SCRIPT_SHA:raise ValueError('VM flow source/script SHA')
    checks={0x4C20A4:('sete','cl'),0x4C24B6:('mov','word ptr [edx + ecx + 0x24], 0'),0x4C24CF:('mov','dword ptr [ecx + eax + 0x1c], edx'),0x4C3FD4:('call','0x4c1f40'),0x42FBBE:('call','0x4e29e0'),0x42F9DE:('call','0x4e29e0'),0x4E2BBC:('mov','dword ptr [edx + ecx*4 + 0x78], eax'),0x4E2B04:('mov','word ptr [edx + ecx*2 + 0x28], ax'),0x497290:('mov','byte ptr [eax + edx*4 + 0x19], cl'),0x499637:('call','0x4972b0'),0x497331:('mov','word ptr [eax + edx*4 + 0x1a], cx'),0x4977B8:('mov','byte ptr [0x7e0f08], 0'),0x49794F:('fild','dword ptr [ecx + 0x249c]'),0x497955:('fdivr','dword ptr [0x59e8bc]'),0x49795E:('call','0x56cfcc'),0x56CFE5:('fistp','qword ptr [ebp - 0xc]'),0x497B4D:('mov','dword ptr [ecx + 0x2490], edx'),0x497BB7:('mov','dword ptr [edx + 0x249c], ecx'),0x497BD1:('mov','byte ptr [ecx + 0x2499], 0'),0x497C0A:('mov','byte ptr [edx + 0x249a], 2'),0x4CFF2D:('jne','0x4cff48'),0x4CFF41:('mov','word ptr [edx + ecx + 0x20], 0')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('VM flow original operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    commands=[]
    for kind,(pc,opcode,n) in COMMANDS.items():
        if struct.unpack_from('<HH',s,452+pc)!=(opcode,n):raise ValueError('VM flow exact source commands')
        target=struct.unpack_from('<I',raw,0x4D03CF-BASE+(opcode-5)*4)[0];commands.append(dict(kind=kind,PC=pc,opcode=opcode,advance=n,handler=hex(target),hex=s[452+pc:452+pc+n].hex()))
    if struct.unpack_from('<I',s,452+8+16)[0]!=44 or struct.unpack_from('<f',raw,0x59E8BC-BASE)[0]!=38912 or struct.unpack_from('<I',raw,0x4D03B7-BASE+4*4)[0]!=0x4CFF20:raise ValueError('VM flow branch target/fade constant/wait dispatch')
    if raw[0x4997A8-BASE+20]!=6 or struct.unpack_from('<I',raw,0x499750-BASE+6*4)[0]!=0x49962E:raise ValueError('VM flow original pose dispatch')
    functions=[];starts={int(r['va'],16) for r in draw_source()['functions']}|{a for a,b in RESET_NATIVE+TASK_NATIVE}|set(ADDED)
    for a in sorted(starts):
        if a==0x56CD4A:b=a+6;frame=0;args=1;ret=None
        else:
            seq=[]
            for i in md.disasm(raw[a-BASE:a-BASE+20000],a):
                seq.append(i)
                if i.mnemonic=='ret':break
            last=seq[-1]
            if last.mnemonic!='ret':raise ValueError('VM flow finite native function')
            b=last.address+last.size;ret=hex(last.address);args=CDECL_ARGS.get(a,int(last.op_str,0)//4 if last.op_str else 0)
            if a==0x56CEC0:b=0x56CF18;frame=0
            elif a==0x56CFCC:frame=16
            else:
                local=next(i for i in seq[:18] if i.mnemonic=='sub' and i.op_str.startswith('esp, '));seh=12 if a in (0x4D2CA0,0x4075E0,0x407710,0x4036C0,0x41F9E0) else 0;frame=4+int(local.op_str.split(', ')[1],0)+12+seh
        functions.append(dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest(),frame=frame,args=args,ret=ret))
    return dict(source_image_sha256=SOURCE_SHA256,script_sha256=SCRIPT_SHA,parent_draw_source=draw_source(),input_source=cycle_source(),functions=functions,instructions=proof,commands=commands,fade=dict(range=38912,duration=60,step=38912//60,updates=60,accumulator_after60=60*(38912//60),following_wait_clear_polls=1),driver='explicit_original_reset_and_selected_task_calls_after_verified_return',scope='Actual opening branch through global/slot/pose setup and complete captured fade to PC184/wait0; inherited bounded adapters only; no live OS/world/outer frame/GPU/persistence')

def native_ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])

def data(before):
    if [(r['pointer'],r['bytes']) for r in before]!=list(REGIONS) or any(len(bytes.fromhex(r['hex']))!=r['bytes'] for r in before):raise ValueError('VM flow complete fixed owned regions')
    return {r['pointer']:bytearray.fromhex(r['hex']) for r in before}

def typed(value,v):
    kind=value>>28;index=value&0xFFFFFFF
    if kind==2:return index
    if kind==0 and index<50:return struct.unpack_from('<I',v,0x3C+index*4)[0]
    raise ValueError('VM flow selected source operand type')

def operands(kind,v):
    if kind=='wait':return []
    pc,opcode,n=COMMANDS[kind];s=SCRIPT.read_bytes();start=452+pc;fields=struct.unpack_from('<'+'I'*((n-4)//4),s,start+4)
    if kind=='branch':return [typed(fields[1],v),typed(fields[2],v)]
    if kind=='assign':return [typed(fields[1],v)]
    return [typed(x,v) for x in fields]

def call_protocol(kind,inputs,before,fade_completed=False):
    """(entry, source return, semantic receiver or None, complete argument words)."""
    d=data(before);l=layout();p=l['packet'];v=d[VM];pointer=inputs['script_pointer'];x=int.from_bytes(d[TASK+0x196C],'little');y=int.from_bytes(d[TASK+0x1970],'little')
    out=[(0x425DE0,RETURN,INPUT,[]),(0x425E60,0x425E39,INPUT,[0]),(0x425C70,0x425E8C,INPUT,[]),(0x56CD4A,0x425C99,0,[0]),(0x454CF0,RETURN,TACT,[]),(0x454C40,0x454D1E,TACT,[]),(0x457830,0x454D34,TACT,[]),(0x425ED0,0x457860,INPUT,[0]),(0x425A10,0x457871,INPUT,[]),(0x425A50,0x425A35,INPUT,[]),(0x426250,0x425A91,INPUT,[]),(0x56CEC0,0x42627F,None,[INPUT+0x63C,0,64]),(0x426110,0x425A99,INPUT,[]),(0x56CEC0,0x426142,None,[INPUT+0x528,0,256]),(0x426190,0x425AA1,INPUT,[]),(0x56CEC0,0x4261C2,None,[INPUT+0x428,0,256]),(0x4CE8F0,0x454D90,VM,[])]
    if kind!='wait':
        pc,op,n=COMMANDS[kind];command=pointer+452+pc;va,ret=HANDLERS[kind];out.append((va,ret,VM,[0,command,4 if kind.startswith('pose') or kind=='fade' else 0]));s=SCRIPT.read_bytes()
        if kind=='branch':positions=[8,12];returns=[0x4C2439,0x4C2467]
        elif kind=='assign':positions=[8];returns=[0x4C3F95]
        else:
            positions=list(range(4,n,4));returns={'bit':[0x42FB39,0x42FB67,0x42FB95],'word':[0x42F959,0x42F987,0x42F9B5],'hide1':[0x42D4A9,0x42D4D7],'hide2':[0x42D4A9,0x42D4D7],'pose1':[0x42EA29,0x42EA57,0x42EA85,0x42EAB3,0x42EAE1,0x42EB0F,0x42EB3D],'pose2':[0x42EA29,0x42EA57,0x42EA85,0x42EAB3,0x42EAE1,0x42EB0F,0x42EB3D],'fade':[0x42D9A9]}[kind]
        for off,retva in zip(positions,returns):
            operand=struct.unpack_from('<I',s,452+pc+off)[0];out.append((0x4C1EB0,retva,VM,[0,operand>>28,operand&0xFFFFFFF]))
        values=operands(kind,v)
        if kind=='branch':out.append((0x4C2060,0x4C2495,VM,[*values,1]))
        elif kind=='assign':out.append((0x4C1F40,0x4C3FD9,VM,[0,0,0,0]))
        elif kind in ('bit','word'):out.append((0x4E29E0,0x42FBC3 if kind=='bit' else 0x42F9E3,None,[65535,3 if kind=='bit' else 1,0,0]))
        elif kind.startswith('hide'):out.append((0x497210,0x42D4F9,None,values))
        elif kind.startswith('pose'):out.extend([(0x499560,0x42EB9B,None,values),(0x4972B0,0x49963C,None,[values[1],1]),(0x4977A0,0x49973F,None,[])])
        elif kind=='fade':out.extend([(0x4978C0,0x42D9C1,None,[60]),(0x56CFCC,0x497963,None,[])])
    root=[20,0,1,51,(TASK&0xFFFF0000)|x,(VM&0xFFFF0000)|y,424,24,20,30,100,100,255,128,128,128]
    out.extend([(0x4D29E0,0x4D024F,VM+0x94E8,root),(0x4D2CA0,0x4D2A7D,VM+0x94E8,[20,51,x,y,0,424,24,20,30]),(0x4075E0,0x4D2CE3,p,[]),(0x403620,0x40761A,p,[]),(0x41F930,0x403645,p,[]),(0x420990,0x41F955,p,[]),(0x56CEC0,0x41F9BE,None,[p+0x24,0,4]),(0x408C00,0x40762C,p+0x50,[]),(0x4077C0,0x4D2CFB,p,[TASK]),(0x407870,0x4D2D57,p,[20,0]),(0x41F5A0,0x407904,TASK+0x844,[20,0]),(0x4142B0,0x4079A5,TASK,[]),(0x4079C0,0x4D2D9E,p,[0,0]),(0x407A50,0x4079FB,p,[0,0]),(0x407AD0,0x407AB0,p,[0,0]),(0x407710,0x4D2DB0,p,[]),(0x407780,0x407751,p,[]),(0x403730,0x4077A5,p,[]),(0x4036C0,0x407760,p,[]),(0x403730,0x403701,p,[]),(0x41F9E0,0x403710,p,[]),(0x41FA50,0x41FA21,p,[]),(0x4209C0,0x41FA30,p,[])])
    from tools.school_vm_draw import call_protocol as maintenance
    out.extend(maintenance('vm'));out.extend([(0x4563D0,0x454DCD,TACT,[]),(0x497AA0,0x454EAA,None,[])])
    if fade_completed:out.append((0x4977A0,0x497C16,None,[]))
    out.append((0x498310,0x454EAF,None,[]));return out

def project_step(kind,inputs,before):
    source_contract();d=data(before);v=d[VM];t=d[TACT];k=d[INPUT];w=d[WORK+0x2490];pointer=inputs.get('script_pointer');tex=inputs.get('texture_record')
    expected=dict(script_pointer=pointer,script_sha256=SCRIPT_SHA,driver='explicit_original_reset_and_selected_task_calls_after_verified_return',texture_record=tex,ime_target=inputs.get('ime_target'),strlen_target=inputs.get('strlen_target'))
    if inputs!=expected or type(pointer) is not int or not tex or set(tex)!={'pointer','bytes','hex'} or tex['pointer']!=int.from_bytes(d[BANK][:4],'little') or tex['bytes']!=84 or len(bytes.fromhex(tex['hex']))!=84 or not inputs['ime_target'] or not inputs['strlen_target']:raise ValueError('VM flow captured source inputs')
    if t[0x43]!=1 or t[0x44]!=2 or t[0x59]!=1 or struct.unpack_from('<I',t,0x48)[0]!=1 or struct.unpack_from('<I',t,0x60)[0]!=WORK or struct.unpack_from('<I',t,0x64)[0]!=pointer or v[4:6]!=b'\x01\x01' or struct.unpack_from('<I',v,0x10)[0]!=pointer+452 or any(v[o] for o in (0x92E1,0x93E2)) or d[WORK]!=b'\x01\x01\x01':raise ValueError('VM flow selected active task/VM/work')
    if any(d[0]) or any(d[TASK+0xB28E]) or any(d[WORK+0x2434]) or w[0x18] or k[0x630]!=255 or any(k[8:12]) or k[0x528] or any(d[TASK+0x196C]) or any(d[TASK+0x1970]) or int.from_bytes(d[BANK][4:],'little')!=1:raise ValueError('VM flow captured input/menu/render/resource guards')
    for i in range(10):
        o=0x6F60+i*0xE0
        if any(v[o+j] for j in (2,3,4,5,0x22,0x23,0x30,0x31)):raise ValueError('VM flow inactive layer maintenance')
    if any(v[0x1CF+i*0x12] for i in range(5)) or any(v[0x9248:0x924A]) or any(v[0x228+i*0x1A] for i in range(20)):raise ValueError('VM flow inactive secondary/presentation/resource maintenance')
    pc=struct.unpack_from('<I',v,0x1C)[0];wait=struct.unpack_from('<H',v,0x20)[0];values=operands(kind,v);command=None
    if kind=='wait':
        if wait!=4 or pc not in (144,176,184):raise ValueError('VM flow actual wait4 clear/countdown')
        if not v[0x92E0]:struct.pack_into('<H',v,0x20,0)
    else:
        if kind not in COMMANDS or (pc,wait)!=(COMMANDS[kind][0],0):raise ValueError('VM flow exact current command/PC/wait')
        _,opcode,n=COMMANDS[kind];command=dict(PC=pc,file_offset=452+pc,opcode=opcode,advance=n)
        for i,value in enumerate(values):struct.pack_into('<I',v,0x9250+i*4,value)
        if kind=='branch':
            if values!=[1,1]:raise ValueError('VM flow captured equality path')
            pc=44;n=0;struct.pack_into('<I',v,0x1C,pc);struct.pack_into('<I',v,0x9258,1)
        elif kind=='assign':
            if values!=[0]:raise ValueError('VM flow source assignment zero')
            struct.pack_into('<I',v,0x3C,0)
        elif kind in ('bit','word'):
            if values!=[0,65535,0]:raise ValueError('VM flow exact global typed arguments')
            if kind=='bit':old=struct.unpack_from('<I',d[GLOBAL],0x78)[0];struct.pack_into('<I',d[GLOBAL],0x78,old&0x7FFFFFFF)
            else:struct.pack_into('<H',d[GLOBAL],0x28,0)
        elif kind.startswith('hide'):
            index=int(kind[-1])
            if values!=[index,0]:raise ValueError('VM flow selected slot flag arguments')
            d[SLOTS][index*4+1]=0
        elif kind.startswith('pose'):
            index=int(kind[-1])
            if values!=[20,index,1,0,0,0,0]:raise ValueError('VM flow selected pose dispatch arguments')
            struct.pack_into('<H',d[SLOTS],index*4+2,1);v[0x92E0]=0
        elif kind=='fade':
            if values!=[60] or w[9]:raise ValueError('VM flow original60 fade start')
            struct.pack_into('<II',w,0,0,38912//60);w[8:11]=bytes([1,1,1]);struct.pack_into('<I',w,12,60);v[0x92E0]=1
        struct.pack_into('<I',v,0x1C,pc+n);struct.pack_into('<HHH',v,0x20,4 if kind.startswith('pose') or kind=='fade' else 0,opcode,n)
        c=struct.unpack_from('<I',d[0x7A4E18])[0];struct.pack_into('<II',d[0x7A4E18],0,(c+1)&0xFFFFFFFF,0)
    # Original reset consumes FF; task startup writes FF again and clears these buffers.
    k[0x428:0x628]=bytes(512);k[0x63C:0x67C]=bytes(64);k[0x634:0x638]=bytes(4);d[TACT+0x117F20][0]=0
    fade_completed=False
    if w[9]:
        pos,step=struct.unpack_from('<II',w);remaining=struct.unpack_from('<I',w,12)[0]
        if w[8]!=1 or step!=648 or not 1<=remaining<=60 or pos!=(60-remaining)*648 or v[0x92E0]!=1:raise ValueError('VM flow captured native increasing fade')
        struct.pack_into('<I',w,0,min(pos+step,38912));remaining-=1;struct.pack_into('<I',w,12,remaining)
        if not remaining:w[9]=0;w[10]=2;v[0x92E0]=0;fade_completed=True
        else:w[10]=1
    out=deepcopy(before)
    for r in out:r['hex']=d[r['pointer']].hex()
    return dict(kind=kind,after=out,command=command,operand_values=values,CPU=dict(EIP=RETURN,ESP=BASE_SP+4,EBP=BASE_SP-4,EAX=0,ECX=0),reset_CPU=dict(EIP=RETURN,ESP=BASE_SP+4,EBP=BASE_SP-4,EAX=0,ECX=INPUT),packet=dict(pointer=layout()['packet'],bytes=128,hex=packet_project(0xC0,tex,int.from_bytes(d[TASK+0xB210],'little'))),PC=struct.unpack_from('<I',v,0x1C)[0],wait=struct.unpack_from('<H',v,0x20)[0],fade_remaining=struct.unpack_from('<I',w,12)[0],fade_accumulator=struct.unpack_from('<I',w)[0],fade_completed=fade_completed,VM_return=1,task_return=0,task_phase=2,task_status=1,GPU_executed=False,full_outer_frame_executed=False,persistent_write_authority=False)
