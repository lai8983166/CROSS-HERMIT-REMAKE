from devtools.tests.test_terminal_owned_mouse import inert_cursor
import copy
import struct
import unittest
from devtools import terminal_battle_input as battle
from devtools.tests.test_terminal_menu_input import Api


class BattleInputTests(unittest.TestCase):
    def row(self,stage='request'):
        head=bytearray(0x200);head[0x30]=stage=='confirmation';struct.pack_into('<I',head,0x38,5)
        activity=bytearray(0x20);activity[0]=activity[8]=1;node=0x30000
        gates=dict(pointer=node,network_hex='00',panel_hex='00',panel_pointer=node+0x117F20,
            controller_pointer=node+0x190,controller_activity_hex=activity.hex(),backpointer_hex=struct.pack('<I',node).hex())
        return dict(tasks=[dict(pointer=node,vtable=battle.BATTLE,thread_id=9,TLS={},scene_head_hex=head.hex(),battle_gates=gates)],
            scene_global=node,MAIN_event_hex='00'*8,frames=[dict(tid=9,chain=[dict(return_va=x)for x in (0x453CB5,0x451ABC,0x451716,0x421F8A,0x56E183)])])
    def test_original_ordinary_gates_and_separate_confirmation(self):
        self.assertTrue(battle.ready(self.row(),'request'));self.assertTrue(battle.ready(self.row('confirmation'),'confirmation'))
        self.assertFalse(battle.ready(self.row(),'confirmation'))
    def test_script_network_panel_owner_and_ancestor_refused(self):
        for reason in ('script','network','panel','owner','ancestor','other_task'):
            r=self.row();t=r['tasks'][0]
            if reason=='script':
                h=bytearray.fromhex(t['scene_head_hex']);h[0x43]=h[0x59]=1;t['scene_head_hex']=h.hex()
            elif reason=='network':t['battle_gates']['network_hex']='01'
            elif reason=='panel':t['battle_gates']['panel_hex']='01'
            elif reason=='owner':r['scene_global']+=4
            elif reason=='ancestor':r['frames'][0]['chain'].pop()
            else:r['tasks'].append(copy.deepcopy(t))
            self.assertFalse(battle.ready(r,'request'),reason)
    def test_explicit_permission_required(self):
        with self.assertRaises(PermissionError):battle.action(None,None,'request')
    def test_only_two_reviewed_targets_and_release_on_failure(self):
        for stage in ('request','confirmation'):
            api=Api();api.xy=battle.TARGETS[stage]
            api.geometry=lambda target:dict(screen_target=list(target),virtual_desktop=[0,0,1024,768])
            r=battle.guarded_click(inert_cursor(api),lambda:None,stage,lambda _:None)
            self.assertEqual(r['target'],list(battle.TARGETS[stage]));self.assertEqual(api.flags,[2,4])
        with self.assertRaises(ValueError):battle.guarded_click(Api(),lambda:None,'unknown')
    def test_already_retreating_never_submits_again(self):
        r=self.row();h=bytearray.fromhex(r['tasks'][0]['scene_head_hex']);h[0x31]=1;r['tasks'][0]['scene_head_hex']=h.hex()
        self.assertFalse(battle.ready(r,'request'))


if __name__=='__main__':unittest.main()
