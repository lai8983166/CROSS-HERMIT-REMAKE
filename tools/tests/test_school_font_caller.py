import struct
import unittest
from tools.school_font_caller import source_contract,project_owner,gamma_bytes,HEADS,ARENA


class SourceTests(unittest.TestCase):
    def test_original_success_bind_queues_and_gamma_call_source(self):
        c=source_contract();self.assertEqual(c['queue_allocations'],[32768,1048576])
        self.assertEqual(c['phases']['gamma']['stop'],'0x416cfa')
        self.assertFalse(c['gamma']['call_instruction_executed'])

    def test_full_owner_projection_retains_padding_and_unrelated_fields(self):
        for fill in (0xA5,0xCC):
            before=bytes([fill])*0xC000
            bound=project_owner(before,'bind',0x20000000,0x12345678)
            self.assertEqual(struct.unpack_from('<2I',bound,0x1058),(0x20000000,0x12345678))
            self.assertEqual(bound[:0x1058],before[:0x1058]);self.assertEqual(bound[0x1060:],before[0x1060:])
            queued=project_owner(bound,'queues',0x20000000,0x12345678)
            self.assertEqual(struct.unpack_from('<4I',queued,0x1060),(4096,1048576,HEADS,ARENA))
            gamma=project_owner(queued,'gamma',0x20000000,0x12345678)
            self.assertEqual(gamma[:0xB408],queued[:0xB408]);self.assertEqual(gamma[0xBA08:],queued[0xBA08:])
            self.assertEqual(gamma[0xB408:0xBA08],gamma_bytes())

    def test_original_gamma_unsigned16_values_are_three_complete_channels(self):
        self.assertEqual(struct.unpack('<768H',gamma_bytes()),tuple(i<<8 for i in range(256))*3)

    def test_invalid_projection_inputs_refused(self):
        for before,phase,owner in ((bytes(96),'bind',1),(bytes(0xC000),'bad',1),(bytes(0xC000),'bind',0)):
            with self.assertRaises(ValueError):project_owner(before,phase,owner,2)
