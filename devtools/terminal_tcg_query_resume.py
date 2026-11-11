"""Continue receiving one authenticated owned command; never resubmit it."""
import argparse,hashlib,json,re,sys
from pathlib import Path
from devtools.isolated_windows_vm import WORKER
from devtools.isolated_vm_bounded_query_v3 import _supervise,runtime_paths

def _worker():
    request=json.loads(sys.stdin.readline())
    try:
        if not re.fullmatch(r'phase-\d+\.json',request['phase']):raise ValueError('phase name')
        case=WORKER/'tcg-windows-control-v6'
        if not (case/'vm-ready.json').exists()or (case/'vm-stop').exists()or (case/'report.json').exists():raise ValueError('current lifetime required')
        path=WORKER/'tcg-control-evidence-v1'/request['phase'];raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=request['sha256']:raise ValueError('phase identity')
        rows=json.loads(raw)
        if [r['method']for r in rows]!=['open_shell','run_command','get_command_output'] or 'end'in rows[-1]:raise ValueError('owned pending receive required')
        ids=[rows[i]['owned_id']for i in (0,1)]
        if any(not re.fullmatch('[A-Fa-f0-9-]{36}',s)for s in ids):raise ValueError('owned ids')
        import winrm
        secret=json.loads((WORKER/'credentials.private.json').read_bytes())['password']
        protocol=winrm.Session('http://127.0.0.1:15985/wsman',auth=('CHAOMOFA-WORKER\\Administrator',secret),
            transport='ntlm',message_encryption='always',operation_timeout_sec=20,read_timeout_sec=30).protocol
        out,err,code=protocol.get_command_output(*ids)
        protocol.cleanup_command(*ids);protocol.close_shell(ids[0])
        if code:raise RuntimeError('owned command failed')
        result=dict(ok=True,value=json.loads(out.decode('utf8').replace(secret,'[redacted]')),
            remote_completion='observed',owned_command_cleanup=True,owned_shell_closed=True,command_resubmitted=False)
    except Exception as exc:result=dict(ok=False,error_type=type(exc).__name__,remote_completion='unknown',command_resubmitted=False)
    print(json.dumps(result),flush=True)

def resume(phase):
    raw=phase.read_bytes();payload=dict(phase=phase.name,sha256=hashlib.sha256(raw).hexdigest())
    code='import sys;sys.path[:0]='+repr(runtime_paths())+';from devtools.terminal_tcg_query_resume import _worker;_worker()'
    return _supervise(payload,55,code)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',type=Path);print(json.dumps(resume(p.parse_args().phase)))
