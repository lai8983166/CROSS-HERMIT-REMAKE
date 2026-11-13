"""Supplemental readonly re-lock verification; original graphics rows stay intact."""
import struct
from devtools.terminal_input_platform import InputEngine,InputOwner,base,need
from devtools.terminal_window_callbacks import MAX_CALLBACKS,MAX_DEPTH

def logical_pixels(raw,pitch):
    need(512<=pitch<=1024 and len(raw)==pitch*256,'complete bounded256-row atlas mapping')
    return b''.join(raw[y*pitch:y*pitch+512] for y in range(256))

def validate_receipt(q,generation,ptd,error):
    need(q['result']==1 and q['source_generation']==generation and q['verify_generation']>generation,'fresh readonly lock after exact original unlock')
    need(q['lock_hresult']<0x80000000 and q['unlock_hresult']<0x80000000,'both actual supplemental HRESULTs succeeded')
    need(q['readonly_lock_acquired']==q['readonly_unlock_attempted']==q['readonly_unlock_succeeded']==q['geometry_valid']==q['copied']==1 and q['pending']==0,'readonly lock explicitly released')
    need(q['read_process_memory_result']==1 and q['read_rows']==256 and q['read_bytes']==131072 and q['read_failed_row']==0xffffffff,'all logical rows actually readable after relock')
    need((q['readonly_flags'],q['level'],q['logical_row_bytes'],q['rows'],q['logical_bytes'])==(16,0,512,256,131072),'exact readonly logical-pixel contract')
    need(512<=q['pitch']<=1024 and q['bits'] and q['padding_bytes_per_row']==q['pitch']-512,'new current mapping geometry')
    need(q['state_restored']==1 and q['original_last_error']==q['restored_last_error']==q['last_error']==error,'original native LastError restored')
    need(q['ptd_before_hex']==q['ptd_restored_hex']==ptd.hex() and len(bytes.fromhex(q['ptd_observed_hex']))==116,'complete original PTD restored and read back')

class TextureOwner(InputOwner):
    def consume_line(self,line):
        if not isinstance(line,str) or not line.startswith('C ') or not self.waiting or self.requests.get(self.waiting[-1],(None,None))[1]!='TEX_VERIFY':
            return super().consume_line(line)
        parent=self.waiting[-1];need(len(line)<=66000,'bounded texture callback envelope');row={}
        for token in line.split()[1:]:
            key,value=token.split('=',1);need(key not in row,'unique texture callback field')
            row[key]=int(value) if value.isdecimal() and not key.endswith('_hex') else ('' if value=='-' and key.endswith('_hex') else value)
        fields={'callback_id','parent_request','parent_callback_id','depth','lane','tid','teb','guest_entry','hwnd','message','wParam','lParam','data_kind','data_bytes','data_hex','last_error','tls_slot','tls_value','tls_tracked_value','tls_error','ptd_bytes','ptd_hex'}
        need(fields<=row.keys() and all(isinstance(row[k],int) and 0<=row[k]<=0xffffffff for k in fields-{'data_kind','data_hex','ptd_hex'}),'complete typed texture callback')
        ready=next(e for e in self.events if e['event']=='READY')
        need(row['parent_request']==parent and self.requests[parent][0]==row['lane']==0 and (row['tid'],row['teb'])==(ready['main_tid'],ready['main_teb']),'same MAIN texture callback parent')
        need(row['callback_id']==len(self.callback_packets)+1<=MAX_CALLBACKS and row['depth']==len(self.callback_active)+1<=MAX_DEPTH and row['parent_callback_id']==(self.callback_active[-1] if self.callback_active else 0),'texture callback ancestry')
        need(self.callback_handler is not None,'original callback executor')
        self.trace.append(dict(direction='callback',**row));self.callback_packets.append(row);self.callback_active.append(row['callback_id'])
        try:
            value=self.callback_handler(row);reply=self.call('CB_RETURN',row['callback_id'],value)
            need(reply['result']==1 and reply['callback_result']==value,'real texture callback acknowledgement')
        finally:self.callback_active.pop()

