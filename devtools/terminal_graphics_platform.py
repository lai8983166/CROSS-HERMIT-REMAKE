"""Current MAIN graphics projection; no launcher or desktop permission."""
from __future__ import annotations
import struct
from devtools.terminal_game_platform import GameEngine, GameOwner, CALLBACK_PARENTS, base, need
from devtools.terminal_window_callbacks import MAX_CALLBACKS, MAX_DEPTH

METHODS={
 10:{2:('GFX_RELEASE',1),6:('GFX_MODE_COUNT',2),7:('GFX_ENUM_MODE',4),8:('GFX_DISPLAY_MODE',3),10:('GFX_CHECK_FORMAT',7),15:('GFX_CREATE_DEVICE',7)},
 11:{1:('GFX_ADDREF',1),2:('GFX_RELEASE',1),6:('GFX_GET_FACTORY',2),7:('GFX_CAPS',2),8:('GFX_DEVICE_MODE',2),9:('GFX_CREATION',2),16:('GFX_BACKBUFFER',4),18:('GFX_GAMMA_SET',3),19:('GFX_GAMMA_READ',2),20:('GFX_TEXTURE',8),23:('GFX_VERTEX_BUFFER',6),40:('GFX_VIEWPORT',2),50:('GFX_RENDER_STATE',3),51:('GFX_GET_RENDER_STATE',3),52:('GFX_BEGIN',1),53:('GFX_END',2),56:('GFX_DELETE_BLOCK',2),61:('GFX_TEXTURE_BIND',3),63:('GFX_STAGE_STATE',4)},
 12:{2:('GFX_RELEASE',1),8:('GFX_SURFACE_DESC',2)},
 13:{2:('GFX_RELEASE',1),14:('GFX_LEVEL_DESC',3),15:('GFX_TEXTURE_SURFACE',3),16:('GFX_LOCK',5),17:('GFX_UNLOCK',2)},
 14:{2:('GFX_RELEASE',1),13:('GFX_VERTEX_DESC',2)}}
IMPORTS={0x59246c:('GFX_FACTORY',1),0x592068:('GFX_GET_OBJECT',3),0x592094:('GFX_DC_CREATE',1),
 0x592098:('GFX_DIB',6),0x5920a4:('GFX_SELECT',2),0x59208c:('GFX_BK_MODE',2),
 0x5920b4:('GFX_BK_COLOR',2),0x5920b0:('GFX_TEXT_COLOR',2),0x59209c:('GFX_MAP_MODE',2),
 0x5920b8:('GFX_TEXT_ALIGN',2),0x5920ac:('GFX_FONT_INDIRECT',1),0x5920bc:('GFX_TEXT_EXTENT',4),
 0x5920c0:('GFX_TEXT_OUT',8),0x59223c:('GFX_MULDIV',3),
 0x5922c8:('GFX_MODULE_GET',1),0x592184:('GFX_MODULE_LOAD',1),0x5922cc:('GFX_PROC',2)}
DEBUG_TARGET=0x55f0e830
PARENTS=CALLBACK_PARENTS|{n for methods in METHODS.values() for n,_ in methods.values()}|{n for n,_ in IMPORTS.values()}|{'GFX_GAMMA_SAVE','GFX_GAMMA_RESTORE','GFX_RUNTIME_CLOSE','GFX_DEBUG_MUTE','GFX_DEBUG_MUTE_RESOLVED'}


