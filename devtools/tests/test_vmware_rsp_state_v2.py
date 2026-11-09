import unittest

from devtools.vmware_rsp_state import DecodeError
from devtools.vmware_rsp_state_v2 import decode_registers, parse_monitor_register


class PrefixAndMonitorTests(unittest.TestCase):
    def xml(self):
        return {"target.xml": b'<target><architecture>i386:x86-64</architecture><feature>'
            b'<reg name="rax" bitsize="64" regnum="0"/>'
            b'<reg name="st0" bitsize="80" regnum="1"/>'
            b'<reg name="xmm0" bitsize="128" regnum="2"/></feature></target>'}

    def test_prefix_absent_is_not_zero(self):
        decoded = decode_registers(b"01" + b"00" * 7, self.xml())
        self.assertEqual(decoded["missing"], ["st0", "xmm0"])
        self.assertIsNone(decoded["registers"]["st0"]["raw_hex"])
        self.assertEqual(decoded["registers"]["st0"]["status"], "absent_from_g")
        self.assertFalse(decoded["fullstate"])

    def test_partial_and_oversized_g_still_rejected(self):
        for n in (0, 7, 9, 17, 19, 35):
            with self.subTest(n=n), self.assertRaises(DecodeError):
                decode_registers(b"00" * n, self.xml())

    def test_individual_registers_bound_by_xml_and_conflicts_rejected(self):
        out = decode_registers(b"00" * 8, self.xml(), {1:b"01" * 10, 2:b"02" * 16})
        self.assertEqual(out["missing"], [])
        self.assertFalse(out["fullstate"])
        self.assertFalse(out["stopped_epoch_verified"])
        self.assertEqual(out["registers"]["st0"]["source"], "p")
        for p in ({1:b"00" * 8}, {3:b"00" * 4}, {0:b"01" * 8}, {0:b""}):
            with self.subTest(p=p), self.assertRaises(DecodeError):
                decode_registers(b"00" * 8, self.xml(), p)

    def test_p_unavailable_and_unsupported_remain_distinct(self):
        out = decode_registers(b"00" * 8, self.xml(), {1:b"", 2:b"x" * 32})
        self.assertEqual(out["registers"]["st0"]["status"], "unsupported_p")
        self.assertEqual(out["registers"]["xmm0"]["status"], "unavailable")
        out = decode_registers(b"00" * 8, self.xml(), {1:b"E01"})
        self.assertEqual(out["registers"]["st0"]["status"], "p_error")

    def test_observed_control_and_table_text(self):
        self.assertEqual(parse_monitor_register("r cr0", b"cr0=0x80050031\n")["fields"],
                         {"value": 0x80050031})
        out = parse_monitor_register("r gdtr", b"gdtr base=0xffffd2809f050fb0 limit=0x57\n")
        self.assertEqual(out["fields"]["reported_base"], 0xffffd2809f050fb0)
        with self.assertRaises(DecodeError):
            parse_monitor_register("r cr3", b"cr0=0x80050031\n")

    def test_segment_report_is_not_effective_gs_base(self):
        out = parse_monitor_register("r gs", b"gs 0x2b base 0x00000000 limit 0xffffffff type 0x3 s 1 dpl 3 p 1 db 1\n")
        self.assertEqual(out["fields"]["reported_base"], 0)
        self.assertFalse(out["effective_base_verified"])
        self.assertNotIn("g", out["fields"])
        out = parse_monitor_register("r ldtr", b"ldtr sel 0x0 base 0x0 limit 0x00000000 type 0x0 s 0 dpl 0 p 0\n")
        self.assertNotIn("db", out["fields"])

    def test_empty_dr_reply_is_not_value(self):
        out = parse_monitor_register("r dr7", b"")
        self.assertFalse(out["available"])
        self.assertEqual(out["fields"], {})
        with self.assertRaises(DecodeError):
            parse_monitor_register("r dr7", b"dr7=0x0\n")
        with self.assertRaises(DecodeError):
            parse_monitor_register("r cr0", b"cr0=0x10000000000000000\n")


if __name__ == "__main__":
    unittest.main()
