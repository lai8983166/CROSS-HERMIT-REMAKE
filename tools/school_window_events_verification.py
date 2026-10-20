"""Independent original-code replay through real size/move/show/WINDOWPOS callbacks."""
import argparse
import copy
import json
from pathlib import Path
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_MEM_READ
from tools.school_window_events import *
from tools.school_window_class_verification import verify_case as verify_prefix,maps as class_maps
from tools.school_window_callback_verification import expected_maps,check_maps
from tools.school_window_module_validation import digest
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_renderer_init_verification import verify_buffer
from tools.school_device_init_verification import unpack
from tools.school_window_events_platform import SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine
from tools.school_window_module import RESOURCE_DLL,inspect_module


def replay_callback(c,n,index,owner,image,native_stack,caller):
    packet=n['setup']['packet'];message=MESSAGES[index];module=c['module_input']['value'];data=bytes.fromhex(packet['data_hex'])
    if set(packet)!={'event_kind','callback_id','depth','guest_entry','hwnd','message','wParam','lParam','data_kind','data_hex'} or packet['event_kind']!='wndproc' or packet['callback_id']!=index+1 or packet['depth']!=1 or packet['guest_entry']!=ENTRY or packet['message']!=message or packet['wParam']!=(1 if message==24 else 0) or type(packet['lParam']) is not int or not (65536 if message in (129,131,1,70) else 0)<=packet['lParam']<=0xFFFFFFFF:
        raise ValueError('events actual callback identity/order/ABI')
    hwnd=c['callbacks'][0]['setup']['packet']['hwnd']
    if packet['hwnd']!=hwnd or not 0<hwnd<=0xFFFFFFFF:raise ValueError('events actual owned window identity')
    if message in (129,1):
        if packet['data_kind']!='CREATESTRUCTA' or len(data)!=48 or struct.unpack('<12I',data)[:9]!=(parent.OWNER,module,0,0,768,1024,16,16,geometry.STYLE) or dword(data,44)!=0 or not all(65536<=dword(data,o)<=0xFFFFFFFF for o in (36,40)):
            raise ValueError('events exact native CREATESTRUCT/source inputs')
    elif message==131:
        if packet['data_kind']!='RECT' or base.rectangle(data,packet['wParam'])!=[16,16,1040,784]:raise ValueError('events native client input RECT')
    elif message in (5,3,24):
        if packet['data_kind']!='opaque' or data:raise ValueError('events exact scalar packet')
        expected={5:dict(width=1024,height=768,size_state=0),3:dict(x=16,y=16),24:dict(shown=True,reason=0)}[message]
        if scalar(message,packet['wParam'],packet['lParam'])!=expected:raise ValueError('events actual scalar semantics')
    elif message==70:
        fields=windowpos(data,hwnd)
        if packet['data_kind']!='WINDOWPOS' or any(fields[k]!=0 for k in ('x','y','cx','cy')) or fields['flags']!=0x43:raise ValueError('events actual WINDOWPOS entry')
    stack,args=callback_stack(packet);shadow=bytearray(b'\xda'*12288)
    if message==129:shadow[4096:4144]=data
    setup=dict(packet=packet,cpu=callback_cpu(),args=args,stack=buffer_evidence(stack),guarded_shadow=buffer_evidence(shadow),declared_ABI_not_host_register_capture=True)
    if n['setup']!=setup or n['suspended_caller_cpu']!=caller or n['restored_caller_cpu']!=caller:raise ValueError('events declared frame or suspended CPU changed')
    verify_buffer(n['guarded_owner_before'],owner)
    raw=SOURCE.read_bytes();u=Uc(UC_ARCH_X86,UC_MODE_32)
    for at,size,b in ((BASE,(len(image)+4095)&~4095,bytes(image)),(parent.OWNER-4096,len(owner),owner),(STACK,65536,stack),
            (SHADOW-4096,12288,bytes(shadow)),(RETURN,4096,b'\xda'*4096),(parent.STACK,65536,bytes(native_stack))):
        u.mem_map(at,size);u.mem_write(at,b)
    for p,b in expected_maps().items():u.mem_map(p,4096);u.mem_write(p,bytes(b))
    for k,v in callback_cpu().items():u.reg_write(REGISTERS[k],v)
    code={i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}
    runs=[];reads=[];writes=[];returns=[];calls=iter(n['platform_calls']);seen=[]
    def word(p):return struct.unpack('<I',bytes(u.mem_read(p,4)))[0]
    def access(uc,kind,at,size,value,user):
        pc=uc.reg_read(REGISTERS['EIP'])
        if kind==UC_MEM_READ:
            if not any(a<=at and at+size<=b for a,b in ((BASE,BASE+len(image)),(parent.OWNER,parent.OWNER+parent.BACKING),(STACK,STACK+65536),(SHADOW-4096,SHADOW+8192))):raise ValueError('events replay uncaptured memory read')
            reads.append(dict(pc=pc,pointer=at,bytes=size,hex=bytes(uc.mem_read(at,size)).hex()))
        else:
            if not (STACK<=at and at+size<=STACK+65536 or at in (parent.OWNER+4,parent.OWNER+12) and size==4):raise ValueError('events replay unowned write')
            writes.append(dict(pc=pc,pointer=at,bytes=size,value=value&((1<<(size*8))-1)))
    def instruction(uc,at,size,user):
        if at==RETURN:uc.emu_stop();return
        sp=uc.reg_read(REGISTERS['ESP']);slots=[s for s in IMPORTS if at==dword(raw,s-BASE)]
        if slots:
            slot=slots[0];name,count=IMPORTS[slot];a=[word(sp+4+i*4) for i in range(count)]
            try:call=next(calls)
            except StopIteration:raise ValueError('events missing native response')
            request=dict(callback_id=index+1);r=call['result'];value=r['result']
            if name in ('GetPropA','SetPropA'):
                if a[:2]!=[hwnd,0x594AB4] or bytes(uc.mem_read(a[1],10))!=PROPERTY:raise ValueError('events source property ABI')
                op='get_prop' if name=='GetPropA' else 'set_prop';request.update(hwnd=hwnd,name_hex=PROPERTY.hex())
                expected_r=dict(result=value,last_error=r['last_error'],name_unchanged=True,guards_unchanged=True)
                if type(r['last_error']) is not int:raise ValueError('events property actual LastError bits')
                if name=='GetPropA':
                    if value!=(0 if message==129 else parent.OWNER):raise ValueError('events actual existing property owner')
                else:
                    if message!=129 or a[2]!=parent.OWNER or value!=1:raise ValueError('events unexpected rebinding')
                    request['data']=parent.OWNER;expected_r.update(observed_property=parent.OWNER,auxiliary_readback=True)
            elif name=='GetWindowLongA':
                if message!=129 or a[0]!=hwnd or a[1] not in (4,0xFFFFFFFC):raise ValueError('events unexpected window procedure change')
                op='get_window_long';request.update(hwnd=hwnd,index=a[1]);host=c['registered']['platform_calls'][0]['result']['pointer_translations'][0]['host']
                translated=a[1]==0xFFFFFFFC;expected_r=dict(result=ENTRY if translated else 0,host_result=host if translated else 0,
                    last_error=r['last_error'],reverse_translated=translated,owned_host_callback=host,guest_callback=ENTRY)
            else:
                if message in (1,5):raise ValueError('original WM_CREATE/SIZE must not call default procedure')
                op='default_window';request['args']=a
                if a!=args or value!=(1 if message==129 else 0):raise ValueError('events actual native default ABI/result')
                expected_r=dict(result=value,host_args=[hwnd,message,packet['wParam'],packet['lParam']],lparam_reverse_translated=message==129,before_hex=data.hex(),after_hex=data.hex())
            expected_call=dict(name=name,op=op,slot=hex(slot),va=hex(at),sp=sp,return_va=hex(word(sp)),args=a,request=request,result=expected_r,observed_EAX=value,live_host_observed=True)
            if call!=expected_call:raise ValueError('events complete native response/real data/procedure identity')
            seen.append(call);uc.reg_write(REGISTERS['EAX'],value);uc.reg_write(REGISTERS['EIP'],word(sp));uc.reg_write(REGISTERS['ESP'],sp+4+count*4);return
        i=code.get(at)
        if i is None or i.size!=size:raise ValueError('events replay outside original code')
        if runs and runs[-1]['va']==at:runs[-1]['count']+=1
        else:runs.append(dict(va=at,count=1))
        if i.mnemonic=='ret':returns.append(dict(va=hex(at),return_va=hex(word(sp)),sp=sp,eax=uc.reg_read(REGISTERS['EAX'])))
    u.hook_add(UC_HOOK_CODE,instruction);u.hook_add(UC_HOOK_MEM_READ,access);u.hook_add(UC_HOOK_MEM_WRITE,access)
    u.emu_start(ENTRY,RETURN+1,count=100000,timeout=20_000_000)
    names=['GetPropA','GetWindowLongA','SetPropA','GetWindowLongA','DefWindowProcA'] if message==129 else ['GetPropA','DefWindowProcA'] if message not in (1,5,129) else ['GetPropA']
    if next(calls,None) is not None or [a['name'] for a in seen]!=names:raise ValueError('events exact original native API sequence')
    result=1 if message==129 else 0
    if n['instruction_runs']!=runs or n['native_reads']!=reads or n['native_writes']!=writes or n['native_returns']!=returns or n['cpu']!={k:u.reg_read(r) for k,r in REGISTERS.items()} or n['result']!=result or n['original_callback_executed'] is not True:
        raise ValueError('events independent full original instruction/access/CPU replay')
    if any(r['pointer']<=0x7A49FC<r['pointer']+r['bytes'] for r in reads):raise ValueError('events callback read captured game dependency')
    if message!=129 and any(r['va']==0x4249D1 or r['va']==0x424730 for r in runs):raise ValueError('events bound path unexpectedly dereferences/rebinds creation this')
    wanted=bytearray(owner)
    if message==129:store(wanted,4096+4,hwnd);store(wanted,4096+12,0)
    actual_owner=bytes(u.mem_read(parent.OWNER-4096,len(owner)))
    if actual_owner!=wanted:raise ValueError('events unexpected original owner/guard writes')
    state=dict(guarded_owner=buffer_evidence(actual_owner),callback_stack=buffer_evidence(bytes(u.mem_read(STACK,65536))),guarded_shadow=buffer_evidence(shadow),
        native_stack=buffer_evidence(native_stack),image_sha256=hashlib.sha256(image).hexdigest())
    if n['state']!=state:raise ValueError('events full owner/stack/shadow/source/caller preservation')
    if bytes(u.mem_read(BASE,len(image)))!=image or bytes(u.mem_read(parent.STACK,65536))!=native_stack:raise ValueError('events independent source/native stack preservation')
    return actual_owner,dict(message=message,instructions=sum(r['count'] for r in runs),reads=len(reads),writes=len(writes),native_APIs=len(seen),result=result,
        actual_HWND=hwnd,bound_property_reused=message!=129,source_binding_repeated=False,captured_game_global_read=False)