class GraphicsOwner(GameOwner):
    def consume_line(self,line):
        if not isinstance(line,str) or not line.startswith('C ') or not self.waiting:
            return super().consume_line(line)
        parent=self.waiting[-1];lane,op=self.requests.get(parent,(None,None))
        if not str(op).startswith('GFX_'):return super().consume_line(line)
        need(op in PARENTS and len(line)<=66000,'bounded graphics callback parent')
        row={}
        for token in line.split()[1:]:
            key,value=token.split('=',1);need(key not in row,'unique callback field')
            if value=='-' and key.endswith('_hex'):value=''
            row[key]=int(value) if value.isdecimal() and not key.endswith('_hex') else value
        fields={'callback_id','parent_request','parent_callback_id','depth','lane','tid','teb','guest_entry','hwnd','message','wParam','lParam','data_kind','data_bytes','data_hex','last_error','tls_slot','tls_value','tls_tracked_value','tls_error','ptd_bytes','ptd_hex'}
        need(fields<=row.keys(),'complete graphics callback envelope')
        need(all(isinstance(row[k],int) and 0<=row[k]<=0xffffffff for k in fields-{'data_kind','data_hex','ptd_hex'}),'callback uint32 fields')
        ready=next(e for e in self.events if e['event']=='READY')
        need(row['parent_request']==parent and lane==row['lane']==0,'current graphics MAIN parent')
        need((row['tid'],row['teb'])==(ready['main_tid'],ready['main_teb']),'same graphics MAIN TID/TEB')
        need(row['callback_id']==len(self.callback_packets)+1<=MAX_CALLBACKS and row['depth']==len(self.callback_active)+1<=MAX_DEPTH and row['parent_callback_id']==(self.callback_active[-1] if self.callback_active else 0),'graphics callback ancestry')
        need(self.callback_handler is not None,'original callback executor')
        self.trace.append(dict(direction='callback',**row));self.callback_packets.append(row);self.callback_active.append(row['callback_id'])
        try:
            value=self.callback_handler(row);reply=self.call('CB_RETURN',row['callback_id'],value)
            need(reply['result']==1 and reply['callback_result']==value,'real graphics callback acknowledgement')
        finally:self.callback_active.pop()


