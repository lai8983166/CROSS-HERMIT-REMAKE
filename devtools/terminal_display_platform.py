"""Supplemental same-MAIN display observations; original WinMain CPU is preserved."""
import struct
from devtools.terminal_texture_platform import TextureEngine,TextureOwner,base,need
from devtools.terminal_window_callbacks import MAX_CALLBACKS,MAX_DEPTH

BLOB_BYTES=16204

def wide(raw):
    need(len(raw)%2==0,'bounded WCHAR field');end=next((i for i in range(0,len(raw),2) if raw[i:i+2]==b'\0\0'),None)
    need(end is not None,'terminated Win32 display identity');return raw[:end].decode('utf-16-le')

def display_device(raw):
    need(len(raw)==840 and struct.unpack_from('<I',raw)[0]==840,'complete DISPLAY_DEVICEW')
    return dict(name=wide(raw[4:68]),description=wide(raw[68:324]),flags=struct.unpack_from('<I',raw,324)[0],device_id=wide(raw[328:584]),key=wide(raw[584:840]))

def decode_snapshot(raw):
    need(len(raw)==BLOB_BYTES,'complete actual display snapshot')
    h=struct.unpack_from('<16I',raw)
    need(h[:2]==(0x31505344,1) and h[2] in (0,1,2) and h[3] and h[4]==0 and h[5] and 1<=h[6]<=16,'fixed adapter0 display header')
    need(all(h[7:12]) and h[11]==1 and h[13] in (1,2,3) and h[14] and h[15],'all actual read/temporaryDC cleanup APIs succeeded')
    need((h[2]==1)==bool(h[12]),'device lifetime matches snapshot phase')
    m=raw[64:168];need(struct.unpack_from('<I',m)[0]==104,'MONITORINFOEXW size')
    device=wide(m[40:104]);adapter=display_device(raw[168:1008]);monitors=[display_device(raw[1008+i*840:1848+i*840]) for i in range(h[6])]
    need(adapter['name']==device and adapter['flags']&1 and not adapter['flags']&8,'actual attached non-mirror target adapter')
    need(not any(raw[1008+h[6]*840:14448]),'unused monitor slots zero')
    mode=raw[14448:14668];need(struct.unpack_from('<HH',mode,68)==(220,0),'complete current mode without private extension')
    return dict(phase=h[2],factory=h[3],adapter=0,hmonitor=h[5],snapshot_sequence=h[13],hwnd=h[14],window_generation=h[15],device=h[12],target_device=device,
        monitor=dict(rect=list(struct.unpack_from('<4i',m,4)),work=list(struct.unpack_from('<4i',m,20)),flags=struct.unpack_from('<I',m,36)[0],device=device),
        display_identity=dict(adapter=adapter,monitors=monitors),mode_hex=mode.hex(),gamma_hex=raw[14668:].hex(),
        actual_returns=dict(EnumDisplaySettingsW=h[7],GetDeviceGammaRamp=h[8],DeleteDC=h[9],GetMonitorInfoW=h[10]))

class DisplayOwner(TextureOwner):
    def consume_line(self,line):
        if not isinstance(line,str) or not line.startswith('C ') or not self.waiting or self.requests.get(self.waiting[-1],(None,None))[1] not in ('DISPLAY_BIND','DISPLAY_STATE'):
            return super().consume_line(line)
        parent=self.waiting[-1];need(len(line)<=66000,'bounded display callback envelope');row={}
        for token in line.split()[1:]:
            key,value=token.split('=',1);need(key not in row,'unique display callback field')
            row[key]=int(value) if value.isdecimal() and not key.endswith('_hex') else ('' if value=='-' and key.endswith('_hex') else value)
        fields={'callback_id','parent_request','parent_callback_id','depth','lane','tid','teb','guest_entry','hwnd','message','wParam','lParam','data_kind','data_bytes','data_hex','last_error','tls_slot','tls_value','tls_tracked_value','tls_error','ptd_bytes','ptd_hex'}
        need(fields<=row.keys() and all(isinstance(row[k],int) and 0<=row[k]<=0xffffffff for k in fields-{'data_kind','data_hex','ptd_hex'}),'complete typed display callback')
        ready=next(e for e in self.events if e['event']=='READY')
        need(row['parent_request']==parent and self.requests[parent][0]==row['lane']==0 and (row['tid'],row['teb'])==(ready['main_tid'],ready['main_teb']),'same MAIN display callback parent')
        need(row['callback_id']==len(self.callback_packets)+1<=MAX_CALLBACKS and row['depth']==len(self.callback_active)+1<=MAX_DEPTH and row['parent_callback_id']==(self.callback_active[-1] if self.callback_active else 0),'display callback ancestry')
        need(self.callback_handler is not None,'original callback executor')
        self.trace.append(dict(direction='callback',**row));self.callback_packets.append(row);self.callback_active.append(row['callback_id'])
        try:
            value=self.callback_handler(row);reply=self.call('CB_RETURN',row['callback_id'],value)
            need(reply['result']==1 and reply['callback_result']==value,'real display callback acknowledgement')
        finally:self.callback_active.pop()

