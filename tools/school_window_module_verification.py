"""Raw genuine-instance prefix proof and original resource calls/full class verification."""
import argparse
import json
from pathlib import Path
from collections import Counter
from functools import lru_cache
from tools.school_window_module import *
from tools.school_window_module_validation import legacy_prefix_view
from tools.school_window_geometry_verification import maps as geometry_maps
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_verification import verify_buffer
from tools.school_window_module_platform import SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine

window=geometry.window
parent=geometry.parent


@lru_cache(maxsize=1)
def instructions():
    raw=SOURCE.read_bytes()
    return {i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}


def source_runs(phase):
    at=geometry.STOPS['class'] if phase=='icons' else STOPS['icons'];calls=[];rows=[];code=instructions()
    while at!=STOPS[phase]:
        if len(rows)>100:raise ValueError('module finite resource source walk')
        i=code[at];nxt=at+i.size;rows.append(dict(va=at,count=1))
        if i.mnemonic=='call' and i.op_str.startswith('0x'):calls.append(nxt);nxt=int(i.op_str,16)
        elif i.mnemonic=='ret':nxt=calls.pop()
        at=nxt
    if calls:raise ValueError('module original helper return boundary')
    return rows


def maps(extra):
    result=geometry_maps(True);raw=SOURCE.read_bytes()
    if extra:
        for slot in IMPORTS:
            target=dword(raw,slot-BASE);result.setdefault(target&~4095,bytearray(4096))[target%4096]=0xC3
    return result


def verify_maps(rows,extra):
    wanted=maps(extra)
    if [r['pointer'] for r in rows]!=sorted(wanted):raise ValueError('module exact resource import maps')
    for r in rows:verify_buffer({k:v for k,v in r.items() if k!='pointer'},wanted[r['pointer']])


def verify_api(r,module,index):
    raw=SOURCE.read_bytes();value=r['result']['result']
    if type(value) is not int or not 0<value<=0xFFFFFFFF:raise ValueError('module actual shared/stock handle bits')
    if index<2:
        name,op,slot,ret,sp,args='LoadIconA','load_icon',0x5923CC,(0x45041C if index==0 else 0x450439),geometry.FRAME_SP-12,[module,157]
        request=dict(module=module,id_value=157);result=dict(result=value,module=module,resource_id=157,shared=True,destroy_permitted=False)
    elif index==2:
        name,op,slot,ret,sp,args='LoadCursorA','load_cursor',0x5923C8,0x450452,geometry.FRAME_SP-12,[0,32512]
        request=dict(module=0,id_value=32512);result=dict(result=value,shared=True,destroy_permitted=False)
    else:
        name,op,slot,ret,sp,args='GetStockObject','stock_brush',0x592084,0x450466,geometry.FRAME_SP-8,[4]
        request=dict(id_value=4);result=dict(result=value,stock=True,delete_permitted=False)
    expected=dict(name=name,op=op,slot=hex(slot),va=hex(dword(raw,slot-BASE)),return_va=hex(ret),sp=sp,args=args,request=request,result=result,observed_EAX=value,live_host_observed=True)
    if r!=expected:raise ValueError('module exact original resource ABI/result/borrowed ownership')
    return value


