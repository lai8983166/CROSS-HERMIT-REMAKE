"""Apply only after the previous build has exited; fix per-VP stop evidence."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
tree = Path(sys.argv[1])
code = (root/'devtools/terminal_tcg_state_export_v2.c').read_text()
if code.count('if (!cpu_is_stopped(other))') != 1:
    raise ValueError('old guard identity mismatch')
code = code.replace('if (!cpu_is_stopped(other))', 'if (!other->stopped)')
anchor = '    g_string_append_printf(s, "\\\"cpu\\\":%d,\\\"target_bits\\\":%d,\\\"gpr\\\":[",'
insert = '''    g_string_append(s, "\\\"vp_stopped\\\":[");
    i = 0;
    CPU_FOREACH(other) {
        if (i++) { g_string_append_c(s, ','); }
        g_string_append_printf(s, "{\\\"cpu\\\":%d,\\\"stopped\\\":%s}",
                               other->cpu_index, other->stopped ? "true" : "false");
    }
    g_string_append(s, "],");
'''
if code.count(anchor) != 1:
    raise ValueError('export anchor mismatch')
code = code.replace(anchor, insert + anchor)
(root/'devtools/terminal_tcg_state_export_v3.c').write_text(code)
(tree/'target/i386/terminal-state.c').write_text(code)
