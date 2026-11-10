"""Correct the first build's QAPI schema before restarting compilation."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
tree = Path(sys.argv[1])
schema = tree / 'qapi/misc-i386.json'
text = schema.read_text().replace('diagnostic. Not a machine', 'diagnostic.  Not a machine')
text = text.replace("{ 'command': 'x-query-tcg-state',", """##
# @TcgStateJson:
#
# Project-local diagnostic state.
#
# @state: Versioned JSON CPU data, not a machine checkpoint.
#
# Since: 11.1
##
{ 'struct': 'TcgStateJson', 'data': { 'state': 'str' } }

{ 'command': 'x-query-tcg-state',""")
text = text.replace("'returns': 'str' }", "'returns': 'TcgStateJson' }")
# Move the struct's documentation before the command's documentation.
start = text.index('##\n# @x-query-tcg-state:')
struct_start = text.index('##\n# @TcgStateJson:')
command_start = text.index("{ 'command': 'x-query-tcg-state',")
text = text[:start] + text[struct_start:command_start] + text[start:struct_start] + text[command_start:]
schema.write_text(text)
code = (root/'devtools/terminal_tcg_state_export.c').read_text()
code = code.replace('char *qmp_x_query_tcg_state', 'TcgStateJson *qmp_x_query_tcg_state')
code = code.replace('    GString *s;', '    GString *s;\n    TcgStateJson *result;')
code = code.replace('    return g_string_free(s, false);',
                    '    result = g_new0(TcgStateJson, 1);\n    result->state = g_string_free(s, false);\n    return result;')
(tree/'target/i386/terminal-state.c').write_text(code)
(root/'devtools/terminal_tcg_state_export_v2.c').write_text(code)
