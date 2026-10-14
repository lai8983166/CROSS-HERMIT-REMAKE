"""Independent complete-region and natural-stack verification of world prefix."""
import struct
from copy import deepcopy
from tools.school_world_mode import source_contract,project,first_entry_update
from tools.school_world_mode_emulation import PROBES,cpu_digest
from tools.school_deployment_tail_emulation import UNITCTRL,STACK,CHECKPOINTS
from tools.school_entry_control_emulation import MAPCTRL


def verify_case(case,parent):
    known=dict(CHECKPOINTS)
    if case.get('name') not in known or case.get('checkpoint_sha256')!=known[case['name']] or case.get('complete_parent_equality') is not True:
        raise ValueError('world prefix current-school provenance')
    actual=case['actual_world_prefix'];before=actual['before']
    if before[0]['hex']!=parent['world_admission']['actual_captured_entry']['before_control_hex']:
        raise ValueError('world exact original parent control')
    task_owner=struct.unpack_from('<I',bytes.fromhex(actual['entry_before'][0]['hex']),0x60)[0]
    if [(r['name'],r['pointer'],r['bytes']) for r in before]!=[
        ('control',UNITCTRL+0x108B30,50),('map_flags',MAPCTRL+0x26595,4),('task_flags',task_owner+0x20E8,329)]:
        raise ValueError('world complete owned-region identity')
    expected=project(before,-1,0);control=bytearray.fromhex(expected[0]['hex']);control[26]=4;expected[0]['hex']=control.hex()
    if actual['after']!=expected or actual['entry_after']!=first_entry_update(actual['entry_before']):
        raise ValueError('world complete source-derived after state')
    root_sp=STACK+0xFF00-92
    calls=[{'va':'0x46b4b2','kind':'mode_natural_return','sp':root_sp+4},
        {'va':'0x499da0','receiver':UNITCTRL,'return_va':'0x46b4c8','sp':root_sp},
        {'va':'0x43b400','receiver':MAPCTRL,'return_va':'0x499e3d','args':[304,264]},
        {'va':'0x43b460','receiver':MAPCTRL,'return_va':'0x43b444','args':[-208,-21]},
        {'va':'0x46b4c8','kind':'entry_natural_return','sp':root_sp+4}]
    if actual['calls']!=calls or actual['pending']!={'va':'0x493630','receiver':UNITCTRL,'return_va':'0x46b4d0','sp':root_sp,'first_instruction_executed':False}:
        raise ValueError('world complete natural caller/return stack')
    if (actual['entry_controller_state'],actual['opening_request'],actual['opening_completion'])!=(4,1,0):
        raise ValueError('world first controller completion scope')
    for key in ('mode_request_consumed','full_world_tick_executed','AI_or_waves_executed','mode_store_bodies_stubbed'):
        if actual.get(key) is not False:raise ValueError('world exact unclaimed scope')
    if not actual['retained_ranges_unchanged'] or actual['retained_bytes']<100000000:
        raise ValueError('world retained bytes')
    probes=case['declared_mode_probes']
    if [row['declared_request'] for row in probes]!=[list(p) for p in PROBES]:
        raise ValueError('world complete declared probe matrix')
    c=source_contract()
    for p in probes:
        kind,flag=p['declared_request'];expected_before=deepcopy(before)
        values=bytearray.fromhex(expected_before[0]['hex']);values[11:13]=bytes([kind&255,flag]);expected_before[0]['hex']=values.hex()
        if p['before']!=expected_before or p['after']!=project(p['before'],kind,flag,c):
            raise ValueError('world probe full source comparison')
        if p['return_sp']!=STACK+0xFF04 or not p['captured_parent_restored'] or not p['retained_ranges_unchanged'] or p['retained_bytes']<100000000:
            raise ValueError('world probe caller/restoration/retention')
        r=p['restoration']
        if r['cpu_registers_before']!=r['cpu_registers_after'] or len(r['cpu_registers_before'])!=50 or cpu_digest(r['cpu_registers_before'])!=r['cpu_before_sha256']:
            raise ValueError('world architectural register restoration')
        for field in ('cpu','stack'):
            if len(r[field+'_before_sha256'])!=64 or r[field+'_before_sha256']!=r[field+'_after_sha256']:
                raise ValueError('world complete CPU/stack restoration')
        on=kind==1 and flag!=0
        if kind==-1 or (kind==2 and flag==0):
            if p['calls']:raise ValueError('world idle/empty original calls')
        else:
            child_calls=[{'va':'0x43b250','receiver':MAPCTRL,'return_va':'0x467930' if on else '0x46798e' if kind==1 else '0x4679fd','args':[0 if on else 1]},
                {'va':'0x455160','receiver':actual['entry_before'][0]['pointer'],'return_va':'0x467940' if on else '0x46799e' if kind==1 else '0x467a0d','args':[1 if on else 0]}]
            for va,ret in [(0x4553E0,0x455189),(0x4558A0,0x455195),(0x455D00,0x4551A1)]:
                child_calls.append({'va':hex(va),'receiver':actual['entry_before'][0]['pointer'],'return_va':hex(ret),'args':[1 if on else 0]})
            if p['calls']!=child_calls:raise ValueError('world original mode leaf call provenance')
    return True
