"""Independent source/parent/stack/probe verifier for the paused original return."""
import hashlib,json,struct
from copy import deepcopy
from tools.school_world_tail_emulation import ROOT,UNITCTRL,STACK,RETURN,PARENT,PARENT_SHA,PROBES,ROOTS
from tools.school_world_tail import source_contract,project,idle_effects,EFFECT_STRIDE,SECONDARY_STRIDE
from tools.school_world_command_verification import verify_case as verify_parent_case
from tools.school_world_lists_verification import REPORT as LIST_PARENT,REPORT_SHA as LIST_SHA

REPORT=ROOT/'analysis/school-world-tail-native-v1-20261014.json'
REPORT_SHA='e2ea4525d3530b00b3a36af387f06dc0af414ba494f008ee1efd0cf10206fd7f'


def pinned(path,sha):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('tail pinned report identity')
    return json.loads(raw)


def effect_calls(inputs,actual):
    return [{'index':i,'receiver':inputs['effect_receivers'][i],'anim':UNITCTRL+0x10C680+i*EFFECT_STRIDE+0x48,
      'return_va':'0x4668dd','sp':STACK+0xFF00-(192 if actual else 100)} for i in range(10)]


def verify_case(case):
    parent=next((r for r in pinned(PARENT,PARENT_SHA)['cases'] if r['name']==case['name']),None)
    if parent is None or case['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('tail checkpoint provenance')
    verify_parent_case(parent)
    previous=next(r for r in pinned(LIST_PARENT,LIST_SHA)['cases'] if r['name']==case['name'])
    a=case['actual_tail'];inputs=a['inputs'];before=a['before']
    if a['after']!=project(inputs,before):raise ValueError('tail full independent source projection')
    pointers=[UNITCTRL+0x3098C,UNITCTRL+0x2F150,UNITCTRL+0x115CB8,UNITCTRL+0x10C680,
       UNITCTRL+0x116254,UNITCTRL+0x108B30,UNITCTRL+0x1798,UNITCTRL+0x2A80,UNITCTRL+0x117C3C,0x7F4491]
    if [r['pointer'] for r in before]!=pointers:raise ValueError('tail exact owned pointer identity')
    queue_parent=parent['actual_suffix']['after'][0]
    if before[0]!=parent['actual_suffix']['after'][3] or before[1]['hex']!=previous['actual_list_suffix']['after'][0]['hex'] or any(before[6][k]!=queue_parent[k] for k in ('pointer','bytes','hex')):raise ValueError('tail exact full parent-owned bytes')
    if len(inputs['effect_receivers'])!=10 or inputs['entry_receiver']!=UNITCTRL-400:raise ValueError('tail source controller identities')
    effects=bytes.fromhex(before[3]['hex'])
    if inputs['effect_receivers']!=[struct.unpack_from('<I',effects,i*EFFECT_STRIDE+0x44)[0] for i in range(10)]:raise ValueError('tail effect source receivers')
    if any(r!=0x11000000 for r in inputs['effect_receivers']):raise ValueError('tail actual original animation binding')
    sp=STACK+0xFF00-92
    calls=[{'va':hex(va),'receiver':UNITCTRL,'return_va':hex(ret),'sp':sp} for va,ret in ROOTS.items()]
    calls += [{'va':'0x456b20','receiver':inputs['entry_receiver'],'return_va':'0x48ce8b','sp':sp-88},
      {'va':'0x48d5d0','receiver':UNITCTRL,'return_va':'0x48ce99','sp':sp-88},
      {'va':'0x496450','receiver':UNITCTRL,'return_va':'0x48d5f5','sp':sp-192},
      {'va':'0x427de0','receiver':UNITCTRL+0x2A80,'return_va':'0x48d618','sp':sp-192}]
    if a['calls']!=calls or a['effect_calls']!=effect_calls(inputs,True) or a['effect_returns']!=[1]*10:raise ValueError('tail exact inner caller/ten effects')
    if a['real_ret']!={'va':'0x46b662','return_va':hex(RETURN),'sp':STACK+0xFF00,'eax':0,'original_outer_caller':False}:raise ValueError('tail real original ret/declared outer driver')
    if a['driver_return']!={'va':hex(RETURN),'sp':STACK+0xFF00+4,'ebp':STACK+0xFF00-4,'expected_caller_ebp':STACK+0xFF00-4,'eax':0,'declared_audit_sentinel':True}:raise ValueError('tail root stack/EBP/result')
    required=set(ROOTS)|{0x40A100,0x456B20,0x48D5D0,0x496450,0x427DE0,0x46B662}
    if not required<=set(a['visited']) or any(va in a['visited'] for va in (0x40A800,0x409FF0,0x427D60,0x496690,0x49CE90,0x4CE8F0)):raise ValueError('tail original executed/skipped bodies')
    if a['first_paused_46B470_body_completed'] is not True:raise ValueError('tail bounded body completion')
    for k in ('enabled_gameplay_tick_completed','original_outer_task_frame_completed','active_animation_commands_executed','nonempty_queue_forwarded','owned_bodies_stubbed'):
        if a.get(k) is not False:raise ValueError('tail scope/authority')
    if a['retained_ranges_unchanged'] is not True or a['retained_bytes']<100000000:raise ValueError('tail complete retained memory')
    probes=case['declared_probes']
    if probes['live_input_captured'] is not False or [r['declared_counter_word'] for r in probes['counter']]!=list(PROBES):raise ValueError('tail finite declared counter input')
    for row in probes['counter']:
        expected_before=deepcopy(a['after']);buf=bytearray.fromhex(expected_before[3]['hex'])
        for i in range(10):struct.pack_into('<H',buf,i*EFFECT_STRIDE+10,row['declared_counter_word'])
        expected_before[3]['hex']=buf.hex()
        expected_after=deepcopy(expected_before);expected_after[3]['hex']=idle_effects(buf).hex()
        if row['before']!=expected_before or row['after']!=expected_after:raise ValueError('tail counter full byte input/projection')
        if row['effect_calls']!=effect_calls(inputs,False) or row['effect_returns']!=[1]*10:raise ValueError('tail declared ten original effect calls')
        if row['retained_ranges_unchanged'] is not True or row['retained_bytes']<100000000:raise ValueError('tail probe retained memory')
    for row in [r['restoration'] for r in probes['counter']]+[probes['final_restoration']]:
        if row['register_count']!=50 or row['complete_owned_input_restored'] is not True:raise ValueError('tail complete probe restoration')
        for k in ('cpu','stack'):
            if len(row[k+'_before_sha256'])!=64 or row[k+'_before_sha256']!=row[k+'_after_sha256']:raise ValueError('tail full CPU/stack restore equality')
    return True
