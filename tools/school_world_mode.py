"""Source-only original world mode request effects; not gameplay authority."""
import hashlib
import struct
from copy import deepcopy
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86_const import X86_OP_MEM, X86_OP_IMM
from tools.tactics_exit_emulation import SOURCE, SOURCE_SHA256, BASE

RANGES = ((0x4678C0,0x467A9D),(0x43B250,0x43B336),(0x455160,0x4551B4),
          (0x4553E0,0x455413),(0x4558A0,0x4558D3),(0x455D00,0x455D33))


def source_contract(raw=None):
    raw = SOURCE.read_bytes() if raw is None else raw
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('world mode source identity')
    md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
    def instructions(a,b): return list(md.disasm(raw[a-BASE:b-BASE],a))
    def stores(a,b):
        result = []
        for i in instructions(a,b):
            if i.mnemonic != 'mov' or len(i.operands) != 2: continue
            dst,src = i.operands
            if dst.type == X86_OP_MEM and dst.size == 1 and src.type == X86_OP_IMM:
                result.append([dst.mem.disp,src.imm])
        return result
    checks={0x4678E7:('cmp','ecx, -1'),0x4678FD:('cmp','byte ptr [ebp - 8], 1'),
        0x467903:('cmp','byte ptr [ebp - 8], 2'),0x467A7B:('mov','byte ptr [ecx + 0x108b3b], 0xff'),
        0x467A85:('mov','byte ptr [edx + 0x108b3c], 0xff'),
        0x4678EA:('jne','0x4678f1'),0x46791E:('je','0x46797e'),0x4679EB:('je','0x467a49'),
        0x455184:('call','0x4553e0'),0x455190:('call','0x4558a0'),0x45519C:('call','0x455d00')}
    for va, expected in checks.items():
        i=instructions(va,va+16)[0]
        if (i.mnemonic,i.op_str)!=expected: raise ValueError('world mode branch identity')
    branches={name:stores(a,b) for name,a,b in [('on',0x467940,0x46797C),
        ('off',0x46799E,0x4679DA),('partial',0x467A0D,0x467A49)]}
    offsets=[0x108B34,0x108B35,0x108B36,0x108B38,0x108B39,0x108B3A]
    for name,values in [('on',[1]*6),('off',[0]*6),('partial',[1,1,0,0,0,0])]:
        if branches[name] != list(map(list,zip(offsets,values))): raise ValueError('world mode stores')
    jumps=list(struct.unpack_from('<4I',raw,0x43B338-BASE))
    map_modes=[stores(a,0x43B32D if n==3 else jumps[n+1]) for n,a in enumerate(jumps)]
    if map_modes != [[[0x26595+i,v] for i,v in enumerate(values)] for values in ([0]*4,[1]*4,[1,1,1,0],[1]*4)]:
        raise ValueError('world map mode dispatch')
    leaf_offsets=[]
    for a,b in RANGES[3:]:
        seq=instructions(a,b)
        candidates=[i for i in seq if i.mnemonic=='mov' and i.operands[0].type==X86_OP_MEM and i.operands[0].size==1]
        if len(candidates)!=1: raise ValueError('world task leaf store')
        leaf_offsets.append(candidates[0].operands[0].mem.disp)
        if not any(i.op_str=='ecx, dword ptr [eax + 0x60]' for i in seq): raise ValueError('world task owner binding')
    if leaf_offsets != [0x20E8,0x216C,0x2230]: raise ValueError('world task offsets')
    calls={0x46792B:0x43B250,0x46793B:0x455160,0x467989:0x43B250,
        0x467999:0x455160,0x4679F8:0x43B250,0x467A08:0x455160}
    for va,target in calls.items():
        if instructions(va,va+5)[0].op_str != hex(target): raise ValueError('world mode child call')
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'functions':[{'va':hex(a),'end':hex(b),'sha256':hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()} for a,b in RANGES],
        'branches':branches,'map_modes':map_modes,'task_owner_offset':0x60,'task_leaf_offsets':leaf_offsets,
        'pending_offsets':[0x108B3B,0x108B3C],'control_region_offset':0x108B30,
        'child_call_returns':[hex(va+5) for va in calls],
        'scope':'Independent mode stores only; no world tick, original opening completion or school persistence'}


def admitted_request(kind,flag):
    if type(kind) is not int or kind not in (-1,255,1,2) or type(flag) is not int or not 0<=flag<=255:
        raise ValueError('unsupported mode request before execution')
    return kind & 255,flag


def project(before,kind,flag,contract=None):
    kind,flag=admitted_request(kind,flag); c=source_contract() if contract is None else contract
    out=deepcopy(before)
    if [row['name'] for row in out]!=['control','map_flags','task_flags']:
        raise ValueError('world mode complete region set')
    data={row['name']:bytearray.fromhex(row['hex']) for row in out}
    if len(data['control'])!=50 or len(data['map_flags'])!=4 or len(data['task_flags'])!=329:
        raise ValueError('world mode complete region size')
    data['control'][11]=kind; data['control'][12]=flag
    branch='on' if kind==1 and flag else 'off' if kind==1 else 'partial' if kind==2 and flag else None
    if branch:
        for offset,value in c['branches'][branch]: data['control'][offset-c['control_region_offset']]=value
        map_mode=0 if branch=='on' else 1
        for offset,value in c['map_modes'][map_mode]: data['map_flags'][offset-0x26595]=value
        for offset in c['task_leaf_offsets']: data['task_flags'][offset-c['task_leaf_offsets'][0]]=1 if branch=='on' else 0
    if kind!=255: data['control'][11:13]=b'\xff\xff'
    for row in out: row['hex']=data[row['name']].hex()
    return out


def first_entry_update(before):
    """Only the actual controller0/request1 first update, independently sourced."""
    from tools.school_entry_control_catalog import source_catalog,memory_regions,REGIONS
    from tools.school_tactical_startup_emulation import TACT
    from tools.school_deployment_tail_emulation import UNITCTRL
    source_catalog()
    memory=memory_regions(before); control=memory[UNITCTRL+0x108B30]
    task=memory[TACT];camera=memory[UNITCTRL+0x3D68+0x265A6]
    if control[26]!=0 or control[24]!=1 or task[0x170]!=1 or task[0x171]!=0:
        raise ValueError('first nested entry actual state')
    x,y=struct.unpack_from('<2h',control,16)
    if [x,y]!=[9,16]: raise ValueError('first nested entry origin')
    cx=min(max(x*32+16-512,0),64*32-1024)
    cy=min(max(y*16+8-285,0),96*16-568)
    struct.pack_into('<2h',camera,0,cx,cy);control[26]=4
    return [{'pointer':at,'bytes':n,'hex':memory[at].hex()} for at,n in REGIONS]