class TextureEngine(InputEngine):
    def __init__(self):
        super().__init__();self.texture_generations={};self.texture_verifications=[]

    def graphics_api(self,slot,name,argc,guest=None):
        source=None
        if name=='GFX_UNLOCK':
            lock=self.locked[guest].copy()
            if not lock['flags']&16:source=logical_pixels(self.read(lock['guest'],lock['bytes']),lock['pitch'])
        record_index=len(self.records)
        yield from super().graphics_api(slot,name,argc,guest)
        row=self.records[record_index];leaf=row['native_leaf']
        if name=='GFX_LOCK' and leaf['result']<0x80000000:
            generation=leaf['lock_generation'];need(generation>self.texture_generations.get(guest,0),'fresh original lock generation')
            self.texture_generations[guest]=generation
        if name!='GFX_UNLOCK' or leaf['result']>=0x80000000:return
        generation=self.texture_generations[guest]
        need(leaf['lock_generation']==leaf['unlocked_generation']==generation,'exact original successful unlock generation')
        if source is None:
            need(leaf['verification_required']==0,'original readonly unlock has no upload obligation');return
        need(leaf['verification_required']==1,'original writable upload requires independent verification')
        saved=self.u.context_save();cpu=self.state()['cpu'];ptd=self.thread_ptd[0];ptd_bytes=self.read(ptd,116);out=0
        check=dict(source_generation=generation,original_unlock_request=leaf['id'],original_unlock_result=leaf['result'],original_last_error=leaf['last_error'],expected_logical_sha256=base.sha(source),source_pitch=lock['pitch'],wire_start=len(self.owner.trace),accepted=False,temporary_freed=False,CPU57_before=cpu)
        self.texture_verifications.append(check)
        try:
            before=yield('MEM_READ',self.native(ptd),116);need(before['hex']==ptd_bytes.hex(),'original post-unlock PTD before supplemental call')
            allocated=yield('MEM_ALLOC',131072);out=allocated['result'];need(out,'owned logical-pixel output')
            observed=yield('TEX_VERIFY',self.graphics[guest]['native'],generation,out);check['receipt']=observed
            # Always record actual failure and cleanup before deciding acceptance.
            validate_receipt(observed,generation,ptd_bytes,leaf['last_error'])
            need(observed['tls_slot']!=0xffffffff and observed['tls_value']==self.native(ptd),'supplemental receipt belongs to current MAIN PTD')
            raw=yield from self.readback(out,131072);check['observed_logical_sha256']=base.sha(raw)
            need(raw==source,'persistent logical pixels survive original unlock and fresh readonly lock')
            restored=yield('MEM_READ',self.native(ptd),116);need(restored['hex']==ptd_bytes.hex(),'actual restored PTD read back after supplementary operation');check['PTD_readback']=restored
            check['accepted']=True
        finally:
            self.u.context_restore(saved);self.put(ptd,ptd_bytes)
            need(self.state()['cpu']==cpu,'complete original CPU57 including EAX restored')
            restored=yield('MEM_READ',self.native(ptd),116);check['final_PTD_readback']=restored
            need(restored['hex']==ptd_bytes.hex(),'actual native PTD restored even on verification failure')
            if out:
                freed=yield('MEM_FREE',out);check['free_receipt']=freed;need(freed['result']==1,'supplemental pixel output explicitly freed');check['temporary_freed']=True
            final_error=yield('GetLastError',);check['last_error_readback']=final_error
            need(final_error['result']==leaf['last_error'],'actual original LastError retained after infrastructure')
            check['wire_end']=len(self.owner.trace);check['CPU57_after']=self.state()['cpu'];check['CPU57_restored']=check['CPU57_after']==cpu
            need(check['CPU57_restored'],'supplemental cleanup preserves original CPU57')