def verify_case(c,through='class_ready'):
    _,proof=legacy_prefix_view(c)
    if through=='instance':return proof
    module=c['hello']['resource_module']['pointer'];old=c['class'];code=instructions();raw=SOURCE.read_bytes()
    admission=c['icons']['import_admission'];expected=dict(slots=[hex(s) for s in IMPORTS],before_cpu=old['cpu'],after_cpu=old['cpu'],
        retained_owner_sha256=old['state']['guarded_owner']['sha256'],retained_stack_sha256=old['state']['stack']['sha256'],retained_image_sha256=old['state']['image_sha256'],
        foreign_before=admission['foreign_before'],foreign_after=admission['foreign_after'],native_game_call=False)
    if admission!=expected:raise ValueError('module late resource admission preserves raw genuine-instance state')
    verify_maps(admission['foreign_before'],False);verify_maps(admission['foreign_after'],True)
    if admission['foreign_before']!=old['state']['foreign_maps'] or admission['foreign_after']!=c['icons']['state']['foreign_maps']:raise ValueError('module actual resource map continuity')
    calls=c['icons']['platform_calls']+c['class_ready']['platform_calls']
    if len(calls)!=4:raise ValueError('module all four original resource calls')
    handles=[verify_api(r,module,i) for i,r in enumerate(calls)]
    stack=bytearray(unpack(old['state']['stack']));owner=unpack(old['state']['owner']);fill=c['fill'];previous=old
    cls=bytearray(geometry.partial_class());store(cls,20,module)
    for phase in STOPS:
        n=c[phase];state=n['state'];runs=source_runs(phase)
        if n['phase']!=phase or n['before_cpu']!=previous['cpu'] or n['instruction_runs']!=runs:raise ValueError('module exact original resource path/CPU continuity')
        expected_cpu=dict(EIP=STOPS[phase],ESP=geometry.FRAME_SP-(4 if phase=='class_ready' else 0),EBP=geometry.FRAME_BP,
            EAX=handles[3] if phase=='class_ready' else handles[1],EBX=0x55667788,ECX=geometry.CLASS_AT if phase=='class_ready' else module,
            EDX=module,ESI=geometry.FRAME_SP,EDI=geometry.FRAME_BP,EFLAGS=70)
        if n['cpu']!=expected_cpu:raise ValueError('module complete original resource boundary CPU')
        pending=dict(va=hex(STOPS[phase]),sp=expected_cpu['ESP'],first_instruction_executed=False)
        if phase=='class_ready':pending.update(import_slot='0x592408',import_target=dword(raw,0x592408-BASE),stack_args=[geometry.CLASS_AT],call_instruction_executed=False)
        else:pending['stack_top_dword']=parent.BP
        if n['pending']!=pending:raise ValueError('module registration call instruction remains unexecuted')
        index=0 if phase=='icons' else 2
        rets=(0x450423,0x450440) if phase=='icons' else (0x450459,0x45046D)
        expected_returns=[dict(va='0x56ce82',return_va=hex(ret),sp=geometry.FRAME_SP-4,eax=handles[index+i]) for i,ret in enumerate(rets)]
        if n['entries'] or n['returns']!=expected_returns or n['platform_calls']!=calls[index:index+2]:raise ValueError('module natural stack-check returns and actual resource call order')
        if phase=='class_ready' and n['import_admission'] is not None:raise ValueError('module no late class map replacement')
        counts=Counter()
        for run in runs:
            i=code[run['va']]
            if i.mnemonic in ('push','call') or i.mnemonic=='mov' and '[' in i.op_str.split(',')[0]:counts[i.address]+=1
        if Counter(w['pc'] for w in n['native_writes'])!=counts:raise ValueError('module exact original resource write counts')
        for w in n['native_writes']:
            pc,p,size,value=w['pc'],w['pointer'],w['bytes'],w['value']
            if pc not in code or size!=4 or type(value) is not int or not 0<=value<=0xFFFFFFFF or not geometry.FRAME_SP-32<=p or p+4>geometry.ENTRY_SP:raise ValueError('module exact bounded resource stack writes')
            if code[pc].mnemonic=='call' and value!=pc+code[pc].size:raise ValueError('module source resource return-address push')
            store(stack,p-parent.STACK,value)
        if phase=='icons':store(cls,24,handles[0]);store(cls,44,handles[1])
        else:store(cls,28,handles[2]);store(cls,32,handles[3]);store(cls,36,0)
        if stack[geometry.CLASS_AT-parent.STACK:geometry.CLASS_AT-parent.STACK+48]!=cls:raise ValueError('module original actual handle/class field stores')
        verify_buffer(state['class_structure'],cls);verify_buffer(state['stack'],stack);verify_buffer(state['owner'],owner)
        verify_buffer(state['guarded_owner'],bytes([fill])*4096+owner+bytes([fill])*4096);verify_buffer(state['null_page'],bytes(4096));verify_maps(state['foreign_maps'],True)
        if state['image_sha256']!=old['state']['image_sha256'] or state['SEH']!=0 or n['genuine_instance']!=module:raise ValueError('module full raw source image/SEH/actual instance retained')
        for flag in ('class_registration_executed','callback_executed','window_created','retained_VM_advanced'):
            if n[flag] is not False:raise ValueError('module honest registration/callback/window boundary')
        previous=n
        if phase==through:return proof


