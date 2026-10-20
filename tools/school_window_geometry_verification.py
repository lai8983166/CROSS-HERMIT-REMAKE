"""Independent source paths, exact geometry ABI, partial class and full-memory replay."""
import argparse
import json
from pathlib import Path
from functools import lru_cache
from collections import Counter
from tools.school_window_geometry import *
from tools.school_main_window_verification import verify_case as verify_window_case,expected_maps as window_maps
from tools.school_renderer_init_verification import verify_buffer
from tools.school_device_init_verification import unpack
from tools.school_window_geometry_platform import SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine


@lru_cache(maxsize=1)
def instructions():
    raw=SOURCE.read_bytes()
    return {i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}


def source_runs(phase):
    at={'rect':ENTRY,'adjust':STOPS['rect'],'class':STOPS['adjust']}[phase];code=instructions();calls=[];rows=[]
    while at!=STOPS[phase]:
        if len(rows)>100:raise ValueError('geometry finite source walk')
        i=code[at];nxt=at+i.size;rows.append(dict(va=at,count=34 if at==0x45036D else 1))
        if i.mnemonic=='call' and i.op_str.startswith('0x'):calls.append(nxt);nxt=int(i.op_str,16)
        elif i.mnemonic=='ret':nxt=calls.pop()
        at=nxt
    if calls:raise ValueError('geometry source helper returns before boundary')
    return rows


def maps(extra):
    result=window_maps(True);raw=SOURCE.read_bytes()
    if extra:
        for slot in IMPORTS:
            target=dword(raw,slot-BASE);result.setdefault(target&~4095,bytearray(4096))[target%4096]=0xC3
    return result


def verify_maps(rows,extra):
    wanted=maps(extra)
    if [r['pointer'] for r in rows]!=sorted(wanted):raise ValueError('geometry exact new import maps')
    for r in rows:verify_buffer({k:v for k,v in r.items() if k!='pointer'},wanted[r['pointer']])


def verify_admission(c):
    a=c['rect']['import_admission'];before=c['branch']
    expected=dict(slots=[hex(s) for s in IMPORTS],before_cpu=before['cpu'],after_cpu=before['cpu'],
        retained_owner_sha256=before['state']['guarded_owner']['sha256'],retained_stack_sha256=before['state']['stack']['sha256'],
        retained_image_sha256=before['state']['image_sha256'],retained_null_page_sha256=sha(bytes(4096)),
        foreign_before=a['foreign_before'],foreign_after=a['foreign_after'],native_game_call=False)
    if a!=expected:raise ValueError('geometry late import admission preserves full pending state')
    verify_maps(a['foreign_before'],False);verify_maps(a['foreign_after'],True)
    if a['foreign_before']!=before['state']['foreign_maps'] or a['foreign_after']!=c['rect']['state']['foreign_maps']:raise ValueError('geometry exact import-map continuity')


def verify_api(row):
    phase=row['phase'];calls=row['platform_calls'];raw=SOURCE.read_bytes()
    if phase=='class':
        if calls:raise ValueError('geometry no icon/system call in class preparation')
        return None
    if len(calls)!=1:raise ValueError('geometry exactly one original API call per geometry phase')
    r=calls[0];result=r['result'];eax=result['result']
    if type(eax) is not int or not 0<eax<=0xFFFFFFFF:raise ValueError('geometry actual nonzero BOOL bits')
    if result!=dict(result=eax,hex=CLIENT_RECT.hex(),guards_unchanged=True):raise ValueError('geometry complete actual RECT/guard preservation')
    if phase=='rect':
        name,op,slot,ret,sp,args='SetRect','set_rect',0x5923F8,0x450395,FRAME_SP-24,[parent.OWNER+CLIENT_OFFSET,0,0,1024,768]
        request=dict(before_hex='cd'*16,args=[0,0,1024,768])
    else:
        name,op,slot,ret,sp,args='AdjustWindowRect','adjust_window_rect',0x5923FC,0x4503CE,FRAME_SP-16,[RECT_AT,STYLE,0]
        request=dict(before_hex=CLIENT_RECT.hex(),style=STYLE,menu=0)
    wanted=dict(name=name,op=op,slot=hex(slot),va=hex(dword(raw,slot-BASE)),return_va=hex(ret),sp=sp,args=args,
        request=request,result=result,observed_EAX=eax,mapped_output_pointer=args[0],mapped_output_bytes=16,live_host_observed=True)
    if r!=wanted:raise ValueError('geometry original import/parent stack/arguments/full output')
    return eax


