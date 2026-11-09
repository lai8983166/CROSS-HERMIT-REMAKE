"""Resume offline original-wait decoding in the qualified guest; no game launch."""
import argparse
import gzip
import json
from pathlib import PureWindowsPath
import re

from devtools.isolated_windows_vm import ROOT, WORKER, VMX, vmrun, identity
from devtools.isolated_vm_guest_admin import run_script


def require_label(value):
    if not re.fullmatch('[a-z0-9-]+', value):
        raise ValueError('simple unique lowercase label required')
    return value


def checked_artifact(row, expected, maximum):
    if (PureWindowsPath(row['path']) != expected
            or not 0 < row['bytes'] <= maximum
            or not re.fullmatch('[0-9a-f]{64}', row['sha256'])):
        raise ValueError('exact bounded guest artifact identity required')


def transferred(row, local):
    got = identity(local)
    if (got['bytes'], got['sha256']) != (row['bytes'], row['sha256']):
        raise ValueError('transferred artifact identity mismatch')
    return got


def restore_guest_artifact(local, remote, expected):
    """Restore a retired transfer copy, never overwrite a different guest file."""
    base = PureWindowsPath('C:/ChaomofaWorker/project/analysis')
    remote = PureWindowsPath(remote)
    if not remote.is_relative_to(base) or '..' in remote.parts:
        raise ValueError('guest analysis artifact path required')
    literal = str(remote).replace("'", "''")
    inspect = ("$p='" + literal + "';if(Test-Path -LiteralPath $p){"
               "[pscustomobject]@{exists=$true;bytes=(Get-Item -LiteralPath $p).Length;"
               "sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()}"
               "|ConvertTo-Json -Compress}else{'{\"exists\":false}'}")
    state = json.loads(run_script(inspect))
    restored = not state['exists']
    if restored:
        parent = str(remote.parent).replace("'", "''")
        run_script("$p='" + parent + "';if(!(Test-Path -LiteralPath $p)){"
                   "New-Item -ItemType Directory -Path $p -ErrorAction Stop|Out-Null};'ready'")
        # The idle guest and single scheduler contract prevents concurrent writers.
        # Recheck source bytes immediately before transfer and guest bytes after it.
        transferred(expected, local)
        vmrun(['CopyFileFromHostToGuest', VMX, local, remote], guest=True)
        state = json.loads(run_script(inspect))
    if not state.get('exists') or any(state.get(k) != expected[k] for k in ('bytes', 'sha256')):
        raise ValueError('existing or restored guest artifact identity mismatch; never overwrite')
    return dict(path=str(remote), restored=restored, bytes=state['bytes'], sha256=state['sha256'])