def verify_report(report,through='class_ready'):
    if report['source_contract']!=source_contract() or [c['fill'] for c in report['cases']]!=[0xA5,0xCC]:raise ValueError('module actual source/resources/two declared inputs')
    pinned=json.loads((ROOT/'analysis/school-window-module-platform-v1-20261020.json').read_text(encoding='utf8'))
    build=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))
    if report['platform_build']!=pinned['build'] or build!=pinned['build'] or inspect_module(RESOURCE_DLL.read_bytes())!=pinned['resource_dll']:raise ValueError('module actual resource/helper build provenance')
    proofs=[]
    for c in report['cases']:
        h=json.loads(json.dumps(c['hello']));module=h['resource_module']['pointer']
        if type(module) is not int or not 0<module<=0xFFFFFFFF:raise ValueError('module actual owned HMODULE input')
        h['resource_module']['pointer']=pinned['hello']['resource_module']['pointer']
        if h!=pinned['hello'] or c['system_modules']!=pinned['system_modules']:raise ValueError('module actual loaded code-free resources/system identities')
        for r in c['system_modules'].values():
            if machine(r['path'])!=0x14C or sha(Path(r['path']).read_bytes())!=r['sha256']:raise ValueError('module actual x86 system module bytes')
        proofs.append(verify_case(c,through))
        calls=c['constructor']['platform_calls']+c['query']['platform_calls']+c['rect']['platform_calls']+c['adjust']['platform_calls']+c['icons']['platform_calls']+c['class_ready']['platform_calls']
        cleanup=dict(resource_module_refs_released=1,gdi32_module_refs_released=1,icon_load_calls=2,cursor_load_calls=1,stock_brush_calls=1,
            shared_icons_destroyed=0,shared_cursor_destroyed=False,stock_brush_deleted=False,critical_sections_deleted=2,event_handles_closed=1,user32_module_refs_released=1,
            set_rect_calls=1,adjust_window_rect_calls=1,all_owned_resources_released=True)
        trace=[dict(request=dict(id=i+1,op=r.get('op',r['name']),**r['request']),reply=dict(ok=True,id=i+1,result=r['result'])) for i,r in enumerate(calls)]
        trace.append(dict(request=dict(id=len(calls)+1,op='close'),reply=dict(ok=True,id=len(calls)+1,result=cleanup)))
        if c['platform_trace']!=trace or c['platform_cleanup']!=cleanup:raise ValueError('module complete same-lifetime protocol and actual/shared resource cleanup')
    for k,v in dict(actual_genuine_module_declared_before_first_instruction=True,one_continuous_CPU_per_case=True,original_IAT_changed=False,
            game_helpers_stubbed=False,class_registration_executed=False,callback_executed=False,window_created=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False).items():
        if report[k] is not v:raise ValueError('module report runtime authority')
    return dict(cases=2,verified_through=through,genuine_instances=[p['actual_module'] for p in proofs],legacy_view_substitutions=[len(p['substitutions']) for p in proofs],
        raw_prefix_sha256=[p['raw_prefix_sha256'] for p in proofs],native_resource_calls_per_case=4,pending='0x45047d',class_registration_executed=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--through',choices=['instance','icons','class_ready'],default='class_ready');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')),a.through),indent=2))