def verify_case(c):
    before=digest(c);prefix=verify_prefix(c);old=c['create_ready'];creation=c['creation'];module=c['module_input']['value'];raw=SOURCE.read_bytes()
    a=creation['import_admission'];expected=dict(slots=[hex(s) for s in (CREATE_SLOT,*IMPORTS)],before_cpu=old['cpu'],after_cpu=old['cpu'],
        owner_sha256=old['state']['guarded_owner']['sha256'],stack_sha256=old['state']['stack']['sha256'],image_sha256=old['state']['image_sha256'],
        foreign_before=old['state']['foreign_maps'],foreign_after=a['foreign_after'],declared_maps=[dict(pointer=p,bytes=n,initial_byte=0xDA) for p,n in ((STACK,65536),(RETURN,4096),(SHADOW-4096,12288))])
    if a!=expected:raise ValueError('events pending state changed at import admission')
    check_maps(a['foreign_before'],class_maps());check_maps(a['foreign_after'],expected_maps())
    cpu=dict(old['cpu']);cpu.update(EIP=dword(raw,CREATE_SLOT-BASE),ESP=old['cpu']['ESP']-4)
    native_stack=bytearray(unpack(old['state']['stack']));store(native_stack,cpu['ESP']-parent.STACK,0x4504D5)
    if creation!=dict(import_admission=a,cpu=cpu,instruction_runs=[dict(va=CREATE,count=1)],native_writes=[dict(pc=CREATE,pointer=cpu['ESP'],bytes=4,value=0x4504D5)],
            sp=cpu['ESP'],args=base.callback.previous.creation_args(module),return_va='0x4504d5',native_stack=buffer_evidence(native_stack)):raise ValueError('events original native call/arguments/stack')
    image=bytearray(window.project_image(parent.project_image('publication',c['constructor']['platform_calls']),'branch'));store(image,window.INSTANCE-BASE,module)
    if hashlib.sha256(image).hexdigest()!=old['state']['image_sha256']:raise ValueError('events actual raw source projection')
    if len(c['callbacks'])!=len(MESSAGES):raise ValueError('events exact seven completed callbacks')
    owner=unpack(old['state']['guarded_owner']);proofs=[]
    for i,n in enumerate(c['callbacks']):owner,p=replay_callback(c,n,i,owner,image,native_stack,cpu);proofs.append(p)
    verify_buffer(c['final_guarded_owner'],owner)
    if c['final_image_sha256']!=old['state']['image_sha256']:raise ValueError('events final image/captured globals modified')
    pending=c['pending_callback'];p=pending['packet'];hwnd=proofs[0]['actual_HWND']
    entry=c['callbacks'][-1]['setup']['packet'];fields=windowpos(bytes.fromhex(p['data_hex']),hwnd)
    previous=windowpos(bytes.fromhex(entry['data_hex']),hwnd);previous['flags']=3
    if fields!=previous or p!=dict(event_kind='wndproc',callback_id=8,depth=1,guest_entry=ENTRY,hwnd=hwnd,message=70,wParam=0,lParam=entry['lParam'],data_kind='WINDOWPOS',data_hex=p['data_hex']):raise ValueError('events exact next WINDOWPOS3/identity')
    stack,args=callback_stack(p)
    if pending!=dict(packet=p,cpu=callback_cpu(),args=args,stack=buffer_evidence(stack),guarded_shadow=buffer_evidence(b'\xda'*12288),declared_ABI_not_host_register_capture=True):raise ValueError('events exact unanswered next callback frame')
    if before!=digest(c):raise ValueError('events verifier mutated raw evidence')
    return dict(callbacks=proofs,prefix_substitutions=len(prefix['prefix']['substitutions']),pending_message=70,pending_WINDOWPOS_flags=3,raw_evidence_modified=False)


