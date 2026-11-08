from devtools.tests.test_terminal_owned_mouse import inert_cursor
import copy
import struct
import unittest

from devtools import terminal_school_input as school


def sample(stage='departure'):
    node=0x120000;tid=55
    h=bytearray(64);struct.pack_into('<I',h,0,school.GROUP);struct.pack_into('<I',h,0x24,tid)
    control=bytearray(16)
    for offset,value in ((0,0),(2,1),(4,1),(8,1),(10,school.MODES[stage])):struct.pack_into('<H',control,offset,value)
    classes=bytearray(140)
    for i in range(5):struct.pack_into('<h',classes,i*28,-1)
    struct.pack_into('<h',classes,0,101);struct.pack_into('<4h',classes,16,3,4,9,-1)
    selection=bytearray(20);struct.pack_into('<H',selection,2,1);struct.pack_into('<H',selection,14,1)
    fields=[dict(pointer=a,bytes=len(v),name=n,hex=v.hex())for a,n,v in (
        (0x7A528E,'date_hex',struct.pack('<HH',4,1)),(0x7A55FA,'gate_hex',b'\x01\0'),
        (0x7AAB08,'selected_hex',selection),(0x7AAA12,'classes_hex',classes),
        (0x7D6A26,'ready_hex',b'\x01'),(0x7A4E60,'school_ui_state_hex',b'\0\0'))]
    data=dict(nodes=[dict(pointer=node,header_hex=h.hex(),control_pointer=node+0x76BC,
        control_hex=control.hex(),selection_pointer=node+0x7950,selection_hex='0000')],
        ledger_count=1,ledger_pointer=0x7A5662,ledger_hex='01000103000000000100000000000000',fields=fields)
    return dict(school=data,MAIN_event_hex='00'*8,tasks=[dict(pointer=node,thread_id=tid,vtable=school.GROUP,TLS={}),
        dict(pointer=node+0x10000,thread_id=56,vtable=school.UI,TLS={})],
        frames=[dict(tid=tid,chain=[dict(return_va=a)for a in(0x4A7CEA,0x4AB7F1,0x421F8A,0x56E183)])])


class Api:
    def __init__(self,target):self.xy=target;self.flags=[];self.covered=False
    def geometry(self,target):
        if self.covered:raise ValueError('covered')
        return dict(screen_target=list(target),virtual_desktop=[0,0,1024,768])
    def position(self):return self.xy
    def left_button_down(self):return False
    def submit(self,value):self.flags.append(value.data.mi.dwFlags);return 1
    def final_guard(self):pass


class SchoolInputTests(unittest.TestCase):
    def test_explicit_authorization_default_off(self):
        with self.assertRaises(PermissionError):school.action(None,None,'departure')

    def test_two_original_ready_modes(self):
        for stage in school.MODES:
            self.assertTrue(school.ready(sample(stage),stage))
            other='confirmation' if stage=='departure' else 'departure'
            self.assertFalse(school.ready(sample(stage),other))

    def test_wrong_task_date_readiness_rejected(self):
        row=sample()
        for index,hexvalue in ((0,'04000500'),(1,'0000'),(4,'00')):
            changed=copy.deepcopy(row);changed['school']['fields'][index]['hex']=hexvalue
            self.assertFalse(school.ready(changed,'departure'))

    def test_same_bytes_wrong_original_field_address_rejected(self):
        row=sample();row['school']['fields'][0]['pointer']+=4
        self.assertFalse(school.ready(row,'departure'))

    def test_teacher_alone_or_additional_class_rejected(self):
        row=sample()
        for offset,value in ((16,-1),(28,102)):
            changed=copy.deepcopy(row);data=bytearray.fromhex(changed['school']['fields'][3]['hex'])
            struct.pack_into('<h',data,offset,value);changed['school']['fields'][3]['hex']=data.hex()
            self.assertFalse(school.ready(changed,'departure'))

    def test_actual_task_and_worker_binding(self):
        row=sample();row['tasks'][0]['thread_id']=99
        self.assertFalse(school.ready(row,'departure'))
        row=sample();row['frames'][0]['chain'].pop()
        self.assertFalse(school.ready(row,'departure'))

    def test_unrelated_owner_pending_event_and_missing_tls_rejected(self):
        for mutation in (lambda r:r['tasks'].append(dict(vtable=0x59B060)),
                         lambda r:r.update(MAIN_event_hex='0100000000000000'),
                         lambda r:r['tasks'][0].pop('TLS')):
            row=sample();mutation(row);self.assertFalse(school.ready(row,'departure'))

    def test_unknown_stage_no_input(self):
        api=Api((1,2))
        with self.assertRaises(ValueError):school.guarded_click(inert_cursor(api),lambda:None,'other',lambda _:None)
        self.assertEqual(api.flags,[])

    def test_two_targets_and_actual_release_receipt(self):
        for stage,target in school.TARGETS.items():
            api=Api(target);result=school.guarded_click(inert_cursor(api),lambda:None,stage,lambda _:None)
            self.assertEqual(result['target'],list(target));self.assertEqual(api.flags,[2,4])
            self.assertTrue(result['released']);self.assertFalse(result['transition_proved'])
            self.assertFalse(result['game_memory_written'])

    def test_geometry_and_original_guard_before_any_down(self):
        api=Api(school.TARGETS['departure']);api.covered=True
        result=school.guarded_click(inert_cursor(api),lambda:None,'departure',lambda _:None)
        self.assertFalse(result['down_submitted']);self.assertEqual(api.flags,[])

    def test_interruption_after_down_releases(self):
        api=Api(school.TARGETS['confirmation'])
        def fail(delay):
            if delay==.08:raise ValueError('stop')
        result=school.guarded_click(inert_cursor(api),lambda:None,'confirmation',fail)
        self.assertEqual(api.flags,[2,4]);self.assertTrue(result['released']);self.assertIsNotNone(result['error'])


if __name__=='__main__':unittest.main()
