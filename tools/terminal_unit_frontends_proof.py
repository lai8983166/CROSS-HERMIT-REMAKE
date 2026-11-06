"""Authenticate a bounded source, replay it, then verify a new native lifetime."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback

from tools import terminal_unit_frontends_corpus as corpus
from tools import terminal_unit_frontends_emulation as source
from tools import terminal_unit_frontends_delta as delta
from tools.terminal_unit_frontends_verification import verify_case,need


def authenticate_source(prefix):
    prefix=Path(prefix)
    process_path=Path(str(prefix)+'.process.json')
    data=json.loads(process_path.read_text(encoding='utf8'))
    need(data['source_execution_complete'] and data['implementation_unchanged'],
         'source process completed with exact loaded implementation files')
    required={'tools/terminal_unit_frontends_'+name+'.py' for name in
              ('corpus','emulation','delta','trace','records','images','minimap')}
    need(required<=data['implementation_start'].keys()
         and all(data['implementation_end'].get(k)==v for k,v in data['implementation_start'].items()),
         'complete principal source implementations and matching start/end identities')
    need(data['fixed_base']==corpus.fixed_base()[0],'source process binds the exact fixed predecessor')
    for key,identity in data['implementation_end'].items():
        need(corpus.identity(corpus.ROOT/key)==identity,'actual exact source implementation '+key)
    expected={(Path(str(prefix)+suffix)).relative_to(corpus.ROOT).as_posix()
              for suffix in ('.chunks.zip','.delta.jsonl.gz')}
    need(len(data['artifacts'])==2 and {r['path'] for r in data['artifacts']}==expected,
         'exact two source artifacts actually decoded from this prefix')
    for identity in data['artifacts']:
        need(corpus.identity(corpus.ROOT/identity['path'])==identity,'complete actual source artifact digest')
    cases=source.previous.overlay.parent.corpus()
    need(data['case'] in cases,'fixed original source case')
    index=cases.index(data['case'])
    helpers={}
    for kind,suffix,name in (('CRT','crt','terminal_unit_frontends_crt_platform.cs'),
                            ('GPU','gpu','terminal_unit_frontends_d3d8_platform.cs')):
        build=data['helper_build'][kind]
        source_path='tools/'+name
        binary=corpus.ROOT/'.venv-audit'/(prefix.name+'-'+str(index)+'-'+suffix+'.exe')
        source_identity=corpus.identity(corpus.ROOT/source_path)
        binary_identity=corpus.identity(binary)
        need(Path(build['source']).as_posix()==source_path and build['source_sha256']==source_identity['sha256']
             and build['helper_sha256']==binary_identity['sha256'] and build['machine']==0x14C,
             'actual retained source helper CS and executable identities '+kind)
        helpers[kind]=dict(source=source_identity,executable=binary_identity,machine=build['machine'])
    data['authenticated_helpers']=helpers
    return data,corpus.identity(process_path)


def compare_fresh(row,other):
    """Compare full initial/forward/final state and every transaction digest."""
    left=row['unit_frontends']['execution'];right=other['unit_frontends']['execution']
    for key in ('initial_CPU','initial_memory','initial_regions','initial_mutable',
                'initial_memory_digest','final_CPU','final_memory_digest','final_trace'):
        need(delta.exact(left[key],right[key]),'fresh complete original '+key)
    need(left['write_PCs']==right['write_PCs'],'fresh all actual original write PCs')
    for key in ('forward_memory','forward_CPU','instructions','writes',
                'code_trace_sha256','write_trace_sha256','frontier'):
        need(delta.exact(row[key],other[key]),'fresh forward whole-state/cumulative '+key)
    need(len(left['transactions'])==len(right['transactions']),'fresh exact transaction count')
    keys=('entry','end','driver','before_CPU','before_memory','before_trace',
          'after_CPU','after_memory','after_trace')
    for index,(a,b) in enumerate(zip(left['transactions'],right['transactions'])):
        for key in keys:
            need(delta.exact(a[key],b[key]),'fresh transaction'+str(index)+' exact '+key)
    return dict(entire_initial_memory=True,entire_forward_memory=True,
                final_memory_reconstructed_and_digest_equal=True,
                all57_CPU_at_all_transactions=True,all_original_cumulative_fields_equal=True,
                every_root_and_continuation_equal=True,transactions=len(left['transactions']))


def resume_source_proof(path,expected_sha,data,process_identity,row,index,prior_orchestrator=None):
    path=Path(path)
    identity=corpus.identity(path)
    need(expected_sha==identity['sha256'],'explicit immutable completed source-proof checkpoint SHA')
    previous=json.loads(path.read_bytes())
    need(previous['case_index']==index and previous['implementation_unchanged'] is True
         and previous['source_process']==process_identity
         and previous['source_artifacts']==data['artifacts']
         and previous['source_helpers']==data['authenticated_helpers'],
         'completed source proof belongs to this exact case/source/helpers')
    required={'tools/terminal_unit_frontends_'+name+'.py' for name in
              ('proof','verification','trace','retries','platform_verification','inputs_verification',
               'other_platform_verification','projection_verification')}
    need(required<=previous['implementation_start'].keys(),
         'completed source proof records every required independent checker')
    need(all(previous['implementation_end'].get(k)==v
             for k,v in previous['implementation_start'].items()),
         'checkpoint checker implementations remained byte-identical throughout source proof')
    archived=None
    for key,want in previous['implementation_end'].items():
        actual=corpus.identity(corpus.ROOT/key)
        if actual==want:continue
        need(key=='tools/terminal_unit_frontends_proof.py' and prior_orchestrator is not None,
             'every source verification implementation remains identical '+key)
        archive_path=Path(prior_orchestrator)
        saved=json.loads(archive_path.read_bytes())
        raw=saved['source_utf8'].encode('utf8')
        need({k:saved[k] for k in ('path','bytes','sha256')}==want
             and len(raw)==want['bytes'] and hashlib.sha256(raw).hexdigest()==want['sha256'],
             'exact historical orchestration bytes retained separately')
        archived=corpus.identity(archive_path)
    proof=previous['source_proof']
    execution=row['unit_frontends']['execution']
    need(proof['transactions']==len(execution['transactions'])
         and proof['final_trace']==execution['final_trace']
         and proof['final_memory']==execution['final_memory_digest']
         and proof['complete_CPU_and_mapped_memory_compared_at_every_transaction'] is True
         and proof['all_cumulative_original_digests_reproduced'] is True
         and proof['canonical_trace_matches_source'] is True
         and proof['original_wait_reached'] is True
         and proof['wait_body_executed'] is False
         and proof['outer_result_consumed'] is False and proof['complete_battle_exit'] is False,
         'fully completed independent source replay with the exact final state and boundary')
    return proof,dict(checkpoint=identity,historical_orchestrator=archived,
                      source_replay_reexecuted=False,all_verification_modules_unchanged=True)


def prove(prefix,index,output,checkpoint=None,checkpoint_sha=None,prior_orchestrator=None):
    output=Path(output)
    need(not output.exists(),'fresh immutable unit frontend proof report')
    report=dict(schema_version=1,accepted=False,case_index=index,
                source_and_fresh_case_verified=False)
    started=time.monotonic()
    try:
        data,identity=authenticate_source(prefix)
        need(data['case']==source.previous.overlay.parent.corpus()[index],'fixed source case identity')
        row=corpus.read_case(prefix,index)
        report.update(source_process=identity,source_artifacts=data['artifacts'],
                      source_helpers=data['authenticated_helpers'],
                      implementation_start=corpus.implementation_files())
        if checkpoint is None:
            print('independent original replay',row['input']['name'],flush=True)
            report['source_proof']=verify_case(row)
        else:
            report['source_proof'],report['resumed_source_proof']=resume_source_proof(
                checkpoint,checkpoint_sha,data,identity,row,index,prior_orchestrator)
            print('authenticated completed source replay',row['input']['name'],flush=True)
        ch,gh,build=source.images.CORE_helpers(output.stem+'-fresh')
        print('new complete native lifetime',row['input']['name'],flush=True)
        other=corpus.compact_case(source.run_case(row['input'],ch,gh))
        report['fresh_comparison']=compare_fresh(row,other)
        # No after-state or native handles are restored in this second pass.
        report['fresh_proof']=verify_case(other)
        report.update(fresh_helper_build=build,fresh_native_creation=other['platform']['creation'],
                      fresh_CRT_cleanup=other['CRT_cleanup'],fresh_GPU_cleanup=other['GPU_cleanup'],
                      source_and_fresh_case_verified=True)
    except Exception as error:
        report.update(error=repr(error),context=getattr(error,'unit_frontends_context',None),
                      traceback=traceback.format_exc(limit=12))
        raise
    finally:
        report.update(duration_seconds=round(time.monotonic()-started,2),
                      implementation_end=corpus.implementation_files())
        report['implementation_unchanged']=all(report['implementation_end'].get(k)==v
                         for k,v in report.get('implementation_start',{}).items())
        if not report.get('implementation_start'):report['implementation_unchanged']=False
        with output.open('x',encoding='utf8',newline='\n') as f:
            json.dump(report,f,separators=(',',':'));f.write('\n')
    need(report['implementation_unchanged'],'actual proof implementations unchanged throughout execution')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--case',type=int,choices=(0,1),required=True)
    parser.add_argument('--out',required=True)
    parser.add_argument('--source-proof-checkpoint')
    parser.add_argument('--source-proof-checkpoint-sha256')
    parser.add_argument('--prior-orchestrator')
    args=parser.parse_args()
    need(bool(args.source_proof_checkpoint)==bool(args.source_proof_checkpoint_sha256),
         'source-proof checkpoint requires its explicit SHA-256')
    result=prove(corpus.ROOT/args.source,args.case,corpus.ROOT/args.out,
                 corpus.ROOT/args.source_proof_checkpoint if args.source_proof_checkpoint else None,
                 args.source_proof_checkpoint_sha256,
                 corpus.ROOT/args.prior_orchestrator if args.prior_orchestrator else None)
    print(json.dumps({k:v for k,v in result.items() if not k.startswith('implementation_')},ensure_ascii=False),flush=True)