def verify_case(c,through='class'):
    verify_window_case(c)
    if c['query']['observed_duplicate'] is not False or c['branch']['pending']['va']!=hex(ENTRY):raise ValueError('geometry requires actual original absent-window admission')
    verify_admission(c);previous=c['branch'];code=instructions();fill=c['fill']
    owner=bytearray(unpack(previous['state']['owner']));stack=bytearray(unpack(previous['state']['stack']));expected_owner=project_owner(bytes(owner))
    raw=SOURCE.read_bytes();rect_eax=c['rect']['platform_calls'][0]['result']['result'];adjust_eax=c['adjust']['platform_calls'][0]['result']['result']
    for phase in STOPS:
        row=c[phase];state=row['state'];runs=source_runs(phase);eax=verify_api(row)
        if row['phase']!=phase or row['instruction_runs']!=runs or row['before_cpu']!=previous['cpu']:raise ValueError('geometry exact source path/REP/pending CPU continuity')
        cpu=dict(EIP=STOPS[phase],ESP=FRAME_SP,EBP=FRAME_BP,EAX=rect_eax if phase=='rect' else adjust_eax,
            EBX=0x55667788,ECX=parent.OWNER+CLIENT_OFFSET if phase=='rect' else 768 if phase=='adjust' else window.HINSTANCE,
            EDX=0 if phase=='rect' else STYLE if phase=='adjust' else window.HINSTANCE,ESI=FRAME_SP,EDI=FRAME_BP,EFLAGS=70)
        if phase=='class':cpu['ESP']-=8
        if row['cpu']!=cpu:raise ValueError('geometry complete original boundary CPU')
        pending=dict(va=hex(STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='class':pending.update(import_slot='0x5923cc',import_target=dword(raw,0x5923CC-BASE),stack_args=[window.HINSTANCE,157],call_instruction_executed=False)
        else:pending['stack_top_dword']=parent.BP
        if row['pending']!=pending:raise ValueError('geometry unexecuted instruction versus callee boundary semantics')
        entries=[dict(va=hex(ENTRY),return_va='0x49decb',sp=ENTRY_SP,receiver=parent.OWNER,args=[0,0,1024,768,STYLE,1])] if phase=='rect' else []
        returns=[] if phase=='class' else [dict(va='0x56ce82',return_va=hex(STOPS[phase]),sp=FRAME_SP-4,eax=eax)]
        if row['entries']!=entries or row['returns']!=returns:raise ValueError('geometry actual original root and stack-check returns')
        if phase!='rect' and row['import_admission'] is not None:raise ValueError('geometry no new map change after first boundary')
        counts=Counter()
        for run in runs:
            i=code[run['va']]
            if i.mnemonic.startswith('rep stos'):counts[i.address]+=run['count']-1
            elif i.mnemonic in ('push','call') or i.mnemonic=='mov' and '[' in i.op_str.split(',')[0]:counts[i.address]+=1
        if +Counter(w['pc'] for w in row['native_writes'])!=+counts:raise ValueError('geometry exact source write multiplicity')
        for w in row['native_writes']:
            pc,p,n,value=w['pc'],w['pointer'],w['bytes'],w['value']
            if pc not in code or n!=4 or type(value) is not int or not 0<=value<=0xFFFFFFFF or not FRAME_SP-64<=p or p+n>ENTRY_SP:raise ValueError('geometry exact bounded stack writes')
            if code[pc].mnemonic=='call' and value!=pc+code[pc].size:raise ValueError('geometry original call return-address writes')
            store(stack,p-parent.STACK,value)
        if phase=='rect':owner[CLIENT_OFFSET:CLIENT_OFFSET+16]=bytes.fromhex(row['platform_calls'][0]['result']['hex'])
        if phase=='adjust':
            if stack[RECT_AT-parent.STACK:RECT_AT-parent.STACK+16]!=CLIENT_RECT:raise ValueError('geometry original client-to-local copy before adjustment')
            stack[RECT_AT-parent.STACK:RECT_AT-parent.STACK+16]=bytes.fromhex(row['platform_calls'][0]['result']['hex'])
        if owner!=expected_owner:raise ValueError('geometry full owner/API replay equals independent projection')
        verify_buffer(state['owner'],expected_owner);verify_buffer(state['guarded_owner'],bytes([fill])*4096+expected_owner+bytes([fill])*4096)
        verify_buffer(state['stack'],stack);verify_buffer(state['client_rectangle'],CLIENT_RECT)
        verify_buffer(state['local_rectangle'],b'\xcc'*16 if phase=='rect' else CLIENT_RECT)
        verify_buffer(state['class_structure'],partial_class() if phase=='class' else b'\xcc'*48)
        cls=bytes(stack[CLASS_AT-parent.STACK:CLASS_AT-parent.STACK+48]);rectangle=bytes(stack[RECT_AT-parent.STACK:RECT_AT-parent.STACK+16])
        if cls!=(partial_class() if phase=='class' else b'\xcc'*48) or rectangle!=(b'\xcc'*16 if phase=='rect' else CLIENT_RECT):raise ValueError('geometry original complete local structures')
        verify_buffer(state['null_page'],bytes(4096));verify_maps(state['foreign_maps'],True)
        if state['image_sha256']!=c['branch']['state']['image_sha256'] or state['SEH']!=0:raise ValueError('geometry preserved full original image/SEH')
        if dword(stack,ENTRY_SP-parent.STACK)!=0x49DECB or [dword(stack,ENTRY_SP+4+i*4-parent.STACK) for i in range(6)]!=[0,0,1024,768,STYLE,1]:raise ValueError('geometry original parent return and six arguments preserved')
        for flag in ('LoadIconA_executed','class_registered','window_created','retained_VM_advanced'):
            if row[flag] is not False:raise ValueError('geometry honest unexecuted icon/window boundary')
        if row['original_window_function_prefix_executed'] is not True:raise ValueError('geometry original prefix execution authority')
        previous=row
        if phase==through:return


def verify_report(report,through='class'):
    if report['source_contract']!=source_contract() or [c['fill'] for c in report['cases']]!=[0xA5,0xCC]:raise ValueError('geometry exact source/resource/two-case inputs')
    pinned=json.loads((ROOT/'analysis/school-window-geometry-platform-v1-20261020.json').read_text(encoding='utf8'))
    build=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))
    if report['platform_build']!=pinned['build'] or build!=pinned['build']:raise ValueError('geometry actual helper build identity')
    for c in report['cases']:
        if c['hello']!=pinned['hello'] or c['system_modules']!=pinned['system_modules']:raise ValueError('geometry actual helper/system identity')
        for r in c['system_modules'].values():
            if machine(r['path'])!=0x14C or sha(Path(r['path']).read_bytes())!=r['sha256']:raise ValueError('geometry actual x86 system bytes')
        verify_case(c,through)
        calls=c['constructor']['platform_calls']+c['query']['platform_calls']+c['rect']['platform_calls']+c['adjust']['platform_calls']
        cleanup=dict(critical_sections_deleted=2,event_handles_closed=1,user32_module_refs_released=1,set_rect_calls=1,adjust_window_rect_calls=1,all_owned_resources_released=True)
        trace=[dict(request=dict(id=i+1,op=r.get('op',r['name']),**r['request']),reply=dict(ok=True,id=i+1,result=r['result'])) for i,r in enumerate(calls)]
        trace.append(dict(request=dict(id=len(calls)+1,op='close'),reply=dict(ok=True,id=len(calls)+1,result=cleanup)))
        if c['platform_trace']!=trace or c['platform_cleanup']!=cleanup:raise ValueError('geometry complete same-lifetime protocol/call counts/cleanup')
    for k,v in dict(actual_prefix_replayed_under_new_build_identity=True,one_continuous_CPU_per_case=True,declared_mid_WinMain_frame=True,
            original_IAT_changed=False,game_helpers_stubbed=False,LoadIconA_executed=False,window_created=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False).items():
        if report[k] is not v:raise ValueError('geometry report authority')
    return dict(cases=2,verified_through=through,original_geometry_calls_per_case=2,partial_class_initialized_dwords=7,
        partial_class_uninitialized_dwords=5,icon_group=157,icon_image=5,pending='0x450416',LoadIconA_executed=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--through',choices=list(STOPS),default='class');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')),a.through),indent=2))
