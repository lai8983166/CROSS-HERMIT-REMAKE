import hashlib
import io
import struct
import unittest

from devtools.vmware_vmss_cpu_v2 import parse_cpu_groups, CheckpointError
from devtools.vmware_vmss_state import decode_fxsave, decode_cpu_report


def checkpoint_tag(name, data, indices=()):
    extended = len(data) >= 62
    prefix = bytes([(len(indices) << 6) | (63 if extended else len(data)), len(name)])
    prefix += name.encode() + struct.pack("<" + "I" * len(indices), *indices)
    if extended:
        prefix += struct.pack("<QQH", len(data), len(data), 0)
    return prefix + data


def fixture():
    rows = [checkpoint_tag("cpu:numVCPUs", struct.pack("<I",1))]
    def add(name, raw, indices=(0,)):
        rows.append(checkpoint_tag(name,raw,indices))
    add("gpregs",struct.pack("<16Q",*range(1,17)))
    add("rip",struct.pack("<Q",0x401000))
    add("eflags",struct.pack("<I",0x82));add("EFLAGS",struct.pack("<I",0x40202))
    add("CR64",struct.pack("<9Q",*range(9)))
    add("DR64",struct.pack("<8Q",*range(8)))
    for i in range(8):
        add("S",struct.pack("<I",i*8),(0,i))
        add("S.base64",struct.pack("<Q",0x100000000 if i==7 else 0),(0,i))
        add("S.limit",struct.pack("<I",0xfffff),(0,i))
        add("S.rights",struct.pack("<I",0xc09b00),(0,i))
    for name in ("GDTR","IDTR"):add(name,struct.pack("<HQ",0x57,0x123456789))
    fx=bytearray(512);struct.pack_into("<H",fx,0,0x27f);struct.pack_into("<I",fx,24,0x1f80)
    add("fpu:fxstate",fx);add("fpu:vmFcs",b"\0\0");add("fpu:vmFds",b"\0\0")
    add("xsave:xheader",b"\0"*64);add("KERNELGSBASE",b"\0"*8)
    raw=b"".join(rows)+b"\0\0"
    header=struct.pack("<III64sQQ",0xBED2BED2,0,1,b"cpu",92,0)
    return parse_cpu_groups(io.BytesIO(header+raw),len(header)+len(raw))


class CpuStateTests(unittest.TestCase):
    def test_physical_fp_mapping_and_tags_nonzero_top(self):
        raw=bytearray(512);struct.pack_into("<H",raw,2,6<<11);raw[4]=0xc3
        # logical 0->physical6 normal; logical1->physical7 zero;
        # logical2->physical0 infinity; logical3->physical1 unnormal.
        for logical,(mant,exp) in enumerate([(1<<63,0x3fff),(0,0),(1<<63,0x7fff),(1,0x3fff)]):
            struct.pack_into("<QH",raw,32+16*logical,mant,exp)
        out=decode_fxsave(bytes(raw))["registers"]
        self.assertEqual(out["FP6"],[1<<63,0x3fff])
        self.assertEqual(out["FP0"],[1<<63,0x7fff])
        self.assertEqual(out["FPTAG"],2|(2<<2)|sum(3<<(2*i) for i in range(2,6))|(1<<14))

    def test_pointer_variant_is_explicit(self):
        raw=bytearray(512);struct.pack_into("<Q",raw,8,0x123456789abcdef0)
        self.assertEqual(decode_fxsave(bytes(raw))["missing"],["FIP","FDP","FCS","FDS"])
        self.assertEqual(decode_fxsave(bytes(raw),pointer_format="legacy32")["registers"]["FIP"],0x9abcdef0)
        self.assertEqual(decode_fxsave(bytes(raw),pointer_format="fxsave64")["registers"]["FIP"],0x123456789abcdef0)

    def test_raw_report_reparsed_and_64bit_bases_preserved(self):
        report=fixture();report["cpu_groups"][0]["tags"]=[{"name":"spoofed"}]
        cpu=decode_cpu_report(report)["cpus"][0]
        self.assertEqual(cpu["eflags"],0x40282)
        self.assertEqual(cpu["canonical_fields"]["TR"][1],0x100000000)
        self.assertTrue(cpu["unicorn32_descriptor_base_truncation_gap"])
        self.assertFalse(cpu["canonical57_mapping_complete"])
        complete=decode_cpu_report(report,fx_pointer_format="legacy32")["cpus"][0]
        self.assertEqual(len(complete["canonical_fields"]),57)
        self.assertFalse(complete["accepted"])

    def test_tampered_raw_identity_rejected(self):
        report=fixture();report["cpu_groups"][0]["raw_hex"]="ff"+report["cpu_groups"][0]["raw_hex"][2:]
        with self.assertRaises(CheckpointError):decode_cpu_report(report)

    def test_fxsave_matches_unicorn_physical_register_contract(self):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
        from unicorn import x86_const
        uc=Uc(UC_ARCH_X86,UC_MODE_32);uc.mem_map(0x1000,0x2000)
        # FNINIT; FLD1; FLDPI; FXSAVE [0x2000]. No native execution.
        code=bytes.fromhex("dbe3d9e8d9eb0fae0500200000")
        uc.mem_write(0x1000,code);uc.emu_start(0x1000,0x1000+len(code))
        decoded=decode_fxsave(bytes(uc.mem_read(0x2000,512)),pointer_format="legacy32")["registers"]
        for name in ("FPCW","FPSW","FPTAG","FOP","FIP","FDP","FCS","FDS"):
            self.assertEqual(decoded[name],uc.reg_read(getattr(x86_const,"UC_X86_REG_"+name)),name)
        for i in range(8):
            self.assertEqual(decoded[f"FP{i}"],list(uc.reg_read(x86_const.UC_X86_REG_FP0+i)))


if __name__ == "__main__":
    unittest.main()
