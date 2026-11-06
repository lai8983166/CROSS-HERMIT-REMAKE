"""Retain the existing idle guard, excluding only this proven observer chain."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from devtools.reverse_iteration import BUSY_SCRIPT


def other_processes(rows, pid, parent_pid, executable):
    current = next((r for r in rows if r['ProcessId'] == pid),None)
    excluded = {pid}
    if current:
        def arguments(command):
            match = re.match(r'^(?:"[^"]+"|\S+)\s+(.*)$',command or '')
            return match.group(1) if match else None
        parent = next((r for r in rows if r['ProcessId'] == parent_pid),None)
        if (parent and current.get('ParentProcessId') == parent_pid
                and parent.get('ExecutablePath')
                and Path(parent['ExecutablePath']).resolve() == Path(executable).resolve()
                and arguments(current.get('CommandLine')) is not None
                and arguments(parent.get('CommandLine')) == arguments(current.get('CommandLine'))):
            # Windows venv redirector and its real Python interpreter share argv.
            excluded.add(parent_pid)
    return [r for r in rows if r['ProcessId'] not in excluded]


def require_idle():
    if sys.platform != 'win32':
        raise RuntimeError('native observer requires Windows inventory')
    script = BUSY_SCRIPT.replace('Select-Object ProcessId,Name',
        'Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine')
    result = subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],
                            capture_output=True,text=True,timeout=15,check=True)
    rows = json.loads(result.stdout)
    if not isinstance(rows,list):
        raise RuntimeError('invalid inventory; refusing native launch')
    others = other_processes(rows,os.getpid(),os.getppid(),sys.executable)
    if others:
        raise RuntimeError('reverse work is active; no task started or stopped: '+
                           json.dumps([dict(pid=r['ProcessId'],name=r['Name']) for r in others]))
