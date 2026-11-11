"""Single owned Windows wait preflight, durable receipts and bounded commands."""
import json
import subprocess
import sys
import time
from pathlib import Path
from devtools.terminal_tcg_wait_control_v6 import request
from devtools.isolated_vm_bounded_query_v3 import completed
from devtools.terminal_cr2_receipt_poll import poll

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / '.venv-audit/native-worker/tcg-wait-native-v9'


def save(name, value):
    with (CASE / name).open('x', encoding='utf8') as stream:
        json.dump(value, stream, indent=2)


def fast(module, name, output):
    process = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-m', module, name],
        cwd=ROOT, capture_output=True, timeout=45, creationflags=subprocess.CREATE_NO_WINDOW)
    value = json.loads(process.stdout)
    save(output, value)
    return value


def run():
    observer = None
    report = dict(accepted=False, errors=[], original_game=False)
    started = time.monotonic()
    try:
        while not (CASE / 'vm-ready.json').exists():
            if (CASE/'report.json').exists() or time.monotonic()-started > 210:
                raise TimeoutError('VM ready budget')
            time.sleep(.5)
        prepared = request(CASE, 'prepare.ps1', 'run')
        save('prepare-response.json', prepared)
        if not completed(prepared):
            prepared, _ = poll(lambda i: fast('devtools.terminal_tcg_context_wait_read_v2', 'prepare-receipt.json', 'prepare-durable-response-'+str(i)+'.json'), lambda v: v.get('prepared') is True, 150)
        if not completed(prepared) or prepared['response']['value'].get('prepared') is not True:
            raise ValueError('prepare not confirmed; no resubmission')
        save('boot-auth.json', prepared)
        launched = request(CASE, 'launch.ps1', 'run')
        save('launch-response.json', launched)
        if not completed(launched):
            launched, _ = poll(lambda i: fast('devtools.terminal_tcg_context_wait_read_v2', 'launch-receipt.json', 'launch-recovered-response-'+str(i)+'.json'), lambda v: v.get('launched') is True, 90)
        if not completed(launched) or not launched['response']['value'].get('launched'):
            raise ValueError('launch not confirmed; no relaunch')
        save('launch-auth.json', launched)
        ready, _ = poll(lambda i: fast('devtools.terminal_tcg_context_wait_read_v2', 'ready.json', 'read-ready-response-'+str(i)+'.json'), lambda v: v.get('pid') == launched['response']['value']['pid'], 120)
        if not completed(ready) or ready['response']['value'].get('pid') != launched['response']['value']['pid']:
            raise ValueError('ready current-owner mismatch')
        save('ready.json', ready['response']['value'])
        command = ['wsl.exe', '-d', 'Ubuntu', '--cd', '/mnt/f/project/chaomofa', '--',
            'python3', '-B', '-m', 'devtools.terminal_tcg_context_wait_observe_v1',
            '.venv-audit/native-worker/tcg-wait-native-v9', '.venv-audit/native-worker/tcg-wow64-path-v1/trace-plan.json']
        observer = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
        arm_start = time.monotonic()
        while not (CASE/'observer-armed.json').exists():
            if observer.poll() is not None or time.monotonic()-arm_start > 15:
                raise TimeoutError('observer setup')
            time.sleep(.1)
        gate = fast('devtools.terminal_tcg_context_wait_go_v2', 'ready.json', 'go-response.json')
        report['go_receipt_confirmed'] = completed(gate) and gate['response']['value'].get('go') is True
        # Never resend gate on a lost response; actual guest trace is separate evidence.
        stdout, stderr = observer.communicate(timeout=130)
        save('observer-process.json', dict(exit_code=observer.returncode, stdout=stdout.decode(errors='replace'), stderr=stderr.decode(errors='replace')))
        result = request(CASE, 'result.ps1', 'run')
        save('result-exit-response.json', result)
        report['result_receipt_confirmed'] = completed(result)
        observation = json.loads((CASE/'observation.json').read_bytes())
        report['ledger_verified'] = observation.get('ledger_verification', {}).get('cr2_chain_verified', False)
        report['observation_errors'] = observation['errors']
        from devtools.terminal_tcg_context_wait_verify_v2 import verify
        proof=verify(observation,json.loads((ROOT/'.venv-audit/native-worker/tcg-wow64-path-v1/trace-plan.json').read_bytes()))
        save('proof.json',proof)
        report['same_wait_writes_verified']=proof['same_wait_writes_verified']
    except Exception as exc:
        report['errors'].append(type(exc).__name__ + ': ' + str(exc))
    finally:
        if observer and observer.poll() is None:
            # VM lifetime supervisor remains the owner of the actual guest process.
            report['observer_still_running'] = True
        report['seconds'] = time.monotonic()-started
        save('orchestration.json', report)
        if not report.get('observer_still_running'):
            (CASE/'vm-stop').write_text('bounded preflight finished', encoding='utf8')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
