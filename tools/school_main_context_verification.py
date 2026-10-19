"""Independent main-context source flow, exact ABI and complete memory projections."""
import argparse
import json
from collections import Counter
from pathlib import Path
from functools import lru_cache
from tools.school_main_context import *
from tools.school_main_context_emulation import initial_cpu,initial_stack
from tools.school_main_context_platform import SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine,WORKDIR
from tools.school_renderer_init_verification import verify_buffer


@lru_cache(maxsize=1)
def instructions():
    raw=SOURCE.read_bytes()
    return {i.address:i for a,b in functions().items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}


def frame(va):
    if va==ENTRY:return 0
    total=0;filled=False
    for i in instructions().values():
        if i.address<va or i.address>=functions()[va]:continue
        if filled and not (i.mnemonic=='pop' and i.op_str=='ecx'):return total
        if i.mnemonic=='push':total+=4
        elif i.mnemonic=='pop':total-=4
        elif i.mnemonic in ('sub','add') and i.op_str.startswith('esp, '):
            total+=int(i.op_str.split(', ')[1],0)*(1 if i.mnemonic=='sub' else -1)
        elif i.mnemonic.startswith('rep '):filled=True
    raise ValueError('main finite source frame')


def expected_runs(phase):
    if phase=='constructor':raise ValueError('main constructor requires complete native trace')
    code=instructions();at=ENTRY if phase=='allocation' else STOPS['constructor'];rows=[];calls=[]
    while at!=STOPS[phase]:
        i=code[at];nxt=at+i.size;count={0x4288F6:17,0x428A56:18}.get(at,1);rows.append(dict(va=at,count=count))
        if len(rows)>160:raise ValueError('main bounded source walk')
        if i.mnemonic=='call':
            target=int(i.op_str,16)
            if target!=0x56E810:calls.append(nxt);nxt=target
        elif i.mnemonic=='ret':nxt=calls.pop()
        elif i.mnemonic=='jmp':nxt=int(i.op_str,16)
        elif i.mnemonic.startswith('j') and at in (0x428A8C,0x49DE0E):nxt=int(i.op_str,16)
        at=nxt
    if calls!=([0x49DDEC] if phase=='allocation' else []):raise ValueError('main pending source call stack')
    return rows


