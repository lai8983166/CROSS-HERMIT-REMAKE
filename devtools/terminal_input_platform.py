"""Original input continuation in the graphics MAIN owner; no native launcher."""
from __future__ import annotations
import struct
from devtools.terminal_graphics_platform import GraphicsEngine,GraphicsOwner,base,need
from devtools.terminal_input_native import METHODS,IMPORTS,OPS,original_contract
from devtools.terminal_window_callbacks import MAX_CALLBACKS,MAX_DEPTH


class InputOwner(GraphicsOwner):
    def consume_line(self,line):
        if not isinstance(line,str) or not line.startswith('C ') or not self.waiting:
            return super().consume_line(line)
        parent=self.waiting[-1];lane,op=self.requests.get(parent,(None,None))
        if not str(op).startswith('INPUT_'):return super().consume_line(line)
        need(op in OPS and len(line)<=66000,'bounded fixed input callback parent')
        row={}
        for token in line.split()[1:]:
            key,value=token.split('=',1);need(key not in row,'unique input callback field')
            if value=='-' and key.endswith('_hex'):value=''
            row[key]=int(value) if value.isdecimal() and not key.endswith('_hex') else value
        fields={'callback_id','parent_request','parent_callback_id','depth','lane','tid','teb','guest_entry','hwnd','message','wParam','lParam','data_kind','data_bytes','data_hex','last_error','tls_slot','tls_value','tls_tracked_value','tls_error','ptd_bytes','ptd_hex'}
        need(fields<=row.keys(),'complete input callback envelope')
        need(all(isinstance(row[k],int) and 0<=row[k]<=0xffffffff for k in fields-{'data_kind','data_hex','ptd_hex'}),'input callback uint32 fields')
        ready=next(e for e in self.events if e['event']=='READY')
        need(row['parent_request']==parent and lane==row['lane']==0,'current input MAIN parent')
        need((row['tid'],row['teb'])==(ready['main_tid'],ready['main_teb']),'same input MAIN TID/TEB')
        need(row['callback_id']==len(self.callback_packets)+1<=MAX_CALLBACKS and row['depth']==len(self.callback_active)+1<=MAX_DEPTH and row['parent_callback_id']==(self.callback_active[-1] if self.callback_active else 0),'input callback ancestry')
        need(self.callback_handler is not None,'original input callback executor')
        self.trace.append(dict(direction='callback',**row));self.callback_packets.append(row);self.callback_active.append(row['callback_id'])
        try:
            value=self.callback_handler(row);reply=self.call('CB_RETURN',row['callback_id'],value)
            need(reply['result']==1 and reply['callback_result']==value,'actual input callback acknowledgement')
        finally:self.callback_active.pop()


def verify_original_format(read,contract,va):
    matches=[x for x in contract['formats'] if x['va']==va];need(len(matches)==1,'fixed original format VA')
    f=matches[0];header=read(va,24);need(header.hex()==f['header_hex'],'complete original dataformat header unchanged')
    table=read(f['header'][5],f['header'][4]*16);need(table.hex()==f['objects_hex'],'complete original dataformat table unchanged')
    guids=[]
    for address in sorted({x[0] for x in f['objects'] if x[0]}):
        expected=next(x for x in contract['GUIDs'] if x['va']==address);raw=read(address,16)
        need(raw.hex()==expected['hex'],'original dataformat GUID unchanged');guids.append(dict(va=address,sha256=base.sha(raw)))
    return dict(va=va,bytes=len(header)+len(table),sha256=base.sha(header+table),GUIDs=guids)


