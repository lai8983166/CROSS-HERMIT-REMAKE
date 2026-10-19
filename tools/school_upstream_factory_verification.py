"""Independent actual factory source flow, nested constructor ABI and full buffers."""
import argparse
import hashlib
import json
from functools import lru_cache
from tools.school_upstream_factory import *
from tools.school_upstream_factory_emulation import OWNER,STACK,TOP,RETURN
from tools.school_owner_startup import IMPORTS
from tools.school_owner_startup_verification import verify_native,verify_state
from tools.school_renderer_init_verification import verify_buffer
from tools.school_owner_platform import SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine


@lru_cache(maxsize=1)
def instructions():
    raw=SOURCE.read_bytes()
    return {i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}


@lru_cache(maxsize=4)
def source_runs(kind,phase):
    f=FACTORIES[kind];at=f['entry'] if phase=='allocation' else f['constructor_return']
    stop=CTOR if phase=='allocation' else f['admission'];stack=[];rows=[]
    branches={0x412CB8:False,0x4505BD:False,0x428A8C:True,0x56CE80:False,0x412CE5:True,0x4505EA:True}
    reps={0x412C9B:22,0x45059C:23,0x428A56:18}
    code=instructions()
    while at!=stop:
        if len(rows)>200:raise ValueError('factory bounded source walk')
        i=code[at];nxt=at+i.size;rows.append(dict(va=at,count=reps.get(at,1)))
        if i.mnemonic=='call':
            target=int(i.op_str,16)
            if target!=0x56E810:stack.append(nxt);nxt=target
        elif i.mnemonic=='ret':nxt=stack.pop()
        elif i.mnemonic=='jmp':nxt=int(i.op_str,16)
        elif i.mnemonic.startswith('j'):
            if branches[at]:nxt=int(i.op_str,16)
        at=nxt
    if stack!=[f['constructor_return'] if phase=='allocation' else f['admission_return']]:raise ValueError('factory natural pending call stack')
    return rows


def verify_constructor_trace(row,stop):
    runs=row['instruction_runs'];code=instructions();returns=iter(row['native']['returns']);api={int(r['return_va'],16):r for r in row['platform_calls']}
    entries={int(e['return_va'],16):int(e['va'],16) for e in row['native']['entries'][1:]}
    if sum(r['count'] for r in runs)!=61547:raise ValueError('factory complete native constructor instruction count')
    for n,r in enumerate(runs):
        at=r['va'];i=code.get(at)
        if set(r)!={'va','count'} or i is None or type(r['count']) is not int or r['count']<1:
            raise ValueError('factory constructor bounded original trace')
        if r['count']>1 and not i.mnemonic.startswith('rep '):raise ValueError('factory REP-only instruction run')
        nxt=runs[n+1]['va'] if n+1<len(runs) else stop;fall=at+i.size
        expected={fall}
        if i.mnemonic=='ret':
            ret=next(returns,None)
            if ret is None or int(ret['va'],16)!=at:raise ValueError('factory original return trace order')
            expected={int(ret['return_va'],16)}
        elif i.mnemonic=='call':
            if i.op_str.startswith('0x'):expected={int(i.op_str,16)}
            elif fall in api:expected={fall}
            elif fall in entries:expected={entries[fall]}
            else:raise ValueError('factory original indirect call authority')
        elif i.mnemonic=='jmp':expected={int(i.op_str,16)}
        elif i.mnemonic.startswith('j'):expected.add(int(i.op_str,16))
        if nxt not in expected:raise ValueError('factory original constructor contiguous source control flow')
    if next(returns,None) is not None:raise ValueError('factory no extra native return records')