def verify_trace(row):
    phase=row['phase'];code=instructions();runs=row['instruction_runs'];entries=iter(row['entries']);returns=iter(row['returns']);active=[]
    expected_start=ENTRY if phase=='allocation' else CTOR if phase=='constructor' else STOPS['constructor']
    if not runs or runs[0]['va']!=expected_start:raise ValueError('main contiguous source trace start')
    if phase!='constructor' and runs!=expected_runs(phase):raise ValueError('main exact allocation/publication source trace')
    if phase=='constructor' and sum(r['count'] for r in runs)!=1694:raise ValueError('main complete constructor instruction count')
    # The parent remains active between phase nodes; the root is an admitted frame.
    root_sp=SP-4 if phase=='constructor' else SP
    active=[dict(va=CTOR if phase=='constructor' else ENTRY,sp=root_sp,return_va=0x49DDEC if phase=='constructor' else None,args=[])]
    if phase=='constructor':
        e=next(entries,None)
        if e!=dict(va=hex(CTOR),sp=SP-4,return_va='0x49ddec',receiver=OWNER,args=[]):raise ValueError('main actual constructor parent stack')
    for index,r in enumerate(runs):
        at=r['va'];i=code.get(at)
        if i is None or set(r)!={'va','count'} or type(r['count']) is not int or r['count']<1:raise ValueError('main bounded original instruction run')
        fall=at+i.size;nxt=runs[index+1]['va'] if index+1<len(runs) else STOPS[phase];expected={fall}
        if i.mnemonic.startswith('rep '):
            if at==0x56CF01:
                a=active[-1]['args'];wanted=a[2]//4+1
                if active[-1]['va']!=0x56CEC0 or a[0]%4:raise ValueError('main original aligned clear REP')
            else:
                previous=[j for j in code.values() if at-20<=j.address<at and j.mnemonic=='mov' and j.op_str.startswith('ecx, 0x')]
                if not previous:raise ValueError('main original REP prologue counter')
                wanted=int(max(previous,key=lambda j:j.address).op_str.split(', ')[1],0)+1
            if r['count']!=wanted:raise ValueError('main exact original REP count')
        elif r['count']!=1:raise ValueError('main only REP may repeat')
        if i.mnemonic=='call':
            if i.op_str.startswith('0x'):
                target=int(i.op_str,16)
                if target==0x56E810:expected={fall}
                else:
                    expected={target}
                    if target==STOPS[phase]:active.append(dict(va=target,sp=None,return_va=fall,args=[]))
                    elif target==0x56CE80:active.append(dict(va=target,sp=None,return_va=fall,args=[]))
                    else:
                        e=next(entries,None)
                        if e is None or e['va']!=hex(target) or e['return_va']!=hex(fall):raise ValueError('main original call/entry order')
                        parent=active[-1];sp=parent['sp']-frame(parent['va'])-4-4*ARGS.get(target,0)
                        if e['sp']!=sp or len(e['args'])!=ARGS.get(target,0):raise ValueError('main exact nested native stack ABI')
                        active.append(dict(va=target,sp=sp,return_va=fall,args=e['args']))
            else:
                api=next((r for r in row['platform_calls'] if int(r['return_va'],16)==fall),None)
                if api is None or i.op_str!='dword ptr ['+api['slot']+']':raise ValueError('main exact original import call')
                parent=active[-1]
                if api['sp']!=parent['sp']-frame(parent['va'])-4-4*len(api['args']):raise ValueError('main exact system call parent ABI')
        elif i.mnemonic=='ret':
            ret=next(returns,None)
            if ret is None or ret['va']!=hex(at):raise ValueError('main exact original return order')
            entry=active.pop()
            if ret['return_va']!=hex(entry['return_va']) or entry['sp'] is not None and ret['sp']!=entry['sp']:raise ValueError('main natural original return stack')
            expected={int(ret['return_va'],16)}
        elif i.mnemonic=='jmp':expected={int(i.op_str,16)}
        elif i.mnemonic.startswith('j'):expected.add(int(i.op_str,16))
        if nxt not in expected:raise ValueError('main contiguous original source control flow')
    if next(entries,None) is not None or next(returns,None) is not None:raise ValueError('main no extra native entries/returns')
    if phase=='allocation' and len(active)!=2 or phase=='constructor' and active or phase=='publication' and len(active)!=1:raise ValueError('main source stack boundary')