class InputEngine(GraphicsEngine):
    def __init__(self):
        super().__init__();self.input_objects={};self.input_targets={};self.input_closed=False;self.input_contract=original_contract()
        self.slots.update(IMPORTS)
        for slot in IMPORTS:
            target=self.word(slot);self.targets[target]=slot
            if not any(a<=target<=b for a,b,_ in self.u.mem_regions()):self.u.mem_map(target&-4096,4096)
            self.put(target,b'\xc3')
        self.md.topology()

    def input_interface(self,reply,kind):
        need(reply.get('object') and reply.get('kind')==kind and kind in METHODS and reply.get('vtable') and reply.get('owned_refs')==1,'actual fresh typed input object')
        need(not any(x['native']==reply['object'] and x['refs'] for x in self.input_objects.values()),'one input identity per lifetime')
        if kind==20:need(reply['group']==0,'input factory root')
        else:need(any(x['native']==reply['group'] and x['kind']==20 and x['refs'] for x in self.input_objects.values()),'current input factory parent')
        for slot in METHODS[kind]:need(reply.get('method'+str(slot)),'actual input vtable method')
        guest=0x6e000000+len(self.input_objects)*4096;self.u.mem_map(guest,4096);self.md.topology()
        self.input_objects[guest]=dict(native=reply['object'],kind=kind,refs=1,identity=reply.copy());self.put(guest,struct.pack('<I',guest+256))
        for slot,(name,argc) in METHODS[kind].items():
            target=guest+2048+slot*8;self.put(guest+256+slot*4,struct.pack('<I',target));self.put(target,b'\xc3')
            self.input_targets[target]=(guest,name,argc);self.targets[target]=target
        return guest

    def api(self,slot):
        if slot in self.input_targets:
            guest,name,argc=self.input_targets[slot];yield from self.input_api(slot,name,argc,guest);return
        if slot in IMPORTS:yield from self.input_api(slot,*IMPORTS[slot]);return
        yield from super().api(slot)

    def input_api(self,slot,name,argc,guest=None):
        need(self.lane==0 and not self.frames and self.window_handle,'current input MAIN with original HWND')
        sp=self.reg('ESP');args=[self.word(sp+4+4*i) for i in range(argc)];wire=list(args)
        row=dict(name=name,slot=slot,lane=0,sp=sp,ret=self.word(sp),args=args,before=self.state(),wire_start=len(self.owner.trace),temporary_buffers=[],projections=[],outputs=[]);self.records.append(row)
        ptd=self.thread_ptd[0];need(ptd,'live MAIN input PTD');yield from self.sync(ptd)
        observed=yield('MEM_READ',self.native(ptd),116);need(observed['hex']==self.read(ptd,116).hex(),'current input PTD bytes');row['current_native_PTD']=observed
        if guest is not None:
            entry=self.input_objects[guest];need(entry['refs'] and args[0]==guest,'current original input this');wire[0]=entry['native']
        if name=='INPUT_FORMAT':row['original_format']=verify_original_format(self.read,self.input_contract,args[1])
        if name in ('INPUT_CREATE','INPUT_DEVICE'):
            address=args[2] if name=='INPUT_CREATE' else args[1]
            expected=next(x for x in self.input_contract['GUIDs'] if x['va']==address)
            need(self.read(address,16).hex()==expected['hex'],'original input interface/device GUID unchanged');row['original_GUID']=expected
        specs={'INPUT_CREATE':{3:(4,True)},'INPUT_DEVICE':{2:(4,True)},'INPUT_PROPERTY':{2:(20,False)},'INPUT_DEVICE_INFO':{1:(580,True)},'INPUT_CLIENT_TO_SCREEN':{1:(8,True)}}
        for index,(size,output) in specs.get(name,{}).items():
            raw=self.read(args[index],size);wire[index]=yield from self.buffer(raw,row['temporary_buffers'])
            row['projections'].append(dict(index=index,guest=args[index],native=wire[index],bytes=size,input_hex=raw.hex(),output=output))
        if name=='INPUT_CREATE':
            qualified=yield('INPUT_INSTANCE_INFO',args[0]);need(qualified['result']==1 and qualified['original_instance']==args[0] and qualified['helper_instance_substituted']==0,'actual original WinMain instance retained');row['instance']=qualified
        reply=yield(name,*wire);row['native_leaf']=reply;value=reply['result'];outputs={}
        for p in row['projections']:
            raw=yield from self.readback(p['native'],p['bytes'])
            if p['output']:outputs[p['index']]=raw
            else:need(raw.hex()==p['input_hex'],'input-only original structure retained')
        if name in ('INPUT_CREATE','INPUT_DEVICE'):
            index=3 if name=='INPUT_CREATE' else 2;kind=20 if name=='INPUT_CREATE' else (21 if args[1]==0x5cc04c else 22)
            native=struct.unpack('<I',outputs[index])[0];need(native==reply.get('object'),'actual input output identity')
            if value<0x80000000:outputs[index]=struct.pack('<I',self.input_interface(reply,kind))
            else:need(native==0,'non-null failure output requires explicit ownership route')
        if name=='INPUT_RELEASE':
            need(reply['remaining_owned_refs']==0 and reply['native_remaining_refs']==value,'actual input Release receipt');entry['refs']=0
            if entry['kind']==20:
                need(value==0 and not any(x['refs'] for x in self.input_objects.values()),'all original input releases complete')
                restore=yield('INPUT_CURSOR_RESTORE',);need(restore['result']==1 and restore['actual_readback']==1,'owner cursor baseline read back before graphics release')
                close=yield('INPUT_CLOSE',);need(close['result']==1,'input module released after cursor restore')
                gate=yield('INPUT_GATE',0);need(gate['result']==1,'empty input gate closed')
                row['supplemental_input_restore']=dict(cursor=restore,close=close,gate=gate);self.input_closed=True
        for index,raw in outputs.items():self.put(args[index],raw);row['outputs'].append(dict(guest=args[index],hex=raw.hex()))
        for t in reversed(row['temporary_buffers']):
            q=yield('MEM_FREE',t['native']);need(q['result']==1,'input temporary freed');t['released']=True
        self.reg('EAX',value);self.reg('ESP',sp+4+argc*4);self.reg('EIP',row['ret']);row.update(value=value,after=self.state(),wire_end=len(self.owner.trace))


