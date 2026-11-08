"""Observe host input without injecting/blocking it while a guest probe runs."""
import argparse
import ctypes as C
from ctypes import wintypes as W
from datetime import datetime
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import threading
import time
import uuid
from devtools.isolated_windows_vm import ROOT,WORKER,VMX,vmrun,environment,identity,validate_vmx

IMPLEMENTATIONS=(Path(__file__),ROOT/'devtools/isolated_windows_vm.py',ROOT/'devtools/isolated_guest_preflight.cs')


def validate_boot_utc(value):
    """Accept an explicit UTC ISO timestamp while preserving its exact bytes."""
    if not isinstance(value,str) or re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,7})?(?:Z|\+00:00)',value)is None:
        raise ValueError('actual guest boot time must be explicit UTC ISO')
    # .NET round-trip timestamps have seven fractional digits; Python 3.10's
    # fromisoformat accepts only three or six. Validate the calendar separately,
    # retaining all seven original digits for exact boot-identity comparison.
    try:datetime.strptime(value[:19],'%Y-%m-%dT%H:%M:%S')
    except ValueError:raise ValueError('valid actual guest boot UTC calendar date')from None
    return value


def host_identity():
    code="[pscustomobject]@{uuid=(Get-CimInstance Win32_ComputerSystemProduct).UUID;computer=$env:COMPUTERNAME;free_kib=(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory}|ConvertTo-Json -Compress"
    r=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',code],
        env=environment(),capture_output=True,text=True,timeout=20,check=True)
    return json.loads(r.stdout)


def observe_host(nonce,execute,seconds=120):
    """All low-level hooks always call the next hook. No key values are saved."""
    if not 10<=seconds<=180:raise ValueError('bounded host observation')
    u=C.WinDLL('user32',use_last_error=True);k=C.WinDLL('kernel32',use_last_error=True)
    proc=C.WINFUNCTYPE(C.c_ssize_t,C.c_int,W.WPARAM,W.LPARAM)
    class Mouse(C.Structure):_fields_=[('point',W.POINT),('data',W.DWORD),('flags',W.DWORD),('time',W.DWORD),('extra',C.c_size_t)]
    class Key(C.Structure):_fields_=[('vk',W.DWORD),('scan',W.DWORD),('flags',W.DWORD),('time',W.DWORD),('extra',C.c_size_t)]
    u.SetWindowsHookExW.argtypes=[C.c_int,proc,W.HINSTANCE,W.DWORD];u.SetWindowsHookExW.restype=W.HANDLE
    u.CallNextHookEx.argtypes=[W.HANDLE,C.c_int,W.WPARAM,W.LPARAM];u.CallNextHookEx.restype=C.c_ssize_t
    u.UnhookWindowsHookEx.argtypes=[W.HANDLE];u.UnhookWindowsHookEx.restype=W.BOOL
    u.GetForegroundWindow.restype=W.HWND
    u.GetWindowThreadProcessId.argtypes=[W.HWND,C.POINTER(W.DWORD)]
    u.PeekMessageW.argtypes=[C.POINTER(W.MSG),W.HWND,W.UINT,W.UINT,W.UINT]
    k.GetModuleHandleW.argtypes=[W.LPCWSTR];k.GetModuleHandleW.restype=W.HMODULE
    report=dict(hooks_installed=False,tagged_mouse=0,tagged_keyboard=0,total_mouse_events=0,total_keyboard_events=0,
                host_input_injected=False,host_input_blocked=False,foreground_pids=[],error=None)
    @proc
    def mouse(code,w,l):
        if code>=0:
            report['total_mouse_events']+=1
            if C.cast(l,C.POINTER(Mouse)).contents.extra==nonce:report['tagged_mouse']+=1
        return u.CallNextHookEx(None,code,w,l)
    @proc
    def keyboard(code,w,l):
        if code>=0:
            report['total_keyboard_events']+=1
            if C.cast(l,C.POINTER(Key)).contents.extra==nonce:report['tagged_keyboard']+=1
        return u.CallNextHookEx(None,code,w,l)
    hooks=[];result={};thread=None;started=time.monotonic();pids=set()
    try:
        for kind,callback in ((14,mouse),(13,keyboard)):
            handle=u.SetWindowsHookExW(kind,callback,k.GetModuleHandleW(None),0)
            if not handle:raise C.WinError(C.get_last_error())
            hooks.append(handle)
        report['hooks_installed']=True
        def run():
            try:result['value']=execute()
            except Exception as e:result['error']=str(e)
        thread=threading.Thread(target=run,daemon=True);thread.start();ended=None
        while time.monotonic()-started<seconds:
            msg=W.MSG()
            while u.PeekMessageW(C.byref(msg),None,0,0,1):
                u.TranslateMessage(C.byref(msg));u.DispatchMessageW(C.byref(msg))
            pid=W.DWORD();u.GetWindowThreadProcessId(u.GetForegroundWindow(),C.byref(pid));pids.add(pid.value)
            if not thread.is_alive():
                if ended is None:ended=time.monotonic()
                if time.monotonic()-ended>=.5:break
            time.sleep(.005)
        if thread.is_alive():raise TimeoutError('guest command exceeded bounded host observation')
        if 'error'in result:raise RuntimeError(result['error'])
    except Exception as e:report['error']=str(e)
    finally:
        report['hooks_removed']=[bool(u.UnhookWindowsHookEx(h))for h in reversed(hooks)]
        report['elapsed_seconds']=round(time.monotonic()-started,3);report['foreground_pids']=sorted(pids)
    return report


