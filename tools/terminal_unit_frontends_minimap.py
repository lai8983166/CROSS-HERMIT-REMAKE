"""Bounded MAP05 minimap initialization through original packet/bitmap roots.

The accepted battle fixture already declares the real MAP05 logical header and
SEEN/VISIBLE buffers. The complete matching BMP is a new early immutable-file
input copied to guest RAM; its original in-memory bitmap loader executes. This
is deliberately not a claim that the complete original map file loader ran.
Native smoke is owned by the caller; importing/configuring never creates GPU
objects or changes any old fixture record, visibility byte or activation gate.
"""
import copy
import hashlib
import struct
from functools import lru_cache

from tools import terminal_unit_frontends_images as images

ROOT, CODE = images.ROOT, images.CODE
MAIN, CTRL = images.MAIN, images.CTRL
MAP = CTRL+0x3D68
BACKGROUND, FOG = MAP+0x2648C, MAP+0x2650C
BMP_POINTER = 0x3C200000
BMP_PATH = 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP/MAP05.BMP'
BMP_SHA = '123ae60bdf213a0e70b51112f6795923eab29979f9cd83aaf5c0ea1a43fc7b2e'
HEADER_SHA = 'bb8ef4d51cc3228cf38cda21435030a5dd6d9955a303ef445d46508c5fa11c45'
POOL, STRIDE, BITS_OFFSET, MAX_SURFACE = 0x3C000000, 0x100000, 0x20000, 0x80000
DOMAINS = ('unit-frontends-minimap-background', 'unit-frontends-minimap-fog')
# Exact half-open full original function extents, excluding assertion padding.
EXTRA_RANGES = ((0x404870,0x4048C2),(0x4404A0,0x4406E7),
                (0x440A10,0x440AEE),(0x440AF0,0x440C0A),
                (0x440C10,0x440D31),(0x440F00,0x440FD3),
                (0x441170,0x441270),(0x410680,0x410730),
                (0x425620,0x425780),(0x4096D0,0x409769),
                (0x457C40,0x457CFA),(0x457D00,0x457DFE),
                (0x458280,0x45837E))
MUTABLE = ((MAP+0x2646C,MAP+0x26594),)
BMP_MUTABLE = ((BMP_POINTER+0x2E,BMP_POINTER+0x32),
               (BMP_POINTER+54,BMP_POINTER+1078))


def need(condition, message):
    if not condition:
        raise ValueError('minimap: '+message)


@lru_cache(maxsize=1)
def asset():
    raw = (ROOT/BMP_PATH).read_bytes()
    need(len(raw)==23094 and hashlib.sha256(raw).hexdigest()==BMP_SHA,
         'exact complete immutable MAP05 BMP')
    need(raw[:2]==b'BM' and struct.unpack_from('<ii',raw,18)==(172,128) and
         struct.unpack_from('<H',raw,28)[0]==8 and struct.unpack_from('<I',raw,10)[0]==1078,
         'actual complete BMP8 header/palette/pixel extent')
    return raw


def dimensions(header, bitmap):
    need(type(header) is bytes and len(header)>=16, 'complete declared logical MAP header')
    world_x,world_y,w,h=struct.unpack_from('<4h',header)
    need((world_x,world_y,w,h)==(2048,1536,64,96), 'matching real MAP05 logical dimensions')
    need(bitmap[:2]==b'BM' and struct.unpack_from('<ii',bitmap,18)==(172,128), 'matching MAP05 background dimensions')
    return dict(original_args=[w*32,h*16],logical_size=[172,128],texture_size=[256,128],
                nominal_pitch=512,nominal_surface_bytes=65536,fog_user_bytes=44032,
                cells=[w,h],world=[world_x,world_y])