def cleanup_after_publication(engine,owner,game):
    """Supplemental original destructors; the pending WinMain never returned."""
    from devtools.terminal_scene_dc_probe_v2 import delete_proof
    need(engine.reg('EIP')==0x4506eb and engine.word(0x7a49fc)==game and 0x4506e9 in engine.sites,'original GAME store executed before cleanup')
    main=engine.word(0x7a4a00);allocation,_=engine.owned(game);pending=engine.read(base.cold.old.STACK,65536)
    engine.stack=base.WORK_STACK
    engine.root('supplemental_original_graphics_GAME_destructor_free',0x412dd0,(1,),game,True)
    need(engine.input_closed and not any(x['refs'] for x in engine.input_objects.values()),'input released and owner cursor restored before parent teardown')
    need(allocation not in engine.allocations and not any(x['refs'] for x in engine.interfaces.values()),'GAME and audio/movie references released')
    need(not any(x['refs'] for x in engine.graphics.values()) and not engine.locked and not engine.gamma_saved,'original graphics references/locks/gamma restored')
    need(not engine.graphics_dcs and not engine.graphics_fonts and not engine.pending_gdi,'original graphics GDI retirement receipts complete')
    deletions=[r for r in engine.records if r['name']=='DeleteDC'];need(len(deletions)==1 and delete_proof(deletions[0]['native_leaf']),'original screen DC retirement')
    dc=deletions[0]['args'][0];observed=owner.call('DC_INFO',dc);need(observed['dc_retired']==1 and not observed['now_type'] and not observed['now_font'] and observed['now_gdi_count']==observed['baseline_gdi_count'],'post-GAME original DC invalid');engine.dcs.remove(dc)
    runtime=owner.call('GFX_RUNTIME_CLOSE');need(runtime['result']==1 and runtime['remaining_load_refs']==0,'all actual module load references released')
    need(owner.call('GFX_BASELINE_CLEAR')['result']==1 and owner.call('GFX_GATE',0)['result']==1,'empty graphics gate closed')
    close=owner.call('WINDOW_CLOSE',engine.window_handle);engine.assert_closed(close)
    need(owner.call('UnregisterClassA',engine.class_atom,engine.window_module)['result']==1,'class cleanup')
    need(owner.call('WINDOW_MODULE_CLOSE',engine.window_module)['result']==1,'window module cleanup')
    uninit=owner.call('CoUninitialize');need(uninit['void']==1 and uninit['com_balance']==0,'COM apartment balanced')
    engine.com_balance=0;need(owner.call('GAME_GATE',0)['result']==1 and owner.call('WINDOW_GATE',0)['result']==1,'empty platform gates')
    engine.root('supplemental_original_MAIN_destructor',0x44fe60,receiver=main,callee=True)
    engine.root('supplemental_original_MAIN_free',0x428ad0,(main,))
    engine.root('supplemental_original_MAIN_PTD_free_TLS_clear',0x575450,(0,))
    engine.root('supplemental_original_TLS_and_lock_teardown',0x575360)
    engine.root('supplemental_original_heap_teardown',0x57ba60)
    need(engine.read(base.cold.old.STACK,65536)==pending,'pending WinMain/factory full stack unchanged during supplemental cleanup')
    need(not any((engine.allocations,engine.events,engine.locks,engine.fonts,engine.dcs,engine.heap)),'guest original resource ledgers zero')
    status=owner.call('STATUS')
    fields=('ui_gate','game_gate','com_balance','com_interfaces','com_refs','com_groups','audio_initialized','audio_pending_close','graph_notifications','game_call_active','window_modules','window_classes','windows','allocations','memory_bytes','heaps','handles','criticals','tls_slots','fonts','dcs','gfx_gate','gfx_baseline','gfx_modules','gfx_interfaces','gfx_refs','gfx_locks','gfx_blocks','gfx_recording','gfx_gamma_dirty','gfx_dcs','gfx_bitmaps','gfx_fonts','gfx_mute','gfx_unresolved_refs','input_gate','input_baseline','input_instance','input_interfaces','input_modules','input_show_delta_bits','input_position_dirty')
    for field in fields:need(status[field]==0,'actual zero resource field '+field)
    shutdown=owner.call('Shutdown');need(shutdown['result']==1,'empty-resource shutdown request')
    return dict(status=status,zero_fields=fields,runtime_close=runtime,window_close=close,shutdown=shutdown,pending_stack_sha256=base.sha(pending),WinMain_completed=False,cleaned_state_resumable=False,actual_desktop_gamma_after_mode_restore_proven=False,original_GAME_global_left_as_abandoned_pending_state=True)