def verify_foreground(guest):
    """Check the recorded same-session acquisition and exact detach branch."""
    def need(ok,reason):
        if not ok:raise ValueError(reason)
    def identifier(value):return type(value)is int and 0<value<=0xffffffff
    def handle(value):return type(value)is int and -(1<<31)<=value<=(1<<32)-1 and value!=0
    pid=guest['pid'];need(identifier(pid),'actual guest probe PID')
    before=guest['foreground_before'];after=guest['foreground_after']
    for row in (before,after):
        need(handle(row['own_window']) and row['own_pid']==pid and identifier(row['own_tid']),
             'guest foreground own HWND/PID/thread binding')
        need(row['own_desktop_query_succeeded']is True and row['own_desktop']=='Default',
             'actual guest Default desktop query')
    need(before['own_window']==after['own_window'] and before['own_tid']==after['own_tid'],
         'same guest probe window and thread before and after acquisition')
    need(after['hwnd']==after['own_window'] and after['pid']==pid and after['tid']==after['own_tid']
         and after['title']=='Dedicated guest input preflight','actual final foreground belongs to guest probe')
    direct=guest['set_foreground_result'];need(type(direct)is bool,'actual SetForegroundWindow boolean')
    fallback=('guest_queue_attached','attached_set_foreground_result','guest_queue_detached','guest_queue_binding')
    if direct:
        need(all(key not in guest for key in fallback),'no unexecuted attach branch claimed')
    else:
        need(all(guest[key]is True for key in fallback[:3]),'successful guest queue attach/focus/detach')
        binding=guest['guest_queue_binding'];session=guest['machine']['session']
        need(binding['own_tid']==after['own_tid'] and identifier(binding['target_tid'])
             and binding['target_tid']!=binding['own_tid'] and identifier(binding['target_pid'])
             and handle(binding['target_hwnd']),'actual AttachThreadInput source and target binding')
        need(type(binding['own_session'])is int and type(binding['target_session'])is int
             and binding['own_session']==binding['target_session']==session,
             'attach target belongs to the same guest console session')
    return dict(guest_probe_foreground_verified=True,guest_queue_fallback_used=not direct,
                guest_queue_detach_verified=not direct)


