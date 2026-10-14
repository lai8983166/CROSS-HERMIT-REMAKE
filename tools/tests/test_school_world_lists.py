import unittest,struct
from copy import deepcopy
from tools.school_world_lists import source_contract,vision_merge,viewport,project


class WorldListSourceTests(unittest.TestCase):
    def fixture(self,depths=(2,2,3)):
        records=[]
        for n in range(250):
            record=bytearray(176);record[15]=1
            records.append({'index':n,'pointer':10000+n*0x520,'used_word':1 if n<3 else 0,
                'x_fixed':100<<16,'y_fixed':depths[n]<<16 if n<3 else 0,'record_hex':record.hex() if n<3 else None})
        inputs={'works':records,'team':0,'relation_hex':(b'\1'*256).hex(),'opening':1,'event':0,'dimensions':[64,96],'origin':[9,16],'view':0,'camera':[0,0]}
        regions=[{'name':name,'pointer':n+1,'bytes':size,'hex':(b'Z'*size).hex()} for n,(name,size) in enumerate([
            ('window',20),('fog_current',6144),('fog_history',6144),('visible',1004),('categories',5020)])]
        return inputs,regions

    def test_source_masks_all_shapes_and_clipped_max_merge(self):
        masks=source_contract()['masks'];self.assertEqual(len(masks),33);self.assertEqual(masks[0]['payload_hex'],'ff000000')
        current,history=vision_merge(b'\0'*6144,b'\0'*6144,0,0,1)
        self.assertEqual([current[0],current[1],current[64],current[65]],[255,159,159,0]);self.assertEqual(current,history)
        a,b=vision_merge(current,b'\xff'*6144,0,0,1);self.assertEqual(a,current);self.assertEqual(b,b'\xff'*6144)
        with self.assertRaises(ValueError):vision_merge(current,history,0,0,33)

    def test_source_swap_ties_and_unwritten_output_tails(self):
        inputs,regions=self.fixture();before=deepcopy(regions);p=project(inputs,regions)
        self.assertEqual(p['display_indices'],[2,1,0]);self.assertEqual(p['category_counts'],[3,0,0,3,3])
        self.assertEqual(p['after'][3]['hex'][32:],regions[3]['hex'][32:]);self.assertEqual(regions,before)
        inputs,regions=self.fixture((2,2,2));self.assertEqual(project(inputs,regions)['display_indices'],[0,1,2])

    def test_occupied_deferred_record_is_not_displayable_and_groups_are_separate(self):
        inputs,regions=self.fixture();r=bytearray.fromhex(inputs['works'][1]['record_hex']);r[15]=11;inputs['works'][1]['record_hex']=r.hex()
        r=bytearray.fromhex(inputs['works'][2]['record_hex']);r[164]=1;inputs['works'][2]['record_hex']=r.hex()
        p=project(inputs,regions);self.assertEqual(p['occupied_slots'],3);self.assertEqual(p['display_state1_slots'],2)
        self.assertEqual(p['category_counts'],[2,0,1,1,1]);self.assertNotIn(1,p['display_indices'])
        r=bytearray.fromhex(inputs['works'][1]['record_hex']);r[15]=0;inputs['works'][1]['record_hex']=r.hex()
        p=project(inputs,regions);self.assertEqual(p['category_counts'],[2,1,1,1,1]);self.assertNotIn(1,p['display_indices'])
        inputs['team']=16
        with self.assertRaises(ValueError):project(inputs,regions)

    def test_viewport_short_truncation_inclusive_edges(self):
        for x,y in [(-64,-34),(1088,664),(65536,65536)]:self.assertTrue(viewport(x,y))
        for x,y in [(-65,0),(1089,0),(0,-35),(0,665)]:self.assertFalse(viewport(x,y))
        with self.assertRaises(ValueError):viewport(True,0)


if __name__=='__main__':unittest.main()