def verify_calls(case):
    calls=case['constructor']['platform_calls'];names=['InitializeCriticalSection']*2+['CreateEventA','GetCurrentDirectoryA','PathAddBackslashA']+['lstrcpyA']*7+['lstrcatA']
    if [r['name'] for r in calls]!=names:raise ValueError('main complete original system call order')
    original=SOURCE.read_bytes();directory=original[DIRECTORY-BASE:DIRECTORY-BASE+DIRECTORY_BYTES];paths={}
    cwd=case['hello']['working_directory'].encode('cp'+str(case['hello']['acp']))
    if cwd!=str(WORKDIR).encode('cp'+str(case['hello']['acp'])):raise ValueError('main actual declared ANSI cwd')
    for index,r in enumerate(calls):
        name=r['name'];slot=int(r['slot'],16);rule=IMPORTS[slot];result=r['result'];request=r['request']
        if rule[0]!=name or r['va']!=hex(dword(original,slot-BASE)) or int(r['return_va'],16) not in rule[3] or r['live_host_observed'] is not True:raise ValueError('main original API identity')
        if index<2:
            expected=[OWNER+(0x14 if index==0 else 0x164)];pointer,n=expected[0],24
            wanted_request=dict(index=index,before_hex='cd'*24)
            code=bytes.fromhex(result['forwarder_hex'])
            if len(bytes.fromhex(result['hex']))!=24 or len(code)!=19 or code[:7]!=bytes.fromhex('558becff7508b8') or code[11:]!=bytes.fromhex('ffd08be55dc20400') or not dword(code,7):raise ValueError('main real void call/full critical section capture')
            if result['native_return_type']!='void' or result['eax_is_status'] is not False or result['forwarder_freed'] is not True:raise ValueError('main void return authority')
            eax=result['eax_bits_observed']
            if type(eax) is not int or not 0<=eax<=0xFFFFFFFF:raise ValueError('main actual observed EAX bits')
        elif name=='CreateEventA':
            expected=[0,0,0,0];pointer,n=None,0;wanted_request=dict(args=expected);eax=result['result']
            if type(eax) is not int or not 0<eax<=0xFFFFFFFF:raise ValueError('main actual live event handle')
        elif name=='GetCurrentDirectoryA':
            expected=[DIRECTORY_BYTES,DIRECTORY];pointer,n=DIRECTORY,DIRECTORY_BYTES;wanted_request=dict(before_hex=directory.hex())
            wanted=bytearray(directory);wanted[:len(cwd)+1]=cwd+b'\0';directory=bytes(wanted)
            if result['result']!=len(cwd) or result['hex']!=directory.hex():raise ValueError('main actual ANSI cwd/full unmodified tail')
            eax=len(cwd)
        elif name=='PathAddBackslashA':
            expected=[DIRECTORY];pointer,n=DIRECTORY,DIRECTORY_BYTES;wanted_request=dict(before_hex=directory.hex())
            text=cwd if cwd.endswith(b'\\') else cwd+b'\\';wanted=bytearray(directory);wanted[:len(text)+1]=text+b'\0';directory=bytes(wanted)
            if result['hex']!=directory.hex() or result['return_offset']!=len(text):raise ValueError('main actual backslash/full preserved directory')
            eax=DIRECTORY+len(text)
        else:
            text=directory.split(b'\0',1)[0]+b'\0'
            if name=='lstrcpyA':
                j=index-5;offset=PATHS[j];expected=[OWNER+offset,DIRECTORY if j==0 else OWNER+0x9EC]
                before=bytes([0xCD if offset in (0xAF0,0xDFC) else 0])*260;source=text;after=bytearray(before);after[:len(source)]=source
            else:
                offset=0x1004;expected=[OWNER+offset,0x598694];before=paths[offset];source=b'SaveData\\\0';after=bytearray(before)
                after[len(text)-1:len(text)-1+len(source)]=source
            pointer,n=expected[0],260;wanted_request=dict(before_hex=before.hex(),source_hex=source.hex())
            if result['hex']!=bytes(after).hex() or result['return_offset']!=0 or result['source_unchanged'] is not True:raise ValueError('main full native ANSI destination/source bytes')
            paths[offset]=bytes(after);eax=pointer
        if n and result['guards_unchanged'] is not True:raise ValueError('main actual host buffer guards')
        if r['args']!=expected or request!=wanted_request or r['observed_EAX']!=eax or r['mapped_output_pointer']!=pointer or r['mapped_output_bytes']!=n:raise ValueError('main exact original system arguments/results')
    return calls


