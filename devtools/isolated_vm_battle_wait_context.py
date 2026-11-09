"""Short-only guest transport for the complete context collector."""
import ast
import inspect
import textwrap
from devtools import isolated_vm_battle_wait as parent
from devtools.isolated_vm_battle_wait import *

PARENT_SHA='335bc66418b506591e58a5a595b1ae90f5d27e947ee809f2afcc0f7229d54b3f'


def capture(label):
    if identity(parent.__file__)['sha256']!=PARENT_SHA:raise ValueError('fixed original guarded guest transport')
    tree=ast.parse(textwrap.dedent(inspect.getsource(parent.capture)));counts=dict(deploy=0,module=0)
    class ShortOnly(ast.NodeTransformer):
        def visit_Tuple(self,node):
            if all(isinstance(x,ast.Constant)for x in node.elts)and [x.value for x in node.elts]==['terminal_battle_wait_window.py','terminal_battle_wait_window_v2.py','terminal_original_wait_etw.py','terminal_wait_etw_probe.py']:
                node.elts.extend([ast.Constant('terminal_battle_wait_clock.py'),ast.Constant('terminal_battle_wait_clock_armed.py'),ast.Constant('terminal_battle_wait_clock_settled.py'),ast.Constant('terminal_battle_wait_context.py')]);counts['deploy']+=1
            return self.generic_visit(node)
        def visit_Constant(self,node):
            if node.value=='devtools.terminal_battle_wait_window_v2':node.value='devtools.terminal_battle_wait_context';counts['module']+=1
            return node
    tree=ShortOnly().visit(tree)
    if counts!=dict(deploy=1,module=1):raise ValueError('only explicit short collector/deployment adaptation')
    # The short CLI has no phase option. Keep all old transport guards and paths.
    class Args(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id=='args':
                node.value=ast.parse("[module,'--out',str(remote)]",mode='eval').body
            return self.generic_visit(node)
    tree=Args().visit(tree);ast.fix_missing_locations(tree)
    scope=dict(parent.__dict__,__file__=__file__)
    exec(compile(tree,__file__,'exec'),scope)
    result=scope['capture'](label,'startup_preflight')
    if identity(parent.__file__)['sha256']!=PARENT_SHA:raise ValueError('original transport changed')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--label',required=True);a=p.parse_args();r=capture(a.label)
    print(json.dumps({k:v for k,v in r.items()if k not in ('sources','driver')},indent=2))
    observed=r.get('observed',{})
    raise SystemExit(1 if r['errors']or not r['sources_unchanged']or not observed or observed.get('error')or observed.get('lifecycle_error')else 0)
