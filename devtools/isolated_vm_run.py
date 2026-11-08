"""Run one bounded guest-only observation and retrieve its report, without UI."""
import argparse
import json
from pathlib import PureWindowsPath
import re
from devtools.isolated_windows_vm import ROOT, WORKER, VMX, identity, vmrun
from devtools.isolated_vm_guest_admin import run_script

OVERLAY = ('isolated_game_compat.py', 'isolated_guest_focus.py', 'isolated_guest_dep_observer.py',
           'native_input_isolation.py','terminal_input_window.py','terminal_school_handoff.py',
           'terminal_school_handoff_verification.py')


def run(kind, label):
    if kind not in ('compat', 'school') or not re.fullmatch('[a-z0-9-]+', label):
        raise ValueError('explicit bounded observation and unique simple label required')
    stem = ('isolated-game-compat-' if kind == 'compat' else 'terminal-school-handoff-') + label
    output = WORKER / (stem + '.json.gz')
    receipt = WORKER / (stem + '.run.json')
    if output.exists() or receipt.exists():
        raise ValueError('never overwrite an existing observation')
    guest_root = PureWindowsPath('C:/ChaomofaWorker/project')
    guest_output = guest_root / 'analysis' / output.name
    # Stop before deploying any source if an earlier guest acquisition is active.
    guard = """$busy=@(Get-CimInstance Win32_Process | Where-Object {
        $_.Name -eq 'CROSS HERMIT.EXE' -or $_.ExecutablePath -like 'C:\\ChaomofaWorker\\Python\\python*.exe'});
        if($busy.Count){throw 'Existing guest acquisition must finish before source deployment'};
        'idle'"""
    if run_script(guard).strip() != 'idle':
        raise ValueError('guest idle guard did not complete')
    sources = [ROOT / 'devtools' / name for name in OVERLAY]
    before = [identity(p) for p in sources]
    for path in sources:
        vmrun(['CopyFileFromHostToGuest', VMX, path, guest_root / 'devtools' / path.name], guest=True)
    module = 'devtools.isolated_game_compat' if kind == 'compat' else 'devtools.terminal_school_handoff'
    argv = [module, '--out', str(guest_output)]
    if kind == 'school':
        argv += ['--seconds', '1800']
    launcher = WORKER / (stem + '-driver.py')
    guest_launcher = PureWindowsPath('C:/ChaomofaWorker') / launcher.name
    guest_log = PureWindowsPath('C:/ChaomofaWorker') / (stem + '.log')
    script = ('import os,sys,runpy,traceback\n'
              'os.chdir(' + repr(str(guest_root)) + ');sys.path.insert(0,' + repr(str(guest_root)) + ')\n'
              'sys.argv=' + repr(argv) + '\n'
              'with open(' + repr(str(guest_log)) + ',"x",encoding="utf8") as log:\n'
              ' sys.stdout=sys.stderr=log\n'
              ' try:runpy.run_module(' + repr(module) + ',run_name="__main__")\n'
              ' except BaseException:traceback.print_exc();raise\n')
    with launcher.open('x', encoding='utf8') as stream:
        stream.write(script)
    report = dict(module=module, sources=before, launcher=identity(launcher),
                  host_input_actions=0, accepted=False, errors=[])
    try:
        vmrun(['CopyFileFromHostToGuest', VMX, launcher, guest_launcher], guest=True)
        vmrun(['runProgramInGuest', VMX, '-activeWindow', '-interactive',
               PureWindowsPath('C:/ChaomofaWorker/Python/pythonw.exe'), '-B', guest_launcher],
              guest=True, timeout=240 if kind == 'compat' else 2400)
    except Exception as exc:
        report['errors'].append(str(exc))
    finally:
        for guest, local in ((guest_output, output), (guest_log, WORKER / guest_log.name)):
            try:
                vmrun(['CopyFileFromGuestToHost', VMX, guest, local], guest=True)
                report.setdefault('retrieved', []).append(identity(local))
            except Exception as exc:
                report['errors'].append(str(exc))
        report['sources_unchanged'] = before == [identity(p) for p in sources]
        with receipt.open('x', encoding='utf8') as stream:
            json.dump(report, stream, indent=2)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['compat', 'school'])
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    result = run(args.kind, args.label)
    print(json.dumps(result, indent=2))
    if result['errors'] or not result['sources_unchanged']:
        raise SystemExit(1)
