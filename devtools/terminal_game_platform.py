"""Original post-window WinMain platform leaves on the current MAIN owner.

No launcher or desktop authorization. GAME and device admission stay separate.
"""
from __future__ import annotations
import struct
from devtools.terminal_window_destruction import DestructionEngine, DestructionOwner
from devtools.terminal_window_callbacks import MAX_CALLBACKS, MAX_DEPTH
from devtools import terminal_native_owner_probe as base

need, ROOT = base.need, base.ROOT
POST_WINDOW = {0x592410:('ShowWindow',2),0x592414:('UpdateWindow',1),
    0x592424:('GetWindowRect',2),0x592420:('GetClientRect',2),
    0x592478:('CoInitialize',1),0x592024:('InitCommonControlsEx',1),
    0x59247c:('CoCreateInstance',5),0x59228c:('MultiByteToWideChar',6)}
METHODS = {1:{5:('DM_STOP',5),34:('DM_SET_VOLUME',4),38:('DM_CLOSE_DOWN',1),
                  44:('DM_INIT_AUDIO',8),51:('DM_GET_DEFAULT_AUDIO_PATH',2)},
    2:{5:('DM_LOADER_SEARCH',4)},3:{},4:{0:('COM_QUERY',3)},5:{9:('DS_STOP',1)},
    6:{},7:{},8:{13:('DS_SET_NOTIFY',4)},9:{}}
CLASSES = {(0x5cb3ec,0x5caf0c):1,(0x5cb37c,0x5caf1c):2,(0x5cfd7c,0x5ce80c):4}
QUERIES = {0x5cef3c:5,0x5ce8dc:6,0x5cef0c:7,0x5cef1c:8,0x5ceefc:9}
CALLBACK_PARENTS = {'ShowWindow','UpdateWindow','CoInitialize','CoUninitialize','InitCommonControlsEx','CoCreateInstance',
    'COM_QUERY','COM_RELEASE',*(name for methods in METHODS.values() for name,_ in methods.values())}


class GameOwner(DestructionOwner):
    def consume_line(self, line):
        if not isinstance(line,str) or not line.startswith('C ') or not self.waiting:
            return super().consume_line(line)
        parent=self.waiting[-1]
        if self.requests.get(parent,(None,None))[1] not in CALLBACK_PARENTS:
            return super().consume_line(line)
        need(len(line)<=66000,'bounded post-window callback')
        row={}
        for token in line.split()[1:]:
            key,value=token.split('=',1)
            need(key not in row,'unique callback field')
            if value=='-' and key.endswith('_hex'):value=''
            row[key]=int(value) if value.isdecimal() and not key.endswith('_hex') else value
        fields={'callback_id','parent_request','parent_callback_id','depth','lane','tid','teb','guest_entry',
            'hwnd','message','wParam','lParam','data_kind','data_bytes','data_hex','last_error',
            'tls_slot','tls_value','tls_tracked_value','tls_error','ptd_bytes','ptd_hex'}
        need(fields<=row.keys(),'complete post-window callback envelope')
        need(all(isinstance(row[k],int) and 0<=row[k]<=0xffffffff for k in fields-{'data_kind','data_hex','ptd_hex'}),'callback uint32 fields')
        lane,op=self.requests[parent]
        ready=next(e for e in self.events if e['event']=='READY')
        need(row['parent_request']==parent and lane==row['lane']==0 and op in CALLBACK_PARENTS,'exact pending post-window MAIN operation')
        need((row['tid'],row['teb'])==(ready['main_tid'],ready['main_teb']),'same actual MAIN callback identity')
        need(row['callback_id']==len(self.callback_packets)+1<=MAX_CALLBACKS and
             row['depth']==len(self.callback_active)+1<=MAX_DEPTH and
             row['parent_callback_id']==(self.callback_active[-1] if self.callback_active else 0),'bounded exact callback ancestry')
        need(self.callback_handler is not None,'original callback executor installed')
        self.trace.append(dict(direction='callback',**row))
        self.callback_packets.append(row);self.callback_active.append(row['callback_id'])
        try:
            value=self.callback_handler(row)
            reply=self.call('CB_RETURN',row['callback_id'],value)
            need(reply['result']==1 and reply['callback_result']==value,'actual callback acknowledges original result')
        finally:self.callback_active.pop()


