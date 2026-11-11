"""v2 preserves pointer payload width; synthetic oracle is NOT a new capture."""
import json
import unittest
from pathlib import Path
from devtools import terminal_tcg_canonical57 as v1
from devtools import terminal_tcg_canonical57_v2 as v2
from devtools.tests.test_terminal_tcg_canonical57 import (
    SOURCES, WORKER, actual, unicorn_from_source)


def project(raw):
    return v2.from_tcg(raw,expected_cpu=0,expected_vcpus=2)


def width_oracle():
    """Synthetic ordinary32 context with two actual high parent pointer values.

    Only the pointer scalar values are imported; this explicitly does not
    represent the actual long-mode parent, which remains rejected as a whole.
    """
    path=WORKER/'tcg-device-restore64-v4/report.json'
    high=json.loads(path.read_bytes())['before'][0]
    raw=actual(SOURCES[1])
    raw['fip'],raw['fdp']=high['fip'],high['fdp']
    return raw, path


class CanonicalV2Tests(unittest.TestCase):
    def test_real_ordinary32_projections_unchanged_except_version(self):
        for name in SOURCES:
            raw=actual(name)
            self.assertEqual(project(raw)['registers'],v1.from_tcg(raw,expected_cpu=0,expected_vcpus=2)['registers'])
            self.assertEqual(project(raw)['schema'],'x86-architectural-canonical57-v2')
            self.assertEqual(v2.from_unicorn(unicorn_from_source(name,raw))['registers'],project(raw)['registers'])

    def test_actual_high_payloads_in_synthetic_width_oracle(self):
        from unicorn import x86_const as x
        raw,_=width_oracle()
        expected=project(raw)['registers']
        self.assertGreater(expected['FIP'],0xffffffff)
        self.assertGreater(expected['FDP'],0xffffffff)
        u=unicorn_from_source(SOURCES[1],actual(SOURCES[1]))
        u.reg_write(x.UC_X86_REG_FIP,expected['FIP'])
        u.reg_write(x.UC_X86_REG_FDP,expected['FDP'])
        self.assertEqual(v2.from_unicorn(u)['registers'],expected)
        with self.assertRaises(v1.Canonical57Error):
            v1.from_tcg(raw,expected_cpu=0,expected_vcpus=2)

    def test_uint64_pointer_boundary_without_masking(self):
        raw=actual(SOURCES[1]);raw['fip']='ffffffffffffffff';raw['fdp']='8000000000000000'
        r=project(raw)['registers']
        self.assertEqual(r['FIP'],0xffffffffffffffff)
        self.assertEqual(r['FDP'],0x8000000000000000)
        for value in ('10000000000000000','-000000000000001','00000000000000GG',0):
            raw=actual(SOURCES[1]);raw['fip']=value
            with self.assertRaises(v2.Canonical57Error):project(raw)

    def test_other_high_fields_and_compat_mode_still_refused(self):
        changes=[lambda r:r.update(eip='0000000100000000'),
                 lambda r:r['gpr'].__setitem__(0,'0000000100000000'),
                 lambda r:r['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][8].__setitem__(1,'0000000100000000'),
                 lambda r:r.update(efer='0000000000000500'),
                 lambda r:r['cr0_cr2_cr3_cr4'].__setitem__(3,'0000000000000208')]
        for change in changes:
            raw=actual(SOURCES[1]);change(raw)
            with self.assertRaises(v2.Canonical57Error):project(raw)
        high=json.loads((WORKER/'tcg-device-restore64-v4/report.json').read_bytes())['before'][0]
        with self.assertRaises(v2.Canonical57Error):project(high)


if __name__=='__main__':unittest.main()
