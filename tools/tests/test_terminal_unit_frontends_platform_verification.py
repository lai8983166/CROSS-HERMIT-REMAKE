"""Bounded real-leaf/independent ABI fixtures; no native lifetime is run."""
import copy
import hashlib
import struct
import unittest
from pathlib import Path
from types import SimpleNamespace

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn import x86_const as x86
from tools.terminal_unit_frontends_trace import Replay, CPU_REGISTERS
from tools import terminal_unit_frontends_platform_verification as v

ROOT = Path(__file__).resolve().parents[2]
CODE = (ROOT/'analysis/hermit_game.exe').read_bytes()
STACK = 0x12000000


class Mirror(Replay):
    def __init__(self):
        self.u = Uc(UC_ARCH_X86, UC_MODE_32)
        self.x86 = x86
        self.register_names = CPU_REGISTERS
        self.mutable = []
        self.u.mem_map(0x400000,(len(CODE)+4095)&-4096)
        self.u.mem_write(0x400000,CODE)
        self.u.mem_map(STACK,0x20000)
        self.u.mem_map(0x12A00000,0x10000)
        self.u.reg_write(x86.UC_X86_REG_EBP,STACK+0x18000)
        self.u.reg_write(x86.UC_X86_REG_EFLAGS,0x202)

    def call(self, pc, ret, args):
        sp = STACK+0xF000
        self.u.mem_write(sp,struct.pack('<'+'I'*(len(args)+1),ret,*args))
        self.u.reg_write(x86.UC_X86_REG_ESP,sp)
        self.u.reg_write(x86.UC_X86_REG_EIP,pc)
        return sp

    def apply_fixture(self, actions):
        for a in actions:
            if a['kind']=='mem_map':self.u.mem_map(a['address'],a['bytes'],a['permission'])
            elif a['kind']=='mem_write':self.u.mem_write(a['address'],bytes.fromhex(a['hex']))
            elif a['kind']=='reg_write':self.u.reg_write(a['register'],a['value'])
            else:raise AssertionError(a)


def identity(p, slots):
    return dict(pointer=p,vtable=p+0x100,methods={str(s):p+0x200+i*4 for i,s in enumerate(slots)})


def wire(op, result, **args):
    return dict(request=dict(id=1,op=op,**args),reply=dict(id=1,ok=True,result=result))


def fixture(crt=(), gpu=(), extra=()):
    device = identity(0x10000000,[80])
    ledger = [dict(domain='overlay',native=p,guest=0x64001000+i*0x100000)
              for i,p in enumerate((device['pointer'],device['vtable'],device['methods']['80']))]
    ledger += list(extra)
    return dict(unit_frontends=dict(initial_platform=dict(
        CRT=dict(pointer_bytes=4,heap=0,critical=0,critical_hex='',GPU_created=False,
                 window_created=False,directory='F:\\installed'),
        GPU=dict(pointer_bytes=4,window_visible=False,max_textures=1024,max_creates=1024,device=device),
        device=device),image_input=dict(projection=[])),
        typed_GPU_projection=ledger,CRT_trace=list(crt),GPU_trace=list(gpu))


def event(r, effects, value, pop, end, channel='CRT'):
    before = r.cpu(); sp=before['ESP']; ret=v.word(r.read(sp,4))
    changes={k:w for k,w in dict(EAX=value,ESP=sp+4+pop,EIP=ret).items() if before[k]!=w}
    return dict(pc=before['EIP'],before_CPU=before,effects=effects,CPU_changes=changes,
                stop=False,continues_guest=False,
                wire={k:[0,end if k==channel else 0] for k in ('CRT','GPU','GDI','TLS')})


def returns(sp, ret, pop, value):
    return [dict(kind='reg_write',register=getattr(x86,'UC_X86_REG_'+n),value=w)
            for n,w in (('EAX',value),('ESP',sp+4+pop),('EIP',ret))]


