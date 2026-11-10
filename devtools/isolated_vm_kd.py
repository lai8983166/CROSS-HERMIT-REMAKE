"""Owned virtual serial KD channel, never a physical host serial device.

Adds a narrowly validated virtual named-pipe endpoint to the dedicated F: VM.
Only the guest boot configuration may be changed; the host BCD/Hyper-V/VBS
configuration is never accessed for mutation. This is not game qualification.
"""
from pathlib import Path
from devtools.isolated_windows_vm import WORKER,VMX,validate_vmx

PIPE = r'\\.\pipe\chaomofa-kd-e6d84d56'
SETTINGS = {'serial0.present':'TRUE','serial0.fileType':'pipe','serial0.fileName':PIPE,
            'serial0.pipe.endPoint':'server','serial0.startConnected':'TRUE',
            'serial0.tryNoRxLoss':'FALSE','serial0.yieldOnMsrRead':'TRUE'}


def validate_kd_vmx(text):
    serial={};base=[]
    for line in text.splitlines(keepends=True):
        key=line.split('=',1)[0].strip()
        if key.startswith('serial'):
            if key in serial or '=' not in line:raise ValueError('duplicate virtual serial setting')
            serial[key]=line.split('=',1)[1].strip().strip('"')
        else:base.append(line)
    if serial!=SETTINGS:raise ValueError('only the exact owned virtual KD pipe is allowed')
    return validate_vmx(''.join(base))


def run_guest(script):
    """Reuse authenticated encrypted administration with the narrow VMX profile.

    The parent function's globals are cloned, never patched in a running module.
    The original UUID/MAC/computer/manufacturer/NTLM guards remain unchanged.
    """
    import types
    from devtools.isolated_vm_guest_admin import run_script
    scope=dict(run_script.__globals__,validate_vmx=validate_kd_vmx)
    call=types.FunctionType(run_script.__code__,scope,run_script.__name__,run_script.__defaults__,run_script.__closure__)
    return call(script)
