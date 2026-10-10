"""Declared first-scene NPC loader probes at palette boundaries; no tail/loop."""
import argparse
from tools.school_scene_unit_constructor_emulation import (
    SchoolSceneUnitConstructorEmulator,ROOT,report_text,AUTHORITY,SOURCE_SHA256,
    UNITCTRL,TASK,SCENE_CONTROLLER,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,STACK,RETURN,
    UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EIP)


def report():
    e=SchoolSceneUnitConstructorEmulator()
    first=e.declared_templates()['records'][0]
    e.write(0x7F4488,5,'h');e.write(0x7A49FC,TASK);e.bind_resources()
    checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()]
    cpu=e.uc.context_save();outputs=[];student_rules=e.current_rules
    for variant in (1,40):
        for at,raw in checkpoint:e.uc.mem_write(at,raw)
        e.uc.context_restore(cpu);e.scene_complete_loading=False
        e.uc.mem_write(UNITCTRL+CACHE_OFFSET,bytes(CACHE_COUNT*8))
        e.write(UNITCTRL+COUNTER_OFFSET,110);e.uc.mem_write(SCENE_CONTROLLER,bytes(84))
        e.uc.mem_write(first['record_pointer'],bytes.fromhex(first['record_hex']))
        e.begin_scene_work(0,'declared_isolated_scene_unit_prefix')
        sp=STACK+0xFF00;e.write(sp,RETURN);e.write(sp+4,249)
        e.uc.reg_write(UC_X86_REG_ECX,UNITCTRL);e.uc.reg_write(UC_X86_REG_ESP,sp)
        e.uc.reg_write(UC_X86_REG_EIP,0x4680B0)
        prefix=e.run_scene_prefix()
        # The original role/job selects5. This isolated driver changes only the
        # suspended loader argument, explicitly testing loader palette bounds.
        pending_sp=e.uc.reg_read(UC_X86_REG_ESP);e.write(pending_sp+8,variant)
        animation=e.run_scene_animation(variant)
        if e.current_rules is not student_rules:raise RuntimeError('scene loader replaced upstream student rules')
        outputs.append({'variant':variant,'prefix':prefix,'animation':animation,
            'declared_argument_write':{'pointer':pending_sp+8,'before':5,'after':variant},
            'stop_reason':e.stop_reason,'constructor_tail_executed':False})
        print(f'Declared scene loader palette{variant}:244 textures',flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'declared_first_scene_npc_loader_palette_boundary_driver',
        'declared_inputs':{'empty_cache':True,'counter':110,'renderer':TASK,'zero_controller_allocation':True,
            'classification_selector':0,'relation_hex':bytes(256).hex(),'loader_variants':[1,40],
            'source_selected_variant':5,'gpu_creation_and_upload_return':0},
        'school_enemy_loop_executed':False,'scene_placement_executed':False,'scene_vm_executed':False,
        'probes':outputs,**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True)
    a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
