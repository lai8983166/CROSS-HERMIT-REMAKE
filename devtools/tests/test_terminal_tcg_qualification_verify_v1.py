"""Synthetic offline contract tests; no Win32 calls or VM execution."""
import copy
import unittest
from devtools.terminal_tcg_qualification_verify_v1 import verify


def fixture():
    n=0x41234567
    ctx=dict(session=1,active_console_session=1,input_desktop='Default',input_desktop_query_succeeded=True,input_desktop_closed=True)
    fg=dict(hwnd=100,pid=20,tid=30,title='Dedicated guest input preflight',own_window=100,own_pid=20,own_tid=30,own_desktop='Default',own_desktop_query_succeeded=True)
    g=dict(schema='terminal-tcg-qualification-guest-v1',accepted=False,game_executed=False,guest_guard_passed=True,
           nonce=n,source_sha256='a'*64,executable_sha256='b'*64,pid=20,
           machine=dict(uuid='626d1a20-6383-4cd3-85d5-6c9831d6f941',computer_name='CHAOMOFA-WORKER',manufacturer='QEMU',
                        logical_processors=2,memory_bytes=4*1024**3,session=1,active_console_session=1,boot_utc='2026-11-11T01:02:03.1234567Z'),
           foreground_before=copy.deepcopy(fg),foreground_after=copy.deepcopy(fg),set_foreground_result=True,
           initial_input_context=copy.deepcopy(ctx),input_guards=[copy.deepcopy(ctx) for _ in range(5)],cleanup_input_context=copy.deepcopy(ctx),
           cleanup_foreground_owned=True,cleanup_release_submissions=2,window_destroyed=True,input_messages_received=True,
           events=[dict(message=m,extra=n,foreground=True) for m in (0x201,0x202,0x100,0x101)],preflight_passed=True,
           graphics=[dict(fullscreen=f,sdk_version=220,device_type=1,behavior_flags=36,fallback_attempted=False,factory_attempted=True,
                          factory_created=True,device_created=True,adapter_count=1,adapter_identifier_buffer_freed=True,display_mode_hr=0,create_hr=0,clear_hr=0,
                          present_hr=0,device_release=0,factory_release=0,passed=True) for f in (False,True)])
    r=dict(schema='terminal-tcg-qualification-v1',accepted=False,nonce=n,source_sha256='a'*64,guest_executable=dict(bytes=1000,sha256='b'*64),
           host=dict(uuid='12345678-1234-1234-1234-123456789abc'),guest=g,
           host_observation=dict(hooks_installed=True,hooks_removed=[True,True],error=None,tagged_mouse=0,tagged_keyboard=0,host_input_injected=False,host_input_blocked=False))
    args=dict(expected_source_sha256='a'*64,expected_executable_sha256='b'*64,expected_nonce=n,expected_boot_utc=g['machine']['boot_utc'])
    return r,args


class QualificationTest(unittest.TestCase):
    def test_success_is_bounded(self):
        r,a=fixture();v=verify(r,**a)
        self.assertTrue(v['qualified']);self.assertFalse(v['accepted']);self.assertFalse(v['original_game_compatible'])

    def test_null_factory_preserves_input_only_result(self):
        r,a=fixture();g=r['guest'];g['preflight_passed']=False;g['error']='HAL failed'
        for row in g['graphics']:
            row.clear();row.update(fullscreen=len([x for x in g['graphics'] if x.get('error')])==1,
                sdk_version=220,device_type=1,behavior_flags=36,fallback_attempted=False,factory_attempted=True,
                factory_created=False,factory_last_error=0,passed=False,error='Direct3DCreate8 returned NULL')
        v=verify(r,**a);self.assertTrue(v['input_isolation_verified']);self.assertFalse(v['qualified'])

    def test_tamper_rejections(self):
        mutations=[
            lambda r:r['guest']['machine'].update(manufacturer='VMware'),
            lambda r:r['guest']['machine'].update(uuid=r['host']['uuid']),
            lambda r:r['host'].update(uuid=r['guest']['machine']['uuid']),
            lambda r:r['guest']['machine'].update(boot_utc='2026-11-11T01:02:04Z'),
            lambda r:r['guest']['machine'].update(logical_processors=True),
            lambda r:r['guest']['machine'].update(memory_bytes=5*1024**3),
            lambda r:r['guest']['input_guards'][2].update(input_desktop='Winlogon'),
            lambda r:r['guest']['input_guards'][2].update(active_console_session=2),
            lambda r:r['guest']['input_guards'].pop(),
            lambda r:r['guest'].update(cleanup_foreground_owned=False),
            lambda r:r['guest'].update(cleanup_release_submissions=1),
            lambda r:r['guest']['events'][0].update(extra=1),
            lambda r:r['host_observation'].update(tagged_keyboard=1),
            lambda r:r['host_observation'].update(hooks_removed=[True,False]),
            lambda r:r['guest']['graphics'][0].update(fallback_attempted=True),
            lambda r:r['guest']['graphics'][1].update(factory_release=1),
            lambda r:r['guest']['foreground_after'].update(pid=99),
            lambda r:r.update(source_sha256='c'*64),
            lambda r:r['guest_executable'].update(sha256='d'*64),
            lambda r:r.update(nonce=0x41234568),
        ]
        for i,mutation in enumerate(mutations):
            with self.subTest(i=i):
                r,a=fixture();mutation(r)
                with self.assertRaises(ValueError):verify(r,**a)

    def test_expected_values_are_independent(self):
        for key,value in [('expected_nonce',0x41234568),('expected_source_sha256','c'*64),('expected_executable_sha256','c'*64),('expected_boot_utc','2026-11-11T01:02:04Z')]:
            with self.subTest(key=key):
                r,a=fixture();a[key]=value
                with self.assertRaises(ValueError):verify(r,**a)


if __name__=='__main__':unittest.main()
