"""Independent source walk, live query ABI, full writes and parent-prefix checks."""
import argparse
import json
from pathlib import Path
from collections import Counter
from functools import lru_cache
from tools.school_main_window import *
from tools.school_main_context_verification import verify_case as verify_parent_case
from tools.school_renderer_init_verification import verify_buffer
from tools.school_device_init_verification import unpack
from tools.school_main_window_platform import SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine


@lru_cache(maxsize=1)
def instructions():
    raw=SOURCE.read_bytes()
    return {i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}


def source_runs(phase,duplicate):
    at={'tasks':ENTRY,'query':STOPS['tasks'],'branch':STOPS['query']}[phase]
    stop=STOPS[phase] if phase!='branch' else EXIT_ENTRY if duplicate else WINDOW_ENTRY
    code=instructions();counter=0;calls=[];rows=[]
    while at!=stop:
        if len(rows)>600:raise ValueError('window bounded original source walk')
        i=code[at];nxt=at+i.size;rows.append(dict(va=at,count=19 if at in (0x421677,0x4293F7) else 18 if at==0x4502A7 else 1))
        if at==0x421686:counter+=1
        if i.mnemonic=='call':
            if i.op_str.startswith('0x'):calls.append(nxt);nxt=int(i.op_str,16)
        elif i.mnemonic=='ret':nxt=calls.pop()
        elif i.mnemonic=='jmp':nxt=int(i.op_str,16)
        elif i.mnemonic.startswith('j'):
            take=(at==0x421693 and counter==32) or at in (0x42941A,0x49DE55) and not duplicate
            if take:nxt=int(i.op_str,16)
        at=nxt
    if calls!=([0x49DECB] if phase=='branch' and not duplicate else []):raise ValueError('window natural pending call stack')
    return rows


def expected_maps(extra=False):
    raw=SOURCE.read_bytes();maps={}
    for slot in (*parent.IMPORTS,*([FIND_SLOT] if extra else [])):
        target=dword(raw,slot-BASE);maps.setdefault(target&~4095,bytearray(4096))[target%4096]=0xC3
    return maps


def verify_maps(rows,extra):
    maps=expected_maps(extra)
    if [r['pointer'] for r in rows]!=sorted(maps):raise ValueError('window exact declared import maps')
    for r in rows:verify_buffer({k:v for k,v in r.items() if k!='pointer'},maps[r['pointer']])


def verify_query(c):
    calls=c['query']['platform_calls'];raw=SOURCE.read_bytes()
    if len(calls)!=2:raise ValueError('window exact two new system calls')
    before=raw[TITLE-BASE:TITLE-BASE+TITLE_BYTES];after=bytearray(before);after[:len(TITLE_TEXT)]=TITLE_TEXT
    t,q=calls
    title_result=dict(return_offset=0,hex=bytes(after).hex(),guards_unchanged=True,source_unchanged=True)
    wanted=dict(name='lstrcpyA',op='copy_title',slot='0x592294',va=hex(dword(raw,0x592294-BASE)),return_va='0x49de3e',sp=parent.SP-12,args=[TITLE,0x598748],
        request=dict(before_hex=before.hex(),source_hex=TITLE_TEXT.hex()),result=title_result,observed_EAX=TITLE,mapped_output_pointer=TITLE,mapped_output_bytes=TITLE_BYTES,live_host_observed=True)
    if t!=wanted:raise ValueError('window exact title buffer/ABI/return/source preservation')
    hwnd=q['result']['result']
    if type(hwnd) is not int or not 0<=hwnd<=0xFFFFFFFF:raise ValueError('window actual borrowed HWND bits')
    wanted=dict(name='FindWindowA',op='find_window',slot=hex(FIND_SLOT),va=hex(dword(raw,FIND_SLOT-BASE)),return_va='0x42940c',sp=parent.SP-104,args=[TITLE,0],
        request=dict(class_hex=TITLE_TEXT.hex(),window_name=0),result=dict(result=hwnd,guards_unchanged=True,class_unchanged=True,window_owned=False,window_manipulated=False),
        observed_EAX=hwnd,mapped_output_pointer=None,mapped_output_bytes=0,live_host_observed=True)
    if q!=wanted:raise ValueError('window actual query identity/arguments/result/borrowed ownership')
    a=c['query']['import_admission'];previous=c['tasks'];target=dword(raw,FIND_SLOT-BASE)
    wanted=dict(slot=hex(FIND_SLOT),target=target,before_cpu=previous['cpu'],after_cpu=previous['cpu'],
        retained_owner_sha256=previous['state']['guarded_owner']['sha256'],retained_stack_sha256=previous['state']['stack']['sha256'],
        retained_image_sha256=previous['state']['image_sha256'],retained_null_page_sha256=sha(bytes(4096)),
        foreign_before=a['foreign_before'],foreign_after=a['foreign_after'],native_game_call=False)
    if a!=wanted:raise ValueError('window import admission preserves complete pending state')
    verify_maps(a['foreign_before'],False);verify_maps(a['foreign_after'],True)
    if a['foreign_before']!=previous['state']['foreign_maps'] or a['foreign_after']!=c['query']['state']['foreign_maps']:raise ValueError('window exact import admission map continuity')
    return hwnd


