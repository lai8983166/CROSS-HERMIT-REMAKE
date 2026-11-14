"""Declared symbolic display target, never actual adapter or desktop evidence."""
import struct
from devtools.terminal_texture_model import TextureModel
from devtools.terminal_display_platform import DisplayOwner,decode_snapshot,need

DEVICE=r'\\.\DISPLAY1'

def _wide(text,units):
    raw=(text+'\0').encode('utf-16-le');need(len(raw)<=units*2,'bounded symbolic WCHAR');return raw+bytes(units*2-len(raw))

def _device(name,description,flags,identifier,key):
    return struct.pack('<I',840)+_wide(name,32)+_wide(description,128)+struct.pack('<I',flags)+_wide(identifier,128)+_wide(key,128)

def model_blob(phase,factory,device,hwnd,generation=1):
    width,height=(1024,768) if phase==1 else (1920,1080)
    header=struct.pack('<16I',0x31505344,1,phase,factory,0,0xabcdef,1,1,1,1,1,1,device,phase+1,hwnd,generation)
    monitor=struct.pack('<I8iI',104,0,0,width,height,0,0,width,height-40,1)+_wide(DEVICE,32)
    adapter=_device(DEVICE,'DECLARED SYMBOLIC ADAPTER',5,'symbolic-adapter','symbolic-registry-key')
    child=_device(DEVICE+'\\Monitor0','DECLARED SYMBOLIC MONITOR',3,'symbolic-monitor-interface','symbolic-monitor-key')
    mode=bytearray(220);mode[:64]=_wide(DEVICE,32);struct.pack_into('<HH',mode,68,220,0);struct.pack_into('<5I',mode,168,32,width,height,0,60)
    gamma=struct.pack('<768H',*[i*257 for _ in range(3) for i in range(256)])
    return header+monitor+adapter+child+bytes(840*15)+mode+gamma

class DisplayModel(TextureModel,DisplayOwner):
    consume_line=DisplayOwner.consume_line
    def __init__(self,*args):
        super().__init__(*args);self.display_phase=-1;self.display_bound=False;self.display_generation=1;self.display_token=None;self.declared_input_cursor=None
    def send(self,lane,op,*a):
        if op in ('DISPLAY_BIND','DISPLAY_STATE'):
            self.check();phase=0 if op=='DISPLAY_BIND' else a[0]
            need(lane==0 and len(a)==(3 if op=='DISPLAY_BIND' else 2) and phase==self.display_phase+1<=2,'ordered symbolic display contract')
            need(self.factory in self.objects and self.objects[self.factory]['kind']==10 and self.baseline,'live symbolic factory and registered token')
            device=self.device if self.device in self.objects else 0
            need((phase==1)==bool(device),'symbolic snapshot device phase')
            if phase==0:need(a[:2]==(self.factory,0),'exact symbolic adapter0 factory')
            if phase==2:need(not self.input_live and not self.saved_gamma,'symbolic input and gamma cleaned before post-device read')
            raw=model_blob(phase,self.factory,device,self.hwnd,self.display_generation);self.store(a[-1],raw)
            ptd=self.engine.native(self.engine.thread_ptd[0]);ptd_hex=self.buffer_data(ptd,116).hex();error=self.primitive.errors[0]
            self.display_phase=phase;self.display_bound=True
            fields=dict(phase=phase,snapshot_sequence=phase+1,blob_bytes=16204,factory=self.factory,adapter=0,adapter_monitor_method=0x3500a0e0,hmonitor=0xabcdef,monitor_count=1,same_device=1,
                get_adapter_monitor_error=0,monitor_info_error=0,adapter_enum_error=0,monitor_enum_error=0,adapter_enum_results_hex='0100000000000000',monitor_enum_results_hex='0100000000000000',mode_error=0,create_dc=0x5555,create_dc_error=0,gamma_error=0,delete_dc_error=0,
                original_last_error=error,restored_last_error=error,tls_slot=5,tls_value=ptd,ptd_before_hex=ptd_hex,ptd_observed_hex=ptd_hex,ptd_restored_hex=ptd_hex,state_restored=1,
                baseline_token_hex=self.baseline.hex(),display_baseline_token_hex=self.baseline.hex(),display_window_generation=self.display_generation,display_owner_hwnd=self.hwnd,display_pid=1,display_bound=1,display_failed=0,display_dc=0)
            self.seq+=1;seq=self.seq;self.requests[seq]=(0,op);self.trace.append(dict(direction='request',id=seq,lane=0,op=op,args=list(a)))
            self.deliveries[seq]=[f'R {seq} 0 101 {error} 1 1 teb=4096 '+' '.join(k+'='+str(v) for k,v in fields.items())];return seq
        if op=='GFX_CREATE_DEVICE':need(self.display_bound and self.display_phase==0,'symbolic device binding required')
        if op=='GFX_BASELINE_CLEAR':need(self.display_bound and self.display_phase==2,'symbolic post-release observation required');self.display_bound=False
        if op=='Shutdown':need(not self.display_bound,'symbolic display obligation cleared')
        extra={}
        if op=='GFX_BASELINE':
            self.display_token=self.buffer_data(a[0],32).hex();extra=dict(pid=1,hwnd=self.hwnd,baseline_token_hex=self.display_token,registration_only=1)
        if op=='INPUT_BASELINE':self.declared_input_cursor=self.buffer_data(a[1],36).hex();extra=dict(observed=1,cursor_hex=self.declared_input_cursor)
        if op=='INPUT_UNACQUIRE':extra=dict(unacquired=1,acquired=0,hwnd=self.hwnd,window_alive=1)
        if op=='INPUT_RELEASE':extra=dict(hwnd=self.hwnd,window_alive=1)
        if op=='INPUT_CURSOR_RESTORE':extra=dict(show_delta_bits=0,show_count_bits=0,initial_show_count_bits=0)
        if op=='GFX_RELEASE':extra=dict(kind=self.objects[a[0]]['kind'])
        seq=super().send(lane,op,*a)
        if op in ('GFX_GAMMA_SAVE','GFX_GAMMA_RESTORE'):extra.update(gamma_after_hex=self.gamma[a[0]].hex(),gamma_dirty=0)
        if op.startswith(('INPUT_','GFX_')) and self.display_token:extra['baseline_token_hex']=self.display_token
        for key,value in extra.items():
            need(' '+key+'=' not in self.deliveries[seq][-1],'unique enriched symbolic field')
            self.deliveries[seq][-1]+=' '+key+'='+str(value)
        if op in ('CreateWindowExA','WINDOW_CLOSE'):self.deliveries[seq][-1]+=f' window_generation={self.display_generation}'
        if op=='STATUS':self.deliveries[seq][-1]+=f' display_bound={int(self.display_bound)} display_failed=0 display_dc=0'
        if op.startswith(('INPUT_','GFX_')):self.deliveries[seq][-1]+=f' display_window_generation={self.display_generation}'
        return seq

Model=DisplayModel
