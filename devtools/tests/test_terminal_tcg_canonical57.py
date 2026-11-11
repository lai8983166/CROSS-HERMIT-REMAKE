"""Offline projection/readback/refusal tests; no VM or native game execution."""
import copy
import hashlib
import json
import struct
import unittest
from pathlib import Path

from devtools.terminal_tcg_canonical57 import (
    Canonical57Error, SCHEMA, from_tcg, from_unicorn, full_tag)
from tools.terminal_unit_frontends_trace import CPU_REGISTERS

ROOT = Path(__file__).resolve().parents[2]
WORKER = ROOT / '.venv-audit/native-worker'
SOURCES = ('tcg-roundtrip32-v2', 'tcg-device-restore-v4-rich', 'tcg-device-restore-v4-zero')


def actual(name, key=None):
    report = json.loads((WORKER/name/'report.json').read_bytes())
    return report[(key or ('states' if name == SOURCES[0] else 'before'))][0]


def project(raw):
    return from_tcg(raw, expected_cpu=0, expected_vcpus=2)


def unicorn_from_source(name, raw):
    """Explicit test initialization; never presented as a production restorer.

    Load actual GDT memory before selectors, physical FP before full tags,
    and do NOT initialize Unicorn DR4/5 padding to fake alias compatibility.
    """
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
    from unicorn import x86_const as x
    u = Uc(UC_ARCH_X86, UC_MODE_32)
    u.mem_map(0x100000, 0x5000)
    elf = (WORKER/name/'guest.elf').read_bytes()
    u.mem_write(0x100000, elf[4096:8192])
    r = project(raw)['registers']
    order = ['GDTR','IDTR','LDTR','TR','CR0','CR2','CR3','CR4']
    order += ['CS','DS','ES','FS','GS','SS']
    order += [f'FP{i}' for i in range(8)]
    order += [k for k in CPU_REGISTERS if k not in order and k not in ('DR4','DR5')]
    for name in order:
        value = r[name]
        u.reg_write(getattr(x,'UC_X86_REG_'+name),tuple(value) if type(value) is list else value)
    return u


