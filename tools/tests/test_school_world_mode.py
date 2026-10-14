import unittest
from copy import deepcopy
from tools.school_world_mode import source_contract,project,admitted_request,first_entry_update
from tools.tactics_exit_emulation import SOURCE


class WorldModeSourceTests(unittest.TestCase):
    def setUp(self):
        self.contract=source_contract()
        self.before=[{'name':name,'pointer':i+1,'bytes':size,'hex':(bytes([0x5A])*size).hex()}
                     for i,(name,size) in enumerate([('control',50),('map_flags',4),('task_flags',329)])]

    def test_original_branches_map_dispatch_task_owner_and_leaf_offsets(self):
        self.assertEqual([row[1] for row in self.contract['branches']['partial']],[1,1,0,0,0,0])
        self.assertEqual(self.contract['map_modes'][2][-1],[0x26598,0])
        self.assertEqual(self.contract['task_leaf_offsets'],[0x20E8,0x216C,0x2230])
        self.assertEqual(len(self.contract['functions']),6)

    def test_full_owned_regions_and_unchanged_gaps_in_each_request(self):
        for kind,flag in [(-1,0),(1,0),(1,1),(1,128),(2,0),(2,1),(2,255)]:
            out=project(self.before,kind,flag,self.contract)
            self.assertEqual(self.before[0]['hex'],(b'Z'*50).hex())
            control=bytes.fromhex(out[0]['hex']);task=bytes.fromhex(out[2]['hex'])
            self.assertEqual(control[7],0x5A)
            self.assertEqual(control[:4],b'Z'*4);self.assertEqual(control[13:],b'Z'*37)
            self.assertEqual(task[1:132],b'Z'*131);self.assertEqual(task[133:328],b'Z'*195)
            if kind==1:
                self.assertEqual(bytes.fromhex(out[1]['hex']),bytes([0 if flag else 1])*4)
                self.assertEqual([task[0],task[132],task[328]],[1 if flag else 0]*3)
            if kind==2 and flag:
                self.assertEqual([control[i] for i in [4,5,6,8,9,10]],[1,1,0,0,0,0])
            self.assertEqual(control[11:13],b'\xff\xff' if kind!=-1 else b'\xff\0')

    def test_wrong_source_invalid_request_and_incomplete_regions_refuse(self):
        bad=bytearray(SOURCE.read_bytes());bad[0]^=1
        with self.assertRaises(ValueError):source_contract(bad)
        for kind,flag in [(0,1),(3,1),(-2,0),(True,0),(1,256),(1,-1),(1,False)]:
            with self.assertRaises(ValueError):admitted_request(kind,flag)
        with self.assertRaises(ValueError):project(self.before[:2],1,1,self.contract)

    def test_source_first_controller_update_preserves_request_and_full_regions(self):
        from tools.school_entry_control_catalog import native_fixture
        before=deepcopy(native_fixture()['cases'][0]['entry_control']['before'])
        original=deepcopy(before);after=first_entry_update(before)
        self.assertEqual(before,original)
        self.assertEqual(after[0],before[0])
        expected=bytearray.fromhex(before[1]['hex']);expected[26]=4
        self.assertEqual(bytes.fromhex(after[1]['hex']),expected)
        self.assertEqual(bytes.fromhex(after[2]['hex']),b'\0'*4)
        bad=deepcopy(after)
        with self.assertRaises(ValueError):first_entry_update(bad)


if __name__=='__main__':unittest.main()
