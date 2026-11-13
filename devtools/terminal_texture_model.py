"""Symbolic persistent-storage extension, never a native texture success claim."""
from devtools.terminal_input_model import Model as ParentModel
from devtools.terminal_texture_platform import TextureOwner,logical_pixels,need

class TextureModel(ParentModel,TextureOwner):
    consume_line=TextureOwner.consume_line
    def __init__(self,*args):
        super().__init__(*args);self.texture_generation=0;self.texture_locks={};self.texture_pending={};self.texture_failed=False
    def send(self,lane,op,*a):
        if op=='TEX_VERIFY':
            self.check();need(lane==0 and len(a)==3,'fixed symbolic persistence wire')
            obj,generation,out=a;need(self.texture_pending.get(obj)==generation and obj in self.objects and 'lock' not in self.objects[obj],'fresh post-unlock symbolic storage')
            o=self.objects[obj];need((o['w'],o['h'],o['fmt'])==(256,256,26),'declared font atlas')
            self.texture_generation+=1
            o['lock']=True
            try:raw=logical_pixels(bytes(o['pixels']),o['pitch']);self.store(out,raw)
            finally:del o['lock']
            ptd=self.engine.native(self.engine.thread_ptd[0]);ptd_hex=self.buffer_data(ptd,116).hex();error=self.primitive.errors[0]
            del self.texture_pending[obj]
            # The inherited fixture declares slot5, tid101 and teb4096.
            fields=dict(source_generation=generation,verify_generation=self.texture_generation,readonly_flags=16,level=0,logical_row_bytes=512,rows=256,logical_bytes=131072,pitch=o['pitch'],bits=obj+0x2000000,padding_bytes_per_row=o['pitch']-512,lock_hresult=0,unlock_hresult=0,lock_last_error=error,unlock_last_error=error,readonly_lock_acquired=1,readonly_unlock_attempted=1,readonly_unlock_succeeded=1,geometry_valid=1,copied=1,pending=0,original_last_error=error,restored_last_error=error,tls_slot=5,tls_value=ptd,ptd_before_hex=ptd_hex,ptd_observed_hex=ptd_hex,ptd_restored_hex=ptd_hex,state_restored=1)
            fields.update(read_process_memory_result=1,read_rows=256,read_bytes=131072,read_error=0,read_failed_row=0xffffffff)
            self.seq+=1;seq=self.seq;self.requests[seq]=(0,op);self.trace.append(dict(direction='request',id=seq,lane=0,op=op,args=list(a)))
            self.deliveries[seq]=[f'R {seq} 0 101 {error} 1 1 teb=4096 '+' '.join(k+'='+str(v) for k,v in fields.items())];return seq
        if op in ('GFX_LOCK','GFX_RELEASE'):need(a[0] not in self.texture_pending,'symbolic texture verification obligation retained')
        if op=='Shutdown':need(not self.texture_pending and not self.texture_failed,'symbolic unresolved texture blocks shutdown')
        seq=super().send(lane,op,*a)
        if op=='GFX_LOCK':
            self.texture_generation+=1;self.texture_locks[a[0]]=(self.texture_generation,a[4])
            self.deliveries[seq][-1]+=f' lock_generation={self.texture_generation}'
        elif op=='GFX_UNLOCK':
            generation,flags=self.texture_locks.pop(a[0]);required=int(not(flags&16))
            if required:self.texture_pending[a[0]]=generation
            self.deliveries[seq][-1]+=f' lock_generation={generation} unlocked_generation={generation} verification_required={required}'
        elif op=='STATUS':self.deliveries[seq][-1]+=f' texture_verify_pending={len(self.texture_pending)} texture_verify_failed={int(self.texture_failed)}'
        return seq
