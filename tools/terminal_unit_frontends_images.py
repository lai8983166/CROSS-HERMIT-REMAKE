"""Original unit image loading with current CRT/D3D leaves and bounded evidence.

Mixin ordering: ImagesMixin must precede the current terminal machine. The
caller admits EXTRA_RANGES in its original-code guard, calls
configure_unit_inputs() before any original root, initializes CRT once before
run(), and destroys unit caches before the existing heap teardown.
"""
import copy
import hashlib
import struct
import types
from functools import lru_cache
from pathlib import Path

from tools import terminal_battle_exit_emulation as exit_source
from tools.dxanim_lib import parse_dxanim, parse_container

ROOT, CODE, need, sha = exit_source.ROOT, exit_source.CODE, exit_source.need, exit_source.sha
overlay = exit_source.overlay
MAIN, CTRL = exit_source.MAIN, exit_source.CTRL
PATH_OWNER, PATH_BYTES = 0x3A000000, 0x2000
UNIT_POOL, UNIT_STRIDE, UNIT_RECORDS = 0x34000000, 0x20000, 600
LARGE_POOL, LARGE_STRIDE, LARGE_COUNT = 0x3B000000, 0x40000, 40
PREFIX = 'overlay-unit-frontends-'
OBSERVED = frozenset((0x466C80,0x409B70,0x409BE5,0x41F340,
                      0x4048D0,0x404150,0x428AD0,0x466D85))
ASSETS = {1: ('B0A', 1492764, '2d58f3bf4e5566b1cf021dbffd3531826c0b6ae5b2955905316a35b16bd4f785'),
          3: ('A0A', 1308312, '9d3157608c29b1d3b9a118ba7a3c3d2ac85e3e4be6db7c9b0424be093b7fdc71')}
EXTRA_RANGES = ((0x466B40,0x466C78),(0x466C80,0x466D9A),
                (0x464C60,0x464DD7),(0x464EB0,0x464F7B),
                (0x409900,0x409AD0),(0x409B70,0x409E7C),
                (0x41EAD0,0x41ECFE),(0x4142B0,0x4142DD),
                (0x4500B0,0x45010D),(0x40B960,0x40B98F),
                (0x466F00,0x466FB7),(0x4663B0,0x466401),
                (0x403AA0,0x403AEC),(0x404150,0x40440D),
                (0x4048D0,0x404B0D),(0x56E260,0x56E298))


@lru_cache(maxsize=2)
def unit_asset(job):
    need(type(job) is int and job in ASSETS, 'unit image jobs1/3 only')
    name, size, digest = ASSETS[job]
    path = ROOT / ('CROSS HERMIT/CROSS HERMIT/DATA/DXANIM/'+name+'.BIN')
    raw = path.read_bytes()
    need(len(raw) == size and sha(raw) == digest, 'exact complete original unit archive')
    sections = parse_dxanim(raw)
    need(len(sections) == 9 and sections == sorted(sections), 'nine original unit sections')
    container_bytes, count, offsets = parse_container(raw, sections[6])
    palette_bytes, palettes, palette_offsets = parse_container(raw, sections[7])
    need(count in (209,251) and palettes == 40 and count <= 300, 'finite complete unit image/palette catalog')
    mask = raw[sections[8]:sections[8]+count]
    need(set(mask) <= {0,1} and raw[sections[8]+count:] == bytes((-count)%4), 'complete source palette mask/padding')
    rows = []
    for index, relative in enumerate(offsets):
        end = offsets[index+1] if index+1 < count else container_bytes
        at = sections[6]+relative
        blob = raw[at:sections[6]+end]
        need(blob[:2] == b'BM' and struct.unpack_from('<H',blob,28)[0] == 8, 'all source unit images BMP8')
        w,h = struct.unpack_from('<ii',blob,18)
        need(w > 0 and h > 0, 'original positive bottom-up BMP')
        tw,th = 1 << (w-1).bit_length(), 1 << (h-1).bit_length()
        need(tw*th*2 <= LARGE_STRIDE, 'full source unit texture extent')
        rows.append(dict(index=index, offset=at, bytes=len(blob), sha256=sha(blob),
                         width=w, height=h, texture_size=[tw,th], mask=mask[index]))
    selection = struct.unpack_from('<IhBb',CODE,0x610538+job*8-0x400000)
    return dict(raw=raw, rows=rows, sections=sections, palette_offsets=palette_offsets,
                identity=dict(path=path.relative_to(ROOT).as_posix(), bytes=size, sha256=digest),
                filename_pointer=selection[0], group=selection[1], mode=selection[2],
                metadata_bytes=sections[6], metadata_sha256=sha(raw[:sections[6]]))


