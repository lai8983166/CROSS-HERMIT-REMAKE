"""New precise input-timing verification; frozen v1 preflight remains immutable.

Original coarse wall timestamps remain evidence. Ordering against kernel ETW
uses independent PreciseFILETIME samples around each actual unchanged packet.
"""
import struct
import ast
import inspect
import textwrap
from devtools import terminal_battle_wait_verification as v1
from devtools.terminal_battle_wait_verification import *
from devtools.terminal_scene_resources import clone

V1_SHA='08bf42629930144582c8bfbd369f872e01c8e5704c7d0e48019329ac7b9d532b'


def trace_boundary(ledger,lo,hi,rows,source):
    initial=ledger['initial_unpaired_exits'];final=ledger['final_unpaired_entry']
    if initial and hi<rows[initial[0]]['ns']:return 'initial_partial'
    if final is not None and rows[final]['ns']<lo:return 'final_partial'
    # An already-running syscall at trace enable need not emit either syscall
    # event. Only the all-CSwitch prefix before the first actual syscall entry
    # can explain this boundary; no interior omission receives this exception.
    first=next((i for i,r in enumerate(rows)if r['opcode']in(51,52)),None)
    if first is None or rows[first]['opcode']!=51:return None
    if not source['capture_interval']['begin_ns']<=lo<=hi<rows[first]['ns']:return None
    prefix=rows[:first]
    if not prefix or any(r['opcode']!=36 for r in prefix):return None
    tid=source['subject']['tid']
    intervals=[(a,b)for a,b in zip(prefix,prefix[1:])if
        a['data']['OldThreadId']==tid and b['data']['NewThreadId']==tid and a['ns']<lo<=hi<b['ns']]
    return 'initial_before_first_recorded_syscall'if len(intervals)==1 else None


def make_pairer():
    need(hashlib.sha256(Path(v1.__file__).read_bytes()).hexdigest()==V1_SHA,'fixed independent wait pairing implementation')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v1.pair_snapshots)));changed=0
    class BoundaryOnly(ast.NodeTransformer):
        def visit_Assign(self,node):
            nonlocal changed
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id=='boundary':
                node.value=ast.parse('trace_boundary(ledger,lo,hi,rows,source)',mode='eval').body;changed+=1
            return node
    tree=BoundaryOnly().visit(tree);need(changed==1,'one explicit trace-boundary classification only')
    ast.fix_missing_locations(tree);namespace=dict(v1.__dict__,trace_boundary=trace_boundary)
    exec(compile(tree,v1.__file__,'exec'),namespace);return namespace['pair_snapshots']


pair_snapshots=make_pairer()


def verify_precise_submissions(source,action):
    rows=source['precise_input_submissions']
    need(2<=len(rows)<=16,'bounded complete precise submission ledger')
    previous=None
    for row in rows:
        raw=bytes.fromhex(row['packet_hex'])
        need(len(raw)in(28,40),'actual x86/x64 INPUT size')
        offset=4 if len(raw)==28 else 8
        need(struct.unpack_from('<I',raw)[0]==row['type']==0 and
             struct.unpack_from('<I',raw,offset+12)[0]==row['flags'],
             'actual original mouse packet type and flags')
        need(row['error']is None and row['result']==1 and
             type(row['begin_ns'])is int and type(row['end_ns'])is int and 0<row['begin_ns']<=row['end_ns'],
             'successful actual submission with precise bracketing')
        if previous is not None:need(previous<=row['begin_ns'],'ordered original submissions')
        previous=row['end_ns']
    downs=[r for r in rows if r['flags']==2];ups=[r for r in rows if r['flags']==4]
    need(len(downs)==len(ups)==1 and rows[-2:]==[downs[0],ups[0]],'single actual final down/up without retry')
    need(all(r['flags']in(1,0xC001) for r in rows[:-2]),'only original movement before down')
    need(source['start_trigger']=='second_left_button_down_query' and
         source['start_trigger_ns']<=source['capture_interval']['begin_ns']<=downs[0]['begin_ns'] and
         downs[0]['end_ns']<ups[0]['begin_ns'],'trace begun before actual precise down/up intervals')
    need(action['down_result']==downs[0]['result'] and action['up_results']==[ups[0]['result']] and
         len(action['moves'])==len(rows)-2 and all(m['submitted']==r['result'] for m,r in zip(action['moves'],rows[:-2])),
         'same complete original action submission results')
    for i,row in enumerate(rows):
        raw=bytes.fromhex(row['packet_hex']);offset=4 if len(raw)==28 else 8
        dx,dy,data,flags,timestamp=struct.unpack_from('<iiIII',raw,offset)
        need(data==timestamp==0,'unchanged mouse data and event timestamp')
        if i<len(rows)-2:
            move=action['moves'][i]
            expected=move['normalized']if 'normalized'in move else move['delta']
            need([dx,dy]==expected and flags==move.get('flags',1),'exact submitted original movement')
        else:need(dx==dy==0,'button packet does not add movement')
        extra=offset+(24 if len(raw)==40 else 20)
        need(not any(raw[extra:]),'original zero extra input information')
    return dict(clock='GetSystemTimePreciseAsFileTime',down=downs[0],up=ups[0],
                original_coarse_timestamps_modified=False)


