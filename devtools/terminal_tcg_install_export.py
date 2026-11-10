"""Install the small stopped-state exporter in a disposable pinned build tree."""
import argparse
import hashlib
from pathlib import Path

SCHEMA = '''
##
# @x-query-tcg-state:
#
# Project-local stopped CPU diagnostic. Not a machine checkpoint.
#
# @cpu-index: CPU index
#
# Returns: Versioned JSON string with raw typed/hex CPU fields.
#
# Since: 11.1
##
{ 'command': 'x-query-tcg-state', 'data': { 'cpu-index': 'int' },
  'returns': 'str' }
'''

def install(tree, implementation):
    schema = tree / 'qapi/misc-i386.json'
    meson = tree / 'target/i386/meson.build'
    if 'x-query-tcg-state' in schema.read_text():
        raise ValueError('already installed')
    schema.write_text(schema.read_text() + SCHEMA)
    content = meson.read_text()
    anchor = "  'monitor.c',\n"
    if content.count(anchor) != 1:
        raise ValueError('unexpected meson source')
    meson.write_text(content.replace(anchor, anchor + "  'terminal-state.c',\n"))
    data = implementation.read_bytes()
    (tree / 'target/i386/terminal-state.c').write_bytes(data)
    print('export source SHA256=' + hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('tree', type=Path)
    p.add_argument('implementation', type=Path)
    args = p.parse_args()
    install(args.tree, args.implementation)
