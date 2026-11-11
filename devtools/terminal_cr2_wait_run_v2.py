"""Single owned Windows wait preflight, durable receipts and bounded commands."""
import json
import subprocess
import sys
import time
from pathlib import Path
from devtools.terminal_tcg_wait_control_v6 import request
from devtools.isolated_vm_bounded_query_v3 import completed

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / '.venv-audit/native-worker/tcg-wait-native-v6'


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
            phases = list(CASE.glob('phase-prepare-*.json'))
            if len(phases) != 1:
                raise ValueError('ambiguous prepare ownership')
            prepared = request(CASE, phases[0].name, 'resume')
            save('prepare-resume-response.json', prepared)
        if not completed(prepared):
            raise ValueError('prepare not confirmed; no resubmission')
        save('boot-auth.json', prepared)
        launched = request(CASE, 'launch.ps1', 'run')
        save('launch-response.json', launched)
        if not completed(launched):
            launched = fast('devtools.terminal_cr2_wait_read_v2', 'launch-receipt.json', 'launch-recovered-response.json')
        if not completed(launched) or not launched['response']['value'].get('launched'):
            raise ValueError('launch not confirmed; no relaunch')
        save('launch-auth.json', launched)
        ready_started = time.monotonic()
        for attempt in range(4):
            ready = fast('devtools.terminal_cr2_wait_read_v2', 'ready.json', 'read-ready-response-'+str(attempt)+'.json')
            if completed(ready) and ready['response']['value'].get('pid') == launched['response']['value']['pid']:
                break
            if not completed(ready) or ready['response']['value'].get('file_present') is not False or time.monotonic()-ready_started >= 90:
                break
            time.sleep(2)
        if not completed(ready) or ready['response']['value'].get('pid') != launched['response']['value']['pid']:
            raise ValueError('ready current-owner mismatch')
        save('ready.json', ready['response']['value'])
        command = ['wsl.exe', '-d', 'Ubuntu', '--cd', '/mnt/f/project/chaomofa', '--',
            'python3', '-B', '-m', 'devtools.terminal_cr2_wait_observe',
            '.venv-audit/native-worker/tcg-wait-native-v6', '.venv-audit/native-worker/tcg-wait-native-v6/ready.json']
        observer = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
        arm_start = time.monotonic()
        while not (CASE/'observer-armed.json').exists():
            if observer.poll() is not None or time.monotonic()-arm_start > 15:
                raise TimeoutError('observer setup')
            time.sleep(.1)
        gate = fast('devtools.terminal_cr2_wait_go_v2', 'ready.json', 'go-response.json')
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