def verify(report):
    def need(ok,reason):
        if not ok:raise ValueError(reason)
    h=report['host_observation'];g=report['guest'];n=report['nonce'];machine=g['machine']
    need(report['schema_version']==1 and report['accepted']is False and not report.get('verification_error'),
         'bounded successful host preflight schema, never final acceptance')
    need(type(n)is int and 0x40000000<=n<=0x5fffffff,'fresh nonzero challenge domain')
    expected=[identity(p)for p in IMPLEMENTATIONS];recorded=report['implementations']
    need(len(recorded)==len(expected) and all(Path(a['path']).name==Path(b['path']).name and
        (a['bytes'],a['sha256'])==(b['bytes'],b['sha256']) for a,b in zip(recorded,expected)),
        'all actual preflight source identities match current deployment')
    executable=report['guest_executable']
    need(type(executable['bytes'])is int and 0<executable['bytes']<=4*1024*1024 and
         re.fullmatch('[0-9a-f]{64}',executable['sha256'])is not None,'bounded actual guest executable identity')
    need(g['schema_version']==1 and g['accepted']is False and g['game_executed']is False and not g.get('error'),
         'successful isolated probe cannot claim a game run or contain an error')
    need(h['hooks_installed'] and h['hooks_removed']==[True,True] and h['error']is None,'complete bounded host observation and cleanup')
    need(h['tagged_mouse']==h['tagged_keyboard']==0 and not h['host_input_injected']and not h['host_input_blocked'],'no challenge input reached or was injected/blocked on host')
    need(g['nonce']==n and g['executable_sha256']==report['guest_executable']['sha256'],'same guest challenge and executable')
    guest_uuid=uuid.UUID(machine['uuid']);host_uuid=uuid.UUID(report['host']['uuid'])
    need(guest_uuid.int!=0 and host_uuid.int!=0 and guest_uuid!=host_uuid,'valid separate host and guest machines')
    need(machine['computer_name']=='CHAOMOFA-WORKER'and 'VMware'in machine['manufacturer'] and 'Virtual'in machine['model']
         and type(machine['session'])is int and type(machine['active_console_session'])is int
         and machine['session']>0 and machine['session']==machine['active_console_session'],
         'dedicated guest interactive console identity')
    validate_boot_utc(machine['boot_utc'])
    need(type(machine['logical_processors'])is int and machine['logical_processors']==2
         and type(machine['memory_bytes'])is int and 3*1024**3<=machine['memory_bytes']<=4*1024**3,
         '2 vCPU / 4 GiB resource bound')
    foreground=verify_foreground(g)
    need([e['message']for e in g['events']]==[0x201,0x202,0x100,0x101]and all(e['extra']==n and e['foreground']for e in g['events']),'exact tagged input reached guest-owned foreground')
    need(g['preflight_passed']is True and g['input_messages_received']is True and g['window_destroyed']is True
         and g['cleanup_release_submissions']==2,'guest input release and window cleanup')
    need([r['fullscreen']for r in g['graphics']]==[False,True],'window and fullscreen tested')
    for r in g['graphics']:
        need(r['passed']is True and not r.get('error') and all(r[k]>=0 for k in ('create_hr','clear_hr','present_hr'))and
             r['device_release']==r['factory_release']==0,'HAL D3D8 rendering and cleanup')
    return dict(input_isolation_preflight_passed=True,d3d8_preflight_passed=True,**foreground,
                original_game_compatible=False,full_battle_exit_accepted=False,
                continuous_host_performance_unaffected_proved=False,accepted=False)


def run(label):
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-'for c in label):raise ValueError('simple unique label')
    validate_vmx(VMX.read_text(encoding='utf8'))
    output=WORKER/('preflight-'+label+'.json')
    if output.exists():raise ValueError('new preflight report required')
    exe=WORKER/'guest-preflight.exe';guest_exe='C:\\ChaomofaWorker\\guest-preflight.exe'
    guest_out='C:\\ChaomofaWorker\\preflight-'+label+'.json';local_guest=WORKER/('guest-preflight-'+label+'.json')
    if local_guest.exists():raise ValueError('new guest evidence required')
    vmrun(['CopyFileFromHostToGuest',VMX,exe,guest_exe],guest=True)
    nonce=0x40000000|secrets.randbits(29)
    report=dict(schema_version=1,nonce=nonce,host=host_identity(),guest_executable=identity(exe),
                vmx=identity(VMX),accepted=False)
    paths=IMPLEMENTATIONS
    report['implementations']=[identity(p)for p in paths]
    report['host_observation']=observe_host(nonce,lambda:vmrun(['runProgramInGuest',VMX,'-activeWindow','-interactive',guest_exe,guest_out,format(nonce,'x')],guest=True,timeout=90))
    try:
        vmrun(['CopyFileFromGuestToHost',VMX,guest_out,local_guest],guest=True)
        report['guest']=json.loads(local_guest.read_bytes());report['verification']=verify(report)
        if report['implementations']!=[identity(p)for p in paths]or report['guest_executable']!=identity(exe):
            raise ValueError('preflight implementations must stay frozen during execution')
    except Exception as e:report.pop('verification',None);report['verification_error']=str(e)
    output.write_text(json.dumps(report,indent=2),encoding='utf8');return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--label',required=True);a=p.parse_args()
    r=run(a.label);print(json.dumps({k:r[k]for k in ('verification','verification_error')if k in r}))
    if 'verification_error'in r:raise SystemExit(1)
