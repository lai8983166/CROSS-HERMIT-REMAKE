"""Verify locally retained evidence against the versioned size/SHA catalog."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / 'analysis/local-evidence-migration-v1-20261028.json'
EXCLUSIONS = (
    '/analysis/terminal-*-source-*.json.gz',
    '/analysis/terminal-*-diagnostic-*.json.gz',
    '/local-evidence/',
)


def install_exclusions(root):
    root = root.resolve()
    raw = subprocess.check_output(['git', '-C', str(root), 'rev-parse', '--git-path', 'info/exclude'])
    path = Path(raw.decode('utf8').strip())
    if not path.is_absolute():
        path = root / path
    before = path.read_bytes() if path.exists() else b''
    existing = set(before.decode('utf8').splitlines())
    missing = [item for item in EXCLUSIONS if item not in existing]
    if missing:
        path.parent.mkdir(parents=True, exist_ok=True)
        suffix = b'' if not before or before.endswith(b'\n') else b'\n'
        suffix += b'\n# Local generated evidence; see docs/local-evidence.md\n'
        suffix += ('\n'.join(missing) + '\n').encode('utf8')
        with path.open('ab') as stream:
            stream.write(suffix)
        if path.read_bytes() != before + suffix:
            raise ValueError('local exclusions changed concurrently')
    return len(missing)


def verify(manifest, root):
    root = root.resolve()
    data = json.loads(manifest.read_text(encoding='utf8'))
    if data.get('schema_version') != 1 or not isinstance(data.get('files'), list):
        raise ValueError('unsupported local evidence catalog')
    seen = set()
    total = 0
    for row in data['files']:
        name = row['local_path']
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or name in seen:
            raise ValueError('unsafe or duplicate evidence path: ' + name)
        seen.add(name)
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('missing local evidence; restore from the documented backup: ' + name)
        size = row['bytes']
        if type(size) is not int or size < 0 or path.stat().st_size != size:
            raise ValueError('evidence size mismatch: ' + name)
        if not re.fullmatch('[0-9a-f]{64}', row['sha256']):
            raise ValueError('invalid evidence SHA-256: ' + name)
        if not re.fullmatch('[0-9a-f]{40}', row['original_git_blob']):
            raise ValueError('invalid original Git blob ID: ' + name)
        digest = hashlib.sha256()
        blob = hashlib.sha1(('blob ' + str(size) + '\0').encode())
        actual = 0
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                actual += len(block)
                digest.update(block)
                blob.update(block)
        if actual != size or digest.hexdigest() != row['sha256'] or blob.hexdigest() != row['original_git_blob']:
            raise ValueError('evidence content mismatch: ' + name)
        total += actual
    return dict(files=len(seen), bytes=total, all_original_SHA256_and_Git_blob_ids_match=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--install-excludes', action='store_true', help='append local Git exclusions without changing the frozen .gitignore')
    args = parser.parse_args()
    try:
        if args.install_excludes:
            install_exclusions(args.root)
        result = verify(args.manifest, args.root)
    except (KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result))