class GameEngine(DestructionEngine):
    def __init__(self):
        super().__init__()
        self.slots.update(POST_WINDOW)
        self.targets={self.word(slot):slot for slot in self.slots}
        need(len(self.targets)==len(self.slots),'distinct original post-window imports')
        for slot in POST_WINDOW:
            target=self.word(slot)
            need(not 0x400000<=target<0x9b4000,'external post-window leaf')
            if not any(a<=target<=b for a,b,_ in self.u.mem_regions()):self.u.mem_map(target&-4096,4096)
            self.put(target,b'\xc3')
        self.md.topology()
        self.com_balance=0
        self.interfaces={};self.com_targets={}

    def interface(self,reply,kind):
        native=reply['object']
        need(kind in METHODS and native and reply['kind']==kind and reply['vtable'] and reply['method0'] and reply['method2'],'current typed native COM identity')
        guest=None
        for guest,entry in self.interfaces.items():
            if entry['native']==native:
                need(entry['identity']['vtable']==reply['vtable'] and
                     all(entry['identity'][k]==reply[k] for k in reply if k.startswith('method') and k in entry['identity']) and
                     entry['identity']['group']==reply['group'],'stable retained COM identity')
                entry['refs']+=1
                entry['kinds']=sorted(set(entry['kinds'])|{kind});entry['identity'].update(reply)
                break
        else:
            guest=0x68000000+len(self.interfaces)*0x1000
            need(not any(a<=guest<=b for a,b,_ in self.u.mem_regions()),'fresh opaque COM projection page')
            self.u.mem_map(guest,4096);self.md.topology()
            self.put(guest,struct.pack('<I',guest+0x100))
            self.interfaces[guest]=dict(native=native,kinds=[kind],refs=1,identity=reply.copy())
        need(reply['owned_refs']==self.interfaces[guest]['refs'],'current native owned COM reference count')
        vtable=guest+0x100
        methods={2:('COM_RELEASE',1),**METHODS[kind]}
        for index,(name,argc) in methods.items():
            need(reply.get('method'+str(index),0),'actual native whitelisted method identity')
            target=guest+0x800+index*8
            if target in self.com_targets:
                need(self.com_targets[target]==(guest,index,name,argc),'aliased COM slot retains same ABI')
            self.put(vtable+index*4,struct.pack('<I',target));self.put(target,b'\xc3')
            self.targets[target]=target
            self.com_targets[target]=(guest,index,name,argc)
        return guest

    def wide(self,address,limit=260):
        for count in range(1,limit+1):
            data=self.read(address,count*2)
            if data[-2:]==b'\0\0':return data
        raise ValueError('bounded original WCHAR string')

    def com_api(self,target):
        guest,index,name,argc=self.com_targets[target]
        entry=self.interfaces[guest]
        need(entry['refs']>0 and self.lane==0 and not self.frames,'live current MAIN COM reference')
        sp=self.reg('ESP');args=[self.word(sp+4+4*i) for i in range(argc)]
        need(args[0]==guest,'original COM this identity')
        row=dict(name=name,method_index=index,guest_interface=guest,native_interface=entry['native'],
            native_method=entry['identity']['method'+str(index)],lane=0,sp=sp,ret=self.word(sp),args=args,
            before=self.state(),wire_start=len(self.owner.trace),temporary_buffers=[],outputs=[])
        self.records.append(row)
        ptd=self.thread_ptd[0];yield from self.sync(ptd)
        observed=yield('MEM_READ',self.native(ptd),116)
        need(observed['hex']==self.read(ptd,116).hex(),'live MAIN PTD at COM call')
        row['current_native_PTD']=dict(guest=ptd,native=self.native(ptd),hex=observed['hex'])
        projected=[entry['native'],*args[1:]]
        output=None;kind=None
        if name in ('COM_QUERY','DM_GET_DEFAULT_AUDIO_PATH'):
            output=args[-1];kind=QUERIES.get(args[1]) if name=='COM_QUERY' else 3
            need(kind and self.word(output)==0,'original zero COM output and fixed queried IID')
            projected[-1]=yield from self.buffer(self.read(output,4),row['temporary_buffers'])
        elif name=='DM_LOADER_SEARCH':
            need(args[1]==0x5cb2fc and args[3]==0,'original loader GUID/clear flag')
            raw=self.wide(args[2]);need(raw=='.\\\0'.encode('utf-16le'),'original relative loader search path')
            projected[2]=yield from self.buffer(raw,row['temporary_buffers'])
        elif name=='DM_SET_VOLUME':
            need(args[1]==0x5cb08c and args[3]==4,'original volume GUID and LONG extent')
            projected[2]=yield from self.buffer(self.read(args[2],4),row['temporary_buffers'])
        elif name=='DM_INIT_AUDIO':need(args[1:]==[0,0,self.window_handle,8,64,63,0],'original audio init arguments')
        elif name=='DS_SET_NOTIFY':need(args[1:3]==[self.window_handle,0x464] or args[1:]==[0,0,0],'original notify or clear')
        reply=yield(name,*projected)
        if output is not None:
            observed=yield('MEM_READ',projected[-1],4)
            need(observed['result']==4 and len(bytes.fromhex(observed['hex']))==4,'complete COM output readback')
            native=struct.unpack('<I',bytes.fromhex(observed['hex']))[0]
            need(native==reply.get('object',0),'COM output matches actual native identity')
            value=self.interface(reply,kind) if reply['result']<0x80000000 else 0
            if not value:need(native==0,'failed COM output remains null')
            self.put(output,struct.pack('<I',value))
            row['outputs'].append(dict(guest=output,native_output=native,projected_output=value))
        if name=='COM_RELEASE':
            need(reply['released_owned_ref']==1 and reply['remaining_owned_refs']==entry['refs']-1,'actual native reference release accounting')
            entry['refs']-=1
        for temporary in reversed(row['temporary_buffers']):
            released=yield('MEM_FREE',temporary['native']);need(released['result']==1,'COM temporary released');temporary['released']=True
        value=reply['result']
        self.reg('EAX',value);self.reg('ESP',sp+4+argc*4);self.reg('EIP',row['ret'])
        row.update(native_leaf=reply,value=value,after=self.state(),wire_end=len(self.owner.trace))

    def api(self,slot):
        if slot in self.com_targets:
            yield from self.com_api(slot)
            return
        if slot not in POST_WINDOW:
            yield from super().api(slot)
            return
        need(self.lane==0 and not self.frames and self.window_handle,'post-window current MAIN only')
        name,argc=POST_WINDOW[slot]
        sp=self.reg('ESP');args=[self.word(sp+4+4*i) for i in range(argc)]
        row=dict(name=name,slot=slot,target=self.word(slot),lane=0,sp=sp,ret=self.word(sp),args=args,
            before=self.state(),wire_start=len(self.owner.trace),temporary_buffers=[],projections=[],outputs=[])
        self.records.append(row)
        ptd=self.thread_ptd[0]
        need(ptd,'live current MAIN PTD')
        yield from self.sync(ptd)
        observed=yield('MEM_READ',self.native(ptd),116)
        need(observed['hex']==self.read(ptd,116).hex(),'actual MAIN PTD mirror at post-window boundary')
        row['current_native_PTD']=dict(guest=ptd,native=self.native(ptd),hex=observed['hex'])
        if name in ('ShowWindow','UpdateWindow'):
            need(args[0]==self.window_handle and (name!='ShowWindow' or args[1]==1),'original current HWND/show command')
            reply=yield(name,*args)
            # ShowWindow returns prior visibility, not success. Never force TRUE.
        elif name in ('GetClientRect','GetWindowRect','InitCommonControlsEx'):
            size=8 if name=='InitCommonControlsEx' else 16
            address=args[0] if size==8 else args[1]
            raw=self.read(address,size)
            if size==8:need(raw==struct.pack('<II',8,0x800),'original INITCOMMONCONTROLSEX bytes')
            else:need(args[0]==self.window_handle,'original geometry query on owned HWND')
            pointer=yield from self.buffer(raw,row['temporary_buffers'])
            row['projections'].append(dict(guest=address,native=pointer,bytes=size,input_hex=raw.hex()))
            reply=yield(name,pointer) if size==8 else (name,self.window_handle,pointer)
            need(reply['result']!=0,'actual post-window BOOL success '+name)
            observed=yield('MEM_READ',pointer,size)
            data=bytes.fromhex(observed['hex'])
            need(observed['result']==size==len(data),'complete post-window structure readback')
            if size==16:
                self.put(address,data);row['outputs'].append(dict(pointer=address,hex=data.hex()))
            else:need(data==raw,'input-only common controls structure retained')
        elif name=='CoCreateInstance':
            kind=CLASSES.get((args[0],args[3]))
            need(kind and args[1:3]==[0,3] and self.word(args[4])==0,'original fixed CLSID/IID/context/null output')
            pointer=yield from self.buffer(self.read(args[4],4),row['temporary_buffers'])
            reply=yield(name,*args[:4],pointer)
            observed=yield('MEM_READ',pointer,4)
            need(observed['result']==4 and len(bytes.fromhex(observed['hex']))==4,'complete created COM output')
            native=struct.unpack('<I',bytes.fromhex(observed['hex']))[0]
            need(native==reply.get('object',0),'created native COM identity binding')
            value=self.interface(reply,kind) if reply['result']<0x80000000 else 0
            if not value:need(native==0,'failed creation has null output')
            self.put(args[4],struct.pack('<I',value))
            row['outputs'].append(dict(guest=args[4],native_output=native,projected_output=value))
        elif name=='MultiByteToWideChar':
            need(args[:2]==[0,0] and args[3]==0xffffffff and args[5]==260,'original conversion ABI')
            text=yield from self.buffer(self.string(args[2],260),row['temporary_buffers'])
            output=yield from self.buffer(self.read(args[4],520),row['temporary_buffers'])
            reply=yield(name,0,0,text,0xffffffff,output,260)
            need(0<reply['result']<=260,'actual bounded wide conversion')
            observed=yield('MEM_READ',output,520)
            data=bytes.fromhex(observed['hex']);need(len(data)==520 and observed['result']==520,'complete wide output buffer')
            self.put(args[4],data);row['outputs'].append(dict(pointer=args[4],hex=data.hex()))
        else:
            need(name=='CoInitialize' and args==[0] and self.com_balance==0,'original initial apartment call')
            reply=yield(name,0)
            if reply['result'] in (0,1):self.com_balance+=1
            # Original signed HRESULT branch handles failure; no success substitute.
        value=reply['result'];row['native_leaf']=reply
        for temporary in reversed(row['temporary_buffers']):
            closed=yield('MEM_FREE',temporary['native'])
            need(closed['result']==1,'post-window temporary freed')
            temporary['released']=True
        self.reg('EAX',value);self.reg('ESP',sp+4+argc*4);self.reg('EIP',row['ret'])
        row.update(value=value,after=self.state(),wire_end=len(self.owner.trace))


