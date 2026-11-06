"""Independent raw-clock/TLS contracts and fresh owned GDI API effects."""
import copy
import ctypes
import struct
import types
from types import SimpleNamespace

from unicorn import x86_const as x86
from tools import terminal_unit_frontends_emulation as source
from tools import battle_hit_damage_emulation as combat
from tools import battle_terminal_selection_emulation as selection
from tools import terminal_task_emulation as task
from tools import terminal_name_emulation as names
from tools import terminal_last_dialogue_gdi as lifetime


def need(ok,message):
    if not ok:
        raise ValueError(message)


def word(replay,address):
    return struct.unpack('<I',replay.read(address,4))[0]


def text(replay,address,maximum=4096):
    result=bytearray()
    for i in range(maximum):
        b=replay.read(address+i,1)[0]
        if not b:return bytes(result)
        result.append(b)
    raise ValueError('unterminated bounded Win32 input string')


def return_effects(replay,value,pop):
    sp=replay.cpu()['ESP']
    return [dict(kind='reg_write',register=reg,value=v)
            for reg,v in ((x86.UC_X86_REG_EAX,value & 0xFFFFFFFF),
                          (x86.UC_X86_REG_ESP,sp+4+pop),
                          (x86.UC_X86_REG_EIP,word(replay,sp)))]


class OtherLeaves:
    def __init__(self,row):
        self.row=row
        self.ticks=iter(source.clock_inputs()[row['input']['name']])
        self.clock_count=self.tls_count=self.task_count=0
        self.common_count=0
        self.application_receivers={}
        self.last_error=0x1234
        self.kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        self.kernel.lstrcmpA.argtypes=[ctypes.c_char_p,ctypes.c_char_p]
        self.kernel.lstrcmpA.restype=ctypes.c_int
        self.kernel.lstrlenA.argtypes=[ctypes.c_char_p]
        self.kernel.lstrlenA.restype=ctypes.c_int

    def handles(self,replay,event):
        if (word(replay,0x5922C4)==event['pc'] and
                word(replay,replay.cpu()['ESP'])==0x41F416):return True
        return event['pc'] in combat.APIS or event['pc'] in selection.APIS or (
            event['pc'] in task.APIS and word(replay,replay.cpu()['ESP'])==task.APIS[event['pc']][2])

    def validate_event(self,replay,event):
        pc=event['pc'];sp=replay.cpu()['ESP'];ret=word(replay,sp)
        if pc==word(replay,0x5922C4) and ret==0x41F416:
            need(word(replay,sp+4)==0x594734 and text(replay,0x594734)==b'Dm-No-MakeTex',
                 'exact original COMMON marker string and caller')
            value=int(self.kernel.lstrlenA(b'Dm-No-MakeTex'))
            need(value==13,'actual original marker byte length')
            self.common_count+=1;pop=4
        elif pc in combat.APIS:
            name,n,caller=combat.APIS[pc]
            need(ret==caller,'exact original TLS leaf caller')
            args=[word(replay,sp+4+4*i) for i in range(n)]
            creation=self.row['platform']['creation']
            observed=self.row['platform']['trace'][self.tls_count]
            if name=='GetLastError':value=self.last_error
            elif name=='TlsGetValue':
                need(args==[51] and creation['guest_index']==51 and creation['guest_token']==combat.TLS,
                     'owned TLS index and guest token role')
                value=combat.TLS
            else:value=0
            after=(0 if name=='TlsGetValue' else args[0] if name=='SetLastError' else self.last_error)
            expected=dict(name=name,guest_args=args,value=value,error_before=self.last_error,error_after=after,
                          actual_native_index=creation['native_index'] if name=='TlsGetValue' else None,
                          actual_API_executed=True,void_EAX_normalized=name=='SetLastError')
            need(observed==expected,'independent full owned TLS receipt and LastError transition')
            self.last_error=after;self.tls_count+=1;pop=4*n
        elif pc in selection.APIS:
            name,n,caller=selection.APIS[pc]
            need(ret==caller,'exact original condition Win32 leaf caller')
            if name=='GetTickCount':
                try:value=next(self.ticks)
                except StopIteration:raise ValueError('captured clock stream exhausted')
                self.clock_count+=1
            else:
                strings=[text(replay,word(replay,sp+4+4*i)) for i in range(2)]
                # Win32 applies locale collation even to ASCII. Execute an
                # independent actual query instead of substituting byte order.
                value=int(self.kernel.lstrcmpA(*strings))
            pop=n*4
        else:
            need(pc in task.APIS,'declared original task text/IME leaf')
            name,slot,caller=task.APIS[pc]
            need(word(replay,slot)==pc and ret==caller,'exact task original IAT/caller')
            argument=word(replay,sp+4)
            if name=='ImmGetOpenStatus':
                need(argument==word(replay,source.APPLICATION_INPUT+8)==0,'original null IME input')
                value=0
            else:
                actual_this=word(replay,replay.cpu()['EBP']-4)
                need(actual_this==word(replay,0x7A4A00)+0x180
                     and argument==actual_this+0x528 and text(replay,argument)==b'',
                     'original application CInput receiver and genuinely empty member text')
                value=0
                key=hex(actual_this)
                self.application_receivers[key]=self.application_receivers.get(key,0)+1
            self.task_count+=1;pop=4
        need(event['effects']==return_effects(replay,value,pop)
             and not event['stop'] and not event['continues_guest'],
             'only independently validated Win32 return effects')

    def finish(self):
        need(self.tls_count==len(self.row['platform']['trace']),'all actual TLS leaves consumed')
        need(next(self.ticks,None) is None,'entire fixed raw clock stream consumed')
        creation=self.row['platform']['creation'];cleanup=self.row['platform']['cleanup']
        need(creation['actual_set_and_readback'] and creation['pointer_is_guest_token_not_native_dereference']
             and creation['thread']==cleanup['thread'] and creation['native_index']==cleanup['native_index']
             and cleanup['actual_clear'] and cleanup['actual_free'] and cleanup['freed_readback']==0
             and not cleanup['forced_cleanup'],'one actual owned and normally closed native TLS lifetime')
        reported=self.row['unit_frontends']['application_text']
        need(reported['receivers']==self.application_receivers
             and reported['calls']==sum(self.application_receivers.values()),
             'actual independently observed application text receiver counts')
        return dict(TLS=self.tls_count,clock=self.clock_count,task_text=self.task_count,
                    COMMON_marker_strings=self.common_count)


