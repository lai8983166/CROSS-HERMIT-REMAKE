import io
import unittest

from devtools.vmware_vmss_cpu_v2 import parse_cpu_groups, CheckpointError
from devtools.tests.test_vmware_vmss_cpu import fixture, small_tag


class RepeatedCpuTagsTests(unittest.TestCase):
    def test_repeated_tags_preserve_both_original_payloads(self):
        first = small_tag("smmVersion", b"\x01\0\0\0", (0,))
        second = small_tag("smmVersion", b"\x02\0\0\0", (0,))
        raw = fixture(first + second)
        result = parse_cpu_groups(io.BytesIO(raw), len(raw))
        cpu = result["cpu_groups"][0]
        self.assertEqual(cpu["duplicate_identities"], [{"name":"smmVersion", "indices":[0], "count":2}])
        self.assertEqual([t["occurrence"] for t in cpu["tags"]], [0,1])
        self.assertEqual([t["little_endian_scalar"] for t in cpu["tags"]], [1,2])
        self.assertEqual(bytes.fromhex(cpu["raw_hex"]), first + second + b"\0\0")
        self.assertFalse(result["fullstate"])

    def test_invalid_names_and_bounds_still_rejected(self):
        for tags in (b"\x08\x00", b"\x08\x03rip\x01"):
            raw = fixture(tags)
            with self.subTest(tags=tags), self.assertRaises(CheckpointError):
                parse_cpu_groups(io.BytesIO(raw),len(raw))


if __name__ == "__main__":
    unittest.main()
