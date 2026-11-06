"""Small pure CPU/source/extent tests; deliberately no native GPU smoke."""
import hashlib
import struct
import unittest
from types import SimpleNamespace

from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn import x86_const as x86
from tools import terminal_unit_frontends_minimap as m


class MinimapTests(unittest.TestCase):
    def test_configuration_preserves_all_old_packets_and_visibility(self):
        u=Uc(UC_ARCH_X86,UC_MODE_32)
        for a,n in ((0x11000000,0x30000),(0x11400000,0xA000),(0x12740000,0x4000)):
            u.mem_map(a,n)
        logical=(m.ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP/MAP05.BIN').read_bytes()
        u.mem_write(0x11400000,logical);seen=bytes([0x55])*6144;visible=bytes([0x33])*6144
        u.mem_write(0x12742000,seen);u.mem_write(0x12740000,visible)
        for p,value in ((m.MAP+0x2659C,0x11400000),(m.MAP+0xA0,0x12742000),(m.MAP+0xA4,0x12740000)):
            u.mem_write(p,struct.pack('<I',value))
        fixture=SimpleNamespace(uc=u,mutable=[],mark=lambda:dict(instructions=0),
            read=lambda p,n:bytes(u.mem_read(p,n)),get=lambda p:struct.unpack('<I',u.mem_read(p,4))[0])
        original=bytes(u.mem_read(0x11000000,0x30000))
        m.MinimapMixin.configure_minimap_inputs(fixture)
        self.assertEqual(bytes(u.mem_read(0x11000000,0x30000)),original)
        self.assertEqual(bytes(u.mem_read(0x12742000,6144)),seen)
        self.assertEqual(bytes(u.mem_read(0x12740000,6144)),visible)
        self.assertEqual(bytes(u.mem_read(m.BMP_POINTER,len(m.asset()))),m.asset())
        self.assertFalse(fixture.minimap_resources)
        self.assertEqual(fixture.mutable,list(m.MUTABLE)+list(m.BMP_MUTABLE))
        self.assertEqual(fixture.minimap_input['header_normalization']['before'],0)
        self.assertEqual(struct.unpack_from('<I',u.mem_read(m.BMP_POINTER,54),0x2E)[0],0)
        fixture.minimap_configured=False;fixture.mark=lambda:dict(instructions=1)
        with self.assertRaises(ValueError):m.MinimapMixin.configure_minimap_inputs(fixture)

    def test_original_420A40_normalizes_only_exact_biClrUsed_span(self):
        for bpp,used,bits,expected in ((8,0,1078,256),(8,128,1078,128),
                                       (24,0,1078,0),(4,0,118,16)):
            with self.subTest(bpp=bpp,used=used,bits=bits):
                u=Uc(UC_ARCH_X86,UC_MODE_32);size=(len(m.CODE)+4095)&-4096
                u.mem_map(0x400000,size,7);u.mem_write(0x400000,m.CODE);u.mem_protect(0x400000,size,5)
                u.mem_map(m.BMP_POINTER,0x6000);u.mem_map(0x12000000,0x20000);u.mem_map(0x12100000,4096)
                raw=bytearray(m.asset());struct.pack_into('<H',raw,28,bpp)
                struct.pack_into('<I',raw,46,used);struct.pack_into('<I',raw,10,bits)
                u.mem_write(m.BMP_POINTER,bytes(raw));sp=0x1200F000
                u.mem_write(sp,struct.pack('<II',0x12100000,m.BMP_POINTER))
                u.reg_write(x86.UC_X86_REG_ESP,sp);u.reg_write(x86.UC_X86_REG_ECX,0x12001000)
                writes=[]
                def code(uc,pc,n,_):
                    self.assertTrue(0x420A40<=pc<0x420AB5)
                    self.assertEqual(bytes(uc.mem_read(pc,n)),m.CODE[pc-0x400000:pc-0x400000+n])
                def write(uc,access,p,n,value,_):
                    if not (0x12000000<=p and p+n<=0x12020000):
                        writes.append((uc.reg_read(x86.UC_X86_REG_EIP),p,n,value))
                        self.assertTrue(any(a<=p and p+n<=z for a,z in m.BMP_MUTABLE))
                u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,write)
                u.emu_start(0x420A40,0x12100000,count=1000)
                after=bytes(u.mem_read(m.BMP_POINTER,len(raw)));want=bytearray(raw)
                struct.pack_into('<I',want,46,expected)
                self.assertEqual(after,bytes(want))
                self.assertEqual(writes,[(0x420AA7,m.BMP_POINTER+46,4,expected)] if bpp in (4,8) and used==0 else [])
                self.assertEqual(u.reg_read(x86.UC_X86_REG_ESP),sp+8)
        for offset in (0x2D,0x32,0x35):
            self.assertFalse(any(a<=m.BMP_POINTER+offset and m.BMP_POINTER+offset+1<=z
                                 for a,z in m.BMP_MUTABLE))

    def test_real_asset_and_complete_dimensions(self):
        raw=m.asset();header=struct.pack('<8h',2048,1536,64,96,256,256,8,6)
        shape=m.dimensions(header,raw)
        self.assertEqual(shape['original_args'],[2048,1536])
        self.assertEqual(shape['texture_size'],[256,128])
        self.assertEqual(shape['fog_user_bytes'],44032)
        self.assertEqual(shape['nominal_surface_bytes'],65536)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),m.BMP_SHA)
        with self.assertRaises(ValueError):m.dimensions(struct.pack('<8h',0,0,0,0,0,0,0,0),raw)

    def test_two_complete_projection_spans_disjoint_from_BMP(self):
        space=m.MinimapAddressSpace()
        for i,domain in enumerate(m.DOMAINS):
            native=dict(pointer=0x10000000+i*0x1000,vtable=0x20000000,
                        methods={str(s):0x21000000+j*4 for j,s in enumerate((8,56,64,68))})
            result=space.texture(domain,native)
            self.assertEqual(result['pointer'],m.POOL+i*m.STRIDE+4096)
            bits=space.guest(domain,0x30000000,True,m.MAX_SURFACE)
            self.assertEqual(bits,m.POOL+i*m.STRIDE+m.BITS_OFFSET)
            self.assertLessEqual(bits+m.MAX_SURFACE,m.POOL+(i+1)*m.STRIDE)
        self.assertLess(m.POOL+2*m.STRIDE-1,m.BMP_POINTER)
        with self.assertRaises(ValueError):space.guest(m.DOMAINS[0],0x30000000,True,m.MAX_SURFACE+1)
        with self.assertRaises(ValueError):space.guest(m.DOMAINS[0],0x10000000,True,65536)
        with self.assertRaises(ValueError):space.guest('overlay',0x10000000)

    def test_pitch_padding_and_pair_duplication(self):
        header=struct.pack('<8h',2048,1536,64,96,256,256,8,6)
        seen=bytes(6144);before=bytes([0xA5])*(1024*128)
        out=m.fog_upload(header,seen,before,1024)
        for row in range(128):
            self.assertEqual(out[row*1024:row*1024+344],b'\0\x80'*172)
            self.assertEqual(out[row*1024+344:(row+1)*1024],before[row*1024+344:(row+1)*1024])
        self.assertEqual(m.fog_pixels(header,bytes([1])*6144),bytes(44032))
        with self.assertRaises(ValueError):m.fog_upload(header,seen,bytes(512*128),511)
        with self.assertRaises(ValueError):m.fog_upload(header,seen,bytes(512*128-1),512)

    def test_original_440A10_full_CPU_execution_matches_independent_pixels(self):
        # This independent bounded engine executes the actual x87 sampling,
        # source getters, CRT conversion and successful debug-stack check. No
        # original function result/return instruction is intercepted or stubbed.
        u=Uc(UC_ARCH_X86,UC_MODE_32);size=(len(m.CODE)+4095)&-4096
        u.mem_map(0x400000,size,7);u.mem_write(0x400000,m.CODE);u.mem_protect(0x400000,size,5)
        u.mem_map(0x11000000,0x30000);u.mem_map(0x11400000,4096)
        u.mem_map(0x12742000,0x2000);u.mem_map(0x3D000000,0xB000)
        u.mem_map(0x12000000,0x20000);u.mem_map(0x12100000,4096)
        header=struct.pack('<8h',2048,1536,64,96,256,256,8,6)
        seen=bytes(0 if i%37 else 1 for i in range(6144));u.mem_write(0x11400000,header);u.mem_write(0x12742000,seen)
        for p,value,fmt in ((m.MAP+0x2659C,0x11400000,'I'),(m.MAP+0xA0,0x12742000,'I'),
                            (m.MAP+0x2658C,0x3D000000,'I'),(m.MAP+0x26544,172,'h'),(m.MAP+0x26546,128,'h'),
                            (m.MAP+0x2647C,2048/172,'f'),(m.MAP+0x26480,1536/128,'f')):
            u.mem_write(p,struct.pack('<'+fmt,value))
        stack=0x1200F000;u.mem_write(stack,struct.pack('<I',0x12100000))
        for reg,value in ((x86.UC_X86_REG_ESP,stack),(x86.UC_X86_REG_ECX,m.MAP),(x86.UC_X86_REG_FPCW,0x027F)):
            u.reg_write(reg,value)
        counters=dict(instructions=0,writes=0)
        ranges=((0x440A10,0x440AEE),(0x440AF0,0x440C0A),(0x43D1A0,0x43D1CD),
                (0x43D200,0x43D22D),(0x56CE80,0x56CE84),(0x56CF00,0x56D4D0))
        def code(uc,pc,n,_):
            self.assertTrue(any(a<=pc<z for a,z in ranges),hex(pc))
            self.assertEqual(bytes(uc.mem_read(pc,n)),m.CODE[pc-0x400000:pc-0x400000+n])
            self.assertNotEqual(m.CODE[pc-0x400000],0xCC)
            counters['instructions']+=1
        def write(uc,access,p,n,value,_):
            self.assertTrue((0x12000000<=p and p+n<=0x12020000) or
                            (0x3D000000<=p and p+n<=0x3D000000+44032),hex(p))
            counters['writes']+=1
        u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,write)
        u.emu_start(0x440A10,0x12100000,count=5_000_000)
        self.assertEqual(u.reg_read(x86.UC_X86_REG_EIP),0x12100000)
        self.assertEqual(u.reg_read(x86.UC_X86_REG_ESP),stack+4)
        self.assertEqual(bytes(u.mem_read(0x3D000000,44032)),m.fog_pixels(header,seen))
        self.assertGreater(counters['instructions'],100000)


if __name__=='__main__':unittest.main()
