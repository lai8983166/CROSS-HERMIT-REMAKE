"""Deploy the fixed transfer packages inside the dedicated guest, once."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import zipfile


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def extract(package, target, expected, limit):
    if package.stat().st_size != expected['bytes'] or digest(package) != expected['sha256']:
        raise ValueError('unaltered declared transfer package')
    with zipfile.ZipFile(package) as archive:
        rows = archive.infolist()
        if sum(r.file_size for r in rows) > limit or len(rows) > 12000:
            raise ValueError('bounded deployment')
        names = set()
        for row in rows:
            name = PurePosixPath(row.filename)
            if name.is_absolute() or '..' in name.parts or '\\' in row.filename or ':' in row.filename:
                raise ValueError('relative owned archive entries only')
            key = row.filename.lower()
            if key in names:
                raise ValueError('no duplicate/case-colliding deployment entries')
            names.add(key)
            if not (target / row.filename).resolve().is_relative_to(target.resolve()):
                raise ValueError('owned extraction root')
        archive.extractall(target)
    return len(rows)


def main():
    base = Path('C:/ChaomofaWorker')
    status = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
        '[pscustomobject]@{name=$env:COMPUTERNAME;manufacturer=(Get-CimInstance Win32_ComputerSystem).Manufacturer;uuid=(Get-CimInstance Win32_ComputerSystemProduct).UUID}|ConvertTo-Json -Compress'],
        check=True, capture_output=True, text=True, timeout=20)
    machine = json.loads(status.stdout)
    if machine['name'] != 'CHAOMOFA-WORKER' or 'VMware' not in machine['manufacturer']:
        raise ValueError('deployment is guest-only')
    manifest = json.loads((base / 'transfer-manifest.json').read_bytes())
    if machine['uuid'].lower() != manifest['guest_uuid'].lower():
        raise ValueError('this transfer belongs to another guest')
    project = base / 'project'
    if project.exists():
        raise ValueError('new dedicated guest project required')
    if shutil.disk_usage(base).free < 6 * 1024**3:
        raise ValueError('guest deployment space reserve')
    report = dict(accepted=False, machine=machine, archives=manifest['archives'])
    project.mkdir()
    report['asset_files'] = extract(base / 'game-assets.zip', project, manifest['archives']['assets'], 2*1024**3)
    installed = project / 'CROSS HERMIT/CROSS HERMIT'
    private = project / '.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT'
    shutil.copytree(installed, private)  # Distinct file identities; no hardlinks.
    report['source_files'] = extract(base / 'project-sources.zip', project, manifest['archives']['sources'], 32*1024**2)
    report['wheel_files'] = extract(base / 'guest-wheels.zip', base / 'wheels', manifest['archives']['wheels'], 64*1024**2)
    result = subprocess.run([str(base / 'Python/python.exe'), '-m', 'pip', 'install', '--no-cache-dir',
        '--no-index', '--find-links', str(base / 'wheels'), '-r', str(base / 'guest-requirements.txt')],
        capture_output=True, timeout=180)
    report['pip_exit'] = result.returncode
    report['pip_output'] = (result.stdout + result.stderr).decode('utf8', errors='replace')[-6000:]
    (base / 'deployment-v1.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    if result.returncode:
        raise RuntimeError('guest dependencies failed; preserved bounded installation report')


if __name__ == '__main__':
    main()
