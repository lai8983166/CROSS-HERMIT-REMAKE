"""Small recorded no-input source plus explicitly synthetic mouse receipts.

No native calls or actual input. Synthetic receipts test rejection contracts;
they are never written as native evidence or a successful handoff proof.
"""
import copy
import struct
import unittest
from unittest import mock

from devtools import terminal_menu_handoff_verification as v


class MenuVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=v.owner.read_report(v.ROOT/'analysis/terminal-menu-handoff-v1-20261107.json.gz',v.V1_SOURCE_SHA)
        cls.raw=v.contract.read_source()

    def reject(self,change,part=None):
        r=copy.deepcopy(self.report);change(r)
        with self.assertRaises(ValueError) as caught:v.verify_report(r,self.raw)
        if part:self.assertIn(part,str(caught.exception))

    def test_actual_v1_is_only_no_input_partial_observation(self):
        result=v.verify_report(self.report,self.raw)
        self.assertEqual((result['samples'],result['TLS_samples']),(46,46))
        self.assertFalse(result['native_menu_handoff_observed'])
        self.assertFalse(result['input']['attempted'])
        for name in ('accepted','full_battle_exit_accepted','wait_return_proved',
                     'result_consumption_proved','full_resource_lifetime_proved',
                     'formal_terminal_boundary_advanced','WinMain_normal_return_proved'):
            self.assertIs(result[name],False)

    def test_explicit_v1_source_archive(self):
        result=v.verify_file(v.ROOT/'analysis/terminal-menu-handoff-v1-20261107.json.gz',v.V1_SOURCE_SHA,True)
        self.assertEqual(result['implementation_archive_used'],v.V1_ARCHIVE)
        self.assertFalse(result['native_menu_handoff_observed'])

    def test_actual_v5_archive_replays_inputs_without_inventing_missing_owners(self):
        result=v.verify_file(v.ROOT/'analysis/terminal-menu-handoff-v5-20261107.json.gz',v.V5_SOURCE_SHA,
                             allow_v5_archive=True)
        self.assertEqual((result['samples'],result['TLS_samples']),(343,343))
        self.assertTrue(result['input']['input_edges_observed'])
        self.assertEqual(len(result['story_confirmations']),96)
        self.assertEqual(sum(x['original_key_query_replays'] for x in result['story_confirmations']),1198)
        self.assertFalse(result['native_menu_handoff_observed'])
        self.assertFalse(result['menu_ready_one_second_independently_sampled'])
        self.assertTrue(any(s['vtable']==v.ADV and s['TLS_verified'] for s in result['successor_observations']))
        self.assertFalse(any(s['vtable']==v.NEW_GAME for s in result['successor_observations']))

    def test_v5_archive_requires_exact_member_identity(self):
        with mock.patch.object(v,'V5_ARCHIVE_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'archive'):v.archived_v5_sources()

    def test_actual_v6_adv_retirement_and_workroom_remain_partial(self):
        result=v.verify_file(v.ROOT/'analysis/terminal-menu-handoff-v6-20261107.json.gz',
            'af9e1d76f665ab06e913288b3e487f25d4777cd27acd98e6828bb1d991de7533')
        self.assertEqual((result['samples'],result['TLS_samples']),(638,637))
        self.assertEqual(len(result['story_confirmations']),178)
        self.assertEqual(sum(x['original_key_query_replays'] for x in result['story_confirmations']),2219)
        self.assertTrue(result['menu_ready_one_second_independently_sampled'])
        self.assertTrue(result['ADV_exit0_and_workroom_observed'])
        self.assertGreaterEqual(result['workroom_stable_observed_seconds'],10)
        self.assertFalse(result['workroom_callback_code_live_authenticated'])
        self.assertFalse(result['native_menu_handoff_observed'])
        self.assertFalse(result['collector_workroom_input_executed'])
        self.assertFalse(result['full_battle_exit_accepted'])

    def test_old_collector_cannot_pass_current_identity(self):
        with self.assertRaisesRegex(ValueError,'implementation set'):
            v.verify_file(v.ROOT/'analysis/terminal-menu-handoff-v1-20261107.json.gz',v.V1_SOURCE_SHA)

    def test_full_acceptance_upgrade_rejected(self):
        self.reject(lambda r:r.update(full_battle_exit_accepted=True),'scope')

    def test_missing_original_range_rejected(self):
        def change(r):
            r['probe']['source_before']['code'].pop();r['probe']['source_after']=copy.deepcopy(r['probe']['source_before'])
        self.reject(change,'ranges')

    def test_wrong_worker_event_owner_rejected(self):
        self.reject(lambda r:r['probe']['workers'][0]['event'].update(owner_pid=1),'node event')

    def test_abnormal_menu_exit_rejected(self):
        self.reject(lambda r:r['probe']['workers'][0].update(exit=dict(code=0xC0000005,wait_status=0,
            elapsed=324,before_WM_CLOSE=True)),'normal worker exit')

    def test_exit_after_cleanup_rejected(self):
        self.reject(lambda r:r['probe']['workers'][0].update(exit=dict(code=0,wait_status=0,
            elapsed=324,before_WM_CLOSE=False)),'normal worker exit')

    def test_full_context_truncation_rejected(self):
        self.reject(lambda r:r['probe']['samples'][0]['frames'][0].update(context_hex='00'),'WOW64_CONTEXT')

    def test_raw_vtable_tamper_rejected(self):
        self.reject(lambda r:r['probe']['samples'][0]['tasks'][0].update(vtable_hex='00'*8),'vtable')

    def test_cycle_rejected(self):
        def change(r):
            row=r['probe']['samples'][0]['registered_tasks'][0];b=bytearray.fromhex(row['head_hex'])
            struct.pack_into('<I',b,12,row['pointer']);row['head_hex']=b.hex()
        self.reject(change,'acyclic')

    def test_ptd_worker_owner_tamper(self):
        def change(r):
            task=r['probe']['samples'][0]['tasks'][0];b=bytearray.fromhex(task['TLS']['PTD_hex'])
            struct.pack_into('<I',b,0x4C,1);task['TLS']['PTD_hex']=b.hex()
        self.reject(change,'PTD worker')

    def test_host_calls_and_writes_rejected(self):
        for field in ('host_game_calls','host_memory_writes'):
            self.reject(lambda r:r['probe'][field].append({'fake':True}),'no host game')

    def test_hidden_input_rejected(self):
        self.reject(lambda r:r['probe']['collector_input_actions'].append({'fake':True}),'hidden collector input')

    def gate_fixture(self):
        """Synthetic schema conversion of original bytes; not native gate evidence."""
        r=copy.deepcopy(self.report);p=r['probe']['startup']
        p.update(gate_contract='original_startup_retired_v1',retirement_trigger_proved=False,
                 original_mouse_press_sampled=any(v.word(bytes.fromhex(s['mouse_hex']),0x24)&1
                     for s in p['samples'] if 'startup_node' in s),
                 stop_reason='original_startup_exit0_and_menu_alone')
        return r

    def test_explicit_retirement_gate_keeps_trigger_unproved(self):
        r=self.gate_fixture();result=v.verify_report(r,self.raw)
        self.assertEqual(result['startup_gate_contract'],'original_startup_retired_v1')
        self.assertFalse(result['startup_retirement_trigger_proved'])
        self.assertFalse(result['native_menu_handoff_observed'])

    def test_campaign_gate_does_not_require_animation_threshold(self):
        r=self.gate_fixture();p=r['probe']['startup'];p['natural_animation_limit_observed']=False
        for s in p['samples']:
            if 'startup_head_hex' in s:
                b=bytearray.fromhex(s['startup_head_hex'])
                if b[0x30]==100:b[0x30]=22
                s['startup_head_hex']=b.hex()
        result=v.verify_startup_gate(r,self.raw)
        self.assertTrue(result['native_handoff_observed'])
        self.assertFalse(result['natural_animation_limit_observed'])
        self.assertFalse(result['retirement_trigger_proved'])

    def test_gate_cannot_claim_unsampled_trigger(self):
        r=self.gate_fixture();r['probe']['startup']['original_mouse_press_sampled']=not r['probe']['startup']['original_mouse_press_sampled']
        with self.assertRaisesRegex(ValueError,'trigger observations'):v.verify_startup_gate(r,self.raw)
        r=self.gate_fixture();r['probe']['startup']['retirement_trigger_proved']=True
        with self.assertRaisesRegex(ValueError,'scope'):v.verify_startup_gate(r,self.raw)

    def test_gate_requires_real_exit0_and_stable_menu(self):
        r=self.gate_fixture();r['probe']['startup']['worker_exit']['exit_code']=0xC0000005
        with self.assertRaisesRegex(ValueError,'exit0'):v.verify_startup_gate(r,self.raw)
        r=self.gate_fixture();p=r['probe']['startup'];p['samples'][-1]['elapsed']=p['samples'][-2]['elapsed']+.5
        with self.assertRaisesRegex(ValueError,'stable menu'):v.verify_startup_gate(r,self.raw)

    def synthetic_input(self):
        """Inert schema fixture; no claim that these bytes were captured live."""
        p=copy.deepcopy(self.report['probe']);game=self.report['lifecycle']['ready']['game']['pointer']
        hwnd=self.report['lifecycle']['ready']['window']['hwnd'];worker=p['workers'][0]
        row=next(s for s in p['samples'] if any(f['tid']==worker['thread_id'] and
            any(c['return_va']==0x45F065 for c in f['chain']) for f in s['frames']))
        frame=next(f for f in row['frames'] if f['tid']==worker['thread_id'])
        wait=next(c for c in frame['chain'] if c['return_va']==0x45F065)
        selector=next(c for c in frame['chain'] if c['bp']==wait['saved_bp'])
        selector_raw=bytearray(28);struct.pack_into('<I',selector_raw,0,3000)
        struct.pack_into('<III',selector_raw,12,worker['pointer'],selector['saved_bp'],0x45EE6A)
        guard=dict(pid=p['pid'],main=p['main'],game=game,hwnd=hwnd,node=worker['pointer'],
            head_hex=row['tasks'][0]['header_hex'],manager_hex=row['manager_hex'],MAIN_event_hex='00'*8,
            frame=frame,selector_pointer=selector['bp'],selector_hex=selector_raw.hex(),
            input_HWND_hex=hwnd.to_bytes(4,'little').hex(),coordinate_mode_hex='01000000',
            cursor_hex=struct.pack('<ii',318,508).hex(),code=v.code_rows(self.raw,v.INPUT_RANGES),
            all_threads_resumed_before_input=True,producer_exports={},IAT=[])
        for slot,symbol in ((0x59236C,'GetCursorPos'),(0x592368,'ScreenToClient')):
            export=dict(module='user32.dll',symbol=symbol,base=0x76000000,RVA=slot-0x590000,
                        target=0x76000000+slot-0x590000,module_path='C:/Windows/SysWOW64/user32.dll',module_sha256='0'*64)
            guard['producer_exports'][str(slot)]=export
            guard['IAT'].append(dict(slot=slot,hex=export['target'].to_bytes(4,'little').hex()))
        wall=10**12
        action=dict(target=[318,508],before_click=[318,508],error=None,down_submitted=True,released=True,
            down_result=1,up_results=[1],down_wall_time_ns=wall+20_000_000,up_wall_time_ns=wall+100_000_000,
            moves=[],guard_observations=[copy.deepcopy(guard) for _ in range(4)],game_memory_written=False,transition_proved=False)
        receipt=dict(index=0,error=None,before_elapsed=300,after_elapsed=300.2,
                     activation=dict(hwnd=hwnd,before=hwnd,after=hwnd,operations=[]),action=action,input_samples=[])
        for ms,previous,current in [(0,0,0),(30,0,1),(60,1,1),(110,1,0),(150,0,0)]:
            b=bytearray(88);struct.pack_into('<ii',b,0,318,508)
            for offset,value in ((0x1C,previous),(0x20,current),(0x24,(previous^current)&current),
                                 (0x30,(previous^current)&previous)):struct.pack_into('<I',b,offset,value)
            receipt['input_samples'].append(dict(elapsed=300+ms/1000,wall_time_ns=wall+ms*1_000_000,
                mouse_hex=b.hex(),MAIN_event_hex='00'*8))
        p['mouse_controller']=dict(attempted=True,receipt=receipt,user_override_required=True,maximum_clicks=1)
        p['collector_input_actions']=[receipt]
        return p,game,hwnd,worker

    def input_result(self,fixture):
        p,game,hwnd,worker=fixture
        return v.verify_input(p,self.raw,game,hwnd,worker,check_disk=False)

    def test_synthetic_raw_press_hold_release_semantics(self):
        result=self.input_result(self.synthetic_input())
        self.assertTrue(result['input_edges_observed'])
        self.assertEqual(result['press_samples'],[1]);self.assertEqual(result['release_samples'],[3])

    def test_submission_without_raw_release_never_proves_edges(self):
        fixture=self.synthetic_input();s=fixture[0]['mouse_controller']['receipt']['input_samples'][3]
        b=bytearray.fromhex(s['mouse_hex']);struct.pack_into('<I',b,0x30,0);s['mouse_hex']=b.hex()
        result=self.input_result(fixture)
        self.assertFalse(result['input_edges_observed']);self.assertEqual(result['asynchronous_incoherent_samples'],[3])

    def test_guard_selector_owner_and_caller_tamper_rejected(self):
        for offset in (12,20):
            fixture=self.synthetic_input();g=fixture[0]['mouse_controller']['receipt']['action']['guard_observations'][0]
            b=bytearray.fromhex(g['selector_hex']);struct.pack_into('<I',b,offset,1);g['selector_hex']=b.hex()
            with self.assertRaisesRegex(ValueError,'selector this/caller'):self.input_result(fixture)

    def test_guard_iat_and_producer_code_tamper_rejected(self):
        for field in ('IAT','code'):
            fixture=self.synthetic_input();g=fixture[0]['mouse_controller']['receipt']['action']['guard_observations'][0]
            if field=='IAT':g[field][0]['hex']='00000000'
            else:g[field].pop()
            with self.assertRaises(ValueError):self.input_result(fixture)

    def test_duplicate_receipt_or_wrong_target_rejected(self):
        fixture=self.synthetic_input();fixture[0]['collector_input_actions'].append(copy.deepcopy(fixture[0]['collector_input_actions'][0]))
        with self.assertRaisesRegex(ValueError,'at most one'):self.input_result(fixture)
        fixture=self.synthetic_input();fixture[0]['mouse_controller']['receipt']['action']['before_click']=[0,0]
        with self.assertRaisesRegex(ValueError,'actual cursor'):self.input_result(fixture)

    def test_release_exception_and_unbounded_hold_rejected(self):
        fixture=self.synthetic_input();fixture[0]['mouse_controller']['receipt']['action']['release_error']='OSError'
        with self.assertRaisesRegex(ValueError,'down/up'):self.input_result(fixture)
        fixture=self.synthetic_input();fixture[0]['mouse_controller']['receipt']['action']['up_wall_time_ns']+=10**9
        with self.assertRaisesRegex(ValueError,'wall interval'):self.input_result(fixture)

    def absolute_fixture(self):
        fixture=self.synthetic_input();action=fixture[0]['mouse_controller']['receipt']['action']
        geometry=dict(screen_target=[318,508],virtual_desktop=[0,0,1024,768],
                      window_rect=[0,0,1024,768],coordinate_mode=1,point_window=fixture[2])
        action.update(movement_mode='absolute_virtual_desktop',click_geometry=copy.deepcopy(geometry),
                      moves=[dict(before=[520,376],submitted=1,flags=0xC001,geometry=geometry,
                                  normalized=[round(318*65535/1023),round(508*65535/767)])])
        return fixture

    def test_absolute_input_requires_raw_feedback_and_final_geometry(self):
        fixture=self.absolute_fixture();result=self.input_result(fixture)
        self.assertTrue(result['input_edges_observed'])
        self.assertEqual(result['movement_mode'],'absolute_virtual_desktop')
        fixture[0]['mouse_controller']['receipt']['action']['moves']=[]
        self.assertTrue(self.input_result(fixture)['input_edges_observed'])
        del fixture[0]['mouse_controller']['receipt']['action']['click_geometry']
        with self.assertRaisesRegex(ValueError,'final geometry'):self.input_result(fixture)

    def test_absolute_geometry_wrong_window_or_normalization_rejected(self):
        fixture=self.absolute_fixture();fixture[0]['mouse_controller']['receipt']['action']['click_geometry']['point_window']=1
        with self.assertRaisesRegex(ValueError,'unobscured window'):self.input_result(fixture)
        fixture=self.absolute_fixture();fixture[0]['mouse_controller']['receipt']['action']['moves'][0]['normalized'][0]+=1
        with self.assertRaisesRegex(ValueError,'normalized'):self.input_result(fixture)

    def test_absolute_geometry_negative_origin_and_bounds(self):
        g=dict(screen_target=[-1920,0],virtual_desktop=[-1920,0,3840,1080],
               window_rect=[-1920,0,1920,1080],coordinate_mode=1,point_window=7)
        v.verify_geometry(g,(318,508),7,1,[0,0])
        g['screen_target']=[1919,1079];v.verify_geometry(g,(318,508),7,1,[65535,65535])
        g['screen_target']=[1920,1079]
        with self.assertRaisesRegex(ValueError,'desktop'):v.verify_geometry(g,(318,508),7,1)

    def test_authorization_binds_original_archive_without_rewriting_receipt(self):
        backend=v.authorization_backend()
        self.assertEqual(backend['sha256'],'22feb6770b4e26d251b845b7ea8992db982de55d28d75537584fee516950ec26')
        with mock.patch.object(v,'AUTHORIZATION_ARCHIVE_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'archive'):v.authorization_backend()

    def story_fixture(self):
        """Inert ADV/keyboard schema fixture, not an observed native ADV task."""
        p=copy.deepcopy(self.report['probe']);row=copy.deepcopy(p['samples'][-1]);task=row['tasks'][0]
        node=task['pointer'];tid=task['thread_id'];program=0x20000;pc=100
        head=bytearray.fromhex(task['header_hex']);struct.pack_into('<I',head,0,v.ADV)
        task.update(vtable=v.ADV,header_hex=head.hex(),vtable_hex=self.raw[v.ADV-0x400000:v.ADV-0x400000+8].hex())
        row['registered_tasks'][0]['head_hex']=head[:48].hex()
        vm=bytearray(128);vm[4]=1;struct.pack_into('<I',vm,16,program);struct.pack_into('<I',vm,28,pc)
        struct.pack_into('<HH',vm,32,1,51);row['VM_hex']=vm.hex();row['elapsed']=300
        prior=copy.deepcopy(row);prior['elapsed']=299;p['samples']=[prior,row]
        worker=copy.deepcopy(p['workers'][0]);worker['vtable']=v.ADV
        hwnd=self.report['lifecycle']['ready']['window']['hwnd'];game=row['game'];wall=10**12
        receipt=dict(scan_code=0x39,hold_ms=120,maximum_hold_ms=120,hold_ms_is_ceiling=True,
            hold_policy='release_on_first_observed_VM_advance_or_120ms',input_returned=True,released=True,
            down_submitted=True,up_attempted=True,down_result=1,up_results=[1],hwnd=hwnd,pid=p['pid'],
            existing_process_memory_written=False,start_ns=1_000_000_000,down_ns=1_010_000_000,
            up_ns=1_090_000_000,end_ns=1_100_000_000,start_wall_time_ns=wall,
            down_wall_time_ns=wall+10_000_000,up_wall_time_ns=wall+90_000_000,end_wall_time_ns=wall+100_000_000)
        action=dict(key=[node,program,pc],before_elapsed=300.01,after_elapsed=300.2,error=None,
            game_memory_written=False,full_instruction_causality_proved=False,before_sample=row,
            input_code_identity=v.code_rows(self.raw,v.KEY_RANGES),activation=dict(hwnd=hwnd,before=hwnd,after=hwnd,operations=[]),
            backend=dict(receipt=receipt),samples=[],transition=dict(press_index=1,release_index=2,advanced_index=2,
                before_PC=100,after_PC=104,transition_observed=True,full_instruction_causality_proved=False))
        for i,ms in enumerate((0,40,120)):
            keyboard=bytearray(0xA00);current_vm=bytearray(vm)
            if i==1:keyboard[0x4B9]=0x80;struct.pack_into('<H',current_vm,32,0)
            if i==2:struct.pack_into('<I',current_vm,28,104)
            action['samples'].append(dict(index=i,elapsed=300.02+ms/1000,wall_time_ns=wall+ms*1_000_000,
                foreground_hwnd=hwnd,keyboard_hex=keyboard.hex(),VM_hex=current_vm.hex(),mouse_hex='00'*0x58))
        p.update(collector_story_input_actions=[action],maximum_story_confirmations=96,
                 collector_input_actions_scope='mouse_menu_only',collector_input_actions=[{'synthetic_only':True}],
                 mouse_controller=dict(attempted=True))
        return p,game,hwnd,{(node,tid):worker}

    def story_result(self,fixture):
        p,game,hwnd,workers=fixture
        return v.verify_story_actions(p,self.raw,game,hwnd,workers)

    def test_synthetic_story_uses_original_key_query_and_scope(self):
        result=self.story_result(self.story_fixture())
        self.assertEqual(len(result),1);self.assertEqual(result[0]['original_key_query_replays'],3)
        self.assertEqual(result[0]['after_PC'],104);self.assertFalse(result[0]['full_instruction_causality_proved'])

    def test_story_cannot_be_ignored_or_exceed_budget(self):
        fixture=self.story_fixture();fixture[0]['collector_input_actions_scope']='all_input'
        with self.assertRaisesRegex(ValueError,'separated'):self.story_result(fixture)
        fixture=self.story_fixture();fixture[0]['maximum_story_confirmations']=97
        with self.assertRaisesRegex(ValueError,'budget'):self.story_result(fixture)

    def test_story_non_confirmation_and_short_wait_rejected(self):
        fixture=self.story_fixture();a=fixture[0]['collector_story_input_actions'][0]
        vm=bytearray.fromhex(a['before_sample']['VM_hex']);struct.pack_into('<H',vm,34,52);a['before_sample']['VM_hex']=vm.hex()
        with self.assertRaisesRegex(ValueError,'opcode51'):self.story_result(fixture)
        fixture=self.story_fixture();fixture[0]['samples'][0]['elapsed']=299.9
        with self.assertRaisesRegex(ValueError,'stable original'):self.story_result(fixture)

    def test_story_cached_transition_cannot_forge_original_input(self):
        fixture=self.story_fixture();a=fixture[0]['collector_story_input_actions'][0]
        a['transition']['after_PC']=999
        with self.assertRaisesRegex(ValueError,'derived story transition'):self.story_result(fixture)
        fixture=self.story_fixture();a=fixture[0]['collector_story_input_actions'][0]
        a['samples'][1]['keyboard_hex']='00'*0xA00
        with self.assertRaises(ValueError):self.story_result(fixture)

    def test_story_hold_limit_and_actual_tls_owner_rejected(self):
        fixture=self.story_fixture();r=fixture[0]['collector_story_input_actions'][0]['backend']['receipt']
        r['up_ns']=r['down_ns']+121_000_000;r['end_ns']=r['up_ns']+1
        with self.assertRaisesRegex(ValueError,'hold limit'):self.story_result(fixture)
        fixture=self.story_fixture();t=fixture[0]['collector_story_input_actions'][0]['before_sample']['tasks'][0]
        t['TLS']['owner_pid']=1
        with self.assertRaisesRegex(ValueError,'same TEB'):self.story_result(fixture)

    def test_story_uses_pre_key_raw_vm_endpoint_not_snapshot_start_clock(self):
        fixture=self.story_fixture();action=fixture[0]['collector_story_input_actions'][0]
        action['before_sample']['elapsed']=299.984
        result=self.story_result(fixture)[0]
        self.assertAlmostEqual(result['ready_task_snapshot_seconds'],.984)
        self.assertGreaterEqual(result['ready_VM_sample_seconds'],1)

    def test_story_expanded_budget_requires_explicit_generation_limit(self):
        fixture=self.story_fixture();p,game,hwnd,workers=fixture;p['maximum_story_confirmations']=192
        with self.assertRaisesRegex(ValueError,'budget'):self.story_result(fixture)
        self.assertEqual(len(v.verify_story_actions(p,self.raw,game,hwnd,workers,maximum_allowed=192)),1)

    def test_budget_stop_requires_exact_count_and_unconsumed_original_wait(self):
        fixture=self.story_fixture();p,game,hwnd,workers=fixture
        results=self.story_result(fixture);p['maximum_story_confirmations']=1
        row=copy.deepcopy(p['samples'][-1]);row['elapsed']=302
        vm=bytearray.fromhex(row['VM_hex']);struct.pack_into('<I',vm,28,200);row['VM_hex']=vm.hex()
        row['keyboard_hex']='00'*0xA00
        p.update(stop_reason='story_confirmation_budget',story_budget_wait_sample=row)
        result=v.verify_budget_stop(p,self.raw,game,workers,results)
        self.assertEqual(result['PC'],200);self.assertFalse(result['next_confirmation_submitted'])
        self.assertFalse(result['chapter_completion_proved'])
        p['maximum_story_confirmations']=2
        with self.assertRaisesRegex(ValueError,'exactly'):v.verify_budget_stop(p,self.raw,game,workers,results)
        p['maximum_story_confirmations']=1;vm[32]=0;row['VM_hex']=vm.hex()
        with self.assertRaisesRegex(ValueError,'unconsumed'):v.verify_budget_stop(p,self.raw,game,workers,results)

    def opcode40_fixture(self):
        fixture=self.story_fixture();a=fixture[0]['collector_story_input_actions'][0]
        pending=copy.deepcopy(a['samples'][1]);pending.update(index=2,elapsed=300.10,wall_time_ns=10**12+80_000_000)
        b=bytearray.fromhex(pending['VM_hex']);struct.pack_into('<HHH',b,32,0,40,12);pending['VM_hex']=b.hex()
        a['samples'].insert(2,pending);a['samples'][-1]['index']=3
        b=bytearray.fromhex(a['samples'][-1]['VM_hex']);struct.pack_into('<I',b,28,112)
        struct.pack_into('<HHH',b,32,1,40,12);a['samples'][-1]['VM_hex']=b.hex()
        a['transition'].update(release_index=3,advanced_index=3,after_PC=112)
        return fixture

    def test_original_next_opcode_is_written_before_pc_advancement(self):
        result=self.story_result(self.opcode40_fixture())[0]
        self.assertEqual(result['opcode_dispatch_samples'],[dict(index=2,opcode=40,length=12,PC=100)])
        self.assertEqual(result['after_PC'],112)
        altered=bytearray(self.raw);altered[0x4CE9DD-0x400000]=0x90
        with self.assertRaisesRegex(ValueError,'dispatch update order'):v.vm_dispatch_contract(altered)

    def test_dispatch_phase_cannot_relax_prepress_or_command_length(self):
        fixture=self.opcode40_fixture();a=fixture[0]['collector_story_input_actions'][0]
        b=bytearray.fromhex(a['samples'][0]['VM_hex']);struct.pack_into('<HH',b,32,0,40);a['samples'][0]['VM_hex']=b.hex()
        with self.assertRaisesRegex(ValueError,'before first press'):self.story_result(fixture)
        fixture=self.opcode40_fixture();a=fixture[0]['collector_story_input_actions'][0]
        b=bytearray.fromhex(a['samples'][2]['VM_hex']);struct.pack_into('<H',b,36,8);a['samples'][2]['VM_hex']=b.hex()
        with self.assertRaisesRegex(ValueError,'command-length'):self.story_result(fixture)


if __name__=='__main__':unittest.main()
