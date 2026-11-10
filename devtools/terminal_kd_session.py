"""Bounded SDK KD stdin/stdout session for the dedicated virtual serial pipe.

No host keyboard input, local kernel attach, software breakpoint or memory write.
Prompt/continue are separate states; an echo before `g` never proves continuation.
"""
import ctypes as C
import re
import subprocess
import time
from pathlib import Path
from devtools.isolated_windows_vm import WORKER, VMX, environment, identity
from devtools.isolated_vm_kd import PIPE, validate_kd_vmx

SDK = Path('C:/Program Files (x86)/Windows Kits/10/Debuggers/x64/kd.exe')


def need(value, message):
    if not value:
        raise ValueError(message)


def at_prompt(text):
    return re.search(r'(?:^|\n)[0-9]+: kd>\s*\Z', text) is not None


def pending_debug_break(text):
    # Only an explicitly reported kernel debugger break, never an arbitrary #DB.
    return at_prompt(text) and bool(re.search(
        r'nt!DbgBreakPointWithStatus(?:\+0x1)?:\s*\n[0-9a-f`]+\s+(?:cc\s+int\s+3|c3\s+ret)', text))


def pipe_owner():
    k=C.WinDLL('kernel32',use_last_error=True)
    k.CreateFileW.argtypes=[C.c_wchar_p,C.c_ulong,C.c_ulong,C.c_void_p,C.c_ulong,C.c_ulong,C.c_void_p];k.CreateFileW.restype=C.c_void_p
    k.GetNamedPipeServerProcessId.argtypes=[C.c_void_p,C.POINTER(C.c_ulong)];k.GetNamedPipeServerProcessId.restype=C.c_int
    k.CloseHandle.argtypes=[C.c_void_p];k.CloseHandle.restype=C.c_int
    h=k.CreateFileW(PIPE,0,0,None,3,0,None)
    need(h!=C.c_void_p(-1).value,'owned virtual pipe identity open')
    try:
        pid=C.c_ulong();need(k.GetNamedPipeServerProcessId(h,C.byref(pid)),'pipe owner query')
        log=(WORKER/'vmware.log').read_text(encoding='utf8')
        m=re.search(r'Log for VMware Workstation pid=(\d+)',log)
        need(m and int(m[1])==pid.value and 'Config file: '+str(VMX)in log,'actual owned VM pipe server')
        return pid.value
    finally:need(k.CloseHandle(h),'pipe identity handle cleanup')


class Session:
    def __init__(self, log):
        validate_kd_vmx(VMX.read_text(encoding='utf8'))
        self.log=Path(log);need(not self.log.exists(),'fresh debugger transcript')
        self.rows=[];self.sequence=0;self.pending_breaks=0;self.cursor=0
        self.server_pid=pipe_owner();self.client=identity(SDK)
        env=environment();env['_NT_SYMBOL_PATH']=str(WORKER/'symbols');env['_NT_ALT_SYMBOL_PATH']=''
        self.file=self.log.open('xb')
        self.process=subprocess.Popen([str(SDK),'-k','com:pipe,port='+PIPE+',resets=0,reconnect',
            '-bonc','-noshell','-sins','-y',str(WORKER/'symbols'),'-c','.echo OWNED_SESSION_INITIAL'],
            stdin=subprocess.PIPE,stdout=self.file,stderr=subprocess.STDOUT,
            cwd=WORKER,env=env,creationflags=subprocess.CREATE_NO_WINDOW)

    def text(self):
        need(self.log.stat().st_size<=1024*1024,'bounded SDK transcript')
        return self.log.read_text(encoding='utf8',errors='replace')

    def wait_prompt(self, seconds=10):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            text=self.text()
            if at_prompt(text):return text[self.cursor:]
            need(self.process.poll()is None,'SDK client exited')
            time.sleep(.02)
        raise TimeoutError('bounded debugger prompt')

    def send(self, command):
        self.rows.append(dict(command=command,monotonic=time.monotonic()))
        self.process.stdin.write((command+'\n').encode('ascii'));self.process.stdin.flush()

    def execute(self, command):
        allowed=command in ('lm m nt','r','bc *','bl','.lastevent','r dr0,dr1,dr2,dr3,dr6,dr7','r cr0,cr2,cr3,cr4')
        allowed |= bool(re.fullmatch(r'!process [0-9a-f]+ 2',command))
        allowed |= bool(re.fullmatch(r'(?:dq|db|u) [0-9a-f`]+ L[0-9a-f]{1,3}',command))
        allowed |= bool(re.fullmatch(r'\? @\$(?:tpid|tid|thread|proc|pcr)',command))
        allowed |= bool(re.fullmatch(r'ba e 1 /p ffff[0-9a-f`]+ /t ffff[0-9a-f`]+ ffff[0-9a-f`]+',command))
        need(allowed,'read-only query or scoped owned kernel hardware breakpoint')
        self.wait_prompt();self.sequence+=1;marker='OWNED_QUERY_END_'+str(self.sequence)
        start=len(self.text());self.send(command+';.echo '+marker)
        end=time.monotonic()+10
        while time.monotonic()<end:
            text=self.text();tail=text[start:]
            if re.search(r'^'+marker+r'\r?$',tail,re.M)and at_prompt(text):
                self.cursor=len(text)
                need(not re.search(r'(?i)(syntax error|numeric expression missing|could not resolve|unable to insert)',tail),'debugger command refused')
                return tail
            need(self.process.poll()is None,'SDK client exited during query');time.sleep(.02)
        raise TimeoutError('bounded debugger query')

    def go(self):
        self.wait_prompt();self.cursor=len(self.text());self.send('g')

    def poll_stop(self):
        text=self.text();tail=text[self.cursor:]
        if not at_prompt(text)or not tail.strip():return None
        if pending_debug_break(tail):
            need(self.pending_breaks<4,'bounded pending debugger break budget')
            event=self.execute('.lastevent')
            need('80000003'in event,'only the debugger-created break instruction is auto-continued')
            self.pending_breaks+=1;self.go();return None
        return tail

    def close_after_resume(self):
        # Caller must independently verify the guest response before this call.
        need(not at_prompt(self.text()),'do not terminate a paused debug session')
        self.process.terminate();self.process.wait(timeout=5);self.file.close()
