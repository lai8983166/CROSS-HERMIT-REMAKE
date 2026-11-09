"""Read a retained ETL in raw-QPC mode inside the dedicated guest only."""
import ast
import inspect
import textwrap
from devtools import isolated_vm_battle_wait_decode as parent
from devtools.isolated_vm_battle_wait_decode import *

PARENT_SHA='7d2c239222937137134d03c09c42e0ee33cb39a1ce5b1063f2811f3f088c26ae'


def decode(label,source_label):
    if identity(parent.__file__)['sha256']!=PARENT_SHA:raise ValueError('fixed existing offline transport')
    tree=ast.parse(textwrap.dedent(inspect.getsource(parent.decode)));counts=dict(deploy=0,module=0,label=0)
    class RawOnly(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                if node.targets[0].id=='modules':
                    counts['deploy']+=1
                    return [node,*ast.parse("modules.append(ROOT/'devtools/terminal_battle_wait_clock_etl.py')").body]
                if node.targets[0].id=='module':
                    counts['module']+=1;node.value=ast.Constant('devtools.terminal_battle_wait_clock_etl')
            return self.generic_visit(node)
        def visit_keyword(self,node):
            if node.arg=='verification_version':node.value=ast.Constant('raw-clock-only');counts['label']+=1
            return self.generic_visit(node)
    tree=RawOnly().visit(tree)
    if counts!=dict(deploy=1,module=1,label=1):raise ValueError('only explicit raw reader/module report changed')
    ast.fix_missing_locations(tree);scope=dict(parent.__dict__,__file__=__file__)
    exec(compile(tree,__file__,'exec'),scope)
    result=scope['decode'](label,source_label,True,4)
    if identity(parent.__file__)['sha256']!=PARENT_SHA:raise ValueError('original offline transport changed')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--label',required=True);p.add_argument('--source-label',required=True);a=p.parse_args()
    r=decode(a.label,a.source_label)
    print(json.dumps({k:v for k,v in r.items()if k not in ('implementations','driver','guest_inputs')},indent=2))
    raise SystemExit(1 if r['errors']or r.get('result',{}).get('errors')or not r['implementations_unchanged']or not r['inputs_unchanged']else 0)
