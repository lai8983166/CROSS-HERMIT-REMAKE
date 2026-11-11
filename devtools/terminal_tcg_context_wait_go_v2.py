"""Bounded read-only file retrieval from this boot's already authenticated fixture."""
import json
import sys
from pathlib import Path
from devtools.isolated_windows_vm import WORKER
from devtools.isolated_vm_bounded_query_v3 import _supervise, runtime_paths
from devtools.terminal_winrm_output_v2 import receive


def worker():
    req = json.loads(sys.stdin.readline())
    try:
        case = WORKER / req['case']
        if case.name != 'tcg-wait-native-v9' or (case/'report.json').exists() or (case/'vm-stop').exists():
            raise ValueError('current owned boot required')
        launch = json.loads((case/'launch-auth.json').read_bytes())
        if not launch['response']['ok'] or launch['response']['value']['uuid'].lower() != '626d1a20-6383-4cd3-85d5-6c9831d6f941':
            raise ValueError('authenticated boot launch required')
        if not (case/'observer-armed.json').exists():raise ValueError('observer required')
        name = req['name']
        if name not in ('ready.json', 'result.json', 'launch-receipt.json'):
            raise ValueError('fixed owned JSON only')
        import winrm
        secret = json.loads((WORKER/'credentials.private.json').read_bytes())['password']
        p = winrm.Session('http://127.0.0.1:15985/wsman', auth=('CHAOMOFA-WORKER\\Administrator', secret),
                         transport='ntlm', message_encryption='always', operation_timeout_sec=10, read_timeout_sec=20).protocol
        shell = p.open_shell()
        command = p.run_command(shell,'powershell.exe',['-NoProfile','-NonInteractive','-EncodedCommand','JABwAD0AJwBDADoALwBDAGgAYQBvAG0AbwBmAGEAVwBvAHIAawBlAHIALwB0AGMAZwAtAHcAYQBpAHQALQBuAGEAdABpAHYAZQAtAHYAOQAvAGcAbwAnADsAaQBmACgAVABlAHMAdAAtAFAAYQB0AGgAIAAkAHAAKQB7AGUAeABpAHQAIAAzAH0AOwBbAEkATwAuAEYAaQBsAGUAXQA6ADoAVwByAGkAdABlAEEAbABsAFQAZQB4AHQAKAAkAHAALAAnAGcAbwAnACkAOwAnAHsAIgBnAG8AIgA6AHQAcgB1AGUAfQAnAA=='])
        out, err, code = receive(p, case, shell, command)
        p.cleanup_command(shell, command); p.close_shell(shell)
        if code:
            raise ValueError('file read failed')
        print(json.dumps(dict(ok=True, value=json.loads(out.decode('utf-8-sig')), command_and_shell_closed=True,remote_completion="observed")))
    except Exception as exc:
        print(json.dumps(dict(ok=False, error_type=type(exc).__name__)))


if __name__ == '__main__':
    bootstrap = 'import sys;sys.path[:0]='+repr(runtime_paths())+';from devtools.terminal_tcg_context_wait_go_v2 import worker;worker()'
    print(json.dumps(_supervise(dict(case='tcg-wait-native-v9',name=sys.argv[1]),35,bootstrap)))
