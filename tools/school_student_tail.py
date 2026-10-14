"""Independent first-unit empty event/damage tail, regeneration and map totals."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE
from tools.school_unitctrl_map_emulation import map_resource
from tools.school_world_lists import vision_merge
from tools.school_world_command import STRIDE,COUNT,cell
from tools.school_student_action import POOL,NODE,SLOTS

FUNCTIONS=(0x482A30,0x482AC0,0x4918D0,0x491960,0x493450,0x472370,0x469220,0x472550,0x472770,
  0x430400,0x43BB90,0x4305C0,0x4DDBB0,0x46B2C0,0x469480,0x46A430,0x46A5E0,0x468D10)
PROBES=[{'hp_gap':0,'mp_gap':0,'state':1,'hp_counter':17,'mp_counter':19},
 {'hp_gap':1,'mp_gap':1,'state':1,'hp_counter':0,'mp_counter':0},
 {'hp_gap':1,'mp_gap':1,'state':1,'hp_counter':262,'mp_counter':124},
 {'hp_gap':1,'mp_gap':1,'state':2,'hp_counter':130,'mp_counter':249},
 {'hp_gap':1,'mp_gap':1,'state':1,'hp_counter':32767,'mp_counter':32767},
 {'hp_gap':117,'mp_gap':445,'state':1,'hp_counter':262,'mp_counter':124}]


@lru_cache(maxsize=1)
def source_contract():
    exe=SOURCE.read_bytes()
    if hashlib.sha256(exe).hexdigest()!=SOURCE_SHA256:raise ValueError('student tail source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);functions=[]
    for a in FUNCTIONS:
        end=next((i.address+i.size for i in md.disasm(exe[a-BASE:a-BASE+4096],a) if i.mnemonic=='ret'),None)
        if end is None:raise ValueError('student tail complete source range')
        functions.append({'va':hex(a),'end':hex(end),'sha256':hashlib.sha256(exe[a-BASE:end-BASE]).hexdigest()})
    checks={0x46B868:('call','0x482a30'),0x46B878:('call','0x4918d0'),0x46B884:('call','0x493450'),
      0x46B890:('call','0x472370'),0x46B8BA:('call','0x472770'),0x46B8C6:('call','0x430400'),
      0x46B956:('call','0x43d270'),0x46BA07:('ret','8'),0x43BCDF:('and','eax, 0xff'),
      0x4692AA:('cmp','byte ptr [ebp - 8], 2'),0x4692B0:('cmp','byte ptr [ebp - 8], 4')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(exe[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('student tail exact operand '+hex(a))
        proof.append({'va':hex(a),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    raw,identity=map_resource('map05.bin');category=exe[0x6B2D8A-BASE+10*64]
    return {'source_image_sha256':SOURCE_SHA256,'functions':functions,'instructions':proof,'map_source':identity,
       'map_dimensions':[64,96],'cell_stride':6,'cell_event_offset':2,'record_class':10,'source_class_category':category,
       'source_class_mask':1<<(category-1) if 1<=category<=5 else 0,
       'scope':'First actual empty-queue full-value unit tail and declared isolated regen probes; no nonempty damage/AI/VM/world completion'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])
def i16(value):return (value+32768)%65536-32768
def get(buf,at):return struct.unpack_from('<h',buf,at)[0]
def put(buf,at,value):struct.pack_into('<h',buf,at,i16(value))


def regen(work,record):
    if len(work)!=STRIDE or len(record)!=176:raise ValueError('regen complete work/record')
    w=bytearray(work);r=bytearray(record);heals=[];special=2<=r[15]<=4
    maxima=[get(r,0x14),get(r,0x1A)];values=[get(r,0x16),get(r,0x1C)]
    if any(not 0<=cur<=cap<=32767 for cur,cap in zip(values,maxima)):raise ValueError('regen supported HP/MP values')
    for kind,maxat,curat,periodat,counterat,adjustat in ((0,0x14,0x16,0x18,0x504,0x508),(1,0x1A,0x1C,0x1E,0x506,0x50A)):
        cap,cur=get(r,maxat),get(r,curat)
        needs=(cur>0 and cur<cap) if kind==0 else cur==0 or cur<cap
        if not needs:put(w,counterat,0);continue
        count=i16(get(w,counterat)+1);put(w,counterat,count);threshold=get(r,periodat)-get(w,adjustat)
        if special:
            n=threshold*(50 if kind==0 else 200);threshold=(abs(n)//100)*(-1 if n<0 else 1)
        if threshold<0:threshold=1
        if threshold<=count:
            put(w,counterat,0);put(r,curat,min(cap,cur+1,32767));heals.append([kind,1])
    return {'work_hex':w.hex(),'record_hex':r.hex(),'heals':heals}


def project(inputs,before):
    s=source_contract();out=deepcopy(before)
    names=['works','record','region_stats','fog_current','fog_history','occupancy','pool','control','task','current_work']
    sizes=[STRIDE*COUNT,176,2048,6144,6144,12288,NODE*SLOTS,50,400,4]
    if [r['name'] for r in out]!=names or [r['bytes'] for r in out]!=sizes:raise ValueError('student tail complete owned regions')
    data={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(data[r['name']])!=r['bytes'] for r in out):raise ValueError('student tail complete owned byte lengths')
    w=data['works'];record=data['record'];ctrl=data['control']
    if record[15]!=1 or record[164]!=inputs['team'] or inputs['team']!=0 or struct.unpack_from('<H',record,0xC)[0]!=10:raise ValueError('student actual display/team/class scope')
    if ctrl[4]!=1 or ctrl[24]!=1 or ctrl[26]!=5 or ctrl[9] or ctrl[10]:raise ValueError('student tail action/opening/AI gates')
    for at in [0x48]+[0xA0+i*88 for i in range(5)]:
        if struct.unpack_from('<I',w,at+0x34)[0] or struct.unpack_from('<I',w,at+0x40)[0]:raise ValueError('student nonempty animation effect/damage events unsupported')
    if struct.unpack_from('<I',w,0x510)[0] or get(record,0x14)!=get(record,0x16) or get(record,0x1A)!=get(record,0x1C) or get(record,0x16)<=0:raise ValueError('student actual empty damage/full live values')
    if w[0x14] or w[0x34]:raise ValueError('student modified view unsupported')
    recovered=regen(w[:STRIDE],record);w[:STRIDE]=bytes.fromhex(recovered['work_hex']);data['record'][:]=bytes.fromhex(recovered['record_hex'])
    x,y=struct.unpack_from('<2i',w,0x2EC);cx,cy=cell(x,32),cell(y,16)
    if not 0<=cx<64 or not 0<=cy<96:raise ValueError('student source map cell bounds')
    raw,identity=map_resource('map05.bin')
    if inputs['map_sha256']!=identity['sha256']:raise ValueError('student actual map source identity')
    event=raw[0x10+(cy*64+cx)*6+2]
    if event<32:
        at=event*64+record[164]*4;put(data['region_stats'],at,get(data['region_stats'],at)+1)
        data['region_stats'][at+2]|=s['source_class_mask']
    view=min(32,max(0,record[44]-256 if record[44]>=128 else record[44]))
    current,history=vision_merge(data['fog_current'],data['fog_history'],cx,cy,view)
    data['fog_current'][:]=current;data['fog_history'][:]=history
    oldx,oldy=w[0x4E7:0x4E9]
    if [oldx,oldy]!=[cx,cy]:raise ValueError('student actual stationary cell scope')
    w[0x4E7:0x4EB]=bytes([cx,cy,oldx,oldy])
    for r in out:r['hex']=data[r['name']].hex()
    return {'after':out,'cell':[cx,cy],'event_region':event,'event_class_mask':s['source_class_mask'],
      'vision_args':[cx,cy,view],'actual_heals':recovered['heals'],'first_unit_completed':True,'next_slot':1}
