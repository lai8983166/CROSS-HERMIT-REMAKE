"""Pure observation tamper tests; never creates a VM, window, hook or input."""
import copy
import unittest

from devtools import isolated_vm_preflight as v


def fixture():
    nonce=0x41234567
    graphics=[dict(fullscreen=f,passed=True,create_hr=0,clear_hr=0,present_hr=0,
                   device_release=0,factory_release=0)for f in (False,True)]
    return dict(schema_version=1,accepted=False,nonce=nonce,
        host=dict(uuid='12345678-1234-1234-1234-123456789abc'),
        guest_executable=dict(path=str(v.WORKER/'guest-preflight.exe'),bytes=4096,sha256='a'*64),
        implementations=[v.identity(p)for p in (v.ROOT/'devtools/isolated_vm_preflight.py',
            v.ROOT/'devtools/isolated_windows_vm.py',v.ROOT/'devtools/isolated_guest_preflight.cs')],
        host_observation=dict(hooks_installed=True,hooks_removed=[True,True],error=None,
            tagged_mouse=0,tagged_keyboard=0,host_input_injected=False,host_input_blocked=False),
        guest=dict(schema_version=1,accepted=False,game_executed=False,nonce=nonce,pid=3184,
            foreground_before=dict(hwnd=196682,pid=1196,tid=4204,title='',own_desktop='Default',
                own_window=393760,own_pid=3184,own_tid=3140,own_desktop_query_succeeded=True),
            foreground_after=dict(hwnd=393760,pid=3184,tid=3140,title='Dedicated guest input preflight',
                own_desktop='Default',own_window=393760,own_pid=3184,own_tid=3140,
                own_desktop_query_succeeded=True),
            set_foreground_result=False,guest_queue_attached=True,attached_set_foreground_result=True,
            guest_queue_detached=True,guest_queue_binding=dict(own_tid=3140,target_hwnd=196682,
                target_pid=1196,target_tid=4204,target_session=1,own_session=1),
            executable_sha256='a'*64,machine=dict(uuid='87654321-4321-4321-4321-cba987654321',
                computer_name='CHAOMOFA-WORKER',manufacturer='VMware, Inc.',model='VMware Virtual Platform',
                session=1,active_console_session=1,logical_processors=2,memory_bytes=4*1024**3,
                boot_utc='2026-11-08T01:02:03.1234560Z'),
            events=[dict(message=m,extra=nonce,foreground=True)for m in (0x201,0x202,0x100,0x101)],
            preflight_passed=True,input_messages_received=True,window_destroyed=True,
            cleanup_release_submissions=2,graphics=graphics))


