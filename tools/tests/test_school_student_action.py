import struct,unittest
from copy import deepcopy
from tools.school_student_action import *


def fixture():
    work=0xE080C7C;w=bytearray(STRIDE*COUNT);put(w,0,1,'h');put(w,0x44,0x14000000);w[0x290]=25
    put(w,0x2EC,336<<16,'i');put(w,0x2F0,280<<16,'i');put(w,0x48+0x24,work+0x48);put(w,0x48+0x2C,0xE02F2F4)
    ctrl=bytearray(50);ctrl[4]=1;ctrl[24]=1;ctrl[26]=5;rec=bytearray(176);put(rec,2,3,'H');rec[15]=1
    s=source_contract();inputs={'work_pointer':work,'main_controller':0x14000000,'effect_controller':0x11000000,'main_metadata_pointer':0x150DFE00,
       'main_program_pointer':0x150DFE00+s['main']['offset'],'attachment_program_pointers':[0x11EEFD20+p['offset'] for p in s['attachments']], 'record_hex':rec.hex()}
    rows=[{'name':n,'pointer':p,'bytes':len(b),'hex':bytes(b).hex()} for n,p,b in [
       ('works',work,w),('pool',POOL,bytes(NODE*SLOTS)),('control',0xE108B30,ctrl),('task',0xE000000,bytes(400)),('current_work',0x7A49E0,struct.pack('<I',work))]]
    return inputs,rows


class SourceTests(unittest.TestCase):
    def test_raw_pose_archive_frames_and_sprite_layer(self):
        s=source_contract();self.assertEqual(s['pose_code'],89);self.assertEqual(s['direction_index'],1)
        self.assertEqual([p['duration'] for p in [s['main']]+s['attachments']],[30,6,30]);self.assertEqual(s['attachments'][0]['sprite'],1968)
        self.assertEqual(bytes.fromhex(s['attachments'][0]['sprite_hex'])[8],12)

    def test_main_binding_full_work_and_retained_pool(self):
        inputs,before=fixture();original=deepcopy(before);after=bind_project(inputs,before);w=bytes.fromhex(after[0]['hex'])
        self.assertEqual(before,original);self.assertEqual(w[0x28A],2);self.assertEqual(struct.unpack_from('<h',w,0x54)[0],18)
        self.assertEqual(u32(w,0x4C),inputs['main_program_pointer']);self.assertEqual(struct.unpack_from('<h',w,0x56)[0],30)
        self.assertEqual(after[1:],before[1:]);self.assertEqual(w[STRIDE:],bytes(STRIDE*(COUNT-1)))

    def test_original_pool_first_free_links_immediate_waits_and_cell_phase(self):
        inputs,before=fixture();pool=bytearray.fromhex(before[1]['hex']);pool[0]=1;before[1]['hex']=pool.hex()
        p=initialized_project(inputs,before);self.assertEqual(p['allocated_nodes'],[POOL+NODE,POOL+2*NODE]);self.assertEqual(p['linked_order'],[POOL+2*NODE,POOL+NODE])
        w=bytes.fromhex(p['after'][0]['hex']);out=bytes.fromhex(p['after'][1]['hex'])
        self.assertEqual(w[0x293],1);self.assertEqual(list(w[0x2E8:0x2EA]),[10,17]);self.assertEqual(u32(w,0x68),POOL+2*NODE)
        self.assertEqual(struct.unpack_from('<h',out,NODE+0xE)[0],5);self.assertEqual(struct.unpack_from('<h',out,2*NODE+0xE)[0],29)
        self.assertEqual(u32(out,NODE+0x18),12);self.assertEqual(u32(out,2*NODE+0x18),7);self.assertEqual(out[0:NODE],pool[0:NODE])
        self.assertEqual(out[3*NODE:],bytes(NODE*(SLOTS-3)))

    def test_first_animation_has_distinct_main_child_auxiliary_results(self):
        inputs,before=fixture();p=animated_project(inputs,before);w=bytes.fromhex(p['after'][0]['hex']);pool=bytes.fromhex(p['after'][1]['hex'])
        self.assertEqual(p['frame_waits'],[29,4,28]);self.assertEqual(p['auxiliary_returns'],[1]*5);self.assertEqual(p['main_return'],0)
        self.assertEqual(w[4],0);self.assertEqual(struct.unpack_from('<h',w,10)[0],1);self.assertEqual(w[0x49],1)
        self.assertEqual(pool[1],1);self.assertEqual(pool[NODE+1],1)

    def test_unsupported_eligibility_child_pool_and_auxiliary_refusals(self):
        inputs,before=fixture();bad=deepcopy(inputs);rec=bytearray.fromhex(bad['record_hex']);rec[164]=5;bad['record_hex']=rec.hex()
        with self.assertRaises(ValueError):bind_project(bad,before)
        bad=deepcopy(before);w=bytearray.fromhex(bad[0]['hex']);put(w,0x68,POOL);bad[0]['hex']=w.hex()
        with self.assertRaises(ValueError):initialized_project(inputs,bad)
        bad=deepcopy(before);bad[1]['hex']=(bytes([1])*NODE*SLOTS).hex()
        with self.assertRaises(ValueError):initialized_project(inputs,bad)
        bad=deepcopy(before);w=bytearray.fromhex(bad[0]['hex']);put(w,0xA4,1234);bad[0]['hex']=w.hex()
        with self.assertRaises(ValueError):animated_project(inputs,bad)


if __name__=='__main__':unittest.main()
