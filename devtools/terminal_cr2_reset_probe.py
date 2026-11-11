"""Exercise reset poison without the baseline VM's intentional no-reboot exit."""
import argparse
from pathlib import Path
from devtools import terminal_cr2_rejection_probe as probe
from devtools.terminal_cr2_reset_vm import VM

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in ('binary', 'firmware', 'output'):
        parser.add_argument('--' + key, type=Path, required=True)
    args = parser.parse_args()
    args.mode = 'reset'
    probe.VM = VM
    raise SystemExit(not probe.run(args))