def verify_case(case,through='publication'):
    fill=case['fill'];initial_owner(fill);raw=SOURCE.read_bytes();prior=None;stack=bytearray(initial_stack(fill))
    replay_owner=bytearray(initial_owner(fill));replay_image=bytearray(raw);replay_seh=bytearray(4096)
    calls=verify_calls(case) if through!='allocation' else []
    if case['declared_initial_cpu']!=initial_cpu():raise ValueError('main explicit initial CPU')
    for phase in STOPS:
        row=case[phase];state=row['state'];verify_trace(row)
        before=initial_cpu() if prior is None else prior['cpu']
        cpu=dict(EIP=STOPS[phase],ESP=SP-4 if phase=='allocation' else SP,EBP=BP,EAX=OWNER,
            EBX=0x55667788,ECX=OWNER if phase!='constructor' else 0,EDX=SIZE if phase=='allocation' else OWNER,
            ESI=0x88776655,EDI=BP,EFLAGS=70 if phase=='constructor' else 6)
        if row['phase']!=phase or row['before_cpu']!=before or row['cpu']!=cpu:raise ValueError('main exact phase CPU continuity')
        expected_pending=dict(va=hex(STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='allocation':expected_pending.update(return_va='0x49ddec',receiver=OWNER,args=[])
        else:expected_pending['stack_top_dword']=0x44332211
        if row['pending']!=expected_pending:raise ValueError('main caller versus callee pending semantics')
        alloc=source_contract()['allocator']
        expected_alloc=[dict(va='0x56e810',return_va='0x428a73',sp=SP-112,args=[SIZE,1,alloc['file'],alloc['line']],pointer=OWNER,
            bytes=SIZE,initial_byte=0xCD,adapter='declared debug CRT allocation')]
        if row['allocations']!=expected_alloc:raise ValueError('main exact original CRT request/response')
        if phase=='constructor':
            if [int(e['va'],16) for e in row['entries']]!=CONSTRUCTOR_SEQUENCE:raise ValueError('main all26 original constructor calls')
            clears={0x439D3D:(OWNER+0x2C,0,8),0x426142:(OWNER+0x6A8,0,256),0x4261C2:(OWNER+0x5A8,0,256),0x42627F:(OWNER+0x7BC,0,64),
                0x44FC7A:(OWNER+0x8D4,0,12),0x44FC92:(OWNER+0x9EC,0,260),0x44FCAB:(OWNER+0xBF4,0,260),
                0x44FCC4:(OWNER+0xCF8,0,260),0x44FCDC:(OWNER+0xF00,0,260),0x44FCF5:(OWNER+0x1004,0,260),0x429749:(DIRECTORY,525,0)}
            offsets={0x439D10:0x10,0x424670:0,0x429310:0x34,0x423480:0x34,0x421540:0x64,0x425780:0x180,
                0x425800:0x180,0x426110:0x180,0x426190:0x180,0x426250:0x180,0x428B90:0x8CC,0x429540:0x34,0x429720:0x34}
            for e in row['entries']:
                va=int(e['va'],16)
                if va==0x56CEC0 and e['args']!=list(clears[int(e['return_va'],16)]):raise ValueError('main exact original memset ranges/zero length')
                if va in offsets and e['receiver']!=OWNER+offsets[va]:raise ValueError('main actual native subobject receiver')
                if va==0x4297A0 and e['args']!=[DIRECTORY]:raise ValueError('main actual original path call')
        elif row['platform_calls']:raise ValueError('main unexpected platform calls outside constructor')
        owner=initial_owner(fill) if phase=='allocation' else project_constructor(initial_owner(fill),calls)
        image=project_image(phase,calls)
        verify_buffer(state['owner'],owner);verify_buffer(state['guarded_owner'],bytes([fill])*4096+owner+bytes([fill])*4096)
        verify_buffer(state['null_page'],bytes(4096));verify_buffer(state['directory'],image[DIRECTORY-BASE:DIRECTORY-BASE+DIRECTORY_BYTES])
        expected_global=OWNER if phase=='publication' else dword(raw,GLOBAL-BASE)
        if state['image_sha256']!=sha(image) or state['SEH']!=0 or state['global_value']!=expected_global or state['counter']!=SIZE:raise ValueError('main complete source image/global/counter/SEH')
        foreign={}
        for slot in IMPORTS:
            target=dword(raw,slot-BASE);foreign.setdefault(target&~4095,bytearray(4096))[target%4096]=0xC3
        if [r['pointer'] for r in state['foreign_maps']]!=sorted(foreign):raise ValueError('main exact import map set')
        for r in state['foreign_maps']:verify_buffer({k:v for k,v in r.items() if k!='pointer'},foreign[r['pointer']])
        valid={r['va'] for r in row['instruction_runs']};expected_writes=Counter();code=instructions()
        for run in row['instruction_runs']:
            i=code[run['va']]
            if i.mnemonic.startswith('rep stos'):expected_writes[i.address]+=run['count']-1
            elif i.mnemonic in ('push','call') or i.mnemonic in ('mov','add','sub','and','or','xor','inc','dec') and '[' in i.op_str.split(',')[0]:expected_writes[i.address]+=1
        if +Counter(w['pc'] for w in row['native_writes'])!=+expected_writes:raise ValueError('main exact source instruction write multiplicity')
        for w in row['native_writes']:
            pc,p,n,value=w['pc'],w['pointer'],w['bytes'],w['value']
            if pc not in valid or type(n) is not int or n not in (1,2,4,8) or not 0<=value<1<<(n*8):raise ValueError('main bounded original memory write')
            if code[pc].mnemonic=='call' and (n!=4 or value!=pc+code[pc].size):raise ValueError('main original call return-address store')
            if STACK<=p and p+n<=STACK+65536:
                if not SP-1024<=p or p+n>BP:raise ValueError('main exact owned stack write range')
                stack[p-STACK:p-STACK+n]=value.to_bytes(n,'little')
            elif p==0 and n==4:
                if phase!='constructor' or pc not in (0x44FBC1,0x44FE3C):raise ValueError('main exact native SEH stores')
                replay_seh[:4]=value.to_bytes(4,'little')
            elif phase=='allocation' and p==COUNTER and n==4:
                if (pc,value) not in ((0x4288F8,0),(0x428A82,SIZE)):raise ValueError('main original allocation counter stores')
                store(replay_image,p-BASE,value)
            elif phase=='constructor' and OWNER<=p and p+n<=OWNER+SIZE:replay_owner[p-OWNER:p-OWNER+n]=value.to_bytes(n,'little')
            elif phase=='publication' and (pc,p,n,value)==(0x49DE01,GLOBAL,4,OWNER):store(replay_image,p-BASE,value)
            else:raise ValueError('main source write ownership')
        for call in row['platform_calls']:
            p,n=call['mapped_output_pointer'],call['mapped_output_bytes']
            if not n:continue
            output=bytes.fromhex(call['result']['hex'])
            if OWNER<=p and p+n<=OWNER+SIZE:replay_owner[p-OWNER:p-OWNER+n]=output
            elif p==DIRECTORY and n==DIRECTORY_BYTES:replay_image[p-BASE:p-BASE+n]=output
            else:raise ValueError('main owned exact system output region')
        if replay_owner!=owner or replay_image!=image or replay_seh!=bytes(4096):raise ValueError('main complete source-write/API replay agrees with independent projections')
        verify_buffer(state['stack'],stack)
        if dword(stack,BP-STACK)!=0x11223344 or dword(stack,SP-STACK)!=0x44332211 or dword(stack,SP+4-STACK)!=0x88776655 or dword(stack,SP+8-STACK)!=0x55667788:raise ValueError('main declared parent frame preserved')
        if phase=='publication' and sum(w['pointer']==GLOBAL for w in row['native_writes'])!=1:raise ValueError('main one original global publication')
        if row['original_global_published']!=(phase=='publication') or row['retained_VM_advanced'] is not False or row['full_WinMain_executed'] is not False:raise ValueError('main honest experiment authority')
        prior=row
        if phase==through:return


def verify_report(report,through='publication'):
    if report['source_contract']!=source_contract() or len(report['cases'])!=2 or [c['fill'] for c in report['cases']]!=[0xA5,0xCC]:raise ValueError('main complete source/input cases')
    expected_build=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))
    pinned=json.loads((ROOT/'analysis/school-main-context-platform-v1-20261019.json').read_text(encoding='utf8'))
    if report['platform_build']!=expected_build or expected_build!=pinned['build']:raise ValueError('main actual owned helper provenance')
    for c in report['cases']:
        if c['system_modules']!=pinned['system_modules'] or c['hello']!=pinned['hello']:raise ValueError('main real system/hello provenance')
        for r in c['system_modules'].values():
            if machine(r['path'])!=0x14C or sha(Path(r['path']).read_bytes())!=r['sha256']:raise ValueError('main actual system module bytes')
        verify_case(c,through)
        requests=c['constructor']['platform_calls'];trace=c['platform_trace']
        cleanup=dict(critical_sections_deleted=2,event_handles_closed=1,all_owned_resources_released=True)
        expected=[dict(request=dict(id=i+1,op=r['name'],**r['request']),reply=dict(ok=True,id=i+1,result=r['result'])) for i,r in enumerate(requests)]
        expected.append(dict(request=dict(id=len(requests)+1,op='close'),reply=dict(ok=True,id=len(requests)+1,result=cleanup)))
        if trace!=expected or c['platform_cleanup']!=cleanup:raise ValueError('main complete owned helper protocol/cleanup')
    for k,v in dict(one_continuous_CPU_per_case=True,declared_mid_WinMain_frame=True,WinMain_prelude_executed=False,
            original_IAT_changed=False,game_helpers_stubbed=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False).items():
        if report[k] is not v:raise ValueError('main report scope authority')
    return dict(cases=2,verified_through=through,allocation_bytes=SIZE,constructor_calls_per_case=26,
        real_system_calls_per_case=13,original_publication_verified=through=='publication',retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--through',choices=list(STOPS),default='publication');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')),a.through),indent=2))
