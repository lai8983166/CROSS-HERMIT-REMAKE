"""Reuse the exact microprobe with normal TCG blocks; frozen baseline untouched."""
import argparse
from pathlib import Path
from devtools import terminal_cr2_microprobe as probe
from devtools.terminal_cr2_normal_vm import VM


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in ('binary', 'firmware', 'output'):
        parser.add_argument('--' + key, type=Path, required=True)
    parser.add_argument('--ledger', action='store_true')
    probe.VM = VM
    raise SystemExit(not probe.run(parser.parse_args()))
