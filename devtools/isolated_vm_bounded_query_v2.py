"""Read-only guest queries with a host deadline independent of WinRM retries.

The disposable host Python and its descendants belong to a private kill-on-close
Job. A host timeout does NOT assert that the remote PowerShell command stopped.
No game launch, mutation, debugger connection or host input is exposed here.
"""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from devtools.isolated_windows_vm import ROOT,WORKER,VMX,environment,validate_vmx

MAX_OUTPUT=2*1024*1024


class BasicLimit(C.Structure):
    _fields_=[('per_process',C.c_longlong),('per_job',C.c_longlong),('flags',W.DWORD),
              ('min_ws',C.c_size_t),('max_ws',C.c_size_t),('active_limit',W.DWORD),
              ('affinity',C.c_size_t),('priority',W.DWORD),('scheduling',W.DWORD)]


class IoCounters(C.Structure):
    _fields_=[(name,C.c_ulonglong)for name in ('ro','wo','oo','rb','wb','ob')]


class ExtendedLimit(C.Structure):
    _fields_=[('basic',BasicLimit),('io',IoCounters),('process_memory',C.c_size_t),
              ('job_memory',C.c_size_t),('peak_process',C.c_size_t),('peak_job',C.c_size_t)]


class Accounting(C.Structure):
    _fields_=[('user',C.c_longlong),('kernel',C.c_longlong),('period_user',C.c_longlong),
              ('period_kernel',C.c_longlong),('faults',W.DWORD),('total',W.DWORD),
              ('active',W.DWORD),('terminated',W.DWORD)]