class GraphicsEngine(GameEngine):
    def __init__(self):
        super().__init__();self.graphics={};self.graphics_targets={};self.pixel_regions={};self.locked={};self.bitmap_regions={};self.graphics_fonts=set();self.graphics_dcs=set();self.selected={};self.gamma_saved=set();self.debug_targets={};self.lock_generation=0;self.bitmap_generation=0;self.pending_gdi=set()
        self.slots.update(IMPORTS);self.targets.update({self.word(s):s for s in IMPORTS})
        need(self.word(0x8097a8)==self.word(0x8097a4)==0,'cold original debug globals require original runtime resolution')
        for target in [self.word(s) for s in IMPORTS]:
            if not any(a<=target<=b for a,b,_ in self.u.mem_regions()):self.u.mem_map(target&-4096,4096)
            self.put(target,b'\xc3')
        self.md.topology()

    def graphics_interface(self,reply,kind):
        native=reply.get('object',0)
        need(kind in METHODS and native and reply['kind']==kind and reply['vtable'] and reply['method2'],'current typed graphics interface')
        found=[(g,x) for g,x in self.graphics.items() if x['native']==native and x['refs']]
        if found:
            need(len(found)==1,'one current graphics identity');guest,entry=found[0]
            need(entry['kind']==kind and entry['identity']['vtable']==reply['vtable'] and entry['identity']['group']==reply['group'],'stable graphics alias type/table/parent')
            entry['refs']+=1
        else:
            guest=0x69000000+len(self.graphics)*4096;self.u.mem_map(guest,4096);self.md.topology()
            entry=dict(native=native,kind=kind,refs=1,identity=reply.copy());self.graphics[guest]=entry
            self.put(guest,struct.pack('<I',guest+256))
        need(entry['refs']==reply['owned_refs'],'native graphics reference receipt')
        for slot,(name,argc) in METHODS[kind].items():
            # Only expose implemented methods which the native side attests.
            if not reply.get('method'+str(slot)):continue
            if 'method'+str(slot) in entry['identity']:need(entry['identity']['method'+str(slot)]==reply['method'+str(slot)],'stable graphics method')
            target=guest+2048+slot*8;self.put(guest+256+slot*4,struct.pack('<I',target));self.put(target,b'\xc3')
            self.graphics_targets[target]=(guest,name,argc);self.targets[target]=target
        entry['identity'].update(reply);return guest

    def pixel_map(self,key,native,size):
        need(0<size<=1048576,'bounded native pixel span')
        if key in self.pixel_regions:
            row=self.pixel_regions[key];need(row['native']==native and row['bytes']==size,'stable current pixel allocation');return row['guest']
        guest=0x6a000000+len(self.pixel_regions)*0x200000
        self.u.mem_map(guest,(size+4095)&-4096);self.md.topology()
        self.pixel_regions[key]=dict(native=native,guest=guest,bytes=size);return guest

    def code(self,u,pc,n,user):
        # A new bounded graphics case; the frozen construction case stays2M.
        if pc in (base.RETURN,self.stop) or pc in self.targets:u.emu_stop();return
        need(0x400000<=pc<0x592000 and self.read(pc,n)==self.image[pc-0x400000:pc-0x400000+n],'original graphics source instruction '+hex(pc))
        self.count+=1;need(self.count<=6000000,'six million original graphics and cleanup instruction bound')
        if self.count%2048==0:self.owner.check()
        self.ih.update(struct.pack('<BI',self.lane,pc)+self.read(pc,n));self.sites[pc]=[n,self.sites.get(pc,[n,0])[1]+1]
        if self.frames:
            f=self.frames[-1];runs=f['instruction_runs']
            if runs and runs[-1]['va']==pc:runs[-1]['count']+=1
            else:runs.append(dict(va=pc,count=1))
            f['count']+=1;need(f['count']<=100000,'bounded original graphics callback')

    def readback(self,pointer,size):
        data=bytearray()
        for offset in range(0,size,32768):
            count=min(32768,size-offset);q=yield('MEM_READ',pointer+offset,count)
            raw=bytes.fromhex(q['hex']);need(len(raw)==count==q['result'],'complete graphics buffer readback');data+=raw
        return bytes(data)

    def transfer_pixels(self,op,obj,guest,size,row,write=False):
        for offset in range(0,size,32768):
            count=min(32768,size-offset)
            buf=yield from self.buffer(self.read(guest+offset,count) if write else bytes(count),row['temporary_buffers'])
            q=yield(op,obj,offset,buf,count);need(q['result']==count,'bounded actual pixel transfer')
            if not write:self.put(guest+offset,(yield from self.readback(buf,count)))

    def api(self,slot):
        if slot==0x5920c4 and (self.word(self.reg('ESP')+4) in self.graphics_fonts or self.word(self.reg('ESP')+4) in self.bitmap_regions or self.word(self.reg('ESP')+4) in self.fonts):
            yield from self.graphics_api(slot,'GFX_DELETE_OBJECT',1);return
        if slot==0x592060 and self.word(self.reg('ESP')+4) in self.graphics_dcs:
            yield from self.graphics_api(slot,'GFX_DC_DELETE',1);return
        if slot in self.graphics_targets:
            guest,name,argc=self.graphics_targets[slot];yield from self.graphics_api(slot,name,argc,guest);return
        if slot in self.debug_targets:yield from self.graphics_api(slot,'GFX_DEBUG_MUTE_RESOLVED',1);return
        if slot in IMPORTS:yield from self.graphics_api(slot,*IMPORTS[slot]);return
        yield from super().api(slot)

    def gdi_retirements(self,reply):
        need(reply['retirement_flush']==1,'real GDI flush before retirement census')
        for key in ('retired_fonts_hex','retired_bitmaps_hex'):
            raw=bytes.fromhex(reply[key]);need(len(raw)%4==0 and len(raw)<=64,'bounded exact retired GDI handles')
            for handle in struct.unpack('<'+'I'*(len(raw)//4),raw):
                if key=='retired_fonts_hex':
                    need(handle in self.fonts or handle in self.graphics_fonts,'retired font belongs to current generation')
                    self.fonts.pop(handle,None);self.graphics_fonts.discard(handle)
                else:
                    need(handle in self.bitmap_regions and not self.bitmap_regions[handle].get('retired'),'retired bitmap current generation')
                    self.bitmap_regions[handle].update(live=False,retired=True)
                self.pending_gdi.discard(handle)

    def graphics_api(self,slot,name,argc,guest=None):
        need(self.lane==0 and not self.frames and self.window_handle,'current MAIN graphics only')
        sp=self.reg('ESP');args=[self.word(sp+4+4*i) for i in range(argc)];wire=list(args)
        row=dict(name=name,slot=slot,lane=0,sp=sp,ret=self.word(sp),args=args,before=self.state(),wire_start=len(self.owner.trace),temporary_buffers=[],projections=[],outputs=[]);self.records.append(row)
        ptd=self.thread_ptd[0];need(ptd,'current graphics PTD');yield from self.sync(ptd)
        observed=yield('MEM_READ',self.native(ptd),116);need(observed['hex']==self.read(ptd,116).hex(),'current graphics PTD bytes');row['current_native_PTD']=observed
        if guest is not None:
            entry=self.graphics[guest];need(entry['refs'] and args[0]==guest,'live original graphics this');wire[0]=entry['native']
        if name=='GFX_DEBUG_MUTE_RESOLVED':wire=[self.debug_targets[slot]['module'],args[0]]
        specs={ # index: (bytes, input/output). Outputs retain complete pre-call bytes.
         'GFX_DISPLAY_MODE':{2:(16,True)},'GFX_ENUM_MODE':{3:(16,True)},'GFX_CREATE_DEVICE':{5:(52,True),6:(4,True)},
         'GFX_CAPS':{1:(212,True)},'GFX_DEVICE_MODE':{1:(16,True)},'GFX_CREATION':{1:(16,True)},'GFX_GET_FACTORY':{1:(4,True)},
         'GFX_BACKBUFFER':{3:(4,True)},'GFX_SURFACE_DESC':{1:(32,True)},'GFX_VIEWPORT':{1:(24,False)},
         'GFX_TEXTURE':{7:(4,True)},'GFX_TEXTURE_SURFACE':{2:(4,True)},'GFX_LEVEL_DESC':{2:(32,True)},
         'GFX_VERTEX_BUFFER':{5:(4,True)},'GFX_VERTEX_DESC':{1:(24,True)},'GFX_END':{1:(4,True)},
         'GFX_GET_RENDER_STATE':{2:(4,True)},'GFX_LOCK':{2:(8,True)},'GFX_GAMMA_SET':{2:(1536,False)},'GFX_GAMMA_READ':{1:(1536,True)},
         'GFX_GET_OBJECT':{2:(60,True)},'GFX_FONT_INDIRECT':{0:(60,False)},'GFX_DIB':{1:(40,False),3:(4,True)},
         'GFX_TEXT_EXTENT':{1:(args[2],False),3:(8,True)} if name=='GFX_TEXT_EXTENT' else {},
         'GFX_TEXT_OUT':{5:(args[6],False)} if name=='GFX_TEXT_OUT' else {}}
        if name in ('GFX_MODULE_GET','GFX_MODULE_LOAD','GFX_PROC'):
            index=1 if name=='GFX_PROC' else 0
            raw=self.string(args[index],32);need(raw in (b'd3d8.dll\0',b'd3d8d.dll\0',b'DebugSetMute\0'),'fixed original DLL/export string')
            wire[index]=yield from self.buffer(raw,row['temporary_buffers'])
        if name=='GFX_TEXT_OUT':need(args[4]==args[7]==0,'original bounded ExtTextOut no rect/spacing')
        for index,(size,output) in specs.get(name,{}).items():
            need(0<size<=32768,'bounded original graphics structure');raw=self.read(args[index],size)
            wire[index]=yield from self.buffer(raw,row['temporary_buffers']);row['projections'].append(dict(index=index,guest=args[index],native=wire[index],bytes=size,input_hex=raw.hex(),output=output))
        if name=='GFX_TEXTURE_BIND' and args[2]:
            texture=self.graphics[args[2]];need(texture['kind']==13 and texture['refs'],'current texture bind');wire[2]=texture['native']
        if name=='GFX_LOCK':
            need(args[3]==0 and args[4] in (0,16),'bounded original full texture lock')
            for bitmap,bits in self.bitmap_regions.items():
                if bits.get('live'):yield from self.transfer_pixels('GFX_DIB_READ',bitmap,bits['guest'],bits['bytes'],row)
        if name=='GFX_UNLOCK':
            lock=self.locked[guest]
            if lock['flags']&16:need(base.sha(self.read(lock['guest'],lock['bytes']))==lock['initial_sha256'],'readonly original texture remained unchanged')
            else:yield from self.transfer_pixels('GFX_LOCK_WRITE',wire[0],lock['guest'],lock['bytes'],row,True)
            # Read the real lock bytes again before unlock; keep an equality receipt.
            before=self.read(lock['guest'],lock['bytes']);yield from self.transfer_pixels('GFX_LOCK_READ',wire[0],lock['guest'],lock['bytes'],row)
            need(self.read(lock['guest'],lock['bytes'])==before,'actual uploaded texture bytes read back')
            row['uploaded_sha256']=base.sha(before)
        if name=='GFX_RELEASE' and entry['kind']==11 and entry['refs']==1:
            gamma=yield from self.buffer(bytes(1536),row['temporary_buffers'])
            restored=yield('GFX_GAMMA_RESTORE',wire[0],gamma)
            raw=yield from self.readback(gamma,1536)
            need(restored['gamma_restored']==1 and raw.hex()==entry['saved_gamma_hex'],'device gamma restored before final Release')
            row['supplemental_gamma_restore']=dict(receipt=restored,hex=raw.hex());self.gamma_saved.remove(guest)
        reply=yield(name,*wire);row['native_leaf']=reply;value=reply['result']
        outputs={}
        for p in row['projections']:
            raw=yield from self.readback(p['native'],p['bytes'])
            if p['output']:outputs[p['index']]=raw
            else:need(raw.hex()==p['input_hex'],'input-only graphics buffer retained')
        object_outputs={'GFX_CREATE_DEVICE':(6,11),'GFX_GET_FACTORY':(1,10),'GFX_BACKBUFFER':(3,12),'GFX_TEXTURE':(7,13),'GFX_TEXTURE_SURFACE':(2,12),'GFX_VERTEX_BUFFER':(5,14)}
        if name in object_outputs:
            index,kind=object_outputs[name];native=struct.unpack('<I',outputs[index])[0]
            need(native==reply.get('object',0),'actual graphics output identity')
            mapped=self.graphics_interface(reply,kind) if value<0x80000000 else 0
            if not mapped:need(native==0,'failed graphics creation/query null output')
            outputs[index]=struct.pack('<I',mapped)
            if mapped and kind==11:
                gamma=yield from self.buffer(bytes(1536),row['temporary_buffers']);saved=yield('GFX_GAMMA_SAVE',native,gamma)
                need(saved['result']==1,'actual device gamma saved before original set');raw=yield from self.readback(gamma,1536)
                self.gamma_saved.add(mapped);row['device_gamma_baseline_hex']=raw.hex();self.graphics[mapped]['saved_gamma_hex']=raw.hex()
        elif name=='GFX_FACTORY':value=self.graphics_interface(reply,10) if value else 0
        elif name=='GFX_PROC' and value:
            target=0x6f000000+len(self.debug_targets)*4096;self.u.mem_map(target,4096);self.md.topology();self.put(target,b'\xc3')
            self.debug_targets[target]=dict(module=args[0],native=value);self.targets[target]=target;value=target
        elif name in ('GFX_ADDREF','GFX_RELEASE'):
            entry=self.graphics[guest];entry['refs']+=1 if name=='GFX_ADDREF' else -1
            need(reply['remaining_owned_refs']==entry['refs'],'native AddRef/Release tracked receipt')
        elif name=='GFX_LOCK' and value<0x80000000:
            pitch,bits=struct.unpack('<II',outputs[2]);need(pitch and bits and pitch<=4096,'current lock pitch/bits')
            size=reply['lock_bytes'];self.lock_generation+=1;ptr=self.pixel_map(('texture',guest,self.lock_generation),bits,size)
            self.locked[guest]=dict(guest=ptr,bytes=size,native=bits,pitch=pitch,flags=args[4])
            yield from self.transfer_pixels('GFX_LOCK_READ',wire[0],ptr,size,row)
            self.locked[guest]['initial_sha256']=base.sha(self.read(ptr,size))
            outputs[2]=struct.pack('<II',pitch,ptr)
        elif name=='GFX_UNLOCK' and value<0x80000000:self.locked.pop(guest)
        elif name=='GFX_DIB' and value:
            bits=struct.unpack('<I',outputs[3])[0];size=256*256*4;self.bitmap_generation+=1;ptr=self.pixel_map(('bitmap',value,self.bitmap_generation),bits,size)
            self.bitmap_regions[value]=dict(guest=ptr,native=bits,bytes=size,live=True)
            yield from self.transfer_pixels('GFX_DIB_READ',value,ptr,size,row);outputs[3]=struct.pack('<I',ptr)
        elif name=='GFX_DC_CREATE' and value:self.graphics_dcs.add(value)
        elif name=='GFX_FONT_INDIRECT' and value:self.graphics_fonts.add(value)
        elif name=='GFX_SELECT' and value:self.selected[args[0]]=args[1]
        elif name=='GFX_DELETE_OBJECT' and value:
            need(reply.get('retirement_observed') or reply.get('deferred_delete'),'actual GDI retirement or explicit deferred obligation')
            if reply.get('deferred_delete'):self.pending_gdi.add(args[0])
            if args[0] in self.bitmap_regions:self.bitmap_regions[args[0]]['live']=False
            self.gdi_retirements(reply)
            if reply['retirement_observed']:need(args[0] not in self.fonts and args[0] not in self.graphics_fonts and args[0] not in self.pending_gdi,'immediate retirement reconciled')
        elif name=='GFX_DC_DELETE' and value:
            need(reply['retirement_observed']==1 and reply['object_type_after']==0,'actual compatible DC retirement')
            self.graphics_dcs.remove(args[0]);self.gdi_retirements(reply)
        for index,raw in outputs.items():self.put(args[index],raw);row['outputs'].append(dict(guest=args[index],hex=raw.hex()))
        for t in reversed(row['temporary_buffers']):
            q=yield('MEM_FREE',t['native']);need(q['result']==1,'graphics temporary freed');t['released']=True
        self.reg('EAX',value);self.reg('ESP',sp+4+(0 if name in ('GFX_DEBUG_MUTE','GFX_DEBUG_MUTE_RESOLVED') else argc*4));self.reg('EIP',row['ret'])
        row.update(value=value,after=self.state(),wire_end=len(self.owner.trace))


def cleanup_before_input(engine,owner,game):
    """Supplemental original destructors; the pending WinMain never returned."""
    from devtools.terminal_scene_dc_probe_v2 import delete_proof
    need(engine.reg('EIP')==0x413560 and 0x413560 not in engine.sites,'before any DirectInput/cursor instruction')
    main=engine.word(0x7a4a00);allocation,_=engine.owned(game);pending=engine.read(base.cold.old.STACK,65536)
    engine.stack=base.WORK_STACK
    engine.root('supplemental_original_graphics_GAME_destructor_free',0x412dd0,(1,),game,True)
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
    fields=('ui_gate','game_gate','com_balance','com_interfaces','com_refs','com_groups','audio_initialized','audio_pending_close','graph_notifications','game_call_active','window_modules','window_classes','windows','allocations','memory_bytes','heaps','handles','criticals','tls_slots','fonts','dcs','gfx_gate','gfx_baseline','gfx_modules','gfx_interfaces','gfx_refs','gfx_locks','gfx_blocks','gfx_recording','gfx_gamma_dirty','gfx_dcs','gfx_bitmaps','gfx_fonts','gfx_mute','gfx_unresolved_refs')
    for field in fields:need(status[field]==0,'actual zero resource field '+field)
    shutdown=owner.call('Shutdown');need(shutdown['result']==1,'empty-resource shutdown request')
    return dict(status=status,zero_fields=fields,runtime_close=runtime,window_close=close,shutdown=shutdown,pending_stack_sha256=base.sha(pending),WinMain_completed=False,cleaned_state_resumable=False,actual_desktop_gamma_after_mode_restore_proven=False)
