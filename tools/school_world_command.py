"""Independent original paused queue/input/unit policy; no runtime authority."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE
from tools.school_world_lists import vision_merge

FUNCTIONS=(0x48CD90,0x427DE0,0x46EA10,0x493670,0x4945B0,0x4947B0,
           0x494620,0x494690,0x4128F0,0x46F170,0x4690A0,0x46F440,
           0x46B760,0x46B2C0,0x4DDBB0,0x43C470)
STRIDE=0x520;COUNT=250


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('command source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);functions=[]
    for a in FUNCTIONS:
        end=next((i.address+i.size for i in md.disasm(raw[a-BASE:a-BASE+4096],a) if i.mnemonic=='ret'),None)
        if end is None:raise ValueError('command complete function')
        functions.append({'va':hex(a),'end':hex(end),'sha256':hashlib.sha256(raw[a-BASE:end-BASE]).hexdigest()})
    checks={0x48CDBD:('add','ecx, 0x1798'),0x427E00:('cmp','dword ptr [eax + 0x10], 0'),
      0x46B503:('call','0x46ea10'),0x46B50B:('call','0x46f440'),0x46B521:('call','0x56cec0'),
      0x46B53B:('cmp','dword ptr [ebp - 8], 0xfa'),0x46B57F:('call','0x46b760'),
      0x46B79B:('movsx','ecx, byte ptr [eax + 0x108b34]'),0x46B7A6:('jmp','0x46b9ed'),
      0x46B9ED:('jmp','0x46b8cb'),0x46B8D2:('call','0x469480'),0x46B956:('call','0x43d270'),
      0x46F209:('movsx','ecx, byte ptr [eax + edx + 0x80d78]'),
      0x46F475:('mov','word ptr [ecx + 0x30992], 0xffff'),0x46F48C:('jmp','0x46f86e')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(raw[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('command source operand '+hex(a))
        proof.append({'va':hex(a),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    return {'source_image_sha256':SOURCE_SHA256,'functions':functions,'instructions':proof,
      'scope':'Empty queue, declared no-command input, selection and paused unit loop; no actions/animation/AI/VM completion',
      'work_slots':COUNT,'work_stride':STRIDE,'cursor_bytes':10,'selection_bytes':1016,'work_scratch_bytes':2048}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def signed8(v):return v-256 if v>=128 else v


def normalize_selection(works,records,team):
    """Original46F170: work selection flag is independent of record state."""
    out=bytearray(works);rows=[];own_selected=active_selected=0
    if len(out)!=STRIDE*COUNT or len(records)!=COUNT or not 0<=team<16:raise ValueError('selection full inputs')
    for i,rec in enumerate(records):
        at=i*STRIDE
        if not struct.unpack_from('<h',out,at)[0]:continue
        if len(rec)!=176 or rec[164]>=16:raise ValueError('selection complete record')
        own=rec[164]==team;selected=out[at+0x28C]!=0
        if own and selected:
            own_selected+=1;active_selected+=int(rec[15]==1)
        elif not own and (12<=signed8(out[at+0x290])<=13 or rec[15]!=1):out[at+0x28C]=0
    for i,rec in enumerate(records):
        at=i*STRIDE
        if not struct.unpack_from('<h',out,at)[0]:continue
        if own_selected and rec[164]!=team or active_selected and rec[15]!=1:out[at+0x28C]=0
        if out[at+0x28C]:rows.append(i)
    kind=0 if not rows else 1 if own_selected and active_selected else 2 if own_selected else 3
    return bytes(out),rows,kind


def cell(fixed,divisor):
    if type(fixed) is not int or not -0x80000000<=fixed<=0x7FFFFFFF:raise ValueError('signed fixed cell')
    high=fixed>>16
    return (high+(divisor-1 if fixed<0 else 0))//divisor


def project(inputs,regions):
    source_contract();out=deepcopy(regions)
    names=['queue','works','selection','cursor','scratch','fog_current','fog_history','occupancy','current_work']
    sizes=[20,STRIDE*COUNT,1016,10,2048,6144,6144,12288,4]
    if [r['name'] for r in out]!=names or [r['bytes'] for r in out]!=sizes:raise ValueError('command complete regions')
    data={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(data[r['name']])!=r['bytes'] for r in out):raise ValueError('command full buffers')
    if struct.unpack_from('<I',data['queue'],16)[0] or data['queue'][8:16]!=bytes(8):raise ValueError('nonempty queue unsupported')
    if inputs['gates']!=[1,0,0,0,0,0] or inputs['map_state']!=0 or inputs['task_mouse']!=[0,0,0] or inputs['ctrl_keys']!=[0,0]:raise ValueError('paused no-command gate/input scope')
    records=[bytes.fromhex(r) if r is not None else None for r in inputs['record_hex']]
    works,selected,kind=normalize_selection(data['works'],records,inputs['team']);data['works'][:]=works
    struct.pack_into('<2I',data['selection'],0,len(selected),kind)
    for n,i in enumerate(selected):struct.pack_into('<I',data['selection'],16+n*4,inputs['work_base']+i*STRIDE)
    data['cursor'][:]=bytes(6)+b'\xff\xff'+bytes(2);data['scratch'][:]=bytes(2048)
    occupied=[];active=[];vision=[];changed=[];matrix=bytes.fromhex(inputs['relations'])
    if len(matrix)!=256 or any(v>3 for v in matrix):raise ValueError('command relation matrix')
    for i,rec in enumerate(records):
        at=i*STRIDE
        if not struct.unpack_from('<h',data['works'],at)[0]:continue
        occupied.append(i)
        if rec[15]!=1:continue
        active.append(i);x,y=struct.unpack_from('<2i',works,at+0x2EC);cx,cy=cell(x,32),cell(y,16)
        if rec[164]==inputs['team'] or matrix[inputs['team']*16+rec[164]]==0:
            if works[at+0x34] in (46,47) or works[at+0x14]==6:raise ValueError('modified vision unsupported')
            view=min(32,max(0,signed8(rec[44])))
            current,history=vision_merge(data['fog_current'],data['fog_history'],cx,cy,view)
            data['fog_current'][:]=current;data['fog_history'][:]=history
            vision.append({'index':i,'args':[cx,cy,view]})
        oldx,oldy=works[at+0x4E7:at+0x4E9];newx,newy=cx&255,cy&255
        data['works'][at+0x4E7:at+0x4EB]=bytes([newx,newy,oldx,oldy])
        if (newx,newy)!=(oldx,oldy):
            calls=[]
            for xx,yy,delta in ((oldx,oldy,-1),(newx,newy,1)):
                calls.append([xx,yy,int(delta>0)])
                if xx!=255 and yy!=255:
                    if not 0<=xx<64 or not 0<=yy<96:raise ValueError('finite occupancy bounds')
                    k=2*(yy*64+xx)+1;data['occupancy'][k]=(data['occupancy'][k]+delta)&255
            changed.append({'index':i,'calls':calls})
    data['current_work'][:]=bytes(4)
    for r in out:r['hex']=data[r['name']].hex()
    return {'after':out,'occupied_indices':occupied,'active_indices':active,'selected_indices':selected,
            'selection_kind':kind,'vision_calls':vision,'cell_changes':changed}