class CanonicalTests(unittest.TestCase):
    def test_real_sources_and_no_mutation(self):
        for name in SOURCES:
            raw = actual(name); original = copy.deepcopy(raw)
            result = project(raw)
            self.assertEqual(raw, original)
            self.assertEqual(tuple(result['registers']), CPU_REGISTERS)
            self.assertEqual(result['schema'], SCHEMA)
            self.assertFalse(result['legacy_unicorn_raw_api_compatible'])
            self.assertFalse(result['replay_accepted'])
            self.assertEqual(result['registers']['DR4'],result['registers']['DR6'])
            self.assertEqual(result['registers']['DR5'],result['registers']['DR7'])

    def test_actual_restored_states_project_equal(self):
        for name in SOURCES[1:]:
            r=json.loads((WORKER/name/'report.json').read_bytes())
            self.assertEqual(project(r['before'][0])['registers'],project(r['after'][0])['registers'])
            self.assertEqual(project(r['disturbed'][0])['registers'],project(r['second_b'][0])['registers'])
            self.assertNotEqual(project(r['before'][0])['registers'],project(r['disturbed'][0])['registers'])

    def test_original_fxsave_physical_order(self):
        r = project(actual(SOURCES[0]))['registers']
        fx=(WORKER/SOURCES[0]/'guest.bin').read_bytes()[:512]
        top=(struct.unpack_from('<H',fx,2)[0]>>11)&7
        physical=[None]*8
        for logical in range(8):
            physical[(logical+top)&7]=list(struct.unpack_from('<QH',fx,32+logical*16))
        self.assertEqual(physical,[r[f'FP{i}']for i in range(8)])
        self.assertEqual(full_tag(physical,fx[4]^0xff),r['FPTAG'])
        self.assertEqual(struct.unpack_from('<I',fx,8)[0],r['FIP'])
        self.assertEqual(struct.unpack_from('<I',fx,16)[0],r['FDP'])

    def test_zero_special_normal_empty_classification(self):
        physical=[[0x8000000000000000,0x3fff],[0,0],[0,0x8000],[1,0],
                  [0x8000000000000000,0x7fff],[0xc000000000000000,0x7fff],
                  [1,0x3fff],[0x8000000000000000,0]]
        self.assertEqual(full_tag(physical,0),0xaa94)
        self.assertEqual(full_tag(physical,0x42),0xba9c)
        self.assertEqual(full_tag(physical,255),0xffff)

    def test_high_mode_and_hidden_extended_values_rejected(self):
        r=json.loads((WORKER/'tcg-device-restore64-v4/report.json').read_bytes())
        with self.assertRaises(Canonical57Error):project(r['before'][0])
        for field in ('eip','fip','fdp','eflags'):
            raw=actual(SOURCES[0]);raw[field]='0000000100000000'
            with self.subTest(field=field),self.assertRaises(Canonical57Error):project(raw)
        for group,index in [('gpr',0),('gpr',8),('cr0_cr2_cr3_cr4',2),('dr0_dr1_dr2_dr3_dr6_dr7',0)]:
            raw=actual(SOURCES[0]);raw[group][index]='0000000100000000'
            with self.subTest(group=group,index=index),self.assertRaises(Canonical57Error):project(raw)
        raw=actual(SOURCES[0]);raw['xmm_low64_high64'][8][0]='0000000000000001'
        with self.assertRaises(Canonical57Error):project(raw)

    def test_descriptor_widths_and_unused_fields_refused(self):
        for index,field,value in [(8,0,1),(9,3,1),(8,2,0x10000),(6,1,0x100000000),(0,1,0x100000000)]:
            raw=actual(SOURCES[0]);raw['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][index][field]=f'{value:016x}'
            with self.subTest(index=index,field=field),self.assertRaises(Canonical57Error):project(raw)

    def test_unknown_missing_malformed_and_unstopped_rejected(self):
        changes=[lambda r:r.pop('fcs'),lambda r:r.update(extra=0),
                 lambda r:r.update(cpu=True),lambda r:r.update(fp_control=True),
                 lambda r:r.update(fop=0x800),lambda r:r.update(fip='100000'),
                 lambda r:r.update(top=1),lambda r:r.update(fp_empty_mask=256),
                 lambda r:r.update(dr4_dr5_policy='raw slots'),
                 lambda r:r['vp_stopped'][1].update(stopped=False),
                 lambda r:r['vp_stopped'][1].update(cpu=0),
                 lambda r:r['cr0_cr2_cr3_cr4'].__setitem__(3,'0000000000000208'),
                 lambda r:r.update(efer='0000000000000500'),
                 lambda r:r.update(eflags='0000000000020002')]
        for change in changes:
            raw=actual(SOURCES[0]);change(raw)
            with self.subTest(change=change),self.assertRaises(Canonical57Error):project(raw)

    def test_real_unicorn_full57_write_read(self):
        from unicorn import x86_const as x
        for name in SOURCES:
            raw=actual(name);u=unicorn_from_source(name,raw)
            after=from_unicorn(u)
            self.assertEqual(after['registers'],project(raw)['registers'])
            self.assertEqual(u.reg_read(x.UC_X86_REG_DR4),0)
            self.assertNotEqual(after['registers']['DR4'],u.reg_read(x.UC_X86_REG_DR4))

    def test_unicorn_dr6_mutation_alias_and_de_refusal(self):
        from unicorn import x86_const as x
        u=unicorn_from_source(SOURCES[1],actual(SOURCES[1]))
        # MOV DR6,EAX; MOV EBX,DR4. APIs must agree on the NEW architecture
        # contract even though the old DR4 padding stays zero.
        u.reg_write(x.UC_X86_REG_EAX,0xffff0ff1)
        code=bytes.fromhex('0f23f00f21e3')
        u.mem_write(0x103000,code)
        u.emu_start(0x103000,0x103000+len(code),timeout=100000,count=2)
        r=from_unicorn(u)['registers']
        self.assertEqual(r['DR4'],r['DR6'])
        self.assertEqual(r['DR4'],r['EBX'])
        self.assertEqual(u.reg_read(x.UC_X86_REG_DR4),0)
        u.reg_write(x.UC_X86_REG_CR4,r['CR4']|8)
        with self.assertRaises(Canonical57Error):from_unicorn(u)

    def test_unicorn_16bit_descriptor_or_null_cs_refusal(self):
        u=unicorn_from_source(SOURCES[1],actual(SOURCES[1]))
        # Read adapter refuses an incompatible descriptor instead of treating
        # constructor UC_MODE_32 as proof of current protected CS semantics.
        raw=bytearray(u.mem_read(0x100808,8));raw[6]&=~0x40
        u.mem_write(0x100808,bytes(raw))
        with self.assertRaises(Canonical57Error):from_unicorn(u)


if __name__ == '__main__':
    unittest.main()
