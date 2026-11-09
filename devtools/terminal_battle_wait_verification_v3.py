"""Complete battle verification with explicitly expanded offline capacity only."""
import ast
import inspect
import textwrap
from devtools import terminal_battle_wait_verification_v2 as v2
from devtools.terminal_battle_wait_verification_v2 import *
from devtools import terminal_battle_wait_etl_v2 as etl

V2_SHA='81bdbd01c9e782653d9d4ebc017f94185dddf4a4ca0b730f472fbf6235638043'
validate_records=clone(v1.validate_records,etl=etl)
verify_receipt=clone(v1.verify_receipt,etl=etl)
pair_snapshots=clone(v2.pair_snapshots,validate_records=validate_records)
verify=clone(v2.verify,verify_receipt=verify_receipt,pair_snapshots=pair_snapshots)


def make_decoder():
    need(hashlib.sha256(Path(v2.__file__).read_bytes()).hexdigest()==V2_SHA,'fixed complete v2 verification source')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v2.decode_source)));counts=dict(paths=0,identities=0,message=0)
    class CapacityOnly(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                if node.targets[0].id=='paths':
                    need(isinstance(node.value,ast.List)and len(node.value.elts)==6,'six original verifier dependencies')
                    node.value.elts.extend(ast.parse('[Path(v2.__file__),Path(etl.parent.__file__)]',mode='eval').body.elts)
                    counts['paths']+=1
                elif node.targets[0].id=='identities':
                    counts['identities']+=1
                    return [node,*ast.parse("need(identities[6]['sha256']==V2_SHA and identities[7]['sha256']==etl.PARENT_SHA,'fixed v2 verifier and original reader dependencies')").body]
            return self.generic_visit(node)
        def visit_Constant(self,node):
            if node.value=='all selected records within 512 KiB gzip cap; never truncate':
                node.value='all selected records within explicit 2 MiB offline gzip cap; never truncate';counts['message']+=1
            return node
    tree=CapacityOnly().visit(tree);need(counts==dict(paths=1,identities=1,message=1),'only explicit capacity/dependency substitutions')
    ast.fix_missing_locations(tree)
    namespace=dict(v2.__dict__,__file__=__file__,v2=v2,etl=etl,verify=verify,V2_SHA=V2_SHA)
    exec(compile(tree,__file__,'exec'),namespace);return namespace['decode_source']


decode_source=make_decoder()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--source-sha',required=True)
    p.add_argument('--etl',type=Path,required=True);p.add_argument('--etl-sha',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--diagnostic-only',action='store_true')
    p.add_argument('--school-source',type=Path)
    a=p.parse_args();r=decode_source(a.source,a.source_sha,a.etl,a.etl_sha,a.out,a.diagnostic_only,a.school_source)
    print(json.dumps(dict(status=r['status'],errors=r['errors'],accepted=False)))
    raise SystemExit(0 if r['status']=='wait_window_observed'else 2 if r['status'].startswith('diagnostic_')else 1)
