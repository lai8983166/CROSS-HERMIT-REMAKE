import hashlib
import io
import struct
import unittest

from devtools.tests.test_vmware_vmss_state import fixture
from devtools.vmware_vmss_cpu_v2 import parse_cpu_groups, CheckpointError
from devtools.vmware_vmss_state import decode_cpu_report as decode_v1
from devtools.vmware_vmss_state_v2 import decode_cpu_report


def v3_fixture():
    raw = bytes.fromhex(fixture()["cpu_groups"][0]["raw_hex"])
    header = struct.pack("<III64sQQ", 0xBED3BED3, 8, 1, b"cpu", 92, len(raw))
    return parse_cpu_groups(io.BytesIO(header + raw), len(header) + len(raw))


class SnapshotStateTests(unittest.TestCase):
    def test_v2_semantics_preserved_and_v3_equivalent(self):
        old = fixture()
        baseline = decode_v1(old)
        self.assertEqual(decode_cpu_report(old)["cpus"], baseline["cpus"])
        report = v3_fixture()
        decoded = decode_cpu_report(report)
        self.assertEqual(decoded["cpus"], baseline["cpus"])
        self.assertEqual(decoded["container_profile"],
                         {"magic": "bed3bed3", "version": 3, "header_reserved": 8})
        self.assertFalse(decoded["same_stopped_epoch_verified"])
        self.assertFalse(decoded["accepted"])
        with self.assertRaises(CheckpointError):
            decode_v1(report)

    def test_unknown_and_inconsistent_profiles_rejected(self):
        for key, value in (("magic", "bed4bed4"), ("version", 2),
                           ("header_reserved", 0), ("header_reserved", True)):
            report = v3_fixture()
            report[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(CheckpointError):
                decode_cpu_report(report)

    def test_header_bytes_are_checked(self):
        for raw in ("", "not hex", "00" * (12 + 513 * 80)):
            report = v3_fixture()
            report["header_and_directory_hex"] = raw
            with self.subTest(raw_length=len(raw)), self.assertRaises(CheckpointError):
                decode_cpu_report(report)

    def test_raw_integrity_and_missing_extended_payload_rejected(self):
        report = v3_fixture()
        group = report["cpu_groups"][0]
        group["raw_hex"] = "ff" + group["raw_hex"][2:]
        with self.assertRaises(CheckpointError):
            decode_cpu_report(report)
        # A valid new digest cannot make a truncated extended GP payload valid.
        report = v3_fixture()
        group = report["cpu_groups"][0]
        gp = next(t for t in group["tags"] if t["name"] == "gpregs")
        raw = bytes.fromhex(group["raw_hex"])[:gp["data_offset"] - group["offset"] + 8]
        group.update(raw_hex=raw.hex(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        with self.assertRaises(CheckpointError):
            decode_cpu_report(report)


if __name__ == "__main__":
    unittest.main()