def verify_constructor_row(c,row):
    f=FACTORIES[c['factory']];sp=TOP-f['constructor_depth'];native=row['native'];calls=row['platform_calls']
    verify_native(native,CTOR,sp,f['constructor_return'],OWNER,[])
    if [int(e['va'],16) for e in native['entries']]!=CTOR_SEQUENCE:raise ValueError('factory all42 original constructor calls')
    memset={0x40BEEB:(0x1AAC,0x7080),0x40C1CF:(0x8C2C,80),0x417E81:(0x92B4,48),0x417EFC:(0x92EC,208),
        0x417F15:(0x93BC,0x150C),0x417F2B:(0x9184,256),0x417F41:(0x9284,40),0x41AB42:(0xA8F8,0x880),0x412F7D:(0xB234,52),0x413008:(0xB214,16)}
    for e in native['entries']:
        va,ret=int(e['va'],16),int(e['return_va'],16)
        if va==0x56CEC0:
            p,n=(0x765728,0x2C000) if ret==0x40B5C7 else (OWNER+memset[ret][0],memset[ret][1])
            if e['args']!=[p,0,n]:raise ValueError('factory full constructor clear ranges')
        elif va==0x56DDA0 and e['args']!=[OWNER+0x8C88,632,2,0x41D2E0,0x41D3C0]:raise ValueError('factory original two-element constructor array')
        elif va==0x4170C0 and e['args']!=[1] or va==0x414F90 and e['args']!=[0]:raise ValueError('factory inherited timer/mode arguments')
    if [r['name'] for r in calls]!=['GetDC','QueryPerformanceCounter','QueryPerformanceFrequency']:raise ValueError('factory exact live DC/timer calls')
    raw=SOURCE.read_bytes()
    for r in calls:
        slot=int(r['slot'],16);name,desc,ret,count=IMPORTS[slot]
        args=[sp-236] if name=='QueryPerformanceCounter' else [OWNER+0xB188] if name=='QueryPerformanceFrequency' else [0]
        expected=dict(name=name,slot=hex(slot),va=hex(dword(raw,slot-BASE)),return_va=hex(ret),sp=sp-(392 if name=='QueryPerformanceCounter' else 112),
            args=args,request={},result=r['result'],live_host_observed=True)
        if r!=expected:raise ValueError('factory actual platform ABI on parent stack')
        if name=='GetDC':
            if not 0<r['result']['result']<=0xFFFFFFFF:raise ValueError('factory actual owned screen DC')
        elif r['result']['result']!=1 or len(bytes.fromhex(r['result']['hex']))!=8:raise ValueError('factory actual complete timer response')
    verify_constructor_trace(row,f['constructor_return'])
    return {r['name']:r['result'] for r in calls}


