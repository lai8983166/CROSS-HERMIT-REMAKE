"""Independent original-code replay of callback ABI, accesses and live API observations."""
import argparse
import copy
import json
from pathlib import Path
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_MEM_READ
from tools.school_window_callback import *
from tools.school_window_class_verification import verify_case as verify_prefix,maps as class_maps
from tools.school_window_module_validation import digest
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_renderer_init_verification import verify_buffer
from tools.school_device_init_verification import unpack
from tools.school_window_callback_platform import SOURCE as PLATFORM_SOURCE,HELPER,COMPILER,sha,machine
from tools.school_window_module import RESOURCE_DLL,inspect_module


def expected_maps():
    result=class_maps();raw=SOURCE.read_bytes()
    for slot in (CREATE_SLOT,*IMPORTS):
        target=dword(raw,slot-BASE);result.setdefault(target&~4095,bytearray(4096))[target%4096]=0xC3
    return result


def check_maps(rows,expected):
    if [r['pointer'] for r in rows]!=sorted(expected):raise ValueError('callback exact import maps')
    for r in rows:verify_buffer({k:v for k,v in r.items() if k!='pointer'},expected[r['pointer']])


def verify_case(c):
    before_digest=digest(c);prefix=verify_prefix(c);old=c['create_ready'];creation=c['creation'];module=c['module_input']['value'];raw=SOURCE.read_bytes()
    admission=creation['import_admission'];expected=dict(slots=[hex(s) for s in (CREATE_SLOT,*IMPORTS)],before_cpu=old['cpu'],after_cpu=old['cpu'],
        owner_sha256=old['state']['guarded_owner']['sha256'],stack_sha256=old['state']['stack']['sha256'],image_sha256=old['state']['image_sha256'],
        foreign_before=old['state']['foreign_maps'],foreign_after=admission['foreign_after'],
        declared_maps=[dict(pointer=p,bytes=n,initial_byte=0xDA) for p,n in ((STACK,65536),(RETURN,4096),(SHADOW-4096,12288))])
    if admission!=expected:raise ValueError('callback import/frame admission modifies retained state')
    check_maps(admission['foreign_before'],class_maps());check_maps(admission['foreign_after'],expected_maps())
    cpu=dict(old['cpu']);cpu.update(EIP=dword(raw,CREATE_SLOT-BASE),ESP=old['cpu']['ESP']-4)
    native_stack=bytearray(unpack(old['state']['stack']));store(native_stack,cpu['ESP']-parent.STACK,0x4504D5)
    expected=dict(import_admission=admission,cpu=cpu,instruction_runs=[dict(va=CREATE,count=1)],
        native_writes=[dict(pc=CREATE,pointer=cpu['ESP'],bytes=4,value=0x4504D5)],sp=cpu['ESP'],args=previous.creation_args(module),return_va='0x4504d5',native_stack=buffer_evidence(native_stack))
    if creation!=expected:raise ValueError('callback original creation call push/ABI/full native stack')
    if len(c['callbacks'])!=1:raise ValueError('observed bounded trajectory has one completed original WM_NCCREATE')
    n=c['callbacks'][0];packet=n['setup']['packet'];pending=c['pending_callback'];next_packet=pending['packet']
    if packet['message']!=129 or packet['callback_id']!=1 or next_packet['message']!=131 or next_packet['callback_id']!=2 or packet['hwnd']!=next_packet['hwnd']:
        raise ValueError('callback actual observed creation message order/identity')
    for p in (packet,next_packet):
        if set(p)!={'event_kind','callback_id','depth','guest_entry','hwnd','message','wParam','lParam','data_kind','data_hex'} or p['event_kind']!='wndproc' or p['depth']!=1 or p['guest_entry']!=ENTRY or not 0<p['hwnd']<=0xFFFFFFFF or not 65536<=p['lParam']<=0xFFFFFFFF or p['wParam']!=0:
            raise ValueError('callback genuine packet ABI')
    data=bytes.fromhex(packet['data_hex'])
    if packet['data_kind']!='CREATESTRUCTA' or len(data)!=48 or struct.unpack('<12I',data)[:9]!=(parent.OWNER,module,0,0,768,1024,16,16,geometry.STYLE) or dword(data,44)!=0:
        raise ValueError('callback actual CREATESTRUCT source call identity')
    if not all(65536<=dword(data,o)<=0xFFFFFFFF for o in (36,40)) or next_packet['data_kind']!='opaque' or next_packet['data_hex']!='':raise ValueError('callback actual opaque creation string/pending data')
    # Independent VM has no live-helper orchestration, subclass hooks or generator methods.
    image=bytearray(window.project_image(parent.project_image('publication',c['constructor']['platform_calls']),'branch'));store(image,window.INSTANCE-BASE,module)
    if hashlib.sha256(image).hexdigest()!=old['state']['image_sha256']:raise ValueError('callback full actual source projection')
    owner=unpack(old['state']['guarded_owner']);stack,args=callback_stack(packet);shadow=bytearray(b'\xda'*12288);shadow[4096:4144]=data
    setup=dict(packet=packet,cpu=callback_cpu(),args=args,stack=buffer_evidence(stack),guarded_shadow=buffer_evidence(shadow),declared_ABI_not_host_register_capture=True)
    if n['setup']!=setup or n['suspended_caller_cpu']!=cpu or n['restored_caller_cpu']!=cpu:raise ValueError('callback declared frame/suspended CPU restoration')
    verify_buffer(n['guarded_owner_before'],owner)
    u=Uc(UC_ARCH_X86,UC_MODE_32)
    for at,size,b in ((BASE,(len(image)+4095)&~4095,bytes(image)),(parent.OWNER-4096,len(owner),owner),(STACK,65536,stack),
            (SHADOW-4096,12288,bytes(shadow)),(RETURN,4096,b'\xda'*4096),(parent.STACK,65536,bytes(native_stack))):
        u.mem_map(at,size);u.mem_write(at,b)
    for p,b in expected_maps().items():u.mem_map(p,4096);u.mem_write(p,bytes(b))
    for k,v in callback_cpu().items():u.reg_write(REGISTERS[k],v)
    code={i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}
    runs=[];reads=[];writes=[];returns=[];calls=iter(n['platform_calls']);seen=[]
    def word(p):return struct.unpack('<I',bytes(u.mem_read(p,4)))[0]
    def on_access(uc,access,at,size,value,user):
        pc=uc.reg_read(REGISTERS['EIP'])
        if access==UC_MEM_READ:
            if not any(a<=at and at+size<=b for a,b in ((BASE,BASE+len(image)),(parent.OWNER,parent.OWNER+parent.BACKING),(STACK,STACK+65536),(SHADOW-4096,SHADOW+8192))):raise ValueError('callback replay foreign heap read')
            reads.append(dict(pc=pc,pointer=at,bytes=size,hex=bytes(uc.mem_read(at,size)).hex()))
        else:
            if not (STACK<=at and at+size<=STACK+65536 or at in (parent.OWNER+4,parent.OWNER+12) and size==4):raise ValueError('callback replay unowned write')
            writes.append(dict(pc=pc,pointer=at,bytes=size,value=value&((1<<(size*8))-1)))
    def on_code(uc,at,size,user):
        if at==RETURN:uc.emu_stop();return
        sp=uc.reg_read(REGISTERS['ESP'])
        slots=[s for s in IMPORTS if at==dword(raw,s-BASE)]
        if slots:
            slot=slots[0];name,count=IMPORTS[slot];a=[word(sp+4+i*4) for i in range(count)]
            try:call=next(calls)
            except StopIteration:raise ValueError('callback missing live API response')
            request=dict(callback_id=1);r=call['result'];value=r['result'];h=packet['hwnd']
            if name in ('GetPropA','SetPropA'):
                if a[:2]!=[h,0x594AB4] or bytes(uc.mem_read(a[1],10))!=PROPERTY:raise ValueError('callback replay source property ABI')
                op='get_prop' if name=='GetPropA' else 'set_prop';request.update(hwnd=h,name_hex=PROPERTY.hex())
                expected_r=dict(result=value,last_error=r['last_error'],name_unchanged=True,guards_unchanged=True)
                if name=='GetPropA':
                    if value!=0:raise ValueError('callback genuine initial property absence')
                else:
                    if a[2]!=parent.OWNER or value!=1:raise ValueError('callback real property binding')
                    request['data']=parent.OWNER;expected_r.update(observed_property=parent.OWNER,auxiliary_readback=True)
            elif name=='GetWindowLongA':
                op='get_window_long';request.update(hwnd=h,index=a[1]);host=c['registered']['platform_calls'][0]['result']['pointer_translations'][0]['host']
                if a[0]!=h or a[1] not in (4,0xFFFFFFFC):raise ValueError('callback replay source window-long ABI')
                translated=a[1]==0xFFFFFFFC;expected_r=dict(result=ENTRY if translated else 0,host_result=host if translated else 0,
                    last_error=r['last_error'],reverse_translated=translated,owned_host_callback=host,guest_callback=ENTRY)
            else:
                op='default_window';request['args']=a
                if a!=[h,129,0,SHADOW] or value!=1:raise ValueError('callback actual default LRESULT/ABI')
                expected_r=dict(result=1,host_args=[h,129,0,packet['lParam']],lparam_reverse_translated=True,before_hex=data.hex(),after_hex=data.hex())
            expected_call=dict(name=name,op=op,slot=hex(slot),va=hex(at),sp=sp,return_va=hex(word(sp)),args=a,request=request,result=expected_r,observed_EAX=value,live_host_observed=True)
            if call!=expected_call:raise ValueError('callback exact real API/source ABI/procedure identity')
            seen.append(call);uc.reg_write(REGISTERS['EAX'],value);uc.reg_write(REGISTERS['EIP'],word(sp));uc.reg_write(REGISTERS['ESP'],sp+4+count*4);return
        i=code.get(at)
        if i is None or i.size!=size:raise ValueError('callback replay outside original functions')
        if runs and runs[-1]['va']==at:runs[-1]['count']+=1
        else:runs.append(dict(va=at,count=1))
        if i.mnemonic=='ret':returns.append(dict(va=hex(at),return_va=hex(word(sp)),sp=sp,eax=uc.reg_read(REGISTERS['EAX'])))
    u.hook_add(UC_HOOK_CODE,on_code);u.hook_add(UC_HOOK_MEM_READ,on_access);u.hook_add(UC_HOOK_MEM_WRITE,on_access)
    u.emu_start(ENTRY,RETURN+1,count=100000,timeout=20_000_000)
    if next(calls,None) is not None or [a['name'] for a in seen]!=['GetPropA','GetWindowLongA','SetPropA','GetWindowLongA','DefWindowProcA']:raise ValueError('callback exact native API call sequence')
    if n['instruction_runs']!=runs or n['native_reads']!=reads or n['native_writes']!=writes or n['native_returns']!=returns or n['cpu']!={k:u.reg_read(r) for k,r in REGISTERS.items()} or n['result']!=1 or n['original_callback_executed'] is not True:
        raise ValueError('callback independent full original instruction/access/register replay')
    if any(row['pointer']<=0x7A49FC<row['pointer']+row['bytes'] for row in reads):raise ValueError('callback unexpectedly reads captured game dependency')
    verify_buffer(n['state']['guarded_owner'],bytes(u.mem_read(parent.OWNER-4096,len(owner))))
    verify_buffer(n['state']['callback_stack'],bytes(u.mem_read(STACK,65536)));verify_buffer(n['state']['guarded_shadow'],bytes(shadow));verify_buffer(n['state']['native_stack'],native_stack)
    if n['state']['image_sha256']!=hashlib.sha256(image).hexdigest():raise ValueError('callback preserved complete source image')
    desired=bytearray(owner);store(desired,4096+4,packet['hwnd']);store(desired,4096+12,0)
    verify_buffer(n['state']['guarded_owner'],desired);verify_buffer(c['final_guarded_owner'],desired)
    if c['final_image_sha256']!=old['state']['image_sha256']:raise ValueError('callback source/captured globals preserved')
    pending_stack,pending_args=callback_stack(next_packet)
    if pending!=dict(packet=next_packet,cpu=callback_cpu(),args=pending_args,stack=buffer_evidence(pending_stack),guarded_shadow=buffer_evidence(b'\xda'*12288),declared_ABI_not_host_register_capture=True):raise ValueError('callback exact unanswered next entry ABI')
    if digest(c)!=before_digest:raise ValueError('callback verifier modified raw evidence')
    return dict(native_instructions=sum(r['count'] for r in runs),reads=len(reads),writes=len(writes),native_APIs=len(seen),
        result=1,bound_HWND=packet['hwnd'],original_virtual_dispatch=True,captured_game_global_read=False,prefix_substitutions=len(prefix['prefix']['substitutions']))


