"""Source-only first student pose, persistent attachments and first frame step."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE
from tools.school_first_unit_animation_emulation import unit_resource
from tools.school_unit_assets_emulation import effect_resource
from tools.dxanim_lib import parse_dxanim
from tools.school_world_command import STRIDE,COUNT,cell

POOL=0x765728;NODE=88;SLOTS=2048
FUNCTIONS=(0x475D60,0x46C040,0x46BCC0,0x465040,0x409FF0,0x409F70,0x40A400,0x4214F0,0x40A520,0x409FB0,
  0x468EB0,0x468D80,0x468E10,0x46BE50,0x465140,0x40AF40,0x40B5E0,0x409EF0,0x40A800,0x47A8E0,
  0x475700,0x480A60,0x490350,0x490A50,0x4690A0,0x40A100,0x468D10)


def program(raw,bank,index):
    offsets=parse_dxanim(raw);head=offsets[bank]
    count=struct.unpack_from('<I',raw,head+4)[0]
    if not 0<=index<count:raise ValueError('student source program bounds')
    at=head+struct.unpack_from('<I',raw,head+8+index*4)[0];frame=raw[at:at+10]
    if len(frame)!=10 or frame[0]&15:raise ValueError('student unsupported first opcode/event flags')
    sprite=frame[2]+((struct.unpack_from('<H',frame,6)[0]&15)<<8)
    sprite_hex=None
    if sprite<4095:
        sprite_hex=raw[offsets[4]+sprite*10:offsets[4]+sprite*10+10].hex()
        if len(sprite_hex)!=20:raise ValueError('student source sprite bounds')
    return {'bank':bank,'index':index,'offset':at,'frame_hex':frame.hex(),'duration':struct.unpack_from('<h',frame,8)[0],
       'sprite':sprite,'sprite_hex':sprite_hex,'metadata_bytes':offsets[6],'metadata_sha256':hashlib.sha256(raw[:offsets[6]]).hexdigest()}


@lru_cache(maxsize=1)
def source_contract():
    exe=SOURCE.read_bytes()
    if hashlib.sha256(exe).hexdigest()!=SOURCE_SHA256:raise ValueError('student source executable identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);functions=[]
    for a in FUNCTIONS:
        end=next((i.address+i.size for i in md.disasm(exe[a-BASE:a-BASE+8192],a) if i.mnemonic=='ret'),None)
        if end is None:raise ValueError('student complete source function')
        functions.append({'va':hex(a),'end':hex(end),'sha256':hashlib.sha256(exe[a-BASE:end-BASE]).hexdigest()})
    checks={0x475DAE:('push','2'),0x475DBC:('push','0x12'),0x475DDE:('push','0x80f'),0x475E12:('add','eax, 0x834'),
      0x475E73:('mov','byte ptr [ecx], al'),0x40B60F:('cmp','dword ptr [ebp - 8], 0x800'),
      0x40B630:('add','eax, 0x765728'),0x40B639:('call','0x409ef0')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(exe[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('student exact source operand '+hex(a))
        proof.append({'va':hex(a),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    direction=exe[0x610510-BASE+2];lookup=exe[0x60D160-BASE+(18*8+direction)*2:0x60D160-BASE+(18*8+direction)*2+2]
    code=struct.unpack_from('<H',exe,0x60DFC8-BASE+lookup[0]*2)[0]
    raw,identity=unit_resource();efct,eidentity=effect_resource();main=program(raw,code>>8,code&255);attachments=[]
    for animation in (2063,2103):
        at=0x60F890-BASE+((animation//1000)-1)*800+(animation%1000)*4;definition=exe[at:at+4]
        p=program(efct,definition[1],definition[2]);p.update({'animation':animation,'definition_hex':definition.hex()});attachments.append(p)
    if [p['duration'] for p in [main]+attachments]!=[30,6,30]:raise ValueError('student current supported frame timers')
    return {'source_image_sha256':SOURCE_SHA256,'functions':functions,'instructions':proof,'main_source':identity,'effect_source':eidentity,
       'pose':18,'direction':2,'direction_index':direction,'pose_lookup_hex':lookup.hex(),'pose_code':code,'main':main,'attachments':attachments,
       'pool':POOL,'pool_slots':SLOTS,'node_bytes':NODE,'scope':'First mode25/job3 student phase0 and first original frame update only; no full unit/world/VM/AI completion'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def u32(buf,at):return struct.unpack_from('<I',buf,at)[0]
def put(buf,at,value,fmt='I'):struct.pack_into('<'+fmt,buf,at,value)


def validate(inputs,before):
    s=source_contract()
    if [r['name'] for r in before]!=['works','pool','control','task','current_work'] or [r['bytes'] for r in before]!=[STRIDE*COUNT,NODE*SLOTS,50,400,4]:raise ValueError('student complete owned regions')
    data={r['name']:bytearray.fromhex(r['hex']) for r in before}
    if any(len(data[r['name']])!=r['bytes'] for r in before):raise ValueError('student complete owned byte lengths')
    w=data['works'];record=bytes.fromhex(inputs['record_hex']);aw=w[0x48:0xA0]
    if len(record)!=176 or record[15]!=1 or record[164]!=0 or struct.unpack_from('<H',record,2)[0]!=3:raise ValueError('student exact current record eligibility')
    if not struct.unpack_from('<h',w)[0] or w[0x290]!=25 or w[0x293] or w[0x2A7] or u32(w,0x518) or u32(aw,0x20):raise ValueError('student exact first initializer mode/chain')
    if data['control'][4]!=1 or data['control'][24]!=1 or data['control'][26]!=5 or data['control'][9] or data['control'][10]:raise ValueError('student action/opening/AI scope')
    if inputs['main_controller']!=u32(w,0x44) or inputs['main_program_pointer']!=inputs['main_metadata_pointer']+s['main']['offset']:raise ValueError('student source main program binding')
    return data


def frame_setup(aw,pc,p):
    frame=bytes.fromhex(p['frame_hex'])
    if frame[0]&15:raise ValueError('student unsupported frame/events')
    put(aw,4,pc);put(aw,0x28,pc);put(aw,0xE,p['duration'],'h')
    if p['sprite']<4095:put(aw,0x18,bytes.fromhex(p['sprite_hex'])[8])


def bind_project(inputs,before):
    data=validate(inputs,before);s=source_contract();w=data['works'];aw=bytearray(w[0x48:0xA0]);pointer=inputs['work_pointer']+0x48
    w[0x28A]=2;put(aw,0xC,18,'h');aw[3]=bytes.fromhex(s['pose_lookup_hex'])[1]&3;aw[8]=0;put(aw,0x18,7)
    put(aw,0x12,0,'h');put(aw,0x14,0,'h');put(aw,0x24,pointer);aw[0xB]=0;put(aw,0x10,0,'h')
    frame_setup(aw,inputs['main_program_pointer'],s['main']);w[0x48:0xA0]=aw;w[4]=0;put(w,10,0,'h')
    return output(before,data)


def output(before,data):
    out=deepcopy(before)
    for r in out:r['hex']=data[r['name']].hex()
    return out


def initialized_project(inputs,before):
    bound=bind_project(inputs,before);data={r['name']:bytearray.fromhex(r['hex']) for r in bound};s=source_contract();w=data['works'];pool=data['pool'];aw=bytearray(w[0x48:0xA0]);nodes=[]
    for n,p in enumerate(s['attachments']):
        index=next((i for i in range(SLOTS) if pool[i*NODE]==0),None)
        if index is None:raise ValueError('student supported pool requires two available nodes')
        ptr=POOL+index*NODE;node=bytearray(NODE);node[0]=1;put(node,0xC,-1,'h');node[0x54:0x57]=bytes([128])*3
        definition=bytes.fromhex(p['definition_hex']);node[3]=(aw[3] if not definition[0]&128 else 128)|64
        put(node,0x1C,inputs['effect_controller']);node[2]=1;put(node,0x24,u32(aw,0x24));put(node,0x20,u32(aw,0x20));put(aw,0x20,ptr)
        put(node,0x12,struct.unpack_from('<h',aw,0x12)[0],'h');put(node,0x14,struct.unpack_from('<h',aw,0x14)[0],'h');node[8]=aw[8]+1;put(node,0x18,7)
        if u32(aw,0x2C):put(node,0x2C,u32(aw,0x2C));node[0x48:0x54]=aw[0x48:0x54]
        frame_setup(node,inputs['attachment_program_pointers'][n],p);node[1]=1;put(node,0xE,p['duration']-1,'h')
        pool[index*NODE:(index+1)*NODE]=node;nodes.append(ptr)
    w[0x48:0xA0]=aw;x,y=struct.unpack_from('<2i',w,0x2EC);w[0x2E8]=cell(x,32)&255;w[0x2E9]=cell(y,16)&255;w[0x293]=1
    return {'after':output(before,data),'allocated_nodes':nodes,'linked_order':nodes[::-1]}


def animated_project(inputs,before):
    initialized=initialized_project(inputs,before);data={r['name']:bytearray.fromhex(r['hex']) for r in initialized['after']};w=data['works'];pool=data['pool']
    aw=bytearray(w[0x48:0xA0]);aw[1]=1
    if struct.unpack_from('<h',aw,0xE)[0]<=1:raise ValueError('student unsupported frame expiry')
    put(aw,0xE,struct.unpack_from('<h',aw,0xE)[0]-1,'h');w[0x48:0xA0]=aw
    for ptr in initialized['linked_order']:
        at=ptr-POOL;pool[at+1]=1;timer=struct.unpack_from('<h',pool,at+0xE)[0]
        if timer<=1:raise ValueError('student unsupported attached frame expiry')
        put(pool,at+0xE,timer-1,'h')
    for n in range(5):
        at=0xA0+n*NODE
        if u32(w,at+4) or u32(w,at+0x20):raise ValueError('student active auxiliary unsupported')
    w[4]=0;put(w,10,(struct.unpack_from('<H',w,10)[0]+1)&65535,'H')
    return {**initialized,'after':output(before,data),'main_return':0,'auxiliary_returns':[1]*5,'frame_waits':[29,4,28],'work_counter':1}
