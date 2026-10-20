"""Independent source path, ABI, native writes and owned class lifetime checks."""
import argparse
import copy
import json
from pathlib import Path
from functools import lru_cache
from tools.school_window_class import *
from tools.school_window_module_verification import verify_case as verify_module_case,maps as module_maps
from tools.school_window_module_validation import digest
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_verification import verify_buffer
from tools.school_window_class_platform import (SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine,
    verify_registration,verify_unregistration)


@lru_cache(maxsize=1)
def instructions():
    raw=SOURCE.read_bytes();validate_source(raw)
    return {i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}


def source_runs(phase):
    at=ENTRY if phase=='registered' else STOPS['registered'];rows=[];returns=[];code=instructions()
    while at!=STOPS[phase]:
        if len(rows)>100:raise ValueError('class finite original caller path')
        i=code[at];nxt=at+i.size;rows.append(dict(va=at,count=1))
        if i.mnemonic=='call' and i.op_str.startswith('0x'):returns.append(nxt);nxt=int(i.op_str,16)
        elif i.mnemonic=='ret':nxt=returns.pop()
        elif i.mnemonic=='jne':
            if at!=0x450491:raise ValueError('class unknown original branch')
            nxt=int(i.op_str,16) # Proved nonzero actual ATOM, not an assumed API success.
        at=nxt
    if returns:raise ValueError('class original stack-check return')
    return rows


def maps():
    result=module_maps(True);raw=SOURCE.read_bytes();target=dword(raw,SLOT-BASE)
    result.setdefault(target&~4095,bytearray(4096))[target%4096]=0xC3
    return result


def verify_maps(rows,expected):
    if [r['pointer'] for r in rows]!=sorted(expected):raise ValueError('class exact import shadow list')
    for r in rows:verify_buffer({k:v for k,v in r.items() if k!='pointer'},expected[r['pointer']])