def verify_report(report):
    if report['source_contract']!=source_contract() or [c['fill'] for c in report['cases']]!=[0xA5,0xCC]:raise ValueError('callback actual source/two cases')
    pin=json.loads((ROOT/'analysis/school-window-callback-platform-v1-20261020.json').read_text(encoding='utf8'))
    build=dict(source_sha256=sha(PLATFORM_SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))
    if build!=pin['build'] or report['platform_build']!=build or inspect_module(RESOURCE_DLL.read_bytes())['sha256']!=pin['hello']['resource_module']['sha256']:raise ValueError('callback actual immutable native helper/resource identity')
    proofs=[]
    for c in report['cases']:
        h=copy.deepcopy(c['hello']);h['resource_module']['pointer']=pin['hello']['resource_module']['pointer']
        if h!=pin['hello'] or c['system_modules']!=pin['system_modules']:raise ValueError('callback actual host provenance')
        for r in c['system_modules'].values():
            if machine(r['path'])!=0x14C or sha(Path(r['path']).read_bytes())!=r['sha256']:raise ValueError('callback actual system modules')
        proofs.append(verify_case(c));calls=sum([c[p]['platform_calls'] for p in ('constructor','query','rect','adjust','icons','class_ready','registered')],[])
        trace=[dict(request=dict(id=i+1,op=a.get('op',a['name']),**a['request']),reply=dict(ok=True,id=i+1,result=a['result'])) for i,a in enumerate(calls)]
        wire=[]
        for row in trace:wire.extend([dict(direction='request',value=row['request']),dict(direction='response',value=row['reply'])])
        seq=len(trace)+1;wire.append(dict(direction='request',value=dict(id=seq,op='create_window',args=c['creation']['args'])))
        node=c['callbacks'][0];wire.append(dict(direction='response',value=node['setup']['packet']))
        for a in node['platform_calls']:
            seq+=1;row=dict(request=dict(id=seq,op=a['op'],**a['request']),reply=dict(ok=True,id=seq,result=a['result']));trace.append(row)
            wire.extend([dict(direction='request',value=row['request']),dict(direction='response',value=row['reply'])])
        wire.append(dict(direction='callback_return',value=dict(op='callback_return',callback_id=1,result=node['result'])))
        wire.append(dict(direction='response',value=c['pending_callback']['packet']))
        if c['wire']!=wire or c['platform_trace']!=trace:raise ValueError('callback exact nested wire/monotonic IDs/no pending reply')
        abort=c['platform_abort'];expected=dict(owned_process_exited=True,exit_code=abort['exit_code'],reason='after original WM_NCCREATE; next callback first instruction unexecuted',
            pending_callback=c['pending_callback']['packet'],unanswered=True,explicit_cleanup_performed=False,CreateWindowExA_return_received=False,normal_class_unregistration_performed=False)
        if abort!=expected or type(abort['exit_code']) is not int or abort['exit_code']==0 or c['platform_cleanup'] is not None:raise ValueError('callback honest terminated ownership/not normal cleanup')
    for key,value in dict(one_original_CPU_per_case=True,original_callback_executed=True,WM_NCCREATE_completed=True,CreateWindowExA_return_received=False,HWND_global_published=False,
            original_IAT_modified=False,game_helpers_stubbed=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False).items():
        if report[key] is not value:raise ValueError('callback report authority')
    return dict(cases=2,completed_messages=[129],pending_message=131,pending_guest_EIP=hex(ENTRY),creation_return_pending=True,
        callbacks=proofs,explicit_normal_cleanup=False,owned_processes_exited=True,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8'))),indent=2))
