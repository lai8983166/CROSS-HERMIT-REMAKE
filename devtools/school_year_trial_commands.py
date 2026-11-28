"""Regenerate or check the portable October command tape against the accepted v31 save."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

PARENT_SHA = '3c1eee1843f5835493569835514268d4cb81a6dcc8dad69d3c393d592eb9d82e'
OUTPUT = Path(__file__).resolve().parents[1]/'prototype/data/school_year_october_commands.bin'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('parent', type=Path)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    raw = args.parent.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PARENT_SHA:
        parser.error('The selected save does not match the accepted October v31 campaign.')
    commands = json.loads(raw)['commands']
    tape = json.dumps(commands, ensure_ascii=False, separators=(',', ':')).encode()
    if args.write:
        OUTPUT.write_bytes(gzip.compress(tape, compresslevel=9, mtime=0))
    if gzip.decompress(OUTPUT.read_bytes()) != tape:
        raise ValueError('The playable October command tape differs from the accepted save.')
    print(f'{len(commands)} commands, {len(tape)} bytes, opening v31.')


if __name__ == '__main__':
    main()
