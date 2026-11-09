"""Authenticate live wait pairs and preserve an unpaired Thread-End tail.

Thread End is an observed ETW boundary, not proof that the TID ceases execution.
All later raw headers/payloads/CPU transitions remain checked and retained; their
syscalls receive no pairing, return value attribution, or cleanup interpretation.
"""
import ast
import inspect
import textwrap
from devtools import terminal_battle_wait_verification_v3 as v3
from devtools.terminal_battle_wait_verification_v3 import *

V3_SHA='f0971f5d964e9c96c16b61d2f0803d1595ec9e964074bd13ecb25dcf2d5481eb'


def make_lifetime_validator():
    need(hashlib.sha256(Path(v1.__file__).read_bytes()).hexdigest()==V1_SHA,'fixed raw record and CPU verifier')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v1.validate_records)))
    fn=tree.body[0];fn.name='validate_lifetime_records';fn.args.args.append(ast.arg(arg='reported_end_ns'))
    at=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.For));fn.body[at:at]=ast.parse('terminal_tail=[]').body
    counts=dict(entry=0,exit=0,returned=0)
    gate=ast.parse("if row['ns']>reported_end_ns:\n terminal_tail.append(pos)\n continue").body[0]
    class TailOnly(ast.NodeTransformer):
        def visit_Expr(self,node):
            if (isinstance(node.value,ast.Call) and len(node.value.args)==2 and
                isinstance(node.value.args[1],ast.Constant) and node.value.args[1].value==
                    'overlapping target syscalls; no inferred nesting or discarded entry'):
                counts['entry']+=1;return [ast.fix_missing_locations(ast.parse(ast.unparse(gate)).body[0]),node]
            return node
        def visit_If(self,node):
            if ast.dump(node.test)==ast.dump(ast.parse('pending is None',mode='eval').body):
                counts['exit']+=1;return [ast.parse(ast.unparse(gate)).body[0],node]
            return self.generic_visit(node)
        def visit_Return(self,node):
            need(isinstance(node.value,ast.Tuple)and len(node.value.elts)==2,'original raw-record return contract')
            call=node.value.elts[1];need(isinstance(call,ast.Call),'original explicit pairing ledger')
            for kw in call.keywords:
                if kw.arg=='full_global_pairing':kw.value=ast.BoolOp(op=ast.And(),values=[kw.value,ast.UnaryOp(op=ast.Not(),operand=ast.Name(id='terminal_tail',ctx=ast.Load()))])
            call.keywords.extend(ast.parse('dict(reported_thread_end_ns=reported_end_ns,post_end_unpaired_indices=terminal_tail,terminal_tail_syscalls_interpreted=False)',mode='eval').body.keywords)
            counts['returned']+=1;return node
    tree=TailOnly().visit(tree);need(counts==dict(entry=1,exit=1,returned=1),'only post-End syscall pairing and explicit ledger change')
    ast.fix_missing_locations(tree);namespace=dict(v1.__dict__,etl=etl)
    exec(compile(tree,__file__,'exec'),namespace);return namespace['validate_lifetime_records']


validate_lifetime_records=make_lifetime_validator()