def unit_bmp8_upload(blob, palette, before, pitch, texture_height, colorkey, normalize_black=1):
    """Independent full surface, selected/embedded palette and padding oracle."""
    need(type(palette) is bytes and len(palette) == 1024, 'complete source BMP8 palette')
    patched = bytearray(blob)
    need(len(patched) >= 1078, 'original complete BMP8 palette extent')
    patched[54:1078] = palette
    return exit_source.bmp8_upload(bytes(patched),before,pitch,texture_height,colorkey,normalize_black)


class UnitAddressSpace(exit_source.CommonAddressSpace):
    """Small identity slots plus a bounded pool for actual large surface bytes."""
    def __init__(self):
        super().__init__()
        self.surface_bytes = {}
        self.large_domains = []

    def unit_address(self, domain, pointer, bits=False):
        if not pointer:
            return 0
        suffix = domain[len(PREFIX):].split('-')
        need(len(suffix) == 2 and all(s.isdecimal() for s in suffix), 'typed unit projection domain')
        ordinal,index = map(int,suffix)
        need(0 <= ordinal < 2 and 0 <= index < 300, 'finite two-cache unit identities')
        key = domain,pointer
        if key not in self.native_to_guest:
            base = UNIT_POOL+(ordinal*300+index)*UNIT_STRIDE
            if bits:
                size = self.surface_bytes.get(domain,0)
                need(0 < size <= LARGE_STRIDE, 'complete actual locked surface extent')
                if size > 0x10000:
                    if domain not in self.large_domains:
                        need(len(self.large_domains) < LARGE_COUNT, 'bounded large unit surface pool')
                        self.large_domains.append(domain)
                    guest = LARGE_POOL+self.large_domains.index(domain)*LARGE_STRIDE
                else:
                    guest = base+0x10000
            else:
                ordinal_in_domain = sum(d == domain for d,p in self.native_to_guest)
                offset = (ordinal_in_domain+1)*0x1000
                need(offset < 0x10000, 'finite unit COM identities before surface')
                guest = base+offset
            need(guest not in self.guest_to_native, 'unit logical identity alias refused')
            self.native_to_guest[key] = guest
            self.guest_to_native[guest] = key
        return self.native_to_guest[key]

    def guest(self, domain, pointer):
        return self.unit_address(domain,pointer) if domain.startswith(PREFIX) else super().guest(domain,pointer)

    def result(self, domain, value, key=None):
        if domain.startswith(PREFIX) and key == 'bits' and type(value) is int:
            return self.unit_address(domain,value,True)
        return super().result(domain,value,key)


def _expected_helpers():
    crt = (ROOT/'tools/terminal_battle_exit_crt_platform.cs').read_bytes()
    old = b'path=="data\\\\Tactics\\\\common.bin"'
    need(crt.count(old) == 1, 'frozen CRT path contract')
    crt = crt.replace(old,old+b' || path=="data\\\\DxAnim\\\\b0a.bin" || path=="data\\\\DxAnim\\\\a0a.bin"')
    old = b'expectedFileBytes=path.EndsWith("Gybc_00.bin")?524312u:(path.EndsWith("common.bin")?1793036u:262168u);'
    need(crt.count(old) == 1, 'frozen CRT exact extent contract')
    crt = crt.replace(old,b'expectedFileBytes=path.EndsWith("b0a.bin")?1492764u:(path.EndsWith("a0a.bin")?1308312u:(path.EndsWith("Gybc_00.bin")?524312u:(path.EndsWith("common.bin")?1793036u:262168u)));')
    crt = crt.replace(b'blocks.Count<6',b'blocks.Count<32')
    gpu = (ROOT/'tools/terminal_battle_exit_d3d8_platform.cs').read_bytes()
    gpu = gpu.replace(b'resources.Count>=500 || issued>=512',b'resources.Count>=1024 || issued>=1024')
    gpu = gpu.replace(b'max_textures=500,max_creates=512',b'max_textures=1024,max_creates=1024')
    return crt,gpu


