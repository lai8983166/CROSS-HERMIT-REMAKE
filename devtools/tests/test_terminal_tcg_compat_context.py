"""Offline compatibility envelope tests; never starts a VM or native guest."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from devtools import terminal_tcg_compat_context as c

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '.venv-audit/native-worker/tcg-compatibility-v8b/report.json'
SOURCE_SHA = '34b5d318f69c011644088c5843107d945311e5f05df69daf3ea6e64421321d1c'


def original():
    data = SOURCE.read_bytes()
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA:
        raise RuntimeError('fixed actual compatibility capture changed')
    return json.loads(data)['state']


def kwargs(raw):
    return dict(expected_cpu=0, expected_vcpus=2, expected_source_sha256=c.source_digest(raw))


class CompatibilityContextTests(unittest.TestCase):
    def setUp(self):
        self.raw = original()
        self.anchor = kwargs(self.raw)
        self.envelope = c.pack(self.raw, **self.anchor)

    def test_actual_lossless_and_high_fields(self):
        self.assertEqual(c.unpack(self.envelope, **self.anchor), self.raw)
        v = self.envelope['view32']
        self.assertEqual(len(v['registers']), 57)
        self.assertEqual(v['retained_context']['extended_gpr_r8_r15'][0], 0x123456789abcdef0)
        self.assertEqual(v['retained_context']['segment_caches']['FS'][1], 0x100000000)
        self.assertEqual(v['registers']['FIP'], 0x10010039f)
        self.assertEqual(v['registers']['FDP'], 0x100100904)
        self.assertEqual(v['retained_context']['extended_xmm8_xmm15'][7],
                         0xefcdab8967452301e0ac6824df9b5713)
        self.assertEqual(v['registers']['FP7'], [0xc000000000000000, 0x4000])
        self.assertEqual(v['registers']['FPTAG'], 0x3fff)
        self.assertEqual(v['retained_context']['top'], 7)
        self.assertFalse(self.envelope['unicorn32_replay_admitted'])
        self.assertFalse(self.envelope['legacy_unicorn32_load_format'])
        self.assertFalse(self.envelope['windows_admitted'])
        self.assertEqual(c.unpack(json.loads(json.dumps(self.envelope)), **self.anchor), self.raw)

    def test_synthetic_full_width_gpr_control_descriptor_retention(self):
        r = deepcopy(self.raw)
        r['gpr'][0] = 'f123456789abcdef'
        r['cr0_cr2_cr3_cr4'][1] = 'ff123456789abcde'
        r['dr0_dr1_dr2_dr3_dr6_dr7'][0] = '0000000100123456'
        for i in (6, 7, 8, 9):
            r['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][i][1] = '0000000200123456'
        e = c.pack(r, **kwargs(r))
        self.assertEqual(e['view32']['registers']['EAX'], 0x89abcdef)
        self.assertEqual(e['view32']['retained_context']['gpr_upper32'][0], 0xf1234567)
        self.assertEqual(e['view32']['registers']['CR2'], 0xff123456789abcde)
        self.assertEqual(e['view32']['registers']['DR0'], 0x100123456)
        for name in ('GDTR', 'IDTR', 'LDTR', 'TR'):
            self.assertEqual(e['view32']['registers'][name][1], 0x200123456)
        self.assertEqual(c.unpack(e, **kwargs(r)), r)

    def test_de1_capture_does_not_invent_readable_dr45(self):
        r = deepcopy(self.raw)
        r['cr0_cr2_cr3_cr4'][3] = '0000000000000628'
        e = c.pack(r, **kwargs(r))
        for name in ('DR4', 'DR5'):
            self.assertEqual(e['view32']['registers'][name],
                             {'readable': False, 'reason': 'CR4.DE=1: #UD'})
        self.assertEqual(c.unpack(e, **kwargs(r)), r)
        self.assertFalse(e['unicorn32_replay_admitted'])

    def test_de0_aliases_are_not_old_api_padding(self):
        regs = self.envelope['view32']['registers']
        self.assertEqual(regs['DR4'], regs['DR6'])
        self.assertEqual(regs['DR5'], regs['DR7'])
        self.assertEqual(regs['DR4'], 0xffff0ff0)

    def test_external_anchor_rejects_even_internally_rehashed_raw(self):
        e = deepcopy(self.envelope)
        e['raw64']['gpr'][8] = '123456789abcdef1'
        e['source']['canonical_json_sha256'] = c.source_digest(e['raw64'])
        with self.assertRaises(c.CompatContextError):
            c.unpack(e, **self.anchor)
        with self.assertRaises(c.CompatContextError):
            c.pack(self.raw, **dict(self.anchor, expected_source_sha256='0' * 64))

    def test_derived_view_and_qualification_tamper(self):
        variants = []
        for key, value in [('capture_lossless', 1), ('full_machine_state', True),
                           ('windows_admitted', True), ('schema', 'legacy'),
                           ('unicorn32_replay_admitted', True)]:
            e = deepcopy(self.envelope)
            e[key] = value
            variants.append(e)
        e = deepcopy(self.envelope)
        e['view32']['registers']['FIP'] &= 0xffffffff
        variants.append(e)
        e = deepcopy(self.envelope)
        e['view32']['retained_context']['segment_caches']['FS'][1] = 0
        variants.append(e)
        e = deepcopy(self.envelope)
        e['view32']['registers']['DR4'] = 0
        variants.append(e)
        e = deepcopy(self.envelope)
        e['extra'] = False
        variants.append(e)
        for i, e in enumerate(variants):
            with self.subTest(i=i), self.assertRaises(c.CompatContextError):
                c.unpack(e, **self.anchor)

    def test_topology_rejection(self):
        for key, value in [('expected_cpu', 1), ('expected_vcpus', 1),
                           ('expected_cpu', False), ('expected_vcpus', 0)]:
            with self.subTest(key=key, value=value), self.assertRaises(c.CompatContextError):
                c.pack(self.raw, **dict(self.anchor, **{key: value}))
        for value in [False, 1, None]:
            r = deepcopy(self.raw)
            r['vp_stopped'][1]['stopped'] = value
            with self.subTest(value=value), self.assertRaises(c.CompatContextError):
                c.pack(r, **kwargs(r))

    def test_mode_and_cache_consistency_rejection(self):
        variants = []
        for key, value in [('efer', '0000000000000000'), ('hflags', '000000000040c2b0'),
                           ('target_bits', 32), ('eflags', '0000000000020046'),
                           ('eip', '0000000100100600')]:
            r = deepcopy(self.raw)
            r[key] = value
            variants.append(r)
        for index, value in [(0, '0000000000000033'), (3, '0000000000000600'),
                             (3, '0000000000000420')]:
            r = deepcopy(self.raw)
            r['cr0_cr2_cr3_cr4'][index] = value
            variants.append(r)
        r = deepcopy(self.raw)
        r['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][1][3] = '0000000000af9b00'
        variants.append(r)
        for i, r in enumerate(variants):
            with self.subTest(i=i), self.assertRaises(c.CompatContextError):
                c.pack(r, **kwargs(r))

    def test_strict_fields_widths_and_types(self):
        variants = []
        for key, value in [('fp_status', True), ('top', 6), ('mxcsr', 0x10000),
                           ('fop', 0x800), ('fcs', -1), ('fp_empty_mask', 256),
                           ('eip', '100600'), ('fip', '000000010010039F')]:
            r = deepcopy(self.raw)
            r[key] = value
            variants.append(r)
        r = deepcopy(self.raw)
        del r['fds']
        variants.append(r)
        r = deepcopy(self.raw)
        r['new_field'] = 'not silently ignored'
        variants.append(r)
        r = deepcopy(self.raw)
        r['xmm_low64_high64'].pop()
        variants.append(r)
        r = deepcopy(self.raw)
        r['fp_physical_low64_high16'][0][1] = '0000000000010000'
        variants.append(r)
        for i, r in enumerate(variants):
            with self.subTest(i=i), self.assertRaises(c.CompatContextError):
                c.pack(r, **kwargs(r))

    def test_detached_inputs_outputs(self):
        saved = deepcopy(self.raw)
        self.raw['gpr'][8] = '0000000000000000'
        self.assertEqual(c.unpack(self.envelope, **self.anchor), saved)
        result = c.unpack(self.envelope, **self.anchor)
        result['gpr'][8] = '0000000000000000'
        self.assertEqual(c.unpack(self.envelope, **self.anchor), saved)


if __name__ == '__main__':
    unittest.main()