def verify_case(c,through='branch'):
    verify_parent_case(c)
    hwnd=verify_query(c);duplicate=hwnd!=0
    oldcalls=c['constructor']['platform_calls'];fill=c['fill'];raw=SOURCE.read_bytes()
    baseowner=parent.project_constructor(parent.initial_owner(fill),oldcalls);baseimage=parent.project_image('publication',oldcalls)
    owner=bytearray(baseowner);image=bytearray(baseimage);stack=bytearray(unpack(c['publication']['state']['stack']))
    previous=c['publication'];code=instructions()
    for phase in ('tasks','query','branch'):
        row=c[phase];state=row['state'];stop=STOPS[phase] if phase!='branch' else EXIT_ENTRY if duplicate else WINDOW_ENTRY
        runs=source_runs(phase,duplicate)
        if row['phase']!=phase or row['instruction_runs']!=runs:raise ValueError('window exact original source path/loop/REP counts')
        if row['before_cpu']!=previous['cpu']:raise ValueError('window same original pending CPU continuity')
        cpu=dict(EIP=stop,ESP=parent.SP,EBP=parent.BP,EAX=0,EBX=0x55667788,ECX=parent.OWNER+0x64,
            EDX=HINSTANCE,ESI=0x88776655,EDI=parent.BP,EFLAGS=70)
        if phase!='tasks':cpu.update(EAX=int(duplicate),ECX=parent.OWNER+0x34,ESI=parent.SP)
        if phase=='branch':
            cpu['EFLAGS']=2
            if not duplicate:cpu.update(ESP=parent.SP-28,EAX=1024,ECX=parent.OWNER,EDX=0)
        if row['cpu']!=cpu:raise ValueError('window exact original CPU at boundary')
        pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='branch' and not duplicate:pending.update(return_va='0x49decb',receiver=parent.OWNER,args=[0,0,1024,768,0x90000000,1])
        else:pending['stack_top_dword']=0x44332211
        if row['pending']!=pending:raise ValueError('window natural caller/callee pending semantics')
        def entry(va,ret,sp,receiver,args):return dict(va=hex(va),return_va=hex(ret),sp=sp,receiver=receiver,args=args)
        def ret(va,result,sp,eax):return dict(va=hex(va),return_va=hex(result),sp=sp,eax=eax)
        if phase=='tasks':
            entries=[entry(0x421660,0x49DE23,parent.SP-4,parent.OWNER+0x64,[])]
            returns=[ret(0x4216BA,0x49DE23,parent.SP-4,0)]
        elif phase=='query':
            entries=[entry(0x4293E0,0x49DE53,parent.SP-4,parent.OWNER+0x34,[])]
            returns=[ret(0x56CE82,0x49DE45,parent.SP-4,TITLE),ret(0x56CE82,0x429413,parent.SP-96,hwnd),
                ret(0x56CE82,0x429432,parent.SP-12,int(duplicate)),ret(0x429435,0x49DE53,parent.SP-4,int(duplicate))]
        elif duplicate:entries,returns=[],[]
        else:
            entries=[entry(0x450290,0x49DE6B,parent.SP-8,parent.OWNER,[0])]
            returns=[ret(0x4502BF,0x49DE6B,parent.SP-8,parent.OWNER)]
        if row['entries']!=entries or row['returns']!=returns:raise ValueError('window exact original native receiver/arguments/return stack')
        if phase!='query' and (row['platform_calls'] or row['import_admission'] is not None):raise ValueError('window no platform or map change outside query phase')
        expected_writes=Counter()
        for run in runs:
            i=code[run['va']]
            if i.mnemonic.startswith('rep stos'):expected_writes[i.address]+=run['count']-1
            elif i.mnemonic in ('push','call') or i.mnemonic in ('mov','add','sub') and '[' in i.op_str.split(',')[0]:expected_writes[i.address]+=1
        if +Counter(w['pc'] for w in row['native_writes'])!=+expected_writes:raise ValueError('window exact source write counts')
        task_stores=[]
        for w in row['native_writes']:
            pc,p,n,value=w['pc'],w['pointer'],w['bytes'],w['value']
            if pc not in code or type(n) is not int or n!=4 or type(value) is not int or not 0<=value<=0xFFFFFFFF:raise ValueError('window bounded source write schema')
            if code[pc].mnemonic=='call' and value!=pc+code[pc].size:raise ValueError('window original return-address push')
            if parent.SP-1024<=p and p+n<=parent.BP:store(stack,p-parent.STACK,value)
            elif phase=='tasks' and p==INSTANCE and (pc,value)==(0x49DE26,HINSTANCE):store(image,p-BASE,value)
            elif phase=='tasks' and pc in (0x42169B,0x4216A9) and parent.OWNER+0x64<=p<parent.OWNER+0x164:
                task_stores.append((pc,p,value));store(owner,p-parent.OWNER,value)
            elif phase=='branch' and not duplicate and (pc,p,value) in ((0x4502B3,parent.OWNER+0x1108,0),
                    (0x49DE71,parent.OWNER+0x5C,0x69),(0x49DE7E,parent.OWNER+0x60,0x67)):store(owner,p-parent.OWNER,value)
            else:raise ValueError('window exact source write ownership')
        if phase=='tasks':
            expected=[x for i in range(32) for x in ((0x42169B,parent.OWNER+0x64+i*8+4,0),(0x4216A9,parent.OWNER+0x64+i*8,0))]
            if task_stores!=expected:raise ValueError('window complete32 task records in original order')
        if phase=='query':image[TITLE-BASE:TITLE-BASE+TITLE_BYTES]=bytes.fromhex(row['platform_calls'][0]['result']['hex'])
        wanted_owner=project_owner(baseowner,phase,duplicate);wanted_image=project_image(baseimage,phase)
        if owner!=wanted_owner or image!=wanted_image:raise ValueError('window complete source/API replay matches independent projections')
        verify_buffer(state['owner'],wanted_owner);verify_buffer(state['guarded_owner'],bytes([fill])*4096+wanted_owner+bytes([fill])*4096)
        verify_buffer(state['stack'],stack);verify_buffer(state['null_page'],bytes(4096));verify_buffer(state['title'],image[TITLE-BASE:TITLE-BASE+TITLE_BYTES])
        if state['image_sha256']!=sha(wanted_image) or state['SEH']!=0 or state['instance_value']!=HINSTANCE:raise ValueError('window complete image/instance/SEH')
        verify_maps(state['foreign_maps'],phase!='tasks')
        if row['observed_duplicate']!=(None if phase=='tasks' else duplicate):raise ValueError('window original branch uses only actual observed result')
        for flag in ('window_creation_body_executed','exit_body_executed','retained_VM_advanced'):
            if row[flag] is not False:raise ValueError('window exact unexecuted boundary authority')
        for p,value in ((parent.BP,0x11223344),(parent.SP,0x44332211),(parent.SP+4,0x88776655),(parent.SP+8,0x55667788)):
            if dword(stack,p-parent.STACK)!=value:raise ValueError('window parent saved registers preserved')
        previous=row
        if phase==through:return