def begin_original_game(engine,owner,stop):
    """One declared WinMain root; subsequent phases preserve its entire caller."""
    engine.owner=owner;owner.callback_handler=engine.callback
    need(owner.call('WINDOW_GATE',1)['result']==1,'explicit window gate')
    module=owner.call('WINDOW_MODULE')['result']
    need(module,'owned resource module')
    engine.root('original_heap_init',0x57b9d0,(1,))
    need(engine.root('original_MAIN_TLS_init',0x5752d0)==1,'original current MAIN TLS')
    command=0x65600000
    engine.u.mem_map(command,4096);engine.md.topology();engine.put(command,b'\0')
    engine.root('original_WinMain_continuous',0x49dd70,(module,0,command,1),stop=0x49de23)
    main=engine.word(0x7a4a00)
    need(main and engine.word(main)==0x5986a0,'original MAIN publication')
    engine.bind_window(main,module)
    engine.stop=0x4504e1;engine.done[0]=False;engine.drive()
    engine.checkpoint('original_current_HWND_before_ShowWindow')
    need(owner.call('GAME_GATE',1)['result']==1,'explicit GAME-platform gate')
    engine.stop=stop;engine.done[0]=False;engine.drive()
    engine.checkpoint('continuous_original_GAME_prepublication_boundary')
    need(engine.word(0x7a49fc)==0 and not engine.worker_handle,'no fabricated GAME publication or worker')
    return dict(stop=engine.reg('EIP'),cpu=engine.state()['cpu'],MAIN=main,HWND=engine.window_handle,
        com_balance=engine.com_balance,GAME_published=False,declared_roots=3)


