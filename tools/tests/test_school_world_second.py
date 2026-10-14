import unittest,struct
from copy import deepcopy
from tools.school_world_second import source_contract,project,NAMES
from tools.school_world_map import MAP_STATE_BYTES,MAP_STATE_BASE
from tools.school_world_command import STRIDE,COUNT


def fixture():
    task=bytearray(400);struct.pack_into('<I',task,0x38,5);task[0x170]=1
    ctrl=bytearray(50);struct.pack_into('<h',ctrl,2,1);ctrl[11]=255;ctrl[24]=1;ctrl[26]=4
    state=bytearray(MAP_STATE_BYTES);state[0x26595-MAP_STATE_BASE:0x26599-MAP_STATE_BASE]=bytes([1])*4
    fog=[0x20000000,0x21000000,0x22000000];works=bytearray(STRIDE*COUNT);struct.pack_into('<h',works,0,1)
    works[8]=255;works[0x290]=25;struct.pack_into('<2i',works,0x2EC,336<<16,280<<16)
    record=bytearray(176);record[15]=1
    rows=[{'index':i,'pointer':0xE080000+i*STRIDE,'used_word':1 if i==0 else 0,'record_hex':record.hex() if i==0 else None,
           'x_fixed':336<<16 if i==0 else 0,'y_fixed':280<<16 if i==0 else 0} for i in range(COUNT)]
    inputs={'mouse':[0,0],'map_state':0,'task_input':[0,0,0],'ctrl_keys':[0,0],
      'lists':{'works':rows,'team':0,'relation_hex':bytes(256).hex(),'opening':1,'event':0,'dimensions':[64,96],'origin':[9,16],'view':0,'camera':[0,0]}}
    data=[task,ctrl,bytes(24),struct.pack('<3I',*fog),state,bytes(6144),bytes([0x23])*6144,bytes([0x43])*6144,bytes(32),
      bytes(20),bytes(1004),bytes(5020),works,bytes(1016),bytes([0x57])*10,bytes([0x67])*2048,bytes(20),bytes(12288),bytes(4)]
    regions=[{'name':name,'pointer':fog[i-5] if i in (5,6,7) else 0x30000000+i*0x100000,'bytes':len(buf),'hex':bytes(buf).hex()} for i,(name,buf) in enumerate(zip(NAMES,data))]
    return inputs,regions


class SourceTests(unittest.TestCase):
    def test_exact_state4_and_mode25_source_dispatch(self):
        s=source_contract();self.assertEqual(s['mode25_target'],'0x475797');self.assertEqual(s['native_delay'],180)
        self.assertEqual(s['next_handler'],'0x475d60');self.assertEqual(len(s['functions']),5)

    def test_full_composed_pointer_swap_vision_and_first_work_admission(self):
        inputs,before=fixture();original=deepcopy(before);p=project(inputs,before);out={r['name']:bytes.fromhex(r['hex']) for r in p['after']}
        self.assertEqual(before,original);self.assertEqual(out['task'][0x170],0);self.assertEqual(out['control'][4],1)
        self.assertEqual(out['control'][26],5);self.assertEqual(struct.unpack_from('<h',out['control'],28)[0],180)
        self.assertEqual(struct.unpack('<3I',out['map_slots']),(0x20000000,0x22000000,0x21000000))
        self.assertEqual(out['fog_previous'][16*64+9],255);self.assertEqual(sum(out['fog_previous']),255)
        self.assertEqual(out['fog_current'],bytes([0x23])*6144);self.assertEqual(out['fog_history'][16*64+9],255)
        self.assertEqual(out['works'][8],127);self.assertEqual(out['works'][0x290],25)
        self.assertEqual(struct.unpack('<I',out['current_work'])[0],inputs['lists']['works'][0]['pointer'])
        self.assertEqual(p['display_indices'],[0]);self.assertEqual(p['tested_indices'],[0]);self.assertFalse(p['handler_executed'])
        for name in ('clock','queue','occupancy'):self.assertEqual(out[name],bytes.fromhex(next(r for r in before if r['name']==name)['hex']))

    def test_controller_queue_pending_and_mode_refusals(self):
        inputs,before=fixture()
        for name,offset,value in [('task',0x171,1),('control',26,5),('works',0x292,1),('works',0x290,2),('works',0x2A7,1),('queue',16,1)]:
            bad=deepcopy(before);r=next(r for r in bad if r['name']==name);b=bytearray.fromhex(r['hex']);b[offset]=value;r['hex']=b.hex()
            with self.assertRaises(ValueError):project(inputs,bad)

    def test_new_player_input_or_incomplete_region_refusal(self):
        inputs,before=fixture();inputs['task_input']=[1,0,0]
        with self.assertRaises(ValueError):project(inputs,before)
        inputs['task_input']=[0,0,0];before[12]['hex']=before[12]['hex'][:-2]
        with self.assertRaises(ValueError):project(inputs,before)


if __name__=='__main__':unittest.main()