def helper_contract():
    crt,gpu = _expected_helpers()
    need((ROOT/'tools/terminal_unit_frontends_crt_platform.cs').read_bytes() == crt, 'only bounded unit paths/extents/block capacity change')
    need((ROOT/'tools/terminal_unit_frontends_d3d8_platform.cs').read_bytes() == gpu, 'only bounded multi-texture capacity change')
    return dict(CRT=dict(source='tools/terminal_unit_frontends_crt_platform.cs',sha256=sha(crt),max_blocks=32,max_allocation=2097152),
                GPU=dict(source='tools/terminal_unit_frontends_d3d8_platform.cs',sha256=sha(gpu),max_textures=1024,max_creates=1024))


def CORE_helpers(prefix='terminal-unit-frontends'):
    helper_contract()
    ch,cb = overlay.platform.build(ROOT/'tools/terminal_unit_frontends_crt_platform.cs',prefix+'-crt')
    gh,gb = overlay.platform.build(ROOT/'tools/terminal_unit_frontends_d3d8_platform.cs',prefix+'-gpu')
    return ch,gh,dict(CRT=cb,GPU=gb)


helpers = CORE_helpers
CRTLive = exit_source.CommonCRTLive


class ImagesMixin:
    def read(self, pointer, count=4):
        return bytes(self.uc.mem_read(pointer,count))

    def return_api(self, sp, value, pop):
        for reg,v in ((exit_source.x86.UC_X86_REG_EAX,value & 0xFFFFFFFF),
                      (exit_source.x86.UC_X86_REG_ESP,sp+4+pop),
                      (exit_source.x86.UC_X86_REG_EIP,self.get(sp))):
            self.uc.reg_write(reg,v)

    def configure_unit_inputs(self):
        need(not getattr(self,'unit_configured',False) and self.mark()['instructions'] == 0, 'unit declarations precede first original root')
        self.unit_configured = True
        self.unit_phase = None
        self.unit_loads = []
        self.unit_current_load = self.unit_current_image = None
        self.unit_resources = []
        self.unit_live = {}
        self.unit_leaves = []
        self.unit_observers = []
        self.unit_cleanup = []
        self.unit_crt_initialization = []
        self.unit_input_changes = []
        need(not any(a < PATH_OWNER+PATH_BYTES and b >= PATH_OWNER for a,b,p in self.uc.mem_regions()), 'disjoint resource path owner')
        for lo,hi in ((UNIT_POOL,UNIT_POOL+UNIT_RECORDS*UNIT_STRIDE),(LARGE_POOL,LARGE_POOL+LARGE_COUNT*LARGE_STRIDE)):
            need(not any(a < hi and b >= lo for a,b,p in self.uc.mem_regions()), 'disjoint complete unit projection pool')
        self.uc.mem_map(PATH_OWNER,PATH_BYTES)
        self.mutable += [(PATH_OWNER,PATH_OWNER+PATH_BYTES),(CTRL+0x2A6F0,CTRL+0x2A7F0),
                         (CTRL+0x2E6F0,CTRL+0x2E6F4),(0x765520,0x765724)]

        def declare(at, data, origin):
            before = self.read(at,len(data))
            self.uc.mem_write(at,data)
            self.unit_input_changes.append(dict(pointer=at,bytes=len(data),before_hex=before.hex(),after_hex=data.hex(),source=origin))
        # Only entries explicitly occupied by the old two-unit fixture change;
        # the remaining original zero cache is asserted, never silently cleared.
        declare(CTRL+0x2A6F0,bytes(16),'replace two old metadata-only occupied cache declarations with cold entries')
        need(self.read(CTRL+0x2A6F0+16,4096-16) == bytes(4096-16), 'all other initial cache entries empty')
        need(self.get(CTRL+0x2E6F0) == 0, 'declared original-constructor-compatible counter0')
        declare(0x7A4A00,struct.pack('<I',PATH_OWNER),'separate source path owner, original4500B0 scratch must not alias renderer group20')
        need(self.get(0x7A49FC) == MAIN and self.get(MAIN+0xB210) == self.device_ptr, 'current real renderer/device already declared')
        need(self.read(MAIN+0x844,16) == bytes(16), 'source destination groups0/1 genuinely empty')
        self.unit_input_contract = dict(path_owner=PATH_OWNER,path_bytes=PATH_BYTES,prefix_hex=self.read(PATH_OWNER+0xBF4,1).hex(),
                                        counter=0,scene_counter110_setter_executed=False,cache_bytes=4096,
                                        renderer=MAIN,device=self.device_ptr,before_first_root=True)
        space = UnitAddressSpace()
        space.native_to_guest = self.space.native_to_guest
        space.guest_to_native = self.space.guest_to_native
        space.next = self.space.next
        self.space = self.unit_space = space

    def initialize_unit_CRT(self):
        need(self.unit_configured and not self.unit_crt_initialization and not self.crt.allocations and not self.crt.criticals,
             'one original early CRT initialization')
        self.unit_phase = 'CRT_initialization'
        try:
            self.resource_root('unit_original_heap_initialization',0x57B9D0,[1],cdecl=True)
            self.unit_crt_initialization.append(copy.deepcopy(self.resource_steps[-1]))
            self.resource_root('unit_original_lock_initialization',0x576F60)
            self.unit_crt_initialization.append(copy.deepcopy(self.resource_steps[-1]))
        finally:
            self.unit_phase = None

    def api_crt(self, slot):
        if not getattr(self,'unit_phase',None):
            return super().api_crt(slot)
        original = self.crt.api
        if self.unit_phase == 'load' and slot == 0x5921EC:
            name = self.unit_current_load['relative_path']
            fn = overlay.CrtGuest.api
            self.crt.api = types.MethodType(types.FunctionType(fn.__code__,dict(fn.__globals__,RESOURCE_NAME=name),closure=fn.__closure__),self.crt)
        try:
            overlay.OverlayMachine.api_crt(self,slot)
        finally:
            self.crt.api = original
        self.unit_leaves.append(dict(kind='CRT',phase=self.unit_phase,call=copy.deepcopy(self.crt_apis[-1])))

    def gpu_api(self, at):
        if not getattr(self,'unit_phase',None):
            return super().gpu_api(at)
        need(self.unit_phase in ('load','cleanup'), 'unit GPU call only in original load/destruction')
        slot = self.methods[at]
        pop = {80:32,56:12,64:20,68:8,8:4}[slot]
        sp,bp = self.getreg('ESP'),self.getreg('EBP')
        ret = self.get(sp)
        args = [self.get(sp+4+j) for j in range(0,pop,4)]
        wire = len(self.gpu.trace)
        outputs = []
        need(ret == {80:0x403C8A,64:0x40395E,68:0x4039D3,8:0x40378D}.get(slot,ret) and
             (slot != 56 or ret in (0x403CBE,0x403A44)), 'original unit COM caller')

        def put(p,b):
            self.map_new(p,len(b))
            self.uc.mem_write(p,b)
            outputs.append(dict(pointer=p,hex=b.hex()))
        if slot == 80:
            r = self.unit_current_image
            need(self.unit_phase == 'load' and r is not None and not r.get('texture'), 'one current original unit image')
            w,h = r['source']['texture_size']
            need(args == [self.device_ptr,w,h,1,0,25,1,r['record']+44], 'complete source unit texture creation ABI')
            domain = PREFIX+str(r['cache_ordinal'])+'-'+str(r['source']['index'])
            native = self.gpu.create(w,h)
            result = self.unit_space.result(domain,native)
            t = result['texture']
            r.update(projection_domain=domain,texture=t,native_pointer=native['texture']['pointer'],generation=wire+1,
                     create_wire_index=wire,alive=True,size=[w,h])
            self.unit_resources.append(r)
            self.unit_live[t['pointer']] = r
            self.map_identity(t)
            self.methods.update({p:int(k) for k,p in t['methods'].items()})
            put(args[-1],struct.pack('<I',t['pointer']))
            op = 'create'
        else:
            need(args[0] in self.unit_live, 'owned current unit texture')
            r = self.unit_live[args[0]]
            t,p = r['texture'],r['native_pointer']
            need(self.get(r['record']+44) == t['pointer'], 'original unit record owns actual texture')
            if slot == 56:
                need(args == [t['pointer'],0,bp-(52 if ret == 0x403CBE else 36)], 'original descriptor destination')
                native = self.gpu.describe(p)
                result = copy.deepcopy(native)
                put(args[-1],bytes.fromhex(result['hex']))
                op = 'describe'
            elif slot == 64:
                need(self.unit_phase == 'load' and r is self.unit_current_image and args == [t['pointer'],0,self.get(bp+8),0,2048], 'original unit full lock ABI')
                native = self.gpu.lock(p)
                raw = bytes.fromhex(native['hex'])
                self.unit_space.surface_bytes[r['projection_domain']] = len(raw)
                result = self.unit_space.result(r['projection_domain'],native)
                r['lock'] = copy.deepcopy(result)
                put(result['bits'],raw)
                self.mutable.append((result['bits'],result['bits']+len(raw)))
                put(args[2],struct.pack('<II',result['pitch'],result['bits']))
                op = 'lock'
            elif slot == 68:
                need(self.unit_phase == 'load' and r is self.unit_current_image and args == [t['pointer'],0], 'original unit unlock ABI')
                raw = self.read(r['lock']['bits'],len(bytes.fromhex(r['lock']['hex'])))
                asset = unit_asset(self.unit_current_load['job'])
                s = r['source']
                blob = asset['raw'][s['offset']:s['offset']+s['bytes']]
                palette = (asset['raw'][r['palette_file_offset']:r['palette_file_offset']+1024]
                           if r['palette_file_offset'] is not None else blob[54:1078])
                expected = unit_bmp8_upload(blob,palette,bytes.fromhex(r['lock']['hex']),r['lock']['pitch'],r['size'][1],
                                            r['conversion']['args'][1],r['bitmap_loader']['args'][4])
                need(raw == expected, 'independent entire unit palette/pixel/stride/padding prediction')
                r.update(upload_hex=raw.hex(),expected_sha256=sha(expected))
                native = self.gpu.unlock(p,raw)
                result = copy.deepcopy(native)
                op = 'unlock'
                observer = len(self.gpu.trace)
                r['readback'] = self.gpu.readback(p)
                r['readback_wire_index'] = observer
                need(r['readback']['hex'] == raw.hex() and r['readback']['pitch'] == r['lock']['pitch'], 'entire actual unit surface readback')
                self.unit_observers.append(dict(cache_ordinal=r['cache_ordinal'],index=s['index'],wire_index=observer,result=copy.deepcopy(r['readback'])))
            else:
                need(self.unit_phase == 'cleanup' and args == [t['pointer']], 'original unit supplemental release only')
                native = self.gpu.release(p)
                result = copy.deepcopy(native)
                r.update(alive=False,release_wire_index=wire)
                del self.unit_live[t['pointer']]
                op = 'release'
        value = result['count'] if slot == 8 else result['hr']
        need(value == 0, 'current native unit GPU success')
        row = dict(generation=r['generation'],record=r['record'],cache_ordinal=r['cache_ordinal'],index=r['source']['index'],
                   wire_index=wire,phase=self.unit_phase,slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,
                   op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True)
        self.unit_leaves.append(dict(kind='GPU',call=row))
        self.return_api(sp,value,pop)

    def _unit_observe(self, at):
        if at not in OBSERVED or not self.unit_configured:
            return
        sp = self.uc.reg_read(exit_source.x86.UC_X86_REG_ESP)
        if at == 0x466C80:
            need(self.unit_phase is None and len(self.unit_loads) < 2 and len(self.unit_crt_initialization) == 2, 'two natural cache loads after original CRT initialization')
            entry,group,variant = [self.get(sp+4+j*4) for j in range(3)]
            job = self.combat_input['job']
            asset = unit_asset(job)
            ordinal = len(self.unit_loads)
            identity = 11 if ordinal == 0 else 10
            palette_byte = struct.unpack_from('<b',CODE,0x618090+job*40+identity-0x400000)[0]
            need(self.getreg('ECX') == CTRL and entry == CTRL+0x2A6F0+ordinal*8 and group == asset['group'] and variant == palette_byte+1,
                 'natural target then actor original cache/type/palette selection')
            need(self.get(CTRL+0x2E6F0) == ordinal and self.read(MAIN+0x844+ordinal*8,8) == bytes(8), 'actual counter and empty source destination slot')
            self.unit_phase = 'load'
            r = dict(cache_ordinal=ordinal,cache_entry=entry,controller=self.get(entry+4),job=job,group=group,variant=variant,
                     identity=identity,slot=ordinal,relative_path='data\\DxAnim\\'+ASSETS[job][0].lower()+'.bin',
                     source=copy.deepcopy(asset['identity']),metadata_bytes=asset['metadata_bytes'],entries=[],
                     configure_call=dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[entry,group,variant],CPU=self.cpu()))
            self.unit_loads.append(r)
            self.unit_current_load = r
            return
        if self.unit_phase != 'load':
            return
        load = self.unit_current_load
        asset = unit_asset(load['job'])
        if at == 0x409B70:
            args = [self.get(sp+4+j*4) for j in range(6)]
            need(self.getreg('ECX') == load['controller'] and args[:2] == [self.device_ptr,MAIN+0x844] and
                 self.read(args[2],260).split(b'\0',1)[0].decode('ascii') == load['relative_path'] and args[3:] == [load['variant'],1,0], 'complete original natural unit file loader ABI')
            load['loader'] = dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=args,CPU=self.cpu())
        elif at == 0x409BE5:
            file = self.get(self.getreg('EBP')-0x10)
            need(self.read(file,len(asset['raw'])) == asset['raw'], 'actual complete current unit source read')
            load['file'] = dict(pointer=file,bytes=len(asset['raw']),sha256=sha(asset['raw']))
        elif at == 0x41F340:
            args = [self.get(sp+4+j*4) for j in range(6)]
            index = args[2]
            need(index == len(load['entries']) and 0 <= index < len(asset['rows']) and args[:2] == [self.device_ptr,load['file']['pointer']+asset['sections'][6]], 'all original unit images in order')
            s = copy.deepcopy(asset['rows'][index])
            palette_offset = asset['sections'][7]+asset['palette_offsets'][load['variant']-1] if s['mask'] == 0 else None
            palette_pointer = load['file']['pointer']+palette_offset if palette_offset is not None else 0
            need(args[4:] == [0,palette_pointer], 'original per-image palette mask branch')
            r = dict(cache_ordinal=load['cache_ordinal'],source=s,record=args[3]+index*84,palette_file_offset=palette_offset,
                     loader=dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=args,CPU=self.cpu()),alive=False)
            load['entries'].append(r)
            self.unit_current_image = r
        elif at == 0x4048D0:
            r = self.unit_current_image
            need(r is not None and self.getreg('ECX') == r['record'], 'current unit bitmap preparation')
            r['bitmap_loader'] = dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[self.get(sp+4+j*4) for j in range(7)],CPU=self.cpu())
        elif at == 0x404150:
            r = self.unit_current_image
            need(r is not None and self.getreg('ECX') == r['record'], 'current unit palette conversion')
            r['conversion'] = dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[self.get(sp+4+j*4) for j in range(4)],CPU=self.cpu())
        elif at == 0x428AD0 and self.get(sp+4) == load.get('file',{}).get('pointer'):
            need(self.get(sp) == 0x409E5D and len(load['entries']) == len(asset['rows']), 'original temporary unit file release after complete images')
            file = load['file']
            load['file_release'] = dict(pointer=file['pointer'],bytes=file['bytes'],sha256_at_release=sha(self.read(file['pointer'],file['bytes'])),caller=self.get(sp))
        elif at == 0x466D85:
            controller = load['controller']
            need(len(load['entries']) == len(asset['rows']) and all(r.get('readback') for r in load['entries']), 'complete actual original unit texture cache')
            need(self.get(controller+0x24) == MAIN+0x844 and self.get(controller+0x28) == load['slot'] and
                 self.get(controller+0x40) == 1 and self.get(CTRL+0x2E6F0) == load['slot']+1, 'original slot/manager/mode/counter publication')
            metadata = self.get(controller)
            need(self.read(metadata,asset['metadata_bytes']) == asset['raw'][:asset['metadata_bytes']], 'exact original complete metadata copy')
            load.update(controller_forward_hex=self.read(controller,84).hex(),metadata_pointer=metadata,
                        metadata_sha256=sha(self.read(metadata,asset['metadata_bytes'])),
                        group_forward_hex=self.read(MAIN+0x844+load['slot']*8,8).hex(),complete=True)
            for r in load['entries']:
                r['record_forward_hex'] = self.read(r['record'],84).hex()
            self.unit_phase = None
            self.unit_current_load = self.unit_current_image = None

    def code(self, uc, at, size, context):
        if getattr(self,'unit_configured',False):
            self._unit_observe(at)
        return super().code(uc,at,size,context)

    def destroy_unit_images(self, segment=None):
        need(self.unit_configured and self.unit_phase is None and all(r.get('complete') for r in self.unit_loads), 'original cache destruction after complete loads')
        self.unit_phase = 'cleanup'
        first = len(self.unit_leaves)
        try:
            if segment is None:
                self.resource_root('supplemental_original_unit_cache_destructor',0x466F00,receiver=CTRL)
                call = copy.deepcopy(self.resource_steps[-1])
            else:
                call = segment('supplemental_original_unit_cache_destructor',0x466F00,
                               root=dict(receiver=CTRL,args=[],origin='explicit original cache destruction after frozen forward result'))
        finally:
            self.unit_phase = None
        need(not self.unit_live and self.read(CTRL+0x2A6F0,4096) == bytes(4096), 'all unit textures/controllers and cache entries released')
        for load in self.unit_loads:
            need(self.read(MAIN+0x844+load['slot']*8,8) == bytes(8), 'original unit renderer group cleared')
        self.unit_cleanup.append(dict(call=call,leaves=[first,len(self.unit_leaves)],cache_empty=True,live_textures=0))
        return self.unit_cleanup[-1]

    def unit_image_result(self):
        return dict(input_contract=copy.deepcopy(self.unit_input_contract),input_changes=copy.deepcopy(self.unit_input_changes),
                    CRT_initialization=copy.deepcopy(self.unit_crt_initialization),loads=copy.deepcopy(self.unit_loads),
                    leaves=copy.deepcopy(self.unit_leaves),observers=copy.deepcopy(self.unit_observers),
                    cleanup=copy.deepcopy(self.unit_cleanup),projection=copy.deepcopy(self.unit_space.ledger()),
                    large_surface_domains=list(self.unit_space.large_domains),live_textures=len(self.unit_live),
                    source_contract=source_contract())


