"""Independent recursive original-code replay and exact nested IPC verification."""
import argparse,copy,hashlib,json,struct
from pathlib import Path
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_MEM_READ
from tools.school_window_events import *
from tools.school_window_class_verification import verify_case as verify_prefix
from tools.school_window_callback_verification import expected_maps,check_maps
from tools.school_window_module_validation import digest
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_renderer_init_verification import verify_buffer
from tools.school_device_init_verification import unpack
from tools.school_startup_inputs import verify_observation
from tools.school_window_events_platform import COMPILER,sha,machine

INPUTS={0x7A49FC:0,0x80A398:0};GLOBAL_HWND=0x7A0BB4
PHASES=('allocation','constructor','publication','tasks','query','branch','rect','adjust','class','icons','class_ready','registered','create_ready')


def fresh(image):
    b=bytearray(image)
    for at,v in INPUTS.items():store(b,at-BASE,v)
    return bytes(b)


def prefix_view(c):
    """Validate fresh image hashes; adapt only those hashes in a disclosed old-check view."""
    view=copy.deepcopy(c);calls=c['constructor']['platform_calls'];pairs={};changes=[]
    for phase in PHASES:
        if phase in parent.STOPS:old=parent.project_image(phase,calls)
        else:
            old=bytearray(window.project_image(parent.project_image('publication',calls),phase if phase in ('tasks','query','branch') else 'branch'))
            store(old,window.INSTANCE-BASE,c['module_input']['value']);old=bytes(old)
        actual=hashlib.sha256(fresh(old)).hexdigest();legacy=hashlib.sha256(old).hexdigest()
        if c[phase]['state']['image_sha256']!=actual:raise ValueError('raw fresh prefix image differs: '+phase)
        pairs[actual]=legacy
    def visit(obj,path):
        if isinstance(obj,dict):
            for key,value in list(obj.items()):
                if key in ('image_sha256','retained_image_sha256') and isinstance(value,str):
                    if value not in pairs:raise ValueError('unexpected fresh prefix hash location '+path+'.'+key)
                    changes.append(dict(path=path+'.'+key,actual=value,legacy=pairs[value]));obj[key]=pairs[value]
                elif isinstance(value,(dict,list)):visit(value,path+'.'+key)
        elif isinstance(obj,list):
            for i,value in enumerate(obj):visit(value,path+'['+str(i)+']')
    for phase in PHASES:visit(view[phase],phase)
    proof=verify_prefix(view)
    return dict(legacy_prefix_proof=proof,declared_fresh_input_hash_views=changes,CPU_or_raw_case_modified=False)