def verify_case(c,through='create_ready'):
    original_digest=digest(c);prefix=verify_module_case(c);old=c['class_ready'];raw=SOURCE.read_bytes()
    module_handle=c['hello']['resource_module']['pointer'];call=c['registered']['platform_calls']
    if len(call)!=1:raise ValueError('class exactly one original registration')
    call=call[0];guest=unpack(old['state']['class_structure']);result=call['result'];registration=verify_registration(result,guest)
    request=dict(class_hex=guest.hex(),class_name_hex=NAME_BYTES.hex())
    expected=dict(name='RegisterClassExA',op='register_class',slot=hex(SLOT),va=hex(dword(raw,SLOT-BASE)),return_va='0x450483',sp=geometry.FRAME_SP-8,args=[geometry.CLASS_AT],
        request=request,result=result,observed_EAX=result['eax_bits_observed'],live_host_observed=True)
    if call!=expected or type(result['eax_bits_observed']) is not int or not 0<=result['eax_bits_observed']<=0xFFFFFFFF:raise ValueError('class complete original API ABI/result')
    a=c['registered']['import_admission']
    expected=dict(slots=[hex(SLOT)],before_cpu=old['cpu'],after_cpu=old['cpu'],retained_owner_sha256=old['state']['guarded_owner']['sha256'],retained_stack_sha256=old['state']['stack']['sha256'],
        retained_image_sha256=old['state']['image_sha256'],foreign_before=old['state']['foreign_maps'],foreign_after=c['registered']['state']['foreign_maps'],native_game_call=False)
    if a!=expected:raise ValueError('class admission changed original pending state')
    verify_maps(a['foreign_before'],module_maps(True));verify_maps(a['foreign_after'],maps())
    stack=bytearray(unpack(old['state']['stack']));previous=old
    for phase in STOPS:
        n=c[phase];state=n['state'];eax=result['eax_bits_observed'];cpu=dict(old['cpu'])
        cpu.update(EIP=STOPS[phase],ESP=geometry.FRAME_SP if phase=='registered' else geometry.FRAME_SP-48,EAX=eax if phase=='registered' else geometry.STYLE)
        if phase=='create_ready':cpu.update(ECX=768,EDX=1024,EFLAGS=6)
        if n['phase']!=phase or n['before_cpu']!=previous['cpu'] or n['cpu']!=cpu or n['instruction_runs']!=source_runs(phase):raise ValueError('class exact original path/CPU continuity')
        if n['entries']:raise ValueError('class no synthetic game entry')
        pending=dict(va=hex(STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='registered':pending['stack_top_dword']=parent.BP
        else:pending.update(import_slot='0x59240c',import_target=dword(raw,0x59240C-BASE),stack_args=creation_args(module_handle),call_instruction_executed=False)
        if n['pending']!=pending:raise ValueError('class exact pending original instruction/creation arguments')
        if phase=='registered':
            writes=[dict(pc=ENTRY,pointer=geometry.FRAME_SP-8,bytes=4,value=STOPS['registered'])];returns=[];calls=[call]
        else:
            writes=[dict(pc=0x450485,pointer=geometry.FRAME_SP-4,bytes=4,value=0x45048A)]
            pushes=[0x4504A2,0x4504A8,0x4504A9,0x4504AB,0x4504B3,0x4504BA,0x4504BB,0x4504BD,0x4504C2,0x4504C3,0x4504C8,0x4504CD]
            for i,(pc,value) in enumerate(zip(pushes,reversed(creation_args(module_handle)))):
                writes.append(dict(pc=pc,pointer=geometry.FRAME_SP-(i+1)*4,bytes=4,value=value))
            returns=[dict(va='0x56ce82',return_va='0x45048a',sp=geometry.FRAME_SP-4,eax=eax)];calls=[]
            if n['import_admission'] is not None:raise ValueError('class no second admission')
        if n['native_writes']!=writes or n['returns']!=returns or n['platform_calls']!=calls:raise ValueError('class exact source native writes/returns/calls')
        for w in writes:store(stack,w['pointer']-parent.STACK,w['value'])
        verify_buffer(state['stack'],stack);verify_buffer(state['class_structure'],guest)
        if set(state)!={'owner','guarded_owner','stack','class_structure','image_sha256','null_page','SEH','foreign_maps'}:raise ValueError('class full state schema')
        for key in ('owner','guarded_owner','image_sha256','null_page','SEH'):
            if state[key]!=old['state'][key]:raise ValueError('class preserved full memory/guards/image/SEH')
        verify_maps(state['foreign_maps'],maps())
        for flag,value in dict(class_registration_executed=True,callback_executed=False,window_created=False,retained_VM_advanced=False).items():
            if n[flag] is not value:raise ValueError('class honest registration/callback/window scope')
        previous=n
        if phase==through:break
    if digest(c)!=original_digest:raise ValueError('class verifier modified raw evidence')
    return dict(prefix=prefix,registration=registration,pending=hex(STOPS[through]),raw_modified=False)


def verify_report(report,through='create_ready'):
    if report['source_contract']!=source_contract() or [c['fill'] for c in report['cases']]!=[0xA5,0xCC]:raise ValueError('class actual source/two declared cases')
    pin=json.loads((ROOT/'analysis/school-window-class-platform-v1-20261020.json').read_text(encoding='utf8'))
    build=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))
    if build!=pin['build'] or report['platform_build']!=build:raise ValueError('class actual immutable fresh helper identity')
    proofs=[]
    for c in report['cases']:
        h=copy.deepcopy(c['hello']);h['resource_module']['pointer']=pin['hello']['resource_module']['pointer']
        if h!=pin['hello'] or c['system_modules']!=pin['system_modules']:raise ValueError('class actual resource module/system provenance')
        for r in c['system_modules'].values():
            if machine(r['path'])!=0x14C or sha(Path(r['path']).read_bytes())!=r['sha256']:raise ValueError('class actual x86 system module SHA')
        proofs.append(verify_case(c,through));cleanup=c['platform_cleanup'];reg=c['registered']['platform_calls'][0]['result']
        verify_unregistration(cleanup['unregistration'],reg['atom'])
        expected_cleanup=dict(registration_calls=1,inspection_calls=4,unregistration_calls=1,callback_calls=0,unregistration=cleanup['unregistration'],window_created=False,
            resource_module_refs_released=1,gdi32_module_refs_released=1,icon_load_calls=2,cursor_load_calls=1,stock_brush_calls=1,
            shared_icons_destroyed=0,shared_cursor_destroyed=False,stock_brush_deleted=False,critical_sections_deleted=2,event_handles_closed=1,user32_module_refs_released=1,
            set_rect_calls=1,adjust_window_rect_calls=1,all_owned_resources_released=True)
        if cleanup!=expected_cleanup or c['callback_packets']!=[]:raise ValueError('class complete owned cleanup/dormant transport')
        calls=sum([c[p]['platform_calls'] for p in ('constructor','query','rect','adjust','icons','class_ready','registered')],[])
        trace=[dict(request=dict(id=i+1,op=r.get('op',r['name']),**r['request']),reply=dict(ok=True,id=i+1,result=r['result'])) for i,r in enumerate(calls)]
        trace.append(dict(request=dict(id=len(calls)+1,op='close'),reply=dict(ok=True,id=len(calls)+1,result=cleanup)))
        if c['platform_trace']!=trace:raise ValueError('class exact same-lifetime platform protocol')
    for key,value in dict(actual_genuine_module_declared_before_first_instruction=True,one_continuous_CPU_per_case=True,original_IAT_changed=False,
            game_helpers_stubbed=False,class_registration_executed=True,callback_executed=False,window_created=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False).items():
        if report[key] is not value:raise ValueError('class report authority boundary')
    return dict(cases=2,verified_through=through,pending=hex(STOPS[through]),
        actual_atoms=[p['registration']['atom'] for p in proofs],prefix_validation_substitutions=[len(p['prefix']['substitutions']) for p in proofs],
        native_registration_calls_per_case=1,inspections_per_case=4,unregistrations_per_case=1,
        raw_evidence_modified=False,callback_executed=False,window_created=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--through',choices=list(STOPS),default='create_ready');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')),a.through),indent=2))
