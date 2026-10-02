#!/usr/bin/env python3
"""Launch through the installed Chinese entry point with the resource directory.

python tools/launch_original.py --check
python tools/launch_original.py
python tools/launch_original.py --direct-game  # Explicit diagnostic alternative.
"""
import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / 'CROSS HERMIT' / 'CROSS HERMIT'
GAME = GAME_DIR / 'CROSS HERMIT.EXE'
CHINESE_LAUNCHER = GAME_DIR / 'CROSS HERMIT CHT.EXE'
REQUIRED = (
    GAME,
    GAME_DIR / 'DATA/SOUND/PLW/COMMON/E_SE04.WAV',
    GAME_DIR / 'DATA/TACTICS/SCRIPT/T0005.BIN',
)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check paths without launching')
    parser.add_argument('--direct-game', action='store_true',
                        help='bypass the installed Chinese launcher for explicit diagnostics')
    args = parser.parse_args(argv)
    entry = GAME if args.direct_game else CHINESE_LAUNCHER
    missing = [path for path in dict.fromkeys((*REQUIRED, entry)) if not path.is_file()]
    if missing:
        for path in missing:
            print(f'Missing required file: {path}', file=sys.stderr)
        return 2
    print(f'Entry point: {entry}', flush=True)
    print(f'Working directory: {GAME_DIR}', flush=True)
    if args.check:
        return 0
    if sys.platform != 'win32':
        print('Launching the installed original requires Windows.', file=sys.stderr)
        return 2
    try:
        process = subprocess.Popen([str(entry)], cwd=str(GAME_DIR))
    except OSError as error:
        print(f'Launch failed: {error}', file=sys.stderr)
        return 2
    print(f'Launcher PID: {process.pid} (the original may create a child process)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
