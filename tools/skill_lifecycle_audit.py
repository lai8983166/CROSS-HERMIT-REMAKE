"""Read-only skill signal audit helpers; executable is a VA-addressed memory dump."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def report_program(archive, block, animation):
    import dxanim_lib as dx

    data = (ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM' / f'{archive}.BIN').read_bytes()
    programs = dx.parse_program_blocks(data)
    print(f'{archive} block={block} animation={animation}')
    tick = 0
    for pc, op in enumerate(programs[block][animation]):
        fields = {key: value for key, value in op.items()
                  if key in ('opcode', 'flags', 'duration_ticks', 'child_animation',
                             'repeat', 'jump', 'terminal')}
        print(f'  linear_tick={tick:3} pc={pc:2} {fields}')
        tick += op.get('duration_ticks', 0)
    timeline = dx.interpret_animation(data, block, animation)
    print('  timeline duration:', timeline['duration_ticks'])
    print('  signals:', timeline['events'], 'root completion updates:',
          timeline['root_completion_ticks'])


def report_samples():
    from unit_action_table import EXE, decode_action, type_for_archive

    image = EXE.read_bytes()
    for archive in ('C1A', 'D0A'):
        for action in (31, 7):
            lookup = decode_action(image, type_for_archive(image, archive), action)
            for direction in lookup['directions']:
                entry = lookup['directions'][direction]
                print(f'action {action} {direction}')
                report_program(archive, entry['block'], entry['animation'])
    for global_id in (2098, 3017, 3027, 2029, 3032):
        report_program('EFCT', global_id // 1000 - 1, global_id % 1000)


def disassemble(start, end):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32

    data = (ROOT / 'analysis/hermit_game.exe').read_bytes()
    for instruction in Cs(CS_ARCH_X86, CS_MODE_32).disasm(
            data[start - 0x400000:end - 0x400000], start):
        print(f'{instruction.address:08x}: {instruction.mnemonic:8} {instruction.op_str}')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--disasm', nargs=2, type=lambda value: int(value, 0))
    parser.add_argument('--samples', action='store_true')
    args = parser.parse_args()
    if args.disasm:
        disassemble(*args.disasm)
    if args.samples:
        report_samples()


if __name__ == '__main__':
    main()