def verify_input_reference(source,school_path,image):
    if source['phase']=='startup_preflight':return dict(input_required=False,input_transition_claimed=False)
    school=input_verifier();expected=source['school_source_reference'];path=Path(school_path)
    actual=etw.identity(path);need(all(actual[k]==expected[k] for k in ('bytes','sha256')),'exact once-retained full school source')
    need(0<actual['bytes']<=24*1024*1024,'bounded compressed school history')
    with gzip.open(path,'rb') as f:raw=f.read(192*1024*1024+1)
    need(len(raw)<=192*1024*1024,'bounded expanded school history')
    report=json.loads(raw);reference=source['input_receipt'];index=reference['object_path']
    need(index[:2]==['probe','battle_inputs'] and len(index)==3 and type(index[2])is int and index[2]>=0,
         'exact original battle action object path')
    need(all(reference['source'][k]==actual[k] for k in ('bytes','sha256')),'same referenced input source')
    record=report['probe']['battle_inputs'][index[2]]
    raw_record=json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    canonical=reference['canonical']
    need(len(raw_record)==canonical['bytes'] and hashlib.sha256(raw_record).hexdigest()==canonical['sha256'],
         'exact original action canonical bytes')
    need(canonical['encoding']=='UTF-8 JSON sort_keys=True,separators=(comma,colon),ensure_ascii=False', 'explicit canonical encoding')
    need(record['stage']=='confirmation' and record['error'] is None and reference['error'] is None,
         'one successful original retreat confirmation')
    action=record['action'];down=action['down_wall_time_ns'];up=action['up_wall_time_ns']
    need((reference['down_wall_time_ns'],reference['up_wall_time_ns'])==(down,up)
         and reference['released'] is action['released'] is True,'actual original mouse release receipt')
    precise=verify_precise_submissions(source,action)
    need(down<up,'original coarse-clock action timestamps remain ordered')
    probe=report['probe'];ready=report['lifecycle']['ready'];sub=source['subject']
    need(probe['pid']==sub['pid'] and probe['main']==sub['main'] and source['lifecycle']==report['lifecycle'],
         'same original whole-school lifetime')
    isolation=school.verify_input_isolation(report['input_isolation'])
    viewed,focus=school.guest_focus_view(report,isolation,sub['pid'],ready['window']['hwnd'])
    probe=viewed['probe'];receipt=probe['battle_inputs'][index[2]]
    workers={(w['pointer'],w['thread_id']):w for w in probe['workers']}
    result=school.verify_mouse_action(receipt,'retreat_confirmation',probe,image,ready['game']['pointer'],
        ready['window']['hwnd'],workers,check_disk=False)
    need(result['input_edges_observed'] is True and (result['node'],result['thread_id'])==(sub['node'],sub['tid']),
         'same battle original press/held/release edge proven')
    return dict(input_required=True,source=actual,canonical=canonical,object_path=index,
        actual_input_edges_verified=True,down_ns=down,up_ns=up,precise_submissions=precise,
        native_result_inferred_from_input=False,full_school_history_independently_replayed=False)


verify=clone(v1.verify,verify_input_reference=verify_input_reference,pair_snapshots=pair_snapshots)