class Verification(unittest.TestCase):
    def reject(self,change):
        report=fixture();change(report)
        with self.assertRaises((ValueError,KeyError,TypeError)):v.verify(report)

    def test_finite_capability_only(self):
        result=v.verify(fixture())
        self.assertTrue(result['input_isolation_preflight_passed'])
        self.assertTrue(result['d3d8_preflight_passed'])
        for name in ('accepted','original_game_compatible','full_battle_exit_accepted',
                     'continuous_host_performance_unaffected_proved'):self.assertIs(result[name],False)

    def test_guest_error_rejected(self):self.reject(lambda r:r['guest'].update(error='failed'))
    def test_game_claim_rejected(self):self.reject(lambda r:r['guest'].update(game_executed=True))
    def test_acceptance_claim_rejected(self):self.reject(lambda r:r.update(accepted=True))
    def test_zero_nonce_rejected(self):
        def change(r):
            r['nonce']=r['guest']['nonce']=0
            for event in r['guest']['events']:event['extra']=0
        self.reject(change)
    def test_same_host_guest_rejected(self):self.reject(lambda r:r['guest']['machine'].update(uuid=r['host']['uuid']))
    def test_invalid_guest_uuid_rejected(self):self.reject(lambda r:r['guest']['machine'].update(uuid=''))
    def test_wrong_console_rejected(self):self.reject(lambda r:r['guest']['machine'].update(active_console_session=2))
    def test_host_challenge_leak_rejected(self):self.reject(lambda r:r['host_observation'].update(tagged_mouse=1))
    def test_blocking_host_rejected(self):self.reject(lambda r:r['host_observation'].update(host_input_blocked=True))
    def test_hook_cleanup_rejected(self):self.reject(lambda r:r['host_observation'].update(hooks_removed=[True,False]))
    def test_missing_guest_release_rejected(self):self.reject(lambda r:r['guest']['events'].pop())
    def test_wrong_nonce_edge_rejected(self):self.reject(lambda r:r['guest']['events'][1].update(extra=1))
    def test_not_foreground_rejected(self):self.reject(lambda r:r['guest']['events'][1].update(foreground=False))
    def test_wrong_binary_rejected(self):self.reject(lambda r:r['guest'].update(executable_sha256='b'*64))
    def test_failed_d3d_rejected(self):self.reject(lambda r:r['guest']['graphics'][1].update(present_hr=-1))
    def test_leaked_d3d_rejected(self):self.reject(lambda r:r['guest']['graphics'][0].update(device_release=1))
    def test_graphics_error_not_success(self):self.reject(lambda r:r['guest']['graphics'][0].update(error='failure'))
    def test_source_identity_rejected(self):self.reject(lambda r:r['implementations'][0].update(sha256='0'*64))
    def test_missing_boot_rejected(self):self.reject(lambda r:r['guest']['machine'].pop('boot_utc'))
    def test_local_boot_time_rejected(self):self.reject(lambda r:r['guest']['machine'].update(boot_utc='2026-11-08T01:02:03'))
    def test_non_utc_boot_time_rejected(self):self.reject(lambda r:r['guest']['machine'].update(boot_utc='2026-11-08T01:02:03+08:00'))
    def test_invalid_boot_calendar_rejected(self):self.reject(lambda r:r['guest']['machine'].update(boot_utc='2026-02-30T01:02:03.0000000Z'))
    def test_non_integer_resource_rejected(self):self.reject(lambda r:r['guest']['machine'].update(logical_processors=2.0))

    def test_direct_foreground_without_attach(self):
        report=fixture();g=report['guest'];g['set_foreground_result']=True
        for key in ('guest_queue_attached','guest_queue_detached','guest_queue_binding','attached_set_foreground_result'):del g[key]
        result=v.verify(report)
        self.assertIs(result['guest_queue_fallback_used'],False)
        self.assertIs(result['guest_queue_detach_verified'],False)

    def test_actual_fallback_with_detach(self):
        result=v.verify(fixture())
        self.assertIs(result['guest_queue_fallback_used'],True)
        self.assertIs(result['guest_queue_detach_verified'],True)

    def test_failed_detach_rejected(self):self.reject(lambda r:r['guest'].update(guest_queue_detached=False))
    def test_missing_detach_rejected(self):self.reject(lambda r:r['guest'].pop('guest_queue_detached'))
    def test_attach_failed_rejected(self):self.reject(lambda r:r['guest'].update(guest_queue_attached=False))
    def test_attached_focus_failed_rejected(self):self.reject(lambda r:r['guest'].update(attached_set_foreground_result=False))
    def test_fallback_target_session_rejected(self):self.reject(lambda r:r['guest']['guest_queue_binding'].update(target_session=2))
    def test_fallback_wrong_calling_thread_rejected(self):self.reject(lambda r:r['guest']['guest_queue_binding'].update(own_tid=999))
    def test_fallback_self_thread_rejected(self):self.reject(lambda r:r['guest']['guest_queue_binding'].update(target_tid=3140))
    def test_fallback_zero_target_rejected(self):self.reject(lambda r:r['guest']['guest_queue_binding'].update(target_hwnd=0))
    def test_missing_actual_binding_rejected(self):self.reject(lambda r:r['guest'].pop('guest_queue_binding'))
    def test_other_final_pid_rejected(self):self.reject(lambda r:r['guest']['foreground_after'].update(pid=1196))
    def test_other_final_window_rejected(self):self.reject(lambda r:r['guest']['foreground_after'].update(hwnd=196682))
    def test_other_final_thread_rejected(self):self.reject(lambda r:r['guest']['foreground_after'].update(tid=4204))
    def test_failed_desktop_query_rejected(self):self.reject(lambda r:r['guest']['foreground_after'].update(own_desktop_query_succeeded=False))
    def test_other_desktop_rejected(self):self.reject(lambda r:r['guest']['foreground_after'].update(own_desktop='Winlogon'))
    def test_fabricated_direct_attach_branch_rejected(self):self.reject(lambda r:r['guest'].update(set_foreground_result=True))
    def test_attach_target_may_change_after_initial_observation(self):
        report=fixture();report['guest']['guest_queue_binding'].update(target_hwnd=196688,target_pid=1200,target_tid=4208)
        self.assertIs(v.verify(report)['guest_queue_detach_verified'],True)


if __name__=='__main__':unittest.main()
