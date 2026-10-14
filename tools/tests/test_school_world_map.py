import unittest
import struct
from tools.school_world_map import source_contract,clock_step,pointer_outputs,project_map_frame,MAP_STATE_BYTES,MAP_STATE_BASE
from tools.tactics_exit_emulation import SOURCE


class WorldMapSourceTests(unittest.TestCase):
    def test_source_identity_ranges_and_hover_boundary_difference(self):
        c=source_contract();self.assertEqual(c['hover_screen_y'],[30,605]);self.assertEqual(c['pixel_screen_y'],[30,599])
        self.assertEqual(len(c['functions']),16)
        bad=bytearray(SOURCE.read_bytes());bad[0]^=1
        with self.assertRaises(ValueError):source_contract(bad)

    def test_exact_clock_gates_signed_wrap_and_negative_clamp(self):
        self.assertEqual(clock_step(1,1,5,7,0)['remaining'],5)
        self.assertEqual(clock_step(0,0,5,7,0)['elapsed'],7)
        self.assertEqual(clock_step(0,1,5,7,0),{'remaining':4,'elapsed':8,'limit':0,'return_eax':0,'increment_called':True})
        self.assertEqual(clock_step(0,128,0,0,0x7FFFFFFF)['return_eax'],1)
        self.assertEqual(clock_step(0,1,-0x80000000,0x7FFFFFFF,0x7FFFFFFF)['remaining'],0x7FFFFFFF)
        self.assertEqual(clock_step(0,1,2,0x7FFFFFFF,-1)['elapsed'],-0x80000000)
        with self.assertRaises(ValueError):clock_step(False,0,1,2,3)

    def test_pointer_bottom_edge_and_signed_division_pixel_truncation(self):
        self.assertEqual(pointer_outputs([31,29]),{'tile':[-1,-1],'pixel':[-1,-1]})
        self.assertEqual(pointer_outputs([31,30]),{'tile':[0,0],'pixel':[31,0]})
        self.assertEqual(pointer_outputs([31,599]),{'tile':[0,35],'pixel':[31,569]})
        self.assertEqual(pointer_outputs([31,605]),{'tile':[0,35],'pixel':[-1,-1]})
        self.assertEqual(pointer_outputs([31,606]),{'tile':[-1,-1],'pixel':[-1,-1]})
        self.assertEqual(pointer_outputs([-1,30]),{'tile':[0,0],'pixel':[-1,0]})
        self.assertEqual(pointer_outputs([2048,30]),{'tile':[-1,-1],'pixel':[2048,0]})
        with self.assertRaises(ValueError):pointer_outputs([True,30])

    def test_complete_map_swap_clear_preserves_history_and_unwritten_bytes(self):
        rows=[('map_slots',100,12),('map_state',200,MAP_STATE_BYTES),('fog_history',1000,6144),
              ('fog_current',8000,6144),('fog_previous',15000,6144),('minimap_globals',300,32)]
        before=[{'name':n,'pointer':p,'bytes':size,'hex':(b'Z'*size).hex()} for n,p,size in rows]
        before[0]['hex']=struct.pack('<3I',1000,8000,15000).hex()
        state=bytearray.fromhex(before[1]['hex']);idx=lambda o:o-MAP_STATE_BASE
        state[idx(0x26595):idx(0x26599)]=b'\1'*4;struct.pack_into('<2h',state,idx(0x265A6),0,0)
        struct.pack_into('<4I',state,0,1,2,3,4);before[1]['hex']=state.hex()
        out=project_map_frame(before)
        self.assertEqual(struct.unpack('<3I',bytes.fromhex(out[0]['hex'])),(1000,15000,8000))
        self.assertEqual(out[2:4],before[2:4]);self.assertEqual(out[4]['hex'],(b'\0'*6144).hex())
        self.assertEqual(bytes.fromhex(out[1]['hex'])[16:100],b'Z'*84)
        self.assertEqual(struct.unpack('<8I',bytes.fromhex(out[5]['hex'])),(1,2,4,6,1,2,3,4))
        bad=[r.copy() for r in before];bad[0]['hex']=struct.pack('<3I',1000,1000,15000).hex()
        with self.assertRaises(ValueError):project_map_frame(bad)


if __name__=='__main__':unittest.main()
