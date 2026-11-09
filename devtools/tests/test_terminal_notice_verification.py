import copy
import struct
import unittest
from devtools import terminal_school_handoff_verification as v


def fields():
    node=0x200000;game=0x40000000
    head=bytearray(512);struct.pack_into('<I',head,0,0x59A430)
    struct.pack_into('<II',head,0x34,2,5)
    head[0x43]=1;head[0x44]=3;head[0x59]=2
    activity=bytearray(32);activity[0]=activity[22]=1;activity[24]=9
    anim=bytearray(20);anim[:3]=bytes((1,2,0));struct.pack_into('<II',anim,8,0xFF00,0x800)
    gates=dict(pointer=node,controller_pointer=node+0x190,panel_pointer=node+0x117F20,
        backpointer_hex=struct.pack('<I',node).hex(),network_hex='00',panel_hex='00',
        controller_activity_hex=activity.hex(),game_pointer=game)
    for name,p,raw in [('notice',node+0x30B28,anim),('notice_flags',0x7F44B9,b'\1\0'),
        ('VM',0x7D7C28,bytes(128)),('keyboard_action',game+0x1950,bytes(4)),
        ('mouse_pressed',game+0x1990,bytes(4))]:
        gates[name+'_pointer']=p;gates[name+'_hex']=raw.hex()
    return head,gates,node,game


class NoticeVerificationTests(unittest.TestCase):
    def test_independent_original_contract(self):
        raw=v.menu.contract.read_source();self.assertEqual(v.notice_contract(raw)['instruction_checks'],13)
        changed=bytearray(raw);changed[0x99A61]^=1
        with self.assertRaises(ValueError):v.notice_contract(bytes(changed))

    def test_actual_notice_fields_and_false_modes_rejected(self):
        v.notice_fields(*fields())
        for field,offset,value in [('notice_hex',1,3),('notice_hex',2,1),('VM_hex',4,1),
                ('controller_activity_hex',24,12),('notice_flags_hex',0,0),
                ('keyboard_action_hex',1,0x80),('mouse_pressed_hex',0,1)]:
            head,gates,node,game=fields();raw=bytearray.fromhex(gates[field]);raw[offset]=value;gates[field]=raw.hex()
            with self.subTest(field=field,offset=offset),self.assertRaises(ValueError):v.notice_fields(head,gates,node,game)
        head,gates,node,game=fields();gates['notice_pointer']+=4
        with self.assertRaises(ValueError):v.notice_fields(head,gates,node,game)

    def test_transition_requires_real_edges_and_post_press_advance(self):
        def sample(t,state):
            anim=bytearray(20);anim[:3]=bytes((1,state,0))
            head=bytearray(29);head[:2]=bytes((1,3))
            return dict(wall_time_ns=t,notice_state_hex=anim.hex(),battle_head_tail_hex=head.hex())
        receipt=dict(action=dict(down_wall_time_ns=100),input_samples=[sample(90,2),sample(110,4)])
        result=v.notice_transition(receipt,dict(input_edges_observed=True))
        self.assertEqual(result['post_press_progress_samples'],[1]);self.assertFalse(result['accepted'])
        with self.assertRaises(ValueError):v.notice_transition(receipt,dict(input_edges_observed=False))
        for rows in ([sample(90,2),sample(110,2)],[sample(90,2),sample(95,4),sample(110,4)]):
            bad=copy.deepcopy(receipt);bad['input_samples']=rows
            with self.assertRaises(ValueError):v.notice_transition(bad,dict(input_edges_observed=True))


if __name__=='__main__':unittest.main()