def cleanup_before_graphics(engine,owner):
    """Explicit supplemental original roots; never pretend pending WinMain returned."""
    from devtools.terminal_scene_dc_probe_v2 import delete_proof
    need(engine.reg('EIP')==0x413450 and 0x413450 not in engine.sites,'before any graphics initialization')
    game=engine.reg('ECX');main=engine.word(0x7a4a00)
    allocation,_=engine.owned(game)
    pending=engine.read(base.cold.old.STACK,65536)
    engine.stack=base.WORK_STACK
    engine.root('supplemental_original_GAME_destructor_and_free',0x412dd0,(1,),game,True)
    need(allocation not in engine.allocations and not any(x['refs'] for x in engine.interfaces.values()),'original GAME and COM references released')
    deletions=[r for r in engine.records if r['name']=='DeleteDC']
    need(len(deletions)==1 and delete_proof(deletions[0]['native_leaf']),'original DeleteDC with real retirement observations required')
    dc=deletions[0]['args'][0];observed=owner.call('DC_INFO',dc)
    need(observed['dc_retired']==1 and observed['now_flush'] and not observed['now_type'] and not observed['now_font'] and
         not observed['now_gdi_error'] and observed['now_gdi_count']==observed['baseline_gdi_count'],'post-GAME DC remains invalid')
    engine.dcs.remove(dc)
    close=owner.call('WINDOW_CLOSE',engine.window_handle);engine.assert_closed(close)
    need(owner.call('UnregisterClassA',engine.class_atom,engine.window_module)['result']==1,'class cleanup')
    need(owner.call('WINDOW_MODULE_CLOSE',engine.window_module)['result']==1,'module cleanup')
    uninit=owner.call('CoUninitialize')
    need(uninit['void']==1 and uninit['com_balance']==0,'same MAIN balanced apartment teardown')
    engine.com_balance=0
    need(owner.call('GAME_GATE',0)['result']==1 and owner.call('WINDOW_GATE',0)['result']==1,'all platform gates closed')
    engine.root('supplemental_original_MAIN_destructor',0x44fe60,receiver=main,callee=True)
    engine.root('supplemental_original_MAIN_free',0x428ad0,(main,))
    engine.root('supplemental_original_MAIN_PTD_free_TLS_clear',0x575450,(0,))
    engine.root('supplemental_original_TLS_and_lock_teardown',0x575360)
    engine.root('supplemental_original_heap_teardown',0x57ba60)
    need(engine.read(base.cold.old.STACK,65536)==pending,'pending original WinMain/factory stack retained')
    need(not any((engine.allocations,engine.events,engine.locks,engine.fonts,engine.dcs,engine.heap)),'original guest resource ledgers empty')
    status=owner.call('STATUS')
    for field in ('ui_gate','game_gate','com_balance','com_interfaces','com_refs','com_groups','audio_initialized','audio_pending_close','graph_notifications','game_call_active',
                  'window_modules','window_classes','windows','allocations','memory_bytes','heaps','handles','criticals','tls_slots','fonts','dcs'):
        need(status[field]==0,'native original resource ledger zero: '+field)
    shutdown=owner.call('Shutdown');need(shutdown['result']==1,'empty-resource helper shutdown request')
    return dict(close=close,status=status,shutdown=shutdown,DC_after_GAME=observed,pending_stack_sha256=base.sha(pending),
        WinMain_completed=False,pending_native_state_resumable_after_cleanup=False)
