import struct
import unittest
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn import x86_const as x86

from tools import terminal_unit_frontends_images as images


class UnitImageContractTests(unittest.TestCase):
    def test_original_frame_geometry_returns_real_archive_row(self):
        from tools import terminal_unit_frontends_emulation as source

        asset = images.unit_asset(1)
        code = source.previous.CODE
        entry, caller, index = source.UNIT_FRAME_GEOMETRY, 0x40B30A, 11
        self.assertEqual(code[caller-5-0x400000], 0xE8)
        self.assertEqual(caller + struct.unpack_from('<i', code, caller-4-0x400000)[0], entry)
        u = Uc(UC_ARCH_X86, UC_MODE_32)
        size = (len(code)+4095)&-4096
        u.mem_map(0x400000, size, 7)
        u.mem_write(0x400000, code)
        u.mem_protect(0x400000, size, 5)
        stack, owner, metadata = 0x12000000, 0x12100000, 0x12200000
        u.mem_map(stack, 4096)
        u.mem_map(owner, 4096)
        u.mem_map(metadata, 0x4000)
        raw = asset['raw'][:asset['metadata_bytes']]
        u.mem_write(metadata, raw)
        u.mem_protect(metadata, 0x4000, 1)
        table = metadata + asset['sections'][5]
        u.mem_write(owner+4, struct.pack('<I', table))
        sp = stack + 0x800
        u.mem_write(sp, struct.pack('<II', caller, index))
        u.reg_write(x86.UC_X86_REG_ECX, owner)
        u.reg_write(x86.UC_X86_REG_ESP, sp)

        def check_code(uc, pc, size, _):
            self.assertIn(pc, source.ALLOWED)
            self.assertEqual(bytes(uc.mem_read(pc, size)), code[pc-0x400000:pc-0x400000+size])

        u.hook_add(UC_HOOK_CODE, check_code)
        u.emu_start(entry, caller, count=200)
        self.assertEqual(u.reg_read(x86.UC_X86_REG_EIP), caller)
        self.assertEqual(u.reg_read(x86.UC_X86_REG_ESP), sp+8)
        self.assertEqual(u.reg_read(x86.UC_X86_REG_EAX), table+index*8)
        self.assertNotIn(0x41ED26, source.ALLOWED)

    def test_original_unit_status_dispatch_uses_live_record_and_command(self):
        from tools import terminal_unit_frontends_emulation as source

        code = source.previous.CODE
        u = Uc(UC_ARCH_X86, UC_MODE_32)
        for page in (0x469000, 0x56C000):
            u.mem_map(page, 4096, 7)
            u.mem_write(page, code[page-0x400000:page-0x400000+4096])
            u.mem_protect(page, 4096, 5)
        base = 0x12000000
        u.mem_map(base, 0x3000)
        unit, record, sp = base+0x1000, base+0x2000, base+0x800
        caller = 0x46D042
        u.mem_map(caller & -4096, 4096, 5)
        u.mem_write(unit+0x258, struct.pack('<I', record))
        u.hook_add(UC_HOOK_CODE, lambda _, pc, size, ctx: self.assertIn(pc, source.ALLOWED))
        for alive, command, expected in ((1, 1, 0), (1, 5, 1), (0, 5, 0)):
            with self.subTest(alive=alive, command=command):
                u.mem_write(record+0xF, bytes([alive]))
                u.mem_write(unit+0x290, bytes([command]))
                u.mem_write(sp, struct.pack('<II', caller, unit))
                u.reg_write(x86.UC_X86_REG_ESP, sp)
                u.reg_write(x86.UC_X86_REG_ECX, base)
                u.emu_start(0x469500, caller, count=200)
                self.assertEqual(u.reg_read(x86.UC_X86_REG_EIP), caller)
                self.assertEqual(u.reg_read(x86.UC_X86_REG_ESP), sp+8)
                self.assertEqual(u.reg_read(x86.UC_X86_REG_EAX), expected)
        self.assertNotIn(0x469523, source.ALLOWED)

    def test_initial_cache_owner_contract_and_late_reconfiguration_refused(self):
        class Inputs(images.ImagesMixin):
            def __init__(self):
                self.uc = Uc(UC_ARCH_X86,UC_MODE_32)
                for p,n in ((images.CTRL,0x120000),(images.MAIN,0x10000),(0x7A4000,0x1000)):
                    self.uc.mem_map(p,n)
                self.mutable = []
                self.space = images.UnitAddressSpace()
                self.device_ptr = 0x64001000
                self.uc.mem_write(images.MAIN+0xB210,struct.pack('<I',self.device_ptr))
                self.uc.mem_write(0x7A49FC,struct.pack('<I',images.MAIN))
                self.uc.mem_write(0x7A4A00,struct.pack('<I',images.MAIN))
                self.uc.mem_write(images.CTRL+0x2A6F0,bytes([1,3,1,0])+struct.pack('<I',0x11300000)+bytes([1,4,1,0])+struct.pack('<I',0x12622000))
                self.instructions = 0
            def get(self,p):
                return struct.unpack('<I',self.uc.mem_read(p,4))[0]
            def mark(self):
                return dict(instructions=self.instructions)
        m = Inputs()
        m.configure_unit_inputs()
        self.assertEqual(m.get(0x7A4A00),images.PATH_OWNER)
        self.assertEqual(m.get(0x7A49FC),images.MAIN)
        self.assertEqual(m.read(images.CTRL+0x2A6F0,4096),bytes(4096))
        self.assertEqual(m.read(images.MAIN+0x844+20*8+4,4),bytes(4))
        self.assertEqual(m.read(images.PATH_OWNER+0xBF4,1),b'\0')
        self.assertTrue(m.unit_input_changes[0]['before_hex'].startswith('0103'))
        self.assertEqual(len(m.unit_input_changes),2)
        with self.assertRaises(ValueError):
            m.configure_unit_inputs()
        late = Inputs()
        late.instructions = 1
        with self.assertRaises(ValueError):
            late.configure_unit_inputs()

    def test_original_archives_complete_and_large_extents(self):
        for job, count, large in ((1,209,15),(3,251,5)):
            a = images.unit_asset(job)
            self.assertEqual(len(a['rows']),count)
            self.assertEqual(sum(r['texture_size'][0]*r['texture_size'][1]*2 > 65536 for r in a['rows']),large)
            self.assertEqual(max(r['texture_size'][0]*r['texture_size'][1]*2 for r in a['rows']),262144)
            self.assertEqual(a['metadata_bytes'],12284 if job == 1 else 17180)
        self.assertEqual(images.helper_contract()['CRT']['max_blocks'],32)
        self.assertEqual(images.helper_contract()['GPU']['max_textures'],1024)

    def test_disjoint_small_and_full_large_surface_projection(self):
        s = images.UnitAddressSpace()
        d = images.PREFIX+'0-83'
        p = s.guest(d,101)
        s.surface_bytes[d] = 262144
        bits = s.result(d,{'bits':202})['bits']
        self.assertEqual(p,images.UNIT_POOL+83*images.UNIT_STRIDE+0x1000)
        self.assertEqual(bits,images.LARGE_POOL)
        self.assertLessEqual(bits+262144,images.LARGE_POOL+images.LARGE_STRIDE)
        d2 = images.PREFIX+'1-2'
        s.surface_bytes[d2] = 65536
        b2 = s.result(d2,{'bits':203})['bits']
        self.assertEqual(b2,images.UNIT_POOL+302*images.UNIT_STRIDE+0x10000)
        self.assertLessEqual(b2+65536,images.UNIT_POOL+303*images.UNIT_STRIDE)
        self.assertLess(images.UNIT_POOL+600*images.UNIT_STRIDE,images.PATH_OWNER)
        self.assertLess(images.PATH_OWNER+images.PATH_BYTES,images.LARGE_POOL)
        self.assertGreaterEqual(images.UNIT_POOL,0x32200000)
        self.assertEqual(s.result(d,{'bits':202})['bits'],bits)

    def test_projection_overflow_extent_alias_and_domain_refused(self):
        s = images.UnitAddressSpace()
        d = images.PREFIX+'0-1'
        with self.assertRaises(ValueError):
            s.result(d,{'bits':5})
        s.surface_bytes[d] = 262145
        with self.assertRaises(ValueError):
            s.result(d,{'bits':5})
        with self.assertRaises(ValueError):
            s.guest(images.PREFIX+'2-0',1)
        with self.assertRaises(ValueError):
            s.guest(images.PREFIX+'0-300',1)
        s.guest_to_native[images.UNIT_POOL+images.UNIT_STRIDE+0x1000] = ('other',22)
        with self.assertRaises(ValueError):
            s.guest(d,8)
        for i in range(40):
            domain = images.PREFIX+'1-'+str(i)
            s.surface_bytes[domain] = 131072
            s.result(domain,{'bits':100+i})
        domain = images.PREFIX+'1-40'
        s.surface_bytes[domain] = 131072
        with self.assertRaises(ValueError):
            s.result(domain,{'bits':999})

    def test_independent_palette_stride_and_full_padding_prediction(self):
        # Three source pixels plus the original fourth stride byte. Both rows
        # are converted; texture pitch and unused rows retain their old bytes.
        blob = bytearray(54+1024+8)
        blob[:2] = b'BM'
        struct.pack_into('<I',blob,10,1078)
        struct.pack_into('<ii',blob,18,3,2)
        struct.pack_into('<H',blob,28,8)
        struct.pack_into('<I',blob,46,256)
        blob[1078:] = bytes((2,1,0,2,1,2,2,0))
        palette = bytearray(1024)
        palette[0:4] = bytes((248,0,0,0))
        palette[8:12] = bytes((0,248,0,0))
        before = bytes([0x77])*64
        out = images.unit_bmp8_upload(bytes(blob),bytes(palette),before,16,4,1)
        self.assertEqual(out[:8],struct.pack('<4H',0,0x83E0,0x83E0,0))
        self.assertEqual(out[16:24],struct.pack('<4H',0x83E0,0,0,0x83E0))
        self.assertEqual(out[8:16],before[8:16])
        self.assertEqual(out[24:],before[24:])
        opaque = images.unit_bmp8_upload(bytes(blob),bytes(palette),before,16,4,0)
        self.assertEqual(struct.unpack_from('<H',opaque,0)[0],0x801F)
        self.assertEqual(blob[54:1078],bytes(1024))


if __name__ == '__main__':
    unittest.main()
