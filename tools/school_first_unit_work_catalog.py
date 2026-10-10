"""Independent source rules for the first unit work/cache constructor prefix."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE = ROOT/'analysis/school-first-unit-work-v1-20261010.json'
EVIDENCE_SHA256 = 'ccca98bc858881706f3199384c27706300d9a9fa5e07b4a0dba0cef79a65b8a2'


def source_catalog():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('first unit source image differs')
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    md.detail = True
    code = []
    def instruction(va,mnemonic,operands=None):
        ins = next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        if ins.mnemonic != mnemonic or (operands is not None and ins.op_str != operands):
            raise ValueError(f'first unit source instruction differs at {va:#x}')
        code.append({'va':hex(va),'instruction_hex':ins.bytes.hex(),'mnemonic':ins.mnemonic,'operands':ins.op_str})
        return ins
    def constant(va,mnemonic,index=-1):
        op = instruction(va,mnemonic).operands[index]
        if op.type==X86_OP_IMM:
            return op.imm
        if op.type==X86_OP_MEM:
            return op.mem.disp
        raise ValueError('first unit constant operand differs')
    work_bytes = constant(0x468109,'imul')
    work_offset = constant(0x468112,'lea')
    record_stride = constant(0x468186,'imul')
    record_offset = constant(0x46818F,'lea')
    record_pointer_offset = constant(0x468199,'mov',0)
    work_stores = []
    for va in (0x468160,0x468173,0x46817A,0x4681BA,0x4681C4,0x4681DF,0x4682B0):
        ins = instruction(va,'mov')
        dest,value = ins.operands
        if dest.type != X86_OP_MEM or value.type != X86_OP_IMM:
            raise ValueError('first unit immediate work store differs')
        work_stores.append({'offset':dest.mem.disp,'bytes':dest.size,'value':value.imm & ((1<<(dest.size*8))-1)})
    record_stores = []
    for va in (0x4681EF,0x468201,0x468213,0x468225,0x468237,0x47500E,0x47501E):
        ins = instruction(va,'mov')
        dest,value = ins.operands
        if dest.type != X86_OP_MEM or value.type != X86_OP_IMM:
            raise ValueError('first unit immediate record store differs')
        record_stores.append({'offset':dest.mem.disp,'bytes':dest.size,'value':value.imm & ((1<<(dest.size*8))-1)})
    classification_offset = constant(0x474FF3,'mov')
    classification_limit = constant(0x474FF9,'cmp')
    status_work_offset = constant(0x474FD0,'add')
    status_template_offset = constant(0x475067,'add')
    status_template_pointer = constant(0x47505E,'add')
    status_template_count = constant(0x47506A,'mov')*4
    status_for_inactive = constant(0x46826B,'push')
    status_for_character = constant(0x46828D,'push')
    status_for_other = constant(0x46829F,'push')
    mode_field = constant(0x46C0DB,'mov',0)
    mode_value = constant(0x4681CE,'push')
    source_tables = {'job':constant(0x466D3E,'mov'),'job_stride':8,
        'palette':constant(0x4670F3,'movsx'),'palette_stride':constant(0x4670ED,'imul'),
        'animation':constant(0x464DAB,'mov'),'position':constant(0x464DBF,'mov')}
    controller_stores = []
    for start,end,base_offset in ((0x409900,0x4099E8,0),(0x41EAD0,0x41EB25,0x18),(0x464C60,0x464CC0,0)):
        for ins in md.disasm(image[start-BASE:end-BASE],start):
            if ins.mnemonic!='mov' or len(ins.operands)!=2:
                continue
            dest,value = ins.operands
            if dest.type==X86_OP_MEM and value.type==X86_OP_IMM and 0 <= dest.mem.disp < 84:
                # Resolve register identity symbolically by excluding EBP;
                # these constructors only use object registers for positive stores.
                if md.reg_name(dest.mem.base)=='ebp' or dest.mem.segment:
                    continue
                controller_stores.append({'va':hex(ins.address),'offset':base_offset+dest.mem.disp,
                    'bytes':dest.size,'value':value.imm & ((1<<(dest.size*8))-1)})
                instruction(ins.address,'mov',ins.op_str)
    jobs = []
    animation_delta = constant(0x466CEB,'add')
    for job in (6,7,10):
        table = source_tables['job']+job*8
        filename,group,mode,variant = struct.unpack_from('<IhBb',image,table-BASE)
        path = image[filename-BASE:filename-BASE+260].split(b'\0',1)[0].decode('ascii')
        if path not in ('data\\DxAnim\\c1a.bin','data\\DxAnim\\e0a.bin','data\\DxAnim\\d1a.bin'):
            raise ValueError('supported first unit art filename differs')
        animation = group+animation_delta
        palettes = list(struct.unpack_from('<35b',image,source_tables['palette']-BASE+job*40))
        file = ROOT/'CROSS HERMIT/CROSS HERMIT'/path.replace('\\','/')
        raw = file.read_bytes()
        jobs.append({'job':job,'table_va':hex(table),'record_hex':image[table-BASE:table-BASE+8].hex(),
            'filename_pointer':filename,'relative_path':path,'group':group,'mode':mode,'variant':variant,
            'palettes_by_character':palettes,'animation_id':animation,
            'animation_table_pointer':struct.unpack_from('<I',image,source_tables['animation']-BASE+animation*4)[0],
            'position_table_pointer':struct.unpack_from('<I',image,source_tables['position']-BASE+animation*4)[0],
            'resource_identity':{'path':file.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                'header_hex':raw[:36].hex(),'loaded_by_native_stage':False}})
    for va,mnemonic,operands in ((0x4681D7,'call','0x46c040'),(0x468245,'call','0x474fb0'),
            (0x468251,'call','0x4750b0'),(0x4682C4,'call','0x467020'),
            (0x466EB8,'call','0x466da0'),(0x466ECE,'call','0x466b40'),
            (0x466EE5,'call','0x466c80'),(0x466BCE,'call','0x464c60'),
            (0x466CF9,'call','0x464d70'),(0x466D49,'call','0x464eb0'),
            (0x464F1A,'call','0x4500b0')):
        instruction(va,mnemonic,operands)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'work_bytes':work_bytes,'work_offset':work_offset,
        'record_stride':record_stride,'record_offset':record_offset,'record_pointer_offset':record_pointer_offset,
        'work_stores':work_stores,'record_stores':record_stores,'mode_field':mode_field,'mode_value':mode_value,
        'classification_offset':classification_offset,'classification_limit':classification_limit,
        'status_work_offset':status_work_offset,'status_template_offset':status_template_offset,
        'status_template_pointer':status_template_pointer,'status_template_hex':image[status_template_pointer-BASE:status_template_pointer-BASE+status_template_count].hex(),
        'status_by_record':{'inactive':status_for_inactive,'character':status_for_character,'other':status_for_other},
        'controller_bytes':constant(0x466BB1,'push'),'controller_stores':controller_stores,
        'cache_offset':constant(0x466B97,'lea'),'cache_count':constant(0x466B84,'cmp'),'cache_stride':8,
        'counter_offset':constant(0x466D07,'mov'),'source_tables':source_tables,'jobs':jobs,'code_inputs':code,
        'scope':'Supported friendly school records/jobs; isolated controller allocation starts zero. Constructor tail, art loading/GPU, enemy work and placement are not asserted.',**AUTHORITY}


def expected_first_work(record_hex,index,prior_counter,renderer,controller_pointer,rules=None):
    r = source_catalog() if rules is None else rules
    try:
        record = bytearray.fromhex(record_hex)
    except (TypeError,ValueError) as error:
        raise ValueError('first unit record encoding') from error
    if len(record)!=176 or type(index) is not int or not 0 <= index < 250 \
        or type(prior_counter) is not int or not 0 <= prior_counter < 256:
        raise ValueError('first unit index/counter/record size')
    identity,job = struct.unpack_from('<H',record,2)[0],struct.unpack_from('<H',record,0xC)[0]
    if not 1 <= identity <= 34 or record[r['classification_offset']] >= r['classification_limit']:
        raise ValueError('unsupported first unit ownership/identity')
    jobs = [j for j in r['jobs'] if j['job']==job]
    if len(jobs)!=1:
        raise ValueError('unsupported first unit job')
    j = jobs[0]
    variant = j['palettes_by_character'][identity]+1 if j['mode']==2 and j['palettes_by_character'][identity] else 0
    if variant < 0 or variant > 255:
        raise ValueError('unsupported first unit palette')
    work = bytearray(r['work_bytes'])
    for store in r['work_stores']:
        work[store['offset']:store['offset']+store['bytes']] = store['value'].to_bytes(store['bytes'],'little')
    struct.pack_into('<H',work,2,index)
    # Source receiver is an input, not inferred from the evidence fixture.
    record_pointer = 0xE000000+0x190+r['record_offset']+index*r['record_stride']
    struct.pack_into('<I',work,r['record_pointer_offset'],record_pointer)
    work[r['mode_field']] = r['mode_value']
    at = r['status_work_offset']+r['status_template_offset']
    template = bytes.fromhex(r['status_template_hex'])
    work[at:at+len(template)] = template
    work[r['status_work_offset']] = r['status_by_record']['character'] if record[0xF]==1 else r['status_by_record']['inactive']
    for store in r['record_stores']:
        record[store['offset']:store['offset']+store['bytes']] = store['value'].to_bytes(store['bytes'],'little')
    controller = bytearray(r['controller_bytes'])
    for store in r['controller_stores']:
        controller[store['offset']:store['offset']+store['bytes']] = store['value'].to_bytes(store['bytes'],'little')
    struct.pack_into('<I',controller,0x28,prior_counter)
    struct.pack_into('<I',controller,0x44,renderer)
    struct.pack_into('<H',controller,0x48,j['animation_id'])
    struct.pack_into('<I',controller,0x4C,j['animation_table_pointer'])
    struct.pack_into('<I',controller,0x50,j['position_table_pointer'])
    cache = bytearray(r['cache_count']*r['cache_stride'])
    struct.pack_into('<BBHI',cache,0,1,variant,j['group'],controller_pointer)
    return {'work_hex':work.hex(),'record_hex':record.hex(),'controller_hex':controller.hex(),
        'cache_hex':cache.hex(),'counter':prior_counter+1,
        'resource_args':[j['filename_pointer'],variant,int(variant!=0),0],
        'relative_path':j['relative_path']}


def native_fixture():
    raw = EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:
        raise ValueError('frozen first unit evidence differs')
    data = json.loads(raw)
    fields = ('name','ready','first_unit_work_prefix_initialized','first_unit_work','stop_reason',
              'persistent_ranges_unchanged','battle_world_constructed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
            'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in data['cases']],**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rules-out',required=True)
    p.add_argument('--fixture-out',required=True)
    args = p.parse_args()
    for name,data in [(args.rules_out,source_catalog()),(args.fixture_out,native_fixture())]:
        (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')
