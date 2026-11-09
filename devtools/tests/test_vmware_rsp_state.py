import unittest

from devtools.vmware_rsp_state import (DecodeError, decode_frame, decode_payload,
    encode_packet, register_layout, decode_registers, decode_monitor_reply)


class RSPStateTests(unittest.TestCase):
    def xml(self):
        return {"target.xml": b'<target><architecture>i386:x86-64</architecture>'
            b'<feature><reg name="rax" bitsize="64" regnum="0"/></feature>'
            b'<xi:include href="sse.xml"/></target>',
            "sse.xml": b'<feature><reg name="xmm0" bitsize="128" regnum="1"/></feature>'}

    def test_frame_binary_roundtrip_and_checksum(self):
        raw = b"a$#}*\x00\xff"
        frame = encode_packet(raw)
        self.assertEqual(decode_frame(frame), raw)
        with self.assertRaises(DecodeError):
            decode_frame(frame[:-2] + b"00")

    def test_rle_is_bounded_and_escaped_star_literal(self):
        self.assertEqual(decode_payload(b"0* "), b"0000")
        self.assertEqual(decode_payload(b"}\x0a"), b"*")
        for value in (b"* ", b"a*", b"a*#", b"a*$", b"a*\x7f", b"a}", b"$"):
            with self.subTest(value=value), self.assertRaises(DecodeError):
                decode_payload(value)
        with self.assertRaises(DecodeError):
            decode_payload(b"0*~", limit=16)

    def test_xml_binds_raw_register_bytes_without_float_conversion(self):
        state = decode_registers(b"0100000000000000" + b"ff" * 16, self.xml())
        self.assertEqual(state["registers"]["rax"]["value_hex"], "0000000000000001")
        self.assertEqual(state["registers"]["xmm0"]["raw_hex"], "ff" * 16)
        self.assertFalse(state["fullstate"])
        self.assertFalse(state["accepted"])

    def test_unknown_layout_is_not_guessed(self):
        state = decode_registers(b"00" * 536)
        self.assertFalse(state["layout_known"])
        self.assertEqual(state["registers"], {})

    def test_unavailable_and_length_fail_closed(self):
        state = decode_registers(b"x" * 16 + b"00" * 16, self.xml())
        self.assertEqual(state["unavailable"], ["rax"])
        self.assertIsNone(state["registers"]["rax"]["value_hex"])
        for data in (b"00", b"00" * 25, b"0x" * 8 + b"00" * 16):
            with self.subTest(data=data), self.assertRaises(DecodeError):
                decode_registers(data, self.xml())

    def test_xml_missing_annex_entity_cycle_and_number_gap(self):
        cases = []
        missing = self.xml(); del missing["sse.xml"]; cases.append(missing)
        entity = self.xml(); entity["target.xml"] = b'<!DOCTYPE target [<!ENTITY x "x">]>' + entity["target.xml"]; cases.append(entity)
        cycle = self.xml(); cycle["sse.xml"] = b'<feature><xi:include href="target.xml"/></feature>'; cases.append(cycle)
        gap = self.xml(); gap["sse.xml"] = gap["sse.xml"].replace(b'regnum="1"', b'regnum="2"'); cases.append(gap)
        duplicate = self.xml(); duplicate["sse.xml"] = duplicate["sse.xml"].replace(b'xmm0', b'rax'); cases.append(duplicate)
        for case in cases:
            with self.subTest(case=case), self.assertRaises(DecodeError):
                register_layout(case)

    def test_monitor_console_and_final_hex(self):
        self.assertEqual(decode_monitor_reply([b"O6869", b"0a"]), b"hi\n")
        self.assertEqual(decode_monitor_reply([b"O6869", b"OK"]), b"hi")
        for packets in ([b"O6869"], [b"E01"], [b"OK", b"OK"], []):
            with self.subTest(packets=packets), self.assertRaises(DecodeError):
                decode_monitor_reply(packets)


if __name__ == "__main__":
    unittest.main()
