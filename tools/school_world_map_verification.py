"""Independent full-region checks for original current-school map suffix."""
import struct
from copy import deepcopy
from tools.school_world_map import source_contract,project_map_frame,clock_step,pointer_outputs,MAP_STATE_BASE,MAP_STATE_BYTES
from tools.school_world_map_emulation import CLOCK_CASES,MOUSE_CASES
from tools.school_deployment_tail_emulation import UNITCTRL,STACK,CHECKPOINTS
from tools.school_entry_control_emulation import MAPCTRL


def retained(row):
    if row.get('retained_ranges_unchanged') is not True or row['retained_bytes']<100000000:raise ValueError('world map retained memory')


def restored(row):
    r=row['restoration']
    if r['register_count']!=50 or r['complete_owned_input_restored'] is not True:raise ValueError('world map restored context scope')
    for name in ('cpu','stack'):
        if len(r[name+'_before_sha256'])!=64 or r[name+'_before_sha256']!=r[name+'_after_sha256']:raise ValueError('world map restored context/stack')


def verify_case(case,parent):
    if case.get('checkpoint_sha256')!=dict(CHECKPOINTS).get(case.get('name')) or case.get('complete_parent_equality') is not True:
        raise ValueError('world map actual school provenance')
    a=case['actual_map_suffix'];before=a['before'];after=a['after'];p=parent['actual_world_prefix']
    if before[0]['pointer']!=MAPCTRL+0xA0 or before[1]['pointer']!=MAPCTRL+MAP_STATE_BASE or before[1]['bytes']!=MAP_STATE_BYTES or before[5]['pointer']!=0x7A2960:
        raise ValueError('world map complete owned identities')
    if after!=project_map_frame(before,a['mouse']) or a['clock_before_hex']!=a['clock_after_hex'] or len(bytes.fromhex(a['clock_before_hex']))!=24:
        raise ValueError('world map full original frame projection/clock retention')
    if a['mode_before']!=p['after'] or a['mode_after']!=a['mode_before']:raise ValueError('world map exact captured parent mode')
    sp=STACK+0xFF00-92
    calls=[{'va':'0x493630','receiver':UNITCTRL,'return_va':'0x46b4d0','sp':sp},
           {'va':'0x467b60','receiver':UNITCTRL,'return_va':'0x46b4d8','sp':sp},
           {'va':'0x46e9c0','receiver':UNITCTRL,'return_va':'0x46b4e0','sp':sp},
           {'va':'0x43b350','receiver':MAPCTRL,'return_va':'0x46e9eb','sp':sp-88},
           {'va':'0x56cec0','return_va':'0x43d10c','args':[before[4]['pointer'],0,6144],'original_body_executed':True},
           {'va':'0x481610','receiver':UNITCTRL,'return_va':'0x46e9f3','sp':sp-88}]
    if a['calls']!=calls or a['pending']!={'va':'0x49b180','receiver':UNITCTRL,'return_va':'0x46b4e8','sp':sp,'first_instruction_executed':False}:
        raise ValueError('world map complete natural stack/calls')
    if a.get('original_memset_body_executed') is not True:raise ValueError('world map real memset scope')
    for field in ('full_world_tick_executed','AI_or_waves_executed','live_input_captured'):
        if a.get(field) is not False:raise ValueError('world map unclaimed scope')
    retained(a)
    probes=case['declared_probes']
    if probes['live_input_captured'] is not False or [r['declared_input'] for r in probes['clock']]!=[list(p) for p in CLOCK_CASES] or [r['declared_mouse'] for r in probes['mouse']]!=[list(p) for p in MOUSE_CASES]:
        raise ValueError('world map complete declared probe matrix')
    for row in probes['clock']:
        opening,event,remaining,elapsed,limit=row['declared_input'];expected=clock_step(opening,event,remaining,elapsed,limit)
        b=deepcopy(row['before']);data=bytearray.fromhex(b[0]['hex']);struct.pack_into('<3i',data,0,remaining,elapsed,limit)
        if data.hex()!=b[0]['hex'] or b[1]['hex']!=bytes([opening]).hex() or b[2]['hex']!=bytes([event]).hex():raise ValueError('declared clock input binding')
        struct.pack_into('<3i',data,0,*[expected[k] for k in ('remaining','elapsed','limit')]);b[0]['hex']=data.hex()
        if row['after']!=b or row['return_eax']!=expected['return_eax'] or bool(row['calls'])!=expected['increment_called']:raise ValueError('world exact complete clock probe')
        if expected['increment_called']:
            if len(row['calls'])!=1 or {k:row['calls'][0][k] for k in ('va','return_va','args')}!={'va':'0x415040','return_va':'0x467bd2','args':[1]}:raise ValueError('original clock increment call')
        retained(row);restored(row)
    for row in probes['mouse']:
        b=deepcopy(row['before']);x,y=row['declared_mouse']
        if b[0]['hex']!=struct.pack('<2i',x,y).hex():raise ValueError('declared mouse binding')
        data=bytearray.fromhex(b[1]['hex']);camera=struct.unpack_from('<2h',data,0);expected=pointer_outputs((x,y),camera)
        struct.pack_into('<4h',data,4,*(expected['tile']+expected['pixel']));b[1]['hex']=data.hex()
        if row['outputs']!=expected or row['after']!=b:raise ValueError('world complete source pointer probe')
        retained(row);restored(row)
    return True
