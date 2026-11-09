"""Offline diagnostic for individually provable waits in a rejected full window.

Strict verification is not changed. A snapshot crossing a recorded switch is
preserved as unproven; it never supplies a counted wait. Other snapshots must
meet the exact original single-switch-out rule, including semantic consistency
with every sample of that same pending syscall. This command always exits 2.
"""
import ast
import inspect
import textwrap
from types import SimpleNamespace
from devtools import terminal_battle_wait_verification_v4 as v4
from devtools.terminal_battle_wait_verification_v4 import *


def diagnostic_pairer():
    need(hashlib.sha256(Path(v1.__file__).read_bytes()).hexdigest()==V1_SHA,'fixed strict original pair verifier')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v1.pair_snapshots)));fn=tree.body[0]
    pos=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.For));fn.body[pos:pos]=ast.parse('all_candidates={}').body
    counts=dict(boundary=0,semantic=0,switch=0)
    class DiagnosticOnly(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                if node.targets[0].id=='boundary':
                    node.value=ast.parse('trace_boundary(ledger,lo,hi,rows,source)',mode='eval').body;counts['boundary']+=1
                elif node.targets[0].id=='switches':
                    counts['semantic']+=1
                    before=ast.parse("candidate={k:proof.get(k)for k in ('wait_return_site','wait_frame_bp','caller_frame_bp','result_locals','tail_counter')}\nneed((a,b)not in all_candidates or all_candidates[(a,b)]==candidate,'same pending syscall semantics include unproven switch-spanning samples')\nall_candidates[(a,b)]=candidate").body
                    return before+[node]
            return self.generic_visit(node)
        def visit_Expr(self,node):
            if (isinstance(node.value,ast.Call)and len(node.value.args)==2 and
                isinstance(node.value.args[1],ast.Constant)and node.value.args[1].value==
                    'actual complete snapshot strictly inside one target switch-out interval'):
                counts['switch']+=1
                return ast.parse("if len(off)==0:\n unsupported.append(dict(snapshot_index=index,reason='snapshot not wholly inside one raw switch-out interval; never used to prove a wait',raw_Nt_context_checked=True,containing_syscall_global_indices=[rows[a]['index'],rows[b]['index']],used_to_prove_wait=False))\n continue").body+[node]
            return node
    tree=DiagnosticOnly().visit(tree);need(counts==dict(boundary=1,semantic=1,switch=1),'only explicit diagnostic exclusions and stronger cross-sample semantic check')
    ast.fix_missing_locations(tree);namespace=dict(v1.__dict__,trace_boundary=v2.trace_boundary,validate_records=v3.validate_records)
    exec(compile(tree,__file__,'exec'),namespace);return namespace['pair_snapshots']


def diagnose(source,rows,receipt,image,kernel_image,module_loader,school_path):
    proxy=SimpleNamespace(**dict(v3.__dict__,pair_snapshots=diagnostic_pairer()))
    result=clone(v4.verify,v3=proxy)(source,rows,receipt,image,kernel_image,module_loader,False,school_path)
    unproven=[r for r in result['unsupported_Nt_snapshots']if r.get('raw_Nt_context_checked')]
    result['unsupported_Nt_snapshots']=[r for r in result['unsupported_Nt_snapshots']if not r.get('raw_Nt_context_checked')]
    result.update(diagnostic_only=True,strict_full_window_verified=False,unproven_switch_interval_snapshots=unproven,
        strict_single_switch_out_rule_for_every_counted_wait=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','source-sha','reader-report','reader-sha','records','records-sha','etl','etl-sha','school-source','kernel-image','guest-module-directory','out'):
        p.add_argument('--'+name,required=True)
    a=p.parse_args();out=Path(a.out);need(not out.exists(),'fresh explicit diagnostic output')
    paths=[Path(__file__),Path(v4.__file__),Path(v3.__file__),Path(v2.__file__),Path(v1.__file__),
           Path(etl.__file__),Path(etl.parent.__file__),Path(original.__file__),Path(etw.__file__),ROOT/'devtools/terminal_school_handoff_verification.py']
    before=[etw.identity(q)for q in paths]
    result=dict(status='blocked',accepted=False,strict_full_window_verified=False,new_native_capture=False,errors=[])
    try:
        entries=[]
        for path,digest,limit in ((a.source,a.source_sha,2*1024*1024),(a.reader_report,a.reader_sha,1024*1024),
                                  (a.records,a.records_sha,2*1024*1024),(a.etl,a.etl_sha,64*1024*1024)):
            item=etw.identity(Path(path));need(item['sha256']==digest and 0<item['bytes']<=limit,'exact bounded retained artifact');entries.append(item)
        result.update(source=entries[0],reader_report=entries[1],selected_records=entries[2],ETL=entries[3])
        def packed(path,limit):
            with gzip.open(path,'rb')as f:raw=f.read(limit+1)
            need(len(raw)<=limit,'bounded expanded retained artifact');return json.loads(raw)
        source=packed(a.source,8*1024*1024);artifact=packed(a.records,128*1024*1024);receipt=json.loads(Path(a.reader_report).read_text())
        need(receipt['status']=='blocked' and receipt['errors']==["ValueError('actual complete snapshot strictly inside one target switch-out interval')"],
             'preserve exact strict rejection; no broader diagnostic bypass')
        for key,item in (('source',entries[0]),('selected_records',entries[2]),('ETL',entries[3])):
            need(all(receipt[key][k]==item[k]for k in ('bytes','sha256')),'strict reader artifact binding')
        need(all(artifact['source'][k]==entries[0][k]and artifact['ETL'][k]==entries[3][k]for k in ('bytes','sha256'))
             and artifact['subject']==source['subject'],'raw records bind same native source and subject')
        need(receipt['implementations']==receipt['implementations_after'],'strict reader execution identities remained fixed')
        for item in receipt['implementations']:
            actual=etw.identity(ROOT/'devtools'/Path(item['path']).name)
            need(all(actual[k]==item[k]for k in ('bytes','sha256')),'actual strict reader implementation preserved')
        producer_identities(source)
        directory=Path(a.guest_module_directory)
        def module_loader(item):
            data=(directory/Path(item['module_path']).name).read_bytes()
            need(hashlib.sha256(data).hexdigest()==item['module_sha256'],'exact retained guest module, never host fallback');return data
        result['analysis']=diagnose(source,artifact['records'],receipt,(ROOT/'analysis/hermit_game.exe').read_bytes(),
            Path(a.kernel_image).read_bytes(),module_loader,Path(a.school_source))
        result['status']='diagnostic_individual_waits_with_unproven_switch_snapshots'
    except Exception as exc:result['errors'].append(repr(exc))
    finally:
        result['implementations']=before;result['implementations_after']=[etw.identity(q)for q in paths]
        if before!=result['implementations_after']:result['errors'].append('diagnostic implementation changed');result['status']='blocked'
        raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();need(len(raw)<=512*1024,'bounded complete diagnostic')
        with out.open('xb')as f:f.write(raw)
    print(json.dumps(dict(status=result['status'],errors=result['errors'],accepted=False)))
    return 2 if not result['errors']else 1


if __name__=='__main__':raise SystemExit(main())