class BufferedMemory:
    """Stage independent native outputs without applying any source effects."""
    def __init__(self,replay):
        self.replay=replay
        self.actions=[]

    def mem_regions(self):
        regions=list(self.replay.u.mem_regions())
        return sorted(regions+[(a['address'],a['address']+a['bytes']-1,a['permission'])
                              for a in self.actions if a['kind']=='mem_map'])

    def mem_map(self,address,size,permission=7):
        need(address%4096==0 and size>0 and size%4096==0
             and all(not(a<address+size and address<=b) for a,b,_ in self.mem_regions()),
             'fresh complete independently owned GDI raster span')
        self.actions.append(dict(kind='mem_map',address=address,bytes=size,permission=permission))

    def mem_write(self,address,raw):
        self.actions.append(dict(kind='mem_write',address=address,hex=bytes(raw).hex()))


class GDI:
    """Execute each real GDI leaf against independent replay input bytes.

    The frozen native transport owns new objects. Only opaque handle roles use
    the fixed identity plan; a separate chronological auditor verifies the
    submitted native trace/lifetimes. Pixels and sizes come from these new APIs.
    """
    def __init__(self,row):
        self.row=row
        self.platform=names.NativeGDI()
        plan=lifetime.fixed_plan(source.ROOT)
        case=next(c for c in plan['cases'] if c['name']==row['input']['name'])
        self.owner=lifetime.LifetimeGDI(self.platform,case,lifetime.plan_reference(source.ROOT),lambda:True)
        self.ordinal=0
        self.used_rasters=set()

    def handles(self,replay,event):
        return any(word(replay,slot)==event['pc'] for slot in names.GDI)

    def validate_event(self,replay,event):
        bindings=[(slot,*row) for slot,row in names.GDI.items() if word(replay,slot)==event['pc']]
        need(len(bindings)==1,'one actual original GDI IAT identity')
        slot,name,caller,pop=bindings[0]
        sp=replay.cpu()['ESP'];ret=word(replay,sp)
        if name=='CreateFontA':need(ret in (0x4CA7CB,0x4CAD09),'original name/dialogue font caller')
        elif caller is not None:need(ret==caller,'original GDI ABI caller')
        args=[word(replay,sp+4+i) for i in range(0,pop,4)]
        trace=self.row['GDI_trace'][self.ordinal]
        need(trace['name']==name and trace['args']==args,'GDI receipt bound to independent current stack')
        memory=BufferedMemory(replay)
        adapter=SimpleNamespace(u=memory,read=replay.read,cpu=replay.cpu)
        if name=='CreateDIBSection':
            address=trace['native_result']['guest_bits']
            need(address%0x100000==0 and 0x3E000000<=address<=0x3F300000
                 and address not in self.used_rasters,'bounded unique declared offscreen DIB address')
            self.used_rasters.add(address)
            fn=self.platform.service.call_raster
            self.platform.service.call_raster=types.MethodType(types.FunctionType(
                fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=address)),self.platform.service)
        observed=self.owner.call(adapter,name,args,ret)
        native=trace['native_result']
        if name=='CreateDIBSection':
            bits=native.get('native_bits')
            need(type(bits) is int and 0<bits<2**(8*ctypes.sizeof(ctypes.c_void_p)),
                 'valid current-host opaque DIB bits identity')
        excluded={'args','dc_translated_args','result','native_bits','actual_API_executed'}
        need({k:v for k,v in native.items() if k not in excluded} ==
             {k:v for k,v in observed.items() if k not in excluded},
             'all submitted native GDI sizes/pixels/status buffers equal new real APIs')
        need(trace['logical_result']==observed['result'], 'GDI logical return bound to exact independent role')
        if name not in lifetime.HANDLE_RESULTS:
            need(native['result']==observed['result'],'GDI non-handle native result preserved')
        else:
            need(type(native['result']) is int and native['result'] not in (0,-1,0xFFFFFFFF),
                 'valid submitted current native GDI identity')
        expected=memory.actions+return_effects(replay,observed['result'],pop)
        need(event['effects']==expected and not event['stop'] and not event['continues_guest'],
             'entire independently executed current GDI output and return effects')
        for action in memory.actions:
            if action['kind']=='mem_map':
                replay.mutable.append((action['address'],action['address']+action['bytes']))
        self.ordinal+=1

    def close(self):
        return self.owner.close()

    def finish(self):
        need(self.ordinal==len(self.row['GDI_trace']),'every reported GDI call independently executed')
        self.close()
        return dict(calls=self.ordinal,fresh_native_GDI_API_outputs_compared=True)
