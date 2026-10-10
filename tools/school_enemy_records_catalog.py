"""Independent EXE template/profile/numeric/overlay rules for scene5 records."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM,X86_OP_REG
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE=ROOT/'analysis/school-enemy-records-v2-20261010.json'
EVIDENCE_SHA256='afe6d5f2e9076de16c294cf305342e8208aa29fa31c3abe1096c6f28ac4e3e21'
COUNTER_EVIDENCE=ROOT/'analysis/school-enemy-record-counter-v1-20261010.json'
COUNTER_SHA256='a1d74b5b10cc011fff805d55532b15186eecb712400aea6e99ac9b1cfcf3d491'


def digest(raw):return hashlib.sha256(raw).hexdigest()
def word(raw,at):return struct.unpack_from('<H',raw,at)[0]
def signed(raw,at):return struct.unpack_from('<h',raw,at)[0]
def trunc(value,divisor=100):return (1 if value>=0 else -1)*(abs(value)//divisor)


def source_catalog():
    image=SOURCE.read_bytes()
    if digest(image)!=SOURCE_SHA256:raise ValueError('scene record EXE identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True
    code=[]
    def instruction(va,mnemonic):
        i=next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        if i.mnemonic!=mnemonic:raise ValueError('scene record source instruction changed')
        code.append({'va':hex(va),'instruction_hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
        return i
    def value(va,mnemonic):
        op=instruction(va,mnemonic).operands[-1]
        if op.type==X86_OP_IMM:return op.imm
        if op.type==X86_OP_MEM:return op.mem.disp
        raise ValueError('scene record constant source operand')
    pointer_table=value(0x45356B,'mov');count_table=value(0x45357C,'movsx')
    scene=5;pointer=struct.unpack_from('<I',image,pointer_table-BASE+scene*4)[0]
    count=signed(image,count_table-BASE+scene*2);stride=value(0x45360D,'imul')
    if count!=35 or stride!=84:raise ValueError('supported scene template shape')
    templates=[image[pointer-BASE+i*stride:pointer-BASE+(i+1)*stride].hex() for i in range(count)]
    profile_base=value(0x4DA61C,'add');profile_stride=value(0x4DA619,'imul');profile_subtract=value(0x4DA614,'sub')
    character_base=value(0x4DA649,'add');character_stride=value(0x4DA643,'imul')
    characters={str(signed(bytes.fromhex(t),0)):{'pointer':character_base+signed(bytes.fromhex(t),0)*character_stride,
        'row_hex':image[character_base-BASE+signed(bytes.fromhex(t),0)*character_stride:
            character_base-BASE+(signed(bytes.fromhex(t),0)+1)*character_stride].hex()}
        for t in templates if signed(bytes.fromhex(t),0)<profile_subtract}
    job_base=value(0x4DFC48,'add');archetype_base=value(0x4DFC5B,'add')
    profiles={}
    for text in templates:
        identity=signed(bytes.fromhex(text),0)
        if identity>=profile_subtract:
            at=profile_base+(identity-profile_subtract)*profile_stride
            profiles[str(identity)]={'pointer':at,'profile_hex':image[at-BASE:at-BASE+profile_stride].hex()}
    jobs={};archetypes={}
    # Character profiles may select any valid source job. All original fixed job rows
    # are inputs, not copied native record outputs.
    job_ids=set(range(40))|{signed(bytes.fromhex(p['profile_hex']),2) for p in profiles.values()}
    for j in sorted(job_ids):
        raw=image[job_base-BASE+j*64:job_base-BASE+(j+1)*64]
        if len(raw)!=64:raise ValueError('source job row bounds')
        k=signed(raw,0x18)
        if 0<=k<1024:
            jobs[str(j)]={'pointer':job_base+j*64,'row_hex':raw.hex()}
            at=archetype_base+k*72
            archetypes[str(k)]={'pointer':at,'row_hex':image[at-BASE:at-BASE+72].hex()}
    clamps={};signed_reads={}
    for i in md.disasm(image[0x4E0A00-BASE:0x4E1A07-BASE],0x4E0A00):
        if i.mnemonic in ('mov','movsx','movzx') and len(i.operands)==2:
            dest,src=i.operands
            if dest.type==X86_OP_REG and src.type==X86_OP_MEM and md.reg_name(src.mem.base)!='ebp':
                signed_reads[(src.mem.disp,src.size)]=i.mnemonic=='movsx'
        if i.mnemonic=='mov' and len(i.operands)==2:
            dest,src=i.operands
            if dest.type==X86_OP_MEM and src.type==X86_OP_IMM and md.reg_name(dest.mem.base)!='ebp':
                clamps.setdefault((dest.mem.disp,dest.size),[]).append(src.imm)
                instruction(i.address,'mov')
    ranges=[]
    for (at,size),values in clamps.items():
        if len(values)!=2 or not 0<=at<176:raise ValueError('source normalization store pair differs')
        ranges.append({'offset':at,'bytes':size,'minimum':values[0],'maximum':values[1],
            'signed':signed_reads.get((at,size),size==4)})
    def copies(start,end,destination_ok):
        pending={};result=[]
        for i in md.disasm(image[start-BASE:end-BASE],start):
            if i.mnemonic!='mov' or len(i.operands)!=2:continue
            dest,src=i.operands
            if src.type==X86_OP_MEM and md.reg_name(src.mem.base)!='ebp' and src.mem.index==0 and dest.type==X86_OP_REG:
                pending[dest.reg]=(src.mem.disp,src.size)
            if dest.type==X86_OP_MEM and md.reg_name(dest.mem.base)!='ebp' and dest.mem.index==0 and src.type==X86_OP_REG \
                    and src.reg in pending and destination_ok(dest.mem.disp):
                at,n=pending[src.reg]
                if n!=dest.size:raise ValueError('source field copy widths differ')
                row=(at,dest.mem.disp,n)
                if row not in result:result.append(row)
                instruction(i.address,'mov')
        return result
    character_copies=copies(0x4DA652,0x4DA6F8,lambda at:0<=at<48)
    mapping=copies(0x4DA490,0x4DA5DC,lambda at:at==0xF or 0x94<=at<=0xA8)
    if len(character_copies)!=12 or len(mapping)!=15:raise ValueError('source profile/scene field copy count')
    bodies=[{'start':hex(a),'end':hex(b),'instruction_hex':image[a-BASE:b-BASE].hex(),'sha256':digest(image[a-BASE:b-BASE])}
        for a,b in ((0x453540,0x45364E),(0x4DA450,0x4DA5E8),(0x4DA5F0,0x4DA70C),(0x4DFC20,0x4E0931),(0x4E0A00,0x4E1A07))]
    first_index=value(0x45355D,'mov');index_step=value(0x4535A2,'sub')
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scene':scene,'template_pointer':pointer,
        'unit_first_index':first_index,'unit_index_decrement':index_step,
        'template_count':count,'template_stride':stride,'templates':templates,'profiles':profiles,
        'profile_base':profile_base,'profile_stride':profile_stride,'profile_subtract':profile_subtract,
        'character_base':character_base,'character_stride':character_stride,
        'character_definitions':characters,
        'character_profile_copies':[list(c) for c in character_copies],
        'job_base':job_base,'jobs':jobs,'archetype_base':archetype_base,'archetypes':archetypes,
        'engage_seconds':list(struct.unpack_from('<51I',image,0x6E4528-BASE)),
        'movement_types_hex':image[0x738C10-BASE:0x738C10-BASE+256].hex(),
        'normalization':ranges,'overlays':[{'source':a,'destination':b,'bytes':n} for a,b,n in mapping],
        'code_inputs':code,'source_branch_bodies':bodies,
        'scope':'Scene5 source record preparation only; original EXE character definitions/profile inputs, not persistent school growth; no equipped item/skill modifiers applied by this original path; unit work/assets/placement/VM unexecuted.',**AUTHORITY}


def expected_profile(template_hex,character_hex=None,rules=None):
    r=source_catalog() if rules is None else rules
    try:t=bytes.fromhex(template_hex)
    except (ValueError,TypeError) as error:raise ValueError('template encoding') from error
    if len(t)!=84 or template_hex not in r['templates']:raise ValueError('unsupported scene5 template')
    identity=signed(t,0)
    if identity<r['profile_subtract']:
        if character_hex is None:character_hex=r['character_definitions'][str(identity)]['row_hex']
        try:character=bytes.fromhex(character_hex)
        except (ValueError,TypeError) as error:raise ValueError('character input encoding') from error
        if len(character)!=r['character_stride'] or word(character,0)!=identity:raise ValueError('character input size/identity')
        profile=bytearray(48)
        for a,b,n in r['character_profile_copies']:profile[b:b+n]=character[a:a+n]
        pointer=0x7E11B0
    else:
        if character_hex is not None:raise ValueError('static profile cannot use character input')
        if str(identity) not in r['profiles']:raise ValueError('unsupported static profile')
        entry=r['profiles'][str(identity)];profile=bytes.fromhex(entry['profile_hex']);pointer=entry['pointer']
    return {'pointer':pointer,'profile_hex':profile.hex()}


def expected_record(template_hex,character_hex=None,rules=None):
    r=source_catalog() if rules is None else rules
    resolved=expected_profile(template_hex,character_hex,r);p=bytes.fromhex(resolved['profile_hex']);t=bytes.fromhex(template_hex)
    job=signed(p,2)
    if str(job) not in r['jobs']:raise ValueError('unsupported source profile job')
    j=bytes.fromhex(r['jobs'][str(job)]['row_hex']);kind=j[2]-1;k=signed(j,0x18)
    if not 0<=kind<=9 or str(k) not in r['archetypes'] or p[12]>50:raise ValueError('unsupported source profile kind/level')
    w=bytes.fromhex(r['archetypes'][str(k)]['row_hex']);a,b,c,d,e,f,g=p[5:12]
    if kind%5==2 and p[46] not in (1,2,3):raise ValueError('unsupported weapon profile type')
    out=bytearray(176)
    def put(at,v,n=2):out[at:at+n]=(v&((1<<(n*8))-1)).to_bytes(n,'little')
    put(0,word(p,0));put(2,word(p,0));out[4:11]=p[5:12];put(12,job);put(14,p[12],1);put(15,1,1)
    hp=3*f+a+b;put(20,hp);hp=signed(out,20)
    put(20,trunc(hp*word(j,6)));put(22,word(out,20))
    put(24,signed(j,8)-f-a*50//100)
    put(26,3*g+e+d);put(28,word(out,26));put(30,signed(j,12)-g-d*50//100)
    engage=r['engage_seconds'][p[12]]*60;put(32,engage,4);put(36,engage,4)
    put(40,(p[12]*10//100+10)*3600,4);put(44,j[0x12]+c*10//100,1)
    put(46,signed(j,0x14)+(word(j,0x14)>>1)*b//100)
    put(48,bytes.fromhex(r['movement_types_hex'])[j[0x16]],1)
    put(50,word(w,10));put(52,word(w,14));put(54,w[16],1)
    family=kind%5
    attack_range=w[0x12]+(d*10//100 if family in (2,3) else e*10//100 if family==4 else 0)
    if w[0x18]==6:attack_range=w[0x16]
    put(55,attack_range,1)
    accuracy=w[0x14]+(a*50//100 if family==0 else b if family==1 else c*75//100 if family==2 else 0)
    if family in (3,4):accuracy=100
    put(56,accuracy)
    stat=[a,b,c+(a//10 if p[46] in (1,3) else 0),d,e][family]
    put(58,trunc(signed(w,0x20)*stat));put(60,trunc(signed(w,0x24)*stat))
    put(62,word(w,2));put(64,w[5],1);put(65,100,1)
    put(66,signed(w,0x28)+trunc(signed(w,0x2A)*50));put(68,w[0x16],1);put(69,w[0x1A],1)
    put(72,word(w,0x1C)+word(w,0x1E)*50//100,4)
    put(76,j[0x1A]*b//100+b*25//100,1);put(77,j[0x1B]*a//100+a*15//100,1)
    put(78,j[0x1C]+f*10//100+c*5//100,1);put(79,j[0x1D]+e*15//100,1)
    put(80,j[0x1E]+g*5//100+d*10//100,1)
    put(82,trunc(signed(out,20)*j[0x21]));out[0x84:0x94]=p[14:30];put(0xA4,5,1)
    # Native narrow stores precede field-specific signed/unsigned clamps, decoded
    # from the original MOVSX versus zero-extended loads and dword comparisons.
    for limit in r['normalization']:
        at,n=limit['offset'],limit['bytes'];value=int.from_bytes(out[at:at+n],'little',signed=limit['signed'])
        put(at,max(limit['minimum'],min(limit['maximum'],value)),n)
    out[0x37]=min(out[0x37],32);out[0x44]=min(out[0x44],32)
    if t[3] not in (0,4,5,6,7):raise ValueError('unsupported source scene category')
    for field in r['overlays']:
        a,b,n=field['source'],field['destination'],field['bytes'];out[b:b+n]=t[a:a+n]
    return {'profile_pointer':resolved['pointer'],'profile_hex':p.hex(),'record_hex':out.hex(),
        'job':job,'identity':word(out,2),'state':out[15],'category':out[0xA4],
        'coordinates':list(out[0x9B:0x9D]),'hp_max':word(out,20),'mp_max':word(out,26)}


def native_fixture():
    raw=EVIDENCE.read_bytes()
    if digest(raw)!=EVIDENCE_SHA256:raise ValueError('frozen enemy records evidence differs')
    data=json.loads(raw)
    counter=COUNTER_EVIDENCE.read_bytes()
    if digest(counter)!=COUNTER_SHA256:raise ValueError('frozen enemy record counter evidence differs')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,'scene_inputs':deepcopy(data['scene_inputs']),
        'counter_report_sha256':COUNTER_SHA256,'declared_counter_diagnostic':json.loads(counter),
        'declared_template_diagnostic':deepcopy(data['declared_template_diagnostic']),
        'cases':[{k:deepcopy(c[k]) for k in ('name','ready','scene_unit_record_prepared','scene_unit_record','stop_reason')}
            for c in data['cases']],**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True)
    args=p.parse_args()
    for path,data in ((args.rules_out,source_catalog()),(args.fixture_out,native_fixture())):
        (ROOT/path).write_text(report_text(data),encoding='utf-8',newline='\n')
