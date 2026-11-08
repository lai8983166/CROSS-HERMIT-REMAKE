"""Build bounded x86 guest-only probes on F:, without executing them on host."""
import argparse
import json
from pathlib import Path
import subprocess
from devtools.isolated_windows_vm import ROOT, WORKER, environment, identity, require_owned_root


def build(name):
    if name not in ('preflight', 'clock', 'audio'):
        raise ValueError('reviewed guest probe required')
    require_owned_root()
    source = ROOT / ('devtools/isolated_guest_' + name + '.cs')
    target = WORKER / ('guest-' + name + '.exe')
    compiler = Path('C:/Windows/Microsoft.NET/Framework/v4.0.30319/csc.exe')
    before = identity(source)
    flags = ['/nologo', '/platform:x86', '/target:winexe',
             '/r:System.Management.dll', '/r:System.Web.Extensions.dll']
    result = subprocess.run([str(compiler), *flags, '/out:' + str(target), str(source)],
                            env=environment(), cwd=WORKER, capture_output=True, timeout=30)
    if result.returncode:
        raise RuntimeError(result.stdout.decode('mbcs', errors='replace')[:4000])
    if before != identity(source):
        raise RuntimeError('source changed during build')
    report = dict(source=before, compiler=identity(compiler), flags=flags, executable=identity(target),
                  host_executed=False)
    (WORKER / ('guest-' + name + '-build.json')).write_text(json.dumps(report, indent=2), encoding='utf8')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('name', choices=['preflight', 'clock', 'audio'])
    print(json.dumps(build(p.parse_args().name)))