def verify_report(report):
    if report['source_contract']!=source_contract() or [c['fill'] for c in report['cases']]!=[0xA5,0xCC]:raise ValueError('events actual source/two inputs')
    pin=json.loads((ROOT/'analysis/school-window-events-platform-v1-20261020.json').read_text(encoding='utf8'))
    build=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))
    if build!=pin['build'] or report['platform_build']!=build or inspect_module(RESOURCE_DLL.read_bytes())['sha256']!=pin['hello']['resource_module']['sha256']:raise ValueError('events actual immutable helper/resource')
    proofs=[]
    for c in report['cases']:
        h=copy.deepcopy(c['hello']);h['resource_module']['pointer']=pin['hello']['resource_module']['pointer']
        if h!=pin['hello'] or c['system_modules']!=pin['system_modules']:raise ValueError('events actual loaded module provenance')
        for r in c['system_modules'].values():
            if machine(r['path'])!=0x14C or sha(Path(r['path']).read_bytes())!=r['sha256']:raise ValueError('events actual x86 system modules')
        proofs.append(verify_case(c));calls=sum([c[p]['platform_calls'] for p in ('constructor','query','rect','adjust','icons','class_ready','registered')],[])
        trace=[dict(request=dict(id=i+1,op=a.get('op',a['name']),**a['request']),reply=dict(ok=True,id=i+1,result=a['result'])) for i,a in enumerate(calls)];wire=[]
        for row in trace:wire.extend([dict(direction='request',value=row['request']),dict(direction='response',value=row['reply'])])
        seq=len(trace)+1;wire.append(dict(direction='request',value=dict(id=seq,op='create_window',args=c['creation']['args'])))
        for n in c['callbacks']:
            p=n['setup']['packet'];wire.append(dict(direction='response',value=p))
            for a in n['platform_calls']:
                seq+=1;row=dict(request=dict(id=seq,op=a['op'],**a['request']),reply=dict(ok=True,id=seq,result=a['result']));trace.append(row)
                wire.extend([dict(direction='request',value=row['request']),dict(direction='response',value=row['reply'])])
            wire.append(dict(direction='callback_return',value=dict(op='callback_return',callback_id=p['callback_id'],result=n['result'])))
        wire.append(dict(direction='response',value=c['pending_callback']['packet']))
        if c['wire']!=wire or c['platform_trace']!=trace:raise ValueError('events exact nested protocol/three real callback returns/no pending answer')
        abort=c['platform_abort'];expected=dict(owned_process_exited=True,exit_code=abort['exit_code'],reason=STOP_REASON,pending_callback=c['pending_callback']['packet'],
            unanswered=True,explicit_cleanup_performed=False,CreateWindowExA_return_received=False,normal_class_unregistration_performed=False)
        if abort!=expected or type(abort['exit_code']) is not int or abort['exit_code']==0 or c['platform_cleanup'] is not None:raise ValueError('events honest ended lifetime/pending native call')
    for key,value in dict(one_original_CPU_per_case=True,original_callback_executed=True,WM_SIZE_MOVE_SHOW_WINDOWPOS_completed=True,
            CreateWindowExA_return_received=False,HWND_global_published=False,original_IAT_modified=False,game_helpers_stubbed=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False).items():
        if report[key] is not value:raise ValueError('events report authority')
    return dict(cases=2,completed_messages=list(MESSAGES),pending_message=70,pending_WINDOWPOS_flags=3,pending_guest_EIP=hex(ENTRY),creation_return_pending=True,
        case_proofs=proofs,explicit_normal_cleanup=False,owned_processes_exited=True,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8'))),indent=2))
