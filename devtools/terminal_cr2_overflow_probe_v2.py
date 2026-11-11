"""Same saturation guest and 15s cap, with bounded buffered QMP transport."""
import argparse
from pathlib import Path
from devtools import terminal_cr2_normal_vm as vm_module
from devtools.terminal_cr2_qmp import QMP
from devtools.terminal_cr2_overflow_probe import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in ('binary', 'firmware', 'output'):
        parser.add_argument('--' + key, type=Path, required=True)
    vm_module.QMP = QMP
    raise SystemExit(not run(parser.parse_args()))
