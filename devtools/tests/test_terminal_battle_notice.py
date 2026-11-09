import copy
import struct
import unittest

from devtools import terminal_battle_notice as notice
from devtools.tests.test_terminal_menu_input import Api
from devtools.tests.test_terminal_owned_mouse import inert_cursor


class NoticeTests(unittest.TestCase):
    def row(self):
        node = 0x30000
        game = 0x40000
        head = bytearray(512)
        struct.pack_into('<II', head, 0x34, 2, 5)
        head[0x43] = 1
        head[0x44] = 3
        head[0x59] = 2
        activity = bytearray(32)
        activity[0] = activity[0x16] = 1
        activity[0x18] = 9
        anim = bytearray(20)
        anim[:3] = b'\x01\x02\x00'
        struct.pack_into('<II', anim, 8, 0xFF00, 0x800)
        gates = dict(pointer=node,network_hex='00',panel_hex='00',panel_pointer=node+0x117F20,
                     controller_pointer=node+0x190,controller_activity_hex=activity.hex(),
                     backpointer_hex=struct.pack('<I',node).hex(),game_pointer=game,
                     notice_pointer=node+0x190+0x30998,notice_hex=anim.hex(),
                     notice_flags_pointer=0x7F44B9,notice_flags_hex='0100',
                     VM_pointer=notice.base.native.VM,VM_hex='00'*128,
                     keyboard_action_pointer=game+0x1950,keyboard_action_hex='00'*4,
                     mouse_pressed_pointer=game+0x1990,mouse_pressed_hex='00'*4)
        return dict(tasks=[dict(pointer=node,vtable=notice.battle.BATTLE,thread_id=9,
                    TLS=dict(thread_id=9,ancestry=dict(worker_argument=node,callback_this=node)),
                    scene_head_hex=head.hex(),battle_gates=gates)],scene_global=node,MAIN_event_hex='00'*8,
                    frames=[dict(tid=9,chain=[dict(return_va=x) for x in notice.ANCESTORS])])

    def test_exact_notification_predicate(self):
        self.assertTrue(notice.ready(self.row(), 'opening_notice'))
        self.assertFalse(notice.ready(self.row(), 'request'))

    def test_mutated_fields_fail_closed(self):
        mutations = [('scene_head_hex',0x30,1),('scene_head_hex',0x31,1),('scene_head_hex',0x34,1),
                     ('scene_head_hex',0x38,4),('scene_head_hex',0x43,0),('scene_head_hex',0x44,2),
                     ('scene_head_hex',0x58,1),('scene_head_hex',0x59,1),
                     ('controller_activity_hex',0,0),('controller_activity_hex',8,1),
                     ('controller_activity_hex',0x16,0),('controller_activity_hex',0x18,10),
                     ('notice_hex',0,0),('notice_hex',1,4),('notice_hex',2,1),
                     ('notice_hex',9,0),('notice_hex',13,0),('VM_hex',4,1),
                     ('notice_flags_hex',0,0),('keyboard_action_hex',1,0x80),('mouse_pressed_hex',0,1)]
        for key, offset, value in mutations:
            with self.subTest(key=key,offset=offset):
                row = self.row()
                owner = row['tasks'][0] if key == 'scene_head_hex' else row['tasks'][0]['battle_gates']
                raw = bytearray.fromhex(owner[key]); raw[offset] = value; owner[key] = raw.hex()
                self.assertFalse(notice.ready(row, 'opening_notice'))

    def test_owner_missing_memory_and_wrong_addresses_rejected(self):
        for kind in ('scene','task','tls','ancestor','missing','short','pointer','network','panel'):
            row = self.row(); task = row['tasks'][0]; gates = task['battle_gates']
            if kind == 'scene': row['scene_global'] += 4
            elif kind == 'task': row['tasks'].append(copy.deepcopy(task))
            elif kind == 'tls': task['TLS']['thread_id'] += 1
            elif kind == 'ancestor': row['frames'][0]['chain'].pop()
            elif kind == 'missing': del gates['VM_hex']
            elif kind == 'short': gates['notice_hex'] = '00'
            elif kind == 'pointer': gates['notice_pointer'] += 4
            elif kind == 'network': gates['network_hex'] = '01'
            else: gates['panel_hex'] = '01'
            self.assertFalse(notice.ready(row, 'opening_notice'), kind)

    def test_capture_is_read_only_with_expected_schema(self):
        row = self.row(); gates = row['tasks'][0]['battle_gates']; memory = {}
        for name in ('notice','notice_flags','keyboard_action','mouse_pressed','VM'):
            memory[gates[name+'_pointer']] = bytes.fromhex(gates[name+'_hex'])
        node = gates['pointer']
        memory.update({0x7A49FC:struct.pack('<I',gates['game_pointer']),0x7F4491:b'\0',
                       node+0x117F20:b'\0',node+0x190+0x108B32:bytes.fromhex(gates['controller_activity_hex']),
                       node+0x190+0x117C38:struct.pack('<I',node)})
        class Reader:
            def get(self, address, size):
                result = memory[address]
                if len(result) != size: raise AssertionError('wrong read size')
                return result
        self.assertEqual(notice.capture(Reader(), node), gates)

    def test_no_guard_after_press_and_always_release(self):
        api = Api(); api.xy = notice.TARGETS['opening_notice']
        api.geometry = lambda target:dict(screen_target=list(target),virtual_desktop=[0,0,1024,768])
        inert_cursor(api)
        def guard():
            if 2 in api.flags: raise AssertionError('must not demand obsolete post-input state')
            return {'ready': True}
        receipt = notice.guarded_click(api, guard, 'opening_notice', lambda _:None)
        self.assertIsNone(receipt['error']); self.assertEqual(api.flags, [2,4])
        self.assertTrue(receipt['released'])
        api.flags.clear()
        def fail(delay):
            if delay == .08: raise ValueError('interrupted hold')
        receipt = notice.guarded_click(api, guard, 'opening_notice', fail)
        self.assertEqual(api.flags, [2,4]); self.assertTrue(receipt['released'])

    def test_no_permission_or_foreign_stage(self):
        with self.assertRaises(PermissionError): notice.action(None, None, 'opening_notice')
        with self.assertRaises(ValueError): notice.guarded_click(Api(), lambda:None, 'request')

    def test_original_branch_and_tamper_rejection(self):
        raw = notice.base.SOURCE.read_bytes()
        self.assertFalse(notice.source_contract(raw)['accepted'])
        for mouse, key, opens in ((0,0,False),(1,0,True),(2,0,False),(0,0x8000,True),(0,1,False)):
            result = notice.branch_probe(raw, mouse_pressed=mouse, keyboard_action=key)
            self.assertEqual(result['opens_gate'], opens)
            self.assertFalse(result['native_execution'])
        changed = bytearray(raw); changed[0x499A61-0x400000] ^= 1
        with self.assertRaises(ValueError): notice.source_contract(changed)


if __name__ == '__main__': unittest.main()
