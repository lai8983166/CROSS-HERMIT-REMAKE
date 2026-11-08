"""Bounded headless boot observation; stop this owned test VM on a bugcheck."""
import argparse
import json
import time
from devtools.isolated_windows_vm import WORKER, VMX, identity, validate_vmx, validate_disk, vmrun


def watch(label, seconds=600):
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('simple unique label')
    if not 30 <= seconds <= 1200:
        raise ValueError('bounded guest boot observation')
    output = WORKER / ('boot-' + label + '.json')
    if output.exists():
        raise ValueError('new observation required')
    validate_vmx(VMX.read_text(encoding='utf8'))
    validate_disk(WORKER / 'worker.vmdk')
    if str(VMX).lower() in vmrun(['list']).lower():
        raise ValueError('start only the stopped owned worker')
    report = dict(schema_version=1, accepted=False, vmx_before=identity(VMX),
                  start_mode='nogui', host_input_actions=0, states=[], bugcheck_lines=[])
    started = time.monotonic()
    recovery_attempted = False
    try:
        vmrun(['start', VMX, 'nogui'])
        while time.monotonic() - started < seconds:
            # VMware rotates vmware.log at power-on; this file belongs to this boot.
            log = WORKER / 'vmware.log'
            lines = log.read_text(encoding='utf8', errors='replace').splitlines()
            errors = [line for line in lines if 'WinBSOD:' in line]
            if errors:
                report['bugcheck_lines'] = errors
                report['stop_reason'] = 'guest_bugcheck'
                break
            try:
                state = vmrun(['checkToolsState', VMX], timeout=15)
            except RuntimeError as exc:
                state = str(exc)
            if not report['states'] or state != report['states'][-1]['state']:
                report['states'].append(dict(state=state, elapsed_seconds=round(time.monotonic()-started, 3)))
                print(json.dumps(report['states'][-1]), flush=True)
            if state.strip() == 'running':
                report['stop_reason'] = 'tools_running_not_yet_qualified'
                break
            if state.strip() == 'installed' and time.monotonic()-started >= 30:
                try:
                    processes = vmrun(['listProcessesInGuest', VMX], guest=True, timeout=15)
                    if not processes.startswith('Process list:'):
                        raise RuntimeError('unexpected authenticated Tools response')
                    report['authenticated_tools_rpc_succeeded'] = True
                    report['stop_reason'] = 'tools_running_not_yet_qualified'
                    break
                except RuntimeError as exc:
                    report['last_tools_rpc_error'] = str(exc)
                if not recovery_attempted and time.monotonic()-started >= 45:
                    recovery_attempted = True
                    from devtools.isolated_vm_guest_admin import run_script, STATUS
                    report['guest_recovery_implementation'] = identity(WORKER.parents[1] / 'devtools/isolated_vm_guest_admin.py')
                    try:
                        # A dedicated fresh boot only; never restart Tools during a game run.
                        service = "$s=Get-Service VMTools;$s.Stop();$s.WaitForStatus('Stopped',[TimeSpan]::FromSeconds(15));$s.Start();$s.WaitForStatus('Running',[TimeSpan]::FromSeconds(15));"
                        report['one_guest_tools_restart'] = json.loads(run_script(service + STATUS))
                    except Exception as exc:
                        report['guest_recovery_error'] = str(exc)
            time.sleep(5)
        else:
            report['stop_reason'] = 'boot_deadline'
    except Exception as exc:
        report['error'] = str(exc)
    finally:
        report['elapsed_seconds'] = round(time.monotonic()-started, 3)
        report['cleanup_errors'] = []
        if report.get('stop_reason') != 'tools_running_not_yet_qualified':
            # No accepted game/source exists in this new installation. Avoid reboot loops.
            running = True
            try:
                running = str(VMX).lower() in vmrun(['list']).lower()
            except Exception as exc:
                report['cleanup_errors'].append('query: ' + str(exc))
            if running:
                try:
                    report['owned_power_off'] = vmrun(['stop', VMX, 'hard'])
                except Exception as exc:
                    report['cleanup_errors'].append('owned power off: ' + str(exc))
        for key, operation in (('running_vms_after', lambda: vmrun(['list'])),
                               ('vmx_after', lambda: identity(VMX)),
                               ('log', lambda: identity(WORKER / 'vmware.log'))):
            try:
                report[key] = operation()
            except Exception as exc:
                report['cleanup_errors'].append(key + ': ' + str(exc))
        with output.open('x', encoding='utf8') as stream:
            json.dump(report, stream, indent=2)
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--label', required=True)
    p.add_argument('--seconds', type=int, default=600)
    args = p.parse_args()
    result = watch(args.label, args.seconds)
    print(json.dumps({k: result[k] for k in ('stop_reason', 'error', 'elapsed_seconds') if k in result}))
    if result.get('stop_reason') != 'tools_running_not_yet_qualified':
        raise SystemExit(1)
