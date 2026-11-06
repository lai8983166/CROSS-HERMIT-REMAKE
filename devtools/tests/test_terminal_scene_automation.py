import copy
import struct
import unittest
from devtools.terminal_scene_automation import transition


class TransitionTests(unittest.TestCase):
    def fixture(self):
        rows=[]
        for i,(t,down,pc) in enumerate(((100,False,154),(110,True,172),(130,False,172))):
            keyboard=bytearray(0xA00);keyboard[0x4B9]=128 if down else 0
            vm=bytearray(128);struct.pack_into('<I',vm,28,pc)
            rows.append(dict(index=i,wall_time_ns=t,foreground_hwnd=123,
                             keyboard_hex=keyboard.hex(),VM_hex=vm.hex()))
        receipt=dict(input_returned=True,released=True,down_result=1,up_results=[1],
                     scan_code=0x39,hold_ms=120,down_wall_time_ns=105,up_wall_time_ns=125)
        return rows,receipt

    def test_observed_transition(self):
        rows,receipt=self.fixture()
        r=transition(rows,receipt,154,123)
        self.assertEqual((r['press_index'],r['release_index'],r['after_PC']),(1,2,172))
        self.assertFalse(r['full_instruction_causality_proved'])

    def test_delivery_without_game_input_rejected(self):
        rows,receipt=self.fixture()
        rows[1]['keyboard_hex']=bytes(0xA00).hex()
        with self.assertRaises(ValueError):transition(rows,receipt,154,123)

    def test_no_release_or_no_advancement_rejected(self):
        for field in ('release','advance'):
            rows,receipt=self.fixture()
            if field=='release':rows[2]['keyboard_hex']=rows[1]['keyboard_hex']
            else:
                for r in rows:r['VM_hex']=rows[0]['VM_hex']
            with self.subTest(field=field),self.assertRaises(ValueError):transition(rows,receipt,154,123)

    def test_receipt_scope_and_focus_rejected(self):
        for key,value in (('input_returned',False),('released',False),('scan_code',1),
                          ('hold_ms',500),('down_result',0),('up_results',[0]),
                          ('down_wall_time_ns',90),('up_wall_time_ns',140)):
            rows,receipt=self.fixture();receipt[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):transition(rows,receipt,154,123)
        rows,receipt=self.fixture();rows[1]['foreground_hwnd']=124
        with self.assertRaises(ValueError):transition(rows,receipt,154,123)

    def test_truncated_or_unordered_raw_fields_rejected(self):
        rows,receipt=self.fixture();rows[1]['keyboard_hex']='00'
        with self.assertRaises(ValueError):transition(rows,receipt,154,123)
        rows,receipt=self.fixture();rows[1]['index']=99
        with self.assertRaises(ValueError):transition(rows,receipt,154,123)


if __name__=='__main__':unittest.main()