def fog_pixels(header, seen, width=172, height=128):
    """Independent 440A10/440AF0 duplicate-pair A1R5G5B5 fog words.

    Each stored ratio is single precision; the x87 product of a <=172 integer
    and that 24-bit ratio is exactly representable in Python binary64 here.
    Division by the original constants32/16 is exact before truncation.
    """
    world_x,world_y,w,h=struct.unpack_from('<4h',header)
    need((world_x,world_y,w,h)==(2048,1536,64,96) and len(seen)==w*h and
         (width,height)==(172,128), 'bounded real MAP05 visibility sampling')
    f32=lambda value:struct.unpack('<f',struct.pack('<f',value))[0]
    scale_x,scale_y=f32(world_x/width),f32(world_y/height)
    out=bytearray(width*height*2)
    for y in range(height):
        sy=min(int(y*scale_y/16),h-1)
        for x in range(0,width,2):
            sx=min(int(x*scale_x/32),w-1)
            pixel=0 if seen[sy*w+sx] else 0x8000
            struct.pack_into('<HH',out,(y*width+x)*2,pixel,pixel)
    return bytes(out)


def fog_upload(header, seen, before, pitch):
    need(type(pitch) is int and 512<=pitch<=4096 and pitch%2==0 and
         len(before)==pitch*128<=MAX_SURFACE, 'entire real full-pitch fog surface')
    pixels=fog_pixels(header,seen)
    out=bytearray(before)
    for row in range(128):
        out[row*pitch:row*pitch+344]=pixels[row*344:(row+1)*344]
    return bytes(out)


class MinimapAddressSpace:
    """Independent two-record domain; never inserted in legacy GPU ledgers."""
    def __init__(self):
        self.identities={}
        self.reverse={}
        self.roles={}

    def guest(self,domain,native,bits=False,size=0):
        need(domain in DOMAINS and type(native) is int and 0<native<0xFFFFFFFF,
             'typed owned minimap x86 identity')
        key=domain,native
        if bits:
            need(0<size<=MAX_SURFACE, 'bounded entire minimap locked surface')
        if key in self.identities:
            need(self.roles[key]==bits,'native minimap surface/interface role alias refused')
        if key not in self.identities:
            base=POOL+DOMAINS.index(domain)*STRIDE
            if bits:
                need(0<size<=MAX_SURFACE, 'bounded entire minimap locked surface')
                address=base+BITS_OFFSET
            else:
                ordinal=sum(d==domain for d,p in self.identities)
                need(ordinal<15, 'bounded identity pages below full surface')
                address=base+(ordinal+1)*4096
            need(address not in self.reverse, 'minimap identity/surface alias refused')
            self.identities[key]=address;self.reverse[address]=key;self.roles[key]=bits
        return self.identities[key]

    def texture(self,domain,native):
        need(set(native)=={'pointer','vtable','methods'} and
             set(native['methods'])=={'8','56','64','68'}, 'complete native minimap texture interface')
        return dict(pointer=self.guest(domain,native['pointer']),vtable=self.guest(domain,native['vtable']),
                    methods={str(s):self.guest(domain,native['methods'][str(s)]) for s in (8,56,64,68)})

    def ledger(self):
        return [dict(domain=d,native=n,guest=p) for (d,n),p in self.identities.items()]


