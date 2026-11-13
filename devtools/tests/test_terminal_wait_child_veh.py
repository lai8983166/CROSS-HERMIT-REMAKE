"""Mutation rejection on the actual bounded host fixture; never starts processes."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import unittest

from devtools import terminal_wait_child_veh_preflight as preflight


class NativeReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = preflight.ROOT/'analysis/terminal-wait-child-veh-preflight-v3-20261113.json'
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != 'd9b5a5a2aaf5798bc6b16ba9e20ae5be42e82eb627005323700fe8775f619169':
            raise ValueError('fixed original v3 native report')
        cls.report = json.loads(raw)
        cls.cases = []
        for case in cls.report['cases']:
            blobs = []
            for source in case['sources']:
                data = Path(source['path']).read_bytes()
                if len(data) != source['bytes'] or hashlib.sha256(data).hexdigest() != source['sha256']:
                    raise ValueError('fixed original native bytes')
                blobs.append(data)
            cls.cases.append((blobs[0], json.loads(blobs[1])))

    def rejected_word(self, offset, value, message):
        raw = bytearray(self.cases[1][0])
        struct.pack_into('<I', raw, offset, value)
        with self.assertRaisesRegex(ValueError, message):
            preflight.decode(bytes(raw), self.cases[1][1], True)

    def test_actual_baseline_and_precise_faults(self):
        for gated, (raw, debugger) in zip((False, True), self.cases):
            result = preflight.decode(raw, debugger, gated)
            self.assertEqual(result['actual_returns'], [0, 0, 0, 258])
            self.assertEqual(result['exact_preconsumer_stops'], 4 if gated else 0)
            self.assertFalse(result['game_acquisition_allowed'])
            self.assertFalse(result['full57'])

    def test_already_consumed_before_hold_is_rejected(self):
        self.rejected_word(280+9*4, 1, 'held before consumption')

    def test_wrong_fault_ip_is_rejected(self):
        offset = 280+76+2*716+184
        self.rejected_word(offset, preflight.word(self.cases[1][0], offset)+1, 'exact fault')

    def test_substituted_wait_result_is_rejected(self):
        self.rejected_word(280+76+2*716+176, 258, 'returned EAX')

    def test_modified_RF_in_resume_is_rejected(self):
        offset = 280+76+3*716+192
        self.rejected_word(offset, preflight.word(self.cases[1][0], offset)^0x10000, 'non-DR context including RF')

    def test_modified_SIMD_in_resume_is_rejected(self):
        self.rejected_word(280+76+3*716+204+160, 0x1234, 'non-DR context including RF')

    def test_missing_actual_DR_restore_is_rejected(self):
        self.rejected_word(280+76+4*716+24, 1, 'debug state restored')

    def test_other_armed_slot_is_rejected(self):
        self.rejected_word(280+76+716+24, 5, 'one execution breakpoint')

    def test_preexisting_RF_is_not_silently_cleared(self):
        offset = 280+76+192
        self.rejected_word(offset, preflight.word(self.cases[1][0], offset)|0x10000, 'RF/TF')

    def test_replacing_debugger_reply_is_rejected(self):
        debugger = copy.deepcopy(self.cases[1][1])
        next(r for r in debugger['events'] if r['exception'] in (0x80000004, 0x4000001e))['reply'] = 0x10002
        with self.assertRaisesRegex(ValueError, 'NOT_HANDLED'):
            preflight.decode(self.cases[1][0], debugger, True)

    def test_unreported_extra_exception_is_rejected(self):
        debugger = copy.deepcopy(self.cases[1][1])
        extra = dict(next(r for r in debugger['events'] if r['type'] == 1))
        extra['exception'] = 0xc0000005
        debugger['events'].append(extra)
        with self.assertRaisesRegex(ValueError, 'hidden or second-chance'):
            preflight.decode(self.cases[1][0], debugger, True)

    def test_parent_abnormal_cleanup_is_rejected(self):
        debugger = dict(self.cases[1][1], forced=True)
        with self.assertRaisesRegex(ValueError, 'normal current child exit'):
            preflight.decode(self.cases[1][0], debugger, True)


if __name__ == '__main__':
    unittest.main()