def verify_report(report,through='branch'):
    if report['source_contract']!=source_contract() or [c['fill'] for c in report['cases']]!=[0xA5,0xCC]:raise ValueError('window complete source/two declared cases')
    pinned=json.loads((ROOT/'analysis/school-main-window-platform-v1-20261020.json').read_text(encoding='utf8'))
    build=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))
    if report['platform_build']!=pinned['build'] or build!=pinned['build']:raise ValueError('window actual new helper build identity')
    outcomes=[]
    for c in report['cases']:
        if c['hello']!=pinned['hello'] or c['system_modules']!=pinned['system_modules']:raise ValueError('window actual helper/system provenance')
        for r in c['system_modules'].values():
            if machine(r['path'])!=0x14C or sha(Path(r['path']).read_bytes())!=r['sha256']:raise ValueError('window actual x86 system bytes')
        verify_case(c,through)
        calls=c['constructor']['platform_calls']+c['query']['platform_calls'];cleanup=dict(critical_sections_deleted=2,event_handles_closed=1,user32_module_refs_released=1,all_owned_resources_released=True)
        trace=[dict(request=dict(id=i+1,op=r.get('op',r['name']),**r['request']),reply=dict(ok=True,id=i+1,result=r['result'])) for i,r in enumerate(calls)]
        trace.append(dict(request=dict(id=len(calls)+1,op='close'),reply=dict(ok=True,id=len(calls)+1,result=cleanup)))
        if c['platform_trace']!=trace or c['platform_cleanup']!=cleanup:raise ValueError('window complete constructor/title/query/cleanup protocol')
        outcomes.append(c['query']['observed_duplicate'])
    for k,v in dict(prefix_verified_with_new_build_identity=True,one_continuous_CPU_per_case=True,declared_mid_WinMain_frame=True,
            live_query_result_fabricated=False,original_IAT_changed=False,game_helpers_stubbed=False,retained_VM_advanced=False,window_created=False,standalone_resumable_checkpoint=False).items():
        if report[k] is not v:raise ValueError('window report scope authority')
    return dict(cases=2,verified_through=through,original_task_slots=32,actual_new_system_calls_per_case=2,
        observed_duplicate=outcomes,pending=[c['branch']['pending']['va'] for c in report['cases']],retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--through',choices=['tasks','query','branch'],default='branch');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')),a.through),indent=2))
