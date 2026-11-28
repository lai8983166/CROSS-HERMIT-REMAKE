"""Preserve the winter command suffix and reconstruct the exact March save."""
import argparse
import hashlib
import json
from pathlib import Path


PARENT_SHA = '05aa0e94a801cb687cab070210b1a105d5febe2dfc3e0a6e513e8fbed6d9aafe'
DELTA = Path(__file__).resolve().parents[1] / 'prototype/sim/tests/school_year_winter_commands.json'


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_exact(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f'Existing file differs: {path}')
        return
    with path.open('xb') as output:
        output.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['extract', 'restore'])
    parser.add_argument('parent', type=Path)
    parser.add_argument('march_save', type=Path)
    parser.add_argument('--delta', type=Path, default=DELTA)
    args = parser.parse_args()
    parent = args.parent.read_bytes()
    if digest(parent) != PARENT_SHA:
        raise ValueError('Expected the authenticated December week two v39 save')
    prefix = json.loads(parent)['commands']
    if args.mode == 'extract':
        source = args.march_save.read_bytes()
        final = json.loads(source)
        commands = final.pop('commands')
        if final['version'] != 40 or commands[:len(prefix)] != prefix:
            raise ValueError('March v40 does not extend this parent')
        delta = dict(parent_sha256=PARENT_SHA, file_sha256=digest(source), header=final,
                     commands=commands[len(prefix):])
        output_path = args.delta
        data = encoded(delta)
    else:
        delta = json.loads(args.delta.read_bytes())
        output_path = args.march_save
    if delta['parent_sha256'] != PARENT_SHA or delta['header']['version'] != 40:
        raise ValueError('Invalid winter command delta')
    restored = encoded(dict(delta['header'], commands=prefix + delta['commands']))
    if digest(restored) != delta['file_sha256']:
        raise ValueError('Reconstructed save digest differs')
    write_exact(output_path, data if args.mode == 'extract' else restored)
    print(f"{len(delta['commands'])} winter commands, March save SHA-256 {digest(restored)}")


if __name__ == '__main__':
    main()