class PlatformTests(unittest.TestCase):
    def test_CRT_allocate_open_complete_read_close_free(self):
        raw=bytes(262208);data=b'independently supplied source file'+bytes(262168-34)
        self.assertEqual(len(data),262168)
        p=0x50001000;native=0x12350000;handle=0x33440000
        after=raw[:32]+data+raw[32+len(data):];poison=bytes([0xDD])*len(raw)
        path='data\\adv\\bin\\sc001.bin'
        transcript=[
            wire('alloc',dict(pointer=native,bytes=len(raw),hex=raw.hex()),heap=0x12340000,flags=0,bytes=len(raw)),
            wire('open',dict(handle=handle),path=path,access=0x80000000,share=1,security=0,disposition=3,attributes=1,template=0),
            wire('sync',dict(pointer=native,hex=raw.hex()),pointer=native,hex=raw.hex()),
            wire('read',dict(value=1,read=len(data),pointer=native,before_hex=raw.hex(),after_hex=after.hex()),
                 handle=handle,pointer=native,offset=32,bytes=len(data),overlapped=0),
            wire('file_close',dict(value=1),handle=handle),
            wire('sync',dict(pointer=native,hex=poison.hex()),pointer=native,hex=poison.hex()),
            wire('free',dict(value=1,pointer=native,before_hex=poison.hex()),heap=0x12340000,flags=0,pointer=native)]
        for i,t in enumerate(transcript):t['request']['id']=t['reply']['id']=i+1
        row=fixture(crt=transcript);r=Mirror();check=v.PlatformVerifier(row,CODE,{path:data})
        check.heap=0x12340000;check.depth=1
        def leaf(slot,args,value,outputs,start,end):
            _,pop,ret=v.IMPORTS[slot];target=v.word(CODE,slot-0x400000);sp=r.call(target,ret,args)
            acts=outputs+returns(sp,ret,pop,value);e=event(r,acts,value,pop,end)
            e['wire']['CRT'][0]=start
            check.validate_event(r,e);r.apply_fixture(acts)
        leaf(0x592144,[v.HEAP,0,len(raw)],p,[dict(kind='mem_map',address=p,bytes=0x41000,permission=7),
             dict(kind='mem_write',address=p,hex=raw.hex())],0,1)
        self.assertIn((p,p+len(raw)),r.mutable)
        r.u.mem_write(0x12A03000,path.encode()+b'\0')
        leaf(0x5921EC,[0x12A03000,0x80000000,1,0,3,1,0],0x62001000,[],1,2)
        count=STACK+0x19000
        target=v.word(CODE,0x5921E8-0x400000);sp=r.call(target,0x42AD82,[0x62001000,p+32,len(data),count,0])
        acts=[dict(kind='mem_write',address=p,hex=after.hex()),dict(kind='mem_write',address=count,hex=struct.pack('<I',len(data)).hex())]+returns(sp,0x42AD82,20,1)
        e=event(r,copy.deepcopy(acts),1,20,4);e['wire']['CRT'][0]=2
        # Mutate real ReadFile effect bytes while both raw wire and independently
        # supplied source remain intact: the complete buffer comparison rejects.
        bad=copy.deepcopy(e);bad['effects'][0]['hex']=bad['effects'][0]['hex'][:-2]+'01'
        old=copy.deepcopy(check)
        with self.assertRaises(ValueError):old.validate_event(r,bad)
        check.validate_event(r,e);r.apply_fixture(acts)
        self.assertEqual(r.read(p+32,len(data)),data)
        leaf(0x592270,[0x62001000],1,[],4,5)
        r.u.mem_write(p,poison)
        leaf(0x592258,[v.HEAP,0,p],1,[],5,7)
        self.assertFalse(check.blocks);self.assertFalse(check.open_files)
        self.assertNotIn((p,p+len(raw)),r.mutable)

    def test_original_heap_leaf_effects_and_tampering(self):
        # Execute the existing original bridge implementation, rather than
        # manufacturing the expected source effects with the new verifier.
        from tools.school_crt_init_fixture import Guest
        source = Mirror(); target=v.word(CODE,0x59212C-0x400000)
        source.u.mem_write(0x80AB28,bytes(4)); source.call(target,0x57B9EA,[0,4096,0])
        before=source.cpu(); actions=[]
        original=source.u.reg_write
        def record(reg,value):
            actions.append(dict(kind='reg_write',register=reg,value=value)); original(reg,value)
        source.u.reg_write=record
        transcript=[]
        def request(op,**args):
            result=dict(pointer=0x12340000); transcript.append(wire(op,result,**args)); return result
        g=object.__new__(Guest); g.u=source.u; g.live=SimpleNamespace(trace=transcript,hello={},request=request)
        g.declaration=dict(heap_token_translation=dict(native=0)); g.api_calls=[]
        g.api(0x59212C)
        row=fixture(crt=transcript)
        for mutation in (None,'value','register','extra','CPU','wire'):
            r=Mirror();r.u.mem_write(0x80AB28,bytes(4));r.call(target,0x57B9EA,[0,4096,0])
            verifier=v.PlatformVerifier(row,CODE,{})
            e=event(r,copy.deepcopy(actions),v.HEAP,12,1)
            self.assertEqual(e['before_CPU'],before)
            if mutation=='value':e['effects'][0]['value']+=4
            if mutation=='register':e['effects'][0]['register']=x86.UC_X86_REG_EBX
            if mutation=='extra':e['effects'].insert(0,dict(kind='mem_write',address=0x80AB28,hex='01000000'))
            if mutation=='CPU':e['CPU_changes']['EBX']=1
            if mutation=='wire':e['wire']['GPU'][1]=1
            if mutation:
                with self.subTest(mutation=mutation),self.assertRaises(ValueError): verifier.validate_event(r,e)
            else:
                verifier.validate_event(r,e)
                self.assertEqual(verifier.heap,0x12340000)

    def test_real_overlay_critical_normalization_effects(self):
        from tools.school_crt_init_fixture import Guest
        from tools.terminal_overlay_emulation import OverlayMachine
        r=Mirror();target=v.word(CODE,0x59227C-0x400000);r.call(target,0x576F89,[0x80A4B0])
        raw=struct.pack('<6I',0x11110000,0xFFFFFFFF,0,0,0,0)
        t=wire('initialize',dict(pointer=0x12345000,hex=raw.hex()),guest=0x80A4B0)
        actions=[]
        for name in ('reg_write','mem_write'):
            original=getattr(r.u,name)
            def wrap(*args,_name=name,_original=original):
                actions.append(dict(kind=_name,register=args[0],value=args[1]) if _name=='reg_write' else
                               dict(kind=_name,address=args[0],hex=bytes(args[1]).hex()))
                return _original(*args)
            setattr(r.u,name,wrap)
        transcript=[]
        def request(op,**args): transcript.append(t);return t['reply']['result']
        g=object.__new__(Guest);g.u=r.u;g.live=SimpleNamespace(trace=transcript,hello={},request=request)
        g.api_calls=[];g.criticals={};g.allocations={}
        m=SimpleNamespace(crt=g,uc=r.u,mutable=[],crt_apis=[])
        OverlayMachine.api_crt(m,0x59227C)
        self.assertEqual([a['kind'] for a in actions],['mem_write']+['reg_write']*3+['mem_write'])
        check=Mirror();check.call(target,0x576F89,[0x80A4B0]);row=fixture(crt=[t])
        e=event(check,actions,0,4,1);v.PlatformVerifier(row,CODE,{}).validate_event(check,e)
        e=copy.deepcopy(e);e['effects'][-1]['hex']=raw.hex()
        with self.assertRaises(ValueError):v.PlatformVerifier(row,CODE,{}).validate_event(check,e)

    def test_modern_opaque_lock_count_and_owner_checked(self):
        guest=0x80A4B0;native=0x12345000;thread=0x2233
        raw=struct.pack('<6I',0x11110000,0xFFFFFFFE,1,thread,0,0)
        q=wire('enter',dict(depth=1,critical_hex=raw.hex()),critical=native)
        for bad in (False,True):
            r=Mirror();target=v.word(CODE,0x592234-0x400000);sp=r.call(target,0x5770D3,[guest])
            normalized=bytearray(raw)
            for off in (0,12):struct.pack_into('<I',normalized,off,0x63000000+off+(guest-0x80A480)*0x100)
            acts=[dict(kind='mem_write',address=guest,hex=raw.hex())]+returns(sp,0x5770D3,4,0)+[
                dict(kind='mem_write',address=guest,hex=normalized.hex())]
            p=v.PlatformVerifier(fixture(crt=[q]),CODE,{})
            p.locks[guest]=native;p.lock_spins[guest]=0
            if bad:p.native_thread=thread+1
            e=event(r,acts,0,4,1)
            if bad:
                with self.assertRaises(ValueError):p.validate_event(r,e)
            else:p.validate_event(r,e)

    def test_IAT_and_original_caller_rejected(self):
        target=v.word(CODE,0x59212C-0x400000)
        for bad in ('IAT','caller'):
            r=Mirror();sp=r.call(target,0x57B9EA+(bad=='caller'),[0,4096,0]);r.u.mem_write(0x80AB28,bytes(4))
            e=event(r,returns(sp,0x57B9EA,12,v.HEAP),v.HEAP,12,1)
            if bad=='IAT':r.u.mem_write(0x59212C,struct.pack('<I',target+4))
            p=v.PlatformVerifier(fixture(crt=[wire('heap_create',dict(pointer=0x12340000),flags=0,initial=4096,maximum=0)]),CODE,{})
            with self.assertRaises(ValueError):p.validate_event(r,e)

    def gpu_create_fixture(self):
        native=identity(0x11000000,[8,56,64,68]); domain='overlay-unit-frontends-0-0'
        values=[native['pointer'],native['vtable'],*native['methods'].values(),0x11800000]
        ledger=[dict(domain=domain,native=p,guest=0x34000000+(i+1)*0x1000 if i<6 else 0x34010000)
                for i,p in enumerate(values)]
        row=fixture(gpu=[wire('create',dict(hr=0,texture=native),width=2,height=2,levels=1,usage=0,format=25,pool=1)],extra=ledger)
        p=v.PlatformVerifier(row,CODE,{})
        r=Mirror();device=p.device
        for a in (device['pointer'],device['vtable'],*device['methods'].values()):r.u.mem_map(a&-4096,4096)
        r.u.mem_write(device['pointer'],struct.pack('<I',device['vtable']))
        r.u.mem_write(device['vtable']+80,struct.pack('<I',device['methods']['80']))
        record=0x12A02000;sp=r.call(device['methods']['80'],0x403C8A,[device['pointer'],2,2,1,0,25,1,record+44])
        actions=[dict(kind='mem_map',address=0x34000000+i*4096,bytes=4096,permission=7) for i in range(1,7)]
        actions.append(dict(kind='mem_write',address=0x34001000,hex=struct.pack('<I',0x34002000).hex()))
        for i,slot in enumerate((8,56,64,68)):
            actions.append(dict(kind='mem_write',address=0x34002000+slot,hex=struct.pack('<I',0x34003000+i*4096).hex()))
        actions.append(dict(kind='mem_write',address=record+44,hex=struct.pack('<I',0x34001000).hex()))
        actions+=returns(sp,0x403C8A,32,0)
        return row,p,r,event(r,actions,0,32,1,'GPU')

    def test_GPU_create_exact_effects_and_mapping_tamper(self):
        row,p,r,e=self.gpu_create_fixture();p.validate_event(r,e)
        self.assertEqual(len(p.textures),1)
        for kind in ('map','bytes','output','extra'):
            _,p,r,e=self.gpu_create_fixture()
            if kind=='map':e['effects'][0]['address']+=0x10000
            if kind=='bytes':e['effects'][0]['bytes']*=2
            if kind=='output':e['effects'][-4]['hex']='00000000'
            if kind=='extra':e['effects'].insert(0,dict(kind='mem_unmap',address=0x400000,bytes=4096))
            with self.subTest(kind=kind),self.assertRaises(ValueError):p.validate_event(r,e)

    def test_GPU_current_vtable_not_diagnostic_label(self):
        _,p,r,e=self.gpu_create_fixture()
        r.u.mem_write(p.device['vtable']+80,bytes(4));e['boundary']=dict(kind='GPU',vtable_slot=80)
        with self.assertRaises(ValueError):p.validate_event(r,e)

    def test_GPU_descriptor_lock_upload_readback_release(self):
        row,_,_,_=self.gpu_create_fixture()
        native=0x11000000;before=bytes(8);upload=bytes(range(8));desc=struct.pack('<8I',25,1,0,1,8,0,2,2)
        row['GPU_trace'] += [wire('describe',dict(hr=0,hex=desc.hex(),width=2,height=2,size=8),pointer=native),
            wire('lock',dict(hr=0,pitch=4,bits=0x11800000,hex=before.hex()),pointer=native,flags=2048),
            wire('unlock',dict(hr=0,uploaded_sha256=hashlib.sha256(upload).hexdigest()),pointer=native,hex=upload.hex()),
            wire('readback',dict(hr=0,unlock_hr=0,pitch=4,hex=upload.hex(),sha256=hashlib.sha256(upload).hexdigest()),pointer=native),
            wire('release',dict(count=0),pointer=native)]
        for i,t in enumerate(row['GPU_trace']):t['request']['id']=t['reply']['id']=i+1
        _,_,r,create=self.gpu_create_fixture();p=v.PlatformVerifier(row,CODE,{})
        p.validate_event(r,create);r.apply_fixture(create['effects'])
        tex=0x34001000;bp=r.cpu()['EBP'];lockout=STACK+0x1A000;r.u.mem_write(bp+8,struct.pack('<I',lockout))
        def leaf(slot,ret,args,outputs,start,end):
            pc=p.textures[tex]['identity']['methods'][str(slot)]
            sp=r.call(pc,ret,args);acts=outputs+returns(sp,ret,v.GPU_POP[slot],0)
            e=event(r,acts,0,v.GPU_POP[slot],end,'GPU');e['wire']['GPU'][0]=start
            p.validate_event(r,e);r.apply_fixture(acts)
        leaf(56,0x403CBE,[tex,0,bp-52],[dict(kind='mem_write',address=bp-52,hex=desc.hex())],1,2)
        leaf(64,0x40395E,[tex,0,lockout,0,2048],
             [dict(kind='mem_map',address=0x34010000,bytes=4096,permission=7),
              dict(kind='mem_write',address=0x34010000,hex=before.hex()),
              dict(kind='mem_write',address=lockout,hex=struct.pack('<II',4,0x34010000).hex())],2,3)
        self.assertIn((0x34010000,0x34010008),r.mutable)
        r.u.mem_write(0x34010000,upload)
        leaf(68,0x4039D3,[tex,0],[],3,5)
        leaf(8,0x40378D,[tex],[],5,6)
        self.assertFalse(p.textures);self.assertFalse(p.intervals)
        self.assertNotIn((0x34010000,0x34010008),r.mutable)

    def test_projection_address_and_alias_rejected(self):
        row,_,r,e=self.gpu_create_fixture()
        row['typed_GPU_projection'][3]['guest']=0x12000000
        with self.assertRaises(ValueError):v.PlatformVerifier(row,CODE,{}).validate_event(r,e)
        row,_,r,e=self.gpu_create_fixture()
        row['typed_GPU_projection'][4]['guest']=row['typed_GPU_projection'][3]['guest']
        with self.assertRaises(ValueError):v.PlatformVerifier(row,CODE,{}).validate_event(r,e)

    def test_surface_extent_alias_and_overflow_rejected(self):
        row,p,_,_=self.gpu_create_fixture()
        self.assertEqual(p.surface('overlay-unit-frontends-0-0',0x11800000,8),0x34010000)
        with self.assertRaises(ValueError):p.surface('overlay-unit-frontends-0-0',0x11800000,8)
        with self.assertRaises(ValueError):p.surface('overlay-unit-frontends-0-0',0x11800000,0x40001)
        row,p,_,_=self.gpu_create_fixture();p.projections[('overlay-unit-frontends-0-0',0x11800000)]=0x3BA00000
        with self.assertRaises(ValueError):p.surface('overlay-unit-frontends-0-0',0x11800000,0x20000)

    def test_GPU_readback_entire_padding_rejected(self):
        raw=bytes.fromhex('01020304000000000506070800000000')
        t=dict(native=0x11000000,upload=raw,pitch=8,locked=False)
        good=dict(hr=0,unlock_hr=0,pitch=8,hex=raw.hex(),sha256=hashlib.sha256(raw).hexdigest())
        for kind in ('good','padding','hash','pitch'):
            q=copy.deepcopy(good)
            if kind=='padding':q['hex']=q['hex'][:-2]+'01'
            if kind=='hash':q['sha256']='0'*64
            if kind=='pitch':q['pitch']=4
            p=v.PlatformVerifier(fixture(gpu=[wire('readback',q,pointer=t['native'])]),CODE,{})
            if kind=='good':p.readback(t)
            else:
                with self.subTest(kind=kind),self.assertRaises(ValueError):p.readback(t)

    def test_unimplemented_GDI_TLS_fail_closed(self):
        r=Mirror();r.call(0x77010000,0x401000,[]);e=event(r,[],0,0,0)
        e['boundary']=dict(kind='CRT',import_slot=0x59212C)
        p=v.PlatformVerifier(fixture(),CODE,{})
        self.assertFalse(p.handles(r,e))
        with self.assertRaisesRegex(ValueError,'unsupported boundary'):p.validate_event(r,e)

    def test_wire_request_and_close_ownership_rejected(self):
        p=v.PlatformVerifier(fixture(),CODE,{})
        with self.assertRaises(ValueError):p.finish(Mirror())
        target=v.word(CODE,0x59212C-0x400000);r=Mirror();r.u.mem_write(0x80AB28,bytes(4));sp=r.call(target,0x57B9EA,[0,4096,0])
        row=fixture(crt=[wire('heap_create',dict(pointer=0x12340000),flags=1,initial=4096,maximum=0)])
        p=v.PlatformVerifier(row,CODE,{})
        with self.assertRaises(ValueError):p.validate_event(r,event(r,returns(sp,0x57B9EA,12,v.HEAP),v.HEAP,12,1))

    def test_normal_empty_owner_close_and_split_projection(self):
        close_CRT=dict(all_owned_resources_released=True,heap_destroyed=True,critical_deleted=True,
                       open_files=0,allocations=0,depth=0,forced_cleanup=False)
        close_GPU=dict(texture_releases=[],device_release_count=0,factory_release_count=0,
                       window_destroyed=True,all_owned_resources_released=True)
        row=fixture(crt=[wire('close',close_CRT)],gpu=[wire('close',close_GPU)])
        row['unit_frontends']['image_input']['projection']=copy.deepcopy(row['typed_GPU_projection'])+[
            dict(domain='overlay-unit-frontends-0-0',native=0x11000000,guest=0x34001000)]
        p=v.PlatformVerifier(row,CODE,{})
        self.assertEqual(len(p.projections),4)
        self.assertEqual(p.finish(Mirror())['wire'],dict(CRT=1,GPU=1))
        row['unit_frontends']['image_input']['projection'][0]['guest']+=4096
        with self.assertRaises(ValueError):v.PlatformVerifier(row,CODE,{})


if __name__ == '__main__':
    unittest.main()
