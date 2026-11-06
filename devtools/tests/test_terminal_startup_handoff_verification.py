"""Mutate the small retained native v1 source; never start native execution."""
import copy
import unittest

from devtools import terminal_startup_handoff_verification as v


class StartupHandoffVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=v.owner.read_report(v.ROOT/'analysis/terminal-startup-handoff-v1-20261107.json.gz',
            'f855f920bef4b80bec82acaa3af90fb1c97c8c90c81e4cad18c46753d6abe42e')
        cls.raw=(v.ROOT/'analysis/hermit_game.exe').read_bytes()

    def reject(self,mutate,message=None):
        changed=copy.deepcopy(self.report)
        mutate(changed)
        with self.assertRaises(ValueError) as caught:
            v.verify_report(changed,self.raw)
        if message:self.assertIn(message,str(caught.exception))

    def v2_fixture(self):
        """Synthetic schema upgrade, not a native v2 observation or receipt."""
        r=copy.deepcopy(self.report);p=r['probe']
        p['source_before']['code'] += [dict(pointer=a,bytes=b-a,
            sha256=v.owner.sha(self.raw[a-0x400000:b-0x400000])) for a,b in v.V2_RANGES]
        p['source_before']['IAT'] += [dict(slot=a,hex='00000077') for a in (0x592440,0x592284)]
        p['source_after']=copy.deepcopy(p['source_before'])
        event=copy.deepcopy(p['worker']['node_event'])
        event['remote_handle']=v.word(bytes.fromhex(p['samples'][0]['manager_hex']),0x118)
        p['worker']['manager_event']=event
        for s in p['samples']:
            if 'TLS' in s:
                tls=s['TLS'];tls['index_memory']=dict(pointer=0x761BC0,
                    hex=tls['TLS_index'].to_bytes(4,'little').hex())
                if tls['TLS_index']>=64:
                    tls['expansion_memory']=dict(pointer=tls['TEB']+0xF94,
                        hex=tls['expansion_pointer'].to_bytes(4,'little').hex())
        return r

    def reject_v2(self,mutate,message=None):
        changed=self.v2_fixture();mutate(changed)
        with self.assertRaises(ValueError) as caught:v.verify_report(changed,self.raw)
        if message:self.assertIn(message,str(caught.exception))

    @staticmethod
    def tls_sample(report):
        return next(r for r in report['probe']['samples'] if 'TLS' in r)

    def test_actual_record_is_only_partial_handoff(self):
        result=v.verify_report(self.report,self.raw)
        self.assertEqual((result['samples'],result['TLS_samples']),(262,258))
        self.assertEqual(result['status'],'partial_handoff_observation')
        self.assertTrue(result['native_handoff_observed'])
        for name in ('accepted','normal_PTD_cleanup_proved','full_resource_lifetime_proved',
                     'full_battle_exit_accepted','formal_terminal_boundary_advanced',
                     'continuously_proved_no_overlap','all_static_contract_ranges_live_authenticated'):
            self.assertIs(result[name],False)

    def test_exception_exit_cannot_be_natural_handoff(self):
        self.reject(lambda r:r['probe']['worker_exit'].update(exit_code=0xC0000005),'handoff claim')

    def test_unsigned_exit_cannot_pass(self):
        self.reject(lambda r:r['probe']['worker_exit'].update(wait_status=258),'signaled')

    def test_post_cleanup_exit_rejected(self):
        self.reject(lambda r:r['probe']['worker_exit'].update(before_WM_CLOSE=False),'before cleanup')

    def test_no_writes_or_calls_allowed(self):
        for name in ('host_memory_writes','host_original_calls','host_input_actions'):
            with self.subTest(name=name):
                self.reject(lambda r:r['probe'][name].append({'fake':True}),'no original calls')

    def test_write_capable_process_handle_rejected(self):
        self.reject(lambda r:r['probe'].update(process_access=0x1FFFFF),'process rights')

    def test_false_scope_cannot_be_upgraded(self):
        self.reject(lambda r:r.update(full_battle_exit_accepted=True),'scope')
        self.reject(lambda r:r['probe'].update(normal_PTD_cleanup_proved=True),'scope')

    def test_omitted_live_range_rejected(self):
        def change(r):
            r['probe']['source_before']['code'].pop()
            r['probe']['source_after']=copy.deepcopy(r['probe']['source_before'])
        self.reject(change,'declared live original ranges')

    def test_null_iat_rejected_even_if_before_equals_after(self):
        def change(r):
            r['probe']['source_before']['IAT'][0]['hex']='00000000'
            r['probe']['source_after']=copy.deepcopy(r['probe']['source_before'])
        self.reject(change,'non-null')

    def test_raw_counter_does_not_match_scalar(self):
        self.reject(lambda r:self.tls_sample(r)['callback_locals'].update(counter=16205),'raw callback')

    def test_no_threshold_observation_cannot_be_invented(self):
        def change(r):
            for s in r['probe']['samples']:
                if 'startup_head_hex' in s:
                    b=bytearray.fromhex(s['startup_head_hex'])
                    if b[0x30]==100:b[0x30]=22;s['startup_head_hex']=b.hex()
        self.reject(change,'threshold claim')

    def test_wrong_callback_stack_pointer(self):
        self.reject(lambda r:self.tls_sample(r)['callback_locals'].update(pointer=0x10000),'frame address')

    def test_wrong_tls_index_or_owner(self):
        self.reject(lambda r:self.tls_sample(r)['TLS'].update(TLS_index=63),'pointer arithmetic')
        self.reject(lambda r:self.tls_sample(r)['TLS'].update(owner_pid=1),'same TEB')

    def test_ptd_callback_tamper(self):
        def change(r):
            s=self.tls_sample(r);b=bytearray.fromhex(s['TLS']['PTD_hex']);b[0x48:0x4C]=(0x451670).to_bytes(4,'little')
            s['TLS']['PTD_hex']=b.hex()
        self.reject(change,'PTD worker')

    def test_cycle_rejected(self):
        def change(r):
            s=self.tls_sample(r);row=s['registered_tasks'][0];b=bytearray.fromhex(row['head_hex'])
            b[12:16]=row['pointer'].to_bytes(4,'little');row['head_hex']=b.hex()
        self.reject(change,'acyclic')

    def test_short_stable_menu_suffix_rejected(self):
        self.reject(lambda r:r['probe']['samples'][-1].update(
            elapsed=r['probe']['samples'][-2]['elapsed']+.5),'handoff claim')

    def test_missing_cleanup_and_forced_kill_rejected(self):
        self.reject(lambda r:r['lifecycle']['lifetime'].update(members_after_cleanup=[1]),'Job drained')
        self.reject(lambda r:r['lifecycle']['lifetime'].update(forced_termination=True),'Job drained')

    def test_nonfinite_timing_rejected(self):
        self.reject(lambda r:r['probe']['samples'][-1].update(elapsed=float('nan')),'sample time')

    def test_protected_child_cleanup_is_not_normal_winmain(self):
        result=v.verify_report(self.report,self.raw)
        self.assertIs(result['WinMain_normal_return_proved'],False)
        child=str(self.report['probe']['pid'])
        self.assertEqual(result['cleanup_process_exits'][child]['code'],0xC0000354)
        self.reject(lambda r:r['lifecycle']['lifetime'].update(child_status_is_not_WinMain_return=False),'WinMain')
        self.reject(lambda r:r['lifecycle']['lifetime']['exits'].pop(child),'complete owned process')

    def test_cannot_relabel_old_report_as_new_range_version(self):
        self.reject(lambda r:r.update(schema_version=2),'schema')

    def test_synthetic_v2_schema_covers_static_contract_ranges(self):
        result=v.verify_report(self.v2_fixture(),self.raw)
        self.assertEqual(result['observed_source_contract_version'],2)
        self.assertTrue(result['all_static_contract_ranges_live_authenticated'])
        self.assertTrue(result['TLS_index_raw_identity_verified'])
        self.assertTrue(result['manager_event_object_identity_verified'])
        self.assertFalse(result['accepted'])

    def test_v2_mixed_iat_version_rejected(self):
        def change(r):
            r['probe']['source_before']['IAT']=r['probe']['source_before']['IAT'][:-2]
            r['probe']['source_after']=copy.deepcopy(r['probe']['source_before'])
        self.reject_v2(change,'live IAT')

    def test_v2_raw_index_pointer_and_bytes_rejected(self):
        self.reject_v2(lambda r:self.tls_sample(r)['TLS']['index_memory'].update(pointer=0x761BC4),'TLS index address')
        self.reject_v2(lambda r:self.tls_sample(r)['TLS']['index_memory'].update(hex='40000000'),'TLS index address')
        self.reject_v2(lambda r:self.tls_sample(r)['TLS'].pop('index_memory'),'TLS index address')

    def test_v2_manager_event_owner_type_and_raw_handle_rejected(self):
        self.reject_v2(lambda r:r['probe']['worker']['manager_event'].update(owner_pid=1),'manager event')
        self.reject_v2(lambda r:r['probe']['worker']['manager_event'].update(type_name='Thread'),'manager event')
        self.reject_v2(lambda r:r['probe']['worker']['manager_event'].update(remote_handle=4),'raw manager')
        self.reject_v2(lambda r:r['probe']['worker'].pop('manager_event'),'manager Event identity')

    def test_v1_cannot_ignore_v2_raw_fields(self):
        self.reject(lambda r:self.tls_sample(r)['TLS'].update(index_memory={'pointer':1,'hex':'00000000'}),'v1 cannot')

    def test_v2_expansion_raw_pointer_contract(self):
        r=self.v2_fixture();s=self.tls_sample(r);tls=s['TLS'];worker=r['probe']['worker']
        frame=next(f for f in s['frames'] if f['tid']==worker['thread_id'])
        tls.update(TLS_index=65,expansion_pointer=0x300000,slot=0x300004,
            index_memory=dict(pointer=0x761BC0,hex='41000000'),
            expansion_memory=dict(pointer=tls['TEB']+0xF94,hex='00003000'))
        args=(tls,frame,bytes.fromhex(s['startup_head_hex']),worker['node'],worker['thread_id'],
              r['probe']['pid'],s['callback_locals'],2)
        v.verify_tls(*args)
        tls['expansion_memory']['pointer']+=4
        with self.assertRaisesRegex(ValueError,'TEB expansion'):v.verify_tls(*args)
        tls['expansion_memory']['pointer']-=4;tls['expansion_memory']['hex']='04003000'
        with self.assertRaisesRegex(ValueError,'TEB expansion'):v.verify_tls(*args)

    def test_same_native_worker_cannot_switch_ptd_mid_callback(self):
        def change(r):
            s=self.tls_sample(r);tls=s['TLS'];tls['PTD']+=0x100
            tls['TLS_slot_hex']=tls['PTD'].to_bytes(4,'little').hex()
            tls['ancestry']['wrapper_argument']=tls['PTD']
            tls['ancestry_memory']['wrapper_argument']['hex']=tls['TLS_slot_hex']
        self.reject_v2(change,'same callback/TEB/TLS/PTD')


if __name__=='__main__':unittest.main()
