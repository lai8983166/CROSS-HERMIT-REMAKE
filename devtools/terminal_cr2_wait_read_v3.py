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
        if case.name != 'tcg-wait-native-v7' or (case/'report.json').exists() or (case/'vm-stop').exists():
            raise ValueError('current owned boot required')
        name = req['name']
        if name == 'prepare-receipt.json':
            phases = list(case.glob('phase-prepare-*.json'))
            if len(phases) != 1:raise ValueError('owned prepare command required')
            phase = json.loads(phases[0].read_bytes())
            if len(phase) < 2 or not all(phase[i].get('owned_id') for i in (0,1)):
                raise ValueError('prepare dispatch unconfirmed')
        else:
            launch = json.loads((case/'boot-auth.json').read_bytes())
            if not launch['response']['ok'] or launch['response']['value']['uuid'].lower() != '626d1a20-6383-4cd3-85d5-6c9831d6f941':
                raise ValueError('authenticated boot required')
        if name not in ('ready.json', 'result.json', 'launch-receipt.json', 'prepare-receipt.json'):
            raise ValueError('fixed owned JSON only')
        import winrm
        secret = json.loads((WORKER/'credentials.private.json').read_bytes())['password']
        p = winrm.Session('http://127.0.0.1:15985/wsman', auth=('CHAOMOFA-WORKER\\Administrator', secret),
                         transport='ntlm', message_encryption='always', operation_timeout_sec=10, read_timeout_sec=20).protocol
        shell = p.open_shell()
        command = p.run_command(shell, 'cmd.exe', ['/d','/c','type', 'C:\\ChaomofaWorker\\'+case.name+'\\'+name])
        out, err, code = receive(p, case, shell, command)
        p.cleanup_command(shell, command); p.close_shell(shell)
        if code:
            print(json.dumps(dict(ok=True,value=dict(file_present=False,status_code=code),command_and_shell_closed=True,remote_completion='observed')));return
        value=json.loads(out.decode('utf-8-sig'))
        if name == 'prepare-receipt.json' and (value.get('prepared') is not True or value.get('uuid','').lower() != '626d1a20-6383-4cd3-85d5-6c9831d6f941' or value.get('directory') != 'C:/ChaomofaWorker/tcg-wait-native-v7'):
            raise ValueError('durable authenticated prepare receipt')
        print(json.dumps(dict(ok=True,value=value,command_and_shell_closed=True,remote_completion='observed')))
    except Exception as exc:
        print(json.dumps(dict(ok=False, error_type=type(exc).__name__)))


if __name__ == '__main__':
    bootstrap = 'import sys;sys.path[:0]='+repr(runtime_paths())+';from devtools.terminal_cr2_wait_read_v3 import worker;worker()'
    print(json.dumps(_supervise(dict(case='tcg-wait-native-v7',name=sys.argv[1]),35,bootstrap)))
