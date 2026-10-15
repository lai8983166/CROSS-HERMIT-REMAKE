"""Source third-world admission, phase1 animation and delayed root clearing."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE
from tools.school_world_second import NAMES
from tools.school_world_map import project_map_frame
from tools.school_world_lists import project as list_project
from tools.school_world_command import normalize_selection,STRIDE,COUNT
from tools.school_student_action import source_contract as student_source,u32,put,NODE,POOL
from tools.school_following_students import data

FUNCTIONS=(0x499DA0,0x475D60,0x40A100,0x40A800,0x40AB80)


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('next source image')
    md=Cs(CS_ARCH_X86,CS_MODE_32);bodies=[]
    for a in FUNCTIONS:
        end=next(i.address+i.size for i in md.disasm(raw[a-BASE:a-BASE+8192],a) if i.mnemonic=='ret')
        bodies.append(dict(va=hex(a),end=hex(end),sha256=hashlib.sha256(raw[a-BASE:end-BASE]).hexdigest()))
    checks={0x49A09C:('mov','ax, word ptr [edx + 0xe]'),0x49A0A0:('sub','ax, 1'),
        0x475E83:('je','0x475ed6'),0x40A82D:('je','0x40a84f'),
        0x40A832:('mov','dword ptr [eax + 4], 0'),0x40A840:('call','0x40ab80'),
        0x40ABA7:('jne','0x40abfd'),0x40ABBF:('je','0x40abcc'),0x40ABD9:('jmp','0x40abfb')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(raw[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('next exact source operand '+hex(a))
        proof.append(dict(va=hex(a),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,functions=bodies,instructions=proof,
        student=student_source(),scope='Third declared world prefix and first phase1 unit only; isolated root-clearing probes restore state; no third whole world/180/VM/audio or attached-node release')


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def clearing_project(controller):
    source_contract();a=bytearray(controller)
    if len(a)!=88 or a[8] or not a[11] or not u32(a,4) or u32(a,0x20):raise ValueError('ended depth0 root without children required')
    a[1]=1;put(a,4,0)
    return bytes(a)


def prefix_project(inputs,before):
    source_contract();out=deepcopy(before)
    if [r['name'] for r in out]!=NAMES:raise ValueError('next full prefix regions')
    d={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(d[r['name']])!=r['bytes'] for r in out):raise ValueError('next complete prefix bytes')
    task,ctrl,works=d['task'],d['control'],d['works']
    if len(task)!=400 or len(ctrl)!=50 or len(works)!=STRIDE*COUNT or task[0x170] or task[0x171] or task[0x43] or u32(task,0x38)!=5:raise ValueError('next actual task scope')
    if (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or struct.unpack_from('<h',ctrl,28)[0]!=180 or struct.unpack_from('<h',ctrl,2)[0]!=1 or ctrl[11]!=255 or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('next actual opening delay180')
    if inputs['mouse']!=[0,0] or inputs['map_state'] or inputs['task_input']!=[0,0,0] or inputs['ctrl_keys']!=[0,0]:raise ValueError('next closed input')
    if len(d['queue'])!=20 or d['queue'][8:]!=bytes(12) or len(d['selection'])!=1016 or len(d['cursor'])!=10 or len(d['scratch'])!=2048:raise ValueError('next empty queue/complete prefix bounds')
    if not struct.unpack_from('<h',works)[0] or works[0x290]!=25 or works[0x292] or works[0x293]!=1 or works[4] or works[0x2A7] or u32(works,0x518):raise ValueError('next actual phase1 first student')
    struct.pack_into('<h',ctrl,28,179)
    for r in project_map_frame(out[3:9],inputs['mouse']):d[r['name']][:]=bytes.fromhex(r['hex'])
    slots=struct.unpack('<3I',d['map_slots']);by_pointer={r['pointer']:r for r in out}
    def row(name,p):
        r=by_pointer[p];return dict(name=name,pointer=p,bytes=r['bytes'],hex=d[r['name']].hex())
    li=deepcopy(inputs['lists'])
    if li['opening']!=1 or li['event']!=0:raise ValueError('next actual list gates')
    listed=list_project(li,[row('window',out[9]['pointer']),row('fog_current',slots[1]),row('fog_history',slots[0]),row('visible',out[10]['pointer']),row('categories',out[11]['pointer'])])
    for r in listed['after']:d[by_pointer[r['pointer']]['name']][:]=bytes.fromhex(r['hex'])
    records=[bytes.fromhex(r['record_hex']) if r['record_hex'] else None for r in li['works']]
    selected,indices,kind=normalize_selection(works,records,li['team']);works[:]=selected
    struct.pack_into('<2I',d['selection'],0,len(indices),kind)
    for n,i in enumerate(indices):struct.pack_into('<I',d['selection'],16+n*4,li['works'][i]['pointer'])
    d['cursor'][:]=bytes(6)+b'\xff\xff'+bytes(2);d['scratch'][:]=bytes(2048)
    works[8]&=127;put(d['current_work'],0,li['works'][0]['pointer'])
    for r in out:r['hex']=d[r['name']].hex()
    return dict(after=out,display_indices=listed['display_indices'],category_counts=listed['category_counts'],selected_indices=indices,selection_kind=kind,delay=179,action=1,controller_state=5)


def animation_project(inputs,before):
    s=source_contract()['student'];d=data(before);w=d['works'];ctrl=d['control'];main=s['main']
    if (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or struct.unpack_from('<h',ctrl,28)[0]!=179 or any(ctrl[i] for i in (6,8,9,10)):raise ValueError('next animation actual control')
    if w[0x290]!=25 or w[0x293]!=1 or w[4] or w[0x2A7] or struct.unpack_from('<H',w,10)[0]!=1 or w[0x292] or u32(w,0x518):raise ValueError('next animation phase1 scope')
    aw=bytearray(w[0x48:0xA0]);ptr=before[0]['pointer']+0x48
    if aw[8] or aw[11] or u32(aw,4)!=inputs['main_program_pointer'] or inputs['main_program_pointer']!=inputs['main_metadata_pointer']+main['offset'] or struct.unpack_from('<h',aw,14)[0]!=29:raise ValueError('next original main frame')
    if inputs['metadata_bindings'][0]['metadata_sha256']!=main['metadata_sha256'] or inputs['metadata_bindings'][1]['metadata_sha256']!=s['attachments'][0]['metadata_sha256']:raise ValueError('next metadata identities')
    nodes=[];p=u32(aw,0x20)
    for rule,timer in zip(s['attachments'][::-1],(28,4)):
        at=p-POOL
        if at<0 or at%NODE or at+NODE>len(d['pool']):raise ValueError('next source linked bounds')
        node=bytearray(d['pool'][at:at+NODE])
        if node[0]!=1 or node[2]!=1 or node[8]!=1 or node[11] or u32(node,0x24)!=ptr or u32(node,4)!=inputs['metadata_bindings'][1]['metadata_pointer']+rule['offset'] or struct.unpack_from('<h',node,14)[0]!=timer:raise ValueError('next exact attached frame')
        if u32(node,0x34) or u32(node,0x40) or u32(node,0x2C)!=u32(aw,0x2C) or struct.unpack_from('<h',node,0x48)[0]:raise ValueError('next empty attached queues/zero frame delay')
        node[1]=1;put(node,14,timer-1,'h');d['pool'][at:at+NODE]=node;nodes.append(p);p=u32(node,0x20)
    if p:raise ValueError('next exactly two linked nodes')
    for pos in [0x48]+[0xA0+n*NODE for n in range(5)]:
        if u32(w,pos+0x34) or u32(w,pos+0x40) or (pos!=0x48 and (u32(w,pos+4) or u32(w,pos+0x20))):raise ValueError('next empty effects/auxiliary scope')
    aw[1]=1;put(aw,14,28,'h');w[0x48:0xA0]=aw;w[4]=0;put(w,10,2,'H')
    out=deepcopy(before)
    for r in out:r['hex']=d[r['name']].hex()
    return dict(after=out,main_return=0,auxiliary_returns=[1]*5,frame_waits=[28,27,3],linked_order=nodes,work_counter=2)