def verify_case(c):
    before=digest(c);prefix=prefix_view(c);raw=SOURCE.read_bytes();old=c['create_ready'];module=c['module_input']['value']
    image=bytearray(fresh(window.project_image(parent.project_image('publication',c['constructor']['platform_calls']),'branch')));store(image,window.INSTANCE-BASE,module)
    initial=c['initial_input_declaration']
    from tools.school_main_context_emulation import initial_cpu
    if initial!=dict(before_first_original_instruction=True,cpu=initial_cpu(),globals={hex(a):v for a,v in INPUTS.items()},image_sha256=hashlib.sha256(fresh(raw)).hexdigest(),prefix_instruction_count=0):raise ValueError('fresh inputs not declared at original root')
    creation=c['creation'];a=creation['import_admission'];check_maps(a['foreign_after'],expected_maps())
    expected_admission=dict(slots=[hex(s) for s in (CREATE_SLOT,*IMPORTS)],before_cpu=old['cpu'],after_cpu=old['cpu'],image_sha256=old['state']['image_sha256'],owner_sha256=old['state']['guarded_owner']['sha256'],stack_sha256=old['state']['stack']['sha256'],foreign_before=old['state']['foreign_maps'],foreign_after=a['foreign_after'],declared_maps=[dict(pointer=p,bytes=n,initial_byte=0xda) for p,n in ((STACK,65536),(RETURN,4096),(SHADOW-4096,12288))])
    if a!=expected_admission:raise ValueError('creation admission changed pending state')
    caller=dict(old['cpu']);caller.update(EIP=dword(raw,CREATE_SLOT-BASE),ESP=old['cpu']['ESP']-4)
    native=bytearray(unpack(old['state']['stack']));store(native,caller['ESP']-parent.STACK,0x4504D5)
    if creation!=dict(import_admission=a,cpu=caller,instruction_runs=[dict(va=CREATE,count=1)],native_writes=[dict(pc=CREATE,pointer=caller['ESP'],bytes=4,value=0x4504D5)],sp=caller['ESP'],args=base.callback.previous.creation_args(module),return_va='0x4504d5',native_stack=buffer_evidence(native)):raise ValueError('original creation source call/frame')
    u=Uc(UC_ARCH_X86,UC_MODE_32);owner=unpack(old['state']['guarded_owner'])
    for at,size,b in ((BASE,(len(image)+4095)&~4095,image),(parent.OWNER-4096,len(owner),owner),(STACK,65536,b'\xda'*65536),(SHADOW-4096,12288,b'\xda'*12288),(RETURN,4096,b'\xda'*4096),(parent.STACK,65536,native)):
        u.mem_map(at,size);u.mem_write(at,bytes(b))
    for at,b in expected_maps().items():u.mem_map(at,4096);u.mem_write(at,bytes(b))
    for k,v in caller.items():u.reg_write(REGISTERS[k],v)
    code={i.address:i for start,end in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[start-BASE:end-BASE],start)}
    code.update({i.address:i for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[0x4504D5-BASE:0x4504E1-BASE],0x4504D5)})
    nodes={n['setup']['packet']['callback_id']:n for n in c['callbacks']}
    if list(nodes)!=list(range(1,len(nodes)+1)) or len(nodes)>128:raise ValueError('actual callback entry order')
    wire=iter(c['wire']);trace=[];sequence=0;seen=[];active=[];proofs=[];pending=[None];pub=False
    def cpu():return {k:u.reg_read(v) for k,v in REGISTERS.items()}
    def word(at):return struct.unpack('<I',bytes(u.mem_read(at,4)))[0]
    def expect(direction,value):
        if next(wire,None)!=dict(direction=direction,value=value):raise ValueError('exact nested protocol '+direction)
    def request(op,args,result,children=None):
        nonlocal sequence
        sequence+=1;req=dict(id=sequence,op=op,**args);expect('request',req)
        if children:children()
        reply=dict(ok=True,id=req['id'],result=result);expect('response',reply);trace.append(dict(request=req,reply=reply))
    calls=sum([c[p]['platform_calls'] for p in ('constructor','query','rect','adjust','icons','class_ready','registered')],[])
    for row in calls:request(row.get('op',row['name']),row['request'],row['result'])
    sequence+=1;create_req=dict(id=sequence,op='create_window',args=creation['args']);expect('request',create_req)
    def access(uc,kind,at,n,value,user):
        state=active[-1];pc=uc.reg_read(REGISTERS['EIP'])
        if kind==UC_MEM_READ:
            if not any(a<=at and at+n<=b for a,b in ((BASE,BASE+len(image)),(parent.OWNER,parent.OWNER+parent.BACKING),(STACK,STACK+65536),(SHADOW-4096,SHADOW+8192),*(([(parent.STACK,parent.STACK+65536)]) if pub else []))):raise ValueError('independent read outside owned state')
            state['reads'].append(dict(pc=pc,pointer=at,bytes=n,hex=bytes(uc.mem_read(at,n)).hex()))
        else:
            if not (STACK<=at and at+n<=STACK+65536 or parent.OWNER<=at and at+n<=parent.OWNER+parent.SIZE or pub and (parent.STACK<=at and at+n<=parent.STACK+65536 or at==GLOBAL_HWND and n==4)):raise ValueError('independent unowned write')
            state['writes'].append(dict(pc=pc,pointer=at,bytes=n,value=value&((1<<(n*8))-1)))
    def instruction(uc,at,n,user):
        if at==RETURN or pub and at==0x4504E1:uc.emu_stop();return
        for slot in IMPORTS:
            if at==dword(raw,slot-BASE):pending[0]=(slot,uc.reg_read(REGISTERS['ESP']));uc.emu_stop();return
        i=code.get(at)
        if i is None or i.size!=n:raise ValueError('independent original instruction boundary')
        state=active[-1]
        if state['runs'] and state['runs'][-1]['va']==at:state['runs'][-1]['count']+=1
        else:state['runs'].append(dict(va=at,count=1))
        if i.mnemonic=='ret':state['returns'].append(dict(va=hex(at),return_va=hex(word(uc.reg_read(REGISTERS['ESP']))),sp=uc.reg_read(REGISTERS['ESP']),eax=uc.reg_read(REGISTERS['EAX'])))
    u.hook_add(UC_HOOK_CODE,instruction);u.hook_add(UC_HOOK_MEM_READ,access);u.hook_add(UC_HOOK_MEM_WRITE,access)
    def replay_node(ident):
        node=nodes[ident];packet=node['setup']['packet'];outer=bool(active);expected_parent=active[-1]['ident'] if outer else None
        if set(packet)!={'event_kind','callback_id','depth','guest_entry','hwnd','message','wParam','lParam','data_kind','data_hex'} or ident!=len(seen)+1 or packet['depth']!=len(active)+1 or packet['guest_entry']!=ENTRY or packet['event_kind']!='wndproc' or node['parent_callback_id']!=expected_parent:raise ValueError('independent callback parent/depth/order')
        if ident==1:hwnd=packet['hwnd']
        else:hwnd=nodes[1]['setup']['packet']['hwnd']
        if not 0<hwnd<=0xffffffff or packet['hwnd']!=hwnd or not all(type(packet[k]) is int and 0<=packet[k]<=0xffffffff for k in ('wParam','lParam')):raise ValueError('actual callback scalar/window ABI')
        data=bytes.fromhex(packet['data_hex']);message=packet['message']
        if message in (129,1):
            if packet['data_kind']!='CREATESTRUCTA' or len(data)!=48 or struct.unpack('<12I',data)[:9]!=(parent.OWNER,module,0,0,768,1024,16,16,geometry.STYLE):raise ValueError('native original creation data')
        elif message==131:
            if packet['data_kind']!='RECT' or base.rectangle(data,packet['wParam'])!=[16,16,1040,784]:raise ValueError('native original client RECT')
        elif message in (70,71):
            if packet['data_kind']!='WINDOWPOS':raise ValueError('typed position data')
            windowpos(data,hwnd)
        elif packet['data_kind']!='opaque' or data:raise ValueError('unadmitted typed callback data')
        expect('response',packet);seen.append(ident)
        saved=u.context_save();caller_cpu=cpu();oldstack=bytes(u.mem_read(STACK,65536));oldshadow=bytes(u.mem_read(SHADOW-4096,12288));oldnative=bytes(u.mem_read(parent.STACK,65536))
        verify_buffer(node['guarded_owner_before'],bytes(u.mem_read(parent.OWNER-4096,len(owner))))
        stack,args=callback_stack(packet);shadow=bytearray(b'\xda'*12288)
        if message==129:shadow[4096:4144]=data
        setup=dict(packet=packet,cpu=callback_cpu(),args=args,stack=buffer_evidence(stack),guarded_shadow=buffer_evidence(shadow),declared_ABI_not_host_register_capture=True)
        if node['setup']!=setup or node['suspended_caller_cpu']!=caller_cpu:raise ValueError('independent declared callback frame/caller')
        u.mem_write(STACK,stack);u.mem_write(SHADOW-4096,bytes(shadow))
        for k,v in callback_cpu().items():u.reg_write(REGISTERS[k],v)
        state=dict(ident=ident,runs=[],reads=[],writes=[],returns=[]);active.append(state);calls_iter=iter(node['platform_calls']);seen_apis=[]
        while True:
            pending[0]=None;u.emu_start(cpu()['EIP'],RETURN+1,count=100000,timeout=20_000_000)
            if pending[0] is None:break
            slot,sp=pending[0];name,count=IMPORTS[slot];aa=[word(sp+4+i*4) for i in range(count)]
            call=next(calls_iter,None)
            if call is None:raise ValueError('missing actual native result')
            r=call['result'];value=r['result'];req=dict(callback_id=ident)
            if type(value) is not int or not 0<=value<=0xffffffff:raise ValueError('actual native result bits')
            if name in ('GetPropA','SetPropA'):
                if aa[:2]!=[hwnd,0x594AB4] or bytes(u.mem_read(aa[1],10))!=PROPERTY:raise ValueError('original property identity')
                op='get_prop' if name=='GetPropA' else 'set_prop';req.update(hwnd=hwnd,name_hex=PROPERTY.hex())
                rr=dict(result=value,last_error=r['last_error'],name_unchanged=True,guards_unchanged=True)
                if name=='GetPropA':
                    if value!=(0 if message==129 else parent.OWNER):raise ValueError('actual property binding')
                else:
                    if message!=129 or aa[2]!=parent.OWNER or value!=1:raise ValueError('unexpected source property rebinding')
                    req['data']=parent.OWNER;rr.update(observed_property=parent.OWNER,auxiliary_readback=True)
            elif name=='GetWindowLongA':
                if message!=129 or aa[0]!=hwnd or aa[1] not in (4,0xfffffffc):raise ValueError('original WNDPROC query')
                op='get_window_long';req.update(hwnd=hwnd,index=aa[1]);host=c['registered']['platform_calls'][0]['result']['pointer_translations'][0]['host'];translated=aa[1]==0xfffffffc
                rr=dict(result=ENTRY if translated else 0,host_result=host if translated else 0,last_error=r['last_error'],reverse_translated=translated,owned_host_callback=host,guest_callback=ENTRY)
            else:
                if aa!=args:raise ValueError('source default procedure scalar/pointer forwarding')
                op='default_window';req['args']=aa
                rr=dict(result=value,host_args=[hwnd,message,packet['wParam'],packet['lParam']],lparam_reverse_translated=message==129,before_hex=data.hex(),after_hex=data.hex())
            child_ids=call['nested_callback_ids'];old_seen=len(seen)
            def children():
                for cid in child_ids:
                    if nodes[cid]['parent_callback_id']==ident:replay_node(cid)
            request(op,req,r,children)
            if seen[old_seen:]!=child_ids:raise ValueError('actual nested API callback subtree')
            wanted=dict(name=name,op=op,slot=hex(slot),va=hex(dword(raw,slot-BASE)),sp=sp,return_va=hex(word(sp)),args=aa,request=req,result=rr,observed_EAX=value,live_host_observed=True,nested_callback_ids=child_ids)
            if call!=wanted:raise ValueError('complete actual native ABI/result/typed data')
            if message==129 and name=='DefWindowProcA':u.mem_write(SHADOW,bytes.fromhex(r['after_hex']))
            u.reg_write(REGISTERS['EAX'],value);u.reg_write(REGISTERS['EIP'],word(sp));u.reg_write(REGISTERS['ESP'],sp+4+count*4);seen_apis.append(name)
        if next(calls_iter,None) is not None or node['instruction_runs']!=state['runs'] or node['native_reads']!=state['reads'] or node['native_writes']!=state['writes'] or node['native_returns']!=state['returns'] or node['cpu']!=cpu() or node['result']!=cpu()['EAX'] or node['original_callback_executed'] is not True:raise ValueError('independent full original callback replay')
        if cpu()['EIP']!=RETURN or cpu()['ESP']!=TOP+20 or any(cpu()[k]!=callback_cpu()[k] for k in ('EBP','EBX','ESI','EDI')):raise ValueError('original callback return ABI')
        st=dict(guarded_owner=buffer_evidence(bytes(u.mem_read(parent.OWNER-4096,len(owner)))),callback_stack=buffer_evidence(bytes(u.mem_read(STACK,65536))),guarded_shadow=buffer_evidence(bytes(u.mem_read(SHADOW-4096,12288))),native_stack=buffer_evidence(oldnative),image_sha256=hashlib.sha256(image).hexdigest())
        if node['state']!=st or bytes(u.mem_read(BASE,len(image)))!=image or bytes(u.mem_read(parent.STACK,65536))!=oldnative:raise ValueError('independent full callback state')
        expect('callback_return',dict(op='callback_return',callback_id=ident,result=node['result']))
        active.pop();u.context_restore(saved)
        if outer:u.mem_write(STACK,oldstack);u.mem_write(SHADOW-4096,oldshadow)
        if node['restored_caller_cpu']!=cpu() or node['outer_guest_buffers_restored'] is not True:raise ValueError('nested caller restoration')
        proofs.append(dict(callback_id=ident,parent=expected_parent,message=message,depth=packet['depth'],instructions=sum(r['count'] for r in state['runs']),reads=len(state['reads']),writes=len(state['writes']),native_APIs=len(seen_apis),result=node['result']))
    for ident,n in nodes.items():
        if n['parent_callback_id'] is None:replay_node(ident)
    if seen!=list(nodes):raise ValueError('all actual callbacks executed exactly once')
    result=c['creation_result'];expected_result=dict(result=nodes[1]['setup']['packet']['hwnd'],callback_calls=len(nodes),original_creation_returned=True)
    if result!=expected_result:raise ValueError('actual native creation success return')
    reply=dict(ok=True,id=create_req['id'],result=result);expect('response',reply);trace.append(dict(request=create_req,reply=reply))
    if next(wire,None) is not None or c['platform_trace']!=trace:raise ValueError('complete actual nested wire/trace')
    u.reg_write(REGISTERS['EAX'],result['result']);u.reg_write(REGISTERS['EIP'],word(caller['ESP']));u.reg_write(REGISTERS['ESP'],caller['ESP']+52)
    publication=c['hwnd_publication']
    if publication['before_cpu']!=cpu():raise ValueError('original native caller stdcall continuation')
    pub=True;state=dict(ident=None,runs=[],reads=[],writes=[],returns=[]);active.append(state)
    u.emu_start(cpu()['EIP'],parent.RETURN+1,count=1000,timeout=20_000_000)
    final_image=bytearray(image);store(final_image,GLOBAL_HWND-BASE,result['result'])
    final_owner=bytes(u.mem_read(parent.OWNER-4096,len(owner)));final_native=bytes(u.mem_read(parent.STACK,65536))
    wanted=dict(before_cpu=publication['before_cpu'],cpu=cpu(),instruction_runs=state['runs'],native_writes=state['writes'],hwnd=result['result'],state=dict(image_sha256=hashlib.sha256(final_image).hexdigest(),guarded_owner=buffer_evidence(final_owner),native_stack=buffer_evidence(final_native)))
    if publication!=wanted or cpu()['EIP']!=0x4504E1 or bytes(u.mem_read(BASE,len(image)))!=final_image:raise ValueError('independent original HWND publication/state')
    verify_buffer(c['final_guarded_owner'],final_owner)
    if c['final_image_sha256']!=hashlib.sha256(final_image).hexdigest():raise ValueError('final full image')
    expected_reads=[dict(**r,callback_id=n['setup']['packet']['callback_id']) for n in c['callbacks'] for r in n['native_reads'] if any(r['pointer']<=p<r['pointer']+r['bytes'] for p in INPUTS)]
    if c['declared_input_reads']!=expected_reads or any(r['hex']!='00000000' for r in expected_reads):raise ValueError('fresh input reads and no prefix repair')
    lifetime=c['lifetime']
    if lifetime!=dict(owned_process_exited=True,exit_code=lifetime['exit_code'],CreateWindowExA_return_received=True,explicit_normal_cleanup=False,pending_native_callback=False,resources_ended_with_owned_process=True,standalone_resumable_checkpoint=False) or type(lifetime['exit_code']) is not int or lifetime['exit_code']==0:raise ValueError('honest owned-window lifetime termination')
    if digest(c)!=before:raise ValueError('independent verifier modified raw case')
    return dict(prefix=prefix,callbacks=sorted(proofs,key=lambda r:r['callback_id']),callback_count=len(nodes),max_depth=max(n['setup']['packet']['depth'] for n in c['callbacks']),creation_returned=True,HWND_published=True,pending_original_EIP=hex(cpu()['EIP']),raw_case_modified=False)