def source_contract():
    return dict(helper=helper_contract(),original_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                assets={str(j):{k:v for k,v in unit_asset(j).items() if k not in ('raw','rows','palette_offsets')} for j in ASSETS},
                path_owner=dict(pointer=PATH_OWNER,bytes=PATH_BYTES,global_pointer=0x7A4A00,disjoint_renderer=True),
                projection=dict(base=UNIT_POOL,stride=UNIT_STRIDE,records=UNIT_RECORDS,bits_offset=0x10000,small_surface_max=0x10000,
                                large_base=LARGE_POOL,large_stride=LARGE_STRIDE,large_count=LARGE_COUNT,
                                reason='Original B0A has15 large images per cache; A0A has5. Full surface/pitch/padding must not cross identity slots.'),
                counter_initial=0,original_scene_counter110_setter_executed=False,loaded_cache_predeclared=False,
                complete_original_file_metadata_images=True,current_native_CRT_GPU=True,full_surface_readback=True,
                game_function_return_stubs=False,host_slot_or_lookup_result_writes=False,draw_or_Present=False)


def native_binding_smoke(job=1):
    """Bounded native load/bind/destruct diagnostic, without a world frame.

    Only small summaries leave this function. Full IPC surfaces and temporary
    diagnostic state remain in memory; failures retain CPU and the first error.
    """
    need(job in (1,3), 'smoke source job')
    ch,gh,build = CORE_helpers('terminal-unit-frontends-smoke')
    allowed = overlay.ALLOWED | frozenset(p for a,b in EXTRA_RANGES for p in range(a,b))
    reference = types.FunctionType(overlay.REFERENCE.__code__,dict(overlay.REFERENCE.__globals__,RANGES=overlay.RANGES+EXTRA_RANGES))

    class Smoke(ImagesMixin,overlay.OverlayMachine):
        source_code = types.FunctionType(overlay.OverlayMachine.source_code.__code__,
                                         dict(overlay.OverlayMachine.source_code.__globals__,ALLOWED=allowed,REFERENCE=reference))

    c = next(c for c in overlay.parent.corpus() if c['name'] == 'neutral_running')
    need(job == 1, 'standalone neutral fixture is job1; job3 full-life caller supplies its own declared case')
    live = CRTLive(ch)
    gpu = overlay.platform.OverlayGPU(gh)
    m = None
    result = dict(schema_version=1,accepted=False,kind='bounded_native_original_unit_first_binding_smoke',job=job,helper_build=build)
    try:
        m = Smoke(c,live,gpu)
        m.configure_unit_inputs()
        m.initialize_unit_CRT()
        sp = exit_source.STACK+0xF000
        m.put(sp,exit_source.RETURN)
        m.put(sp+4,exit_source.terminal.TARGET)
        m.put(sp+8,job)
        m.uc.reg_write(exit_source.x86.UC_X86_REG_ESP,sp)
        m.uc.reg_write(exit_source.x86.UC_X86_REG_ECX,CTRL)
        for batch in range(32):
            entry = 0x467020 if batch == 0 else m.getreg('EIP')
            m.uc.emu_start(entry,exit_source.RETURN,timeout=0,count=2000000)
            if m.getreg('EIP') == exit_source.RETURN:
                break
            print('unit native smoke batch',batch+1,'PC',hex(m.getreg('EIP')),'images',sum(len(l['entries']) for l in m.unit_loads),flush=True)
        else:
            raise ValueError('bounded original first-binding instruction budget')
        need(m.getreg('ESP') == sp+12 and len(m.unit_loads) == 1 and m.unit_loads[0].get('complete'), 'complete native first binding return')
        load = m.unit_loads[0]
        result.update(binding_return_CPU=m.cpu(),input_changes=m.unit_input_changes,CRT_initialization=m.unit_crt_initialization,
                      load={k:copy.deepcopy(v) for k,v in load.items() if k != 'entries'},
                      images=[dict(index=r['source']['index'],source=r['source'],record=r['record'],record_hex=r['record_forward_hex'],
                                   domain=r['projection_domain'],surface_bytes=len(bytes.fromhex(r['upload_hex'])),
                                   pitch=r['lock']['pitch'],expected_sha256=r['expected_sha256'],readback_sha256=r['readback']['sha256'])
                              for r in load['entries']],large_surface_domains=list(m.unit_space.large_domains),trace=m.mark())
        m.destroy_unit_images()
        m.resource_root('smoke_original_lock_teardown',0x576FA0)
        m.resource_root('smoke_original_heap_teardown',0x57BA60)
        need(not m.crt.allocations and not m.crt.criticals, 'empty original CRT after unit cleanup')
        result.update(success=True,cleanup=m.unit_cleanup,CRT_cleanup=live.close(),GPU_cleanup=gpu.close(),
                      CRT_calls=len(m.crt_apis),GPU_calls=len(m.unit_leaves),native_GPU_operations=len(gpu.trace),
                      code_sha256=sha(CODE),images_module_sha256=sha(Path(__file__).read_bytes()))
    except Exception as error:
        result.update(success=False,error=str(error),CPU=m.cpu() if m else None,
                      load_count=len(m.unit_loads) if m and getattr(m,'unit_configured',False) else 0,
                      completed_images=sum(len(l['entries']) for l in m.unit_loads) if m and getattr(m,'unit_configured',False) else 0)
    finally:
        if not live.closed:
            live._terminate()
        if not gpu.closed:
            gpu._terminate()
    return result


if __name__ == '__main__':
    import argparse
    import json
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--smoke-out',required=True)
    args = p.parse_args()
    out = ROOT/args.smoke_out
    need(not out.exists(), 'new small smoke diagnostic path')
    r = native_binding_smoke()
    out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('unit native smoke',r.get('success'),r.get('error',''),out,out.stat().st_size,flush=True)
    if not r.get('success'):
        raise SystemExit(1)