class MinimapMixin:
    """Before ImagesMixin; caller adds EXTRA_RANGES and initializes after CRT.

    configure_minimap_inputs(): constructor tail, before Recorder/first root.
    initialize_minimap(root=None): after original CRT roots, before first WORK.
    destroy_minimap(root=None): before unit-cache cleanup and CRT teardown.
    root uses resource_root(label,entry,args,receiver,cdecl) keyword contract.
    """
    def configure_minimap_inputs(self):
        need(not getattr(self,'minimap_configured',False) and self.mark()['instructions']==0,
             'minimap inputs precede the first original root')
        raw=asset();header_pointer=self.get(MAP+0x2659C)
        header=self.read(header_pointer,36880)
        need(hashlib.sha256(header).hexdigest()==HEADER_SHA,'same complete original MAP05 BIN input')
        shape=dimensions(header,raw)
        seen,visible=self.get(MAP+0xA0),self.get(MAP+0xA4)
        need(seen and visible and seen!=visible, 'existing distinct declared battle visibility buffers retained')
        self.read(seen,6144);self.read(visible,6144)
        for lo,hi in ((POOL,POOL+2*STRIDE),(BMP_POINTER,BMP_POINTER+0x6000)):
            need(all(not(a<hi and lo<=b) for a,b,p in self.uc.mem_regions()), 'disjoint minimap input/projection pools')
        need(self.read(BACKGROUND,256)==bytes(256), 'genuinely cold background/fog packet inputs')
        self.uc.mem_map(BMP_POINTER,0x6000,3);self.uc.mem_write(BMP_POINTER,raw)
        self.mutable+=list(MUTABLE)+list(BMP_MUTABLE)
        self.minimap_configured=True;self.minimap_initializing=self.minimap_cleaning=False
        self.minimap_current=None;self.minimap_space=MinimapAddressSpace()
        self.minimap_resources={};self.minimap_calls=[];self.minimap_roots=[];self.minimap_observers=[]
        self.minimap_cleanup=[]
        self.minimap_initialized=self.minimap_destroyed=False
        self.minimap_input=dict(source=dict(path=BMP_PATH,bytes=len(raw),sha256=BMP_SHA),
            header_pointer=header_pointer,header_bytes=len(header),header_sha256=HEADER_SHA,
            input_pointer=BMP_POINTER,input_bytes=len(raw),input_mapped_bytes=0x6000,
            original_palette_copy_writable=[BMP_POINTER+54,BMP_POINTER+1078],
            original_header_copy_writable=[BMP_POINTER+0x2E,BMP_POINTER+0x32],
            header_normalization=dict(original_entry=0x420A40,write_PC=0x420AA7,
                original_bytes='89512e',field='BITMAPINFOHEADER.biClrUsed',width=4,
                before=struct.unpack_from('<I',raw,0x2E)[0],
                derived_value=(struct.unpack_from('<I',raw,10)[0]-54)//4,
                condition='biBitCount is4 or8 and biClrUsed is0'),
            before_first_root=True,full_original_map_loader_executed=False,
            original_memory_bitmap_loader=0x404870,shape=shape,
            retained_visibility=dict(seen=seen,visible=visible,bytes=6144,
                seen_sha256=hashlib.sha256(self.read(seen,6144)).hexdigest(),
                visible_sha256=hashlib.sha256(self.read(visible,6144)).hexdigest()))

    def initialize_minimap(self,root=None):
        need(self.minimap_configured and not self.minimap_initialized and not self.minimap_resources,
             'one earliest original minimap initialization')
        call=root or self.resource_root
        self.minimap_initializing=True
        try:
            for label,record in (('background',BACKGROUND),('fog',FOG)):
                self.minimap_roots.append(dict(label='minimap_original_'+label+'_packet_constructor',entry=0x4075E0,receiver=record,args=[]))
                call(self.minimap_roots[-1]['label'],0x4075E0,receiver=record)
            call('minimap_original_empty_background_reset',0x407780,receiver=BACKGROUND)
            self.minimap_roots.append(dict(label='minimap_original_empty_background_reset',entry=0x407780,receiver=BACKGROUND,args=[]))
            self.minimap_current='background'
            args=[self.device_ptr,0,BMP_POINTER,1,1,1]
            call('minimap_original_memory_BMP8_loader',0x404870,args,receiver=BACKGROUND)
            self.minimap_roots.append(dict(label='minimap_original_memory_BMP8_loader',entry=0x404870,receiver=BACKGROUND,args=args))
            need(self.getreg('EAX')==0 and self.read(BACKGROUND+0x38,4)==struct.pack('<HH',172,128),
                 'original full background bitmap loaded')
            self.minimap_current='fog';args=self.minimap_input['shape']['original_args']
            call('minimap_original_dynamic_fog_initialization',0x4404A0,args,receiver=MAP)
            self.minimap_roots.append(dict(label='minimap_original_dynamic_fog_initialization',entry=0x4404A0,receiver=MAP,args=list(args)))
            need(self.getreg('EAX')==0 and self.get(MAP+0x2658C)!=0 and self.get(MAP+0x26590)==22016,
                 'original dynamic fog texture and full CRT pixel buffer initialized')
            self.minimap_initialized=True
        finally:
            self.minimap_current=None;self.minimap_initializing=False

    def api_crt(self,slot):
        if not (getattr(self,'minimap_initializing',False) or getattr(self,'minimap_cleaning',False)):
            return super().api_crt(slot)
        images.overlay.OverlayMachine.api_crt(self,slot)

    def gpu_api(self,at):
        slot=self.methods[at];sp=self.getreg('ESP');receiver=self.get(sp+4)
        owns=any(r['texture']['pointer']==receiver and r['alive'] for r in getattr(self,'minimap_resources',{}).values())
        if not (owns or slot==80 and getattr(self,'minimap_initializing',False)):
            return super().gpu_api(at)
        pop={80:32,56:12,64:20,68:8,8:4}[slot];bp=self.getreg('EBP');ret=self.get(sp)
        args=[self.get(sp+4+i) for i in range(0,pop,4)];outputs=[];start=len(self.gpu.trace)
        need(ret in {80:(0x403C8A,),56:(0x403CBE,0x403A44),64:(0x40395E,),68:(0x4039D3,),8:(0x40378D,)}[slot], 'original minimap COM caller')
        def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
        if slot==80:
            label=self.minimap_current
            need(label in ('background','fog') and label not in self.minimap_resources, 'one actual texture per minimap record')
            record=BACKGROUND if label=='background' else FOG
            need(args==[self.device_ptr,256,128,1,0,25,1,record+44], 'actual original minimap texture dimensions/ABI')
            native=self.gpu.create(256,128);domain=DOMAINS[0 if label=='background' else 1]
            t=self.minimap_space.texture(domain,native['texture'])
            r=dict(label=label,record=record,domain=domain,native=native['texture']['pointer'],texture=t,alive=True,locked=False)
            self.minimap_resources[label]=r;self.map_identity(t)
            self.methods.update({p:int(s) for s,p in t['methods'].items()});put(record+44,struct.pack('<I',t['pointer']));op='create'
        else:
            r=next(r for r in self.minimap_resources.values() if r['texture']['pointer']==receiver and r['alive'])
            t=r['texture'];p=r['native'];need(self.get(r['record']+44)==t['pointer'],'original minimap record owns current texture')
            if slot==56:
                need(args==[receiver,0,bp-(52 if ret==0x403CBE else 36)], 'original descriptor local')
                native=self.gpu.describe(p);need(bytes.fromhex(native['hex'])==struct.pack('<8I',25,1,0,1,65536,0,256,128),'entire real minimap descriptor')
                put(args[2],bytes.fromhex(native['hex']));op='describe'
            elif slot==64:
                need(args==[receiver,0,self.get(bp+8),0,2048] and not r['locked'], 'original complete minimap lock')
                native=self.gpu.lock(p);raw=bytes.fromhex(native['hex']);pitch=native['pitch']
                need(512<=pitch<=4096 and pitch%2==0 and len(raw)==pitch*128<=MAX_SURFACE,'actual full minimap pitch/padding')
                bits=self.minimap_space.guest(r['domain'],native['bits'],True,len(raw))
                r.update(locked=True,bits=bits,pitch=pitch,lock_before=raw.hex(),surface_bytes=len(raw))
                put(bits,raw);self.mutable.append((bits,bits+len(raw)));put(args[2],struct.pack('<II',pitch,bits));op='lock'
            elif slot==68:
                need(args==[receiver,0] and r['locked'],'original owned minimap unlock')
                before=bytes.fromhex(r['lock_before']);raw=self.read(r['bits'],r['surface_bytes'])
                if r['label']=='background':
                    expected=images.unit_bmp8_upload(asset(),asset()[54:1078],before,r['pitch'],128,1,1)
                else:
                    header=self.read(self.get(MAP+0x2659C),16);seen=self.read(self.get(MAP+0xA0),6144)
                    expected=fog_upload(header,seen,before,r['pitch'])
                need(raw==expected,'independent complete minimap source pixels and untouched full-pitch padding')
                native=self.gpu.unlock(p,raw);r.update(locked=False,upload_sha256=hashlib.sha256(raw).hexdigest())
                observed=self.gpu.readback(p)
                need(observed['hex']==raw.hex() and observed['pitch']==r['pitch'] and observed['sha256']==hashlib.sha256(raw).hexdigest(), 'actual full minimap surface readback')
                self.minimap_observers.append(dict(label=r['label'],wire_index=len(self.gpu.trace)-1,
                    pitch=r['pitch'],bytes=len(raw),sha256=observed['sha256']))
                op='unlock'
            else:
                need(self.minimap_cleaning and args==[receiver] and not r['locked'],'original supplemental minimap release')
                native=self.gpu.release(p);r['alive']=False;op='release'
        value=native['count'] if slot==8 else native['hr'];need(value==0,'actual successful native minimap COM operation')
        self.minimap_calls.append(dict(label=r['label'],op=op,slot=slot,target=at,args=args,sp=sp,return_va=ret,
                                      wire_start=start,wire_end=len(self.gpu.trace),outputs=outputs,value=value))
        self.return_api(sp,value,pop)

    def destroy_minimap(self,root=None):
        need(self.minimap_initialized and not self.minimap_destroyed,'one original minimap supplemental teardown')
        call=root or self.resource_root;self.minimap_cleaning=True
        before=dict(game_bytes=self.get(0x79FC74),texture_bytes=self.get(0x765720))
        try:
            for label,record in (('fog',FOG),('background',BACKGROUND)):
                name='supplemental_original_minimap_'+label+'_destructor'
                call(name,0x403730,receiver=record)
                self.minimap_cleanup.append(dict(label=name,entry=0x403730,receiver=record,args=[]))
            p=self.get(MAP+0x2658C)
            call('supplemental_original_minimap_fog_buffer_free',0x428AD0,[p],cdecl=True)
            self.minimap_cleanup.append(dict(label='supplemental_original_minimap_fog_buffer_free',entry=0x428AD0,receiver=0,args=[p],cdecl=True))
            need(not any(r['alive'] for r in self.minimap_resources.values()),'both original minimap textures released')
            after=dict(game_bytes=self.get(0x79FC74),texture_bytes=self.get(0x765720))
            need(before['game_bytes']-after['game_bytes']==44032 and
                 before['texture_bytes']-after['texture_bytes']==131072,
                 'all additional original minimap user/texture bytes released')
            self.minimap_cleanup.append(dict(before=before,after=after,
                source_fog_pointer_retained_after_explicit_buffer_free=True,
                full_map_destructor_executed=False))
            self.minimap_destroyed=True
        finally:self.minimap_cleaning=False

    def minimap_result(self):
        return dict(input=copy.deepcopy(self.minimap_input),roots=copy.deepcopy(self.minimap_roots),
                    calls=copy.deepcopy(self.minimap_calls),observers=copy.deepcopy(self.minimap_observers),
                    cleanup=copy.deepcopy(self.minimap_cleanup),
                    resources={k:{n:v for n,v in r.items() if n!='lock_before'} for k,r in self.minimap_resources.items()},
                    projection=self.minimap_space.ledger(),initialized=self.minimap_initialized,
                    destroyed=self.minimap_destroyed,source_contract=source_contract())