def verify_case(c):
    kind=c['factory'];f=FACTORIES[kind];depth=f['constructor_depth'];fill=c['fill'];raw=SOURCE.read_bytes()
    if c['root_args']!=[WINDOW,OUTPUT,c['width'],c['height']] or c['declared_root_receiver']!=RECEIVER:raise ValueError('factory explicit root inputs')
    prior=None;owner=initial_owner(fill);image=bytearray(raw);store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+OWNER_BYTES)
    for phase in ('allocation','constructor','admission'):
        row=c[phase];n=row['native'];cpu=dict(EIP=CTOR,ESP=TOP-depth,EBP=TOP-4,EAX=OWNER,EBX=0x55667788,ECX=OWNER,
            EDX=dword(raw,COUNTER-BASE)+OWNER_BYTES,ESI=0x88776655,EDI=TOP-16,EFLAGS=6)
        if phase=='allocation':
            before=dict(EIP=f['entry'],ESP=TOP,EBP=0x11223344,EBX=0x55667788,ESI=0x88776655,EDI=0x44332211,ECX=RECEIVER,EAX=0,EDX=0,EFLAGS=2)
            ret=0x412CA7 if kind=='window' else 0x4505AC
            entries=[dict(va=hex(f['entry']),return_va=hex(RETURN),sp=TOP,receiver=RECEIVER,args=c['root_args']),
                dict(va='0x428a40',return_va=hex(ret),sp=TOP-depth-4,receiver=0 if kind=='window' else RECEIVER,args=[OWNER_BYTES])]
            returns=[dict(va='0x56ce82',return_va='0x428ac2',sp=TOP-depth-12,eax=OWNER),dict(va='0x428ac5',return_va=hex(ret),sp=TOP-depth-4,eax=OWNER)]
            if n['entries']!=entries or n['returns']!=returns:raise ValueError('factory original allocation wrapper/stack return')
        else:
            before=prior['native']['cpu']
            if phase=='constructor':
                api=verify_constructor_row(c,row);owner=project_constructor(initial_owner(fill),api);image=bytearray(project_image(api))
                store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+OWNER_BYTES)
                cpu.update(EIP=f['constructor_return'],ESP=TOP-depth+4,ECX=TOP-16,EDX=OWNER,EFLAGS=70)
            elif kind=='window':cpu.update(EIP=0x413450,ESP=TOP-136,EAX=c['width'],ECX=OWNER,EDX=c['height'])
            else:cpu.update(EIP=0x4500B0,ESP=TOP-124,ECX=dword(raw,GAME_GLOBAL-BASE),EDX=OWNER)
        if row['phase']!=phase or row['before_cpu']!=before or n['cpu']!=cpu or n['boundary']!=hex(cpu['EIP']):raise ValueError('factory exact continuous original CPU')
        if phase!='constructor':
            if row['instruction_runs']!=source_runs(kind,phase):raise ValueError('factory exact source allocation/admission trace')
            if row['platform_calls']:raise ValueError('factory no platform calls outside constructor')
            if phase=='admission' and (n['entries'] or n['returns']):raise ValueError('factory child admission first instruction not executed')
        visited=sorted({r['va'] for r in row['instruction_runs']})
        if n['visited']!=visited or cpu['EIP'] in visited or n['platform_calls'] or n['live_results']:raise ValueError('factory original visited code/no D3D call')
        pending=dict(va=hex(cpu['EIP']),sp=cpu['ESP'],return_va=hex(f['constructor_return'] if phase=='allocation' else f['admission_return']),
            receiver=cpu['ECX'],args=[] if phase=='allocation' else [WINDOW,1,1,c['width'],c['height']] if kind=='window' else [0x598758],first_instruction_executed=False)
        if phase=='constructor':pending=dict(va=hex(cpu['EIP']),sp=cpu['ESP'],stack_top_dword=0x44332211,first_instruction_executed=False)
        if row['pending']!=pending:raise ValueError('factory correct entry versus parent stack-top boundary semantics')
        rule=source_contract()['allocator']
        expected=[dict(va='0x56e810',return_va='0x428a73',sp=TOP-depth-108,args=[OWNER_BYTES,1,rule['file'],rule['line']],
            pointer=OWNER,bytes=OWNER_BYTES,initial_byte=0xCD,adapter='declared debug CRT allocation')]
        if row['allocations']!=expected:raise ValueError('factory one exact owned CRT response')
        verify_state(row['state'],owner,bytes(image),TOP-16)
        verify_buffer(row['guarded_owner'],bytes([fill])*4096+owner+bytes([fill])*4096)
        out=bytearray(bytes([fill])*12288);store(out,4096,OUTPUT_VALUE);verify_buffer(row['guarded_output'],bytes(out))
        missing=[dict(global_va=hex(at),pointer=dword(raw,at-BASE),mapped=False) for at in (HEAD,GAME_GLOBAL)]
        if row['inherited_missing_heaps']!=missing:raise ValueError('factory inherited globals/missing heaps unchanged')
        if row['owner_constructed'] is not (phase!='allocation'):raise ValueError('factory actual owner construction scope')
        for k in ('factory_output_published','original_device_startup_executed','game_context_body_executed','audio_COM_initialized','retained_VM_advanced'):
            if row[k] is not False:raise ValueError('factory unresolved game/device/output/VM boundary')
        prior=row
    cleanup=dict(fonts_released=0,dcs_released=1,all_owned_resources_released=True)
    if c['platform_cleanup']!=cleanup:raise ValueError('factory actual DC lifetime cleanup')
    calls=c['constructor']['platform_calls'];expected=[dict(request=dict(id=i,op=r['name'],**r['request']),reply=dict(ok=True,id=i,result=r['result'])) for i,r in enumerate(calls,1)]
    expected.append(dict(request=dict(id=4,op='close'),reply=dict(ok=True,id=4,result=cleanup)))
    if c['platform_trace']!=expected:raise ValueError('factory full actual platform protocol trace')


def verify_report(report):
    if report['schema_version']!=1 or report['source_contract']!=source_contract():raise ValueError('factory original source contract')
    if report['platform_build']!=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(HELPER)!=0x14C:
        raise ValueError('factory unchanged owned x86 platform provenance')
    if [(c['factory'],c['fill'],c['width'],c['height']) for c in report['cases']]!=[(k,f,w,h) for k in FACTORIES for f,w,h in ((0xA5,640,480),(0xCC,1024,768))]:
        raise ValueError('factory exact four declared cases')
    for c in report['cases']:
        if c['platform_hello']['pointer_bytes']!=4:raise ValueError('factory actual x86 helper')
        verify_case(c)
    for k in ('one_continuous_trajectory_per_case','inherited_cache_and_game_globals_unchanged','CRT_adapter_executed'):
        if report[k] is not True:raise ValueError('factory same continuous original trajectory')
    for k in ('original_IAT_changed','game_helpers_stubbed','factory_output_published','original_device_startup_executed','retained_VM_advanced','full_outer_frame'):
        if report[k] is not False:raise ValueError('factory remaining initialization boundary')
    return dict(cases=4,actual_factory_owner_allocations=4,original_constructor_calls_per_case=42,
        window_stop='0x413450',game_stop='0x4500b0',inherited_cache_and_game_heaps_missing=True,
        factory_output_published=False,device_startup_executed=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))))
