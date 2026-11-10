"""SDK session with optional passive connection to avoid hiding a prior stop."""
import subprocess
from pathlib import Path
from devtools.terminal_kd_session import Session as Prior,SDK,pipe_owner,need
from devtools.isolated_windows_vm import WORKER,VMX,environment,identity
from devtools.isolated_vm_kd import PIPE,validate_kd_vmx


class Session(Prior):
    def __init__(self,log,*,break_on_connect=True):
        validate_kd_vmx(VMX.read_text(encoding='utf8'))
        self.log=Path(log);need(not self.log.exists(),'fresh debugger transcript')
        self.rows=[];self.sequence=0;self.pending_breaks=0;self.cursor=0
        self.server_pid=pipe_owner();self.client=identity(SDK)
        env=environment();env['_NT_SYMBOL_PATH']=str(WORKER/'symbols');env['_NT_ALT_SYMBOL_PATH']=''
        self.file=self.log.open('xb')
        args=[str(SDK),'-k','com:pipe,port='+PIPE+',resets=0,reconnect']
        if break_on_connect:args+=['-bonc']
        args+=['-noshell','-sins','-y',str(WERK if False else WORKER/'symbols'),'-c','.echo OWNED_SESSION_INITIAL']
        self.process=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=self.file,stderr=subprocess.STDOUT,cwd=WORKER,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