def decode_source(source_path,source_sha,etl_path,etl_sha,out,diagnostic_only=False,school_path=None):
    begun=time.monotonic();qualification=etw.qualify()
    source_path=Path(source_path).resolve();etl_path=Path(etl_path).resolve();out=Path(out).resolve()
    records_path=out.with_suffix('.records.json.gz')
    need(out.parent==ROOT/'analysis' and out.suffix=='.json' and not out.exists() and not records_path.exists(),
         'fresh bounded guest offline outputs')
    paths=[Path(v1.__file__),Path(etl.__file__),Path(original.__file__),Path(etw.__file__),
           ROOT/'devtools/terminal_school_handoff_verification.py',Path(__file__)]
    identities=[etw.identity(p) for p in paths]
    result=dict(kind='battle_wait_result_window_decode',status='blocked',phase=None,accepted=False,
        long_capture_preflight_passed=False,diagnostic_only=diagnostic_only,new_native_capture=False,
        fullABI=False,fullstate=False,PTDcleanup=False,full_instruction_trace=False,
        full_resource_lifetime_proved=False,result_consumption_proved=False,
        qualification=qualification,implementations=identities,trace_limits=etl.LIMITS,errors=[])
    selected=[]
    try:
        need(identities[0]['sha256']==V1_SHA,'frozen independent window verifier')
        need(identities[2]['sha256']==ORIGINAL_SHA and identities[3]['sha256']==etl.FROZEN_READER_SHA
             and identities[4]['sha256']==INPUT_VERIFIER_SHA,'exact frozen verification dependencies')
        need(0<source_path.stat().st_size<=etl.SOURCE_GZIP_LIMIT and 0<etl_path.stat().st_size<etl.ETL_LIMIT,
             'bounded original source and full ETL files')
        result['source']=etw.identity(source_path);result['ETL']=etw.identity(etl_path)
        need(result['source']['sha256']==source_sha and result['ETL']['sha256']==etl_sha,'explicit original source/ETL SHA')
        with gzip.open(source_path,'rb') as f:raw=f.read(etl.SOURCE_EXPANDED_LIMIT+1)
        need(len(raw)<=etl.SOURCE_EXPANDED_LIMIT,'bounded complete expanded window source')
        source=json.loads(raw);result['phase']=source['phase']
        result['source_cleanup']=source_contract(source,result['ETL'],diagnostic_only)
        result['window_implementations']=producer_identities(source)
        def consume(rows):
            selected.extend(rows)
            return dict(scope='raw selected original target records; no inferred result or helper fixture')
        etl.decode_etl(etl_path,source,result,begun+etl.DECODE_SECONDS,consume)
        artifact=dict(schema_version=1,source=result['source'],ETL=result['ETL'],subject=source['subject'],
            phase=source['phase'],scope=result['retained_sequence_scope'],records=selected)
        packed=gzip.compress(json.dumps(artifact,separators=(',',':')).encode(),mtime=0)
        need(len(packed)<=etl.SELECTED_GZIP_LIMIT,'all selected records within 512 KiB gzip cap; never truncate')
        with records_path.open('xb') as f:f.write(packed)
        result['selected_records']=etw.identity(records_path)
        if source['phase']=='battle_retreat' and school_path is None:
            school_path=Path(source['school_source_reference']['path'])
        result['analysis']=verify(source,selected,result,(ROOT/'analysis/hermit_game.exe').read_bytes(),
            Path(source['kernel_wait_export']['module']['path']).read_bytes(),
            lambda row:Path(row['module_path']).read_bytes(),diagnostic_only,school_path)
        need(etw.identity(source_path)==result['source'] and etw.identity(etl_path)==result['ETL'],'raw source files remained unchanged')
        need(producer_identities(source)==result['window_implementations'],'window implementation identity remained unchanged')
        current=all(source['input_isolation'][k]==qualification[k] for k in
                    ('current_guest_uuid','current_guest_boot_utc','current_guest_resources'))
        result['same_current_guest_boot_and_resources']=current
        result['long_capture_preflight_passed']=(source['phase']=='startup_preflight'
            and result['analysis']['distinct_successful_waits']>=3 and current)
        result['status']=('diagnostic_wait_window_observed_cleanup_unproven' if diagnostic_only
            and not result['source_cleanup']['strict_source_cleanup_verified'] else
            'diagnostic_wait_window_observed' if diagnostic_only else 'wait_window_observed')
    except Exception as exc:
        result['errors'].append(repr(exc));result['long_capture_preflight_passed']=False
    finally:
        result['elapsed_seconds']=time.monotonic()-begun
        result['implementations_after']=[etw.identity(p) for p in paths]
        if result['implementations_after']!=identities:
            result['errors'].append('decoder or dependency implementation changed');result['status']='blocked'
        if result['elapsed_seconds']>etl.DECODE_SECONDS:
            result['errors'].append('bounded offline decode deadline exceeded');result['status']='blocked'
        if result['errors']:result['long_capture_preflight_passed']=False
        raw=json.dumps(result,ensure_ascii=False,indent=2).encode()
        need(len(raw)<=512*1024,'bounded 512 KiB result summary; full raw records stored separately')
        with out.open('xb') as f:f.write(raw+b'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--source-sha',required=True)
    p.add_argument('--etl',type=Path,required=True);p.add_argument('--etl-sha',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--diagnostic-only',action='store_true')
    p.add_argument('--school-source',type=Path)
    a=p.parse_args();r=decode_source(a.source,a.source_sha,a.etl,a.etl_sha,a.out,a.diagnostic_only,a.school_source)
    print(json.dumps(dict(status=r['status'],errors=r['errors'],accepted=False,
        long_capture_preflight_passed=r['long_capture_preflight_passed'])))
    raise SystemExit(0 if r['status']=='wait_window_observed' else 2 if r['status'].startswith('diagnostic_') else 1)
