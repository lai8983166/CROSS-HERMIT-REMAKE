"""Small synthetic rejection cases; no native calls or fabricated proof files."""
import copy
from contextlib import contextmanager
import gzip
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from devtools import terminal_school_handoff_verification as v


def school_data(mode=0):
    head=bytearray(64);struct.pack_into('<I',head,0,v.GROUP);struct.pack_into('<I',head,0x24,77)
    control=bytearray(16)
    for offset,value in((0,0),(2,1),(4,1),(8,1),(10,mode)):struct.pack_into('<H',control,offset,value)
    classes=bytearray(140)
    for i in range(5):struct.pack_into('<h',classes,i*28,-1)
    struct.pack_into('<h',classes,0,101);struct.pack_into('<4h',classes,16,3,4,9,-1)
    selection=bytearray(20);struct.pack_into('<H',selection,2,1);struct.pack_into('<H',selection,14,1)
    return dict(nodes=[dict(pointer=0x120000,header_hex=head.hex(),control_pointer=0x1276BC,
        control_hex=control.hex(),selection_pointer=0x127950,selection_hex='0000')],
        ledger_count=1,ledger_pointer=0x7A5662,ledger_hex='01000103000000000100000000000000',
        fields=[dict(pointer=a,bytes=len(data),name=name,hex=data.hex())for a,name,data in(
            (0x7A528E,'date_hex',struct.pack('<HH',4,1)),(0x7A55FA,'gate_hex',b'\x01\0'),
            (0x7AAB08,'selected_hex',selection),(0x7AAA12,'classes_hex',classes),
            (0x7D6A26,'ready_hex',b'\x01'),(0x7A4E60,'school_ui_state_hex',b'\0\0'))])


def battle_data(stage=0):
    pointer=0x120000;head=bytearray(0x200)
    struct.pack_into('<I',head,0,v.BATTLE);struct.pack_into('<I',head,0x38,5);head[0x30]=stage
    activity=bytearray(0x20);activity[0]=activity[8]=1
    gates=dict(pointer=pointer,controller_pointer=pointer+0x190,panel_pointer=pointer+0x117F20,
        network_hex='00',panel_hex='00',backpointer_hex=struct.pack('<I',pointer).hex(),controller_activity_hex=activity.hex())
    return head,gates,pointer


class SchoolHandoffVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=v.menu.contract.read_source()
        cls.first_failure=v.read_report(v.ROOT/'analysis/terminal-school-handoff-v1-20261107.json.gz',
            'bcc2fb7490feb0bcae304ecc77b8c65820f710a8c9ccc1c35714844949b802cb')

    def test_independent_original_school_phase_values(self):
        for stage,mode in(('departure',0),('confirmation',14)):
            result=v.school_fields(school_data(mode),stage)
            self.assertEqual(result['ratings'],[2,0,0,0,0])
            self.assertEqual((result['pointer'],result['thread_id']),(0x120000,77))

    def test_source_tamper_rejected(self):
        changed=bytearray(self.raw);changed[0x5868B]^=1
        with self.assertRaisesRegex(ValueError,'SHA'):v.retreat_contract(bytes(changed))

    def test_original_retreat_release_and_result_instructions(self):
        result=v.retreat_contract(self.raw)
        by={r['pointer']:r for r in result}
        self.assertIn('0x19bc',by[0x45863D]['instruction'])
        self.assertIn('0x199c',by[0x45868B]['instruction'])
        self.assertIn('[ebp - 8]',by[0x453C34]['instruction'])

    def test_phase14_cannot_be_reported_as_departure(self):
        with self.assertRaisesRegex(ValueError,'phase'):v.school_fields(school_data(14),'departure')

    def test_wrong_date_and_task_rejected(self):
        for index,value in((0,'04000500'),(1,'0000'),(4,'00')):
            data=school_data();data['fields'][index]['hex']=value
            with self.assertRaises(ValueError):v.school_fields(data,'departure')
        data=school_data();raw=bytearray.fromhex(data['fields'][2]['hex']);struct.pack_into('<H',raw,14,5)
        data['fields'][2]['hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'task1'):v.school_fields(data,'departure')

    def test_same_data_from_wrong_pointer_rejected(self):
        data=school_data();data['fields'][0]['pointer']+=4
        with self.assertRaisesRegex(ValueError,'location'):v.school_fields(data,'departure')

    def test_missing_class_member_rejected(self):
        data=school_data();raw=bytearray.fromhex(data['fields'][3]['hex']);struct.pack_into('<h',raw,18,-1)
        data['fields'][3]['hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'class'):v.school_fields(data,'departure')

    def test_additional_teacher_rejected(self):
        data=school_data();raw=bytearray.fromhex(data['fields'][3]['hex']);struct.pack_into('<h',raw,28,102)
        data['fields'][3]['hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'class'):v.school_fields(data,'departure')

    def test_ledger_count_bool_and_disabled_row_rejected(self):
        data=school_data();data['ledger_count']=True
        with self.assertRaisesRegex(ValueError,'ledger'):v.school_fields(data,'departure')
        data=school_data();raw=bytearray.fromhex(data['ledger_hex']);raw[6]=1;data['ledger_hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'task1'):v.school_fields(data,'departure')

    def test_invented_node_field_pointer_rejected(self):
        data=school_data();data['nodes'][0]['control_pointer']+=2
        with self.assertRaisesRegex(ValueError,'locations'):v.school_fields(data,'departure')

    def test_current_battle_gates(self):
        for stage,value in(('retreat_request',0),('retreat_confirmation',1)):
            h,g,p=battle_data(value);v.battle_fields(h,g,p,stage)

    def test_script_active_or_wrong_loop_mode_rejected(self):
        for modify in(lambda h:h.__setitem__(0x43,1)or h.__setitem__(0x59,1),
                      lambda h:struct.pack_into('<I',h,0x38,4)):
            h,g,p=battle_data();modify(h)
            with self.assertRaisesRegex(ValueError,'gates'):v.battle_fields(h,g,p,'retreat_request')

    def test_network_panel_and_callback_ownership_rejected(self):
        for field,value in(('network_hex','01'),('panel_hex','01'),('backpointer_hex','00001201')):
            h,g,p=battle_data();g[field]=value
            with self.assertRaisesRegex(ValueError,'gates'):v.battle_fields(h,g,p,'retreat_request')

    def test_controller_field_alias_rejected(self):
        h,g,p=battle_data();g['controller_pointer']+=4
        with self.assertRaisesRegex(ValueError,'addresses'):v.battle_fields(h,g,p,'retreat_request')

    def test_complete_range_identity_has_school_and_retreat(self):
        rows=v.source_rows(self.raw)
        self.assertEqual(len(rows),len({(r['pointer'],r['bytes'])for r in rows}))
        for begin,end in((0x4A1570,0x4A1750),(0x4A6F90,0x4A7C40),(0x453D00,0x453E04)):
            self.assertIn(dict(pointer=begin,bytes=end-begin,sha256=v.owner.sha(self.raw[begin-0x400000:end-0x400000])),rows)

    def test_fixed_report_sha_rejects_mismatch(self):
        with tempfile.TemporaryDirectory()as directory:
            path=Path(directory)/'source.json.gz';packed=gzip.compress(b'{"value":1}',mtime=0);path.write_bytes(packed)
            self.assertEqual(v.read_report(path,v.owner.sha(packed)),dict(value=1))
            with self.assertRaisesRegex(ValueError,'SHA'):v.read_report(path,'0'*64)

    def test_changed_implementation_layer_rejected(self):
        report=dict(parent_implementations=v.identities(v.PARENT_IMPLEMENTATIONS),
            implementation_layers=v.identities(v.LAYER_IMPLEMENTATIONS),observer=v.identities(v.PARENT_IMPLEMENTATIONS)[2])
        report['implementation_layers'][3]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'layers'):v.verify_implementations(report)

    def test_frozen_parent_collector_change_rejected(self):
        report=dict(parent_implementations=v.identities(v.PARENT_IMPLEMENTATIONS),
            implementation_layers=v.identities(v.LAYER_IMPLEMENTATIONS),observer=v.identities(v.PARENT_IMPLEMENTATIONS)[2])
        report['parent_implementations'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'parent'):v.verify_implementations(report)

    def test_all_current_implementation_and_authorization_identities(self):
        parents=v.identities(v.PARENT_IMPLEMENTATIONS)
        result=v.verify_implementations(dict(parent_implementations=parents,
            implementation_layers=v.identities(v.LAYER_IMPLEMENTATIONS),observer=parents[2]))
        self.assertEqual(len(result['parent']),12);self.assertEqual(len(result['layers']),14)

    def test_actual_first_failure_is_rejected_not_accepted(self):
        report=self.first_failure
        self.assertEqual(report['probe']['source_before']['code'],v.source_rows(self.raw))
        action=report['probe']['collector_input_actions'][0]['action']
        self.assertFalse(action['down_submitted'])
        self.assertEqual(len(action['moves']),4)
        with self.assertRaisesRegex(ValueError,'failed acquisition'):v.verify_report(report,self.raw,{})

    def test_real_failed_acquisition_still_has_bounded_valid_owner_snapshots(self):
        p=self.first_failure['probe'];game=self.first_failure['lifecycle']['ready']['game']['pointer']
        workers={(w['pointer'],w['thread_id']):w for w in p['workers']}
        count=sum(v.verify_task_row(row,p,self.raw,game,workers)for row in p['samples'])
        self.assertGreater(count,0)

    def test_real_snapshot_truncated_PTD_rejected(self):
        p=self.first_failure['probe'];game=self.first_failure['lifecycle']['ready']['game']['pointer']
        workers={(w['pointer'],w['thread_id']):w for w in p['workers']}
        row=copy.deepcopy(next(r for r in p['samples']if any('TLS'in t for t in r['tasks'])))
        next(t for t in row['tasks']if 'TLS'in t)['TLS']['PTD_hex']='00'*115
        with self.assertRaisesRegex(ValueError,'PTD'):v.verify_task_row(row,p,self.raw,game,workers)

    def test_real_snapshot_graph_event_owner_tamper_rejected(self):
        p=self.first_failure['probe'];game=self.first_failure['lifecycle']['ready']['game']['pointer']
        workers={(w['pointer'],w['thread_id']):w for w in p['workers']}
        row=copy.deepcopy(p['samples'][-1]);manager=bytearray.fromhex(row['manager_hex'])
        struct.pack_into('<I',manager,0x118,1);row['manager_hex']=manager.hex()
        with self.assertRaisesRegex(ValueError,'manager event'):v.verify_task_row(row,p,self.raw,game,workers)

    def feedback_action(self):
        geometry=dict(screen_target=[318,508],virtual_desktop=[-3840,0,4864,1440],
            window_rect=[0,0,1024,768],point_window=77,coordinate_mode=0)
        def samples(point,start):
            return [dict(screen_point=list(point),os_game_point=list(point),game_point=list(point),
                geometry=copy.deepcopy(geometry),wall_time_ns=start+i*25_000_000,
                monotonic_ns=start+i*25_000_000)for i in range(3)]
        return dict(movement_mode='absolute_virtual_desktop_feedback',click_geometry=geometry,
            before_click_settling=samples([318,508],1_200_000_000),
            pre_down_cursor=samples([318,508],1_260_000_000)[0],down_wall_time_ns=1_270_000_000,moves=[
            dict(before=[520,376],geometry=geometry,flags=0xC001,submitted=1,normalized=[56034,23135],
                 settling=samples([318,507],1_000_000_000)),
            dict(before=[318,507],geometry=geometry,flags=0xC001,submitted=1,normalized=[56034,23181],
                 settling=samples([318,508],1_100_000_000),
                 feedback_correction=dict(error=[0,1],previous_normalized=[56034,23135],delta=[0,46]))])

    def test_exact_multi_monitor_one_pixel_feedback(self):
        corrections,canonical=v.verify_absolute_moves(self.feedback_action(),(318,508),77,0)
        self.assertEqual(canonical,[[56034,23135],[56034,23135]])
        self.assertEqual(corrections[0]['normalized'],[56034,23181])

    def test_feedback_modified_delta_rejected(self):
        action=self.feedback_action();action['moves'][1]['feedback_correction']['delta'][1]=47
        with self.assertRaisesRegex(ValueError,'correction'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_feedback_large_error_rejected(self):
        action=self.feedback_action();action['moves'][1]['before']=[318,503]
        with self.assertRaisesRegex(ValueError,'previously settled'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_feedback_geometry_change_rejected(self):
        action=self.feedback_action();action['moves'][1]['geometry']=copy.deepcopy(action['moves'][0]['geometry'])
        action['moves'][1]['geometry']['window_rect']=[0,0,1024,769]
        with self.assertRaisesRegex(ValueError,'unqualified'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_feedback_real_normalized_coordinate_tamper_rejected(self):
        action=self.feedback_action();action['moves'][1]['normalized'][0]+=1
        with self.assertRaisesRegex(ValueError,'submitted normalized'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_integer_negative_and_tie_rounding(self):
        self.assertEqual([v.nearest_even(n,2)for n in(-5,-3,-1,1,3,5)],[-2,-2,0,0,2,2])

    def test_settling_os_and_game_disagree_rejected(self):
        action=self.feedback_action();action['before_click_settling'][-1]['game_point']=[318,507]
        with self.assertRaisesRegex(ValueError,'continuously'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_settling_too_short_rejected(self):
        action=self.feedback_action();action['before_click_settling'].pop()
        with self.assertRaisesRegex(ValueError,'complete OS/game'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_settling_deadline_rejected(self):
        action=self.feedback_action()
        for s in action['before_click_settling'][1:]:
            s['monotonic_ns']+=300_000_000;s['wall_time_ns']+=300_000_000
        with self.assertRaisesRegex(ValueError,'300 millisecond'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_final_settled_point_must_be_target(self):
        action=self.feedback_action()
        for s in action['before_click_settling']:
            for key in ('screen_point','os_game_point','game_point'):s[key]=[318,507]
        with self.assertRaisesRegex(ValueError,'exact OS/game target'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_pre_down_cursor_movement_rejected(self):
        action=self.feedback_action();action['pre_down_cursor']['game_point']=[318,509]
        with self.assertRaisesRegex(ValueError,'recheck'):v.verify_absolute_moves(action,(318,508),77,0)

    def test_settling_screen_client_transform_rejected(self):
        action=self.feedback_action();action['before_click_settling'][0]['screen_point']=[319,508]
        with self.assertRaisesRegex(ValueError,'transformation'):v.verify_absolute_moves(action,(318,508),77,0)

    def qualification(self):
        from devtools.tests.test_isolated_vm_preflight import fixture
        from devtools.isolated_vm_preflight import verify
        source=fixture();raw=json.dumps(source).encode('utf8')
        return dict(path='C:/ChaomofaWorker/isolation-qualified.json',bytes=len(raw),sha256=v.owner.sha(raw),
            source_utf8=raw.decode('utf8'),current_guest_uuid=source['guest']['machine']['uuid'],
            current_guest_boot_utc=source['guest']['machine']['boot_utc'],
            current_guest_resources={k:source['guest']['machine'][k]for k in ('logical_processors','memory_bytes')},
            verification=verify(source))

    def focus(self,attached=False):
        isolation=v.verify_input_isolation(self.qualification())
        receipt=dict(hwnd=77,before=88,after=77,operations=[dict(name='SetForegroundWindow',result=True)],
            guest_only=True,current_tid=123,console_session=isolation['console_session'],
            guest_uuid=isolation['current_guest_uuid'],guest_boot_utc=isolation['current_guest_boot_utc'],
            own_pid=111,own_session=isolation['console_session'],target_pid=222,
            target_session=isolation['console_session'],foreground_wait_seconds=.01)
        if attached:
            receipt['operations'][0]['result']=False
            receipt['operations'] += [dict(name=n,result=True)for n in
                ('AttachThreadInput','SetForegroundWindow','DetachThreadInput')]
            receipt.update(attached_foreground=88,attached_tid=333,attached_pid=444,
                           attached_session=isolation['console_session'])
        return receipt,isolation

    def test_guest_focus_direct_and_already_foreground(self):
        a,q=self.focus();self.assertEqual(v.verify_guest_focus(a,q,222,77)['path'],'direct')
        a['before']=77;a['operations']=[]
        self.assertEqual(v.verify_guest_focus(a,q,222,77)['path'],'direct')

    def test_guest_focus_attach_success_and_async_ack(self):
        a,q=self.focus(True);a['operations'][-2]['result']=False
        result=v.verify_guest_focus(a,q,222,77)
        self.assertEqual(result['path'],'attached');self.assertEqual(result['receipt'],a)
        a['before']=77;a['operations']=a['operations'][1:]
        self.assertEqual(v.verify_guest_focus(a,q,222,77)['path'],'attached')

    def test_guest_focus_failed_detach_and_missing_participants_rejected(self):
        a,q=self.focus(True);a['operations'][-1]['result']=False
        with self.assertRaisesRegex(ValueError,'detachment'):v.verify_guest_focus(a,q,222,77)
        a,q=self.focus(True);del a['attached_tid']
        with self.assertRaisesRegex(ValueError,'participant'):v.verify_guest_focus(a,q,222,77)

    def test_guest_focus_wrong_sessions_rejected(self):
        for field in ('console_session','own_session','target_session','attached_session'):
            a,q=self.focus(True);a[field]+=1
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'session'):
                v.verify_guest_focus(a,q,222,77)

    def test_guest_focus_wrong_uuid_boot_and_owner_rejected(self):
        for key,value in (('guest_uuid','wrong'),('guest_boot_utc','2026-01-01T00:00:00Z'),
                          ('target_pid',333),('after',88),('own_pid',222)):
            a,q=self.focus();a[key]=value
            with self.subTest(field=key),self.assertRaises(ValueError):v.verify_guest_focus(a,q,222,77)

    def test_guest_focus_illegal_operation_order_and_result_rejected(self):
        for change in ('name','reorder','bool','extra','unreported_attach'):
            a,q=self.focus(True)
            if change=='name':a['operations'][0]['name']='SendInput'
            elif change=='reorder':a['operations'][-2:]=list(reversed(a['operations'][-2:]))
            elif change=='bool':a['operations'][1]['result']=1
            elif change=='extra':a['operations'].append(dict(name='SetForegroundWindow',result=True))
            else:a['operations']=a['operations'][:1]
            with self.subTest(change=change),self.assertRaises(ValueError):v.verify_guest_focus(a,q,222,77)

    def test_guest_focus_old_receipt_not_promoted(self):
        a,q=self.focus();a={k:a[k]for k in ('hwnd','before','after','operations')}
        with self.assertRaisesRegex(ValueError,'complete'):v.verify_guest_focus(a,q,222,77)

    def test_guest_focus_wait_and_same_thread_rejected(self):
        a,q=self.focus(True);a['attached_tid']=a['current_tid']
        with self.assertRaisesRegex(ValueError,'distinct'):v.verify_guest_focus(a,q,222,77)
        for wait in (-.01,.351,float('nan')):
            a,q=self.focus();a['foreground_wait_seconds']=wait
            with self.assertRaises(ValueError):v.verify_guest_focus(a,q,222,77)

    def test_guest_focus_private_views_cover_all_callers_without_raw_mutation(self):
        a,q=self.focus(True);action=dict(activation=a,raw_input_samples=[{'hex':'0123'}])
        p=dict(mouse_controller=dict(receipt=action),collector_input_actions=[copy.deepcopy(action)],
               story_phases=[dict(actions=[action])],workroom_inputs=[action],school_inputs=[action],battle_inputs=[action])
        report=dict(probe=p,startup_activation=[dict(a,elapsed=1)])
        before=copy.deepcopy(report);view,observations=v.guest_focus_view(report,q,222,77)
        self.assertEqual(report,before);self.assertEqual(len(observations),6)
        self.assertEqual(view['probe']['collector_input_actions'][0]['activation']['operations'],[])
        self.assertIs(view['probe']['story_phases'][0]['actions'][0]['raw_input_samples'],action['raw_input_samples'])
        self.assertEqual(observations[0]['receipt']['operations'],a['operations'])

    def test_guest_focus_mismatching_title_alias_rejected_before_adaptation(self):
        a,q=self.focus();report=dict(probe=dict(mouse_controller=dict(receipt=dict(activation=a)),collector_input_actions=[]))
        with self.assertRaisesRegex(ValueError,'aliases'):v.guest_focus_view(report,q,222,77)

    def test_qualification_boot_and_resource_reuse_rejected(self):
        for key,value in (('current_guest_boot_utc','2026-01-01T00:00:00Z'),
                          ('current_guest_resources',dict(logical_processors=4,memory_bytes=4294430720))):
            receipt=self.qualification();receipt[key]=value
            with self.subTest(field=key),self.assertRaises(ValueError):v.verify_input_isolation(receipt)

    @contextmanager
    def module_fixture(self):
        # A real local PE is only fixture bytes; no DLL is loaded or executed.
        data=Path('C:/Windows/SysWOW64/kernelbase.dll').read_bytes()
        receipt=self.qualification();isolation=v.verify_input_isolation(receipt)
        with tempfile.TemporaryDirectory()as directory:
            root=Path(directory);owned=root/'.venv-audit/native-worker'
            local=owned/'guest-system-dlls/KERNELBASE.dll';local.parent.mkdir(parents=True);local.write_bytes(data)
            row=dict(module_path='C:/Windows/SysWOW64/KERNELBASE.dll',module_sha256=v.owner.sha(data),
                     local_path=str(local),bytes=len(data))
            report=dict(input_isolation=receipt,TLS=dict(module_path=row['module_path'],module_sha256=row['module_sha256']))
            manifest=owned/'modules.json';digest='a'*64
            doc=dict(schema_version=1,kind='isolated_guest_system_module_sources',
                     guest_uuid=isolation['current_guest_uuid'],guest_boot_utc=isolation['current_guest_boot_utc'],
                     source_report_sha256=digest,modules=[row])
            def write():manifest.write_text(json.dumps(doc),encoding='utf8')
            write()
            with patch.object(v,'ROOT',root),patch.object(v,'verify_input_isolation',return_value=isolation):
                yield manifest,doc,report,digest,write

    def test_guest_module_actual_pe_exports_and_scoped_loader_restored(self):
        with self.module_fixture()as(path,doc,report,digest,write):
            sources=v.GuestModuleSources(path,report,digest);row=doc['modules'][0];previous=v.menu._module
            with sources.scope():
                pe=v.menu._module(row['module_path'],row['module_sha256'])
                export=next(e for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name==b'TlsGetValue')
                v.menu.verify_export(dict(module='kernelbase.dll',symbol='TlsGetValue',base=0x70000000,
                    target=0x70000000+export.address,RVA=export.address,module_path=row['module_path'],
                    module_sha256=row['module_sha256']),'kernelbase.dll','TlsGetValue')
            self.assertIs(v.menu._module,previous)
            with self.assertRaisesRegex(RuntimeError,'test failure'):
                with sources.scope():raise RuntimeError('test failure')
            self.assertIs(v.menu._module,previous)

    def test_guest_module_missing_duplicate_and_extra_mapping_rejected(self):
        for kind in ('missing','duplicate','extra'):
            with self.module_fixture()as(path,doc,report,digest,write):
                if kind=='missing':doc['modules']=[]
                elif kind=='duplicate':doc['modules'].append(dict(doc['modules'][0]))
                else:report['additional']=dict(module_path='C:/Windows/SysWOW64/USER32.dll',module_sha256='b'*64)
                write()
                with self.subTest(kind=kind),self.assertRaises(ValueError):v.GuestModuleSources(path,report,digest)

    def test_guest_module_sha_and_size_tamper_rejected(self):
        for kind in ('sha','size','bytes'):
            with self.module_fixture()as(path,doc,report,digest,write):
                row=doc['modules'][0]
                if kind=='sha':row['module_sha256']='b'*64
                elif kind=='size':row['bytes']+=1
                else:
                    local=Path(row['local_path']);data=bytearray(local.read_bytes());data[-1]^=1;local.write_bytes(data)
                write()
                with self.subTest(kind=kind),self.assertRaises(ValueError):v.GuestModuleSources(path,report,digest)

    def test_guest_module_cross_path_and_guest_binding_rejected(self):
        for key,value in (('source_report_sha256','b'*64),('guest_uuid','bad'),('guest_boot_utc','2026-01-01T00:00:00Z')):
            with self.module_fixture()as(path,doc,report,digest,write):
                doc[key]=value;write()
                with self.subTest(key=key),self.assertRaisesRegex(ValueError,'bound'):v.GuestModuleSources(path,report,digest)
        for original in ('C:/Windows/System32/KERNELBASE.dll','C:/Windows/SysWOW64/../KERNELBASE.dll',
                         'D:/Windows/SysWOW64/KERNELBASE.dll','C:/Windows/SysWOW64/KERNELBASE.dll:stream'):
            with self.assertRaises(ValueError):v.guest_module_key(original,'a'*64)

    def test_guest_module_outside_owned_copy_directory_rejected(self):
        with self.module_fixture()as(path,doc,report,digest,write):
            row=doc['modules'][0];original=Path(row['local_path']);outside=original.parent.parent/'KERNELBASE.dll'
            outside.write_bytes(original.read_bytes());row['local_path']=str(outside);write()
            with self.assertRaisesRegex(ValueError,'confined'):v.GuestModuleSources(path,report,digest)

    def test_guest_module_invalid_pe_and_machine_rejected(self):
        import pefile
        for kind in ('magic','machine'):
            with self.module_fixture()as(path,doc,report,digest,write):
                row=doc['modules'][0];local=Path(row['local_path']);data=bytearray(local.read_bytes());header=struct.unpack_from('<I',data,0x3c)[0]
                struct.pack_into('<H',data,header+(24 if kind=='magic'else 4),0x20b if kind=='magic'else 0x8664)
                local.write_bytes(data);row['module_sha256']=v.owner.sha(data);report['TLS']['module_sha256']=row['module_sha256'];write()
                with self.subTest(kind=kind),self.assertRaises((ValueError,pefile.PEFormatError)):v.GuestModuleSources(path,report,digest)

    def test_guest_module_unknown_lookup_never_uses_host_cache(self):
        with self.module_fixture()as(path,doc,report,digest,write):
            sources=v.GuestModuleSources(path,report,digest)
            with sources.scope(),self.assertRaisesRegex(ValueError,'exact manifest'):
                v.menu._module('C:/Windows/SysWOW64/USER32.dll','b'*64)

    def test_guest_runtime_exact_relative_layout(self):
        path='C:/ChaomofaWorker/project/'+v.owner.APP
        report=dict(probe=dict(startup=dict(process_image=path)))
        self.assertEqual(v.guest_runtime_location(report)['private_relative_executable'],v.owner.APP)
        for bad in (path.replace('project/','other/'),path.replace('C:/','D:/'),
                    path.replace('/scene-callback-runtime/','/scene-callback-runtime/../other/'),path+'.other'):
            report['probe']['startup']['process_image']=bad
            with self.subTest(path=bad),self.assertRaisesRegex(ValueError,'layout'):v.guest_runtime_location(report)

    def test_exact_embedded_guest_qualification(self):
        receipt=self.qualification();result=v.verify_input_isolation(receipt)
        self.assertEqual(result['sha256'],receipt['sha256'])
        self.assertIs(result['original_game_compatible'],False)

    def test_qualification_raw_tamper_rejected(self):
        receipt=self.qualification();receipt['source_utf8']+=' '
        with self.assertRaisesRegex(ValueError,'source bytes'):v.verify_input_isolation(receipt)

    def test_qualification_other_guest_rejected(self):
        receipt=self.qualification();receipt['current_guest_uuid']='12345678-1234-1234-1234-123456789abc'
        with self.assertRaisesRegex(ValueError,'current guest'):v.verify_input_isolation(receipt)

    def test_qualification_success_boolean_not_proof(self):
        receipt=self.qualification();receipt['verification']['original_game_compatible']=True
        with self.assertRaisesRegex(ValueError,'independently recomputed'):v.verify_input_isolation(receipt)

    def terminal_row(self):
        pointer=0x120000;tid=77;head=bytearray(0x200);struct.pack_into('<I',head,0,v.BATTLE);head[0x31]=1
        frames=[];memory=[]
        for i,(address,result_offset,result)in enumerate(((0x451ABC,0x78,1),(0x451716,0x78,0xCCCCCCCC),(0x421F8A,0x74,0))):
            bp=0x31008000+i*0x100;f=dict(bp=bp,saved_bp=bp+0x100,return_va=address);frames.append(f)
            raw=bytearray(b'\xCC'*0x90);struct.pack_into('<I',raw,0x7C,pointer)
            struct.pack_into('<II',raw,0x80,f['saved_bp'],address);struct.pack_into('<I',raw,result_offset,result)
            memory.append(dict(pointer=bp-0x80,return_va=address,hex=raw.hex()))
        frames.insert(0,dict(bp=0x31007F00,saved_bp=0x31008000,return_va=0x453CD3))
        return dict(elapsed=20,frames=[dict(tid=tid,chain=frames)],tasks=[dict(pointer=pointer,thread_id=tid,
            vtable=v.BATTLE,header_hex=head[:64].hex(),scene_head_hex=head.hex(),controller_task_backpointer=pointer,
            terminal_frames=memory,TLS={})])

    def test_original_inner_dispatcher_callback_results_not_conflated(self):
        result=v.verify_terminal_rows([self.terminal_row()],{},{} )
        self.assertEqual(result[0]['original_result_locals'],dict(inner_result=1,dispatcher_result=0xCCCCCCCC,callback_result=0))
        self.assertIn(0x453CD3,result[0]['return_sites'])

    def test_wrong_terminal_frame_return_address_rejected(self):
        row=self.terminal_row();row['tasks'][0]['terminal_frames'][0]['return_va']=0x451716
        with self.assertRaisesRegex(ValueError,'terminal locals'):v.verify_terminal_rows([row],{},{} )

    def test_terminal_result_from_other_object_rejected(self):
        row=self.terminal_row();raw=bytearray.fromhex(row['tasks'][0]['terminal_frames'][0]['hex'])
        struct.pack_into('<I',raw,0x7C,0x130000);row['tasks'][0]['terminal_frames'][0]['hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'terminal locals'):v.verify_terminal_rows([row],{},{} )


if __name__=='__main__':unittest.main()