def reported_end_boundary(source,rows,receipt):
    # This includes original raw PID/TID/schema/time binding and all-buffer checks.
    v3.verify_receipt(source,rows,receipt)
    bindings=receipt['subject_thread_bindings'];ends=[b for b in bindings if b['opcode']==2]
    need(len(ends)==1,'one actual Thread End, not rundown or guessed worker exit')
    end=ends[0];ns=end['ns'];sub=source['subject'];h=bytes.fromhex(end['header_hex']);raw=bytes.fromhex(end['payload_hex'])
    need(struct.unpack_from('<II',h,8)==(sub['tid'],sub['pid']) and
         struct.unpack_from('<II',raw)==(sub['pid'],sub['tid']), 'raw End header and payload identify same original worker')
    need(all(b['ns']<ns for b in bindings if b['opcode']in(1,3)), 'no subsequent same-TID birth or reuse')
    need(max(x['snapshot_end_ns']for x in source['window_snapshots'])<ns<source['capture_interval']['end_ns'],
         'all observed wait snapshots strictly precede the reported End boundary')
    need(all(r['ns']!=ns for r in rows),'no selected record with ambiguous equal End timestamp')
    exit_row=source['worker_exit']
    need(exit_row['code']==exit_row['wait_status']==0 and exit_row['before_WM_CLOSE']is True
         and exit_row['duplicate_handle_query_only']is True and exit_row['PTDcleanup']is False
         and ns<exit_row['observed_ns']<=source['capture_interval']['end_ns'],
         'actual retained worker exit query after reported End, not a PTD inference')
    return end


def verify(source,rows,receipt,image,kernel_image,module_loader,diagnostic_only=False,school_path=None):
    if source['phase']!='battle_retreat' or not any(b['opcode']==2 for b in receipt['subject_thread_bindings']):
        return v3.verify(source,rows,receipt,image,kernel_image,module_loader,diagnostic_only,school_path)
    end=reported_end_boundary(source,rows,receipt)
    def scoped(sequence,subject,cpu_count):return validate_lifetime_records(sequence,subject,cpu_count,end['ns'])
    pairer=clone(v3.pair_snapshots,validate_records=scoped)
    result=clone(v3.verify,pair_snapshots=pairer)(source,rows,receipt,image,kernel_image,module_loader,diagnostic_only,school_path)
    ledger=result['boundary_ledger'];tail=ledger['post_end_unpaired_indices']
    result['reported_thread_end_boundary']=dict(binding=end,post_end_selected_indices=tail,
        post_end_global_indices=[rows[i]['index']for i in tail],
        all_post_end_record_global_indices=[r['index']for r in rows if r['ns']>end['ns']],
        complete_raw_headers_payloads_CPU_checked=True,post_end_syscalls_paired=False,
        end_event_means_last_CPU_execution=False,terminal_entry_return_inferred=False,
        original_resource_cleanup_proved=False,PTDcleanup=False)
    return result


def make_decoder():
    need(hashlib.sha256(Path(v3.__file__).read_bytes()).hexdigest()==V3_SHA,'fixed complete v3 capacity verifier')
    need(hashlib.sha256(Path(v2.__file__).read_bytes()).hexdigest()==V2_SHA,'fixed complete v2 verification source')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v2.decode_source)));counts=dict(paths=0,identities=0,message=0)
    class TailDependencies(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                if node.targets[0].id=='paths':
                    need(isinstance(node.value,ast.List)and len(node.value.elts)==6,'six original verifier dependencies')
                    node.value.elts.extend(ast.parse('[Path(v2.__file__),Path(etl.parent.__file__),Path(v3.__file__)]',mode='eval').body.elts)
                    counts['paths']+=1
                elif node.targets[0].id=='identities':
                    counts['identities']+=1
                    return [node,*ast.parse("need(identities[6]['sha256']==V2_SHA and identities[7]['sha256']==etl.PARENT_SHA and identities[8]['sha256']==V3_SHA,'fixed complete verification dependencies')").body]
            return self.generic_visit(node)
        def visit_Constant(self,node):
            if node.value=='all selected records within 512 KiB gzip cap; never truncate':
                node.value='all selected records within explicit 2 MiB offline gzip cap; never truncate';counts['message']+=1
            return node
    tree=TailDependencies().visit(tree);need(counts==dict(paths=1,identities=1,message=1),'only explicit dependencies and offline capacity')
    ast.fix_missing_locations(tree)
    namespace=dict(v2.__dict__,__file__=__file__,v2=v2,v3=v3,etl=etl,verify=verify,V2_SHA=V2_SHA,V3_SHA=V3_SHA)
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
