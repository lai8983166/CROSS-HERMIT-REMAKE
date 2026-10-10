"""Declared scene-prefix counterfactuals; no school loop or archive loader."""
import argparse
from copy import deepcopy
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_scene_unit_work_emulation import (
    SchoolSceneUnitWorkEmulator,ROOT,UNITCTRL,WORK_OFFSET,WORK_BYTES,CACHE_OFFSET,CACHE_COUNT,
    COUNTER_OFFSET,SCENE_CONTROLLER,STACK,RETURN,TASK,report_text,AUTHORITY,SOURCE_SHA256)


def report():
    e=SchoolSceneUnitWorkEmulator();records=e.declared_templates()['records'];outputs=[]
    original_templates=deepcopy(e.enemy_inputs['templates'])
    for name,ordinal in [('npc_template_overlay',0),('friendly_category',0),
        ('special_relation1',2),('special_relation2',2),('special_relation3',2),('special_own_category',2)]:
        n=records[ordinal];template=bytearray.fromhex(original_templates[ordinal]);record=bytearray.fromhex(n['record_hex'])
        relation=bytearray(256);selector=0;mutations=[]
        if name=='npc_template_overlay':
            struct.pack_into('<H',template,0x10,0x1234);template[0x14:0x54]=bytes(range(1,65))
            mutations.append('original scene-template status64 bytes=1..64 and record overlay word=0x1234; pre-prefix numeric record retained')
        elif name=='friendly_category':record[0xA4]=3;mutations.append('declared pre-prefix record category7 to3')
        elif name=='special_own_category':selector=7;mutations.append('declared selector7 equals record category7')
        else:relation[7]=int(name[-1]);mutations.append('declared relation row0/category7='+name[-1])
        e.enemy_inputs['templates']=deepcopy(original_templates);e.enemy_inputs['templates'][ordinal]=template.hex()
        e.uc.mem_write(e.enemy_inputs['pointer']+ordinal*84,bytes(template))
        e.uc.mem_write(n['record_pointer'],bytes(record));e.uc.mem_write(UNITCTRL+WORK_OFFSET+n['index']*WORK_BYTES,bytes(WORK_BYTES))
        e.uc.mem_write(UNITCTRL+CACHE_OFFSET,bytes(CACHE_COUNT*8));e.write(UNITCTRL+COUNTER_OFFSET,110)
        e.uc.mem_write(SCENE_CONTROLLER,bytes(84));e.write(0x7A49FC,TASK);e.write(0x7F4488,5,'h')
        e.write(UNITCTRL+0x2EF44,selector,'B');e.uc.mem_write(UNITCTRL+0x115AAC,bytes(relation))
        e.begin_scene_work(ordinal,'declared_isolated_scene_unit_prefix')
        sp=STACK+0xFF00;e.write(sp,RETURN);e.write(sp+4,n['index'])
        e.uc.reg_write(UC_X86_REG_ECX,UNITCTRL);e.uc.reg_write(UC_X86_REG_ESP,sp);e.uc.reg_write(UC_X86_REG_EIP,0x4680B0)
        output=e.run_scene_prefix();output.update({'name':name,'declared_mutations':mutations});outputs.append(output)
        e.uc.mem_write(e.enemy_inputs['pointer']+ordinal*84,bytes.fromhex(original_templates[ordinal]))
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'units':outputs,
        'evidence_kind':'declared_scene_work_prefix_counterfactual_driver',
        'declared_inputs':'Original numeric records derived on CPU, then explicit isolated record/template/selector/relation mutations before prefix. Empty cache/counter110/renderer/zero allocation declared.',
        'school_enemy_loop_executed':False,'constructor_tails_executed':False,'archives_loaded':False,**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
