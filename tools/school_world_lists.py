"""Independent original opening visibility and 250-slot display/category policy."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE
from tools.school_map_common_emulation import map_common_resource
from tools.school_map_common_catalog import map_common_inputs
from tools.school_world_map import i16

FUNCTIONS=(0x49B180,0x49B9F0,0x43D270,0x43D1A0,0x43D200,0x46E520,0x46E730,
           0x468D10,0x469480,0x4695D0,0x46B130,0x46A430,0x46A550,0x46A5E0,0x46A950)


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('list source image identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);ranges=[]
    for a in FUNCTIONS:
        end=next((i.address+i.size for i in md.disasm(raw[a-BASE:a-BASE+2048],a) if i.mnemonic=='ret'),None)
        if end is None:raise ValueError('list complete return range')
        ranges.append((a,end))
    checks={0x468D5A:('movsx','edx, word ptr [ecx]'),0x4694D2:('mov','al, byte ptr [edx + 0xf]'),
       0x4694D5:('cmp','eax, 1'),0x46962C:('cmp','byte ptr [ebp - 8], 1'),0x469632:('cmp','byte ptr [ebp - 8], 5'),
       0x46A48C:('mov','cl, byte ptr [eax + 0xa4]'),0x46A497:('mov','al, byte ptr [edx + 0x2ef44]'),
       0x46A98F:('shl','edx, 4'),0x46A995:('lea','ecx, [eax + edx + 0x115aac]'),
       0x46A9BD:('jmp','dword ptr [ecx*4 + 0x46aa22]'),
       0x46B4EB:('call','0x46e520'),0x46B4F3:('call','0x46e730'),0x46B4FB:('call','0x48cd90'),
       0x49BA39:('call','0x43d270')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(raw[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('list source predicate '+hex(a))
        proof.append({'va':hex(a),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    targets=struct.unpack_from('<4I',raw,0x46AA22-BASE)
    if [next(md.disasm(raw[a-BASE:a-BASE+8],a)).op_str for a in targets]!=['eax, 4','eax, 1','eax, 2','eax, 3']:
        raise ValueError('list relation jump table')
    map_raw,meta=map_common_resource();entries=map_common_inputs(map_raw)['first_section_entries'];sizes=raw[0x59558C-BASE:0x5955CE-BASE]
    masks=[]
    for n,e in enumerate(entries):
        w,h=sizes[n*2:n*2+2];payload=map_raw[e['file_offset']:e['file_offset']+e['bytes']]
        if (w,h)!=(2*n+1,2*n+1) or len(payload)!=(w*h+3)//4*4 or any(payload[w*h:]):raise ValueError('source mask shape/padding')
        masks.append({'view':n,'width':w,'height':h,'file_offset':e['file_offset'],'payload_bytes':e['bytes'],
                      'payload_hex':payload.hex(),'sha256':hashlib.sha256(payload).hexdigest()})
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'functions':[{'va':hex(a),'end':hex(b),'sha256':hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()} for a,b in ranges],
        'instructions':proof,'mapcom':meta,'masks':masks,'work_stride':0x520,'work_slots':250,
        'used_word_offset':0,'record_pointer_offset':0x258,'record_state_offset':15,'record_group_offset':0xA4,
        'viewport_bounds':[-64,1088,-34,664],'display_count_offset':0xDC30C,'category_base_offset':0xDC8EC,
        'category_stride':1004,'scope':'Opening visibility and lists only; no original action/AI/VM/waves/world completion'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def viewport(x,y):
    if type(x) is not int or type(y) is not int:raise ValueError('viewport short inputs')
    return -64<=i16(x)<=1088 and -34<=i16(y)<=664


def vision_merge(current,history,x,y,view):
    if type(view) is not int or not 0<=view<=32 or type(x) is not int or type(y) is not int or not 0<=x<64 or not 0<=y<96:
        raise ValueError('unsupported finite view input')
    if len(current)!=6144 or len(history)!=6144:raise ValueError('vision complete planes')
    mask=source_contract()['masks'][view];w,h=mask['width'],mask['height'];pixels=bytes.fromhex(mask['payload_hex'])
    out=bytearray(current);old=bytearray(history)
    for my in range(h):
        yy=y-view+my
        if not 0<=yy<96:continue
        for mx in range(w):
            xx=x-view+mx
            if not 0<=xx<64:continue
            value=pixels[my*w+mx]
            if not value:continue
            index=yy*64+xx;out[index]=max(out[index],value);old[index]=max(old[index],out[index])
    return bytes(out),bytes(old)


def project(inputs,regions):
    source_contract();out=deepcopy(regions)
    if [r['name'] for r in out]!=['window','fog_current','fog_history','visible','categories'] or [r['bytes'] for r in out]!=[20,6144,6144,1004,5020]:
        raise ValueError('list complete output regions')
    data={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(data[r['name']])!=r['bytes'] for r in out):raise ValueError('list full buffer lengths')
    rows=inputs['works'];team=inputs['team'];matrix=bytes.fromhex(inputs['relation_hex'])
    if len(rows)!=250 or [r['index'] for r in rows]!=list(range(250)) or type(team) is not int or not 0<=team<16 or len(matrix)!=256 or any(v>3 for v in matrix):
        raise ValueError('list source row/matrix/group bounds')
    if inputs['opening']!=1 or inputs['event']!=0 or inputs['dimensions']!=[64,96]:raise ValueError('actual opening list scope')
    current,history=vision_merge(data['fog_current'],data['fog_history'],*inputs['origin'],inputs['view'])
    data['window'][7]=0;data['fog_current'][:]=current;data['fog_history'][:]=history
    admitted=[];categories=[[],[],[],[],[]];cx,cy=inputs['camera']
    for r in rows:
        if type(r['used_word']) is not int or not -32768<=r['used_word']<=32767 or type(r['pointer']) is not int:raise ValueError('list work input type')
        if not r['used_word']:continue
        record=bytes.fromhex(r['record_hex'])
        if len(record)!=176 or record[0xA4]>=16:raise ValueError('list complete record/group')
        state,group=record[15],record[164]
        if any(type(r[k]) is not int or not -0x80000000<=r[k]<=0x7FFFFFFF for k in ('x_fixed','y_fixed')):raise ValueError('list signed fixed coordinates')
        if state==1:
            if viewport(i16(r['x_fixed']>>16)-cx,i16(r['y_fixed']>>16)-cy+30):admitted.append(r)
            categories[0].append(r['pointer'])
            own=group==team;relation=0 if own else [4,1,2,3][matrix[team*16+group]]
            if relation in (1,2):categories[2].append(r['pointer'])
            if own:categories[3].append(r['pointer'])
            if own or matrix[team*16+group]==0:categories[4].append(r['pointer'])
        if state in (0,2,3,4,5):categories[1].append(r['pointer'])
    # Original pairwise exchange. Equal-depth items can be reversed by a later
    # greater-depth exchange; a stable language sort is not equivalent.
    for i in range(len(admitted)-1):
        for j in range(i+1,len(admitted)):
            if admitted[i]['y_fixed']<admitted[j]['y_fixed']:admitted[i],admitted[j]=admitted[j],admitted[i]
    pointers=[r['pointer'] for r in admitted]
    struct.pack_into('<I',data['visible'],0,len(pointers))
    for i,p in enumerate(pointers):struct.pack_into('<I',data['visible'],4+i*4,p)
    for n,values in enumerate(categories):
        struct.pack_into('<I',data['categories'],n*1004,len(values))
        for i,p in enumerate(values):struct.pack_into('<I',data['categories'],n*1004+4+i*4,p)
    for r in out:r['hex']=data[r['name']].hex()
    return {'after':out,'display_indices':[r['index'] for r in admitted],'category_counts':[len(v) for v in categories],
            'occupied_slots':sum(bool(r['used_word']) for r in rows),'display_state1_slots':len(categories[0])}
