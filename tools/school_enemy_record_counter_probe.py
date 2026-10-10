"""Declared profile mutations on native record functions, separate from school."""
import argparse
from copy import deepcopy
import hashlib
import json
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX
from tools.school_enemy_records_emulation import SchoolEnemyRecordsEmulator,ROOT,UNITCTRL,RECORD_OFFSET,CHARACTER_DEFINITION_BASE,CHAR_BASE,STACK,RETURN,AUTHORITY,report_text
from tools.school_enemy_records_catalog import EVIDENCE,EVIDENCE_SHA256


def report():
    raw=EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('declared counter input evidence identity')
    first=json.loads(raw)['declared_template_diagnostic']['records'][0]
    original=bytes.fromhex(first['character_input_hex']);records=[]
    for name in ('attributes_zero','attributes_255','ranged_job2','persistent_attributes_255'):
        e=SchoolEnemyRecordsEmulator();character=bytearray(original)
        mutation_pointer=(CHAR_BASE if name=='persistent_attributes_255' else CHARACTER_DEFINITION_BASE)+5*0x4A0
        if name!='ranged_job2':
            for i in range(7):character[12+8*i]=0 if name=='attributes_zero' else 255
        else:character[6:8]=(2).to_bytes(2,'little')
        e.uc.mem_write(mutation_pointer,bytes(character))
        e.enemy_mode='declared_template_driver';e.enemy_ordinal=0;e.enemy_loading=True
        sp=STACK+0xFF00;e.write(sp,RETURN);e.write(sp+4,e.enemy_inputs['pointer']);e.write(sp+8,UNITCTRL+RECORD_OFFSET+249*176)
        e.uc.reg_write(UC_X86_REG_ESP,sp);e.uc.reg_write(UC_X86_REG_ECX,0);e.clear_trace('tactical_startup')
        e.uc.emu_start(0x4DA450,RETURN,timeout=1_000_000,count=100_000)
        if e.uc.reg_read(UC_X86_REG_EIP)!=RETURN or e.uc.reg_read(UC_X86_REG_ESP)!=sp+4:
            raise RuntimeError('declared counter native cdecl return')
        n=e.finish_record();n['name']=name;n['coverage']=e.coverage()
        n['declared_mutation_pointer']=mutation_pointer;n['declared_mutation_hex']=character.hex()
        n['declared_mutation_retained']=bytes(e.uc.mem_read(mutation_pointer,len(character)))==bytes(character)
        records.append(deepcopy(n))
    return {'schema_version':1,'evidence_kind':'declared_scene5_role5_record_attribute_and_job_counterfactuals',
        'input_source_report_sha256':EVIDENCE_SHA256,'declared_inputs':'Original frozen EXE role5 definition; mutate definition attributes to0/255 or job to2, separately mutate persistent attributes to255. Direct4DA450 calls in zero task memory; no school/scene loop/work constructor.',
        'records':records,'school_enemy_loop_executed':False,'unit_work_constructors_executed':False,**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