class Job:
    def __init__(self):
        k=self.k=C.WinDLL('kernel32',use_last_error=True)
        for name,result,args in (
            ('CreateJobObjectW',W.HANDLE,[C.c_void_p,W.LPCWSTR]),
            ('SetInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD]),
            ('AssignProcessToJobObject',W.BOOL,[W.HANDLE,W.HANDLE]),
            ('TerminateJobObject',W.BOOL,[W.HANDLE,W.UINT]),
            ('QueryInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p]),
            ('CloseHandle',W.BOOL,[W.HANDLE])):
            f=getattr(k,name);f.restype=result;f.argtypes=args
        self.handle=k.CreateJobObjectW(None,None)
        if not self.handle:raise C.WinError(C.get_last_error())
        limits=ExtendedLimit();limits.basic.flags=0x2000  # KILL_ON_JOB_CLOSE
        if not k.SetInformationJobObject(self.handle,9,C.byref(limits),C.sizeof(limits)):
            error=C.get_last_error();k.CloseHandle(self.handle);self.handle=None;raise C.WinError(error)

    def assign(self,process):
        if not self.k.AssignProcessToJobObject(self.handle,int(process._handle)):
            raise C.WinError(C.get_last_error())

    def active(self):
        a=Accounting()
        if not self.k.QueryInformationJobObject(self.handle,1,C.byref(a),C.sizeof(a),None):
            raise C.WinError(C.get_last_error())
        return a.active

    def terminate(self):
        if not self.k.TerminateJobObject(self.handle,124):raise C.WinError(C.get_last_error())

    def close(self):
        if self.handle:
            if not self.k.CloseHandle(self.handle):raise C.WinError(C.get_last_error())
            self.handle=None


def runtime_paths():
    # Preserve installed dependency resolution, without executing site/.pth hooks.
    return [str(ROOT)]+[str(Path(p).resolve())for p in sys.path if p and Path(p).is_absolute()]


def request_script(action,argument=None):
    if action=='status' and argument is None:
        from devtools.isolated_vm_guest_admin import STATUS
        return STATUS
    if action=='sleep_echo' and type(argument)is int and 1<=argument<=15:
        return "Start-Sleep -Seconds %d;'bounded-query-finished'"%argument
    if action=='read_text' and isinstance(argument,str) and len(argument)<=256 and re.fullmatch(
            r'(?:kd-[a-z0-9-]+|vm-[a-z0-9-]+)/[a-z0-9-]+\.json',argument):
        path='C:/ChaomofaWorker/'+argument
        return ("$p='"+path+"';if(!(Test-Path -LiteralPath $p)){'NOT_READY'}else{"
                "if((Get-Item -LiteralPath $p).Length -gt 1048576){throw 'read budget'};[IO.File]::ReadAllText($p)}")
    raise ValueError('only bounded read-only owned guest queries')


def validate_profile(profile):
    if profile=='normal':return validate_vmx(VMX.read_text(encoding='utf8'))
    if profile=='kd':
        from devtools.isolated_vm_kd import validate_kd_vmx
        return validate_kd_vmx(VMX.read_text(encoding='utf8'))
    raise ValueError('explicit owned VM profile required')


def _worker():
    # Parent sends this line only AFTER assigning this direct interpreter to Job.
    request=json.loads(sys.stdin.readline())
    try:
        script=request_script(request['action'],request['argument'])
        validate_profile(request['profile'])
        if request['profile']=='kd':
            from devtools.isolated_vm_kd import run_guest as run
        else:
            from devtools.isolated_vm_guest_admin import run_script as run
        value=run(script)
        result=dict(ok=True,value=value,remote_completion='observed')
    except Exception as exc:
        # Never return arbitrary exception messages or credentials from transport.
        result=dict(ok=False,error_type=type(exc).__name__,remote_completion='unknown')
    print(json.dumps(result),flush=True)


def _supervise(payload,seconds,bootstrap=None):
    if not isinstance(seconds,(int,float))or not 0.1<=seconds<=60:raise ValueError('bounded host deadline')
    wire=(json.dumps(payload)+'\n').encode()
    if len(wire)>1024:raise ValueError('bounded request before child creation')
    started=time.monotonic();deadline=started+seconds
    env=environment();job=Job();process=None
    report=dict(deadline_seconds=seconds,host_input_actions=0,remote_completion='unknown',errors=[])
    # Direct base interpreter, -S/-I: no venv launcher child or site startup hooks.
    base=Path(sys._base_executable).resolve()
    code=bootstrap or ('import sys;sys.path[:0]='+repr(runtime_paths())+
                       ';from devtools.isolated_vm_bounded_query_v2 import _worker;_worker()')
    try:
        with tempfile.TemporaryFile(dir=WORKER/'tmp')as output:
            process=subprocess.Popen([str(base),'-I','-S','-B','-X','utf8','-c',code],stdin=subprocess.PIPE,
                stdout=output,stderr=output,cwd=WORKER,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
            report['host_pid']=process.pid
            job.assign(process);report['assigned_before_request']=True
            process.stdin.write(wire);process.stdin.close()
            while process.poll()is None:
                if time.monotonic()>=deadline:
                    report['timed_out']=True;job.terminate();break
                output.seek(0,2)
                if output.tell()>MAX_OUTPUT:
                    report['errors'].append('output budget');job.terminate();break
                time.sleep(min(.02,max(0,deadline-time.monotonic())))
            if time.monotonic()>=deadline:
                report['timed_out']=True
                if process.poll() is None:job.terminate()
            # Cleanup budget is explicit and separate from the operation deadline.
            process.wait(timeout=2)
            if job.active():job.terminate()
            cleanup_end=time.monotonic()+2
            while job.active() and time.monotonic()<cleanup_end:time.sleep(.01)
            report['host_job_active_after']=job.active()
            if report['host_job_active_after']:report['errors'].append('host descendants remain')
            report['host_exit_code']=process.returncode
            output.seek(0,2);length=output.tell();report['output_bytes']=length
            if not report.get('timed_out') and not report['errors'] and length<=MAX_OUTPUT:
                output.seek(0)
                try:report['response']=json.loads(output.read().decode('utf8'))
                except (ValueError,UnicodeError):report['errors'].append('invalid worker response')
                else:report['remote_completion']=report['response'].get('remote_completion','unknown')
            elif length>MAX_OUTPUT and 'output budget' not in report['errors']:report['errors'].append('output budget')
    except Exception as exc:
        report['errors'].append('host supervision: '+type(exc).__name__)
    finally:
        # Close kills only this private Job. No existing host or guest task is killed.
        job.close()
        if process and process.poll()is None:
            process.kill();process.wait(timeout=2)
        report['elapsed_seconds']=time.monotonic()-started
    return report


def query(action,argument=None,*,seconds=15,profile='normal'):
    request_script(action,argument);validate_profile(profile)
    return _supervise(dict(action=action,argument=argument,profile=profile),seconds)
