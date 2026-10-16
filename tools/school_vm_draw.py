"""Source projection for captured inactive drawing, native cleanup and VM/task returns."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_vm_present import ROOT,SOURCE,SOURCE_SHA256,SCRIPT,SCRIPT_SHA,BASE,TASK,TACT,WORK,VM,STACK,RETURN,BASE_SP,BANK,layout,REGIONS as PARENT_REGIONS,project as parent_project,NATIVE as PARENT_NATIVE

REGIONS=PARENT_REGIONS+((TASK+0xB28E,2),(WORK+0x2434,32))
PHASES=('cleanup','vm','task');PREVIOUS={'vm':'cleanup','task':'vm'}
START={'cleanup':0x407AD0,'vm':0x4D024F,'task':0x454D90}
STOP={'cleanup':0x4D024F,'vm':0x454D90,'task':RETURN}
ADDED=(0x407AD0,0x407710,0x407780,0x4036C0,0x403730,0x41F9E0,0x41FA50,0x4209C0,0x4CA1B0,0x4C99E0,0x4CD4D0,0x4C7770,0x4CBA60,0x454CF0,0x4563D0,0x497AA0,0x498310)

@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM draw source/script SHA')
    checks={0x407B0C:('movsx','eax, word ptr [edx + 0xb28e]'),0x407B15:('jne','0x407b21'),0x407B17:('mov','eax, 1'),0x407B1C:('jmp','0x408111'),0x40774C:('call','0x407780'),0x40775B:('call','0x4036c0'),0x403750:('cmp','dword ptr [eax + 0x2c], 0'),0x4037A4:('cmp','dword ptr [ecx + 0x30], 0'),0x4037D5:('mov','dword ptr [eax + 0x28], 0'),0x41FA70:('cmp','dword ptr [eax + 0x14], 0'),0x41FA99:('cmp','dword ptr [ecx + 0xc], 0'),0x41FAC2:('cmp','dword ptr [edx], 0'),0x4209D2:('mov','eax, 0xcccccccc'),0x4D2DB3:('mov','dword ptr fs:[0], ecx'),0x4D0289:('call','0x4ca1b0'),0x4D02A6:('call','0x4c99e0'),0x4D02E2:('call','0x4cd4d0'),0x4D0327:('je','0x4d0344'),0x4D034F:('call','0x4c7770'),0x4D038C:('call','0x4cba60'),0x4CA1F2:('ja','0x4ca1fe'),0x4CD54B:('mov','word ptr [ecx + 4], ax'),0x4C779E:('jne','0x4c7a0e'),0x4CBA89:('jmp','0x4cbc79'),0x4D03A3:('mov','eax, dword ptr [ebp - 0x10]'),0x4D03B6:('ret',''),0x454DA0:('jne','0x454dc5'),0x454DC8:('call','0x4563d0'),0x456404:('je','0x456615'),0x454EA5:('call','0x497aa0'),0x454EAA:('call','0x498310'),0x454EAF:('xor','eax, eax'),0x454EC1:('ret','')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('VM draw source operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    functions=[]
    for a in sorted({a for a,b in PARENT_NATIVE}|set(ADDED)):
        seq=[]
        for i in md.disasm(raw[a-BASE:a-BASE+16000],a):
            seq.append(i)
            if i.mnemonic=='ret':break
        ret=seq[-1];b=ret.address+ret.size
        if ret.mnemonic!='ret':raise ValueError('VM draw finite native function')
        if a==0x56CEC0:frame=0
        else:
            local=next(i for i in seq[:18] if i.mnemonic=='sub' and i.op_str.startswith('esp, '));seh=12 if a in (0x4D2CA0,0x4075E0,0x407710,0x4036C0,0x41F9E0) else 0;frame=4+int(local.op_str.split(', ')[1],0)+12+seh
        functions.append(dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest(),frame=frame,args=int(ret.op_str,0)//4 if ret.op_str else 0,ret=hex(ret.address)))
    return dict(source_image_sha256=SOURCE_SHA256,script_sha256=SCRIPT_SHA,functions=functions,instructions=proof,render_gate=dict(pointer=TASK+0xB28E,width=2,value=0),maintenance=dict(layer_triplets=10,secondary_inline_checks=5,presentation_calls=1,resource_calls=20,native_calls=51),scope='Captured disabled renderer, native cleanup and first normal VM/existing selected-task returns; no GPU output, outer frame, later playback, AI or persistent writes')

def native_ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])

def cpu_expected(phase):
    l=layout()
    if phase=='cleanup':return dict(EIP=STOP[phase],ESP=l['vm']-128,EBP=l['vm']-4,EAX=0xCCCCCCCC,ECX=0)
    if phase=='vm':return dict(EIP=STOP[phase],ESP=BASE_SP-96,EBP=BASE_SP-4,EAX=1,ECX=0)
    if phase=='task':return dict(EIP=RETURN,ESP=BASE_SP+4,EBP=BASE_SP-4,EAX=0,ECX=0)
    raise ValueError('VM draw known phase')

def call_protocol(phase):
    p=layout()['packet']
    if phase=='cleanup':return [(0x407AD0,0x407AB0,p,[0,0]),(0x407710,0x4D2DB0,p,[]),(0x407780,0x407751,p,[]),(0x403730,0x4077A5,p,[]),(0x4036C0,0x407760,p,[]),(0x403730,0x403701,p,[]),(0x41F9E0,0x403710,p,[]),(0x41FA50,0x41FA21,p,[]),(0x4209C0,0x41FA30,p,[])]
    if phase=='vm':
        out=[]
        for i in range(10):
            layer=VM+0x6F60+i*0xE0;out.extend([(0x4CA1B0,0x4D028E,layer,[]),(0x4C99E0,0x4D02AB,layer,[]),(0x4CD4D0,0x4D02E7,VM,[layer,VM+0x430+i*0xAB8])])
        return out+[(0x4C7770,0x4D0354,VM+0x9248,[])]+[(0x4CBA60,0x4D0391,VM+0x228+i*0x1A,[]) for i in range(20)]
    if phase=='task':return [(0x4563D0,0x454DCD,TACT,[]),(0x497AA0,0x454EAA,WORK+0x2434,[]),(0x498310,0x454EAF,0,[])]
    raise ValueError('VM draw known phase')

def project(phase,inputs,before):
    source_contract()
    if phase not in PHASES or [(r['pointer'],r['bytes']) for r in before]!=list(REGIONS) or any(len(bytes.fromhex(r['hex']))!=r['bytes'] for r in before):raise ValueError('VM draw full owned buffers/phase')
    d={r['pointer']:bytearray.fromhex(r['hex']) for r in before};l=layout()
    if int.from_bytes(d[0],'little')!=(l['seh'] if phase=='cleanup' else 0) or any(d[TASK+0xB28E]) or any(d[WORK+0x2434]):raise ValueError('VM draw captured SEH/disabled renderer/menu guard')
    parent=deepcopy(before[:len(PARENT_REGIONS)]);next(r for r in parent if r['pointer']==0)['hex']=struct.pack('<I',l['seh']).hex();packet=parent_project('draw',inputs,parent)['packet']
    v=d[VM]
    if struct.unpack_from('<I',d[TACT],0x60)[0]!=WORK or d[WORK+0x2490][9] or d[WORK+0x2490][0x18]:raise ValueError('VM draw inactive task work/fade/board')
    for i in range(10):
        layer=0x6F60+i*0xE0
        if any(v[layer+o] for o in (2,3,4,5,0x22,0x23,0x30,0x31)):raise ValueError('VM draw captured inactive layer')
    if any(v[0x1CF+i*0x12] for i in range(5)) or any(v[0x9248:0x924A]) or any(v[0x228+i*0x1A] for i in range(20)):raise ValueError('VM draw inactive secondary/presentation/resource records')
    if phase=='cleanup':d[0][:]=bytes(4)
    if phase=='vm':
        for i in range(10):o=0x6F60+i*0xE0;v[o+4:o+6]=v[o+2:o+4]
    out=deepcopy(before)
    for r in out:r['hex']=d[r['pointer']].hex()
    return dict(after=out,CPU=cpu_expected(phase),packet=packet if phase=='cleanup' else None,draw_return=1 if phase=='cleanup' else None,VM_returned=phase!='cleanup',VM_return=1 if phase!='cleanup' else None,selected_task_returned=phase=='task',task_return=0 if phase=='task' else None,task_phase=2,task_status=1,script_PC=8,GPU_executed=False,full_outer_frame_executed=False,persistent_write_authority=False)