def verify_report(report):
    before=digest(report)
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256 or report['source_image_sha256']!=SOURCE_SHA256 or report['initial_globals']!={hex(a):v for a,v in INPUTS.items()} or [c['fill'] for c in report['cases']]!=[0xa5,0xcc]:raise ValueError('source/actual declared inputs/cases')
    observations=json.loads((ROOT/report['initial_inputs']).read_text(encoding='utf8'))
    if len(observations['cases'])!=2 or any(verify_observation(o)!=INPUTS for o in observations['cases']):raise ValueError('fresh original observations')
    pin=json.loads((ROOT/'analysis/school-window-startup-platform-v1-20261020.json').read_text(encoding='utf8'))
    cs=ROOT/'tools/school_window_startup_platform.cs';helper=ROOT/'.venv-audit/school-window-startup-platform-v1.exe'
    if pin!=dict(source_sha256=sha(cs.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(helper.read_bytes()),machine=machine(helper)):raise ValueError('actual immutable native helper')
    oldpin=json.loads((ROOT/'analysis/school-window-events-platform-v1-20261020.json').read_text(encoding='utf8'))
    proofs=[]
    for c in report['cases']:
        hello=copy.deepcopy(c['hello']);hello['resource_module']['pointer']=oldpin['hello']['resource_module']['pointer']
        if hello!=oldpin['hello'] or c['system_modules']!=oldpin['system_modules']:raise ValueError('actual original resource and system modules')
        for m in c['system_modules'].values():
            if machine(m['path'])!=0x14c or sha(Path(m['path']).read_bytes())!=m['sha256']:raise ValueError('real x86 system module identity')
        proofs.append(verify_case(c))
    for flag in ('original_game_code_modified','original_IAT_modified','retained_VM_advanced','full_WinMain_executed','normal_cleanup_completed'):
        if report[flag] is not False:raise ValueError('startup authority boundary')
    if digest(report)!=before:raise ValueError('raw report modified')
    return dict(cases=2,case_proofs=proofs,original_creation_returned=True,original_HWND_published=True,retained_VM_advanced=False,normal_cleanup_completed=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args();print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8'))),indent=2))