class DisplayEngine(TextureEngine):
    def __init__(self):
        super().__init__();self.display_snapshots=[];self.binding_validator=None;self.display_factory=0

    def graphics_api(self,slot,name,argc,guest=None):
        final_device=name=='GFX_RELEASE' and self.graphics[guest]['kind']==11 and self.graphics[guest]['refs']==1
        index=len(self.records)
        yield from super().graphics_api(slot,name,argc,guest)
        leaf=self.records[index]['native_leaf']
        if name=='GFX_FACTORY' and leaf['result']:
            self.display_factory=leaf['result'];yield from self.capture_display(0,leaf['last_error'])
        elif final_device and leaf['result']==0:yield from self.capture_display(2,leaf['last_error'])

    def capture_display(self,phase,error=None):
        need(phase==len(self.display_snapshots) and phase in (0,1,2) and self.display_factory,'one ordered display observation per phase')
        need(callable(self.binding_validator),'parent display binding validator required before any device creation')
        saved=self.u.context_save();cpu=self.state()['cpu'];ptd=self.thread_ptd[0];ptd_bytes=self.read(ptd,116);out=0
        check=dict(phase=phase,wire_start=len(self.owner.trace),accepted=False,temporary_freed=False,CPU57_before=cpu)
        self.display_snapshots.append(check)
        try:
            initial=yield('GetLastError',)
            if error is None:error=initial['result']
            need(initial['result']==error,'original LastError before display observation')
            actual=yield('MEM_READ',self.native(ptd),116);need(actual['hex']==ptd_bytes.hex(),'original native PTD before supplemental observation')
            allocated=yield('MEM_ALLOC',BLOB_BYTES);out=allocated['result'];need(out,'owned fixed display output')
            q=yield (('DISPLAY_BIND',self.display_factory,0,out) if phase==0 else ('DISPLAY_STATE',phase,out));check['receipt']=q
            raw=yield from self.readback(out,BLOB_BYTES);check.update(blob_hex=raw.hex(),blob_sha256=base.sha(raw))
            need(q['result']==1 and q['phase']==phase and q['snapshot_sequence']==phase+1 and q['blob_bytes']==BLOB_BYTES,'complete actual display receipt')
            need(q['state_restored']==1 and q['original_last_error']==q['restored_last_error']==q['last_error']==error,'display operation restores original LastError')
            need(q['ptd_before_hex']==q['ptd_restored_hex']==ptd_bytes.hex() and len(bytes.fromhex(q['ptd_observed_hex']))==116 and q['tls_value']==self.native(ptd),'display operation restores complete current PTD')
            decoded=decode_snapshot(raw);check['decoded']=decoded
            need(decoded['hwnd']==self.window_handle and decoded['window_generation']==q['display_window_generation'] and decoded['factory']==self.display_factory==q['factory'] and decoded['hmonitor']==q['hmonitor'],'actual snapshot header/receipt/owner agree')
            need(decoded['snapshot_sequence']==q['snapshot_sequence'] and decoded['phase']==q['phase'],'actual phase/sequence agree')
            if phase:
                first=self.display_snapshots[0]['decoded'];need(decoded['target_device']==first['target_device'] and decoded['display_identity']==first['display_identity'] and decoded['window_generation']==first['window_generation'],'same physical display identity across device lifetime')
            self.binding_validator(check)
            check['accepted']=True
        finally:
            self.u.context_restore(saved);self.put(ptd,ptd_bytes)
            final_ptd=yield('MEM_READ',self.native(ptd),116);check['final_PTD_readback']=final_ptd;need(final_ptd['hex']==ptd_bytes.hex(),'actual PTD read back even on display failure')
            if out:
                freed=yield('MEM_FREE',out);check['free_receipt']=freed;need(freed['result']==1,'display output explicitly freed');check['temporary_freed']=True
            last=yield('GetLastError',);check['last_error_readback']=last;need(last['result']==error,'original LastError retained after supplemental display cleanup')
            check['CPU57_after']=self.state()['cpu'];check['CPU57_restored']=check['CPU57_after']==cpu;need(check['CPU57_restored'],'complete original CPU57 restored including EAX')
            check['wire_end']=len(self.owner.trace)