def source_contract():
    return dict(schema_version=1,executable=dict(path='analysis/hermit_game.exe',bytes=len(CODE),
                sha256=hashlib.sha256(CODE).hexdigest()),
                functions=[dict(start=a,end=b,bytes=b-a,sha256=hashlib.sha256(CODE[a-0x400000:b-0x400000]).hexdigest(),
                                hex=CODE[a-0x400000:b-0x400000].hex()) for a,b in EXTRA_RANGES],
                natural_calls=[dict(pc=0x453C8A,target=0x440F00,receiver=MAP,args=[199]),
                               dict(pc=0x453CA6,target=0x457C40,receiver=CTRL-0x190,args=[])],
                asset=dict(path=BMP_PATH,bytes=len(asset()),sha256=BMP_SHA),
                logical_header_sha256=HEADER_SHA,shape=dimensions(struct.pack('<4h',2048,1536,64,96)+bytes(8),asset()),
                map_owner=MAP,background_record=BACKGROUND,fog_record=FOG,
                mutable=[list(x) for x in MUTABLE],
                BMP_mutable=[list(x) for x in BMP_MUTABLE],
                original_BMP_header_normalizer=dict(entry=0x420A40,end=0x420AB5,
                    bytes=0x75,sha256=hashlib.sha256(CODE[0x20A40:0x20AB5]).hexdigest(),
                    hex=CODE[0x20A40:0x20AB5].hex(),caller_PC=0x404914,
                    write_PC=0x420AA7,write_original_bytes='89512e',
                    write_offset=0x2E,write_bytes=4,field='BITMAPINFOHEADER.biClrUsed',
                    source_input_value=0,original_derived_value=256,
                    derivation='(bfOffBits1078 - fixed BMP palette start54) >>2',
                    predicate='biBitCount in(4,8) and biClrUsed==0',
                    only_non_stack_write_in_complete_function=True),
                pool=dict(base=POOL,stride=STRIDE,records=2,bits_offset=BITS_OFFSET,max_full_pitch_bytes=MAX_SURFACE,
                          input_base=BMP_POINTER,input_mapped_bytes=0x6000),
                original_file_map_loader_executed=False,declared_complete_original_BMP_input=True,
                original_bitmap_memory_entry=0x404870,original_dynamic_fog_initializer=0x4404A0,
                original_SEEN_VISIBLE_preserved=True,host_activation_gate_writes=False,
                owner_fields=dict(
                    coordinates_and_scales=[MAP+0x2646C,MAP+0x2648C],
                    background_packet=[BACKGROUND,BACKGROUND+128],fog_packet=[FOG,FOG+128],
                    source_fog_buffer_pointer=MAP+0x2658C,source_fog_pixel_count=MAP+0x26590,
                    fog_grid_source_pointer=MAP+0xA0,visible_grid_source_pointer=MAP+0xA4,
                    logical_map_header_pointer=MAP+0x2659C),
                original_pixel_writes=[dict(pc=0x440ABB,width=2,source='current SEEN sample mapped to0 or0x8000'),
                                       dict(pc=0x440AD1,width=2,source='duplicate adjacent pixel')],
                before_wait_second_entry=dict(entry=0x457C40,full_function_end=0x457CFA,
                    source_gates=[dict(function=0x456B20,pointer=0x7F4491,width=1,
                                       meaning='nonzero enables457D00/458280 group90 packet queries'),
                                  dict(function=0x4577F0,pointer=CTRL-0x190+0x117F20,width=1,
                                       meaning='nonzero enters426820 text/IME drawing path')],
                    ring=dict(pointer=CTRL-0x190+0x118040,count_s16=0,current_s16=4,mode_s8=6,records_pointer=8),
                    conditional_426820_not_admitted=True,
                    conditional_API_callers=[dict(pc=0x426873,import_slot=0x5922C4,return_va=0x426879),
                                             dict(pc=0x4269E2,import_slot=0x592210,return_va=0x4269E8)]),
                WAIT_body_executed=False,native_smoke_executed=False)