def decode(label, source_label, diagnostic_only=False):
    stem = 'terminal-original-wait-decode-' + require_label(label)
    source_stem = 'terminal-original-wait-' + require_label(source_label)
    output = WORKER / (stem + '.json')
    receipt = WORKER / (stem + '.run.json')
    records = WORKER / (stem + '.records.json.gz')
    driver = WORKER / (stem + '-driver.py')
    log_local = WORKER / (stem + '.log')
    if any(p.exists() for p in (output, receipt, records, driver, log_local)):
        raise ValueError('immutable fresh decoder outputs required')
    source_path = WORKER / (source_stem + '.json.gz')
    etl_path = WORKER / source_stem / 'trace.etl'
    sid, eid = identity(source_path), identity(etl_path)
    if sid['bytes'] > 2 * 1024 * 1024 or not 0 < eid['bytes'] < 4 * 1024 * 1024:
        raise ValueError('bounded existing source and ETL required')
    # The independent guest decoder checks decompression, source semantics and
    # current guest identity. This host guard also binds the ETL to the source.
    with gzip.open(source_path, 'rb') as f:
        raw = f.read(2 * 1024 * 1024 + 1)
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError('bounded decompressed source required')
    source = json.loads(raw)
    guest = PureWindowsPath('C:/ChaomofaWorker/project')
    checked_artifact(source['ETL'], guest / 'analysis' / source_stem / 'trace.etl', 4 * 1024 * 1024)
    transferred(source['ETL'], etl_path)
    idle = "$p=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'CROSS HERMIT.EXE' -or $_.Name -like 'python*'});if($p.Count){throw 'guest busy'};'idle'"
    if run_script(idle).strip() != 'idle':
        raise ValueError('guest not idle before offline decoder deployment')
    guest_inputs = [restore_guest_artifact(source_path, guest / 'analysis' / source_path.name, sid),
                    restore_guest_artifact(etl_path, guest / 'analysis' / source_stem / 'trace.etl', eid)]
    modules = [ROOT / 'devtools' / name for name in
               ('terminal_original_wait_etw_verification.py', 'terminal_wait_native_verification.py')]
    before = [identity(p) for p in modules]
    args = ['devtools.terminal_original_wait_etw_verification',
            '--source', str(guest / 'analysis' / source_path.name), '--source-sha', sid['sha256'],
            '--etl', str(guest / 'analysis' / source_stem / 'trace.etl'), '--etl-sha', eid['sha256'],
            '--out', str(guest / 'analysis' / output.name)]
    if diagnostic_only:
        args.append('--diagnostic-only')
    log = PureWindowsPath('C:/ChaomofaWorker') / log_local.name
    remote_driver = log.parent / driver.name
    script = ('import os,sys,runpy,traceback\nos.chdir(' + repr(str(guest))
              + ');sys.path.insert(0,' + repr(str(guest)) + ')\nsys.argv=' + repr(args)
              + '\nwith open(' + repr(str(log)) + ',"x",encoding="utf8")as f:\n'
                ' sys.stdout=sys.stderr=f\n'
                ' try:runpy.run_module("devtools.terminal_original_wait_etw_verification",run_name="__main__")\n'
                ' except BaseException:traceback.print_exc();raise\n')
    with driver.open('x', encoding='utf8') as f:
        f.write(script)
    result = dict(implementations=before, driver=identity(driver), source=sid, ETL=eid,
                  accepted=False, new_capture=False, host_input_actions=0,
                  diagnostic_only=diagnostic_only, guest_inputs=guest_inputs, errors=[])
    try:
        for p in modules:
            vmrun(['CopyFileFromHostToGuest', VMX, p, guest / 'devtools' / p.name], guest=True)
        vmrun(['CopyFileFromHostToGuest', VMX, driver, remote_driver], guest=True)
        vmrun(['runProgramInGuest', VMX, '-activeWindow', '-interactive',
               PureWindowsPath('C:/ChaomofaWorker/Python/pythonw.exe'), '-B', remote_driver],
              guest=True, timeout=65)
    except Exception as exc:
        result['errors'].append(str(exc))
    finally:
        for remote, local in ((guest / 'analysis' / output.name, output), (log, log_local)):
            try:
                vmrun(['CopyFileFromGuestToHost', VMX, remote, local], guest=True)
            except Exception as exc:
                result['errors'].append('retrieve: ' + str(exc))
        try:
            if not output.exists() or output.stat().st_size > 128 * 1024:
                raise ValueError('bounded independent decoder report required')
            report = json.loads(output.read_text(encoding='utf8'))
            result['report'] = identity(output)
            result['result'] = {k: report.get(k) for k in
                ('status', 'errors', 'elapsed_seconds', 'total_records', 'retained_subject_records',
                 'process_trace_status', 'close_trace_status')}
            if report.get('selected_records'):
                row = report['selected_records']
                expected = guest / 'analysis' / records.name
                checked_artifact(row, expected, 64 * 1024)
                vmrun(['CopyFileFromGuestToHost', VMX, expected, records], guest=True)
                result['selected_records'] = transferred(row, records)
        except Exception as exc:
            result['errors'].append('decode/artifact validation: ' + str(exc))
        result['implementations_unchanged'] = before == [identity(p) for p in modules]
        result['inputs_unchanged'] = (sid, eid) == (identity(source_path), identity(etl_path))
        with receipt.open('x', encoding='utf8') as f:
            json.dump(result, f, indent=2)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--label', required=True)
    p.add_argument('--source-label', required=True)
    p.add_argument('--diagnostic-only', action='store_true')
    a = p.parse_args()
    result = decode(a.label, a.source_label, a.diagnostic_only)
    print(json.dumps({k: v for k, v in result.items() if k not in ('implementations', 'driver')}, indent=2))
    failed = (result['errors'] or result.get('result', {}).get('errors')
              or not result['implementations_unchanged'] or not result['inputs_unchanged'])
    raise SystemExit(1 if failed else 0)
