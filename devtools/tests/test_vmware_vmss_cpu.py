import io
import struct
import unittest

from devtools.vmware_vmss_cpu import CheckpointError, parse_cpu_groups


def group(name, offset):
    return struct.pack("<64sQQ", name.encode(), offset, 0)


def small_tag(name, data, indices=()):
    return bytes([(len(indices) << 6) | len(data), len(name)]) + name.encode() + struct.pack("<" + "I" * len(indices), *indices) + data


def fixture(tags):
    directory_end = 12 + 160
    cpu = tags + b"\0\0"
    return struct.pack("<III", 0xBED3BED3, 0, 2) + group("cpu", directory_end) + group("memory", directory_end + len(cpu)) + cpu + b"RAM_MUST_NOT_BE_READ"


class CpuTagTests(unittest.TestCase):
    def test_cpu_only_reads_and_original_bytes(self):
        tags = small_tag("rip", (0x12345678).to_bytes(8, "little"), (0,))
        blob = fixture(tags)
        boundary = blob.index(b"RAM_MUST_NOT_BE_READ")

        class Guarded(io.BytesIO):
            def read(self, n=-1):
                if n < 0 or self.tell() + n > boundary:
                    raise AssertionError("memory read attempted")
                return super().read(n)

        result = parse_cpu_groups(Guarded(blob), len(blob))
        cpu = result["cpu_groups"][0]
        self.assertEqual(bytes.fromhex(cpu["raw_hex"]), tags + b"\0\0")
        self.assertEqual(cpu["tags"][0]["little_endian_scalar"], 0x12345678)
        self.assertFalse(result["memory_groups_read"])
        self.assertFalse(result["fullstate"])

    def test_extended_payload_preserved_not_guessed_or_inflated(self):
        tag = bytes([126, 5]) + b"xsave" + struct.pack("<IQQH", 1, 4, 4096, 3) + b"PAD" + b"ABCD"
        blob = fixture(tag)
        result = parse_cpu_groups(io.BytesIO(blob), len(blob))
        out = result["cpu_groups"][0]["tags"][0]
        self.assertEqual((out["disk_size"],out["memory_size"],out["indices"]), (4,4096,[1]))
        self.assertNotIn("little_endian_scalar", out)

    def test_truncated_data_and_group_boundary_rejected(self):
        blob = fixture(b"\x08\x03rip" + b"\x01")
        with self.assertRaises(CheckpointError):
            parse_cpu_groups(io.BytesIO(blob), len(blob))

    def test_bad_magic_count_and_duplicate_groups_rejected(self):
        base = fixture(small_tag("rip", b"\0" * 8))
        for blob in (b"AAAA" + base[4:], base[:8] + struct.pack("<I",513) + base[12:],
                     base[:92] + group("cpu",172) + base[172:]):
            with self.subTest(), self.assertRaises(CheckpointError):
                parse_cpu_groups(io.BytesIO(blob), len(blob))

    def test_duplicate_tag_and_invalid_name_rejected(self):
        tag = small_tag("rip", b"\0" * 8, (0,))
        for tags in (tag + tag, b"\x08\x00", small_tag("r\0p", b"\0" * 8)):
            blob = fixture(tags)
            with self.subTest(), self.assertRaises(CheckpointError):
                parse_cpu_groups(io.BytesIO(blob), len(blob))

    def test_extended_huge_size_rejected_without_large_read(self):
        tag = bytes([63, 5]) + b"xsave" + struct.pack("<QQH", 2**40, 2**40, 0)
        blob = fixture(tag)
        with self.assertRaises(CheckpointError):
            parse_cpu_groups(io.BytesIO(blob), len(blob))


if __name__ == "__main__":
    unittest.main()
